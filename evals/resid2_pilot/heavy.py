"""SUPERSEDED by scripts/push_endings.py (kept as the evidence behind an earlier, retracted reading).

First 80 kg check (seed 4000): joint pressing, command saturation, force during stalls vs while moving (10 Hz traces).
Its "pressing" uses the raw 10 Hz force (>= 30 N) and the planner's on_contact flag. Both flicker with the gait and
with robots pressing just outside on_contact's 0.25 m drift radius, so it reports joint pushes as rare and < 1 s long.
push_endings.py smooths force and touch over 1 s and uses physical contact: sustained joint pushes are then common on
heavy beams (about 15 s per episode at 80 kg).

  python evals/resid2_pilot/heavy.py r2dev-base r2dev-resid     (from the repo root)
"""
import sys

import numpy as np

sys.path.insert(0, "scripts")
from exec_failures import episodes  # noqa: E402

AG = ("anymal1", "anymal2")
P = 30.0  # N along the command direction counts as "pressing"


def runs(m):  # longest run of True, in samples
    best = cur = 0
    for x in m:
        cur = cur + 1 if x else 0
        best = max(best, cur)
    return best


print("| arm | mass | live s/ep | both press % | longest both-press s (mean/max) | fwd cmd sat % (on contact) | "
      "vx track (on, sat) | F tot stall N (mean/p90) | F tot moving N (mean/p90) | moving % of both-press |")
print("|---|---|---|---|---|---|---|---|---|---|")
for arm in sys.argv[1:]:
    for m in (20, 40, 60, 80):
        L, J, LR, SAT, TR, FS, FM, MV = [], [], [], [], [], [], [], []
        for (o, s), rows in episodes(f"logs/evals/{arm}-s4000-expert/pair/trace_{m}kg.csv.gz"):
            g = lambda c: np.array([float(r[c]) if r[c] not in ("", "nan") else np.nan for r in rows])  # noqa: E731
            live = (g("live") > .5) & (g("want_speed") >= .03)
            fa = [np.nan_to_num(g(f"force_along_cmd_{a}")) for a in AG]
            on = [g(f"on_{a}") > .5 for a in AG]
            press = [on[i] & (fa[i] >= P) for i in range(2)]
            both = live & press[0] & press[1]
            tot = fa[0] + fa[1]
            sp = g("obj_speed")
            L.append(live.sum() / 10)
            J.append(both.sum() / max(live.sum(), 1))
            LR.append(runs(both) / 10)
            for a in AG:
                oc = live & (g(f"on_{a}") > .5)
                sat = oc & (g(f"wcmd_vx_{a}") >= .79)  # the walker's forward limit is 0.8 m/s
                SAT.append((sat.sum(), oc.sum()))
                if sat.any():
                    TR.append(np.nanmean(g(f"vx_{a}")[sat]))
            FS += list(tot[both & (sp < .02)])
            FM += list(tot[both & (sp >= .05)])
            MV.append(((both & (sp >= .05)).sum(), both.sum()))
        q = lambda v: f"{np.mean(v):.0f}/{np.percentile(v, 90):.0f}" if len(v) else "-"  # noqa: E731
        sat = sum(a for a, _ in SAT) / max(sum(b for _, b in SAT), 1)
        mv = sum(a for a, _ in MV) / max(sum(b for _, b in MV), 1)
        print(f"| {arm} | {m} | {np.mean(L):.0f} | {100 * np.mean(J):.0f} | {np.mean(LR):.1f}/{np.max(LR):.1f} | "
              f"{100 * sat:.0f} | {np.mean(TR) if TR else float('nan'):.2f} | {q(FS)} | {q(FM)} | {100 * mv:.0f} |")
