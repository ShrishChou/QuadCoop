"""Run a standard evaluation suite on a registered method.

Everything (videos, snapshots, per-episode data) is written to logs/evals/<id>/<suite>/; the stats
files are then copied to evals/<id>/eval/<suite>/, the part that goes in the repo.

Suites (same settings for every method of a stage, so results compare directly):

  walker    standard   eval_walker (track, resist 25% body weight, push objects) + the Stage 0 gate
  stage1b/c standard   eval_push.py defaults (its task grid, 40 s)
  stage2    standard   eval_push2.py defaults: 12 shapes, in/out-of-range sizes, 10/25/40 kg,
                       40 s, 10 cm / 6 deg held 1 s, all ablations of the variant, videos
            h80        same success rule, 80 s, training-range sizes, no ablations, no videos
            precise    80 s, 10 cm / 3 deg with the object at rest (the "terminate" rule)

    python scripts/eval_method.py --id s2b-anymal --suite standard
    python scripts/eval_method.py --id s2b-anymal --suite h80 --dry-run      # print the command
    ID=s2b-anymal SUITE=h80 sbatch slurm/eval_method.sbatch
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from methods import EVALS, STORE, resolve  # noqa: E402

STATS = ("summary.md", "summary.json", "episodes.csv", "eval.json", "validation.json", "vs_mass.png")

SUITES = {
    "walker": {"standard": []},
    "stage1b": {"standard": []},
    "stage1c": {"standard": []},
    "stage2": {
        "standard": [],
        "h80": ["--horizon", "80", "--conditions", "normal", "--sizes", "in", "--videos", "0",
                "--ablation-videos", "0"],
        "precise": ["--horizon", "80", "--yaw-tol", "3", "--hold", "0.02", "--settle-speed", "0.15",
                    "--conditions", "normal", "--sizes", "in", "--videos", "1", "--ablation-videos", "0"],
    },
}


def commands(mid: str, suite: str, extra: list[str]) -> tuple[list[list[str]], dict, Path]:
    m = resolve(mid)
    stage = m["stage"]
    if suite not in SUITES[stage]:
        raise SystemExit(f"suite {suite!r} not defined for {stage}; choose from {sorted(SUITES[stage])}")
    out = STORE / mid / suite  # full output (videos etc.)
    env = dict(m["env_all"])
    py = sys.executable
    if stage == "walker":
        cmds = [[py, "scripts/eval_walker.py", "--task", m["task"], "--checkpoint", m["checkpoint_abs"],
                 "--out-dir", str(out), "--video"],
                [py, "scripts/validate_walker.py", "--task", m["task"], "--checkpoint", m["checkpoint_abs"],
                 "--num-envs", "256", "--out", str(out / "validation.json")]]
        env.pop("QUADCOOP_PUSH_FORCE", None)  # test B applies its own force
    else:
        env["QUADCOOP_WALKER_CKPT"] = m["walker_checkpoint"]
        script = "scripts/eval_push2.py" if stage == "stage2" else "scripts/eval_push.py"
        cmds = [[py, script, "--task", m["task"], "--checkpoint", m["checkpoint_abs"],
                 "--walker", m["walker_checkpoint"], "--out", str(out), *SUITES[stage][suite], *extra]]
    return cmds, env, out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--id", required=True)
    ap.add_argument("--suite", default="standard")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("extra", nargs="*", help="extra args passed to the eval script (after --)")
    a = ap.parse_args()
    cmds, env, out = commands(a.id, a.suite, a.extra)
    for c in cmds:
        print(" ".join(f"{k}={v}" for k, v in env.items()), " ".join(c), flush=True)
    if a.dry_run:
        return 0
    out.mkdir(parents=True, exist_ok=True)
    full = {**os.environ, **env}
    for k in ("QUADCOOP_WALKER_CKPT_ANYMAL_C", "QUADCOOP_WALKER_CKPT_SPOT", "QUADCOOP_PUSH_FORCE"):
        if k not in env:
            full.pop(k, None)
    rc = 0
    for c in cmds:
        r = subprocess.run(c, cwd=ROOT, env=full).returncode
        # validate_walker exits 1 when the gate is not passed: a result, not an error
        if r != 0 and not (r == 1 and "validate_walker.py" in c[1]):
            print(f"command failed ({r}): {' '.join(c)}")
            rc = r
            break
    import shutil

    stats = EVALS / a.id / "eval" / a.suite
    stats.mkdir(parents=True, exist_ok=True)
    for name in STATS:
        if (out / name).exists():
            shutil.copy2(out / name, stats / name)
    print(f"stats in {stats}\nvideos and full output in {out}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
