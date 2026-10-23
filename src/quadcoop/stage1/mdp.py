"""Stage 1 pieces: high-level action -> frozen walker, the push-to-goal task, rewards.

Control loop each env step (50 Hz):

    high-level policy action a in [-1, 1]^3
      -> velocity command (vx, vy, wz), clipped to what the walker was trained on and
         low-pass filtered
      -> written into the "twist" command the walker observes
      -> walker observation (exactly the Stage 0 actor observation) -> frozen walker
      -> 12 joint position targets -> PD -> physics

Only the high-level policy is trained. All goal geometry is planar: positions are
(x, y) and orientations are yaw about the vertical axis; box tilt is not a goal
coordinate, it only ends the episode if the box tips over.
"""

from __future__ import annotations

import math
import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

import torch
from mjlab.envs.mdp.actions import JointPositionActionCfg
from mjlab.managers.action_manager import ActionTerm, ActionTermCfg
from mjlab.managers.command_manager import CommandTerm, CommandTermCfg
from mjlab.utils.lab_api.math import quat_apply_inverse, quat_from_euler_xyz, yaw_quat

from quadcoop.stage1.objects import BOX_NAMES, BOX_SHAPE_INDEX, GOAL_NAMES, SHAPES
from quadcoop.stage1.walker_policy import FrozenWalker

if TYPE_CHECKING:
    from mjlab.envs import ManagerBasedRlEnv


# ---------------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------------
def wrap(a: torch.Tensor) -> torch.Tensor:
    return torch.atan2(torch.sin(a), torch.cos(a))


def yaw_of(q: torch.Tensor) -> torch.Tensor:
    """Yaw (rotation about world z) of wxyz quaternions."""
    w, x, y, z = q.unbind(-1)
    return torch.atan2(2.0 * (w * z + x * y), 1.0 - 2.0 * (y * y + z * z))


def tilt_of(q: torch.Tensor) -> torch.Tensor:
    """Angle between the body's z axis and world up (rad)."""
    w, x, y, z = q.unbind(-1)
    return torch.acos(torch.clamp(1.0 - 2.0 * (x * x + y * y), -1.0, 1.0))


def sym_error(err: torch.Tensor, symmetry: torch.Tensor) -> torch.Tensor:
    """Yaw error folded by the box's symmetry: a cube is 'there' at any multiple of 90 deg."""
    period = 2.0 * math.pi / symmetry
    return torch.remainder(err + period / 2, period) - period / 2


# ---------------------------------------------------------------------------------
# the command the walker sees
# ---------------------------------------------------------------------------------
class HighLevelTwist(CommandTerm):
    """Holds (vx, vy, wz); written by the walker action term, never resampled."""

    def __init__(self, cfg: HighLevelTwistCfg, env: ManagerBasedRlEnv):
        super().__init__(cfg, env)
        self.vel_command_b = torch.zeros(self.num_envs, 3, device=self.device)

    @property
    def command(self) -> torch.Tensor:
        return self.vel_command_b

    def _update_metrics(self) -> None:
        pass

    def _resample_command(self, env_ids: torch.Tensor) -> None:
        self.vel_command_b[env_ids] = 0.0

    def _update_command(self) -> None:
        pass


@dataclass(kw_only=True)
class HighLevelTwistCfg(CommandTermCfg):
    resampling_time_range: tuple[float, float] = (1e9, 1e9)

    def build(self, env: ManagerBasedRlEnv) -> HighLevelTwist:
        return HighLevelTwist(self, env)


