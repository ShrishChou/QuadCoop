"""Two-robot task: ANYmal C and Spot move one object to a goal pose together.

The object, goal, success rule (held inside the tolerance) and object rewards are
Stage 1b's: ``CoopGoalCommand`` keeps the ``HardGoalCommand`` interface, so the
Stage 1b object rewards and observations (``quadcoop.stage1b.mdp``) work unchanged.
What is new:

* two robots, placed on the far side of the object from the goal (spread around it
  more as the level rises), never closer than ``min_separation_deg`` to each other;
* robot-specific observations take the robot's entity name (``robot="anymal"``) and
  are expressed in that robot's frame, exactly like Stage 1b's, plus the partner's
  pose and velocity in the robot's frame;
* heavier objects (the mass window rises to well past what one robot can push);
* per-robot effort (mechanical power), available to the trainer for an individual
  effort cost.

Entity names: "anymal" and "spot". Agent order everywhere: (anymal, spot).
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import torch
from mjlab.managers.command_manager import CommandTerm
from mjlab.utils.lab_api.math import quat_apply_inverse, quat_from_euler_xyz, yaw_quat

from quadcoop.stage1.mdp import wrap, yaw_of
from quadcoop.stage1b.mdp import (
    BOX_YAW,
    D_HI,
    D_LO,
    DYAW,
    GOAL_DIR,
    MASS_HI,
    HardGoalCommand,
    HardGoalCommandCfg,
    fold,
)
from quadcoop.stage1b.shapes import GOAL_NAMES, OBJ_NAMES, SHAPES

AGENTS = ("anymal", "spot")
SPREAD = 2  # level-table column 2 (Stage 1b's "bearing"): robots' spread around "behind", +- deg
MASS_LO = 10  # extra column: lightest object at this level (kg)


class CoopGoalCommand(HardGoalCommand):
    cfg: CoopGoalCommandCfg

    def __init__(self, cfg: CoopGoalCommandCfg, env):
        CommandTerm.__init__(self, cfg, env)
        n, dev = self.num_envs, self.device
        self.robots = {a: env.scene[a] for a in AGENTS}
        self.robot = self.robots[AGENTS[0]]  # unused by the inherited methods; kept for safety
        self.objs = [env.scene[name] for name in OBJ_NAMES]
        self.goals = [env.scene[name] for name in GOAL_NAMES]
        S = len(SHAPES)
        self.sym = torch.tensor([float(s.symmetry) for s in SHAPES], device=dev)
        self.roller = torch.tensor([s.roller for s in SHAPES], device=dev)
        self.axis_y = torch.tensor([s.heading_axis_y for s in SHAPES], device=dev)
        self.radius = torch.tensor([s.radius() for s in SHAPES], device=dev)
        self.bbox = torch.tensor([s.bbox_half() for s in SHAPES], device=dev)
        self.rest_h = torch.tensor([s.rest_height for s in SHAPES], device=dev)
        self.table = torch.tensor(cfg.levels, device=dev)
        self.shape = torch.zeros(n, dtype=torch.long, device=dev)
        self.goal_xy = torch.zeros(n, 2, device=dev)
        self.goal_yaw = torch.zeros(n, device=dev)
        self.env_level = torch.zeros(n, dtype=torch.long, device=dev)
        self.prev_dist = torch.zeros(n, device=dev)
        self.prev_yaw_err = torch.zeros(n, device=dev)
        self.in_goal_time = torch.zeros(n, device=dev)
        self.level = cfg.start_level
        self.ema_success = 0.0
        self.last_change_iter = 0.0
        for k in ("success", "pos_err", "yaw_err_deg", "level", "hold_frac"):
            self.metrics[k] = torch.zeros(n, device=dev)
        self.shape_success = torch.zeros(S, device=dev)
        # Eval hook: if set, (m,) -> placement override; see scripts/eval_coop.py.
        self.scenario = None

    @property
    def command(self) -> torch.Tensor:
        _, e = self.errors()
        z = torch.zeros(self.num_envs, 1, device=self.device)
        return torch.cat([self.goal_xy, e.unsqueeze(-1), z], -1)

    # -- placement ------------------------------------------------------------------------
    def _resample_command(self, env_ids: torch.Tensor) -> None:
        c, dev = self.cfg, self.device
        m = len(env_ids)
        if m == 0:
            return
        self.metrics["success"][env_ids] = 0.0
        self.in_goal_time[env_ids] = 0.0

        lvl = torch.full((m,), self.level, dtype=torch.long, device=dev)
        replay = torch.rand(m, device=dev) < c.replay_frac
        lvl = torch.where(replay, torch.randint(0, self.level + 1, (m,), device=dev), lvl)
        self.env_level[env_ids] = lvl
        t = self.table[lvl]

        # Shape: uniform among shapes whose (per-env, fixed) mass is inside the level's window.
        masses = torch.stack([self._env.sim.model.body_mass[env_ids, o.indexing.body_ids[0]]
                              for o in self.objs], -1)
        ok = (masses >= t[:, MASS_LO].unsqueeze(-1)) & (masses <= t[:, MASS_HI].unsqueeze(-1))
        if c.only is not None:
            ok &= torch.tensor([nm == c.only for nm in OBJ_NAMES], device=dev).unsqueeze(0)
        score = torch.where(ok, torch.rand_like(masses) + 10.0, -(masses - t[:, MASS_LO:MASS_LO + 1]).abs())
        if c.only is not None:
            only = torch.tensor([nm == c.only for nm in OBJ_NAMES], device=dev).unsqueeze(0)
            score = torch.where(only, score, torch.full_like(score, -1e9))
        shape = score.argmax(-1)
        sc = self.scenario(env_ids) if self.scenario is not None else None  # eval: exact scenario
        if sc is not None and "shape" in sc:
            shape = sc["shape"]
        self.shape[env_ids] = shape

        def U(lo, hi):
            return lo + torch.rand(m, device=dev) * (hi - lo)

        def sym_u(half_deg):
            return torch.deg2rad(half_deg) * (2 * torch.rand(m, device=dev) - 1)

        origin = self._env.scene.env_origins[env_ids][:, :2]
        obj_xy = origin.clone()
        gdir = 2 * math.pi * torch.rand(m, device=dev)  # world direction object -> goal
        obj_heading = gdir + sym_u(t[:, BOX_YAW])
        gd = U(t[:, D_LO], t[:, D_HI])
        goal_xy = obj_xy + gd.unsqueeze(-1) * torch.stack([torch.cos(gdir), torch.sin(gdir)], -1)
        cap = torch.where(self.sym[shape] > 0, (math.pi / self.sym[shape].clamp(min=1)) * c.max_yaw_frac_of_symmetry,
                          torch.zeros_like(gd))
        dyaw = torch.minimum(torch.deg2rad(t[:, DYAW]), cap) * (2 * torch.rand(m, device=dev) - 1)
        goal_yaw = wrap(obj_heading + dyaw)
        # GOAL_DIR (Stage 1b: goal direction rel. to the robot) here rotates the robots'
        # "behind" direction away from straight behind the object.
        behind = gdir + math.pi + sym_u(t[:, GOAL_DIR])

        # Robots: around "behind", spread by the level, at least min_separation apart.
        b = [behind + sym_u(t[:, SPREAD]) for _ in AGENTS]
        sep = math.radians(c.min_separation_deg)
        diff = wrap(b[1] - b[0])
        side = torch.where(diff >= 0, torch.ones_like(diff), -torch.ones_like(diff))
        b[1] = torch.where(diff.abs() < sep, b[0] + side * sep, b[1])
        bearings = b
        if sc is not None:
            obj_xy, obj_heading, goal_xy, goal_yaw, bearings = (
                sc["obj_xy"], sc["obj_heading"], sc["goal_xy"], sc["goal_yaw"], sc["bearings"])

        self.goal_xy[env_ids] = goal_xy
        self.goal_yaw[env_ids] = goal_yaw
        zeros = torch.zeros(m, device=dev)
        for k, a in enumerate(AGENTS):
            robot = self.robots[a]
            dist = self.radius[shape] + c.reach[k] + U(c.gap[0], c.gap[1])
            if sc is not None and "gaps" in sc:
                dist = self.radius[shape] + c.reach[k] + sc["gaps"][k]
            pos = obj_xy + dist.unsqueeze(-1) * torch.stack([torch.cos(bearings[k]), torch.sin(bearings[k])], -1)
            yaw = bearings[k] + math.pi + (sym_u(torch.full((m,), c.robot_yaw_noise_deg, device=dev))
                                           if sc is None else zeros)
            q_adr = robot.indexing.free_joint_q_adr
            z = robot.data.data.qpos[env_ids][:, q_adr[2]]
            st = torch.zeros(m, 13, device=dev)
            st[:, :2] = pos
            st[:, 2] = z
            st[:, 3:7] = quat_from_euler_xyz(zeros, zeros, yaw)
            robot.write_root_state_to_sim(st, env_ids)

        obj_quat = quat_from_euler_xyz(zeros, zeros, obj_heading)
        for k, o in enumerate(self.objs):
            here = shape == k
            st = torch.zeros(m, 13, device=dev)
            st[:, :2] = torch.where(here.unsqueeze(-1), obj_xy,
                                    origin + torch.tensor([c.park_distance + 4.0 * k, 0.0], device=dev))
            st[:, 2] = float(SHAPES[k].rest_height) + 0.005
            st[:, 3:7] = obj_quat
            o.write_root_state_to_sim(st, env_ids)

        gquat = quat_from_euler_xyz(zeros, zeros, goal_yaw)
        for k, g in enumerate(self.goals):
            pose = torch.zeros(m, 7, device=dev)
            pose[:, :2] = goal_xy
            pose[:, 2] = torch.where(shape == k, torch.full_like(zeros, 0.002), torch.full_like(zeros, -5.0))
            pose[:, 3:7] = gquat
            g.write_mocap_pose_to_sim(pose, env_ids)

        self.prev_dist[env_ids] = torch.linalg.norm(goal_xy - obj_xy, dim=-1)
        self.prev_yaw_err[env_ids] = fold(wrap(goal_yaw - obj_heading), self.sym[shape]).abs()


@dataclass(kw_only=True)
class CoopGoalCommandCfg(HardGoalCommandCfg):
    reach: tuple[float, float] = (0.55, 0.55)  # body half-length per agent (anymal, spot)
    gap: tuple[float, float] = (0.3, 1.0)  # clear space body -> object at the start
    min_separation_deg: float = 55.0
    robot_yaw_noise_deg: float = 20.0
    # d_lo, d_hi [m] | robot spread +- [deg] | "behind" offset +- [deg] | object start
    # yaw +- | goal yaw change +- | pos tol [m] | yaw tol [deg] | hold [s] |
    # max mass [kg] | min mass [kg]
    levels: tuple[tuple[float, ...], ...] = (
        (1.0, 2.0, 40, 0, 20, 20, 0.20, 12, 0.0, 40, 10),
        (1.5, 3.0, 60, 20, 45, 45, 0.15, 10, 0.5, 60, 15),
        (2.0, 4.0, 75, 45, 90, 90, 0.15, 8, 0.5, 80, 20),
        (2.5, 5.0, 90, 90, 180, 135, 0.12, 7, 1.0, 100, 30),
        (3.0, 6.0, 90, 180, 180, 180, 0.10, 6, 1.0, 120, 40),
    )

    def build(self, env) -> CoopGoalCommand:
        return CoopGoalCommand(self, env)


# ---------------------------------------------------------------------------------
# observations, per robot (the robot's yaw frame), Stage 1b names and layouts
# ---------------------------------------------------------------------------------
def _g(env) -> CoopGoalCommand:
    return env.command_manager.get_term("goal")


def _to_frame(env, robot: str, v_w: torch.Tensor) -> torch.Tensor:
    v = torch.zeros(v_w.shape[0], 3, device=env.device)
    v[:, :2] = v_w[:, :2]
    return quat_apply_inverse(yaw_quat(env.scene[robot].data.root_link_quat_w), v)[:, :2]


def box_in_frame(env, robot: str) -> torch.Tensor:
    """Stage 1b's 7: object position (2), folded heading rel. robot (sin, cos), velocity (2), yaw rate."""
    g = _g(env)
    r = env.scene[robot]
    pos = _to_frame(env, robot, g.box_pos() - r.data.root_link_pos_w)
    rel = wrap(g.heading() - yaw_of(r.data.root_link_quat_w))
    k = g.symmetry()
    return torch.cat([pos, torch.sin(k * rel).unsqueeze(-1), torch.cos(k * rel).unsqueeze(-1),
                      _to_frame(env, robot, g.box_vel()), g.box_ang_vel()[:, 2:3]], dim=-1)


