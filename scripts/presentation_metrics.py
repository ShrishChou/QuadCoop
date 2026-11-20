"""Evaluation metrics for the presentation folders (presentation_export/02-05), from the evaluators' episodes.csv
(scripts/eval_coop2.py for the single robot, IPPO and MAPPO; scripts/contact_test.py for the contact planner; same
columns for everything used here).

    python scripts/presentation_metrics.py metrics --csv <episodes.csv> --name "ANYmal single robot" --out <dir>
        -> <dir>/metrics.md, <dir>/metrics_by_case.csv (one row per mass x object x position), <dir>/episodes.csv
    python scripts/presentation_metrics.py compare --csv "Single robot=<csv>" --csv "IPPO=<csv>" ... --out <file.md>

Definitions (as the evaluators'):
  success        within 10 cm and 6 deg of the goal, held 1 s, within the 80 s horizon
  precise        within 10 cm and 3 deg with the object at rest
  time           seconds to success, over the successful trials only (n shown)
  fell           a robot fell (any robot; the single-robot runs park the second robot far away)
  timeout        the 80 s horizon ran out
  final error    distance / heading error to the goal when the trial ended (failed trials: where they stopped)
  closeness      final distance / task distance + final heading error / 180 deg (used to pick the best failed video)
"""
from __future__ import annotations

import argparse
import csv
import math
import shutil
import statistics as st
from collections import defaultdict
from pathlib import Path

SCEN_DESC = {"A_straight": "3 m straight ahead", "B_left": "3 m at 60 deg left, turn 30 deg",
             "C_backright": "3 m back-right (-135 deg), turn -60 deg", "D_far_turn": "5 m ahead, turn 90 deg"}


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def load(path: str) -> list[dict]:
    rows = list(csv.DictReader(open(path)))
    rows = [r for r in rows if r.get("formation", "standard") in ("", "standard") and str(r.get("swap", "0")) in ("", "0")]
    for r in rows:
        r["mass"] = num(r["mass"])
        r["success"] = int(float(r["success"]))
        r["precise"] = int(float(r.get("precise") or 0))
        r["t"] = num(r.get("t_success"))
        r["fell"] = int(any(int(float(r.get(k) or 0)) for k in r if k.startswith("fell_")))
        r["fe"] = num(r.get("final_pos_err"))
        r["fy"] = num(r.get("final_yaw_err"))
        r["me"] = num(r.get("min_pos_err"))
    return rows


def mean(xs):
    xs = [x for x in xs if x is not None]
    return st.mean(xs) if xs else None


def f1(x, nd=1, pct=False):
    if x is None:
        return "–"
    return f"{100 * x:.0f}%" if pct else f"{x:.{nd}f}"


def summarise(rs: list[dict]) -> dict:
    ts = [r["t"] for r in rs if r["success"] and r["t"] is not None]
    oc = defaultdict(int)
    for r in rs:
        oc[r["outcome"]] += 1
    return {"n": len(rs), "success": mean([r["success"] for r in rs]), "precise": mean([r["precise"] for r in rs]),
            "t_mean": mean(ts), "t_sd": st.stdev(ts) if len(ts) > 1 else None, "t_med": st.median(ts) if ts else None,
            "n_succ": len(ts), "fell": mean([r["fell"] for r in rs]),
            "timeout": oc.get("horizon", 0) / max(len(rs), 1),
            "other_fail": sum(v for k, v in oc.items() if k not in ("success", "horizon") and not k.startswith("fell")) / max(len(rs), 1),
            "fe": mean([r["fe"] for r in rs]), "fy": mean([r["fy"] for r in rs]), "me": mean([r["me"] for r in rs]),
            "outcomes": dict(oc)}