# ---------------------------------------------------------------------------------
# high-level action -> frozen walker -> joints
# ---------------------------------------------------------------------------------
def _check_walker_gains(path: str, env) -> None:
    """Refuse a walker trained with different joint gains than this env's robot.

    The walker's actions only make sense with the PD gains (and action scale, which follows
    them) it was trained with. Its run folder keeps params/env.yaml; the gains saved there
    must match. Matters for Spot, whose gains are selected by QUADCOOP_SPOT_PROFILE."""
    import re as _re

    yml = Path(path).resolve().parent / "params" / "env.yaml"
    if not yml.exists():
        print(f"[stage1] note: {yml} not found, cannot check the walker's joint gains")
        return
    m = _re.search(r"stiffness: ([0-9.eE+-]+)\s*\n\s*damping: ([0-9.eE+-]+)", yml.read_text())
    if m is None:
        return
    saved = (float(m.group(1)), float(m.group(2)))
    act = env.scene["robot"].cfg.articulation.actuators[0]
    now = (float(act.stiffness), float(act.damping))
    if any(abs(a - b) > 1e-6 * max(1.0, abs(b)) for a, b in zip(saved, now, strict=True)):
        raise RuntimeError(
            f"walker {path} was trained with kp={saved[0]:g}, kd={saved[1]:g} but this robot has "
            f"kp={now[0]:g}, kd={now[1]:g}. For Spot set QUADCOOP_SPOT_PROFILE to the profile the "
            f"walker was trained with (see quadcoop/robots/spot.py).")


class WalkerCommandAction(ActionTerm):
    cfg: WalkerCommandActionCfg

    def __init__(self, cfg: WalkerCommandActionCfg, env: ManagerBasedRlEnv):
        super().__init__(cfg, env)
        self._joint = cfg.joint_cfg.build(env)
        path = cfg.checkpoint or os.environ.get(cfg.checkpoint_env, "")
        if not path:
            raise RuntimeError(
                f"No walker checkpoint: set {cfg.checkpoint_env}=/path/to/model_<iter>.pt "
                f"(the Stage 0 checkpoint for this robot).")
        self.walker = FrozenWalker(path, self.device)
        _check_walker_gains(path, env)
        if self.walker.act_dim != self._joint.action_dim:
            raise RuntimeError(f"walker outputs {self.walker.act_dim} actions, robot has "
                               f"{self._joint.action_dim} joints: wrong checkpoint for this robot?")
        print(f"[stage1] frozen walker: {path} (iter {self.walker.iteration}, "
              f"obs {self.walker.obs_dim}, act {self.walker.act_dim})")
        n = self.num_envs
        self._raw = torch.zeros(n, 3, device=self.device)
        self.walker_action = torch.zeros(n, self.walker.act_dim, device=self.device)
        self._lo = torch.tensor([cfg.vx_range[0], cfg.vy_range[0], cfg.wz_range[0]], device=self.device)
        self._hi = torch.tensor([cfg.vx_range[1], cfg.vy_range[1], cfg.wz_range[1]], device=self.device)
        self._checked = False

    @property
    def action_dim(self) -> int:
        return 3

    @property
    def raw_action(self) -> torch.Tensor:
        return self._raw

    def target_command(self, a: torch.Tensor) -> torch.Tensor:
        a = torch.clamp(a, -1.0, 1.0)
        return self._lo + (a + 1.0) * 0.5 * (self._hi - self._lo)

    def process_actions(self, actions: torch.Tensor) -> None:
        self._raw[:] = actions
        twist = self._env.command_manager.get_term(self.cfg.twist_name)
        s = self.cfg.smoothing
        twist.vel_command_b[:] = (1.0 - s) * twist.vel_command_b + s * self.target_command(actions)
        obs = self._env.observation_manager.compute_group(self.cfg.walker_obs_group)
        if not self._checked:
            if obs.shape[-1] != self.walker.obs_dim:
                raise RuntimeError(f"walker observation has {obs.shape[-1]} dims, checkpoint "
                                   f"expects {self.walker.obs_dim}")
            self._checked = True
        act = self.walker(obs)
        self.walker_action[:] = act
        self._joint.process_actions(act)

    def apply_actions(self) -> None:
        self._joint.apply_actions()

    def reset(self, env_ids: torch.Tensor | slice | None = None) -> None:
        self._joint.reset(env_ids)
        self._raw[env_ids] = 0.0
        self.walker_action[env_ids] = 0.0


@dataclass(kw_only=True)
class WalkerCommandActionCfg(ActionTermCfg):
    joint_cfg: JointPositionActionCfg
    checkpoint: str = ""  # path; empty -> read from the env var below
    checkpoint_env: str = "QUADCOOP_WALKER_CKPT"
    twist_name: str = "twist"
    walker_obs_group: str = "walker"
    # Inside what the Stage 0 walkers were trained on (and slow enough to push).
    vx_range: tuple[float, float] = (-0.6, 0.8)
    vy_range: tuple[float, float] = (-0.5, 0.5)
    wz_range: tuple[float, float] = (-0.7, 0.7)
    smoothing: float = 0.3  # share of the new target taken each step (50 Hz)

    def build(self, env: ManagerBasedRlEnv) -> WalkerCommandAction:
        return WalkerCommandAction(self, env)


