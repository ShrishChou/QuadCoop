"""Velocity command that sets up a pushing task: an object appears on the commanded line.

Same command (vx, vy, wz in the body frame) and same actor observation as mjlab's
stock velocity task, so the trained walker stays a drop-in low-level controller.
What changes is *when and where objects appear*: whenever a command is sampled, with
probability ``p_place`` an object is put ahead of the robot on the bearing the command
points along, the command is aimed at it (no turning), and the command is held for
``hold_s`` so the robot actually walks into the object. While an object is still near,
re-sampling keeps the robot pointed at it instead of teleporting it away.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import torch
from mjlab.tasks.velocity.mdp.velocity_command import (
    UniformVelocityCommand,
    UniformVelocityCommandCfg,
)

from quadcoop.mdp.object_events import place_objects

if TYPE_CHECKING:
    from mjlab.envs import ManagerBasedRlEnv


class PushTaskCommand(UniformVelocityCommand):
    cfg: PushTaskCommandCfg

    def __init__(self, cfg: PushTaskCommandCfg, env: ManagerBasedRlEnv):
        super().__init__(cfg, env)
        self._resetting = False

    def reset(self, env_ids):
        self._resetting = True
        try:
            return super().reset(env_ids)
        finally:
            self._resetting = False

    def _resample_command(self, env_ids: torch.Tensor) -> None:
        super()._resample_command(env_ids)
        c = self.cfg
        if not c.sample_from_ranges:
            # One constant velocity per segment: a speed, a bearing, and (mostly) no turning.
            m, dev = len(env_ids), self.device
            speed = torch.empty(m, device=dev).uniform_(*c.speed_range)
            ahead = torch.rand(m, device=dev) < c.free_p_forward
            bearing = torch.where(
                ahead,
                torch.empty(m, device=dev).uniform_(-0.3, 0.3),
                torch.empty(m, device=dev).uniform_(-torch.pi, torch.pi),
            )
            turn = torch.rand(m, device=dev) >= c.p_yaw_zero
            wz = torch.where(turn, torch.empty(m, device=dev).uniform_(-c.yaw_max, c.yaw_max),
                             torch.zeros(m, device=dev))
            self.vel_command_b[env_ids, 0] = speed * torch.cos(bearing)
            self.vel_command_b[env_ids, 1] = speed * torch.sin(bearing)
            self.vel_command_b[env_ids, 2] = wz
            self.vel_command_w[env_ids] = self.vel_command_b[env_ids]
        self.is_heading_env[env_ids] = False  # never steer toward a random world heading
        place_objects(self._env, env_ids, self, self.cfg, self._resetting)


@dataclass(kw_only=True)
class PushTaskCommandCfg(UniformVelocityCommandCfg):
    robot_half_length: float = 0.55
    gap_range: tuple[float, float] = (0.1, 1.0)  # clear distance from bumper to object face
    lateral_range: tuple[float, float] = (-0.25, 0.25)
    yaw_jitter: float = 0.3  # object orientation noise
    park_distance: float = 30.0
    p_forward: float = 0.8  # share of pushes straight ahead (rest: left/right/back)
    angle_jitter: float = 0.2  # rad
    speed_range: tuple[float, float] = (0.2, 0.8)  # m/s, every command (kept modest on purpose)
    free_p_forward: float = 0.5  # share of object-free segments that walk straight ahead
    p_yaw_zero: float = 0.7  # share of segments with no turning at all
    yaw_max: float = 0.4  # rad/s when turning
    sample_from_ranges: bool = False  # True: stock uniform sampling from ``ranges`` (eval)
    hold_s: tuple[float, float] = (5.0, 10.0)
    engaged_dist: float = 3.0  # an object this close is "being pushed": keep it
    # Evaluation-only overrides (bypass the curriculum):
    p_override: float | None = None
    max_mass_override: float | None = None
    only: str | None = None

    def build(self, env: ManagerBasedRlEnv) -> PushTaskCommand:
        return PushTaskCommand(self, env)