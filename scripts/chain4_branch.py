"""2 -> 3 and 3 -> 4 at the same decision time, on one system with four ANYmal C (docs/k_dispatch.md, "3 -> 4").

    python scripts/chain4_branch.py --masses 20,40,60,80,100 --seed 1001 --prefix k4-s1001
    python scripts/chain4_branch.py --masses 60,100 --reps 1 --prefix k4-check     # validation

The contact planner (expert rule 4 + the Stage 4 executor turn_debug/model_15000, start behind, 80 s) drives the pair
(robots 1, 2) from t = 0, exactly as in planner-bench. Robots 3 and 4 are scripted helpers
(quadcoop.contact_control.ContactController), parked and idle until added. An added helper appears --stage-dist m behind
the object, 0.8 m to the side away from the robots already there, and from then on all contacts are planned jointly:

    1 helper   helper_branch's joint trio search (summed per-contact score - time_weight x the slowest arrival -
               stop_weight per incumbent leaving a contact it pushes on; keep / move one / move both all candidates)
    2 helpers  the same objective over joint quadruples: the pair's contacts over all K candidates, the helpers'
               over the top --prune contacts by per-contact score (bounded search: K^2 x M^2 per env)

Tree (every branch a full state copy, scripts/branch_help.clone_envs):

    t1: k2 --+-- (keep) k2 ------ t2 --+-- (keep) k2      leaf "k2"   (the pair)
             |                         +-- (add)  k3b     leaf "k3b"  (robot 3 at t2: a 2 -> 3 decision at t2)
             +-- (add)  k3 ------ t2 --+-- (keep) k3      leaf "k3"   (robot 3 at t1)
                                       +-- (add)  k4      leaf "k4"   (robot 4 at t2: a 3 -> 4 decision at t2)
    nulls: k2null = k2 copied at t2 (stays 2); k3null = k3 copied at t2 (stays 3)

So both transitions are decided at the same time (t2, 60 s left) from a team that has had its size since t1 (2 -> 3)
or since t1 with the pair since 0 (3 -> 4). Logged at each decision (f1_*, f2_*): the chain_branch features plus
team-size-invariant ones: k, the fraction of present robots pressing, force per robot, and whether the next helper
has a useful unoccupied contact (n_free, free_best: contacts compatible with every current contact, never against the
wanted motion, and the best per-contact score among them).

Validation output (per twin): per-robot pressing fraction after it is added, falls, the joint search's call count,
mean runtime and feasible-assignment rate for 1 and 2 helpers.
Output: logs/evals/<prefix>/ (episodes.csv, planner.json, summary.md / json).
"""

from __future__ import annotations

import argparse
import csv
import gc
import json
import math
import os
import random
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT))

SCENARIOS = (("A_straight", 3.0, 0.0, 0.0), ("B_left", 3.0, 60.0, 30.0), ("C_backright", 3.0, -135.0, -60.0),
             ("D_far_turn", 5.0, 0.0, 90.0))
