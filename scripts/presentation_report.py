"""Presentation report: every system on the same 480 seed-7100 ten-object tasks (slurm/submit_presentation.sh).

    python scripts/presentation_report.py [--out=evals/presentation/report.md]

Systems (two runs each where they exist; tasks matched on object, mass, scenario, rep; standard formation):
  single ANYmal       pres-solo-anymal (+ -r2)              Stage 2b single-robot policy, partner parked
  frozen pair         pres-frozen-pair (+ -r2)              two copies of the single-robot policy, untrained together
  planner + executor  pres-planner-expert (+ -r2-expert)    contact planner + Stage 4 executor (turn_debug), start behind
  IPPO                pres-ippo-it4000 (+ place-ten-ippo-it4000 standard rows)
  MAPPO               pres-mappo-B-it5000 (+ place-nwB-mappo-it5000 standard rows)
Reported: success, precise success, falls, time to success, by mass and object; pair vs single ANYmal (tasks the
second robot rescues / loses, per-task two-run means); each trained actor alone; the filmed tasks.
Rerun noise: a second evaluation of the same checkpoint flips ~15% of outcomes; differences inside it are noise.
"""
from __future__ import annotations

import csv
import random
import statistics as st
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEN = ("cube", "long", "sphere", "cylinder", "arch", "dumbbell", "t_shape", "l_shape", "u_channel", "plus")
SYSTEMS = [  # label, runs
    ("single ANYmal", ["pres-solo-anymal", "pres-solo-anymal-r2"]),
    ("frozen pair", ["pres-frozen-pair", "pres-frozen-pair-r2"]),
    ("planner + executor", ["pres-planner-expert", "pres-planner-r2-expert"]),
    ("IPPO (it 4000)", ["pres-ippo-it4000", "place-ten-ippo-it4000"]),
    ("MAPPO (B, it 5000)", ["pres-mappo-B-it5000", "place-nwB-mappo-it5000"]),
]
ALONE = [("IPPO actor 1 alone", "pres-ippo-it4000-solo-anymal1"), ("IPPO actor 2 alone", "pres-ippo-it4000-solo-anymal2"),
         ("MAPPO actor 1 alone", "pres-mappo-B-it5000-solo-anymal1"), ("MAPPO actor 2 alone", "pres-mappo-B-it5000-solo-anymal2")]


def load(name: str) -> dict | None:
    f = ROOT / "evals" / name / "eval" / "pair" / "episodes.csv"
    if not f.exists():
        return None
    out = {}
    for r in csv.DictReader(open(f)):
        if r["object"] not in TEN or r.get("formation", "standard") != "standard" or int(r.get("swap") or 0):
            continue
        fell = int(r.get("fell_anymal1") or 0) or int(r.get("fell_anymal2") or 0)
        out[(r["object"], float(r["mass"]), r["scenario"], int(r["rep"]))] = {
            "success": int(r["success"]), "precise": int(r.get("precise") or 0), "fell": int(bool(fell)),
            "t": float(r["t_success"]) if r.get("t_success") else None, "video": r.get("video", "")}
    return out


def ci(d, n=4000, seed=0):
    rng = random.Random(seed)
    m = sum(d) / len(d)
    bs = sorted(sum(rng.choice(d) for _ in d) / len(d) for _ in range(n))
    return m, bs[int(0.025 * n)], bs[int(0.975 * n) - 1]


