"""Spot-arm pair, turn in place: demonstrations from the scripted maneuver (docs/spot_arm_pair.md, "Turn in place").

    python scripts/spot_arm/collect_demos.py --out logs/demos/turn40.pt [--envs 256] [--episodes 3] [--turn 40]

Builds the training env of the turn-in-place runs (slurm/spot_arm_turn.env: --arm hand_rate --hand-obs, opposite
starts, +-turn goals at the object's centre, observation noise and resets as in training) and drives both robots
with quadcoop/coop2/spot_arm_script.py. Every second step, each actor's inputs (actor_<a>, top_<a>, front; sanitized
as the trainer does) and the env action are recorded; only episodes that end in success are kept (successes up to
their success step). Writes {"obs": {group: fp16 tensor}, "act": (N, 14), "episodes", "success_rate", "turn"}.
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", required=True)
    ap.add_argument("--envs", type=int, default=256)
    ap.add_argument("--episodes", type=int, default=3, help="episode lengths of simulation per env")
    ap.add_argument("--turn", type=float, default=40.0)
    ap.add_argument("--every", type=int, default=2)
    ap.add_argument("--seed", type=int, default=11)
    a = ap.parse_args()
    os.environ["QUADCOOP_SHAPES"] = "v2"
    os.environ["QUADCOOP_PAIR"] = "spot_arm"
    import torch

    import quadcoop  # noqa: F401
    from mjlab.envs import ManagerBasedRlEnv

    from quadcoop.coop2.env_cfg import make_coop2_env_cfg
    from quadcoop.coop2.marl import MarlCfg, actor_groups
    from quadcoop.coop2.mdp import AGENTS
    from quadcoop.coop2.spot_arm_script import TurnScript

    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    level = (0.0, 0.0, 15, 0, 10, a.turn, 0.10, 6, 1.0, 22, 18)
    cfg = make_coop2_env_cfg("b", partner_map=True, reward_set="r7", arm="hand_rate", hand_obs=True, pilot_level=level,
                             pilot_episode_s=20.0, turn_signs=True, start_mode="opposite", train_shapes=("long",),
                             train_mass=(18.0, 22.0), fixed_difficulty=True)
    cfg.scene.num_envs = a.envs
    cfg.seed = a.seed
    cfg.commands["goal"].start_level = 0
    cfg.commands["goal"].tol_start_finest = True
    env = ManagerBasedRlEnv(cfg=cfg, device=device)
    n, dev = env.num_envs, env.device
    clip = MarlCfg().obs_clip
    groups = sorted({g_ for ag in AGENTS for g_ in actor_groups(ag, "b")})
    obs, _ = env.reset()
    script = TurnScript(env)
    tm = env.termination_manager
    steps = int(a.episodes * 20.0 / env.step_dt)
    rec = {g_: [] for g_ in groups}
    rec_act, rec_ep, rec_k = [], [], []
    ep_id = torch.arange(n, device=dev)  # each env's current episode number (unique across envs)
    next_id = n
    ep_success: dict[int, bool] = {}
    with torch.no_grad():
        for k in range(steps):
            act = script.act()
            if k % a.every == 0:
                for g_ in groups:
                    rec[g_].append(torch.nan_to_num(obs[g_], nan=0.0, posinf=clip, neginf=-clip).clamp(-clip, clip).half().cpu())
                rec_act.append(act.cpu())
                rec_ep.append(ep_id.cpu().clone())
                rec_k.append(k)
            obs, _, term, trunc, _ = env.step(act)
            done = (term | trunc)
            if bool(done.any()):
                ok = tm.get_term("goal_reached") if "goal_reached" in tm.active_terms else torch.zeros_like(done)
                for j in done.nonzero().flatten().tolist():
                    ep_success[int(ep_id[j])] = bool(ok[j])
                ids = done.nonzero().flatten()
                ep_id[ids] = torch.arange(next_id, next_id + len(ids), device=dev)
                next_id += len(ids)
                script.reset(ids)
            if k % 500 == 0:
                ended = len(ep_success)
                print(f"step {k}/{steps}: {ended} episodes ended, {sum(ep_success.values())} successful", flush=True)
    eps = torch.stack(rec_ep)  # (S, n)
    good = torch.tensor([ep_success.get(int(e), False) for e in range(next_id)])
    keep = good[eps]  # (S, n): successful episodes only (unfinished episodes are dropped)
    out = {"obs": {g_: torch.stack(rec[g_])[keep] for g_ in groups}, "act": torch.stack(rec_act)[keep],
           "episodes": int(good.sum()), "ended": len(ep_success), "success_rate": float(good.sum()) / max(len(ep_success), 1),
           "turn": a.turn, "every": a.every}
    p = ROOT / a.out
    p.parent.mkdir(parents=True, exist_ok=True)
    torch.save(out, p)
    print(f"demonstrations: {out['episodes']} successful of {out['ended']} ended episodes ({out['success_rate']:.0%}); "
          f"{out['act'].shape[0]} samples -> {p} ({p.stat().st_size / 1e9:.2f} GB)", flush=True)
    env.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
