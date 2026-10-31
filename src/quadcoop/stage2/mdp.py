"""Stage 2: Stage 1b's push-to-pose task, with object shape profiles as policy input.

What changes from Stage 1b (``quadcoop.stage1b.mdp``):

* Twelve shapes whose sizes are randomized per environment (``shapes.py``); seven are
  trained on, five are held out for evaluation.
* ``Push2Command`` keeps per-environment part geometry, and the profile images:
  object-frame top + front (variant "a"), robot-frame top + object-frame front ("b",
  top recomputed at ``map_hz``), or none ("ctrl": same task, no images).
* Shapes are drawn in proportion to how badly each is going (per-shape success EMA),
  so the failing ones get practised more.
* The approach reward pays for the robot's front getting close to the object's actual
  surface (signed distance to the body-height slice), not to its centre; standing in the
  arch's doorway no longer counts as "at the object".
* Ablation switches for the evaluation: report the object's heading as 0 (relative to
  the robot) in the numeric input (``heading_zero``) and optionally also in the robot-frame
  map (``heading_zero_map``), zero the profile images, or swap them between envs.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import torch
from mjlab.managers.command_manager import CommandTerm
from mjlab.managers.event_manager import requires_model_fields
from mjlab.managers.scene_entity_config import SceneEntityCfg
from mjlab.utils.lab_api.math import quat_apply_inverse, quat_from_euler_xyz, yaw_quat

from quadcoop.stage1.mdp import wrap, yaw_of
from quadcoop.stage1b.mdp import (
    BEARING, BOX_YAW, D_HI, D_LO, DYAW, GOAL_DIR, MASS_HI, HardGoalCommand, HardGoalCommandCfg, fold,
)
from quadcoop.stage2 import profiles as pf
from quadcoop.stage2.shapes import (
    FACTOR_RANGE, GOAL_NAMES2, KIND_NONE, KIND_SPHERE, OBJ_NAMES2, SHAPES2,
    TRAIN_MASK, bbox_and_radius, geom_size_pos, kinds_tensor, nominal_parts, shape_parts,
)


class Push2Command(HardGoalCommand):
    cfg: Push2CommandCfg

    def __init__(self, cfg: Push2CommandCfg, env):
        CommandTerm.__init__(self, cfg, env)
        n, dev = self.num_envs, self.device
        self.robot = env.scene["robot"]
        self.objs = [env.scene[name] for name in OBJ_NAMES2]
        self.goals = [env.scene[name] for name in GOAL_NAMES2]
        self.shape_list = SHAPES2
        S = len(SHAPES2)
        self.sym = torch.tensor([float(s.symmetry) for s in SHAPES2], device=dev)
        self.roller = torch.tensor([s.roller for s in SHAPES2], device=dev)
        self.axis_y = torch.tensor([s.heading_axis_y for s in SHAPES2], device=dev)
        self.kinds = kinds_tensor(dev)  # (S, P)
        nom, nom_rest = nominal_parts(dev)
        self.parts = nom.unsqueeze(0).repeat(n, 1, 1, 1)  # (n, S, P, 6), overwritten by the geometry event
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
        self.train_mask = torch.tensor(TRAIN_MASK, device=dev) if not cfg.allow_heldout else torch.ones(S, dtype=torch.bool, device=dev)
        self.shape_weight = torch.ones(S, device=dev)
        # profile images
        self.variant = cfg.variant
        self.profile_top = torch.zeros(n, 1, *(pf.ROBOT_TOP if cfg.variant == "b" else pf.OBJ_TOP)["hw"], device=dev)
        self.profile_front = torch.zeros(n, 1, *pf.FRONT["hw"], device=dev)
        self.map_every = max(1, round(1.0 / (cfg.map_hz * env.step_dt)))
        self.steps = 0
        self.map_updates = 0
        # evaluation switches
        self.success_flag = torch.zeros(n, dtype=torch.bool, device=dev)  # success_mode "terminate"
        self.prev_precise = torch.zeros(n, device=dev)
        self.heading_zero = False  # numeric heading input reads 0
        self.heading_zero_map = False  # robot-frame map ("b") also drawn with the object unrotated
        self.profile_mode = "normal"  # normal | zero | roll
        self.profile_roll = 1
        self.scenario = None

    # -- geometry of the active object --------------------------------------------------------
    def active(self, env_ids: torch.Tensor | None = None):
        if env_ids is None:
            env_ids = torch.arange(self.num_envs, device=self.device)
        s = self.shape[env_ids]
        return self.parts[env_ids, s], self.kinds[s], self.rest_env[env_ids, s]

    def obs_rel_yaw(self) -> torch.Tensor:
        """Object heading relative to the robot, as the policy is told it (0 under the ablation)."""
        rel = wrap(self.heading() - yaw_of(self.robot.data.root_link_quat_w))
        return torch.zeros_like(rel) if self.heading_zero else rel

    def object_in_robot_frame(self, env_ids: torch.Tensor | None = None):
        """Object origin (xy) in the robot's yaw frame and its heading relative to the robot."""
        if env_ids is None:
            env_ids = torch.arange(self.num_envs, device=self.device)
        d = torch.zeros(len(env_ids), 3, device=self.device)
        d[:, :2] = (self.box_pos() - self.robot.data.root_link_pos_w)[env_ids, :2]
        xy = quat_apply_inverse(yaw_quat(self.robot.data.root_link_quat_w[env_ids]), d)[:, :2]
        # heading() is the body-x heading for every shape (the lying cylinder's is computed
        # from its rolling axis, which gives the same angle while it lies flat)
        rel = wrap(self.heading() - yaw_of(self.robot.data.root_link_quat_w))[env_ids]
        return xy, torch.zeros_like(rel) if self.heading_zero_map else rel

    def refresh_profiles(self, env_ids: torch.Tensor | None = None, rel_xy: torch.Tensor | None = None,
                         rel_yaw: torch.Tensor | None = None) -> None:
        """Recompute the images for env_ids (all envs if None). For the robot-frame map the
        object's pose relative to the robot is read from the sim unless given."""
        if self.variant == "ctrl":
            return
        if env_ids is None:
            env_ids = torch.arange(self.num_envs, device=self.device)
        if len(env_ids) == 0:
            return
        parts, kinds, rest = self.active(env_ids)
        self.profile_front[env_ids] = pf.front_object_frame(parts, kinds, rest)
        if self.variant == "a":
            self.profile_top[env_ids] = pf.top_object_frame(parts, kinds, rest)
        else:
            if rel_xy is None:
                rel_xy, rel_yaw = self.object_in_robot_frame(env_ids)
            self.profile_top[env_ids] = pf.top_robot_frame(parts, kinds, rest, rel_xy, rel_yaw)

    def set_geometry(self, env_ids: torch.Tensor, shape_idx: int, parts: torch.Tensor, rest: torch.Tensor) -> None:
        self.parts[env_ids, shape_idx] = parts
        self.rest_env[env_ids, shape_idx] = rest
        bb, rad = bbox_and_radius(parts, self.kinds[shape_idx].unsqueeze(0))
        self.bbox_env[env_ids, shape_idx] = bb
        self.radius_env[env_ids, shape_idx] = rad

    def surface_distance(self) -> torch.Tensor:
        """Signed distance from the robot's front (bumper) to the object's body-height slice."""
        parts, kinds, rest = self.active()
        q = self.robot.data.root_link_quat_w
        front = torch.zeros(self.num_envs, 3, device=self.device)
        front[:, 0] = self.cfg.robot_reach
        from mjlab.utils.lab_api.math import quat_apply
        p_w = self.robot.data.root_link_pos_w + quat_apply(yaw_quat(q), front)
        d = p_w[:, :2] - self.box_pos()[:, :2]
        h = self.heading()
        cs, sn = torch.cos(h), torch.sin(h)
        p_obj = torch.stack([cs * d[:, 0] + sn * d[:, 1], -sn * d[:, 0] + cs * d[:, 1]], -1)
        return pf.point_distance(parts, kinds, rest, p_obj)

    # -- hooks --------------------------------------------------------------------------------------
    def precise_value(self) -> torch.Tensor:
        """Stage 1b's precise_pose (1 at the exact pose, ~0.37 at 15 cm / 6 deg)."""
        d, e = self.errors()
        pos = torch.exp(-(d / 0.15).square())
        yaw = torch.exp(-(e / math.radians(6.0)).square())
        return pos * torch.where(self.symmetry() > 0, yaw, torch.ones_like(yaw))

    def _update_metrics(self) -> None:
        super()._update_metrics()
        if self.cfg.success_mode == "terminate":
            c = self.cfg
            d, e = self.errors()
            still = (torch.linalg.norm(self.box_vel()[:, :2], dim=-1) < c.success_max_speed) & \
                    (self.box_ang_vel()[:, 2].abs() < c.success_max_yaw_rate)
            self.success_flag[:] = (d < c.success_pos_tol) & (e.abs() < math.radians(c.success_yaw_tol_deg)) & still
            self.metrics["success"][:] = self.success_flag.float()

    def _update_command(self) -> None:
        super()._update_command()
        self.prev_precise[:] = self.precise_value()
        self.steps += 1
        if self.variant == "b" and self.steps % self.map_every == 0:
            self.refresh_profiles()
            self.map_updates += 1

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

        # Shape: among the trainable shapes whose mass is inside the level's window, drawn
        # in proportion to shape_weight (more often the worse it is going).
        masses = torch.stack([self._env.sim.model.body_mass[env_ids, o.indexing.body_ids[0]] for o in self.objs], -1)
        ok = (masses >= c.mass_lo) & (masses <= t[:, MASS_HI].unsqueeze(-1)) & self.train_mask.unsqueeze(0)
        if c.only is not None:
            ok &= torch.tensor([nm == c.only for nm in OBJ_NAMES2], device=dev).unsqueeze(0)
        gumbel = -torch.log(-torch.log(torch.rand_like(masses).clamp(1e-9, 1 - 1e-9)))
        fallback = self.train_mask.unsqueeze(0) if c.only is None else \
            torch.tensor([nm == c.only for nm in OBJ_NAMES2], device=dev).unsqueeze(0)
        score = torch.where(ok, torch.log(self.shape_weight).unsqueeze(0) + gumbel,
                            torch.where(fallback, -1e6 - masses, torch.full_like(masses, -1e9)))
        shape = score.argmax(-1)
        self.shape[env_ids] = shape

        q_adr = self.robot.indexing.free_joint_q_adr
        qpos = self.robot.data.data.qpos[env_ids]
        root = qpos[:, q_adr[0:3]]
        ryaw = yaw_of(qpos[:, q_adr[3:7]])
        radius = self.radius_env[env_ids, shape]

        def U(lo, hi):
            return lo + torch.rand(m, device=dev) * (hi - lo)

        def sym_u(half_deg):
            return torch.deg2rad(half_deg) * (2 * torch.rand(m, device=dev) - 1)

        bearing = ryaw + sym_u(t[:, BEARING])
        dist = c.robot_reach + radius + U(c.gap[0], c.gap[1])
        obj_xy = root[:, :2] + dist.unsqueeze(-1) * torch.stack([torch.cos(bearing), torch.sin(bearing)], -1)
        obj_heading = bearing + sym_u(t[:, BOX_YAW])
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
            st[:, 2] = self.rest_env[env_ids, k] + 0.005
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
        # images for the new episode, from the poses just written (the sim's body poses are
        # only updated at the next forward pass)
        cs, sn = torch.cos(ryaw), torch.sin(ryaw)
        dxy = obj_xy - root[:, :2]
        rel_xy = torch.stack([cs * dxy[:, 0] + sn * dxy[:, 1], -sn * dxy[:, 0] + cs * dxy[:, 1]], -1)
        rel_yaw = torch.zeros(m, device=dev) if self.heading_zero_map else wrap(obj_heading - ryaw)
        self.refresh_profiles(env_ids, rel_xy, rel_yaw)
        # precise-pose potential of the new start (the goal is >= 1 m away, so ~0)
        self.prev_precise[env_ids] = 0.0


