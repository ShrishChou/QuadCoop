"""Planner feedback extension (docs/planner_feedback.md): share-response preflight and the matched comparison.

  python scripts/feedback_compare.py response m02=pf1-m02 zero=pf1-0 p02=pf1-p02
  python scripts/feedback_compare.py compare A=fbA-f05 B=fbB-f05 [C=fbC-f05] [--out evals/planner_feedback/f05.md]

Folders: logs/evals/<prefix>-expert/pair (episodes.csv, trace_<mass>kg.csv.gz from --trace 2). Tasks are matched by
(object, scenario, mass, rep); traces carry no rep column, so reps are numbered by order within (object, scenario).

Trace samples (10 Hz), with force and touch averaged over a centred 1 s window (the gait pulses them):
  requested-both  live, motion wanted (want_speed >= 0.03 m/s or |want yaw rate| >= 5 deg/s), both robots engaged,
                  both sent shares >= 0.15
  share sample    requested-both, both touching (1 s share >= 0.5), total force along the push directions >= 60 N
  delivered share anymal1's share of the force along the push directions (1 s means); requested = its sent share
Per task: success, final position / heading error, falls, capped completion time, settled (after a success), contact
switches (episodes.csv); unintended yaw (S_straight only: largest |heading change| from the start while live);
delivered and requested share (share samples); |delivered - requested|; desired vs measured object motion (mean
|v_obj - v_wanted| m/s and |yaw rate - wanted| deg/s while motion is wanted); contact duty (share of live samples with
both robots touching, raw 10 Hz, and with each); how much correction happened (mean |sent - nominal share| and
|corrected - nominal velocity| while wanted).
Paired differences against the first arm: bootstrap 95% CI over tasks (2,000 resamples).
"""
import csv
import gzip
import math
import random
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
AG = ("anymal1", "anymal2")
WIN = 10


def sm(v):
    return np.convolve(np.nan_to_num(v), np.ones(WIN) / WIN, mode="same")


def trace_tasks(folder):
    out = {}
    for f in sorted(folder.glob("trace_*kg.csv.gz")):
        mass = float(f.name.split("_")[1].replace("kg.csv.gz", ""))
        rows, key, last_t, count = [], None, 1e9, defaultdict(int)

        def flush():
            if rows:
                k = (rows[0]["object"], rows[0]["scenario"])
                out[(k[0], k[1], mass, count[k])] = rows[:]
                count[k] += 1
        for r in csv.DictReader(gzip.open(f, "rt")):
            t, k = float(r["t"]), (r["object"], r["scenario"])
            if rows and (t < last_t or k != key):
                flush()
                rows.clear()
            key, last_t = k, t
            rows.append(r)
        flush()
    return out


def trace_metrics(rows, scenario):
    g = lambda c: np.array([float(r[c]) if r.get(c, "") not in ("", "nan") else np.nan for r in rows])  # noqa: E731
    live = g("live") > .5
    want = live & ((g("want_speed") >= .03) | (np.abs(g("want_yaw_rate_deg")) >= 5.0))
    sent = [g(f"share_cmd_{a}") for a in AG]
    req = want & (g("engaged_anymal1") > .5) & (g("engaged_anymal2") > .5) & (sent[0] >= .15) & (sent[1] >= .15)
    along = [sm(np.clip(g(f"force_along_cmd_{a}"), 0, None)) for a in AG]
    tc = [sm(g(f"touching_{a}")) >= .5 for a in AG]
    tot = along[0] + along[1]
    samp = req & tc[0] & tc[1] & (tot >= 60.0)
    deliv = np.where(tot > 1e-6, along[0] / np.maximum(tot, 1e-6), np.nan)
    m = {}
    m["share_n"] = int(samp.sum())
    m["share_deliv"] = float(np.nanmean(deliv[samp])) if samp.any() else np.nan
    m["share_req"] = float(np.nanmean(sent[0][samp])) if samp.any() else np.nan
    m["share_err"] = float(np.nanmean(np.abs(deliv[samp] - sent[0][samp]))) if samp.any() else np.nan
    nom = g("share_nom_anymal1") if "share_nom_anymal1" in rows[0] else np.full(len(rows), np.nan)
    m["share_corr"] = float(np.nanmean(np.abs(sent[0][want] - nom[want]))) if want.any() else np.nan
    wv = np.stack([g("want_vx"), g("want_vy")], -1) if "want_vx" in rows[0] else None
    if wv is not None and want.any():
        ov = np.stack([g("obj_vx"), g("obj_vy")], -1)
        m["v_err"] = float(np.nanmean(np.linalg.norm(ov[want] - wv[want], axis=-1)))
        fv = np.stack([g("fb_vx"), g("fb_vy")], -1)
        m["v_corr"] = float(np.nanmean(np.linalg.norm(fv[want] - wv[want], axis=-1)))
    else:
        m["v_err"] = m["v_corr"] = np.nan
    yr = np.rad2deg(g("obj_yaw_rate"))
    m["w_err"] = float(np.nanmean(np.abs(yr[want] - g("want_yaw_rate_deg")[want]))) if want.any() else np.nan
    yaw = g("obj_yaw_deg")
    if scenario == "S_straight" and live.any():
        d = (yaw[live] - yaw[live][0] + 180.0) % 360.0 - 180.0
        m["yaw_unint"] = float(np.max(np.abs(d)))
    else:
        m["yaw_unint"] = np.nan
    if "tr_phase_anymal1" in rows[0] and not np.all(np.isnan(g("tr_phase_anymal1"))):  # request tracking columns
        ph = np.concatenate([g(f"tr_phase_{a}")[live] for a in AG])
        er = np.concatenate([g(f"tr_err_{a}")[live] for a in AG])
        dv = np.concatenate([g(f"tr_deliv_{a}")[live] for a in AG])
        tg = np.concatenate([g(f"tr_target_{a}")[live] for a in AG])
        tr, st = ph == 1, (ph == 2) | (ph == 3)
        m["trk_ratio"] = float(np.mean(dv[tr] / np.maximum(tg[tr], 1.0))) if tr.any() else np.nan
        m["trk_err_transport"] = float(np.mean(er[tr])) if tr.any() else np.nan
        m["trk_err_stop"] = float(np.mean(er[st])) if st.any() else np.nan
    else:
        m["trk_ratio"] = m["trk_err_transport"] = m["trk_err_stop"] = np.nan
    raw = [g(f"touching_{a}") > .5 for a in AG]
    m["duty_both"] = float((raw[0] & raw[1])[live].mean()) if live.any() else np.nan
    m["duty_each"] = float(np.mean([r_[live].mean() for r_ in raw])) if live.any() else np.nan
    return m