def main() -> int:
    args = dict(x.split("=", 1) for x in sys.argv[1:] if x.startswith("--") and "=" in x)
    runs = {lab: [x for x in (load(n) for n in names) if x] for lab, names in SYSTEMS}
    have = {lab: rr for lab, rr in runs.items() if rr}
    keys = sorted(set.intersection(*[set(r) for rr in have.values() for r in rr]))
    mean = {lab: {k: sum(r[k]["success"] for r in rr) / len(rr) for k in keys} for lab, rr in have.items()}
    md = ["# Presentation: two-robot pushing, all systems on the same tasks", "",
          f"{len(keys)} matched tasks (10 objects x 4 masses x 4 scenarios x 3 placements, seed 7100). Rates are "
          "per-task means over the runs available (n runs in brackets).", "",
          "| system | runs | success | precise | episodes with a fall | time to success, median s |", "|---|---|---|---|---|---|"]
    for lab, rr in have.items():
        s_ = sum(mean[lab].values()) / len(keys)
        p_ = sum(r[k]["precise"] for r in rr for k in keys) / (len(rr) * len(keys))
        f_ = sum(r[k]["fell"] for r in rr for k in keys) / (len(rr) * len(keys))
        ts = [r[k]["t"] for r in rr for k in keys if r[k]["t"] is not None]
        md.append(f"| {lab} | {len(rr)} | {s_:.1%} | {p_:.1%} | {f_:.1%} | {st.median(ts):.1f} |")
    masses = sorted({k[1] for k in keys})
    md += ["", "## Success by mass", "", "| system | " + " | ".join(f"{m:g} kg" for m in masses) + " |",
           "|---|" + "---|" * len(masses)]
    for lab in have:
        md.append(f"| {lab} | " + " | ".join(
            f"{sum(v for k, v in mean[lab].items() if k[1] == m) / sum(1 for k in keys if k[1] == m):.0%}" for m in masses) + " |")
    md += ["", "## Success by object", "", "| system | " + " | ".join(TEN) + " |", "|---|" + "---|" * len(TEN)]
    for lab in have:
        md.append(f"| {lab} | " + " | ".join(
            f"{sum(v for k, v in mean[lab].items() if k[0] == o) / sum(1 for k in keys if k[0] == o):.0%}" for o in TEN) + " |")
    scen = sorted({k[2] for k in keys})
    md += ["", "## Success by scenario", "", "| system | " + " | ".join(scen) + " |", "|---|" + "---|" * len(scen)]
    for lab in have:
        md.append(f"| {lab} | " + " | ".join(
            f"{sum(v for k, v in mean[lab].items() if k[2] == s) / sum(1 for k in keys if k[2] == s):.0%}" for s in scen) + " |")
    if "single ANYmal" in have:
        md += ["", "## Against one ANYmal (paired per task)", "",
               "Rescued: the single robot fails in every run and the system succeeds in every run; lost: the reverse.", "",
               "| system | change in success [95% CI] | rescued | lost | rescued at 60-80 kg |", "|---|---|---|---|---|"]
        solo = mean["single ANYmal"]
        for lab in have:
            if lab == "single ANYmal":
                continue
            m, lo, hi = ci([mean[lab][k] - solo[k] for k in keys])
            res = [k for k in keys if solo[k] == 0 and mean[lab][k] == 1]
            lost = [k for k in keys if solo[k] == 1 and mean[lab][k] == 0]
            md.append(f"| {lab} | {100 * m:+.1f} [{100 * lo:+.1f}, {100 * hi:+.1f}] pts | {len(res)} | {len(lost)} | "
                      f"{sum(k[1] >= 60 for k in res)} |")
    al = [(lab, load(n)) for lab, n in ALONE]
    al = [(lab, x) for lab, x in al if x]
    if al:
        md += ["", "## Each trained actor alone (partner parked far away)", "", "| actor | success |", "|---|---|"]
        for lab, x in al:
            ks = [k for k in keys if k in x]
            md.append(f"| {lab} | {sum(x[k]['success'] for k in ks) / len(ks):.1%} |")
    md += ["", "## Filmed tasks (same tasks for every system, every outcome)", ""]
    for lab, rr in have.items():
        vids = sorted(r[k]["video"] for k in keys for r in rr[:1] if r[k]["video"])
        md.append(f"- {lab}: {len(vids)} videos in `logs/evals/{SYSTEMS[[l for l, _ in SYSTEMS].index(lab)][1][0]}/pair/`")
    text = "\n".join(md) + "\n"
    out = Path(args.get("--out", "evals/presentation/report.md"))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text)
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
