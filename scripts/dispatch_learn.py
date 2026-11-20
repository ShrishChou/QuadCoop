"""When to add a robot: learn dispatch rules from the late-help branches (scripts/branch_help.py), compare them,
and replay them online with regret minimization (docs/late_help.md). CPU only (numpy).

    python scripts/dispatch_learn.py --train logs/evals/lh-p8-s1001 logs/evals/lh-p8-s1002 ... \
        --test logs/evals/lh-p8 --out logs/evals/dispatch-1to2
    # transfer: rules learned on 1 -> 2, tested on 2 -> 3 decisions
    python scripts/dispatch_learn.py --train <1->2 dirs> --test <2->3 dirs> --out logs/evals/dispatch-2to3

Decision per branched task (both outcomes are known from the twin envs): add a robot or not. Payoff =
success - lam x helper time (fraction of the horizon the added robot spends, from the branch to success or the
deadline). Inputs do not depend on the team size: team size before help, mass, shape (one-hot), distance and
heading left after the probe, the probe's progress on both (fraction of the start), contact time share, object speed
and yaw rate, time left.

Rules compared on the test tasks (lam swept; each rule tuned on --train only):
  never / always            never add / always add
  object-mass               add if, on the training tasks of that object and mass, adding paid more
  stall                     add if the probe's progress (distance + heading, fraction of the start) is below a
                            threshold tuned on train
  predictor                 two logistic models P(success | add), P(success | no add) on the inputs; add if
                            the predicted gain > lam x expected helper time
  oracle                    the better branch per task (upper bound)
Online (regret minimization, test tasks in random order, --shuffles orders): the rules above are the experts.
  hedge   full information: every expert's payoff on each task is seen (the branches give it)
  exp4    bandit: only the payoff of the action taken is seen; importance-weighted expert updates
  exp3    bandit over the two actions with no inputs at all
Reported: mean payoff, success and helper time, and regret vs the best fixed expert in hindsight, over time.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def load(dirs: list[str]) -> list[dict]:
    rows = []
    for d in dirs:
        p = Path(d)
        p = p if p.suffix == ".csv" else p / "branches.csv"
        if not p.is_absolute():
            p = ROOT / p
        rows += list(csv.DictReader(open(p)))
    out = []
    for r in rows:
        if int(r["ended_in_probe"]):
            continue
        num = lambda k: float(r[k]) if r.get(k, "") not in ("", None) else float("nan")  # noqa: E731
        out.append({"object": r["object"], "mass": float(r["mass"]), "scenario": r["scenario"],
                    "team": int(r.get("team_from", 1)), "probe": num("probe_s"),
                    "y0": int(r["success_solo"]), "y1": int(r["success_help"]),
                    "t1": num("t_help"), "d0": num("d0"), "e0": num("e0_deg"), "dp": num("d_probe"),
                    "ep": num("e_probe_deg"), "touch": num("touch_probe"), "speed": num("speed_probe"),
                    "yaw": num("yawrate_probe")})
    return out


def helper_time(r: dict, horizon: float) -> float:
    end = r["t1"] if r["y1"] and not math.isnan(r["t1"]) else horizon
    return max(end - r["probe"], 0.0) / horizon


def features(rows: list[dict], objects: list[str], horizon: float) -> np.ndarray:
    X = []
    for r in rows:
        prog_d = 1.0 - r["dp"] / max(r["d0"], 1e-3)
        prog_e = 1.0 - r["ep"] / max(r["e0"], 1.0) if r["e0"] > 1.0 else 0.0
        X.append([r["team"], r["mass"] / 80.0, r["dp"] / 3.0, r["ep"] / 90.0, prog_d, prog_e, r["touch"], r["speed"],
                  r["yaw"], (horizon - r["probe"]) / horizon] + [float(r["object"] == o) for o in objects])
    return np.array(X, dtype=float)


class Logit:
    def __init__(self, l2: float = 1.0):
        self.l2 = l2

    def fit(self, X: np.ndarray, y: np.ndarray):
        self.mu, self.sd = X.mean(0), X.std(0) + 1e-6
        Z = np.c_[np.ones(len(X)), (X - self.mu) / self.sd]
        w = np.zeros(Z.shape[1])
        for _ in range(50):  # Newton / IRLS
            p = 1.0 / (1.0 + np.exp(-Z @ w))
            g = Z.T @ (p - y) + self.l2 * np.r_[0.0, w[1:]]
            Hm = (Z * (p * (1 - p))[:, None]).T @ Z + self.l2 * np.diag(np.r_[0.0, np.ones(len(w) - 1)])
            step = np.linalg.solve(Hm, g)
            w -= step
            if np.abs(step).max() < 1e-6:
                break
        self.w = w
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        Z = np.c_[np.ones(len(X)), (X - self.mu) / self.sd]
        return 1.0 / (1.0 + np.exp(-Z @ self.w))


def payoff(rows, act, lam, horizon):
    """Per-task payoff of actions act (0/1)."""
    return np.array([(r["y1"] - lam * helper_time(r, horizon)) if a_ else r["y0"] for r, a_ in zip(rows, act)])


def rules(train, test, objects, lam, horizon) -> dict[str, np.ndarray]:
    """Each rule's actions on the test tasks, tuned on train."""
    Xtr, Xte = features(train, objects, horizon), features(test, objects, horizon)
    out = {"never": np.zeros(len(test), int), "always": np.ones(len(test), int)}
    # object-mass table
    gain = {}
    for r in train:
        k = (r["object"], r["mass"])
        gain.setdefault(k, []).append((r["y1"] - lam * helper_time(r, horizon)) - r["y0"])
    out["object-mass"] = np.array([int(np.mean(gain.get((r["object"], r["mass"]), [0.0])) > 0) for r in test])
    # stall threshold
    prog = lambda X: X[:, 4] + X[:, 5]  # noqa: E731
    best, thr = -1e9, 0.0
    for c in np.linspace(-0.5, 1.5, 41):
        v = payoff(train, (prog(Xtr) < c).astype(int), lam, horizon).mean()
        if v > best:
            best, thr = v, c
    out["stall"] = (prog(Xte) < thr).astype(int)
    # predictor (T-learner)
    y0 = np.array([r["y0"] for r in train])
    y1 = np.array([r["y1"] for r in train])
    m0, m1 = Logit().fit(Xtr, y0), Logit().fit(Xtr, y1)
    ht = np.array([helper_time(r, horizon) for r in train])
    mean_ht = float(ht.mean())
    gain_te = m1.predict(Xte) - m0.predict(Xte)
    out["predictor"] = (gain_te > lam * mean_ht).astype(int)
    out["oracle"] = np.array([int((r["y1"] - lam * helper_time(r, horizon)) > r["y0"]) for r in test])
    return out


