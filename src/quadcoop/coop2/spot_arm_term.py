"""Spot with its arm in the two-robot task: the action term over RAI's frozen walker, and its observations.

Action per robot (docs/spot_arm_pair.md), 50 Hz:
  arm "stowed"   3: forward, lateral, yaw velocity (the same ranges and smoothing as the other robots' walker term)
  arm "learned"  9: those 3 + six arm joint targets. Arm action a in [-1, 1] per joint -> target = stowed pose +
                 a x ARM_SPAN, clamped to the joint limits (a = 0 is the stowed arm; + unfolds the shoulder and the
                 elbow).
  arm "hand"     7: those 3 + a hand point (3, body frame: HAND_CENTER + a x HAND_SPAN, m) + extension (1). The
                 joint targets are stowed + w x (IK(hand point) - stowed), w = clamp(extension, 0, 1): extension <= 0
                 is the stowed arm whatever the hand point, small positive values start the reach from stowed, 1 is
                 the commanded reach. IK: sa.hand_ik (gripper level, out-of-reach points brought within reach).
  arm "hand_rate" 7: those 3 + hand point rate (3) + extension rate (1): a persistent, bounded hand target. Zero holds
                 the current target; the hand point moves at a x ``hand_speed`` m/s inside the HAND_CENTER +- HAND_SPAN
                 box; the extension w moves at a x ``ext_rate`` /s inside [0, 1] (negative = retract). Joint targets
                 as "hand": stowed + w x (IK(hand point) - stowed). Optional ``arm_hold_steps``: the arm part of the
                 action is latched for that many steps (exploration setting), except that a retract (extension
                 action < -0.5) acts at once. The action-rate cost skips these 4 outputs (mdp.agent_action_rate).
Arm targets (all arm modes) are rate-limited to ``arm_rate`` rad/s: the walker stays up through a gradual arm
motion and falls when the arm is snapped outward (port acceptance, docs/spot_arm.md). Gripper held closed.
The applied command (base velocity, arm targets, default torso) goes to the walker, whose leg targets and the arm
targets go to the model's own position actuators.

``arm_locked`` (per env, default off) holds a robot's arm stowed whatever the policy outputs: the evaluation's
arm ablation of a learned-arm checkpoint. A zero action is "stand still, arm stowed" (a parked robot).

Torso (docs/spot_arm_pair.md, "Torso interface"): ``torso=True`` appends 2 outputs, pitch and height, after the arm
outputs. Action 0 is RAI's default posture (pitch 0, height 0.52 m) exactly; pitch = a x torso_pitch (+-0.2 rad);
height = 0.52 + a x (0.52 - 0.40) for a < 0, + a x (0.55 - 0.52) for a > 0 (the range the posture walker was trained
on, 0.40-0.55 m); roll stays 0. The applied torso command moves toward that goal at most torso_pitch_rate rad/s and
torso_height_rate m/s. Evaluation overrides (per env, off by default): ``torso_override_on`` + ``torso_override``
(roll, pitch, height) replaces the goal (scripted posture sweeps, any checkpoint); ``arm_pose_on`` + ``arm_pose``
(6 joint targets) holds the arm at a fixed pose (arm-mechanism test). Both are rate-limited like the policy's own.
"""
from __future__ import annotations

from dataclasses import dataclass

import torch
from mjlab.envs import ManagerBasedRlEnv
from mjlab.envs.mdp.actions import JointPositionActionCfg
from mjlab.managers.action_manager import ActionTerm, ActionTermCfg

from quadcoop.robots import spot_arm as sa

