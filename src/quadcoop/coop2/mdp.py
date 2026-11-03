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
        lists = [C.candidates(nom_np[s], kinds_np[s], float(rest_np[s])) for s in range(S)]
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
        print(f"[coop2] contact mode: {', '.join(f'{SHAPES2[s].name} {len(cl)}' for s, cl in enumerate(lists))} "
              f"candidate contacts; pairs >= {self.cfg.contact_min_sep:g} m apart; rule mix {self.cfg.contact_mix}")

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

    def front_point(self, robot: str) -> torch.Tensor:
        r = self.robots[robot]
        yaw = yaw_of(r.data.root_link_quat_w)
        return r.data.root_link_pos_w[:, :2] + self.reach[robot] * torch.stack([torch.cos(yaw), torch.sin(yaw)], -1)

    def contact_heading_err(self, k: int) -> torch.Tensor:
        """|robot k's heading - its contact's push direction (-n)| (rad)."""
        _, nw = self.contact_world(k)
        want = torch.atan2(-nw[:, 1], -nw[:, 0])
        return wrap(yaw_of(self.robots[AGENTS[k]].data.root_link_quat_w) - want).abs()

    def contact_phi(self, k: int) -> torch.Tensor:
        """How far robot k is from being on its contact: front-to-contact distance (m) - with guide,
        the length of its route - plus phi_heading_weight x heading error (rad; with guide, only over
        the last metre of the route)."""
        if self.cfg.guide:
            _, route = self.guide(k)
            return route + self.cfg.phi_heading_weight * self.contact_heading_err(k) * (1.0 - route).clamp(0.0, 1.0)
        return self.contact_dist(k) + self.cfg.phi_heading_weight * self.contact_heading_err(k)

    def guide(self, k: int, pos_w: torch.Tensor | None = None) -> tuple[torch.Tensor, torch.Tensor]:
        """Robot k's route to its contact: the next waypoint (world, (n, 2)) and the route length
        left (m, (n,)), planned in the object frame around the bounding box inflated by guide_margin.
        pos_w: the robot centre to plan from (default: where robot k is)."""
        a = AGENTS[k]
        n, dev = self.num_envs, self.device
        ar = torch.arange(n, device=dev)
        yaw = self.contact_frame_yaw()
        cs, sn = torch.cos(yaw), torch.sin(yaw)
        obj = self.box_pos()[:, :2]
        bb = self.bbox_env[ar, self.shape]  # (cx, cy, hx, hy), object frame
        ctr = bb[:, :2]
        A = bb[:, 2:4] + self.cfg.guide_margin  # inflated half extents
        d = (self.robots[a].data.root_link_pos_w[:, :2] if pos_w is None else pos_w) - obj
        q = torch.stack([cs * d[:, 0] + sn * d[:, 1], -sn * d[:, 0] + cs * d[:, 1]], -1) - ctr  # robot centre
        nk = self.c_nobj[:, k]
        stand = self.c_pobj[:, k] + nk * (self.reach[a] + 0.06) - ctr
        pre = self.c_preobj[:, k] - ctr
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
        geo, best = cand.min(-1)
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

    def _contact_geom(self, env_ids, shape):
        """Candidate contacts of each env's object, scaled to its size (object frame)."""
        f = (self.bbox_env[env_ids, shape, 2:4] / self.c_bbox_nom[shape].clamp(min=1e-3)).clamp(0.5, 2.0)
        p = self.c_p[shape] * f.unsqueeze(1)
        nn = self.c_n[shape] / f.unsqueeze(1)
        nn = nn / torch.linalg.norm(nn, dim=-1, keepdim=True).clamp(min=1e-6)
        return p, nn, self.c_pre[shape] * f.unsqueeze(1), self.c_com[shape] * f, self.c_valid[shape], self.c_sep_ok[shape]

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

    def _pick_contacts(self, env_ids, shape, obj_heading, gdir, forced=None, forced_rule=None):
        """Per env: the two robots' contacts for this goal direction (object frame, scaled to the
        env's object size), their approach points and the centre of mass."""
        c, dev, m = self.cfg, self.device, len(env_ids)
        p, nn, pre, com, valid, sep = self._contact_geom(env_ids, shape)
        rel = gdir - obj_heading
        u = torch.stack([torch.cos(rel), torch.sin(rel)], -1)  # goal direction, object frame
        mix = torch.tensor(c.contact_mix, device=dev, dtype=torch.float)
        rule = torch.multinomial((mix / mix.sum()).expand(m, 3), 1).squeeze(-1)
        if forced_rule is not None:  # evaluation: this rule for every env (0 spread, 1 adjacent, 2 random)
            rule = forced_rule.to(dev).long()
        score, _, _, _ = self._pair_scores(p, nn, com, valid, sep, u, rule)
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
        ok_x = valid & (align >= lim) & sep[ar, :, keep_idx]
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
            sw = swap_d < keep_d
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
            lo, hi = self.cfg.reselect_s
            if hi > 0:
                self.c_reselect_t -= dt
                due = self.c_reselect_t <= 0.0
                if bool(due.any()):
                    ids = due.nonzero().flatten()
                    nd = len(ids)
                    self.c_reselect_t[ids] = lo + (hi - lo) * torch.rand(nd, device=self.device)
                    settled = self.c_engaged[ids].all(-1)  # nobody still on the way to a new contact
                    # close to the goal the direction to it is noise: keep the contacts there
                    far = torch.linalg.norm(self.goal_xy[ids] - self.box_pos()[ids, :2], dim=-1) > self.cfg.reselect_min_dist
                    self._reselect(ids[settled & far])
            # the approach potential's baseline for the next step (after resets and re-selections, so
            # a new contact or a new episode never pays for the jump)
            for k in range(len(AGENTS)):
                self.c_prev_phi[:, k] = self.contact_phi(k)

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
        cpose = None
        if c.contact_mode:
            forced = sc.get("contact_idx") if sc is not None else None
            forced_rule = sc.get("contact_rule") if sc is not None else None
            gdir_now = torch.atan2((goal_xy - obj_xy)[:, 1], (goal_xy - obj_xy)[:, 0])
            idx, cp, cn, cpre, ccom, rule = self._pick_contacts(env_ids, shape, obj_heading, gdir_now, forced, forced_rule)
            self.c_idx[env_ids], self.c_pobj[env_ids], self.c_nobj[env_ids] = idx, cp, cn
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
    # Stage 4 contact mode (see the module docstring)
    contact_mode: bool = False
    contact_mix: tuple[float, float, float] = (1.0, 1.0, 1.0)  # spread, adjacent, random pair
    contact_start_at: float = 0.7  # share of robots starting at the contact (the rest at its approach point)
    contact_min_sep: float = 0.85  # m between the two robots' standing points
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
    if not hasattr(g, "lvl_ema"):
        g.lvl_ema = 0.0
    if isinstance(env_ids, torch.Tensor) and len(env_ids) > 0:
        succ = g.metrics["success"][env_ids]
        ordinary = ~g.need_episode[env_ids]

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
