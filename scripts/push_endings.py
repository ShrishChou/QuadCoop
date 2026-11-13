"""Why do requested joint pushes end? (residual pilot close-out; CPU analysis of existing 10 Hz traces, --trace 2)

  python scripts/push_endings.py r2dev-base:4000,4001,4002 r2dev-resid:4000 r2dev-resid600:4001,4002 [--objects=beam]

Denominator: "both requested" = live, the planner wants motion (want_speed >= 0.03 m/s or |want_yaw_rate| >= 5 deg/s)
and both robots are engaged with a commanded share >= 0.15. Time when the planner wants one robot only is excluded.
A robot "presses" when, averaged over a centred 1 s window (the raw 10 Hz contact pulses with the gait), it touches
the object at least half the time and pushes >= 30 N along the commanded direction. This is physical contact, not the
planner's on_contact flag: robots often press 0.25-0.4 m from their assigned point (more so on heavy beams), outside
on_contact's drift radius, so the flag flickers while force is delivered. "off-point %" reports that separately.
A "delivery bout" (gait-averaged joint force delivery) is a run of both-requested samples where both press. Because of
the 1 s averaging this is NOT continuous simultaneous contact: two robots touching in alternation also count (a
synthetic 10 s sequence of strictly alternating contact gives one 9 s bout, with 0 s simultaneous). "simultaneous %" reports the share of
requested-both time with both robots touching at the same 10 Hz sample, unsmoothed. It ends at the first sample where a condition holds for >= 0.3 s
(3 samples; shorter dips are bridged), classified by the first condition, in this priority order:
  fell       a robot has fallen (checked first: a fall also ends the episode and the request)
  episode    the episode ended (live false without a fall: success or time limit), or the trace ended in the bout
  request    the planner stopped requesting both (motion done, single-robot share)
  reassign   a robot's contact index changed (planner replan)
  touch      a robot stopped touching (1 s touching share < 0.5)
  force      both still touching but a robot's 1 s mean force along the command fell below 30 N
Table 1, per arm x mass: requested-both s/ep, simultaneous %, share of it in delivery bouts, bouts/ep, median / 90th pct bout
length (s), share of requested-both time in bouts >= 2 s, off-point % (joint-push time with a robot outside on_contact:
>= drift_dist 0.25 m from its point or >= 30 deg off the push direction), then the ending classes (share of bouts), and the share of
"touch" endings followed by a fall within 3 s (falls show up there: a robot about to fall loses touch for >= 0.3 s
first, so bouts rarely end as "fell").
Table 2 (delivered force), per arm x mass, inside sustained delivery bouts (>= 2 s): total 1 s mean force along the
command (p50 / p90), smoothed beam speed (p50) and the share of samples with the beam moving >= 0.03 m/s; then, over all
delivery-bout samples, each robot's 1 s mean force along the command while its forward walker command is held at the
walker's 0.8 m/s limit (>= 0.79 m/s for >= 90% of the window), p50 / p90, and the share of samples held there.
"""
import csv
import gzip
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
AG = ("anymal1", "anymal2")
P_N, HOLD, WIN = 30.0, 3, 10
CLASSES = ("fell", "episode", "request", "reassign", "touch", "force")


def episodes(path):
    rows, key, last_t = [], None, 1e9
    for r in csv.DictReader(gzip.open(path, "rt")):
        t, k = float(r["t"]), (r["object"], r["scenario"])
        if rows and (t < last_t or k != key):
            yield key, rows
            rows = []
        key, last_t = k, t
        rows.append(r)
    if rows:
        yield key, rows