N_ARM = 6
ARM_MODES = ("stowed", "learned", "hand", "hand_rate")  # "learned": joint targets
N_HAND = 4


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
        self._dim = 3 + {"stowed": 0, "learned": N_ARM, "hand": N_HAND, "hand_rate": N_HAND}[cfg.arm]
        if cfg.torso:  # 2 torso outputs after the arm outputs
            self._dim += 2
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
        self.hand_c = torch.tensor(sa.HAND_CENTER, device=dev)
        self.hand_s = torch.tensor(sa.HAND_SPAN, device=dev)
        self.hand_cmd = self.hand_c.repeat(n, 1)  # hand mode: the commanded hand point (body frame)
        self.blend = torch.zeros(n, device=dev)  # hand modes: w, 0 stowed .. 1 the commanded reach
        self._held = torch.zeros(n, N_HAND, device=dev)  # hand_rate: the latched arm action (arm_hold_steps)
        self._hold_k = 0
        self.walker_action = self.walker.prev  # (n, 12) the walker's last leg action
        self.torso_default = torch.tensor([0.0, 0.0, sa.STAND_HEIGHT_CMD], device=dev)
        self.torso = self.torso_default.repeat(n, 1)  # applied torso command (roll, pitch, height), rate-limited
        self.torso_goal = self.torso_default.repeat(n, 1)
        self.torso_override_on = torch.zeros(n, dtype=torch.bool, device=dev)
        self.torso_override = self.torso_default.repeat(n, 1)
        self.arm_pose_on = torch.zeros(n, dtype=torch.bool, device=dev)
        self.arm_pose = self.stow.repeat(n, 1)
        print(f"[spot_arm] {cfg.entity_name}: RAI walker, arm {cfg.arm} ({self._dim} actions"
              + (f", arm targets rate-limited to {cfg.arm_rate:g} rad/s" if cfg.arm != "stowed" else "") + ")")

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
        if self.cfg.arm == "learned":
            goal = torch.maximum(torch.minimum(self.stow + a[:, 3:] * self.span, self.arm_hi), self.arm_lo)
            goal = torch.where(self.arm_locked.unsqueeze(-1), self.stow.expand_as(goal), goal)
        elif self.cfg.arm == "hand":
            self.hand_cmd[:] = self.hand_c + a[:, 3:6] * self.hand_s
            w = torch.where(self.arm_locked, torch.zeros_like(a[:, 6]), a[:, 6].clamp(0.0, 1.0))
            self.blend[:] = w
            goal = self.stow + w.unsqueeze(-1) * (sa.hand_ik(self.hand_cmd) - self.stow)
        elif self.cfg.arm == "hand_rate":
            ar = a[:, 3:7]
            if self.cfg.arm_hold_steps > 1:  # latch the arm action; a retract acts at once
                if self._hold_k % self.cfg.arm_hold_steps == 0:
                    self._held[:] = ar
                self._hold_k += 1
                ret = ar[:, 3] < -0.5
                ar = torch.where(ret.unsqueeze(-1), torch.cat([self._held[:, :3], ar[:, 3:]], -1), self._held)
            dt = self._env.step_dt
            self.hand_cmd[:] = torch.minimum(torch.maximum(self.hand_cmd + ar[:, :3] * self.cfg.hand_speed * dt,
                                                           self.hand_c - self.hand_s), self.hand_c + self.hand_s)
            w = (self.blend + ar[:, 3] * self.cfg.ext_rate * dt).clamp(0.0, 1.0)
            self.blend[:] = torch.where(self.arm_locked, torch.zeros_like(w), w)
            goal = self.stow + self.blend.unsqueeze(-1) * (sa.hand_ik(self.hand_cmd) - self.stow)
        else:
            goal = self.stow.expand(self.num_envs, N_ARM)
        goal = torch.where(self.arm_pose_on.unsqueeze(-1), self.arm_pose, goal)
        self.arm_goal[:] = goal
        step = self.cfg.arm_rate * self._env.step_dt
        self.arm_target += torch.clamp(goal - self.arm_target, -step, step)
        arm7 = torch.cat([self.arm_target, torch.zeros(self.num_envs, 1, device=self.device)], -1)
        tgoal = self.torso_default.expand(self.num_envs, 3)
        if self.cfg.torso:
            at = a[:, -2:]
            lo_h, hi_h = self.cfg.torso_height
            d0 = float(sa.STAND_HEIGHT_CMD)
            h = d0 + torch.where(at[:, 1] < 0, at[:, 1] * (d0 - lo_h), at[:, 1] * (hi_h - d0))
            tgoal = torch.stack([torch.zeros_like(h), at[:, 0] * self.cfg.torso_pitch, h], -1)
        tgoal = torch.where(self.torso_override_on.unsqueeze(-1), self.torso_override, tgoal)
        self.torso_goal[:] = tgoal
        dt_ = self._env.step_dt
        lim = torch.tensor([0.0, self.cfg.torso_pitch_rate * dt_, self.cfg.torso_height_rate * dt_], device=self.device)
        self.torso += torch.maximum(torch.minimum(tgoal - self.torso, lim), -lim)
        tg = self.walker.targets(sa.RaiWalker.command(twist.vel_command_b, arm7, self.torso))
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
        self.hand_cmd[ids] = self.hand_c
        self.blend[ids] = 0.0
        self._held[ids] = 0.0
        self.torso[ids] = self.torso_default
        self.torso_goal[ids] = self.torso_default
        self.walker.reset(env_ids)


