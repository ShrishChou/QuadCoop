"""Train ANYmal C + Spot to push one Stage 2 object together, with IPPO or MAPPO (Stages 3-4).

    python train_coop2.py --algo mappo --seed 0                  # new run logs/marl2/mappo_s0
    python train_coop2.py --algo ippo  --seed 0
    python train_coop2.py --algo mappo --seed 0 --resume         # continue it
    python train_coop2.py --algo mappo --check                   # build, warm start, a few steps, exit
    python train_coop2.py --algo mappo --partner-map --reward r5 --mean-clip 1.1 --bound-coef 0.01 \
        --entropy-coef 0.003 --run-name mappo_r6_s0                # r6: r5 + exploration fixes
    python train_coop2.py --algo mappo --scratch --partner-map --reward r5 --mean-clip 1.1 \
        --bound-coef 0.01 --entropy-coef 0.003 --run-name mappo_scratch_s0   # from the walkers only
    python train_coop2.py --algo mappo --pair anymal --partner-map --reward r7 ...   # two ANYmal C
    python train_coop2.py --algo mappo --pair anymal --partner-map --reward r7 --kl-ref 0.05 \
        --critic-warmup 500 --max-actor-lr 1e-4 --run-name mappo_aa_kl_s0   # anchored to Stage 2b

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


def _pairs():
    """quadcoop/coop2/pairs.py, loaded as a plain file (importing the quadcoop package would read
    robot settings from the environment before set_env has set them)."""
    import importlib.util

    spec = importlib.util.spec_from_file_location("_qc_pairs", ROOT / "src" / "quadcoop" / "coop2" / "pairs.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def robot_of(pair: str | None = None) -> dict[str, str]:
    """slot -> robot type ("anymal_c" / "spot") for the pair (default: QUADCOOP_PAIR or mixed)."""
    return dict(_pairs().slots(pair))


ROBOT_OF = robot_of("mixed")  # the default pair (older callers)


def resolve_models(variant: str, pair: str = "mixed") -> dict:
    """The models from evals/models.yaml (a walker and a Stage 2 policy per robot type in the
    pair) + everything needed to rebuild their envs. policy is keyed by slot, walker_* by robot
    type."""
    import yaml

    from methods import EVALS, load, resolve

    role_of = _pairs().ROLE
    sel = yaml.safe_load((EVALS / "models.yaml").read_text()) or {}
    reg = load()
    out = {"selection": {}, "walker_ckpt": {}, "walker_env": {}, "policy": {}, "pair": pair}
    for a, robot in robot_of(pair).items():
        role = role_of[robot]
        w_role, p_role = f"walker_{role}", f"push2{variant}_{role}"
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
    os.environ["QUADCOOP_PAIR"] = models.get("pair", "mixed")
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
    ap.add_argument("--pair", choices=("mixed", "anymal", "spot"), default="mixed",
                    help="which two robots: ANYmal C + Spot (mixed), two ANYmal C, two Spot "
                         "(quadcoop/coop2/pairs.py); both start from that type's Stage 2 policy")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--num-envs", type=int, default=4096)
    ap.add_argument("--max-iterations", type=int, default=6000, help="total (a resumed run stops here too)")
    ap.add_argument("--run-name", default=None, help="default <algo>[_ctrl]_s<seed>")
    ap.add_argument("--resume", action="store_true", help="continue the newest checkpoint of this run")
    ap.add_argument("--critic-warmup", type=int, default=None, help="default 100 (warm start), 0 (--scratch)")
    ap.add_argument("--scratch", action="store_true",
                    help="no Stage 2 warm start: random actors and critics on the frozen walkers")
    ap.add_argument("--kl-ref", type=float, default=0.0,
                    help="beta: penalty beta * KL(policy || its frozen Stage 2b policy) in the actor loss "
                         "(KL-regularized fine-tuning; 0 = off; not with --scratch)")
    ap.add_argument("--kl-partner-scale", type=float, default=1.0,
                    help="< 1: the KL anchor is multiplied by this while the partner is within 1.5 m, back to "
                         "full beyond 3 m (partner-aware anchor: stay 2b alone, free to change together)")
    ap.add_argument("--start-around", action="store_true",
                    help="robots start anywhere around the object (>= 60 deg apart) instead of behind it")
    ap.add_argument("--need-frac", type=float, default=0.0,
                    help="share of training episodes with a wide object (long, arch, dumbbell, T) above "
                         "--need-mass kg, i.e. one robot alone cannot do it (evaluations unchanged)")
    ap.add_argument("--need-mass", type=float, default=45.0)
    ap.add_argument("--actor-lr", type=float, default=None,
                    help="starting actor learning rate (adapted to the KL target); default 1e-4, 3e-4 with --scratch")
    ap.add_argument("--max-actor-lr", type=float, default=None,
                    help="cap on the adapted actor learning rate; default 3e-4, 1e-3 with --scratch")
    ap.add_argument("--partner-map", action="store_true", help="partner footprint as a 2nd map channel")
    ap.add_argument("--reward", choices=("r3", "r4", "r5", "r7", "r8"), default="r3",
                    help="r4: no per-robot behind-the-object term, exponential proximity penalty below 0.6 m; "
                         "r5: r4 + approach reward only for getting closer, team time cost, stronger "
                         "push_along and yaw_progress; r7: outcome-based: goal-error cost per second, "
                         "failure pays the time left, push_credit, proximity on the body gap; "
                         "r8: r7 with work_credit (contact force x object speed) and touch-only penalty "
                         "(quadcoop/coop2/env_cfg.py)")
    ap.add_argument("--entropy-coef", type=float, default=0.0)
    ap.add_argument("--max-std-factor", type=float, default=1.0,
                    help="action noise may not rise above this x its warm-start value")
    ap.add_argument("--mean-clip", type=float, default=0.0,
                    help="> 0: sample actions around the policy mean clamped to +-this, gradient passed "
                         "straight through, so noise acts on saturated outputs (r6: 1.1; 0 = off)")
    ap.add_argument("--bound-coef", type=float, default=0.0,
                    help="penalty on the raw policy mean past +-mean-clip (r6: 0.01; 0 = off)")
    ap.add_argument("--start-level", type=int, default=0)
    ap.add_argument("--video-interval", type=int, default=500, help="training video every N iterations (0 = off)")
    ap.add_argument("--video-length", type=int, default=1000, help="steps per training video (50 per second)")
    ap.add_argument("--logger", choices=("wandb", "tensorboard"), default="tensorboard")
    ap.add_argument("--wandb-project", default="quadcoop")
    ap.add_argument("--device", default=None)
    ap.add_argument("--check", action="store_true", help="build, warm start, run 2 iterations, exit")
    a = ap.parse_args()

    if a.kl_ref > 0 and a.scratch:
        raise SystemExit("--kl-ref anchors to the Stage 2 policies: it does not apply with --scratch")
    if a.critic_warmup is None:
        a.critic_warmup = 0 if a.scratch else 100
    if a.actor_lr is None:
        a.actor_lr = 3e-4 if a.scratch else 1e-4
    if a.max_actor_lr is None:
        a.max_actor_lr = 1e-3 if a.scratch else 3e-4
    models = resolve_models(a.variant, a.pair)
    set_env(models)
    import torch
    import yaml

    device = a.device or ("cuda:0" if torch.cuda.is_available() else "cpu")
    run = a.run_name or f"{a.algo}{'_ctrl' if a.variant == 'ctrl' else ''}_s{a.seed}"
    log_dir = ROOT / "logs" / "marl2" / (run + ("_check" if a.check else ""))
    print(f"run {run}  algo {a.algo}  pair {a.pair}  variant {a.variant}  seed {a.seed}  device {device}  "
          f"partner map {a.partner_map}  rewards {a.reward}  entropy {a.entropy_coef:g}  mean clip {a.mean_clip:g}  "
          f"bound {a.bound_coef:g}  kl_ref {a.kl_ref:g} (partner scale {a.kl_partner_scale:g})  "
          f"start {'around' if a.start_around else 'behind'}  need_frac {a.need_frac:g}  "
          f"{'FROM SCRATCH' if a.scratch else 'warm start from Stage 2b'}")
    for k, v in models["selection"].items():
        print(f"  {k:15s} {v}")

    random.seed(a.seed)
    torch.manual_seed(a.seed)
    import quadcoop  # noqa: F401
    from mjlab.envs import ManagerBasedRlEnv

    from quadcoop.coop2.env_cfg import make_coop2_env_cfg
    from quadcoop.coop2.marl import MarlCfg, MarlTrainer

    env_cfg = make_coop2_env_cfg(a.variant, partner_map=a.partner_map, reward_set=a.reward,
                                 start_mode="around" if a.start_around else "behind",
                                 need_frac=a.need_frac, need_mass=a.need_mass)
    env_cfg.scene.num_envs = a.num_envs
    env_cfg.seed = a.seed
    env_cfg.commands["goal"].start_level = a.start_level
    env = ManagerBasedRlEnv(cfg=env_cfg, device=device)
    cfg = MarlCfg(algo=a.algo, variant=a.variant, num_envs=a.num_envs, seed=a.seed,
                  max_iterations=2 if a.check else a.max_iterations,
                  critic_warmup=1 if a.check else a.critic_warmup, init={} if a.scratch else dict(models["policy"]),
                  scratch=a.scratch, actor_learning_rate=a.actor_lr, max_actor_learning_rate=a.max_actor_lr,
                  entropy_coef=a.entropy_coef, max_std_factor=a.max_std_factor,
                  mean_clip=a.mean_clip, bound_coef=a.bound_coef, kl_ref=a.kl_ref,
                  kl_partner_scale=a.kl_partner_scale, start_mode="around" if a.start_around else "behind",
                  need_frac=a.need_frac,
                  partner_map=a.partner_map, reward_set=a.reward, pair=a.pair,
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
        if a.scratch:
            trainer.init_scratch()
        else:
            trainer.warm_start(models["policy"])
    if a.kl_ref > 0:
        trainer.build_refs(models["policy"])
    (log_dir / "inputs.yaml").write_text(yaml.safe_dump({"run": run, "algo": a.algo, "variant": a.variant,
                                                         "partner_map": a.partner_map, "reward_set": a.reward,
                                                         "scratch": a.scratch,
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
