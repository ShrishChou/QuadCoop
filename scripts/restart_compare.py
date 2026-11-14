"""Paired comparison of two evaluations on the same tasks (the ten-object restart: iteration 3000 vs 4000).

    python scripts/restart_compare.py [--ref ten-ippo-source-dev7100] [--new ten-ippo-it4000-dev7100] [--out FILE.md]

Reads evals/<name>/eval/pair/episodes.csv; tasks are matched on (object, mass, scenario, rep) and only tasks
present in both count. Reports, new minus reference:
  success      count and paired change in rate, mean [95% bootstrap CI over matched tasks]; gained (0 -> 1) and
               lost (1 -> 0) successes
  falls        episodes where either robot fell, same paired form
  transport    final distance to the goal (m), paired mean change (negative = closer)
  per object   successes /48 each, change, gained / lost; the targets (>= 70% overall, >= 20/48 on every object)
  groups       arch and cylinder; the strong objects (reference >= 75%, plus sphere and long); l_shape, u_channel
               and plus together (their training exposure rose in the restart, which alone could explain a gain)
"""
from __future__ import annotations

import csv
import random
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEN = ("cube", "long", "sphere", "cylinder", "arch", "dumbbell", "t_shape", "l_shape", "u_channel", "plus")
EXPOSED = ("l_shape", "u_channel", "plus")


def load(name: str) -> dict:
    f = ROOT / "evals" / name / "eval" / "pair" / "episodes.csv"
    out = {}
    for r in csv.DictReader(open(f)):
        if r["object"] not in TEN:
            continue
        k = (r["object"], float(r["mass"]), r["scenario"], int(r["rep"]))
        out[k] = {"success": int(r["success"]), "fell": int(int(r["fell_anymal1"]) or int(r["fell_anymal2"])),
                  "pos": float(r["final_pos_err"])}
    return out


def ci(d: list[float], n: int = 4000, seed: int = 0) -> tuple[float, float, float]:
    rng = random.Random(seed)
    m = sum(d) / len(d)
    bs = sorted(sum(rng.choice(d) for _ in d) / len(d) for _ in range(n))
    return m, bs[int(0.025 * n)], bs[int(0.975 * n) - 1]


def block(keys, A, B, what: str) -> list[str]:
    n = len(keys)
    sa, sb = sum(A[k]["success"] for k in keys), sum(B[k]["success"] for k in keys)
    gain = sum(1 for k in keys if B[k]["success"] > A[k]["success"])
    lost = sum(1 for k in keys if B[k]["success"] < A[k]["success"])
    m, lo, hi = ci([B[k]["success"] - A[k]["success"] for k in keys])
    fa, fb = sum(A[k]["fell"] for k in keys), sum(B[k]["fell"] for k in keys)
    fm, flo, fhi = ci([B[k]["fell"] - A[k]["fell"] for k in keys])
    pm, plo, phi = ci([B[k]["pos"] - A[k]["pos"] for k in keys])
    return [f"| {what} | {n} | {sa} ({sa / n:.1%}) | {sb} ({sb / n:.1%}) | {m:+.3f} [{lo:+.3f}, {hi:+.3f}] | +{gain} / -{lost} "
            f"| {fa} -> {fb} ({fm:+.3f} [{flo:+.3f}, {fhi:+.3f}]) | {pm:+.2f} [{plo:+.2f}, {phi:+.2f}] |"]


def main() -> int:
    args = dict(x.split("=", 1) for x in sys.argv[1:] if x.startswith("--") and "=" in x)
    ref, new = args.get("--ref", "ten-ippo-source-dev7100"), args.get("--new", "ten-ippo-it4000-dev7100")
    A, B = load(ref), load(new)
    keys = sorted(set(A) & set(B))
    if len(keys) != len(A) or len(keys) != len(B):
        print(f"warning: {len(A)} reference / {len(B)} new tasks, {len(keys)} matched", file=sys.stderr)
    by = defaultdict(list)
    for k in keys:
        by[k[0]].append(k)
    hdr = ["| tasks | n | reference | new | success change [95% CI] | gained / lost | falls (change) | final dist m |",
           "|---|---|---|---|---|---|---|---|"]
    md = [f"# {new} vs {ref} (paired, {len(keys)} matched tasks)", "", "## Overall", "", *hdr,
          *block(keys, A, B, "all ten")]
    tot = sum(B[k]["success"] for k in keys)
    need = -(-7 * len(keys) // 10)
    md += ["", f"Target >= 70%: {tot}/{len(keys)} vs {need} needed -> {'met' if tot >= need else 'not met'}.", "",
           "## Per object", "", *hdr]
    below = []
    for o in TEN:
        if by[o]:
            md += block(by[o], A, B, o)
            nb = sum(B[k]["success"] for k in by[o])
            if nb * 48 < 20 * len(by[o]):
                below.append(f"{o} {nb}/{len(by[o])}")
    md += ["", f"Target >= 20/48 on every object: {'met' if not below else 'not met: ' + ', '.join(below)}."]
    strong = sorted({o for o in TEN if by[o] and sum(A[k]["success"] for k in by[o]) >= 0.75 * len(by[o])}
                    | {"sphere", "long"})
    md += ["", "## Groups", "", *hdr,
           *block(by["arch"], A, B, "arch"), *block(by["cylinder"], A, B, "cylinder"),
           *block([k for o in strong for k in by[o]], A, B, "strong: " + ", ".join(strong)),
           *block([k for o in EXPOSED for k in by[o]], A, B, "newly exposed: " + ", ".join(EXPOSED)),
           *block([k for o in TEN if o not in EXPOSED for k in by[o]], A, B, "the other seven"),
           "", "l_shape, u_channel and plus were held out before the restart and are trained on in it: a gain there "
           "has that explanation available.",
           "", "## Strong objects: successes lost (1 -> 0)", ""]
    for o in strong:
        ls = [k for k in by[o] if A[k]["success"] > B[k]["success"]]
        md.append(f"- {o}: {len(ls)} lost" + (": " + "; ".join(f"{k[1]:g} kg {k[2]} rep {k[3]}" for k in ls) if ls else ""))
    text = "\n".join(md) + "\n"
    if "--out" in args:
        Path(args["--out"]).parent.mkdir(parents=True, exist_ok=True)
        Path(args["--out"]).write_text(text)
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