@dataclass(kw_only=True)
class Push2CommandCfg(HardGoalCommandCfg):
    variant: str = "a"  # "a" object-frame profiles | "b" robot-frame top map | "ctrl" no images
    map_hz: float = 10.0  # how often the robot-frame map is recomputed (variant b)
    allow_heldout: bool = False  # eval only: let the sampler pick held-out shapes
    # "hold": Stage 1b's rule (inside the level's tolerance for the level's hold time, the
    # episode then runs on to its time limit). "terminate": success = inside success_pos_tol /
    # success_yaw_tol_deg with the object nearly at rest; the episode ends there (goal_reached
    # termination + goal_bonus reward) and a new one starts.
    success_mode: str = "hold"
    success_pos_tol: float = 0.10
    success_yaw_tol_deg: float = 3.0
    success_max_speed: float = 0.15  # m/s, object nearly at rest
    success_max_yaw_rate: float = 0.3  # rad/s

    def build(self, env) -> Push2Command:
        return Push2Command(self, env)


# ---------------------------------------------------------------------------------
# events
# ---------------------------------------------------------------------------------
@requires_model_fields("geom_size", "geom_pos", "geom_rbound", "geom_aabb")
def randomize_geometry(env, env_ids: torch.Tensor | None, factor_range: tuple[float, float] = FACTOR_RANGE):
    """Startup: draw size factors per env and shape (uniform in factor_range, per axis),
    resize the object's geoms (and its goal marker) to match, and give the command term the
    new part geometry."""
    if env_ids is None:
        env_ids = torch.arange(env.num_envs, device=env.device)
    env_ids = env_ids.to(env.device, dtype=torch.long)
    lo, hi = factor_range
    for k in range(len(SHAPES2)):
        apply_geometry(env, env_ids, k, lo + (hi - lo) * torch.rand(len(env_ids), 3, device=env.device))
    _g(env).refresh_profiles(env_ids)  # the active objects' images must reflect the new sizes
    fix_render_frames(env)


