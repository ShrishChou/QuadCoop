"""When to add another robot, K -> K+1 (docs/k_dispatch.md). Learns dispatch policies on chain_branch.py trees and
scores them on held-out trees. CPU only.

    python scripts/k_dispatch.py --train logs/evals/kc-s1001 logs/evals/kc-s1002 logs/evals/kc-s1003 \
        --test logs/evals/kc-s7100 logs/evals/kc-s7900 --out logs/evals/k-dispatch

A policy makes two decisions per task: at t1 (one robot) add robot 2 or wait; at t2 (K = 1 or 2 robots, whichever
it is in) add the next robot or wait. The tree holds every outcome (leaves k1, k2b, k2a, k3), so any policy is
scored exactly. Payoff = success - lam x robots added (a robot sent to a task that has already ended is not sent).

Policies
  fixed      1 robot; 2 from t1; 2 from t2; 3 (2 from t1 + 1 at t2); oracle (best leaf per task, an upper bound)
  aware      the planner knows the weight
               table        per (decision, K, mass): add iff it pays on the training tasks (backward induction)
               hedge-mass   Hedge over threshold experts "add at t1 iff mass >= m1, at t2 iff mass >= m2(K)"
  blind      the planner does not know the weight; it sees how the object responds to the push
               est-mass     the weight estimated from the response (ridge on log mass), then the aware table
               fitted-Q     logistic T-learners per (decision, K) on the response features
               hedge-blind  Hedge (full feedback) over experts "add iff the time the object would still need at its
                            current progress rate exceeds tau x the time left" (one tau per decision and K)
               exp4-blind   the same experts, bandit feedback (only the outcome of the played branch)
               exp3-blind   Exp3 over the 4 open-loop plans per bin of that signal at t1 (bandit, no experts)
Online learners run over the training tasks in random orders (--orders), are frozen (largest mean weight) and scored on
the test tasks. Reported per lam: test success, robots added, payoff; paired differences vs the aware table
(bootstrap); training regret of the online learners vs the best expert in hindsight; per mass the policies' choices.
"""
from __future__ import annotations

import argparse
import csv
import itertools
import json
import math
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
LEAVES = ("k1", "k2b", "k2a", "k3")  # (a1, a2) = (0, 0), (0, 1), (1, 0), (1, 1)
BLIND = ("t", "d", "e_deg", "d0", "speed", "yawrate", "prog_rate", "force", "stall_s", "on1", "on2")
HORIZON = 80.0


def _f(x):
    return float(x) if x not in ("", None) else float("nan")


def load(dirs):
    rows = defaultdict(dict)
    for d in dirs:
        p = Path(d)
        p = (p if p.is_absolute() else ROOT / p) / "episodes.csv"
        for r in csv.DictReader(open(p)):
            rows[(r["object"], float(r["mass"]), r["scenario"], int(r["rep"]), str(d))][r["arm"]] = r
    tasks = []
    for k, tw in rows.items():
        if not all(x in tw for x in LEAVES):
            continue
        y = np.array([int(tw[x]["success"]) for x in LEAVES], dtype=float)
        adds = np.array([int(tw[x]["t_add2"] != "") + int(tw[x]["t_add3"] != "") for x in LEAVES], dtype=float)
        x1 = {f: _f(tw["k1"][f"f1_{f}"]) for f in BLIND}
        x2 = {1: {f: _f(tw["k1"][f"f2_{f}"]) for f in BLIND}, 2: {f: _f(tw["k2a"][f"f2_{f}"]) for f in BLIND}}
        tasks.append({"key": k, "object": k[0], "mass": k[1], "y": y, "adds": adds, "x1": x1, "x2": x2,
                      "end1": int(tw["k1"]["ended_t1"]), "end2": {1: int(tw["k1"]["ended_t2"]), 2: int(tw["k2a"]["ended_t2"])},
                      "null": {"k1": int(tw["k1null"]["success"]), "k2": int(tw["k2null"]["success"])}})
    return tasks


def leaf(a1, a2):
    return 2 * a1 + a2


def value(t, a1, a2, lam):
    j = leaf(a1, a2)
    return t["y"][j] - lam * t["adds"][j]


