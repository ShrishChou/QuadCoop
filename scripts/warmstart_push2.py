"""Turn a Stage 1b push checkpoint into a Stage 2 starting checkpoint.

The Stage 2 actor's MLP takes [Stage 1b's 42 normalized inputs, top-image features,
front-image features] (critic: 45 + features). This copies Stage 1b's weights for the
first 42 (45) inputs and every deeper layer, sets the weights from the image features to
zero, and keeps the convolutional encoders at their random initialization. The result
acts exactly like the Stage 1b policy until training gives the images weight
(checked here on real observations). The action noise is reset to --std (default 0.5)
so the policy explores again; the optimizer starts fresh.

For the control ("ctrl", no images) the networks are identical and are copied as they are.

    QUADCOOP_WALKER_CKPT=<walker.pt> python scripts/warmstart_push2.py \\
        --task QuadCoop-Push2a-AnymalC --init logs/rsl_rl/pushhard_anymal_c/<run>/model_N.pt
writes logs/rsl_rl/push2a_anymal_c/0000_warmstart/model_0.pt
"""

from __future__ import annotations

import argparse
import os
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
os.environ.setdefault("QUADCOOP_SHAPES", "v2")

import torch  # noqa: E402


def transplant(new_sd: dict, old_sd: dict, n_old: int) -> tuple[dict, list[str]]:
    out = {k: v.clone() for k, v in new_sd.items()}
    w_new, w_old = out["mlp.0.weight"], old_sd["mlp.0.weight"]
    assert w_old.shape[1] == n_old, f"old first layer has {w_old.shape[1]} inputs, expected {n_old}"
    assert w_new.shape[0] == w_old.shape[0], "hidden sizes differ"
    w_new.zero_()
    w_new[:, :n_old] = w_old
    for key in ("obs_normalizer._mean", "obs_normalizer._var", "obs_normalizer._std"):
        assert out[key].shape[-1] == n_old, f"{key}: new normalizer covers {out[key].shape[-1]} inputs"
        out[key] = old_sd[key].clone()
    out["obs_normalizer.count"] = old_sd["obs_normalizer.count"].clone()
    copied = []
    for key, val in old_sd.items():
        if key == "mlp.0.weight" or key.startswith("obs_normalizer."):
            continue
        if key in out and out[key].shape == val.shape:
            out[key] = val.clone()
            copied.append(key)
    return out, copied


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True)
    ap.add_argument("--init", required=True, help="Stage 1b checkpoint (model_N.pt, 42-input actor)")
    ap.add_argument("--out", default=None)
    ap.add_argument("--std", type=float, default=0.5, help="action noise to restart from")
    ap.add_argument("--device", default="cpu")
    a = ap.parse_args()

    import quadcoop  # noqa: F401
    import quadcoop.stage1  # noqa: F401
    import quadcoop.stage1b  # noqa: F401
    import quadcoop.stage2  # noqa: F401
    from mjlab.envs import ManagerBasedRlEnv
    from mjlab.rl import MjlabOnPolicyRunner, RslRlVecEnvWrapper
    from mjlab.tasks.registry import load_env_cfg, load_rl_cfg

    cfg = load_env_cfg(a.task)
    cfg.scene.num_envs = 4
    env = ManagerBasedRlEnv(cfg=cfg, device=a.device)
    wrapped = RslRlVecEnvWrapper(env)
    rl = load_rl_cfg(a.task)
    runner = MjlabOnPolicyRunner(wrapped, asdict(rl), device=a.device)
    saved = runner.alg.save()
    old = torch.load(a.init, map_location=a.device, weights_only=False)
    saved["actor_state_dict"], copied_a = transplant(saved["actor_state_dict"], old["actor_state_dict"], 42)
    saved["critic_state_dict"], copied_c = transplant(saved["critic_state_dict"], old["critic_state_dict"], 45)
    if "distribution.std_param" in saved["actor_state_dict"]:
        saved["actor_state_dict"]["distribution.std_param"].fill_(a.std)
    saved["iter"] = 0
    saved["infos"] = {"env_state": {"common_step_counter": 0}, "warmstart_from": a.init}
    print(f"actor: copied {len(copied_a)} tensors; critic: copied {len(copied_c)} tensors")

    # -- check: on real observations the new actor's mean action equals the old one's ------
    runner.alg.load(saved, load_cfg={"actor": True, "critic": True}, strict=True)
    from rsl_rl.models.mlp_model import MLPModel
    from tensordict import TensorDict

    obs = wrapped.get_observations()
    for _ in range(5):
        obs, *_ = wrapped.step(torch.randn(4, 3, device=a.device) * 0.3)
    old_actor = MLPModel(TensorDict({"actor": obs["actor"]}, batch_size=[4]), {"p": ["actor"]}, "p", 3,
                         tuple(rl.actor.hidden_dims), rl.actor.activation, obs_normalization=True,
                         distribution_cfg={"class_name": "GaussianDistribution", "init_std": 0.5, "std_type": "scalar"})
    old_actor.load_state_dict(old["actor_state_dict"])
    old_actor.to(a.device)
    old_actor.eval()
    policy = runner.alg.get_policy()
    policy.eval()
    with torch.no_grad():
        diff = float((policy(obs) - old_actor(TensorDict({"actor": obs["actor"]}, batch_size=[4]))).abs().max())
    print(f"max |new - old| mean action on real observations: {diff:.2e}")
    assert diff < 1e-5, "warm start does not reproduce the Stage 1b policy"

    exp = rl.experiment_name
    out = Path(a.out) if a.out else ROOT / "logs" / "rsl_rl" / exp / "0000_warmstart" / "model_0.pt"
    out.parent.mkdir(parents=True, exist_ok=True)
    torch.save(saved, out)
    print(f"wrote {out}")
    env.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
