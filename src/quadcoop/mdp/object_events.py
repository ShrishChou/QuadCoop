"""Object placement and the competence-gated object curriculum.

Curriculum state lives on the env (``env.qc_objects``) so the placement event,
the curriculum term and the evaluation scripts all read the same numbers:

    p_place   probability a placement puts an object in the robot's path
    max_mass  heaviest object (kg) currently allowed in the path

Schedule (in PPO iterations, 1 iteration = 24 env steps):
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
from mjlab.envs.mdp.events import resolve_env_ids
from mjlab.utils.lab_api.math import quat_apply, quat_from_euler_xyz, yaw_quat

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


def place_object_in_path(
    env: ManagerBasedRlEnv,
    env_ids: torch.Tensor | None,
    robot_half_length: float,
    gap_range: tuple[float, float] = (0.1, 1.0),
    lateral_range: tuple[float, float] = (-0.25, 0.25),
    yaw_jitter: float = 0.3,
    park_distance: float = 30.0,
    command_name: str = "twist",
    p_override: float | None = None,
    max_mass_override: float | None = None,
    only: str | None = None,
) -> None:
    """Put at most one eligible object ahead along the commanded direction; park the rest.

    ``p_override`` / ``max_mass_override`` / ``only`` bypass the curriculum (used by
    evaluation, e.g. "always the cube").
    """
    env_ids = resolve_env_ids(env, env_ids)
    n = len(env_ids)
    if n == 0:
        return
    dev = env.device
    st = _state(env)
    p = st["p_place"] if p_override is None else p_override
    max_mass = st["max_mass"] if max_mass_override is None else max_mass_override

    robot: Entity = env.scene["robot"]
    # Root pose from qpos: root_link_pos_w is stale inside reset events.
    q_adr = robot.indexing.free_joint_q_adr
    qpos = robot.data.data.qpos[env_ids]
    root_pos = qpos[:, q_adr[0:3]]
    q_yaw = yaw_quat(qpos[:, q_adr[3:7]])
    robot_yaw = 2.0 * torch.atan2(q_yaw[:, 3], q_yaw[:, 0])

    twist = env.command_manager.get_command(command_name)[env_ids]
    vxy = twist[:, :2]
    moving = torch.linalg.norm(vxy, dim=-1) > 0.1
    angle = torch.where(moving, torch.atan2(vxy[:, 1], vxy[:, 0]), torch.zeros(n, device=dev))

    # Which object (if any) each env gets.
    entities = [env.scene[o.name] for o in OBJECTS]
    masses = torch.stack(
        [env.sim.model.body_mass[env_ids, e.indexing.body_ids[0]] for e in entities], dim=-1
    )  # (n, K)
    eligible = masses <= max_mass + 1e-6
    if only is not None:
        mask = torch.tensor([o.name == only for o in OBJECTS], device=dev)
        eligible = eligible & mask
    score = torch.where(eligible, torch.rand_like(masses), torch.full_like(masses, -1.0))
    choice = score.argmax(dim=-1)
    place = (torch.rand(n, device=dev) < p) & eligible.any(dim=-1)
    choice = torch.where(place, choice, torch.full_like(choice, -1))

    zeros = torch.zeros(n, device=dev)
    lat = torch.empty(n, device=dev).uniform_(*lateral_range)
    gap = torch.empty(n, device=dev).uniform_(*gap_range)
    yaw = robot_yaw + angle + torch.empty(n, device=dev).uniform_(-yaw_jitter, yaw_jitter)
    quat = quat_from_euler_xyz(zeros, zeros, yaw)
    for k, (obj, ent) in enumerate(zip(OBJECTS, entities, strict=True)):
        dist = robot_half_length + obj.half_extent_x + gap
        offset_yaw = torch.stack(
            [dist * torch.cos(angle) - lat * torch.sin(angle),
             dist * torch.sin(angle) + lat * torch.cos(angle),
             zeros], dim=-1)
        in_path = root_pos + quat_apply(q_yaw, offset_yaw)
        parked = root_pos + torch.tensor([park_distance + 3.0 * k, 0.0, 0.0], device=dev)
        pos = torch.where((choice == k).unsqueeze(-1), in_path, parked)
        pos[:, 2] = obj.half_height + 0.005
        state = torch.zeros(n, 13, device=dev)
        state[:, 0:3] = pos
        state[:, 3:7] = quat
        ent.write_root_state_to_sim(state, env_ids)

    if not hasattr(env, "qc_choice"):
        env.qc_choice = torch.full((env.num_envs,), -1, dtype=torch.long, device=dev)  # type: ignore[attr-defined]
    env.qc_choice[env_ids] = choice  # type: ignore[attr-defined]


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
