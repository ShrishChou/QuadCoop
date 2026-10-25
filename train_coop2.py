"""Train ANYmal C + Spot to push one Stage 2 object together, with IPPO or MAPPO (Stages 3-4).

    python train_coop2.py --algo mappo --seed 0                  # new run logs/marl2/mappo_s0
    python train_coop2.py --algo ippo  --seed 0
    python train_coop2.py --algo mappo --seed 0 --resume         # continue it
    python train_coop2.py --algo mappo --check                   # build, warm start, a few steps, exit

The models come from evals/models.yaml (the roles walker_anymal, walker_spot, push2b_anymal,
push2b_spot; push2ctrl_* for --variant ctrl), resolved through evals/registry.yaml: each robot's
walker checkpoint and the env vars it was trained with (Spot's joint gains and history length),
and each robot's Stage 2 policy, whose registered walker must be the same one. What was used is
written to logs/marl2/<run>/inputs.yaml and into every checkpoint.
Checkpoints: logs/marl2/<run>/model_<iter>.pt; model_0.pt = the warm-started pair before any
update (the frozen-pair baseline).
"""

from __future__ import annotations

import argparse
import os
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
ROBOT_OF = {"anymal": "anymal_c", "spot": "spot"}


def resolve_models(variant: str) -> dict:
    """The four models from evals/models.yaml + everything needed to rebuild their envs."""
    import yaml

    from methods import EVALS, load, resolve

    sel = yaml.safe_load((EVALS / "models.yaml").read_text()) or {}
    reg = load()
    out = {"selection": {}, "walker_ckpt": {}, "walker_env": {}, "policy": {}}
    for a, robot in ROBOT_OF.items():
        w_role, p_role = f"walker_{a}", f"push2{variant}_{a}"
        if w_role not in sel or p_role not in sel:
            raise SystemExit(f"evals/models.yaml needs {w_role} and {p_role} "
                             f"(python scripts/select_models.py --set {p_role}=<id>)")
        w, p = resolve(sel[w_role], reg), resolve(sel[p_role], reg)
        if reg[sel[p_role]].get("walker") != sel[w_role]:
            raise SystemExit(f"{sel[p_role]} was trained on walker {reg[sel[p_role]].get('walker')}, but "
                             f"evals/models.yaml has {w_role}: {sel[w_role]}")
        for path in (w["checkpoint_abs"], p["checkpoint_abs"]):
            if not Path(path).exists():
                raise SystemExit(f"{path} not found (registered models live in logs/evals/<id>/)")
        out["selection"][w_role], out["selection"][p_role] = sel[w_role], sel[p_role]
        out["walker_ckpt"][robot] = w["checkpoint_abs"]
        out["walker_env"][robot] = dict(w["env_all"])
        out["policy"][a] = p["checkpoint_abs"]
    return out