def walker_last_action(env: ManagerBasedRlEnv, action_name: str = "walker") -> torch.Tensor:
    """The walker's own previous joint action (its 'actions' observation term)."""
    return env.action_manager.get_term(action_name).walker_action


# ---------------------------------------------------------------------------------
# the task: one box in front, a goal pose on the floor
# ---------------------------------------------------------------------------------
class PushGoalCommand(CommandTerm):
    """Places the robot's box and the goal at every reset, tracks progress and success.

    Box: ahead of the robot (a little left or right), roughly square to it.
    Goal: further ahead of the box, offset left/right, with a yaw change. How far,
    how far to the side and how much yaw all grow with the curriculum ``level``.
    """

    cfg: PushGoalCommandCfg

    def __init__(self, cfg: PushGoalCommandCfg, env: ManagerBasedRlEnv):
        super().__init__(cfg, env)
        n, dev = self.num_envs, self.device
        self.robot = env.scene["robot"]
        self.boxes = [env.scene[name] for name in BOX_NAMES]
        self.goals = [env.scene[name] for name in GOAL_NAMES]
        self.box_shape = torch.tensor(BOX_SHAPE_INDEX, device=dev)
        self.shape_half = torch.tensor([s.half for s in SHAPES], device=dev)  # (S, 3)
        self.shape_sym = torch.tensor([float(s.symmetry) for s in SHAPES], device=dev)
        self.box_idx = torch.zeros(n, dtype=torch.long, device=dev)
        self.shape = torch.zeros(n, dtype=torch.long, device=dev)
        self.goal_xy = torch.zeros(n, 2, device=dev)
        self.goal_yaw = torch.zeros(n, device=dev)
        self.env_level = torch.zeros(n, dtype=torch.long, device=dev)
        self.prev_dist = torch.zeros(n, device=dev)
        self.prev_yaw_err = torch.zeros(n, device=dev)
        self.in_goal_time = torch.zeros(n, device=dev)
        # Curriculum state (written by push_curriculum).
        self.level = cfg.start_level
        self.mass_window = cfg.mass_window_start
        self.ema_success = 0.0
        self.last_change_iter = 0.0
        for k in ("success", "pos_err", "yaw_err_deg", "level"):
            self.metrics[k] = torch.zeros(n, device=dev)

    # -- state of the active box ----------------------------------------------------
    def _gather(self, field_name: str) -> torch.Tensor:
        data = torch.stack([getattr(b.data, field_name) for b in self.boxes], dim=1)
        return data[torch.arange(self.num_envs, device=self.device), self.box_idx]

    def box_pos(self) -> torch.Tensor:
        return self._gather("root_link_pos_w")

    def box_quat(self) -> torch.Tensor:
        return self._gather("root_link_quat_w")

    def box_vel(self) -> torch.Tensor:
        return self._gather("root_link_lin_vel_w")

    def box_ang_vel(self) -> torch.Tensor:
        return self._gather("root_link_ang_vel_w")

    def symmetry(self) -> torch.Tensor:
        return self.shape_sym[self.shape]

    def half(self) -> torch.Tensor:
        return self.shape_half[self.shape]

    def errors(self) -> tuple[torch.Tensor, torch.Tensor]:
        """(distance box->goal in m, symmetry-folded yaw error in rad)."""
        d = torch.linalg.norm(self.goal_xy - self.box_pos()[:, :2], dim=-1)
        e = sym_error(wrap(self.goal_yaw - yaw_of(self.box_quat())), self.symmetry())
        return d, e

    def success_now(self) -> torch.Tensor:
        d, e = self.errors()
        return (d < self.cfg.pos_tol) & (e.abs() < math.radians(self.cfg.yaw_tol_deg))

    @property
    def command(self) -> torch.Tensor:
        """Goal relative to the robot (yaw frame): x, y, and the folded yaw error."""
        rel = torch.zeros(self.num_envs, 3, device=self.device)
        rel[:, :2] = self.goal_xy - self.robot.data.root_link_pos_w[:, :2]
        rel_b = quat_apply_inverse(yaw_quat(self.robot.data.root_link_quat_w), rel)
        _, e = self.errors()
        return torch.stack([rel_b[:, 0], rel_b[:, 1], e], dim=-1)

    # -- CommandTerm hooks -----------------------------------------------------------
    def _update_metrics(self) -> None:
        d, e = self.errors()
        self.metrics["pos_err"][:] = d
        self.metrics["yaw_err_deg"][:] = torch.rad2deg(e.abs())
        self.metrics["success"][:] = torch.maximum(self.metrics["success"],
                                                   self.success_now().float())
        self.metrics["level"][:] = self.env_level.float()

    def _update_command(self) -> None:
        d, e = self.errors()
        self.prev_dist[:] = d
        self.prev_yaw_err[:] = e.abs()

    def _resample_command(self, env_ids: torch.Tensor) -> None:
        c, dev = self.cfg, self.device
        m = len(env_ids)
        if m == 0:
            return
        self.metrics["success"][env_ids] = 0.0

        # Level per env: the current level, with some envs replaying easier ones.
        lvl = torch.full((m,), self.level, dtype=torch.long, device=dev)
        replay = torch.rand(m, device=dev) < c.replay_frac
        lvl = torch.where(replay, torch.randint(0, self.level + 1, (m,), device=dev), lvl)
        self.env_level[env_ids] = lvl
        table = torch.tensor(c.levels, device=dev)[lvl]  # (m, 4): d_lo, d_hi, lat, yaw_deg

        # Shape, then a copy of that shape whose mass is in the curriculum window.
        shape = torch.randint(0, len(SHAPES), (m,), device=dev)
        masses = torch.stack(
            [self._env.sim.model.body_mass[env_ids, b.indexing.body_ids[0]] for b in self.boxes], -1
        )  # (m, B)
        lo, hi = self.mass_window
        of_shape = self.box_shape.unsqueeze(0) == shape.unsqueeze(1)  # (m, B)
        in_window = (masses >= lo) & (masses <= hi) & of_shape
        mid = 0.5 * (lo + hi)
        score = torch.where(in_window, torch.rand_like(masses) + 10.0,  # any in-window copy
                            torch.where(of_shape, -(masses - mid).abs(), torch.full_like(masses, -1e9)))
        box = score.argmax(-1)
        self.box_idx[env_ids] = box
        self.shape[env_ids] = shape
        half = self.shape_half[shape]  # (m, 3)

        # Robot pose (qpos: always current, even inside reset).
        q_adr = self.robot.indexing.free_joint_q_adr
        qpos = self.robot.data.data.qpos[env_ids]
        root = qpos[:, q_adr[0:3]]
        ryaw = yaw_of(qpos[:, q_adr[3:7]])
        u = torch.stack([torch.cos(ryaw), torch.sin(ryaw)], -1)
        v = torch.stack([-torch.sin(ryaw), torch.cos(ryaw)], -1)

        def U(lo_hi, k=m):
            return torch.empty(k, device=dev).uniform_(*lo_hi)

        # Box: just ahead of the robot, a little to the side, roughly square to it.
        ahead = c.robot_reach + half[:, 0] + U(c.box_gap)
        box_xy = root[:, :2] + ahead.unsqueeze(-1) * u + U(c.box_lateral).unsqueeze(-1) * v
        box_yaw = ryaw + U((-c.box_yaw_jitter, c.box_yaw_jitter))

        # Goal: further ahead of the box, off to a side, with a yaw change.
        r = torch.rand(m, device=dev)
        fwd = table[:, 0] + r * (table[:, 1] - table[:, 0])
        lat = (torch.rand(m, device=dev) * 2 - 1) * table[:, 2]
        yaw_max = torch.minimum(torch.deg2rad(table[:, 3]),
                                (math.pi / self.shape_sym[shape]) * c.max_yaw_frac_of_symmetry)
        dyaw = (torch.rand(m, device=dev) * 2 - 1) * yaw_max
        self.goal_xy[env_ids] = box_xy + fwd.unsqueeze(-1) * u + lat.unsqueeze(-1) * v
        self.goal_yaw[env_ids] = wrap(box_yaw + dyaw)

        # Write the boxes: the chosen one in place, the rest parked far away.
        zeros = torch.zeros(m, device=dev)
        box_quat = quat_from_euler_xyz(zeros, zeros, box_yaw)
        for k, b in enumerate(self.boxes):
            sk = BOX_SHAPE_INDEX[k]
            pos = torch.zeros(m, 3, device=dev)
            pos[:, :2] = torch.where((box == k).unsqueeze(-1), box_xy,
                                     root[:, :2] + torch.tensor([30.0 + 3.0 * k, 0.0], device=dev))
            pos[:, 2] = SHAPES[sk].half[2] + 0.005
            st = torch.zeros(m, 13, device=dev)
            st[:, :3] = pos
            st[:, 3:7] = box_quat
            b.write_root_state_to_sim(st, env_ids)

        # Move the goal marker of this shape to the goal; hide the other one.
        gquat = quat_from_euler_xyz(zeros, zeros, self.goal_yaw[env_ids])
        for s, g in enumerate(self.goals):
            pose = torch.zeros(m, 7, device=dev)
            pose[:, :2] = self.goal_xy[env_ids]
            pose[:, 2] = torch.where(shape == s, torch.full_like(zeros, 0.002), torch.full_like(zeros, -5.0))
            pose[:, 3:7] = gquat
            g.write_mocap_pose_to_sim(pose, env_ids)

        # Progress terms start from the initial errors.
        d0 = torch.linalg.norm(self.goal_xy[env_ids] - box_xy, dim=-1)
        e0 = sym_error(wrap(self.goal_yaw[env_ids] - box_yaw), self.shape_sym[shape]).abs()
        self.prev_dist[env_ids] = d0
        self.prev_yaw_err[env_ids] = e0