def load(prefix):
    d = ROOT / "logs" / "evals" / f"{prefix}-expert" / "pair"
    eps = {}
    for r in csv.DictReader(open(d / "episodes.csv")):
        k = (r["object"], r["scenario"], float(r["mass"]), int(r["rep"]))
        ts = r["t_success"]
        eps[k] = dict(success=float(r["success"]), fell=float(r["outcome"].startswith("fell")),
                      pos_err=float(r["final_pos_err"]), yaw_err=abs(float(r["final_yaw_err"])),
                      time=float(ts) if ts not in ("", "nan") and float(r["success"]) > 0 else 20.0,
                      settled=float(r["settled"]) if r.get("settled", "") not in ("",) else np.nan,
                      switches=float(r["switches"] or 0), outcome=r["outcome"])
    for k, rows in trace_tasks(d).items():
        if k in eps:
            eps[k].update(trace_metrics(rows, k[1]))
    return eps


def mean(v):
    v = [x for x in v if x == x]
    return sum(v) / len(v) if v else float("nan")


def ci(d, n=2000, seed=0):
    d = [x for x in d if x == x]
    if not d:
        return float("nan"), float("nan"), float("nan")
    rng = random.Random(seed)
    bs = sorted(mean([rng.choice(d) for _ in d]) for _ in range(n))
    return mean(d), bs[int(0.025 * n)], bs[int(0.975 * n) - 1]


def response(arms):
    data = {k: load(v) for k, v in arms.items()}
    names = list(arms)
    lo_, hi_ = names[0], names[-1]
    keys = sorted(set.intersection(*[set(x) for x in data.values()]))
    print(f"{len(keys)} matched tasks; arms {arms}\n")
    print("| group | arm | n | share samples/task | requested share (anymal1) | delivered share (anymal1) |")
    print("|---|---|---|---|---|---|")
    groups = [("all", lambda k: True)] + [(f"{m:g} kg", lambda k, m=m: k[2] == m) for m in sorted({k[2] for k in keys})] + \
        [(s, lambda k, s=s: k[1] == s) for s in sorted({k[1] for k in keys})]
    for gname, f in groups:
        ks = [k for k in keys if f(k)]
        for a in names:
            print(f"| {gname} | {a} | {len(ks)} | {mean([data[a][k].get('share_n', 0) for k in ks]):.0f} | "
                  f"{mean([data[a][k].get('share_req', np.nan) for k in ks]):.3f} | "
                  f"{mean([data[a][k].get('share_deliv', np.nan) for k in ks]):.3f} |")
    print(f"\nPaired response, {hi_} - {lo_} (tasks with share samples in both arms)")
    print("| group | n | requested change | delivered change [95% CI] | delivered / requested |")
    print("|---|---|---|---|---|")
    for gname, f in groups:
        ks = [k for k in keys if f(k) and data[lo_][k].get("share_n", 0) > 0 and data[hi_][k].get("share_n", 0) > 0]
        dr = [data[hi_][k]["share_req"] - data[lo_][k]["share_req"] for k in ks]
        dd = [data[hi_][k]["share_deliv"] - data[lo_][k]["share_deliv"] for k in ks]
        mu, lo, hi = ci(dd)
        print(f"| {gname} | {len(ks)} | {mean(dr):+.3f} | {mu:+.3f} [{lo:+.3f}, {hi:+.3f}] | "
              f"{mu / mean(dr) if mean(dr) == mean(dr) and abs(mean(dr)) > 1e-6 else float('nan'):.2f} |")
    print("\nPer task (delivered share, anymal1): " + " / ".join(names))
    for k in keys:
        print(f"  {k[1]} {k[2]:g} kg rep {k[3]}: " + " / ".join(
            f"{data[a][k].get('share_deliv', np.nan):.2f} (n {data[a][k].get('share_n', 0)})" for a in names))


