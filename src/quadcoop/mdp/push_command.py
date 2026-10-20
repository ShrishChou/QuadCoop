"""Velocity command for Stage 0: walk one fixed way and push whatever is in the path.

Same command (vx, vy, wz in the body frame) and same actor observation as mjlab's
stock velocity task, so the trained walker stays a drop-in low-level controller.

Two kinds of episode, chosen at every reset:

* **Push episode** (share ``1 - p_free_walk``): the robot walks in a direction picked
  at reset from the full circle (forward, sideways, backward, diagonal), sometimes
  while turning slowly, and every ``reaim_s`` the direction is nudged by up to
  ``reaim_deg`` so it learns to keep pushing while the push angle changes. Objects are
  put on that line ahead of the robot; when the robot has passed one (or it slid or
  rolled out of the way) a new one is put ahead.
* **Free-walk episode** (share ``p_free_walk``): no objects; the command changes every
  few seconds and can turn. This keeps the walker responsive to changing commands,
  which is what the Stage 1 high-level policy will send it.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import torch
from mjlab.tasks.velocity.mdp.velocity_command import (
    UniformVelocityCommand,
    UniformVelocityCommandCfg,
)

from quadcoop.mdp.object_events import _state, object_is_done, place_ahead

if TYPE_CHECKING:
    from mjlab.envs import ManagerBasedRlEnv


class PushTaskCommand(UniformVelocityCommand):
    cfg: PushTaskCommandCfg

    def __init__(self, cfg: PushTaskCommandCfg, env: ManagerBasedRlEnv):
        super().__init__(cfg, env)
        n, dev = self.num_envs, self.device
        self._resetting = False
        self.push_mode = torch.zeros(n, dtype=torch.bool, device=dev)
        self.bearing = torch.zeros(n, device=dev)  # body-frame direction of travel
        self.clock = torch.zeros(n, device=dev)
        self.next_try = torch.zeros(n, device=dev)

    # -- helpers ------------------------------------------------------------------
    def _p_and_mass(self) -> tuple[float, float]:
        st = _state(self._env)
        c = self.cfg
        p = st["p_place"] if c.p_override is None else c.p_override
        m = st["max_mass"] if c.max_mass_override is None else c.max_mass_override
        return p, m

    def _sample_bearing(self, m: int) -> torch.Tensor:
        c, dev = self.cfg, self.device
        if c.fixed_bearing is not None:
            return torch.full((m,), float(c.fixed_bearing), device=dev)
        ahead = torch.rand(m, device=dev) < c.p_forward
        return torch.where(
            ahead,
            torch.empty(m, device=dev).uniform_(-c.angle_jitter, c.angle_jitter),
            torch.empty(m, device=dev).uniform_(-torch.pi, torch.pi),
        )

    # -- CommandTerm hooks ----------------------------------------------------------
    def reset(self, env_ids):
        self._resetting = True
        try:
            return super().reset(env_ids)
        finally:
            self._resetting = False

    def _resample_command(self, env_ids: torch.Tensor) -> None:
        super()._resample_command(env_ids)
        c, dev = self.cfg, self.device
        self.is_heading_env[env_ids] = False  # never steer toward a random world heading
        if c.sample_from_ranges:  # evaluation: stock sampling from ``ranges``
            self.push_mode[env_ids] = False
            place_ahead(self._env, env_ids, torch.zeros(len(env_ids), device=dev), c, 0.0, 0.0)
            return

        if self._resetting:
            self.push_mode[env_ids] = torch.rand(len(env_ids), device=dev) >= c.p_free_walk
            self.clock[env_ids] = 0.0
            self.next_try[env_ids] = 0.0
        push = env_ids[self.push_mode[env_ids]]
        free = env_ids[~self.push_mode[env_ids]]
        m = len(env_ids)
        speed = torch.empty(m, device=dev).uniform_(*c.speed_range)
        bearing = self._sample_bearing(m)

        # Free walk: constant speed per segment, sometimes turning, no objects.
        if len(free):
            sel = ~self.push_mode[env_ids]
            turn = torch.rand(len(free), device=dev) >= c.p_yaw_zero
            wz = torch.where(turn, torch.empty(len(free), device=dev).uniform_(-c.yaw_max, c.yaw_max),
                             torch.zeros(len(free), device=dev))
            self.vel_command_b[free, 0] = speed[sel] * torch.cos(bearing[sel])
            self.vel_command_b[free, 1] = speed[sel] * torch.sin(bearing[sel])
            self.vel_command_b[free, 2] = wz
            self.vel_command_w[free] = self.vel_command_b[free]
            if self._resetting:  # park everything once per episode
                place_ahead(self._env, free, bearing[sel], c, 0.0, 0.0)

        # Push episode: any direction; re-aimed by a bounded nudge every reaim_s.
        if len(push):
            sel = self.push_mode[env_ids]
            k = len(push)
            if self._resetting:
                self.bearing[push] = bearing[sel]
            else:
                nudge = torch.empty(k, device=dev).uniform_(-1.0, 1.0) * c.reaim_deg * torch.pi / 180
                self.bearing[push] = torch.atan2(torch.sin(self.bearing[push] + nudge),
                                                 torch.cos(self.bearing[push] + nudge))
            turn = torch.rand(k, device=dev) < c.push_yaw_prob
            wz = torch.where(turn, torch.empty(k, device=dev).uniform_(-c.push_yaw_max, c.push_yaw_max),
                             torch.zeros(k, device=dev))
            b = self.bearing[push]
            self.vel_command_b[push, 0] = speed[sel] * torch.cos(b)
            self.vel_command_b[push, 1] = speed[sel] * torch.sin(b)
            self.vel_command_b[push, 2] = wz
            self.vel_command_w[push] = self.vel_command_b[push]
            if self._resetting:
                p, max_mass = self._p_and_mass()
                choice = place_ahead(self._env, push, b, c, p, max_mass)
                self.next_try[push] = torch.where(choice < 0, c.retry_s, 0.0)
            self.is_standing_env[push] = False
            self.time_left[push] = torch.empty(k, device=dev).uniform_(*c.reaim_s)

    def _update_command(self) -> None:
        super()._update_command()
        if self.cfg.sample_from_ranges:
            return
        self.clock += self._env.step_dt
        due = self.push_mode & (self.clock >= self.next_try)
        if not due.any():
            return
        ids = due.nonzero(as_tuple=False).flatten()
        done = object_is_done(self._env, ids, self.bearing[ids])
        ids = ids[done]
        if len(ids) == 0:
            return
        p, max_mass = self._p_and_mass()
        choice = place_ahead(self._env, ids, self.bearing[ids], self.cfg, p, max_mass)
        # Nothing placed (curriculum said no): look again in a few seconds.
        self.next_try[ids] = torch.where(choice < 0, self.clock[ids] + self.cfg.retry_s,
                                         self.clock[ids])


@dataclass(kw_only=True)
class PushTaskCommandCfg(UniformVelocityCommandCfg):
    robot_half_length: float = 0.55
    p_free_walk: float = 0.25  # share of episodes with changing commands and no objects
    speed_range: tuple[float, float] = (0.3, 0.7)  # m/s
    p_forward: float = 0.25  # share of directions drawn near straight ahead; rest: full circle
    angle_jitter: float = 0.2  # rad, around straight ahead
    fixed_bearing: float | None = None  # rad; eval only: every push goes this way
    push_yaw_prob: float = 0.3  # share of push segments that also turn
    push_yaw_max: float = 0.3  # rad/s
    reaim_s: tuple[float, float] = (5.0, 10.0)  # push direction is nudged this often
    reaim_deg: float = 45.0  # by at most this much
    p_yaw_zero: float = 0.7  # free walk: share of segments with no turning
    yaw_max: float = 0.4  # rad/s, free walk turning rate
    gap_range: tuple[float, float] = (0.3, 1.5)  # clear distance from bumper to a new object
    lateral_range: tuple[float, float] = (-0.2, 0.2)
    yaw_jitter: float = 0.3  # object orientation noise
    park_distance: float = 30.0
    retry_s: float = 3.0  # when the curriculum declined to place an object, try again after
    sample_from_ranges: bool = False  # True: stock uniform sampling from ``ranges`` (eval)
    # Evaluation-only overrides (bypass the curriculum):
    p_override: float | None = None
    max_mass_override: float | None = None
    only: str | None = None

    def build(self, env: ManagerBasedRlEnv) -> PushTaskCommand:
        return PushTaskCommand(self, env)