@dataclass(kw_only=True)
class PushGoalCommandCfg(CommandTermCfg):
    resampling_time_range: tuple[float, float] = (1e9, 1e9)  # one task per episode
    robot_reach: float = 0.55  # robot body half-length (m); set per robot
    box_gap: tuple[float, float] = (0.15, 0.40)  # clear gap robot -> box at the start
    box_lateral: tuple[float, float] = (-0.25, 0.25)
    box_yaw_jitter: float = 0.15
    # Curriculum levels: (goal ahead of box min, max [m], goal side offset +- [m],
    # goal yaw change +- [deg]). Yaw is further capped by the box symmetry.
    levels: tuple[tuple[float, float, float, float], ...] = (
        (0.8, 1.2, 0.3, 10.0),
        (1.0, 1.6, 0.6, 20.0),
        (1.2, 2.2, 1.0, 30.0),
        (1.5, 2.8, 1.5, 45.0),
        (2.0, 3.5, 2.0, 60.0),
        (2.5, 4.5, 2.5, 90.0),
    )
    start_level: int = 0
    replay_frac: float = 0.2  # envs that replay an easier level
    max_yaw_frac_of_symmetry: float = 0.9  # cube: <= 40 deg, long box: <= 81 deg
    pos_tol: float = 0.20  # m
    yaw_tol_deg: float = 12.0
    mass_window_start: tuple[float, float] = (6.0, 12.0)  # kg, until the task is learned
    mass_window_final: tuple[float, float] = (3.0, 25.0)

    def build(self, env: ManagerBasedRlEnv) -> PushGoalCommand:
        return PushGoalCommand(self, env)