def play(tasks, pol1, pol2, lam):
    """pol1(t) -> 0/1, pol2(t, K) -> 0/1. Returns per-task leaf index, payoff, success, robots added."""
    L = np.array([leaf(a1 := int(pol1(t)), int(pol2(t, 1 + a1))) for t in tasks])
    y = np.array([t["y"][j] for t, j in zip(tasks, L)])
    ad = np.array([t["adds"][j] for t, j in zip(tasks, L)])
    return L, y - lam * ad, y, ad


def rho(x):
    """The 'struggle' signal: time the object would still need at its current progress rate / time left."""
    rate = max(x["prog_rate"], 0.01)
    return max((max(x["d"], 0.0) / rate) / max(HORIZON - x["t"], 1.0), 1e-3)


def bfeat(x, objects, obj):
    v = [x[f] for f in BLIND] + [x["d"] / max(x["d0"], 1e-3), math.log(rho(x)),
                                 x["force"] / (x["speed"] + 0.05), math.log(x["force"] + 1.0)]
    return np.array(v + [float(obj == o) for o in objects])


class Ridge:
    def __init__(self, l2=1.0):
        self.l2 = l2

    def fit(self, X, y):
        self.mu, self.sd = X.mean(0), X.std(0) + 1e-6
        Z = np.c_[np.ones(len(X)), (X - self.mu) / self.sd]
        R = self.l2 * np.eye(Z.shape[1])
        R[0, 0] = 0
        self.w = np.linalg.solve(Z.T @ Z + R, Z.T @ y)
        return self

    def predict(self, X):
        return np.c_[np.ones(len(X)), (X - self.mu) / self.sd] @ self.w


class Logit:
    def __init__(self, l2=1.0):
        self.l2 = l2

    def fit(self, X, y):
        self.mu, self.sd = X.mean(0), X.std(0) + 1e-6
        Z = np.c_[np.ones(len(X)), (X - self.mu) / self.sd]
        w = np.zeros(Z.shape[1])
        I = np.diag(np.r_[0.0, np.ones(len(w) - 1)])
        for _ in range(50):
            p = 1.0 / (1.0 + np.exp(-np.clip(Z @ w, -30, 30)))
            step = np.linalg.solve((Z * (p * (1 - p))[:, None]).T @ Z + self.l2 * I, Z.T @ (p - y) + self.l2 * I @ w)
            w -= step
            if np.abs(step).max() < 1e-6:
                break
        self.w = w
        return self

    def predict(self, X):
        Z = np.c_[np.ones(len(X)), (X - self.mu) / self.sd]
        return 1.0 / (1.0 + np.exp(-np.clip(Z @ self.w, -30, 30)))


# ---------------------------------------------------------------- weight-aware table (backward induction)
def fit_table(tr, lam, ctx=lambda t: t["mass"]):
    """pol2[(K, c)]: add at t2 iff the mean gain pays; pol1[c]: add at t1 iff the K=2 subtree (under pol2) pays."""
    g2 = defaultdict(list)
    for t in tr:
        c = ctx(t)
        for K in (1, 2):
            a = 2 * (K - 1)
            g2[(K, c)].append((t["y"][a + 1] - lam * t["adds"][a + 1]) - (t["y"][a] - lam * t["adds"][a]))
    p2 = {k: int(np.mean(v) > 1e-9) for k, v in g2.items()}
    g1 = defaultdict(list)
    for t in tr:
        c = ctx(t)
        g1[c].append(value(t, 1, p2[(2, c)], lam) - value(t, 0, p2[(1, c)], lam))
    p1 = {k: int(np.mean(v) > 1e-9) for k, v in g1.items()}
    return p1, p2


def nearest(m, ms):
    return min(ms, key=lambda x: abs(math.log(x) - math.log(m)))