METRICS = ("success", "pos_err", "yaw_err", "yaw_unint", "fell", "time", "settled", "share_req", "share_deliv",
           "share_err", "v_err", "w_err", "duty_both", "duty_each", "switches", "share_corr", "v_corr",
           "trk_ratio", "trk_err_transport", "trk_err_stop")


def compare(arms):
    data = {k: load(v) for k, v in arms.items()}
    names = list(arms)
    base = names[0]
    keys = sorted(set.intersection(*[set(x) for x in data.values()]))
    print(f"{len(keys)} matched tasks per arm; arms {arms}\n")
    groups = [("all", lambda k: True)] + [(f"{m:g} kg", lambda k, m=m: k[2] == m) for m in sorted({k[2] for k in keys})] + \
        [(s, lambda k, s=s: k[1] == s) for s in sorted({k[1] for k in keys})]
    print("| group | arm | n | " + " | ".join(METRICS) + " |")
    print("|---" * (3 + len(METRICS)) + "|")
    for gname, f in groups:
        ks = [k for k in keys if f(k)]
        for a in names:
            print(f"| {gname} | {a} | {len(ks)} | " + " | ".join(
                f"{mean([data[a][k].get(m, np.nan) for k in ks]):.3f}" for m in METRICS) + " |")
    print(f"\nPaired differences vs {base} (mean [95% CI]): success / fell in points, errors in m and deg, time in s")
    pm = ("success", "fell", "pos_err", "yaw_err", "yaw_unint", "time", "share_err", "v_err", "w_err", "duty_both", "switches",
          "trk_ratio", "trk_err_transport", "trk_err_stop")
    print("| group | arm | " + " | ".join(pm) + " |")
    print("|---" * (2 + len(pm)) + "|")
    for gname, f in groups:
        ks = [k for k in keys if f(k)]
        for a in names[1:]:
            cells = []
            for m in pm:
                mu, lo, hi = ci([data[a][k].get(m, np.nan) - data[base][k].get(m, np.nan) for k in ks])
                sc = 100.0 if m in ("success", "fell", "duty_both") else 1.0
                cells.append(f"{mu * sc:+.2f} [{lo * sc:+.2f}, {hi * sc:+.2f}]")
            print(f"| {gname} | {a} | " + " | ".join(cells) + " |")
    for a in names[1:]:
        gained = [k for k in keys if data[a][k]["success"] > data[base][k]["success"]]
        lost = [k for k in keys if data[a][k]["success"] < data[base][k]["success"]]
        print(f"\n{a} vs {base}: gained {len(gained)}, lost {len(lost)}")
        for k in gained:
            print(f"  + {k[1]} {k[2]:g} kg rep {k[3]} ({data[base][k]['outcome']} -> {data[a][k]['outcome']})")
        for k in lost:
            print(f"  - {k[1]} {k[2]:g} kg rep {k[3]} ({data[base][k]['outcome']} -> {data[a][k]['outcome']})")
    print("\nPer task: outcome, final pos err m / heading err deg, switches: " + " | ".join(names))
    for k in keys:
        print(f"  {k[1]} {k[2]:g} kg rep {k[3]}: " + " | ".join(
            f"{data[a][k]['outcome']} {data[a][k]['pos_err']:.2f}/{data[a][k]['yaw_err']:.0f} sw {data[a][k]['switches']:.0f}"
            for a in names))


def main():
    mode = sys.argv[1]
    arms = dict(x.split("=", 1) for x in sys.argv[2:] if "=" in x and not x.startswith("--"))
    {"response": response, "compare": compare}[mode](arms)


if __name__ == "__main__":
    main()