# ---------------------------------------------------------------------------------
# observations (all in the robot's yaw frame)
# ---------------------------------------------------------------------------------
def _goal(env) -> PushGoalCommand:
    return env.command_manager.get_term("goal")


def _to_robot(env, vec_w: torch.Tensor) -> torch.Tensor:
    robot = env.scene["robot"]
    v = torch.zeros(vec_w.shape[0], 3, device=env.device)
    v[:, :2] = vec_w[:, :2]
    return quat_apply_inverse(yaw_quat(robot.data.root_link_quat_w), v)[:, :2]


def box_in_robot_frame(env: ManagerBasedRlEnv) -> torch.Tensor:
    """Box position (2), box yaw rel. robot folded by symmetry as sin/cos (2),
    box velocity (2), box yaw rate (1)."""
    g = _goal(env)
    robot = env.scene["robot"]
    pos = _to_robot(env, g.box_pos() - robot.data.root_link_pos_w)
    rel_yaw = wrap(yaw_of(g.box_quat()) - yaw_of(robot.data.root_link_quat_w))
    k = g.symmetry()
    vel = _to_robot(env, g.box_vel())
    return torch.cat([pos, torch.sin(k * rel_yaw).unsqueeze(-1), torch.cos(k * rel_yaw).unsqueeze(-1),
                      vel, g.box_ang_vel()[:, 2:3]], dim=-1)