def set_env(models: dict) -> None:
    """Env vars the two-robot env reads at import / build time."""
    os.environ["QUADCOOP_SHAPES"] = "v2"
    for k in ("QUADCOOP_WALKER_CKPT", "QUADCOOP_WALKER_HISTORY", "QUADCOOP_PUSH_FORCE", "QUADCOOP_SUCCESS_MODE"):
        os.environ.pop(k, None)
    for robot, path in models["walker_ckpt"].items():
        os.environ[f"QUADCOOP_WALKER_CKPT_{robot.upper()}"] = path
        env = models["walker_env"][robot]
        os.environ[f"QUADCOOP_WALKER_HISTORY_{robot.upper()}"] = str(env.get("QUADCOOP_WALKER_HISTORY", "0"))
        if robot == "spot":
            os.environ["QUADCOOP_SPOT_PROFILE"] = env.get("QUADCOOP_SPOT_PROFILE", "v1")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--algo", choices=("ippo", "mappo"), required=True)
    ap.add_argument("--variant", choices=("b", "ctrl"), default="b")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--num-envs", type=int, default=4096)
    ap.add_argument("--max-iterations", type=int, default=6000, help="total (a resumed run stops here too)")
    ap.add_argument("--run-name", default=None, help="default <algo>[_ctrl]_s<seed>")
    ap.add_argument("--resume", action="store_true", help="continue the newest checkpoint of this run")
    ap.add_argument("--critic-warmup", type=int, default=100)
    ap.add_argument("--partner-map", action="store_true", help="partner footprint as a 2nd map channel")
    ap.add_argument("--reward", choices=("r3", "r4"), default="r3",
                    help="r4: no per-robot behind-the-object term, exponential proximity penalty below 0.6 m")
    ap.add_argument("--entropy-coef", type=float, default=0.0)
    ap.add_argument("--max-std-factor", type=float, default=1.0,
                    help="action noise may not rise above this x its warm-start value")
    ap.add_argument("--start-level", type=int, default=0)
    ap.add_argument("--video-interval", type=int, default=500, help="training video every N iterations (0 = off)")
    ap.add_argument("--video-length", type=int, default=1000, help="steps per training video (50 per second)")
    ap.add_argument("--logger", choices=("wandb", "tensorboard"), default="tensorboard")
    ap.add_argument("--wandb-project", default="quadcoop")
    ap.add_argument("--device", default=None)
    ap.add_argument("--check", action="store_true", help="build, warm start, run 2 iterations, exit")
    a = ap.parse_args()

    models = resolve_models(a.variant)
    set_env(models)
    import torch
    import yaml

    device = a.device or ("cuda:0" if torch.cuda.is_available() else "cpu")
    run = a.run_name or f"{a.algo}{'_ctrl' if a.variant == 'ctrl' else ''}_s{a.seed}"
    log_dir = ROOT / "logs" / "marl2" / (run + ("_check" if a.check else ""))
    print(f"run {run}  algo {a.algo}  variant {a.variant}  seed {a.seed}  device {device}  "
          f"partner map {a.partner_map}  rewards {a.reward}")
    for k, v in models["selection"].items():
        print(f"  {k:15s} {v}")

    random.seed(a.seed)
    torch.manual_seed(a.seed)
    import quadcoop  # noqa: F401
    from mjlab.envs import ManagerBasedRlEnv

    from quadcoop.coop2.env_cfg import make_coop2_env_cfg
    from quadcoop.coop2.marl import MarlCfg, MarlTrainer

    env_cfg = make_coop2_env_cfg(a.variant, partner_map=a.partner_map, reward_set=a.reward)
    env_cfg.scene.num_envs = a.num_envs
    env_cfg.seed = a.seed
    env_cfg.commands["goal"].start_level = a.start_level
    env = ManagerBasedRlEnv(cfg=env_cfg, device=device)
    cfg = MarlCfg(algo=a.algo, variant=a.variant, num_envs=a.num_envs, seed=a.seed,
                  max_iterations=2 if a.check else a.max_iterations,
                  critic_warmup=1 if a.check else a.critic_warmup, init=dict(models["policy"]),
                  entropy_coef=a.entropy_coef, max_std_factor=a.max_std_factor,
                  partner_map=a.partner_map, reward_set=a.reward,
                  video_interval=0 if a.check else a.video_interval, video_length=a.video_length,
                  inputs=models["selection"])
    trainer = MarlTrainer(env, cfg, log_dir, device, logger="tensorboard" if a.check else a.logger,
                          wandb_project=a.wandb_project)
    last = MarlTrainer.newest(log_dir)
    if a.resume and last is not None:
        trainer.load(last)
    else:
        if last is not None and not a.check:
            raise SystemExit(f"{log_dir} already has checkpoints: pass --resume, or another --run-name")
        trainer.warm_start(models["policy"])
    (log_dir / "inputs.yaml").write_text(yaml.safe_dump({"run": run, "algo": a.algo, "variant": a.variant,
                                                         "partner_map": a.partner_map, "reward_set": a.reward,
                                                         "seed": a.seed, **models}, sort_keys=False, width=120))
    print(f"[marl2] reward terms: team {[trainer.term_names[i] for i in trainer.team_idx]}")
    for ag, ix in trainer.own_idx.items():
        print(f"[marl2]               {ag} {[trainer.term_names[i] for i in ix]}")
    if trainer.it >= cfg.max_iterations:
        print(f"{log_dir} is already at iteration {trainer.it} (target {cfg.max_iterations})")
        return 0
    trainer.learn()
    env.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
