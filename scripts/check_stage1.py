"""Checks for the Stage 1 push-to-goal env (run before training it).

    QUADCOOP_WALKER_CKPT=<walker model_N.pt> python scripts/check_stage1.py --task QuadCoop-Push-AnymalC

  1  frozen walker: our rebuild gives the same actions as rsl_rl's own inference policy
  2  the walker sees exactly the observation layout it was trained on (48 dims, its
     command term is the high-level command, its 'actions' term is its own last action)
  3  scene: box ahead of the robot, goal ahead of the box, goal marker under the goal,
     goal yaw only (xy-plane rotation), errors folded by box symmetry
  4  closing the loop: high-level action -> command -> walker -> joints move, no NaNs
  5  curriculum: levels move on success, mass window opens only after the task is learned
"""

from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import torch  # noqa: E402

FAILS: list[str] = []


def check(cond: bool, msg: str) -> None:
    print(("  ok   " if cond else "  FAIL ") + msg)
    if not cond:
        FAILS.append(msg)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True)
    ap.add_argument("--device", default=None)
    ap.add_argument("--envs", type=int, default=16)
    a = ap.parse_args()
    device = a.device or ("cuda:0" if torch.cuda.is_available() else "cpu")

    import quadcoop  # noqa: F401
    import quadcoop.stage1  # noqa: F401
    from mjlab.envs import ManagerBasedRlEnv
    from mjlab.tasks.registry import load_env_cfg

    from quadcoop.stage1 import mdp
    from quadcoop.stage1.objects import SHAPES

    cfg = load_env_cfg(a.task)
    cfg.scene.num_envs = a.envs
    env = ManagerBasedRlEnv(cfg=cfg, device=device)
    obs, _ = env.reset()
    act = env.action_manager.get_term("walker")
    goal = env.command_manager.get_term("goal")
    twist = env.command_manager.get_term("twist")
    robot = env.scene["robot"]

    # [1] frozen walker == rsl_rl inference policy -----------------------------------
    print("\n[1] frozen walker")
    from rsl_rl.models import MLPModel  # noqa: F401  (import check only)

    ck = torch.load(act.cfg.checkpoint or __import__("os").environ["QUADCOOP_WALKER_CKPT"],
                    map_location=device, weights_only=False)
    sd = ck["actor_state_dict"]
    x = torch.randn(64, act.walker.obs_dim, device=device)
    ref = (x - sd["obs_normalizer._mean"]) / (sd["obs_normalizer._std"] + 1e-2)
    i = 0
    while f"mlp.{i}.weight" in sd:
        ref = ref @ sd[f"mlp.{i}.weight"].T + sd[f"mlp.{i}.bias"]
        if f"mlp.{i + 2}.weight" in sd:
            ref = torch.nn.functional.elu(ref)
        i += 2
    err = (act.walker(x) - ref).abs().max().item()
    check(err < 1e-5, f"rebuilt walker matches the checkpoint's MLP (max err {err:.1e})")
    try:
        from dataclasses import asdict

        from mjlab.rl import MjlabOnPolicyRunner, RslRlVecEnvWrapper
        from mjlab.tasks.registry import load_rl_cfg

        wtask = a.task.replace("Push", "Walker")
        wcfg = load_env_cfg(wtask)
        wcfg.scene.num_envs = 2
        wenv = RslRlVecEnvWrapper(ManagerBasedRlEnv(cfg=wcfg, device=device))
        runner = MjlabOnPolicyRunner(wenv, asdict(load_rl_cfg(wtask)), device=device)
        runner.load(act.cfg.checkpoint or __import__("os").environ["QUADCOOP_WALKER_CKPT"],
                    load_cfg={"actor": True}, strict=True, map_location=device)
        pol = runner.get_inference_policy(device=device)
        from tensordict import TensorDict

        y = pol(TensorDict({"actor": x}, batch_size=[64]))
        err2 = (act.walker(x) - y).abs().max().item()
        check(err2 < 1e-4, f"... and rsl_rl's own inference policy (max err {err2:.1e})")
        wenv.close()
    except Exception as e:  # noqa: BLE001
        print(f"       (skipped rsl_rl comparison: {e})")

    # [2] walker observation ------------------------------------------------------------
    print("\n[2] walker observation")
    wterms = env.observation_manager.active_terms["walker"]
    check(wterms == ["base_lin_vel", "base_ang_vel", "projected_gravity", "joint_pos",
                     "joint_vel", "actions", "command"],
          f"walker obs terms in training order: {wterms}")
    wobs = env.observation_manager.compute_group("walker")
    check(wobs.shape[-1] == act.walker.obs_dim, f"walker obs is {wobs.shape[-1]} dims, "
          f"checkpoint expects {act.walker.obs_dim}")
    a3 = torch.tensor([[1.0, -1.0, 0.5]], device=device).repeat(a.envs, 1)
    env.step(a3)
    wobs = env.observation_manager.compute_group("walker")
    nj = act.walker.act_dim
    cmd_slice = wobs[:, -3:]
    check(torch.allclose(cmd_slice, twist.vel_command_b), "walker's command term = high-level command")
    check(torch.allclose(wobs[:, -3 - nj:-3], act.walker_action),
          "walker's 'actions' term = its own last joint action (not the 3-dim high-level action)")
    tgt = act.target_command(a3)
    check(bool((tgt[:, 0] <= act.cfg.vx_range[1] + 1e-6).all()) and
          bool((tgt[:, 1] >= act.cfg.vy_range[0] - 1e-6).all()),
          f"high-level action maps into the walker's command ranges (e.g. {tgt[0].tolist()})")

    # [3] scene geometry ----------------------------------------------------------------
    print("\n[3] scene: box, goal, marker")
    env.reset()
    env.step(torch.zeros(a.envs, 3, device=device))
    rp = robot.data.root_link_pos_w[:, :2]
    ryaw = mdp.yaw_of(robot.data.root_link_quat_w)
    u = torch.stack([torch.cos(ryaw), torch.sin(ryaw)], -1)
    bp = goal.box_pos()[:, :2]
    ahead_box = ((bp - rp) * u).sum(-1)
    ahead_goal = ((goal.goal_xy - bp) * u).sum(-1)
    check(bool((ahead_box > 0.6).all()), f"box ahead of the robot ({ahead_box.min():.2f}-{ahead_box.max():.2f} m)")
    check(bool((ahead_goal > 0.5).all()), f"goal ahead of the box ({ahead_goal.min():.2f}-{ahead_goal.max():.2f} m)")
    bq = goal.box_quat()
    check(bool((mdp.tilt_of(bq) < math.radians(2)).all()), "box upright (rotations are about z only)")
    for s, g in enumerate(goal.goals):
        mp = env.sim.data.mocap_pos[:, g.indexing.mocap_id] if hasattr(env.sim.data, "mocap_pos") else None
        if mp is None:
            break
        mine = goal.shape == s
        if mine.any():
            check(torch.allclose(mp[mine, :2], goal.goal_xy[mine], atol=1e-4)
                  and bool((mp[mine, 2] > 0).all()),
                  f"green {SHAPES[s].name} marker sits on the goal")
            mq = env.sim.data.mocap_quat[:, g.indexing.mocap_id][mine]
            check(torch.allclose(mdp.tilt_of(mq), torch.zeros_like(mq[:, 0]), atol=1e-5)
                  and torch.allclose(mdp.wrap(mdp.yaw_of(mq) - goal.goal_yaw[mine]),
                                     torch.zeros_like(mq[:, 0]), atol=1e-4),
                  f"  ... with the goal yaw, rotated only in the xy-plane")
        if (~mine).any():
            check(bool((mp[~mine, 2] < -1).all()), f"  other marker hidden where the box is not a {SHAPES[s].name}")
    # symmetry folding
    e = torch.tensor([0.0, math.pi / 2, math.pi, 1.0], device=device)
    f4 = mdp.sym_error(e, torch.full_like(e, 4.0))
    f2 = mdp.sym_error(e, torch.full_like(e, 2.0))
    check(abs(f4[1]) < 1e-6 and abs(f4[2]) < 1e-6 and abs(f2[2]) < 1e-6 and abs(abs(f2[1]) - math.pi / 2) < 1e-6,
          "yaw error folded by symmetry (cube: 90 deg = done; long box: 180 deg = done, 90 deg not)")
    d, err = goal.errors()
    lvl0 = goal.cfg.levels[0]
    check(bool((d > lvl0[0] - 0.5).all()) and bool((d < math.hypot(lvl0[1], lvl0[2]) + 0.5).all()),
          f"level-0 goal distance {d.min():.2f}-{d.max():.2f} m")
    check(bool((err.abs() < math.radians(lvl0[3]) + 0.2).all()),
          f"level-0 yaw change <= {lvl0[3]:.0f} deg (+ box jitter): max {math.degrees(err.abs().max()):.1f}")

    # [4] closed loop ------------------------------------------------------------------
    print("\n[4] closed loop")
    q0 = robot.data.joint_pos.clone()
    nan = False
    for _ in range(25):
        o, r, term, trunc, _ = env.step(torch.tensor([[0.8, 0.0, 0.0]], device=device).repeat(a.envs, 1))
        nan |= bool(torch.isnan(o["actor"]).any() or torch.isnan(r).any())
    moved = (robot.data.joint_pos - q0).abs().max().item()
    check(not nan, "no NaNs in observations or rewards")
    check(moved > 0.05, f"walker moves the joints (max change {moved:.2f} rad)")
    settled = env.episode_length_buf > 10  # envs that did not just reset
    check(bool(settled.any()) and bool((twist.vel_command_b[settled, 0] > 0.6).all()),
          f"smoothed command follows the high-level action ({int(settled.sum())} settled envs)")
    print(f"       actor obs {o['actor'].shape[-1]} dims, critic {o['critic'].shape[-1]} dims")

    # [5] curriculum ------------------------------------------------------------------
    print("\n[5] curriculum")
    ids = torch.arange(a.envs, device=device)
    goal.env_level[:] = goal.level
    goal.metrics["success"][:] = 1.0
    start = goal.level
    env.common_step_counter = 1000 * 24
    for _ in range(40):
        mdp.push_curriculum(env, ids, ema=0.5)
        env.common_step_counter += 60 * 24
        goal.env_level[:] = goal.level
    check(goal.level > start, f"level rises with success: {start} -> {goal.level}")
    opened = goal.mass_window == goal.cfg.mass_window_final
    check(opened, f"mass window opens after the task is learned: {goal.mass_window} kg")
    goal.metrics["success"][:] = 0.0
    top = goal.level
    for _ in range(5):
        mdp.push_curriculum(env, ids, ema=0.5)
        env.common_step_counter += 60 * 24
        goal.env_level[:] = goal.level
    check(goal.level < top, f"and falls on failure: {top} -> {goal.level}")

    env.close()
    print()
    if FAILS:
        print(f"FAILED ({len(FAILS)})")
        return 1
    print("All Stage 1 checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())