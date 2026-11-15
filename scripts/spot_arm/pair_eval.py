"""Spot-arm pair, turn-pilot evaluation on held-out starts (docs/spot_arm_pair.md).

    python scripts/spot_arm/pair_eval.py --checkpoint logs/marl2/<run>/model_<n>.pt --name sa-pilot-<run>
    python scripts/spot_arm/pair_eval.py --report sa-pilot-<run1>,sa-pilot-<run2>,...     # systems side by side

Tasks (the same for every checkpoint: --seed): one elongated object ("long", --mass 20 kg), goal 1 m ahead with the
heading turned left (+30 deg), straight (0) or right (-30 deg); the robots start behind it at -35 / +35 deg
(+-10 deg jitter, 0.3-0.6 m clear, object heading jittered +-10 deg), each task also with the two start places
exchanged; --reps placements per turn. Success: within 0.10 m and 6 deg for 1 s inside --horizon; a fall ends
the episode as a failure.
Arm modes, all in one build for a learned-arm checkpoint (the policy is the same, only what its arm outputs may
do differs): both (as trained), only_1 / only_2 (the other robot's arm held stowed), none (both held stowed).
A stowed-arm checkpoint has the one mode "stowed".
Per episode: success, time, final position and signed heading error, falls, each robot's arm and trunk contact
share and mean arm contact force. Videos: rep 0, unswapped, of each turn, in every arm mode (captions: wanted and
actual object heading). Writes evals/<name>/episodes.csv and summary.md; videos to logs/evals/<name>/.
"""
from __future__ import annotations

import argparse
import csv
import math
import os
import random
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
TURNS = (("left", 30.0), ("straight", 0.0), ("right", -30.0))
POS_TOL, YAW_TOL_DEG, HOLD_S = 0.10, 6.0, 1.0


def ci(d, n=4000, seed=0):
    rng = random.Random(seed)
    m = sum(d) / len(d)
    bs = sorted(sum(rng.choice(d) for _ in d) / len(d) for _ in range(n))
    return m, bs[int(0.025 * n)], bs[int(0.975 * n) - 1]


def load(name: str) -> list[dict]:
    return list(csv.DictReader(open(ROOT / "evals" / name / "episodes.csv")))


