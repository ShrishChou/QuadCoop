"""Object placement tied to the velocity command, and the object curriculum.

Why placement lives in the command term (``push_command.py``): mjlab resets in the
order  events -> command resample, so an event that aims an object along "the
command" at reset sees the *previous* episode's command. Here the command term
resamples first and then calls ``place_objects``, which sets the command and the
object together, so the object is always on the line the robot has been told to walk.

Curriculum state lives on the env (``env.qc_objects``):

    p_place   probability a command segment contains an object
    max_mass  heaviest object (kg) currently allowed

Schedule (PPO iterations, 1 iteration = 24 env steps):
    0 .. warmup             plain walking: no objects (p_place = 0)
    warmup .. warmup+ramp   p_place rises linearly to p_max
    after warmup            max_mass starts at mass_start and moves up by mass_step
                            when robots that touched an object in their episode
                            rarely fell and still tracked their command; it moves
                            down if they fall often. At most one change per dwell.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import torch
from mjlab.utils.lab_api.math import quat_apply, quat_apply_inverse, quat_from_euler_xyz, yaw_quat

from quadcoop.robots.objects import OBJECTS

if TYPE_CHECKING:
    from mjlab.entity import Entity
    from mjlab.envs import ManagerBasedRlEnv

STEPS_PER_ITER = 24


def _state(env: ManagerBasedRlEnv, defaults: dict | None = None) -> dict:
    if not hasattr(env, "qc_objects"):
        d = {"p_place": 0.0, "max_mass": 8.0, "ema_fall": 0.0, "ema_err": 0.0,
             "last_change": 0, "n_engaged": 0}
        if defaults:
            d.update(defaults)
        env.qc_objects = d  # type: ignore[attr-defined]
    return env.qc_objects  # type: ignore[attr-defined]


def _set_push_command(term, ids: torch.Tensor, angle: torch.Tensor, speed_range, hold_s) -> None:
    """Walk toward bearing ``angle`` (body frame) at a sampled speed, no turning, for a while."""
    dev = angle.device
    speed = torch.empty(len(ids), device=dev).uniform_(*speed_range)
    term.vel_command_b[ids, 0] = speed * torch.cos(angle)
    term.vel_command_b[ids, 1] = speed * torch.sin(angle)
    term.vel_command_b[ids, 2] = 0.0
    term.is_standing_env[ids] = False
    term.is_heading_env[ids] = False
    term.vel_command_w[ids] = term.vel_command_b[ids]
    term.time_left[ids] = torch.empty(len(ids), device=dev).uniform_(*hold_s)


def place_objects(env: ManagerBasedRlEnv, env_ids: torch.Tensor, term, c, resetting: bool) -> None:
    """Called by the command term after it samples a command for ``env_ids``.

    * Env whose chosen object is still near the robot (and not a reset): keep it, and
      re-aim the command at it so the robot keeps pushing it.
    * Otherwise: with probability p_place put one eligible object ahead on a sampled
      bearing and command the robot to walk along it; else park every object.
    """
    n = len(env_ids)
    if n == 0:
        return
    dev = env.device
    st = _state(env)
    p = st["p_place"] if c.p_override is None else c.p_override
    max_mass = st["max_mass"] if c.max_mass_override is None else c.max_mass_override

    if not hasattr(env, "qc_choice"):
        env.qc_choice = torch.full((env.num_envs,), -1, dtype=torch.long, device=dev)  # type: ignore[attr-defined]

    robot: Entity = env.scene["robot"]
    # Root pose from qpos: derived quantities are stale inside reset.
    q_adr = robot.indexing.free_joint_q_adr
    qpos = robot.data.data.qpos[env_ids]
    root_pos = qpos[:, q_adr[0:3]]
    q_yaw = yaw_quat(qpos[:, q_adr[3:7]])
    robot_yaw = 2.0 * torch.atan2(q_yaw[:, 3], q_yaw[:, 0])

    entities = [env.scene[o.name] for o in OBJECTS]
    K = len(entities)

    # -- envs that are still pushing their object ------------------------------------
    prev = env.qc_choice[env_ids]
    engaged = torch.zeros(n, dtype=torch.bool, device=dev)
    if not resetting:
        obj_pos = torch.stack([e.data.root_link_pos_w[env_ids] for e in entities], dim=1)  # (n,K,3)
        chosen = obj_pos[torch.arange(n, device=dev), prev.clamp(min=0)]
        rel = chosen - root_pos
        rel[:, 2] = 0.0
        engaged = (prev >= 0) & (torch.linalg.norm(rel, dim=-1) < c.engaged_dist)
        if engaged.any():
            rel_b = quat_apply_inverse(q_yaw, rel)
            bearing = torch.atan2(rel_b[:, 1], rel_b[:, 0])
            _set_push_command(term, env_ids[engaged], bearing[engaged], c.speed_range, c.hold_s)

    fresh = ~engaged
    if not fresh.any():
        return
    ids = env_ids[fresh]
    m = len(ids)
    root_pos, q_yaw, robot_yaw = root_pos[fresh], q_yaw[fresh], robot_yaw[fresh]

    # -- which object (if any) -------------------------------------------------------
    masses = torch.stack(
        [env.sim.model.body_mass[ids, e.indexing.body_ids[0]] for e in entities], dim=-1
    )  # (m, K)
    eligible = masses <= max_mass + 1e-6
    if c.only is not None:
        eligible = eligible & torch.tensor([o.name == c.only for o in OBJECTS], device=dev)
    score = torch.where(eligible, torch.rand_like(masses), torch.full_like(masses, -1.0))
    choice = score.argmax(dim=-1)
    place = (torch.rand(m, device=dev) < p) & eligible.any(dim=-1)
    choice = torch.where(place, choice, torch.full_like(choice, -1))

    # -- bearing of the push: mostly straight ahead (the robot's bumper faces forward) --
    side = torch.tensor([torch.pi / 2, -torch.pi / 2, torch.pi], device=dev)
    other = side[torch.randint(0, 3, (m,), device=dev)]
    angle = torch.where(torch.rand(m, device=dev) < c.p_forward, torch.zeros(m, device=dev), other)
    angle = angle + torch.empty(m, device=dev).uniform_(-c.angle_jitter, c.angle_jitter)
    if place.any():
        _set_push_command(term, ids[place], angle[place], c.speed_range, c.hold_s)

    zeros = torch.zeros(m, device=dev)
    lat = torch.empty(m, device=dev).uniform_(*c.lateral_range)
    gap = torch.empty(m, device=dev).uniform_(*c.gap_range)
    yaw = robot_yaw + angle + torch.empty(m, device=dev).uniform_(-c.yaw_jitter, c.yaw_jitter)
    quat = quat_from_euler_xyz(zeros, zeros, yaw)
    for k, (obj, ent) in enumerate(zip(OBJECTS, entities, strict=True)):
        dist = c.robot_half_length + obj.half_extent_x + gap
        offset = torch.stack(
            [dist * torch.cos(angle) - lat * torch.sin(angle),
             dist * torch.sin(angle) + lat * torch.cos(angle), zeros], dim=-1)
        in_path = root_pos + quat_apply(q_yaw, offset)
        parked = root_pos + torch.tensor([c.park_distance + 3.0 * k, 0.0, 0.0], device=dev)
        pos = torch.where((choice == k).unsqueeze(-1), in_path, parked)
        pos[:, 2] = obj.half_height + 0.005
        state = torch.zeros(m, 13, device=dev)
        state[:, 0:3] = pos
        state[:, 3:7] = quat
        ent.write_root_state_to_sim(state, ids)
    env.qc_choice[ids] = choice  # type: ignore[attr-defined]


def object_curriculum(
    env: ManagerBasedRlEnv,
    env_ids: torch.Tensor,
    warmup_iters: int,
    ramp_iters: int,
    p_max: float,
    mass_start: float,
    mass_final: float,
    mass_step: float = 2.0,
    dwell_iters: int = 50,
    advance_fall: float = 0.10,
    advance_err: float = 0.35,
    retreat_fall: float = 0.25,
    min_contact_frac: float = 0.02,
    ema: float = 0.05,
) -> dict[str, torch.Tensor]:
    """Runs at every reset (before the episode stats are cleared)."""
    st = _state(env, {"max_mass": mass_start})
    it = env.common_step_counter / STEPS_PER_ITER
    st["p_place"] = p_max * min(1.0, max(0.0, (it - warmup_iters) / max(ramp_iters, 1)))

    if it >= warmup_iters and isinstance(env_ids, torch.Tensor) and len(env_ids) > 0:
        mm = env.metrics_manager
        steps = mm._step_count[env_ids].float().clamp(min=1)  # noqa: SLF001
        contact = mm._episode_sums["object_contact"][env_ids] / steps  # noqa: SLF001
        err = mm._episode_sums["vel_error_xy"][env_ids] / steps  # noqa: SLF001
        fell = env.termination_manager.terminated[env_ids].float()
        engaged = contact > min_contact_frac
        n_eng = int(engaged.sum())
        if n_eng > 0:
            w = min(1.0, ema * n_eng)  # Weight by how many engaged episodes just ended.
            st["ema_fall"] = (1 - w) * st["ema_fall"] + w * float(fell[engaged].mean())
            st["ema_err"] = (1 - w) * st["ema_err"] + w * float(err[engaged].mean())
            st["n_engaged"] += n_eng
            # Decide at most once per dwell window, and only in a call that brought
            # fresh engaged episodes; each decision consumes the evidence it used.
            if it - st["last_change"] >= dwell_iters and st["n_engaged"] >= 200:
                if st["ema_fall"] < advance_fall and st["ema_err"] < advance_err:
                    st["max_mass"] = min(mass_final, st["max_mass"] + mass_step)
                elif st["ema_fall"] > retreat_fall:
                    st["max_mass"] = max(mass_start, st["max_mass"] - mass_step)
                st["last_change"] = it
                st["n_engaged"] = 0

    return {k: torch.tensor(float(st[k])) for k in ("p_place", "max_mass", "ema_fall", "ema_err")}