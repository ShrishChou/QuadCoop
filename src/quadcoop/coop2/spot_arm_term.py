"""Spot with its arm in the two-robot task: the action term over RAI's frozen walker, and its observations.

Action per robot (docs/spot_arm_pair.md), 50 Hz:
  arm "stowed"   3: forward, lateral, yaw velocity (the same ranges and smoothing as the other robots' walker term)
  arm "learned"  9: those 3 + six arm joint targets. Arm action a in [-1, 1] per joint -> target = stowed pose +
                 a x ARM_SPAN, clamped to the joint limits (a = 0 is the stowed arm; + unfolds the shoulder and the
                 elbow), then rate-limited to ``arm_rate`` rad/s: the walker stays up through a gradual arm motion
                 and falls when the arm is snapped outward (port acceptance, docs/spot_arm.md). Gripper held closed.
The applied command (base velocity, arm targets, default torso) goes to the walker, whose leg targets and the arm
targets go to the model's own position actuators.

``arm_locked`` (per env, default off) holds a robot's arm stowed whatever the policy outputs: the evaluation's
arm ablation of a learned-arm checkpoint. A zero action is "stand still, arm stowed" (a parked robot).
"""
from __future__ import annotations

from dataclasses import dataclass

import torch
from mjlab.envs import ManagerBasedRlEnv
from mjlab.envs.mdp.actions import JointPositionActionCfg
from mjlab.managers.action_manager import ActionTerm, ActionTermCfg

from quadcoop.robots import spot_arm as sa

N_ARM = 6
ARM_MODES = ("stowed", "learned")


class SpotArmAction(ActionTerm):
    cfg: SpotArmActionCfg

    def __init__(self, cfg: SpotArmActionCfg, env: ManagerBasedRlEnv):
        super().__init__(cfg, env)
        assert cfg.arm in ARM_MODES, cfg.arm
        self._joint = JointPositionActionCfg(entity_name=cfg.entity_name, actuator_names=(".*",), scale=1.0,
                                             use_default_offset=False).build(env)
        self.robot = env.scene[cfg.entity_name]
        self.walker = sa.RaiWalker(self.robot, self.device)
        n, dev = self.num_envs, self.device
        self._dim = 3 + (N_ARM if cfg.arm == "learned" else 0)
        self._raw = torch.zeros(n, self._dim, device=dev)
        self._lo = torch.tensor([cfg.vx_range[0], cfg.vy_range[0], cfg.wz_range[0]], device=dev)
        self._hi = torch.tensor([cfg.vx_range[1], cfg.vy_range[1], cfg.wz_range[1]], device=dev)
        self.applied_norm = torch.zeros(n, 3, device=dev)
        self.stow = torch.tensor(sa.ARM_STOWED[:N_ARM], device=dev)
        self.span = torch.tensor(sa.ARM_SPAN, device=dev)
        self.arm_lo = torch.tensor(sa.ARM_LO, device=dev)
        self.arm_hi = torch.tensor(sa.ARM_HI, device=dev)
        self.arm_goal = self.stow.repeat(n, 1)  # what the policy asked for (after the clamp)
        self.arm_target = self.stow.repeat(n, 1)  # what the arm actuators get (rate-limited)
        self.arm_locked = torch.zeros(n, dtype=torch.bool, device=dev)
        self.walker_action = self.walker.prev  # (n, 12) the walker's last leg action
        print(f"[spot_arm] {cfg.entity_name}: RAI walker, arm {cfg.arm} ({self._dim} actions"
              + (f", arm targets rate-limited to {cfg.arm_rate:g} rad/s" if cfg.arm == "learned" else "") + ")")

    @property
    def action_dim(self) -> int:
        return self._dim

    @property
    def raw_action(self) -> torch.Tensor:
        return self._raw

    def process_actions(self, actions: torch.Tensor) -> None:
        self._raw[:] = actions
        a = torch.clamp(actions, -1.0, 1.0)
        twist = self._env.command_manager.get_term(self.cfg.twist_name)
        target = self._lo + (a[:, :3] + 1.0) * 0.5 * (self._hi - self._lo)
        self.applied_norm[:] = a[:, :3]
        s = self.cfg.smoothing
        twist.vel_command_b[:] = (1.0 - s) * twist.vel_command_b + s * target
        if self._dim > 3:
            goal = torch.maximum(torch.minimum(self.stow + a[:, 3:] * self.span, self.arm_hi), self.arm_lo)
            goal = torch.where(self.arm_locked.unsqueeze(-1), self.stow.expand_as(goal), goal)
        else:
            goal = self.stow.expand(self.num_envs, N_ARM)
        self.arm_goal[:] = goal
        step = self.cfg.arm_rate * self._env.step_dt
        self.arm_target += torch.clamp(goal - self.arm_target, -step, step)
        arm7 = torch.cat([self.arm_target, torch.zeros(self.num_envs, 1, device=self.device)], -1)
        tg = self.walker.targets(sa.RaiWalker.command(twist.vel_command_b, arm7))
        self._joint.process_actions(tg)

    def apply_actions(self) -> None:
        self._joint.apply_actions()

    def reset(self, env_ids: torch.Tensor | slice | None = None) -> None:
        ids = slice(None) if env_ids is None else env_ids
        self._joint.reset(env_ids)
        self._raw[ids] = 0.0
        self.applied_norm[ids] = 0.0
        self.arm_goal[ids] = self.stow
        self.arm_target[ids] = self.stow
        self.walker.reset(env_ids)


