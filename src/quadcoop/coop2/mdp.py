"""Two-robot Stage 2 task: ANYmal C and Spot push one Stage 2 object to a goal pose together.

Everything single-robot is Stage 2's (``quadcoop.stage2``): the twelve shapes with randomized
sizes, the per-environment part geometry, the robot-frame top map + object-frame front
profile, the terminate-on-success rule (10 cm / 3 deg with the object at rest) and its
rewards. ``CoopPush2Command`` extends Stage 2's goal command to two robots:

* both robots start around the object, on the side away from the goal ("behind"), spread
  further apart and further from "behind" as the curriculum level rises, never closer than
  ``min_separation_deg`` to each other;
* each robot gets its own robot-frame top map (recomputed at ``map_hz``), so each robot's
  input is exactly its Stage 2b input, in its own frame; with ``partner_map`` the map has a
  second channel with the partner's footprint (same frame, scale and rate);
* the object mass window rises with the level past what one robot can push.

Per-robot observation and reward functions take the robot's entity name (``robot="spot"``).
Entity names come from quadcoop.coop2.pairs (QUADCOOP_PAIR): "anymal" and "spot" by default,
"anymal1"/"anymal2" or "spot1"/"spot2" for two robots of one type; agent order everywhere: AGENTS.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import torch
from mjlab.managers.command_manager import CommandTerm
from mjlab.utils.lab_api.math import quat_apply, quat_apply_inverse, quat_from_euler_xyz, yaw_quat

from quadcoop import falls
from quadcoop.stage1.mdp import wrap, yaw_of
from quadcoop.stage1b.mdp import BOX_YAW, D_HI, D_LO, DYAW, MASS_HI, fold
from quadcoop.stage2 import profiles as pf
from quadcoop.stage2.mdp import Push2Command, Push2CommandCfg, _image
from quadcoop.stage2.shapes import (
    GOAL_NAMES2, OBJ_NAMES2, SHAPES2, TRAIN_MASK, bbox_and_radius, kinds_tensor, nominal_parts,
)

from quadcoop.coop2.pairs import AGENTS, PARTNER, ROBOT_TYPE  # noqa: E402

_FOOTPRINT_OF_TYPE = {"anymal_c": (0.55, 0.30), "spot": (0.55, 0.28)}  # m: half-length, half-width
FOOTPRINT_HALF = {a: _FOOTPRINT_OF_TYPE[ROBOT_TYPE[a]] for a in AGENTS}  # partner map, body gap
SPREAD = 2  # level-table column 2: each robot's spread around "behind", +- deg
BEHIND = 3  # level-table column 3: "behind" rotated away from straight behind the object, +- deg
MASS_LO = 10  # extra column: lightest object at this level (kg)


class CoopPush2Command(Push2Command):
    cfg: CoopPush2CommandCfg

    def __init__(self, cfg: CoopPush2CommandCfg, env):
        CommandTerm.__init__(self, cfg, env)
        assert cfg.variant in ("b", "ctrl"), "the two-robot task supports variants b and ctrl"
        n, dev = self.num_envs, self.device
        self.robots = {a: env.scene[a] for a in AGENTS}
        self.robot = self.robots[AGENTS[0]]  # for inherited code that needs "a" robot (not used for obs)
        self.reach = dict(zip(AGENTS, cfg.reach, strict=True))
        self.objs = [env.scene[name] for name in OBJ_NAMES2]
        self.goals = [env.scene[name] for name in GOAL_NAMES2]
        self.shape_list = SHAPES2
        S = len(SHAPES2)
        self.sym = torch.tensor([float(s.symmetry) for s in SHAPES2], device=dev)
        self.roller = torch.tensor([s.roller for s in SHAPES2], device=dev)
        self.axis_y = torch.tensor([s.heading_axis_y for s in SHAPES2], device=dev)
        self.kinds = kinds_tensor(dev)
        nom, nom_rest = nominal_parts(dev)
        self.parts = nom.unsqueeze(0).repeat(n, 1, 1, 1)
        self.rest_env = nom_rest.unsqueeze(0).repeat(n, 1)
        self.bbox_env, self.radius_env = bbox_and_radius(self.parts, self.kinds.unsqueeze(0))
        self.bbox, self.radius, self.rest_h = self.bbox_env[0].clone(), self.radius_env[0].clone(), nom_rest
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
        self.train_mask = (torch.tensor(TRAIN_MASK, device=dev) if not cfg.allow_heldout
                           else torch.ones(S, dtype=torch.bool, device=dev))
        self.shape_weight = torch.ones(S, device=dev)
        # images: one robot-frame top map per robot, one object-frame front profile
        self.variant = cfg.variant
        ch = 2 if cfg.partner_map else 1
        self.tops = {a: torch.zeros(n, ch, *pf.ROBOT_TOP["hw"], device=dev) for a in AGENTS}
        self.fp_half = {a: torch.tensor(FOOTPRINT_HALF[a], device=dev) for a in AGENTS}
        self.profile_top = self.tops[AGENTS[0]][:, :1]  # Stage 2 name (anymal's object channel)
        self.profile_front = torch.zeros(n, 1, *pf.FRONT["hw"], device=dev)
        self.map_every = max(1, round(1.0 / (cfg.map_hz * env.step_dt)))
        self.steps = 0
        self.map_updates = 0
        self.success_flag = torch.zeros(n, dtype=torch.bool, device=dev)
        self.prev_precise = torch.zeros(n, device=dev)
        # approach potential per robot (r5's approach reward pays for its change, not its value)
        self.prev_near = {a: torch.zeros(n, device=dev) for a in AGENTS}
        # start distance to the goal, per episode (r7's goal-error cost is measured against it)
        self.d0 = torch.ones(n, device=dev)
        self.need_episode = torch.zeros(n, dtype=torch.bool, device=dev)  # need_frac pick (for logging)
        # evaluation switches (as in Stage 2)
        self.heading_zero = False
        self.heading_zero_map = False
        self.profile_mode = "normal"
        self.profile_roll = 1
        # eval hook: callable(env_ids) -> dict overriding the placement (see scripts/eval_coop2.py)
        self.scenario = None

    # -- per-robot geometry -------------------------------------------------------------------
    def obs_rel_yaw(self, robot: str = AGENTS[0]) -> torch.Tensor:
        rel = wrap(self.heading() - yaw_of(self.robots[robot].data.root_link_quat_w))
        return torch.zeros_like(rel) if self.heading_zero else rel

    def object_in_frame(self, robot: str, env_ids: torch.Tensor):
        r = self.robots[robot]
        d = torch.zeros(len(env_ids), 3, device=self.device)
        d[:, :2] = (self.box_pos() - r.data.root_link_pos_w)[env_ids, :2]
        xy = quat_apply_inverse(yaw_quat(r.data.root_link_quat_w[env_ids]), d)[:, :2]
        rel = wrap(self.heading() - yaw_of(r.data.root_link_quat_w))[env_ids]
        return xy, torch.zeros_like(rel) if self.heading_zero_map else rel

    def partner_in_frame(self, robot: str, env_ids: torch.Tensor):
        r, p = self.robots[robot], self.robots[PARTNER[robot]]
        d = torch.zeros(len(env_ids), 3, device=self.device)
        d[:, :2] = (p.data.root_link_pos_w - r.data.root_link_pos_w)[env_ids, :2]
        xy = quat_apply_inverse(yaw_quat(r.data.root_link_quat_w[env_ids]), d)[:, :2]
        yaw = wrap(yaw_of(p.data.root_link_quat_w) - yaw_of(r.data.root_link_quat_w))[env_ids]
        return xy, yaw

    def refresh_profiles(self, env_ids: torch.Tensor | None = None, rel: dict | None = None,
                         partner: dict | None = None, *_unused) -> None:
        """Front profile + each robot's top map for env_ids (all if None). rel / partner: optional
        {robot: (xy, yaw)} of the object / the partner in that robot's frame; read from the sim if
        None."""
        if self.variant == "ctrl":
            return
        if env_ids is None:
            env_ids = torch.arange(self.num_envs, device=self.device)
        if len(env_ids) == 0:
            return
        parts, kinds, rest = self.active(env_ids)
        self.profile_front[env_ids] = pf.front_object_frame(parts, kinds, rest)
        for a in AGENTS:
            xy, yaw = rel[a] if rel is not None else self.object_in_frame(a, env_ids)
            self.tops[a][env_ids, :1] = pf.top_robot_frame(parts, kinds, rest, xy, yaw)
            if self.cfg.partner_map:
                pxy, pyaw = partner[a] if partner is not None else self.partner_in_frame(a, env_ids)
                half = self.fp_half[PARTNER[a]].expand(len(env_ids), 2)
                self.tops[a][env_ids, 1:2] = pf.top_robot_frame_box(pxy, pyaw, half)

    def surface_distance(self, robot: str = AGENTS[0]) -> torch.Tensor:
        """Signed distance from the robot's front (bumper) to the object's body-height slice."""
        parts, kinds, rest = self.active()
        r = self.robots[robot]
        q = r.data.root_link_quat_w
        front = torch.zeros(self.num_envs, 3, device=self.device)
        front[:, 0] = self.reach[robot]
        p_w = r.data.root_link_pos_w + quat_apply(yaw_quat(q), front)
        d = p_w[:, :2] - self.box_pos()[:, :2]
        h = self.heading()
        cs, sn = torch.cos(h), torch.sin(h)
        p_obj = torch.stack([cs * d[:, 0] + sn * d[:, 1], -sn * d[:, 0] + cs * d[:, 1]], -1)
        return pf.point_distance(parts, kinds, rest, p_obj)

    @property
    def command(self) -> torch.Tensor:
        _, e = self.errors()
        return torch.cat([self.goal_xy, e.unsqueeze(-1)], -1)

    def near_value(self, robot: str, std: float = 0.4) -> torch.Tensor:
        """Approach potential: 1 with the robot's front at the object's surface, fading over ~std m."""
        d = self.surface_distance(robot).clamp(min=0.0)
        return 1.0 - torch.tanh(torch.clamp(d - 0.05, min=0.0) / std)

    def _update_command(self) -> None:
        super()._update_command()  # Stage 2: progress bookkeeping, precise potential, map refresh
        if self.cfg.track_approach:  # after the rewards and resets of this step: next step's baseline
            for a in AGENTS:
                self.prev_near[a][:] = self.near_value(a)

    # -- placement --------------------------------------------------------------------------------
    def _resample_command(self, env_ids: torch.Tensor) -> None:
        c, dev = self.cfg, self.device
        m = len(env_ids)
        if m == 0:
            return
        self.metrics["success"][env_ids] = 0.0
        self.in_goal_time[env_ids] = 0.0
        self.success_flag[env_ids] = False
        lvl = torch.full((m,), self.level, dtype=torch.long, device=dev)
        replay = torch.rand(m, device=dev) < c.replay_frac
        lvl = torch.where(replay, torch.randint(0, self.level + 1, (m,), device=dev), lvl)
        self.env_level[env_ids] = lvl
        t = self.table[lvl]

        # shape: trainable shapes whose mass is inside the level's window, weighted by how badly
        # each is going (Stage 2); none inside -> the trainable one closest to the window
        masses = torch.stack([self._env.sim.model.body_mass[env_ids, o.indexing.body_ids[0]] for o in self.objs], -1)
        lo, hi = t[:, MASS_LO].unsqueeze(-1), t[:, MASS_HI].unsqueeze(-1)
        ok = (masses >= lo) & (masses <= hi) & self.train_mask.unsqueeze(0)
        if c.only is not None:
            ok &= torch.tensor([nm == c.only for nm in OBJ_NAMES2], device=dev).unsqueeze(0)
        fallback = self.train_mask.unsqueeze(0) if c.only is None else \
            torch.tensor([nm == c.only for nm in OBJ_NAMES2], device=dev).unsqueeze(0)
        gumbel = -torch.log(-torch.log(torch.rand_like(masses).clamp(1e-9, 1 - 1e-9)))
        gap_to_window = torch.relu(lo - masses) + torch.relu(masses - hi)
        score = torch.where(ok, torch.log(self.shape_weight).unsqueeze(0) + gumbel,
                            torch.where(fallback, -1e6 - gap_to_window, torch.full_like(masses, -1e9)))
        shape = score.argmax(-1)
        if c.need_frac > 0 and c.only is None:
            # training mix: a share of episodes gets a wide object heavy enough to need both robots
            # (mass from need_mass up to the level's window + need_extra); evaluations are unchanged
            need_names = torch.tensor([nm[len("obj_"):] in c.need_shapes for nm in OBJ_NAMES2], device=dev)
            top = torch.maximum(hi, torch.full_like(hi, c.need_mass)) + c.need_extra
            cand = need_names.unsqueeze(0) & self.train_mask.unsqueeze(0) & (masses >= c.need_mass) & (masses <= top)
            pick = (torch.rand(m, device=dev) < c.need_frac) & cand.any(-1)
            nscore = torch.where(cand, gumbel, torch.full_like(gumbel, -1e9))
            shape = torch.where(pick, nscore.argmax(-1), shape)
            self.need_episode[env_ids] = pick
        sc = self.scenario(env_ids) if self.scenario is not None else None
        if sc is not None and "shape" in sc:
            shape = sc["shape"]
        self.shape[env_ids] = shape

        def U(a, b):
            return a + torch.rand(m, device=dev) * (b - a)

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
        behind = gdir + math.pi + sym_u(t[:, BEHIND])
        b0 = behind + sym_u(t[:, SPREAD])
        b1 = behind + sym_u(t[:, SPREAD])
        sep = math.radians(c.min_separation_deg)
        diff = wrap(b1 - b0)
        side = torch.where(diff >= 0, torch.ones_like(diff), -torch.ones_like(diff))
        # push them apart symmetrically to at least `sep`
        short = (sep - diff.abs()).clamp(min=0.0) * 0.5
        b0, b1 = b0 - side * short, b1 + side * short
        if c.start_mode == "around":  # anywhere around the object, still at least `sep` apart
            b0 = 2 * math.pi * torch.rand(m, device=dev)
            b1 = b0 + U(torch.full((m,), sep, device=dev), torch.full((m,), 2 * math.pi - sep, device=dev))
        bearings = [b0, b1]
        gaps = [U(c.gap[0], c.gap[1]) for _ in AGENTS]
        yaw_noise = [sym_u(torch.full((m,), c.robot_yaw_noise_deg, device=dev)) for _ in AGENTS]
        park = [torch.zeros(m, dtype=torch.bool, device=dev) for _ in AGENTS]
        if sc is not None:
            obj_xy = origin + sc.get("obj_xy_rel", obj_xy - origin)
            obj_heading = sc.get("obj_heading", obj_heading)
            goal_xy = origin + sc.get("goal_xy_rel", goal_xy - origin)
            goal_yaw = sc.get("goal_yaw", goal_yaw)
            bearings = sc.get("bearings", bearings)
            gaps = sc.get("gaps", gaps)
            yaw_noise = sc.get("yaw_noise", yaw_noise)
            park = sc.get("park", park)  # eval "solo": the other robot stands far away

        self.goal_xy[env_ids] = goal_xy
        self.goal_yaw[env_ids] = goal_yaw
        zeros = torch.zeros(m, device=dev)
        rel, poses = {}, {}
        for k, a in enumerate(AGENTS):
            robot = self.robots[a]
            dist = self.radius_env[env_ids, shape] + self.reach[a] + gaps[k]
            pos = obj_xy + dist.unsqueeze(-1) * torch.stack([torch.cos(bearings[k]), torch.sin(bearings[k])], -1)
            yaw = bearings[k] + math.pi + yaw_noise[k]
            far = origin + torch.tensor([0.0, c.park_distance * (1.0 if k == 0 else -1.0)], device=dev)
            pos = torch.where(park[k].unsqueeze(-1), far, pos)
            q_adr = robot.indexing.free_joint_q_adr
            z = robot.data.data.qpos[env_ids][:, q_adr[2]]
            st = torch.zeros(m, 13, device=dev)
            st[:, :2] = pos
            st[:, 2] = z
            st[:, 3:7] = quat_from_euler_xyz(zeros, zeros, yaw)
            robot.write_root_state_to_sim(st, env_ids)
            poses[a] = (pos, yaw)
            cs, sn = torch.cos(yaw), torch.sin(yaw)
            dxy = obj_xy - pos
            rel[a] = (torch.stack([cs * dxy[:, 0] + sn * dxy[:, 1], -sn * dxy[:, 0] + cs * dxy[:, 1]], -1),
                      zeros if self.heading_zero_map else wrap(obj_heading - yaw))

        obj_quat = quat_from_euler_xyz(zeros, zeros, obj_heading)
        for k, o in enumerate(self.objs):
            here = shape == k
            st = torch.zeros(m, 13, device=dev)
            st[:, :2] = torch.where(here.unsqueeze(-1), obj_xy,
                                    origin + torch.tensor([c.park_distance + 4.0 * k, 0.0], device=dev))
            st[:, 2] = self.rest_env[env_ids, k] + 0.005
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
        self.d0[env_ids] = self.prev_dist[env_ids].clamp(min=0.5)
        partner = {}
        for a in AGENTS:
            (pos, yaw), (ppos, pyaw) = poses[a], poses[PARTNER[a]]
            cs, sn = torch.cos(yaw), torch.sin(yaw)
            dxy = ppos - pos
            partner[a] = (torch.stack([cs * dxy[:, 0] + sn * dxy[:, 1], -sn * dxy[:, 0] + cs * dxy[:, 1]], -1),
                          wrap(pyaw - yaw))
        self.refresh_profiles(env_ids, rel, partner)
        self.prev_precise[env_ids] = 0.0


@dataclass(kw_only=True)
class CoopPush2CommandCfg(Push2CommandCfg):
    variant: str = "b"
    success_mode: str = "terminate"
    reach: tuple[float, float] = (0.55, 0.55)  # body half-length (anymal, spot)
    gap: tuple[float, float] = (0.3, 0.9)  # clear space body -> object at the start
    min_separation_deg: float = 60.0
    robot_yaw_noise_deg: float = 20.0
    park_distance: float = 40.0
    partner_map: bool = False  # second map channel: the partner's footprint
    track_approach: bool = False  # keep each robot's approach potential (r5's approach reward)
    # training-only options (evaluations place robots and objects themselves):
    start_mode: str = "behind"  # "behind": robots start behind the object (level table); "around": anywhere
    need_frac: float = 0.0  # share of episodes with a wide object heavy enough to need both robots
    need_mass: float = 45.0  # kg: about what one ANYmal can push alone
    need_extra: float = 20.0  # kg above the level's mass window allowed for those episodes
    need_shapes: tuple[str, ...] = ("long", "arch", "dumbbell", "t_shape")  # trainable wide shapes
    # d_lo, d_hi [m] | robot spread +- [deg] | "behind" offset +- [deg] | object start yaw +- |
    # goal yaw change +- | pos tol [m] | yaw tol [deg] | hold [s] (tolerances: "hold" mode only;
    # "terminate" uses success_pos_tol / success_yaw_tol_deg) | max mass [kg] | min mass [kg]
    levels: tuple[tuple[float, ...], ...] = field(default_factory=lambda: (
        (1.5, 3.0, 25, 0, 30, 30, 0.15, 10, 0.5, 40, 10),     # each robot could do it alone
        (2.0, 4.0, 40, 20, 60, 60, 0.12, 8, 0.5, 50, 20),
        (2.0, 5.0, 55, 45, 90, 90, 0.10, 6, 1.0, 60, 30),
        (3.0, 6.0, 70, 90, 180, 135, 0.10, 6, 1.0, 75, 40),
        (3.0, 6.0, 90, 180, 180, 180, 0.10, 6, 1.0, 90, 50),  # one robot cannot push most of these
    ))

    def build(self, env) -> CoopPush2Command:
        return CoopPush2Command(self, env)


# ---------------------------------------------------------------------------------
# observations, per robot (that robot's yaw frame); same layout as Stage 2's
# ---------------------------------------------------------------------------------
def _g(env) -> CoopPush2Command:
    return env.command_manager.get_term("goal")


def _to_frame(env, robot: str, v_w: torch.Tensor) -> torch.Tensor:
    v = torch.zeros(v_w.shape[0], 3, device=env.device)
    v[:, :2] = v_w[:, :2]
    return quat_apply_inverse(yaw_quat(env.scene[robot].data.root_link_quat_w), v)[:, :2]


def box_obs(env, robot: str) -> torch.Tensor:
    """Stage 2's 7: object position (2), folded heading rel. robot (sin, cos), velocity (2), yaw rate."""
    g = _g(env)
    r = env.scene[robot]
    pos = _to_frame(env, robot, g.box_pos() - r.data.root_link_pos_w)
    rel = g.obs_rel_yaw(robot)
    k = g.symmetry()
    return torch.cat([pos, torch.sin(k * rel).unsqueeze(-1), torch.cos(k * rel).unsqueeze(-1),
                      _to_frame(env, robot, g.box_vel()), g.box_ang_vel()[:, 2:3]], dim=-1)


