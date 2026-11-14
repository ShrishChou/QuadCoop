"""Contact loss and recovery (docs/recovery_eval.md), from eval_coop2.py --recovery traces.

    python scripts/recovery_analysis.py --runs=ten-ippo-source-dev7100-recovery,ten-ippo-it4000-dev7100-recovery \
        [--match=ten-ippo-source-dev7100,ten-ippo-it4000-dev7100] [--out=evals/recovery/summary.md]

Per robot, from 0.1 s bins of physical robot-object contact (contact sensors), live part of the episode only:
  engaged       sustained contact: the 1 s trailing mean of the contact fraction >= 0.3 for >= 1 s (a gait cycle
                is ~0.5-0.8 s, so the pulses of a pushing gait stay engaged)
  disengage     after an engaged period, >= 1 s with no contact at all (a dip inside one gait cycle does not count);
                t_loss = the first contact-free bin, confirmed at t_loss + 1 s
  re-engage     the first bin after t_loss starting 1 s of contact fraction >= 0.3; recovered within W s (W = 1, 3, 5)
                if that is <= W s after confirmation; not recovered and the episode ended first -> censored for W,
                by how it ended (success, own / partner fall, tipped / lost, horizon)
  where         front point in the object frame, last engaged second before the loss vs first second after
                re-engaging: same place if within 0.3 m, else a different part / face
During the separation (t_loss to re-engagement or the episode's end):
  partner_push  share of the time the partner was engaged and behind the object (eval push rule)
  d_pos, d_yaw  change of the object's position error (m) and heading error (deg)
  kind          release near goal (position error <= 0.3 m at the loss), stall (d_pos > -0.05 m and d_yaw > -2 deg),
                productive (d_pos <= -0.10 m or d_yaw <= -5 deg), modest (between)
Prolonged = separation >= 3 s. Episode link: success of episodes with a prolonged stall vs the others.
"""
from __future__ import annotations

import csv
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
S_ON, WIN, GAP, SAME_M = 0.3, 10, 10, 0.3
WINDOWS = (1.0, 3.0, 5.0)


def trailing_mean(x: np.ndarray, w: int) -> np.ndarray:
    c = np.concatenate([[0.0], np.cumsum(x)])
    out = np.empty_like(x, dtype=float)
    for i in range(len(x)):
        lo = max(0, i + 1 - w)
        out[i] = (c[i + 1] - c[lo]) / (i + 1 - lo)
    return out


def forward_mean(x: np.ndarray, j: int, w: int) -> float:
    seg = x[j:j + w]
    return float(seg.mean()) if len(seg) == w else -1.0


def events_for(c: np.ndarray, cp: np.ndarray, push_p: np.ndarray, front: np.ndarray, d: np.ndarray, e: np.ndarray,
               dtb: float):
    """c / cp: own / partner contact fraction per bin (live part); yields event dicts."""
    T = len(c)
    s, sp = trailing_mean(c, WIN), trailing_mean(cp, WIN)
    run_on = 0
    engaged_ever = False
    i = 0
    while i < T:
        run_on = run_on + 1 if s[i] >= S_ON else 0
        if run_on >= WIN:
            engaged_ever = True
        if engaged_ever and c[i] == 0 and i > 0 and c[i - 1] > 0:
            z = i
            while z < T and c[z] == 0:
                z += 1
            if z - i >= GAP:  # a real separation
                t_loss = i
                j = next((k for k in range(i, T) if c[k] > 0 and forward_mean(c, k, WIN) >= S_ON), None)
                end = j if j is not None else T
                before = front[max(0, i - WIN):i].mean(0)
                after = front[j:j + WIN].mean(0) if j is not None else None
                sep = slice(t_loss, max(end, t_loss + 1))
                ev = {"t_loss": t_loss * dtb, "t_re": None if j is None else j * dtb,
                      "sep_s": (end - t_loss) * dtb, "reengaged": j is not None,
                      "place": "" if after is None else ("same" if np.linalg.norm(after - before) < SAME_M else "different"),
                      "place_shift_m": "" if after is None else round(float(np.linalg.norm(after - before)), 2),
                      "partner_push": float(((sp[sep] >= S_ON) & push_p[sep]).mean()),
                      "d_at_loss": float(d[t_loss]),
                      "d_pos": float(d[min(end, T - 1)] - d[t_loss]),
                      "d_yaw": float(np.degrees(e[min(end, T - 1)] - e[t_loss]))}
                if ev["d_at_loss"] <= 0.3:
                    ev["kind"] = "release_near_goal"
                elif ev["d_pos"] > -0.05 and ev["d_yaw"] > -2.0:
                    ev["kind"] = "stall"
                elif ev["d_pos"] <= -0.10 or ev["d_yaw"] <= -5.0:
                    ev["kind"] = "productive"
                else:
                    ev["kind"] = "modest"
                yield ev
                engaged_ever = False  # the next event needs a new engaged period
                run_on = 0
                i = end
                continue
            i = z
            continue
        i += 1


