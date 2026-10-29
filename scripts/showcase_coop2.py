"""Per-object videos of a two-robot policy, to look at what the pair actually does.

    python scripts/showcase_coop2.py --name mappo_aa_kl --checkpoint logs/marl2/mappo_aa_kl_s0/model_3000.pt
    python scripts/showcase_coop2.py --name pair_frozen_aa --frozen-pair --pair anymal      # untrained 2b pair
    python scripts/showcase_coop2.py --name solo_anymal --solo anymal1 --pair anymal       # one 2b ANYmal
    python scripts/showcase_coop2.py --compare pair_frozen_aa,mappo_aa_kl,ippo_aa_kl,solo_anymal --name cmp_aa

Every object x mass x goal scenario is run with up to 3 attempts that differ only by a small,
fixed perturbation of the object's start (the same for every policy, so all policies face
identical tasks). The first successful attempt is filmed; if all 3 fail, attempt 1 is filmed.
Objects use their nominal size; both robots start behind the object (180 deg +- 35 deg), as in
scripts/eval_coop2.py.

    A_straight   goal 2.5 m straight ahead, no turn
    B_left       goal 3 m at 60 deg to the left, turned +30 deg
    C_backright  goal 3 m at 135 deg to the right (the robots have to go around), turned -60 deg
    D_far_turn   goal 5 m ahead, turned 90 deg
(turns capped by each shape's symmetry, as in training). Success: 10 cm / 6 deg held 1 s within
--horizon s; a fall of either robot, the object tipping or being lost ends the attempt.

Output (eval_videos/ is git-ignored):
    eval_videos/<name>/<object>/<mass>kg/<scenario>__<outcome>.mp4
    eval_videos/<name>/index.html      grid: objects x masses, the scenario videos in each cell
    eval_videos/<name>/showcase.csv    one row per object x mass x scenario (copied with showcase.md
                                       to evals/<name>/eval/showcase/ for the repo)
--compare a,b,...: no simulation; eval_videos/<name>.html puts those showcases side by side, one
row per object x mass x scenario (run the showcases with the same --masses first).
Captions: time, distance / heading error to the goal, and each robot's state.
"""

from __future__ import annotations

import argparse
import csv
import html
import math
import shutil
import sys
import time
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT))

OUT_ROOT = ROOT / "eval_videos"
SCENARIOS = (  # name, distance (m), direction (deg, + = left), turn (deg)
    ("A_straight", 2.5, 0.0, 0.0),
    ("B_left", 3.0, 60.0, 30.0),
    ("C_backright", 3.0, -135.0, -60.0),
    ("D_far_turn", 5.0, 0.0, 90.0),
)
ATTEMPTS = ((0.0, 0.0), (0.15, 7.0), (-0.15, -7.0))  # object start: lateral offset (m), yaw (deg)