@dataclass(kw_only=True)
class SpotArmActionCfg(ActionTermCfg):
    twist_name: str = "twist"
    arm: str = "stowed"  # "stowed" | "learned"
    vx_range: tuple[float, float] = (-0.6, 0.8)  # WalkerCommandActionCfg's (the walker tracks 1.0 m/s)
    vy_range: tuple[float, float] = (-0.5, 0.5)
    wz_range: tuple[float, float] = (-0.7, 0.7)
    smoothing: float = 0.3
    arm_rate: float = 1.5  # rad/s; the port check's ramp (stowed -> out in 1.5 s) peaked at 1.5 rad/s
    interface: str = "raw"

    def build(self, env: ManagerBasedRlEnv) -> SpotArmAction:
        return SpotArmAction(self, env)


# -- observations ----------------------------------------------------------------------------------------------
def base_lin_vel(env, robot: str) -> torch.Tensor:
    return env.scene[robot].data.root_link_lin_vel_b


def base_ang_vel(env, robot: str) -> torch.Tensor:
    return env.scene[robot].data.root_link_ang_vel_b


def _fngr(env, robot: str) -> int:
    cache = env.__dict__.setdefault("_spot_arm_fngr", {})
    if robot not in cache:
        cache[robot] = int(env.scene[robot].find_bodies(sa.GRIPPER_BODY)[0][0])
    return cache[robot]


def gripper_pos_w(env, robot: str) -> torch.Tensor:
    return env.scene[robot].data.body_link_pos_w[:, _fngr(env, robot)]


def arm_state(env, robot: str, action_name: str) -> torch.Tensor:
    """(21) arm joint positions relative to stowed (6), joint velocities x 0.1 (6), the arm targets the actuators
    last got relative to stowed (6), the gripper relative to the object's origin (3: xy in the robot's yaw frame, z)."""
    from mjlab.utils.lab_api.math import quat_apply_inverse, yaw_quat

    r = env.scene[robot]
    term = env.action_manager.get_term(action_name)
    q = r.data.joint_pos[:, 12:12 + N_ARM] - term.stow
    qd = 0.1 * r.data.joint_vel[:, 12:12 + N_ARM]
    g = env.command_manager.get_term("goal")
    rel = gripper_pos_w(env, robot) - g.box_pos()
    xy = torch.cat([rel[:, :2], torch.zeros_like(rel[:, :1])], -1)
    xy = quat_apply_inverse(yaw_quat(r.data.root_link_quat_w), xy)[:, :2]
    return torch.cat([q, qd, term.arm_target - term.stow, xy, rel[:, 2:3]], -1)


def touch(env, sensor: str) -> torch.Tensor:
    return env.scene[sensor].data.found.view(env.num_envs, -1).any(-1)


def arm_touch(env, robot: str) -> torch.Tensor:
    """(2) the arm is touching the object; the trunk is touching the object."""
    return torch.stack([touch(env, f"arm_{robot}"), touch(env, f"trunk_{robot}")], -1).float()