def goal_obs(env, robot: str) -> torch.Tensor:
    """Stage 2's 7: goal rel. robot (2), goal rel. object (2), folded yaw error (sin, cos, normalized)."""
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


def walker_command_of(env, twist_name: str) -> torch.Tensor:
    return env.command_manager.get_command(twist_name)


def partner_obs(env, robot: str, other: str, other_action: str) -> torch.Tensor:
    """New (9): partner position (2), its heading rel. this robot (sin, cos), its velocity (2),
    all in this robot's frame, and the command it last sent its walker (3, clipped to [-1, 1])."""
    r, p = env.scene[robot], env.scene[other]
    pos = _to_frame(env, robot, p.data.root_link_pos_w - r.data.root_link_pos_w)
    rel = wrap(yaw_of(p.data.root_link_quat_w) - yaw_of(r.data.root_link_quat_w))
    cmd = env.action_manager.get_term(other_action).raw_action.clamp(-1.0, 1.0)
    return torch.cat([pos, torch.sin(rel).unsqueeze(-1), torch.cos(rel).unsqueeze(-1),
                      _to_frame(env, robot, p.data.root_link_lin_vel_w), cmd], dim=-1)


def top_map(env, robot: str) -> torch.Tensor:
    g = _g(env)
    return _image(g, g.tops[robot])