def analyse(rows):
    g = lambda c: np.array([float(r[c]) if r[c] not in ("", "nan") else np.nan for r in rows])  # noqa: E731
    n = len(rows)
    want = (g("live") > .5) & ((g("want_speed") >= .03) | (np.abs(g("want_yaw_rate_deg")) >= 5.0))
    eng = [(g(f"engaged_{a}") > .5) & (g(f"share_cmd_{a}") >= .15) for a in AG]
    req = want & eng[0] & eng[1]
    on = [g(f"on_{a}") > .5 for a in AG]
    sm = lambda v: np.convolve(np.nan_to_num(v), np.ones(WIN) / WIN, mode="same")  # noqa: E731
    fa = [sm(g(f"force_along_cmd_{a}")) for a in AG]
    tc = [sm(g(f"touching_{a}")) >= 0.5 for a in AG]
    press = [tc[i] & (fa[i] >= P_N) for i in range(2)]
    joint = req & press[0] & press[1]
    live = g("live") > .5
    fell = np.maximum.accumulate((g("fell_anymal1") > .5) | (g("fell_anymal2") > .5))  # stays set after a fall
    raw_t = [g(f"touching_{a}") > .5 for a in AG]
    cid = [g(f"cidx_{a}") for a in AG]
    bouts, long_ix, touch_fall, i = [], [], [], 0
    while i < n:
        if not joint[i]:
            i += 1
            continue
        s, j, last = i, i, i
        while j < n and j - last <= HOLD:  # extend the bout over dips shorter than HOLD samples
            if joint[j]:
                last = j
            j += 1
        e = last + 1  # first sample of the persisting break
        if e >= n or j - last <= HOLD:  # the trace ended inside the bout or inside a short dip (a fall ends the
            cls = "fell" if fell[n - 1] else "episode"  # trace within 1-3 samples, before a 0.3 s break can show)
        else:
            k = e
            if fell[k]:
                cls = "fell"
            elif not live[k]:
                cls = "episode"
            elif not req[k]:
                cls = "request"
            elif any(cid[a][k] != cid[a][e - 1] for a in range(2)):
                cls = "reassign"
            elif not (tc[0][k] and tc[1][k]):
                cls = "touch"
            else:
                cls = "force"
        bouts.append(((e - s) / 10.0, cls))
        if cls == "touch":  # did this loss of touch precede a fall (within 3 s)?
            touch_fall.append(bool(fell[min(n - 1, e + 30)]))
        if e - s >= 20:
            long_ix.append(np.arange(s, e))
        i = j
    li = np.concatenate(long_ix) if long_ix else np.zeros(0, dtype=int)
    held = [sm(g(f"wcmd_vx_{a}") >= .79) >= .9 for a in AG]
    return dict(req_s=req.sum() / 10.0, joint_s=joint.sum() / 10.0, sim_s=(req & raw_t[0] & raw_t[1]).sum() / 10.0, off_s=(joint & ~(on[0] & on[1])).sum() / 10.0, bouts=bouts, touch_fall=touch_fall,
                f_long=(fa[0] + fa[1])[li], v_long=sm(g("obj_speed"))[li],
                f_held=np.concatenate([fa[a][joint & held[a]] for a in range(2)]), n_joint=2 * int(joint.sum()))


def main():
    arms, objs = [], None
    for x in sys.argv[1:]:
        if x.startswith("--objects="):
            objs = x.split("=", 1)[1].split(",")
        else:
            p, s = x.split(":")
            arms.append((p, [int(v) for v in s.split(",")]))
    print("| arm | seeds | mass | eps | req-both s/ep | simultaneous % | delivery % of req | bouts/ep | bout s med / p90 | "
          "req time in bouts >= 2 s % | off-point % | " + " | ".join(CLASSES) + " | touch then fell <= 3 s % |")
    print("|---" * (12 + len(CLASSES)) + "|")
    table2 = []
    for p, seeds in arms:
        res = defaultdict(list)
        for s in seeds:
            d = ROOT / "logs" / "evals" / f"{p}-s{s}-expert" / "pair"
            for f in sorted(d.glob("trace_*kg.csv.gz")):
                m = float(f.name.split("_")[1].replace("kg.csv.gz", ""))
                for (o, _), rows in episodes(f):
                    if objs is None or o in objs:
                        res[m].append(analyse(rows))
        for m, L in sorted(res.items()):
            req = sum(x["req_s"] for x in L)
            joint = sum(x["joint_s"] for x in L)
            b = [bt for x in L for bt in x["bouts"]]
            ln = np.array([x for x, _ in b]) if b else np.zeros(0)
            c = Counter(cl for _, cl in b)
            long_t = ln[ln >= 2.0].sum()
            print(f"| {p} | {','.join(map(str, seeds))} | {m:g} | {len(L)} | {req / len(L):.1f} | "
                  f"{100 * sum(x['sim_s'] for x in L) / max(req, 1e-9):.0f} | {100 * joint / max(req, 1e-9):.0f} | {len(b) / len(L):.1f} | "
                  f"{np.median(ln) if len(ln) else 0:.1f} / {np.percentile(ln, 90) if len(ln) else 0:.1f} | "
                  f"{100 * long_t / max(req, 1e-9):.0f} | {100 * sum(x['off_s'] for x in L) / max(joint, 1e-9):.0f} | "
                  + " | ".join(f"{100 * c[k] / max(len(b), 1):.0f}" for k in CLASSES)
                  + f" | {100 * np.mean(tf) if (tf := [v for x in L for v in x['touch_fall']]) else 0:.0f} |")
            fl, vl, fh = (np.concatenate([x[k] for x in L]) for k in ("f_long", "v_long", "f_held"))
            q = lambda v: f"{np.percentile(v, 50):.0f} / {np.percentile(v, 90):.0f}" if len(v) else "-"  # noqa: E731
            table2.append(f"| {p} | {','.join(map(str, seeds))} | {m:g} | {len(fl) / 10 / len(L):.1f} | {q(fl)} | "
                          f"{np.median(vl) if len(vl) else float('nan'):.3f} | {100 * np.mean(vl >= .03) if len(vl) else float('nan'):.0f} | "
                          f"{q(fh)} | {100 * len(fh) / max(sum(x['n_joint'] for x in L), 1):.0f} |")
    print("\n| arm | seeds | mass | sustained s/ep | total F along N p50 / p90 | beam speed p50 m/s | moving % | "
          "per-robot F at cmd limit N p50 / p90 | held at limit % |")
    print("|---" * 9 + "|")
    print("\n".join(table2))


if __name__ == "__main__":
    main()