TEN = "cube,long,sphere,cylinder,arch,dumbbell,t_shape,l_shape,u_channel,plus"
ARMS_STD = ("k2", "k2null", "k3b", "k3", "k3null", "k4")
LEAVES_STD = ("k2", "k3b", "k3", "k4")
ROBOTS_STD = {"k2": 2, "k2null": 2, "k3b": 3, "k3": 3, "k3null": 3, "k4": 4}
BLIND = ("t", "d", "e_deg", "d0", "speed", "yawrate", "prog_rate", "force", "stall_s", "on1", "on2", "on3", "on4")
INV = ("k", "frac_press", "force_per", "n_free", "free_best")
AWARE = ("mass", "strength", "need_more")
D_AT = (30, 40, 50, 60)  # position error logged at these times (s)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--checkpoint", default="logs/keep/marl2/turn_debug/model_15000.pt")
    ap.add_argument("--objects", default=TEN)
    ap.add_argument("--masses", default="20,40,60,80,100")
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--seed", type=int, default=1001)
    ap.add_argument("--horizon", type=float, default=80.0)
    ap.add_argument("--t1", type=float, default=8.0, help="first decision (s): add robot 3?")
    ap.add_argument("--t2", type=float, default=20.0, help="second decision (s): add the next robot?")
    ap.add_argument("--stage-dist", type=float, default=3.0)
    ap.add_argument("--push-force", type=float, default=160.0)
    ap.add_argument("--slow-min-s", type=float, default=1.0)
    ap.add_argument("--prune", type=int, default=8, help="helpers' candidate contacts in the joint quadruple search")
    ap.add_argument("--withdraw", default="", help="diagnostic tree (docs/k_dispatch.md, step 1): comma list of radii (m); "
                    "arm k4w<cm> = robot 4 joins at t2 and withdraws once the position error first drops below the radius")
    ap.add_argument("--region", type=float, default=0.5, help="near-goal region (position error, m) for t_region")
    ap.add_argument("--release-dist", type=float, default=1.5, help="withdrawn helper released this far beyond the radius")
    ap.add_argument("--prefix", default="k4chain")
    ap.add_argument("--device", default=None)
    a = ap.parse_args()
    assert a.t2 > a.t1 > 0
    WD = [float(x) for x in a.withdraw.split(",") if x.strip()]
    WARMS = tuple(f"k4w{round(100 * x)}" for x in WD)
    if WD:  # diagnostic tree: k2 is only the root; the 3 -> 4 leaves are k3, k4 and the withdrawing k4w arms
        ARMS = ("k2", "k3", "k3null", "k4") + WARMS
        LEAVES = ("k3", "k4") + WARMS
    else:
        ARMS, LEAVES = ARMS_STD, LEAVES_STD
    ROBOTS_OF = {**ROBOTS_STD, **{w: 4 for w in WARMS}}

    os.environ["QUADCOOP_PAIR"] = "anymal4"
    os.environ["QUADCOOP_HELPER"] = "1"
    from train_coop2 import resolve_models, set_env

    set_env(resolve_models("b", "anymal4"))
    import numpy as np
    import torch
    from tensordict import TensorDict

    import quadcoop  # noqa: F401
    from mjlab.envs import ManagerBasedRlEnv
    from mjlab.utils.lab_api.math import quat_from_euler_xyz

    from branch_help import clone_envs
    from quadcoop import falls
    from quadcoop.contact_control import IDLE_ACTION, VX, VY, ContactController, to_action
    from quadcoop.coop2 import mdp as cm
    from quadcoop.coop2.env_cfg import SPECS, make_coop2_env_cfg
    from quadcoop.coop2.marl import actor_groups, actor_state, make_model
    from quadcoop.coop2.mdp import AGENTS, PLAN
    from quadcoop.stage1.mdp import wrap, yaw_of
    from quadcoop.stage1b import mdp as hb
    from quadcoop.stage1b.shapes import NOMINAL_MASS
    from quadcoop.stage2 import mdp as m2
    from quadcoop.stage2.shapes import OBJ_NAMES2, SHAPE_NAMES2, SHAPES2

    assert len(AGENTS) == 4, AGENTS
    HS = AGENTS[2:]
    device = a.device or ("cuda:0" if torch.cuda.is_available() else "cpu")
    ck = torch.load(a.checkpoint, map_location="cpu", weights_only=False)
    ck_cfg = ck.get("cfg", {})
    objects = [o.strip() for o in a.objects.split(",")]
    masses = [float(x) for x in a.masses.split(",")]
    out = ROOT / "logs" / "evals" / a.prefix
    out.mkdir(parents=True, exist_ok=True)

    base_cases = [(o, s, r) for o in objects for s in range(len(SCENARIOS)) for r in range(a.reps)]
    rng = random.Random(f"{a.seed}-coop2")
    jit_b = [[rng.uniform(-10, 10) for _ in range(2)] for _ in base_cases]
    gap_b = [[rng.uniform(0.3, 0.6) for _ in range(2)] for _ in base_cases]
    cases = [(arm, o, s, r, k) for arm in ARMS for k, (o, s, r) in enumerate(base_cases)]
    n = len(cases)
    print(f"K4-chain: {len(base_cases)} tasks x {len(ARMS)} twins = {n} envs per mass; masses {masses}; "
          f"decisions at {a.t1:g} s and {a.t2:g} s", flush=True)
    rows = []
    plan_stats = {}
    t_start = time.time()
    rs = ck_cfg.get("reselect_s", (3.0, 6.0))

    def run_mass(mass):  # one function call per mass, so its GPU state is freed before the next mass is built
        cfg = make_coop2_env_cfg(
            "b", play=True, helper=True, partner_map=bool(ck_cfg.get("partner_map", False)),
            reward_set=ck_cfg.get("reward_set", "r7"), contacts=True, tol_levels=tuple(tuple(x) for x in ck_cfg.get("tol_levels", ())),
            drift_dist=float(ck_cfg.get("drift_dist", 0.35)), drift_heading_deg=float(ck_cfg.get("drift_heading_deg", 45.0)),
            reselect_s=(float(rs[0]), float(rs[-1])), guide=bool(ck_cfg.get("guide", False)),
            off_contact=ck_cfg.get("off_contact", "soft") if ck_cfg.get("guide") else "soft", push_sensors=True,
            push_cmd=bool(ck_cfg.get("push_cmd", False)), wrench=True, walk_cost=float(ck_cfg.get("walk_cost", 0.3)),
            reselect_min_dist=float(ck_cfg.get("reselect_min_dist", 0.15)), expert=True,
            exec_v2=bool(ck_cfg.get("exec_v2", False)), effort=bool(ck_cfg.get("effort", False)),
            contact_sense=bool(ck_cfg.get("contact_sense", False)))
        cfg.scene.num_envs = n
        cfg.episode_length_s = 1e5
        cfg.terminations = {}
        cfg.commands["goal"].robot_push_force = a.push_force
        alpha = 0.5 * math.log(mass / NOMINAL_MASS)
        for name in OBJ_NAMES2:
            cfg.events[f"{name}_mass"].params["alpha_range"] = (alpha, alpha)
        torch.manual_seed(a.seed)
        base = ManagerBasedRlEnv(cfg=cfg, device=device)
        g = base.command_manager.get_term("goal")
        dev = base.device
        ids = torch.arange(n, device=dev)
        for k in range(len(SHAPES2)):
            m2.apply_geometry(base, ids, k, torch.ones(n, 3, device=dev))
        idx_of = {tw: torch.tensor([j for j, c in enumerate(cases) if c[0] == tw], device=dev) for tw in ARMS}
        g.c_cap_mult[:] = 1.0

        obj_idx = torch.tensor([SHAPE_NAMES2.index(o) for _, o, _, _, _ in cases], device=dev)
        dist = torch.tensor([SCENARIOS[s][1] for _, _, s, _, _ in cases], device=dev)
        gdir = torch.deg2rad(torch.tensor([SCENARIOS[s][2] for _, _, s, _, _ in cases], device=dev))
        turn = torch.deg2rad(torch.tensor([SCENARIOS[s][3] for _, _, s, _, _ in cases], device=dev))
        sym = g.sym[obj_idx]
        capy = torch.where(sym > 0, (math.pi / sym.clamp(min=1)) * g.cfg.max_yaw_frac_of_symmetry, torch.zeros_like(sym))
        turn = torch.sign(turn) * torch.minimum(turn.abs(), capy)
        jit = torch.tensor([jit_b[k] for *_, k in cases], device=dev)
        gap = torch.tensor([gap_b[k] for *_, k in cases], device=dev)
        bearings = [math.pi + torch.deg2rad(sgn * 35.0 + jit[:, i]) for i, sgn in enumerate((-1.0, 1.0))]
        bearings += [torch.full((n,), math.pi, device=dev), torch.full((n,), math.pi, device=dev)]
        z = torch.zeros(n, device=dev)
        T_ = torch.ones(n, dtype=torch.bool, device=dev)
        F_ = torch.zeros(n, dtype=torch.bool, device=dev)
        sc = {"shape": obj_idx, "obj_xy_rel": torch.zeros(n, 2, device=dev), "obj_heading": z.clone(),
              "goal_xy_rel": dist.unsqueeze(-1) * torch.stack([torch.cos(gdir), torch.sin(gdir)], -1),
              "goal_yaw": wrap(turn), "bearings": bearings,
              "gaps": [gap[:, 0], gap[:, 1], torch.full((n,), 1.2, device=dev), torch.full((n,), 1.2, device=dev)],
              "yaw_noise": [z, z, z, z], "park": [F_, F_, T_, T_],
              "contact_rule": torch.full((n,), 4, dtype=torch.long, device=dev),
              "contact_idx": torch.full((n, 2), -1, dtype=torch.long, device=dev),
              "start_behind": torch.ones(n, dtype=torch.bool, device=dev)}
        g.scenario = lambda env_ids: {k: ([x[env_ids] for x in v] if isinstance(v, list) else v[env_ids])
                                      for k, v in sc.items()}
        obs, _ = base.reset()
        g.scenario = None
        g.cfg.expert_first_only = False
        g.cfg.slow_min_s = a.slow_min_s
        obs = TensorDict({k: v for k, v in obs.items() if not k.startswith("walker_")}, batch_size=[n])
        actors = {}
        for ag in PLAN:
            m_ = make_model(obs, actor_groups(ag, "b"), 3, (256, 128, 64), "b", True).to(dev)
            m_.load_state_dict(actor_state(ck["actors"], ag))
            actors[ag] = m_.eval()
        robots = [base.scene[ag] for ag in AGENTS]
        ctrls = [ContactController(n, dev, reach=SPECS[h].half_length) for h in HS]
        idle = torch.tensor(IDLE_ACTION, device=dev)
        radius = g.radius_env[ids, obj_idx]

        nanv = lambda: torch.full((n,), float("nan"), device=dev)  # noqa: E731
        zf = lambda: torch.zeros(n, device=dev)  # noqa: E731
        zb = lambda: torch.zeros(n, dtype=torch.bool, device=dev)  # noqa: E731
        z2 = lambda: torch.zeros(n, 2, device=dev)  # noqa: E731
        S = {"done": zb(), "hold": zf(), "t_succ": nanv(), "nh": torch.zeros(n, dtype=torch.long, device=dev),
             "t_add3": nanv(), "t_add4": nanv(), "touch_t": zf(), "live_t": zf(), "robot_s": zf(),
             "last_d": g.errors()[0].clone(), "last_e": zf(),
             "ema_v": zf(), "ema_w": zf(), "ema_p": zf(), "ema_f": zf(), "best_d": g.errors()[0].clone(), "stall": zf(),
             "prev_xy": g.box_pos()[:, :2].clone(), "prev_yaw": g.contact_frame_yaw().clone(), "prev_d": g.errors()[0].clone()}
        for q in range(4):
            S[f"fell{q}"], S[f"tf{q}"], S[f"press_t{q}"], S[f"pres_t{q}"] = zb(), nanv(), zf(), zf()
            S[f"sw{q}"] = zf()  # contact switches from t2 on (robot q + 1)
        for j in range(2):
            S[f"h_on{j}"], S[f"h_has{j}"], S[f"h_arr{j}"] = zb(), zb(), nanv()
            S[f"h_p{j}"], S[f"h_n{j}"], S[f"h_pre{j}"] = z2(), z2(), z2()
            S[f"h_idx{j}"] = torch.full((n,), -1, dtype=torch.long, device=dev)
            S[f"ph{j}"] = zb()
        S["wd"], S["rel"], S["t_wd"], S["t_rel"] = zb(), zb(), nanv(), nanv()  # robot 4 withdrawn / released
        S["t_reg"], S["h4_s"] = nanv(), zf()
        for tt in D_AT:
            S[f"d{tt}"] = nanv()
        rw = torch.full((n,), -1.0, device=dev)  # withdrawal radius per env (-1: never)
        for w_, x_ in zip(WARMS, WD):
            rw[idx_of[w_]] = x_
        d0 = g.errors()[0].clone()
        how = [""] * n
        feats = {1: None, 2: None}
        st_ = {1: {"calls": 0, "envs": 0, "feasible": 0, "sec": 0.0}, 2: {"calls": 0, "envs": 0, "feasible": 0, "sec": 0.0}}

        def present():
            return [torch.ones(n, dtype=torch.bool, device=dev), torch.ones(n, dtype=torch.bool, device=dev),
                    S["nh"] >= 1, (S["nh"] >= 2) | (S["wd"] & ~S["rel"])]

        def pressing():
            return [g.on_contact(0), g.on_contact(1), S["ph0"] & (S["nh"] >= 1), S["ph1"] & (S["nh"] >= 2)]

        def contact_scores(e_, p, nn):
            yaw = g.contact_frame_yaw()[e_]
            cs, sn = torch.cos(yaw), torch.sin(yaw)
            vw = g.c_vdes[e_]
            v_o = torch.stack([cs * vw[:, 0] + sn * vw[:, 1], -sn * vw[:, 0] + cs * vw[:, 1]], -1)
            wz, cg = g.c_wdes[e_], g.c_cg[e_]
            vn = torch.linalg.norm(v_o, dim=-1, keepdim=True)
            u = v_o / vn.clamp(min=1e-6)
            f = -nn
            along = (f * u.unsqueeze(1)).sum(-1) * (vn > 1e-3).float()
            r = p - g.c_cof[e_].unsqueeze(1)
            tau = (r[..., 0] * f[..., 1] - r[..., 1] * f[..., 0]) / cg.unsqueeze(-1)
            tfrac = ((cg * wz).abs() / ((cg * wz).abs() + vn.squeeze(-1)).clamp(min=1e-6)).unsqueeze(-1)
            return along + tfrac * torch.sign(wz).unsqueeze(-1) * tau - 0.3 * (1.0 - tfrac) * tau.abs(), along > -0.2

        def free_contacts():
            """For the next helper: contacts compatible with every current contact, not against the wanted motion."""
            p, nn, _, _, valid, sep = g._contact_geom(ids, g.shape[ids])
            sc_, ok_ = contact_scores(ids, p, nn)
            K = p.shape[1]
            ar = torch.arange(n, device=dev)
            ok = ok_ & valid
            used = [g.c_idx[:, 0], g.c_idx[:, 1]] + [S[f"h_idx{j}"] for j in range(2)]
            act = [torch.ones(n, dtype=torch.bool, device=dev)] * 2 + [S["nh"] >= 1, S["nh"] >= 2]
            for u_, on_ in zip(used, act):
                good = on_ & (u_ >= 0)
                ok &= ~good.unsqueeze(-1) | sep[ar, u_.clamp(min=0, max=K - 1)]
            best = torch.where(ok, sc_, torch.full_like(sc_, -1e9)).max(-1).values
            return ok.float().sum(-1), torch.where(best > -1e8, best, torch.zeros_like(best))

        def snapshot():
            d_, e_ = g.errors()
            e_ = torch.where(g.symmetry() > 0, e_, torch.zeros_like(e_))
            pr, ps = pressing(), present()
            k_ = sum(x.float() for x in ps)
            nf, fb = free_contacts()
            return {"t": torch.full((n,), t, device=dev), "d": d_.clone(), "e_deg": torch.rad2deg(e_.abs()),
                    "d0": d0.clone(), "speed": S["ema_v"].clone(), "yawrate": S["ema_w"].clone(),
                    "prog_rate": S["ema_p"].clone(), "force": S["ema_f"].clone(), "stall_s": S["stall"].clone(),
                    **{f"on{q + 1}": (pr[q] & ps[q]).float() for q in range(4)},
                    "k": k_, "frac_press": sum((pr[q] & ps[q]).float() for q in range(4)) / k_, "force_per": S["ema_f"] / k_,
                    "n_free": nf, "free_best": fb,
                    "mass": torch.full((n,), mass, device=dev), "strength": g.current_strength().clamp(max=1e3),
                    "need_more": g.c_need_more.float().clone(), "done": S["done"].clone()}

        def branch(src_arm, dst_arms):
            src = idx_of[src_arm]
            cnt = 0
            for tw in dst_arms:
                dst = idx_of[tw]
                cnt = clone_envs(base, obs, src, dst)
                for v in S.values():
                    v[dst] = v[src]
                for fd in feats.values():
                    if fd is not None:
                        for v in fd.values():
                            v[dst] = v[src]
                for jj, kk in zip(dst.tolist(), src.tolist()):
                    how[jj] = how[kk]
                for cc in ctrls:
                    for v in vars(cc).values():
                        if torch.is_tensor(v) and v.ndim >= 1 and v.shape[0] == n:
                            v[dst] = v[src]
            return cnt

        def stage(robot, e_, others):
            bp = g.box_pos()[e_, :2]
            u = g.goal_xy[e_] - bp
            u = u / torch.linalg.norm(u, dim=-1, keepdim=True).clamp(min=1e-6)
            lat = torch.stack([-u[:, 1], u[:, 0]], -1)
            cen = sum(robots[k].data.root_link_pos_w[e_, :2] for k in others) / len(others) - bp
            side = torch.where((cen * lat).sum(-1) >= 0, -1.0, 1.0).unsqueeze(-1)
            pos = bp - a.stage_dist * u + 0.8 * side * lat
            yw = torch.atan2(bp[:, 1] - pos[:, 1], bp[:, 0] - pos[:, 0])
            st = torch.zeros(len(e_), 13, device=dev)
            st[:, :2] = pos
            st[:, 2] = robot.data.root_link_pos_w[e_, 2]
            zz = torch.zeros(len(e_), device=dev)
            st[:, 3:7] = quat_from_euler_xyz(zz, zz, yw)
            robot.write_root_state_to_sim(st, e_)

        def joint_decide(e_, nh):
            """All contacts together for the pair + nh helpers (1: full trio search; 2: bounded quadruple search)."""
            if len(e_) == 0:
                return
            t_c = time.time()
            c_ = g.cfg
            prop = g._propose_expert(e_)
            p, nn, pre, use, cur = prop["p"], prop["nn"], prop["pre"], prop["use"], prop["cur"]
            m_, K = p.shape[0], p.shape[1]
            ar = torch.arange(m_, device=dev)
            _, _, _, _, valid, sep = g._contact_geom(e_, g.shape[e_])
            sc_, ok_ = contact_scores(e_, p, nn)
            ok_ = ok_ & valid
            t1_, t2_ = prop["t_route"]
            yw = g.contact_frame_yaw()[e_]
            cs, sn = torch.cos(yw), torch.sin(yw)
            pw = g.box_pos()[e_, :2].unsqueeze(1) + torch.stack([cs.unsqueeze(1) * pre[..., 0] - sn.unsqueeze(1) * pre[..., 1],
                                                                  sn.unsqueeze(1) * pre[..., 0] + cs.unsqueeze(1) * pre[..., 1]], -1)
            th = [1.3 * torch.linalg.norm(pw - robots[2 + j].data.root_link_pos_w[e_, :2].unsqueeze(1), dim=-1) / c_.walk_speed
                  for j in range(nh)]
            on = prop["on"]
            kk = torch.arange(K, device=dev)
            stop1 = ((kk.unsqueeze(0) != cur[:, :1]) & on[:, :1]).float()
            stop2 = ((kk.unsqueeze(0) != cur[:, 1:2]) & on[:, 1:2]).float()
            pair_t = torch.maximum(t1_[:, :, None], t2_[:, None, :])  # (m, K, K)
            pair_sc = sc_[:, :, None] + sc_[:, None, :] - c_.stop_weight * (stop1[:, :, None] + stop2[:, None, :])
            pair_ok = use & ok_[:, :, None] & ok_[:, None, :] & (kk[:, None] != kk[None, :]).unsqueeze(0)
            if nh == 1:
                Tm = (pair_sc[..., None] + sc_[:, None, None, :]
                      - c_.time_weight * torch.maximum(pair_t[..., None], th[0][:, None, None, :]))
                feas = (pair_ok[..., None] & sep[:, :, None, :] & sep[:, None, :, :] & ok_[:, None, None, :]
                        & (kk[:, None, None] != kk[None, None, :]).unsqueeze(0) & (kk[None, :, None] != kk[None, None, :]).unsqueeze(0))
                Tm = torch.where(feas, Tm, torch.full_like(Tm, -1e9))
                best, flat = Tm.view(m_, -1).max(-1)
                ia, ib, hc = flat // (K * K), (flat // K) % K, [flat % K]
            else:
                M = min(a.prune, K)
                # the top M contacts by score, always including each present helper's current (still valid) contact,
                # so the bounded search never evicts a helper from a contact it is pushing at (the trio search, over
                # all K contacts, can always keep it)
                rank = torch.where(ok_, sc_, torch.full_like(sc_, -1e9))
                for j in range(nh):
                    hc0 = S[f"h_idx{j}"][e_]
                    kp = (hc0 >= 0) & ok_[ar, hc0.clamp(min=0)]
                    rank[ar[kp], hc0[kp]] += 1e6
                cand = rank.topk(M, -1).indices  # (m, M)
                cok = ok_.gather(1, cand)
                csc = sc_.gather(1, cand)
                ct = [x.gather(1, cand) for x in th]
                sepPC = sep.gather(2, cand.unsqueeze(1).expand(m_, K, M))  # (m, K, M): pair contact vs candidate
                sepCC = sep[ar[:, None, None], cand[:, :, None], cand[:, None, :]]  # (m, M, M)
                dPC = kk.view(1, K, 1) != cand.unsqueeze(1)
                dCC = cand[:, :, None] != cand[:, None, :]
                Tm = (pair_sc[:, :, :, None, None] + csc[:, None, None, :, None] + csc[:, None, None, None, :]
                      - c_.time_weight * torch.maximum(torch.maximum(pair_t[:, :, :, None, None], ct[0][:, None, None, :, None]),
                                                       ct[1][:, None, None, None, :]))
                hok = (sepPC & dPC)  # (m, K, M)
                feas = (pair_ok[:, :, :, None, None]
                        & hok[:, :, None, :, None] & hok[:, None, :, :, None] & hok[:, :, None, None, :] & hok[:, None, :, None, :]
                        & (sepCC & dCC)[:, None, None, :, :] & cok[:, None, None, :, None] & cok[:, None, None, None, :])
                Tm = torch.where(feas, Tm, torch.full_like(Tm, -1e9))
                best, flat = Tm.view(m_, -1).max(-1)
                ia, ib = flat // (K * M * M), (flat // (M * M)) % K
                hc = [cand[ar, (flat // M) % M], cand[ar, flat % M]]
            has = best > -1e8
            new = torch.where(has.unsqueeze(-1), torch.stack([ia, ib], -1), cur)
            post = t >= a.t2 - 1e-6
            for q in range(2):
                S[f"sw{q}"][e_] += (has & (new[:, q] != cur[:, q]) & post).float()
            g.c_need_more[e_] = prop["need_more"]
            g.apply_assignment(e_, new, p, nn, pre, prop["t_route"])
            for j, ic in enumerate(hc):
                changed = has & (ic != S[f"h_idx{j}"][e_])
                S[f"sw{2 + j}"][e_] += (changed & (S[f"h_idx{j}"][e_] >= 0) & post).float()
                S[f"h_idx{j}"][e_] = torch.where(has, ic, S[f"h_idx{j}"][e_])
                for key, src_ in (("h_p", p), ("h_n", nn), ("h_pre", pre)):
                    S[f"{key}{j}"][e_] = torch.where(has.unsqueeze(-1), src_[ar, ic], S[f"{key}{j}"][e_])
                S[f"h_has{j}"][e_] = has | S[f"h_has{j}"][e_]
                if bool(changed.any()):
                    ctrls[j].reset(torch.zeros(n, dtype=torch.bool, device=dev).index_fill_(0, e_[changed], True))
            if torch.cuda.is_available():
                torch.cuda.synchronize()
            st_[nh]["calls"] += 1
            st_[nh]["envs"] += m_
            st_[nh]["feasible"] += int(has.sum())
            st_[nh]["sec"] += time.time() - t_c

        def add_helper(arm, j):
            """Helper j (0: robot 3, 1: robot 4) joins in every live env of arm; returns how many were added."""
            e_ = idx_of[arm][~S["done"][idx_of[arm]]]
            if len(e_) == 0:
                return 0
            stage(robots[2 + j], e_, list(range(2 + j)))
            S["nh"][e_] = j + 1
            joint_decide(e_, j + 1)
            go = torch.zeros(n, dtype=torch.bool, device=dev).index_fill_(0, e_, True) & S[f"h_has{j}"]
            S[f"h_on{j}"] |= go
            S[f"t_add{3 + j}"] = torch.where(go, torch.full_like(S[f"t_add{3 + j}"], t), S[f"t_add{3 + j}"])
            ctrls[j].reset(go)
            return int(go.sum())

        class Coord:
            def __call__(self, g_, ids_):
                nh_ = S["nh"][ids_]
                for q in (1, 2):
                    joint_decide(ids_[nh_ == q], q)
                if bool((nh_ == 0).any()):
                    g_._reselect_expert(ids_[nh_ == 0])
        g.coordinator = Coord()

        dt = base.step_dt
        steps = int(a.horizon / dt)
        n1, n2 = int(round(a.t1 / dt)), int(round(a.t2 / dt))
        pt, yt = 0.10, math.radians(6.0)
        t0 = time.time()
        t = 0.0
        with torch.no_grad():
            for i in range(steps):
                t = i * dt
                if i == n1:
                    feats[1] = snapshot()
                    if WD:
                        c_ = branch("k2", [x for x in ARMS if x != "k2"])
                        na = sum(add_helper(tw, 0) for tw in ARMS if tw != "k2")
                    else:
                        c_ = branch("k2", ["k3", "k3null", "k4", "k2null", "k3b"])
                        na = sum(add_helper(tw, 0) for tw in ("k3", "k3null", "k4"))
                    print(f"  [{mass:g} kg] t1 {t:.1f} s ({c_} tensors per copy): "
                          f"{int(feats[1]['done'][idx_of['k2']].sum())}/{len(base_cases)} ended; robot 3 added in {na}", flush=True)
                if i == n2:
                    feats[2] = snapshot()
                    if WD:
                        branch("k3", ["k3null", "k4", *WARMS])
                        nb = 0
                        nc = sum(add_helper(tw, 1) for tw in ("k4", *WARMS))
                    else:
                        branch("k2", ["k2null", "k3b"])
                        branch("k3", ["k3null", "k4"])
                        nb = add_helper("k3b", 0)
                        nc = add_helper("k4", 1)
                    print(f"  [{mass:g} kg] t2 {t:.1f} s: robot 3 added in {nb} (k3b), robot 4 in {nc} (k4)", flush=True)
                if WD and i > n2:
                    w_ = (S["nh"] >= 2) & ~S["wd"] & ~S["done"] & (g.errors()[0] < rw)
                    if bool(w_.any()):
                        S["wd"] |= w_
                        S["t_wd"] = torch.where(w_, torch.full_like(S["t_wd"], t), S["t_wd"])
                        S["h_on1"] &= ~w_
                        S["nh"] = torch.where(w_, torch.ones_like(S["nh"]), S["nh"])
                        ctrls[1].reset(w_)
                        joint_decide(w_.nonzero().flatten(), 1)  # the trio re-plans at once
                live = ~S["done"]
                act = torch.cat([actors[ag](obs) for ag in PLAN], -1)
                _, e = g.errors()
                e = torch.where(g.symmetry() > 0, e, torch.zeros_like(e))
                acts = [act]
                for j, h in enumerate(HS):
                    hr = robots[2 + j]
                    hp = hr.data.root_link_pos_w[:, :2]
                    mates = torch.stack([robots[k].data.root_link_pos_w[:, :2] for k in range(4) if k != 2 + j], 1)
                    dm = torch.linalg.norm(mates - hp.unsqueeze(1), dim=-1)
                    near = mates[torch.arange(n, device=dev), dm.argmin(-1)]
                    act_h = S[f"h_on{j}"] & S[f"h_has{j}"] & live
                    tw_, ph = ctrls[j](hp, yaw_of(hr.data.root_link_quat_w), g.box_pos()[:, :2], g.contact_frame_yaw(), radius,
                                       S[f"h_p{j}"], S[f"h_n{j}"], g.c_cof, g.goal_xy, e, pre_obj=S[f"h_pre{j}"],
                                       partner_pos=near, active=act_h)
                    S[f"ph{j}"] = ph & act_h
                    a_h = torch.where(act_h.unsqueeze(-1), to_action(tw_), idle.expand(n, 3))
                    if WD and j == 1:  # withdrawn and not yet released: walk straight out, clear of teammates
                        ret = S["wd"] & ~S["rel"] & live
                        if bool(ret.any()):
                            out_ = hp - g.box_pos()[:, :2]
                            u_ = out_ / torch.linalg.norm(out_, dim=-1, keepdim=True).clamp(min=1e-3)
                            aw = hp - near
                            dn = torch.linalg.norm(aw, dim=-1, keepdim=True).clamp(min=1e-3)
                            v_w = 0.5 * u_ + torch.clamp(1.0 - dn / 1.2, min=0.0) * aw / dn
                            v_w = v_w * torch.clamp(0.6 / torch.linalg.norm(v_w, dim=-1, keepdim=True).clamp(min=1e-6), max=1.0)
                            yw4 = yaw_of(hr.data.root_link_quat_w)
                            c4, s4 = torch.cos(yw4), torch.sin(yw4)
                            tw_r = torch.stack([(c4 * v_w[:, 0] + s4 * v_w[:, 1]).clamp(*VX),
                                                (-s4 * v_w[:, 0] + c4 * v_w[:, 1]).clamp(*VY), torch.zeros_like(c4)], -1)
                            a_h = torch.where(ret.unsqueeze(-1), to_action(tw_r), a_h)
                    acts.append(a_h)
                o_, _, _, _, _ = base.step(torch.cat(acts, -1))
                obs = TensorDict({kk: v for kk, v in o_.items() if not kk.startswith("walker_")}, batch_size=[n])
                t = (i + 1) * dt
                pres, prs = present(), pressing()
                f_any = torch.zeros(n, dtype=torch.bool, device=dev)
                for k, ag in enumerate(AGENTS):
                    f_ = falls.fallen(base, asset_name=ag, nominal_height=SPECS[ag].nominal_height) & pres[k] & live
                    S[f"fell{k}"] |= f_
                    S[f"tf{k}"] = torch.where(f_ & torch.isnan(S[f"tf{k}"]), torch.full_like(S[f"tf{k}"], t), S[f"tf{k}"])
                    f_any |= f_
                tip = hb.box_tipped(base) & live & ~f_any
                lost = cm.box_lost(base) & live & ~f_any & ~tip
                d, e2 = g.errors()
                ok = live & ~f_any & ~tip & ~lost
                S["last_d"] = torch.where(ok, d, S["last_d"])
                S["last_e"] = torch.where(ok, e2.abs(), S["last_e"])
                inside = ok & (d < pt) & (e2.abs() < yt)
                S["hold"] = torch.where(inside, S["hold"] + dt, torch.zeros_like(S["hold"]))
                succ = ok & (S["hold"] >= 1.0)
                S["t_succ"] = torch.where(succ, torch.full_like(S["t_succ"], t), S["t_succ"])
                xy, yw_ = g.box_pos()[:, :2], g.contact_frame_yaw()
                al = dt / 2.0
                S["ema_v"] += al * (torch.linalg.norm(xy - S["prev_xy"], dim=-1) / dt - S["ema_v"])
                S["ema_w"] += al * (wrap(yw_ - S["prev_yaw"]).abs() / dt - S["ema_w"])
                S["ema_p"] += al * ((S["prev_d"] - d) / dt - S["ema_p"])
                fsum = sum(torch.linalg.norm(cm.object_force_from(base, ag), dim=-1) * pres[k].float()
                           for k, ag in enumerate(AGENTS))
                S["ema_f"] += al * (fsum - S["ema_f"])
                S["prev_xy"], S["prev_yaw"], S["prev_d"] = xy.clone(), yw_.clone(), d.clone()
                better = d < S["best_d"] - 0.05
                S["best_d"] = torch.where(better, d, S["best_d"])
                S["stall"] = torch.where(better, torch.zeros_like(S["stall"]), S["stall"] + dt)
                for j in range(2):
                    arr = S[f"ph{j}"] & ok
                    S[f"h_arr{j}"] = torch.where(arr & torch.isnan(S[f"h_arr{j}"]), torch.full_like(S[f"h_arr{j}"], t),
                                                 S[f"h_arr{j}"])
                for q in range(4):
                    S[f"pres_t{q}"] += (pres[q] & ok).float() * dt
                    S[f"press_t{q}"] += (prs[q] & pres[q] & ok).float() * dt
                S["touch_t"] += (cm.robots_touching(base) > 0).float() * ok.float() * dt
                S["live_t"] += ok.float() * dt
                S["h4_s"] += (pres[3] & ok).float() * dt
                reg = ok & (d < a.region) & torch.isnan(S["t_reg"])
                S["t_reg"] = torch.where(reg, torch.full_like(S["t_reg"], t), S["t_reg"])
                for tt in D_AT:
                    if abs(t - tt) < dt / 2:
                        S[f"d{tt}"] = S["last_d"].clone()
                if WD:
                    dr = torch.linalg.norm(robots[3].data.root_link_pos_w[:, :2] - g.box_pos()[:, :2], dim=-1)
                    rl = S["wd"] & ~S["rel"] & ((dr >= radius + a.release_dist) | (t - S["t_wd"] >= 8.0) | S["done"])
                    S["rel"] |= rl
                    S["t_rel"] = torch.where(rl, torch.full_like(S["t_rel"], t), S["t_rel"])
                S["robot_s"] += ok.float() * dt * sum(p_.float() for p_ in pres)
                for j in f_any.nonzero().flatten().tolist():
                    how[j] = "fell_" + "+".join(ag for k, ag in enumerate(AGENTS) if bool(S[f"fell{k}"][j]))
                for j in tip.nonzero().flatten().tolist():
                    how[j] = "tipped"
                for j in lost.nonzero().flatten().tolist():
                    how[j] = "lost"
                for j in succ.nonzero().flatten().tolist():
                    how[j] = "success"
                S["done"] |= f_any | tip | lost | succ
                if i % 1000 == 0:
                    print(f"  [{mass:g} kg] step {i}/{steps}: live {int((~S['done']).sum())}/{n} ({time.time() - t0:.0f} s)",
                          flush=True)
                if i > n2 and bool(S["done"].all()):
                    break
        if feats[2] is None:
            feats[2] = snapshot()
        plan_stats[f"{mass:g}"] = {str(q): {**v, "ms_per_env": 1e3 * v["sec"] / max(v["envs"], 1),
                                            "feasible_rate": v["feasible"] / max(v["envs"], 1)} for q, v in st_.items()}
        print(f"  [{mass:g} kg] joint search: " + "; ".join(
            f"{q} helper(s) {v['calls']} calls, {v['envs']} env-decisions, {1e3 * v['sec'] / max(v['envs'], 1):.2f} ms/env, "
            f"feasible {100 * v['feasible'] / max(v['envs'], 1):.0f}%" for q, v in st_.items()), flush=True)
        for j, (arm, o, s, r, k) in enumerate(cases):
            fv = lambda q, key: round(float(feats[q][key][j]), 4)  # noqa: E731
            nanr = lambda x: "" if math.isnan(float(x)) else round(float(x), 2)  # noqa: E731
            rows.append({"arm": arm, "object": o, "mass": mass, "scenario": SCENARIOS[s][0], "rep": r, "task": k,
                         "success": int(how[j] == "success"), "outcome": how[j] or "horizon",
                         "t_success": nanr(S["t_succ"][j]), "final_pos_err": round(float(S["last_d"][j]), 3),
                         "robots": ROBOTS_OF[arm], "robot_s": round(float(S["robot_s"][j]), 1),
                         "t_add3": nanr(S["t_add3"][j]), "t_add4": nanr(S["t_add4"][j]),
                         "arrive3": nanr(S["h_arr0"][j]), "arrive4": nanr(S["h_arr1"][j]),
                         **{f"press_frac{q + 1}": (round(float(S[f"press_t{q}"][j] / S[f"pres_t{q}"][j]), 3)
                                                   if float(S[f"pres_t{q}"][j]) > 0 else "") for q in range(4)},
                         **{f"fell_{ag}": int(bool(S[f"fell{q}"][j])) for q, ag in enumerate(AGENTS)},
                         **{f"switches{q + 1}": int(S[f"sw{q}"][j]) for q in range(4)},
                         **{f"t_fall_{ag}": nanr(S[f"tf{q}"][j]) for q, ag in enumerate(AGENTS)},
                         "robots_touch_frac": round(float(S["touch_t"][j] / S["live_t"][j].clamp(min=1e-6)), 3),
                         "t_region": nanr(S["t_reg"][j]), "helper4_s": round(float(S["h4_s"][j]), 1),
                         "t_withdraw": nanr(S["t_wd"][j]), "t_release": nanr(S["t_rel"][j]),
                         **{f"d{tt}": nanr(S[f"d{tt}"][j]) for tt in D_AT},
                         "ended_t1": int(bool(feats[1]["done"][j])), "ended_t2": int(bool(feats[2]["done"][j])),
                         **{f"f1_{key}": fv(1, key) for key in BLIND + INV + AWARE},
                         **{f"f2_{key}": fv(2, key) for key in BLIND + INV + AWARE}})
        sel = [x for x in rows if x["mass"] == mass]
        print(f"[{mass:g} kg] " + "  ".join(f"{arm} {sum(x['success'] for x in sel if x['arm'] == arm)}/"
                                          f"{sum(1 for x in sel if x['arm'] == arm)}" for arm in ARMS)
              + f"  ({time.time() - t_start:.0f} s)", flush=True)
        base.close()
        del base

    def dump():
        with open(out / "episodes.csv", "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        (out / "planner.json").write_text(json.dumps(plan_stats, indent=1))

    for mass in masses:
        run_mass(mass)
        gc.collect()
        torch.cuda.empty_cache()
        dump()  # after every mass, so a later failure keeps the finished masses
        free, total = torch.cuda.mem_get_info()
        print(f"[{mass:g} kg] GPU after release: {(total - free) / 2**30:.1f} of {total / 2**30:.0f} GiB in use", flush=True)

    brng = np.random.default_rng(0)
    key = lambda r_: (r_["object"], r_["mass"], r_["scenario"], r_["rep"])  # noqa: E731
    by = {tw: {key(r_): r_ for r_ in rows if r_["arm"] == tw} for tw in ARMS}

    def ci(v):
        v = np.asarray(v, dtype=float)
        bs = v[brng.integers(0, len(v), (2000, len(v)))].mean(1)
        return 100 * v.mean(), 100 * np.percentile(bs, 2.5), 100 * np.percentile(bs, 97.5)
    PAIRS = ([("k4", "k3"), *((w, "k3") for w in WARMS), ("k3null", "k3")] if WD else
             [("k3b", "k2"), ("k2null", "k2"), ("k4", "k3"), ("k3null", "k3")])
    md = [f"# 2 -> 3 and 3 -> 4 tree: {a.prefix}", "",
          f"Seed {a.seed}, {len(base_cases)} tasks per mass; robot 3 at {a.t1:g} s (k3) or {a.t2:g} s (k3b); robot 4 at "
          f"{a.t2:g} s after robot 3 at {a.t1:g} s (k4). Success over all starts. Nets in pp, 95% paired bootstrap.", "",
          "| mass | " + " | ".join(LEAVES) + " | " + " | ".join(f"{x}-{b}" for x, b in PAIRS)
          + " | press frac robot 3 / 4 (k4) | falls (k4) |",
          "|---|" + "---|" * (len(LEAVES) + len(PAIRS) + 2)]
    summ = {"seed": a.seed, "t1": a.t1, "t2": a.t2, "planner": plan_stats, "by_mass": {}}
    for m in masses + ["all"]:
        ks = [k_ for k_, r_ in by["k2"].items() if m == "all" or r_["mass"] == m]
        y = {tw: np.array([by[tw][k_]["success"] for k_ in ks], dtype=float) for tw in ARMS}
        diffs = {f"{x}-{b}": ci(y[x] - y[b]) for x, b in PAIRS}
        pf = [np.mean([float(by["k4"][k_][f"press_frac{q}"]) for k_ in ks if by["k4"][k_][f"press_frac{q}"] != ""] or [np.nan])
              for q in (3, 4)]
        fl = np.mean([any(by["k4"][k_][f"fell_{ag}"] for ag in AGENTS) for k_ in ks])
        summ["by_mass"][str(m)] = {"success": {tw: 100 * float(y[tw].mean()) for tw in ARMS},
                                   "net": {k_: list(v) for k_, v in diffs.items()}, "press_frac": pf, "falls_k4": float(fl)}
        md.append(f"| {m if m == 'all' else f'{m:g}'} | " + " | ".join(f"{100 * y[tw].mean():.0f}%" for tw in LEAVES) + " | "
                  + " | ".join(f"{v[0]:+.1f} [{v[1]:+.0f}, {v[2]:+.0f}]" for v in diffs.values())
                  + f" | {pf[0]:.2f} / {pf[1]:.2f} | {100 * fl:.0f}% |")
    (out / "summary.md").write_text("\n".join(md) + "\n")
    (out / "summary.json").write_text(json.dumps(summ, indent=1))
    print("\n".join(md))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
