#!/usr/bin/env python3
"""Check that everything builds and the disturbances do what they claim. No checkpoint needed.

    python scripts/smoke_test.py            # GPU if visible, else CPU (slow but works)
    python scripts/smoke_test.py --quick    # fewer steps

For each walker task (ANYmal C, Spot):
  1. the env builds and steps without NaNs;
  2. the actor observation has NO force term and the critic has a 3-d one;
  3. the push force actually turns on, stays horizontal, and has the planned size;
  4. the box lands in front of the robot when told to, and is parked otherwise.

Then the day-one check for Stage 2: ANYmal C + Spot + a box in ONE scene.
Exit code 0 = all passed.
"""

from __future__ import annotations

import argparse
import gc
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import torch  # noqa: E402

FAILS: list[str] = []


def check(ok: bool, msg: str) -> None:
    print(f"  {'ok  ' if ok else 'FAIL'} {msg}")
    if not ok:
        FAILS.append(msg)


def build(cfg, num_envs: int, device: str):
    from mjlab.envs import ManagerBasedRlEnv

    cfg.scene.num_envs = num_envs
    return ManagerBasedRlEnv(cfg=cfg, device=device)


def test_walker(task_id: str, device: str, steps: int) -> None:
    from mjlab.tasks.registry import load_env_cfg

    print(f"\n[{task_id}]")
    cfg = load_env_cfg(task_id)
    # Make the force arrive quickly and at full curriculum scale.
    pf = cfg.commands["push_force"]
    pf.gap_s, pf.ramp_s, pf.hold_s = (0.0, 0.1), (0.1, 0.2), (2.0, 3.0)
    pf.curriculum_start_scale = 1.0
    # Half the envs get a box in the path.
    cfg.events["box_reset"].params["p_in_path"] = 0.5
    cfg.events.pop("box_interval")
    cfg.events.pop("push_robot")

    env = build(cfg, 8, device)
    obs, _ = env.reset()
    actor_dim = obs["actor"].shape[-1]
    critic_dim = obs["critic"].shape[-1]
    term_names = env.observation_manager.active_terms
    check("push_force" not in term_names["actor"], f"actor has no force term (dim {actor_dim})")
    check("push_force" in term_names["critic"], f"critic has push_force (dim {critic_dim})")

    robot = env.scene["robot"]
    box = env.scene["box"]
    term = env.command_manager.get_term("push_force")
    print(f"       robot mass {term.robot_weight_n / 9.81:.1f} kg, "
          f"peak force {pf.max_frac_of_weight * term.robot_weight_n:.0f} N")

    # Box placement right after reset.
    rel = box.data.root_link_pos_w[:, :2] - robot.data.root_link_pos_w[:, :2]
    dist = torch.linalg.norm(rel, dim=-1)
    near = dist < 3.0
    check(bool(near.any()) and bool((~near).any()),
          f"box near robot in {int(near.sum())}/8 envs, parked in the rest")
    if near.any():
        check(bool((dist[near] > cfg.events["box_reset"].params["robot_half_length"]).all()),
              f"near boxes start clear of the body (min {dist[near].min():.2f} m)")

    max_force, max_fz, nan = 0.0, 0.0, False
    zero = torch.zeros(env.action_space.shape, device=device)
    for _ in range(steps):
        obs, *_ = env.step(zero)
        f = term.applied_force_yaw
        max_force = max(max_force, float(torch.linalg.norm(f, dim=-1).max()))
        max_fz = max(max_fz, float(f[:, 2].abs().max()))
        nan |= bool(torch.isnan(obs["actor"]).any())
    check(not nan, "no NaNs in observations")
    check(max_force > 0.0, f"push force turned on (max {max_force:.0f} N)")
    check(max_fz == 0.0, "push force is horizontal")
    check(max_force <= pf.max_frac_of_weight * term.robot_weight_n + 1e-3,
          "push force within the configured peak")
    env.close()
    del env
    gc.collect()


def test_two_robot_scene(device: str, steps: int) -> None:
    """ANYmal C + Spot + box in one MuJoCo world: the Stage 2 scene, built early."""
    from mjlab.tasks.registry import load_env_cfg

    from quadcoop.robots.spot import ROBOT as SPOT

    print("\n[two-robot scene: ANYmal C + Spot + box]")
    cfg = load_env_cfg("QuadCoop-Walker-AnymalC", play=True)
    spot = SPOT.get_robot_cfg()
    spot.init_state.pos = (0.0, 3.0, 0.46)  # Beside ANYmal, clear of the box spot.
    cfg.scene.entities["spot"] = spot
    env = build(cfg, 2, device)
    env.reset()
    # Only ANYmal has an action term here; hold Spot's PD targets at its stance.
    spot_data = env.scene["spot"].data
    spot_data.joint_pos_target[:] = spot_data.default_joint_pos
    names = list(env.scene.entities.keys())
    check({"robot", "spot", "box"} <= set(names), f"entities present: {names}")
    model = env.sim.mj_model
    spot_geoms = [model.geom(i).name for i in range(model.ngeom)
                  if model.geom(i).name.startswith("spot/")]
    check(any(n.endswith("body_collision") for n in spot_geoms),
          "Spot's body collision mesh is in the scene (prefixed 'spot/')")
    zero = torch.zeros(env.action_space.shape, device=device)
    for _ in range(steps):
        env.step(zero)
    finite = all(bool(torch.isfinite(env.scene[k].data.root_link_pos_w).all())
                 for k in ("robot", "spot", "box"))
    check(finite, "ANYmal, Spot and box simulate together without NaNs")
    z = env.scene["spot"].data.root_link_pos_w[:, 2]
    check(bool((z > 0.3).all()), f"Spot still standing on its held stance (base z {z.min():.2f} m)")
    env.close()
    del env
    gc.collect()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--device", default=None)
    args = ap.parse_args()
    device = args.device or ("cuda:0" if torch.cuda.is_available() else "cpu")
    steps = 40 if args.quick else 150
    print(f"device: {device}")

    try:
        import mjlab  # noqa: F401
        import quadcoop
    except Exception as e:  # noqa: BLE001
        print(f"  FAIL import: {type(e).__name__}: {e}")
        return 1
    for name, xml in (("anymal_c", "anymal_c.xml"), ("spot", "spot.xml")):
        path = Path(quadcoop.__file__).parent / "assets" / name / xml
        check(path.exists(), f"asset {name} present")
    if FAILS:
        print("Run `python scripts/fetch_assets.py` first.")
        return 1

    for task_id in quadcoop.TASKS:
        test_walker(task_id, device, steps)
    test_two_robot_scene(device, steps)

    print()
    if FAILS:
        print(f"FAILED ({len(FAILS)}):")
        for f in FAILS:
            print(f"  - {f}")
        return 1
    print("All smoke checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
