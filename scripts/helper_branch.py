"""Does a third robot change the outcome, and does where it pushes matter? Branching pilot on the contact planner
(docs/late_help.md, "three-robot contact-planner pilot").

    python scripts/helper_branch.py --masses 60,80,100 --seed 7100 --prefix hb-7100

Three ANYmal C (QUADCOOP_PAIR=anymal3). Robots 1 and 2 are the contact planner's pair exactly as in planner-bench /
helper_test (expert rule 4 + the Stage 4 executor turn_debug/model_15000.pt, start behind, 80 s), with the measured
force limit (--push-force 160 N) and NO change to its planning when a helper is present (--cap-mult 1). Robot 3 is
parked. Each task runs in 2 + --ranks twins; at --branch-s the pair twin's whole state is copied into the others:
  pair     the pair continues (abstain)
  null     the pair continues too: the noise floor (simulator nondeterminism flips outcomes by itself)
  h<r>     the helper appears at a staging point --stage-dist m behind the object (w.r.t. the goal, on the side away
           from the pair) and walks to the r-th best free third contact under the direct score (push along the
           wanted motion + turning moment when a turn is wanted, never against the motion; the pair's contacts at
           the decision held out, standing points clear of theirs); the contact is kept for the rest of the episode
           and the helper (the scripted ContactController) presses along its normal
Per task: outcomes of every twin, what the planner saw at the decision (its force-model strength, need-more flag,
distance / heading left, the pair on its contacts), the scores of the ranked contacts, helper arrival, push time and
force, robot-robot contact. Summary: rescue / disruption / net (rescue - disruption) of each helper rank and of the
null against the pair, per mass, with paired bootstrap intervals; and the best rank per task (an upper bound on
choosing the contact).
Output: logs/evals/<prefix>/ (episodes.csv, summary.md / json); evals/<prefix>/ (copies).
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


def _film(a, base, cases, film_ids, how, t_succ, mass, fdt, rec_q, rec_mp, rec_mq, rec_pts, rec_cap, out):
    """One MP4 per filmed episode in logs/evals/<prefix>/videos/ (+ index.html), with the planner's two contacts
    (cyan, yellow posts), the helper's contact (magenta post, solid once engaged) and a caption."""
    import numpy as np

    from quadcoop.coop2.video import Camera, render_episode

    sys.path.insert(0, str(ROOT / "scripts"))
    from contact_test import _video_index

    vw, vh = (int(x) for x in a.video_size.lower().split("x"))
    cam = Camera(base, vw, vh)
    Q = np.stack(rec_q, 1)
    MP = np.stack(rec_mp, 1) if rec_mp else None
    MQ = np.stack(rec_mq, 1) if rec_mq else None
    P = np.stack(rec_pts, 1)
    C = np.stack(rec_cap, 1)
    vdir = out / "videos"
    for fi, j in enumerate(film_ids):
        arm, o, s, r, _ = cases[j]
        outcome = how[j] or "horizon"
        end = float(t_succ[j]) if not math.isnan(float(t_succ[j])) else Q.shape[1] * fdt
        F = min(Q.shape[1], int(end / fdt) + int(1.0 / fdt) + 1)
        stem = f"{o}_{mass:g}kg_{SCENARIOS[s][0]}_r{r}_{arm}"
        name = f"{stem}__{outcome}.mp4"
        head = f"{arm}: {o} {mass:g} kg {SCENARIOS[s][0]} rep {r} -> {outcome}"

        def cap(f, fi=fi, head=head):
            d_, e_, on, pushing, st = C[fi, f, :5]
            return (f"{head} | t {f * fdt:4.1f} s\nto goal {d_:.2f} m, {e_:+.0f} deg | pair strength {st:.2f} | helper "
                    f"{'ENGAGED' if on > 0.5 else 'waiting'}{' PUSHING' if pushing > 0.5 else ''}\n"
                    "cyan / yellow: planner pair contacts, magenta: helper contact; ball above = robot")

        def marks(f, fi=fi):
            out_ = []
            row = C[fi, f]
            for k, col in enumerate(((0.0, 0.95, 0.95), (1.0, 0.85, 0.0))):
                px, py, on = row[5 + 3 * k: 8 + 3 * k]
                al = 1.0 if on > 0.5 else 0.4
                out_.append(("arrow", (px, py, 0.25), (px, py, 1.05), 0.012, (*col, al)))
                out_.append(("sphere", (px, py, 1.05), 0.07, (*col, al)))
            hx, hy = row[11:13]
            if row[2] > 0.5:
                out_.append(("arrow", (hx, hy, 0.25), (hx, hy, 1.05), 0.012, (1.0, 0.2, 1.0, 1.0)))
                out_.append(("sphere", (hx, hy, 1.05), 0.07, (1.0, 0.2, 1.0, 1.0)))
            for k, col in enumerate(((0.0, 0.95, 0.95), (1.0, 0.85, 0.0), (1.0, 0.2, 1.0))):
                rx, ry = P[fi, f, k]
                out_.append(("sphere", (rx, ry, 1.45), 0.11, (*col, 1.0)))
            return out_

        try:
            render_episode(cam, j, Q[fi, :F], None if MP is None else MP[fi, :F], None if MQ is None else MQ[fi, :F],
                           P[fi, :F], vdir / name, 1.0 / fdt, caption=cap, marks=marks)
            (vdir / f"{stem}.json").write_text(json.dumps({"object": o, "mass": mass, "scenario": SCENARIOS[s][0],
                                                           "rep": r, "arm": arm, "outcome": outcome,
                                                           "success": int(outcome == "success"), "file": name}))
        except Exception as ex:  # noqa: BLE001
            print(f"video failed {name}: {ex}", flush=True)
    _video_index(vdir)
    print(f"[{mass:g} kg] {len(film_ids)} videos in {vdir}", flush=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--checkpoint", default="logs/keep/marl2/turn_debug/model_15000.pt")
    ap.add_argument("--objects", default=TEN)
    ap.add_argument("--masses", default="60,80,100")
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--seed", type=int, default=7100)
    ap.add_argument("--horizon", type=float, default=80.0)
    ap.add_argument("--branch-s", type=float, default=10.0, help="decision time (s from the start)")
    ap.add_argument("--ranks", type=int, default=3, help="helper twins: the 1st .. r-th best third contact")
    ap.add_argument("--joint", action="store_true",
                    help="add a 'joint' twin: from the branch on, every re-plan chooses all three robots' contacts together")
    ap.add_argument("--stage-dist", type=float, default=3.0, help="helper staging distance behind the object (m)")
    ap.add_argument("--push-force", type=float, default=160.0, help="N per robot for pair160 / helper (measured)")
    ap.add_argument("--cap-mult", type=float, default=1.0,
                    help="helper engaged: the env's force limit x this (evals/beam-push3: three robots deliver about "
                         "1.3x a pair's force at 80-120 kg)")
    ap.add_argument("--engage-s", type=float, default=0.5)
    ap.add_argument("--repick-s", type=float, default=2.0)
    ap.add_argument("--slow-min-s", type=float, default=1.0)
    ap.add_argument("--set", default="", help="more goal-command settings, key=value comma list (e.g. roll_ratio=0.1)")
    ap.add_argument("--prefix", default="helper")
    ap.add_argument("--device", default=None)
    ap.add_argument("--videos", type=int, default=0, help="1 = film the --video-* episodes (helper arm by default)")
    ap.add_argument("--video-arms", default="helper")
    ap.add_argument("--video-objects", default="all")
    ap.add_argument("--video-masses", default="80")
    ap.add_argument("--video-scenarios", default="A_straight,D_far_turn")
    ap.add_argument("--video-reps", default="0")
    ap.add_argument("--video-size", default="640x480")
    ap.add_argument("--video-only", type=int, default=0,
                    help="1 = run only the filmed episodes' tasks (no statistics; for making videos)")
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
    from mjlab.utils.lab_api.math import quat_from_euler_xyz
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
    arms = ["pair", "null"] + [f"h{r_ + 1}" for r_ in range(a.ranks)] + (["joint"] if a.joint else [])
    from branch_help import clone_envs
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
    v_arms = {x.strip() for x in a.video_arms.split(",")}
    v_objs = None if a.video_objects == "all" else {x.strip() for x in a.video_objects.split(",")}
    v_mass = {float(x) for x in a.video_masses.split(",")}
    v_scen = None if a.video_scenarios == "all" else {x.strip() for x in a.video_scenarios.split(",")}
    v_reps = None if a.video_reps == "all" else {int(x) for x in a.video_reps.split(",")}

    def filmed(c):
        arm, o, s_, r, _ = c
        return (a.videos > 0 and arm in v_arms and (v_objs is None or o in v_objs)
                and (v_scen is None or SCENARIOS[s_][0] in v_scen) and (v_reps is None or r in v_reps))
    if a.video_only:
        cases = [c for c in cases if filmed(c)]
        masses = [m for m in masses if m in v_mass]
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
        is_joint = torch.tensor([x == "joint" for x in arm_of], device=dev)
        is_helper = torch.tensor([x.startswith("h") for x in arm_of], device=dev) | is_joint
        rank_of = torch.tensor([int(x[1:]) - 1 if x.startswith("h") else 0 for x in arm_of], device=dev)
        joint_on = torch.zeros(n, dtype=torch.bool, device=dev)
        j_moves = torch.zeros(n, device=dev)  # joint plans that moved an incumbent
        base_mult = torch.ones(n, device=dev)
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
        park_h = torch.ones(n, dtype=torch.bool, device=dev)  # every helper parked until the branch
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
        present = [torch.ones(n, dtype=torch.bool, device=dev)] * 2 + [torch.zeros(n, dtype=torch.bool, device=dev)]
        h_on = torch.zeros(n, dtype=torch.bool, device=dev)
        h_has = torch.zeros(n, dtype=torch.bool, device=dev)
        h_weak = torch.zeros(n, device=dev)
        h_t_on = torch.full((n,), float("nan"), device=dev)
        h_next = torch.zeros(n, device=dev)
        h_p, h_n, h_pre = (torch.zeros(n, 2, device=dev) for _ in range(3))
        h_idx = torch.full((n,), -1, dtype=torch.long, device=dev)

        h_score = torch.full((n,), float("nan"), device=dev)
        h_best = torch.full((n,), float("nan"), device=dev)
        h_nfeas = torch.zeros(n, device=dev)

        def pick(mask):
            """The helper's contact for these envs: the rank_of-th best under the direct score."""
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
            srt, order = score.sort(-1, descending=True)
            rk = rank_of[e_].clamp(min=0, max=K - 1)
            best = srt[ar, rk]
            j = order[ar, rk]
            has = best > -1e8
            h_score[e_] = torch.where(has, best, torch.full_like(best, float("nan")))
            h_best[e_] = torch.where(srt[:, 0] > -1e8, srt[:, 0], torch.full_like(best, float("nan")))
            h_nfeas[e_] = (score > -1e8).float().sum(-1)
            changed = has & (j != h_idx[e_])
            h_idx[e_] = torch.where(has, j, h_idx[e_])
            h_p[e_] = torch.where(has.unsqueeze(-1), p[ar, j], h_p[e_])
            h_n[e_] = torch.where(has.unsqueeze(-1), nn[ar, j], h_n[e_])
            h_pre[e_] = torch.where(has.unsqueeze(-1), pre[ar, j], h_pre[e_])
            h_has[e_] = has | h_has[e_]
            if bool(changed.any()):
                ctrl.reset(torch.zeros(n, dtype=torch.bool, device=dev).index_fill_(0, e_[changed], True))

        def contact_scores(e_, p, nn):
            """Per-contact push score (m, K): the helper's direct score (push along the wanted motion + turning moment
            when a turn is wanted), and whether the contact may be used (never against the wanted motion)."""
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
            """All three robots' contacts together: maximise the summed push score of three distinct, separated
            contacts minus the expert's transition costs (time_weight x the slowest arrival, stop_weight per
            incumbent that leaves a contact it is pushing on). Keep / move one / move both are all candidates."""
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
            t1, t2 = prop["t_route"]
            # the helper's route: straight line to the contact's standing point / walk speed, x1.3 for going around
            yw = g.contact_frame_yaw()[e_]
            cs, sn = torch.cos(yw), torch.sin(yw)
            pw = g.box_pos()[e_, :2].unsqueeze(1) + torch.stack([cs.unsqueeze(1) * pre[..., 0] - sn.unsqueeze(1) * pre[..., 1],
                                                                  sn.unsqueeze(1) * pre[..., 0] + cs.unsqueeze(1) * pre[..., 1]], -1)
            th = 1.3 * torch.linalg.norm(pw - hr.data.root_link_pos_w[e_, :2].unsqueeze(1), dim=-1) / c_.walk_speed
            on = prop["on"]  # (m, 2) incumbents pushing on their contacts
            kk = torch.arange(K, device=dev)
            stop1 = ((kk.unsqueeze(0) != cur[:, :1]) & on[:, :1]).float()  # (m, K)
            stop2 = ((kk.unsqueeze(0) != cur[:, 1:2]) & on[:, 1:2]).float()
            T = (sc_[:, :, None, None] + sc_[:, None, :, None] + sc_[:, None, None, :]
                 - c_.time_weight * torch.maximum(torch.maximum(t1[:, :, None, None], t2[:, None, :, None]), th[:, None, None, :])
                 - c_.stop_weight * (stop1[:, :, None, None] + stop2[:, None, :, None]))
            feas = (use[:, :, :, None] & sep[:, :, None, :] & sep[:, None, :, :]
                    & ok_[:, :, None, None] & ok_[:, None, :, None] & ok_[:, None, None, :])
            feas &= (kk[:, None, None] != kk[None, None, :]).unsqueeze(0) & (kk[None, :, None] != kk[None, None, :]).unsqueeze(0)
            T = torch.where(feas, T, torch.full_like(T, -1e9))
            best, flat = T.view(m_, -1).max(-1)
            has = best > -1e8
            ia, ib, ic = flat // (K * K), (flat // K) % K, flat % K
            new = torch.where(has.unsqueeze(-1), torch.stack([ia, ib], -1), cur)
            j_moves[e_] += ((new != cur).any(-1) & has).float()
            g.c_need_more[e_] = prop["need_more"]
            g.apply_assignment(e_, new, p, nn, pre, prop["t_route"])
            changed = has & (ic != h_idx[e_])
            h_idx[e_] = torch.where(has, ic, h_idx[e_])
            h_p[e_] = torch.where(has.unsqueeze(-1), p[ar, ic], h_p[e_])
            h_n[e_] = torch.where(has.unsqueeze(-1), nn[ar, ic], h_n[e_])
            h_pre[e_] = torch.where(has.unsqueeze(-1), pre[ar, ic], h_pre[e_])
            h_has[e_] = has | h_has[e_]
            h_score[e_] = torch.where(has, best, h_score[e_])
            if bool(changed.any()):
                ctrl.reset(torch.zeros(n, dtype=torch.bool, device=dev).index_fill_(0, e_[changed], True))

        class JointCoordinator:
            """The env's re-plan events: joint twins after the branch -> joint_decide, every other env -> the expert."""
            def __call__(self, g_, ids_):
                jm = joint_on[ids_]
                joint_decide(ids_[jm])
                if bool((~jm).any()):
                    g_._reselect_expert(ids_[~jm])
        if a.joint:
            g.coordinator = JointCoordinator()

        dt = base.step_dt
        steps = int(a.horizon / dt)
        n_branch = int(round(a.branch_s / dt))
        idx_of = {tw: torch.tensor([j_ for j_, c in enumerate(cases) if c[0] == tw], device=dev) for tw in arms}
        src_of = {tw: idx_of["pair"] for tw in arms}
        dst_of = {tw: idx_of[tw] for tw in arms}
        done = torch.zeros(n, dtype=torch.bool, device=dev)
        hold = torch.zeros(n, device=dev)
        t_succ = torch.full((n,), float("nan"), device=dev)
        how = [""] * n
        fell = [torch.zeros(n, dtype=torch.bool, device=dev) for _ in AGENTS]
        film_ids = [j for j, c in enumerate(cases) if filmed(c) and mass in v_mass]
        fid = torch.tensor(film_ids, dtype=torch.long, device=dev) if film_ids else None
        stride = 2
        rec_q, rec_mp, rec_mq, rec_pts, rec_cap = [], [], [], [], []
        nmocap = base.sim.mj_model.nmocap

        def record():
            sd = base.sim.data
            rec_q.append(sd.qpos[fid].cpu().numpy().copy())
            if nmocap:
                rec_mp.append(sd.mocap_pos[fid].cpu().numpy().copy())
                rec_mq.append(sd.mocap_quat[fid].cpu().numpy().copy())
            pts = [r_.data.root_link_pos_w[fid, :2] for r_ in robots] + [g.box_pos()[fid, :2], g.goal_xy[fid]]
            rec_pts.append(np.stack([p_.cpu().numpy() for p_ in pts], 1))
            d_, e_ = g.errors()
            e_ = torch.where(g.symmetry() > 0, e_, torch.zeros_like(e_))
            mk = [torch.cat([g.contact_world(k_)[0], g.on_contact(k_).float().unsqueeze(-1)], -1) for k_ in range(2)]
            rec_cap.append(torch.stack([d_, torch.rad2deg(e_), h_on.float(), (ph & h_on).float(),
                                        g.current_strength(), *[x for m_ in mk for x in m_.unbind(-1)],
                                        *h_world().unbind(-1)], -1)[fid].cpu().numpy())
        ph = torch.zeros(n, dtype=torch.bool, device=dev)

        def h_world():  # the helper's contact point is kept in the object's contact frame
            yw = g.contact_frame_yaw()
            cs_, sn_ = torch.cos(yw), torch.sin(yw)
            return g.box_pos()[:, :2] + torch.stack([cs_ * h_p[:, 0] - sn_ * h_p[:, 1], sn_ * h_p[:, 0] + cs_ * h_p[:, 1]], -1)
        h_push_t = torch.zeros(n, device=dev)
        h_force = torch.zeros(n, device=dev)
        touch_t = torch.zeros(n, device=dev)
        live_t = torch.zeros(n, device=dev)
        last_d, last_e = g.errors()[0].clone(), torch.zeros(n, device=dev)
        pt, yt = 0.10, math.radians(6.0)
        t0 = time.time()
        feat = None
        with torch.no_grad():
            for i in range(steps):
                t = i * dt
                if fid is not None and i % stride == 0:
                    record()
                live = ~done
                if i == n_branch:  # ---- branch: copy the pair twin into every other twin, then dispatch ----
                    feat = {"strength": g.current_strength().clone(), "need_more": g.c_need_more.clone().float(),
                            "d": g.errors()[0].clone(), "e": g.errors()[1].abs().clone(),
                            "on1": g.on_contact(0).float().clone(), "on2": g.on_contact(1).float().clone(),
                            "done": done.clone()}
                    for tw in arms[1:]:
                        cnt = clone_envs(base, obs, src_of[tw], dst_of[tw])
                    for kk_, v_ in feat.items():
                        for tw in arms[1:]:
                            v_[dst_of[tw]] = v_[src_of[tw]]
                    for tw in arms[1:]:
                        done[dst_of[tw]] = done[src_of[tw]]
                        hold[dst_of[tw]] = hold[src_of[tw]]
                        t_succ[dst_of[tw]] = t_succ[src_of[tw]]
                        for q in range(len(AGENTS)):
                            fell[q][dst_of[tw]] = fell[q][src_of[tw]]
                        for jj_, kk2 in zip(dst_of[tw].tolist(), src_of[tw].tolist()):
                            how[jj_] = how[kk2]
                    live = ~done
                    hsel = is_helper & live
                    pick(hsel & ~is_joint)
                    go = hsel & ~is_joint & h_has
                    jsel = is_joint & live
                    if bool(go.any()):
                        e_ = go.nonzero().flatten()
                        bp = g.box_pos()[e_, :2]
                        u = g.goal_xy[e_] - bp
                        u = u / torch.linalg.norm(u, dim=-1, keepdim=True).clamp(min=1e-6)
                        lat = torch.stack([-u[:, 1], u[:, 0]], -1)
                        cen = 0.5 * (robots[0].data.root_link_pos_w[e_, :2] + robots[1].data.root_link_pos_w[e_, :2]) - bp
                        side = torch.where((cen * lat).sum(-1) >= 0, -1.0, 1.0).unsqueeze(-1)
                        pos = bp - a.stage_dist * u + 0.8 * side * lat
                        yw = torch.atan2(bp[:, 1] - pos[:, 1], bp[:, 0] - pos[:, 0])
                        st = torch.zeros(len(e_), 13, device=dev)
                        st[:, :2] = pos
                        st[:, 2] = hr.data.root_link_pos_w[e_, 2]
                        zz = torch.zeros(len(e_), device=dev)
                        st[:, 3:7] = quat_from_euler_xyz(zz, zz, yw)
                        hr.write_root_state_to_sim(st, e_)
                        h_on |= go
                        h_t_on = torch.where(go, torch.full_like(h_t_on, t), h_t_on)
                        present[2] = present[2] | go
                        if a.cap_mult != 1.0:
                            g.c_cap_mult[go] = a.cap_mult
                        ctrl.reset(go)
                    if bool(jsel.any()):  # joint twins: place the helper at staging, then plan all three contacts
                        e_ = jsel.nonzero().flatten()
                        bp = g.box_pos()[e_, :2]
                        u = g.goal_xy[e_] - bp
                        u = u / torch.linalg.norm(u, dim=-1, keepdim=True).clamp(min=1e-6)
                        lat = torch.stack([-u[:, 1], u[:, 0]], -1)
                        cen = 0.5 * (robots[0].data.root_link_pos_w[e_, :2] + robots[1].data.root_link_pos_w[e_, :2]) - bp
                        side = torch.where((cen * lat).sum(-1) >= 0, -1.0, 1.0).unsqueeze(-1)
                        pos = bp - a.stage_dist * u + 0.8 * side * lat
                        yw = torch.atan2(bp[:, 1] - pos[:, 1], bp[:, 0] - pos[:, 0])
                        st = torch.zeros(len(e_), 13, device=dev)
                        st[:, :2] = pos
                        st[:, 2] = hr.data.root_link_pos_w[e_, 2]
                        zz = torch.zeros(len(e_), device=dev)
                        st[:, 3:7] = quat_from_euler_xyz(zz, zz, yw)
                        hr.write_root_state_to_sim(st, e_)
                        joint_on[e_] = True
                        joint_decide(e_)
                        jgo = jsel & h_has
                        h_on |= jgo
                        h_t_on = torch.where(jgo, torch.full_like(h_t_on, t), h_t_on)
                        present[2] = present[2] | jgo
                        ctrl.reset(jgo)
                        go = go | jgo
                    print(f"  [{mass:g} kg] branch at {t:.1f} s ({cnt} tensors per copy): "
                          f"{int(feat['done'][src_of['pair']].sum())}/{len(base_cases)} tasks already ended; helper sent in "
                          f"{int(go.sum())}/{int(hsel.sum())} live helper twins", flush=True)
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
                         "robots_touch_frac": round(float(touch_t[j] / live_t[j].clamp(min=1e-6)), 3),
                         "ended_before_branch": int(bool(feat["done"][j])) if feat is not None else 1,
                         **({f"branch_{k_}": round(float(v_[j]), 3) for k_, v_ in feat.items() if k_ != "done"}
                            if feat is not None else {}),
                         "contact_score": "" if math.isnan(float(h_score[j])) else round(float(h_score[j]), 3),
                         "best_score": "" if math.isnan(float(h_best[j])) else round(float(h_best[j]), 3),
                         "n_feasible": int(h_nfeas[j]), "joint_incumbent_moves": int(j_moves[j])})
        if fid is not None:
            _film(a, base, cases, film_ids, how, t_succ, mass, dt * stride, rec_q, rec_mp, rec_mq, rec_pts, rec_cap, out)
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

    import numpy as np
    brng = np.random.default_rng(0)
    key = lambda r_: (r_["object"], r_["mass"], r_["scenario"], r_["rep"])  # noqa: E731
    by = {tw: {key(r_): r_ for r_ in rows if r_["arm"] == tw} for tw in arms}
    hr_arms = [tw for tw in arms if tw.startswith("h")]

    def ci(v):
        v = np.asarray(v, dtype=float)
        if len(v) == 0:
            return (float("nan"),) * 3
        bs = v[brng.integers(0, len(v), (2000, len(v)))].mean(1)
        return (100 * v.mean(), 100 * np.percentile(bs, 2.5), 100 * np.percentile(bs, 97.5))
    summ = {"arms": arms, "masses": masses, "seed": a.seed, "branch_s": a.branch_s, "stage_dist": a.stage_dist,
            "by_mass": {}}
    md = [f"# Third robot by branching: {a.prefix}", "",
          f"Seed {a.seed}, {len(base_cases)} tasks per mass, branch at {a.branch_s:g} s, helper staged {a.stage_dist:g} m "
          f"behind; pair = the planner pair continues (abstain); null = the same, a noise floor; h<r> = helper to the "
          f"r-th best third contact. Tasks that ended before the branch are excluded. Rescue = pair fails and the twin "
          f"succeeds; disruption = the reverse; net = rescue - disruption (pp, 95% paired bootstrap over tasks).", ""]
    for m in masses + ["all"]:
        ks = [k_ for k_, r_ in by["pair"].items() if (m == "all" or r_["mass"] == m) and not r_["ended_before_branch"]]
        if not ks:
            continue
        ent = {"branched": len(ks), "pair_success": 100 * float(np.mean([by["pair"][k_]["success"] for k_ in ks]))}
        md += [f"## {m if m == 'all' else f'{m:g} kg'}: {len(ks)} branched tasks, pair success {ent['pair_success']:.0f}%", "",
               "| twin | success | rescue | disruption | net [95% CI] |", "|---|---|---|---|---|"]
        cols = [tw for tw in arms if tw != "pair"] + ["best_rank"]
        for tw in cols:
            if tw == "best_rank":
                ys = [max(by[h][k_]["success"] for h in hr_arms) for k_ in ks]
            else:
                ys = [by[tw][k_]["success"] for k_ in ks]
            y0 = [by["pair"][k_]["success"] for k_ in ks]
            resc = [int(b and not a_) for a_, b in zip(y0, ys)]
            disr = [int(a_ and not b) for a_, b in zip(y0, ys)]
            net = ci([r_ - d_ for r_, d_ in zip(resc, disr)])
            ent[tw] = {"success": 100 * float(np.mean(ys)), "rescue": 100 * float(np.mean(resc)),
                       "disruption": 100 * float(np.mean(disr)), "net": list(net)}
            md.append(f"| {tw} | {ent[tw]['success']:.0f}% | {ent[tw]['rescue']:.1f}% | {ent[tw]['disruption']:.1f}% | "
                      f"{net[0]:+.1f} [{net[1]:+.1f}, {net[2]:+.1f}] |")
        md.append("")
        summ["by_mass"][str(m)] = ent
    hx = [x for x in rows if x["arm"].startswith("h") and not x["ended_before_branch"]]
    if hx:
        md += [f"Helper twins: helper fell in {sum(x[f'fell_{H}'] for x in hx)} of {len(hx)}; mean push time "
               f"{np.mean([x['helper_push_s'] for x in hx]):.1f} s; robots touching {100 * np.mean([x['robots_touch_frac'] for x in hx]):.0f}% "
               f"of live time (pair twins: {100 * np.mean([x['robots_touch_frac'] for x in rows if x['arm'] == 'pair']):.0f}%)."]
    (out / "summary.md").write_text("\n".join(md) + "\n")
    (out / "summary.json").write_text(json.dumps(summ, indent=1))
    stats.mkdir(parents=True, exist_ok=True)
    for f in ("summary.md", "summary.json", "episodes.csv"):
        shutil.copy2(out / f, stats / f)
    print("\n".join(md))
    return 0


if __name__ == "__main__":
    sys.exit(main())