def fail_note(rs: list[dict]) -> str:
    bad = [r for r in rs if not r["success"]]
    if not bad:
        return ""
    oc = defaultdict(int)
    for r in bad:
        oc["timeout" if r["outcome"] == "horizon" else r["outcome"].replace("fell_", "fell ")] += 1
    best = min(bad, key=lambda r: (r["fe"] or 9e9))
    why = ", ".join(f"{v} {k}" for k, v in sorted(oc.items(), key=lambda kv: -kv[1]))
    return f"{len(bad)}/{len(rs)} failed ({why}; closest stop {f1(best['fe'], 2)} m / {f1(best['fy'], 0)} deg)"


def metrics(a) -> None:
    rows = load(a.csv)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    shutil.copy(a.csv, out / "episodes.csv")
    masses = sorted({r["mass"] for r in rows})
    objects = list(dict.fromkeys(r["object"] for r in rows))
    scens = list(dict.fromkeys(r["scenario"] for r in rows))
    reps = len({r["rep"] for r in rows})
    by = defaultdict(list)
    for r in rows:
        by[(r["mass"], r["object"], r["scenario"])].append(r)
    with open(out / "metrics_by_case.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["mass_kg", "object", "position", "trials", "success_rate", "precise_rate", "mean_time_s", "sd_time_s",
                    "successes", "fell_rate", "timeout_rate", "mean_final_pos_err_m", "mean_final_yaw_err_deg",
                    "mean_min_pos_err_m", "failure_note"])
        for (m, o, s), rs in sorted(by.items(), key=lambda kv: (kv[0][0], objects.index(kv[0][1]), scens.index(kv[0][2]))):
            S = summarise(rs)
            w.writerow([f"{m:g}", o, s, S["n"], f1(S["success"], 3), f1(S["precise"], 3), f1(S["t_mean"], 2),
                        f1(S["t_sd"], 2), S["n_succ"], f1(S["fell"], 3), f1(S["timeout"], 3), f1(S["fe"], 3),
                        f1(S["fy"], 1), f1(S["me"], 3), fail_note(rs)])
    L = [f"# {a.name}: evaluation metrics", "",
         f"{len(objects)} objects x {len(scens)} start positions x {len(masses)} masses x {reps} trials = {len(rows)} "
         f"episodes (seed {a.seed}; each trial a different random placement of the same task).", "",
         "Positions (goal relative to the start, robots behind the object): "
         + "; ".join(f"`{s}` {SCEN_DESC.get(s, '')}" for s in scens) + ".", "",
         "Success = within 10 cm and 6 deg of the goal, held 1 s, within 80 s. Time = seconds to success, averaged over "
         "the successful trials (n in brackets). Fell = a robot fell. Final error = where the object ended "
         "(failed trials included). Per-case rows (mass x object x position, 10 trials each): `metrics_by_case.csv`; "
         "every episode: `episodes.csv`.", "", "## By mass", "",
         "| mass | success | precise | mean time (s) | median time (s) | fell | timeout | final error (m / deg) |",
         "|---|---|---|---|---|---|---|---|"]
    for m in masses:
        S = summarise([r for r in rows if r["mass"] == m])
        L.append(f"| {m:g} kg | {f1(S['success'], pct=True)} | {f1(S['precise'], pct=True)} | {f1(S['t_mean'])} "
                 f"(n {S['n_succ']}) | {f1(S['t_med'])} | {f1(S['fell'], pct=True)} | {f1(S['timeout'], pct=True)} | "
                 f"{f1(S['fe'], 2)} / {f1(S['fy'], 0)} |")
    for m in masses:
        L += ["", f"## {m:g} kg: by object", "",
              "| object | success | mean time (s) | fell | final error (m / deg) | "
              + " | ".join(f"{s}" for s in scens) + " |",
              "|---|---|---|---|---|" + "---|" * len(scens)]
        for o in objects:
            rs = [r for r in rows if r["mass"] == m and r["object"] == o]
            S = summarise(rs)
            cells = []
            for s in scens:
                Sc = summarise(by[(m, o, s)])
                cells.append(f"{Sc['n_succ']}/{Sc['n']}" + (f", {Sc['t_mean']:.0f} s" if Sc["t_mean"] is not None else ""))
            L.append(f"| {o} | {f1(S['success'], pct=True)} | {f1(S['t_mean'])} (n {S['n_succ']}) | {f1(S['fell'], pct=True)} "
                     f"| {f1(S['fe'], 2)} / {f1(S['fy'], 0)} | " + " | ".join(cells) + " |")
    L += ["", "## Notes: positions with failures", "",
          "Per mass and object, each start position that failed at least once: failed / trials, how, and the closest "
          "any failed trial got.", ""]
    for m in masses:
        L.append(f"**{m:g} kg**")
        L.append("")
        for o in objects:
            notes = [f"`{s}` {fail_note(by[(m, o, s)])}" for s in scens if fail_note(by[(m, o, s)])]
            if notes:
                L.append(f"- {o}: " + "; ".join(notes))
        L.append("")
    if a.videos:
        L += ["## Videos", "",
              "One per mass x object x position: the fastest successful trial, or when none succeeded, the trial that "
              "ended closest to the goal (closeness = final distance / task distance + heading error / 180 deg). File "
              "name: `<object>_<mass>kg_<position>_rep<trial>__<outcome>.mp4`.", ""]
    (out / "metrics.md").write_text("\n".join(L) + "\n")
    print(f"wrote {out / 'metrics.md'}, {out / 'metrics_by_case.csv'}")