# ---------------------------------------------------------------------------------
# rewards: per-robot terms (their names end in _anymal / _spot, which is how the trainer
# splits them out); the object terms are Stage 2's (team terms)
# ---------------------------------------------------------------------------------
def near_surface(env, robot: str, std: float = 0.4) -> torch.Tensor:
    """Stage 2's approach term for this robot: 1 when its front is at the object's surface."""
    d = _g(env).surface_distance(robot).clamp(min=0.0)
    return 1.0 - torch.tanh(torch.clamp(d - 0.05, min=0.0) / std)


def approach(env, robot: str, max_rate: float = 10.0) -> torch.Tensor:
    """r5: change of this robot's approach potential per second (potential-based shaping): pays
    for getting to the object's surface, nothing for staying there, the same back for leaving.
    Summed over an episode it is at most the potential's range (1). The clip is only a guard
    against glitches: walking changes the potential by at most ~2/s, and a tighter clip would let
    a robot dash away (loss clipped) and walk back (full gain) for a net profit."""
    g = _g(env)
    return torch.clamp((g.near_value(robot) - g.prev_near[robot]) / env.step_dt, -max_rate, max_rate)


def time_cost(env) -> torch.Tensor:
    """r5 (team): 1 per second the episode lasts, so running out of time is not free."""
    return torch.ones(env.num_envs, device=env.device)


