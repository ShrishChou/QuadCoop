"""Spot-arm walker under load: the walker comparison and the posture test (docs/spot_arm.md, "Pushing walker").

    python scripts/spot_arm/walker_load_test.py --policy rai --policy s1=<model.pt> --policy s2=<model.pt> \
        --out evals/walker_load/summary.md

No objects: the load is an external force, so every policy, arm pose and torso command gets the identical push.

1. Ramp (the posture test): command forward 0.3 m/s; a force against the travel rises 0 -> 250 N over 12.5 s
   (20 N/s), on the trunk front with the arm stowed, on the hand with the arm braced (RAI's "out" pose, forward and
   low). Torso: default (height 0.52 m) or lowered (0.45 m, pitch 0.1). Per config:
     held force   = the force when forward speed first stays under 0.1 m/s for 0.5 s (stall) or the robot falls
                    (250 if neither), median over envs
     displacement = forward travel until then;  yaw drift = |yaw change| until then
     foot slip    = mean planar speed of feet in ground contact;  torque sat = share of leg-actuator steps at >= 98%
                    of the force limit;  falls = share of envs that fell (base contact or tilt) during the ramp
2. Sweep (the walker comparison): 60 N against the travel (trunk, arm stowed, torso default) for 8 s at each command:
   forward 0.5, sideways 0.4, backward 0.4, turn 0.6 rad/s, stop. Velocity error (planar, and yaw rate), falls,
   yaw drift (for the translations); 0 N for reference.
"""
from __future__ import annotations

import argparse
import math
import os
import sys
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

RAMP_RATE = 20.0
RAMP_MAX = 250.0
SWEEP = {"forward": (0.5, 0.0, 0.0), "sideways": (0.0, 0.4, 0.0), "backward": (-0.4, 0.0, 0.0),
         "turn": (0.0, 0.0, 0.6), "stop": (0.0, 0.0, 0.0)}
TORSO = {"default": (0.0, 0.0, 0.52), "lowered": (0.0, 0.1, 0.45)}


def yaw_of(q: torch.Tensor) -> torch.Tensor:
    return torch.atan2(2 * (q[:, 0] * q[:, 3] + q[:, 1] * q[:, 2]), 1 - 2 * (q[:, 2] ** 2 + q[:, 3] ** 2))