def apply_geometry(env, env_ids: torch.Tensor, k: int, f: torch.Tensor) -> None:
    """Give shape k size factors f (len(env_ids), 3) in env_ids: sim geoms, goal marker and
    the command term's part table. Used by the startup event and by the evaluation."""
    from mjlab.envs.mdp.dr.geom import _recompute_geom_bounds

    g = _g(env)
    shape, obj, goal = SHAPES2[k], g.objs[k], g.goals[k]
    parts, rest = shape_parts(shape.name, f)
    g.set_geometry(env_ids, k, parts, rest)
    kinds = g.kinds[k]
    n_parts = int((kinds != KIND_NONE).sum())
    size, pos = geom_size_pos(parts, kinds.unsqueeze(0))
    gids = obj.indexing.geom_ids[:n_parts].to(torch.long)
    eg, gg = torch.meshgrid(env_ids, gids, indexing="ij")
    env.sim.model.geom_size[eg, gg] = size[:, :n_parts]
    env.sim.model.geom_pos[eg, gg] = pos[:, :n_parts]
    _recompute_geom_bounds(env, env_ids.to(torch.int), SceneEntityCfg(OBJ_NAMES2[k]))
    # goal marker: the footprint, 3 cm larger, as flat boxes (or a flat disc for spheres)
    mids = goal.indexing.geom_ids[:n_parts].to(torch.long)
    em, mm = torch.meshgrid(env_ids, mids, indexing="ij")
    p = parts[:, :n_parts]
    sph = (kinds[:n_parts] == KIND_SPHERE).unsqueeze(0)
    msize = torch.stack([p[..., 3] + 0.03, p[..., 4] + 0.03, torch.full_like(p[..., 3], 0.002)], -1)
    msize = torch.where(sph.unsqueeze(-1), torch.stack([p[..., 3] + 0.03, torch.full_like(p[..., 3], 0.002),
                                                        torch.zeros_like(p[..., 3])], -1), msize)
    mpos = torch.stack([p[..., 0], p[..., 1], torch.zeros_like(p[..., 0])], -1)
    env.sim.model.geom_size[em, mm] = msize
    env.sim.model.geom_pos[em, mm] = mpos
    _recompute_geom_bounds(env, env_ids.to(torch.int), SceneEntityCfg(GOAL_NAMES2[k]))


