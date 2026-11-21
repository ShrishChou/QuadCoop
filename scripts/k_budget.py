"""When should a working pair call robot 3? A budget-matched test on the K -> K+1 trees (docs/k_dispatch.md). CPU only.

    python scripts/k_budget.py --train logs/evals/kc-s1001 logs/evals/kc-s1002 logs/evals/kc-s1003 \
        --test logs/evals/kc-s7100 logs/evals/kc-s7900 --out logs/evals/k-budget

The decision: at t2 = 20 s, a pair (robot 2 added at t1, leaf k2a) is still pushing. Keep the pair (k2a) or send robot
3 (k3)? Both outcomes are observed on every task (the branches), so any allocation of helpers is scored exactly.

The question is not whether helpers pay on average (they do at 80 kg) but whether watching this push tells the
planner which tasks a helper will rescue. So every ranker gets the same budget: a fraction B of the decisions receive
a helper, chosen in the ranker's order (ties broken at random, scored as the expectation). Rankers, fitted on --train:

  random                 expected value of a random B-fraction
  mass                   the training uplift (k3 - k2a success) of the task's mass
  mass + object          the training uplift of (mass, object), shrunk toward the mass's
  response               predicted uplift from the observed push only (no mass): two logistic success models,
                         with and without robot 3, on the t2 response features + object (T-learner; the primary)
  response + mass        the same with the mass as a feature: does watching the push add to knowing the mass?
  mass, then response    the mass rule's order across masses, the response + mass order within a mass (the direct
                         test: at a budget that splits a mass, does the push pick better than a random tie-break?)
  response (ridge)       ridge regression on the uplift itself (a robustness check)
  hindsight              the actual uplift (upper bound)

Reported on --test: success per budget and paired differences vs the mass rule (95% bootstrap over tasks); a
placebo null for each difference (the same allocations scored with the k2null copy in place of robot 3, so the true
difference is 0; for hindsight it is not 0, because hindsight selects on the noisy outcome itself); and within each mass, the actual uplift among the top half vs the bottom half of the response
ranking.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from k_dispatch import ROOT, Logit, Ridge, bfeat, load  # noqa: E402

BUDGETS = (0.1, 0.2, 0.3, 0.5, 0.7)


def decisions(tasks):
    """Tasks where the pair is still running at t2, with keep / add / null outcomes."""
    out = [t for t in tasks if t["end2"][2] == 0]
    for t in out:
        t["keep"], t["add"], t["nul"] = t["y"][2], t["y"][3], float(t["null"]["k2"])
        t["u"] = t["add"] - t["keep"]
    return out


def alloc(score, frac, rng=None):
    """Weights in [0, 1] giving a helper to the top frac of tasks by score; tied tasks at the boundary share the rest
    equally (the expectation of a random tie-break)."""
    n = len(score)
    left = frac * n
    w = np.zeros(n)
    for s in sorted(set(score.tolist()), reverse=True):
        idx = np.flatnonzero(score == s)
        take = min(left, len(idx))
        w[idx] = take / len(idx)
        left -= take
        if left <= 1e-9:
            break
    return w


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--train", nargs="+", required=True)
    ap.add_argument("--test", nargs="+", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--l2", type=float, default=10.0)
    a = ap.parse_args()
    tr, te = decisions(load(a.train)), decisions(load(a.test))
    objects = sorted({t["object"] for t in tr + te})
    masses = sorted({t["mass"] for t in tr})
    out = Path(a.out) if Path(a.out).is_absolute() else ROOT / a.out
    out.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(0)

    def X(ts, mass):
        rows = []
        for t in ts:
            v = bfeat(t["x2"][2], objects, t["object"])
            if mass:
                v = np.r_[v, math.log(t["mass"]), [float(t["mass"] == m) for m in masses]]
            rows.append(v)
        return np.nan_to_num(np.array(rows))

    def arr(ts, k):
        return np.array([t[k] for t in ts])

    # ---- rankers fitted on training decisions
    mu = {m: arr([t for t in tr if t["mass"] == m], "u").mean() for m in masses}
    mo = {}
    for m in masses:
        for o in objects:
            s = [t["u"] for t in tr if t["mass"] == m and t["object"] == o]
            mo[(m, o)] = (sum(s) + 5 * mu[m]) / (len(s) + 5)
    score = {"mass": np.array([mu[t["mass"]] for t in te]),
             "mass + object": np.array([mo[(t["mass"], t["object"])] for t in te])}
    for name, mass in (("response", False), ("response + mass", True)):
        Xtr, Xte = X(tr, mass), X(te, mass)
        pa = Logit(a.l2).fit(Xtr, arr(tr, "add")).predict(Xte)
        pk = Logit(a.l2).fit(Xtr, arr(tr, "keep")).predict(Xte)
        score[name] = pa - pk
    r = score["response + mass"]
    score["mass, then response"] = score["mass"] + 1e-3 * (r - r.min()) / (r.max() - r.min() + 1e-12)
    score["response (ridge)"] = Ridge(a.l2).fit(X(tr, False), arr(tr, "u")).predict(X(te, False))
    score["random"] = np.zeros(len(te))
    score["hindsight"] = arr(te, "u") + 1e-6 * rng.random(len(te))
    order = ("random", "mass", "mass + object", "response", "response + mass", "mass, then response", "response (ridge)",
             "hindsight")

    keep, add, nul = arr(te, "keep"), arr(te, "add"), arr(te, "nul")
    n = len(te)
    B = rng.integers(0, n, (4000, n))

    def ci(d):
        bs = d[B].mean(1)
        lo, hi = np.percentile(bs, [2.5, 97.5])
        return 100 * d.mean(), 100 * lo, 100 * hi

    def fmt(c):
        return f"{c[0]:+.1f} [{c[1]:+.1f}, {c[2]:+.1f}]"

    L = [f"# When should a working pair call robot 3? ({len(tr)} training / {n} test decisions at t2)", "",
         "Every ranker sends helpers to the same fraction of the test decisions, in its own order. Success % per "
         "budget; differences vs the mass rule in pp of success over all decisions (95% paired bootstrap over tasks). "
         "Placebo: the same allocations scored with the k2null copy of the pair in place of robot 3 (true value 0).", "",
         f"Keeping the pair everywhere: {100 * keep.mean():.1f}%; robot 3 everywhere: {100 * add.mean():.1f}% "
         f"(uplift {fmt(ci(add - keep))}); placebo everywhere {fmt(ci(nul - keep))}.", ""]
    summ = {"train": len(tr), "test": n, "keep": float(keep.mean()), "add_all": float(add.mean()), "budgets": {}}
    for f in BUDGETS:
        W = {k: alloc(score[k], f) for k in order}
        succ = {k: keep + W[k] * (add - keep) for k in order}
        plac = {k: keep + W[k] * (nul - keep) for k in order}
        L += [f"## Budget: a helper for {100 * f:.0f}% of decisions ({f * n:.0f} helpers)", "",
              "| ranker | success | extra objects at the goal vs keeping the pair | vs mass [95% CI] | placebo vs mass |",
              "|---|---|---|---|---|"]
        ent = {}
        for k in order:
            d, dp = succ[k] - succ["mass"], plac[k] - plac["mass"]
            extra = (succ[k] - keep).sum()
            L.append(f"| {k} | {100 * succ[k].mean():.1f}% | {extra:+.1f} of {n} | {fmt(ci(d))} | {fmt(ci(dp))} |")
            ent[k] = {"success": float(succ[k].mean()), "extra": float(extra), "vs_mass": ci(d), "placebo": ci(dp)}
        summ["budgets"][f"{f:g}"] = ent
        L.append("")

    # ---- within a mass: does the response ranking pick the rescuable pushes?
    L += ["## Within each mass: actual uplift of robot 3 among the response ranking's top half vs bottom half", "",
          "Ranking by 'response + mass' (within a mass the mass term is constant, so the order comes from the push). "
          "Placebo: the same split scored with the k2null copy.", "",
          "| mass | decisions | uplift, top half | uplift, bottom half | top - bottom [95% CI] | placebo top - bottom |",
          "|---|---|---|---|---|---|"]
    summ["within"] = {}
    pooled = []
    for m in masses:
        idx = np.flatnonzero(np.array([t["mass"] for t in te]) == m)
        if len(idx) < 10:
            continue
        s = score["response + mass"][idx]
        top = s >= np.median(s)
        u, up = (add - keep)[idx], (nul - keep)[idx]
        bi = rng.integers(0, len(idx), (4000, len(idx)))

        def gap(v):
            g = [v[b][top[b]].mean() - v[b][~top[b]].mean() for b in bi if top[b].any() and (~top[b]).any()]
            return 100 * (v[top].mean() - v[~top].mean()), *np.percentile(100 * np.array(g), [2.5, 97.5])
        g, gp = gap(u), gap(up)
        L.append(f"| {m:g} kg | {len(idx)} | {100 * u[top].mean():+.1f} | {100 * u[~top].mean():+.1f} | {fmt(g)} | {fmt(gp)} |")
        pooled.append((idx, top))
        summ["within"][f"{m:g}"] = {"top": float(u[top].mean()), "bottom": float(u[~top].mean()), "gap": g, "placebo": gp}
    # pooled: the mean over masses of (top - bottom), bootstrapped by resampling within each mass
    def pool(v):
        g0 = np.mean([v[i][t].mean() - v[i][~t].mean() for i, t in pooled])
        bs = []
        for _ in range(2000):
            gs = []
            for i, t in pooled:
                b = rng.integers(0, len(i), len(i))
                if t[b].any() and (~t[b]).any():
                    gs.append(v[i][b][t[b]].mean() - v[i][b][~t[b]].mean())
            bs.append(np.mean(gs))
        return 100 * g0, *np.percentile(100 * np.array(bs), [2.5, 97.5])
    gp_, gpp = pool(add - keep), pool(nul - keep)
    L.append(f"| all masses (mean of the gaps) | {n} | | | {fmt(gp_)} | {fmt(gpp)} |")
    summ["within_pooled"] = {"gap": gp_, "placebo": gpp}
    L.append("")
    np.savez(out / "scores.npz", keys=np.array([str(t["key"]) for t in te]), keep=keep, add=add, nul=nul,
             **{k.replace(" ", "_").replace("+", "p").replace("(", "").replace(")", "").replace(",", ""): v for k, v in score.items()})
    (out / "summary.md").write_text("\n".join(L) + "\n")
    (out / "summary.json").write_text(json.dumps(summ, indent=1, default=float))
    print("\n".join(L))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
