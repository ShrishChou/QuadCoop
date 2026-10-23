"""The method registry: one entry per model we report, kept in evals/registry.yaml.

Training output stays in logs/rsl_rl/ (scratch, many attempts). A model we want to keep and
report is *registered*: its checkpoint (and the params/ folder the walker loader checks) is
copied to logs/evals/<id>/ (a stable place outside the training runs; not committed), and
evals/registry.yaml (committed) records what it is:

    s2b-anymal:
      stage: stage2              # walker | stage1b | stage1c | stage2
      task: QuadCoop-Push2b-AnymalC
      checkpoint: logs/evals/s2b-anymal/model.pt
      walker: walker-anymal-v1   # registry id of the walker it runs on (push policies)
      env: {QUADCOOP_SHAPES: v2} # env vars needed to rebuild its env exactly
      source: logs/rsl_rl/push2b_anymal_c/2026-10-22_10-31-59_seed0/model_5999.pt
      note: Stage 2b, robot-frame map, 6000 it.

Evaluations run with scripts/eval_method.py: videos, snapshots and other bulky output go to
logs/evals/<id>/<suite>/; the stats (summary.md / summary.json / episodes.csv / validation.json)
are copied to evals/<id>/eval/<suite>/ for the repo, and scripts/report.py turns them into
evals/README.md.

    python scripts/methods.py register --id s2b-anymal --stage stage2 --task QuadCoop-Push2b-AnymalC \\
        --checkpoint logs/rsl_rl/push2b_anymal_c/<run>/model_5999.pt --walker walker-anymal-v1 \\
        --env QUADCOOP_SHAPES=v2 --note "Stage 2b, 6000 it"
    python scripts/methods.py list
"""

from __future__ import annotations

import argparse
import datetime as dt
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
EVALS = ROOT / "evals"  # committed: registry + stats
STORE = ROOT / "logs" / "evals"  # not committed: checkpoints, videos
REGISTRY = EVALS / "registry.yaml"
STAGES = ("walker", "stage1b", "stage1c", "stage2")


def load() -> dict:
    if not REGISTRY.exists():
        return {}
    return yaml.safe_load(REGISTRY.read_text()) or {}


def save(reg: dict) -> None:
    EVALS.mkdir(exist_ok=True)
    REGISTRY.write_text(yaml.safe_dump(dict(sorted(reg.items())), sort_keys=False, width=110))


def resolve(mid: str, reg: dict | None = None) -> dict:
    """The entry plus everything needed to run it: absolute checkpoint, walker checkpoint and
    the merged env vars (walker's first, then the method's own)."""
    reg = reg or load()
    if mid not in reg:
        raise SystemExit(f"unknown method {mid!r}; registered: {', '.join(sorted(reg)) or '(none)'}")
    m = dict(reg[mid])
    env = {}
    if m.get("walker"):
        w = reg[m["walker"]]
        env.update(w.get("env") or {})
        m["walker_checkpoint"] = str(ROOT / w["checkpoint"])
    env.update(m.get("env") or {})
    m["env_all"] = {k: str(v) for k, v in env.items()}
    m["checkpoint_abs"] = str(ROOT / m["checkpoint"])
    return m


def register(a) -> int:
    reg = load()
    if a.id in reg and not a.force:
        raise SystemExit(f"{a.id} is already registered (pass --force to replace it)")
    if a.stage not in STAGES:
        raise SystemExit(f"--stage must be one of {STAGES}")
    if a.stage != "walker" and not a.walker:
        raise SystemExit("push policies need --walker <registered walker id>")
    if a.walker and a.walker not in reg:
        raise SystemExit(f"walker {a.walker!r} is not registered yet")
    src = Path(a.checkpoint)
    if not src.exists():
        raise SystemExit(f"{src} not found")
    dst_dir = STORE / a.id
    dst_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst_dir / "model.pt")
    params = src.parent / "params"
    if params.is_dir():  # the walker loader checks params/env.yaml (joint gains)
        shutil.copytree(params, dst_dir / "params", dirs_exist_ok=True)
    try:
        commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True,
                                text=True).stdout.strip()
    except Exception:  # noqa: BLE001
        commit = ""
    env = dict(kv.split("=", 1) for kv in a.env)
    reg[a.id] = {
        "stage": a.stage, "task": a.task, "checkpoint": str((dst_dir / "model.pt").relative_to(ROOT)),
        **({"walker": a.walker} if a.walker else {}),
        "env": env, "source": str(src), "registered": dt.date.today().isoformat(),
        "commit": commit, "note": a.note,
    }
    save(reg)
    print(f"registered {a.id}: {src} -> {dst_dir / 'model.pt'}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("register")
    r.add_argument("--id", required=True)
    r.add_argument("--stage", required=True, choices=STAGES)
    r.add_argument("--task", required=True)
    r.add_argument("--checkpoint", required=True)
    r.add_argument("--walker", default=None, help="registry id of the walker (push policies)")
    r.add_argument("--env", nargs="*", default=[], help="KEY=VALUE env vars its env needs")
    r.add_argument("--note", default="")
    r.add_argument("--force", action="store_true")
    sub.add_parser("list")
    a = ap.parse_args()
    if a.cmd == "register":
        return register(a)
    for k, v in load().items():
        print(f"{k:28s} {v['stage']:8s} {v['task']:30s} {v.get('walker', ''):20s} {v.get('note', '')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