def analyse(name: str):
    rows, eps = [], []
    for f in sorted((ROOT / "logs" / "evals" / name / "pair").glob("recovery_*kg.npz")):
        z = np.load(f, allow_pickle=False)
        dtb, mass = float(z["dt_bin"]), float(z["mass"])
        live, found, push, front, d, e = z["live"], z["found"], z["pushing"], z["front_obj"], z["d"], z["e"]
        for j in range(live.shape[0]):
            L = int(np.argmin(live[j])) if not live[j].all() else live.shape[1]
            key = (str(z["object"][j]), mass, str(z["scenario"][j]), int(z["rep"][j]))
            outcome = str(z["outcome"][j])
            eps.append({"key": key, "success": int(z["success"][j]), "outcome": outcome, "events": []})
            for k in range(2):
                for ev in events_for(found[j, :L, k], found[j, :L, 1 - k], push[j, :L, 1 - k], front[j, :L, k],
                                     d[j, :L], e[j, :L], dtb):
                    conf = ev["t_loss"] + GAP * dtb
                    ev.update(object=key[0], mass=mass, scenario=key[2], rep=key[3], robot=k, outcome=outcome,
                              ep_success=int(z["success"][j]), t_end=L * dtb)
                    for w in WINDOWS:
                        if ev["reengaged"] and ev["t_re"] <= conf + w:
                            ev[f"rec{w:g}"] = "yes"
                        elif L * dtb < conf + w:  # ended before the window ran out
                            own = "fell" in outcome and (f"anymal{k + 1}" in outcome)
                            ev[f"rec{w:g}"] = ("censored_success" if outcome == "success" else
                                               "censored_own_fall" if own else
                                               "censored_partner_fall" if "fell" in outcome else
                                               "censored_" + outcome)
                        else:
                            ev[f"rec{w:g}"] = "no"
                    ev["t_re_after_conf"] = "" if not ev["reengaged"] else round(ev["t_re"] - conf, 1)
                    rows.append(ev)
                    eps[-1]["events"].append(ev)
    return rows, eps


