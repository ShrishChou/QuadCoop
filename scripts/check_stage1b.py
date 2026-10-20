"""Checks for the Stage 1b env (ten shapes, random starts, held success).

    QUADCOOP_WALKER_CKPT=<walker.pt> python scripts/check_stage1b.py --task QuadCoop-PushHard-AnymalC
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
    ap.add_argument("--envs", type=int, default=96)
    ap.add_argument("--device", default=None)
    a = ap.parse_args()
    device = a.device or ("cuda:0" if torch.cuda.is_available() else "cpu")

    import quadcoop  # noqa: F401
    import quadcoop.stage1  # noqa: F401
    import quadcoop.stage1b  # noqa: F401
    from mjlab.envs import ManagerBasedRlEnv
    from mjlab.tasks.registry import load_env_cfg

    from quadcoop.stage1.mdp import wrap
    from quadcoop.stage1b import mdp
    from quadcoop.stage1b.shapes import SHAPES

    cfg = load_env_cfg(a.task)
    cfg.scene.num_envs = a.envs
    cfg.commands["goal"].start_level = len(cfg.commands["goal"].levels) - 1  # hardest, all masses
    cfg.commands["goal"].replay_frac = 0.0
    env = ManagerBasedRlEnv(cfg=cfg, device=device)
    env.reset()
    g = env.command_manager.get_term("goal")
    robot = env.scene["robot"]
    zero = torch.zeros(a.envs, 3, device=device)
    env.step(zero)

    print("\n[1] spawning")
    present = sorted({SHAPES[int(k)].name for k in g.shape})
    check(len(present) >= 8, f"{len(present)}/10 shapes in {a.envs} envs: {present}")
    # no object overlapping the robot or another object at the start
    mjm = env.sim.mj_model
    names = [mjm.geom(i).name for i in range(mjm.ngeom)]
    wd = env.sim.data
    n = int(wd.nacon.cpu().numpy().reshape(-1)[0]) if hasattr(wd, "nacon") else 0
    bad = 0
    if n:
        geom = wd.contact.geom.cpu().numpy()[:n]
        for g0, g1 in geom:
            a0, a1 = names[g0], names[g1]
            if a0.startswith("obj_") and (a1.startswith("robot/") or a1.startswith("obj_")):
                bad += 1
            if a1.startswith("obj_") and a0.startswith("robot/"):
                bad += 1
    check(bad == 0, f"no object touches the robot or another object at the start ({bad} contacts)")
    d, e = g.errors()
    t = g.table[g.env_level]
    check(bool((d >= t[:, mdp.D_LO] - 0.05).all()) and bool((d <= t[:, mdp.D_HI] + 0.05).all()),
          f"goal distances {d.min():.2f}-{d.max():.2f} m inside the level's range")
    sph = g.symmetry() == 0
    check(bool((e[sph] == 0).all()) if sph.any() else True, "sphere: any heading counts (yaw error 0)")
    tilt_ok = ~g.tipped(5.0)
    check(bool(tilt_ok.all()), "every object starts upright (lying cylinder on its side)")

    print("\n[2] resting and markers")
    p0 = g.box_pos().clone()
    h0 = g.heading().clone()
    for _ in range(25):
        env.step(zero)
    alive = env.episode_length_buf > 20
    moved = torch.linalg.norm(g.box_pos() - p0, dim=-1)[alive & ~g.roller[g.shape]]
    check(moved.numel() == 0 or float(moved.max()) < 0.05,
          f"non-rolling objects rest (max drift {float(moved.max()) if moved.numel() else 0:.3f} m)")
    dh = wrap(g.heading() - h0).abs()[alive & ~g.roller[g.shape]]
    check(dh.numel() == 0 or float(dh.max()) < 0.05, "and keep their heading")
    for k, goal in enumerate(g.goals):
        mine = g.shape == k
        mp = env.sim.data.mocap_pos[:, goal.indexing.mocap_id]
        if mine.any():
            check(torch.allclose(mp[mine, :2], g.goal_xy[mine], atol=1e-4) and bool((mp[mine, 2] > 0).all())
                  and bool((mp[~mine, 2] < -1).all()), f"green {SHAPES[k].name} marker on its goal, hidden elsewhere")

    print("\n[3] folding, held success, curriculum")
    e = torch.tensor([math.pi / 2, math.pi, 0.3], device=device)
    f1 = mdp.fold(e, torch.full_like(e, 1.0))
    f0 = mdp.fold(e, torch.full_like(e, 0.0))
    check(torch.allclose(f1.abs(), torch.tensor([math.pi / 2, math.pi, 0.3], device=device)) and bool((f0 == 0).all()),
          "L/T/arch need the full heading; sphere none")
    g.in_goal_time[:] = 0.0
    g.metrics["success"][:] = 0.0
    g.goal_xy[:] = g.box_pos()[:, :2] + 3.0  # far from the goal
    g._update_metrics()
    check(not bool(g.metrics["success"].any()), "no success while the object is away from the goal")
    hold = g._tol()[2]
    check(float(hold.max()) >= 1.0, f"hardest level needs a {float(hold.max()):.1f} s hold")
    obs = env.observation_manager.compute_group("actor")
    check(not bool(torch.isnan(obs).any()), f"actor observation finite ({obs.shape[-1]} dims)")
    g.level = 0
    g.env_level[:] = 0
    g.metrics["success"][:] = 1.0
    env.common_step_counter = 10_000 * 24
    ids = torch.arange(a.envs, device=device)
    for _ in range(30):
        mdp.hard_curriculum(env, ids, ema=0.5)
        env.common_step_counter += 100 * 24
        g.env_level[:] = g.level
    check(g.level == len(g.cfg.levels) - 1, f"levels climb with success: 0 -> {g.level}")
    env.close()
    print()
    if FAILS:
        print(f"FAILED ({len(FAILS)})")
        return 1
    print("All Stage 1b checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())