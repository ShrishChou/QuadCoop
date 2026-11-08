"""Compliant walker (walker v2): the velocity command becomes an admittance law.

The v1 walker tracks its velocity command no matter what it touches: against an object it
cannot move it pushes as hard as it can (the force is close to on/off, 140-200 N in taps),
and below ~0.2-0.3 m/s it does not walk at all (it never saw small commands). Neither lets a
planner ask for "push this hard" or "step 3 cm closer".

Walker v2 keeps the same command interface (vx, vy, wz in the body frame) but is trained to
track a *compliant* target instead of the raw command:

    v_target_xy = v_cmd_xy + F_xy / k        (F: horizontal contact force ON the robot from
    wz_target   = wz_cmd                     objects, body frame; k: stiffness, N per m/s)

so it behaves like a spring-damper at its front: in free space it walks at the command;
against an object it slows by F / k; against an object it cannot move it settles where
F = k x |v_cmd|, i.e. **the commanded speed sets the push force** (k = 1000: 0.1 m/s ~ 100 N,
0.25 m/s ~ 250 N). Pushing a movable object of sliding force F_s it walks at v_cmd - F_s / k.

The robot observes the contact force (``bumper_force_obs``, body frame, last in the actor
input) so the law is learnable; ``ComplianceTargetCommand`` computes the target every step and
the stock tracking / gait / posture rewards read it as their command. Added rewards:
``force_rate_penalty`` (steady pressing instead of taps) and ``velocity_progress_target``.

Walker v2.1 (same network): the force F also includes the smooth training force field when the
env has one (``applied_force_b``), the force is filtered more slowly and the target never asks
for more than 0.1 m/s of back-off (both set in walker_env_cfg.py).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import TYPE_CHECKING

import torch
from mjlab.managers.command_manager import CommandTerm, CommandTermCfg

if TYPE_CHECKING:
    from mjlab.envs import ManagerBasedRlEnv
    from mjlab.sensor import ContactSensor


def _yaw(q: torch.Tensor) -> torch.Tensor:
    w, x, y, z = q.unbind(-1)
    return torch.atan2(2.0 * (w * z + x * y), 1.0 - 2.0 * (y * y + z * z))


def contact_force_on_robot_w(env: ManagerBasedRlEnv, sensor_name: str) -> torch.Tensor:
    """(n, 2) horizontal contact force on the robot from the objects, world frame. The sensor's
    primary is the objects and its secondary the robot; its reading is the force on the
    secondary (same convention as the two-robot env's push_<robot> sensors, see
    coop2.mdp.object_force_from), summed over all object bodies."""
    sensor: ContactSensor = env.scene[sensor_name]
    f = sensor.data.force
    assert f is not None, f"sensor {sensor_name} needs fields=('found', 'force')"
    return f.sum(1)[:, :2]


def applied_force_b(env: ManagerBasedRlEnv, term_name: str = "push_force") -> torch.Tensor | None:
    """(n, 2) the smooth training force field on the robot (mdp/push_force.py), robot yaw frame, N;
    None when the env has no such field. Walker v2.1 treats it as one more contact force: it
    enters the compliant target and the force input exactly like a push from an object, so the
    walker practises the whole force range on clean ramp-hold-ramp loads, not only on rigid
    impacts (as in Portela et al. 2024 and the unified position/force policy, arXiv 2505.20829)."""
    term = getattr(env.command_manager, "_terms", {}).get(term_name)
    if term is None or not hasattr(term, "applied_force_yaw"):
        return None
    return term.applied_force_yaw[:, :2]


def sensed_force_b(env: ManagerBasedRlEnv, sensor_name: str, entity: str = "robot") -> torch.Tensor:
    """(n, 2) everything the walker should feel at its front, robot yaw frame, N: contact from
    objects plus the training force field (if any)."""
    f = to_body(env, contact_force_on_robot_w(env, sensor_name), entity)
    extra = applied_force_b(env)
    return f if extra is None else f + extra


def to_body(env: ManagerBasedRlEnv, v_w: torch.Tensor, entity: str = "robot") -> torch.Tensor:
    yaw = _yaw(env.scene[entity].data.root_link_quat_w)
    c, s = torch.cos(yaw), torch.sin(yaw)
    return torch.stack([c * v_w[:, 0] + s * v_w[:, 1], -s * v_w[:, 0] + c * v_w[:, 1]], -1)


class ComplianceTargetCommand(CommandTerm):
    """The velocity the robot should actually move at (body frame vx, vy, wz): the twist
    command plus F / k (see the module docstring). A command term so the stock rewards can
    read it as their ``command_name``."""

    cfg: ComplianceTargetCommandCfg

    def __init__(self, cfg: ComplianceTargetCommandCfg, env: ManagerBasedRlEnv):
        super().__init__(cfg, env)
        n, dev = self.num_envs, self.device
        self.target = torch.zeros(n, 3, device=dev)
        self.force_b = torch.zeros(n, 2, device=dev)  # filtered contact force on the robot, body frame (N)
        self.contact_b = torch.zeros(n, 2, device=dev)  # contact from objects only (force_rate_penalty)
        self.prev_force_b = torch.zeros(n, 2, device=dev)  # contact_b, previous step
        self.raw_force_b = torch.zeros(n, 2, device=dev)  # contact + training force field, unfiltered
        self._steps = torch.zeros(n, device=dev)
        self._sums = {k: torch.zeros(n, device=dev) for k in ("force_n", "target_speed", "target_err", "pressing")}
        for k in self._sums:
            self.metrics[k] = torch.zeros(n, device=dev)

    @property
    def command(self) -> torch.Tensor:
        return self.target

    def _twist(self) -> torch.Tensor:
        return self._env.command_manager.get_command(self.cfg.twist_name)

    def _update_command(self) -> None:
        c = self.cfg
        self.prev_force_b[:] = self.contact_b
        self.contact_b[:] = to_body(self._env, contact_force_on_robot_w(self._env, c.sensor_name))
        extra = applied_force_b(self._env)
        f_b = self.contact_b if extra is None else self.contact_b + extra
        self.raw_force_b[:] = f_b
        a = c.filter_alpha
        self.force_b[:] = (1.0 - a) * self.force_b + a * f_b
        f = self.force_b
        mag = torch.linalg.norm(f, dim=-1, keepdim=True)
        f = torch.where(mag > c.force_deadband, f * (1.0 - c.force_deadband / mag.clamp(min=1e-6)), torch.zeros_like(f))
        tw = self._twist()
        v = tw[:, :2] + f / c.stiffness
        # never told to back away faster than max_backoff, nor to go faster than the command
        sp = torch.linalg.norm(v, dim=-1, keepdim=True)
        cap = torch.maximum(torch.linalg.norm(tw[:, :2], dim=-1, keepdim=True), torch.full_like(sp, c.max_backoff))
        v = v * torch.clamp(cap / sp.clamp(min=1e-6), max=1.0)
        self.target[:, :2] = v
        self.target[:, 2] = tw[:, 2]

    def _resample_command(self, env_ids: torch.Tensor) -> None:
        self.force_b[env_ids] = 0.0
        self.raw_force_b[env_ids] = 0.0
        self.contact_b[env_ids] = 0.0
        self.prev_force_b[env_ids] = 0.0
        self.target[env_ids] = self._twist()[env_ids]

    def _update_metrics(self) -> None:
        robot = self._env.scene["robot"]
        v_b = to_body(self._env, robot.data.root_link_lin_vel_w[:, :2])
        fmag = torch.linalg.norm(self.raw_force_b, dim=-1)
        self._steps += 1
        self._sums["force_n"] += fmag
        self._sums["target_speed"] += torch.linalg.norm(self.target[:, :2], dim=-1)
        self._sums["target_err"] += torch.linalg.norm(v_b - self.target[:, :2], dim=-1)
        self._sums["pressing"] += (fmag > self.cfg.force_deadband).float()
        for k, s in self._sums.items():
            self.metrics[k][:] = s / self._steps.clamp(min=1)

    def reset(self, env_ids):
        out = super().reset(env_ids)
        self._steps[env_ids] = 0.0
        for s in self._sums.values():
            s[env_ids] = 0.0
        return out


@dataclass(kw_only=True)
class ComplianceTargetCommandCfg(CommandTermCfg):
    resampling_time_range: tuple[float, float] = (1e9, 1e9)  # resampled only at reset
    twist_name: str = "twist"
    sensor_name: str = "bumper_force"
    stiffness: float = 1000.0  # N per m/s: against a wall, push force = stiffness x commanded speed
    force_deadband: float = 5.0  # N: contact below this is not a push
    filter_alpha: float = 0.3  # low-pass on the force (per 50 Hz step); v2.1 uses 0.1 (~0.2 s), so an
    #                            impact spike barely moves the target while a sustained push does
    max_backoff: float = 0.3  # m/s: fastest the target ever asks the robot to give way (v2.1: 0.1)

    def build(self, env: ManagerBasedRlEnv) -> ComplianceTargetCommand:
        return ComplianceTargetCommand(self, env)


# -- observation ---------------------------------------------------------------------------
def bumper_force_obs(env: ManagerBasedRlEnv, sensor_name: str = "bumper_force", f_ref: float = 200.0,
                     entity: str = "robot") -> torch.Tensor:
    """(n, 2): the horizontal contact force on the robot from objects, robot frame, / f_ref
    (clipped to +-2.5). Walker v2's last actor input."""
    f_b = sensed_force_b(env, sensor_name, entity)
    return (f_b / f_ref).clamp(-2.5, 2.5)


