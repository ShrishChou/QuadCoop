"""Where does execution fail while motion and a contribution were actually requested? (residual-pilot case selection)

Reads 10 Hz traces (contact_test.py --trace 2). A sample is "requested" for robot k when the episode is live, the
planner wants motion (want_speed >= 0.03 m/s or |want_yaw_rate| >= 5 deg/s), robot k is on its contact (on_k) and
its commanded share is >= 0.15 (share_cmd_k). This replaces the geometric "push" label (front near a contact).

  python scripts/exec_failures.py logs/evals/e1s-Aw-expert/pair [--objects beam,cube,sphere,arch]

Per object x mass (all episodes, then failures only):
  req s/ep     requested robot-seconds per episode
  both         share of live time with both robots requested
  F along      mean force along the commanded push direction while requested (N)
  speed ratio  object speed / wanted speed while both are requested and wanted speed >= 0.03
  yaw ok       share of samples (|wanted yaw rate| >= 5 deg/s, both requested) turning the wanted way
  share err    mean |measured share - commanded share| while both requested and pushing >= 20 N in total
  off/req      share of requested-contact time robots spend off contact (on_k false while engaged_k)
Failure classes (episodes that did not succeed), by the end state and the requested-time evidence:
  fell       a robot fell
  stall      requested >= 10 s, speed ratio < 0.3 (object barely moves while pushed)
  turn       final position error < 0.3 m but heading error >= 6 deg
  unreached  requested < 5 s (the pushing phase was rarely reached)
  slow       none of the above (moving, but did not finish in time)
"""
import csv
import gzip
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

AG = ("anymal1", "anymal2")


def episodes(path):
    rows, key, last_t = [], None, 1e9
    for r in csv.DictReader(gzip.open(path, "rt")):
        t = float(r["t"])
        k = (r["object"], r["scenario"])
        if rows and (t < last_t or k != key):
            yield key, rows
            rows = []
        key, last_t = k, t
        rows.append(r)
    if rows:
        yield key, rows


def analyse(rows):
    g = lambda c: np.array([float(r[c]) if r[c] not in ("", "nan") else np.nan for r in rows])  # noqa: E731
    live = g("live") > 0.5
    ws, wy = g("want_speed"), g("want_yaw_rate_deg")
    want = live & ((ws >= 0.03) | (np.abs(wy) >= 5.0))
    req = [want & (g(f"on_{a}") > 0.5) & (g(f"share_cmd_{a}") >= 0.15) for a in AG]
    both = req[0] & req[1]
    fa = [g(f"force_along_cmd_{a}") for a in AG]
    sp = g("obj_speed")
    yr = np.rad2deg(g("obj_yaw_rate"))
    m_sp = both & (ws >= 0.03)
    tot = fa[0] + fa[1]
    m_sh = both & (tot >= 20.0)
    eng = [(g(f"engaged_{a}") > 0.5) & want & (g(f"share_cmd_{a}") >= 0.15) for a in AG]
    off = sum(int((e & (g(f"on_{a}") < 0.5)).sum()) for e, a in zip(eng, AG))
    n_eng = sum(int(e.sum()) for e in eng)
    m_y = both & (np.abs(wy) >= 5.0)
    last = rows[-1]
    out = dict(
        outcome=last["outcome"],
        fell=any(float(r[f"fell_{a}"]) > 0.5 for r in rows for a in AG),
        req_s=0.1 * sum(int(x.sum()) for x in req),
        both=float(both.sum()) / max(int(live.sum()), 1),
        f_along=float(np.nanmean(np.concatenate([fa[i][req[i]] for i in range(2)]))) if any(x.any() for x in req) else np.nan,
        ratio=float(np.nanmean(sp[m_sp] / ws[m_sp])) if m_sp.any() else np.nan,
        yaw_ok=float(np.mean(np.sign(yr[m_y]) == np.sign(wy[m_y]))) if m_y.any() else np.nan,
        share_err=float(np.nanmean(np.abs(fa[0][m_sh] / tot[m_sh] - g(f"share_cmd_{AG[0]}")[m_sh]))) if m_sh.any() else np.nan,
        off=off / max(n_eng, 1),
        end_d=float(last["goal_dist"]), end_e=abs(float(last["goal_yaw_err_deg"])),
    )
    if out["outcome"] == "success":
        out["cls"] = "success"
    elif out["fell"]:
        out["cls"] = "fell"
    elif out["req_s"] >= 10 and out["ratio"] == out["ratio"] and out["ratio"] < 0.3:
        out["cls"] = "stall"
    elif out["end_d"] < 0.3 and out["end_e"] >= 6.0:
        out["cls"] = "turn"
    elif out["req_s"] < 5:
        out["cls"] = "unreached"
    else:
        out["cls"] = "slow"
    return out


def main():
    d = Path(sys.argv[1])
    objs = None
    for x in sys.argv[2:]:
        if x.startswith("--objects="):
            objs = x.split("=", 1)[1].split(",")
    res = defaultdict(list)
    for f in sorted(d.glob("trace_*kg.csv.gz")):
        mass = float(f.stem.split("_")[1].replace("kg.csv", ""))
        for (o, s), rows in episodes(f):
            if objs and o not in objs:
                continue
            res[(o, mass)].append(dict(analyse(rows), scenario=s))
    nm = lambda v: float(np.nanmean(v)) if len(v) and not np.all(np.isnan(v)) else float("nan")  # noqa: E731
    print("| object | mass | n | success | req s/ep | both | F along N | speed ratio | yaw ok | share err | off/req | "
          "fell | stall | turn | unreached | slow |")
    print("|---" * 16 + "|")
    for (o, m), L in sorted(res.items()):
        col = lambda k, sub=L: nm(np.array([x[k] for x in sub], dtype=float))  # noqa: E731
        cls = defaultdict(int)
        for x in L:
            cls[x["cls"]] += 1
        print(f"| {o} | {m:g} | {len(L)} | {cls['success'] / len(L):.2f} | {col('req_s'):.1f} | {col('both'):.2f} | "
              f"{col('f_along'):.0f} | {col('ratio'):.2f} | {col('yaw_ok'):.2f} | {col('share_err'):.2f} | {col('off'):.2f} | "
              + " | ".join(str(cls[c]) for c in ("fell", "stall", "turn", "unreached", "slow")) + " |")


if __name__ == "__main__":
    main()
