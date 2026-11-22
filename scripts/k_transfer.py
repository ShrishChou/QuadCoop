"""Does a dispatcher trained at 2 -> 3 make useful 3 -> 4 decisions without retraining? CPU only, on chain4_branch trees.

    python scripts/k_transfer.py --train logs/evals/k4-s1001 logs/evals/k4-s1002 logs/evals/k4-s1003 \
        --test logs/evals/k4-s8201 logs/evals/k4-s8202 --out logs/evals/k-transfer

Decisions at t2 (60 s left), from chain4_branch's tree:
  2 -> 3: the pair (k2) still pushing; stay = k2, recruit = k3b, null = k2null.
  3 -> 4: the trio (k3) still pushing; stay = k3, recruit = k4, null = k3null.
Features with the same meaning at every team size: distance / heading left, start distance, object speed, yaw rate,
progress rate, stall time, force per robot, fraction of robots pressing, the next helper's unoccupied useful contacts
(count, best score), log struggle ratio, object identity; and, declared, the mass (log + one-hot).

Rules, each fitted on --train only:
  transferred   T-learner (P(delivery | h, stay), P(delivery | h, recruit)) fitted on 2 -> 3, frozen, applied to 3 -> 4
  in-domain     the same model fitted on 3 -> 4
  mass (2->3) / mass (3->4)   training uplift per mass
  random, always stay, always recruit
Reported on --test 3 -> 4 decisions: the within-mass top-half - bottom-half uplift (endpoint B), net deliveries per
100 calls at a 10% budget, and the independent ask rule (delta > tau, tau chosen on the rule's own training
decisions at cost 0.1) against the fixed choices; paired 95% bootstrap; k3null placebo. The same table for 2 -> 3
(both directions).
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from k_confirm import alloc, within_ci  # noqa: E402
from k_dispatch import ROOT, Logit  # noqa: E402

FEATS = ("d", "e_deg", "d0", "speed", "yawrate", "prog_rate", "stall_s", "force_per", "frac_press", "n_free", "free_best")
COST, BUDGET, L2 = 0.1, 0.10, 10.0
TRANS = {"23": ("k2", "k3b", "k2null"), "34": ("k3", "k4", "k3null")}


def _f(x):
    return float(x) if x not in ("", None) else float("nan")


def load(dirs):
    rows = defaultdict(dict)
    for d in dirs:
        p = Path(d)
        p = (p if p.is_absolute() else ROOT / p) / "episodes.csv"
        for r in csv.DictReader(open(p)):
            rows[(r["object"], float(r["mass"]), r["scenario"], int(r["rep"]), str(d))][r["arm"]] = r
    out = {"23": [], "34": []}
    for k, tw in rows.items():
        for tr_, (s_, a_, n_) in TRANS.items():
            if not all(x in tw for x in (s_, a_, n_)) or int(tw[s_]["ended_t2"]):
                continue
            x = {f: _f(tw[s_][f"f2_{f}"]) for f in FEATS}
            rate = max(x["prog_rate"], 0.01)
            x["lrho"] = math.log(max((max(x["d"], 0.0) / rate) / 60.0, 1e-3))
            out[tr_].append({"key": k, "object": k[0], "mass": k[1], "x": x, "keep": float(tw[s_]["success"]),
                             "add": float(tw[a_]["success"]), "nul": float(tw[n_]["success"])})
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--train", nargs="+", required=True)
    ap.add_argument("--test", nargs="+", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    tr, te = load(a.train), load(a.test)
    objects = sorted({t["object"] for q in tr.values() for t in q})
    masses = sorted({t["mass"] for q in tr.values() for t in q})
    rng = np.random.default_rng(0)

    def X(ts):
        return np.nan_to_num(np.array([[t["x"][f] for f in FEATS + ("lrho",)] + [float(t["object"] == o) for o in objects]
                                       + [math.log(t["mass"])] + [float(t["mass"] == m) for m in masses] for t in ts]))

    def arr(ts, k):
        return np.array([t[k] for t in ts])

    fit = {}
    for q in ("23", "34"):
        Xq = X(tr[q])
        pa, pk = Logit(L2).fit(Xq, arr(tr[q], "add")), Logit(L2).fit(Xq, arr(tr[q], "keep"))
        dl = pa.predict(Xq) - pk.predict(Xq)
        k_, a_ = arr(tr[q], "keep"), arr(tr[q], "add")
        cand = np.r_[-np.inf, np.sort(dl), np.inf]
        pay = [((k_ + (dl > c) * (a_ - k_)) - COST * (dl > c)).mean() for c in cand]
        mu = {m: float(np.mean([t["add"] - t["keep"] for t in tr[q] if t["mass"] == m])) for m in masses}
        fit[q] = {"pa": pa, "pk": pk, "tau": float(cand[int(np.argmax(pay))]), "mu": mu}

    L = [f"# Transfer across team sizes ({', '.join(f'{q[0]} -> {q[1]}: {len(tr[q])} train / {len(te[q])} test' for q in tr)})",
         "", "Rules fitted on the training trees only and frozen; scored on the test trees' decisions. Paired 95% bootstrap "
         "over tasks; placebo = the same allocation scored with the null copy in place of the recruit.", ""]
    summ = {}
    for target, source, other in (("34", "23", "34"), ("23", "34", "23")):
        ts = te[target]
        if len(ts) < 20:
            continue
        Xt = X(ts)
        keep, add, nul = arr(ts, "keep"), arr(ts, "add"), arr(ts, "nul")
        u = add - keep
        n = len(ts)
        B = rng.integers(0, n, (4000, n))
        ms = arr(ts, "mass")

        def ci(v):
            bs = v[B].mean(1)
            return float(v.mean()), *np.percentile(bs, [2.5, 97.5]).tolist()

        def f(c, k=100):
            return f"{k * c[0]:+.1f} [{k * c[1]:+.1f}, {k * c[2]:+.1f}]"
        dl = {nm: fit[q]["pa"].predict(Xt) - fit[q]["pk"].predict(Xt) for nm, q in
              ((f"transferred ({source[0]} -> {source[1]})", source), (f"in-domain ({other[0]} -> {other[1]})", other))}
        mu = {f"mass ({q[0]} -> {q[1]})": np.array([fit[q]["mu"][m] for m in ms]) for q in (source, other)}
        tau = {f"transferred ({source[0]} -> {source[1]})": fit[source]["tau"], f"in-domain ({other[0]} -> {other[1]})": fit[other]["tau"]}
        T_, D_ = list(dl)
        L += [f"## Applied to {target[0]} -> {target[1]} ({n} test decisions; recruiting everywhere: {f(ci(u))} pp, "
              f"placebo {f(ci(nul - keep))})", ""]
        ent = {}
        # endpoint B, within mass
        L += ["Within a mass, uplift of the top half of delta minus the bottom half (pp):", "",
              "| rule | top - bottom | placebo |", "|---|---|---|"]
        for nm, v in dl.items():
            g, gp = within_ci(v, u, ms, masses, rng), within_ci(v, nul - keep, ms, masses, rng)
            ent[f"B {nm}"] = [g, gp]
            L.append(f"| {nm} | {f(g)} | {f(gp)} |")
        L.append("")
        # budget
        W = {**{nm: alloc(v, BUDGET) for nm, v in dl.items()},
             **{nm: alloc(v + 1e-3 * (dl[T_] - dl[T_].min()) / (np.ptp(dl[T_]) + 1e-12), BUDGET) for nm, v in mu.items()},
             "random": alloc(np.zeros(n), BUDGET)}
        calls = W["random"].sum()
        L += [f"At a {100 * BUDGET:.0f}% budget ({calls:.0f} calls): net deliveries per 100 calls, and vs the transferred rule:", "",
              "| rule | net per 100 calls | vs transferred [95% CI] | placebo vs transferred |", "|---|---|---|---|"]
        for nm, w_ in W.items():
            L.append(f"| {nm} | {100 * (w_ * u).sum() / calls:+.1f} | {f(ci((w_ - W[T_]) * u * n / calls))} | "
                     f"{f(ci((w_ - W[T_]) * (nul - keep) * n / calls))} |")
            ent[f"budget {nm}"] = float(100 * (w_ * u).sum() / calls)
        L.append("")
        # ask rule
        rules = {f"{nm}: delta > {tau[nm]:.3f}": (v > tau[nm]).astype(float) for nm, v in dl.items()}
        rules |= {f"{nm}: uplift > cost": (v > COST).astype(float) for nm, v in mu.items()}
        rules |= {"always stay": np.zeros(n), "always recruit": np.ones(n)}
        pay = {k: keep + w_ * u - COST * w_ for k, w_ in rules.items()}
        ref = list(rules)[0]
        best_fixed = max(("always stay", "always recruit"), key=lambda k: pay[k].mean())
        L += [f"Each team decides alone (cost {COST} per call):", "",
              f"| rule | call rate | success | payoff | vs transferred | vs best fixed ({best_fixed}) |", "|---|---|---|---|---|---|"]
        for k, w_ in rules.items():
            L.append(f"| {k} | {100 * w_.mean():.0f}% | {100 * (keep + w_ * u).mean():.1f}% | {pay[k].mean():.3f} | "
                     f"{f(ci(pay[k] - pay[ref]))} | {f(ci(pay[k] - pay[best_fixed]))} |")
            ent[f"ask {k}"] = float(pay[k].mean())
        L.append("")
        summ[target] = ent
    out = Path(a.out) if Path(a.out).is_absolute() else ROOT / a.out
    out.mkdir(parents=True, exist_ok=True)
    (out / "summary.md").write_text("\n".join(L) + "\n")
    (out / "summary.json").write_text(json.dumps(summ, indent=1, default=float))
    print("\n".join(L))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
