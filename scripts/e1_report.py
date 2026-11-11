"""Diagnostic E1 (and any matched arm comparison): per-arm metrics and paired contrasts with bootstrap 95% CIs.

  python scripts/e1_report.py A=logs/evals/<a>-expert/pair B=... [C=... D=...] [--contrast B-A,D-C,...] [--out file.md]

Arms are eval folders from scripts/contact_test.py with the same tasks (object, mass, scenario, rep). Episode
metrics come from episodes.csv; trace metrics (need --trace 2) from trace_<mass>kg.csv.gz. Contrasts are paired
over tasks and bootstrapped over tasks (not timesteps). With arms A-D present the default contrasts are the E1
factorial: start (B-A, D-C), fixed pair (C-A, D-B) and their interaction (D-C)-(B-A).

Definitions (all from the 10 Hz traces unless noted):
  useful press      force along the push direction >= 30 N (force magnitude reported alongside)
  first push        first time either robot holds a useful press 0.5 s; both: both at once for 0.5 s.
                    Censored at the episode end: reported as the share reached within 10 s and the mean
                    time capped at 30 s (restricted mean), never as a mean over only the successes
  progress@T        1 - pose_err(T) / pose_err(0) (pose_err = the planner's position + scaled heading error)
  capped time       time to success, or the 80 s horizon if not successful (from episodes.csv)
  reassignments     changes of the recorded contact ids, by the planner's re-plan cause
"""
import collections
import csv
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import exec_report as X  # noqa: E402

PRESS = X.PRESS
HOLD = 5          # samples (0.5 s) a press must last to count
CAP = 30.0        # s, restricted-mean cap for first-push times
HORIZON = 80.0
REASONS = {0: "reset", 1: "timer", 2: "residual", 3: "no progress", 4: "weak pair", 5: "finish", 6: "slow arrival"}
rng = np.random.default_rng(0)


def num(x):
    return X.num(x)


def first_hold(m):
    """Index of the first run of HOLD True samples (its start), or None."""
    run = 0
    for i, v in enumerate(m):
        run = run + 1 if v else 0
        if run >= HOLD:
            return i - HOLD + 1
    return None


def trace_metrics(d):
    """{(object, mass, scenario, rep): dict} from the traces."""
    out = {}
    seen = collections.Counter()
    for obj, sc, mass, outcome, rows in X.traces(d):
        key3 = (obj, f"{float(mass):.1f}", sc)
        rep = seen[key3]
        seen[key3] += 1
        ags = X.agents(rows[0].keys())
        t = np.array([float(r["t"]) for r in rows])
        col = lambda c: np.array([num(r[c]) for r in rows])  # noqa: E731
        live = col("live") > 0.5
        pe = col("pose_err")
        pe0 = pe[0] if pe[0] > 1e-6 else np.nan
        prog = lambda T: (1.0 - (pe[min(int(T / 0.1), len(pe) - 1)] / pe0)) if live.any() else np.nan  # noqa: E731
        fa = np.stack([col(f"force_along_cmd_{a}") for a in ags])
        fm = np.stack([col(f"force_{a}") for a in ags])
        on = np.stack([col(f"on_{a}") > 0.5 for a in ags])
        press = fa >= PRESS
        i1 = first_hold(press.any(0))
        i2 = first_hold(press.all(0))
        sc_ = X.stall_causes(rows, ags, t)
        lv = live.sum()
        m = dict(prog5=prog(5.0), prog10=prog(10.0), prog20=prog(20.0),
                 push1=t[i1] if i1 is not None else np.inf, push2=t[i2] if i2 is not None else np.inf,
                 end=t[-1], stalled=sc_["stalled_s"] / max(sc_["live_s"], 1e-9),
                 causes=np.bincount(sc_["cause"][sc_["cause"] >= 0].astype(int), minlength=len(X.CAUSES)) * 0.1,
                 press_along=press[:, live].mean() if lv else np.nan,
                 press_mag=(fm[:, live] >= PRESS).mean() if lv else np.nan,
                 on_not_touch=(on & ~(np.stack([col(f"touching_{a}") for a in ags]) > 0.5))[:, live].mean() if lv else np.nan,
                 both_press=press.all(0)[live].mean() if lv else np.nan, sus=sc_["sus_s"] / max(sc_["live_s"], 1e-9))
        if f"cidx_{ags[0]}" in rows[0]:
            ci = np.stack([col(f"cidx_{a}") for a in ags])
            pr = col("plan_reason")
            ch = (np.diff(ci, axis=1) != 0).any(0)
            m["reassign"] = int(ch.sum())
            m["reassign_why"] = collections.Counter(REASONS.get(int(pr[i + 1]), "?") for i in np.nonzero(ch)[0])
            m["replans"] = float(col("plan_n")[-1])
        out[(obj, f"{float(mass):.1f}", sc, str(rep))] = m
    return out