def online(test, experts: dict[str, np.ndarray], lam, horizon, shuffles: int, seed: int = 0) -> dict:
    """Hedge (full info), EXP4 (bandit, experts' advice), Exp3 (bandit over 2 actions). Regret vs the best fixed
    expert on that order, per round."""
    names = [k for k in experts if k != "oracle"]
    T = len(test)
    P = np.stack([payoff(test, experts[k], lam, horizon) for k in names], 1)  # (T, E) expert payoffs (in [-1, 1])
    A = np.stack([experts[k] for k in names], 1)  # (T, E) advice
    pay = {a_: np.array([payoff(test, np.full(T, a_), lam, horizon)]).squeeze(0) for a_ in (0, 1)}
    rng = np.random.default_rng(seed)
    E = len(names)
    eta_h = math.sqrt(8 * math.log(E) / T)
    gamma = min(1.0, math.sqrt(E * math.log(E) / ((math.e - 1) * T)))
    curves = {"hedge": [], "exp4": [], "exp3": []}
    finals = {"hedge": [], "exp4": [], "exp3": [], "best_expert": []}
    for _ in range(shuffles):
        order = rng.permutation(T)
        wh = np.zeros(E)
        w4 = np.zeros(E)
        w3 = np.zeros(2)
        got = {k: np.zeros(T) for k in curves}
        for t, i in enumerate(order):
            # hedge: play the weighted expert mixture's expected payoff (full info update)
            ph = np.exp(wh - wh.max())
            ph /= ph.sum()
            got["hedge"][t] = ph @ P[i]
            wh += eta_h * (P[i] + 1.0) / 2.0
            # exp4: sample an action from the experts' advice mixture; only that action's payoff is seen
            q = np.exp(w4 - w4.max())
            q /= q.sum()
            p1 = (1 - gamma) * (q @ A[i]) + gamma / 2
            a_ = int(rng.random() < p1)
            r_ = pay[a_][i]
            got["exp4"][t] = r_
            pa = p1 if a_ else 1 - p1
            xhat = (r_ + 1.0) / 2.0 / pa  # importance-weighted reward of the action taken, in [0, 1] / p
            w4 += gamma / 2 * (A[i] == a_) * xhat
            # exp3 over the two actions, no context
            p3 = np.exp(w3 - w3.max())
            p3 = (1 - gamma) * p3 / p3.sum() + gamma / 2
            b = int(rng.random() < p3[1])
            r3 = pay[b][i]
            got["exp3"][t] = r3
            w3[b] += gamma / 2 * ((r3 + 1.0) / 2.0) / p3[b]
        best = P[order].sum(0).max()
        cbest = np.cumsum(P[order], 0).max(1)
        for k in curves:
            curves[k].append(cbest - np.cumsum(got[k]))
            finals[k].append(got[k].mean())
        finals["best_expert"].append(best / T)
    res = {"experts": names, "T": T}
    for k in curves:
        c = np.mean(curves[k], 0)
        res[k] = {"mean_payoff": float(np.mean(finals[k])),
                  "regret_final": float(c[-1]), "regret_per_task_final": float(c[-1] / T),
                  "regret_at": {str(n): float(c[min(n, T) - 1]) for n in (25, 50, 100, 200, 400, 800) if n <= T}}
    res["best_expert_mean_payoff"] = float(np.mean(finals["best_expert"]))
    return res


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--train", nargs="+", required=True)
    ap.add_argument("--test", nargs="+", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--horizon", type=float, default=80.0)
    ap.add_argument("--lams", default="0,0.1,0.25,0.5,1.0")
    ap.add_argument("--shuffles", type=int, default=50)
    a = ap.parse_args()
    train, test = load(a.train), load(a.test)
    objects = sorted({r["object"] for r in train + test})
    out = Path(a.out) if Path(a.out).is_absolute() else ROOT / a.out
    out.mkdir(parents=True, exist_ok=True)
    lams = [float(x) for x in a.lams.split(",")]
    summ = {"train_tasks": len(train), "test_tasks": len(test), "by_lam": {}}
    L = [f"# Dispatch: when to add a robot ({len(train)} training / {len(test)} test branched tasks)", "",
         f"Test team sizes {sorted({r['team'] for r in test})} -> +1; training {sorted({r['team'] for r in train})} -> +1.",
         "Payoff = success - lam x helper time (fraction of the 80 s horizon). Success / helper time over the branched "
         "test tasks.", ""]
    for lam in lams:
        acts = rules(train, test, objects, lam, a.horizon)
        row = {}
        for k, act in acts.items():
            succ = np.array([r["y1"] if x else r["y0"] for r, x in zip(test, act)])
            ht = np.array([helper_time(r, a.horizon) if x else 0.0 for r, x in zip(test, act)])
            row[k] = {"payoff": float(payoff(test, act, lam, a.horizon).mean()), "success": float(succ.mean()),
                      "helper_time": float(ht.mean()), "add_rate": float(act.mean())}
        onl = online(test, acts, lam, a.horizon, a.shuffles)
        summ["by_lam"][f"{lam:g}"] = {"rules": row, "online": onl}
        L += [f"## lam = {lam:g}", "", "| rule | payoff | success | helper time | adds |", "|---|---|---|---|---|"]
        for k, v in row.items():
            L.append(f"| {k} | {v['payoff']:.3f} | {100 * v['success']:.1f}% | {v['helper_time']:.3f} | "
                     f"{100 * v['add_rate']:.0f}% |")
        L += ["", f"Online over {a.shuffles} random orders (experts: {', '.join(onl['experts'])}); best fixed expert "
              f"mean payoff {onl['best_expert_mean_payoff']:.3f}:", "",
              "| learner | mean payoff | regret at end (total / per task) | regret after 50 / 200 tasks |", "|---|---|---|---|"]
        for k in ("hedge", "exp4", "exp3"):
            v = onl[k]
            ra = v["regret_at"]
            L.append(f"| {k} | {v['mean_payoff']:.3f} | {v['regret_final']:.1f} / {v['regret_per_task_final']:.3f} | "
                     f"{ra.get('50', float('nan')):.1f} / {ra.get('200', float('nan')):.1f} |")
        L.append("")
    (out / "summary.json").write_text(json.dumps(summ, indent=1))
    (out / "summary.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