# -- rewards ---------------------------------------------------------------------------------
def force_rate_penalty(env: ManagerBasedRlEnv, command_name: str = "compliance", f_ref: float = 200.0) -> torch.Tensor:
    """Change of the contact force from the last step (/ f_ref, at most 2): taps and bumps cost,
    a steady press does not. Contact with objects only: the training force field's ramps are not
    the robot's doing."""
    term: ComplianceTargetCommand = env.command_manager.get_term(command_name)  # type: ignore[assignment]
    d = torch.linalg.norm(term.contact_b - term.prev_force_b, dim=-1)
    return (d / f_ref).clamp(max=2.0)


def velocity_progress_target(env: ManagerBasedRlEnv, command_name: str = "compliance",
                             min_speed: float = 0.03, floor: float = 0.1) -> torch.Tensor:
    """Like rewards.velocity_progress (fraction of the target speed achieved along it, 0..1),
    on the compliant target and down to small speeds (denominator floored at `floor` m/s so
    tiny targets are paid in proportion, not amplified)."""
    robot = env.scene["robot"]
    tgt = env.command_manager.get_command(command_name)[:, :2]
    speed = torch.linalg.norm(tgt, dim=-1)
    v_b = to_body(env, robot.data.root_link_lin_vel_w[:, :2])
    frac = (v_b * tgt).sum(-1) / torch.maximum(speed, torch.full_like(speed, floor)).square()
    lim = (speed / torch.maximum(speed, torch.full_like(speed, floor))).square()
    return torch.where(speed > min_speed, torch.minimum(frac, lim).clamp(min=0.0), torch.zeros_like(frac))


def stiffness_check(k: float, speeds=(0.05, 0.1, 0.25)) -> str:
    return ", ".join(f"{v:g} m/s -> {k * v:.0f} N" for v in speeds) + f" (k = {k:g} N per m/s)"


__all__ = ["ComplianceTargetCommand", "ComplianceTargetCommandCfg", "bumper_force_obs", "force_rate_penalty",
           "velocity_progress_target", "contact_force_on_robot_w", "applied_force_b", "sensed_force_b", "stiffness_check", "math"]
