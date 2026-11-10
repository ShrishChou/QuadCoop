"""Executor report from a contact_test eval: acquisition, cooperation, finishing, and where falls happen.

  python scripts/exec_report.py logs/evals/<A>-expert/pair [logs/evals/<B>-expert/pair]

Reads episodes.csv (every episode) and trace_<mass>kg.csv.gz (10 Hz; from --trace 1 = rep 0, --trace 2 = all).
With two folders, success is also compared task by task. Fall phase = the robot's state in the 1 s before it fell:
  approach     not yet reached any contact this episode
  reposition   reached a contact before, off contact now (walking to a new one or recovering)
  hold/light   on contact, pressing < PRESS N
  pushing      on contact, pressing >= PRESS N
"""
import csv, gzip, sys, collections
from pathlib import Path
import numpy as np

PRESS = 30.0     # N along the push direction counted as a real press
WIN = 1.0        # s before a fall that decides its phase
NEAR = (0.30, 15.0)  # "near the goal": within 30 cm and 15 deg
JUMP = 0.3       # m: a step change of the distance to the assigned contact = the planner reassigned it
STALL = (2.0, 0.03)  # s, pose-error drop: less progress than this over the past 2 s = transport stalled
SWITCH_S = 3.0   # s: a stall this soon after a reassignment is blamed on it
SUSTAIN = 1.0    # s: a both-pressing interval at least this long counts as sustained
CAUSES = ("reassigned", "never acquired", "acquired, lost", "on, not pressing", "both pressing")


def stall_causes(rows, ags, t):
    """Per-sample cause of stalled transport, plus sustained-press and acquisition stats, for one episode."""
    live = np.array([float(r["live"]) for r in rows]) > 0.5
    pe = np.array([float(r["pose_err"]) for r in rows])
    lag = int(round(STALL[0] / 0.1))
    stalled = np.zeros(len(rows), bool)
    stalled[lag:] = (pe[:-lag] - pe[lag:]) < STALL[1]
    far = (np.array([float(r["goal_dist"]) for r in rows]) >= NEAR[0]) | \
        (np.abs(np.array([float(r["goal_yaw_err_deg"]) for r in rows])) >= NEAR[1])
    stalled &= live & far  # transport only: slow final adjustments near the goal are not stalls
    on = np.stack([np.array([float(r[f"on_{a}"]) for r in rows]) > 0.5 for a in ags])
    press = np.stack([np.array([float(r[f"force_along_cmd_{a}"]) for r in rows]) >= PRESS for a in ags])
    cd = np.stack([np.array([float(r[f"contact_dist_{a}"]) for r in rows]) for a in ags])
    jump = np.zeros_like(on)
    jump[:, 1:] = np.abs(np.diff(cd, axis=1)) > JUMP
    # since each robot's latest assignment: has it been on contact?
    got = np.zeros_like(on)
    since_sw = np.full(len(rows), 1e9)
    acq_t = []  # time from (re)assignment to first sustained press (0.5 s), per assignment that got one
    for k in range(len(ags)):
        g, t0, run = False, t[0], 0
        done = False
        for i in range(len(rows)):
            if jump[k, i]:
                g, t0, run, done = False, t[i], 0, False
            g |= on[k, i]
            got[k, i] = g
            run = run + 1 if (on[k, i] and press[k, i]) else 0
            if run >= 5 and not done:
                acq_t.append(t[i] - 0.4 - t0); done = True  # noqa: E702
    last = -1e9
    for i in range(len(rows)):
        if jump[:, i].any():
            last = t[i]
        since_sw[i] = t[i] - last
    cause = np.full(len(rows), -1)
    for i in np.nonzero(stalled)[0]:
        if since_sw[i] <= SWITCH_S:
            c = 0
        elif not got[:, i].all():
            c = 1
        elif not on[:, i].all():
            c = 2
        elif not press[:, i].all():
            c = 3
        else:
            c = 4
        cause[i] = c
    both = press.all(0) & on.all(0) & live
    sus, run = 0, 0
    lens = []
    for i in range(len(rows) + 1):
        if i < len(rows) and both[i]:
            run += 1
        else:
            if run * 0.1 >= SUSTAIN:
                sus += run; lens.append(run * 0.1)  # noqa: E702
            run = 0
    return dict(cause=cause, live_s=live.sum() * 0.1, stalled_s=stalled.sum() * 0.1, both_s=both.sum() * 0.1,
                sus_s=sus * 0.1, lens=lens, acq=acq_t, n_jump=int(jump.sum()),
                press_on=(press & on)[:, live].sum() / max(on[:, live].sum(), 1))


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return np.nan


