"""Torso interface compatibility: an older Spot-arm pair checkpoint, expanded for the 2 torso outputs and 4 torso
inputs, acts exactly as before (docs/spot_arm_pair.md, "Torso interface").

    python scripts/spot_arm/torso_compat_check.py --checkpoint logs/marl2/sa_heavy_learned_s0/model_4000.pt

In an env built with the torso interface, for --steps steps of the expanded policy acting:
  1. the expanded actor's first outputs equal the original actor's on the same observations without the torso
     inputs (largest difference at rounding level, <= 1e-5), and its torso outputs are exactly 0;
  2. the applied torso command stays RAI's default (0, 0, 0.52) exactly.
Behaviour (whole episodes) is compared separately: scripts/spot_arm/pair_eval.py with and without --torso-interface
on the same tasks, against the rerun spread of two runs without it. Exit 0 = pass.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--checkpoint", required=True)
    ap.add_argument("--envs", type=int, default=32)
    ap.add_argument("--steps", type=int, default=300)
    a = ap.parse_args()
    import torch
    from train_coop2 import resolve_models, set_env

    ck = torch.load(a.checkpoint, map_location="cpu", weights_only=False)
    rc = ck.get("cfg", {})
    set_env(resolve_models(ck.get("variant", "b"), rc.get("pair", "spot_arm")))
    from tensordict import TensorDict

    import quadcoop  # noqa: F401
    from mjlab.envs import ManagerBasedRlEnv

    from quadcoop.coop2.env_cfg import ARM, make_coop2_env_cfg
    from quadcoop.coop2.marl import PairPolicy, action_slices, actor_groups, actor_state, make_model
    from quadcoop.coop2.mdp import AGENTS

    v = ck.get("variant", "b")
    cfg = make_coop2_env_cfg(v, play=True, partner_map=bool(rc.get("partner_map")), reward_set=rc.get("reward_set", "r7"),
                             arm=rc.get("arm") or "stowed", pilot_level=tuple(rc.get("pilot_level") or ()),
                             dyaw_choices=bool(rc.get("dyaw_choices")), hand_obs=bool(rc.get("hand_obs")), torso=True)
    cfg.scene.num_envs = a.envs
    if rc.get("pilot_level"):  # as pair_eval.py: the one pilot level is level 0
        cfg.commands["goal"].start_level = 0
    dev = "cuda:0" if torch.cuda.is_available() else "cpu"
    env = ManagerBasedRlEnv(cfg=cfg, device=dev)
    td = lambda o: TensorDict({k: x for k, x in o.items() if not k.startswith("walker_")}, batch_size=[a.envs])  # noqa: E731
    obs = td(env.reset()[0])
    sl = action_slices(env)
    new = PairPolicy(obs, dev, v, checkpoint=a.checkpoint, act_dims={ag: s.stop - s.start for ag, s in sl.items()})
    old_dims = ck["act_dims"]
    strip = {ag: 4 if ARM[ag] else 0 for ag in AGENTS}

    def old_obs(o):
        d = {k: x for k, x in o.items()}
        for ag in AGENTS:
            if strip[ag]:
                d[f"actor_{ag}"] = d[f"actor_{ag}"][:, :-strip[ag]]
        return TensorDict(d, batch_size=[a.envs])

    olds = {}
    for ag in AGENTS:
        m = make_model(old_obs(obs), actor_groups(ag, v), int(old_dims[ag]), (256, 128, 64), v, True).to(dev)
        m.load_state_dict(actor_state(ck["actors"], ag))
        olds[ag] = m.eval()
    terms = {ag: env.action_manager.get_term(f"walker_{ag}") for ag in AGENTS}
    worst, worst_new, worst_torso = 0.0, 0.0, 0.0
    default = torch.tensor([0.0, 0.0, 0.52], device=dev)
    with torch.no_grad():
        for _ in range(a.steps):
            oo = old_obs(obs)
            acts = []
            for ag in AGENTS:
                an = new.actors[ag](obs)
                ao = olds[ag](oo)
                k = int(old_dims[ag])
                worst = max(worst, float((an[:, :k] - ao).abs().max()))
                if an.shape[-1] > k:
                    worst_new = max(worst_new, float(an[:, k:].abs().max()))
                acts.append(an)
            obs = td(env.step(torch.cat(acts, -1))[0])
            for ag in AGENTS:
                if ARM[ag]:
                    worst_torso = max(worst_torso, float((terms[ag].torso - default).abs().max()))
    # zero-weight columns can change the float summation order of the first layer: allow rounding (1e-5)
    ok = worst <= 1e-5 and worst_new == 0.0 and worst_torso == 0.0 and bool(new.expanded)
    print(f"expanded actors: {new.expanded}; over {a.steps} steps x {a.envs} envs: old outputs, largest difference "
          f"{worst:.3g}; torso outputs, largest |value| {worst_new:.3g}; applied torso vs default, largest difference "
          f"{worst_torso:.3g} -> {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