def compare(a) -> None:
    runs = []
    for spec in a.csv:
        name, path = spec.split("=", 1)
        runs.append((name, load(path)))
    masses = sorted({r["mass"] for _, rs in runs for r in rs})
    objects = list(dict.fromkeys(r["object"] for _, rs in runs for r in rs))
    names = [n for n, _ in runs]
    L = [f"# Comparison: {', '.join(names)}", "",
         "Same protocol for every system: the same objects, start positions, masses and seed, 10 trials per case. "
         "Success = 10 cm / 6 deg held 1 s within 80 s; time = mean seconds to success over successful trials (n).", "",
         "## By mass", "",
         "| mass | " + " | ".join(f"{n} success | {n} time (s) | {n} fell" for n in names) + " |",
         "|---|" + "---|---|---|" * len(names)]
    for m in masses:
        cells = []
        for _, rs in runs:
            S = summarise([r for r in rs if r["mass"] == m])
            cells += [f1(S["success"], pct=True), f"{f1(S['t_mean'])} (n {S['n_succ']})", f1(S["fell"], pct=True)]
        L.append(f"| {m:g} kg | " + " | ".join(cells) + " |")
    S_all = [(n, summarise(rs)) for n, rs in runs]
    L += ["", "Overall: " + "; ".join(f"{n} {f1(S['success'], pct=True)} success, {f1(S['t_mean'])} s"
                                      for n, S in S_all) + ".", ""]
    for m in masses:
        L += [f"## {m:g} kg: by object (success / mean time)", "",
              "| object | " + " | ".join(names) + " |", "|---|" + "---|" * len(names)]
        for o in objects:
            cells = []
            for _, rs in runs:
                S = summarise([r for r in rs if r["mass"] == m and r["object"] == o])
                cells.append("–" if not S["n"] else
                             f"{f1(S['success'], pct=True)} / {f1(S['t_mean'])} s" if S["t_mean"] is not None
                             else f"{f1(S['success'], pct=True)}")
            L.append(f"| {o} | " + " | ".join(cells) + " |")
        L.append("")
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text("\n".join(L) + "\n")
    print(f"wrote {a.out}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("metrics")
    p.add_argument("--csv", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--seed", default="7100")
    p.add_argument("--videos", action="store_true", help="add the video-selection note")
    p = sub.add_parser("compare")
    p.add_argument("--csv", action="append", required=True, help="NAME=path/to/episodes.csv (repeat)")
    p.add_argument("--out", required=True)
    a = ap.parse_args()
    {"metrics": metrics, "compare": compare}[a.cmd](a)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
