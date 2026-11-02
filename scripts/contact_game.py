"""Stage 5: the contact game. Each robot picks one of the object's contacts; both are rewarded by
the team outcome. Payoffs come from the payoff sweep (scripts/contact_test.py --executor stage4
--rules allpairs), which ran the Stage 4 contact policy from every usable ordered contact pair of
every task (object x scenario x mass, several placements each).

    python scripts/contact_game.py --sweep evals/game-s4b-allpairs              # -> evals/game-s4b-game/
    python scripts/contact_game.py --sweep evals/game-s4b-allpairs --payoff success --rounds 3000

Per task (object, scenario, mass) this builds the payoff matrix M[a, b] (robot 1 at contact a,
robot 2 at contact b; mean over placements) on each robot's action set (the contacts that push
within 75 deg of the goal). Joint actions the policy cannot be given (the same contact, or
standing points closer than 0.85 m) are collisions and pay 0. Then:

* team optimum: the best pair (a common-payoff game: it is also the best Nash equilibrium and the
  best correlated equilibrium - a mediator that recommends it is all the coordination needed);
* pure Nash equilibria: pairs where neither robot gains by switching alone; the worst one shows
  how badly two robots can get stuck (miscoordination traps); their number shows how hard
  equilibrium selection is;
* the hand-made rules (spread, adjacent: quadcoop/contacts.py assign) and a random usable pair, as
  read off the same matrix;
* independent learning: two learners, each seeing only its own action set, play the game
  repeatedly with noisy payoffs (each round's payoff is one recorded episode of that pair, drawn
  at random): regret matching, RM+, multiplicative weights (Hedge) - full information: each
  learner is told what each of its actions would have paid against the partner's choice - and
  Exp3 - bandit feedback: only the payoff of what it played. Reported: the expected team payoff of
  their joint play over time relative to the optimum, and how often the most played pair at the
  end is the optimum.

Payoff (--payoff): "score" (default) = 0.5 x success + 0.5 x closeness, closeness = (1 - final
distance / start distance) x (1 - final heading error / 45 deg), both clipped to [0, 1], so the
games are not flat where nothing succeeds; "success" = success only.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
import zlib
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
ALGOS = ("regret_matching", "rm_plus", "hedge", "exp3")


def payoff_of(r: dict, kind: str) -> float:
    succ = float(r["success"])
    if kind == "success":
        return succ
    d0 = max(float(r["distance"]), 1e-6)
    close = max(0.0, 1.0 - float(r["final_pos_err"]) / d0) * max(0.0, 1.0 - float(r["final_yaw_err"]) / 45.0)
    return 0.5 * succ + 0.5 * min(1.0, close)


def load_tasks(sweep_dirs: list[Path], kind: str) -> dict:
    """{(object, scenario, mass): {"pairs": {(a, b): [payoffs]}, "labels": {idx: label}}}."""
    tasks = defaultdict(lambda: {"pairs": defaultdict(list), "labels": {}})
    for d in sweep_dirs:
        f = d / "eval" / "pair" / "episodes.csv" if (d / "eval").exists() else d / "episodes.csv"
        for r in csv.DictReader(open(f)):
            if r.get("contact_idx_1", "") in ("", None) or r.get("contact_idx_2", "") in ("", None):
                continue
            key = (r["object"], r["scenario"], float(r["mass"]))
            a, b = int(r["contact_idx_1"]), int(r["contact_idx_2"])
            tasks[key]["pairs"][(a, b)].append(payoff_of(r, kind))
            tasks[key]["labels"][a] = r["contact_1"]
            tasks[key]["labels"][b] = r["contact_2"]
    return tasks


def matrix(task: dict):
    acts = sorted({a for a, _ in task["pairs"]} | {b for _, b in task["pairs"]})
    pos = {a: i for i, a in enumerate(acts)}
    n = len(acts)
    M = np.zeros((n, n))
    feas = np.zeros((n, n), dtype=bool)
    samples = {}
    for (a, b), v in task["pairs"].items():
        M[pos[a], pos[b]] = float(np.mean(v))
        feas[pos[a], pos[b]] = True
        samples[(pos[a], pos[b])] = np.array(v)
    return acts, M, feas, samples


def pure_nash(M: np.ndarray, feas: np.ndarray, tol: float = 1e-9) -> list[tuple[int, int]]:
    """Pure equilibria among feasible pairs (infeasible pairs pay 0 as deviations)."""
    out = []
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            if feas[i, j] and M[i, j] >= M[:, j].max() - tol and M[i, j] >= M[i, :].max() - tol:
                out.append((i, j))
    return out


def learn(M: np.ndarray, feas: np.ndarray, samples: dict, algo: str, rounds: int, rng: np.random.Generator):
    """Two independent learners on the common-payoff game. Returns the expected team payoff of the
    current joint mixed strategy per round (against the true mean matrix) and the empirical joint
    play counts."""
    n = M.shape[0]

    def draw(i, j):  # a noisy payoff: one recorded episode of that pair (collisions pay 0)
        if not feas[i, j]:
            return 0.0
        v = samples[(i, j)]
        return float(v[rng.integers(len(v))])

    def counterfactual(own_is_row: bool, partner: int) -> np.ndarray:
        return np.array([draw(k, partner) if own_is_row else draw(partner, k) for k in range(n)])

    curve = np.zeros(rounds)
    counts = np.zeros((n, n))
    if algo in ("regret_matching", "rm_plus"):
        R = [np.zeros(n), np.zeros(n)]

        def strat(r):
            pos = np.maximum(r, 0.0)
            s = pos.sum()
            return pos / s if s > 0 else np.full(n, 1.0 / n)
        for t in range(rounds):
            p, q = strat(R[0]), strat(R[1])
            curve[t] = float(p @ M @ q)
            i, j = rng.choice(n, p=p), rng.choice(n, p=q)
            counts[i, j] += 1
            u1, u2 = counterfactual(True, j), counterfactual(False, i)
            R[0] += u1 - u1[i]
            R[1] += u2 - u2[j]
            if algo == "rm_plus":
                R[0] = np.maximum(R[0], 0.0)
                R[1] = np.maximum(R[1], 0.0)
    elif algo == "hedge":
        eta = math.sqrt(8.0 * math.log(max(n, 2)) / rounds)
        W = [np.zeros(n), np.zeros(n)]
        for t in range(rounds):
            p = np.exp(W[0] - W[0].max()); p /= p.sum()
            q = np.exp(W[1] - W[1].max()); q /= q.sum()
            curve[t] = float(p @ M @ q)
            i, j = rng.choice(n, p=p), rng.choice(n, p=q)
            counts[i, j] += 1
            W[0] += eta * counterfactual(True, j)
            W[1] += eta * counterfactual(False, i)
    elif algo == "exp3":
        gamma = min(1.0, math.sqrt(n * math.log(max(n, 2)) / ((math.e - 1) * rounds)))
        W = [np.zeros(n), np.zeros(n)]
        for t in range(rounds):
            ps = []
            for w in W:
                e = np.exp(w - w.max())
                ps.append((1 - gamma) * e / e.sum() + gamma / n)
            p, q = ps
            curve[t] = float(p @ M @ q)
            i, j = rng.choice(n, p=p), rng.choice(n, p=q)
            counts[i, j] += 1
            x = draw(i, j)  # payoffs in [0, 1]
            W[0][i] += gamma * (x / p[i]) / n
            W[1][j] += gamma * (x / q[j]) / n
    else:
        raise ValueError(algo)
    return curve, counts


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sweep", nargs="+", required=True, help="payoff sweep output(s): evals/<prefix>-allpairs")
    ap.add_argument("--out", default=None, help="default evals/<prefix>-game")
    ap.add_argument("--payoff", choices=("score", "success"), default="score")
    ap.add_argument("--rounds", type=int, default=2000)
    ap.add_argument("--seeds", type=int, default=20)
    ap.add_argument("--min-actions", type=int, default=2, help="skip tasks where a robot has fewer choices")
    a = ap.parse_args()

    sweep = [Path(s) if Path(s).is_absolute() else ROOT / s for s in a.sweep]
    name = sweep[0].name.removesuffix("-allpairs")
    out = Path(a.out) if a.out else ROOT / "evals" / f"{name}-game"
    out.mkdir(parents=True, exist_ok=True)
    tasks = load_tasks(sweep, a.payoff)
    if not tasks:
        raise SystemExit(f"no pair episodes in {sweep} (run contact_test.py --executor stage4 --rules allpairs)")

    import os
    os.environ.setdefault("QUADCOOP_SHAPES", "v2")
    from quadcoop import contacts as C
    from quadcoop.stage2.shapes import SHAPE_NAMES2, kinds_tensor, nominal_parts
    parts, rest = nominal_parts("cpu")
    kinds = kinds_tensor("cpu")
    cand = {nm: C.candidates(parts[s].numpy(), kinds[s].numpy(), float(rest[s])) for s, nm in enumerate(SHAPE_NAMES2)}
    scen_dir = {"A_straight": 0.0, "B_left": 60.0, "C_backright": -135.0, "D_far_turn": 0.0}

    rows, curves = [], {al: [] for al in ALGOS}
    examples = {}
    for key in sorted(tasks):
        obj, scen, mass = key
        acts, M, feas, samples = matrix(tasks[key])
        n = len(acts)
        if n < a.min_actions or feas.sum() < 1:
            continue
        opt = float(M[feas].max())
        oi, oj = np.unravel_index(np.where(feas, M, -1.0).argmax(), M.shape)
        ne = pure_nash(M, feas)
        ne_vals = [float(M[i, j]) for i, j in ne]
        gd = math.radians(scen_dir.get(scen, 0.0))
        u = np.array([math.cos(gd), math.sin(gd)])
        pos = {c: i for i, c in enumerate(acts)}

        def rule_value(rule):
            pr = C.assign(cand[obj], u, rule, min_sep=0.85)
            if pr[1] is None or pr[0] not in pos or pr[1] not in pos:
                return None
            i, j = pos[pr[0]], pos[pr[1]]
            v = [M[i, j]] if feas[i, j] else []
            if feas[j, i]:
                v.append(M[j, i])
            return float(np.mean(v)) if v else None
        row = {"object": obj, "scenario": scen, "mass": mass, "actions": n, "feasible_pairs": int(feas.sum()),
               "optimum": round(opt, 3), "optimum_pair": f"{tasks[key]['labels'][acts[oi]]} + {tasks[key]['labels'][acts[oj]]}",
               "pure_nash": len(ne), "worst_nash": round(min(ne_vals), 3) if ne else "",
               "mean_feasible": round(float(M[feas].mean()), 3),
               "spread": rule_value("spread"), "adjacent": rule_value("adjacent")}
        for al in ALGOS:
            fin, hit = [], []
            for sd in range(a.seeds):
                rng = np.random.default_rng(1000 * sd + zlib.crc32(repr(key).encode()) % 997)  # stable across runs
                curve, counts = learn(M, feas, samples, al, a.rounds, rng)
                curves[al].append(curve / max(opt, 1e-6))
                fin.append(float(curve[-100:].mean()))
                last = np.unravel_index(counts.argmax(), counts.shape)
                hit.append(float(M[last] >= opt - 1e-9))
            row[f"{al}_final"] = round(float(np.mean(fin)), 3)
            row[f"{al}_found_optimum"] = round(float(np.mean(hit)), 2)
        rows.append(row)
        if scen == "A_straight" and obj in ("beam", "arch", "dumbbell", "u_channel") and (obj not in examples or mass < examples[obj][0]):
            examples[obj] = (mass, M.copy(), feas.copy(), [tasks[key]["labels"][c] for c in acts], scen)

    with open(out / "tasks.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    f2 = lambda x: "" if x in (None, "") else f"{x:.2f}"  # noqa: E731
    rich = [r for r in rows if r["actions"] >= 4]

    def mean_of(sel, k):
        v = [r[k] for r in sel if r[k] not in (None, "")]
        return float(np.mean(v)) if v else None
    agg = {}
    for label, sel in (("all tasks", rows), ("tasks with 4+ contacts per robot", rich)):
        agg[label] = {k: mean_of(sel, k) for k in ["optimum", "worst_nash", "mean_feasible", "spread", "adjacent"]
                      + [f"{al}_final" for al in ALGOS] + [f"{al}_found_optimum" for al in ALGOS]}
        agg[label]["tasks"] = len(sel)
        agg[label]["pure_nash"] = mean_of(sel, "pure_nash")
        agg[label]["trap_share"] = (sum(1 for r in sel if r["worst_nash"] != "" and r["worst_nash"] < r["optimum"] - 0.1)
                                    / max(1, len(sel)))
    summary = {"sweep": [str(s) for s in sweep], "payoff": a.payoff, "rounds": a.rounds, "seeds": a.seeds,
               "aggregate": agg, "tasks": rows}
    (out / "summary.json").write_text(json.dumps(summary, indent=1))

    # plots: learning curves, example payoff matrices
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(7, 4))
        for al in ALGOS:
            cv = np.array(curves[al])
            ax.plot(cv.mean(0), label=al.replace("_", " "))
        ax.set_xlabel("round")
        ax.set_ylabel("expected team payoff / optimum")
        ax.set_ylim(0, 1.05)
        ax.grid(alpha=0.3)
        ax.legend()
        ax.set_title(f"Independent learners on the contact game ({len(rows)} tasks, {a.seeds} seeds)")
        fig.savefig(out / "learning_curves.png", dpi=110, bbox_inches="tight")
        plt.close(fig)
        if examples:
            fig, axes = plt.subplots(1, len(examples), figsize=(5.5 * len(examples), 5))
            axes = np.atleast_1d(axes)
            for ax, (obj, (mass, M, feas, labels, scen)) in zip(axes, sorted(examples.items())):
                show = np.where(feas, M, np.nan)
                im = ax.imshow(show, vmin=0, vmax=1, cmap="viridis")
                ax.set_xticks(range(len(labels)))
                ax.set_yticks(range(len(labels)))
                short = [lb.replace("part ", "p").replace("corner ", "c").replace(" seg ", " s") for lb in labels]
                ax.set_xticklabels(short, rotation=90, fontsize=7)
                ax.set_yticklabels(short, fontsize=7)
                for i, j in pure_nash(M, feas):
                    ax.text(j, i, "N", ha="center", va="center", color="w", fontsize=8, fontweight="bold")
                ax.set_title(f"{obj} {scen} {mass:g} kg (N = pure Nash)")
                ax.set_xlabel("robot 2 contact")
                ax.set_ylabel("robot 1 contact")
            fig.colorbar(im, ax=axes.tolist(), shrink=0.7, label=f"payoff ({a.payoff})")
            fig.savefig(out / "payoff_examples.png", dpi=100, bbox_inches="tight")
            plt.close(fig)
    except Exception as ex:  # noqa: BLE001
        print(f"plots skipped: {ex}")

    md = [f"# Contact game: {name}", "", f"payoff: {a.payoff}; {a.rounds} rounds x {a.seeds} seeds per task; "
          f"sweep {', '.join(s.name for s in sweep)}", "",
          "## summary", "", "| | tasks | optimum | worst pure Nash | share with a trap (worst NE < optimum - 0.1) | pure NE per task "
          "| random usable pair | spread rule | adjacent rule | " + " | ".join(f"{al.replace('_', ' ')} (found optimum)" for al in ALGOS) + " |",
          "|---|---|---|---|---|---|---|---|---|" + "---|" * len(ALGOS)]
    for label, s in agg.items():
        md.append(f"| {label} | {s['tasks']} | {f2(s['optimum'])} | {f2(s['worst_nash'])} | {f2(s['trap_share'])} | "
                  f"{f2(s['pure_nash'])} | {f2(s['mean_feasible'])} | {f2(s['spread'])} | {f2(s['adjacent'])} | "
                  + " | ".join(f"{f2(s[f'{al}_final'])} ({f2(s[f'{al}_found_optimum'])})" for al in ALGOS) + " |")
    md += ["", "Learner columns: expected team payoff of the joint play over the last 100 rounds (and the share of runs "
           "whose most played pair is the optimum).", "", "## per task", "",
           "| object | scenario | mass | contacts | optimum (pair) | pure NE | worst NE | random | spread | adjacent | "
           + " | ".join(al.replace("_", " ") for al in ALGOS) + " |", "|---|---|---|---|---|---|---|---|---|---|" + "---|" * len(ALGOS)]
    for r in rows:
        md.append(f"| {r['object']} | {r['scenario']} | {r['mass']:g} | {r['actions']} | {r['optimum']:.2f} ({r['optimum_pair']}) | "
                  f"{r['pure_nash']} | {f2(r['worst_nash'])} | {r['mean_feasible']:.2f} | {f2(r['spread'])} | {f2(r['adjacent'])} | "
                  + " | ".join(f"{r[f'{al}_final']:.2f}" for al in ALGOS) + " |")
    (out / "summary.md").write_text("\n".join(md) + "\n")
    print("\n".join(md[:8]))
    print(f"\n{len(rows)} tasks -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