# ---------------------------------------------------------------- online experts (Hedge / EXP4)
def hedge_exp4(tr, experts, lam, orders, seed):
    """experts: list of (pol1, pol2). Full feedback (hedge) and bandit (exp4) over the training tasks in random orders.
    Returns the frozen expert index per learner and the mean regret curves vs the best expert in hindsight."""
    rng = np.random.default_rng(seed)
    E, T = len(experts), len(tr)
    # every expert's leaf and payoff per task (the tree gives all of them)
    LE = np.zeros((E, T), dtype=int)
    PE = np.zeros((E, T))
    for e, (p1, p2) in enumerate(experts):
        LE[e], PE[e], _, _ = play(tr, p1, p2, lam)
    LV = np.array([[value(t, a1, a2, lam) for a1 in (0, 1) for a2 in (0, 1)] for t in tr])  # (T, 4)
    lo, hi = -2 * lam, 1.0  # payoff range, rescaled to [0, 1] for the updates
    eta = math.sqrt(8 * math.log(E) / T)
    gam = min(1.0, math.sqrt(E * math.log(E) / ((math.e - 1) * T)))
    W = {"hedge": [], "exp4": []}
    C = {"hedge": [], "exp4": []}
    for _ in range(orders):
        order = rng.permutation(T)
        wh, we = np.zeros(E), np.zeros(E)
        gh, ge = np.zeros(T), np.zeros(T)
        for s, i in enumerate(order):
            r01 = (PE[:, i] - lo) / (hi - lo)
            ph = np.exp(wh - wh.max())
            ph /= ph.sum()
            gh[s] = ph @ PE[:, i]
            wh += eta * r01
            # exp4: the experts' advice is a leaf (deterministic); mix, play a leaf, see only its payoff
            pe = np.exp(we - we.max())
            pe /= pe.sum()
            q = np.bincount(LE[:, i], weights=pe, minlength=4)
            q = (1 - gam) * q + gam / 4
            j = rng.choice(4, p=q / q.sum())
            ge[s] = LV[i, j]
            xhat = (LV[i, j] - lo) / (hi - lo) / q[j]
            we += gam / 4 * xhat * (LE[:, i] == j)
        best = np.cumsum(PE[:, order], 1).max(0)
        C["hedge"].append(best - np.cumsum(gh))
        C["exp4"].append(best - np.cumsum(ge))
        W["hedge"].append(wh)
        W["exp4"].append(we)
    frozen = {k: int(np.argmax(np.mean(v, 0))) for k, v in W.items()}
    return frozen, {k: np.mean(v, 0) for k, v in C.items()}, int(np.argmax(PE.sum(1)))


