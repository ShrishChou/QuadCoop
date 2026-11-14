"""Start-placement comparison of trained pairs (eval_coop2.py --formations standard,flank,goal_behind --swap).

    python scripts/placement_compare.py --runs=IPPO:<eval name>,MAPPO:<eval name>[,...] [--out=FILE.md]
        [--focus=arch,cylinder,long,sphere]

Each eval holds every task (object x mass x scenario x rep, the 480 seed-7100 benchmark tasks) in each formation,
unswapped and with the robots' start places exchanged; object, mass, goal, gaps and jitter are the same draw in
all of them. Tasks are matched on (object, mass, scenario, rep, swap). Reported per policy:

  formation    success, falls, precise; paired change vs standard [95% bootstrap CI over matched tasks];
               for all ten objects and each --focus object
  timing       median time of the first push by either robot, and of the object's first 0.25 m of progress
               (episodes where it happened), and the share where it never happened
  roles        who leads (more push time) and who pushes first, by start role and by identity, unswapped vs
               swapped. If leading follows the start place, P(leader = role) is similar in both halves and
               P(leader = anymal1) flips; if it follows the identity, the reverse.
  takeover     share of episodes where the robot that did not push first later pushed alone while the object
               moved >= 0.2 m closer to the goal, and the success of those episodes
  policies     paired difference between policies per formation (same tasks)
Rerun noise: one GPU evaluation rerun flips ~15% of outcomes (docs/ten_restart.md); differences inside that are
not findings.
"""
from __future__ import annotations

import csv
import random
import statistics as st
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AG = ("anymal1", "anymal2")


def load(name: str) -> list[dict]:
    rows = list(csv.DictReader(open(ROOT / "evals" / name / "eval" / "pair" / "episodes.csv")))
    for r in rows:
        r["key"] = (r["object"], float(r["mass"]), r["scenario"], int(r["rep"]), int(r["swap"]))
        r["success"], r["precise"] = int(r["success"]), int(r["precise"])
        r["fell"] = int(int(r["fell_anymal1"]) or int(r["fell_anymal2"]))
    return rows


def ci(d, n=4000, seed=0):
    rng = random.Random(seed)
    m = sum(d) / len(d)
    bs = sorted(sum(rng.choice(d) for _ in d) / len(d) for _ in range(n))
    return m, bs[int(0.025 * n)], bs[int(0.975 * n) - 1]


def pct(x, n):
    return f"{x}/{n} ({x / n:.0%})" if n else "-"


def fnum(x):
    return float(x) if x not in ("", None) else None


def leader(r):
    a, b = float(r["push_frac_anymal1"] or 0), float(r["push_frac_anymal2"] or 0)
    return None if a == b else (AG[0] if a > b else AG[1])


def role_of(r, ag):
    return r[f"role_{ag}"]


