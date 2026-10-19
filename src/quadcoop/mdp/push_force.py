"""Sustained horizontal push-resistance force on the robot base.

Adapted from G1-Force-Movement's ``mdp/torso_force_field.py`` (ramp-hold-ramp
wrench as a CommandTerm, linear intensity curriculum). What changes for a
quadruped that must *push objects*:

* **Direction.** With probability ``p_oppose`` the force points against the
  commanded planar velocity (what an object you walk into does), jittered by
  +/-``oppose_jitter_deg``. Otherwise it is a random horizontal direction (a
  partner or a rolling object bumping you). Standing commands always get a
  random direction.
* **Frame.** Direction is sampled in the yaw frame and kept horizontal, so a
  pitched base doesn't tilt the load into the ground. (The G1 torso field rotates
  by the full base quaternion; that is right for a torso payload, wrong here.)
* **Where it acts.** MuJoCo applies ``xfrc_applied`` at the body COM, so the
  moment of a push landing at ``push_point_b`` (the front of the body) is added
  as an explicit torque ``r x F``. A frontal push therefore also tries to pitch
  the robot, as it does in reality.
* **Magnitude** is a fraction of the robot's own weight, so ANYmal C and Spot
  get comparable difficulty: ``|F| ~ U(0, max_frac_of_weight) * m * g``.
* **Privileged only.** ``command`` exposes the applied force (yaw frame) so the
  critic can see it; the actor never does. The deployed walker has to feel it.

Schedule per env: zero gap -> ramp up -> hold -> ramp down -> repeat, with each
phase length sampled, so loads arrive at unpredictable times like real contact.
"""

from __future__ import annotations

import math
import os
from dataclasses import dataclass
from typing import TYPE_CHECKING

import torch
from mjlab.entity import Entity
from mjlab.managers.command_manager import CommandTerm, CommandTermCfg
from mjlab.utils.lab_api.math import quat_apply, yaw_quat

if TYPE_CHECKING:
    from mjlab.envs.manager_based_rl_env import ManagerBasedRlEnv

GRAVITY = 9.81


def push_force_enabled() -> bool:
    """Kill switch: ``QUADCOOP_PUSH_FORCE=0`` trains a plain walker for ablations."""
    return os.environ.get("QUADCOOP_PUSH_FORCE", "1") not in ("0", "false", "False")