def fix_render_frames(env) -> None:
    """Make our own renders (eval videos, snapshots, check sheets) draw rotated geoms correctly.

    Host-side MuJoCo (used only for rendering) shortcuts a single-geom body's geom pose to
    its inertia frame (``geom_sameframe``). The mass randomization rewrites the inertia frame,
    so a plain host render drew e.g. the lying cylinder standing up. MuJoCo Warp (the physics)
    does not use the shortcut, so the simulation was always right; mjlab's own training-video
    renderer already clears these flags."""
    from mjlab.viewer.model_sync import disable_model_sameframe_shortcuts

    disable_model_sameframe_shortcuts(env.sim.mj_model)


# ---------------------------------------------------------------------------------
# observations
# ---------------------------------------------------------------------------------
def _g(env) -> Push2Command:
    return env.command_manager.get_term("goal")


def _to_robot(env, v_w: torch.Tensor) -> torch.Tensor:
    v = torch.zeros(v_w.shape[0], 3, device=env.device)
    v[:, :2] = v_w[:, :2]
    return quat_apply_inverse(yaw_quat(env.scene["robot"].data.root_link_quat_w), v)[:, :2]


def box_obs(env) -> torch.Tensor:
    """Stage 1b's 7 numbers (position, folded heading sin/cos, velocity, yaw rate); the
    heading is the one the policy is told (0 under the heading ablation)."""
    g = _g(env)
    robot = env.scene["robot"]
    pos = _to_robot(env, g.box_pos() - robot.data.root_link_pos_w)
    rel = g.obs_rel_yaw()
    k = g.symmetry()
    return torch.cat([pos, torch.sin(k * rel).unsqueeze(-1), torch.cos(k * rel).unsqueeze(-1),
                      _to_robot(env, g.box_vel()), g.box_ang_vel()[:, 2:3]], dim=-1)