def goal_in_frame(env, robot: str) -> torch.Tensor:
    """Stage 1b's 7: goal rel. robot (2), goal rel. object (2), folded yaw error (3)."""
    g = _g(env)
    r = env.scene[robot]
    z = torch.zeros(env.num_envs, 1, device=env.device)
    to_goal = _to_frame(env, robot, torch.cat([g.goal_xy, z], -1) - r.data.root_link_pos_w)
    box_to_goal = _to_frame(env, robot, torch.cat([g.goal_xy - g.box_pos()[:, :2], z], -1))
    _, e = g.errors()
    k = g.symmetry()
    norm = torch.where(k > 0, e / (math.pi / k.clamp(min=1)), torch.zeros_like(e))
    return torch.cat([to_goal, box_to_goal, torch.sin(k * e).unsqueeze(-1),
                      torch.cos(k * e).unsqueeze(-1), norm.unsqueeze(-1)], dim=-1)


def partner_in_frame(env, robot: str, other: str) -> torch.Tensor:
    """New (6): partner position (2), partner heading rel. this robot (sin, cos), partner velocity (2)."""
    r, p = env.scene[robot], env.scene[other]
    pos = _to_frame(env, robot, p.data.root_link_pos_w - r.data.root_link_pos_w)
    rel = wrap(yaw_of(p.data.root_link_quat_w) - yaw_of(r.data.root_link_quat_w))
    return torch.cat([pos, torch.sin(rel).unsqueeze(-1), torch.cos(rel).unsqueeze(-1),
                      _to_frame(env, robot, p.data.root_link_lin_vel_w)], dim=-1)


