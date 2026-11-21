"""When a helper arrives, is it worth breaking an established contact? Learn the move type from the helper_branch
--movetypes twins (docs/late_help.md, "move types"). CPU only.

    python scripts/movetype_learn.py --train logs/evals/hbm-s1001 logs/evals/hbm-s1002 logs/evals/hbm-s1003 \
        --test logs/evals/hbm-s7900 --out logs/evals/movetype-learn

One decision per task, at the helper's arrival: keep both incumbents (0), move exactly one (1), move both (2); in
each, direct search supplies the best assignment of that group, and afterwards every branch replans the same way.
The payoff of a choice is the task's eventual success in that twin (all three are observed: the branches).
Only feasible groups can be chosen (a group with no feasible assignment is flagged by the twin).

Selectors (context = mass only; separate weights per mass):
  direct    the group of the highest-scoring assignment (direct search over all groups, from the logged scores)
  table     the group with the highest training success at that mass
  hedge     multiplicative weights, full feedback: every feasible group's outcome updates its weight
  exp3      bandit feedback: one group sampled, only its outcome seen, importance-weighted update
Training: the training tasks in random order (--orders orders); the learned selectors are then frozen (most likely
group) and scored on the test tasks with direct, table, pair alone, the add-on helper and, when present, jnet.
Reported: test success per selector and mass, paired differences vs direct search (bootstrap), training regret vs
the best fixed feasible group in hindsight.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
G = ("keep", "move1", "move2")


def load(dirs):
    tasks = defaultdict(dict)
    for d in dirs:
        p = Path(d)
        p = (p if p.is_absolute() else ROOT / p) / "episodes.csv"
        for r in csv.DictReader(open(p)):
            tasks[(r["object"], float(r["mass"]), r["scenario"], int(r["rep"]), str(d))][r["arm"]] = r
    out = []
    for k, tw in tasks.items():
        if "keep" not in tw or int(tw["keep"].get("ended_before_branch", 1)):
            continue
        y = np.array([int(tw[g]["success"]) for g in G], dtype=float)
        feas = np.array([not int(tw[g].get("group_infeasible", 0)) for g in G])
        sc = np.array([float(tw["keep"][f"group{q}_score"]) if tw["keep"].get(f"group{q}_score", "") != "" else -np.inf
                       for q in range(3)])
        feas &= np.isfinite(sc)
        if not feas.any():
            continue
        out.append({"key": k, "mass": k[1], "y": y, "feas": feas, "direct": int(np.argmax(np.where(feas, sc, -np.inf))),
                    "other": {a: int(tw[a]["success"]) for a in ("pair", "h1", "joint", "jnet", "null") if a in tw}})
    return out


def train(tasks, orders, seed=0):
    masses = sorted({t["mass"] for t in tasks})
    rng = np.random.default_rng(seed)
    T = len(tasks)
    res = {"hedge": {m: [] for m in masses}, "exp3": {m: [] for m in masses}}
    curves = {"hedge": [], "exp3": []}
    for _ in range(orders):
        order = rng.permutation(T)
        w = {alg: {m: np.zeros(3) for m in masses} for alg in ("hedge", "exp3")}
        n_m = defaultdict(int)
        for t in tasks:
            n_m[t["mass"]] += 1
        eta = {m: math.sqrt(8 * math.log(3) / max(n_m[m], 1)) for m in masses}
        gam = {m: min(1.0, math.sqrt(3 * math.log(3) / ((math.e - 1) * max(n_m[m], 1)))) for m in masses}
        got = {"hedge": np.zeros(T), "exp3": np.zeros(T)}
        Y = np.zeros((T, 3))
        F = np.zeros((T, 3), dtype=bool)
        for s_, i in enumerate(order):
            t = tasks[i]
            m, y, f = t["mass"], t["y"], t["feas"]
            Y[s_], F[s_] = y, f
            # hedge: play the mixture over feasible groups, see every feasible outcome
            wh = np.where(f, w["hedge"][m], -np.inf)
            ph = np.exp(wh - wh[f].max())
            ph /= ph.sum()
            got["hedge"][s_] = ph @ np.where(f, y, 0.0)
            w["hedge"][m] += eta[m] * np.where(f, y, 0.0)
            # exp3: sample one feasible group, see only its outcome
            we = np.where(f, w["exp3"][m], -np.inf)
            pe = np.exp(we - we[f].max())
            pe = (1 - gam[m]) * pe / pe.sum() + gam[m] * f / f.sum()
            a_ = rng.choice(3, p=pe)
            got["exp3"][s_] = y[a_]
            w["exp3"][m][a_] += gam[m] / f.sum() * y[a_] / pe[a_]
        # regret vs the best fixed group in hindsight (an infeasible pick falls back to direct search's group)
        direct = np.array([tasks[i]["direct"] for i in order])
        fixed = np.stack([np.where(F[:, q], Y[:, q], Y[np.arange(T), direct]) for q in range(3)], 1)
        best = np.cumsum(fixed, 0).max(1)
        for alg in got:
            curves[alg].append(best - np.cumsum(got[alg]))
            for m in masses:
                res[alg][m].append(w[alg][m].copy())
    frozen = {alg: {m: int(np.argmax(np.mean(res[alg][m], 0))) for m in masses} for alg in res}
    reg = {alg: np.mean(curves[alg], 0) for alg in curves}
    return frozen, reg


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--train", nargs="+", required=True)
    ap.add_argument("--test", nargs="+", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--orders", type=int, default=50)
    a = ap.parse_args()
    tr, te = load(a.train), load(a.test)
    masses = sorted({t["mass"] for t in tr + te})
    out = Path(a.out) if Path(a.out).is_absolute() else ROOT / a.out
    out.mkdir(parents=True, exist_ok=True)
    frozen, reg = train(tr, a.orders)
    table = {}
    for m in masses:
        sel = [t for t in tr if t["mass"] == m]
        rate = [np.mean([t["y"][q] if t["feas"][q] else t["y"][t["direct"]] for t in sel]) for q in range(3)]
        table[m] = int(np.argmax(rate))
    rng = np.random.default_rng(1)

    def pick(t, rule):
        q = {"direct": t["direct"], "table": table[t["mass"]], "hedge": frozen["hedge"][t["mass"]],
             "exp3": frozen["exp3"][t["mass"]]}[rule] if rule in ("direct", "table", "hedge", "exp3") else None
        return q if t["feas"][q] else t["direct"]

    L = [f"# Move type at the helper's arrival ({len(tr)} training / {len(te)} test decisions)", "",
         "Groups: keep both incumbents / move one / move both (direct search's best assignment within the group). "
         "Selectors trained on --train, frozen, scored on --test. Success %; differences vs direct search in pp with "
         "95% paired bootstrap over tasks.", "",
         "Frozen choices per mass: " + "; ".join(
             f"{m:g} kg: table {G[table[m]]}, hedge {G[frozen['hedge'][m]]}, exp3 {G[frozen['exp3'][m]]}" for m in masses), ""]
    summ = {"train": len(tr), "test": len(te), "table": {f"{m:g}": G[q] for m, q in table.items()},
            "frozen": {alg: {f"{m:g}": G[q] for m, q in v.items()} for alg, v in frozen.items()}, "test_by_mass": {}}
    for m in masses + ["all"]:
        sel = [t for t in te if m == "all" or t["mass"] == m]
        if not sel:
            continue
        rows = {}
        for rule in ("direct", "table", "hedge", "exp3"):
            rows[rule] = np.array([t["y"][pick(t, rule)] for t in sel])
        for g_ in range(3):
            rows[f"always {G[g_]}"] = np.array([t["y"][g_] if t["feas"][g_] else t["y"][t["direct"]] for t in sel])
        rows["best group (hindsight)"] = np.array([t["y"][t["feas"]].max() for t in sel])
        for o in ("pair", "h1", "joint", "jnet", "null"):
            if all(o in t["other"] for t in sel):
                rows[{"h1": "add-on helper", "pair": "pair alone"}.get(o, o)] = np.array([t["other"][o] for t in sel])
        base = rows["direct"]
        L += [f"## {m if m == 'all' else f'{m:g} kg'} ({len(sel)} test tasks)", "", "| selector | success | vs direct [95% CI] |",
              "|---|---|---|"]
        ent = {}
        for k, v in rows.items():
            d = v - base
            bs = d[rng.integers(0, len(d), (4000, len(d)))].mean(1)
            lo, hi = np.percentile(bs, [2.5, 97.5])
            ent[k] = [100 * v.mean(), 100 * d.mean(), 100 * lo, 100 * hi]
            L.append(f"| {k} | {100 * v.mean():.1f}% | {100 * d.mean():+.1f} [{100 * lo:+.1f}, {100 * hi:+.1f}] |")
        L.append("")
        summ["test_by_mass"][str(m)] = ent
    T = len(tr)
    L += [f"## Training regret vs the best fixed group ({a.orders} random orders, {T} decisions)", "",
          "| learner | after 50 | after 200 | at the end (total / per decision) |", "|---|---|---|---|"]
    for alg, c in reg.items():
        L.append(f"| {alg} | {c[min(49, T - 1)]:.1f} | {c[min(199, T - 1)]:.1f} | {c[-1]:.1f} / {c[-1] / T:.3f} |")
    summ["regret"] = {alg: {"end": float(c[-1]), "per_decision": float(c[-1] / T)} for alg, c in reg.items()}
    (out / "summary.md").write_text("\n".join(L) + "\n")
    (out / "summary.json").write_text(json.dumps(summ, indent=1))
    print("\n".join(L))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