def object_desc(env) -> torch.Tensor:
    """Stage 1b's 12-number descriptor, from this env's randomized geometry."""
    g = _g(env)
    s = g.shape
    ids = torch.arange(env.num_envs, device=env.device)
    body = torch.tensor([o.indexing.body_ids[0] for o in g.objs], device=env.device)[s]
    com = env.sim.model.body_ipos[ids, body][:, :2]
    sym = g.sym[s]
    onehot = torch.stack([sym == 0, sym == 1, sym == 2, sym == 4], -1).float()
    return torch.cat([g.bbox_env[ids, s], com, onehot, g.roller[s].float().unsqueeze(-1),
                      g.radius_env[ids, s].unsqueeze(-1)], dim=-1)


def _image(g: Push2Command, img: torch.Tensor) -> torch.Tensor:
    if g.profile_mode == "zero":
        return torch.zeros_like(img)
    if g.profile_mode == "roll":
        return torch.roll(img, shifts=g.profile_roll, dims=0)
    return img


def profile_top(env) -> torch.Tensor:
    return _image(_g(env), _g(env).profile_top)


def profile_front(env) -> torch.Tensor:
    return _image(_g(env), _g(env).profile_front)


def last_action_clipped(env) -> torch.Tensor:
    """The last action as the walker received it (clipped to [-1, 1])."""
    return env.action_manager.action.clamp(-1.0, 1.0)


