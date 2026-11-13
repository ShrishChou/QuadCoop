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

Contact mode (``contact_mode``, Stage 4): each episode both robots are assigned a contact from the
object's candidate contacts (quadcoop/contacts.py) - a pair picked for the goal direction by the
"spread" or "adjacent" rule or at random (``contact_mix``) - and start at it (at its standing
point, or with probability 1 - ``contact_start_at`` at its approach point). Each robot's input
gains its contact (``contact_obs``: where it is, which way to push, its arm about the centre of
mass, and the partner's contact). A robot is on its contact when its front is within
``drift_dist`` m of the contact point *and* it faces the contact's push direction within
``drift_heading_deg`` (so walking round a corner onto another face while pressing on the object
is leaving the contact, even on a small object where the faces' centres are close). A robot that
has reached its contact and then is off it for ``drift_s`` s, or never reaches it within
its reach limit (time for the distance), ends the episode as a failure (``off_contact``).
With ``off_contact_mode = "soft"`` (the default for new runs) nothing about contacts ends an
episode and there are no deadlines: a robot is pulled toward its assigned contact by a
potential-based reward (``contact_approach``: pays for getting closer - distance plus heading -
and takes it back for moving away), and once it has reached its contact it pays a cost per
second while off it (``off_contact_cost``); a robot still on its way to a new contact pays
nothing. The time a robot takes to reach a contact is logged, not enforced: r7's goal-error cost
per second already makes slow transitions expensive. With ``guide`` (Stage 4d) each robot is also given a route to its contact: a geometric planner,
recomputed every step in the object's frame (so it moves and turns with the object), leads
around the object's bounding box inflated by ``guide_margin`` (in the shorter direction, via its
corners), backs a robot out first if it is inside that margin away from its contact, and ends
with the straight lane from the contact's approach point to its standing point. The robot gets
the next waypoint, the route length left, the contact's velocity and an on-contact flag
(``guide_obs``); the pull to the contact pays for shortening the route (not the straight line),
and touching the object anywhere while not on its contact costs ``bump_cost`` per second (contact
sensors). With ``disturb_frac`` a share of training episodes move and turn the object by script
for a few seconds (as a partner or a turn would), so keeping up with a moving contact is
practised. With ``reselect_s`` the rule is re-applied every few seconds from the object's current pose and
goal (Stage 4b): the pair changes when a contact no longer pushes toward the goal, or (spread /
adjacent) when a pair scores clearly better; at most one robot moves when possible, and it gets
a reach limit for the walk to its new contact. ``random_start`` robots start anywhere around the
object and walk to their contact themselves. Success tolerances can follow their own curriculum
(``tol_levels``: loose -> 10 cm / 3 deg, advancing on the success rate at the current tolerance;
the task-level curriculum waits until the finest tolerance is reached).

Per-robot observation and reward functions take the robot's entity name (``robot="spot"``).
Entity names come from quadcoop.coop2.pairs (QUADCOOP_PAIR): "anymal" and "spot" by default,
"anymal1"/"anymal2" or "spot1"/"spot2" for two robots of one type; agent order everywhere: AGENTS.
"""

from __future__ import annotations

import math
import os
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
from quadcoop.contacts import PLANNER_PARTS  # noqa: E402

_FOOTPRINT_OF_TYPE = {"anymal_c": (0.55, 0.30), "spot": (0.55, 0.28)}  # m: half-length, half-width
FOOTPRINT_HALF = {a: _FOOTPRINT_OF_TYPE[ROBOT_TYPE[a]] for a in AGENTS}  # partner map, body gap
SPREAD = 2  # level-table column 2: each robot's spread around "behind", +- deg
BEHIND = 3  # level-table column 3: "behind" rotated away from straight behind the object, +- deg
MASS_LO = 10  # extra column: lightest object at this level (kg)


def footprints_clear(stand: torch.Tensor, facing: torch.Tensor, half: tuple[tuple[float, float], tuple[float, float]],
                     margin: float) -> torch.Tensor:
    """Planner v2: (..., K, K) True where robot 0 standing at stand[..., i] facing facing[..., i] and
    robot 1 at stand[..., j] facing facing[..., j] keep their footprints (rectangles, half-length x
    half-width from `half`, each grown by margin) apart: a separating-axis test (stand, facing:
    (..., K, 2), facing unit)."""
    f = facing / torch.linalg.norm(facing, dim=-1, keepdim=True).clamp(min=1e-9)
    lat = torch.stack([-f[..., 1], f[..., 0]], -1)
    (l0, w0), (l1, w1) = [(h[0] + margin, h[1] + margin) for h in half]
    d = stand.unsqueeze(-2) - stand.unsqueeze(-3)  # (..., i, j, 2): j's centre minus i's
    fi, li = f.unsqueeze(-2), lat.unsqueeze(-2)  # robot 0's axes (index i)
    fj, lj = f.unsqueeze(-3), lat.unsqueeze(-3)  # robot 1's axes (index j)
    sep = torch.zeros(d.shape[:-1], dtype=torch.bool, device=d.device)
    for ax in (fi, li, fj, lj):
        ax = ax.expand_as(d)
        r0 = l0 * (fi * ax).sum(-1).abs() + w0 * (li * ax).sum(-1).abs()
        r1 = l1 * (fj * ax).sum(-1).abs() + w1 * (lj * ax).sum(-1).abs()
        sep |= (d * ax).sum(-1).abs() > r0 + r1
    return sep


def order_ok(theta0: torch.Tensor, theta1: torch.Tensor, phi: torch.Tensor, free_rad: float) -> torch.Tensor:
    """Planner v2: (m, K, K) True where giving contact i to robot 0 and contact j to robot 1 keeps
    the robots' order around the object: robot 1 lies counter-clockwise of robot 0 (theta: (m,),
    their bearings from the object's centre) and contact j lies counter-clockwise of contact i
    (phi: (m, K), the standing points' bearings), or the other way round for both. Robots (or
    contacts) about opposite each other (more than free_rad apart) have no order to keep."""
    dt = wrap(theta1 - theta0)  # (m,)
    dp = wrap(phi.unsqueeze(1) - phi.unsqueeze(2))  # (m, i, j): phi_j - phi_i
    same = (dp > 0) == (dt > 0).view(-1, 1, 1)
    return same | (dt.abs() > free_rad).view(-1, 1, 1) | (dp.abs() > free_rad)


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
        for k in ("success", "pos_err", "yaw_err_deg", "level", "hold_frac", "turn_task", "turn_success"):
            self.metrics[k] = torch.zeros(n, device=dev)
        self.shape_success = torch.zeros(S, device=dev)
        if cfg.train_shapes:  # explicit training set (overrides the Stage 2 train / held-out split)
            unknown = set(cfg.train_shapes) - {sh.name for sh in SHAPES2}
            assert not unknown, f"train_shapes: unknown shapes {sorted(unknown)}"
            self.train_mask = torch.tensor([sh.name in cfg.train_shapes for sh in SHAPES2], device=dev)
        else:
            self.train_mask = (torch.tensor(TRAIN_MASK, device=dev) if not cfg.allow_heldout
                               else torch.ones(S, dtype=torch.bool, device=dev))
        # episode starts by object x mass bin (cumulative; logged by the trainer, never used for sampling)
        self.reset_mass_edges = torch.arange(10.0, 91.0, 10.0, device=dev)  # 8 bins of 10 kg over 10-90
        self.reset_counts = torch.zeros(S, len(self.reset_mass_edges) - 1, device=dev)
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
        self.turn_episode = torch.zeros(n, dtype=torch.bool, device=dev)  # turn_frac pick
        # evaluation switches (as in Stage 2)
        self.heading_zero = False
        self.heading_zero_map = False
        self.profile_mode = "normal"
        self.profile_roll = 1
        # eval hook: callable(env_ids) -> dict overriding the placement (see scripts/eval_coop2.py)
        self.scenario = None
        # success-tolerance curriculum (per env: the tolerance its episode started with)
        self.tol_table = torch.tensor(cfg.tol_levels, device=dev) if cfg.tol_levels else None
        self.tol_level = (len(cfg.tol_levels) - 1 if cfg.tol_start_finest else 0) if cfg.tol_levels else 0
        self.tol_ema, self.tol_last_change = 0.0, 0.0
        self.lvl_ema = 0.0  # contact_curriculum's task-level rate
        self.env_tol_level = torch.zeros(n, dtype=torch.long, device=dev)
        self.tol_pos = torch.full((n,), cfg.success_pos_tol, device=dev)
        self.tol_yaw = torch.full((n,), math.radians(cfg.success_yaw_tol_deg), device=dev)
        if cfg.contact_mode:
            self._build_contact_tables(nom, nom_rest)

    # -- contact mode ------------------------------------------------------------------------------
    def _build_contact_tables(self, nom: torch.Tensor, nom_rest: torch.Tensor) -> None:
        """Candidate contacts of every shape at nominal size (quadcoop/contacts.py), padded to K."""
        import numpy as np

        from quadcoop import contacts as C

        n, dev, S = self.num_envs, self.device, len(SHAPES2)
        kinds_np, nom_np, rest_np = self.kinds.cpu().numpy(), nom.cpu().numpy(), nom_rest.cpu().numpy()
        lists = [C.candidates(nom_np[s], kinds_np[s], float(rest_np[s]), face_ends=self.cfg.face_ends) for s in range(S)]
        K = max(len(x) for x in lists)
        self.c_K = K
        self.c_lists = lists
        self.c_p = torch.zeros(S, K, 2, device=dev)
        self.c_n = torch.zeros(S, K, 2, device=dev)
        self.c_n[..., 0] = 1.0
        self.c_pre = torch.zeros(S, K, 2, device=dev)
        self.c_valid = torch.zeros(S, K, dtype=torch.bool, device=dev)
        self.c_sep_ok = torch.zeros(S, K, K, dtype=torch.bool, device=dev)
        self.c_com = torch.zeros(S, 2, device=dev)
        for s, cl in enumerate(lists):
            for c in cl:
                self.c_p[s, c.index] = torch.tensor(c.p, dtype=torch.float)
                self.c_n[s, c.index] = torch.tensor(c.n, dtype=torch.float)
                self.c_pre[s, c.index] = torch.tensor(c.pre, dtype=torch.float)
                self.c_valid[s, c.index] = True
            st = np.stack([c.stand for c in cl]) if cl else np.zeros((0, 2))
            d = np.linalg.norm(st[:, None] - st[None], axis=-1) if len(cl) else np.zeros((0, 0))
            ok = (d >= self.cfg.contact_min_sep) & ~np.eye(len(cl), dtype=bool)
            self.c_sep_ok[s, :len(cl), :len(cl)] = torch.tensor(ok, device=dev)
            self.c_com[s] = torch.tensor(C.centre_of_mass(nom_np[s], kinds_np[s]), dtype=torch.float)
        # a lone sphere spins freely as it rolls: its contacts live in the frame it started with
        valid_parts = self.kinds >= 0
        self.c_free_spin = ((self.kinds == 1) | ~valid_parts).all(-1)
        self.c_bbox_nom = self.bbox_env[0, :, 2:4].clone()  # nominal half extents (before the startup event)
        self.c_idx = torch.zeros(n, 2, dtype=torch.long, device=dev)
        self.c_pobj = torch.zeros(n, 2, 2, device=dev)
        self.c_nobj = torch.zeros(n, 2, 2, device=dev)
        self.c_nobj[..., 0] = 1.0
        self.c_comobj = torch.zeros(n, 2, device=dev)
        self.c_yaw0 = torch.zeros(n, device=dev)
        self.c_engaged = torch.zeros(n, 2, dtype=torch.bool, device=dev)
        self.c_drift_t = torch.zeros(n, 2, device=dev)
        self.c_free_t = torch.zeros(n, 2, device=dev)
        self.c_rule = torch.zeros(n, dtype=torch.long, device=dev)  # 0 spread, 1 adjacent, 2 random
        self.c_reach_lim = torch.full((n, 2), self.cfg.engage_s, device=dev)  # s to reach the assigned contact
        self.c_reselect_t = torch.full((n,), 1e9, device=dev)  # s until the next re-selection
        self.c_switches = torch.zeros(n, device=dev)  # contact changes this episode
        self.c_prev_phi = torch.zeros(n, 2, device=dev)  # contact-approach potential, last step
        self.c_preobj = torch.zeros(n, 2, 2, device=dev)  # approach points (object frame, scaled)
        self.c_time = torch.zeros(n, device=dev)  # s since the episode started
        self.d_t0 = torch.full((n,), 1e9, device=dev)  # scripted object motion: start, end (s), velocity
        self.d_t1 = torch.full((n,), -1.0, device=dev)
        self.d_vel = torch.zeros(n, 3, device=dev)  # vx, vy, wz (world)
        self.c_reach_sum, self.c_reach_cnt = 0.0, 0  # walk-to-contact times (s) since the last log
        # Stage 4e: the object's turning scales, the motion still wanted and each robot's push
        self.c_cg = torch.ones(n, device=dev)  # ground-contact radius (m): friction torque / friction force
        self.c_rg = torch.ones(n, device=dev)  # radius of gyration sqrt(I_zz / m) (m)
        self.c_vdes = torch.zeros(n, 2, device=dev)  # wanted object velocity (world, m/s)
        self.c_wdes = torch.zeros(n, device=dev)  # wanted yaw rate (rad/s)
        self.push_dir_obj = torch.zeros(n, 2, 2, device=dev)  # each robot's push direction (object frame, unit)
        self.push_dir_obj[..., 0] = -1.0
        self.push_share = torch.full((n, 2), 0.5, device=dev)  # each robot's share of the total push
        self.c_resid = torch.zeros(n, device=dev)  # part of the wanted push the current pair cannot make (0..1)
        self.c_res_t = torch.zeros(n, device=dev)  # s the residual has been above resid_bad
        self.c_prev_pose = torch.zeros(n, device=dev)  # distance + rho_g x angle error, last step (pose_progress)
        # expert planner v2 (rule 4)
        self.virt_xy = None  # (n, 2, 2) virtual robot centres (test rigs); None = the simulated robots
        self.virt_yaw = None  # (n, 2)
        self.c_prio = torch.zeros(n, 2, device=dev)  # priority: who yields to whom (higher wins)
        self.c_arrive = torch.zeros(n, 2, device=dev)  # expected seconds until each robot is on its contact
        self.c_phase = torch.zeros(n, 2, dtype=torch.long, device=dev)  # 0 walk, 1 hold, 2 push
        self.c_left_idx = torch.full((n, 2), -1, dtype=torch.long, device=dev)  # contact each robot last left ...
        self.c_left_t = torch.full((n, 2), -1e9, device=dev)  # ... and when (s, c_time)
        self.c_win_t = torch.zeros(n, device=dev)  # no-progress window: time in it,
        self.c_win_xy = torch.zeros(n, 2, device=dev)  # the object's pose at its start
        self.c_win_pe = torch.full((n,), 1e6, device=dev)  # ... and its pose error then (finishing zone)
        self.c_fin_stalls = torch.zeros(n, device=dev)  # no-progress windows in the finishing zone (logged)
        self.c_fin = torch.zeros(n, dtype=torch.bool, device=dev)  # the last window: no progress in the zone
        self.c_win_yaw = torch.zeros(n, device=dev)
        self.c_stalled = torch.zeros(n, dtype=torch.bool, device=dev)  # the last window saw no progress
        # the last re-plan's cause (logged): 0 reset, 1 timer, 2 wrench residual, 3 no progress, 4 weak pair,
        # 5 finish, 6 slow arrival; and re-plans run this episode (a re-plan may keep the same pair)
        self.c_plan_reason = torch.zeros(n, dtype=torch.long, device=dev)
        self.c_plan_n = torch.zeros(n, device=dev)
        # assignment decisions: None = the env's contact rule (_reselect); else a callable (g, ids) that decides for
        # the expert-rule envs in ids and applies its choice through apply_assignment (coop2/coord.py)
        self.coordinator = None
        self.c_replans = torch.zeros(n, device=dev)  # re-plans by cause (logged): no progress,
        self.c_replan_slow = torch.zeros(n, device=dev)  # slow arrival
        self.c_slow_wait = torch.zeros(n, device=dev)  # s until a slow-arrival re-plan may fire again (slow_min_s)
        self.c_rhist = torch.zeros(n, 2, RESID_H, RESID_HF, device=dev)  # resid: per robot, newest first
        self.c_rhist_t = torch.zeros(n, device=dev)
        # resid: each robot's frozen base output (raw, unclipped) from the last step, written by the residual policy
        # wrapper before env.step and zeroed at reset, like the walker term's raw action. The base reads this as
        # its last_action, so it gets the same action history as when it runs alone.
        self.resid_base_last = torch.zeros(n, 2, 3, device=dev)
        self.c_replan_weak = torch.zeros(n, device=dev)  # and no progress the force model expects (pair at its limit)
        self.c_weak = torch.zeros(n, dtype=torch.bool, device=dev)  # the last window saw no progress, pair at its limit
        self.c_strength = torch.full((n,), 1e6, device=dev)  # current pair: most push along the wanted motion / sliding force
        self.c_need_more = torch.zeros(n, dtype=torch.bool, device=dev)  # no usable pair can slide the object
        self.c_need_more_t = torch.zeros(n, device=dev)  # s flagged (logged)
        # Phase 2 executor (exec_v2): the command each robot obeys and the team-ready barrier
        self.c_cmd = torch.zeros(n, 2, dtype=torch.long, device=dev)  # 0 walk, 1 hold, 2 push
        self.c_ready_t = torch.zeros(n, 2, device=dev)  # s steadily ready (front and heading on its contact)
        self.c_ready = torch.zeros(n, 2, dtype=torch.bool, device=dev)  # ready for ready_steady_s
        self.c_team_ready = torch.zeros(n, dtype=torch.bool, device=dev)  # every robot of the push group ready
        self.c_in_group = torch.ones(n, 2, dtype=torch.bool, device=dev)  # in the push group (an eval parks robot 2)
        self.c_rhold = torch.zeros(n, 2, device=dev)  # s left of a random hold (training)
        self.c_was_eng = torch.zeros(n, 2, dtype=torch.bool, device=dev)  # engaged last step (arrivals)
        self.c_was_idx = torch.full((n, 2), -1, dtype=torch.long, device=dev)  # contact last step (arrivals)
        self.c_go = torch.zeros(n, dtype=torch.bool, device=dev)  # the push group is pushing (latched)
        self.c_cmd_flips = torch.zeros(n, device=dev)  # push -> hold changes of the command (logged)
        self.c_mass = torch.ones(n, device=dev)
        self.c_exp_t = 0.0  # time since the last expert update
        self.c_mu = torch.full((n,), 0.5, device=dev)  # sliding friction: weight-averaged over the grounded parts
        self.c_cof = torch.zeros(n, 2, device=dev)  # centre of friction (object frame): friction-weighted pressure centroid
        self._part_geom = None  # (S, MAX_PARTS) geom index of each part
        print(f"[coop2] contact mode: {', '.join(f'{SHAPES2[s].name} {len(cl)}' for s, cl in enumerate(lists))} "
              f"candidate contacts; pairs >= {self.cfg.contact_min_sep:g} m apart; rule mix {self.cfg.contact_mix}")
        print(f"[coop2] planner: QUADCOOP_PLANNER={os.environ.get('QUADCOOP_PLANNER', 'ends')!r} -> face_ends={self.cfg.face_ends} "
              f"keep_order={self.cfg.keep_order} footprint_sep={self.cfg.footprint_sep}")

    def contact_frame_yaw(self) -> torch.Tensor:
        return torch.where(self.c_free_spin[self.shape], self.c_yaw0, self.heading())

    def contact_world(self, k: int) -> tuple[torch.Tensor, torch.Tensor]:
        """Robot k's assigned contact point and outward normal, world frame (n, 2) each."""
        yaw = self.contact_frame_yaw()
        cs, sn = torch.cos(yaw), torch.sin(yaw)

        def rot(v):
            return torch.stack([cs * v[:, 0] - sn * v[:, 1], sn * v[:, 0] + cs * v[:, 1]], -1)
        return self.box_pos()[:, :2] + rot(self.c_pobj[:, k]), rot(self.c_nobj[:, k])

    def contact_arm_world(self, k: int) -> torch.Tensor:
        yaw = self.contact_frame_yaw()
        cs, sn = torch.cos(yaw), torch.sin(yaw)
        v = self.c_pobj[:, k] - self.c_comobj
        return torch.stack([cs * v[:, 0] - sn * v[:, 1], sn * v[:, 0] + cs * v[:, 1]], -1)

    def robot_xy(self, k: int) -> torch.Tensor:
        """Robot k's centre (world xy); a test rig may substitute virtual robots (virt_xy)."""
        if self.virt_xy is not None:
            return self.virt_xy[:, k]
        return self.robots[AGENTS[k]].data.root_link_pos_w[:, :2]

    def robot_yaw(self, k: int) -> torch.Tensor:
        if self.virt_yaw is not None:
            return self.virt_yaw[:, k]
        return yaw_of(self.robots[AGENTS[k]].data.root_link_quat_w)

    def front_point(self, robot: str) -> torch.Tensor:
        k = AGENTS.index(robot)
        yaw = self.robot_yaw(k)
        return self.robot_xy(k) + self.reach[robot] * torch.stack([torch.cos(yaw), torch.sin(yaw)], -1)

    def contact_heading_err(self, k: int) -> torch.Tensor:
        """|robot k's heading - its push direction| (rad): the contact's -n, or with push_cmd the
        push direction the split asks of it."""
        if self.cfg.push_cmd:
            d = self.push_dir_world(k)
            want = torch.atan2(d[:, 1], d[:, 0])
        else:
            _, nw = self.contact_world(k)
            want = torch.atan2(-nw[:, 1], -nw[:, 0])
        return wrap(self.robot_yaw(k) - want).abs()

    def push_dir_world(self, k: int) -> torch.Tensor:
        """Robot k's push direction (world, unit), from the Stage 4e split."""
        yaw = self.contact_frame_yaw()
        cs, sn = torch.cos(yaw), torch.sin(yaw)
        v = self.push_dir_obj[:, k]
        return torch.stack([cs * v[:, 0] - sn * v[:, 1], sn * v[:, 0] + cs * v[:, 1]], -1)

    def contact_phi(self, k: int) -> torch.Tensor:
        """How far robot k is from being on its contact: front-to-contact distance (m) - with guide,
        the length of its route - plus phi_heading_weight x heading error (rad; with guide, only over
        the last metre of the route)."""
        if self.cfg.guide:
            _, route = self.guide(k)
            return route + self.cfg.phi_heading_weight * self.contact_heading_err(k) * (1.0 - route).clamp(0.0, 1.0)
        return self.contact_dist(k) + self.cfg.phi_heading_weight * self.contact_heading_err(k)

    def guide(self, k: int, pos_w: torch.Tensor | None = None, ids: torch.Tensor | None = None,
              target=None) -> tuple[torch.Tensor, torch.Tensor]:
        """Robot k's route to its contact: the next waypoint (world, (m, 2)) and the route length
        left (m, (m,)), planned in the object frame around the bounding box inflated by guide_margin.
        pos_w: the robot centre to plan from (default: where robot k is); ids: only these envs;
        target: (contact, normal, approach point) in the object frame, (m, 2) each, instead of
        robot k's contact (the expert planner prices candidate contacts with it)."""
        a = AGENTS[k]
        dev = self.device
        I = torch.arange(self.num_envs, device=dev) if ids is None else ids
        n = len(I)
        ar = torch.arange(n, device=dev)
        yaw = self.contact_frame_yaw()[I]
        cs, sn = torch.cos(yaw), torch.sin(yaw)
        obj = self.box_pos()[I, :2]
        bb = self.bbox_env[I, self.shape[I]]  # (cx, cy, hx, hy), object frame
        ctr = bb[:, :2]
        A = bb[:, 2:4] + self.cfg.guide_margin  # inflated half extents
        d = (self.robot_xy(k)[I] if pos_w is None else pos_w) - obj
        q = torch.stack([cs * d[:, 0] + sn * d[:, 1], -sn * d[:, 0] + cs * d[:, 1]], -1) - ctr  # robot centre
        pk, nk, prek = (self.c_pobj[I, k], self.c_nobj[I, k], self.c_preobj[I, k]) if target is None else target
        stand = pk + nk * (self.reach[a] + 0.06) - ctr
        pre = prek - ctr
        eps = 0.01
        S = A - eps  # boundary points count as outside: the route may run along the inflated box
        # the lane's outer end T: the approach point, pushed along the lane out of the box if it lies inside
        ld = pre - stand
        ld = ld / torch.linalg.norm(ld, dim=-1, keepdim=True).clamp(min=1e-6)
        pre_in = (pre.abs() < S).all(-1)
        sd = torch.where(ld.abs() > 1e-6, ld, torch.full_like(ld, 1e-6))
        s_exit = ((torch.sign(sd) * A - pre) / sd).min(-1).values.clamp(min=0.0)
        T = torch.where(pre_in.unsqueeze(-1), pre + (s_exit + 0.02).unsqueeze(-1) * ld, pre)
        lane_len = torch.linalg.norm(T - stand, dim=-1)
        # inside the inflated box: back out through the nearest side first (route measured to that side)
        inside = (q.abs() < S).all(-1)
        gap = A - q.abs()
        ax = (gap[:, 1] < gap[:, 0]).long()
        sgn = torch.where(q[ar, ax] >= 0, 1.0, -1.0)
        exit_pt = q.clone()
        exit_pt[ar, ax] = sgn * A[ar, ax]
        back_cue = q.clone()
        back_cue[ar, ax] = sgn * (A[ar, ax] + 0.15)
        start = torch.where(inside.unsqueeze(-1), exit_pt, q)
        # shortest path from start to T around the box: direct, or via 1-3 of its corners
        Ax, Ay = A[:, 0], A[:, 1]
        C = torch.stack([torch.stack([Ax, -Ay], -1), torch.stack([Ax, Ay], -1),
                         torch.stack([-Ax, Ay], -1), torch.stack([-Ax, -Ay], -1)], 1)  # ccw

        def clear(a, b):  # segment a->b keeps out of the open box S (a, b: (n, 2) or (n, m, 2))
            Sb = S.view(S.shape[0], *([1] * (a.dim() - 2)), 2)
            dv = b - a
            ok = dv.abs() > 1e-9
            inv = 1.0 / torch.where(ok, dv, torch.ones_like(dv))
            t1, t2 = (-Sb - a) * inv, (Sb - a) * inv
            within = a.abs() < Sb
            lo = torch.where(ok, torch.minimum(t1, t2), torch.where(within, -1e9, 1e9))
            hi = torch.where(ok, torch.maximum(t1, t2), torch.where(within, 1e9, -1e9))
            tmin, tmax = lo.max(-1).values.clamp(min=0.0), hi.min(-1).values.clamp(max=1.0)
            return tmax <= tmin + 1e-6

        INF = torch.full_like(Ax, 1e9)
        sC = clear(start.unsqueeze(1).expand(-1, 4, -1), C)  # (n, 4) corner visible from start
        Ct = clear(C, T.unsqueeze(1).expand(-1, 4, -1))  # (n, 4) T visible from corner
        dsC = torch.linalg.norm(C - start.unsqueeze(1), dim=-1)
        dCt = torch.linalg.norm(C - T.unsqueeze(1), dim=-1)
        side = torch.stack([2 * Ay, 2 * Ax, 2 * Ay, 2 * Ax], -1)  # edge i -> i+1 (ccw)
        cand = [torch.where(clear(start, T), torch.linalg.norm(T - start, dim=-1), INF)]
        first = [torch.full_like(Ax, -1, dtype=torch.long)]
        second = [first[0].clone()]  # the vertex after the first (-1: T)
        for i in range(4):
            cand.append(torch.where(sC[:, i] & Ct[:, i], dsC[:, i] + dCt[:, i], INF))
            first.append(torch.full_like(first[0], i)); second.append(torch.full_like(first[0], -1))
            for step in (1, -1):  # walk 1 or 2 more corners along the box, either way round
                run = torch.zeros_like(Ax)
                j = i
                for _ in range(2):
                    run = run + (side[:, j] if step == 1 else side[:, (j - 1) % 4])
                    j = (j + step) % 4
                    cand.append(torch.where(sC[:, i] & Ct[:, j], dsC[:, i] + run + dCt[:, j], INF))
                    first.append(torch.full_like(first[0], i)); second.append(torch.full_like(first[0], (i + step) % 4))
        cand, first, second = torch.stack(cand, -1), torch.stack(first, -1), torch.stack(second, -1)
        pick = cand
        if self.cfg.push_cmd or self.cfg.expert:  # a path whose first leg passes the partner is chosen as if longer
            dp = self.robot_xy(1 - k)[I] - obj
            qp = torch.stack([cs * dp[:, 0] + sn * dp[:, 1], -sn * dp[:, 0] + cs * dp[:, 1]], -1) - ctr
            V1 = torch.where((first >= 0).unsqueeze(-1), torch.gather(C, 1, first.clamp(min=0).unsqueeze(-1).expand(-1, -1, 2)),
                             T.unsqueeze(1).expand(-1, first.shape[1], -1))
            a0 = start.unsqueeze(1)
            ab = V1 - a0
            tt = (((qp.unsqueeze(1) - a0) * ab).sum(-1) / ab.square().sum(-1).clamp(min=1e-9)).clamp(0.0, 1.0)
            near = torch.linalg.norm(a0 + tt.unsqueeze(-1) * ab - qp.unsqueeze(1), dim=-1) < self.cfg.partner_clear
            if self.cfg.expert:  # expert planner: only the lower-priority robot yields the way
                near &= (self.c_prio[I, k] < self.c_prio[I, 1 - k]).unsqueeze(-1)
            pick = cand + near.float() * self.cfg.partner_block_m
        _, best = pick.min(-1)
        geo = cand[ar, best]
        geo = torch.where(geo < 1e8, geo, torch.linalg.norm(T - start, dim=-1))  # no clear path: straight
        fi, se = first[ar, best], second[ar, best]
        v1 = torch.where((fi >= 0).unsqueeze(-1), C[ar, fi.clamp(min=0)], T)
        v2 = torch.where((se >= 0).unsqueeze(-1), C[ar, se.clamp(min=0)], T)
        nxt_wp = torch.where((torch.linalg.norm(v1 - start, dim=-1) < 0.05).unsqueeze(-1), v2, v1)  # at that corner already
        out_route = torch.where(inside, torch.linalg.norm(q - exit_pt, dim=-1), torch.zeros_like(Ax)) + geo + lane_len
        wp = torch.where(inside.unsqueeze(-1), back_cue, nxt_wp)
        # near the lane (or the standing point): blend into going straight to the standing point
        lane = T - stand
        t = (((q - stand) * lane).sum(-1) / lane_len.square().clamp(min=1e-9)).clamp(0.0, 1.0)
        off_lane = torch.linalg.norm(q - (stand + t.unsqueeze(-1) * lane), dim=-1)
        to_stand = torch.linalg.norm(q - stand, dim=-1)
        w = torch.maximum(((0.4 - off_lane) / 0.2).clamp(0.0, 1.0), ((0.6 - to_stand) / 0.2).clamp(0.0, 1.0))
        route = w * torch.minimum(to_stand, out_route) + (1.0 - w) * out_route
        wp = torch.where((w > 0.5).unsqueeze(-1), stand, wp)
        wp = wp + ctr
        wp_w = obj + torch.stack([cs * wp[:, 0] - sn * wp[:, 1], sn * wp[:, 0] + cs * wp[:, 1]], -1)
        return wp_w, route

    def contact_velocity(self, k: int) -> torch.Tensor:
        """World velocity of robot k's contact point (the object's velocity plus its turning)."""
        pw, _ = self.contact_world(k)
        r = pw - self.box_pos()[:, :2]
        w = self.box_ang_vel()[:, 2]
        return self.box_vel()[:, :2] + torch.stack([-w * r[:, 1], w * r[:, 0]], -1)

    def on_contact(self, k: int) -> torch.Tensor:
        return (self.contact_dist(k) < self.cfg.drift_dist) & \
            (self.contact_heading_err(k) < math.radians(self.cfg.drift_heading_deg))

    def contact_dist(self, k: int) -> torch.Tensor:
        """Distance from robot k's front to its assigned contact point (m)."""
        return torch.linalg.norm(self.front_point(AGENTS[k]) - self.contact_world(k)[0], dim=-1)

    # -- Stage 4e: wanted motion, push split, pair residuals --------------------------------------
    def _set_radii(self, env_ids: torch.Tensor) -> None:
        """Per env (current shape, randomised size, uniform density): the radius of gyration
        sqrt(I_zz / m) about the centre of mass, and the ground-contact radius c = mean distance
        from the centre of mass over the footprint resting on the floor (grounded parts carry
        weight in proportion to their mass, spread evenly over their footprint: a box's rectangle,
        a lying cylinder's line, a sphere's point). For quasi-static sliding c sets the largest
        friction torque against the largest friction force."""
        parts, kinds, _ = self.active(env_ids)
        valid = kinds >= 0
        cx, cy, cz, hx, hy, hz = parts.unbind(-1)
        sph, cyl = kinds == 1, kinds == 2
        vol = torch.where(sph, 4.0 / 3.0 * math.pi * hx ** 3, torch.where(cyl, math.pi * hx * hx * 2 * hy, 8 * hx * hy * hz))
        vol = torch.where(valid, vol, torch.zeros_like(vol))
        mass = vol.sum(-1).clamp(min=1e-9)
        com = (vol.unsqueeze(-1) * parts[..., :2]).sum(1) / mass.unsqueeze(-1)
        own = torch.where(sph, 0.4 * hx ** 2, torch.where(cyl, hx ** 2 / 4 + hy ** 2 / 3, (hx ** 2 + hy ** 2) / 3))
        r2 = (parts[..., :2] - com.unsqueeze(1)).square().sum(-1)
        self.c_rg[env_ids] = ((vol * (own + r2)).sum(-1) / mass).sqrt().clamp(min=0.05)
        zb = torch.where(valid, cz - torch.where(sph | cyl, hx, hz), torch.full_like(cz, 1e9))
        grounded = valid & (zb <= zb.min(-1, keepdim=True).values + 0.02)
        G = 8
        u = (torch.arange(G, device=self.device, dtype=torch.float) + 0.5) / G * 2 - 1
        ux, uy = torch.meshgrid(u, u, indexing="ij")
        ux, uy = ux.flatten(), uy.flatten()  # (G*G,)
        sx = torch.where(sph | cyl, torch.zeros_like(hx), hx).unsqueeze(-1) * ux
        sy = torch.where(sph, torch.zeros_like(hy), hy).unsqueeze(-1) * uy
        px, py = cx.unsqueeze(-1) + sx, cy.unsqueeze(-1) + sy  # (m, P, G*G)
        dist = torch.sqrt((px - com[:, 0, None, None]) ** 2 + (py - com[:, 1, None, None]) ** 2).mean(-1)
        w = torch.where(grounded, vol, torch.zeros_like(vol))
        self.c_cg[env_ids] = ((w * dist).sum(-1) / w.sum(-1).clamp(min=1e-9)).clamp(min=0.05)
        # expert: friction acts about the centre of friction (pressure x friction centroid; the centre of mass
        # unless the parts' friction differs, as on the split-friction box), with the weight-averaged friction
        # coefficient, and the ground-contact radius taken about that centre
        if self.cfg.expert:
            if self._part_geom is None:
                P = parts.shape[1]
                self._part_geom = torch.tensor([[int(o.indexing.geom_ids[min(i, len(o.indexing.geom_ids) - 1)]) for i in range(P)]
                                                for o in self.objs], device=self.device, dtype=torch.long)
                self._part_frac = torch.tensor([[sh.parts[i].mass_frac if i < len(sh.parts) else 0.0 for i in range(P)]
                                                for sh in SHAPES2], device=self.device)
            gf = self._env.sim.model.geom_friction
            shp = self.shape[env_ids]
            gids = self._part_geom[shp]  # (m, P)
            mu_p = gf[env_ids.unsqueeze(-1), gids, 0] if gf.dim() == 3 else gf[gids, 0]
            frac = torch.where(valid, self._part_frac[shp], torch.zeros_like(vol))
            # the centre of mass as simulated (mass randomisation can move it off the geometric one)
            body = torch.tensor([o.indexing.body_ids[0] for o in self.objs], device=self.device)[shp]
            ip = self._env.sim.model.body_ipos
            com_m = (ip[env_ids, body] if ip.dim() == 3 else ip[body])[:, :2]
            wg = torch.where(grounded, frac, torch.zeros_like(frac))  # load carried by each grounded part
            wm = wg * mu_p
            xw = (wg.unsqueeze(-1) * parts[..., :2]).sum(1) / wg.sum(-1, keepdim=True).clamp(min=1e-9)
            # static balance puts the pressure centroid under the centre of mass; unequal friction shifts the
            # friction centroid from there toward the grippier parts
            cof = com_m + (wm.unsqueeze(-1) * (parts[..., :2] - xw.unsqueeze(1))).sum(1) / wm.sum(-1, keepdim=True).clamp(min=1e-9)
            self.c_cof[env_ids] = cof
            self.c_mu[env_ids] = wm.sum(-1) / wg.sum(-1).clamp(min=1e-9)
            dist_f = torch.sqrt((px - cof[:, 0, None, None]) ** 2 + (py - cof[:, 1, None, None]) ** 2).mean(-1)
            self.c_cg[env_ids] = ((wm * dist_f).sum(-1) / wm.sum(-1).clamp(min=1e-9)).clamp(min=0.05)

    def _wanted(self, ep: torch.Tensor, e: torch.Tensor, sym: torch.Tensor, turn_mask: torch.Tensor | None = None):
        """Wanted object velocity (same frame as ep, the vector to the goal) and yaw rate for the
        error (ep, e): both asked for at once, each saturating at push_vmax / push_wmax."""
        c = self.cfg
        dist = torch.linalg.norm(ep, dim=-1, keepdim=True)
        v = c.push_vmax * ep / dist.clamp(min=1e-6) * (dist / c.push_rv).clamp(max=1.0)
        e = torch.where(sym > 0, e, torch.zeros_like(e))
        w = c.push_wmax * (e / c.push_rw).clamp(-1.0, 1.0)
        if c.turn_full_dist > 0:  # far from the goal travel leads: the turn is asked for in proportion
            # (turn_mask: only these envs, so other rules run alongside the expert keep their own motion)
            fac = (c.turn_full_dist / dist.squeeze(-1).clamp(min=1e-6)).clamp(max=1.0)
            if turn_mask is not None:
                fac = torch.where(turn_mask, fac, torch.ones_like(fac))
            w = w * fac
        return v, w

    def _split(self, p, nn, com, v, wz, cg, cap=None):
        """Split a wanted motion over two contacts (object frame). p, nn: (B, 2, 2) contact points and
        outward normals; com (B, 2); v (B, 2) wanted velocity; wz (B,) wanted yaw rate; cg (B,)
        ground-contact radius. Under an ellipsoidal limit surface the wrench for that motion is
        proportional to (v, cg^2 wz); compared in force units as (F, tau / cg) against (v, cg wz).
        Each robot pushes inside its friction cone (half angle atan(push_mu)) and cannot pull:
        a non-negative least-squares fit over the four cone edges with a ridge penalty push_ridge x
        |coefficients|^2, so a pair that could only make the motion with large forces (squeezing
        the object from two sides and dragging it by friction) scores badly; solved exactly by
        trying every set of edges. Returns forces (B, 2, 2) (relative sizes) and the
        residual (B,) = |unmatched part| / |wanted|, 0..1 (0 when nothing is wanted; about 0.1 for
        an ideal pair, because of the ridge). cap (B,), optional: the most one robot can push, as a
        share of the force that slides the object (robot force / (mu m g)); when the free split asks
        a robot for more, the fit is redone with each robot's force bounded by cap (exact, see
        _bounded_fit), so the shares respect the limit; the residual is then the direction error of
        the best bounded wrench that still slides the object, or 1 if none does (a pair that needs
        one robot to slide a heavy object by itself scores badly)."""
        B, dev = p.shape[0], p.device
        ha = math.atan(self.cfg.push_mu)
        d0 = -nn  # (B, 2, 2)
        cs, sn = math.cos(ha), math.sin(ha)
        e_plus = torch.stack([cs * d0[..., 0] - sn * d0[..., 1], sn * d0[..., 0] + cs * d0[..., 1]], -1)
        e_minus = torch.stack([cs * d0[..., 0] + sn * d0[..., 1], -sn * d0[..., 0] + cs * d0[..., 1]], -1)
        E = torch.stack([e_plus[:, 0], e_minus[:, 0], e_plus[:, 1], e_minus[:, 1]], 1)  # (B, 4, 2)
        R = torch.stack([p[:, 0], p[:, 0], p[:, 1], p[:, 1]], 1) - com.unsqueeze(1)
        tq = (R[..., 0] * E[..., 1] - R[..., 1] * E[..., 0]) / cg.unsqueeze(-1)
        M = torch.cat([E, tq.unsqueeze(-1)], -1)  # (B, 4, 3): rows = cone edges
        w = torch.cat([v, (cg * wz).unsqueeze(-1)], -1)  # (B, 3)
        wn = torch.linalg.norm(w, dim=-1)
        w = w / wn.unsqueeze(-1).clamp(min=1e-9)
        Gm = M @ M.transpose(1, 2)  # (B, 4, 4)
        b = (M @ w.unsqueeze(-1)).squeeze(-1)  # (B, 4)
        lam = self.cfg.push_ridge
        best_j = torch.ones(B, device=dev)  # objective of a = 0
        best_a = torch.zeros(B, 4, device=dev)
        import itertools
        for k in (1, 2, 3, 4):  # with the ridge the optimum may use all four edges
            for S in itertools.combinations(range(4), k):
                idx = torch.tensor(S, device=dev)
                Gs = Gm[:, idx][:, :, idx] + (lam + 1e-6) * torch.eye(k, device=dev)
                bs = b[:, idx]
                a = torch.linalg.solve(Gs, bs.unsqueeze(-1)).squeeze(-1)
                ok = (a >= -1e-7).all(-1)
                j = 1.0 - (bs * a).sum(-1)  # |Ma - w|^2 + lam |a|^2 at this subset's optimum
                take = ok & (j < best_j - 1e-9)
                best_j = torch.where(take, j, best_j)
                full = torch.zeros(B, 4, device=dev)
                full[:, idx] = a.clamp(min=0.0)
                best_a = torch.where(take.unsqueeze(-1), full, best_a)
        best_r2 = (1.0 - 2 * (b * best_a).sum(-1) + (best_a.unsqueeze(1) @ Gm @ best_a.unsqueeze(-1)).view(-1)).clamp(0.0, 1.0)
        if cap is not None:
            # the limit is on the robot's normal (pushing) force; edge coefficients a0 + a1 = normal / cos(half angle)
            cap = cap / cs
            # the free split's shape scaled to slide the object (|wrench| = 1: the ridge only shrinks sizes);
            # if a robot would then exceed its limit, refit with every robot bounded (and a vanishing ridge,
            # so the residual is the real shortfall: direction and size of what the pair can still make)
            size = (best_a.unsqueeze(1) @ Gm @ best_a.unsqueeze(-1)).view(-1).clamp(min=1e-12).sqrt()
            need = torch.stack([best_a[:, 0] + best_a[:, 1], best_a[:, 2] + best_a[:, 3]], -1) / size.unsqueeze(-1)
            over = (need > cap.unsqueeze(-1)).any(-1) & (wn > 1e-6)
            if bool(over.any()):
                # sliding is a threshold: a wrench inside the limit surface does not move the object, one
                # on or past it slides the object along (about) its own direction. So among the bounded
                # wrenches that slide the object (|wrench| >= 0.97) take the one closest in direction to
                # the wanted motion; the residual is then the direction error (1 - cos^2 of the angle),
                # and 1 when the pair cannot slide the object at all. Candidates: the bounded fit to the
                # wanted wrench scaled by 1 .. 2.5 (a larger target saturates the limits while keeping
                # the direction as close as the limits allow).
                Go, bo, co = Gm[over], b[over], cap[over]
                scales = torch.tensor([1.0, 1.25, 1.6, 2.5], device=dev)
                a_s = self._bounded_fit(Go, scales.view(1, -1, 1) * bo.unsqueeze(1), co, 1e-3)  # (m, 4 scales, 4)
                mag = torch.einsum("bsi,bij,bsj->bs", a_s, Go, a_s)
                al = (bo.unsqueeze(1) * a_s).sum(-1)
                r2_s = (1.0 - al.clamp(min=0.0).square() / mag.clamp(min=1e-12)).clamp(0.0, 1.0)
                r2_s = torch.where((mag >= 0.97 ** 2) & (al > 0), r2_s, torch.ones_like(r2_s))
                r2_b, js = r2_s.min(1)
                a_b = torch.gather(a_s, 1, js.view(-1, 1, 1).expand(-1, 1, 4)).squeeze(1)
                # no sliding wrench: keep the plain bounded fit's shares (the most the pair can do)
                stuck = r2_b >= 1.0 - 1e-9
                a_b = torch.where(stuck.unsqueeze(-1), a_s[:, 0], a_b)
                best_a = best_a.clone()
                best_a[over] = a_b
                best_r2 = best_r2.clone()
                best_r2[over] = torch.maximum(best_r2[over], r2_b)
        f = torch.stack([best_a[:, 0:1] * E[:, 0] + best_a[:, 1:2] * E[:, 1],
                         best_a[:, 2:3] * E[:, 2] + best_a[:, 3:4] * E[:, 3]], 1)
        none = wn < 1e-6
        return f, torch.where(none, torch.zeros_like(best_r2), best_r2.sqrt())

    def _pair_strength(self, p, nn, com, v, wz, cg, cap):
        """How hard a pair can push the way it should, in units of the force that slides the object:
        the largest component along the wanted wrench of a wrench the two robots can make inside
        their friction cones and force limits (cap, as in _split). >= 1: the pair can slide the
        object as wanted, so if it does not move the place is at fault; < 1: it cannot, and a slow
        object is a lack of strength, not a bad place. Large (about 4, the target used) when the
        limits do not bind; inf when nothing is wanted. Shapes as _split; returns (B,)."""
        B, dev = p.shape[0], p.device
        ha = math.atan(self.cfg.push_mu)
        d0 = -nn
        cs, sn = math.cos(ha), math.sin(ha)
        e_plus = torch.stack([cs * d0[..., 0] - sn * d0[..., 1], sn * d0[..., 0] + cs * d0[..., 1]], -1)
        e_minus = torch.stack([cs * d0[..., 0] + sn * d0[..., 1], -sn * d0[..., 0] + cs * d0[..., 1]], -1)
        E = torch.stack([e_plus[:, 0], e_minus[:, 0], e_plus[:, 1], e_minus[:, 1]], 1)
        R = torch.stack([p[:, 0], p[:, 0], p[:, 1], p[:, 1]], 1) - com.unsqueeze(1)
        tq = (R[..., 0] * E[..., 1] - R[..., 1] * E[..., 0]) / cg.unsqueeze(-1)
        M = torch.cat([E, tq.unsqueeze(-1)], -1)
        w = torch.cat([v, (cg * wz).unsqueeze(-1)], -1)
        wn = torch.linalg.norm(w, dim=-1)
        w = w / wn.unsqueeze(-1).clamp(min=1e-9)
        Gm = M @ M.transpose(1, 2)
        b = (M @ w.unsqueeze(-1)).squeeze(-1)
        # the bounded fit to a large target saturates the limits while keeping the direction as close as
        # they allow; its component along the wanted wrench is the pair's strength that way
        a = self._bounded_fit(Gm, 4.0 * b, cap / cs, 1e-3)
        s = (b * a).sum(-1).clamp(min=0.0)
        return torch.where(wn < 1e-6, torch.full_like(s, float("inf")), s)

    def current_strength(self, ids=None):
        """_pair_strength of each env's current pair (expert envs; inf elsewhere)."""
        ids = torch.arange(self.num_envs, device=self.device) if ids is None else ids
        out = torch.full((len(ids),), float("inf"), device=self.device)
        if not self.cfg.expert or len(ids) == 0:
            return out
        yaw = self.contact_frame_yaw()[ids]
        cs, sn = torch.cos(yaw), torch.sin(yaw)
        v_w = self.c_vdes[ids]
        v_o = torch.stack([cs * v_w[:, 0] + sn * v_w[:, 1], -sn * v_w[:, 0] + cs * v_w[:, 1]], -1)
        s = self._pair_strength(self.c_pobj[ids], self.c_nobj[ids], self.c_comobj[ids], v_o, self.c_wdes[ids],
                                self.c_cg[ids], self.robot_cap(ids))
        return torch.where(self.c_rule[ids] == 4, s, out)

    _BF_SETS: dict = {}

    @staticmethod
    def _bf_sets(dev):
        """Every active set of the bounded fit: which of the 4 coefficients are free (the rest are 0)
        and which robot limits bind (only robots with a free coefficient). Returned as masks
        (C, 4) and (C, 2), cached per device."""
        key = str(dev)
        if key not in CoopPush2Command._BF_SETS:
            import itertools
            mv, mc = [], []
            for k in (1, 2, 3, 4):
                for S in itertools.combinations(range(4), k):
                    robots = sorted({x // 2 for x in S})
                    for na in range(len(robots) + 1):
                        for A in itertools.combinations(robots, na):
                            mv.append([1.0 if x in S else 0.0 for x in range(4)])
                            mc.append([1.0 if r in A else 0.0 for r in range(2)])
            CoopPush2Command._BF_SETS[key] = (torch.tensor(mv, device=dev), torch.tensor(mc, device=dev))
        return CoopPush2Command._BF_SETS[key]

    @staticmethod
    def _bounded_fit(G, b, cap, lam, a0=None):
        """min a^T (G + lam I) a - 2 b^T a  over a >= 0 (4 cone-edge coefficients, robot 0 = a0, a1 and
        robot 1 = a2, a3) with a0 + a1 <= cap and a2 + a3 <= cap. Exact: the optimum solves the
        equality-constrained problem of its own active set (which coefficients are zero, which robot
        limits bind), so every active set is solved (one batched KKT system, padded to 6 x 6 with
        identity rows for the unused unknowns) and the best feasible solution kept (a = 0 is always
        feasible). b: (B, 4), or (B, M, 4) for M right-hand sides at once (returns (B, M, 4)).
        a0 is unused (kept for the call signature)."""
        dev = G.device
        multi = b.dim() == 3
        if not multi:
            b = b.unsqueeze(1)
        B, M = b.shape[0], b.shape[1]
        mv, mc = CoopPush2Command._bf_sets(dev)  # (C, 4), (C, 2)
        C = mv.shape[0]
        Rm = torch.tensor([[1.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 1.0]], device=dev)
        H = G + lam * torch.eye(4, device=dev)  # (B, 4, 4)
        Pv = mv.unsqueeze(-1) * mv.unsqueeze(-2)  # (C, 4, 4)
        K = torch.zeros(B, C, 6, 6, device=dev)
        K[:, :, :4, :4] = H.unsqueeze(1) * Pv + torch.diag_embed(1.0 - mv)
        Rc = mc.unsqueeze(-1) * Rm.unsqueeze(0) * mv.unsqueeze(1)  # (C, 2, 4) rows of the binding limits
        K[:, :, 4:, :4] = Rc
        K[:, :, :4, 4:] = Rc.transpose(1, 2)
        K[:, :, 4:, 4:] = torch.diag_embed(1.0 - mc)
        rhs = torch.zeros(B, C, 6, M, device=dev)
        rhs[:, :, :4] = (b.transpose(1, 2).unsqueeze(1) * mv.view(1, C, 4, 1))
        rhs[:, :, 4:] = (cap.view(B, 1, 1, 1) * mc.view(1, C, 2, 1)).expand(-1, -1, -1, M)
        sol = torch.linalg.solve(K, rhs)[:, :, :4]  # (B, C, 4, M)
        a = sol.permute(0, 1, 3, 2)  # (B, C, M, 4)
        capv = cap.view(B, 1, 1)
        ok = (a >= -1e-7).all(-1) & (a[..., 0] + a[..., 1] <= capv + 1e-6) & (a[..., 2] + a[..., 3] <= capv + 1e-6)
        a = a.clamp(min=0.0)
        jv = torch.einsum("bcmi,bij,bcmj->bcm", a, H, a) - 2 * (b.unsqueeze(1) * a).sum(-1)
        jv = torch.where(ok, jv, torch.full_like(jv, float("inf")))
        jbest, ib = jv.min(1)  # (B, M)
        best = torch.gather(a, 1, ib.view(B, 1, M, 1).expand(-1, 1, -1, 4)).squeeze(1)
        best = torch.where((jbest < -1e-12).unsqueeze(-1), best, torch.zeros_like(best))
        return best if multi else best.squeeze(1)

    def _pair_residuals(self, p, nn, com, v, wz, cg, use, chunk: int = 8192, cap=None):
        """Residual of every usable contact pair (m, K, K) for the wanted motion (v, wz) per env;
        1 where not usable. The physical residual does not depend on which robot takes which contact:
        computed once per unordered pair {i, j} usable either way round, mirrored, and only then
        masked by the (possibly directed, keep_order) assignment mask `use`. (Before 2026-11-10 only
        i < j was checked, so with a directed mask an allowed (j, i) assignment kept residual 1.)"""
        m, K = p.shape[0], p.shape[1]
        out = torch.ones(m, K, K, device=p.device)
        iu, ju = torch.triu_indices(K, K, 1, device=p.device)
        either = use | use.transpose(1, 2)
        e_ids, pr = torch.nonzero(either[:, iu, ju], as_tuple=True)
        for s0 in range(0, len(e_ids), chunk):
            e, q = e_ids[s0:s0 + chunk], pr[s0:s0 + chunk]
            i, j = iu[q], ju[q]
            pp = torch.stack([p[e, i], p[e, j]], 1)
            nq = torch.stack([nn[e, i], nn[e, j]], 1)
            _, r = self._split(pp, nq, com[e], v[e], wz[e], cg[e], None if cap is None else cap[e])
            out[e, i, j] = r
            out[e, j, i] = r
        return torch.where(use, out, torch.ones_like(out))

    def _update_push(self) -> None:
        """Every step: the motion still wanted, each robot's push direction and share at its current
        contact (low-passed over push_tau, held while nothing is wanted) and the pair's residual."""
        c, dt = self.cfg, self._env.step_dt
        d, e = self.errors()
        sym = self.symmetry()
        v_w, wz = self._wanted(self.goal_xy - self.box_pos()[:, :2], e, sym, self.c_rule == 4)
        self.c_vdes[:], self.c_wdes[:] = v_w, wz
        yaw = self.contact_frame_yaw()
        cs, sn = torch.cos(yaw), torch.sin(yaw)
        v_o = torch.stack([cs * v_w[:, 0] + sn * v_w[:, 1], -sn * v_w[:, 0] + cs * v_w[:, 1]], -1)
        f, r = self._split(self.c_pobj, self.c_nobj, self.c_comobj, v_o, wz, self.c_cg, self.robot_cap())
        mag = torch.linalg.norm(f, dim=-1)  # (n, 2)
        want = (torch.linalg.norm(v_w, dim=-1) > 0.02) | (wz.abs() > 0.02)
        d_new = torch.where((mag > 1e-6).unsqueeze(-1), f / mag.unsqueeze(-1).clamp(min=1e-9), -self.c_nobj)
        alpha = min(1.0, dt / max(c.push_tau, 1e-6))
        blend = self.push_dir_obj + alpha * (d_new - self.push_dir_obj)
        blend = blend / torch.linalg.norm(blend, dim=-1, keepdim=True).clamp(min=1e-6)
        self.push_dir_obj[:] = torch.where(want.view(-1, 1, 1), blend, self.push_dir_obj)
        share = mag / mag.sum(-1, keepdim=True).clamp(min=1e-9)
        self.push_share[:] = torch.where(want.unsqueeze(-1), share, self.push_share)
        self.c_resid[:] = torch.where(want, r, torch.zeros_like(r))
        self.c_res_t[:] = torch.where(self.c_resid > c.resid_bad, self.c_res_t + dt, torch.zeros_like(self.c_res_t))

    def robot_cap(self, ids=None):
        """Expert envs: the normal (pushing) force one robot can apply, as a share of the force that
        slides the object, robot_push_force / (mu m g) (None when the expert is off: rule 3 keeps its trained split)."""
        if not self.cfg.expert:
            return None
        ids = slice(None) if ids is None else ids
        cap = self.cfg.robot_push_force / (self.c_mu[ids] * self.c_mass[ids] * 9.81).clamp(min=1e-6)
        return torch.where(self.c_rule[ids] == 4, cap, torch.full_like(cap, 1e6))

    def pose_error(self) -> torch.Tensor:
        """distance + rho_g x |angle error| (m): the team's progress measure under push_cmd."""
        d, e = self.errors()
        e = torch.where(self.symmetry() > 0, e, torch.zeros_like(e))
        return d + self.c_rg * e.abs()

    def _contact_geom(self, env_ids, shape):
        """Candidate contacts of each env's object, scaled to its size (object frame)."""
        f = (self.bbox_env[env_ids, shape, 2:4] / self.c_bbox_nom[shape].clamp(min=1e-3)).clamp(0.5, 2.0)
        p = self.c_p[shape] * f.unsqueeze(1)
        nn = self.c_n[shape] / f.unsqueeze(1)
        nn = nn / torch.linalg.norm(nn, dim=-1, keepdim=True).clamp(min=1e-6)
        sep = self.c_sep_ok[shape]
        if self.cfg.footprint_sep:  # planner v2: the robots' footprints at this env's object size
            a0, a1 = AGENTS[0], AGENTS[1]
            reach = max(self.reach[a0], self.reach[a1])
            st = p + nn * (reach + 0.06)
            K = p.shape[1]
            far = torch.linalg.norm(st.unsqueeze(2) - st.unsqueeze(1), dim=-1) >= self.cfg.contact_min_sep
            eye = torch.eye(K, dtype=torch.bool, device=p.device).unsqueeze(0)
            sep = far & ~eye & footprints_clear(st, -nn, (FOOTPRINT_HALF[a0], FOOTPRINT_HALF[a1]), self.cfg.footprint_margin)
        return p, nn, self.c_pre[shape] * f.unsqueeze(1), self.c_com[shape] * f, self.c_valid[shape], sep

    def _order_mask(self, ids: torch.Tensor, p: torch.Tensor, nn: torch.Tensor) -> torch.Tensor:
        """Planner v2 (keep_order): (m, K, K) usable assignments (robot 0 -> i, robot 1 -> j) that keep
        the robots' order around the object (order_ok; bearings from the object's bounding-box centre).
        All True without keep_order."""
        m, K = p.shape[0], p.shape[1]
        if not self.cfg.keep_order:
            return torch.ones(m, K, K, dtype=torch.bool, device=p.device)
        yaw = self.contact_frame_yaw()[ids]
        cs, sn = torch.cos(yaw), torch.sin(yaw)
        ctr = self.bbox_env[ids, self.shape[ids], :2]
        obj = self.box_pos()[ids, :2]
        th = []
        for k in range(2):
            d = self.robot_xy(k)[ids] - obj
            q = torch.stack([cs * d[:, 0] + sn * d[:, 1], -sn * d[:, 0] + cs * d[:, 1]], -1) - ctr
            th.append(torch.atan2(q[:, 1], q[:, 0]))
        st = p + nn * 0.6 - ctr.unsqueeze(1)
        phi = torch.atan2(st[..., 1], st[..., 0])
        return order_ok(th[0], th[1], phi, math.radians(self.cfg.order_free_deg))

    def _pair_scores(self, p, nn, com, valid, sep, u, rule):
        """Score of every contact pair (i, j) for goal direction u (object frame) under each env's
        rule, -1e9 where the pair is not usable (returned: masked score, usable mask, each contact's
        alignment cos(push, u), and the unmasked score). Usable: standing points far enough apart,
        both pushing within 46 deg of u (else 75 deg, else any).
          spread (0)    lateral separation across u x the weaker push's alignment (a corner pushes
                        diagonally, ~0.7 of a face's push toward the goal, so two end faces beat
                        the two outermost corners when both are there)
          adjacent (1)  -(both arms across u) - 0.5 x (both pushes' misalignment): side by side
                        close to the centre line, straight pushes preferred
          random (2)    uniform"""
        m, K = p.shape[0], p.shape[1]
        lat = torch.stack([-u[:, 1], u[:, 0]], -1)
        align = -(nn * u.unsqueeze(1)).sum(-1)
        pair = lambda b: b.unsqueeze(2) & b.unsqueeze(1) & sep  # noqa: E731
        p45 = pair(valid & (align >= math.cos(math.radians(46.0))))
        p75 = pair(valid & (align >= math.cos(math.radians(75.0))))
        use = torch.where(p45.any((1, 2), keepdim=True), p45, torch.where(p75.any((1, 2), keepdim=True), p75, pair(valid)))
        pl = (p * lat.unsqueeze(1)).sum(-1)
        rl = ((p - com.unsqueeze(1)) * lat.unsqueeze(1)).sum(-1).abs()
        al = align.clamp(min=0.2)
        spread = (pl.unsqueeze(2) - pl.unsqueeze(1)).abs() * torch.minimum(al.unsqueeze(2), al.unsqueeze(1))
        adjacent = -(rl.unsqueeze(2) + rl.unsqueeze(1)) - 0.5 * ((1 - align).unsqueeze(2) + (1 - align).unsqueeze(1))
        score = torch.where((rule == 0).view(m, 1, 1), spread,
                            torch.where((rule == 1).view(m, 1, 1), adjacent, torch.rand(m, K, K, device=p.device)))
        score = score + 1e-4 * torch.rand_like(score)  # break ties at random
        return torch.where(use, score, torch.full_like(score, -1e9)), use, align, score

    def _pick_contacts(self, env_ids, shape, obj_heading, gdir, forced=None, forced_rule=None, v_obj=None, wz=None):
        """Per env: the two robots' contacts for this goal direction (object frame, scaled to the
        env's object size), their approach points and the centre of mass. The wrench rule (3)
        takes the pair with the smallest residual for the wanted motion (v_obj, wz; object frame)."""
        c, dev, m = self.cfg, self.device, len(env_ids)
        p, nn, pre, com, valid, sep = self._contact_geom(env_ids, shape)
        rel = gdir - obj_heading
        u = torch.stack([torch.cos(rel), torch.sin(rel)], -1)  # goal direction, object frame
        mix = torch.tensor(list(c.contact_mix) + [0.0] * (5 - len(c.contact_mix)), device=dev, dtype=torch.float)
        rule = torch.multinomial((mix / mix.sum()).expand(m, 5), 1).squeeze(-1)
        if forced_rule is not None:  # evaluation: this rule for every env (0 spread, 1 adjacent, 2 random, 3 wrench)
            rule = forced_rule.to(dev).long()
        cap = None
        if c.expert:  # expert envs: the centre of friction and each robot's force limit
            ex = rule == 4
            com = torch.where(ex.unsqueeze(-1), self.c_cof[env_ids], com)
            cap = torch.where(ex, c.robot_push_force / (self.c_mu[env_ids] * self.c_mass[env_ids] * 9.81).clamp(min=1e-6),
                              torch.full((m,), 1e6, device=dev))
        score, _, _, _ = self._pair_scores(p, nn, com, valid, sep, u, rule)
        w3 = (rule >= 3).nonzero().flatten()  # wrench and expert: the smallest residual
        if len(w3) and v_obj is not None:
            usable = valid[w3].unsqueeze(2) & valid[w3].unsqueeze(1) & sep[w3]
            res = self._pair_residuals(p[w3], nn[w3], com[w3], v_obj[w3], wz[w3], self.c_cg[env_ids[w3]], usable,
                                       cap=None if cap is None else cap[w3])
            score[w3] = torch.where(usable, -res + 1e-4 * torch.rand_like(res), torch.full_like(res, -1e9))
        flat = score.view(m, -1).argmax(-1)
        i, j = flat // self.c_K, flat % self.c_K
        swap = torch.rand(m, device=dev) < 0.5
        i, j = torch.where(swap, j, i), torch.where(swap, i, j)
        if forced is not None:  # evaluation: these contacts (a -1 keeps the rule's pick for that env)
            keep = forced[:, 0] >= 0
            i, j = torch.where(keep, forced[:, 0].to(dev), i), torch.where(keep, forced[:, 1].to(dev), j)
        idx = torch.stack([i, j], -1)
        ar = torch.arange(m, device=dev)
        return idx, p[ar.unsqueeze(-1), idx], nn[ar.unsqueeze(-1), idx], pre[ar.unsqueeze(-1), idx], com, rule

    def reach_limit(self, d: torch.Tensor) -> torch.Tensor:
        """Time a robot gets to reach a contact d m (straight line) from its front."""
        c = self.cfg
        return (c.reach_base_s + c.reach_detour * d / c.reach_speed).clamp(3.0, c.reach_max_s)

    def _reselect(self, ids: torch.Tensor) -> None:
        """Re-apply each env's contact rule (the wrench rule has its own re-choice)."""
        if len(ids) == 0:
            return
        r = self.c_rule[ids]
        if bool((r == 4).any()):
            self._reselect_expert(ids[r == 4])
        if bool((r == 3).any()):
            self._reselect_wrench(ids[r == 3])
        if bool((r < 3).any()):
            self._reselect_rule(ids[r < 3])

    def _reselect_wrench(self, ids: torch.Tensor) -> None:
        """Stage 4e re-choice: the pair (robot 0 -> i, robot 1 -> j) with the smallest residual for the
        motion still wanted + walk_weight x the walk of whoever moves, never a contact whose
        standing point is within partner_stand of the partner robot (unless it is the partner's
        own contact). One robot moves when that beats the current residual by resid_margin; both
        move only when the current pair cannot do the job (residual > resid_bad) and no single move
        gets under it. No goal-direction tiers: near the goal the wanted motion is mostly turning,
        so turning pairs win."""
        c, dev = self.cfg, self.device
        m = len(ids)
        ar = torch.arange(m, device=dev)
        shape = self.shape[ids]
        p, nn, pre_all, com, valid, sep = self._contact_geom(ids, shape)
        K = p.shape[1]
        yaw = self.contact_frame_yaw()[ids]
        cs, sn = torch.cos(yaw), torch.sin(yaw)
        obj = self.box_pos()[ids, :2]
        rot = lambda v: torch.stack([cs.unsqueeze(-1) * v[..., 0] - sn.unsqueeze(-1) * v[..., 1],  # noqa: E731
                                     sn.unsqueeze(-1) * v[..., 0] + cs.unsqueeze(-1) * v[..., 1]], -1)
        v_w = self.c_vdes[ids]
        v_o = torch.stack([cs * v_w[:, 0] + sn * v_w[:, 1], -sn * v_w[:, 0] + cs * v_w[:, 1]], -1)
        cur = self.c_idx[ids]
        use = valid.unsqueeze(2) & valid.unsqueeze(1) & sep & self._order_mask(ids, p, nn)
        res = self._pair_residuals(p, nn, com, v_o, self.c_wdes[ids], self.c_cg[ids], use)
        kk = torch.arange(K, device=dev).unsqueeze(0)
        pos = [self.robot_xy(k)[ids] for k in range(len(AGENTS))]
        fr = [self.front_point(a)[ids] for a in AGENTS]
        pw = obj.unsqueeze(1) + rot(p)
        bad, walk = [], []
        for k, a in enumerate(AGENTS):
            st = obj.unsqueeze(1) + rot(p + nn * (self.reach[a] + 0.06))
            bad.append((torch.linalg.norm(st - pos[1 - k].unsqueeze(1), dim=-1) < c.partner_stand) & (kk != cur[:, 1 - k : 2 - k]))
            walk.append(torch.linalg.norm(fr[k].unsqueeze(1) - pw, dim=-1) * (kk != cur[:, k : k + 1]).float())
        ok = use & ~bad[0].unsqueeze(2) & ~bad[1].unsqueeze(1)
        cost = torch.where(ok, res + c.walk_weight * (walk[0].unsqueeze(2) + walk[1].unsqueeze(1)), torch.full_like(res, 1e9))
        cur_res = res[ar, cur[:, 0], cur[:, 1]]
        row, j_r = cost[ar, cur[:, 0], :].min(-1)  # robot 0 keeps its contact, robot 1 moves
        col, i_c = cost[ar, :, cur[:, 1]].min(-1)  # robot 1 keeps, robot 0 moves
        single = torch.minimum(row, col)
        glob, flat = cost.view(m, -1).min(-1)
        gi, gj = flat // K, flat % K
        one = single < cur_res - c.resid_margin
        both = ~one & (cur_res > c.resid_bad) & ~(single < c.resid_bad) & (glob < cur_res - c.resid_margin)
        new = cur.clone()
        tr = one & (row <= col)
        new[:, 1] = torch.where(tr, j_r, new[:, 1])
        new[:, 0] = torch.where(one & ~tr, i_c, new[:, 0])
        new[:, 0] = torch.where(both, gi, new[:, 0])
        new[:, 1] = torch.where(both, gj, new[:, 1])
        chg = new != cur
        for k in range(2):
            sel = chg[:, k]
            if not bool(sel.any()):
                continue
            e = ids[sel]
            nk = new[sel, k]
            pk, nnk = p[ar[sel], nk], nn[ar[sel], nk]
            self.c_idx[e, k] = nk
            self.c_pobj[e, k] = pk
            self.c_nobj[e, k] = nnk
            self.c_preobj[e, k] = pre_all[ar[sel], nk]
            self.push_dir_obj[e, k] = -nnk
            self.c_engaged[e, k] = False
            self.c_drift_t[e, k] = 0.0
            self.c_free_t[e, k] = 0.0
            d = torch.linalg.norm(fr[k][sel] - pw[ar[sel], nk], dim=-1)
            self.c_reach_lim[e, k] = self.reach_limit(d)
            self.c_switches[e] += 1

    def _resid_sample(self) -> torch.Tensor:
        """(n, 2, RESID_HF): per robot, [own force along its push / 200 N, partner's / 200 N, object speed along
        the wanted motion / 0.5 m/s, own on-contact]."""
        fa = torch.stack([(object_force_from(self._env, AGENTS[k]) * self.push_dir_world(k)).sum(-1) for k in range(2)], -1)
        vd = self.c_vdes
        u = vd / torch.linalg.norm(vd, dim=-1, keepdim=True).clamp(min=1e-6)
        sp = (self.box_vel()[:, :2] * u).sum(-1) * (torch.linalg.norm(vd, dim=-1) > 1e-3).float()
        on = torch.stack([self.on_contact(k).float() for k in range(2)], -1)
        out = []
        for k in range(2):
            out.append(torch.stack([fa[:, k] / 200.0, fa[:, 1 - k] / 200.0, sp / 0.5, on[:, k]], -1))
        return torch.stack(out, 1)

    def _update_resid_hist(self, dt: float) -> None:
        """Every 0.1 s, push the newest sample (residual-pilot inputs)."""
        self.c_rhist_t += dt
        due = self.c_rhist_t >= 0.1 - 1e-6
        if bool(due.any()):
            new = self._resid_sample()
            shifted = torch.cat([new.unsqueeze(2), self.c_rhist[:, :, :-1]], 2)
            self.c_rhist[:] = torch.where(due[:, None, None, None], shifted, self.c_rhist)
            self.c_rhist_t[:] = torch.where(due, torch.zeros_like(self.c_rhist_t), self.c_rhist_t)

    def _propose_expert(self, ids: torch.Tensor) -> dict:
        """Expert planner v2 (rule 4): the contact pair AND which robot takes each, together, at the
        lowest cost J = residual + time_weight x (slower robot's arrival, s) + stop_weight x (robots
        that stop pushing to move); arrival = route length around the object / walk_speed. Hand-
        overs are just other assignments. The current choice is priced at its observed result:
        + stall_penalty when the object made no progress in the last window although the pair is strong
        enough to slide it there (a pair at its force limit is not penalised for being slow; when no
        pair can slide the object, c_need_more is set). A robot may not go back
        to a contact it left less than relock_s ago (no flip-flopping). Switch only when the best
        option beats the current one by expert_margin; within finish_dist of the goal only when the current
        pair cannot make the motion left (residual > finish_resid).

        Pure: computes the expert's choice and returns it without changing any state, so it can label
        decisions taken by another coordinator. Returns new (m, 2) contact ids, cur (m, 2), the candidate
        geometry p / nn / pre (m, K, 2), use (m, K, K) = the geometric validity of each ordered pair, t_route
        (2 x (m, K)) = each robot's route time to each contact (0 for its own contact while on it), need_more
        (m,) = no usable pair can slide the object."""
        c, dev = self.cfg, self.device
        m = len(ids)
        ar = torch.arange(m, device=dev)
        shape = self.shape[ids]
        p, nn, pre_all, com, valid, sep = self._contact_geom(ids, shape)
        K = p.shape[1]
        yaw = self.contact_frame_yaw()[ids]
        cs, sn = torch.cos(yaw), torch.sin(yaw)
        v_w = self.c_vdes[ids]
        v_o = torch.stack([cs * v_w[:, 0] + sn * v_w[:, 1], -sn * v_w[:, 0] + cs * v_w[:, 1]], -1)
        cur = self.c_idx[ids]
        use = valid.unsqueeze(2) & valid.unsqueeze(1) & sep & self._order_mask(ids, p, nn)
        com = self.c_cof[ids]  # friction acts about the centre of friction
        res = self._pair_residuals(p, nn, com, v_o, self.c_wdes[ids], self.c_cg[ids], use, cap=self.robot_cap(ids))
        kk = torch.arange(K, device=dev).unsqueeze(0)
        t_arr, stop, t_route, ons = [], [], [], []
        for k in range(2):
            on = (self.c_engaged[ids, k] & self.on_contact(k)[ids])
            ons.append(on)
            rl = torch.stack([self.guide(k, ids=ids, target=(p[:, x], nn[:, x], pre_all[:, x]))[1] for x in range(K)], 1)
            t = rl / c.walk_speed
            same = kk == cur[:, k : k + 1]
            t = torch.where(same & on.unsqueeze(-1), torch.zeros_like(t), t)
            t_route.append(t)
            relock = (kk == self.c_left_idx[ids, k : k + 1]) & ((self.c_time[ids] - self.c_left_t[ids, k]) < c.relock_s).unsqueeze(-1)
            t = torch.where(relock & ~same, torch.full_like(t, 1e6), t)
            t_arr.append(t)
            stop.append((~same & on.unsqueeze(-1)).float())
        J = res + c.time_weight * torch.maximum(t_arr[0].unsqueeze(2), t_arr[1].unsqueeze(1)) + \
            c.stop_weight * (stop[0].unsqueeze(2) + stop[1].unsqueeze(1))
        J = torch.where(use, J, torch.full_like(J, 1e9))
        cur_ok = use[ar, cur[:, 0], cur[:, 1]]
        j_cur = torch.where(cur_ok, J[ar, cur[:, 0], cur[:, 1]], torch.full_like(res[:, 0, 0], 1e9))
        j_cur = j_cur + c.stall_penalty * self.c_stalled[ids].float()
        # no usable pair can slide the object (every residual 1): more robots (or more force) needed
        need_more = torch.where(use, res, torch.ones_like(res)).view(m, -1).min(-1).values >= 1.0 - 1e-6
        best, flat = J.view(m, -1).min(-1)
        gi, gj = flat // K, flat % K
        go = best < j_cur - c.expert_margin
        zone = torch.zeros_like(go)
        if c.finish_dist > 0:
            # finishing zone: keep the pair unless it cannot make the motion left (residual > finish_resid)
            res_cur = torch.where(cur_ok, res[ar, cur[:, 0], cur[:, 1]], torch.ones_like(j_cur))
            zone = self.pose_error()[ids] < c.finish_dist
            go = go & (~zone | (res_cur > c.finish_resid))
        new = cur.clone()
        new[:, 0] = torch.where(go, gi, new[:, 0])
        new[:, 1] = torch.where(go, gj, new[:, 1])
        # the remaining entries are the expert's intermediate quantities, exposed as coordinator features only
        return dict(new=new, cur=cur, p=p, nn=nn, pre=pre_all, use=use, t_route=t_route, need_more=need_more,
                    res=res, J=J, t_arr=t_arr, stop=stop, on=torch.stack(ons, -1), j_cur=j_cur, zone=zone)

    def apply_assignment(self, ids: torch.Tensor, new: torch.Tensor, p: torch.Tensor, nn: torch.Tensor,
                         pre: torch.Tensor, t_route: list) -> torch.Tensor:
        """Apply a decided assignment (expert or learned coordinator) to envs ids: new (m, 2) contact ids into
        the candidate geometry p / nn / pre (m, K, 2). A robot whose contact changes gets the new contact's
        geometry and push direction, loses its engagement (it must reach the new contact), restarts its drift /
        free timers, gets a reach limit of 1.5 x its route time + 2 s (the slow-arrival trigger) and records the
        contact it left (relock); each change counts one switch. Every decision (also a keep) clears the
        stalled / weak / finish flags that triggered it. Returns chg (m, 2)."""
        m = len(ids)
        ar = torch.arange(m, device=self.device)
        cur = self.c_idx[ids]
        chg = new != cur
        for k in range(2):
            sel = chg[:, k]
            if not bool(sel.any()):
                continue
            e = ids[sel]
            nk = new[sel, k]
            self.c_left_idx[e, k] = cur[sel, k]
            self.c_left_t[e, k] = self.c_time[e]
            self.c_idx[e, k] = nk
            self.c_pobj[e, k] = p[ar[sel], nk]
            self.c_nobj[e, k] = nn[ar[sel], nk]
            self.c_preobj[e, k] = pre[ar[sel], nk]
            self.push_dir_obj[e, k] = -nn[ar[sel], nk]
            self.c_engaged[e, k] = False
            self.c_drift_t[e, k] = 0.0
            self.c_free_t[e, k] = 0.0
            self.c_reach_lim[e, k] = 1.5 * t_route[k][ar[sel], nk] + 2.0  # slow-arrival trigger
            self.c_switches[e] += 1
        self.c_stalled[ids] = False
        self.c_weak[ids] = False
        self.c_fin[ids] = False
        return chg

    def _reselect_expert(self, ids: torch.Tensor) -> None:
        """The expert planner's decision (_propose_expert), applied (apply_assignment)."""
        prop = self._propose_expert(ids)
        self.c_need_more[ids] = prop["need_more"]
        self.apply_assignment(ids, prop["new"], prop["p"], prop["nn"], prop["pre"], prop["t_route"])

    def _update_expert(self, dt: float | None = None) -> None:
        """At 1 / expert_dt: priorities, expected arrivals, the no-progress window and the go / hold
        decision (computed for every env; a test rig or Phase 2's executor obeys it). dt: time
        since the last update."""
        c = self.cfg
        dt = self._env.step_dt if dt is None else dt
        on = torch.stack([self.c_engaged[:, k] & self.on_contact(k) for k in range(2)], -1)
        route = torch.stack([self.guide(k)[1] for k in range(2)], -1)
        self.c_arrive[:] = torch.where(on, torch.zeros_like(route), route / c.walk_speed)
        # priority: a robot already on its contact first, then the one that arrives sooner; ties -> robot 1
        self.c_prio[:] = 2.0 * on.float() + 1.0 / (1.0 + self.c_arrive) + torch.tensor([1e-3, 0.0], device=self.device)
        # no progress: the object moved < stall_move m and turned < stall_turn rad over stall_window s
        # while a robot was on its contact and the goal was not reached
        self.c_win_t += dt
        full = self.c_win_t >= c.stall_window
        d, e = self.errors()
        e = torch.where(self.symmetry() > 0, e, torch.zeros_like(e))
        moved = torch.linalg.norm(self.box_pos()[:, :2] - self.c_win_xy, dim=-1)
        turned = wrap(self.heading() - self.c_win_yaw).abs()
        done = (d < 0.1) & (e.abs() < math.radians(6.0))
        # only time spent pushing counts: a robot holding for its partner is waiting, not stalled
        pushing = (on & (self.c_phase == 2)).any(-1)
        pe = self.pose_error()
        # finishing zone (pose error < finish_dist): the motion left is small, so progress is judged
        # against it (no progress = the pose error fell by less than finish_frac of itself over the
        # window), and a stall there never counts against the place: fine positioning is slow, and
        # walking to another pair this close to the goal costs more than it gains
        zone = (pe < c.finish_dist) & (self.c_rule == 4)
        stuck_far = (moved < c.stall_move) & (turned < c.stall_turn)
        stuck_fin = (self.c_win_pe - pe) < c.finish_frac * self.c_win_pe.clamp(max=c.finish_dist)
        stalled = full & torch.where(zone, stuck_fin, stuck_far) & pushing & ~done & (self.c_rule == 4)
        fin = stalled & zone
        self.c_fin_stalls += fin.float()
        self.c_fin |= fin
        stalled = stalled & ~zone
        if bool(stalled.any()):
            # a stall counts against the place only if the force model says the pair should slide the object
            # there (strength >= strength_margin); a pair at its force limit is expected to be slow: re-plan
            # (a stronger pair may exist) without the penalty, so the planner keeps pushing at a good place
            sid = stalled.nonzero().flatten()
            st = self.current_strength(sid)
            self.c_strength[sid] = st.clamp(max=1e6)
            strong = st >= c.strength_margin
            self.c_stalled[sid[strong]] = True
            self.c_weak[sid[~strong]] = True
        self.c_need_more_t += dt * (self.c_need_more & (self.c_rule == 4)).float()
        restart = full | ~pushing
        self.c_win_t = torch.where(restart, torch.zeros_like(self.c_win_t), self.c_win_t)
        self.c_win_xy[:] = torch.where(restart.unsqueeze(-1), self.box_pos()[:, :2], self.c_win_xy)
        self.c_win_yaw[:] = torch.where(restart, self.heading(), self.c_win_yaw)
        self.c_win_pe[:] = torch.where(restart, pe, self.c_win_pe)
        # go / hold: a robot on its contact pushes when its partner is on too; alone only if it can make
        # the wanted motion by itself (solo residual < resid_bad), the partner is > solo_wait_s away and
        # the object is light enough for one robot (mass x friction x g < robot_push_force)
        heavy = self.c_mass * self.c_mu * 9.81 > c.robot_push_force
        yaw = self.contact_frame_yaw()
        cs, sn = torch.cos(yaw), torch.sin(yaw)
        v_w = self.c_vdes
        v_o = torch.stack([cs * v_w[:, 0] + sn * v_w[:, 1], -sn * v_w[:, 0] + cs * v_w[:, 1]], -1)
        for k in range(2):
            pk = self.c_pobj[:, k : k + 1].expand(-1, 2, -1)
            nk = self.c_nobj[:, k : k + 1].expand(-1, 2, -1)
            _, solo = self._split(pk, nk, self.c_comobj, v_o, self.c_wdes, self.c_cg, 0.5 * self.robot_cap())
            alone = (solo < c.resid_bad) & (self.c_arrive[:, 1 - k] > c.solo_wait_s) & ~heavy
            ph = torch.where(on[:, 1 - k] | alone, torch.full_like(self.c_phase[:, k], 2), torch.ones_like(self.c_phase[:, k]))
            self.c_phase[:, k] = torch.where(on[:, k], ph, torch.zeros_like(ph))

    def _reselect_rule(self, ids: torch.Tensor) -> None:
        """Re-apply each env's rule from the object's current pose and goal. A pair changes when the
        current one is no longer usable (a contact no longer pushes toward the goal) or, for the
        spread / adjacent rules, when the best pair scores reselect_margin better. One robot moves
        whenever possible (the partner keeps its contact and keeps pushing); both move only when the
        current pair no longer pushes toward the goal and no single move fixes it. A robot that
        changes must reach its new contact within reach_limit (the drift rule waits until then)."""
        c, dev = self.cfg, self.device
        m = len(ids)
        if m == 0:
            return
        ar = torch.arange(m, device=dev)
        shape = self.shape[ids]
        p, nn, pre_all, com, valid, sep = self._contact_geom(ids, shape)
        yaw = self.contact_frame_yaw()[ids]
        obj = self.box_pos()[ids, :2]
        tg = self.goal_xy[ids] - obj
        rel = torch.atan2(tg[:, 1], tg[:, 0]) - yaw
        u = torch.stack([torch.cos(rel), torch.sin(rel)], -1)
        rule = self.c_rule[ids]
        sep = sep & self._order_mask(ids, p, nn)  # (directed with keep_order: [robot 0's, robot 1's])
        score, use, align, raw = self._pair_scores(p, nn, com, valid, sep, u, rule)
        cur = self.c_idx[ids]
        # the current pair stays usable while both its contacts still push within 75 deg of the goal
        # (a better tier of contacts appearing is not a reason to move; a clearly better score is)
        lim = math.cos(math.radians(75.0))
        cur_ok = (align[ar, cur[:, 0]] >= lim) & (align[ar, cur[:, 1]] >= lim) & sep[ar, cur[:, 0], cur[:, 1]]
        cur_score = raw[ar, cur[:, 0], cur[:, 1]]
        best_score, flat = score.view(m, -1).max(-1)
        bi, bj = flat // self.c_K, flat % self.c_K
        change = ((~cur_ok) | ((rule != 2) & (best_score > cur_score + c.reselect_margin))) & (best_score > -1e8)
        if not bool(change.any()):
            return
        new = cur.clone()
        chg = torch.zeros(m, 2, dtype=torch.bool, device=dev)
        # one of the current contacts is in the best pair: only the other robot moves
        if c.keep_order:  # v2: the best pair is ordered (robot 0 -> bi, robot 1 -> bj); keep each robot's slot
            k0_in, k1_in = cur[:, 0] == bi, cur[:, 1] == bj
        else:
            k0_in = (cur[:, 0] == bi) | (cur[:, 0] == bj)
            k1_in = (cur[:, 1] == bi) | (cur[:, 1] == bj)
        other_of = lambda x: torch.where(x == bi, bj, bi)  # noqa: E731
        a = change & k0_in & ~k1_in
        new[:, 1] = torch.where(a, other_of(cur[:, 0]), new[:, 1])
        chg[:, 1] |= a
        b = change & k1_in & ~k0_in
        new[:, 0] = torch.where(b, other_of(cur[:, 1]), new[:, 0])
        chg[:, 0] |= b
        # neither: the robot whose contact pushes least toward the goal moves, the partner stays
        cc = change & ~k0_in & ~k1_in
        al_cur = torch.stack([align[ar, cur[:, 0]], align[ar, cur[:, 1]]], -1)
        worst = (al_cur[:, 1] < al_cur[:, 0]).long()  # 0 or 1
        keep = 1 - worst
        keep_idx = cur[ar, keep]
        # pairs (x, partner's contact): any x pushing within 75 deg that stands far enough from the partner
        # (looser than the tiers above, so the partner keeps a contact that still pushes usefully)
        # (robot 0 moving: pair (x, keep); robot 1 moving: pair (keep, x))
        ok_x = valid & (align >= lim) & torch.where((worst == 0).unsqueeze(-1), sep[ar, :, keep_idx], sep[ar, keep_idx, :])
        ok_x &= torch.arange(self.c_K, device=dev).unsqueeze(0) != keep_idx.unsqueeze(-1)
        ok_x &= (align[ar, keep_idx] >= lim).unsqueeze(-1)
        row = torch.where(ok_x, raw[ar, :, keep_idx], torch.full_like(raw[:, :, 0], -1e9))
        rbest, rarg = row.max(-1)
        # (a usable current pair only changes for a clear gain, as above)
        single = cc & (rbest > -1e8) & (rbest > cur_score + 1e-6) & ((~cur_ok) | (rbest > cur_score + c.reselect_margin))
        for k in range(2):
            sel = single & (worst == k)
            new[:, k] = torch.where(sel, rarg, new[:, k])
            chg[:, k] |= sel
        # no single move works: both move to the best pair (only when the current pair no longer pushes
        # toward the goal; a usable pair is not given up for a better score that needs both to move)
        both = cc & ~single & ~cur_ok
        if bool(both.any()):
            cs, sn = torch.cos(yaw), torch.sin(yaw)
            to_w = lambda v: obj + torch.stack([cs * v[:, 0] - sn * v[:, 1], sn * v[:, 0] + cs * v[:, 1]], -1)  # noqa: E731
            pi, pj = to_w(p[ar, bi]), to_w(p[ar, bj])
            f0, f1 = self.front_point(AGENTS[0])[ids], self.front_point(AGENTS[1])[ids]
            keep_d = torch.linalg.norm(f0 - pi, dim=-1) + torch.linalg.norm(f1 - pj, dim=-1)
            swap_d = torch.linalg.norm(f0 - pj, dim=-1) + torch.linalg.norm(f1 - pi, dim=-1)
            sw = (swap_d < keep_d) & ~torch.tensor(c.keep_order, device=dev)  # v2: (bi, bj) is already in order
            new[:, 0] = torch.where(both, torch.where(sw, bj, bi), new[:, 0])
            new[:, 1] = torch.where(both, torch.where(sw, bi, bj), new[:, 1])
            chg |= both.unsqueeze(-1) & (new != cur)
        chg &= new != cur
        if not bool(chg.any()):
            return
        cs, sn = torch.cos(yaw), torch.sin(yaw)
        for k in range(2):
            sel = chg[:, k]
            if not bool(sel.any()):
                continue
            e = ids[sel]
            nk = new[sel, k]
            pk, nnk = p[ar[sel], nk], nn[ar[sel], nk]
            self.c_idx[e, k] = nk
            self.c_pobj[e, k] = pk
            self.c_nobj[e, k] = nnk
            self.c_preobj[e, k] = pre_all[ar[sel], nk]
            self.c_engaged[e, k] = False
            self.c_drift_t[e, k] = 0.0
            self.c_free_t[e, k] = 0.0
            pw = obj[sel] + torch.stack([cs[sel] * pk[:, 0] - sn[sel] * pk[:, 1], sn[sel] * pk[:, 0] + cs[sel] * pk[:, 1]], -1)
            d = torch.linalg.norm(self.front_point(AGENTS[k])[e] - pw, dim=-1)
            self.c_reach_lim[e, k] = self.reach_limit(d)
            self.c_switches[e] += 1

    def _update_metrics(self) -> None:
        super()._update_metrics()
        if self.tol_table is not None and self.cfg.success_mode == "terminate":
            c = self.cfg
            d, e = self.errors()
            still = (torch.linalg.norm(self.box_vel()[:, :2], dim=-1) < c.success_max_speed) & \
                    (self.box_ang_vel()[:, 2].abs() < c.success_max_yaw_rate)
            self.success_flag[:] = (d < self.tol_pos) & (e.abs() < self.tol_yaw) & still
            self.metrics["success"][:] = self.success_flag.float()
        # turn practice: turn-in-place success rate = turn_success / turn_task (episode means)
        self.metrics["turn_task"][:] = self.turn_episode.float()
        self.metrics["turn_success"][:] = ((self.metrics["success"] > 0.5) & self.turn_episode).float()

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
        if self.cfg.contact_mode:
            dt = self._env.step_dt
            self.c_time += dt
            if self.cfg.disturb_frac > 0:
                self._disturb()
            if self.cfg.wrench:
                self._update_push()
            if self.cfg.expert:  # at 1 / expert_dt (its route and split work is heavier than a step needs)
                self.c_exp_t += dt
                if self.c_exp_t >= self.cfg.expert_dt - 1e-6:
                    self._update_expert(self.c_exp_t)
                    self.c_exp_t = 0.0
            for k in range(len(AGENTS)):
                near = self.on_contact(k)
                arrived = near & ~self.c_engaged[:, k] & (self.c_free_t[:, k] > 0.5)  # walked to it (not started on it)
                if bool(arrived.any()):
                    self.c_reach_sum += float(self.c_free_t[arrived, k].sum())
                    self.c_reach_cnt += int(arrived.sum())
                self.c_engaged[:, k] |= near
                self.c_drift_t[:, k] = torch.where(self.c_engaged[:, k] & ~near, self.c_drift_t[:, k] + dt,
                                                   torch.zeros_like(self.c_drift_t[:, k]))
                self.c_free_t[:, k] = torch.where(self.c_engaged[:, k], self.c_free_t[:, k], self.c_free_t[:, k] + dt)
            if self.cfg.exec_v2:
                self._update_exec(dt)
            lo, hi = self.cfg.reselect_s
            once = hi <= 0 and self.cfg.expert_first_only  # only the expert's start-up re-plan (timer set to 0.1 s at reset)
            if hi > 0 or once:
                self.c_reselect_t -= dt
                due = self.c_reselect_t <= 0.0
                why = torch.where(due, 1, 0)  # the first cause that applies, in this order (logging only)
                if once:
                    pass
                elif self.cfg.wrench:  # the wrench rule also re-chooses when its pair cannot do the job
                    rd = (self.c_rule >= 3) & (self.c_res_t >= self.cfg.resid_dwell_s)
                    why = torch.where((why == 0) & rd, 2, why)
                    due |= rd
                if self.cfg.expert and not once:  # expert: also when nothing moves, or a robot is late reaching its contact
                    slow = (~self.c_engaged & (self.c_free_t >= self.c_reach_lim)).any(-1) & (self.c_rule == 4)
                    if self.cfg.slow_min_s > 0:
                        self.c_slow_wait -= dt
                        slow &= self.c_slow_wait <= 0.0
                    self.c_replans += (self.c_stalled & ~due).float()
                    self.c_replan_weak += (self.c_weak & ~due & ~self.c_stalled).float()
                    self.c_replan_slow += (slow & ~due & ~self.c_stalled & ~self.c_weak & ~self.c_fin).float()
                    for code, m_ in ((3, self.c_stalled), (4, self.c_weak), (5, self.c_fin), (6, slow)):
                        why = torch.where((why == 0) & m_, code, why)
                    due |= self.c_stalled | self.c_weak | self.c_fin | slow
                if bool(due.any()):
                    ids = due.nonzero().flatten()
                    nd = len(ids)
                    self.c_reselect_t[ids] = 1e9 if once else lo + (hi - lo) * torch.rand(nd, device=self.device)
                    self.c_res_t[ids] = 0.0
                    if self.cfg.expert and not once and self.cfg.slow_min_s > 0:  # this decision answered the slow question
                        self.c_slow_wait[ids] = torch.where(slow[ids], torch.full_like(self.c_slow_wait[ids], self.cfg.slow_min_s),
                                                            self.c_slow_wait[ids])
                    settled = self.c_engaged[ids].all(-1)  # nobody still on the way to a new contact
                    if self.cfg.wrench:  # wrench rule: a robot stuck on its way past its reach limit does not block it
                        stuck = (~self.c_engaged[ids] & (self.c_free_t[ids] >= self.c_reach_lim[ids])).any(-1)
                        settled |= stuck & (self.c_rule[ids] >= 3)
                    if self.cfg.expert:  # the expert prices walking itself: it may re-plan while robots walk
                        settled |= self.c_rule[ids] == 4
                    # close to the goal the direction to it is noise: keep the contacts there
                    far = torch.linalg.norm(self.goal_xy[ids] - self.box_pos()[ids, :2], dim=-1) > self.cfg.reselect_min_dist
                    run = ids[settled & far]
                    self.c_plan_reason[run] = why[run]
                    self.c_plan_n[run] += 1.0
                    if self.coordinator is not None and len(run):
                        ex = self.c_rule[run] == 4
                        self.coordinator(self, run[ex])
                        self._reselect(run[~ex])
                    else:
                        self._reselect(run)
            if self.cfg.resid:
                self._update_resid_hist(dt)
            # the approach potential's baseline for the next step (after resets and re-selections, so
            # a new contact or a new episode never pays for the jump)
            for k in range(len(AGENTS)):
                self.c_prev_phi[:, k] = self.contact_phi(k)
            if self.cfg.push_cmd:
                self.c_prev_pose[:] = self.pose_error()

    def _update_exec(self, dt: float) -> None:
        """Phase 2 executor commands, every step.
        On = engaged on its contact (reached since the contact was assigned) and off it for less than
        flicker_s: a robot pushing at the edge of the drift radius drifts in and out, and that must not
        change its command. Ready = on for ready_steady_s outside a random hold; team ready = every robot
        of the push group ready. Once the group pushes the command is latched (c_go): push until a robot
        is no longer on or its contact changes. Before that: the expert's go / hold (rule 4) or, for the
        other rules, hold until the team is ready. On hold_rand of its real arrivals (engaged for the
        first time on this contact) a robot holds hold_rand_s whatever its partner does; it is not ready
        meanwhile, so a barrier partner waits for it."""
        c = self.cfg
        on = self.c_engaged & (self.c_drift_t < c.flicker_s)
        grp = self.c_in_group
        if c.hold_rand > 0:
            arrive = self.c_engaged & (~self.c_was_eng | (self.c_idx != self.c_was_idx))  # reached a (new) contact
            lo, hi = c.hold_rand_s
            draw = arrive & (torch.rand_like(self.c_rhold) < c.hold_rand)
            self.c_rhold[:] = torch.where(draw, lo + (hi - lo) * torch.rand_like(self.c_rhold), self.c_rhold)
        self.c_was_eng[:] = self.c_engaged
        self.c_was_idx[:] = self.c_idx
        held = on & (self.c_rhold > 0)
        self.c_ready_t[:] = torch.where(on & ~held, self.c_ready_t + dt, torch.zeros_like(self.c_ready_t))
        self.c_ready[:] = self.c_ready_t >= c.ready_steady_s - 1e-6
        self.c_team_ready[:] = (self.c_ready | ~grp).all(-1) & grp.any(-1)
        all_on = (on | ~grp).all(-1)
        start = self.c_team_ready
        if c.expert:  # expert envs: the group pushes once the planner tells every robot of it to push
            r4 = self.c_rule == 4
            start = torch.where(r4, ((self.c_phase == 2) | ~grp).all(-1) & all_on & ~held.any(-1), start)
        self.c_go[:] = (self.c_go | start) & all_on
        ph = torch.where(self.c_go.unsqueeze(-1), torch.full_like(self.c_cmd, 2), torch.ones_like(self.c_cmd))
        if c.expert:  # before the group pushes the planner decides (it may send one robot alone)
            ph = torch.where((r4 & ~self.c_go).unsqueeze(-1), self.c_phase.long(), ph)
        ph = torch.where(on, ph.clamp(min=1), torch.zeros_like(ph))
        ph = torch.where(held, torch.ones_like(ph), ph)
        if c.exec_cmd_mode == "always_push":  # ablation: Stage 4e's behaviour, a robot on its contact pushes
            ph = torch.where(on, torch.full_like(ph, 2), torch.zeros_like(ph))
            self.c_team_ready[:] = all_on
            self.c_go[:] = all_on
        self.c_rhold[:] = (self.c_rhold - dt).clamp(min=0.0)
        self.c_cmd_flips += ((self.c_cmd == 2) & (ph == 1)).any(-1).float()
        self.c_cmd[:] = ph

    def _disturb(self) -> None:
        """Scripted object motion (training): inside its window, an episode's object is given a set
        planar velocity and turn rate every step (height, tilt and their rates kept)."""
        act = (self.c_time >= self.d_t0) & (self.c_time < self.d_t1)
        if not bool(act.any()):
            return
        for k, o in enumerate(self.objs):
            e = (act & (self.shape == k)).nonzero().flatten()
            if len(e) == 0:
                continue
            v = torch.cat([o.data.root_link_lin_vel_w[e], o.data.root_link_ang_vel_w[e]], -1).clone()
            v[:, 0], v[:, 1], v[:, 5] = self.d_vel[e, 0], self.d_vel[e, 1], self.d_vel[e, 2]
            o.write_root_link_velocity_to_sim(v, e)

    # -- placement --------------------------------------------------------------------------------
    def _resample_command(self, env_ids: torch.Tensor) -> None:
        c, dev = self.cfg, self.device
        m = len(env_ids)
        if m == 0:
            return
        self.metrics["success"][env_ids] = 0.0
        self.in_goal_time[env_ids] = 0.0
        self.success_flag[env_ids] = False
        if self.tol_table is not None:
            self.env_tol_level[env_ids] = self.tol_level
            self.tol_pos[env_ids] = self.tol_table[self.tol_level, 0]
            self.tol_yaw[env_ids] = torch.deg2rad(self.tol_table[self.tol_level, 1])
        lvl = torch.full((m,), self.level, dtype=torch.long, device=dev)
        replay = torch.rand(m, device=dev) < c.replay_frac
        lvl = torch.where(replay, torch.randint(0, self.level + 1, (m,), device=dev), lvl)
        self.env_level[env_ids] = lvl
        t = self.table[lvl]

        # shape: trainable shapes whose mass is inside the level's window, weighted by how badly
        # each is going (Stage 2); none inside -> the trainable one closest to the window
        masses = torch.stack([self._env.sim.model.body_mass[env_ids, o.indexing.body_ids[0]] for o in self.objs], -1)
        lo, hi = t[:, MASS_LO].unsqueeze(-1), t[:, MASS_HI].unsqueeze(-1)
        if c.train_mass:  # fixed mass window (kg) instead of the level's
            lo, hi = torch.full_like(lo, float(c.train_mass[0])), torch.full_like(hi, float(c.train_mass[1]))
        ok = (masses >= lo) & (masses <= hi) & self.train_mask.unsqueeze(0)
        if c.only is not None:
            ok &= torch.tensor([nm == c.only for nm in OBJ_NAMES2], device=dev).unsqueeze(0)
        fallback = self.train_mask.unsqueeze(0) if c.only is None else \
            torch.tensor([nm == c.only for nm in OBJ_NAMES2], device=dev).unsqueeze(0)
        gumbel = -torch.log(-torch.log(torch.rand_like(masses).clamp(1e-9, 1 - 1e-9)))
        gap_to_window = torch.relu(lo - masses) + torch.relu(masses - hi)
        sw = self.shape_weight
        if c.shape_bias:
            bias = dict(c.shape_bias)
            sw = sw * torch.tensor([float(bias.get(nm[len("obj_"):], 1.0)) for nm in OBJ_NAMES2], device=dev)
            ok = ok & (sw > 0).unsqueeze(0)
        score = torch.where(ok, torch.log(sw.clamp(min=1e-12)).unsqueeze(0) + gumbel,
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
        m_sel = masses.gather(1, shape.unsqueeze(-1)).squeeze(-1)
        b_ = (torch.bucketize(m_sel, self.reset_mass_edges, right=True) - 1).clamp(0, self.reset_counts.shape[1] - 1)
        self.reset_counts.index_put_((shape, b_), torch.ones_like(m_sel), accumulate=True)
        if c.train_mass and c.only is None and (sc is None or "shape" not in sc):  # training draw: in the window
            bad = (m_sel < c.train_mass[0] - 1e-3) | (m_sel > c.train_mass[1] + 1e-3) | ~self.train_mask[shape]
            if bool(bad.any()):
                raise RuntimeError(f"train_mass {c.train_mass} / train_shapes: drew shape "
                                   f"{SHAPES2[int(shape[bad][0])].name} at {float(m_sel[bad][0]):.1f} kg")

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
        tt = torch.zeros(m, dtype=torch.bool, device=dev)
        if c.turn_frac > 0 and sc is None:  # turn practice (training only): a turn in place
            tt = (torch.rand(m, device=dev) < c.turn_frac) & (self.sym[shape] > 0)
            td = U(c.turn_dist[0], c.turn_dist[1])
            near = obj_xy + td.unsqueeze(-1) * torch.stack([torch.cos(gdir), torch.sin(gdir)], -1)
            goal_xy = torch.where(tt.unsqueeze(-1), near, goal_xy)
            tmag = torch.minimum(torch.deg2rad(U(c.turn_deg[0], c.turn_deg[1])), cap)
            sgn = torch.where(torch.rand(m, device=dev) < 0.5, -torch.ones_like(tmag), torch.ones_like(tmag))
            goal_yaw = torch.where(tt, wrap(obj_heading + sgn * tmag), goal_yaw)
        self.turn_episode[env_ids] = tt
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
        cpose = None
        self.resid_base_last[env_ids] = 0.0  # residual: the base's action history restarts with the episode (any planner)
        if c.contact_mode:
            forced = sc.get("contact_idx") if sc is not None else None
            forced_rule = sc.get("contact_rule") if sc is not None else None
            gdir_now = torch.atan2((goal_xy - obj_xy)[:, 1], (goal_xy - obj_xy)[:, 0])
            v_o = wz = None
            e0 = fold(wrap(goal_yaw - obj_heading), self.sym[shape])
            if c.expert or c.effort:  # (before the pick: the expert's split and the push targets know the mass)
                body = torch.tensor([o.indexing.body_ids[0] for o in self.objs], device=dev)[shape]
                self.c_mass[env_ids] = self._env.sim.model.body_mass[env_ids, body]
            if c.wrench:
                self._set_radii(env_ids)
                ep = goal_xy - obj_xy
                ch0, sh0 = torch.cos(obj_heading), torch.sin(obj_heading)
                ep_o = torch.stack([ch0 * ep[:, 0] + sh0 * ep[:, 1], -sh0 * ep[:, 0] + ch0 * ep[:, 1]], -1)
                v_o, wz = self._wanted(ep_o, e0, self.sym[shape], None if forced_rule is None else forced_rule.to(dev) == 4)
            idx, cp, cn, cpre, ccom, rule = self._pick_contacts(env_ids, shape, obj_heading, gdir_now, forced, forced_rule,
                                                                v_o, wz)
            self.c_idx[env_ids], self.c_pobj[env_ids], self.c_nobj[env_ids] = idx, cp, cn
            self.push_dir_obj[env_ids] = -cn
            self.push_share[env_ids] = 0.5
            if c.exec_v2:
                self.c_cmd[env_ids] = 0
                self.c_ready_t[env_ids] = 0.0
                self.c_ready[env_ids] = False
                self.c_team_ready[env_ids] = False
                self.c_rhold[env_ids] = 0.0
                self.c_was_eng[env_ids] = False
                self.c_was_idx[env_ids] = -1
                self.c_go[env_ids] = False
                self.c_cmd_flips[env_ids] = 0.0
            if c.expert:
                self.c_left_idx[env_ids] = -1
                self.c_left_t[env_ids] = -1e9
                self.c_win_t[env_ids] = 0.0
                self.c_win_xy[env_ids] = obj_xy
                self.c_win_yaw[env_ids] = obj_heading
                self.c_win_pe[env_ids] = 1e6
                self.c_fin_stalls[env_ids] = 0.0
                self.c_fin[env_ids] = False
                self.c_stalled[env_ids] = False
                self.c_replans[env_ids] = 0.0
                self.c_plan_reason[env_ids] = 0
                self.c_plan_n[env_ids] = 0.0
                self.c_replan_slow[env_ids] = 0.0
                self.c_slow_wait[env_ids] = 0.0
                self.c_rhist[env_ids] = 0.0
                self.c_rhist_t[env_ids] = 0.0
                self.c_replan_weak[env_ids] = 0.0
                self.c_weak[env_ids] = False
                self.c_strength[env_ids] = 1e6
                self.c_need_more[env_ids] = False
                self.c_need_more_t[env_ids] = 0.0
                self.c_phase[env_ids] = 0
            self.c_resid[env_ids] = 0.0
            self.c_res_t[env_ids] = 0.0
            self.c_prev_pose[env_ids] = torch.linalg.norm(goal_xy - obj_xy, dim=-1) + self.c_rg[env_ids] * \
                torch.where(self.sym[shape] > 0, e0, torch.zeros_like(e0)).abs()
            self.c_comobj[env_ids], self.c_rule[env_ids] = ccom, rule
            self.c_preobj[env_ids] = cpre
            self.c_time[env_ids] = 0.0
            # scripted object motion for a share of (training) episodes
            dist = torch.rand(m, device=dev) < c.disturb_frac
            t0 = U(c.disturb_start[0], c.disturb_start[1])
            self.d_t0[env_ids] = torch.where(dist, t0, torch.full_like(t0, 1e9))
            self.d_t1[env_ids] = torch.where(dist, t0 + U(c.disturb_dur[0], c.disturb_dur[1]), torch.full_like(t0, -1.0))
            ang = 2 * math.pi * torch.rand(m, device=dev)
            spd = U(c.disturb_speed[0], c.disturb_speed[1])
            self.d_vel[env_ids] = torch.stack([spd * torch.cos(ang), spd * torch.sin(ang),
                                               c.disturb_yaw_rate * (2 * torch.rand(m, device=dev) - 1)], -1)
            self.c_yaw0[env_ids] = obj_heading
            self.c_drift_t[env_ids] = 0.0
            self.c_free_t[env_ids] = 0.0
            self.c_engaged[env_ids] = False
            ch, sh = torch.cos(obj_heading), torch.sin(obj_heading)
            to_w = lambda v: obj_xy + torch.stack([ch * v[:, 0] - sh * v[:, 1], sh * v[:, 0] + ch * v[:, 1]], -1)  # noqa: E731
            self.c_switches[env_ids] = 0.0
            lo, hi = c.reselect_s
            self.c_reselect_t[env_ids] = (lo + (hi - lo) * torch.rand(m, device=dev)) if hi > 0 else 1e9
            if c.expert:  # first expert re-plan right after the start, with the robots' real positions and routes
                self.c_reselect_t[env_ids] = torch.where(rule == 4, torch.full_like(self.c_reselect_t[env_ids], 0.1),
                                                         self.c_reselect_t[env_ids])
            stands, pres = [], []
            for k, a in enumerate(AGENTS):
                nk = cn[:, k]
                lat_k = torch.stack([-nk[:, 1], nk[:, 0]], -1)
                stands.append(cp[:, k] + nk * (self.reach[a] + U(0.02, 0.10)).unsqueeze(-1)
                              + lat_k * U(-0.08, 0.08).unsqueeze(-1))
                pres.append(cpre[:, k])
            cpose = []
            radius = self.radius_env[env_ids, shape]
            for k, a in enumerate(AGENTS):
                # each robot starts at its contact, at its approach point (probability 1 - contact_start_at)
                # or anywhere around the object (random_start), the last two only where they keep 1 m
                # from where the partner is (robot 1) / will most likely be (robot 0: its contact)
                o = 1 - k
                partner_at = cpose[0][0] if k == 1 else to_w(stands[o])
                nk = cn[:, k]
                yaw = torch.atan2(-nk[:, 1], -nk[:, 0]) + obj_heading + sym_u(torch.full((m,), 10.0, device=dev))
                pos = to_w(stands[k])
                pre_w = to_w(pres[k])
                at_pre = (torch.rand(m, device=dev) >= c.contact_start_at) & (torch.linalg.norm(pre_w - partner_at, dim=-1) > 1.0) & \
                    (torch.linalg.norm(pres[k] - pres[o], dim=-1) > 1.0)
                pos = torch.where(at_pre.unsqueeze(-1), pre_w, pos)
                bear = 2 * math.pi * torch.rand(m, device=dev)
                around = obj_xy + (radius + self.reach[a] + U(0.3, 0.9)).unsqueeze(-1) * torch.stack([torch.cos(bear), torch.sin(bear)], -1)
                rnd = (torch.rand(m, device=dev) < c.random_start) & (torch.linalg.norm(around - partner_at, dim=-1) > 1.2)
                if c.keep_order:  # v2: only on its own side of the partner (it must not walk around it)
                    brg = lambda v: torch.atan2((v - obj_xy)[:, 1], (v - obj_xy)[:, 0])  # noqa: E731
                    free = math.radians(c.order_free_deg)
                    dth = wrap(brg(partner_at) - bear)
                    dph = wrap(brg(to_w(stands[o])) - brg(to_w(stands[k])))
                    rnd &= ((dth > 0) == (dph > 0)) | (dth.abs() > free) | (dph.abs() > free)
                pos = torch.where(rnd.unsqueeze(-1), around, pos)
                yaw = torch.where(rnd, bear + math.pi + sym_u(torch.full((m,), 20.0, device=dev)), yaw)
                cpose.append((pos, yaw))
                front = pos + self.reach[a] * torch.stack([torch.cos(yaw), torch.sin(yaw)], -1)
                self.c_reach_lim[env_ids, k] = self.reach_limit(torch.linalg.norm(front - to_w(cp[:, k]), dim=-1))

        self.goal_xy[env_ids] = goal_xy
        self.goal_yaw[env_ids] = goal_yaw
        zeros = torch.zeros(m, device=dev)
        rel, poses = {}, {}
        for k, a in enumerate(AGENTS):
            robot = self.robots[a]
            dist = self.radius_env[env_ids, shape] + self.reach[a] + gaps[k]
            pos = obj_xy + dist.unsqueeze(-1) * torch.stack([torch.cos(bearings[k]), torch.sin(bearings[k])], -1)
            yaw = bearings[k] + math.pi + yaw_noise[k]
            if cpose is not None:
                sb = sc.get("start_behind") if sc is not None else None  # eval: start at the placements, walk to the contacts
                if sb is None:
                    pos, yaw = cpose[k]
                else:
                    pos = torch.where(sb.unsqueeze(-1), pos, cpose[k][0])
                    yaw = torch.where(sb, yaw, cpose[k][1])
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
        sb = sc.get("start_behind") if (sc is not None and cpose is not None) else None
        if c.keep_order and sb is not None:
            # v2: robots placed away from their contacts (eval "start behind") take them in their own order
            # (the pair was drawn without knowing where the robots stand; an evaluation's forced pair is kept)
            ch, sh = torch.cos(obj_heading), torch.sin(obj_heading)
            brg = lambda v: torch.atan2(v[:, 1], v[:, 0])  # noqa: E731
            st_w = [torch.stack([ch * v[:, 0] - sh * v[:, 1], sh * v[:, 0] + ch * v[:, 1]], -1)
                    for v in (self.c_pobj[env_ids, k] + self.c_nobj[env_ids, k] * 0.6 for k in range(2))]
            dth = wrap(brg(poses[AGENTS[1]][0] - obj_xy) - brg(poses[AGENTS[0]][0] - obj_xy))
            dph = wrap(brg(st_w[1]) - brg(st_w[0]))
            free = math.radians(c.order_free_deg)
            crossed = ((dth > 0) != (dph > 0)) & (dth.abs() <= free) & (dph.abs() <= free) & sb & ~park[0] & ~park[1]
            if forced is not None:
                crossed &= forced[:, 0].to(dev) < 0
            if bool(crossed.any()):
                e = env_ids[crossed]
                for t in (self.c_idx, self.c_pobj, self.c_nobj, self.c_preobj, self.push_dir_obj):
                    t[e] = t[e].flip(1)
                for k, a in enumerate(AGENTS):
                    v = self.c_pobj[e, k]
                    hc, hs = ch[crossed], sh[crossed]
                    pw = obj_xy[crossed] + torch.stack([hc * v[:, 0] - hs * v[:, 1], hs * v[:, 0] + hc * v[:, 1]], -1)
                    pos, yaw = poses[a][0][crossed], poses[a][1][crossed]
                    front = pos + self.reach[a] * torch.stack([torch.cos(yaw), torch.sin(yaw)], -1)
                    self.c_reach_lim[e, k] = self.reach_limit(torch.linalg.norm(front - pw, dim=-1))

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
    # turn practice (turn_debug): a share of episodes is a turn in place - the goal within turn_dist m of the object,
    # its heading off by turn_deg (either way, capped by the object's symmetry). Objects whose heading does not
    # matter (sphere) are left out; these episodes do not count toward the task-level curriculum.
    turn_frac: float = 0.0
    turn_dist: tuple[float, float] = (0.0, 0.3)
    turn_deg: tuple[float, float] = (15.0, 90.0)
    # Stage 4 contact mode (see the module docstring)
    contact_mode: bool = False
    contact_mix: tuple[float, ...] = (1.0, 1.0, 1.0)  # spread, adjacent, random[, wrench[, expert]] pair
    contact_start_at: float = 0.7  # share of robots starting at the contact (the rest at its approach point)
    contact_min_sep: float = 0.85  # m between the two robots' standing points
    # planner (QUADCOOP_PLANNER: default "ends"; v2 = all three parts; v1 = the planner before 2026-11-09):
    #   face_ends   turning contacts at the two ends of every short face (a cube had none: all its
    #               contacts pushed through its centre)
    #   footprint   a pair is usable only if the two standing robots' footprints (+ margin) do not
    #               overlap, at the env's object size (v1: standing-point distance at nominal size only)
    #   keep_order  the robots keep their order around the object: an assignment is usable only if
    #               the contacts are in the same order (counter-clockwise) as the robots, so the planner
    #               re-assigns instead of sending one robot around the other (unless they are about
    #               opposite each other, where either order is free); also applied at the episode start
    #   (QUADCOOP_PLANNER may also list the parts: e.g. "ends,order")
    face_ends: bool = "ends" in PLANNER_PARTS
    footprint_sep: bool = "footprint" in PLANNER_PARTS
    keep_order: bool = "order" in PLANNER_PARTS
    footprint_margin: float = 0.08  # m added around each robot's footprint (FOOTPRINT_HALF)
    order_free_deg: float = 150.0  # robots this far apart around the object: either order
    drift_dist: float = 0.35  # m from the front to the contact point
    drift_heading_deg: float = 45.0  # and facing the push direction within this
    drift_s: float = 1.0
    engage_s: float = 8.0  # (initial value of the reach limits; replaced at every assignment)
    reach_base_s: float = 2.0  # reach limit = base + detour x distance / speed, clamped to [3, reach_max_s]
    reach_detour: float = 1.5
    reach_speed: float = 0.4
    reach_max_s: float = 15.0
    random_start: float = 0.0  # share of robots starting anywhere around the object (they walk to their contact)
    reselect_s: tuple[float, float] = (0.0, 0.0)  # re-apply the contact rule every U(lo, hi) s; (0, 0) = fixed contacts
    expert_first_only: bool = False  # with reselect_s (0, 0): still run the expert's first re-plan (0.1 s), then freeze
    # slow-arrival re-plans: at most one per env per slow_min_s (0 = every step while a robot is overdue, as trained).
    # A KEEP leaves the overdue condition true, so without this the same question is asked again next step.
    slow_min_s: float = 0.0
    # residual execution pilot (docs/residual_pilot.md): resid_<robot> inputs (forces, motion, shares, contact
    # geometry, 0.4 s history at 10 Hz) and the per-env gate (1 where the correction is enabled)
    resid: bool = False
    resid_objects: tuple = ()  # shape names with the correction enabled; () = all
    shape_bias: tuple = ()  # ((shape name, weight), ...) multiplies the training shape mix (0 = never drawn)
    # (applied after the eligibility mask: a held-out shape stays out unless it is in train_shapes)
    resid_gate_dist: float = 0.0  # > 0: the correction is also gated per robot to contact_dist <= this (m)
    train_shapes: tuple = ()  # shapes eligible in training; () = the Stage 2 split (TRAIN_NAMES)
    train_mass: tuple = ()  # (lo, hi) kg: fixed mass window for the shape draw instead of the level's
    fixed_difficulty: bool = False  # curriculum holds level and tolerance, shape weights stay uniform
    reselect_margin: float = 0.3  # m of rule score a new pair needs over the current one (hysteresis)
    reselect_min_dist: float = 0.15  # m: no re-selection with the object this close to its goal
    off_contact_mode: str = "terminate"  # "terminate" (Stage 4 / 4b) or "soft" (cost, no ending, no deadlines)
    phi_heading_weight: float = 0.25  # m per rad of heading error in the contact-approach potential
    guide: bool = False  # Stage 4d: route to the contact (guide_obs inputs, route-length pull)
    guide_margin: float = 0.6  # m around the object's bounding box the route keeps the robot's centre
    disturb_frac: float = 0.0  # share of episodes with scripted object motion (training only)
    disturb_start: tuple[float, float] = (1.0, 8.0)  # s after the start
    disturb_dur: tuple[float, float] = (1.5, 3.0)  # s
    disturb_speed: tuple[float, float] = (0.15, 0.35)  # m/s
    disturb_yaw_rate: float = 0.3  # rad/s at most
    # Stage 4e: a push direction per robot recomputed every step from the remaining error
    wrench: bool = False  # compute the wanted motion, the push split and the pair residual (wrench rule)
    push_cmd: bool = False  # push-direction inputs, on-contact judged against it, 4e rewards, partner-aware route
    push_mu: float = 0.5  # robot-object friction for the cones the split keeps each push inside
    push_ridge: float = 0.3  # penalty on push size in the split (large-force solutions score badly)
    push_vmax: float = 0.3  # m/s wanted at most, reached push_rv from the goal
    push_rv: float = 0.5
    push_wmax: float = 0.4  # rad/s wanted at most, reached push_rw from the goal angle
    push_rw: float = 0.5
    push_tau: float = 0.3  # s: low-pass of the push directions
    resid_bad: float = 0.5  # the pair cannot do the job above this residual ...
    resid_dwell_s: float = 1.0  # ... for this long: re-choose now
    resid_margin: float = 0.25  # residual a new pair must gain (hysteresis)
    walk_weight: float = 0.1  # residual per m of walk to a new contact
    partner_stand: float = 0.8  # m: no contact whose standing point is this close to the partner
    partner_clear: float = 0.7  # m: a route leg this close to the partner counts as blocked ...
    partner_block_m: float = 3.0  # ... and is chosen as if this much longer
    # expert planner v2 (contact rule 4)
    expert: bool = False  # the expert planner's machinery (needs wrench)
    walk_speed: float = 0.5  # m/s assumed walking around the object (arrival times)
    time_weight: float = 0.05  # cost per second of the slower robot's arrival
    stop_weight: float = 0.1  # cost per robot that stops pushing to move
    stall_penalty: float = 0.5  # added to the current choice after a window with no progress
    expert_margin: float = 0.15  # a new choice must beat the current one by this much
    relock_s: float = 3.0  # no going back to a contact left less than this long ago
    stall_window: float = 2.0  # s per no-progress window ...
    stall_move: float = 0.05  # ... no progress = moved less than this (m) ...
    stall_turn: float = 0.05  # ... and turned less than this (rad)
    strength_margin: float = 1.3  # a stall is the place's fault only if the pair can push this x the sliding force
    exec_v2: bool = False  # Phase 2 executor: a phase command (walk / hold / push) + team ready as inputs, hold_cost
    hold_rand: float = 0.0  # exec_v2 training: share of contact arrivals told to hold hold_rand_s regardless
    hold_rand_s: tuple[float, float] = (0.5, 4.0)
    ready_dist: float = 0.25  # exec_v2: ready = front within this of its contact (m) ...
    ready_heading_deg: float = 30.0  # ... heading within this of its push direction ...
    ready_steady_s: float = 0.3  # ... for this long
    flicker_s: float = 0.5  # exec_v2: a robot off its contact for less than this still counts as on it
    exec_cmd_mode: str = "planner"  # exec_v2 (eval ablation): "always_push" = on its contact -> push (no hold, no barrier)
    finish_dist: float = 0.0  # > 0: finishing zone, pose error (m, distance + rho_g x angle) below this:
    finish_frac: float = 0.1  # ... no progress = pose error fell by less than this share of itself in a window;
    finish_resid: float = 0.5  # ... stalls not penalised, the pair changed only if its residual is above this
    turn_full_dist: float = 0.0  # > 0: beyond this distance (m) the wanted turn shrinks as 1 / distance
    robot_push_force: float = 250.0  # N one robot can push with (assumed; to be measured): heavier -> push together
    # push effort (force_track): each robot gets an absolute push target - its share of what slides the object,
    # effort_margin x mu m g, at most robot_push_force - and feedback of the force it actually applies
    effort: bool = False
    effort_margin: float = 1.2
    solo_wait_s: float = 2.0  # push alone only if the partner is further than this from its contact
    expert_dt: float = 0.1  # s between expert updates (priorities, arrivals, go / hold, no-progress windows)
    # success-tolerance curriculum: ((pos tol m, yaw tol deg), ...) loose -> fine; () = fixed
    # success_pos_tol / success_yaw_tol_deg
    tol_levels: tuple[tuple[float, float], ...] = ()
    tol_start_finest: bool = False  # evaluation: start at the finest tolerance
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


def contact_obs(env, robot: str) -> torch.Tensor:
    """Stage 4 (9), this robot's frame: its contact point rel. the robot (2), the push direction
    (2), the contact's arm about the object's centre of mass (2), the z torque of a unit push there
    (1), and the partner's contact point rel. this robot (2)."""
    g = _g(env)
    k = AGENTS.index(robot)
    base = env.scene[robot].data.root_link_pos_w[:, :2]
    p_k, n_k = g.contact_world(k)
    p_o, _ = g.contact_world(1 - k)
    arm = g.contact_arm_world(k)
    tau = arm[:, 0] * (-n_k[:, 1]) - arm[:, 1] * (-n_k[:, 0])
    return torch.cat([_to_frame(env, robot, p_k - base), _to_frame(env, robot, -n_k), _to_frame(env, robot, arm),
                      tau.unsqueeze(-1), _to_frame(env, robot, p_o - base)], dim=-1)


def guide_obs(env, robot: str) -> torch.Tensor:
    """Stage 4d (6), this robot's frame: the next waypoint of its route rel. the robot (2), the
    velocity of its contact point (2), on its contact (1), route length left / 3 m (1, at most 2)."""
    g = _g(env)
    k = AGENTS.index(robot)
    wp, route = g.guide(k)
    base = env.scene[robot].data.root_link_pos_w[:, :2]
    return torch.cat([_to_frame(env, robot, wp - base), _to_frame(env, robot, g.contact_velocity(k)),
                      g.on_contact(k).float().unsqueeze(-1), (route / 3.0).clamp(0.0, 2.0).unsqueeze(-1)], dim=-1)


def push_obs(env, robot: str) -> torch.Tensor:
    """Stage 4e (4), this robot's frame: its push direction (cos, sin of the angle from its heading),
    its share of the total push, and the pair's residual (0 = the pair can make the motion still
    wanted, 1 = not at all)."""
    g = _g(env)
    k = AGENTS.index(robot)
    d = g.push_dir_world(k)
    ang = torch.atan2(d[:, 1], d[:, 0]) - yaw_of(env.scene[robot].data.root_link_quat_w)
    return torch.stack([torch.cos(ang), torch.sin(ang), g.push_share[:, k], g.c_resid], -1)


def contact_work(env, robot: str, f_ref: float = 200.0, max_ratio: float = 2.0, max_speed: float = 1.0) -> torch.Tensor:
    """rmin, per robot: this robot's own pushing work toward the motion the planner wants, per second,
    normalised: (its contact force on the object along its commanded push direction / f_ref, 0..
    max_ratio) x (the object's motion along the wanted motion, m/s with turning as rho_g x yaw rate,
    0..max_speed). 0 without contact, 0 if the object does not move the wanted way: only a push that
    helps pays, and two robots share it by how hard each pushes (a difference-reward approximation,
    as r8's work_credit, but along the commanded directions). f_ref = 200 N ~ one ANYmal's push."""
    g = _g(env)
    k = AGENTS.index(robot)
    rg2 = g.c_rg.square()
    norm = torch.sqrt(g.c_vdes.square().sum(-1) + rg2 * g.c_wdes.square())
    proj = ((g.box_vel()[:, :2] * g.c_vdes).sum(-1) + rg2 * g.box_ang_vel()[:, 2] * g.c_wdes) / norm.clamp(min=1e-6)
    f = (object_force_from(env, robot) * g.push_dir_world(k)).sum(-1)
    push = (f / f_ref).clamp(0.0, max_ratio)
    return torch.where(norm > 1e-3, push * proj.clamp(0.0, max_speed), torch.zeros_like(proj))


def push_effort(env, k: int) -> torch.Tensor:
    """force_track: robot k's push target (N) - its share of the pair's push times what slides the object
    (effort_margin x mu m g), at most robot_push_force; 0 with no push wanted."""
    g = _g(env)
    sh = g.push_share
    tot = sh.sum(-1)
    share = sh[:, k] / tot.clamp(min=1e-6)
    need = g.cfg.effort_margin * g.c_mu * g.c_mass * 9.81
    return torch.where(tot > 1e-6, (share * need).clamp(max=g.cfg.robot_push_force), torch.zeros_like(tot))


def effort_obs(env, robot: str, f_ref: float = 200.0) -> torch.Tensor:
    """force_track, this robot's frame (8): the contact force it applies to the object (x, y / f_ref), that
    force along its commanded push direction (/ f_ref), touching (> 5 N), its push target (/ f_ref), and the
    object motion the planner wants (velocity x, y / push_vmax, yaw rate / push_wmax)."""
    g = _g(env)
    k = AGENTS.index(robot)
    yaw = yaw_of(env.scene[robot].data.root_link_quat_w)
    c, s = torch.cos(yaw), torch.sin(yaw)
    to_robot = lambda v: torch.stack([c * v[:, 0] + s * v[:, 1], -s * v[:, 0] + c * v[:, 1]], -1)  # noqa: E731
    f = object_force_from(env, robot)
    along = (f * g.push_dir_world(k)).sum(-1)
    touch = (torch.linalg.norm(f, dim=-1) > 5.0).float()
    fr = (to_robot(f) / f_ref).clamp(-2.0, 2.0)
    vd = to_robot(g.c_vdes) / g.cfg.push_vmax
    wd = (g.c_wdes / g.cfg.push_wmax).unsqueeze(-1)
    return torch.cat([fr, (along / f_ref).clamp(-1.0, 2.0).unsqueeze(-1), touch.unsqueeze(-1),
                      (push_effort(env, k) / f_ref).unsqueeze(-1), vd.clamp(-1.5, 1.5), wd.clamp(-1.5, 1.5)], -1)


def contact_sense_obs(env, robot: str, f_ref: float = 200.0) -> torch.Tensor:
    """contact sense (7), this robot's frame: the contact force it applies to the object (x, y / f_ref),
    that force along its commanded push direction (/ f_ref), touching (> 5 N), and the object motion the
    planner wants (velocity x, y / push_vmax, yaw rate / push_wmax). effort_obs without the push target:
    lets the executor tell 'near the contact' from 'actually pressing it'."""
    g = _g(env)
    k = AGENTS.index(robot)
    yaw = yaw_of(env.scene[robot].data.root_link_quat_w)
    c, s = torch.cos(yaw), torch.sin(yaw)
    to_robot = lambda v: torch.stack([c * v[:, 0] + s * v[:, 1], -s * v[:, 0] + c * v[:, 1]], -1)  # noqa: E731
    f = object_force_from(env, robot)
    along = (f * g.push_dir_world(k)).sum(-1)
    touch = (torch.linalg.norm(f, dim=-1) > 5.0).float()
    vd = to_robot(g.c_vdes) / g.cfg.push_vmax
    wd = (g.c_wdes / g.cfg.push_wmax).unsqueeze(-1)
    return torch.cat([(to_robot(f) / f_ref).clamp(-2.0, 2.0), (along / f_ref).clamp(-1.0, 2.0).unsqueeze(-1),
                      touch.unsqueeze(-1), vd.clamp(-1.5, 1.5), wd.clamp(-1.5, 1.5)], -1)


def contact_acquired(env, robot: str, press_n: float = 30.0, hold_s: float = 0.5, progress_m: float = 0.1) -> torch.Tensor:
    """Contact-acquired event (weighted by bonus / step_dt, so each event pays the bonus once): 1 when the
    robot has been on its assigned contact pushing it with press_n N or more along its push direction for
    hold_s s in a row (a single impact does not count). At most one payout per assignment, and a new
    assignment re-arms it only once the object has made progress_m of pose progress (pose_error, m) since
    the last payout, so switching between contacts cannot farm the bonus; a new episode re-arms it."""
    g = _g(env)
    k = AGENTS.index(robot)
    n, dev = env.num_envs, env.device
    key = f"_qc_acq_{robot}"
    if not hasattr(env, key):
        setattr(env, key, (torch.zeros(n, dtype=torch.bool, device=dev), torch.full((n,), -1, dtype=torch.long, device=dev),
                           torch.zeros(n, device=dev), torch.full((n,), 1e9, device=dev)))
    done, last_idx, t_press, pe_paid = getattr(env, key)
    pe = g.pose_error()
    new_ep = env.episode_length_buf <= 1
    pe_paid[:] = torch.where(new_ep, torch.full_like(pe_paid, 1e9), pe_paid)
    changed = g.c_idx[:, k] != last_idx
    done &= ~(new_ep | (changed & (pe <= pe_paid - progress_m)))
    last_idx[:] = g.c_idx[:, k]
    f = (object_force_from(env, robot) * g.push_dir_world(k)).sum(-1)
    pressing = g.on_contact(k) & (f >= press_n) & ~changed & ~new_ep
    t_press[:] = torch.where(pressing, t_press + env.step_dt, torch.zeros_like(t_press))
    hit = (t_press >= hold_s - 1e-6) & ~done
    done |= hit
    pe_paid[:] = torch.where(hit, pe, pe_paid)
    return hit.float()


def effort_work(env, robot: str, max_speed: float = 1.0) -> torch.Tensor:
    """force_track, per robot (replaces contact_work): its push along the commanded direction as a fraction
    of its push target (0..1: pushing past the target earns nothing more) x the object's motion along the
    wanted motion (m/s, turning as rho_g x yaw rate). Pressing pays only while the object moves usefully."""
    g = _g(env)
    k = AGENTS.index(robot)
    rg2 = g.c_rg.square()
    norm = torch.sqrt(g.c_vdes.square().sum(-1) + rg2 * g.c_wdes.square())
    proj = ((g.box_vel()[:, :2] * g.c_vdes).sum(-1) + rg2 * g.box_ang_vel()[:, 2] * g.c_wdes) / norm.clamp(min=1e-6)
    f = (object_force_from(env, robot) * g.push_dir_world(k)).sum(-1)
    tgt = push_effort(env, k)
    frac = torch.where(tgt > 10.0, (f / tgt.clamp(min=10.0)).clamp(0.0, 1.0), torch.zeros_like(f))
    return torch.where(norm > 1e-3, frac * proj.clamp(0.0, max_speed), torch.zeros_like(proj))


def over_push(env, robot: str, over: float = 1.5, f_ref: float = 200.0) -> torch.Tensor:
    """force_track, per robot, a cost per second: contact force beyond `over` x its push target (/ f_ref, at
    most 2) - pushing much harder than asked (light objects skidding off, a robot told to stay soft)."""
    g = _g(env)
    k = AGENTS.index(robot)
    f = torch.linalg.norm(object_force_from(env, robot), dim=-1)
    return ((f - over * push_effort(env, k)) / f_ref).clamp(0.0, 2.0)


def cmd_obs(env, robot: str) -> torch.Tensor:
    """Phase 2 executor (4): this robot's phase command one-hot (walk, hold, push) and team ready."""
    g = _g(env)
    k = AGENTS.index(robot)
    return torch.cat([torch.nn.functional.one_hot(g.c_cmd[:, k], 3).float(), g.c_team_ready.float().unsqueeze(-1)], -1)


def hold_cost(env, robot: str, f_ref: float = 100.0, max_ratio: float = 3.0) -> torch.Tensor:
    """Phase 2 executor, per robot, while told to hold: its horizontal contact force on the object /
    f_ref (at most max_ratio) + its base's horizontal speed (m/s). Holding = staying on the contact
    without pushing or walking; 0 in the other phases."""
    g = _g(env)
    k = AGENTS.index(robot)
    f = (torch.linalg.norm(object_force_from(env, robot), dim=-1) / f_ref).clamp(max=max_ratio)
    v = torch.linalg.norm(env.scene[robot].data.root_link_lin_vel_w[:, :2], dim=-1)
    return torch.where(g.c_cmd[:, k] == 1, f + v, torch.zeros_like(f))


def pose_progress(env, max_rate: float = 1.0) -> torch.Tensor:
    """Stage 4e, team: decrease per second of distance + rho_g x |angle error| (rho_g = the object's
    radius of gyration), clipped: a radian of turning is worth rho_g metres of travel."""
    g = _g(env)
    return ((g.c_prev_pose - g.pose_error()) / env.step_dt).clamp(-max_rate, max_rate)


def motion_credit(env, robot: str, contact: float = 0.08, max_speed: float = 1.0, press_force: float = 0.0) -> torch.Tensor:
    """Stage 4e, per robot: the object's motion along the motion still wanted (m/s; turning counted
    as rho_g x yaw rate), clipped to 0..max_speed, credited only while this robot's front is on the
    object (within `contact`) and it is on its contact. Pays for turning as much as for travel.
    press_force > 0 (run A of the hovering test): credited only while this robot actually touches
    the object with at least press_force N (contact sensor); with 0 a front within `contact` is
    enough, so a robot hovering near the object is paid for its partner's push."""
    g = _g(env)
    k = AGENTS.index(robot)
    rg2 = g.c_rg.square()
    norm = torch.sqrt(g.c_vdes.square().sum(-1) + rg2 * g.c_wdes.square())
    proj = ((g.box_vel()[:, :2] * g.c_vdes).sum(-1) + rg2 * g.box_ang_vel()[:, 2] * g.c_wdes) / norm.clamp(min=1e-6)
    on = (g.surface_distance(robot) < contact) & g.on_contact(k) & (norm > 1e-3)
    if press_force > 0:
        touching = env.scene[f"push_{robot}"].data.found.view(env.num_envs, -1).any(-1)
        on = on & touching & (torch.linalg.norm(object_force_from(env, robot), dim=-1) >= press_force)
    if g.cfg.exec_v2:  # Phase 2: paid only when told to push
        on = on & (g.c_cmd[:, k] == 2)
    return torch.where(on, proj.clamp(0.0, max_speed), torch.zeros_like(proj))


def walk_cost(env, robot: str) -> torch.Tensor:
    """Stage 4e, per robot: 1 per second while on the way to a contact it has not reached yet (the
    off-contact cost covers a contact it had reached)."""
    g = _g(env)
    k = AGENTS.index(robot)
    return (~g.c_engaged[:, k] & ~g.on_contact(k)).float()


def bump_cost(env, robot: str) -> torch.Tensor:
    """Stage 4d, per robot: 1 per second while it touches the object anywhere but on its contact."""
    g = _g(env)
    k = AGENTS.index(robot)
    touching = env.scene[f"push_{robot}"].data.found.view(env.num_envs, -1).any(-1)
    return (touching & ~g.on_contact(k)).float()


def off_contact(env, robot: str) -> torch.Tensor:
    """Stage 4 termination: the robot left its contact (off it for drift_s after reaching it) or
    did not reach its (new) contact in time (reach_limit of the distance when it was assigned)."""
    g = _g(env)
    k = AGENTS.index(robot)
    return (g.c_drift_t[:, k] >= g.cfg.drift_s) | (g.c_free_t[:, k] >= g.c_reach_lim[:, k])


def contact_approach(env, robot: str, max_rate: float = 5.0) -> torch.Tensor:
    """Soft contact mode, per robot: decrease of its contact-approach potential per second
    (potential-based: walking to the contact pays the distance once, leaving takes it back)."""
    g = _g(env)
    k = AGENTS.index(robot)
    return torch.clamp((g.c_prev_phi[:, k] - g.contact_phi(k)) / env.step_dt, -max_rate, max_rate)


def off_contact_cost(env, robot: str) -> torch.Tensor:
    """Soft contact mode, per robot: 1 per second while it is off the contact it had reached (a
    robot on its way to a newly assigned contact pays nothing)."""
    g = _g(env)
    k = AGENTS.index(robot)
    return (g.c_engaged[:, k] & ~g.on_contact(k)).float()


def own_off_contact(env, robot: str) -> torch.Tensor:
    return off_contact(env, robot).float()


def contact_curriculum(env, env_ids: torch.Tensor, tol_advance: float = 0.5, level_advance: float = 0.30,
                       level_retreat: float = 0.05, level_unlock: int = 2, tol_dwell_iters: int = 100,
                       level_dwell_iters: int = 100, level_fallback_iters: int = 500, ema_per_episode: float = 0.003,
                       steps_per_iter: int = 24):
    """Stage 4 curriculum: the success tolerance (cfg.tol_levels) goes loose -> fine, and the task
    level (distance, turn, mass) rises, each on its own success rate.

    * Rates are running averages per finished episode (weight ema_per_episode each, so a burst of
      resets in one step cannot swing them), over the ordinary episodes only: the need_frac
      episodes (heavy wide objects) and replayed lower levels are left out, so a hard training mix
      cannot hold the curriculum back.
    * The tolerance advances when its rate (episodes started at the current tolerance) passes
      tol_advance, at least tol_dwell_iters after the last change. It never goes back.
    * The task level starts moving once the tolerance has reached level_unlock (0-based; default
      15 cm / 6 deg): up when its rate (episodes at the current level and tolerance) passes
      level_advance, down below level_retreat, at most every level_dwell_iters; and up anyway once
      the finest tolerance is reached and the level has not moved for level_fallback_iters, so
      training always gets to the evaluation's distances and turns.
    Stage 2's push2_curriculum still keeps the per-shape weights (its own level logic is off)."""
    from quadcoop.stage2.mdp import push2_curriculum

    g = _g(env)
    it = env.common_step_counter / steps_per_iter
    n_tol = len(g.cfg.tol_levels)
    out = push2_curriculum(env, env_ids, steps_per_iter=steps_per_iter, allow_level=False)
    if g.cfg.fixed_difficulty:  # fixed-difficulty check: uniform shape weights, level and tolerance held
        g.shape_weight.fill_(1.0)
        tl = g.cfg.tol_levels[g.tol_level]
        out.update({"level": torch.tensor(float(g.level)), "tol_level": torch.tensor(float(g.tol_level)),
                    "tol_pos_m": torch.tensor(float(tl[0])), "tol_yaw_deg": torch.tensor(float(tl[1]))})
        return out
    if not hasattr(g, "lvl_ema"):
        g.lvl_ema = 0.0
    if isinstance(env_ids, torch.Tensor) and len(env_ids) > 0:
        succ = g.metrics["success"][env_ids]
        ordinary = ~g.need_episode[env_ids] & ~g.turn_episode[env_ids]

        def update(ema, sel):
            cnt = int(sel.sum())
            if cnt == 0:
                return ema
            w = 1.0 - (1.0 - ema_per_episode) ** cnt
            return (1.0 - w) * ema + w * float(succ[sel].mean())

        at_tol = ordinary & (g.env_tol_level[env_ids] == g.tol_level)
        g.tol_ema = update(g.tol_ema, at_tol)
        g.lvl_ema = update(g.lvl_ema, at_tol & (g.env_level[env_ids] == g.level))
        if g.tol_level < n_tol - 1 and it - g.tol_last_change >= tol_dwell_iters and g.tol_ema > tol_advance:
            g.tol_level += 1
            g.tol_last_change = it
            g.tol_ema = 0.5 * tol_advance  # restart the estimate at the new tolerance
            g.lvl_ema = min(g.lvl_ema, 0.5 * level_advance)
        if g.tol_level >= min(level_unlock, n_tol - 1) and it - g.last_change_iter >= level_dwell_iters:
            if g.lvl_ema > level_advance and g.level < len(g.cfg.levels) - 1:
                g.level += 1
                g.last_change_iter = it
                g.lvl_ema = 0.5 * (level_advance + level_retreat)
            elif g.lvl_ema < level_retreat and g.level > 0:
                g.level -= 1
                g.last_change_iter = it
                g.lvl_ema = 0.5 * (level_advance + level_retreat)
            elif (g.tol_level >= n_tol - 1 and it - g.last_change_iter >= level_fallback_iters
                  and g.level < len(g.cfg.levels) - 1):
                g.level += 1
                g.last_change_iter = it
                g.lvl_ema = 0.5 * (level_advance + level_retreat)
    tl = g.cfg.tol_levels[g.tol_level]
    out.update({"level": torch.tensor(float(g.level)), "level_success_ema": torch.tensor(g.lvl_ema),
                "tol_level": torch.tensor(float(g.tol_level)), "tol_pos_m": torch.tensor(float(tl[0])),
                "tol_yaw_deg": torch.tensor(float(tl[1])), "tol_success_ema": torch.tensor(g.tol_ema)})
    if g.cfg.contact_mode:
        for k, a in enumerate(AGENTS):
            out[f"engaged_{a}"] = g.c_engaged[:, k].float().mean()
            out[f"contact_dist_{a}"] = g.contact_dist(k).mean()
            out[f"on_contact_{a}"] = g.on_contact(k).float().mean()
            out[f"walking_{a}"] = (~g.c_engaged[:, k]).float().mean()  # on the way to its contact
            off = g.c_engaged[:, k] & ~g.on_contact(k)
            n_off = int(off.sum())
            out[f"off_far_{a}"] = torch.tensor((g.contact_dist(k)[off] >= g.cfg.drift_dist).float().mean().item() if n_off else 0.0)
            out[f"off_turned_{a}"] = torch.tensor(
                (g.contact_heading_err(k)[off] >= math.radians(g.cfg.drift_heading_deg)).float().mean().item() if n_off else 0.0)
            out[f"off_share_{a}"] = off.float().mean()
            if g.cfg.guide:
                touching = env.scene[f"push_{a}"].data.found.view(env.num_envs, -1).any(-1)
                out[f"bump_share_{a}"] = (touching & ~g.on_contact(k)).float().mean()
                out[f"route_len_{a}"] = g.guide(k)[1].mean()
        if isinstance(env_ids, torch.Tensor) and len(env_ids) > 0:
            out["switches_per_episode"] = g.c_switches[env_ids].mean()
        if g.cfg.disturb_frac > 0:
            out["disturbed_now"] = ((g.c_time >= g.d_t0) & (g.c_time < g.d_t1)).float().mean()
        if g.cfg.exec_v2:
            for k, a in enumerate(AGENTS):
                for ph, nm in ((0, "walk"), (1, "hold"), (2, "push")):
                    out[f"cmd_{nm}_{a}"] = (g.c_cmd[:, k] == ph).float().mean()
            out["team_pushing"] = g.c_go.float().mean()
            out["random_hold"] = (g.c_rhold > 0).float().mean()
            if isinstance(env_ids, torch.Tensor) and len(env_ids) > 0:
                out["push_to_hold_per_episode"] = g.c_cmd_flips[env_ids].mean()
        if g.cfg.expert:
            out["expert_rule_share"] = (g.c_rule == 4).float().mean()
            out["holding_share"] = (g.c_phase == 1).float().mean()
        if g.cfg.wrench:
            out["pair_residual"] = g.c_resid.mean()
            out["residual_high"] = (g.c_resid > g.cfg.resid_bad).float().mean()
            out["wrench_rule_share"] = (g.c_rule == 3).float().mean()
        if g.c_reach_cnt > 0:
            out["reach_time_s"] = torch.tensor(g.c_reach_sum / g.c_reach_cnt)
            g.c_reach_sum, g.c_reach_cnt = 0.0, 0
    return out


def walker_command_of(env, twist_name: str) -> torch.Tensor:
    return env.command_manager.get_command(twist_name)


def partner_obs(env, robot: str, other: str, other_action: str) -> torch.Tensor:
    """New (9): partner position (2), its heading rel. this robot (sin, cos), its velocity (2),
    all in this robot's frame, and the command it last sent its walker (3, clipped to [-1, 1])."""
    r, p = env.scene[robot], env.scene[other]
    pos = _to_frame(env, robot, p.data.root_link_pos_w - r.data.root_link_pos_w)
    rel = wrap(yaw_of(p.data.root_link_quat_w) - yaw_of(r.data.root_link_quat_w))
    term = env.action_manager.get_term(other_action)
    # with a command interface the partner's applied (limited) command, so observations match what its walker gets
    cmd = term.applied_norm if getattr(term.cfg, "interface", "raw") != "raw" else term.raw_action.clamp(-1.0, 1.0)
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


RESID_H, RESID_HF = 4, 4  # residual pilot: history length (10 Hz) and features per sample


def resid_obs(env, robot: str) -> torch.Tensor:
    """Residual-pilot inputs for one robot (robot frame where directional), (n, 25 + RESID_H x RESID_HF):
    own and partner contact force on the object (2 + 2, / 200 N), force along own / partner push direction (2),
    commanded shares (own, partner), wanted object velocity (2) and yaw rate, object velocity (2) and yaw rate,
    own base velocity (2) and yaw rate, own push direction (2), own contact point relative to its front (2),
    contact distance, heading error, on-contact (own, partner), then the 10 Hz history (newest first)."""
    g = _g(env)
    k = AGENTS.index(robot)
    o = 1 - k
    yaw = g.robot_yaw(k)
    cs, sn = torch.cos(yaw), torch.sin(yaw)
    rf = lambda v: torch.stack([cs * v[:, 0] + sn * v[:, 1], -sn * v[:, 0] + cs * v[:, 1]], -1)  # noqa: E731
    f_own, f_par = object_force_from(env, AGENTS[k]), object_force_from(env, AGENTS[o])
    fa = [(f * g.push_dir_world(i)).sum(-1, keepdim=True) / 200.0 for f, i in ((f_own, k), (f_par, o))]
    r = env.scene[robot].data
    col = lambda x: x.float().unsqueeze(-1)  # noqa: E731
    out = torch.cat([
        rf(f_own) / 200.0, rf(f_par) / 200.0, *fa,
        g.push_share[:, k:k + 1], g.push_share[:, o:o + 1],
        rf(g.c_vdes), col(g.c_wdes),
        rf(g.box_vel()[:, :2]), col(g.box_ang_vel()[:, 2]),
        r.root_link_lin_vel_b[:, :2], r.root_link_ang_vel_b[:, 2:3],
        rf(g.push_dir_world(k)), rf(g.contact_world(k)[0] - g.front_point(robot)),
        col(g.contact_dist(k)), col(g.contact_heading_err(k)),
        col(g.on_contact(k)), col(g.on_contact(o)),
        g.c_rhist[:, k].reshape(g.num_envs, -1),
    ], -1)
    return out


def resid_base_last_action(env, robot: str) -> torch.Tensor:
    """Residual envs: the frozen base's own last raw output (n, 3), in place of the walker term's raw action. With the
    correction off, or not changing the applied command, the two are identical."""
    return _g(env).resid_base_last[:, AGENTS.index(robot)]


def resid_gate(env, robot: str) -> torch.Tensor:
    """(n, 1) for one robot: 1 where its residual correction is enabled. Object gate: the env's shape is in
    cfg.resid_objects (() = all). Phase gate (cfg.resid_gate_dist > 0): the robot's front is also within that
    distance of its assigned contact, i.e. final approach, pressing, and recovery after slipping off, but not
    the walk around the object or repositioning to a far contact."""
    g = _g(env)
    if not g.cfg.resid_objects:
        on = torch.ones(g.num_envs, dtype=torch.bool, device=g.device)
    else:
        sel = torch.tensor([SHAPES2[s].name in g.cfg.resid_objects for s in range(len(SHAPES2))], device=g.device)
        on = sel[g.shape]
    if g.cfg.resid_gate_dist > 0:
        on = on & (g.contact_dist(AGENTS.index(robot)) <= g.cfg.resid_gate_dist)
    return on.float().unsqueeze(-1)


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
