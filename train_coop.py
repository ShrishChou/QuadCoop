"""Train the two-robot (ANYmal C + Spot) pushing policies with IPPO or MAPPO.

    python train_coop.py --algo mappo --seed 0                 # warm start from the newest
    python train_coop.py --algo ippo  --seed 0                 #   Stage 1b/1c policies
    python train_coop.py --algo mappo --seed 0 --resume        # continue logs/marl/mappo_seed0

Defaults: walkers = newest logs/rsl_rl/walker_<robot> runs; actors warm-started from
the newest logs/rsl_rl/pushhard2_<robot> run if there is one, else pushhard_<robot>.
Checkpoints and tensorboard logs: logs/marl/<run-name>/ (run name: <algo>_seed<seed>
unless --run-name is given). model_0.pt = the warm-started pair before any update.
"""

from __future__ import annotations

import argparse
import os
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
os.environ.setdefault("QUADCOOP_SHAPES", "v2")


def newest_run_ckpt(exp_dir: Path) -> Path | None:
    runs = sorted(p for p in exp_dir.glob("2*") if p.is_dir() and any(p.glob("model_*.pt")))
    if not runs:
        return None
    return max(runs[-1].glob("model_*.pt"), key=lambda p: int(p.stem.split("_")[1]))


def resolve_inputs(a) -> tuple[dict, dict]:
    logs = ROOT / "logs" / "rsl_rl"
    walkers, inits = {}, {}
    for agent, robot in (("anymal", "anymal_c"), ("spot", "spot")):
        w = getattr(a, f"walker_{agent}") or newest_run_ckpt(logs / f"walker_{robot}")
        if w is None:
            raise SystemExit(f"no walker checkpoint for {robot}: pass --walker-{agent}")
        walkers[robot] = str(w)
        i = getattr(a, f"init_{agent}")
        if i is None and not a.scratch:
            i = newest_run_ckpt(logs / f"pushhard2_{robot}") or newest_run_ckpt(logs / f"pushhard_{robot}")
            if i is None:
                raise SystemExit(f"no Stage 1b/1c checkpoint for {robot}: pass --init-{agent} or --scratch")
        if i is not None:
            inits[agent] = str(i)
    return walkers, inits


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--algo", choices=("ippo", "mappo"), required=True)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--num-envs", type=int, default=4096)
    ap.add_argument("--max-iterations", type=int, default=6000)
    ap.add_argument("--run-name", default=None)
    ap.add_argument("--resume", action="store_true", help="continue the newest checkpoint of this run")
    ap.add_argument("--walker-anymal", default=None)
    ap.add_argument("--walker-spot", default=None)
    ap.add_argument("--init-anymal", default=None, help="Stage 1b/1c ANYmal checkpoint to warm-start from")
    ap.add_argument("--init-spot", default=None, help="Stage 1b/1c Spot checkpoint to warm-start from")
    ap.add_argument("--scratch", action="store_true", help="no warm start (random actors)")
    ap.add_argument("--effort-cost", type=float, default=0.0, help="lambda in r_i = r_team - lambda*effort_i*dt")
    ap.add_argument("--critic-warmup", type=int, default=100)
    ap.add_argument("--start-level", type=int, default=0)
    ap.add_argument("--video-interval", type=int, default=500, help="training video every N iterations (0 = off)")
    ap.add_argument("--video-length", type=int, default=750, help="steps per training video (50 per second)")
    ap.add_argument("--logger", choices=("wandb", "tensorboard"), default="tensorboard")
    ap.add_argument("--wandb-project", default="quadcoop")
    ap.add_argument("--device", default=None)
    a = ap.parse_args()

    import torch

    device = a.device or ("cuda:0" if torch.cuda.is_available() else "cpu")
    walkers, inits = resolve_inputs(a)
    for robot, path in walkers.items():
        os.environ[f"QUADCOOP_WALKER_CKPT_{robot.upper()}"] = path
    run = a.run_name or f"{a.algo}_seed{a.seed}"
    log_dir = ROOT / "logs" / "marl" / run
    print(f"run {run}  algo {a.algo}  seed {a.seed}  device {device}  shapes {os.environ['QUADCOOP_SHAPES']}")
    for robot, path in walkers.items():
        print(f"  walker {robot}: {path}")
    for agent, path in inits.items():
        print(f"  init   {agent}: {path}")

    random.seed(a.seed)
    torch.manual_seed(a.seed)
    import quadcoop  # noqa: F401
    from mjlab.envs import ManagerBasedRlEnv

    from quadcoop.coop.env_cfg import make_coop_env_cfg
    from quadcoop.coop.marl import MarlCfg, MarlTrainer

    env_cfg = make_coop_env_cfg()
    env_cfg.scene.num_envs = a.num_envs
    env_cfg.seed = a.seed
    env_cfg.commands["goal"].start_level = a.start_level
    env = ManagerBasedRlEnv(cfg=env_cfg, device=device)
    cfg = MarlCfg(algo=a.algo, num_envs=a.num_envs, max_iterations=a.max_iterations, seed=a.seed,
                  effort_cost=a.effort_cost, critic_warmup=a.critic_warmup, init=inits,
                  video_interval=a.video_interval, video_length=a.video_length)
    trainer = MarlTrainer(env, cfg, log_dir, device, logger=a.logger, wandb_project=a.wandb_project)
    last = MarlTrainer.newest(log_dir)
    if a.resume and last is not None:
        trainer.load(last)
    else:
        if last is not None and not a.resume:
            raise SystemExit(f"{log_dir} already has checkpoints: pass --resume, or another --run-name")
        trainer.warm_start(inits)
    trainer.learn()
    env.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