def episodes(d):
    E = {}
    for r in csv.DictReader(open(Path(d) / "episodes.csv")):
        E[(r["object"], f"{float(r['mass']):.1f}", r["scenario"], r["rep"])] = r
    return E


def ep_metrics(r):
    s = num(r["success"])
    ts = num(r.get("t_success", ""))
    return dict(success=s, capped=(ts if s > 0.5 and ts == ts else HORIZON),
                fell=float(r["outcome"].startswith("fell")), horizon=float(r["outcome"] == "horizon"),
                final_pos=num(r["final_pos_err"]), min_pos=num(r["min_pos_err"]))


def boot(diffs, n=2000):
    d = np.asarray(diffs, float)
    d = d[~np.isnan(d)]
    if not len(d):
        return np.nan, np.nan, np.nan
    idx = rng.integers(0, len(d), size=(n, len(d)))
    bs = d[idx].mean(1)
    return d.mean(), np.percentile(bs, 2.5), np.percentile(bs, 97.5)


def fmt_ci(t):
    m, lo, hi = t
    return f"{m:+.3f} [{lo:+.3f}, {hi:+.3f}]"


def main():
    arms, contrasts, out_md = {}, None, None
    for x in sys.argv[1:]:
        if x.startswith("--contrast="):
            contrasts = x.split("=", 1)[1].split(",")
        elif x.startswith("--out="):
            out_md = x.split("=", 1)[1]
        else:
            k, v = x.split("=", 1)
            arms[k] = Path(v)
    E = {k: episodes(v) for k, v in arms.items()}
    T = {k: trace_metrics(v) for k, v in arms.items()}
    keys = sorted(set.intersection(*[set(e) for e in E.values()]))
    lines = [f"tasks matched across arms: {len(keys)}  ({', '.join(f'{k}: {len(E[k])} episodes, {len(T[k])} traced' for k in arms)})", ""]
    for k, v in arms.items():
        lines.append(f"- {k}: {v}")
    lines.append("")

    def per_arm(k, ks):
        em = [ep_metrics(E[k][x]) for x in ks]
        tm = [T[k][x] for x in ks if x in T[k]]
        g = lambda f: np.nanmean([m[f] for m in em]) if em else np.nan  # noqa: E731
        h = lambda f: np.nanmean([m[f] for m in tm]) if tm else np.nan  # noqa: E731
        p1 = np.array([m["push1"] for m in tm]) if tm else np.array([np.nan])
        p2 = np.array([m["push2"] for m in tm]) if tm else np.array([np.nan])
        ra = [m.get("reassign", np.nan) for m in tm]
        return dict(n=len(em), success=g("success"), fell=g("fell"), timeout=g("horizon"), capped=g("capped"),
                    prog5=h("prog5"), prog10=h("prog10"), prog20=h("prog20"),
                    push1_10=np.mean(p1 <= 10.0) if tm else np.nan, push1_rm=np.mean(np.minimum(p1, CAP)),
                    push2_10=np.mean(p2 <= 10.0) if tm else np.nan, push2_rm=np.mean(np.minimum(p2, CAP)),
                    stalled=h("stalled"), press_along=h("press_along"), press_mag=h("press_mag"),
                    both=h("both_press"), sus=h("sus"), reassign=np.nanmean(ra) if ra else np.nan,
                    causes=np.sum([m["causes"] for m in tm], 0) if tm else np.zeros(len(X.CAUSES)))

    cols = [("success", "success", ".2f"), ("timeout", "timeout", ".2f"), ("fell", "fell", ".2f"),
            ("capped time s", "capped", ".1f"), ("progress 5/10/20 s", None, None),
            ("first push <=10 s / RM s", None, None), ("both push <=10 s / RM s", None, None),
            ("stalled (episode mean)", "stalled", ".2f"), ("press along / magnitude", None, None), ("both press", "both", ".2f"),
            ("reassign/ep", "reassign", ".1f")]
    for strat, sel in [("all", lambda x: True)] + [(f"{m} kg", (lambda m_: lambda x: x[1] == m_)(m))
                                                   for m in sorted({x[1] for x in keys}, key=float)]:
        ks = [x for x in keys if sel(x)]
        lines += [f"### {strat} (n = {len(ks)} tasks per arm)", "",
                  "| arm | " + " | ".join(c[0] for c in cols) + " |", "|---" * (len(cols) + 1) + "|"]
        for k in arms:
            P = per_arm(k, ks)
            cells = []
            for name, f, fm in cols:
                if f:
                    cells.append(format(P[f], fm))
                elif name.startswith("progress"):
                    cells.append(f"{P['prog5']:.2f} / {P['prog10']:.2f} / {P['prog20']:.2f}")
                elif name.startswith("first"):
                    cells.append(f"{P['push1_10']:.2f} / {P['push1_rm']:.1f}")
                elif name.startswith("both push"):
                    cells.append(f"{P['push2_10']:.2f} / {P['push2_rm']:.1f}")
                else:
                    cells.append(f"{P['press_along']:.2f} / {P['press_mag']:.2f}")
            lines.append(f"| {k} | " + " | ".join(cells) + " |")
        lines.append("")
        lines.append("stalled time by cause (share): " + "; ".join(
            f"{k}: " + ", ".join(f"{c} {v / max(per_arm(k, ks)['causes'].sum(), 1e-9):.2f}" for c, v in zip(X.CAUSES, per_arm(k, ks)['causes']))
            for k in arms))
        lines.append("")

    # reassignment causes
    for k in arms:
        why = collections.Counter()
        for m in T[k].values():
            why.update(m.get("reassign_why", {}))
        if why:
            tot = sum(why.values())
            lines.append(f"{k} reassignments by planner cause: " + ", ".join(f"{c} {n / tot:.2f}" for c, n in why.most_common()) + f" (n={tot})")
    lines.append("")

    if contrasts is None:
        contrasts = ["B-A", "D-C", "C-A", "D-B", "(D-C)-(B-A)"] if all(x in arms for x in "ABCD") else \
            [f"{b}-{a}" for a, b in zip(list(arms)[:-1], list(arms)[1:])]
    metr = [("success", lambda k, x: ep_metrics(E[k][x])["success"]),
            ("capped time s", lambda k, x: ep_metrics(E[k][x])["capped"]),
            ("progress@10s", lambda k, x: T[k][x]["prog10"] if x in T[k] else np.nan),
            ("first push RM s", lambda k, x: min(T[k][x]["push1"], CAP) if x in T[k] else np.nan),
            ("both push RM s", lambda k, x: min(T[k][x]["push2"], CAP) if x in T[k] else np.nan),
            ("fell", lambda k, x: ep_metrics(E[k][x])["fell"])]

    def contrast(expr, f, ks):
        if expr.startswith("("):  # (D-C)-(B-A)
            l, r = expr[1:].split(")-(")
            r = r.rstrip(")")
            (a1, b1), (a2, b2) = l.split("-"), r.split("-")
            return [(f(a1, x) - f(b1, x)) - (f(a2, x) - f(b2, x)) for x in ks]
        a, b = expr.split("-")
        return [f(a, x) - f(b, x) for x in ks]

    lines += ["### paired contrasts (mean [bootstrap 95% CI over tasks])", "",
              "| contrast | stratum | " + " | ".join(m[0] for m in metr) + " |", "|---" * (len(metr) + 2) + "|"]
    for c in contrasts:
        for strat, sel in [("all", lambda x: True)] + [(f"{m} kg", (lambda m_: lambda x: x[1] == m_)(m))
                                                       for m in sorted({x[1] for x in keys}, key=float)]:
            ks = [x for x in keys if sel(x)]
            lines.append(f"| {c} | {strat} | " + " | ".join(fmt_ci(boot(contrast(c, f, ks))) for _, f in metr) + " |")
    txt = "\n".join(lines)
    print(txt)
    if out_md:
        Path(out_md).write_text(txt + "\n")


if __name__ == "__main__":
    main()