def main() -> int:
    args = dict(x.split("=", 1) for x in sys.argv[1:] if x.startswith("--") and "=" in x)
    runs = [x.split(":", 1) for x in args["--runs"].split(",")]
    focus = args.get("--focus", "arch,cylinder,long,sphere").split(",")
    data = {lab: load(nm) for lab, nm in runs}
    md = [f"# Start placements: {', '.join(f'{l} = `{n}`' for l, n in runs)}", ""]
    forms = list(dict.fromkeys(r["formation"] for r in next(iter(data.values()))))
    for lab, rows in data.items():
        F = defaultdict(dict)
        for r in rows:
            F[r["formation"]][r["key"]] = r
        std = F.get("standard", {})
        md += [f"## {lab}", "", "### Success by formation (unswapped and swapped pooled)", "",
               "| formation | objects | n | success | falls | precise | success change vs standard [95% CI] |",
               "|---|---|---|---|---|---|---|"]
        for fm in forms:
            for what, objs in [("all ten", None)] + [(o, [o]) for o in focus]:
                ks = [k for k in F[fm] if objs is None or k[0] in objs]
                if not ks:
                    continue
                R = [F[fm][k] for k in ks]
                s_, f_, p_ = (sum(r[x] for r in R) for x in ("success", "fell", "precise"))
                ch = ""
                if fm != "standard":
                    m_ = [k for k in ks if k in std]
                    if m_:
                        m, lo, hi = ci([F[fm][k]["success"] - std[k]["success"] for k in m_])
                        ch = f"{100 * m:+.1f} [{100 * lo:+.1f}, {100 * hi:+.1f}] pts"
                md.append(f"| {fm} | {what} | {len(R)} | {pct(s_, len(R))} | {pct(f_, len(R))} | {pct(p_, len(R))} | {ch} |")
        md += ["", "### Success by formation and mass (all ten)", "",
               "| formation | " + " | ".join(f"{m:g} kg" for m in sorted({k[1] for k in std or F[forms[0]]})) + " |",
               "|---|" + "---|" * len({k[1] for k in std or F[forms[0]]})]
        for fm in forms:
            ms = sorted({k[1] for k in F[fm]})
            md.append(f"| {fm} | " + " | ".join(
                f"{sum(r['success'] for k, r in F[fm].items() if k[1] == m) / max(1, sum(1 for k in F[fm] if k[1] == m)):.0%}"
                for m in ms) + " |")
        md += ["", "### Timing (seconds from the start)", "",
               "| formation | first push, median | never pushed | first 0.25 m progress, median | never progressed |",
               "|---|---|---|---|---|"]
        for fm in forms:
            R = list(F[fm].values())
            tp = [min(v for v in (fnum(r["t_push_anymal1"]), fnum(r["t_push_anymal2"])) if v is not None)
                  for r in R if r["t_push_anymal1"] or r["t_push_anymal2"]]
            tg = [fnum(r["t_progress"]) for r in R if r["t_progress"]]
            md.append(f"| {fm} | {st.median(tp):.1f} | {pct(len(R) - len(tp), len(R))} | "
                      f"{st.median(tg) if tg else float('nan'):.1f} | {pct(len(R) - len(tg), len(R))} |")
        md += ["", "### Roles: who leads (more push time) and who pushes first", "",
               "| formation | half | n | leader = anymal1 | leader by start role | first pusher = anymal1 | first pusher by start role | success |",
               "|---|---|---|---|---|---|---|---|"]
        for fm in forms:
            for w in (0, 1):
                R = [r for r in F[fm].values() if r["key"][4] == w]
                if not R:
                    continue
                L = [(r, leader(r)) for r in R if leader(r)]
                P = [r for r in R if r["first_pusher"]]
                rl = defaultdict(int)
                for r, ag in L:
                    rl[role_of(r, ag)] += 1
                rf = defaultdict(int)
                for r in P:
                    rf[role_of(r, r["first_pusher"])] += 1
                md.append(f"| {fm} | {'swapped' if w else 'unswapped'} | {len(R)} | "
                          f"{pct(sum(ag == AG[0] for _, ag in L), len(L))} | "
                          + ", ".join(f"{k} {v / len(L):.0%}" for k, v in sorted(rl.items())) + " | "
                          f"{pct(sum(r['first_pusher'] == AG[0] for r in P), len(P))} | "
                          + ", ".join(f"{k} {v / len(P):.0%}" for k, v in sorted(rf.items())) + " | "
                          f"{pct(sum(r['success'] for r in R), len(R))} |")
        md += ["", "### Swap: same task, start places exchanged", "",
               "| formation | matched pairs | success unswapped / swapped | outcome differs | leader follows the start place | leader follows identity |",
               "|---|---|---|---|---|---|"]
        for fm in forms:
            u = {k[:4]: r for k, r in F[fm].items() if k[4] == 0}
            s_ = {k[:4]: r for k, r in F[fm].items() if k[4] == 1}
            ks = [k for k in u if k in s_]
            if not ks:
                continue
            both = [(u[k], s_[k]) for k in ks if leader(u[k]) and leader(s_[k])]
            place = sum(role_of(a_, leader(a_)) == role_of(b_, leader(b_)) for a_, b_ in both)
            ident = sum(leader(a_) == leader(b_) for a_, b_ in both)
            md.append(f"| {fm} | {len(ks)} | {sum(u[k]['success'] for k in ks)} / {sum(s_[k]['success'] for k in ks)} | "
                      f"{sum(u[k]['success'] != s_[k]['success'] for k in ks)} | {pct(place, len(both))} | {pct(ident, len(both))} |")
        md += ["", "### Takeover: the second robot pushes alone while the object moves >= 0.2 m toward the goal", "",
               "| formation | episodes with a takeover | their success | success of the rest |", "|---|---|---|---|"]
        for fm in forms:
            R = list(F[fm].values())
            T = [r for r in R if float(r["takeover_prog"]) >= 0.2]
            O = [r for r in R if float(r["takeover_prog"]) < 0.2]
            md.append(f"| {fm} | {pct(len(T), len(R))} | {pct(sum(r['success'] for r in T), len(T))} | "
                      f"{pct(sum(r['success'] for r in O), len(O))} |")
        md.append("")
    if len(data) >= 2:
        labs = list(data)
        md += ["## Policies compared (paired, same tasks)", "",
               "| formation | " + f" {labs[1]} - {labs[0]} success [95% CI] |", "|---|---|"]
        A = {(r["formation"], r["key"]): r for r in data[labs[0]]}
        B = {(r["formation"], r["key"]): r for r in data[labs[1]]}
        for fm in forms:
            ks = [k for k in A if k[0] == fm and k in B]
            m, lo, hi = ci([B[k]["success"] - A[k]["success"] for k in ks])
            md.append(f"| {fm} | {100 * m:+.1f} [{100 * lo:+.1f}, {100 * hi:+.1f}] pts (n {len(ks)}) |")
    text = "\n".join(md) + "\n"
    if "--out" in args:
        Path(args["--out"]).parent.mkdir(parents=True, exist_ok=True)
        Path(args["--out"]).write_text(text)
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