def walker_command_of(env, twist_name: str) -> torch.Tensor:
    return env.command_manager.get_command(twist_name)


# ---------------------------------------------------------------------------------
# rewards (object terms come from stage1b.mdp; these are the per-robot ones)
# ---------------------------------------------------------------------------------
def robot_near_box(env, robot: str, reach: float, std: float = 0.5) -> torch.Tensor:
    g = _g(env)
    dist = torch.linalg.norm(g.box_pos()[:, :2] - env.scene[robot].data.root_link_pos_w[:, :2], dim=-1)
    return 1.0 - torch.tanh(torch.clamp(dist - reach - g.radius[g.shape], min=0.0) / std)


def robot_behind_box(env, robot: str, done_dist: float = 0.25) -> torch.Tensor:
    g = _g(env)
    to_box = g.box_pos()[:, :2] - env.scene[robot].data.root_link_pos_w[:, :2]
    to_goal = g.goal_xy - g.box_pos()[:, :2]
    cos = (to_box * to_goal).sum(-1) / (torch.linalg.norm(to_box, dim=-1) *
                                        torch.linalg.norm(to_goal, dim=-1)).clamp(min=1e-6)
    d, _ = g.errors()
    return torch.where(d > done_dist, cos.clamp(min=0.0), torch.zeros_like(cos))