def behind_box(env, robot: str, done_dist: float = 0.25) -> torch.Tensor:
    """Stage 1b/2's robot_behind_box for this robot."""
    g = _g(env)
    to_box = g.box_pos()[:, :2] - env.scene[robot].data.root_link_pos_w[:, :2]
    to_goal = g.goal_xy - g.box_pos()[:, :2]
    cos = (to_box * to_goal).sum(-1) / (torch.linalg.norm(to_box, dim=-1) *
                                        torch.linalg.norm(to_goal, dim=-1)).clamp(min=1e-6)
    d, _ = g.errors()
    return torch.where(d > done_dist, cos.clamp(min=0.0), torch.zeros_like(cos))


def agent_action_rate(env, agent: int) -> torch.Tensor:
    """Squared change of the command this robot's walker actually gets (actions clipped to
    [-1, 1], so at most 12 per step). The env action is (anymal vx, vy, wz, spot vx, vy, wz).
    (Stage 2 penalized the raw policy output instead; unbounded outputs made that term blow up
    to -1e13 in the first two-robot run.)"""
    am = env.action_manager
    sl = slice(3 * agent, 3 * agent + 3)
    a, p = am.action[:, sl].clamp(-1.0, 1.0), am.prev_action[:, sl].clamp(-1.0, 1.0)
    return torch.sum(torch.square(a - p), dim=-1)