def wrap(a: torch.Tensor) -> torch.Tensor:
    return (a + math.pi) % (2 * math.pi) - math.pi


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--policy", action="append", required=True, help="rai, or name=<model.pt>")
    ap.add_argument("--envs", type=int, default=32)
    ap.add_argument("--out", default="evals/walker_load/summary.md")
    ap.add_argument("--skip-sweep", action="store_true")
    a = ap.parse_args()

    import quadcoop  # noqa: F401
    from mjlab.envs import ManagerBasedRlEnv

    from quadcoop.robots import spot_arm as sa
    from quadcoop.spot_arm_walker import make_spot_arm_walker_env_cfg, rai_actor_weights

    cfg = make_spot_arm_walker_env_cfg(play=True, posture=True)
    cfg.scene.num_envs = a.envs
    cfg.episode_length_s = 1e5
    cfg.observations["actor"].enable_corruption = False
    cfg.actions["joint_pos"].move_arm = False
    cfg.commands["twist"].p_free_walk = 1.0  # no objects
    for name in list(cfg.events):  # no kicks; keep resets and the startup randomization
        if name not in ("reset_base", "reset_robot_joints") and not name.endswith(("_mass", "_friction")):
            cfg.events.pop(name)
    dev = "cuda:0" if torch.cuda.is_available() else "cpu"
    env = ManagerBasedRlEnv(cfg, device=dev)
    n = env.num_envs
    robot = env.scene["robot"]
    term = env.action_manager.get_term("joint_pos")
    twist = env.command_manager.get_term("twist")
    cmd = torch.zeros(n, 3, device=dev)
    orig_res, orig_upd = twist._resample_command, twist._update_command

    def res(ids):
        orig_res(ids)
        twist.vel_command_b[ids] = cmd[ids]

    def upd():
        orig_upd()
        twist.vel_command_b[:] = cmd
    twist._resample_command, twist._update_command = res, upd

    trunk = robot.find_bodies("body")[0][0]
    hand = robot.find_bodies(sa.GRIPPER_BODY)[0][0]
    feet = robot.find_sites(("site_front_left", "site_front_right", "site_rear_left", "site_rear_right"),
                            preserve_order=True)[0]
    leg_act = list(range(12))  # actuators in model order: 12 legs, then the arm
    lim = torch.tensor(env.sim.mj_model.actuator_forcerange[:12, 1], device=dev, dtype=torch.float32)
    lim = torch.where(lim > 0, lim, torch.full_like(lim, float("inf")))
    print("leg torque limits (N m):", [round(float(x), 1) for x in lim], flush=True)
    feet_s = env.scene.sensors["feet_ground_contact"]
    fall_terms = [t for t in env.termination_manager.active_terms if t != "time_out"]

    def make_net(spec: str):
        net = torch.nn.Sequential(torch.nn.Linear(84, 512), torch.nn.ELU(), torch.nn.Linear(512, 256), torch.nn.ELU(),
                                  torch.nn.Linear(256, 128), torch.nn.ELU(), torch.nn.Linear(128, 12)).to(dev)
        if spec == "rai":
            sd = rai_actor_weights()
        else:
            sd = {k: v for k, v in torch.load(spec, map_location="cpu", weights_only=False)["actor_state_dict"].items()
                  if k.startswith("mlp.")}
        net.load_state_dict({k[4:]: v for k, v in sd.items()})
        return net.eval()

    def setup(arm, torso, c):
        cmd[:] = torch.tensor(c, device=dev)
        obs, _ = env.reset()
        z = torch.zeros(n, 2, 3, device=dev)
        robot.write_external_wrench_to_sim(z, z, body_ids=[trunk, hand])
        term.arm_goal[:] = arm
        term.arm_target[:] = arm
        term.torso[:] = torch.tensor(torso, device=dev)
        twist.vel_command_b[:] = cmd
        return env.observation_manager.compute()

    def push(force_mag, body):
        """force_mag (n,) against the commanded planar travel (body forward when the command has none)."""
        v = cmd[:, :2]
        ang = torch.where(torch.linalg.norm(v, dim=-1) > 0.05, torch.atan2(v[:, 1], v[:, 0]), torch.zeros_like(v[:, 0]))
        yaw = yaw_of(robot.data.root_link_quat_w) + ang + math.pi
        f = torch.zeros(n, 2, 3, device=dev)
        k = 0 if body == trunk else 1
        f[:, k, 0] = torch.cos(yaw) * force_mag
        f[:, k, 1] = torch.sin(yaw) * force_mag
        robot.write_external_wrench_to_sim(f, torch.zeros_like(f), body_ids=[trunk, hand])

    def run(net, arm, torso, c, force_fn, body, seconds, stall=False):
        obs = setup(arm, torso, c)
        for _ in range(int(1.0 / env.step_dt)):  # 1 s to settle into the command, no load
            with torch.no_grad():
                obs, *_ = env.step(net(obs["actor"]))
        p0 = robot.data.root_link_pos_w[:, :2].clone()
        y0 = yaw_of(robot.data.root_link_quat_w)
        alive = torch.ones(n, dtype=torch.bool, device=dev)
        done_at = torch.full((n,), float("nan"), device=dev)
        held = torch.full((n,), float("nan"), device=dev)
        disp = torch.zeros(n, device=dev)
        ydr = torch.zeros(n, device=dev)
        slow = torch.zeros(n, device=dev)
        fell = torch.zeros(n, dtype=torch.bool, device=dev)
        slip, sat, verr, werr = [], [], [], []
        heading = torch.stack([torch.cos(y0), torch.sin(y0)], -1)
        steps = int(seconds / env.step_dt)
        for i in range(steps):
            t = (i + 1) * env.step_dt
            mag = force_fn(t)
            push(torch.full((n,), mag, device=dev), body)
            with torch.no_grad():
                obs, _, te, tr, _ = env.step(net(obs["actor"]))
            d = robot.data
            gone = te & alive
            fell |= gone
            vb = d.root_link_lin_vel_b
            fwd = ((d.root_link_pos_w[:, :2] - p0) * heading).sum(-1)
            yaw_d = wrap(yaw_of(d.root_link_quat_w) - y0).abs()
            act = alive & ~gone
            if act.any():
                fc = (feet_s.data.found.view(n, -1)[:, :4] > 0)
                fv = torch.linalg.norm(d.site_lin_vel_w[:, feet, :2], dim=-1)
                if fc[act].any():
                    slip.append(float(fv[act][fc[act]].mean()))
                u = d.actuator_force[act][:, leg_act].abs() / lim
                sat.append((float((u >= 0.98).float().mean()), float(u.max(-1).values.mean())))
                verr.append(float(torch.linalg.norm(vb[act, :2] - cmd[act, :2], dim=-1).mean()))
                werr.append(float((d.root_link_ang_vel_b[act, 2] - cmd[act, 2]).abs().mean()))
            if stall:
                slow = torch.where(vb[:, 0] < 0.1, slow + env.step_dt, torch.zeros_like(slow))
                stop = alive & ((slow >= 0.5) | gone)
                held[stop] = mag
            else:
                stop = gone
            disp = torch.where(alive, fwd, disp)
            ydr = torch.where(alive, yaw_d, ydr)
            done_at[stop] = t
            alive &= ~stop
            if not alive.any():
                break
        held = torch.where(torch.isnan(held), torch.full_like(held, force_fn(seconds)), held)
        mean = lambda xs: sum(xs) / max(1, len(xs))  # noqa: E731
        return {"held": float(held.median()), "held_lo": float(held.quantile(0.25)), "disp": float(disp.mean()),
                "yaw": math.degrees(float(ydr.mean())), "slip": mean(slip), "sat": mean([x[0] for x in sat]), "peak": mean([x[1] for x in sat]), "fall": float(fell.float().mean()),
                "verr": mean(verr), "werr": mean(werr)}

    stow = torch.tensor(sa.ARM_STOWED, device=dev)
    braced = torch.tensor(sa.ARM_OUT, device=dev)
    lines = ["# Spot-arm walker under load", "",
             f"{n} envs per row; no objects; force against the commanded travel (scripts/spot_arm/walker_load_test.py)", ""]
    ramp_rows, sweep_rows = [], []
    for spec in a.policy:
        name, path = ("rai", "rai") if spec == "rai" else spec.split("=", 1)
        net = make_net(path)
        for arm_name, arm, body in (("stowed (trunk)", stow, trunk), ("braced (hand)", braced, hand)):
            for tname, torso in TORSO.items():
                r = run(net, arm, torso, (0.3, 0.0, 0.0), lambda t: min(RAMP_MAX, RAMP_RATE * t), body,
                        RAMP_MAX / RAMP_RATE + 2.0, stall=True)
                ramp_rows.append(f"| {name} | {arm_name} | {tname} | {r['held']:.0f} ({r['held_lo']:.0f}) | {r['disp']:.2f} | "
                                 f"{r['yaw']:.1f} | {r['slip']:.3f} | {r['sat']:.3f} | {r['peak']:.2f} | {r['fall']:.2f} |")
                print(ramp_rows[-1], flush=True)
        if not a.skip_sweep:
            for f in (0.0, 60.0):
                for cname, c in SWEEP.items():
                    r = run(net, stow, TORSO["default"], c, lambda t, f=f: f, trunk, 8.0)
                    sweep_rows.append(f"| {name} | {f:.0f} N | {cname} | {r['verr']:.3f} | {r['werr']:.3f} | "
                                      f"{r['yaw'] if cname != 'turn' else float('nan'):.1f} | {r['slip']:.3f} | {r['fall']:.2f} |")
                    print(sweep_rows[-1], flush=True)
    lines += ["## Ramp: forward 0.3 m/s against a force rising 20 N/s to 250 N", "",
              "| policy | arm (force on) | torso | held force N, median (25%) | displacement m | yaw drift deg | foot slip m/s | torque sat | peak torque / limit | falls |",
              "|---|---|---|---|---|---|---|---|---|---|", *ramp_rows, ""]
    if sweep_rows:
        lines += ["## Sweep: 8 s per command, arm stowed, torso default, force on the trunk", "",
                  "| policy | force | command | planar vel err m/s | yaw-rate err rad/s | yaw drift deg | foot slip m/s | falls |",
                  "|---|---|---|---|---|---|---|---|", *sweep_rows, ""]
    out = ROOT / a.out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines))
    print(f"wrote {out}")


if __name__ == "__main__":
    os.environ.setdefault("MUJOCO_GL", "egl")
    main()
