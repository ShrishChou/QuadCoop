"""Stage 1b task: harder push-to-pose with ten shapes, random starts and held success.

The robot-side machinery (high-level action -> frozen walker) is Stage 1's
(``quadcoop.stage1.mdp``). What changes is the task:

* The object is placed around the robot (bearing grows with the level), with a random
  starting yaw; the goal can lie in any direction from the object, so the robot has to
  walk to the right side of it first.
* Ten shapes, including rollers (sphere: position only; lying cylinder: rolls) and
  shapes that rotate when pushed off-centre (beam, L, T, arch, dumbbell, asym friction).
* Success = staying inside the position/yaw tolerance for ``hold_s`` seconds; the
  tolerance tightens and the hold lengthens with the level.
* The object mass window widens with the level, up to about what one robot can push.

All geometry is planar: positions are (x, y) and orientations are headings about the
vertical axis; tilt only matters for "did it tip over".
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import torch
from mjlab.managers.command_manager import CommandTerm, CommandTermCfg
from mjlab.utils.lab_api.math import quat_apply, quat_apply_inverse, quat_from_euler_xyz, yaw_quat

from quadcoop.stage1.mdp import wrap, yaw_of
from quadcoop.stage1b.shapes import GOAL_NAMES, OBJ_NAMES, SHAPES

if False:  # typing only
    from mjlab.envs import ManagerBasedRlEnv


def fold(err: torch.Tensor, symmetry: torch.Tensor) -> torch.Tensor:
    """Yaw error folded by symmetry; symmetry 0 (sphere) means any yaw is right."""
    k = symmetry.clamp(min=1.0)
    period = 2.0 * math.pi / k
    f = torch.remainder(err + period / 2, period) - period / 2
    return torch.where(symmetry > 0, f, torch.zeros_like(f))


# columns of the level table
D_LO, D_HI, BEARING, GOAL_DIR, BOX_YAW, DYAW, POS_TOL, YAW_TOL, HOLD, MASS_HI = range(10)


class HardGoalCommand(CommandTerm):
    cfg: HardGoalCommandCfg

    def __init__(self, cfg: HardGoalCommandCfg, env):
        super().__init__(cfg, env)
        n, dev = self.num_envs, self.device
        self.robot = env.scene["robot"]
        self.objs = [env.scene[name] for name in OBJ_NAMES]
        self.goals = [env.scene[name] for name in GOAL_NAMES]
        S = len(SHAPES)
        self.sym = torch.tensor([float(s.symmetry) for s in SHAPES], device=dev)
        self.roller = torch.tensor([s.roller for s in SHAPES], device=dev)
        self.axis_y = torch.tensor([s.heading_axis_y for s in SHAPES], device=dev)
        self.radius = torch.tensor([s.radius() for s in SHAPES], device=dev)
        self.bbox = torch.tensor([s.bbox_half() for s in SHAPES], device=dev)  # (S, 4)
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
        self.shape_success = torch.zeros(S, device=dev)  # EMA per shape (logged)

    # -- active object state --------------------------------------------------------------
    def _gather(self, attr: str) -> torch.Tensor:
        data = torch.stack([getattr(o.data, attr) for o in self.objs], dim=1)
        return data[torch.arange(self.num_envs, device=self.device), self.shape]

    def box_pos(self) -> torch.Tensor:
        return self._gather("root_link_pos_w")

    def box_quat(self) -> torch.Tensor:
        return self._gather("root_link_quat_w")

    def box_vel(self) -> torch.Tensor:
        return self._gather("root_link_lin_vel_w")

    def box_ang_vel(self) -> torch.Tensor:
        return self._gather("root_link_ang_vel_w")

    def symmetry(self) -> torch.Tensor:
        return self.sym[self.shape]

    def heading(self) -> torch.Tensor:
        """Yaw of the body x axis; for the lying cylinder, of its rolling axis (minus 90 deg)."""
        q = self.box_quat()
        ex = quat_apply(q, torch.tensor([1.0, 0.0, 0.0], device=self.device).expand_as(q[:, :3]))
        ey = quat_apply(q, torch.tensor([0.0, 1.0, 0.0], device=self.device).expand_as(q[:, :3]))
        hx = torch.atan2(ex[:, 1], ex[:, 0])
        hy = torch.atan2(ey[:, 1], ey[:, 0]) - math.pi / 2
        return wrap(torch.where(self.axis_y[self.shape], hy, hx))

    def tipped(self, limit_deg: float) -> torch.Tensor:
        q = self.box_quat()
        ez = quat_apply(q, torch.tensor([0.0, 0.0, 1.0], device=self.device).expand_as(q[:, :3]))
        ey = quat_apply(q, torch.tensor([0.0, 1.0, 0.0], device=self.device).expand_as(q[:, :3]))
        lim = math.sin(math.radians(limit_deg))
        upright_bad = ez[:, 2] < math.cos(math.radians(limit_deg))
        axis_bad = ey[:, 2].abs() > lim  # lying cylinder stood up on an end
        s = self.shape
        return torch.where(self.axis_y[s], axis_bad, torch.where(self.roller[s], torch.zeros_like(axis_bad),
                                                                 upright_bad))

    def errors(self) -> tuple[torch.Tensor, torch.Tensor]:
        d = torch.linalg.norm(self.goal_xy - self.box_pos()[:, :2], dim=-1)
        e = fold(wrap(self.goal_yaw - self.heading()), self.symmetry())
        return d, e

    def _tol(self):
        t = self.table[self.env_level]
        return t[:, POS_TOL], torch.deg2rad(t[:, YAW_TOL]), t[:, HOLD]

    def in_goal(self) -> torch.Tensor:
        d, e = self.errors()
        pt, yt, _ = self._tol()
        return (d < pt) & (e.abs() < yt)

    def success_now(self) -> torch.Tensor:
        """Inside the tolerance (the per-step reward); 'success' needs the hold too."""
        return self.in_goal()

    @property
    def command(self) -> torch.Tensor:
        rel = torch.zeros(self.num_envs, 3, device=self.device)
        rel[:, :2] = self.goal_xy - self.robot.data.root_link_pos_w[:, :2]
        rel_b = quat_apply_inverse(yaw_quat(self.robot.data.root_link_quat_w), rel)
        _, e = self.errors()
        return torch.stack([rel_b[:, 0], rel_b[:, 1], e], dim=-1)

    # -- hooks ---------------------------------------------------------------------------------
    def _update_metrics(self) -> None:
        d, e = self.errors()
        _, _, hold = self._tol()
        inside = self.in_goal()
        self.in_goal_time[:] = torch.where(inside, self.in_goal_time + self._env.step_dt,
                                           torch.zeros_like(self.in_goal_time))
        # in_goal_time is 0 whenever the object is outside the tolerance, so this needs
        # it inside for at least one step even when the level's hold is 0.
        done = self.in_goal_time >= hold.clamp(min=0.5 * self._env.step_dt)
        self.metrics["pos_err"][:] = d
        self.metrics["yaw_err_deg"][:] = torch.rad2deg(e.abs())
        self.metrics["success"][:] = torch.maximum(self.metrics["success"], done.float())
        self.metrics["hold_frac"][:] = torch.clamp(self.in_goal_time / hold.clamp(min=1e-3), max=1.0)
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
        self.in_goal_time[env_ids] = 0.0

        lvl = torch.full((m,), self.level, dtype=torch.long, device=dev)
        replay = torch.rand(m, device=dev) < c.replay_frac
        lvl = torch.where(replay, torch.randint(0, self.level + 1, (m,), device=dev), lvl)
        self.env_level[env_ids] = lvl
        t = self.table[lvl]

        # Shape: uniform among shapes whose (per-env, fixed) mass is inside the window.
        masses = torch.stack([self._env.sim.model.body_mass[env_ids, o.indexing.body_ids[0]]
                              for o in self.objs], -1)  # (m, S)
        ok = (masses >= c.mass_lo) & (masses <= t[:, MASS_HI].unsqueeze(-1))
        if c.only is not None:
            ok &= torch.tensor([n == c.only for n in OBJ_NAMES], device=dev).unsqueeze(0)
        score = torch.where(ok, torch.rand_like(masses) + 10.0, -masses)  # none ok -> lightest
        if c.only is not None:
            only = torch.tensor([n == c.only for n in OBJ_NAMES], device=dev).unsqueeze(0)
            score = torch.where(only, score, torch.full_like(score, -1e9))
        shape = score.argmax(-1)
        self.shape[env_ids] = shape

        q_adr = self.robot.indexing.free_joint_q_adr
        qpos = self.robot.data.data.qpos[env_ids]
        root = qpos[:, q_adr[0:3]]
        ryaw = yaw_of(qpos[:, q_adr[3:7]])

        def U(lo, hi):
            return lo + torch.rand(m, device=dev) * (hi - lo)

        def sym_u(half_deg):
            return torch.deg2rad(half_deg) * (2 * torch.rand(m, device=dev) - 1)

        # Object around the robot, outside its body.
        bearing = ryaw + sym_u(t[:, BEARING])
        dist = c.robot_reach + self.radius[shape] + U(c.gap[0], c.gap[1])
        obj_xy = root[:, :2] + dist.unsqueeze(-1) * torch.stack([torch.cos(bearing), torch.sin(bearing)], -1)
        obj_heading = bearing + sym_u(t[:, BOX_YAW])
        # Goal: from the object, in a direction rotated from "straight away from the robot".
        gdir = bearing + sym_u(t[:, GOAL_DIR])
        gd = U(t[:, D_LO], t[:, D_HI])
        self.goal_xy[env_ids] = obj_xy + gd.unsqueeze(-1) * torch.stack([torch.cos(gdir), torch.sin(gdir)], -1)
        cap = torch.where(self.sym[shape] > 0, (math.pi / self.sym[shape].clamp(min=1)) * c.max_yaw_frac_of_symmetry,
                          torch.zeros_like(gd))
        dyaw = torch.minimum(torch.deg2rad(t[:, DYAW]), cap) * (2 * torch.rand(m, device=dev) - 1)
        self.goal_yaw[env_ids] = wrap(obj_heading + dyaw)

        zeros = torch.zeros(m, device=dev)
        obj_quat = quat_from_euler_xyz(zeros, zeros, obj_heading)
        for k, o in enumerate(self.objs):
            here = shape == k
            st = torch.zeros(m, 13, device=dev)
            st[:, :2] = torch.where(here.unsqueeze(-1), obj_xy,
                                    root[:, :2] + torch.tensor([c.park_distance + 4.0 * k, 0.0], device=dev))
            st[:, 2] = float(SHAPES[k].rest_height) + 0.005
            st[:, 3:7] = obj_quat
            o.write_root_state_to_sim(st, env_ids)

        gquat = quat_from_euler_xyz(zeros, zeros, self.goal_yaw[env_ids])
        for k, g in enumerate(self.goals):
            pose = torch.zeros(m, 7, device=dev)
            pose[:, :2] = self.goal_xy[env_ids]
            pose[:, 2] = torch.where(shape == k, torch.full_like(zeros, 0.002), torch.full_like(zeros, -5.0))
            pose[:, 3:7] = gquat
            g.write_mocap_pose_to_sim(pose, env_ids)

        self.prev_dist[env_ids] = torch.linalg.norm(self.goal_xy[env_ids] - obj_xy, dim=-1)
        self.prev_yaw_err[env_ids] = fold(wrap(self.goal_yaw[env_ids] - obj_heading), self.sym[shape]).abs()


@dataclass(kw_only=True)
class HardGoalCommandCfg(CommandTermCfg):
    resampling_time_range: tuple[float, float] = (1e9, 1e9)
    robot_reach: float = 0.55
    gap: tuple[float, float] = (0.3, 0.8)  # clear space robot body -> object at the start
    park_distance: float = 40.0
    # d_lo, d_hi [m] | object bearing +- [deg] | goal direction +- [deg] (0 = straight
    # away from the robot) | object start yaw +- | goal yaw change +- [deg] |
    # pos tol [m] | yaw tol [deg] | hold [s] | max mass [kg]
    levels: tuple[tuple[float, ...], ...] = (
        (1.0, 2.0, 20, 20, 20, 20, 0.20, 12, 0.0, 15),
        (1.5, 3.0, 45, 45, 45, 45, 0.15, 10, 0.5, 20),
        (2.0, 4.0, 90, 90, 90, 90, 0.15, 8, 0.5, 25),
        (2.5, 5.0, 135, 135, 180, 135, 0.12, 7, 1.0, 30),
        (3.0, 6.0, 180, 180, 180, 180, 0.10, 6, 1.0, 35),
        (3.0, 7.0, 180, 180, 180, 180, 0.10, 6, 1.0, 40),
    )
    mass_lo: float = 5.0
    start_level: int = 0
    replay_frac: float = 0.2
    max_yaw_frac_of_symmetry: float = 0.9
    only: str | None = None  # eval: always this object (e.g. "obj_arch")

    def build(self, env) -> HardGoalCommand:
        return HardGoalCommand(self, env)


# ---------------------------------------------------------------------------------
# observations
# ---------------------------------------------------------------------------------
def _g(env) -> HardGoalCommand:
    return env.command_manager.get_term("goal")


def _to_robot(env, v_w: torch.Tensor) -> torch.Tensor:
    v = torch.zeros(v_w.shape[0], 3, device=env.device)
    v[:, :2] = v_w[:, :2]
    return quat_apply_inverse(yaw_quat(env.scene["robot"].data.root_link_quat_w), v)[:, :2]


def box_in_robot_frame(env) -> torch.Tensor:
    """Same 7 numbers as Stage 1: position (2), folded heading rel. robot as sin/cos (2),
    velocity (2), yaw rate (1)."""
    g = _g(env)
    robot = env.scene["robot"]
    pos = _to_robot(env, g.box_pos() - robot.data.root_link_pos_w)
    rel = wrap(g.heading() - yaw_of(robot.data.root_link_quat_w))
    k = g.symmetry()
    return torch.cat([pos, torch.sin(k * rel).unsqueeze(-1), torch.cos(k * rel).unsqueeze(-1),
                      _to_robot(env, g.box_vel()), g.box_ang_vel()[:, 2:3]], dim=-1)


def goal_in_robot_frame(env) -> torch.Tensor:
    """Same 7 numbers as Stage 1: goal rel. robot (2), goal rel. object (2), folded yaw error (3)."""
    g = _g(env)
    robot = env.scene["robot"]
    z = torch.zeros(env.num_envs, 1, device=env.device)
    to_goal = _to_robot(env, torch.cat([g.goal_xy, z], -1) - robot.data.root_link_pos_w)
    box_to_goal = _to_robot(env, torch.cat([g.goal_xy - g.box_pos()[:, :2], z], -1))
    _, e = g.errors()
    k = g.symmetry()
    norm = torch.where(k > 0, e / (math.pi / k.clamp(min=1)), torch.zeros_like(e))
    return torch.cat([to_goal, box_to_goal, torch.sin(k * e).unsqueeze(-1),
                      torch.cos(k * e).unsqueeze(-1), norm.unsqueeze(-1)], dim=-1)


def object_descriptor(env) -> torch.Tensor:
    """Shape-agnostic description (12 numbers): bounding-box centre (2) and half-size (2)
    in the object frame, centre-of-mass offset (2), symmetry one-hot over {any, 1, 2, 4}
    (4), roller flag (1), reach radius (1)."""
    g = _g(env)
    s = g.shape
    ids = torch.arange(env.num_envs, device=env.device)
    body = torch.tensor([o.indexing.body_ids[0] for o in g.objs], device=env.device)[s]
    com = env.sim.model.body_ipos[ids, body][:, :2]
    sym = g.sym[s]
    onehot = torch.stack([sym == 0, sym == 1, sym == 2, sym == 4], -1).float()
    return torch.cat([g.bbox[s], com, onehot, g.roller[s].float().unsqueeze(-1),
                      g.radius[s].unsqueeze(-1)], dim=-1)


def hold_progress(env) -> torch.Tensor:
    g = _g(env)
    _, _, hold = g._tol()
    return torch.clamp(g.in_goal_time / hold.clamp(min=1e-3), max=1.0).unsqueeze(-1)


def box_physics(env) -> torch.Tensor:
    """Privileged (critic): mass/10, friction of the first part, curriculum level."""
    g = _g(env)
    ids = torch.arange(env.num_envs, device=env.device)
    body = torch.tensor([o.indexing.body_ids[0] for o in g.objs], device=env.device)[g.shape]
    geom = torch.tensor([o.indexing.geom_ids[0] for o in g.objs], device=env.device)[g.shape]
    gf = env.sim.model.geom_friction
    mu = gf[ids, geom, 0] if gf.dim() == 3 else gf[geom, 0]
    return torch.stack([env.sim.model.body_mass[ids, body] / 10.0, mu, g.env_level.float()], -1)


# ---------------------------------------------------------------------------------
# rewards (same names and weights as Stage 1, so the warm-started critic still fits)
# ---------------------------------------------------------------------------------
def box_progress(env) -> torch.Tensor:
    g = _g(env)
    d, _ = g.errors()
    return torch.clamp((g.prev_dist - d) / env.step_dt, -1.0, 1.0)


def box_near_goal(env, std: float = 1.5) -> torch.Tensor:
    d, _ = _g(env).errors()
    return 1.0 - torch.tanh(d / std)


def yaw_progress(env, gate_dist: float = 1.5) -> torch.Tensor:
    g = _g(env)
    d, e = g.errors()
    rate = torch.clamp((g.prev_yaw_err - e.abs()) / env.step_dt, -1.0, 1.0)
    return torch.where(d < gate_dist, rate, torch.zeros_like(rate))


def yaw_aligned(env, std: float = 0.3, dist_scale: float = 1.0) -> torch.Tensor:
    g = _g(env)
    d, e = g.errors()
    r = (1.0 - torch.tanh(e.abs() / std)) * torch.exp(-d / dist_scale)
    return torch.where(g.symmetry() > 0, r, torch.exp(-d / dist_scale))


def robot_near_box(env, std: float = 0.5) -> torch.Tensor:
    g = _g(env)
    dist = torch.linalg.norm(g.box_pos()[:, :2] - env.scene["robot"].data.root_link_pos_w[:, :2], dim=-1)
    return 1.0 - torch.tanh(torch.clamp(dist - g.cfg.robot_reach - g.radius[g.shape], min=0.0) / std)


def robot_behind_box(env, done_dist: float = 0.25) -> torch.Tensor:
    g = _g(env)
    to_box = g.box_pos()[:, :2] - env.scene["robot"].data.root_link_pos_w[:, :2]
    to_goal = g.goal_xy - g.box_pos()[:, :2]
    cos = (to_box * to_goal).sum(-1) / (torch.linalg.norm(to_box, dim=-1) *
                                        torch.linalg.norm(to_goal, dim=-1)).clamp(min=1e-6)
    d, _ = g.errors()
    return torch.where(d > done_dist, cos.clamp(min=0.0), torch.zeros_like(cos))


def at_goal(env) -> torch.Tensor:
    return _g(env).in_goal().float()


def held(env) -> torch.Tensor:
    """Extra while the hold has been completed (keeps it parked, not swept through)."""
    g = _g(env)
    _, _, hold = g._tol()
    return (g.in_goal_time >= hold.clamp(min=0.5 * env.step_dt)).float()


# ---------------------------------------------------------------------------------
# terminations
# ---------------------------------------------------------------------------------
def box_tipped(env, limit_deg: float = 30.0) -> torch.Tensor:
    return _g(env).tipped(limit_deg)


def box_lost(env, max_dist: float = 12.0) -> torch.Tensor:
    g = _g(env)
    return torch.linalg.norm(g.box_pos()[:, :2] - env.scene["robot"].data.root_link_pos_w[:, :2], dim=-1) > max_dist


# ---------------------------------------------------------------------------------
# curriculum
# ---------------------------------------------------------------------------------
def hard_curriculum(env, env_ids: torch.Tensor, advance: float = 0.55, retreat: float = 0.15,
                    dwell_iters: int = 75, ema: float = 0.02, steps_per_iter: int = 24):
    g = _g(env)
    it = env.common_step_counter / steps_per_iter
    if isinstance(env_ids, torch.Tensor) and len(env_ids) > 0:
        succ = g.metrics["success"][env_ids]
        # per-shape success (logged), over all levels
        for k in range(len(SHAPES)):
            sel = g.shape[env_ids] == k
            if sel.any():
                g.shape_success[k] = 0.95 * g.shape_success[k] + 0.05 * succ[sel].mean()
        at_level = g.env_level[env_ids] == g.level
        if at_level.any():
            s = float(succ[at_level].mean())
            w = min(1.0, ema * int(at_level.sum()))
            g.ema_success = (1 - w) * g.ema_success + w * s
            if it - g.last_change_iter >= dwell_iters:
                if g.ema_success > advance and g.level < len(g.cfg.levels) - 1:
                    g.level += 1
                    g.last_change_iter = it
                    g.ema_success = 0.5 * advance
                elif g.ema_success < retreat and g.level > 0:
                    g.level -= 1
                    g.last_change_iter = it
                    g.ema_success = 0.5 * (advance + retreat)
    out = {"level": torch.tensor(float(g.level)), "success_ema": torch.tensor(g.ema_success),
           "mass_max": torch.tensor(float(g.cfg.levels[g.level][MASS_HI]))}
    for k, s in enumerate(SHAPES):
        out[f"success_{s.name}"] = g.shape_success[k].detach().clone()
    return out


# -- precision and calm near the goal ------------------------------------------------
def precise_pose(env, pos_std: float = 0.15, yaw_std_deg: float = 6.0) -> torch.Tensor:
    """Sharp (Gaussian) reward that only becomes large very close to the exact pose:
    1 at the goal, ~0.37 at 15 cm / 6 deg off, ~0 by 40 cm. Rewards the last few cm."""
    g = _g(env)
    d, e = g.errors()
    pos = torch.exp(-(d / pos_std).square())
    yaw = torch.exp(-(e / math.radians(yaw_std_deg)).square())
    return pos * torch.where(g.symmetry() > 0, yaw, torch.ones_like(yaw))


def box_settle(env, near: float = 0.6) -> torch.Tensor:
    """Object speed and spin near the goal (penalty): bring it in slowly and leave it there."""
    g = _g(env)
    d, _ = g.errors()
    v = g.box_vel()[:, :2].square().sum(-1) + 0.3 * g.box_ang_vel()[:, 2].square()
    return v * torch.exp(-d / near)


def box_runaway(env, max_speed: float = 0.8) -> torch.Tensor:
    """Object faster than it can be pushed (kicked or rolling away): penalty per m/s over."""
    return torch.clamp(torch.linalg.norm(_g(env).box_vel()[:, :2], dim=-1) - max_speed, min=0.0)