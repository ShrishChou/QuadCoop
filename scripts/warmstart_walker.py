"""Warm-start the compliant walker (walker v2) from the current walker (v1).

v2's actor and critic see two more inputs (the contact force, last); everything else is the
same network. This copies v1's weights, adds zero-weight input columns for the new inputs (so
v2 starts out behaving exactly like v1), extends the observation normalizers (mean 0, std 1
for the new inputs), drops the optimizer's moment estimates (their shapes changed), resets the
iteration count to 0, optionally raises the action noise so the new behaviour can be explored,
and writes the result as model_0.pt of a new run folder that train.py can resume from.

    python scripts/warmstart_walker.py                        # from the registered v1 walker
    python scripts/warmstart_walker.py --source logs/evals/walker-anymal-v1/model.pt --min-std 0.3
"""

from __future__ import annotations

import argparse
import shutil
import sys
from datetime import datetime
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parents[1]
NEW_INPUTS = 2  # bumper_force (x, y)


def widen(sd: dict, extra: int, what: str) -> dict:
    out = dict(sd)
    w = sd["mlp.0.weight"]
    out["mlp.0.weight"] = torch.cat([w, torch.zeros(w.shape[0], extra, dtype=w.dtype)], 1)
    for k, fill in (("obs_normalizer._mean", 0.0), ("obs_normalizer._var", 1.0), ("obs_normalizer._std", 1.0)):
        if k in sd:
            v = sd[k]
            out[k] = torch.cat([v, torch.full((*v.shape[:-1], extra), fill, dtype=v.dtype)], -1)
    print(f"  {what}: inputs {w.shape[1]} -> {w.shape[1] + extra} (new columns at zero weight)")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source", default="logs/evals/walker-anymal-v1/model.pt", help="v1 walker checkpoint")
    ap.add_argument("--experiment", default="walker_anymal_c_compliant", help="logs/rsl_rl/<experiment>/")
    ap.add_argument("--name", default="init_from_v1", help="run folder suffix")
    ap.add_argument("--min-std", type=float, default=0.3, help="raise the action noise to at least this (0 = keep)")
    a = ap.parse_args()
    src = Path(a.source)
    if not src.is_absolute():
        src = ROOT / src
    ck = torch.load(str(src), map_location="cpu", weights_only=False)
    print(f"source {src} (iteration {ck.get('iter')})")
    actor = widen(ck["actor_state_dict"], NEW_INPUTS, "actor")
    critic = widen(ck["critic_state_dict"], NEW_INPUTS, "critic")
    if a.min_std > 0 and "distribution.std_param" in actor:
        sp = actor["distribution.std_param"]
        print(f"  action noise: {[round(float(x), 3) for x in sp]} -> at least {a.min_std:g}")
        actor["distribution.std_param"] = sp.clamp(min=a.min_std)
    opt = ck.get("optimizer_state_dict") or {}
    if isinstance(opt, dict) and "param_groups" in opt:
        opt = {"state": {}, "param_groups": opt["param_groups"]}  # moments dropped (shapes changed)
    out = {"actor_state_dict": actor, "critic_state_dict": critic, "optimizer_state_dict": opt, "iter": 0,
           "infos": {"warm_start_from": str(src), "source_iter": ck.get("iter")}}
    run = ROOT / "logs" / "rsl_rl" / a.experiment / f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{a.name}"
    run.mkdir(parents=True, exist_ok=True)
    torch.save(out, run / "model_0.pt")
    params = src.parent / "params"
    if params.is_dir():  # keep v1's settings next to it (joint gains are checked downstream)
        shutil.copytree(params, run / "params_v1", dirs_exist_ok=True)
    print(f"wrote {run / 'model_0.pt'}")
    print(f"RUN_DIR={run.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
