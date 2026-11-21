"""When to add another robot, K -> K+1 (docs/k_dispatch.md). Learns dispatch policies on chain_branch.py trees and
scores them on held-out trees. CPU only.

    python scripts/k_dispatch.py --train logs/evals/kc-s1001 logs/evals/kc-s1002 logs/evals/kc-s1003 \
        --test logs/evals/kc-s7100 logs/evals/kc-s7900 --out logs/evals/k-dispatch

A policy makes two decisions per task: at t1 (one robot) add robot 2 or wait; at t2 (K = 1 or 2 robots, whichever
it is in) add the next robot or wait. The tree holds every outcome (leaves k1, k2b, k2a, k3), so any policy is
scored exactly. Payoff = success - lam x robots added (a robot sent to a task that has already ended is not sent).

Policies
  fixed       1 robot; 2 from t1; 2 from t2; 3 (2 from t1 + 1 at t2); oracle (best leaf per task, an upper bound)
  given mass  table per (decision, K, mass) by backward induction (also with the object); online learners over
              mass-threshold rules; fitted-Q with the mass as a feature
  no mass     the dispatcher sees how the object responds to the push (progress rate, speed, yaw rate, measured
              contact force, time since the last progress, distance / heading left) and the object's shape:
                est-mass   the mass estimated from the response, then the given-mass table
                fitted-Q   logistic T-learners per (decision, K), then ridge at t1 (also response only, without the
                           object; the same predictor with the mass added is the fair test of what the mass adds)
                online     over "struggle" rules: add iff rho = (distance left / progress rate) / time left > tau, one
                           tau per (decision, K):
                             hedge  full information (every rule's payoff, from the tree)
                             exp3   bandit over whole rules: one rule sampled per task and run on its own path
                             exp4   causal bandit with advice: t1 action from the t1 advice, only the t2 state of the
                                    branch taken revealed, t2 action from the advice on that state
Online learners run over the training tasks in random orders (--orders), are frozen (largest mean weight) and scored on
the test tasks by following their own path. Reported per lam: test success, robots added, payoff, paired differences
vs the given-mass table; the mass-feature effect; regret vs the best rule in hindsight; team size per mass; and the
cross-K transfer test (a struggle threshold fitted on 1 -> 2 decisions only, applied to 2 -> 3 at the same time t2).
The tree table gives every matched effect with the null of that comparison.
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
def online(tr, experts, lam, orders, seed):
    """Three online learners over the same policies (experts = (pol1, pol2) threshold rules), training tasks in random
    orders. Returns the frozen expert per learner (largest mean weight), the mean regret curves vs the best expert in
    hindsight, and that best expert.
      hedge   full information: every expert's payoff on the task is revealed (the tree has all four leaves)
      exp3    bandit over whole policies: sample one rule at the task's start, run it on its own path (each decision
              sees only the state that path reaches), see its terminal payoff, importance-weighted update
      exp4    bandit with expert advice, causal: the t1 action is drawn from the experts' t1 advice; only the t2 state
              of the branch taken is revealed and every expert advises on THAT state; the t2 action is drawn from that
              advice; an expert is credited only if its advice matches both actions (estimate / P(path))"""
    rng = np.random.default_rng(seed)
    E, T = len(experts), len(tr)
    A1 = np.array([[int(p1(t)) for t in tr] for p1, _ in experts])  # (E, T) advice at t1
    A2 = np.stack([np.array([[int(p2(t, K)) for t in tr] for _, p2 in experts]) for K in (1, 2)], -1)  # (E, T, 2)
    LE = 2 * A1 + A2[np.arange(E)[:, None], np.arange(T)[None], A1]  # each expert's own leaf
    LV = np.array([[value(t, a1, a2, lam) for a1 in (0, 1) for a2 in (0, 1)] for t in tr])  # (T, 4)
    PE = LV[np.arange(T)[None], LE]  # (E, T)
    lo, hi = -2 * lam, 1.0  # payoff range, rescaled to [0, 1] for the updates
    eta = math.sqrt(8 * math.log(E) / T)
    g3 = min(1.0, math.sqrt(E * math.log(E) / ((math.e - 1) * T)))
    g4 = min(1.0, math.sqrt(2 * math.log(E) / ((math.e - 1) * T)))  # 2 actions per decision
    W = {"hedge": [], "exp3": [], "exp4": []}
    C = {"hedge": [], "exp3": [], "exp4": []}
    for _ in range(orders):
        order = rng.permutation(T)
        w = {k: np.zeros(E) for k in W}
        got = {k: np.zeros(T) for k in W}
        for s, i in enumerate(order):
            # hedge
            ph = np.exp(w["hedge"] - w["hedge"].max())
            ph /= ph.sum()
            got["hedge"][s] = ph @ PE[:, i]
            w["hedge"] += eta * (PE[:, i] - lo) / (hi - lo)
            # exp3 over policies
            p3 = np.exp(w["exp3"] - w["exp3"].max())
            p3 = (1 - g3) * p3 / p3.sum() + g3 / E
            e = rng.choice(E, p=p3)
            r = PE[e, i]
            got["exp3"][s] = r
            w["exp3"][e] += g3 / E * ((r - lo) / (hi - lo)) / p3[e]
            # causal exp4
            p4 = np.exp(w["exp4"] - w["exp4"].max())
            p4 /= p4.sum()
            q1 = (1 - g4) * np.array([p4[A1[:, i] == x].sum() for x in (0, 1)]) + g4 / 2
            a1 = int(rng.random() < q1[1] / q1.sum())
            adv2 = A2[:, i, a1]  # every expert's advice on the revealed t2 state (team of 1 + a1 robots)
            q2 = (1 - g4) * np.array([p4[adv2 == x].sum() for x in (0, 1)]) + g4 / 2
            a2 = int(rng.random() < q2[1] / q2.sum())
            r = LV[i, 2 * a1 + a2]
            got["exp4"][s] = r
            match = (A1[:, i] == a1) & (adv2 == a2)
            w["exp4"] += g4 / 2 * match * ((r - lo) / (hi - lo)) / (q1[a1] / q1.sum() * q2[a2] / q2.sum())
        best = np.cumsum(PE[:, order], 1).max(0)
        for k in W:
            C[k].append(best - np.cumsum(got[k]))
            W[k].append(w[k])
    frozen = {k: int(np.argmax(np.mean(v, 0))) for k, v in W.items()}
    return frozen, {k: np.mean(v, 0) for k, v in C.items()}, int(np.argmax(PE.sum(1)))


def transfer(tr, te, lam, ci, fmt, ent):
    """Cross-K transfer at the same time (t2, 60 s left): a threshold on the struggle signal "add the next robot iff
    rho > tau", tau fitted on K = 1 -> 2 decisions only, frozen, applied to K = 2 -> 3 (and the reverse). Compared with
    tau fitted on the target K, tau fitted on both, and the fixed choices, on the held-out tasks still running at t2."""
    out = ["### Does one struggle threshold transfer across team sizes? (t2 decision, held-out tasks still running)", ""]

    def pay(t, K, add):
        j = 2 * (K - 1) + int(add)
        return t["y"][j] - lam * t["adds"][j], t["y"][j], t["adds"][j]

    def fit(K_list):
        cand = sorted({rho(t["x2"][K]) for K in K_list for t in tr if t["end2"][K] == 0})
        grid = [0.0] + [0.5 * (x + y) for x, y in zip(cand[:-1], cand[1:])][:: max(1, len(cand) // 200)] + [math.inf]
        best, bt = -1e9, math.inf
        for tau in grid:
            v = np.mean([pay(t, K, rho(t["x2"][K]) > tau)[0] for K in K_list for t in tr if t["end2"][K] == 0])
            if v > best + 1e-12:
                best, bt = v, tau
        return bt
    tau = {"K1": fit([1]), "K2": fit([2]), "both": fit([1, 2])}
    ent["transfer_tau"] = tau
    for K in (2, 1):
        sel = [t for t in te if t["end2"][K] == 0]
        rules = {f"tau from 1 -> 2 only ({tau['K1']:.2f})": lambda t: rho(t["x2"][K]) > tau["K1"],
                 f"tau from 2 -> 3 only ({tau['K2']:.2f})": lambda t: rho(t["x2"][K]) > tau["K2"],
                 f"tau from both ({tau['both']:.2f})": lambda t: rho(t["x2"][K]) > tau["both"],
                 f"always keep {K}": lambda t: False, f"always add robot {K + 1}": lambda t: True}
        R = {k: np.array([pay(t, K, f(t)) for t in sel]) for k, f in rules.items()}
        own = list(R)[1] if K == 2 else list(R)[0]
        fixed = max(list(R)[3:], key=lambda k: R[k][:, 0].mean())
        null = ci(np.array([t["null"]["k2" if K == 2 else "k1"] for t in sel]) - np.array([t["y"][2 * (K - 1)] for t in sel]))
        out += [f"Applied to {K} -> {K + 1} ({len(sel)} tasks). Null for this comparison (a copy keeping the same {K}-robot team): "
                f"{fmt(null)} pp of success.", "",
                f"| rule | success | robots sent | payoff | vs the rule fitted on {K} -> {K + 1} | vs the best fixed ({fixed}) |",
                "|---|---|---|---|---|---|"]
        for k, v in R.items():
            out.append(f"| {k} | {100 * v[:, 1].mean():.1f}% | {v[:, 2].mean():.2f} | {v[:, 0].mean():.3f} | "
                       f"{fmt(ci(v[:, 0] - R[own][:, 0]))} | {fmt(ci(v[:, 0] - R[fixed][:, 0]))} |")
        ent[f"transfer_to_K{K}"] = {k: {"payoff": float(v[:, 0].mean()), "success": float(v[:, 1].mean()),
                                        "sent": float(v[:, 2].mean())} for k, v in R.items()}
        out.append("")
    return out


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

    def ci(d):
        d = np.asarray(d, dtype=float)
        bs = d[brng.integers(0, len(d), (4000, len(d)))].mean(1)
        return 100 * d.mean(), 100 * np.percentile(bs, 2.5), 100 * np.percentile(bs, 97.5)
    fmt = lambda c: f"{c[0]:+.1f} [{c[1]:+.1f}, {c[2]:+.1f}]"  # noqa: E731

    # the tree on the test set: each matched effect next to its own null (the same comparison with no change)
    L += ["## The tree on the test tasks", "",
          "Success %, then each matched effect with the null for that comparison (pp, 95% paired bootstrap). "
          "Robot 2's effects are against k1null - k1 (a copy of the solo robot at t1, so the null spans the same or a "
          "longer stretch of rollout); robot 3's effect is against k2null - k2a (a copy of the pair at t2). Every leaf is "
          "one rollout.", "",
          "| mass | 1 robot | 2 from t2 | 2 from t1 | 3 | robot 2 at t1 (k2a-k1) | robot 2 at t2 (k2b-k1) | null k1 | "
          "robot 3 at t2 (k3-k2a) | null k2 |", "|---|---|---|---|---|---|---|---|---|---|"]
    tree = {}
    for m in sorted({t["mass"] for t in te}) + ["all"]:
        s_ = [t for t in te if m == "all" or t["mass"] == m]
        Y = np.array([t["y"] for t in s_])
        n1 = np.array([t["null"]["k1"] for t in s_]) - Y[:, 0]
        n2 = np.array([t["null"]["k2"] for t in s_]) - Y[:, 2]
        eff = {"k2a-k1": ci(Y[:, 2] - Y[:, 0]), "k2b-k1": ci(Y[:, 1] - Y[:, 0]), "null_k1": ci(n1),
               "k3-k2a": ci(Y[:, 3] - Y[:, 2]), "null_k2": ci(n2)}
        tree[str(m)] = {"success": {LEAVES[j]: float(100 * Y[:, j].mean()) for j in range(4)},
                        **{k: list(v) for k, v in eff.items()}}
        L.append(f"| {m if m == 'all' else f'{m:g} kg'} | " + " | ".join(f"{100 * Y[:, j].mean():.0f}%" for j in (0, 1, 2, 3))
                 + " | " + " | ".join(fmt(v) for v in eff.values()) + " |")
    L.append("")
    summ["tree"] = tree

    # experts: one threshold per (decision, K) on rho (blind) or on the mass (aware)
    taus = [0.0, 0.25, 0.5, 1.0, 2.0, 4.0, math.inf]
    blind_exp = [(lambda t, a_=a_: int(t["end1"] == 0 and rho(t["x1"]) > a_),
                  lambda t, K, b_=b_, c_=c_: int(t["end2"][K] == 0 and rho(t["x2"][K]) > (b_ if K == 1 else c_)))
                 for a_, b_, c_ in itertools.product(taus, taus, taus)]
    mth = [0.0] + masses + [math.inf]
    aware_exp = [(lambda t, a_=a_: int(t["end1"] == 0 and t["mass"] >= a_),
                  lambda t, K, b_=b_, c_=c_: int(t["end2"][K] == 0 and t["mass"] >= (b_ if K == 1 else c_)))
                 for a_, b_, c_ in itertools.product(mth, mth, mth)]
    live1 = lambda t: t["end1"] == 0  # noqa: E731
    live2 = lambda t, K: t["end2"][K] == 0  # noqa: E731
    onehot = lambda t: [float(t["object"] == o) for o in objects]  # noqa: E731
    resp = lambda x: list(bfeat(x, [], ""))  # noqa: E731  the response features alone
    FEATS = {"response + object": lambda x, t: resp(x) + onehot(t),
             "response + object + mass": lambda x, t: resp(x) + onehot(t) + [math.log(t["mass"])],
             "response only": lambda x, t: resp(x),
             "mass + object only": lambda x, t: [math.log(t["mass"])] + onehot(t)}

    def fit_q(ff, lam):
        """Fitted Q: logistic T-learners (success with / without the next robot) at t2 per K, then ridge on the t1
        values under the learned t2 policy. ff(x, t) -> features of state x of task t."""
        q2 = {}
        for K in (1, 2):
            aidx = 2 * (K - 1)
            sel = [t for t in tr if live2(t, K)]
            X = np.array([ff(t["x2"][K], t) for t in sel])
            q2[K] = (Logit(3.0).fit(X, np.array([t["y"][aidx] for t in sel])),
                     Logit(3.0).fit(X, np.array([t["y"][aidx + 1] for t in sel])))

        def pol2(t, K):
            if not live2(t, K):
                return 0
            x = np.array(ff(t["x2"][K], t))[None]
            return int(q2[K][1].predict(x)[0] - q2[K][0].predict(x)[0] > lam)
        sel = [t for t in tr if live1(t)]
        X = np.array([ff(t["x1"], t) for t in sel])
        q1 = (Ridge(3.0).fit(X, np.array([value(t, 0, pol2(t, 1), lam) for t in sel])),
              Ridge(3.0).fit(X, np.array([value(t, 1, pol2(t, 2), lam) for t in sel])))

        def pol1(t):
            x = np.array(ff(t["x1"], t))[None]
            return int(live1(t) and q1[1].predict(x)[0] > q1[0].predict(x)[0])
        return pol1, pol2

    for lam in [float(x) for x in a.lams.split(",")]:
        pols = {}
        pols["1 robot"] = (lambda t: 0, lambda t, K: 0)
        pols["2 from t2"] = (lambda t: 0, lambda t, K: int(K == 1 and live2(t, K)))
        pols["2 from t1"] = (lambda t: int(live1(t)), lambda t, K: 0)
        pols["3 (2 at t1 + 1 at t2)"] = (lambda t: int(live1(t)), lambda t, K: int(live2(t, K)))
        p1, p2 = fit_table(tr, lam)
        pols["given mass: table (K, mass)"] = (lambda t, p1=p1: int(live1(t) and p1.get(t["mass"], 0)),
                                               lambda t, K, p2=p2: int(live2(t, K) and p2.get((K, t["mass"]), 0)))
        p1o, p2o = fit_table(tr, lam, ctx=lambda t: (t["mass"], t["object"]))
        pols["given mass: table (K, mass, object)"] = (
            lambda t, p1o=p1o: int(live1(t) and p1o.get((t["mass"], t["object"]), 0)),
            lambda t, K, p2o=p2o: int(live2(t, K) and p2o.get((K, (t["mass"], t["object"])), 0)))
        fa, ca, besta = online(tr, aware_exp, lam, a.orders, 1)
        for k_ in ("hedge", "exp3", "exp4"):
            pols[f"given mass: {k_} (mass thresholds)"] = aware_exp[fa[k_]]
        pols["no mass: estimated mass -> table"] = (lambda t, p1=p1: int(live1(t) and p1.get(t["m1"], 0)),
                                                    lambda t, K, p2=p2: int(live2(t, K) and p2.get((K, t["m2"][K]), 0)))
        for nm, ff in FEATS.items():
            pols[f"{'given mass' if 'mass' in nm else 'no mass'}: fitted-Q ({nm})"] = fit_q(ff, lam)
        fb, cb, bestb = online(tr, blind_exp, lam, a.orders, 3)
        for k_ in ("hedge", "exp3", "exp4"):
            pols[f"no mass: {k_} (struggle thresholds)"] = blind_exp[fb[k_]]

        res = {k: play(te, *v, lam) for k, v in pols.items()}
        REF = "given mass: table (K, mass)"
        ref = res[REF][1]
        orc = np.array([max(value(t, a1, a2, lam) for a1 in (0, 1) for a2 in (0, 1)) for t in te])
        L += [f"## lam = {lam:g} (a robot is worth {lam:g} of a success)", "",
              f"Frozen threshold rules (t1 / t2 with 1 robot / t2 with 2 robots): given mass: hedge "
              f"{fmt_exp(fa['hedge'], mth)}, exp3 {fmt_exp(fa['exp3'], mth)}, exp4 {fmt_exp(fa['exp4'], mth)}, best "
              f"{fmt_exp(besta, mth)} kg; no mass: hedge {fmt_exp(fb['hedge'], taus)}, exp3 {fmt_exp(fb['exp3'], taus)}, "
              f"exp4 {fmt_exp(fb['exp4'], taus)}, best {fmt_exp(bestb, taus)} (tau on the struggle signal).", "",
              "| policy | success | robots added | payoff | payoff vs the given-mass table [95% CI] |", "|---|---|---|---|---|"]
        ent = {}
        for k, (Lf, pay, y, ad) in list(res.items()) + [("oracle (hindsight)", (None, orc, None, None))]:
            c = ci(pay - ref)
            ent[k] = {"payoff": float(pay.mean()), "diff": list(c)}
            if y is not None:
                ent[k].update(success=float(y.mean()), added=float(ad.mean()),
                              leaves={LEAVES[j]: float(np.mean(Lf == j)) for j in range(4)})
            L.append(f"| {k} | {'' if y is None else f'{100 * y.mean():.1f}%'} | {'' if ad is None else f'{ad.mean():.2f}'} | "
                     f"{pay.mean():.3f} | {fmt(c)} |")
        # the fair test of what the mass itself adds: the same fitted-Q with and without it
        dm = ci(res["given mass: fitted-Q (response + object + mass)"][1] - res["no mass: fitted-Q (response + object)"][1])
        ent["mass_feature_effect"] = list(dm)
        L += ["", f"What the mass adds to the same predictor (fitted-Q, response + object, with vs without log mass): "
                  f"{fmt(dm)} pp of payoff.", "",
              "Mean team size at the end per mass (test tasks):", "",
              "| policy | " + " | ".join(f"{m:g} kg" for m in masses) + " |", "|---|" + "---|" * len(masses)]
        for k in (REF, "no mass: estimated mass -> table", "no mass: fitted-Q (response + object)",
                  "no mass: hedge (struggle thresholds)", "no mass: exp3 (struggle thresholds)",
                  "no mass: exp4 (struggle thresholds)"):
            Lf = res[k][0]
            L.append(f"| {k} | " + " | ".join(
                f"{np.mean([[1, 2, 2, 3][j] for t, j in zip(te, Lf) if t['mass'] == m]):.2f}" for m in masses) + " |")
        T = len(tr)
        L += ["", f"Training regret vs the best threshold rule in hindsight ({a.orders} random orders, {T} tasks; payoff "
                  "units). Hedge sees every rule's payoff; exp3 and exp4 see only the path they took (exp4 sees the t2 state "
                  "of the branch it took, never the other).", "",
              "| learner | after 100 | after 500 | end | per task |", "|---|---|---|---|---|"]
        for nm, c in [(f"given mass {k_}", ca[k_]) for k_ in ("hedge", "exp3", "exp4")] + \
                     [(f"no mass {k_}", cb[k_]) for k_ in ("hedge", "exp3", "exp4")]:
            L.append(f"| {nm} | {c[min(99, T - 1)]:.1f} | {c[min(499, T - 1)]:.1f} | {c[-1]:.1f} | {c[-1] / T:.3f} |")
        L.append("")
        ent["regret_per_task"] = {**{f"given_mass_{k_}": float(ca[k_][-1] / T) for k_ in ca},
                                  **{f"no_mass_{k_}": float(cb[k_][-1] / T) for k_ in cb}}
        L += transfer(tr, te, lam, ci, fmt, ent)
        summ["by_lam"][f"{lam:g}"] = ent
        np.savez(out / f"regret_lam{lam:g}.npz", **{f"given_mass_{k}": v for k, v in ca.items()},
                 **{f"no_mass_{k}": v for k, v in cb.items()})
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