def compare(names: list[str], out_name: str) -> int:
    """eval_videos/<out_name>.html: the showcases side by side."""
    data = {}
    for nm in names:
        f = OUT_ROOT / nm / "showcase.csv"
        if not f.exists():
            raise SystemExit(f"{f} not found: run the showcase for {nm} first")
        data[nm] = {(r["object"], float(r["mass"]), r["scenario"]): r for r in csv.DictReader(open(f))}
    keys = list(dict.fromkeys(k for nm in names for k in data[nm]))
    keys.sort(key=lambda k: (k[0], k[1], [s[0] for s in SCENARIOS].index(k[2]) if k[2] in [s[0] for s in SCENARIOS] else 9))
    tot = {nm: sum(r["outcome"] == "success" for r in data[nm].values()) for nm in names}
    h = ["<html><head><meta charset='utf-8'><title>" + html.escape(out_name) + "</title><style>"
         "body{font-family:sans-serif;background:#111;color:#ddd;margin:12px}td{vertical-align:top;padding:4px}"
         "th{position:sticky;top:0;background:#222}video{width:320px}.S{color:#7e7}.F{color:#f97}"
         "tr.obj td{border-top:2px solid #555}</style></head><body>",
         f"<h1>{html.escape(out_name)}</h1><p>Same tasks for every policy; first successful attempt of 3 "
         "(else attempt 1). Totals: " + ", ".join(f"{html.escape(nm)} {tot[nm]}/{len(data[nm])}" for nm in names) +
         "</p><table><tr><th>task</th>" + "".join(f"<th>{html.escape(nm)}</th>" for nm in names) + "</tr>"]
    last_obj = None
    for k in keys:
        o, m, s = k
        h.append(f"<tr class='{'obj' if o != last_obj else ''}'><td><b>{o}</b><br>{m:g} kg<br>{s}</td>")
        last_obj = o
        for nm in names:
            r = data[nm].get(k)
            if r is None:
                h.append("<td></td>")
                continue
            c = "S" if r["outcome"] == "success" else "F"
            t = f", {r['t_success']} s" if r.get("t_success") else ""
            h.append(f"<td><div class='{c}'>{r['outcome']} ({r['attempts_succeeded']}{t})</div>"
                     f"<video controls preload='none' src='{nm}/{r['video']}'></video></td>")
        h.append("</tr>")
    h.append("</table></body></html>")
    OUT_ROOT.mkdir(exist_ok=True)
    (OUT_ROOT / f"{out_name}.html").write_text("\n".join(h))
    print(f"comparison: {OUT_ROOT / (out_name + '.html')}  (" + ", ".join(f"{nm} {tot[nm]}" for nm in names) + ")")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True, help="folder under eval_videos/ (or the comparison page with --compare)")
    src = ap.add_mutually_exclusive_group()
    src.add_argument("--checkpoint", help="a train_coop2.py model_<iter>.pt")
    src.add_argument("--frozen-pair", action="store_true", help="the two Stage 2 policies, untrained together")
    src.add_argument("--compare", help="comma list of existing showcase names: build a side-by-side page only")
    ap.add_argument("--solo", help="only this robot acts (slot name), the other is parked far away")
    ap.add_argument("--pair", choices=("mixed", "anymal", "spot"), default="mixed",
                    help="frozen pair / solo: which two robots (a checkpoint carries its own)")
    ap.add_argument("--variant", choices=("b", "ctrl"), default="b")
    ap.add_argument("--partner-map", action="store_true", help="frozen pair / solo: env with the partner map")
    ap.add_argument("--objects", default="all")
    ap.add_argument("--masses", default="40,60,80")
    ap.add_argument("--scenarios", default="A_straight,B_left,C_backright,D_far_turn")
    ap.add_argument("--horizon", type=float, default=80.0)
    ap.add_argument("--video-size", default="640x480")
    ap.add_argument("--device", default=None)
    a = ap.parse_args()
    if a.compare:
        return compare([x.strip() for x in a.compare.split(",") if x.strip()], a.name)
    if not (a.checkpoint or a.frozen_pair or a.solo):
        ap.error("give --checkpoint, --frozen-pair, --solo or --compare")
    if a.frozen_pair and a.solo:
        ap.error("--frozen-pair and --solo exclude each other")

    from eval_coop2 import models_for
    from train_coop2 import set_env

    models, what = models_for(a)
    set_env(models)
    import numpy as np
    import torch
    from tensordict import TensorDict

    import quadcoop  # noqa: F401
    from mjlab.envs import ManagerBasedRlEnv

    from methods import EVALS
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
    scen = [s for s in SCENARIOS if s[0] in [x.strip() for x in a.scenarios.split(",")]]
    vw, vh = (int(x) for x in a.video_size.lower().split("x"))
    out = OUT_ROOT / a.name
    out.mkdir(parents=True, exist_ok=True)
    cases = [(o, s, k) for o in objects for s in range(len(scen)) for k in range(len(ATTEMPTS))]
    n = len(cases)
    active = [ag for ag in AGENTS if a.solo is None or ag == a.solo]
    print(f"{what}\n{len(objects)} objects x {len(scen)} scenarios x {len(ATTEMPTS)} attempts = {n} envs per mass; "
          f"masses {masses}", flush=True)
    rows: list[dict] = []
    t0 = time.time()

    for mass in masses:
        cfg = make_coop2_env_cfg(variant, play=True, partner_map=partner_map, reward_set=reward_set)
        cfg.scene.num_envs = n
        cfg.episode_length_s = 1e5
        cfg.terminations = {}
        alpha = 0.5 * math.log(mass / NOMINAL_MASS)
        for name in OBJ_NAMES2:
            cfg.events[f"{name}_mass"].params["alpha_range"] = (alpha, alpha)
        torch.manual_seed(0)
        base = ManagerBasedRlEnv(cfg=cfg, device=device)
        g = base.command_manager.get_term("goal")
        dev = base.device
        ids = torch.arange(n, device=dev)
        for k in range(len(SHAPES2)):  # nominal sizes
            m2.apply_geometry(base, ids, k, torch.ones(n, 3, device=dev))

        obj_idx = torch.tensor([SHAPE_NAMES2.index(o) for o, _, _ in cases], device=dev)
        dist = torch.tensor([scen[s][1] for _, s, _ in cases], device=dev)
        gdir = torch.deg2rad(torch.tensor([scen[s][2] for _, s, _ in cases], device=dev))
        turn = torch.deg2rad(torch.tensor([scen[s][3] for _, s, _ in cases], device=dev))
        sym = g.sym[obj_idx]
        cap = torch.where(sym > 0, (math.pi / sym.clamp(min=1)) * g.cfg.max_yaw_frac_of_symmetry, torch.zeros_like(sym))
        turn = torch.sign(turn) * torch.minimum(turn.abs(), cap)
        at = torch.tensor([ATTEMPTS[k] for _, _, k in cases], device=dev, dtype=torch.float)
        z = torch.zeros(n, device=dev)
        # the goal is defined from the unperturbed start, so every attempt has the same goal
        sc = {"shape": obj_idx, "obj_xy_rel": torch.stack([z, at[:, 0]], -1), "obj_heading": torch.deg2rad(at[:, 1]),
              "goal_xy_rel": dist.unsqueeze(-1) * torch.stack([torch.cos(gdir), torch.sin(gdir)], -1),
              "goal_yaw": wrap(turn),
              "bearings": [torch.full((n,), math.pi + math.radians(sg * 35.0), device=dev) for sg in (-1.0, 1.0)],
              "gaps": [torch.full((n,), 0.45, device=dev) for _ in AGENTS], "yaw_noise": [z, z],
              "park": [torch.full((n,), a.solo is not None and ag != a.solo, dtype=torch.bool, device=dev)
                       for ag in AGENTS]}
        g.scenario = lambda env_ids: {k: ([x[env_ids] for x in v] if isinstance(v, list) else v[env_ids])
                                      for k, v in sc.items()}
        obs, _ = base.reset()
        g.scenario = None
        obs = TensorDict({k: v for k, v in obs.items() if not k.startswith("walker_")}, batch_size=[n])
        policy = PairPolicy(obs, device, variant, checkpoint=a.checkpoint,
                            singles=None if a.checkpoint else models["policy"])

        dt = base.step_dt
        steps = int(a.horizon / dt)
        stride = 2
        rec_q, rec_mp, rec_mq, rec_pts, rec_info = [], [], [], [], []
        nmocap = base.sim.mj_model.nmocap

        def record(d_, e_):
            sd = base.sim.data
            rec_q.append(sd.qpos.cpu().numpy().copy())
            if nmocap:
                rec_mp.append(sd.mocap_pos.cpu().numpy().copy())
                rec_mq.append(sd.mocap_quat.cpu().numpy().copy())
            pts = [base.scene[x].data.root_link_pos_w[:, :2] for x in AGENTS]
            if a.solo is not None:  # keep the camera on the robot that acts
                pts = [base.scene[a.solo].data.root_link_pos_w[:, :2] for _ in AGENTS]
            rec_pts.append(np.stack([p.cpu().numpy() for p in pts]
                                    + [g.box_pos()[:, :2].cpu().numpy(), g.goal_xy.cpu().numpy()], 1))
            rec_info.append(np.stack([d_.cpu().numpy(), np.degrees(e_.abs().cpu().numpy())], 1))

        d0, e0 = g.errors()
        record(d0, e0)
        done = torch.zeros(n, dtype=torch.bool, device=dev)
        how = ["horizon"] * n
        t_succ = torch.full((n,), float("nan"), device=dev)
        fell = {ag: torch.zeros(n, dtype=torch.bool, device=dev) for ag in AGENTS}
        hold = torch.zeros(n, device=dev)
        touch = torch.zeros(n, device=dev)
        live_steps = torch.zeros(n, device=dev)
        last_d, last_e, min_d = d0.clone(), e0.abs().clone(), d0.clone()
        end_step = torch.full((n,), steps - 1, dtype=torch.long, device=dev)
        pt, yt = 0.10, math.radians(6.0)
        tail = int(2.0 / dt)
        all_done_at = None
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
                inside = ok & (d < pt) & (ea < yt)
                hold = torch.where(inside, hold + dt, torch.zeros_like(hold))
                succ = ok & (hold >= 1.0)
                t_succ = torch.where(succ, torch.full_like(t_succ, t), t_succ)
                if a.solo is None:
                    touch += (cm.robots_touching(base) > 0).float() * live.float()
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
                end_step = torch.where(ended & ~done, torch.full_like(end_step, i), end_step)
                done |= ended
                if (i + 1) % stride == 0:
                    record(d, e)
                if all_done_at is None and bool(done.all()):
                    all_done_at = i
                if all_done_at is not None and i >= all_done_at + tail:
                    break

        Q, P, INFO = np.stack(rec_q, 1), np.stack(rec_pts, 1), np.stack(rec_info, 1)
        MP = np.stack(rec_mp, 1) if rec_mp else None
        MQ = np.stack(rec_mq, 1) if rec_mq else None
        cam = Camera(base, vw, vh)
        by = defaultdict(list)
        for j, (o, s, k) in enumerate(cases):
            by[(o, s)].append(j)
        fmt = lambda x: "" if math.isnan(x) else round(x, 2)  # noqa: E731
        for (o, s), js in by.items():
            wins = [j for j in js if how[j] == "success"]
            j = wins[0] if wins else js[0]
            sname, sdist, sdir, _ = scen[s]
            tdeg = round(math.degrees(float(turn[j])))
            row = {"object": o, "seen_shape": int(o in TRAIN_NAMES), "mass": mass, "scenario": sname,
                   "distance": sdist, "direction": sdir, "turn": tdeg,
                   "attempts_succeeded": f"{len(wins)}/{len(js)}", "filmed_attempt": js.index(j) + 1,
                   "outcome": how[j], "t_success": fmt(float(t_succ[j])),
                   "final_pos_err": round(float(last_d[j]), 3), "final_yaw_err": round(math.degrees(float(last_e[j])), 1),
                   "closest_pos_err": round(float(min_d[j]), 3),
                   "touch_frac": round(float(touch[j] / live_steps[j].clamp(min=1)), 3) if a.solo is None else "",
                   "attempt_outcomes": " ".join(how[x] for x in js), "video": ""}
            F = min(Q.shape[1], int(end_step[j]) // stride + int(1.0 / (stride * dt)) + 2)
            dst = out / o / f"{mass:g}kg" / f"{sname}__{how[j]}.mp4"
            head = f"{o} {mass:g}kg {sname.split('_')[0]} -> {how[j]}"
            try:
                render_episode(cam, j, Q[j, :F], None if MP is None else MP[j, :F], None if MQ is None else MQ[j, :F],
                               P[j, :F], dst, 1.0 / (stride * dt),
                               caption=lambda f, h=head, jj=j: f"{h} | t {f * stride * dt:4.1f}s | to goal "
                               f"{INFO[jj, f, 0]:4.2f} m {INFO[jj, f, 1]:4.0f} deg")
                row["video"] = str(dst.relative_to(out))
            except Exception as ex:  # noqa: BLE001
                print(f"video failed for {o} {mass:g} {sname}: {ex}")
            rows.append(row)
        mine = [r for r in rows if r["mass"] == mass]
        print(f"[{mass:g} kg] {sum(r['outcome'] == 'success' for r in mine)}/{len(mine)} object-scenarios succeeded "
              f"within 3 attempts ({time.time() - t0:.0f} s)", flush=True)
        base.close()
        del base, policy

    write(rows, out, a, what, masses, [s[0] for s in scen], EVALS)
    return 0


def write(rows, out: Path, a, what: str, masses, scen, evals_dir) -> None:
    with open(out / "showcase.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    objs = list(dict.fromkeys(r["object"] for r in rows))
    cell = {(r["object"], r["mass"], r["scenario"]): r for r in rows}
    md = [f"# Two-robot showcase: {a.name}", "", f"policy: {what}", "",
          f"Each cell: scenarios {' / '.join(s.split('_')[0] for s in scen)} as successful attempts out of 3 "
          "(S = filmed success, F = all 3 failed).", "",
          "| object | " + " | ".join(f"{m:g} kg" for m in masses) + " |", "|---" * (len(masses) + 1) + "|"]
    for o in objs:
        cells = []
        for m in masses:
            parts = []
            for s in scen:
                r = cell.get((o, m, s))
                parts.append("" if r is None else f"{r['attempts_succeeded'][0]}{'S' if r['outcome'] == 'success' else 'F'}")
            cells.append(" / ".join(parts))
        md.append(f"| {o}{'' if any(r['seen_shape'] for r in rows if r['object'] == o) else ' (unseen)'} | "
                  + " | ".join(cells) + " |")
    tot = {m: sum(cell[(o, m, s)]["outcome"] == "success" for o in objs for s in scen if (o, m, s) in cell) for m in masses}
    md += ["", "Succeeded (any attempt): " + ", ".join(f"{m:g} kg {tot[m]}/{len(objs) * len(scen)}" for m in masses)]
    (out / "showcase.md").write_text("\n".join(md) + "\n")
    h = ["<html><head><meta charset='utf-8'><title>" + html.escape(a.name) + "</title><style>"
         "body{font-family:sans-serif;background:#111;color:#ddd;margin:12px}td{vertical-align:top;padding:4px}"
         "video{width:300px}.S{color:#7e7}.F{color:#f97}</style></head><body>",
         f"<h1>{html.escape(a.name)}</h1><p>{html.escape(what)}</p><table><tr><th></th>" +
         "".join(f"<th>{m:g} kg</th>" for m in masses) + "</tr>"]
    for o in objs:
        h.append(f"<tr><td><b>{o}</b></td>")
        for m in masses:
            h.append("<td>")
            for s in scen:
                r = cell.get((o, m, s))
                if r and r["video"]:
                    c = "S" if r["outcome"] == "success" else "F"
                    h.append(f"<div class='{c}'>{s}: {r['outcome']} ({r['attempts_succeeded']})</div>"
                             f"<video controls preload='none' src='{r['video']}'></video>")
            h.append("</td>")
        h.append("</tr>")
    h.append("</table></body></html>")
    (out / "index.html").write_text("\n".join(h))
    stats = evals_dir / a.name / "eval" / "showcase"
    stats.mkdir(parents=True, exist_ok=True)
    shutil.copy2(out / "showcase.csv", stats / "showcase.csv")
    shutil.copy2(out / "showcase.md", stats / "showcase.md")
    print("\n".join(md))
    print(f"\nvideos: {out}/index.html\nstats: {stats}")


if __name__ == "__main__":
    raise SystemExit(main())