# ---------------------------------------------------------------------------------
# rewards / curriculum
# ---------------------------------------------------------------------------------
def action_rate_clipped(env) -> torch.Tensor:
    """Squared change of the command the walker actually gets (clipped actions).

    Stage 1b's version used the raw policy output. Once outputs drift past the clip
    (nothing stops them: every value beyond 1 gives the same command), that term charges
    (60)^2 for reversing a saturated command and nothing for staying pinned, so the policy
    became bang-bang with outputs of 20-35."""
    a = env.action_manager.action.clamp(-1.0, 1.0)
    p = env.action_manager.prev_action.clamp(-1.0, 1.0)
    return torch.sum(torch.square(a - p), dim=-1)


def action_beyond_limit(env) -> torch.Tensor:
    """How far the raw policy output is past the walker's [-1, 1] clip (summed over vx, vy, wz).
    Linear, so a saturated warm start is pulled back steadily rather than blown up."""
    return torch.sum(torch.relu(env.action_manager.action.abs() - 1.0), dim=-1)


def goal_reached(env) -> torch.Tensor:
    """Termination (success_mode "terminate"): the object is at the goal pose and at rest."""
    return _g(env).success_flag.clone()


def goal_bonus(env, horizon_s: float, floor: float = 0.25) -> torch.Tensor:
    """One-off reward on the success step, larger the earlier it comes: 1 at t = 0 falling
    linearly to `floor` at t = horizon_s (the episode limit)."""
    t = env.episode_length_buf.float() * env.step_dt
    scale = torch.clamp(1.0 - (1.0 - floor) * t / horizon_s, min=floor)
    return _g(env).success_flag.float() * scale


def precise_progress(env) -> torch.Tensor:
    """Change of the precise-pose potential per second (clipped): pays for closing the last
    centimetres and degrees, and only for closing them, so there is no reward for lingering
    near the goal instead of finishing."""
    g = _g(env)
    return torch.clamp((g.precise_value() - g.prev_precise) / env.step_dt, -1.0, 1.0)


def failed(env, names: tuple[str, ...] = ("fell_over", "box_tipped", "box_lost")) -> torch.Tensor:
    """A failure termination this step (unlike envs_mdp.is_terminated, not a success)."""
    tm = env.termination_manager
    out = torch.zeros(env.num_envs, dtype=torch.bool, device=env.device)
    for n in names:
        if n in tm.active_terms:
            out |= tm.get_term(n)
    return out.float()


def near_surface(env, std: float = 0.4) -> torch.Tensor:
    """1 when the robot's front is at the object's surface, falling off over ~std metres."""
    d = _g(env).surface_distance().clamp(min=0.0)
    return 1.0 - torch.tanh(torch.clamp(d - 0.05, min=0.0) / std)


def push2_curriculum(env, env_ids: torch.Tensor, advance: float = 0.55, retreat: float = 0.15,
                     dwell_iters: int = 75, ema: float = 0.02, steps_per_iter: int = 24,
                     min_weight: float = 0.15, allow_level: bool = True):
    g = _g(env)
    it = env.common_step_counter / steps_per_iter
    if isinstance(env_ids, torch.Tensor) and len(env_ids) > 0:
        succ = g.metrics["success"][env_ids]
        for k in range(len(g.shape_list)):
            sel = g.shape[env_ids] == k
            if sel.any():
                g.shape_success[k] = 0.95 * g.shape_success[k] + 0.05 * succ[sel].mean()
        g.shape_weight[:] = (1.0 - g.shape_success).clamp(min=min_weight)
        at_level = g.env_level[env_ids] == g.level
        if at_level.any():
            s = float(succ[at_level].mean())
            w = min(1.0, ema * int(at_level.sum()))
            g.ema_success = (1 - w) * g.ema_success + w * s
            if allow_level and it - g.last_change_iter >= dwell_iters:
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
    for k, s in enumerate(g.shape_list):
        if bool(g.train_mask[k]):
            out[f"success_{s.name}"] = g.shape_success[k].detach().clone()
    return out

