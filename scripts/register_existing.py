"""Register the models trained so far (run once on the cluster; safe to re-run, existing ids
are skipped). Paths are the runs every later stage actually used (checked from the job logs)."""

from __future__ import annotations

import glob
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from methods import load  # noqa: E402

L = "logs/rsl_rl"


def pick(pattern: str, max_iter: int | None = None) -> str | None:
    """Highest model_N.pt (N <= max_iter) among the run folders matching pattern."""
    best = None
    for p in glob.glob(str(ROOT / pattern / "model_*.pt")):
        n = int(re.search(r"model_(\d+)\.pt$", p).group(1))
        if max_iter is not None and n > max_iter:
            continue
        if best is None or n > best[0]:
            best = (n, p)
    return best[1] if best else None


METHODS = [
    # id, stage, task, checkpoint, walker, env, note
    ("walker-anymal-v1", "walker", "QuadCoop-Walker-AnymalC",
     f"{L}/walker_anymal_c/2026-10-19_11-44-16_seed0/model_5999.pt", None, [], "ANYmal walker (all stages use it)"),
    ("walker-spot-v1", "walker", "QuadCoop-Walker-Spot",
     f"{L}/walker_spot/2026-10-19_11-45-37_seed0/model_5999.pt", None, ["QUADCOOP_SPOT_PROFILE=v1"],
     "Spot walker, kp 500 (all stages so far use it)"),
    ("s1b-anymal", "stage1b", "QuadCoop-PushHard-AnymalC", pick(f"{L}/pushhard_anymal_c/2*"),
     "walker-anymal-v1", ["QUADCOOP_SHAPES=v1"], "Stage 1b push-to-pose, v1 shapes"),
    ("s1b-spot", "stage1b", "QuadCoop-PushHard-Spot", pick(f"{L}/pushhard_spot/2*"),
     "walker-spot-v1", ["QUADCOOP_SHAPES=v1"], "Stage 1b push-to-pose, v1 shapes"),
    ("s1c-anymal", "stage1c", "QuadCoop-PushHard2-AnymalC", pick(f"{L}/pushhard2_anymal_c/2*"),
     "walker-anymal-v1", ["QUADCOOP_SHAPES=v2"], "Stage 1c: pose falls, uniform masses, v2 shapes"),
    ("s1c-spot", "stage1c", "QuadCoop-PushHard2-Spot", pick(f"{L}/pushhard2_spot/2*"),
     "walker-spot-v1", ["QUADCOOP_SHAPES=v2"], "Stage 1c: pose falls, uniform masses, v2 shapes"),
]
for robot, R, wk in (("anymal_c", "AnymalC", "walker-anymal-v1"), ("spot", "Spot", "walker-spot-v1")):
    short = "anymal" if robot == "anymal_c" else "spot"
    for v, what in (("ctrl", "control, 42 inputs"), ("a", "object-frame profiles"), ("b", "robot-frame map 10 Hz")):
        METHODS.append((f"s2{v}-{short}", "stage2", f"QuadCoop-Push2{v}-{R}",
                        pick(f"{L}/push2{v}_{robot}/2*_seed0", 6000), wk, ["QUADCOOP_SHAPES=v2"],
                        f"Stage 2{v}: {what}; seed 0, 6000 it"))

reg = load()
for mid, stage, task, ck, walker, env, note in METHODS:
    if mid in reg:
        print(f"skip {mid} (registered)")
        continue
    if not ck or not Path(ROOT / ck if not Path(ck).is_absolute() else ck).exists():
        print(f"SKIP {mid}: no checkpoint found")
        continue
    cmd = [sys.executable, "scripts/methods.py", "register", "--id", mid, "--stage", stage, "--task", task,
           "--checkpoint", str(Path(ck).relative_to(ROOT)) if Path(ck).is_absolute() else ck, "--note", note]
    if walker:
        cmd += ["--walker", walker]
    if env:
        cmd += ["--env", *env]
    subprocess.run(cmd, cwd=ROOT, check=True)
    reg = load()