@dataclass(kw_only=True)
class SpotArmActionCfg(ActionTermCfg):
    twist_name: str = "twist"
    arm: str = "stowed"  # "stowed" | "learned" (joint targets) | "hand" (hand point + extension) | "hand_rate"
    hand_speed: float = 0.6  # hand_rate: m/s of hand-target motion at action 1
    ext_rate: float = 1.5  # hand_rate: extension change per second at action 1 (stowed -> full in 0.67 s)
    arm_hold_steps: int = 0  # hand_rate: latch the arm action for this many steps (0/1: off)
    vx_range: tuple[float, float] = (-0.6, 0.8)  # WalkerCommandActionCfg's (the walker tracks 1.0 m/s)
    vy_range: tuple[float, float] = (-0.5, 0.5)
    wz_range: tuple[float, float] = (-0.7, 0.7)
    smoothing: float = 0.3
    arm_rate: float = 1.5  # rad/s; the port check's ramp (stowed -> out in 1.5 s) peaked at 1.5 rad/s
    interface: str = "raw"
    torso: bool = False  # 2 more outputs: torso pitch and height (module docstring)
    torso_pitch: float = 0.2  # rad at action +-1
    torso_height: tuple[float, float] = (0.40, 0.55)  # m at action -1 / +1 (0: 0.52)
    torso_pitch_rate: float = 0.5  # rad/s
    torso_height_rate: float = 0.15  # m/s

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


def _wrist(env, robot: str) -> int:
    cache = env.__dict__.setdefault("_spot_arm_wrist", {})
    if robot not in cache:
        cache[robot] = int(env.scene[robot].find_bodies(sa.WRIST_BODY)[0][0])
    return cache[robot]


def hand_pos_w(env, robot: str) -> torch.Tensor:
    """(n, 3) the hand point (sa.HAND_OFF in the wrist frame), world."""
    from mjlab.utils.lab_api.math import quat_apply

    d = env.scene[robot].data
    k = _wrist(env, robot)
    off = torch.tensor(sa.HAND_OFF, device=env.device).expand(env.num_envs, 3)
    return d.body_link_pos_w[:, k] + quat_apply(d.body_link_quat_w[:, k], off)


def hand_pos_b(env, robot: str) -> torch.Tensor:
    """(n, 3) the measured hand point in the robot's body frame (the frame of the hand command)."""
    from mjlab.utils.lab_api.math import quat_apply_inverse

    d = env.scene[robot].data
    return quat_apply_inverse(d.root_link_quat_w, hand_pos_w(env, robot) - d.root_link_pos_w)


def hand_state(env, robot: str, action_name: str) -> torch.Tensor:
    """(7) the measured hand point in the body frame relative to HAND_CENTER (3), the commanded hand point relative
    to HAND_CENTER (3; 0 unless arm "hand"), the extension w (1; 0 unless arm "hand")."""
    term = env.action_manager.get_term(action_name)
    hb = hand_pos_b(env, robot) - term.hand_c
    return torch.cat([hb, term.hand_cmd - term.hand_c, term.blend.unsqueeze(-1)], -1)


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


def torso_state(env, robot: str, action_name: str) -> torch.Tensor:
    """(4) the applied torso command, pitch and height - 0.52 m; its tracking error, base height - commanded height
    and projected-gravity x - sin(commanded pitch) (ReLIC's attitude term)."""
    term = env.action_manager.get_term(action_name)
    d = env.scene[robot].data
    t = term.torso
    return torch.stack([t[:, 1], t[:, 2] - sa.STAND_HEIGHT_CMD, d.root_link_pos_w[:, 2] - t[:, 2],
                        d.projected_gravity_b[:, 0] - torch.sin(t[:, 1])], -1)


def touch(env, sensor: str) -> torch.Tensor:
    return env.scene[sensor].data.found.view(env.num_envs, -1).any(-1)


def arm_touch(env, robot: str) -> torch.Tensor:
    """(2) the arm is touching the object; the trunk is touching the object."""
    return torch.stack([touch(env, f"arm_{robot}"), touch(env, f"trunk_{robot}")], -1).float()