def agent_action_limit(env, agent: int) -> torch.Tensor:
    """How far this robot's raw policy output is past the walker's [-1, 1] clip (summed over vx,
    vy, wz; linear). Outputs past the clip change nothing the robot does, so this only keeps
    them from drifting without bound."""
    a = env.action_manager.action[:, 3 * agent:3 * agent + 3]
    return torch.sum(torch.relu(a.abs() - 1.0), dim=-1)


def push_along(env, robot: str, near: float = 0.3, done_dist: float = 0.25) -> torch.Tensor:
    """New: this robot's velocity along the object -> goal direction (m/s, clipped to
    [-0.5, 1]), counted only while its front is within `near` of the object's surface and the
    object is not yet at the goal. Credits the robot that is actually pushing the right way
    (cf. Feng et al. 2024's occlusion-based reward)."""
    g = _g(env)
    to_goal = g.goal_xy - g.box_pos()[:, :2]
    u = to_goal / torch.linalg.norm(to_goal, dim=-1, keepdim=True).clamp(min=1e-6)
    v = env.scene[robot].data.root_link_lin_vel_w[:, :2]
    along = (v * u).sum(-1).clamp(-0.5, 1.0)
    d, _ = g.errors()
    gate = (g.surface_distance(robot) < near) & (d > done_dist)
    return torch.where(gate, along, torch.zeros_like(along))


