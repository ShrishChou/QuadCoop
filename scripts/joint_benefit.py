"""What does joint training buy? Matched ten-object benchmark (the pres-* runs: seed 7100, 480 tasks = 10 objects x
4 masses x 4 placements x 3 repeats, the same tasks for every system). CPU only.

    python scripts/joint_benefit.py --out logs/evals/joint-benefit

Systems (episodes.csv from scripts/eval_coop2.py / contact_test.py):
  solo            one ANYmal, its single-robot push policy (the other robot parked far away)
  frozen pair     two copies of that single-robot policy, no joint training
  IPPO / MAPPO    the jointly trained pairs
  IPPO, one robot / MAPPO, one robot   the joint policy driving one robot (the other parked): what the joint policy
                  alone is worth without its partner
  planner         the contact planner (expert rule + learned executor)
A task's success is the mean over its runs; gains over solo are paired over tasks (95% bootstrap resampling tasks,
so a task's repeats and runs move together). Failure anatomy for the policies that log it (all but the planner):
first push, first 0.25 m of progress, and where failed episodes ended.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "logs" / "evals"
SYSTEMS = {
    "solo": ["pres-solo-anymal", "pres-solo-anymal-r2"],
    "frozen pair": ["pres-frozen-pair", "pres-frozen-pair-r2"],
    "IPPO": ["pres-ippo-it4000"],
    "MAPPO": ["pres-mappo-B-it5000"],
    "IPPO, one robot": ["pres-ippo-it4000-solo-anymal1", "pres-ippo-it4000-solo-anymal2"],
    "MAPPO, one robot": ["pres-mappo-B-it5000-solo-anymal1", "pres-mappo-B-it5000-solo-anymal2"],
    "planner": ["pres-planner-expert", "pres-planner-r2-expert"],
}
MAIN = ("solo", "frozen pair", "IPPO", "MAPPO", "planner")


def _f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return float("nan")


def load(dirs):
    runs = []
    for d in dirs:
        runs.append({(r["object"], float(r["mass"]), r["scenario"], int(r["rep"])): r
                     for r in csv.DictReader(open(E / d / "pair" / "episodes.csv"))})
    return runs


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default="logs/evals/joint-benefit")
    a = ap.parse_args()
    data = {s: load(d) for s, d in SYSTEMS.items()}
    keys = sorted(set.intersection(*[set(r) for runs in data.values() for r in runs]))
    masses = sorted({k[1] for k in keys})
    rng = np.random.default_rng(0)

    def succ(s, ks):
        return np.array([np.mean([int(r[k]["success"]) for r in data[s]]) for k in ks])

    def fell(s, ks):
        return np.array([np.mean([float(any(_f(v) == 1 for c, v in r[k].items() if c.startswith("fell_")))
                                  for r in data[s]]) for k in ks])

    def ci(v):
        b = v[rng.integers(0, len(v), (4000, len(v)))].mean(1)
        return 100 * v.mean(), 100 * np.percentile(b, 2.5), 100 * np.percentile(b, 97.5)

    def fmt(c):
        return f"{c[0]:+.1f} [{c[1]:+.1f}, {c[2]:+.1f}]"

    L = [f"# What joint training buys: matched ten-object benchmark ({len(keys)} tasks)", "",
         "Tasks = object x mass x placement x repeat, identical for every system; runs per task: "
         + ", ".join(f"{s} {len(d)}" for s, d in SYSTEMS.items()) + ". Gains over solo in pp, paired over tasks "
         "(95% bootstrap over tasks).", ""]
    fig = []
    L += ["## Success by mass", "", "| mass | tasks | " + " | ".join(SYSTEMS) + " |", "|---|---|" + "---|" * len(SYSTEMS)]
    for m in masses + ["all"]:
        ks = [k for k in keys if m == "all" or k[1] == m]
        L.append(f"| {m if m == 'all' else f'{m:g} kg'} | {len(ks)} | "
                 + " | ".join(f"{100 * succ(s, ks).mean():.0f}%" for s in SYSTEMS) + " |")
    L += ["", "## Gain over solo (pp)", "", "| mass | " + " | ".join(s for s in SYSTEMS if s != "solo") + " |",
          "|---|" + "---|" * (len(SYSTEMS) - 1)]
    for m in masses + ["all"]:
        ks = [k for k in keys if m == "all" or k[1] == m]
        y0 = succ("solo", ks)
        cells = []
        for s in SYSTEMS:
            if s == "solo":
                continue
            c = ci(succ(s, ks) - y0)
            cells.append(fmt(c))
            fig.append({"mass": m, "system": s, "gain": c[0], "lo": c[1], "hi": c[2],
                        "success": 100 * float(succ(s, ks).mean()), "solo": 100 * float(y0.mean()), "tasks": len(ks)})
        L.append(f"| {m if m == 'all' else f'{m:g} kg'} | " + " | ".join(cells) + " |")
    L += ["", "## A robot fell (% of episodes)", "", "| mass | " + " | ".join(MAIN) + " |", "|---|" + "---|" * len(MAIN)]
    for m in masses + ["all"]:
        ks = [k for k in keys if m == "all" or k[1] == m]
        L.append(f"| {m if m == 'all' else f'{m:g} kg'} | " + " | ".join(f"{100 * fell(s, ks).mean():.1f}%" for s in MAIN) + " |")

    # failure anatomy (eval_coop2 columns; the planner's evaluator does not log t_push / t_progress)
    L += ["", "## Why does solo suffice at low mass? Failure anatomy", "",
          "Per episode (all runs): first push by any robot; first 0.25 m of progress toward the goal ('moved'); "
          "for failed episodes, how they ended: fall, never moved, moved but stopped > 0.5 m short, or reached "
          "within 0.5 m with the heading still off (> 6 deg).", "",
          "| mass | system | success | first push (median s) | moved | first 0.25 m (median s) | failed: fell | "
          "never moved | stopped > 0.5 m | near, heading off | near, heading ok | final dist / heading of timeouts |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    anat = {}
    for m in masses:
        for s in ("solo", "frozen pair", "IPPO", "MAPPO", "IPPO, one robot", "MAPPO, one robot"):
            eps = [r[k] for r in data[s] for k in keys if k[1] == m]
            ok = np.array([int(e["success"]) for e in eps])
            tpush = np.array([np.nanmin([_f(v) for c, v in e.items() if c.startswith("t_push_")] or [np.nan]) for e in eps])
            tprog = np.array([_f(e["t_progress"]) for e in eps])
            fl = np.array([any(_f(v) == 1 for c, v in e.items() if c.startswith("fell_")) for e in eps])
            dfin, yfin = np.array([_f(e["final_pos_err"]) for e in eps]), np.array([_f(e["final_yaw_err"]) for e in eps])
            fail = ok == 0
            nf = max(int(fail.sum()), 1)
            nev = fail & ~fl & np.isnan(tprog)
            far = fail & ~fl & ~np.isnan(tprog) & (dfin > 0.5)
            near_off = fail & ~fl & ~np.isnan(tprog) & (dfin <= 0.5) & (np.abs(yfin) > 6)
            near_ok = fail & ~fl & ~np.isnan(tprog) & (dfin <= 0.5) & (np.abs(yfin) <= 6)
            to = fail & ~fl
            row = {"success": ok.mean(), "push": np.nanmedian(tpush), "moved": np.mean(~np.isnan(tprog)),
                   "t_prog": np.nanmedian(tprog), "fell": (fail & fl).sum() / nf, "never": nev.sum() / nf,
                   "far": far.sum() / nf, "near_off": near_off.sum() / nf, "near_ok": near_ok.sum() / nf,
                   "to_d": np.nanmedian(dfin[to]) if to.any() else np.nan, "to_y": np.nanmedian(np.abs(yfin[to])) if to.any() else np.nan}
            anat[f"{m:g}/{s}"] = row
            L.append(f"| {m:g} kg | {s} | {100 * row['success']:.0f}% | {row['push']:.1f} | {100 * row['moved']:.0f}% | "
                     f"{row['t_prog']:.1f} | {100 * row['fell']:.0f}% | {100 * row['never']:.0f}% | {100 * row['far']:.0f}% | "
                     f"{100 * row['near_off']:.0f}% | {100 * row['near_ok']:.0f}% | {row['to_d']:.2f} m / {row['to_y']:.0f} deg |")
    L += ["", "Failed-episode columns are shares of that system's failures at that mass. 'Near, heading ok' failures "
          "are within 0.5 m and 6 deg but not within 10 cm (or not held 1 s).", "",
          "Not available from these logs: the fraction of the episode making progress, and goal-directed force per "
          "robot (needs a re-evaluation with that logging)."]
    out = Path(a.out) if Path(a.out).is_absolute() else ROOT / a.out
    out.mkdir(parents=True, exist_ok=True)
    (out / "summary.md").write_text("\n".join(L) + "\n")
    (out / "figure_data.json").write_text(json.dumps(fig, indent=1))
    (out / "anatomy.json").write_text(json.dumps(anat, indent=1, default=float))
    print("\n".join(L))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