class PushForceCommand(CommandTerm):
    cfg: PushForceCommandCfg

    def __init__(self, cfg: PushForceCommandCfg, env: ManagerBasedRlEnv):
        super().__init__(cfg, env)
        self.robot: Entity = env.scene[cfg.entity_name]
        body_ids, _ = self.robot.find_bodies((cfg.body_name,), preserve_order=True)
        self._body_id = int(body_ids[0])

        # Robot mass from the compiled model (sum over this entity's bodies).
        mass = env.sim.mj_model.body_mass[self.robot.indexing.body_ids.cpu().numpy()].sum()
        self.robot_weight_n = float(mass) * GRAVITY

        n, dev = self.num_envs, self.device
        self.push_point_b = torch.tensor(cfg.push_point_b, device=dev).expand(n, 3)
        self.timer = torch.zeros(n, device=dev)
        self.t_gap = torch.zeros(n, device=dev)
        self.t_ramp = torch.ones(n, device=dev)
        self.t_hold = torch.ones(n, device=dev)
        self.target_mag = torch.zeros(n, device=dev)
        # Direction stored as an angle in the yaw frame (0 = robot forward).
        self.dir_angle = torch.zeros(n, device=dev)
        self.applied_force_yaw = torch.zeros(n, 3, device=dev)
        # Episode-mean bookkeeping, so logged metrics aren't a snapshot that
        # happens to land in a zero-force gap.
        self._sum_frac = torch.zeros(n, device=dev)
        self._steps = torch.zeros(n, device=dev)

        self.metrics["force_n"] = torch.zeros(n, device=dev)
        self.metrics["force_frac_weight"] = torch.zeros(n, device=dev)
        self.metrics["curriculum_scale"] = torch.zeros(n, device=dev)

    @property
    def command(self) -> torch.Tensor:
        """Applied force in the yaw frame, in units of robot weight: (N, 3)."""
        return self.applied_force_yaw / self.robot_weight_n

    # -- schedule ----------------------------------------------------------

    def _curriculum_scale(self) -> float:
        start = float(self.cfg.curriculum_start_scale)
        if start >= 1.0:
            return 1.0
        steps = float(getattr(self._env, "common_step_counter", 0))
        progress = min(1.0, steps / max(float(self.cfg.curriculum_env_steps), 1.0))
        return start + (1.0 - start) * progress

    def _uniform(self, n: int, lo_hi: tuple[float, float]) -> torch.Tensor:
        return torch.empty(n, device=self.device).uniform_(lo_hi[0], lo_hi[1])

    def _sample_cycle(self, env_ids: torch.Tensor) -> None:
        n = len(env_ids)
        if n == 0:
            return
        cfg = self.cfg
        self.timer[env_ids] = 0.0
        self.t_gap[env_ids] = self._uniform(n, cfg.gap_s)
        self.t_ramp[env_ids] = self._uniform(n, cfg.ramp_s)
        self.t_hold[env_ids] = self._uniform(n, cfg.hold_s)
        if cfg.fixed_frac is not None:
            self.target_mag[env_ids] = cfg.fixed_frac
        else:
            self.target_mag[env_ids] = self._uniform(n, (0.0, cfg.max_frac_of_weight))

        # Direction: oppose the commanded velocity, or random.
        twist = self._env.command_manager.get_command(cfg.velocity_command_name)
        vel_xy = twist[env_ids, :2]
        moving = torch.linalg.norm(vel_xy, dim=-1) > cfg.moving_threshold
        oppose = moving & (torch.rand(n, device=self.device) < cfg.p_oppose)
        jitter = math.radians(cfg.oppose_jitter_deg)
        opposed_angle = torch.atan2(-vel_xy[:, 1], -vel_xy[:, 0]) + self._uniform(
            n, (-jitter, jitter)
        )
        random_angle = self._uniform(n, (-math.pi, math.pi))
        self.dir_angle[env_ids] = torch.where(oppose, opposed_angle, random_angle)

    def _envelope(self) -> torch.Tensor:
        """0 during the gap, ramps 0->1, holds 1, ramps 1->0."""
        t = self.timer - self.t_gap
        ramp = torch.clamp(self.t_ramp, min=1e-3)
        up = torch.clamp(t / ramp, 0.0, 1.0)
        down = 1.0 - torch.clamp((t - ramp - self.t_hold) / ramp, 0.0, 1.0)
        return torch.where(t < 0.0, torch.zeros_like(t), torch.minimum(up, down))

    # -- CommandTerm hooks ---------------------------------------------------

    def _resample_command(self, env_ids: torch.Tensor) -> None:
        # Called on episode reset (manager resampling is disabled via a huge range).
        self._sum_frac[env_ids] = 0.0
        self._steps[env_ids] = 0.0
        self._sample_cycle(env_ids)

    def _update_command(self) -> None:
        self.timer += self._env.step_dt
        done = self.timer >= self.t_gap + 2.0 * self.t_ramp + self.t_hold
        if done.any():
            self._sample_cycle(done.nonzero(as_tuple=False).flatten())

        scale = self._curriculum_scale()
        mag = self.target_mag * self._envelope() * scale * self.robot_weight_n
        f_yaw = torch.zeros(self.num_envs, 3, device=self.device)
        f_yaw[:, 0] = mag * torch.cos(self.dir_angle)
        f_yaw[:, 1] = mag * torch.sin(self.dir_angle)
        self.applied_force_yaw = f_yaw

        quat_w = self.robot.data.root_link_quat_w
        force_w = quat_apply(yaw_quat(quat_w), f_yaw)
        # Torque of a force applied at the push point instead of at the COM.
        lever_w = quat_apply(quat_w, self.push_point_b)
        torque_w = torch.linalg.cross(lever_w, force_w)
        self.robot.write_external_wrench_to_sim(
            force_w.unsqueeze(1), torque_w.unsqueeze(1), body_ids=[self._body_id]
        )

        frac = mag / self.robot_weight_n
        self._sum_frac += frac
        self._steps += 1.0
        mean_frac = self._sum_frac / self._steps
        # Episode means; the peak a robot faces is curriculum_scale * max_frac.
        self.metrics["force_frac_weight"] = mean_frac
        self.metrics["force_n"] = mean_frac * self.robot_weight_n
        self.metrics["curriculum_scale"] = torch.full_like(mag, scale)

    def _update_metrics(self) -> None:
        pass


@dataclass(kw_only=True)
class PushForceCommandCfg(CommandTermCfg):
    entity_name: str = "robot"
    body_name: str = "base"
    velocity_command_name: str = "twist"
    push_point_b: tuple[float, float, float] = (0.4, 0.0, 0.0)
    max_frac_of_weight: float = 0.4
    """Peak force as a fraction of robot weight (0.4 ~ 200 N on ANYmal C)."""
    p_oppose: float = 0.7
    oppose_jitter_deg: float = 30.0
    moving_threshold: float = 0.1
    gap_s: tuple[float, float] = (0.5, 2.0)
    ramp_s: tuple[float, float] = (0.2, 0.5)
    hold_s: tuple[float, float] = (1.0, 3.0)
    curriculum_start_scale: float = 0.2
    curriculum_env_steps: float = 2_000 * 24
    """Env steps (iterations x 24) to reach full intensity."""
    fixed_frac: float | None = None
    """Evaluation only: every cycle uses exactly this fraction of weight."""

    def build(self, env: ManagerBasedRlEnv) -> PushForceCommand:
        return PushForceCommand(self, env)