def own_fall(env, robot: str, nominal_height: float) -> torch.Tensor:
    """New: 1 on the step this robot falls (its own extra penalty, on top of the team's)."""
    return falls.fallen(env, asset_name=robot, nominal_height=nominal_height).float()


def robots_close(env, safe: float = 1.0) -> torch.Tensor:
    """New (team): 0 beyond `safe` metres between the two bases, rising linearly to 1 at 0 m."""
    a, b = (env.scene[x].data.root_link_pos_w[:, :2] for x in AGENTS)
    return torch.clamp((safe - torch.linalg.norm(a - b, dim=-1)) / safe, min=0.0, max=1.0)


def robots_close_exp(env, threshold: float = 0.6, rate: float = 8.0, cap: float = 50.0) -> torch.Tensor:
    """New (team, r4): 0 while the two bases are at least `threshold` apart; below it the penalty
    grows exponentially, exp(rate * (threshold - d)) - 1, capped at `cap`: about 1.2 at 0.5 m,
    4 at 0.4 m, 10 at 0.3 m, 24 at 0.2 m (per second, before the weight). Close teamwork is
    free; crowding is not."""
    a, b = (env.scene[x].data.root_link_pos_w[:, :2] for x in AGENTS)
    d = torch.linalg.norm(a - b, dim=-1)
    pen = torch.exp(rate * torch.clamp(threshold - d, min=0.0)) - 1.0
    return pen.clamp(max=cap)