def episodes(d):
    return {(r["object"], r["mass"], r["scenario"], r["rep"]): r for r in csv.DictReader(open(d / "episodes.csv"))}


def traces(d):
    """Yield (object, scenario, mass, outcome, rows) per traced episode."""
    for p in sorted(d.glob("trace_*kg.csv.gz"), key=lambda p: float(p.name[6:-9])):
        mass = p.name[6:-9]
        key, rows, last_t = None, [], 1e9
        for r in csv.DictReader(gzip.open(p, "rt")):
            t = float(r["t"])
            k = (r["object"], r["scenario"])
            if rows and (k != key or t < last_t):
                yield key[0], key[1], mass, rows[0]["outcome"], rows
                rows = []
            key, last_t = k, t
            rows.append(r)
        if rows:
            yield key[0], key[1], mass, rows[0]["outcome"], rows


def agents(head):
    return [c[5:] for c in head if c.startswith("fell_")]


def report(d):
    d = Path(d)
    E = episodes(d)
    ags = sorted({k[5:] for k in next(iter(E.values())) if k.startswith("fell_")})
    masses = sorted({k[1] for k in E}, key=float)
    m = lambda rows, c: np.nanmean([num(r[c]) for r in rows]) if rows else np.nan
    print(f"\n#### {d}   ({len(E)} episodes)")
    print("mass  | success | timeout | fell | reached contact (both) | reach s | on-contact frac | both press share | copush | push N med/p90 | final pos cm / yaw deg (non-success) | min pos err cm | overshoot")
    for ms in masses + ["all"]:
        R = [r for k, r in E.items() if ms == "all" or k[1] == ms]
        oc = collections.Counter("fell" if r["outcome"].startswith("fell") else r["outcome"] for r in R)
        F = [r for r in R if r["outcome"] != "success"]
        reach = np.mean([all(num(r[f"reached_{a}"]) > 0.5 for a in ags) for r in R])
        print(f"{ms:>5} | {m(R,'success'):.2f}    | {oc['horizon']/len(R):.2f}    | {oc['fell']/len(R):.2f} | {reach:.2f}                   | "
              f"{np.nanmean([m(R, f'reach_time_{a}') for a in ags]):.1f}     | {np.nanmean([m(R, f'on_contact_{a}') for a in ags]):.2f}            | "
              f"{m(R,'both_press_share'):.2f}             | {m(R,'copush_frac'):.2f}   | {m(R,'push_force_med'):.0f}/{m(R,'push_force_p90'):.0f}        | "
              f"{100*m(F,'final_pos_err'):.0f} / {m(F,'final_yaw_err'):.0f}                            | {100*m(F,'min_pos_err'):.0f}             | {m(R,'overshoot'):.2f}")

    # ---- traces: falls by phase, and finishing behaviour near the goal
    falls = collections.Counter()
    falls_m = collections.defaultdict(collections.Counter)
    fall_cmd = collections.defaultdict(list)
    near_n = near_ok = 0
    near_rows = collections.Counter()
    n_tr = 0
    st = collections.defaultdict(list)
    for obj, sc, mass, outcome, rows in traces(d):
        n_tr += 1
        ags_t = agents(rows[0].keys())
        t = np.array([float(r["t"]) for r in rows])
        st[mass].append(stall_causes(rows, ags_t, t))
        for a in ags_t:
            fell = np.array([float(r[f"fell_{a}"]) for r in rows]) > 0.5
            if not fell.any():
                continue
            i = int(fell.argmax())
            on = np.array([float(r[f"on_{a}"]) for r in rows]) > 0.5
            fa = np.array([float(r[f"force_along_cmd_{a}"]) for r in rows])
            w = (t >= t[i] - WIN) & (t < t[i])
            if not w.any():
                w = np.zeros_like(fell); w[max(i - 1, 0)] = True  # noqa: E702
            if not on[:i].any():
                ph = "approach"
            elif on[w].mean() < 0.5:
                ph = "reposition"
            elif np.nanmedian(fa[w]) >= PRESS:
                ph = "pushing"
            else:
                ph = "hold/light"
            falls[ph] += 1
            falls_m[mass][ph] += 1
            wc = np.array([[float(r[f"wcmd_{x}_{a}"]) for x in ("vx", "vy", "wz")] for r in rows])[w]
            fall_cmd[ph].append((np.abs(wc).max(0)))
        # finishing: once near the goal, does the pose error keep shrinking to success?
        gd = np.array([float(r["goal_dist"]) for r in rows])
        ye = np.abs(np.array([float(r["goal_yaw_err_deg"]) for r in rows]))
        near = (gd < NEAR[0]) & (ye < NEAR[1])
        if near.any():
            near_n += 1
            near_ok += outcome == "success"
            if outcome != "success":
                j = int(near.argmax())
                left = "pos" if gd[-1] >= 0.10 else ""
                left += ("+" if left else "") + "yaw" if ye[-1] >= 3.0 else ""
                near_rows[f"{outcome}: left {left or 'neither'}{' (drifted back out)' if not near[-1] else ''}"] += 1
    if not n_tr:
        print("(no traces in this folder: run the eval with --trace 2)")
        return E
    print(f"\ntraced episodes {n_tr}")
    print(f"transport stalls (pose error down < {STALL[1]} in {STALL[0]:g} s, outside {NEAR[0]*100:.0f} cm / {NEAR[1]:.0f} deg), share of stalled time by cause; "
          f"sustained = both pressing >= {PRESS:g} N for >= {SUSTAIN:g} s")
    print("mass  | stalled | " + " | ".join(CAUSES) + " | reassign/ep | pressing when on | both press | of it sustained | med interval s | acquire s (med)")
    for ms in sorted(st, key=float) + ["all"]:
        S = [x for k, v in st.items() if ms == "all" or k == ms for x in v]
        live = sum(x["live_s"] for x in S)
        stl = sum(x["stalled_s"] for x in S)
        cc = np.bincount(np.concatenate([x["cause"][x["cause"] >= 0] for x in S]).astype(int), minlength=len(CAUSES))
        both = sum(x["both_s"] for x in S)
        lens = [l_ for x in S for l_ in x["lens"]]
        acq = [a_ for x in S for a_ in x["acq"]]
        print(f"{ms:>5} | {stl/live:.2f}    | " + " | ".join(f"{c/max(cc.sum(),1):.2f}".rjust(len(n_)) for c, n_ in zip(cc, CAUSES))
              + f" | {np.mean([x['n_jump'] for x in S]):.1f}         | {np.mean([x['press_on'] for x in S]):.2f}             | "
              f"{both/live:.2f}       | {sum(x['sus_s'] for x in S)/max(both,1e-9):.2f}            | "
              f"{np.median(lens) if lens else float('nan'):.1f}            | {np.median(acq) if acq else float('nan'):.1f}")
    tot = sum(falls.values())
    print(f"falls by phase ({tot} robot falls): " + ", ".join(f"{p} {c}" for p, c in falls.most_common()))
    for ms in sorted(falls_m, key=float):
        print(f"  {ms:>4} kg: " + ", ".join(f"{p} {c}" for p, c in falls_m[ms].most_common()))
    for p, v in fall_cmd.items():
        v = np.array(v)
        print(f"  {p:10s} max |walker cmd| in last {WIN:g}s: vx {np.median(v[:,0]):.2f}  vy {np.median(v[:,1]):.2f}  wz {np.median(v[:,2]):.2f} (median)")
    print(f"finishing: {near_n} episodes got within {NEAR[0]*100:.0f} cm / {NEAR[1]:.0f} deg; {near_ok} of them succeeded ({near_ok/max(near_n,1):.2f})")
    for k, c in near_rows.most_common(6):
        print(f"  {c:4d}  {k}")
    return E


def paired(A, B):
    keys = sorted(set(A) & set(B))
    d = np.array([num(B[k]["success"]) - num(A[k]["success"]) for k in keys])
    print(f"\npaired success B - A over {len(keys)} tasks: {d.mean():+.3f} +- {d.std() / np.sqrt(len(d)):.3f}  "
          f"(A only {int((d < 0).sum())}, B only {int((d > 0).sum())})")
    for ms in sorted({k[1] for k in keys}, key=float):
        dd = np.array([num(B[k]["success"]) - num(A[k]["success"]) for k in keys if k[1] == ms])
        print(f"  {ms:>4} kg: {dd.mean():+.3f} +- {dd.std() / np.sqrt(len(dd)):.3f}")


if __name__ == "__main__":
    res = [report(p) for p in sys.argv[1:3]]
    if len(res) == 2:
        paired(*res)
