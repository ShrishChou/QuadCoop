"""The two-robot contact planner with a third, helper robot for heavy objects (docs/planner_helper.md).

    python scripts/helper_test.py --masses 60,80,100 --seed 7100 --prefix helper-7100

Three ANYmal C (QUADCOOP_PAIR=anymal3, set here). Robots 1 and 2 are the contact planner's pair exactly as in
planner-bench (expert rule 4 + the Stage 4 executor turn_debug/model_15000.pt, start behind, 80 s); they see each
other as partners (QUADCOOP_HELPER=1). Robot 3 is a scripted helper (quadcoop.contact_control.ContactController):

  engage   when the planner's force model says the current pair cannot slide the object the way it wants
           (current_strength < 1, with robot_push_force = --push-force) for --engage-s; then it stays engaged
  planner  once engaged, the env's per-robot force limit is multiplied by --cap-mult (the pair plans as if it had the
           helper's force behind it)
  contact  a free candidate contact (not the pair's, standing points clear of theirs) whose push direction best
           matches the wanted motion, near the centre of friction unless a turn is wanted, re-chosen every
           --repick-s; it walks there around the object and pushes along the contact normal

Arms (same tasks, one env build per mass; the helper is parked 40 m away in the pair arms):
  pair250   the planner as in planner-bench (robot_push_force 250 N, assumed)
  pair160   the same pair with the measured force limit (--push-force, evals/beam-push*: about 150-165 N per robot)
  helper    pair160 + the helper
Tasks: scripts/eval_coop2.py's 4 scenarios x --reps, the same seeded placements for robots 1 and 2 as contact_test.py
(the helper starts 1.2 m further out, straight behind the object). Success = 10 cm / 6 deg held 1 s before --horizon;
a fall of any present robot, a tipped or lost object ends the episode.
Output: logs/evals/<prefix>/episodes.csv; evals/<prefix>/summary.md (+ summary.json, episodes.csv).
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
             ("D_far_turn", 5.0, 0.0, 90.0))  # as scripts/eval_coop2.py / contact_test.py
TEN = "cube,long,sphere,cylinder,arch,dumbbell,t_shape,l_shape,u_channel,plus"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--checkpoint", default="logs/keep/marl2/turn_debug/model_15000.pt")
    ap.add_argument("--objects", default=TEN)
    ap.add_argument("--masses", default="60,80,100")
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--seed", type=int, default=7100)
    ap.add_argument("--horizon", type=float, default=80.0)
    ap.add_argument("--arms", default="pair250,pair160,helper")
    ap.add_argument("--push-force", type=float, default=160.0, help="N per robot for pair160 / helper (measured)")
    ap.add_argument("--cap-mult", type=float, default=1.3,
                    help="helper engaged: the env's force limit x this (evals/beam-push3: three robots deliver about "
                         "1.3x a pair's force at 80-120 kg)")
    ap.add_argument("--engage-s", type=float, default=0.5)
    ap.add_argument("--repick-s", type=float, default=2.0)
    ap.add_argument("--slow-min-s", type=float, default=1.0)
    ap.add_argument("--set", default="", help="more goal-command settings, key=value comma list (e.g. roll_ratio=0.1)")
    ap.add_argument("--prefix", default="helper")
    ap.add_argument("--device", default=None)
    a = ap.parse_args()

    os.environ["QUADCOOP_HELPER"] = "1"
    from train_coop2 import resolve_models, set_env

    models = resolve_models("b", "anymal3")
    set_env(models)
    import numpy as np
    import torch
    from tensordict import TensorDict

    import quadcoop  # noqa: F401
    from mjlab.envs import ManagerBasedRlEnv

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
    assert ck_cfg.get("contacts"), f"{a.checkpoint} was not trained with --contacts"
    arms = [x.strip() for x in a.arms.split(",")]
    assert set(arms) <= {"pair250", "pair160", "helper"}, arms
    objects = [o.strip() for o in a.objects.split(",")]
    masses = [float(x) for x in a.masses.split(",")]
    overrides = dict(kv.split("=", 1) for kv in a.set.split(",") if kv.strip())
    out = ROOT / "logs" / "evals" / a.prefix
    stats = ROOT / "evals" / a.prefix
    out.mkdir(parents=True, exist_ok=True)

    base_cases = [(o, s, r) for o in objects for s in range(len(SCENARIOS)) for r in range(a.reps)]
    rng = random.Random(f"{a.seed}-coop2")  # robots 1 and 2: the same placements as contact_test / eval_coop2
    jit_b = [[rng.uniform(-10, 10) for _ in range(2)] for _ in base_cases]
    gap_b = [[rng.uniform(0.3, 0.6) for _ in range(2)] for _ in base_cases]
    hrng = random.Random(f"{a.seed}-helper")
    jit_h = [hrng.uniform(-10, 10) for _ in base_cases]
    cases = [(arm, o, s, r, k) for arm in arms for k, (o, s, r) in enumerate(base_cases)]
    n = len(cases)
    print(f"helper test: arms {arms}; {len(objects)} objects x {len(SCENARIOS)} scenarios x {a.reps} reps = "
          f"{len(base_cases)} tasks per arm, {n} envs per mass; masses {masses}; push force {a.push_force:g} N, "
          f"cap x{a.cap_mult:g} with the helper", flush=True)
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
        gc = cfg.commands["goal"]
        gc.robot_push_force = a.push_force
        for k_, v_ in overrides.items():
            if not hasattr(gc, k_):
                raise SystemExit(f"--set: the goal command has no setting '{k_}'")
            setattr(gc, k_, type(getattr(gc, k_))(v_))
            print(f"[set] goal.{k_} = {getattr(gc, k_)}", flush=True)
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
        is_helper = torch.tensor([x == "helper" for x in arm_of], device=dev)
        base_mult = torch.tensor([250.0 / a.push_force if x == "pair250" else 1.0 for x in arm_of], device=dev)
        g.c_cap_mult[:] = base_mult

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
        park_h = ~is_helper
        sc = {"shape": obj_idx, "obj_xy_rel": torch.zeros(n, 2, device=dev), "obj_heading": z.clone(),
              "goal_xy_rel": dist.unsqueeze(-1) * torch.stack([torch.cos(gdir), torch.sin(gdir)], -1),
              "goal_yaw": wrap(turn), "bearings": bearings, "gaps": [gap[:, 0], gap[:, 1], torch.full((n,), 1.2, device=dev)],
              "yaw_noise": [z, z, z], "park": [torch.zeros(n, dtype=torch.bool, device=dev)] * 2 + [park_h],
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
        hr = robots[2]
        ctrl = ContactController(n, dev, reach=SPECS[H].half_length)
        idle = torch.tensor(IDLE_ACTION, device=dev)
        radius = g.radius_env[ids, obj_idx]
        present = [torch.ones(n, dtype=torch.bool, device=dev)] * 2 + [is_helper]
        h_on = torch.zeros(n, dtype=torch.bool, device=dev)
        h_has = torch.zeros(n, dtype=torch.bool, device=dev)
        h_weak = torch.zeros(n, device=dev)
        h_t_on = torch.full((n,), float("nan"), device=dev)
        h_next = torch.zeros(n, device=dev)
        h_p, h_n, h_pre = (torch.zeros(n, 2, device=dev) for _ in range(3))
        h_idx = torch.full((n,), -1, dtype=torch.long, device=dev)

        def pick(mask):
            """The helper's contact for these envs (see the module docstring)."""
            e_ = mask.nonzero().flatten()
            if len(e_) == 0:
                return
            shp = g.shape[e_]
            p, nn, pre, _, valid, sep = g._contact_geom(e_, shp)
            m_, K = p.shape[0], p.shape[1]
            ar = torch.arange(m_, device=dev)
            yaw = g.contact_frame_yaw()[e_]
            cs, sn = torch.cos(yaw), torch.sin(yaw)
            vw = g.c_vdes[e_]
            v_o = torch.stack([cs * vw[:, 0] + sn * vw[:, 1], -sn * vw[:, 0] + cs * vw[:, 1]], -1)
            wz, cg = g.c_wdes[e_], g.c_cg[e_]
            vn = torch.linalg.norm(v_o, dim=-1, keepdim=True)
            u = v_o / vn.clamp(min=1e-6)
            f = -nn  # (m, K, 2) push directions
            along = (f * u.unsqueeze(1)).sum(-1) * (vn > 1e-3).float()
            r = p - g.c_cof[e_].unsqueeze(1)
            tau = (r[..., 0] * f[..., 1] - r[..., 1] * f[..., 0]) / cg.unsqueeze(-1)
            tfrac = ((cg * wz).abs() / ((cg * wz).abs() + vn.squeeze(-1)).clamp(min=1e-6)).unsqueeze(-1)
            score = along + tfrac * torch.sign(wz).unsqueeze(-1) * tau - 0.3 * (1.0 - tfrac) * tau.abs()
            cur = g.c_idx[e_]
            kk = torch.arange(K, device=dev).unsqueeze(0)
            ok = valid & (kk != cur[:, :1]) & (kk != cur[:, 1:2])
            ok &= sep[ar, cur[:, 0]] & sep[ar, cur[:, 1]]
            ok &= along > -0.2  # never against the wanted motion
            score = torch.where(ok, score, torch.full_like(score, -1e9))
            best, j = score.max(-1)
            has = best > -1e8
            changed = has & (j != h_idx[e_])
            h_idx[e_] = torch.where(has, j, h_idx[e_])
            h_p[e_] = torch.where(has.unsqueeze(-1), p[ar, j], h_p[e_])
            h_n[e_] = torch.where(has.unsqueeze(-1), nn[ar, j], h_n[e_])
            h_pre[e_] = torch.where(has.unsqueeze(-1), pre[ar, j], h_pre[e_])
            h_has[e_] = has | h_has[e_]
            if bool(changed.any()):
                ctrl.reset(torch.zeros(n, dtype=torch.bool, device=dev).index_fill_(0, e_[changed], True))

        dt = base.step_dt
        steps = int(a.horizon / dt)
        done = torch.zeros(n, dtype=torch.bool, device=dev)
        hold = torch.zeros(n, device=dev)
        t_succ = torch.full((n,), float("nan"), device=dev)
        how = [""] * n
        fell = [torch.zeros(n, dtype=torch.bool, device=dev) for _ in AGENTS]
        h_push_t = torch.zeros(n, device=dev)
        h_force = torch.zeros(n, device=dev)
        touch_t = torch.zeros(n, device=dev)
        live_t = torch.zeros(n, device=dev)
        last_d, last_e = g.errors()[0].clone(), torch.zeros(n, device=dev)
        pt, yt = 0.10, math.radians(6.0)
        t0 = time.time()
        with torch.no_grad():
            for i in range(steps):
                t = i * dt
                live = ~done
                strength = g.current_strength()
                weak = live & is_helper & ~h_on & (strength < 1.0)
                h_weak = torch.where(weak, h_weak + dt, torch.zeros_like(h_weak))
                new_on = h_weak >= a.engage_s
                if bool(new_on.any()):
                    h_on |= new_on
                    h_t_on = torch.where(new_on, torch.full_like(h_t_on, t), h_t_on)
                    g.c_cap_mult[new_on] = a.cap_mult
                    pick(new_on)
                    h_next = torch.where(new_on, torch.full_like(h_next, t + a.repick_s), h_next)
                due = h_on & live & (t >= h_next)
                if bool(due.any()):
                    pick(due)
                    h_next = torch.where(due, torch.full_like(h_next, t + a.repick_s), h_next)
                act = torch.cat([actors[ag](obs) for ag in PLAN], -1)
                _, e = g.errors()
                e = torch.where(g.symmetry() > 0, e, torch.zeros_like(e))
                mates = torch.stack([robots[k].data.root_link_pos_w[:, :2] for k in range(2)], 1)
                hp = hr.data.root_link_pos_w[:, :2]
                near = mates[torch.arange(n, device=dev), torch.linalg.norm(mates - hp.unsqueeze(1), dim=-1).argmin(-1)]
                act_h = h_on & h_has & live
                tw, ph = ctrl(hp, yaw_of(hr.data.root_link_quat_w), g.box_pos()[:, :2], g.contact_frame_yaw(), radius,
                              h_p, h_n, g.c_cof, g.goal_xy, e, pre_obj=h_pre, partner_pos=near, active=act_h)
                a_h = torch.where(act_h.unsqueeze(-1), to_action(tw), idle.expand(n, 3))
                o_, _, _, _, _ = base.step(torch.cat([act, a_h], -1))
                obs = TensorDict({kk: v for kk, v in o_.items() if not kk.startswith("walker_")}, batch_size=[n])
                t = (i + 1) * dt
                f_any = torch.zeros(n, dtype=torch.bool, device=dev)
                for k, ag in enumerate(AGENTS):
                    f_ = falls.fallen(base, asset_name=ag, nominal_height=SPECS[ag].nominal_height) & present[k] & live
                    fell[k] |= f_
                    f_any |= f_
                tip = hb.box_tipped(base) & live & ~f_any
                lost = cm.box_lost(base) & live & ~f_any & ~tip
                d, e2 = g.errors()
                ok = live & ~f_any & ~tip & ~lost
                last_d = torch.where(ok, d, last_d)
                last_e = torch.where(ok, e2.abs(), last_e)
                inside = ok & (d < pt) & (e2.abs() < yt)
                hold = torch.where(inside, hold + dt, torch.zeros_like(hold))
                succ = ok & (hold >= 1.0)
                t_succ = torch.where(succ, torch.full_like(t_succ, t), t_succ)
                pushing_h = ph & act_h & ok
                h_push_t += pushing_h.float() * dt
                h_force += torch.linalg.norm(cm.object_force_from(base, H), dim=-1) * pushing_h.float() * dt
                touch_t += (cm.robots_touching(base) > 0).float() * ok.float() * dt
                live_t += ok.float() * dt
                for j in f_any.nonzero().flatten().tolist():
                    how[j] = "fell_" + "+".join(ag for k, ag in enumerate(AGENTS) if bool(fell[k][j]))
                for j in tip.nonzero().flatten().tolist():
                    how[j] = "tipped"
                for j in lost.nonzero().flatten().tolist():
                    how[j] = "lost"
                for j in succ.nonzero().flatten().tolist():
                    how[j] = "success"
                done |= f_any | tip | lost | succ
                if i % 1000 == 0:
                    print(f"  [{mass:g} kg] step {i}/{steps}: live {int((~done).sum())}/{n}, helper engaged "
                          f"{int(h_on.sum())}/{int(is_helper.sum())} ({time.time() - t0:.0f} s)", flush=True)
                if bool(done.all()):
                    break
        for j, (arm, o, s, r, k) in enumerate(cases):
            rows.append({"arm": arm, "object": o, "mass": mass, "scenario": SCENARIOS[s][0], "rep": r, "task": k,
                         "success": int(how[j] == "success"), "outcome": how[j] or "horizon",
                         "t_success": "" if math.isnan(float(t_succ[j])) else round(float(t_succ[j]), 2),
                         "final_pos_err": round(float(last_d[j]), 3), "final_yaw_err_deg": round(math.degrees(float(last_e[j])), 1),
                         **{f"fell_{ag}": int(bool(fell[q][j])) for q, ag in enumerate(AGENTS)},
                         "helper_on": int(bool(h_on[j])),
                         "helper_t_on": "" if math.isnan(float(h_t_on[j])) else round(float(h_t_on[j]), 2),
                         "helper_push_s": round(float(h_push_t[j]), 2),
                         "helper_force_n": round(float(h_force[j] / h_push_t[j].clamp(min=1e-6)), 1) if float(h_push_t[j]) > 0 else "",
                         "robots_touch_frac": round(float(touch_t[j] / live_t[j].clamp(min=1e-6)), 3)})
        sel = [x for x in rows if x["mass"] == mass]
        print(f"[{mass:g} kg] " + "  ".join(f"{arm} {sum(x['success'] for x in sel if x['arm'] == arm)}/"
                                          f"{sum(1 for x in sel if x['arm'] == arm)}" for arm in arms)
              + f"  ({time.time() - t_start:.0f} s)", flush=True)
        base.close()
        del base

    with open(out / "episodes.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    def rate(xs):
        return 100.0 * sum(x["success"] for x in xs) / max(1, len(xs))

    md = [f"# Planner + helper: {a.prefix}", "",
          f"Seed {a.seed}, {len(base_cases)} tasks per arm and mass, start behind, {a.horizon:g} s. pair250: the planner "
          f"as in planner-bench; pair160: force limit {a.push_force:g} N; helper: pair160 + a scripted third robot "
          f"(limit x{a.cap_mult:g} once it engages). Success %.", ""]
    md += ["| object | " + " | ".join(f"{arm} {m:g} kg" for m in masses for arm in arms) + " |",
           "|---|" + "---|" * (len(masses) * len(arms))]
    for o in objects + ["all"]:
        md.append(f"| {o} | " + " | ".join(
            f"{rate([x for x in rows if x['arm'] == arm and x['mass'] == m and (o == 'all' or x['object'] == o)]):.0f}"
            for m in masses for arm in arms) + " |")
    md += ["", "Paired differences (percentage points, 95% bootstrap over tasks, 2000 draws):", ""]
    import numpy as np
    brng = np.random.default_rng(0)
    summ = {"arms": arms, "masses": masses, "seed": a.seed, "diff": {}}
    for x_, y_ in (("helper", "pair160"), ("helper", "pair250"), ("pair160", "pair250")):
        if x_ not in arms or y_ not in arms:
            continue
        for m in masses + ["all"]:
            key = lambda r_: (r_["object"], r_["mass"], r_["scenario"], r_["rep"])  # noqa: E731
            A = {key(r_): r_["success"] for r_ in rows if r_["arm"] == x_ and (m == "all" or r_["mass"] == m)}
            B = {key(r_): r_["success"] for r_ in rows if r_["arm"] == y_ and (m == "all" or r_["mass"] == m)}
            ks = sorted(A)
            dvec = np.array([A[k_] - B[k_] for k_ in ks], dtype=float)
            bs = dvec[brng.integers(0, len(dvec), (2000, len(dvec)))].mean(1)
            lo, hi = np.percentile(bs, [2.5, 97.5])
            summ["diff"][f"{x_}-{y_}@{m}"] = [100 * dvec.mean(), 100 * lo, 100 * hi]
            md.append(f"- {x_} - {y_}, {m if m == 'all' else f'{m:g} kg'}: {100 * dvec.mean():+.1f} [{100 * lo:+.1f}, {100 * hi:+.1f}]")
    hx = [x for x in rows if x["arm"] == "helper"]
    if hx:
        md += ["", "Helper: engaged in " + ", ".join(
            f"{m:g} kg {100.0 * sum(x['helper_on'] for x in hx if x['mass'] == m) / max(1, sum(1 for x in hx if x['mass'] == m)):.0f}%"
            for m in masses) + "; helper falls " + str(sum(x[f"fell_{H}"] for x in hx)) + f" of {len(hx)}."]
    outc = {}
    for x in rows:
        outc.setdefault(f"{x['arm']} {x['mass']:g}", {}).setdefault(x["outcome"], 0)
        outc[f"{x['arm']} {x['mass']:g}"][x["outcome"]] += 1
    md += ["", "Outcomes: " + "; ".join(f"{k_}: {v_}" for k_, v_ in outc.items())]
    summ["outcomes"] = outc
    (out / "summary.md").write_text("\n".join(md) + "\n")
    (out / "summary.json").write_text(json.dumps(summ, indent=1))
    stats.mkdir(parents=True, exist_ok=True)
    for f in ("summary.md", "summary.json", "episodes.csv"):
        shutil.copy2(out / f, stats / f)
    print("\n".join(md))
    return 0


if __name__ == "__main__":
    sys.exit(main())
