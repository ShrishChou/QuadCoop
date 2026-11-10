"""Stalled transport with a robot on its contact but pressing < 30 N: A not driving in, B driving in
with no force, C lost it after pressing. Usage: python scripts/exec_engage.py logs/evals/<run>-expert/pair (needs --trace 2)."""
import sys, collections, numpy as np
sys.path.insert(0, "scripts"); import exec_report as X
from pathlib import Path
FWD = 0.15   # m/s forward walker command counted as "driving into the contact"
REC = 1.0    # s: pressed this recently -> a following failure
cls = collections.defaultdict(collections.Counter); det = collections.defaultdict(lambda: collections.defaultdict(list))
for obj, sc, mass, outcome, rows in X.traces(Path(sys.argv[1])):
    ags = X.agents(rows[0].keys()); col = lambda c: np.array([X.num(r[c]) for r in rows])
    live = col("live") > .5; pe = col("pose_err"); lag = 20
    stalled = np.zeros(len(rows), bool); stalled[lag:] = (pe[:-lag] - pe[lag:]) < X.STALL[1]
    far = (col("goal_dist") >= X.NEAR[0]) | (np.abs(col("goal_yaw_err_deg")) >= X.NEAR[1])
    stalled &= live & far
    ospd = col("obj_speed")
    for a in ags:
        on = col(f"on_{a}") > .5; fa = col(f"force_along_cmd_{a}"); f = col(f"force_{a}"); vx = col(f"wcmd_vx_{a}")
        mvx = col(f"vx_{a}"); he = np.abs(col(f"heading_err_deg_{a}")); cd = col(f"contact_dist_{a}"); tch = col(f"touching_{a}") > .5
        pressed = np.zeros(len(rows), bool); last = -1e9
        for i in range(len(rows)):
            if fa[i] >= X.PRESS: last = i
            pressed[i] = (i - last) * .1 <= REC and fa[i] < X.PRESS
        sel = stalled & on & (fa < X.PRESS)
        for i in np.nonzero(sel)[0]:
            if pressed[i]:
                c = "C lost it after pressing" + (" (object moving)" if ospd[i] > .05 else " (object still)")
            elif vx[i] < FWD:
                c = "A not driving in (cmd vx < %.2f)" % FWD
            else:
                c = "B driving in, no force"
            cls[mass][c] += 1
            det[mass][c].append((vx[i], mvx[i], he[i], cd[i], tch[i], f[i], ospd[i]))
for m in sorted(cls, key=float):
    n = sum(cls[m].values())
    print(f"\n{m} kg: {n*0.1:.0f} robot-seconds stalled on-contact-not-pressing")
    for c, k in sorted(cls[m].items()):
        v = np.array(det[m][c])
        print(f"  {k/n:.2f}  {c:38s} cmd vx {np.median(v[:,0]):+.2f}  actual vx {np.median(v[:,1]):+.2f}  heading err {np.median(v[:,2]):4.1f} deg  "
              f"dist to contact {np.median(v[:,3]):.2f} m  touching {v[:,4].mean():.2f}  |force| {np.median(v[:,5]):3.0f} N  obj speed {np.median(v[:,6]):.2f}")