def tables(rows: list[dict], label: str = "") -> list[str]:
    """Markdown for one evaluation: per arm mode, by turn; paired arm ablation; swap; who touches with the arm."""
    f = lambda r, k: float(r[k])  # noqa: E731
    modes = list(dict.fromkeys(r["arm_mode"] for r in rows))
    agents = [k[len("fell_"):] for k in rows[0] if k.startswith("fell_")]
    md = [f"## {label}".rstrip(), "", "| arm mode | turn | episodes | success | falls | time to success, median s | "
          "final position error, median m | final heading error, median abs deg | signed heading error, mean deg |",
          "|---|---|---|---|---|---|---|---|---|"]
    for m in modes:
        for t in [x[0] for x in TURNS] + ["all"]:
            sel = [r for r in rows if r["arm_mode"] == m and (t == "all" or r["turn"] == t)]
            ts = sorted(f(r, "t_success") for r in sel if r["t_success"])
            med = lambda v: sorted(v)[len(v) // 2]  # noqa: E731
            md.append(f"| {m} | {t} | {len(sel)} | {sum(int(r['success']) for r in sel) / len(sel):.1%} | "
                      f"{sum(int(r['fell']) for r in sel) / len(sel):.1%} | {(f'{med(ts):.1f}' if ts else '-')} | "
                      f"{med([f(r, 'pos_err') for r in sel]):.3f} | {med([abs(f(r, 'yaw_err_deg')) for r in sel]):.1f} | "
                      f"{sum(f(r, 'yaw_err_deg') for r in sel) / len(sel):+.1f} |")
    key = lambda r: (r["turn"], r["rep"], r["swap"])  # noqa: E731
    if "both" in modes:
        base = {key(r): r for r in rows if r["arm_mode"] == "both"}
        md += ["", "Arm ablation, paired per task against both arms active (the same policy; a locked arm stays stowed):", "",
               "| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |",
               "|---|---|---|---|---|"]
        for m in modes:
            if m == "both":
                continue
            oth = {key(r): r for r in rows if r["arm_mode"] == m}
            ks = sorted(set(base) & set(oth))
            ds = [int(oth[k]["success"]) - int(base[k]["success"]) for k in ks]
            dh = [abs(f(oth[k], "yaw_err_deg")) - abs(f(base[k], "yaw_err_deg")) for k in ks]
            a, lo, hi = ci(ds)
            b, lo2, hi2 = ci(dh)
            md.append(f"| {m} | {100 * a:+.1f} [{100 * lo:+.1f}, {100 * hi:+.1f}] pts | {sum(d < 0 for d in ds)} | "
                      f"{sum(d > 0 for d in ds)} | {b:+.1f} [{lo2:+.1f}, {hi2:+.1f}] |")
    md += ["", "Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along "
           "the push direction; arm contact = share of the episode with that robot's arm on the object.", "",
           "| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | "
           "arm contact, robot starting right | trunk contact left | trunk contact right |", "|---|---|---|---|---|---|---|---|"]
    for m in modes:
        for t in [x[0] for x in TURNS]:
            sel = [r for r in rows if r["arm_mode"] == m and r["turn"] == t]
            su = [int(r["success"]) for r in sel if r["swap"] == "0"]
            ss = [int(r["success"]) for r in sel if r["swap"] == "1"]
            side = defaultdict(list)
            for r in sel:  # unswapped: agent 0 starts at 180 - 35 deg = left of the push direction
                left, right = (agents[0], agents[1]) if r["swap"] == "0" else (agents[1], agents[0])
                for nm, ag in (("L", left), ("R", right)):
                    side["arm" + nm].append(f(r, f"arm_touch_{ag}"))
                    side["trunk" + nm].append(f(r, f"trunk_touch_{ag}"))
            mean = lambda v: sum(v) / max(len(v), 1)  # noqa: E731
            md.append(f"| {m} | {t} | {mean(su):.1%} | {mean(ss):.1%} | {mean(side['armL']):.1%} | {mean(side['armR']):.1%} | "
                      f"{mean(side['trunkL']):.1%} | {mean(side['trunkR']):.1%} |")
    return md


def report(names: list[str]) -> int:
    md = ["# Spot-arm turn pilot: systems on the same held-out tasks", ""]
    runs = {n: load(n) for n in names}
    md += ["| system | arm mode | success | falls | abs heading error left / straight / right, median deg |", "|---|---|---|---|---|"]
    for n, rows in runs.items():
        for m in dict.fromkeys(r["arm_mode"] for r in rows):
            sel = [r for r in rows if r["arm_mode"] == m]
            med = lambda t: sorted(abs(float(r["yaw_err_deg"])) for r in sel if r["turn"] == t)  # noqa: E731
            md.append(f"| {n} | {m} | {sum(int(r['success']) for r in sel) / len(sel):.1%} | "
                      f"{sum(int(r['fell']) for r in sel) / len(sel):.1%} | "
                      + " / ".join(f"{med(t)[len(med(t)) // 2]:.1f}" for t, _ in TURNS) + " |")
    key = lambda r: (r["turn"], r["rep"], r["swap"])  # noqa: E731
    main_mode = lambda rows: "both" if any(r["arm_mode"] == "both" for r in rows) else rows[0]["arm_mode"]  # noqa: E731
    if len(names) > 1:
        md += ["", "Paired per task, each system as trained (learned arms: both active), against the first:", "",
               "| system | change in success [95% CI] | tasks gained | tasks lost |", "|---|---|---|---|"]
        b = {key(r): int(r["success"]) for r in runs[names[0]] if r["arm_mode"] == main_mode(runs[names[0]])}
        for n in names[1:]:
            o = {key(r): int(r["success"]) for r in runs[n] if r["arm_mode"] == main_mode(runs[n])}
            ks = sorted(set(b) & set(o))
            d = [o[k] - b[k] for k in ks]
            a, lo, hi = ci(d)
            md.append(f"| {n} vs {names[0]} | {100 * a:+.1f} [{100 * lo:+.1f}, {100 * hi:+.1f}] pts | {sum(x > 0 for x in d)} | "
                      f"{sum(x < 0 for x in d)} |")
    for n, rows in runs.items():
        md += [""] + tables(rows, n)
    out = ROOT / "evals" / "spot_arm" / "pilot_report.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(md) + "\n")
    print("\n".join(md))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--checkpoint")
    ap.add_argument("--name")
    ap.add_argument("--report", default="", help="comma list of evaluation names: write evals/spot_arm/pilot_report.md")
    ap.add_argument("--object", default="long")
    ap.add_argument("--mass", type=float, default=20.0)
    ap.add_argument("--dist", type=float, default=1.0)
    ap.add_argument("--reps", type=int, default=20)
    ap.add_argument("--horizon", type=float, default=20.0)
    ap.add_argument("--seed", type=int, default=7100)
    ap.add_argument("--videos", type=int, default=1)
    a = ap.parse_args()
    if a.report:
        return report([x.strip() for x in a.report.split(",") if x.strip()])
    if not (a.checkpoint and a.name):
        ap.error("give --checkpoint and --name (or --report)")
    os.environ["QUADCOOP_SHAPES"] = "v2"
    os.environ["QUADCOOP_PAIR"] = "spot_arm"
    import numpy as np
    import torch
    from tensordict import TensorDict

    import quadcoop  # noqa: F401
    from mjlab.envs import ManagerBasedRlEnv

    from quadcoop import falls
    from quadcoop.coop2.env_cfg import SPECS, make_coop2_env_cfg
    from quadcoop.coop2.marl import PairPolicy, action_slices
    from quadcoop.coop2.mdp import AGENTS
    from quadcoop.coop2.video import Camera, key_points, render_episode
    from quadcoop.stage1.mdp import wrap
    from quadcoop.stage1b.shapes import NOMINAL_MASS
    from quadcoop.stage2 import mdp as m2
    from quadcoop.stage2.shapes import OBJ_NAMES2, SHAPE_NAMES2, SHAPES2

    ck = torch.load(a.checkpoint, map_location="cpu", weights_only=False)
    rc = ck.get("cfg", {})
    assert rc.get("pair") == "spot_arm", f"{a.checkpoint}: pair {rc.get('pair')}"
    arm = rc.get("arm") or "stowed"
    modes = ["both", "only_1", "only_2", "none"] if arm == "learned" else ["stowed"]
    lock = {"both": (0, 0), "only_1": (0, 1), "only_2": (1, 0), "none": (1, 1), "stowed": (0, 0)}
    base_cases = [(t, r) for t in range(len(TURNS)) for r in range(a.reps)]
    cases = [(t, r, w, m) for m in modes for w in (0, 1) for (t, r) in base_cases]
    n = len(cases)
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    cfg = make_coop2_env_cfg(ck.get("variant", "b"), play=True, partner_map=bool(rc.get("partner_map")),
                             reward_set=rc.get("reward_set", "r7"), arm=arm,
                             pilot_level=tuple(rc.get("pilot_level") or ()), dyaw_choices=bool(rc.get("dyaw_choices")))
    if rc.get("pilot_level"):
        cfg.commands["goal"].start_level = 0
    cfg.scene.num_envs = n
    cfg.episode_length_s = 1e5
    cfg.terminations = {}
    alpha = 0.5 * math.log(a.mass / NOMINAL_MASS)
    for name in OBJ_NAMES2:
        cfg.events[f"{name}_mass"].params["alpha_range"] = (alpha, alpha)
    torch.manual_seed(a.seed)
    env = ManagerBasedRlEnv(cfg=cfg, device=device)
    g = env.command_manager.get_term("goal")
    dev, dt = env.device, env.step_dt
    ids = torch.arange(n, device=dev)
    for k in range(len(SHAPES2)):
        m2.apply_geometry(env, ids, k, torch.ones(n, 3, device=dev))

    rng = random.Random(f"{a.seed}-spot-arm-pilot")
    draw = {c: {"jit": [rng.uniform(-10, 10) for _ in AGENTS], "gap": [rng.uniform(0.3, 0.6) for _ in AGENTS],
                "head": rng.uniform(-10, 10)} for c in base_cases}
    T = lambda fn: torch.tensor([fn(c) for c in cases], device=dev, dtype=torch.float32)  # noqa: E731
    sw = lambda c, k: (1 - k) if c[2] else k  # noqa: E731
    head = torch.deg2rad(T(lambda c: draw[c[:2]]["head"]))
    turn = torch.deg2rad(T(lambda c: TURNS[c[0]][1]))
    bearings = [math.pi + torch.deg2rad(T(lambda c, k=k: (-35.0, 35.0)[sw(c, k)] + draw[c[:2]]["jit"][sw(c, k)])) for k in range(2)]
    gaps = [T(lambda c, k=k: draw[c[:2]]["gap"][sw(c, k)]) for k in range(2)]
    z = torch.zeros(n, device=dev)
    sc = {"shape": torch.full((n,), SHAPE_NAMES2.index(a.object), device=dev), "obj_xy_rel": torch.zeros(n, 2, device=dev),
          "obj_heading": head, "goal_xy_rel": torch.tensor([a.dist, 0.0], device=dev).repeat(n, 1),
          "goal_yaw": wrap(head + turn), "bearings": bearings, "gaps": gaps, "yaw_noise": [z, z],
          "park": [torch.zeros(n, dtype=torch.bool, device=dev) for _ in AGENTS]}
    g.scenario = lambda env_ids: {k: ([x[env_ids] for x in v] if isinstance(v, list) else v[env_ids]) for k, v in sc.items()}
    obs, _ = env.reset()
    g.scenario = None
    td = lambda o: TensorDict({k: v for k, v in o.items() if not k.startswith("walker_")}, batch_size=[n])  # noqa: E731
    obs = td(obs)
    policy = PairPolicy(obs, device, ck.get("variant", "b"), checkpoint=a.checkpoint)
    sl = action_slices(env)
    terms = {ag: env.action_manager.get_term(f"walker_{ag}") for ag in AGENTS}
    for k, ag in enumerate(AGENTS):
        terms[ag].arm_locked[:] = torch.tensor([bool(lock[c[3]][k]) for c in cases], device=dev)
    print(f"{a.checkpoint} (iteration {ck['iter']}, {ck['algo']}, arm {arm}; actions { {ag: s.stop - s.start for ag, s in sl.items()} }); "
          f"{len(base_cases)} tasks x swap x modes {modes} = {n} episodes, {a.object} {a.mass:g} kg", flush=True)

    film = [j for j, c in enumerate(cases) if c[1] == 0 and c[2] == 0] if a.videos else []
    rec = {j: {"q": [], "mp": [], "mq": [], "pts": [], "cap": []} for j in film}
    nmocap = env.sim.mj_model.nmocap
    done = torch.zeros(n, dtype=torch.bool, device=dev)
    succ = torch.zeros(n, dtype=torch.bool, device=dev)
    fell = {ag: torch.zeros(n, dtype=torch.bool, device=dev) for ag in AGENTS}
    hold = torch.zeros(n, device=dev)
    t_succ = torch.full((n,), float("nan"), device=dev)
    pos_err, yaw_err = torch.zeros(n, device=dev), torch.zeros(n, device=dev)
    live_steps = torch.zeros(n, device=dev)
    acc = {f"{p}_{ag}": torch.zeros(n, device=dev) for ag in AGENTS for p in ("arm", "trunk", "force")}
    with torch.no_grad():
        for i in range(int(a.horizon / dt)):
            act = policy(obs, env=env)
            act[done] = 0.0  # finished episodes: stand still, arms stowed
            o, *_ = env.step(act)
            obs = td(o)
            t = (i + 1) * dt
            live = ~done
            d, e = g.errors()
            pos_err = torch.where(live, d, pos_err)
            yaw_err = torch.where(live, e, yaw_err)
            live_steps += live.float()
            for ag in AGENTS:
                f_ = falls.fallen(env, asset_name=ag, nominal_height=SPECS[ag].nominal_height) & live
                fell[ag] |= f_
                sd = env.scene[f"arm_{ag}"].data
                on = sd.found.view(n, -1).any(-1) & live
                acc[f"arm_{ag}"] += on.float()
                acc[f"force_{ag}"] += torch.linalg.norm(sd.force.view(n, -1, 3).sum(1), dim=-1) * on.float()
                acc[f"trunk_{ag}"] += (env.scene[f"trunk_{ag}"].data.found.view(n, -1).any(-1) & live).float()
            inside = (d < POS_TOL) & (e.abs() < math.radians(YAW_TOL_DEG))
            hold = torch.where(inside & live, hold + dt, torch.zeros_like(hold))
            new = live & (hold >= HOLD_S)
            succ |= new
            t_succ = torch.where(new, torch.full_like(t_succ, t), t_succ)
            done |= new | fell[AGENTS[0]] | fell[AGENTS[1]]
            if film and i % 2 == 0:
                sd = env.sim.data
                for j in film:
                    if done[j] and len(rec[j]["q"]) > 0 and rec[j].get("tail", 0) > 25:
                        continue
                    rec[j]["tail"] = rec[j].get("tail", 0) + int(bool(done[j]))
                    rec[j]["q"].append(sd.qpos[j].cpu().numpy().copy())
                    if nmocap:
                        rec[j]["mp"].append(sd.mocap_pos[j].cpu().numpy().copy())
                        rec[j]["mq"].append(sd.mocap_quat[j].cpu().numpy().copy())
                    rec[j]["pts"].append(key_points(env, j))
                    c = cases[j]
                    rec[j]["cap"].append(
                        f"{ck['algo'].upper()} arms {arm}, mode {c[3]} | turn {TURNS[c[0]][0]} ({TURNS[c[0]][1]:+.0f} deg) | t {t:4.1f} s\n"
                        f"object heading: wanted {math.degrees(float(g.goal_yaw[j])):+.0f} deg, error {math.degrees(float(e[j])):+.1f} deg | "
                        f"distance to goal {float(d[j]):.2f} m"
                        + (" | SUCCESS" if bool(succ[j]) else " | FELL" if bool(fell[AGENTS[0]][j] | fell[AGENTS[1]][j]) else ""))
            if bool(done.all()):
                break
    rows = []
    for j, c in enumerate(cases):
        ls = max(float(live_steps[j]), 1.0)
        rows.append({"turn": TURNS[c[0]][0], "turn_deg": TURNS[c[0]][1], "rep": c[1], "swap": c[2], "arm_mode": c[3],
                     "success": int(bool(succ[j])), "fell": int(bool(fell[AGENTS[0]][j] | fell[AGENTS[1]][j])),
                     **{f"fell_{ag}": int(bool(fell[ag][j])) for ag in AGENTS},
                     "t_success": "" if not bool(succ[j]) else round(float(t_succ[j]), 2),
                     "pos_err": round(float(pos_err[j]), 4), "yaw_err_deg": round(math.degrees(float(yaw_err[j])), 2),
                     **{f"arm_touch_{ag}": round(float(acc[f'arm_{ag}'][j]) / ls, 4) for ag in AGENTS},
                     **{f"trunk_touch_{ag}": round(float(acc[f'trunk_{ag}'][j]) / ls, 4) for ag in AGENTS},
                     **{f"arm_force_{ag}": round(float(acc[f'force_{ag}'][j]) / max(float(acc[f'arm_{ag}'][j]), 1.0), 1)
                        for ag in AGENTS}})
    out = ROOT / "evals" / a.name
    out.mkdir(parents=True, exist_ok=True)
    with open(out / "episodes.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    srows = [{k: str(v) for k, v in r.items()} for r in rows]
    md = [f"# Spot-arm turn pilot: {a.name}", "",
          f"{a.checkpoint}, iteration {ck['iter']}, {ck['algo']}, arms {arm}. {a.object} {a.mass:g} kg, {a.dist:g} m, "
          f"{a.reps} placements per turn x swap, horizon {a.horizon:g} s, seed {a.seed}.", ""] + tables(srows)
    (out / "summary.md").write_text("\n".join(md) + "\n")
    print("\n".join(md), flush=True)
    if film:
        try:
            cam = Camera(env, 960, 720)
            vdir = ROOT / "logs" / "evals" / a.name
            for j in film:
                c = cases[j]
                render_episode(cam, j, np.stack(rec[j]["q"]), np.stack(rec[j]["mp"]) if nmocap else None,
                               np.stack(rec[j]["mq"]) if nmocap else None, np.stack(rec[j]["pts"]),
                               vdir / f"{TURNS[c[0]][0]}_{c[3]}.mp4", fps=1.0 / (2 * dt), caption=lambda f, j=j: rec[j]["cap"][f])
            print(f"videos: {vdir}")
        except Exception as e:  # noqa: BLE001
            print(f"videos failed: {e!r}")
    env.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
