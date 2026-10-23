"""How saturated is a high-level pushing policy? Raw output statistics for any checkpoint.

The walker clips each command (vx, vy, yaw rate) to [-1, 1]. This runs the policy
deterministically for --steps steps in --envs environments of the task (play settings)
and prints, per command: mean |raw output|, the 50/90/99th percentiles of |raw output|,
and the share of outputs past the clip. Use it to decide whether a checkpoint is a sound
warm start (outputs mostly inside [-1, 1]) or a saturated one.

    QUADCOOP_WALKER_CKPT=<walker.pt> python scripts/action_stats.py \\
        --task QuadCoop-PushHard2-AnymalC --checkpoint logs/rsl_rl/pushhard2_anymal_c/<run>/model_N.pt
"""

from __future__ import annotations

import argparse
import os
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import torch  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--task", required=True)
    ap.add_argument("--checkpoint", required=True)
    ap.add_argument("--envs", type=int, default=256)
    ap.add_argument("--steps", type=int, default=1000)
    ap.add_argument("--device", default=None)
    a = ap.parse_args()
    device = a.device or ("cuda:0" if torch.cuda.is_available() else "cpu")
    if "Push2" in a.task or "PushHard2" in a.task:
        os.environ.setdefault("QUADCOOP_SHAPES", "v2")

    import quadcoop  # noqa: F401
    import quadcoop.stage1  # noqa: F401
    import quadcoop.stage1b  # noqa: F401
    import quadcoop.stage1c  # noqa: F401
    import quadcoop.stage2  # noqa: F401
    from mjlab.envs import ManagerBasedRlEnv
    from mjlab.rl import MjlabOnPolicyRunner, RslRlVecEnvWrapper
    from mjlab.tasks.registry import load_env_cfg, load_rl_cfg

    cfg = load_env_cfg(a.task, play=True)
    cfg.scene.num_envs = a.envs
    env = RslRlVecEnvWrapper(ManagerBasedRlEnv(cfg=cfg, device=device))
    runner = MjlabOnPolicyRunner(env, asdict(load_rl_cfg(a.task)), device=device)
    runner.load(a.checkpoint, load_cfg={"actor": True}, strict=True, map_location=device)
    policy = runner.get_inference_policy(device=device)
    obs = env.get_observations()
    outs = []
    with torch.no_grad():
        for _ in range(a.steps):
            act = policy(obs)
            outs.append(act.abs().cpu())
            obs, *_ = env.step(act)
    x = torch.cat(outs)  # (steps * envs, 3)
    q = torch.quantile(x[torch.randperm(len(x))[:200000]], torch.tensor([0.5, 0.9, 0.99]), dim=0)
    print(f"\n{a.checkpoint}\n{'':10s}{'vx':>10s}{'vy':>10s}{'yaw':>10s}")
    print(f"{'mean |a|':10s}" + "".join(f"{v:10.2f}" for v in x.mean(0)))
    for i, p in enumerate((50, 90, 99)):
        print(f"{f'p{p} |a|':10s}" + "".join(f"{v:10.2f}" for v in q[i]))
    print(f"{'past clip':10s}" + "".join(f"{v:10.1%}" for v in (x > 1).float().mean(0)))
    env.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