def robots_touching(env, sensor_name: str = "robots_touch") -> torch.Tensor:
    return env.scene[sensor_name].data.found.view(env.num_envs, -1).any(-1).float()


def agent_action_rate(env, agent: int) -> torch.Tensor:
    am = env.action_manager
    sl = slice(3 * agent, 3 * agent + 3)  # actions are (anymal vx vy wz, spot vx vy wz)
    return torch.sum(torch.square(am.action[:, sl] - am.prev_action[:, sl]), dim=-1)


def effort(env, robot: str, weight_n: float) -> torch.Tensor:
    """Mechanical power of the robot's joints, |tau . qdot| summed, per (weight x 1 m/s)."""
    d = env.scene[robot].data
    return (d.qfrc_actuator * d.joint_vel).abs().sum(-1) / weight_n


def agent_effort(env) -> torch.Tensor:
    """(num_envs, 2) per-robot effort, for the trainer's individual effort cost."""
    from quadcoop.coop.env_cfg import ROBOT_WEIGHT_N

    return torch.stack([effort(env, a, ROBOT_WEIGHT_N[a]) for a in AGENTS], -1)


# ---------------------------------------------------------------------------------
# terminations
# ---------------------------------------------------------------------------------
def box_lost(env, max_dist: float = 12.0) -> torch.Tensor:
    g = _g(env)
    d = torch.stack([torch.linalg.norm(g.box_pos()[:, :2] - env.scene[a].data.root_link_pos_w[:, :2], dim=-1)
                     for a in AGENTS], -1)
    return d.min(-1).values > max_dist

