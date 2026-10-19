#!/usr/bin/env python3
"""Stage 0 gate: is this walker good enough to freeze and build on?

    python scripts/validate_walker.py --task QuadCoop-Walker-AnymalC \\
        --checkpoint logs/rsl_rl/walker_anymal_c/<run>/model_5999.pt

    # Plumbing check without a trained policy (expected to FAIL the gates):
    python scripts/validate_walker.py --task QuadCoop-Walker-Spot --random-policy

Three deterministic tests, each on --num-envs parallel robots for --seconds:

  A  track     walk at vx=0.5 m/s, no disturbance        -> falls, tracking error
  B  resist    walk at vx=0.5 m/s into a constant force   -> falls, forward speed kept
               of --force-frac x body weight (opposing)
  C  push obj  walk at vx=0.4 m/s into a --obj-mass kg --object -> falls, object displacement
               object placed just in front

Pass criteria are the Stage 0 gate from the proposal and are printed with the
results; results are also written to <checkpoint dir>/validation.json.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import torch  # noqa: E402

GATES = {
    "A_fall_rate_max": 0.02,
    "A_vx_error_max": 0.15,  # m/s
    "B_fall_rate_max": 0.05,
    "B_vx_kept_min": 0.5,  # fraction of the commanded speed kept under load
    "C_fall_rate_max": 0.05,
    "C_box_disp_median_min": 2.0,  # m, the proposal's "push it 2 m" gate
}


def fixed_twist(cfg, vx: float) -> None:
    from mjlab.tasks.velocity.mdp import UniformVelocityCommandCfg

    twist = cfg.commands["twist"]
    assert isinstance(twist, UniformVelocityCommandCfg)
    twist.ranges.lin_vel_x = (vx, vx)
    twist.ranges.lin_vel_y = (0.0, 0.0)
    twist.ranges.ang_vel_z = (0.0, 0.0)
    twist.heading_command = False
    twist.ranges.heading = None
    twist.rel_standing_envs = 0.0
    twist.rel_heading_envs = 0.0
    twist.rel_forward_envs = 0.0
    twist.resampling_time_range = (1e9, 1e9)
    if hasattr(twist, "init_velocity_prob"):
        twist.init_velocity_prob = 0.0


def make_cfg(task: str, test: str, args) -> object:
    from mjlab.tasks.registry import load_env_cfg

    from quadcoop.mdp.push_force import PushForceCommandCfg
    from quadcoop.robots.objects import NOMINAL_MASS
    from quadcoop import TASKS as TASK_ROBOTS

    robot = TASK_ROBOTS[task]
    cfg = load_env_cfg(task, play=True)  # no corruption, no pushes, no curriculum
    cfg.episode_length_s = args.seconds + 1.0
    def objects(**kw):
        for k, v in kw.items():
            setattr(cfg.commands["twist"], k, v)

    objects(sample_from_ranges=True)  # eval commands come from fixed_twist's ranges
    if test == "C":
        fixed_twist(cfg, 0.4)
        objects(p_override=1.0, max_mass_override=1e9, only=args.object,
                gap_range=(0.15, 0.15), lateral_range=(0.0, 0.0), yaw_jitter=0.0,
                p_forward=1.0, angle_jitter=0.0, speed_range=(0.4, 0.4), hold_s=(1e9, 1e9))
        alpha = 0.5 * math.log(args.obj_mass / NOMINAL_MASS)
        cfg.events[f"{args.object}_mass"].params["alpha_range"] = (alpha, alpha)
    else:
        fixed_twist(cfg, 0.5)
        objects(p_override=0.0)
    if test == "B":
        cfg.commands["push_force"] = PushForceCommandCfg(
            resampling_time_range=(1e9, 1e9),
            body_name=robot.base_body,
            push_point_b=robot.push_point_b,
            fixed_frac=args.force_frac,
            p_oppose=1.0,
            oppose_jitter_deg=0.0,
            gap_s=(0.5, 0.5),
            ramp_s=(0.5, 0.5),
            hold_s=(1e9, 1e9),
            curriculum_start_scale=1.0,
        )
    cfg.scene.num_envs = args.num_envs
    return cfg


def load_policy(env, task: str, checkpoint: str | None, device: str):
    from mjlab.rl import MjlabOnPolicyRunner
    from mjlab.tasks.registry import load_rl_cfg, load_runner_cls

    if checkpoint is None:
        shape = env.unwrapped.action_space.shape
        return lambda obs: 2.0 * torch.rand(shape, device=device) - 1.0
    agent_cfg = load_rl_cfg(task)
    runner_cls = load_runner_cls(task) or MjlabOnPolicyRunner
    runner = runner_cls(env, asdict(agent_cfg), device=device)
    runner.load(checkpoint, load_cfg={"actor": True}, strict=True, map_location=device)
    return runner.get_inference_policy(device=device)


@torch.no_grad()
def run_test(task: str, test: str, args, device: str) -> dict:
    from mjlab.envs import ManagerBasedRlEnv
    from mjlab.rl import RslRlVecEnvWrapper
    from mjlab.utils.lab_api.math import quat_apply_inverse, yaw_quat

    torch.manual_seed(args.seed)
    cfg = make_cfg(task, test, args)
    video_dir = getattr(args, "video_dir", None)
    base_env = ManagerBasedRlEnv(
        cfg=cfg, device=device, render_mode="rgb_array" if video_dir else None
    )
    wrapped = base_env
    if video_dir:
        from mjlab.utils.wrappers import VideoRecorder

        wrapped = VideoRecorder(
            base_env, video_folder=video_dir, step_trigger=lambda step: step == 0,
            video_length=int(args.seconds / base_env.step_dt),
            name_prefix=getattr(args, "video_name", f"{test}"), disable_logger=True,
        )
    env = RslRlVecEnvWrapper(wrapped)
    policy = load_policy(env, task, args.checkpoint, device)

    obs = env.get_observations()
    robot, box = base_env.scene["robot"], base_env.scene[args.object]
    n = base_env.num_envs
    alive = torch.ones(n, dtype=torch.bool, device=device)
    q0 = yaw_quat(robot.data.root_link_quat_w).clone()
    box0 = box.data.root_link_pos_w.clone()
    box_disp = torch.zeros(n, device=device)
    vx_sum = torch.zeros(n, device=device)
    vx_cnt = torch.zeros(n, device=device)
    cmd_vx = 0.4 if test == "C" else 0.5
    warmup = int(1.0 / base_env.step_dt)
    steps = int(args.seconds / base_env.step_dt)

    for t in range(steps):
        obs, _, dones, extras = env.step(policy(obs))
        time_outs = extras.get("time_outs", torch.zeros_like(dones)).bool()
        fell = dones.bool() & ~time_outs
        if t >= warmup:
            vx_b = quat_apply_inverse(robot.data.root_link_quat_w, robot.data.root_link_lin_vel_w)[:, 0]
            vx_sum += torch.where(alive, vx_b, 0.0)
            vx_cnt += alive.float()
        # Box displacement along the robot's initial heading, frozen at death.
        d_w = box.data.root_link_pos_w - box0
        d_heading = quat_apply_inverse(q0, d_w)[:, 0]
        box_disp = torch.where(alive & ~fell, d_heading, box_disp)
        alive &= ~fell

    vx_mean = (vx_sum / vx_cnt.clamp(min=1)).mean().item()
    out = {
        "test": test,
        "envs": n,
        "seconds": args.seconds,
        "fall_rate": 1.0 - alive.float().mean().item(),
        "cmd_vx": cmd_vx,
        "vx_mean": vx_mean,
        "vx_error": abs(vx_mean - cmd_vx),
        "vx_kept": vx_mean / cmd_vx,
    }
    if test == "B":
        term = base_env.command_manager.get_term("push_force")
        out["force_n"] = args.force_frac * term.robot_weight_n
    if test == "C":
        out["box_mass_kg"] = args.obj_mass
        out["object"] = args.object
        out["box_disp_median"] = box_disp.median().item()
        out["box_disp_mean"] = box_disp.mean().item()
    base_env.close()
    del env, base_env, policy
    import gc

    gc.collect()
    print(f"  {test}: " + ", ".join(
        f"{k}={v:.3f}" if isinstance(v, float) else f"{k}={v}" for k, v in out.items() if k not in ("test", "object")
    ))
    return out


def judge(results: dict) -> list[tuple[str, bool, str]]:
    a, b, c = results["A"], results["B"], results["C"]
    return [
        ("A falls", a["fall_rate"] <= GATES["A_fall_rate_max"],
         f"{a['fall_rate']:.1%} <= {GATES['A_fall_rate_max']:.0%}"),
        ("A tracking", a["vx_error"] <= GATES["A_vx_error_max"],
         f"|vx err| {a['vx_error']:.2f} <= {GATES['A_vx_error_max']} m/s"),
        ("B falls", b["fall_rate"] <= GATES["B_fall_rate_max"],
         f"{b['fall_rate']:.1%} <= {GATES['B_fall_rate_max']:.0%}"),
        ("B speed kept", b["vx_kept"] >= GATES["B_vx_kept_min"],
         f"{b['vx_kept']:.0%} of cmd >= {GATES['B_vx_kept_min']:.0%} at {b['force_n']:.0f} N"),
        ("C falls", c["fall_rate"] <= GATES["C_fall_rate_max"],
         f"{c['fall_rate']:.1%} <= {GATES['C_fall_rate_max']:.0%}"),
        ("C object pushed", c["box_disp_median"] >= GATES["C_box_disp_median_min"],
         f"median {c['box_disp_median']:.2f} m >= {GATES['C_box_disp_median_min']} m "
         f"({c['box_mass_kg']:.0f} kg {c['object']})"),
    ]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--task", required=True)
    ap.add_argument("--checkpoint", default=None)
    ap.add_argument("--random-policy", action="store_true")
    ap.add_argument("--num-envs", type=int, default=64)
    ap.add_argument("--seconds", type=float, default=10.0)
    ap.add_argument("--force-frac", type=float, default=0.25)
    ap.add_argument("--obj-mass", type=float, default=15.0)
    ap.add_argument("--object", default="obj_cube",
                    choices=["obj_cube", "obj_prism", "obj_cylinder", "obj_sphere"])
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--tests", default="ABC")
    ap.add_argument("--device", default=None)
    ap.add_argument("--out", default=None, help="JSON path (default: next to the checkpoint)")
    args = ap.parse_args()
    if args.checkpoint is None and not args.random_policy:
        ap.error("give --checkpoint, or --random-policy for a plumbing check")

    import quadcoop  # noqa: F401  (registers tasks)

    device = args.device or ("cuda:0" if torch.cuda.is_available() else "cpu")
    print(f"{args.task}  checkpoint={args.checkpoint or 'RANDOM'}  device={device}")
    results = {t: run_test(args.task, t, args, device) for t in args.tests}

    verdicts = judge(results) if set(results) == {"A", "B", "C"} else []
    if verdicts:
        print()
        for name, ok, detail in verdicts:
            print(f"  {'PASS' if ok else 'FAIL'}  {name:14s} {detail}")
    passed = bool(verdicts) and all(ok for _, ok, _ in verdicts)

    out_path = Path(args.out) if args.out else (
        Path(args.checkpoint).with_name("validation.json") if args.checkpoint else None
    )
    if out_path is not None:
        out_path.write_text(json.dumps(
            {"task": args.task, "checkpoint": args.checkpoint, "gates": GATES,
             "results": results, "passed": passed}, indent=2))
        print(f"\nwrote {out_path}")
    if verdicts:
        print("\nSTAGE 0 GATE:", "PASSED -- freeze this walker." if passed else "NOT PASSED")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())