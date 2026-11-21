"""K -> K+1 on one system: start with one robot and decide twice whether to add another (docs/k_dispatch.md).

    python scripts/chain_branch.py --masses 20,40,60,80,100 --seed 1001 --prefix kc-s1001

The contact planner (expert rule 4 + the Stage 4 executor turn_debug/model_15000, start behind, 80 s) with three
ANYmal C (QUADCOOP_PAIR=anymal3). Robot 1 starts alone: robot 2 is parked (out of the push group, idle) and robot 3
(the scripted helper of helper_branch.py) parked too. Two decision times, --t1 and --t2; each task runs in a tree of
twins, every branch a full state copy (scripts/branch_help.clone_envs):

    t1: k1 --+-- (wait)  k1 ------- t2 --+-- (wait) k1        leaf "k1"   (1 robot)
             |                           +-- (add)  k2b       leaf "k2b"  (robot 2 added at t2)
             +-- (add)   k2a ------ t2 --+-- (wait) k2a       leaf "k2a"  (robot 2 added at t1)
                                         +-- (add)  k3        leaf "k3"   (robot 2 at t1, helper at t2)
    nulls: k1null = k1 copied at t1 (stays 1); k2null = k2a copied at t2 (stays 2)

An added robot appears --stage-dist m behind the object (w.r.t. the goal), 0.8 m to the side away from the robots
already there. Robot 2 joins the planner's pair (its contact re-planned at once); robot 3 is planned jointly with
the pair from then on (helper_branch's joint planner: keep / move one / move both all candidates). So any dispatch
policy (wait / add at t1, wait / add at t2) can be scored exactly on this tree.

What the planner can observe at each decision is logged per task (f1_*, f2_* for the K-robot state it is in):
blind features (time, distance / heading left, start distance, object speed, yaw rate and progress rate (2 s EMAs),
robots' measured contact force (EMA), time since the last 5 cm of progress, contact flags) and the weight-aware
ones (the object's mass; the force model's strength and need-more flag, which use the mass).
Output: logs/evals/<prefix>/ (episodes.csv: one row per twin; summary.md / json), evals/<prefix>/ (copies).
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import random
import shutil
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
ARMS = ("k1", "k1null", "k2a", "k2null", "k2b", "k3")
LEAVES = ("k1", "k2b", "k2a", "k3")
ROBOTS_OF = {"k1": 1, "k1null": 1, "k2a": 2, "k2null": 2, "k2b": 2, "k3": 3}
BLIND = ("t", "d", "e_deg", "d0", "speed", "yawrate", "prog_rate", "force", "stall_s", "on1", "on2")
AWARE = ("mass", "strength", "need_more")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--checkpoint", default="logs/keep/marl2/turn_debug/model_15000.pt")
    ap.add_argument("--objects", default=TEN)
    ap.add_argument("--masses", default="20,40,60,80,100")
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--seed", type=int, default=1001)
    ap.add_argument("--horizon", type=float, default=80.0)
    ap.add_argument("--t1", type=float, default=8.0, help="first decision (s): add robot 2?")
    ap.add_argument("--t2", type=float, default=20.0, help="second decision (s): add the next robot?")
    ap.add_argument("--stage-dist", type=float, default=3.0)
    ap.add_argument("--push-force", type=float, default=160.0)
    ap.add_argument("--slow-min-s", type=float, default=1.0)
    ap.add_argument("--prefix", default="kchain")
    ap.add_argument("--device", default=None)
    a = ap.parse_args()
    assert a.t2 > a.t1 > 0

    os.environ["QUADCOOP_HELPER"] = "1"
    from train_coop2 import resolve_models, set_env

    set_env(resolve_models("b", "anymal3"))
    import numpy as np
    import torch
    from tensordict import TensorDict

    import quadcoop  # noqa: F401
    from mjlab.envs import ManagerBasedRlEnv
    from mjlab.utils.lab_api.math import quat_from_euler_xyz

    from branch_help import clone_envs
    from quadcoop import falls
    from quadcoop.contact_control import IDLE_ACTION, ContactController, to_action
    from quadcoop.coop2 import mdp as cm
    from quadcoop.coop2.env_cfg import SPECS, make_coop2_env_cfg
    from quadcoop.coop2.marl import actor_groups, actor_state, make_model
    from quadcoop.coop2.mdp import AGENTS, PLAN
    from quadcoop.stage1.mdp import wrap, yaw_of
    from quadcoop.stage1b import mdp as hb
    from quadcoop.stage1b.shapes import NOMINAL_MASS
    from quadcoop.stage2 import mdp as m2
    from quadcoop.stage2.shapes import OBJ_NAMES2, SHAPE_NAMES2, SHAPES2

    assert len(AGENTS) == 3, AGENTS
    H = AGENTS[2]
    device = a.device or ("cuda:0" if torch.cuda.is_available() else "cpu")
    ck = torch.load(a.checkpoint, map_location="cpu", weights_only=False)
    ck_cfg = ck.get("cfg", {})
    objects = [o.strip() for o in a.objects.split(",")]
    masses = [float(x) for x in a.masses.split(",")]
    out = ROOT / "logs" / "evals" / a.prefix
    stats = ROOT / "evals" / a.prefix
    out.mkdir(parents=True, exist_ok=True)

    base_cases = [(o, s, r) for o in objects for s in range(len(SCENARIOS)) for r in range(a.reps)]
    rng = random.Random(f"{a.seed}-coop2")
    jit_b = [[rng.uniform(-10, 10) for _ in range(2)] for _ in base_cases]
    gap_b = [[rng.uniform(0.3, 0.6) for _ in range(2)] for _ in base_cases]
    hrng = random.Random(f"{a.seed}-helper")
    jit_h = [hrng.uniform(-10, 10) for _ in base_cases]
    cases = [(arm, o, s, r, k) for arm in ARMS for k, (o, s, r) in enumerate(base_cases)]
    n = len(cases)
    print(f"K-chain: {len(base_cases)} tasks x {len(ARMS)} twins = {n} envs per mass; masses {masses}; "
          f"decisions at {a.t1:g} s and {a.t2:g} s", flush=True)
    rows = []
    t_start = time.time()
    rs = ck_cfg.get("reselect_s", (3.0, 6.0))

    for mass in masses:
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
        arm_of = [c[0] for c in cases]
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
        jh = torch.tensor([jit_h[k] for *_, k in cases], device=dev)
        bearings = [math.pi + torch.deg2rad(sgn * 35.0 + jit[:, i]) for i, sgn in enumerate((-1.0, 1.0))]
        bearings.append(math.pi + torch.deg2rad(jh))
        z = torch.zeros(n, device=dev)
        T_ = torch.ones(n, dtype=torch.bool, device=dev)
        F_ = torch.zeros(n, dtype=torch.bool, device=dev)
        sc = {"shape": obj_idx, "obj_xy_rel": torch.zeros(n, 2, device=dev), "obj_heading": z.clone(),
              "goal_xy_rel": dist.unsqueeze(-1) * torch.stack([torch.cos(gdir), torch.sin(gdir)], -1),
              "goal_yaw": wrap(turn), "bearings": bearings, "gaps": [gap[:, 0], gap[:, 1], torch.full((n,), 1.2, device=dev)],
              "yaw_noise": [z, z, z], "park": [F_, T_, T_],
              "contact_rule": torch.full((n,), 4, dtype=torch.long, device=dev),
              "contact_idx": torch.full((n, 2), -1, dtype=torch.long, device=dev),
              "start_behind": torch.ones(n, dtype=torch.bool, device=dev)}
        g.scenario = lambda env_ids: {k: ([x[env_ids] for x in v] if isinstance(v, list) else v[env_ids])
                                      for k, v in sc.items()}
        obs, _ = base.reset()
        g.scenario = None
        g.cfg.expert_first_only = False
        g.cfg.slow_min_s = a.slow_min_s
        g.c_in_group[:, 1] = False  # robot 2 parked: robot 1 pushes without waiting for it
        obs = TensorDict({k: v for k, v in obs.items() if not k.startswith("walker_")}, batch_size=[n])
        actors = {}
        for ag in PLAN:
            m_ = make_model(obs, actor_groups(ag, "b"), 3, (256, 128, 64), "b", True).to(dev)
            m_.load_state_dict(actor_state(ck["actors"], ag))
            actors[ag] = m_.eval()
        robots = [base.scene[ag] for ag in AGENTS]
        hr = robots[2]
        ctrl = ContactController(n, dev, reach=SPECS[H].half_length)
        idle = torch.tensor(IDLE_ACTION, device=dev)
        radius = g.radius_env[ids, obj_idx]

        # every per-env quantity of this script lives in S, so a branch copies it with the simulator state
        nanv = lambda: torch.full((n,), float("nan"), device=dev)  # noqa: E731
        zf = lambda: torch.zeros(n, device=dev)  # noqa: E731
        zb = lambda: torch.zeros(n, dtype=torch.bool, device=dev)  # noqa: E731
        S = {"done": zb(), "hold": zf(), "t_succ": nanv(), "fell0": zb(), "fell1": zb(), "fell2": zb(),
             "pres1": zb(), "pres2": zb(), "joint_on": zb(), "h_on": zb(), "h_has": zb(),
             "h_p": torch.zeros(n, 2, device=dev), "h_n": torch.zeros(n, 2, device=dev), "h_pre": torch.zeros(n, 2, device=dev),
             "h_idx": torch.full((n,), -1, dtype=torch.long, device=dev), "h_arr": nanv(), "t_add2": nanv(), "t_add3": nanv(),
             "touch_t": zf(), "live_t": zf(), "robot_s": zf(), "last_d": g.errors()[0].clone(), "last_e": zf(),
             "ema_v": zf(), "ema_w": zf(), "ema_p": zf(), "ema_f": zf(), "best_d": g.errors()[0].clone(), "stall": zf(),
             "prev_xy": g.box_pos()[:, :2].clone(), "prev_yaw": g.contact_frame_yaw().clone(), "prev_d": g.errors()[0].clone()}
        d0 = g.errors()[0].clone()
        how = [""] * n
        feats = {1: None, 2: None}

        def snapshot():
            d_, e_ = g.errors()
            e_ = torch.where(g.symmetry() > 0, e_, torch.zeros_like(e_))
            return {"t": torch.full((n,), t, device=dev), "d": d_.clone(), "e_deg": torch.rad2deg(e_.abs()),
                    "d0": d0.clone(), "speed": S["ema_v"].clone(), "yawrate": S["ema_w"].clone(),
                    "prog_rate": S["ema_p"].clone(), "force": S["ema_f"].clone(), "stall_s": S["stall"].clone(),
                    "on1": g.on_contact(0).float(), "on2": (g.on_contact(1) & S["pres1"]).float(),
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
            return cnt

        def stage(robot, e_, others):
            """Put robot at the staging point behind the object, on the side away from the robots in `others`."""
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

        def add_robot2(arm):
            e_ = idx_of[arm][~S["done"][idx_of[arm]]]
            if len(e_) == 0:
                return 0
            stage(robots[1], e_, [0])
            S["pres1"][e_] = True
            S["t_add2"][e_] = t
            g.c_in_group[e_, 1] = True
            g._reselect_expert(e_)
            return len(e_)

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

        def joint_decide(e_):
            """helper_branch.joint_decide (summed per-contact score): all three robots' contacts together."""
            if len(e_) == 0:
                return
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
            th = 1.3 * torch.linalg.norm(pw - hr.data.root_link_pos_w[e_, :2].unsqueeze(1), dim=-1) / c_.walk_speed
            on = prop["on"]
            kk = torch.arange(K, device=dev)
            stop1 = ((kk.unsqueeze(0) != cur[:, :1]) & on[:, :1]).float()
            stop2 = ((kk.unsqueeze(0) != cur[:, 1:2]) & on[:, 1:2]).float()
            A3 = lambda x: x[:, :, None, None] + x[:, None, :, None] + x[:, None, None, :]  # noqa: E731
            Tm = (A3(sc_) - c_.time_weight * torch.maximum(torch.maximum(t1_[:, :, None, None], t2_[:, None, :, None]),
                                                           th[:, None, None, :])
                  - c_.stop_weight * (stop1[:, :, None, None] + stop2[:, None, :, None]))
            feas = (use[:, :, :, None] & sep[:, :, None, :] & sep[:, None, :, :]
                    & ok_[:, :, None, None] & ok_[:, None, :, None] & ok_[:, None, None, :])
            feas &= (kk[:, None, None] != kk[None, None, :]).unsqueeze(0) & (kk[None, :, None] != kk[None, None, :]).unsqueeze(0)
            Tm = torch.where(feas, Tm, torch.full_like(Tm, -1e9))
            best, flat = Tm.view(m_, -1).max(-1)
            has = best > -1e8
            ia, ib, ic = flat // (K * K), (flat // K) % K, flat % K
            new = torch.where(has.unsqueeze(-1), torch.stack([ia, ib], -1), cur)
            g.c_need_more[e_] = prop["need_more"]
            g.apply_assignment(e_, new, p, nn, pre, prop["t_route"])
            changed = has & (ic != S["h_idx"][e_])
            S["h_idx"][e_] = torch.where(has, ic, S["h_idx"][e_])
            for key, src_ in (("h_p", p), ("h_n", nn), ("h_pre", pre)):
                S[key][e_] = torch.where(has.unsqueeze(-1), src_[ar, ic], S[key][e_])
            S["h_has"][e_] = has | S["h_has"][e_]
            if bool(changed.any()):
                ctrl.reset(torch.zeros(n, dtype=torch.bool, device=dev).index_fill_(0, e_[changed], True))

        def add_robot3(arm):
            e_ = idx_of[arm][~S["done"][idx_of[arm]]]
            if len(e_) == 0:
                return 0
            stage(hr, e_, [0, 1])
            S["joint_on"][e_] = True
            joint_decide(e_)
            go = torch.zeros(n, dtype=torch.bool, device=dev).index_fill_(0, e_, True) & S["h_has"]
            S["h_on"] |= go
            S["pres2"] |= go
            S["t_add3"] = torch.where(go, torch.full_like(S["t_add3"], t), S["t_add3"])
            ctrl.reset(go)
            return int(go.sum())

        class Coord:
            def __call__(self, g_, ids_):
                jm = S["joint_on"][ids_]
                joint_decide(ids_[jm])
                if bool((~jm).any()):
                    g_._reselect_expert(ids_[~jm])
        g.coordinator = Coord()

        dt = base.step_dt
        steps = int(a.horizon / dt)
        n1, n2 = int(round(a.t1 / dt)), int(round(a.t2 / dt))
        pt, yt = 0.10, math.radians(6.0)
        ph = torch.zeros(n, dtype=torch.bool, device=dev)
        t0 = time.time()
        t = 0.0
        with torch.no_grad():
            for i in range(steps):
                t = i * dt
                if i == n1:
                    feats[1] = snapshot()
                    c_ = branch("k1", ["k1null", "k2a", "k2null", "k3", "k2b"])
                    na = sum(add_robot2(tw) for tw in ("k2a", "k2null", "k3"))
                    print(f"  [{mass:g} kg] t1 {t:.1f} s ({c_} tensors per copy): "
                          f"{int(feats[1]['done'][idx_of['k1']].sum())}/{len(base_cases)} ended; robot 2 added in {na}", flush=True)
                if i == n2:
                    feats[2] = snapshot()
                    branch("k1", ["k2b"])
                    branch("k2a", ["k2null", "k3"])
                    nb = add_robot2("k2b")
                    nc = add_robot3("k3")
                    print(f"  [{mass:g} kg] t2 {t:.1f} s: robot 2 added in {nb} (k2b), robot 3 in {nc} (k3)", flush=True)
                live = ~S["done"]
                act = torch.cat([actors[ag](obs) for ag in PLAN], -1)
                act[:, 3:6] = torch.where(S["pres1"].unsqueeze(-1), act[:, 3:6], idle.expand(n, 3))  # parked: stand
                _, e = g.errors()
                e = torch.where(g.symmetry() > 0, e, torch.zeros_like(e))
                mates = torch.stack([robots[k].data.root_link_pos_w[:, :2] for k in range(2)], 1)
                hp = hr.data.root_link_pos_w[:, :2]
                near = mates[torch.arange(n, device=dev), torch.linalg.norm(mates - hp.unsqueeze(1), dim=-1).argmin(-1)]
                act_h = S["h_on"] & S["h_has"] & live
                tw_, ph = ctrl(hp, yaw_of(hr.data.root_link_quat_w), g.box_pos()[:, :2], g.contact_frame_yaw(), radius,
                               S["h_p"], S["h_n"], g.c_cof, g.goal_xy, e, pre_obj=S["h_pre"], partner_pos=near, active=act_h)
                a_h = torch.where(act_h.unsqueeze(-1), to_action(tw_), idle.expand(n, 3))
                o_, _, _, _, _ = base.step(torch.cat([act, a_h], -1))
                obs = TensorDict({kk: v for kk, v in o_.items() if not kk.startswith("walker_")}, batch_size=[n])
                t = (i + 1) * dt
                pres = [torch.ones(n, dtype=torch.bool, device=dev), S["pres1"], S["pres2"]]
                f_any = torch.zeros(n, dtype=torch.bool, device=dev)
                for k, ag in enumerate(AGENTS):
                    f_ = falls.fallen(base, asset_name=ag, nominal_height=SPECS[ag].nominal_height) & pres[k] & live
                    S[f"fell{k}"] |= f_
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
                # observable motion statistics (2 s EMAs): object speed, yaw rate, progress rate, robots' contact force
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
                pushing_h = ph & act_h & ok
                S["h_arr"] = torch.where(pushing_h & torch.isnan(S["h_arr"]), torch.full_like(S["h_arr"], t), S["h_arr"])
                S["touch_t"] += (cm.robots_touching(base) > 0).float() * ok.float() * dt
                S["live_t"] += ok.float() * dt
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
        for j, (arm, o, s, r, k) in enumerate(cases):
            fv = lambda q, key: round(float(feats[q][key][j]), 4)  # noqa: E731
            rows.append({"arm": arm, "object": o, "mass": mass, "scenario": SCENARIOS[s][0], "rep": r, "task": k,
                         "success": int(how[j] == "success"), "outcome": how[j] or "horizon",
                         "t_success": "" if math.isnan(float(S["t_succ"][j])) else round(float(S["t_succ"][j]), 2),
                         "final_pos_err": round(float(S["last_d"][j]), 3),
                         "robots": ROBOTS_OF[arm], "robot_s": round(float(S["robot_s"][j]), 1),
                         "t_add2": "" if math.isnan(float(S["t_add2"][j])) else round(float(S["t_add2"][j]), 2),
                         "t_add3": "" if math.isnan(float(S["t_add3"][j])) else round(float(S["t_add3"][j]), 2),
                         "helper_arrive_s": "" if math.isnan(float(S["h_arr"][j])) else round(float(S["h_arr"][j]), 2),
                         **{f"fell_{ag}": int(bool(S[f"fell{q}"][j])) for q, ag in enumerate(AGENTS)},
                         "robots_touch_frac": round(float(S["touch_t"][j] / S["live_t"][j].clamp(min=1e-6)), 3),
                         "ended_t1": int(bool(feats[1]["done"][j])), "ended_t2": int(bool(feats[2]["done"][j])),
                         **{f"f1_{key}": fv(1, key) for key in BLIND + AWARE},
                         **{f"f2_{key}": fv(2, key) for key in BLIND + AWARE}})
        sel = [x for x in rows if x["mass"] == mass]
        print(f"[{mass:g} kg] " + "  ".join(f"{arm} {sum(x['success'] for x in sel if x['arm'] == arm)}/"
                                          f"{sum(1 for x in sel if x['arm'] == arm)}" for arm in ARMS)
              + f"  ({time.time() - t_start:.0f} s)", flush=True)
        base.close()
        del base

    with open(out / "episodes.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    brng = np.random.default_rng(0)
    key = lambda r_: (r_["object"], r_["mass"], r_["scenario"], r_["rep"])  # noqa: E731
    by = {tw: {key(r_): r_ for r_ in rows if r_["arm"] == tw} for tw in ARMS}

    def ci(v):
        v = np.asarray(v, dtype=float)
        bs = v[brng.integers(0, len(v), (2000, len(v)))].mean(1)
        return 100 * v.mean(), 100 * np.percentile(bs, 2.5), 100 * np.percentile(bs, 97.5)
    md = [f"# K -> K+1 tree: {a.prefix}", "",
          f"Seed {a.seed}, {len(base_cases)} tasks per mass; robot 2 added at {a.t1:g} s (k2a) or {a.t2:g} s (k2b), robot 3 "
          f"at {a.t2:g} s after robot 2 at {a.t1:g} s (k3). Success over all starts (a task that ended before a branch "
          f"has the same outcome in every twin). Nets in pp with 95% paired bootstrap.", "",
          "| mass | k1 | k2b | k2a | k3 | k1null-k1 | k2a-k1 | k3-k2a | k2null-k2a | k2b-k1 |", "|---|---|---|---|---|---|---|---|---|---|"]
    summ = {"seed": a.seed, "t1": a.t1, "t2": a.t2, "by_mass": {}}
    for m in masses + ["all"]:
        ks = [k_ for k_, r_ in by["k1"].items() if m == "all" or r_["mass"] == m]
        y = {tw: np.array([by[tw][k_]["success"] for k_ in ks], dtype=float) for tw in ARMS}
        diffs = {f"{x}-{b}": ci(y[x] - y[b]) for x, b in (("k1null", "k1"), ("k2a", "k1"), ("k3", "k2a"),
                                                         ("k2null", "k2a"), ("k2b", "k1"))}
        summ["by_mass"][str(m)] = {"success": {tw: 100 * float(y[tw].mean()) for tw in ARMS},
                                   "net": {k_: list(v) for k_, v in diffs.items()}}
        md.append(f"| {m if m == 'all' else f'{m:g}'} | " + " | ".join(f"{100 * y[tw].mean():.0f}%" for tw in LEAVES) + " | "
                  + " | ".join(f"{v[0]:+.1f} [{v[1]:+.0f}, {v[2]:+.0f}]" for v in diffs.values()) + " |")
    (out / "summary.md").write_text("\n".join(md) + "\n")
    (out / "summary.json").write_text(json.dumps(summ, indent=1))
    stats.mkdir(parents=True, exist_ok=True)
    for f in ("summary.md", "summary.json", "episodes.csv"):
        shutil.copy2(out / f, stats / f)
    print("\n".join(md))
    return 0


if __name__ == "__main__":
    sys.exit(main())
