"""Command-to-force probe (docs/command_force.md): how does one robot's fixed forward command change the force it and
its partner deliver, contact retention and object motion?

  python scripts/cmd_force_probe.py [--levels 0.8,0.6,0.4,0.2,0.0] [--window 2,12]

Reads logs/evals/cp-<robot>-v<level>-expert/pair (contact_test.py --cmd-probe <robot>,<level>,0.8 --trace 2): the
probe robot's forward command fixed at <level> m/s, its partner's at 0.8 m/s, both all episode, lateral / heading
from the frozen executor; matched resets across levels (same seed, tasks and contacts, contacts fixed).
Per episode, over live samples in the window (10 Hz):
  F_probe, F_partner   mean force along each robot's push direction (N; the window mean averages over gait cycles)
  share                F_probe / (F_probe + F_partner) of the clipped-at-0 means
  touch_p, touch_q     share of samples touching the object; both = both at once
  on_p                 share of samples on the assigned contact (planner's drift radius)
  speed, yaw           mean object speed (m/s); |heading change| over the window (deg)
  vx_applied           the probe robot's mean walker forward command (check that the override took)
  fell                 a robot fell (the window ends there)
Paired against the 0.8 m/s level (the frozen executor's usual saturated command), task by task: mean [95% bootstrap CI].
"""
import csv
import gzip
import random
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
AG = ("anymal1", "anymal2")


def episodes(path):
    rows, key, last_t, cnt = [], None, 1e9, defaultdict(int)
    for r in csv.DictReader(gzip.open(path, "rt")):
        t, k = float(r["t"]), (r["object"], r["scenario"])
        if rows and (t < last_t or k != key):
            yield key, cnt[key], rows
            cnt[key] += 1
            rows = []
        key, last_t = k, t
        rows.append(r)
    if rows:
        yield key, cnt[key], rows


def metrics(rows, probe, window):
    g = lambda c: np.array([float(r[c]) if r[c] not in ("", "nan") else np.nan for r in rows])  # noqa: E731
    q = AG[1 - AG.index(probe)]
    t = g("t")
    live = g("live") > .5
    w = live & (t >= window[0]) & (t <= window[1])
    fell = any(float(r[f"fell_{a}"]) > .5 for r in rows for a in AG)
    if w.sum() < 30:  # under 3 s of window
        return dict(fell=float(fell), n=int(w.sum()))
    fp, fq = g(f"force_along_cmd_{probe}")[w], g(f"force_along_cmd_{q}")[w]
    tp, tq = g(f"touching_{probe}")[w] > .5, g(f"touching_{q}")[w] > .5
    yaw = g("obj_yaw_deg")[w]
    d = (yaw - yaw[0] + 180.0) % 360.0 - 180.0
    mp, mq = max(np.nanmean(fp), 0.0), max(np.nanmean(fq), 0.0)
    return dict(n=int(w.sum()), F_probe=float(np.nanmean(fp)), F_partner=float(np.nanmean(fq)),
                F_total=float(np.nanmean(fp + fq)), share=mp / (mp + mq) if mp + mq > 1e-6 else np.nan,
                touch_p=float(tp.mean()), touch_q=float(tq.mean()), both=float((tp & tq).mean()),
                on_p=float((g(f"on_{probe}")[w] > .5).mean()), speed=float(np.nanmean(g("obj_speed")[w])),
                yaw=float(np.max(np.abs(d))), vx_applied=float(np.nanmean(g(f"wcmd_vx_{probe}")[w])), fell=float(fell))


def ci(d, n=2000, seed=0):
    d = [x for x in d if x == x]
    if not d:
        return float("nan"), float("nan"), float("nan")
    rng = random.Random(seed)
    m = lambda v: sum(v) / len(v)  # noqa: E731
    bs = sorted(m([rng.choice(d) for _ in d]) for _ in range(n))
    return m(d), bs[int(0.025 * n)], bs[int(0.975 * n) - 1]


def main():
    levels, window = ["0.8", "0.6", "0.4", "0.2", "0.0"], (2.0, 12.0)
    for x in sys.argv[1:]:
        if x.startswith("--levels="):
            levels = x.split("=", 1)[1].split(",")
        elif x.startswith("--window="):
            window = tuple(float(v) for v in x.split("=", 1)[1].split(","))
    data = {}  # (probe, level) -> {(mass, rep): metrics}
    for probe in AG:
        for lv in levels:
            d = ROOT / "logs" / "evals" / f"cp-{probe}-v{lv.replace('.', '')}-expert" / "pair"
            out = {}
            for f in sorted(d.glob("trace_*kg.csv.gz")):
                mass = float(f.name.split("_")[1].replace("kg.csv.gz", ""))
                for _, rep, rows in episodes(f):
                    out[(mass, rep)] = metrics(rows, probe, window)
            data[(probe, lv)] = out
    keys = sorted(set.intersection(*[set(v) for v in data.values()]))
    cols = ("F_probe", "F_partner", "F_total", "share", "touch_p", "touch_q", "both", "on_p", "speed", "yaw", "vx_applied", "fell")
    print(f"window {window} s; {len(keys)} matched tasks per probe robot and level (masses x reps); partner at 0.8 m/s\n")
    print("| mass | probe vx | n | " + " | ".join(cols) + " |")
    print("|---" * (3 + len(cols)) + "|")
    for mass in sorted({k[0] for k in keys}):
        for lv in levels:
            rs = [data[(p, lv)][k] for p in AG for k in keys if k[0] == mass]
            print(f"| {mass:g} | {lv} | {len(rs)} | " + " | ".join(
                f"{np.nanmean([r.get(c, np.nan) for r in rs]):.3f}" for c in cols) + " |")
    print(f"\nPaired change vs probe vx 0.8 (same task, same probe robot): mean [95% CI]")
    pc = ("F_probe", "F_partner", "F_total", "share", "touch_p", "both", "speed", "yaw")
    print("| mass | probe vx | " + " | ".join(pc) + " |")
    print("|---" * (2 + len(pc)) + "|")
    for mass in sorted({k[0] for k in keys}):
        for lv in levels[1:]:
            cells = []
            for c in pc:
                dd = [data[(p, lv)][k].get(c, np.nan) - data[(p, levels[0])][k].get(c, np.nan)
                      for p in AG for k in keys if k[0] == mass]
                mu, lo, hi = ci(dd)
                cells.append(f"{mu:+.3f} [{lo:+.3f}, {hi:+.3f}]")
            print(f"| {mass:g} | {lv} | " + " | ".join(cells) + " |")
    print("\nPer task (probe robot, mass, rep): share / F_probe / F_partner / both / fell, by level " + " | ".join(levels))
    for p in AG:
        for k in keys:
            print(f"  {p} {k[0]:g} kg rep {k[1]}: " + " | ".join(
                f"{data[(p, lv)][k].get('share', np.nan):.2f} / {data[(p, lv)][k].get('F_probe', np.nan):.0f} / "
                f"{data[(p, lv)][k].get('F_partner', np.nan):.0f} / {data[(p, lv)][k].get('both', np.nan):.2f} / "
                f"{data[(p, lv)][k].get('fell', np.nan):.0f}" for lv in levels))


if __name__ == "__main__":
    main()