def exp3_plans(tr, ctx, lam, orders, seed):
    """Exp3 per context over the 4 open-loop plans (bandit). Returns the frozen plan per context and the regret curve
    vs the best fixed plan per context in hindsight."""
    rng = np.random.default_rng(seed)
    T = len(tr)
    LV = np.array([[value(t, a1, a2, lam) for a1 in (0, 1) for a2 in (0, 1)] for t in tr])
    cs = sorted({ctx(t) for t in tr})
    cnt = defaultdict(int)
    for t in tr:
        cnt[ctx(t)] += 1
    lo, hi = -2 * lam, 1.0
    Wc, C = defaultdict(list), []
    for _ in range(orders):
        order = rng.permutation(T)
        w = {c: np.zeros(4) for c in cs}
        got = np.zeros(T)
        for s, i in enumerate(order):
            c = ctx(tr[i])
            gm = min(1.0, math.sqrt(4 * math.log(4) / ((math.e - 1) * cnt[c])))
            p = np.exp(w[c] - w[c].max())
            p = (1 - gm) * p / p.sum() + gm / 4
            j = rng.choice(4, p=p)
            got[s] = LV[i, j]
            w[c][j] += gm / 4 * ((LV[i, j] - lo) / (hi - lo)) / p[j]
        tot = defaultdict(lambda: np.zeros(4))
        best = np.zeros(T)
        for s, i in enumerate(order):
            tot[ctx(tr[i])] += LV[i]
            best[s] = sum(v.max() for v in tot.values())
        C.append(best - np.cumsum(got))
        for c in cs:
            Wc[c].append(w[c])
    return {c: int(np.argmax(np.mean(v, 0))) for c, v in Wc.items()}, np.mean(C, 0)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--train", nargs="+", required=True)
    ap.add_argument("--test", nargs="+", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--lams", default="0,0.05,0.1,0.2")
    ap.add_argument("--orders", type=int, default=30)
    a = ap.parse_args()
    tr, te = load(a.train), load(a.test)
    assert tr and te, (len(tr), len(te))
    objects = sorted({t["object"] for t in tr + te})
    masses = sorted({t["mass"] for t in tr})
    out = Path(a.out) if Path(a.out).is_absolute() else ROOT / a.out
    out.mkdir(parents=True, exist_ok=True)
    brng = np.random.default_rng(0)

    # weight estimator from the response (blind): ridge on log mass, from the t1 state and from each t2 state
    X1 = np.array([bfeat(t["x1"], objects, t["object"]) for t in tr])
    X2 = {K: np.array([bfeat(t["x2"][K], objects, t["object"]) for t in tr]) for K in (1, 2)}
    lm = np.log([t["mass"] for t in tr])
    est1 = Ridge(3.0).fit(X1, lm)
    est2 = {K: Ridge(3.0).fit(X2[K], lm) for K in (1, 2)}
    for t in tr + te:
        t["m1"] = nearest(math.exp(est1.predict(bfeat(t["x1"], objects, t["object"])[None])[0]), masses)
        t["m2"] = {K: nearest(math.exp(est2[K].predict(bfeat(t["x2"][K], objects, t["object"])[None])[0]), masses)
                   for K in (1, 2)}
    acc = {"t1": np.mean([t["m1"] == t["mass"] for t in te]),
           "t2_K1": np.mean([t["m2"][1] == t["mass"] for t in te]), "t2_K2": np.mean([t["m2"][2] == t["mass"] for t in te])}

    L = [f"# When to add a robot: K -> K+1 dispatch ({len(tr)} training / {len(te)} test tasks)", "",
         "Two decisions per task (t1: add robot 2?; t2: add the next robot?), scored exactly on the branching tree. "
         "Payoff = success - lam x robots added. Differences vs the weight-aware table in pp (95% paired bootstrap).", "",
         f"Blind weight estimate on the test tasks (nearest of {', '.join(f'{m:g}' for m in masses)} kg): exact "
         f"{100 * acc['t1']:.0f}% from the t1 state, {100 * acc['t2_K1']:.0f}% / {100 * acc['t2_K2']:.0f}% from the t2 state "
         "with 1 / 2 robots.", ""]
    summ = {"train": len(tr), "test": len(te), "mass_estimate_exact": acc, "by_lam": {}}

    # tree outcomes on the test set
    L += ["## The tree on the test tasks (success %; nulls = a copy that keeps the same team: the noise floor)", "",
          "| mass | 1 robot | 2 from t2 | 2 from t1 | 3 | null 1 | null 2 |", "|---|---|---|---|---|---|---|"]
    for m in sorted({t["mass"] for t in te}) + ["all"]:
        s_ = [t for t in te if m == "all" or t["mass"] == m]
        Y = np.array([t["y"] for t in s_])
        L.append(f"| {m if m == 'all' else f'{m:g} kg'} | " + " | ".join(f"{100 * Y[:, j].mean():.0f}%" for j in (0, 1, 2, 3))
                 + f" | {100 * np.mean([t['null']['k1'] for t in s_]):.0f}% | {100 * np.mean([t['null']['k2'] for t in s_]):.0f}% |")
    L.append("")

    # experts: one threshold per (decision, K) on rho (blind) or on the mass (aware)
    taus = [0.0, 0.25, 0.5, 1.0, 2.0, 4.0, math.inf]
    blind_exp = [(lambda t, a_=a_: int(t["end1"] == 0 and rho(t["x1"]) > a_),
                  lambda t, K, b_=b_, c_=c_: int(t["end2"][K] == 0 and rho(t["x2"][K]) > (b_ if K == 1 else c_)))
                 for a_, b_, c_ in itertools.product(taus, taus, taus)]
    mth = [0.0] + masses + [math.inf]
    aware_exp = [(lambda t, a_=a_: int(t["end1"] == 0 and t["mass"] >= a_),
                  lambda t, K, b_=b_, c_=c_: int(t["end2"][K] == 0 and t["mass"] >= (b_ if K == 1 else c_)))
                 for a_, b_, c_ in itertools.product(mth, mth, mth)]
    rq = np.quantile([rho(t["x1"]) for t in tr], [0.25, 0.5, 0.75])
    rbin = lambda t: int(np.searchsorted(rq, rho(t["x1"])))  # noqa: E731
    PLANS = [(0, 0), (0, 1), (1, 0), (1, 1)]

    for lam in [float(x) for x in a.lams.split(",")]:
        pols = {}
        live1 = lambda t: t["end1"] == 0  # noqa: E731
        live2 = lambda t, K: t["end2"][K] == 0  # noqa: E731
        pols["1 robot"] = (lambda t: 0, lambda t, K: 0)
        pols["2 from t2"] = (lambda t: 0, lambda t, K: int(K == 1 and live2(t, K)))
        pols["2 from t1"] = (lambda t: int(live1(t)), lambda t, K: 0)
        pols["3 (2 at t1 + 1 at t2)"] = (lambda t: int(live1(t)), lambda t, K: int(live2(t, K)))
        p1, p2 = fit_table(tr, lam)
        pols["aware: table (K, mass)"] = (lambda t, p1=p1: int(live1(t) and p1.get(t["mass"], 0)),
                                          lambda t, K, p2=p2: int(live2(t, K) and p2.get((K, t["mass"]), 0)))
        p1o, p2o = fit_table(tr, lam, ctx=lambda t: (t["mass"], t["object"]))
        pols["aware: table (K, mass, object)"] = (
            lambda t, p1o=p1o: int(live1(t) and p1o.get((t["mass"], t["object"]), 0)),
            lambda t, K, p2o=p2o: int(live2(t, K) and p2o.get((K, (t["mass"], t["object"])), 0)))
        fa, ca, besta = hedge_exp4(tr, aware_exp, lam, a.orders, 1)
        pols["aware: hedge (mass thresholds)"] = aware_exp[fa["hedge"]]
        pols["aware: exp4 (mass thresholds)"] = aware_exp[fa["exp4"]]
        pe3, ce3a = exp3_plans(tr, lambda t: t["mass"], lam, a.orders, 2)
        pols["aware: exp3 per mass (plans)"] = (lambda t, pe3=pe3: int(live1(t) and PLANS[pe3.get(t["mass"], 0)][0]),
                                                lambda t, K, pe3=pe3: int(live2(t, K) and PLANS[pe3.get(t["mass"], 0)][1]))
        # blind
        pols["blind: estimated mass -> table"] = (lambda t, p1=p1: int(live1(t) and p1.get(t["m1"], 0)),
                                                  lambda t, K, p2=p2: int(live2(t, K) and p2.get((K, t["m2"][K]), 0)))
        # fitted Q: logistic T-learners at t2 per K, then ridge on the t1 values under the learned t2 policy
        q2 = {}
        for K in (1, 2):
            aidx = 2 * (K - 1)
            sel = [t for t in tr if t["end2"][K] == 0]
            X = np.array([bfeat(t["x2"][K], objects, t["object"]) for t in sel])
            q2[K] = (Logit(3.0).fit(X, np.array([t["y"][aidx] for t in sel])),
                     Logit(3.0).fit(X, np.array([t["y"][aidx + 1] for t in sel])))

        def pol2_q(t, K, q2=q2, lam=lam):
            if not live2(t, K):
                return 0
            x = bfeat(t["x2"][K], objects, t["object"])[None]
            return int(q2[K][1].predict(x)[0] - q2[K][0].predict(x)[0] > lam)
        sel = [t for t in tr if t["end1"] == 0]
        X = np.array([bfeat(t["x1"], objects, t["object"]) for t in sel])
        q1 = (Ridge(3.0).fit(X, np.array([value(t, 0, pol2_q(t, 1), lam) for t in sel])),
              Ridge(3.0).fit(X, np.array([value(t, 1, pol2_q(t, 2), lam) for t in sel])))
        pols["blind: fitted-Q (logistic)"] = (
            lambda t, q1=q1: int(live1(t) and q1[1].predict(bfeat(t["x1"], objects, t["object"])[None])[0]
                                 > q1[0].predict(bfeat(t["x1"], objects, t["object"])[None])[0]), pol2_q)
        fb, cb, bestb = hedge_exp4(tr, blind_exp, lam, a.orders, 3)
        pols["blind: hedge (struggle thresholds)"] = blind_exp[fb["hedge"]]
        pols["blind: exp4 (struggle thresholds)"] = blind_exp[fb["exp4"]]
        pb3, ce3b = exp3_plans(tr, rbin, lam, a.orders, 4)
        pols["blind: exp3 per struggle bin (plans)"] = (
            lambda t, pb3=pb3: int(live1(t) and PLANS[pb3.get(rbin(t), 0)][0]),
            lambda t, K, pb3=pb3: int(live2(t, K) and PLANS[pb3.get(rbin(t), 0)][1]))

        res = {k: play(te, *v, lam) for k, v in pols.items()}
        ref = res["aware: table (K, mass)"][1]
        orc = np.array([max(value(t, a1, a2, lam) for a1 in (0, 1) for a2 in (0, 1)) for t in te])
        L += [f"## lam = {lam:g} (a robot is worth {lam:g} of a success)", "",
              f"Hedge (full feedback) picked: aware {fmt_exp(fa['hedge'], mth)}, blind {fmt_exp(fb['hedge'], taus)}; "
              f"best in hindsight: aware {fmt_exp(besta, mth)}, blind {fmt_exp(bestb, taus)} "
              f"(thresholds at t1 / t2 with 1 robot / t2 with 2 robots).", "",
              "| policy | success | robots added | payoff | payoff vs aware table [95% CI] |", "|---|---|---|---|---|"]
        ent = {}
        for k, (Lf, pay, y, ad) in list(res.items()) + [("oracle (hindsight)", (None, orc, None, None))]:
            d = pay - ref
            bs = d[brng.integers(0, len(d), (4000, len(d)))].mean(1)
            lo_, hi_ = np.percentile(bs, [2.5, 97.5])
            ent[k] = {"payoff": float(pay.mean()), "diff": [float(d.mean()), float(lo_), float(hi_)]}
            if y is not None:
                ent[k].update(success=float(y.mean()), added=float(ad.mean()),
                              leaves={LEAVES[j]: float(np.mean(Lf == j)) for j in range(4)})
            L.append(f"| {k} | {'' if y is None else f'{100 * y.mean():.1f}%'} | {'' if ad is None else f'{ad.mean():.2f}'} | "
                     f"{pay.mean():.3f} | {100 * d.mean():+.1f} [{100 * lo_:+.1f}, {100 * hi_:+.1f}] |")
        L += ["", "Robots used per mass (mean team size at the end, test tasks):", "",
              "| policy | " + " | ".join(f"{m:g} kg" for m in masses) + " |", "|---|" + "---|" * len(masses)]
        for k in ("aware: table (K, mass)", "blind: estimated mass -> table", "blind: fitted-Q (logistic)",
                  "blind: hedge (struggle thresholds)", "blind: exp4 (struggle thresholds)"):
            Lf = res[k][0]
            L.append(f"| {k} | " + " | ".join(
                f"{np.mean([[1, 2, 2, 3][j] for t, j in zip(te, Lf) if t['mass'] == m]):.2f}" for m in masses) + " |")
        T = len(tr)
        L += ["", f"Training regret vs the best expert in hindsight ({a.orders} random orders, {T} tasks; payoff units):", "",
              "| learner | after 100 | after 500 | end | per task |", "|---|---|---|---|---|"]
        for nm, c in (("aware hedge", ca["hedge"]), ("aware exp4", ca["exp4"]), ("aware exp3 (vs best plan per mass)", ce3a),
                      ("blind hedge", cb["hedge"]), ("blind exp4", cb["exp4"]), ("blind exp3 (vs best plan per bin)", ce3b)):
            L.append(f"| {nm} | {c[min(99, T - 1)]:.1f} | {c[min(499, T - 1)]:.1f} | {c[-1]:.1f} | {c[-1] / T:.3f} |")
        L.append("")
        ent["regret_per_task"] = {"aware_hedge": float(ca["hedge"][-1] / T), "aware_exp4": float(ca["exp4"][-1] / T),
                                  "blind_hedge": float(cb["hedge"][-1] / T), "blind_exp4": float(cb["exp4"][-1] / T),
                                  "aware_exp3": float(ce3a[-1] / T), "blind_exp3": float(ce3b[-1] / T)}
        summ["by_lam"][f"{lam:g}"] = ent
        np.savez(out / f"regret_lam{lam:g}.npz", **{k: v for k, v in ca.items()}, **{f"blind_{k}": v for k, v in cb.items()},
                 aware_exp3=ce3a, blind_exp3=ce3b)
    (out / "summary.md").write_text("\n".join(L) + "\n")
    (out / "summary.json").write_text(json.dumps(summ, indent=1))
    print("\n".join(L))
    return 0


def fmt_exp(i, grid):
    n = len(grid)
    a_, b_, c_ = i // (n * n), (i // n) % n, i % n
    return "/".join(f"{grid[x]:g}" for x in (a_, b_, c_))


if __name__ == "__main__":
    raise SystemExit(main())
