"""Three-robot wiring check (QUADCOOP_PAIR=anymal3): actions, teammate inputs, contact sensors, terminations.

    python scripts/three_wiring.py

1. Each robot in turn gets "forward" (action 1 on vx) for 2 s while the others get 0: only that robot may travel.
2. The partner inputs (9 numbers) of every robot equal those of its nearest teammate, recomputed from the sim.
3. One robot-robot contact sensor per pair; one fall termination per robot; one walker action term per robot.
Exit status 0 = all pass.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))
os.environ["QUADCOOP_PAIR"] = "anymal3"


def main() -> int:
    from train_coop2 import resolve_models, set_env
    set_env(resolve_models("b", "anymal3"))
    import torch

    import quadcoop  # noqa: F401
    from mjlab.envs import ManagerBasedRlEnv

    from quadcoop.coop2 import mdp as cm
    from quadcoop.coop2.env_cfg import make_coop2_env_cfg
    from quadcoop.coop2.marl import action_slices
    from quadcoop.coop2.pairs import AGENTS, OTHERS

    assert len(AGENTS) == 3, AGENTS
    cfg = make_coop2_env_cfg("b", play=True, partner_map=True, reward_set="r7")
    cfg.scene.num_envs = 16
    cfg.episode_length_s = 1e5
    cfg.terminations = {k: v for k, v in cfg.terminations.items() if k.endswith("_fell")} | {}
    dev = "cuda:0" if torch.cuda.is_available() else "cpu"
    env = ManagerBasedRlEnv(cfg, device=dev)
    env.reset()
    sl = action_slices(env)
    ok = True
    print("action slices:", {a: (s.start, s.stop) for a, s in sl.items()})
    n_act = env.action_manager.total_action_dim

    def travel(act):
        start = {b: env.scene[b].data.root_link_pos_w[:, :2].clone() for b in AGENTS}
        for _ in range(100):
            env.step(act)
        out = {b: float(torch.linalg.norm(env.scene[b].data.root_link_pos_w[:, :2] - start[b], dim=-1).mean())
               for b in AGENTS}
        env.reset()
        return out
    # baseline: every robot at action 0 (the walker's command for 0 is not exactly "stand": it creeps)
    base = travel(torch.zeros(env.num_envs, n_act, device=dev))
    creep = max(base.values())
    print(f"  all at action 0: {', '.join(f'{b} {v:.2f} m' for b, v in base.items())}")
    for k, a in enumerate(AGENTS):
        act = torch.zeros(env.num_envs, n_act, device=dev)
        act[:, sl[a].start] = 1.0  # forward
        moved = travel(act)
        good = moved[a] > creep + 0.5 and all(moved[b] < creep + 0.08 for b in AGENTS if b != a)
        ok &= good
        print(f"  {a} commanded forward: moved {', '.join(f'{b} {v:.2f} m' for b, v in moved.items())} "
              f"-> {'PASS' if good else 'FAIL'}")
    # 2. partner inputs = nearest teammate's
    for _ in range(5):
        env.step(torch.zeros(env.num_envs, n_act, device=dev))
    for a in AGENTS:
        got = cm.partner_obs(env, a, cm.PARTNER[a], "")
        feats = torch.stack([cm.partner_obs(env, a, o, f"walker_{o}") for o in OTHERS[a]], 1)
        d = torch.linalg.norm(feats[..., :2], dim=-1)
        want = feats[torch.arange(env.num_envs, device=dev), d.argmin(-1)]
        good = bool(torch.allclose(got, want)) and cm.PARTNER[a] == cm.NEAREST
        ok &= good
        print(f"  {a} partner inputs = nearest teammate's: {'PASS' if good else 'FAIL'} "
              f"(nearest: {[OTHERS[a][int(i)] for i in d.argmin(-1)[:4]]} in envs 0-3)")
    # 3. sensors, terminations, action terms
    sens = sorted(k for k in env.scene.sensors if k.startswith("robots_touch") and not k.endswith("_found"))
    falls = sorted(k for k in env.termination_manager.active_terms if k.endswith("_fell"))
    terms = sorted(env.action_manager.active_terms)
    good = len(sens) == 3 and len(falls) == 3 and terms == sorted(f"walker_{a}" for a in AGENTS)
    ok &= good
    print(f"  robot-robot sensors {sens}; fall terminations {falls}; action terms {terms}: {'PASS' if good else 'FAIL'}")
    print("ALL PASS" if ok else "SOME CHECKS FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