def goal_error(env, yaw_weight: float = 1.0, max_dist_frac: float = 2.0) -> torch.Tensor:
    """r7: how far the object is from its goal pose right now, normalized: distance / distance at
    the start of the episode (capped at max_dist_frac) + yaw_weight * heading error / the largest
    heading error the shape can have (pi / symmetry; 0 for the sphere). 1-2 at the start, 0 at
    the goal. As a per-second cost it charges the area under the error-over-time curve: faster
    and more direct pushing (and no needless turning) costs less, without saying how to push."""
    g = _g(env)
    d, e = g.errors()
    k = g.symmetry()
    yaw = torch.where(k > 0, e.abs() / (math.pi / k.clamp(min=1)), torch.zeros_like(e))
    return (d / g.d0).clamp(max=max_dist_frac) + yaw_weight * yaw


def failed_remaining(env, names: tuple[str, ...], horizon_s: float, yaw_weight: float = 1.0) -> torch.Tensor:
    """r7: on a failure step (a robot falls, the object tips or is lost), the goal-error cost the
    rest of the episode would have charged at the current error: goal_error * time left, paid
    at once (divided by the step length because rewards are multiplied by it). With a cost per
    second, ending the episode early must not be cheaper than staying."""
    tm = env.termination_manager
    bad = torch.zeros(env.num_envs, dtype=torch.bool, device=env.device)
    for nm in names:
        if nm in tm.active_terms:
            bad |= tm.get_term(nm)
    left = (horizon_s - env.episode_length_buf.float() * env.step_dt).clamp(min=0.0)
    return bad.float() * goal_error(env, yaw_weight) * left / env.step_dt


def push_credit(env, robot: str, contact: float = 0.08, max_speed: float = 1.0, done_dist: float = 0.1) -> torch.Tensor:
    """r7, per robot: the object's speed toward its goal (m/s, 0..max_speed), credited to this
    robot only while its front is on the object (within `contact` of the surface) and it is
    behind the object relative to the goal (weighted by the cosine between robot -> object and
    object -> goal, 0 from the side or in front). Unlike push_along (the robot's own speed near
    the object), it cannot be earned without moving the object toward the goal."""
    g = _g(env)
    obj = g.box_pos()[:, :2]
    to_goal = g.goal_xy - obj
    dist = torch.linalg.norm(to_goal, dim=-1)
    u = to_goal / dist.unsqueeze(-1).clamp(min=1e-6)
    to_obj = obj - env.scene[robot].data.root_link_pos_w[:, :2]
    behind = ((to_obj * u).sum(-1) / torch.linalg.norm(to_obj, dim=-1).clamp(min=1e-6)).clamp(min=0.0)
    speed = (g.box_vel()[:, :2] * u).sum(-1).clamp(0.0, max_speed)
    on = (g.surface_distance(robot) < contact) & (dist > done_dist)
    return torch.where(on, behind * speed, torch.zeros_like(speed))


def object_force_from(env, robot: str) -> torch.Tensor:
    """(n, 2): horizontal contact force between this robot and the object (world frame, on the
    object), from the push_<robot> contact sensor (r8): net force over all object copies, of
    which only the active one can be touched."""
    f = env.scene[f"push_{robot}"].data.force  # (n, P, 3), net force per object body, global frame
    return -FORCE_SIGN * f.sum(1)[:, :2]


FORCE_SIGN = 1.0  # sensor convention: force on the primary (object) is -FORCE_SIGN * reading (checked in tests)


