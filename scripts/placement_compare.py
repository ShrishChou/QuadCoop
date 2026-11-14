"""Start-placement comparison of trained pairs (eval_coop2.py --formations standard,flank,goal_behind --swap).

    python scripts/placement_compare.py --runs=IPPO:<eval>[+<rerun eval>],MAPPO:<eval>[+<rerun>],... [--out=FILE.md]
        [--focus=arch,cylinder,long,sphere] [--baseline=PARENT] [--pairs=F-A,B-A] [--diag=cylinder]
        [--reruns=IPPO:<rerun eval name>,...]   (older form of LABEL:a+b)

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
  reruns       with --reruns (a second evaluation of the same checkpoint and tasks): outcome flips between the
               two runs per formation, and each formation's change vs standard from the two-run mean per task,
               for every object; that is what to read for a per-object deficit
  pooled       (every run given) per base task (object, mass, scenario, rep): success averaged over the swap
               halves and the runs; a formation's change vs standard is the per-base-task difference, its 95% CI a
               bootstrap over base tasks (swaps and reruns stay together)
  baseline     --baseline=LABEL: each other policy's change vs standard minus the baseline's, per base task
  pairs        --pairs=X-Y: X minus Y success per formation, pooled the same way
  diag         --diag=OBJ: per formation, median time of the object's first 0.25 m of progress (and the share of
               episodes where it never came), median final distance to the goal, falls - getting the push going
               vs finishing it
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
    allruns = {lab: [load(x) for x in nm.split("+")] for lab, nm in runs}
    for x in (args["--reruns"].split(",") if "--reruns" in args else []):
        lab, nm = x.split(":", 1)
        if len(allruns[lab]) == 1:
            allruns[lab].append(load(nm))
    data = {lab: rr[0] for lab, rr in allruns.items()}  # the single-run sections: the first run
    runs = [(lab, nm.split("+")[0]) for lab, nm in runs]
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
        pairs = [(labs[i], labs[j]) for i in range(len(labs)) for j in range(i + 1, len(labs))]
        md += ["## Policies compared (paired, same tasks; single runs)", "",
               "| formation | " + " | ".join(f"{b} - {a} success [95% CI]" for a, b in pairs) + " |",
               "|---|" + "---|" * len(pairs)]
        idx = {lab: {(r["formation"], r["key"]): r for r in rows} for lab, rows in data.items()}
        for fm in forms:
            cells = []
            for a_, b_ in pairs:
                A, B = idx[a_], idx[b_]
                ks = [k for k in A if k[0] == fm and k in B]
                m, lo, hi = ci([B[k]["success"] - A[k]["success"] for k in ks])
                cells.append(f"{100 * m:+.1f} [{100 * lo:+.1f}, {100 * hi:+.1f}] pts")
            md.append(f"| {fm} | " + " | ".join(cells) + " |")
    # -- pooled over swaps and runs, per base task --------------------------------------------------------------
    def pooled(lab):
        acc = defaultdict(lambda: [0.0, 0])
        for rows in allruns[lab]:
            for r in rows:
                a_ = acc[(r["formation"], r["key"][:4])]
                a_[0] += r["success"]
                a_[1] += 1
        return {k: v[0] / v[1] for k, v in acc.items()}

    P = {lab: pooled(lab) for lab in allruns}
    nruns = {lab: len(rr) for lab, rr in allruns.items()}
    groups = [("all ten", None)] + [(o, o) for o in sorted({k[1][0] for k in next(iter(P.values()))})]
    sel = lambda ks, o: [k for k in ks if o is None or k[0] == o]  # noqa: E731
    std_b = lambda lab: sorted(k[1] for k in P[lab] if k[0] == "standard")  # noqa: E731

    def change(lab, fm, o):
        return {b: P[lab][(fm, b)] - P[lab][("standard", b)] for b in sel(std_b(lab), o) if (fm, b) in P[lab]}

    def cell(d):
        if not d:
            return "-"
        m, lo, hi = ci(d)
        return f"{100 * m:+.1f} [{100 * lo:+.1f}, {100 * hi:+.1f}]" + (" **" if hi < 0 or lo > 0 else "")

    md += ["", "## Pooled over swaps and runs (per base task; ** = interval excludes 0)", ""]
    for lab, rr in allruns.items():
        if len(rr) > 1:
            fl = []
            for fm in forms:
                a1 = {r["key"]: r["success"] for r in rr[0] if r["formation"] == fm}
                a2 = {r["key"]: r["success"] for r in rr[1] if r["formation"] == fm}
                fl.append(f"{fm} {sum(a1[k] != a2[k] for k in a1 if k in a2)}")
            md.append(f"- {lab}: rerun flips (of 960 per formation): " + ", ".join(fl))
    md += ["", "### Success rate", "",
           "| object | " + " | ".join(f"{lab} ({nruns[lab]} run{'s' if nruns[lab] > 1 else ''}) {fm}"
                                     for lab in P for fm in forms) + " |",
           "|---|" + "---|" * (len(P) * len(forms))]
    for gname, o in groups:
        cells = []
        for lab in P:
            for fm in forms:
                v = [P[lab][(fm, b)] for b in sel(std_b(lab), o) if (fm, b) in P[lab]]
                cells.append(f"{sum(v) / len(v):.1%}" if v else "-")
        md.append(f"| {gname} | " + " | ".join(cells) + " |")
    md += ["", "### Change vs standard (points [95% CI])", "",
           "| object | " + " | ".join(f"{lab} {fm}" for lab in P for fm in forms if fm != "standard") + " |",
           "|---|" + "---|" * (len(P) * (len(forms) - 1))]
    for gname, o in groups:
        md.append(f"| {gname} | " + " | ".join(cell(list(change(lab, fm, o).values()))
                                              for lab in P for fm in forms if fm != "standard") + " |")
    if "--baseline" in args:
        bl = args["--baseline"]
        others = [lab for lab in P if lab != bl]
        md += ["", f"### Change vs standard, minus {bl}'s (per base task; points [95% CI])", "",
               "| object | " + " | ".join(f"{lab} - {bl} {fm}" for lab in others for fm in forms if fm != "standard") + " |",
               "|---|" + "---|" * (len(others) * (len(forms) - 1))]
        for gname, o in groups:
            cells = []
            for lab in others:
                for fm in forms:
                    if fm == "standard":
                        continue
                    c1, c0 = change(lab, fm, o), change(bl, fm, o)
                    cells.append(cell([c1[b] - c0[b] for b in c1 if b in c0]))
            md.append(f"| {gname} | " + " | ".join(cells) + " |")
    for pr in (args["--pairs"].split(",") if "--pairs" in args else []):
        x, y = pr.split("-")
        md += ["", f"### {x} - {y}, success per formation (per base task; points [95% CI])", "",
               "| object | " + " | ".join(forms) + " |", "|---|" + "---|" * len(forms)]
        for gname, o in groups:
            cells = []
            for fm in forms:
                ks = [k for k in P[x] if k[0] == fm and k in P[y] and (o is None or k[1][0] == o)]
                cells.append(cell([P[x][k] - P[y][k] for k in ks]))
            md.append(f"| {gname} | " + " | ".join(cells) + " |")
    for o in (args["--diag"].split(",") if "--diag" in args else []):
        md += ["", f"### {o}: getting the push going vs finishing it (all runs and swaps)", "",
               "| policy | formation | n | success | falls | first 0.25 m progress, median s | never progressed "
               "| final distance to goal, median m | final distance, failures, median m |",
               "|---|---|---|---|---|---|---|---|---|"]
        for lab, rr in allruns.items():
            for fm in forms:
                R = [r for rows in rr for r in rows if r["formation"] == fm and r["object"] == o]
                if not R:
                    continue
                tg = [float(r["t_progress"]) for r in R if r["t_progress"]]
                fd = [float(r["final_pos_err"]) for r in R]
                ff = [float(r["final_pos_err"]) for r in R if not r["success"]]
                md.append(f"| {lab} | {fm} | {len(R)} | {sum(r['success'] for r in R) / len(R):.1%} | "
                          f"{sum(r['fell'] for r in R) / len(R):.1%} | {st.median(tg) if tg else float('nan'):.1f} | "
                          f"{(len(R) - len(tg)) / len(R):.1%} | {st.median(fd):.2f} | "
                          f"{st.median(ff) if ff else float('nan'):.2f} |")
    text = "\n".join(md) + "\n"
    if "--out" in args:
        Path(args["--out"]).parent.mkdir(parents=True, exist_ok=True)
        Path(args["--out"]).write_text(text)
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