def summary(name: str, rows, eps) -> list[str]:
    n_ep = len(eps)
    md = [f"## {name}", "", f"{n_ep} episodes, {len(rows)} disengagements "
          f"({sum(1 for x in eps if x['events'])} episodes with at least one; "
          f"{len(rows) / max(n_ep, 1):.2f} per episode)", ""]
    md += ["| window after confirmation | recovered | not recovered | censored (success / own fall / partner fall / other) |",
           "|---|---|---|---|"]
    for w in WINDOWS:
        c = Counter(r[f"rec{w:g}"] for r in rows)
        dec = c["yes"] + c["no"]
        oth = sum(v for k, v in c.items() if k.startswith("censored_") and k not in
                  ("censored_success", "censored_own_fall", "censored_partner_fall"))
        md.append(f"| {w:g} s | {c['yes']} ({c['yes'] / max(dec, 1):.0%} of decided) | {c['no']} | "
                  f"{c['censored_success']} / {c['censored_own_fall']} / {c['censored_partner_fall']} / {oth} |")
    t = [r["t_re_after_conf"] for r in rows if r["reengaged"]]
    if t:
        md += ["", f"Re-engagement time after confirmation (s): median {np.median(t):.1f}, p90 {np.percentile(t, 90):.1f} "
               f"(contact-free time is that + 1 s); place: same {sum(r['place'] == 'same' for r in rows)}, "
               f"different {sum(r['place'] == 'different' for r in rows)}"]
    md += ["", "| during separation | n | partner pushing (mean share) | object pos change m (median) | heading change deg (median) | episode success |",
           "|---|---|---|---|---|---|"]
    for kind in ("stall", "productive", "modest", "release_near_goal"):
        rs = [r for r in rows if r["kind"] == kind]
        if rs:
            md.append(f"| {kind} | {len(rs)} | {np.mean([r['partner_push'] for r in rs]):.2f} | "
                      f"{np.median([r['d_pos'] for r in rs]):+.2f} | {np.median([r['d_yaw'] for r in rs]):+.1f} | "
                      f"{np.mean([r['ep_success'] for r in rs]):.0%} |")
    pro = [r for r in rows if r["sep_s"] >= 3.0]
    md += ["", f"Prolonged (>= 3 s) separations: {len(pro)}; by kind " + ", ".join(
        f"{k} {v}" for k, v in Counter(r["kind"] for r in pro).most_common())]
    bad = [x for x in eps if any(r["sep_s"] >= 3.0 and r["kind"] == "stall" for r in x["events"])]
    rest = [x for x in eps if x not in bad]
    md += [(f"Episodes with a prolonged stalled separation: {len(bad)}/{n_ep}, success "
            f"{np.mean([x['success'] for x in bad]):.0%}" if bad else "Episodes with a prolonged stalled separation: 0")
           + (f"; the other episodes: success {np.mean([x['success'] for x in rest]):.0%}" if rest else "")]
    md += ["", "| object | disengagements | prolonged stalls | episodes failed with a prolonged stall |", "|---|---|---|---|"]
    by = defaultdict(list)
    for r in rows:
        by[r["object"]].append(r)
    for o in sorted({x["key"][0] for x in eps}):
        rs = by[o]
        ps = [r for r in rs if r["sep_s"] >= 3.0 and r["kind"] == "stall"]
        fe = {(r["mass"], r["scenario"], r["rep"]) for r in ps if not r["ep_success"]}
        md.append(f"| {o} | {len(rs)} | {len(ps)} | {len(fe)} |")
    return md + [""]


def main() -> int:
    args = dict(x.split("=", 1) for x in sys.argv[1:] if x.startswith("--") and "=" in x)
    runs = args.get("--runs", "ten-ippo-source-dev7100-recovery,ten-ippo-it4000-dev7100-recovery").split(",")
    match = args.get("--match", "").split(",") if args.get("--match") else [None] * len(runs)
    md = ["# Contact loss and recovery", ""]
    for name, ref in zip(runs, match, strict=True):
        rows, eps = analyse(name)
        if not eps:
            md += [f"## {name}", "", "no traces found", ""]
            continue
        if ref:  # the logging pass must reproduce the matched evaluation's episodes
            main_ = {(r["object"], float(r["mass"]), r["scenario"], int(r["rep"])): int(r["success"])
                     for r in csv.DictReader(open(ROOT / "evals" / ref / "eval" / "pair" / "episodes.csv"))}
            same = sum(1 for x in eps if main_.get(x["key"]) == x["success"])
            md += [f"Logging pass vs {ref}: same outcome on {same}/{len(eps)} tasks; successes "
                   f"{sum(x['success'] for x in eps)} vs {sum(main_.get(x['key'], 0) for x in eps)}", ""]
        md += summary(name, rows, eps)
        out_csv = ROOT / "evals" / "recovery" / f"{name}_events.csv"
        out_csv.parent.mkdir(parents=True, exist_ok=True)
        if rows:
            keys = list(rows[0])
            with open(out_csv, "w", newline="") as fh:
                w = csv.DictWriter(fh, fieldnames=keys)
                w.writeheader()
                w.writerows(rows)
    text = "\n".join(md)
    if "--out" in args:
        Path(args["--out"]).write_text(text)
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
