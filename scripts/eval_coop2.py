"""Evaluate two-robot (or single-robot) pushing on the same fixed tasks.

    python scripts/eval_coop2.py --name pair-frozen --frozen-pair            # the two Stage 2b policies, untrained together
    python scripts/eval_coop2.py --name solo-anymal --solo anymal            # ANYmal's Stage 2b policy alone (Spot parked far away)
    python scripts/eval_coop2.py --name solo-spot   --solo spot
    python scripts/eval_coop2.py --name mappo-s0 --checkpoint logs/marl2/mappo_s0/model_6000.pt
    python scripts/eval_coop2.py --name pair-frozen-anymal --frozen-pair --pair anymal   # two ANYmal C

The pair (which two robots, quadcoop/coop2/pairs.py) comes from the checkpoint; for the frozen
pair and solo runs it is --pair (default mixed). --solo takes a slot name of that pair (anymal /
spot for mixed, anymal1 / anymal2 for two ANYmal, ...).

Tasks (same for every policy): every object (7 trained + 5 held out, nominal sizes) x mass
(--masses, default 20,40,60,80 kg: one env build each) x scenario x --reps placements. The object
starts at the origin, both robots behind it (180 deg +- 35 deg, jittered per rep), facing it:

    A_straight   goal 3 m ahead, no turn
    B_left       goal 3 m at 60 deg left, turned +30 deg
    C_backright  goal 3 m at 135 deg right (the robots have to go around), turned -60 deg
    D_far_turn   goal 5 m ahead, turned 90 deg (capped by the shape's symmetry, as in training)

Success (as the single-robot h80 suite): object within 10 cm / 6 deg for 1 s within --horizon
(80 s); "precise" = the training rule (10 cm / 3 deg with the object at rest) reached at some
point. An episode ends at success, a fall (either robot), the object tipping or being lost.
Also recorded: which robot fell, how often the robots touch, their closest approach.

Output: logs/evals/<name>/pair/ (episodes.csv, summary.md/json, videos/: one per object at
--video-mass, the first success else the first failure); the stats are copied to
evals/<name>/eval/pair/ for the repo. Models: from the checkpoint's own record (trained pairs) or
evals/models.yaml (frozen pair / solo).
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
import shutil
import sys
import time
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT))

SCENARIOS = (  # name, distance (m), direction (deg, + = left, 0 = straight ahead of the robots), turn (deg)
    ("A_straight", 3.0, 0.0, 0.0),
    ("B_left", 3.0, 60.0, 30.0),
    ("C_backright", 3.0, -135.0, -60.0),
    ("D_far_turn", 5.0, 0.0, 90.0),
)


def models_for(a) -> tuple[dict, str]:
    """Resolved models (walkers + Stage 2 policies) and a description of the policy."""
    import torch

    from methods import load, resolve
    from train_coop2 import _pairs, resolve_models, robot_of

    role_of = _pairs().ROLE
    if a.checkpoint:
        ck = torch.load(a.checkpoint, map_location="cpu", weights_only=False)
        cfg = ck.get("cfg", {})
        sel = cfg.get("inputs") or {}
        variant = ck.get("variant", "b")
        pair = cfg.get("pair", "mixed")
        what = f"checkpoint {a.checkpoint} (iteration {ck['iter']}, {ck['algo']}, pair {pair})"
        if not sel:
            return resolve_models(variant, pair), what
        reg = load()
        out = {"selection": sel, "walker_ckpt": {}, "walker_env": {}, "policy": {}, "pair": pair}
        for ag, robot in robot_of(pair).items():
            role = role_of[robot]
            w = resolve(sel[f"walker_{role}"], reg)
            out["walker_ckpt"][robot] = w["checkpoint_abs"]
            out["walker_env"][robot] = dict(w["env_all"])
            out["policy"][ag] = resolve(sel[f"push2{variant}_{role}"], reg)["checkpoint_abs"]
        return out, what
    m = resolve_models(a.variant, a.pair)
    slots = robot_of(a.pair)
    if a.solo and a.solo not in slots:
        raise SystemExit(f"--solo {a.solo}: the {a.pair} pair's robots are {list(slots)}")
    pol = lambda x: m["selection"][f"push2{a.variant}_{role_of[slots[x]]}"]  # noqa: E731
    return m, (f"{a.solo} alone ({pol(a.solo)})" if a.solo else
               f"frozen pair ({a.pair}): " + " + ".join(pol(x) for x in slots))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True, help="output id: logs/evals/<name>/pair, evals/<name>/eval/pair")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--checkpoint", help="a train_coop2.py model_<iter>.pt")
    src.add_argument("--frozen-pair", action="store_true", help="the two Stage 2 policies, untrained together")
    src.add_argument("--solo", help="one robot's Stage 2 policy, the other parked (a slot name: anymal / spot, ...)")
    ap.add_argument("--pair", choices=("mixed", "anymal", "spot"), default="mixed",
                    help="frozen pair / solo: which two robots (a checkpoint carries its own)")
    ap.add_argument("--variant", choices=("b", "ctrl"), default="b")
    ap.add_argument("--partner-map", action="store_true",
                    help="frozen pair / solo: build the env with the partner map (no effect on those policies)")
    ap.add_argument("--objects", default="all")
    ap.add_argument("--masses", default="20,40,60,80")
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--horizon", type=float, default=80.0)
    ap.add_argument("--videos", type=int, default=1, help="1 = one video per object at --video-mass, 0 = none")
    ap.add_argument("--video-mass", type=float, default=None, help="default: the heaviest mass below 70 kg")
    ap.add_argument("--video-size", default="640x480")
    ap.add_argument("--device", default=None)
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()

    from train_coop2 import set_env

    models, what = models_for(a)
    set_env(models)
    import numpy as np
    import torch
    from tensordict import TensorDict

    import quadcoop  # noqa: F401
    from mjlab.envs import ManagerBasedRlEnv

    from quadcoop import falls
    from quadcoop.coop2 import mdp as cm
    from quadcoop.coop2.env_cfg import SPECS, make_coop2_env_cfg
    from quadcoop.coop2.marl import PairPolicy
    from quadcoop.coop2.mdp import AGENTS
    from quadcoop.coop2.video import Camera, render_episode
    from quadcoop.stage1.mdp import wrap
    from quadcoop.stage1b import mdp as hb
    from quadcoop.stage1b.shapes import NOMINAL_MASS
    from quadcoop.stage2 import mdp as m2
    from quadcoop.stage2.shapes import OBJ_NAMES2, SHAPE_NAMES2, SHAPES2, TRAIN_NAMES

    device = a.device or ("cuda:0" if torch.cuda.is_available() else "cpu")
    variant, partner_map, reward_set = a.variant, a.partner_map, "r3"
    if a.checkpoint:
        ck_ = torch.load(a.checkpoint, map_location="cpu", weights_only=False)
        variant = ck_.get("variant", "b")
        partner_map = bool(ck_.get("cfg", {}).get("partner_map", False))
        reward_set = ck_.get("cfg", {}).get("reward_set", "r3")
        del ck_
    objects = list(SHAPE_NAMES2) if a.objects == "all" else [o.strip() for o in a.objects.split(",")]
    masses = [float(x) for x in a.masses.split(",")]
    video_mass = a.video_mass if a.video_mass is not None else max([m for m in masses if m < 70] or masses[:1])
    vw, vh = (int(x) for x in a.video_size.lower().split("x"))
    out = ROOT / "logs" / "evals" / a.name / "pair"
    stats_dir = ROOT / "evals" / a.name / "eval" / "pair"
    out.mkdir(parents=True, exist_ok=True)
    cases = [(o, s, r) for o in objects for s in range(len(SCENARIOS)) for r in range(a.reps)]
    n = len(cases)
    print(f"{what}\n{len(objects)} objects x {len(SCENARIOS)} scenarios x {a.reps} reps = {n} episodes per mass; "
          f"masses {masses}", flush=True)
    rows: list[dict] = []
    t_start = time.time()

    for mass in masses:
        cfg = make_coop2_env_cfg(variant, play=True, partner_map=partner_map, reward_set=reward_set)
        cfg.scene.num_envs = n
        cfg.episode_length_s = 1e5
        cfg.terminations = {}
        alpha = 0.5 * math.log(mass / NOMINAL_MASS)
        for name in OBJ_NAMES2:
            cfg.events[f"{name}_mass"].params["alpha_range"] = (alpha, alpha)
        torch.manual_seed(a.seed)
        base = ManagerBasedRlEnv(cfg=cfg, device=device)
        g = base.command_manager.get_term("goal")
        dev = base.device
        ids = torch.arange(n, device=dev)
        for k in range(len(SHAPES2)):  # nominal sizes
            m2.apply_geometry(base, ids, k, torch.ones(n, 3, device=dev))

        # the scenario each env gets at the next reset
        rng = random.Random(f"{a.seed}-coop2")
        obj_idx = torch.tensor([SHAPE_NAMES2.index(o) for o, _, _ in cases], device=dev)
        dist = torch.tensor([SCENARIOS[s][1] for _, s, _ in cases], device=dev)
        gdir = torch.deg2rad(torch.tensor([SCENARIOS[s][2] for _, s, _ in cases], device=dev))
        turn = torch.deg2rad(torch.tensor([SCENARIOS[s][3] for _, s, _ in cases], device=dev))
        sym = g.sym[obj_idx]
        cap = torch.where(sym > 0, (math.pi / sym.clamp(min=1)) * g.cfg.max_yaw_frac_of_symmetry, torch.zeros_like(sym))
        turn = torch.sign(turn) * torch.minimum(turn.abs(), cap)
        jit = torch.tensor([[rng.uniform(-10, 10) for _ in AGENTS] for _ in cases], device=dev)
        gap = torch.tensor([[rng.uniform(0.3, 0.6) for _ in AGENTS] for _ in cases], device=dev)
        bearings = [math.pi + torch.deg2rad(sgn * 35.0 + jit[:, k]) for k, sgn in enumerate((-1.0, 1.0))]
        park = [torch.full((n,), a.solo is not None and ag != a.solo, dtype=torch.bool, device=dev) for ag in AGENTS]
        z = torch.zeros(n, device=dev)
        sc = {"shape": obj_idx, "obj_xy_rel": torch.zeros(n, 2, device=dev), "obj_heading": z.clone(),
              "goal_xy_rel": dist.unsqueeze(-1) * torch.stack([torch.cos(gdir), torch.sin(gdir)], -1),
              "goal_yaw": wrap(turn), "bearings": bearings, "gaps": [gap[:, 0], gap[:, 1]], "yaw_noise": [z, z],
              "park": park}
        g.scenario = lambda env_ids: {k: ([x[env_ids] for x in v] if isinstance(v, list) else v[env_ids])
                                      for k, v in sc.items()}
        obs, _ = base.reset()
        g.scenario = None
        obs = TensorDict({k: v for k, v in obs.items() if not k.startswith("walker_")}, batch_size=[n])
        policy = PairPolicy(obs, device, variant, checkpoint=a.checkpoint,
                            singles=None if a.checkpoint else models["policy"])
        active = [ag for ag in AGENTS if a.solo is None or ag == a.solo]

        dt = base.step_dt
        steps = int(a.horizon / dt)
        film = a.videos > 0 and mass == video_mass
        stride = 2
        rec_q, rec_mp, rec_mq, rec_pts = [], [], [], []
        nmocap = base.sim.mj_model.nmocap

        def record():
            sd = base.sim.data
            rec_q.append(sd.qpos.cpu().numpy().copy())
            if nmocap:
                rec_mp.append(sd.mocap_pos.cpu().numpy().copy())
                rec_mq.append(sd.mocap_quat.cpu().numpy().copy())
            rec_pts.append(np.stack([base.scene[x].data.root_link_pos_w[:, :2].cpu().numpy() for x in AGENTS]
                                    + [g.box_pos()[:, :2].cpu().numpy(), g.goal_xy.cpu().numpy()], 1))
        if film:
            record()

        done = torch.zeros(n, dtype=torch.bool, device=dev)
        how = ["horizon"] * n
        t_succ = torch.full((n,), float("nan"), device=dev)
        t_end = torch.full((n,), a.horizon, device=dev)
        fell = {ag: torch.zeros(n, dtype=torch.bool, device=dev) for ag in AGENTS}
        precise = torch.zeros(n, dtype=torch.bool, device=dev)
        hold = torch.zeros(n, device=dev)
        touch_steps = torch.zeros(n, device=dev)
        live_steps = torch.zeros(n, device=dev)
        min_rd = torch.full((n,), 1e9, device=dev)
        d0, _ = g.errors()
        last_d, last_e, min_d = d0.clone(), torch.zeros(n, device=dev), d0.clone()
        pt, yt = 0.10, math.radians(6.0)
        all_done_at = None
        tail = int(2.0 / dt)
        with torch.no_grad():
            for i in range(steps):
                act = policy(obs)
                for k, ag in enumerate(AGENTS):
                    if ag not in active:
                        act[:, 3 * k:3 * k + 3] = 0.0
                o, _, _, _, _ = base.step(act)
                obs = TensorDict({k: v for k, v in o.items() if not k.startswith("walker_")}, batch_size=[n])
                t = (i + 1) * dt
                live = ~done
                f_any = torch.zeros(n, dtype=torch.bool, device=dev)
                for ag in active:
                    f = falls.fallen(base, asset_name=ag, nominal_height=SPECS[ag].nominal_height) & live
                    fell[ag] |= f
                    f_any |= f
                tip = hb.box_tipped(base) & live & ~f_any
                lost = cm.box_lost(base) & live & ~f_any & ~tip
                d, e = g.errors()
                ea = e.abs()
                ok = live & ~f_any & ~tip & ~lost
                last_d = torch.where(ok, d, last_d)
                last_e = torch.where(ok, ea, last_e)
                min_d = torch.where(ok, torch.minimum(min_d, d), min_d)
                precise |= ok & g.success_flag
                inside = ok & (d < pt) & (ea < yt)
                hold = torch.where(inside, hold + dt, torch.zeros_like(hold))
                succ = ok & (hold >= 1.0)
                t_succ = torch.where(succ, torch.full_like(t_succ, t), t_succ)
                if a.solo is None:
                    touch_steps += (cm.robots_touching(base) > 0).float() * live.float()
                    rd = torch.linalg.norm(base.scene[AGENTS[0]].data.root_link_pos_w[:, :2]
                                           - base.scene[AGENTS[1]].data.root_link_pos_w[:, :2], dim=-1)
                    min_rd = torch.where(live, torch.minimum(min_rd, rd), min_rd)
                live_steps += live.float()
                for j in f_any.nonzero().flatten().tolist():
                    how[j] = "fell_" + "+".join(ag for ag in active if bool(fell[ag][j]))
                for j in tip.nonzero().flatten().tolist():
                    how[j] = "tipped"
                for j in lost.nonzero().flatten().tolist():
                    how[j] = "lost"
                for j in succ.nonzero().flatten().tolist():
                    how[j] = "success"
                ended = f_any | tip | lost | succ
                t_end = torch.where(ended & ~done, torch.full_like(t_end, t), t_end)
                done |= ended
                if film and (i + 1) % stride == 0:
                    record()
                if all_done_at is None and bool(done.all()):
                    all_done_at = i
                if all_done_at is not None and i >= all_done_at + tail:
                    break

        mine = []
        for j, (o, s, r) in enumerate(cases):
            row = {"object": o, "seen_shape": int(o in TRAIN_NAMES), "mass": mass, "scenario": SCENARIOS[s][0],
                   "distance": SCENARIOS[s][1], "direction": SCENARIOS[s][2],
                   "turn": round(math.degrees(float(turn[j])), 1), "rep": r,
                   "success": int(how[j] == "success"), "precise": int(bool(precise[j])), "outcome": how[j],
                   "t_success": round(float(t_succ[j]), 2) if how[j] == "success" else "",
                   **{f"fell_{ag}": int(bool(fell[ag][j])) for ag in AGENTS},
                   "final_pos_err": round(float(last_d[j]), 3), "final_yaw_err": round(math.degrees(float(last_e[j])), 1),
                   "min_pos_err": round(float(min_d[j]), 3),
                   "touch_frac": round(float(touch_steps[j] / live_steps[j].clamp(min=1)), 3) if a.solo is None else "",
                   "min_robot_dist": round(float(min_rd[j]), 2) if a.solo is None else "", "video": ""}
            mine.append(row)
        if film:
            try:
                cam = Camera(base, vw, vh)
                Q, P = np.stack(rec_q, 1), np.stack(rec_pts, 1)  # (n, F, ...)
                MP = np.stack(rec_mp, 1) if rec_mp else None
                MQ = np.stack(rec_mq, 1) if rec_mq else None
                for o in objects:
                    js = [j for j, c in enumerate(cases) if c[0] == o]
                    wins = [j for j in js if how[j] == "success"]
                    j = wins[0] if wins else js[0]
                    F = min(Q.shape[1], int(float(t_end[j]) / (stride * dt)) + int(1.0 / (stride * dt)) + 1)
                    r_ = mine[j]
                    name = f"{o}_{mass:g}kg_{r_['scenario']}__{how[j]}.mp4"
                    cap_txt = f"{o} {mass:g} kg {r_['scenario']} (turn {r_['turn']:g}) -> {how[j]}"
                    render_episode(cam, j, Q[j, :F], None if MP is None else MP[j, :F], None if MQ is None else MQ[j, :F],
                                   P[j, :F], out / "videos" / name, 1.0 / (stride * dt),
                                   caption=lambda f, c=cap_txt: f"{c}   t = {f * stride * dt:5.1f} s")
                    r_["video"] = f"videos/{name}"
            except Exception as ex:  # noqa: BLE001
                print(f"videos skipped: {ex}")
        rows += mine
        sr = sum(r["success"] for r in mine) / len(mine)
        falls_txt = "  ".join(f"{ag} {sum(r[f'fell_{ag}'] for r in mine) / len(mine):.2f}" for ag in AGENTS)
        print(f"[{mass:g} kg] success {sr:.2f}  falls {falls_txt}  ({time.time() - t_start:.0f} s)", flush=True)
        base.close()
        del base

    # -- summary --------------------------------------------------------------------------------------
    with open(out / "episodes.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    def agg(sel):
        k = len(sel)
        if not k:
            return None
        ok = [r for r in sel if r["success"]]
        return {"n": k, "success": sum(r["success"] for r in sel) / k, "precise": sum(r["precise"] for r in sel) / k,
                **{f"fell_{ag}": sum(r[f"fell_{ag}"] for r in sel) / k for ag in AGENTS},
                "t_success": (sum(r["t_success"] for r in ok) / len(ok)) if ok else None,
                "touch_frac": (sum(r["touch_frac"] for r in sel) / k) if a.solo is None else None}

    by = defaultdict(list)
    for r in rows:
        by[("mass", r["mass"])].append(r)
        by[("obj_mass", r["object"], r["mass"])].append(r)
        by[("group_mass", "seen" if r["seen_shape"] else "unseen", r["mass"])].append(r)
        by[("scen_mass", r["scenario"], r["mass"])].append(r)
    summary = {"policy": what, "name": a.name, "agents": list(AGENTS), "masses": masses, "reps": a.reps,
               "horizon_s": a.horizon,
               "overall": agg(rows),
               "by_mass": {f"{m:g}": agg(by[("mass", m)]) for m in masses},
               "by_group_mass": {f"{gname} / {m:g} kg": agg(by[("group_mass", gname, m)])
                                 for gname in ("seen", "unseen") for m in masses},
               "by_object_mass": {f"{o} / {m:g} kg": agg(by[("obj_mass", o, m)]) for o in objects for m in masses},
               "by_scenario_mass": {f"{s[0]} / {m:g} kg": agg(by[("scen_mass", s[0], m)]) for s in SCENARIOS for m in masses}}
    (out / "summary.json").write_text(json.dumps(summary, indent=1))
    f2 = lambda x: "" if x is None else f"{x:.2f}"  # noqa: E731
    md = [f"# Pair evaluation: {a.name}", "", f"policy: {what}", "",
          f"success = 10 cm / 6 deg held 1 s within {a.horizon:g} s; precise = 10 cm / 3 deg with the object at rest "
          f"(the training rule); {a.reps} placements per object x scenario x mass; nominal object sizes", "",
          "## by mass", "", f"| mass | success | precise | {AGENTS[0]} fell | {AGENTS[1]} fell | time to success (s) | robots touching |",
          "|---|---|---|---|---|---|---|"]
    for m in masses:
        s = summary["by_mass"][f"{m:g}"]
        md.append(f"| {m:g} kg | {f2(s['success'])} | {f2(s['precise'])} | {f2(s[f'fell_{AGENTS[0]}'])} | {f2(s[f'fell_{AGENTS[1]}'])} | "
                  f"{'' if s['t_success'] is None else f'{s['t_success']:.1f}'} | {f2(s['touch_frac'])} |")
    md += ["", "## success by object and mass", "", "| object | " + " | ".join(f"{m:g} kg" for m in masses) + " |",
           "|---|" + "---|" * len(masses)]
    for o in objects:
        md.append(f"| {o}{'' if o in TRAIN_NAMES else ' (unseen)'} | "
                  + " | ".join(f2(summary["by_object_mass"][f"{o} / {m:g} kg"]["success"]) for m in masses) + " |")
    md += ["", "## success by scenario and mass", "", "| scenario | " + " | ".join(f"{m:g} kg" for m in masses) + " |",
           "|---|" + "---|" * len(masses)]
    for s in SCENARIOS:
        md.append(f"| {s[0]} | " + " | ".join(f2(summary["by_scenario_mass"][f"{s[0]} / {m:g} kg"]["success"])
                                             for m in masses) + " |")
    (out / "summary.md").write_text("\n".join(md) + "\n")
    stats_dir.mkdir(parents=True, exist_ok=True)
    for f in ("summary.md", "summary.json", "episodes.csv"):
        shutil.copy2(out / f, stats_dir / f)
    print("\n".join(md))
    print(f"\nstats in {stats_dir}\nvideos and full output in {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