def goal_in_robot_frame(env: ManagerBasedRlEnv) -> torch.Tensor:
    """Goal rel. robot (2), goal rel. box (2), folded yaw error: sin/cos(k e) and e/(pi/k) (3)."""
    g = _goal(env)
    robot = env.scene["robot"]
    to_goal = _to_robot(env, torch.cat([g.goal_xy, torch.zeros_like(g.goal_yaw).unsqueeze(-1)], -1)
                        - robot.data.root_link_pos_w)
    box_to_goal = _to_robot(env, torch.cat([g.goal_xy - g.box_pos()[:, :2],
                                            torch.zeros_like(g.goal_yaw).unsqueeze(-1)], -1))
    _, e = g.errors()
    k = g.symmetry()
    return torch.cat([to_goal, box_to_goal, torch.sin(k * e).unsqueeze(-1),
                      torch.cos(k * e).unsqueeze(-1), (e / (math.pi / k)).unsqueeze(-1)], dim=-1)


def box_shape_obs(env: ManagerBasedRlEnv) -> torch.Tensor:
    """One-hot shape (S) and half extents x, y (2)."""
    g = _goal(env)
    onehot = torch.nn.functional.one_hot(g.shape, len(SHAPES)).float()
    return torch.cat([onehot, g.half()[:, :2]], dim=-1)


def walker_command(env: ManagerBasedRlEnv) -> torch.Tensor:
    return env.command_manager.get_command("twist")


def box_physics(env: ManagerBasedRlEnv) -> torch.Tensor:
    """Privileged (critic): mass [kg / 10], ground friction, curriculum level of the env."""
    g = _goal(env)
    ids = torch.arange(env.num_envs, device=env.device)
    body = torch.tensor([b.indexing.body_ids[0] for b in g.boxes], device=env.device)[g.box_idx]
    geom = torch.tensor([b.indexing.geom_ids[0] for b in g.boxes], device=env.device)[g.box_idx]
    mass = env.sim.model.body_mass[ids, body] / 10.0
    mu = env.sim.model.geom_friction[ids, geom, 0] if env.sim.model.geom_friction.dim() == 3 \
        else env.sim.model.geom_friction[geom, 0]
    return torch.stack([mass, mu, g.env_level.float()], dim=-1)


# ---------------------------------------------------------------------------------
# rewards
# ---------------------------------------------------------------------------------
def box_progress(env: ManagerBasedRlEnv) -> torch.Tensor:
    """Speed of the box toward the goal (m/s), clipped to [-1, 1]."""
    g = _goal(env)
    d, _ = g.errors()
    return torch.clamp((g.prev_dist - d) / env.step_dt, -1.0, 1.0)


def box_near_goal(env: ManagerBasedRlEnv, std: float = 1.0) -> torch.Tensor:
    d, _ = _goal(env).errors()
    return 1.0 - torch.tanh(d / std)


def yaw_progress(env: ManagerBasedRlEnv, gate_dist: float = 1.5) -> torch.Tensor:
    """Rate of reduction of the folded yaw error (rad/s), only once the box is close-ish."""
    g = _goal(env)
    d, e = g.errors()
    rate = torch.clamp((g.prev_yaw_err - e.abs()) / env.step_dt, -1.0, 1.0)
    return torch.where(d < gate_dist, rate, torch.zeros_like(rate))


def yaw_aligned(env: ManagerBasedRlEnv, std: float = 0.3, dist_scale: float = 1.0) -> torch.Tensor:
    d, e = _goal(env).errors()
    return (1.0 - torch.tanh(e.abs() / std)) * torch.exp(-d / dist_scale)


