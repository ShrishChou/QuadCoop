"""Spot-arm walker in the walker training env: does a policy walk? (debug + acceptance for spot_arm_walker.py)

    python scripts/spot_arm/walker_ft_check.py [--ckpt logs/rsl_rl/walker_spot_arm/<run>/model_N.pt] [--noise 0.25]
        [--corrupt] [--no-dr] [--steps 400] [--envs 64]

Runs the policy (RAI's onnx weights by default, or a trained checkpoint's actor) deterministically, or with Gaussian
action noise of std --noise (the training rollout's), in QuadCoop-Walker-SpotArm's env (play variant unless
--train-env) and reports: episode terminations by reason and time, base height, velocity tracking, which non-foot
geoms touched the ground first. Writes nothing.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", default="")
    ap.add_argument("--noise", type=float, default=0.0)
    ap.add_argument("--corrupt", action="store_true", help="observation noise on (training's)")
    ap.add_argument("--train-env", action="store_true", help="the training env (curriculum, kicks, randomization)")
    ap.add_argument("--no-arm", action="store_true", help="arm held stowed")
    ap.add_argument("--steps", type=int, default=400)
    ap.add_argument("--compare", action="store_true")
    ap.add_argument("--posture", action="store_true", help="the posture variant's env: torso commands sampled")
    ap.add_argument("--envs", type=int, default=64)
    ap.add_argument("--drop-events", default="", help="comma list of event terms to remove")
    ap.add_argument("--keep-only-reset", action="store_true", help="remove every event but reset_base/reset_robot_joints")
    ap.add_argument("--spawn-z", type=float, default=None, help="reset_base z range fixed at this offset")
    a = ap.parse_args()

    import quadcoop  # noqa: F401
    from mjlab.envs import ManagerBasedRlEnv

    from quadcoop.spot_arm_walker import make_spot_arm_walker_env_cfg, rai_actor_weights

    cfg = make_spot_arm_walker_env_cfg(play=not a.train_env, posture=a.posture)
    cfg.scene.num_envs = a.envs
    cfg.observations["actor"].enable_corruption = a.corrupt
    if not a.train_env:
        cfg.episode_length_s = 20.0
    cfg.actions["joint_pos"].move_arm = not a.no_arm
    for name in [x for x in a.drop_events.split(",") if x]:
        cfg.events.pop(name)
    if a.keep_only_reset:
        for name in list(cfg.events):
            if name not in ("reset_base", "reset_robot_joints") and not name.endswith(("_mass", "_friction")):
                cfg.events.pop(name)
        print("events kept:", sorted(cfg.events), flush=True)
    if a.spawn_z is not None:
        cfg.events["reset_base"].params["pose_range"]["z"] = (a.spawn_z, a.spawn_z)
    dev = "cuda:0" if torch.cuda.is_available() else "cpu"
    env = ManagerBasedRlEnv(cfg, device=dev)
    net = torch.nn.Sequential(torch.nn.Linear(84, 512), torch.nn.ELU(), torch.nn.Linear(512, 256), torch.nn.ELU(),
                              torch.nn.Linear(256, 128), torch.nn.ELU(), torch.nn.Linear(128, 12)).to(dev)
    sd = rai_actor_weights() if not a.ckpt else {k: v for k, v in torch.load(a.ckpt, map_location="cpu",
                                                                            weights_only=False)["actor_state_dict"].items()
                                                  if k.startswith("mlp.")}
    net.load_state_dict({k[4:]: v for k, v in sd.items()})
    print(f"policy: {a.ckpt or 'RAI onnx'}; noise {a.noise}; obs corruption {a.corrupt}; "
          f"{'training' if a.train_env else 'play'} env; arm {'stowed' if a.no_arm else 'moving'}", flush=True)
    obs, _ = env.reset()
    if a.compare:  # this env's actor input against spot_arm.RaiWalker's, at the same state
        from quadcoop.robots import spot_arm as sa
        rw = sa.RaiWalker(env.scene["robot"], dev)
        term = env.action_manager.get_term("joint_pos")
        for k in range(3):
            o = obs["actor"]
            d = env.scene["robot"].data
            ref = torch.cat([d.root_link_lin_vel_b, d.root_link_ang_vel_b, d.projected_gravity_b, term.command25(),
                             d.joint_pos[:, rw.m2i] - rw.joff, d.joint_vel[:, rw.m2i], term.raw_action], -1)
            names = ["lin", "ang", "grav", "cmd", "jpos", "jvel", "prev"]
            sizes = [3, 3, 3, 25, 19, 19, 12]
            print(f"  compare step {k}: obs shape {tuple(o.shape)}")
            i0 = 0
            for nm, sz in zip(names, sizes):
                print(f"    {nm}: max |diff| {float((o[:, i0:i0 + sz] - ref[:, i0:i0 + sz]).abs().max()):.4f}  "
                      f"env0 obs {[round(float(x), 2) for x in o[0, i0:i0 + min(sz, 6)]]}")
                i0 += sz
            with torch.no_grad():
                obs, *_ = env.step(net(obs["actor"]))
    robot = env.scene["robot"]
    tm = env.termination_manager
    n = a.envs
    ep_t = torch.zeros(n, device=dev)
    ends = {}
    h, err, terr = [], [], []
    first_ill = None
    for t in range(a.steps):
        with torch.no_grad():
            act = net(obs["actor"])
            if a.noise > 0:
                act = act + a.noise * torch.randn_like(act)
        obs, _, term, trunc, _ = env.step(act)
        if t < 20:
            print(f"    t={t} z0={float(robot.data.root_link_pos_w[0, 2]):.3f} act0max={float(act[0].abs().max()):.2f} "
                  f"q0legs={[round(float(x), 2) for x in robot.data.joint_pos[0, :3]]}", flush=True)
        ep_t += env.step_dt
        h.append(float(robot.data.root_link_pos_w[:, 2].mean()))
        cmd = env.command_manager.get_term("twist").command[:, :2]
        err.append(float(torch.linalg.norm(robot.data.root_link_lin_vel_b[:, :2] - cmd, dim=-1).mean()))
        tt = env.action_manager.get_term("joint_pos").torso
        terr.append(float((robot.data.root_link_pos_w[:, 2] - tt[:, 2]).abs().mean()))
        done = term | trunc
        if done.any():
            for name in tm.active_terms:
                hit = tm.get_term(name) & done
                if hit.any():
                    e = ends.setdefault(name, [])
                    e += ep_t[hit].tolist()
            if first_ill is None and "illegal_contact" in tm.active_terms and tm.get_term("illegal_contact").any():
                s = env.scene.sensors["nonfoot_ground_touch"]
                f = s.data.found.view(n, -1)
                hits = torch.nonzero(f.any(-1))
                if hits.numel() == 0:
                    continue
                i = int(hits[0])
                first_ill = (t, i, torch.nonzero(f[i]).squeeze(-1).tolist(), float(robot.data.root_link_pos_w[i, 2]))
            ep_t[done] = 0.0
    print(f"steps {a.steps} x {n} envs ({a.steps * env.step_dt:.1f} s)")
    for name, v in ends.items():
        v = torch.tensor(v)
        print(f"  ended by {name}: {len(v)}  (episode time median {v.median():.2f} s, min {v.min():.2f})")
    if not ends:
        print("  no episode ended")
    print(f"  base height mean: first 1 s {sum(h[:50]) / 50:.3f} m, last 2 s {sum(h[-100:]) / 100:.3f} m")
    print(f"  |height - commanded torso height| mean: {sum(terr[50:]) / max(1, len(terr) - 50):.3f} m (after 1 s)")
    print(f"  planar velocity error mean: {sum(err[50:]) / max(1, len(err) - 50):.3f} m/s (after 1 s)")
    if first_ill:
        s = env.scene.sensors["nonfoot_ground_touch"]
        print(f"  first illegal contact: step {first_ill[0]}, env {first_ill[1]}, sensor slots {first_ill[2]}, "
              f"base height {first_ill[3]:.3f}; sensor primary geoms: {getattr(s, 'primary_names', '?')}")


if __name__ == "__main__":
    main()
