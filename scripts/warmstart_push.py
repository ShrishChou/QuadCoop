"""Turn a Stage 1 push checkpoint into a Stage 1b starting checkpoint.

Stage 1b's observation adds terms (object descriptor, hold progress) and drops one
(Stage 1's 2-shape one-hot). This copies every weight it can, term by term:

* first-layer columns of observation terms with the same name and size are copied,
  columns of new terms start at zero -> the new policy initially acts exactly like
  the old one, and learns to use the new inputs;
* the observation normalizer is copied for those terms (new ones start at mean 0, std 1);
* all deeper layers and the action noise are copied as they are.

Same for the critic. The result is a full checkpoint (with a fresh optimizer) that
train_push_hard.py resumes from.

    QUADCOOP_WALKER_CKPT=<walker.pt> python scripts/warmstart_push.py \\
        --task QuadCoop-PushHard-AnymalC --init logs/rsl_rl/push_anymal_c/<run>/model_4999.pt
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import torch  # noqa: E402

TASK_DIR = {"QuadCoop-PushHard-AnymalC": "pushhard_anymal_c", "QuadCoop-PushHard-Spot": "pushhard_spot"}


def layout(env, group: str) -> list[tuple[str, int]]:
    om = env.observation_manager
    return [(n, int(torch.tensor(d).prod())) for n, d in
            zip(om.active_terms[group], om.group_obs_term_dim[group], strict=True)]


def column_map(old: list[tuple[str, int]], new: list[tuple[str, int]]):
    """[(new_slice, old_slice)] for terms present in both with the same size."""
    def offsets(lay):
        out, i = {}, 0
        for n, d in lay:
            out[n] = (i, i + d)
            i += d
        return out, i
    o, n_old = offsets(old)
    n, n_new = offsets(new)
    pairs, kept, fresh = [], [], []
    for name, (a, b) in n.items():
        if name in o and (o[name][1] - o[name][0]) == (b - a):
            pairs.append((slice(a, b), slice(*o[name])))
            kept.append(name)
        else:
            fresh.append(name)
    return pairs, n_old, n_new, kept, fresh


def transplant(new_sd: dict, old_sd: dict, pairs) -> dict:
    out = {k: v.clone() for k, v in new_sd.items()}
    w_new = out["mlp.0.weight"]
    w_new.zero_()
    for ns, os_ in pairs:
        w_new[:, ns] = old_sd["mlp.0.weight"][:, os_]
        for key in ("obs_normalizer._mean", "obs_normalizer._var", "obs_normalizer._std"):
            out[key][:, ns] = old_sd[key][:, os_]
    for key, val in old_sd.items():
        if key == "mlp.0.weight" or key.startswith("obs_normalizer._"):
            continue
        if key in out and out[key].shape == val.shape:
            out[key] = val.clone()
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True, choices=list(TASK_DIR))
    ap.add_argument("--init", required=True, help="Stage 1 push checkpoint (model_N.pt)")
    ap.add_argument("--out", default=None)
    ap.add_argument("--min-std", type=float, default=0.3, help="floor on the action noise")
    ap.add_argument("--device", default="cpu")
    a = ap.parse_args()

    import quadcoop  # noqa: F401
    import quadcoop.stage1  # noqa: F401
    import quadcoop.stage1b  # noqa: F401
    from mjlab.envs import ManagerBasedRlEnv
    from mjlab.rl import MjlabOnPolicyRunner, RslRlVecEnvWrapper
    from mjlab.tasks.registry import load_env_cfg, load_rl_cfg

    old_task = a.task.replace("PushHard", "Push")

    def build(task):
        cfg = load_env_cfg(task)
        cfg.scene.num_envs = 2
        return ManagerBasedRlEnv(cfg=cfg, device=a.device)

    old_env = build(old_task)
    old_lay = {g: layout(old_env, g) for g in ("actor", "critic")}
    old_env.close()
    del old_env

    new_env = build(a.task)
    new_lay = {g: layout(new_env, g) for g in ("actor", "critic")}
    runner = MjlabOnPolicyRunner(RslRlVecEnvWrapper(new_env), asdict(load_rl_cfg(a.task)), device=a.device)
    saved = runner.alg.save()  # fresh state of the new networks + optimizer

    old = torch.load(a.init, map_location=a.device, weights_only=False)
    for part, group in (("actor_state_dict", "actor"), ("critic_state_dict", "critic")):
        pairs, n_old, n_new, kept, fresh = column_map(old_lay[group], new_lay[group])
        w_old = old[part]["mlp.0.weight"].shape[1]
        assert w_old == n_old, f"{part}: checkpoint has {w_old} inputs, Stage 1 layout says {n_old}"
        saved[part] = transplant(saved[part], old[part], pairs)
        print(f"{group}: {n_old} -> {n_new} inputs; copied {kept}; new (zero) {fresh}")
    std_key = "distribution.std_param"
    if std_key in saved["actor_state_dict"]:
        saved["actor_state_dict"][std_key] = saved["actor_state_dict"][std_key].clamp(min=a.min_std)
    saved["iter"] = 0
    saved["infos"] = {"env_state": {"common_step_counter": 0}, "warmstart_from": a.init}

    out = Path(a.out) if a.out else ROOT / "logs" / "rsl_rl" / TASK_DIR[a.task] / "0000_warmstart" / "model_0.pt"
    out.parent.mkdir(parents=True, exist_ok=True)
    torch.save(saved, out)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())