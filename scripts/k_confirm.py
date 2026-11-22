"""Frozen confirmation of selective recruitment at 2 -> 3 (docs/k_dispatch.md, "Confirmation protocol"). CPU only.

    # 1. freeze (development data only): fit on --train, choose the baseline and the ask threshold on --val
    python scripts/k_confirm.py freeze --train logs/evals/kc-s1001 logs/evals/kc-s1002 logs/evals/kc-s1003 \
        --val logs/evals/kc-s7100 logs/evals/kc-s7900 --frozen frozen/k_confirm_2to3.json
    # 2. evaluate the frozen file on untouched seeds (nothing is refitted)
    python scripts/k_confirm.py evaluate --frozen frozen/k_confirm_2to3.json --test logs/evals/kc-s81xx ... \
        --out logs/evals/k-confirm

The decision: at t2 = 20 s, a pair (k2a) still pushing either stays (k2a) or recruits robot 3 (k3). Both branches
keep the planner's normal replanning; the recruit branch pays the helper's staging and travel. Inputs: the t2
response features (no mass) plus, declared, the object's mass and identity.

Dispatcher: two logistic models, P(delivery | h, stay) and P(delivery | h, recruit), fitted on both branches;
delta(h) is their difference. Two uses:
  budget   10% of eligible decisions get a helper. Primary ranker: "mass, then delta" (the training uplift of the
           task's mass orders masses; delta orders tasks within a mass). Fixed before the fresh seeds, after the
           development seeds 7100 / 7900 had informed it.
  ask      each team independently recruits iff delta(h) > tau; tau maximizes success - COST x calls on --val.
Baselines at the same budget: random; mass; mass + object; most likely to fail alone (lowest P(stay)); plus the
endpoints always stay / always recruit. The strongest baseline at 10% on --val is frozen as THE comparison.

Primary metric: net extra deliveries per 100 helper calls at the 10% budget, primary ranker minus the frozen
baseline (95% paired bootstrap over tasks; every task's branches stay together). Also: total success over all
starts and over eligible decisions, rescues, disruptions, calls, helper-seconds, the k2null placebo, the deployable
"one helper for ten teams" version, the ask rule, the budget curve, delta-group rescue - disruption (pooled and
within mass) and the object x mass counts.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from k_dispatch import ROOT, Logit, bfeat, load  # noqa: E402

BUDGET = 0.10
BUDGETS = (0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0)
COST = 0.1
L2 = 10.0
BASELINES = ("random", "mass", "mass + object", "most likely to fail")
PRIMARY = "mass, then delta"


def _p(d):
    p = Path(d)
    return p if p.is_absolute() else ROOT / p


def tasks_of(dirs):
    """All starts (for whole-benchmark success) with the eligible flag (pair still running at t2)."""
    ts = load(dirs)
    for t in ts:
        t["elig"] = t["end2"][2] == 0
        t["keep"], t["add"], t["nul"] = t["y"][2], t["y"][3], float(t["null"]["k2"])
    return ts


def helper_seconds(dirs):
    """Deployed time of robot 3 in each k3 leaf: robot_s = L + (L - t_add2) + (L - t_add3)."""
    import csv
    out = {}
    for d in dirs:
        for r in csv.DictReader(open(_p(d) / "episodes.csv")):
            if r["arm"] == "k3" and r["t_add3"] != "":
                t2, t3 = float(r["t_add2"]), float(r["t_add3"])
                L = (float(r["robot_s"]) + t2 + t3) / 3
                out[(r["object"], float(r["mass"]), r["scenario"], int(r["rep"]), str(d))] = max(L - t3, 0.0)
    return out


class Model:
    """The frozen dispatcher: feature map + two logistic models + the mass / mass-object uplift tables."""

    def __init__(self, spec):
        self.s = spec

    def X(self, ts):
        s = self.s
        rows = []
        for t in ts:
            v = bfeat(t["x2"][2], s["objects"], t["object"])
            v = np.r_[v, math.log(t["mass"]), [float(t["mass"] == m) for m in s["masses"]]]
            rows.append(v)
        return np.nan_to_num(np.array(rows))

    @staticmethod
    def _lp(m, X):
        Z = np.c_[np.ones(len(X)), (X - np.array(m["mu"])) / np.array(m["sd"])]
        return 1.0 / (1.0 + np.exp(-np.clip(Z @ np.array(m["w"]), -30, 30)))

    def scores(self, ts, rng):
        s = self.s
        X = self.X(ts)
        pa, pk = self._lp(s["recruit"], X), self._lp(s["stay"], X)
        delta = pa - pk
        mu = np.array([s["mass_uplift"][f"{t['mass']:g}"] for t in ts])
        mo = np.array([s["mass_object_uplift"].get(f"{t['mass']:g}|{t['object']}", s["mass_uplift"][f"{t['mass']:g}"])
                       for t in ts])
        span = delta.max() - delta.min() + 1e-12
        return {"random": np.zeros(len(ts)), "mass": mu, "mass + object": mo, "most likely to fail": 1.0 - pk,
                "delta": delta, PRIMARY: mu + 1e-3 * (delta - delta.min()) / span}, delta, pk


def alloc(score, frac):
    """Helper weights for the top frac of tasks; boundary ties share the remainder (expected random tie-break)."""
    n = len(score)
    left = frac * n
    w = np.zeros(n)
    for v in sorted(set(score.tolist()), reverse=True):
        idx = np.flatnonzero(score == v)
        take = min(left, len(idx))
        w[idx] = take / len(idx)
        left -= take
        if left <= 1e-9:
            break
    return w


def per10(score, rng, reps=200):
    """One helper per ten eligible teams: random groups of ten, the top-scored team in each gets it (ties shared)."""
    n = len(score)
    W = np.zeros(n)
    for _ in range(reps):
        perm = rng.permutation(n)
        for g in range(0, n - n % 10, 10):
            idx = perm[g:g + 10]
            top = idx[score[idx] == score[idx].max()]
            W[top] += 1.0 / len(top)
    return W / reps


def within_gap(delta, u, masses, levels):
    """Endpoint B: mean over masses of [uplift among the top half of delta within the mass - the bottom half]."""
    gs = []
    for m in levels:
        idx = np.flatnonzero(masses == m)
        if len(idx) < 10:
            continue
        top = delta[idx] >= np.median(delta[idx])
        if top.all() or not top.any():
            continue
        gs.append(u[idx][top].mean() - u[idx][~top].mean())
    return float(np.mean(gs))


def within_ci(delta, u, masses, levels, rng, reps=2000):
    """Bootstrap within each mass (tasks resampled inside their mass; the split is recomputed on the resample)."""
    groups = [np.flatnonzero(masses == m) for m in levels]
    bs = []
    for _ in range(reps):
        idx = np.concatenate([g[rng.integers(0, len(g), len(g))] for g in groups if len(g)])
        bs.append(within_gap(delta[idx], u[idx], masses[idx], levels))
    return within_gap(delta, u, masses, levels), *np.percentile(bs, [2.5, 97.5]).tolist()


def freeze(a):
    tr, va = [t for t in tasks_of(a.train) if t["elig"]], [t for t in tasks_of(a.val) if t["elig"]]
    objects = sorted({t["object"] for t in tr + va})
    masses = sorted({t["mass"] for t in tr})
    spec = {"objects": objects, "masses": masses, "l2": L2, "budget": BUDGET, "cost": COST, "primary": PRIMARY,
            "train": list(a.train), "val": list(a.val)}
    m = Model(spec)
    Xtr = m.X(tr)
    for k, y in (("recruit", "add"), ("stay", "keep")):
        f = Logit(L2).fit(Xtr, np.array([t[y] for t in tr]))
        spec[k] = {"mu": f.mu.tolist(), "sd": f.sd.tolist(), "w": f.w.tolist()}
    u = {mm: np.mean([t["add"] - t["keep"] for t in tr if t["mass"] == mm]) for mm in masses}
    spec["mass_uplift"] = {f"{mm:g}": float(v) for mm, v in u.items()}
    mo = {}
    for mm in masses:
        for o in objects:
            s_ = [t["add"] - t["keep"] for t in tr if t["mass"] == mm and t["object"] == o]
            mo[f"{mm:g}|{o}"] = float((sum(s_) + 5 * u[mm]) / (len(s_) + 5))
    spec["mass_object_uplift"] = mo
    rng = np.random.default_rng(0)
    S, delta, _ = m.scores(va, rng)
    keep, add = np.array([t["keep"] for t in va]), np.array([t["add"] for t in va])
    val = {k: float((keep + alloc(S[k], BUDGET) * (add - keep)).mean()) for k in BASELINES + ("delta", PRIMARY)}
    spec["val_success_at_budget"] = val
    spec["baseline"] = max(BASELINES, key=lambda k: val[k])
    # the independent ask threshold, on validation
    cand = np.r_[-np.inf, np.sort(delta), np.inf]
    pay = [((keep + (delta > c) * (add - keep)) - COST * (delta > c)).mean() for c in cand]
    spec["tau"] = float(cand[int(np.argmax(pay))])
    spec["val_ask"] = {"payoff": float(max(pay)), "call_rate": float((delta > spec["tau"]).mean())}
    # seeds: power for the primary difference at 2/3 of its development effect (shrunk for selection)
    d = (alloc(S[PRIMARY], BUDGET) - alloc(S[spec["baseline"]], BUDGET)) * (add - keep)
    eff, sd = d.mean(), d.std(ddof=1)
    per_seed = len(va) / len(a.val)
    need = (2.80 * sd / max(2 / 3 * eff, 1e-6)) ** 2 if eff > 0 else float("inf")
    spec["power"] = {"dev_effect_pp": 100 * eff, "sd_pp": 100 * sd, "eligible_per_seed": per_seed,
                     "decisions_needed_80pct_at_2/3_effect": need,
                     "seeds_needed": int(math.ceil(need / per_seed)) if math.isfinite(need) else None}
    # endpoint B (the powered test that delta learned something about this push): within-mass top - bottom half
    ms = np.array([t["mass"] for t in va])
    gB = within_ci(delta, add - keep, ms, masses, rng)
    seB = (gB[2] - gB[1]) / (2 * 1.96)
    needB = len(va) * (2.80 * seB / (2 / 3 * gB[0])) ** 2 if gB[0] > 0 else float("inf")
    spec["power_B"] = {"dev_gap_pp": 100 * gB[0], "dev_ci_pp": [100 * gB[1], 100 * gB[2]],
                       "decisions_needed_80pct_at_2/3_effect": needB,
                       "seeds_needed": int(math.ceil(needB / per_seed)) if math.isfinite(needB) else None}
    # endpoint C: each team decides alone (delta > tau) vs the mass rule (mass uplift > cost), payoff at COST
    mt = np.array([spec["mass_uplift"][f"{t['mass']:g}"] > COST for t in va], dtype=float)
    askv = (delta > spec["tau"]).astype(float)
    dC = (keep + askv * (add - keep) - COST * askv) - (keep + mt * (add - keep) - COST * mt)
    bsC = dC[rng.integers(0, len(dC), (4000, len(dC)))].mean(1)
    seC = bsC.std()
    needC = len(va) * (2.80 * seC / (2 / 3 * dC.mean())) ** 2 if dC.mean() > 0 else float("inf")
    spec["power_C"] = {"dev_diff_pp": 100 * dC.mean(), "note": "tau chosen on these same tasks (in-sample)",
                       "decisions_needed_80pct_at_2/3_effect": needC,
                       "seeds_needed": int(math.ceil(needC / per_seed)) if math.isfinite(needC) else None}
    spec["endpoints"] = {
        "A": "net extra deliveries per 100 calls at the 10% budget, primary ranker minus the frozen baseline "
             "(protocol primary; reported regardless; underpowered at the development effect, see power)",
        "B": "mean over masses of robot 3's uplift among the top half of delta minus the bottom half, within the "
             "mass (does the dispatcher learn which pushes a helper rescues beyond the mass); two-sided 95% CI "
             "excluding 0 = confirmed; the k2null placebo of the same statistic is reported",
        "C": "each team alone: payoff (success - cost x calls) of 'recruit iff delta > tau' minus the mass rule "
             "'recruit iff the mass's training uplift > cost', cost 0.1; 95% CI excluding 0 = confirmed"}
    out = _p(a.frozen)
    out.parent.mkdir(parents=True, exist_ok=True)
    txt = json.dumps(spec, indent=1)
    out.write_text(txt)
    print(json.dumps({k: spec[k] for k in ("baseline", "tau", "val_ask", "val_success_at_budget", "power", "power_B", "power_C")}, indent=1))
    print("sha256", hashlib.sha256(txt.encode()).hexdigest())
    return 0


def evaluate(a):
    spec = json.loads(_p(a.frozen).read_text())
    m = Model(spec)
    allt = tasks_of(a.test)
    te = [t for t in allt if t["elig"]]
    hs = helper_seconds(a.test)
    rng = np.random.default_rng(1)
    S, delta, pk = m.scores(te, rng)
    keep, add, nul = (np.array([t[k] for t in te]) for k in ("keep", "add", "nul"))
    hsec = np.array([hs.get(t["key"], 0.0) for t in te])
    n, nall = len(te), len(allt)
    fixed_all = sum(t["keep"] for t in allt if not t["elig"])
    B = rng.integers(0, n, (4000, n))
    base = spec["baseline"]

    def ci(v):
        bs = v[B].mean(1)
        return float(v.mean()), *np.percentile(bs, [2.5, 97.5]).tolist()

    def f(c, k=100):
        return f"{k * c[0]:+.1f} [{k * c[1]:+.1f}, {k * c[2]:+.1f}]"

    def stats(W, out_add=add):
        u = out_add - keep
        return {"success_elig": float((keep + W * u).mean()), "success_all": float(((keep + W * u).sum() + fixed_all) / nall),
                "calls": float(W.sum()), "rescues": float((W * (u > 0)).sum()), "disruptions": float((W * (u < 0)).sum()),
                "net": float((W * u).sum()), "helper_s": float((W * hsec).sum())}

    sha = hashlib.sha256(_p(a.frozen).read_text().encode()).hexdigest()
    L = [f"# Frozen 2 -> 3 confirmation ({n} eligible decisions of {nall} starts)", "",
         f"Frozen file `{a.frozen}` (sha256 {sha[:12]}), fitted on {', '.join(spec['train'])}; baseline and threshold "
         f"chosen on {', '.join(spec['val'])}. Test: {', '.join(a.test)}. Nothing below was refitted.", "",
         f"Primary: net extra deliveries per 100 helper calls at a {100 * spec['budget']:.0f}% budget, "
         f"'{PRIMARY}' minus the frozen baseline '{base}' (95% paired bootstrap over tasks).", ""]
    W = {k: alloc(S[k], spec["budget"]) for k in S}
    calls = W[PRIMARY].sum()
    dP = (W[PRIMARY] - W[base]) * (add - keep) * n / calls
    dN = (W[PRIMARY] - W[base]) * (nul - keep) * n / calls
    prim, plac = ci(dP), ci(dN)
    masses_ = np.array([t["mass"] for t in te])
    gB = within_ci(delta, add - keep, masses_, spec["masses"], rng)
    gBp = within_ci(delta, nul - keep, masses_, spec["masses"], rng)
    L += [f"**Endpoint A: {f(prim)} net deliveries per 100 calls** (placebo, the k2null copy in place of robot 3: "
          f"{f(plac)}).", "",
          f"**Endpoint B: within a mass, robot 3's uplift in the top half of delta minus the bottom half: {f(gB)} pp** "
          f"(placebo {f(gBp)}).", ""]
    mt_ = np.array([spec["mass_uplift"][f"{t['mass']:g}"] > spec["cost"] for t in te], dtype=float)
    ask_ = (delta > spec["tau"]).astype(float)
    gC = ci((keep + ask_ * (add - keep) - spec["cost"] * ask_) - (keep + mt_ * (add - keep) - spec["cost"] * mt_))
    L += [f"**Endpoint C: each team alone, ask rule minus mass rule: {f(gC)} pp of payoff** "
          f"(call rates {100 * ask_.mean():.0f}% vs {100 * mt_.mean():.0f}%).", ""]
    summ = {"frozen_sha256": sha, "eligible": n, "starts": nall, "baseline": base, "primary": prim, "placebo": plac, "B": gB, "B_placebo": gBp, "C": gC}
    L += [f"## At the {100 * spec['budget']:.0f}% budget ({calls:.0f} calls)", "",
          "| policy | success, all starts | success, eligible | calls | rescues | disruptions | net per 100 calls | "
          "helper-s | vs baseline, net per 100 calls |", "|---|---|---|---|---|---|---|---|---|"]
    rows = dict(W)
    rows["always stay"], rows["always recruit"] = np.zeros(n), np.ones(n)
    summ["budget"] = {}
    for k in ("always stay", "random", "mass", "mass + object", "most likely to fail", "delta", PRIMARY, "always recruit"):
        st = stats(rows[k])
        vs = ci((rows[k] - W[base]) * (add - keep) * n / calls) if k not in ("always stay", "always recruit") else None
        per = 100 * st["net"] / max(st["calls"], 1e-9) if st["calls"] else 0.0
        L.append(f"| {k}{' (frozen baseline)' if k == base else ''} | {100 * st['success_all']:.1f}% | "
                 f"{100 * st['success_elig']:.1f}% | {st['calls']:.0f} | {st['rescues']:.0f} | {st['disruptions']:.0f} | "
                 f"{per:+.1f} | {st['helper_s']:.0f} | {f(vs) if vs else ''} |")
        summ["budget"][k] = {**st, "vs_baseline": vs}
    L.append("")
    # deployable: one helper per ten teams
    W10 = {k: per10(S[k], rng) for k in (base, PRIMARY, "random")}
    c10 = W10[PRIMARY].sum()
    d10 = ci((W10[PRIMARY] - W10[base]) * (add - keep) * n / c10)
    L += ["## One helper for ten teams (random groups of ten eligible teams; the top-ranked team gets it)", "",
          f"Net per 100 calls: {PRIMARY} {100 * (W10[PRIMARY] * (add - keep)).sum() / c10:+.1f}, {base} "
          f"{100 * (W10[base] * (add - keep)).sum() / c10:+.1f}, random {100 * (W10['random'] * (add - keep)).sum() / c10:+.1f}; "
          f"{PRIMARY} - {base}: {f(d10)}.", ""]
    summ["per10"] = d10
    # independent ask rule
    ask = (delta > spec["tau"]).astype(float)
    mt = np.array([spec["mass_uplift"][f"{t['mass']:g}"] > spec["cost"] for t in te], dtype=float)
    L += [f"## Each team decides alone: recruit iff delta > {spec['tau']:.3f} (frozen; cost {spec['cost']} per call)", "",
          "| rule | call rate | success, eligible | rescues | disruptions | net per 100 calls | payoff | vs ask rule (payoff, pp) |",
          "|---|---|---|---|---|---|---|---|"]
    pay = {}
    for k, Wk in (("ask rule (delta > tau)", ask), ("mass rule (mass uplift > cost)", mt), ("always stay", np.zeros(n)),
                  ("always recruit", np.ones(n))):
        pay[k] = keep + Wk * (add - keep) - spec["cost"] * Wk
    for k, Wk in (("ask rule (delta > tau)", ask), ("mass rule (mass uplift > cost)", mt), ("always stay", np.zeros(n)),
                  ("always recruit", np.ones(n))):
        st = stats(Wk)
        per = 100 * st["net"] / st["calls"] if st["calls"] else 0.0
        L.append(f"| {k} | {100 * Wk.mean():.1f}% | {100 * st['success_elig']:.1f}% | {st['rescues']:.0f} | "
                 f"{st['disruptions']:.0f} | {per:+.1f} | {pay[k].mean():.3f} | {f(ci(pay[k] - pay['ask rule (delta > tau)']))} |")
    L.append("")
    summ["ask"] = {k: float(v.mean()) for k, v in pay.items()} | {"call_rate": float(ask.mean())}
    # budget curve
    L += ["## Net deliveries vs budget (figure panel 1)", "", "| budget | " + " | ".join(
        ("random", "mass", "mass + object", "most likely to fail", "delta", PRIMARY)) + " |", "|---" * 7 + "|"]
    curve = {}
    for b in BUDGETS:
        vals = {k: float((alloc(S[k], b) * (add - keep)).sum()) for k in ("random", "mass", "mass + object",
                                                                         "most likely to fail", "delta", PRIMARY)}
        curve[f"{b:g}"] = vals
        L.append(f"| {100 * b:.0f}% | " + " | ".join(f"{v:+.1f}" for v in vals.values()) + " |")
    summ["curve"] = curve
    L.append("")
    # delta groups (figure panel 2), pooled and within mass
    u = add - keep
    L += ["## Measured rescue - disruption rate by predicted helper value (figure panel 2)", "",
          "Quintiles of delta, pooled and within each mass (within a mass the order comes from the push). "
          "Rate = (rescues - disruptions) / decisions, in pp; placebo in brackets.", "",
          "| group | Q1 (lowest delta) | Q2 | Q3 | Q4 | Q5 (highest) | Q5 - Q1 [95% CI] |", "|---|---|---|---|---|---|---|"]
    masses = np.array([t["mass"] for t in te])
    summ["groups"] = {}
    for g in ["all"] + spec["masses"]:
        idx = np.arange(n) if g == "all" else np.flatnonzero(masses == g)
        if len(idx) < 25:
            continue
        q = np.searchsorted(np.quantile(delta[idx], [0.2, 0.4, 0.6, 0.8]), delta[idx], side="right")
        cells = [(100 * u[idx][q == j].mean(), 100 * (nul - keep)[idx][q == j].mean()) for j in range(5)]
        bi = rng.integers(0, len(idx), (2000, len(idx)))
        gap = [u[idx][b][q[b] == 4].mean() - u[idx][b][q[b] == 0].mean() for b in bi if (q[b] == 4).any() and (q[b] == 0).any()]
        g0 = 100 * (u[idx][q == 4].mean() - u[idx][q == 0].mean())
        lo, hi = np.percentile(100 * np.array(gap), [2.5, 97.5])
        L.append(f"| {g if g == 'all' else f'{g:g} kg'} | " + " | ".join(f"{c:+.1f} ({p:+.1f})" for c, p in cells)
                 + f" | {g0:+.1f} [{lo:+.1f}, {hi:+.1f}] |")
        summ["groups"][str(g)] = {"cells": cells, "q5_q1": [g0, lo, hi]}
    L.append("")
    # object x mass counts
    objs = spec["objects"]
    L += ["## Object x mass: eligible decisions / rescues / disruptions if every pair recruits / primary's calls", "",
          "| object | " + " | ".join(f"{mm:g} kg" for mm in spec["masses"]) + " |", "|---" * (len(spec["masses"]) + 1) + "|"]
    cells = {}
    for o in objs:
        r = []
        for mm in spec["masses"]:
            idx = [i for i, t in enumerate(te) if t["object"] == o and t["mass"] == mm]
            c = (len(idx), int((u[idx] > 0).sum()), int((u[idx] < 0).sum()), float(W[PRIMARY][idx].sum()))
            cells[f"{o}|{mm:g}"] = c
            r.append(f"{c[0]} / {c[1]} / {c[2]} / {c[3]:.0f}")
        L.append(f"| {o} | " + " | ".join(r) + " |")
    summ["cells"] = cells
    L.append("")
    out = _p(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "summary.md").write_text("\n".join(L) + "\n")
    (out / "summary.json").write_text(json.dumps(summ, indent=1, default=float))
    np.savez(out / "decisions.npz", keys=np.array([str(t["key"]) for t in te]), keep=keep, add=add, nul=nul,
             delta=delta, p_stay=pk, mass_kg=masses, helper_s=hsec, **{"rank_" + k.replace(" ", "_").replace(",", ""): v for k, v in S.items()})
    print("\n".join(L))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("freeze")
    f.add_argument("--train", nargs="+", required=True)
    f.add_argument("--val", nargs="+", required=True)
    f.add_argument("--frozen", required=True)
    e = sub.add_parser("evaluate")
    e.add_argument("--frozen", required=True)
    e.add_argument("--test", nargs="+", required=True)
    e.add_argument("--out", required=True)
    a = ap.parse_args()
    return freeze(a) if a.cmd == "freeze" else evaluate(a)


if __name__ == "__main__":
    raise SystemExit(main())