def work_credit(env, robot: str, f_ref: float = 200.0, max_ratio: float = 2.0, max_speed: float = 1.0,
                done_dist: float = 0.1) -> torch.Tensor:
    """r8, per robot: the work this robot does moving the object toward its goal, per second,
    normalized: (its contact force on the object along the goal direction / f_ref, 0..max_ratio)
    x (object speed toward the goal, 0..max_speed m/s). A robot that is not pushing earns 0; two
    robots pushing share the credit by how hard each pushes (an approximation of each robot's
    marginal contribution, as in difference rewards). f_ref = 200 N ~ what one ANYmal sustains."""
    g = _g(env)
    to_goal = g.goal_xy - g.box_pos()[:, :2]
    dist = torch.linalg.norm(to_goal, dim=-1)
    u = to_goal / dist.unsqueeze(-1).clamp(min=1e-6)
    push = ((object_force_from(env, robot) * u).sum(-1) / f_ref).clamp(0.0, max_ratio)
    speed = (g.box_vel()[:, :2] * u).sum(-1).clamp(0.0, max_speed)
    return torch.where(dist > done_dist, push * speed, torch.zeros_like(speed))


def _segment_distance(p1, q1, p2, q2):
    """Closest distance between 2D segments p1-q1 and p2-q2 (batched, (n, 2) each)."""
    d1, d2, r = q1 - p1, q2 - p2, p1 - p2
    a, e = (d1 * d1).sum(-1), (d2 * d2).sum(-1)
    f, c, b = (d2 * r).sum(-1), (d1 * r).sum(-1), (d1 * d2).sum(-1)
    den = (a * e - b * b).clamp(min=1e-9)
    s = ((b * f - c * e) / den).clamp(0.0, 1.0)
    t = ((b * s + f) / e.clamp(min=1e-9)).clamp(0.0, 1.0)
    s = ((b * t - c) / a.clamp(min=1e-9)).clamp(0.0, 1.0)
    return torch.linalg.norm(p1 + d1 * s.unsqueeze(-1) - (p2 + d2 * t.unsqueeze(-1)), dim=-1)


def robots_body_gap(env) -> torch.Tensor:
    """Clear space between the two robots' bodies (m), each body a capsule over its footprint
    (FOOTPRINT_HALF: half-length along its heading, half-width as the radius). About 0 when they
    stand shoulder to shoulder; negative when overlapping."""
    segs, rad = [], []
    for a in AGENTS:
        r = env.scene[a]
        c = r.data.root_link_pos_w[:, :2]
        yaw = yaw_of(r.data.root_link_quat_w)
        hl, hw = FOOTPRINT_HALF[a]
        ax = torch.stack([torch.cos(yaw), torch.sin(yaw)], -1) * (hl - hw)
        segs.append((c - ax, c + ax))
        rad.append(hw)
    return _segment_distance(*segs[0], *segs[1]) - sum(rad)


def robots_gap_exp(env, threshold: float = 0.15, rate: float = 20.0, cap: float = 50.0) -> torch.Tensor:
    """r7 (team): 0 while the robots' bodies are at least `threshold` apart; below it the penalty
    grows exponentially, exp(rate * (threshold - gap)) - 1, capped: about 0.8 at a 0.12 m gap,
    1.7 at 0.10 m, 6.4 at 0.05 m, 19 touching (per second, before the weight). Same rule as
    robots_close_exp, but on the gap between the bodies: the centre distance is ~0.6 m with the
    robots shoulder to shoulder, where the r4 penalty was already ~0."""
    pen = torch.exp(rate * torch.clamp(threshold - robots_body_gap(env), min=0.0)) - 1.0
    return pen.clamp(max=cap)


def robots_touching(env, sensor_name: str = "robots_touch") -> torch.Tensor:
    """New (team): 1 while any part of one robot touches the other."""
    return env.scene[sensor_name].data.found.view(env.num_envs, -1).any(-1).float()


# ---------------------------------------------------------------------------------
# terminations
# ---------------------------------------------------------------------------------
def unstable(env, max_speed: float = 25.0) -> torch.Tensor:
    """A robot or the object moving impossibly fast, or a non-finite pose (a simulation glitch):
    the episode ends without a penalty."""
    g = _g(env)
    bad = torch.zeros(env.num_envs, dtype=torch.bool, device=env.device)
    for d in [env.scene[a].data for a in AGENTS]:
        bad |= ~torch.isfinite(d.root_link_pos_w).all(-1) | (torch.linalg.norm(d.root_link_lin_vel_w, dim=-1) > max_speed)
    bad |= ~torch.isfinite(g.box_pos()).all(-1) | (torch.linalg.norm(g.box_vel(), dim=-1) > max_speed)
    return bad


def box_lost(env, max_dist: float = 12.0) -> torch.Tensor:
    """The object is far from both robots (kicked away)."""
    g = _g(env)
    d = torch.stack([torch.linalg.norm(g.box_pos()[:, :2] - env.scene[a].data.root_link_pos_w[:, :2], dim=-1)
                     for a in AGENTS], -1)
    return d.min(-1).values > max_dist
