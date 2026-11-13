"""Final coordinator comparison (docs/coordinator_design.md, sections 8-10): teacher vs BC vs PPO on the reserved
placement seeds, identical tasks and settings, greedy. Excludes the declared cell (dumbbell / D_far_turn / 60 kg).

  python scripts/coord_compare.py teacher=final-teacher bc=final-bc0 ppo=final-ppo0 --seeds 3000,3001,3002
  python scripts/coord_compare.py base=rdev-base resid=rdev-resid --seeds=4000 --all-cells --objects=each   # residual pilot

Per arm, overall / by mass / by object: success, precise, falls, capped completion time (80 s if no success),
assignment switches per episode and contact acquisition (share of assignments reached, mean over robots).
Paired differences against the first arm, task = object x scenario x mass x rep x seed; bootstrap 95% CI over tasks
(2,000 resamples).
"""
import csv
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {("dumbbell", "D_far_turn", 60.0)}
AG = ("anymal1", "anymal2")


def load(prefix, seeds, excluded=EXCLUDED):
    out = {}
    for s in seeds:
        for r in csv.DictReader(open(ROOT / "logs" / "evals" / f"{prefix}-s{s}-expert" / "pair" / "episodes.csv")):
            if (r["object"], r["scenario"], float(r["mass"])) in excluded:
                continue
            ts = r["t_success"]
            reach = [float(r[f"reached_{a}"]) for a in AG if r.get(f"reached_{a}", "") not in ("",)]
            out[(r["object"], r["scenario"], float(r["mass"]), r["rep"], s)] = dict(
                success=float(r["success"]), precise=float(r["precise"]),
                fell=float(r["outcome"].startswith("fell")),
                time=float(ts) if ts not in ("", "nan") and float(r["success"]) > 0 else 80.0,
                switches=float(r["switches"] or 0), reached=sum(reach) / len(reach) if reach else float("nan"))
    return out


METRICS = ("success", "precise", "fell", "time", "switches", "reached")


def mean(v):
    v = [x for x in v if x == x]
    return sum(v) / len(v) if v else float("nan")


def ci(d, n=2000, seed=0):
    rng = random.Random(seed)
    bs = sorted(mean([rng.choice(d) for _ in d]) for _ in range(n))
    return mean(d), bs[int(0.025 * n)], bs[int(0.975 * n) - 1]


def main():
    arms, seeds, excluded, objs = {}, [3000, 3001, 3002], EXCLUDED, None
    for x in sys.argv[1:]:
        if x.startswith("--seeds"):
            seeds = [int(v) for v in x.split("=", 1)[1].split(",")]
        elif x == "--all-cells":
            excluded = set()
        elif x.startswith("--objects"):
            objs = x.split("=", 1)[1].split(",")
        else:
            k, v = x.split("=", 1)
            arms[k] = v
    data = {k: load(v, seeds, excluded) for k, v in arms.items()}
    keys = sorted(set.intersection(*[set(d) for d in data.values()]))
    names = list(arms)
    print(f"{len(keys)} matched tasks per arm (seeds {seeds}; excluded cells {sorted(excluded)})\n")
    masses = sorted({k[2] for k in keys})
    objs = objs or ("long", "arch", "dumbbell")
    if objs == ["each"]:
        objs = sorted({k[0] for k in keys})
    groups = [("all", lambda k: True)] + [(f"{m:g} kg", lambda k, m=m: k[2] == m) for m in masses] + \
             [(o, lambda k, o=o: k[0] == o) for o in objs]
    for o in objs:
        groups += [(f"{o} {m:g} kg", lambda k, o=o, m=m: k[0] == o and k[2] == m) for m in masses] if o == "beam" else []
    print("| group | arm | n | success | precise | fell | capped time s | switches/ep | contacts reached |")
    print("|---|---|---|---|---|---|---|---|---|")
    for g, f in groups:
        ks = [k for k in keys if f(k)]
        for a in names:
            vals = [mean([data[a][k][m] for k in ks]) for m in METRICS]
            print(f"| {g} | {a} | {len(ks)} | " + " | ".join(
                f"{v:.3f}" if m not in ("time", "switches") else f"{v:.1f}" for m, v in zip(METRICS, vals)) + " |")
    base = names[0]
    print(f"\nPaired differences vs {base} (mean [95% CI]); points for rates, seconds for time")
    print("| group | arm | success | precise | fell | capped time s |")
    print("|---|---|---|---|---|---|")
    for g, f in groups:
        ks = [k for k in keys if f(k)]
        for a in names[1:]:
            cells = []
            for m in ("success", "precise", "fell", "time"):
                d = [data[a][k][m] - data[base][k][m] for k in ks]
                mu, lo, hi = ci(d)
                sc = 1.0 if m == "time" else 100.0
                cells.append(f"{mu * sc:+.1f} [{lo * sc:+.1f}, {hi * sc:+.1f}]")
            print(f"| {g} | {a} | " + " | ".join(cells) + " |")
    if "ppo" in names and "bc" in names:
        print("\nPPO vs BC (paired)")
        for g, f in groups:
            ks = [k for k in keys if f(k)]
            cells = []
            for m in ("success", "precise"):
                mu, lo, hi = ci([data["ppo"][k][m] - data["bc"][k][m] for k in ks])
                cells.append(f"{m} {mu * 100:+.1f} [{lo * 100:+.1f}, {hi * 100:+.1f}]")
            print(f"  {g}: " + "; ".join(cells))


if __name__ == "__main__":
    main()