def robot_near_box(env: ManagerBasedRlEnv, std: float = 0.5) -> torch.Tensor:
    """Pulls the robot to the box: 1 at contact distance, falls off beyond."""
    g = _goal(env)
    robot = env.scene["robot"]
    dist = torch.linalg.norm(g.box_pos()[:, :2] - robot.data.root_link_pos_w[:, :2], dim=-1)
    reach = g.cfg.robot_reach + g.half()[:, :2].max(dim=-1).values
    return 1.0 - torch.tanh(torch.clamp(dist - reach, min=0.0) / std)


def robot_behind_box(env: ManagerBasedRlEnv, done_dist: float = 0.25) -> torch.Tensor:
    """Robot on the far side of the box from the goal (where pushing moves it the right way)."""
    g = _goal(env)
    robot = env.scene["robot"]
    to_box = g.box_pos()[:, :2] - robot.data.root_link_pos_w[:, :2]
    to_goal = g.goal_xy - g.box_pos()[:, :2]
    cos = (to_box * to_goal).sum(-1) / (torch.linalg.norm(to_box, dim=-1) *
                                        torch.linalg.norm(to_goal, dim=-1)).clamp(min=1e-6)
    d, _ = g.errors()
    return torch.where(d > done_dist, cos.clamp(min=0.0), torch.zeros_like(cos))


def at_goal(env: ManagerBasedRlEnv) -> torch.Tensor:
    return _goal(env).success_now().float()


def hl_action_rate(env: ManagerBasedRlEnv) -> torch.Tensor:
    return torch.sum(torch.square(env.action_manager.action - env.action_manager.prev_action), dim=-1)


# ---------------------------------------------------------------------------------
# terminations
# ---------------------------------------------------------------------------------
def box_tipped(env: ManagerBasedRlEnv, limit_deg: float = 30.0) -> torch.Tensor:
    return tilt_of(_goal(env).box_quat()) > math.radians(limit_deg)


def box_lost(env: ManagerBasedRlEnv, max_dist: float = 6.0) -> torch.Tensor:
    g = _goal(env)
    robot = env.scene["robot"]
    return torch.linalg.norm(g.box_pos()[:, :2] - robot.data.root_link_pos_w[:, :2], dim=-1) > max_dist


# ---------------------------------------------------------------------------------
# curriculum
# ---------------------------------------------------------------------------------
def push_curriculum(
    env: ManagerBasedRlEnv,
    env_ids: torch.Tensor,
    advance: float = 0.6,
    retreat: float = 0.15,
    dwell_iters: int = 50,
    ema: float = 0.02,
    mass_level: int = 3,
    mass_success: float = 0.5,
    steps_per_iter: int = 24,
) -> dict[str, torch.Tensor]:
    """Moves the global level on the success rate of envs playing the current level.

    Mass variety is switched on only after the task itself is learned (level >= mass_level
    with success >= mass_success): first learn to push to a pose, then to do it with
    light and heavy boxes.
    """
    g = _goal(env)
    it = env.common_step_counter / steps_per_iter
    if isinstance(env_ids, torch.Tensor) and len(env_ids) > 0:
        at_level = g.env_level[env_ids] == g.level
        if at_level.any():
            s = float(g.metrics["success"][env_ids][at_level].mean())
            w = min(1.0, ema * int(at_level.sum()))
            g.ema_success = (1 - w) * g.ema_success + w * s
            if it - g.last_change_iter >= dwell_iters:
                if g.ema_success > advance and g.level < len(g.cfg.levels) - 1:
                    g.level += 1
                    g.last_change_iter = it
                    g.ema_success = 0.5 * advance  # don't jump two levels on stale evidence
                elif g.ema_success < retreat and g.level > 0:
                    g.level -= 1
                    g.last_change_iter = it
                    g.ema_success = 0.5 * (advance + retreat)
            if (g.mass_window == g.cfg.mass_window_start and g.level >= mass_level
                    and g.ema_success >= mass_success):
                g.mass_window = g.cfg.mass_window_final
    return {
        "level": torch.tensor(float(g.level)),
        "success_ema": torch.tensor(g.ema_success),
        "mass_max": torch.tensor(float(g.mass_window[1])),
    }