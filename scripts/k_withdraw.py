"""Step 1 of docs/k_dispatch.md: does robot 4 hurt because it stays too long? CPU only, on chain4_branch --withdraw trees.

    python scripts/k_withdraw.py --dirs logs/evals/k4w-s100{1,2,3}{a,b} --out logs/evals/k-withdraw-dev --select
    python scripts/k_withdraw.py --dirs logs/evals/k4w-s830{1,2}{a,b} --out logs/evals/k-withdraw

Eligible decisions: tasks whose trio (k3) is still pushing at t2. For each 3 -> 4 arm (k3 = stay at three, k4 = robot 4
stays, k4w<cm> = robot 4 withdraws below that position error, k3null = a copy of k3), over all eligible starts:
the share entering the near-goal region (t_region logged by chain4_branch), the restricted mean time to the region
and to success over the horizon (never = horizon), success, robot 4's helper-seconds, and matched rescues /
disruptions against k3. Differences against k3 with a paired 95% bootstrap over tasks. --select applies the
protocol's trigger rule: the highest success over all eligible decisions; within 1 pp, the larger radius.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
H = 80.0
HEAVY = (80.0, 100.0)


def _f(x):
    return float(x) if x not in ("", None) else float("nan")


def load(dirs):
    T = defaultdict(dict)
    for d in dirs:
        p = Path(d)
        p = (p if p.is_absolute() else ROOT / p) / "episodes.csv"
        for r in csv.DictReader(open(p)):
            T[(str(d), r["object"], float(r["mass"]), r["scenario"], int(r["rep"]))][r["arm"]] = r
    return [tw for tw in T.values() if "k3" in tw and not int(tw["k3"]["ended_t2"])]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dirs", nargs="+", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--select", action="store_true", help="development: choose the withdrawal trigger")
    a = ap.parse_args()
    ts = load(a.dirs)
    arms = [x for x in ("k3", "k3null", "k4") if x in ts[0]] + sorted((x for x in ts[0] if x.startswith("k4w")),
                                                                     key=lambda x: -int(x[3:]))
    rng = np.random.default_rng(0)

    def col(sub, arm, k):
        return np.array([_f(t[arm][k]) for t in sub])

    def ci(v, B):
        bs = v[B].mean(1)
        return float(v.mean()), *np.percentile(bs, [2.5, 97.5]).tolist()

    def f(c, k=100, p=1):
        return f"{k * c[0]:+.{p}f} [{k * c[1]:+.{p}f}, {k * c[2]:+.{p}f}]"

    groups = {"all masses": ts, "heavy (80 + 100 kg)": [t for t in ts if t["k3"]["mass"] in HEAVY]}
    groups |= {f"{m:g} kg": [t for t in ts if float(t["k3"]["mass"]) == m] for m in sorted({float(t["k3"]["mass"]) for t in ts})}
    L = [f"# Robot 4: stay, or withdraw near the goal? ({len(ts)} eligible trio decisions)", "",
         f"Arms: {', '.join(arms)}. Over all eligible starts; times are restricted means over the {H:g} s horizon "
         "(never = horizon). Differences vs k3 (stay at three), paired 95% bootstrap over tasks.", ""]
    summ = {}
    for gname, sub in groups.items():
        n = len(sub)
        if n < 10:
            continue
        B = rng.integers(0, n, (4000, n))
        y3 = col(sub, "k3", "success")
        reg3 = ~np.isnan(col(sub, "k3", "t_region"))
        L += [f"## {gname} ({n} decisions)", "",
              "| arm | success | in region | time to region (s) | time to success (s) | success if in region | "
              "robot-4 s | rescues / disruptions | success vs k3 (pp) | region vs k3 (pp) | time to region vs k3 (s) | "
              "time to success vs k3 (s) |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
        ent = {}
        for arm in arms:
            y = col(sub, arm, "success")
            tr = col(sub, arm, "t_region")
            reg = ~np.isnan(tr)
            rt = np.where(reg, tr, H)
            tsu = col(sub, arm, "t_success")
            st = np.where(np.isnan(tsu), H, tsu)
            rt3 = np.where(reg3, col(sub, "k3", "t_region"), H)
            ts3 = col(sub, "k3", "t_success")
            st3 = np.where(np.isnan(ts3), H, ts3)
            h4 = col(sub, arm, "helper4_s")
            resc, disr = int(((y == 1) & (y3 == 0)).sum()), int(((y == 0) & (y3 == 1)).sum())
            ds, dr, dt_r, dt_s = ci(y - y3, B), ci(reg.astype(float) - reg3, B), ci(rt - rt3, B), ci(st - st3, B)
            same = arm == "k3"
            L.append(f"| {arm} | {100 * y.mean():.1f}% | {100 * reg.mean():.1f}% | {rt.mean():.1f} | {st.mean():.1f} | "
                     f"{100 * y[reg].mean() if reg.any() else float('nan'):.1f}% | {np.nanmean(h4):.1f} | {resc} / {disr} | "
                     + (" | | | |" if same else f"{f(ds)} | {f(dr)} | {f(dt_r, 1)} | {f(dt_s, 1)} |"))
            ent[arm] = {"success": float(y.mean()), "region": float(reg.mean()), "t_region": float(rt.mean()),
                        "t_success": float(st.mean()), "helper4_s": float(np.nanmean(h4)), "rescues": resc,
                        "disruptions": disr, "d_success": ds, "d_region": dr, "d_t_region": dt_r, "d_t_success": dt_s}
        # transport: position error at fixed times (done episodes keep their last error)
        L += ["", "Mean position error (m) at fixed times:", "",
              "| arm | " + " | ".join(f"{tt} s" for tt in (30, 40, 50, 60)) + " |", "|---|" + "---|" * 4]
        for arm in arms:
            L.append(f"| {arm} | " + " | ".join(f"{np.nanmean(col(sub, arm, f'd{tt}')):.2f}" for tt in (30, 40, 50, 60)) + " |")
        L.append("")
        summ[gname] = ent
    if a.select:
        allg = summ["all masses"]
        w = [x for x in arms if x.startswith("k4w")]
        top = max(allg[x]["success"] for x in w)
        pick = max((x for x in w if allg[x]["success"] >= top - 0.01), key=lambda x: int(x[3:]))
        L += [f"**Selected trigger (protocol rule): {pick}** (success {100 * allg[pick]['success']:.1f}%; best "
              f"{100 * top:.1f}%).", ""]
        summ["selected"] = pick
    out = Path(a.out) if Path(a.out).is_absolute() else ROOT / a.out
    out.mkdir(parents=True, exist_ok=True)
    (out / "summary.md").write_text("\n".join(L) + "\n")
    (out / "summary.json").write_text(json.dumps(summ, indent=1, default=float))
    print("\n".join(L))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
