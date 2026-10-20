"""Object placement for the push episodes, and the object curriculum.

Placement is driven by the command term (``push_command.py``): mjlab resets in the
order  events -> command resample, so only the command term knows the episode's
direction when it places objects.

Curriculum state lives on the env (``env.qc_objects``):

    p_place   probability that a new object is put in the path when the path is clear
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


def place_ahead(env: ManagerBasedRlEnv, ids: torch.Tensor, bearing: torch.Tensor, c, p: float,
                max_mass: float) -> torch.Tensor:
    """Put one eligible object ahead of each robot on body-frame ``bearing`` (with prob. p).

    Every other object of those envs is parked far away. Returns the chosen object index
    per env (-1 = none) and records it in ``env.qc_choice``.
    """
    m = len(ids)
    dev = env.device
    if not hasattr(env, "qc_choice"):
        env.qc_choice = torch.full((env.num_envs,), -1, dtype=torch.long, device=dev)  # type: ignore[attr-defined]
    if m == 0:
        return torch.empty(0, dtype=torch.long, device=dev)

    robot: Entity = env.scene["robot"]
    # Root pose from qpos: always current, also inside reset (derived data is stale there).
    q_adr = robot.indexing.free_joint_q_adr
    qpos = robot.data.data.qpos[ids]
    root_pos = qpos[:, q_adr[0:3]]
    q_yaw = yaw_quat(qpos[:, q_adr[3:7]])
    robot_yaw = 2.0 * torch.atan2(q_yaw[:, 3], q_yaw[:, 0])

    entities = [env.scene[o.name] for o in OBJECTS]
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

    zeros = torch.zeros(m, device=dev)
    lat = torch.empty(m, device=dev).uniform_(*c.lateral_range)
    gap = torch.empty(m, device=dev).uniform_(*c.gap_range)
    yaw = robot_yaw + bearing + torch.empty(m, device=dev).uniform_(-c.yaw_jitter, c.yaw_jitter)
    quat = quat_from_euler_xyz(zeros, zeros, yaw)
    for k, (obj, ent) in enumerate(zip(OBJECTS, entities, strict=True)):
        dist = c.robot_half_length + obj.half_extent_x + gap
        offset = torch.stack(
            [dist * torch.cos(bearing) - lat * torch.sin(bearing),
             dist * torch.sin(bearing) + lat * torch.cos(bearing), zeros], dim=-1)
        in_path = root_pos + quat_apply(q_yaw, offset)
        parked = root_pos + torch.tensor([c.park_distance + 3.0 * k, 0.0, 0.0], device=dev)
        pos = torch.where((choice == k).unsqueeze(-1), in_path, parked)
        pos[:, 2] = obj.half_height + 0.005
        state = torch.zeros(m, 13, device=dev)
        state[:, 0:3] = pos
        state[:, 3:7] = quat
        ent.write_root_state_to_sim(state, ids)
    env.qc_choice[ids] = choice  # type: ignore[attr-defined]
    return choice


def object_is_done(env: ManagerBasedRlEnv, ids: torch.Tensor, bearing: torch.Tensor,
                   behind: float = 0.3, off_line: float = 1.2, too_far: float = 6.0) -> torch.Tensor:
    """True where the env's object is gone from the robot's path: none, passed, off the
    line (slid or rolled aside), or far ahead (rolled away)."""
    dev = env.device
    choice = env.qc_choice[ids]
    robot: Entity = env.scene["robot"]
    q_adr = robot.indexing.free_joint_q_adr
    qpos = robot.data.data.qpos[ids]
    root_pos = qpos[:, q_adr[0:3]]
    q_yaw = yaw_quat(qpos[:, q_adr[3:7]])
    obj_pos = torch.stack([env.scene[o.name].data.root_link_pos_w[ids] for o in OBJECTS], dim=1)
    rel = obj_pos[torch.arange(len(ids), device=dev), choice.clamp(min=0)] - root_pos
    rel[:, 2] = 0.0
    rel_b = quat_apply_inverse(q_yaw, rel)
    u = torch.stack([torch.cos(bearing), torch.sin(bearing)], dim=-1)
    s = (rel_b[:, :2] * u).sum(-1)
    side = (rel_b[:, 0] * u[:, 1] - rel_b[:, 1] * u[:, 0]).abs()
    gone = (s < -behind) | (side > off_line) | (torch.linalg.norm(rel_b[:, :2], dim=-1) > too_far)
    return (choice < 0) | gone


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