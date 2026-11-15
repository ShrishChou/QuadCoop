"""Spot-arm pair, wiring test (docs/spot_arm_pair.md): does the policy's action reach each robot's arm?

    python scripts/spot_arm/pair_wiring.py [--checkpoint logs/marl2/<run>/model_<n>.pt] [--out evals/spot_arm/pair_wiring]

Builds the two-robot training env with --pair spot_arm --arm learned (the turn pilot's settings) and checks:
  1. action layout: 9 actions per robot, 18 in all; the observation sizes;
  2. Spot 1 moves its arm (a scripted unfold-and-sweep action) while Spot 2 gets zeros, then the reverse:
     the moving arm's joints follow its rate-limited targets, the other arm stays stowed, nobody falls;
  3. arm lock: with a robot's arm locked the same action leaves its arm stowed;
  4. with --checkpoint (a train_coop2.py --pair spot_arm --arm learned checkpoint, e.g. after one PPO update):
     the reloaded policy outputs 18 actions and its arm outputs move both arms.
Writes a video of 2 (captions: commanded and measured shoulder / elbow per robot) and report.json. Exit 1 on a failure.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
PILOT_LEVEL = (1.0, 1.0, 25, 0, 10, 30, 0.10, 6, 1.0, 22, 18)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--checkpoint", default="")
    ap.add_argument("--out", default="evals/spot_arm/pair_wiring")
    ap.add_argument("--num-envs", type=int, default=16)
    a = ap.parse_args()
    os.environ["QUADCOOP_SHAPES"] = "v2"
    os.environ["QUADCOOP_PAIR"] = "spot_arm"
    import numpy as np
    import torch
    from tensordict import TensorDict

    import quadcoop  # noqa: F401
    from mjlab.envs import ManagerBasedRlEnv

    from quadcoop import falls
    from quadcoop.coop2.env_cfg import SPECS, make_coop2_env_cfg
    from quadcoop.coop2.marl import PairPolicy, action_slices
    from quadcoop.coop2.mdp import AGENTS
    from quadcoop.coop2.video import Camera, key_points, render_episode

    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    cfg = make_coop2_env_cfg("b", partner_map=True, reward_set="r7", arm="learned", pilot_level=PILOT_LEVEL,
                             pilot_episode_s=1e5, dyaw_choices=True, train_shapes=("long",), train_mass=(18.0, 22.0),
                             fixed_difficulty=True)
    cfg.scene.num_envs = a.num_envs
    cfg.commands["goal"].start_level = 0
    cfg.terminations = {}  # nothing resets during the test; falls are measured below
    env = ManagerBasedRlEnv(cfg=cfg, device=device)
    n, dev, dt = env.num_envs, env.device, env.step_dt
    obs, _ = env.reset()
    sl = action_slices(env)
    terms = {ag: env.action_manager.get_term(f"walker_{ag}") for ag in AGENTS}
    rep = {"agents": list(AGENTS), "action_slices": {ag: [s.start, s.stop] for ag, s in sl.items()},
           "obs": {k: list(v.shape[1:]) for k, v in obs.items()}, "checks": {}}
    ok = {}
    ok["layout_9_per_robot"] = all(s.stop - s.start == 9 for s in sl.values()) and env.action_manager.total_action_dim == 18
    print(f"action layout {rep['action_slices']}, observations {rep['obs']}", flush=True)

    def fallen():
        return torch.stack([falls.fallen(env, asset_name=ag, nominal_height=SPECS[ag].nominal_height) for ag in AGENTS], -1)

    def arm_q(ag):
        return env.scene[ag].data.joint_pos[:, 12:18]

    rec_q, rec_pts, cap, rec_mp, rec_mq = [], [], [], [], []
    nmocap = env.sim.mj_model.nmocap

    def run(mover: str | None, seconds: float, label: str, policy=None, record=True) -> dict:
        """mover's arm: unfold (shoulder, elbow action 0.5) and sweep the shoulder yaw; the other robot: zeros."""
        nonlocal obs
        st = {ag: {"track": [], "dev": [], "goal": []} for ag in AGENTS}
        fell = torch.zeros(n, 2, dtype=torch.bool, device=dev)
        for k in range(int(seconds / dt)):
            t = k * dt
            if policy is not None:
                act = policy(TensorDict({x: v for x, v in obs.items() if not x.startswith("walker_")}, batch_size=[n]), env=env)
            else:
                act = torch.zeros(n, 18, device=dev)
                if mover is not None:
                    s0 = sl[mover].start
                    act[:, s0 + 3] = 0.5 * math.sin(2 * math.pi * 0.25 * t)  # shoulder yaw sweep
                    act[:, s0 + 4] = 0.5  # shoulder up-and-forward
                    act[:, s0 + 5] = 0.5  # elbow open
            obs, *_ = env.step(act)
            fell |= fallen()
            for ag in AGENTS:
                tm = terms[ag]
                st[ag]["track"].append((arm_q(ag) - tm.arm_target).abs().max(-1).values)
                st[ag]["dev"].append((arm_q(ag) - tm.stow).abs().max(-1).values)
                st[ag]["goal"].append((tm.arm_goal - tm.stow).abs().max(-1).values)
            if record and k % 2 == 0:
                rec_q.append(env.sim.data.qpos[0].cpu().numpy().copy())
                rec_pts.append(key_points(env, 0))
                if nmocap:
                    rec_mp.append(env.sim.data.mocap_pos[0].cpu().numpy().copy())
                    rec_mq.append(env.sim.data.mocap_quat[0].cpu().numpy().copy())
                txt = [label]
                for ag in AGENTS:
                    tm = terms[ag]
                    txt.append(f"{ag}: shoulder cmd {float(tm.arm_goal[0, 1]):+.2f} target {float(tm.arm_target[0, 1]):+.2f} "
                               f"measured {float(arm_q(ag)[0, 1]):+.2f} | elbow cmd {float(tm.arm_goal[0, 2]):+.2f} "
                               f"target {float(tm.arm_target[0, 2]):+.2f} measured {float(arm_q(ag)[0, 2]):+.2f} rad")
                cap.append("\n".join(txt))
        out = {"fell_share": [round(float(x), 3) for x in fell.float().mean(0)]}
        for ag in AGENTS:
            tail = int(1.0 / dt)
            out[ag] = {"tracking_err_last_s": round(float(torch.stack(st[ag]["track"][-tail:]).mean()), 3),
                       "max_dev_from_stowed": round(float(torch.stack(st[ag]["dev"]).max(0).values.mean()), 3),
                       "max_commanded_dev": round(float(torch.stack(st[ag]["goal"]).max()), 3)}
        return out

    a1, a2 = AGENTS
    with torch.no_grad():
        run(None, 1.0, "settle", record=False)
        r1 = run(a1, 5.0, f"{a1} moves its arm, {a2} holds")
        back1 = run(None, 3.0, "both return to stowed")
        r2 = run(a2, 5.0, f"{a2} moves its arm, {a1} holds")
        back2 = run(None, 3.0, "both return to stowed")
        terms[a1].arm_locked[:] = True
        r3 = run(a1, 3.0, f"{a1} arm locked, same action", record=False)
        terms[a1].arm_locked[:] = False
        run(None, 2.0, "settle", record=False)
    rep["spot1_moves"], rep["spot2_moves"], rep["return"], rep["locked"] = r1, r2, [back1, back2], r3
    ok["mover_arm_moves"] = r1[a1]["max_dev_from_stowed"] > 0.8 and r2[a2]["max_dev_from_stowed"] > 0.8
    ok["mover_arm_tracks"] = r1[a1]["tracking_err_last_s"] < 0.15 and r2[a2]["tracking_err_last_s"] < 0.15
    ok["holder_arm_stays"] = r1[a2]["max_dev_from_stowed"] < 0.1 and r2[a1]["max_dev_from_stowed"] < 0.1
    ok["arms_return"] = max(back2[a1]["tracking_err_last_s"], back2[a2]["tracking_err_last_s"]) < 0.1
    ok["locked_arm_stays"] = r3[a1]["max_dev_from_stowed"] < 0.1
    ok["no_falls"] = max(r1["fell_share"] + r2["fell_share"] + back1["fell_share"] + back2["fell_share"]) == 0.0

    if a.checkpoint:
        ck = torch.load(a.checkpoint, map_location="cpu", weights_only=False)
        o_td = TensorDict({x: v for x, v in obs.items() if not x.startswith("walker_")}, batch_size=[n])
        pol = PairPolicy(o_td, device, "b", checkpoint=a.checkpoint)
        with torch.no_grad():
            act = pol(o_td, env=env)
            r4 = run(None, 4.0, f"reloaded policy (iteration {int(ck['iter'])}, {ck['algo']}) drives both arms", policy=pol)
        rep["checkpoint"] = {"path": a.checkpoint, "iter": int(ck["iter"]), "algo": ck["algo"], "act_dims": ck.get("act_dims"),
                             "robots": ck.get("robots"), "arm": ck.get("arm"), "action_shape": list(act.shape), "run": r4}
        ok["checkpoint_records_model_and_arm"] = ck.get("arm") == "learned" and set((ck.get("robots") or {}).values()) == {"spot_arm"}
        ok["reloaded_policy_18_actions"] = list(act.shape) == [n, 18]
        # a fresh policy's arm outputs are small but not zero: the arms must leave stowed by more than sensor noise
        ok["reloaded_policy_moves_arms"] = min(r4[a1]["max_commanded_dev"], r4[a2]["max_commanded_dev"]) > 0.01

    rep["checks"], rep["pass"] = ok, all(ok.values())
    out = ROOT / a.out
    out.mkdir(parents=True, exist_ok=True)
    try:
        cam = Camera(env, 960, 720)
        render_episode(cam, 0, np.stack(rec_q), np.stack(rec_mp) if nmocap else None,
                       np.stack(rec_mq) if nmocap else None, np.stack(rec_pts), out / "arms.mp4", fps=1.0 / (2 * dt),
                       caption=lambda f: cap[f])
        rep["video"] = str(out / "arms.mp4")
    except Exception as e:  # noqa: BLE001
        rep["video_error"] = repr(e)
        print(f"video failed: {e!r}")
    (out / "report.json").write_text(json.dumps(rep, indent=1))
    for k, v in ok.items():
        print(f"  {'PASS' if v else 'FAIL'}  {k}")
    for nm, r in (("spot1 moves", r1), ("spot2 moves", r2), ("locked", r3)):
        print(f"  {nm}: {json.dumps(r)}")
    print(f"wiring test: {'PASS' if rep['pass'] else 'FAIL'}  ({out / 'report.json'})")
    env.close()
    return 0 if rep["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
