"""Spot + arm pilot, port acceptance (GPU): RAI's walker in QuadCoop's simulator (mjlab / MuJoCo Warp).

    python scripts/spot_arm/warp_check.py [--copies 16] [--out evals/spot_arm/warp_check.json]

The CPU tracking cases of walker_check.py (stand, forward 0.5 / 1.0, lateral 0.3, turn 0.5; arm stowed and out;
forward 0.5 with the arm sweeping), --copies envs each, under two timings, both 50 Hz control:
  rai       timestep 0.01 x 2 substeps (the walker's own)
  quadcoop  timestep 0.005 x 4 (QuadCoop's push envs: the timing a mixed ANYmal + Spot scene would use)
Pass per timing: no falls, and mean achieved velocity within 0.1 (m/s, rad/s) of the command in every case.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

CASES = [("stand", (0, 0, 0)), ("forward 0.5", (0.5, 0, 0)), ("forward 1.0", (1.0, 0, 0)), ("lateral 0.3", (0, 0.3, 0)),
         ("turn 0.5", (0, 0, 0.5))]


def run(timestep: float, decimation: int, copies: int, device: str) -> list[dict]:
    from mjlab.envs import ManagerBasedRlEnv, ManagerBasedRlEnvCfg
    from mjlab.envs.mdp import joint_pos_rel
    from mjlab.envs.mdp.actions import JointPositionActionCfg
    from mjlab.managers.observation_manager import ObservationGroupCfg, ObservationTermCfg
    from mjlab.scene import SceneCfg
    from mjlab.sim import MujocoCfg, SimulationCfg
    from mjlab.terrains import TerrainEntityCfg

    from quadcoop.robots import spot_arm as sa

    cases = [(arm, name, vel) for arm in ("stowed", "out") for name, vel in CASES] + [("out", "forward 0.5, arm sweeping", (0.5, 0, 0))]
    n = len(cases) * copies
    cfg = ManagerBasedRlEnvCfg(
        scene=SceneCfg(terrain=TerrainEntityCfg(terrain_type="plane"), entities={"robot": sa.get_robot_cfg()},
                       num_envs=n, env_spacing=4.0),
        observations={"actor": ObservationGroupCfg(terms={"q": ObservationTermCfg(func=joint_pos_rel)})},
        actions={"joints": JointPositionActionCfg(entity_name="robot", actuator_names=(".*",), scale=1.0,
                                                  use_default_offset=False)},
        sim=SimulationCfg(mujoco=MujocoCfg(timestep=timestep), njmax=300),
        decimation=decimation, episode_length_s=1e5)
    env = ManagerBasedRlEnv(cfg=cfg, device=device)
    dev = env.device
    robot = env.scene["robot"]
    walker = sa.RaiWalker(robot, dev)
    env.reset()
    idx = torch.arange(n, device=dev) // copies
    vel = torch.tensor([c[2] for c in cases], device=dev, dtype=torch.float32)[idx]
    arm = torch.tensor([sa.ARM_STOWED if c[0] == "stowed" else sa.ARM_OUT for c in cases], device=dev)[idx]
    sweep = torch.tensor(["sweeping" in c[1] for c in cases], device=dev)[idx]
    dt = env.step_dt
    assert abs(dt - 0.02) < 1e-9, dt
    acc = torch.zeros(n, 3, device=dev)
    cnt = 0
    fell = torch.zeros(n, dtype=torch.bool, device=dev)
    stow = torch.tensor(sa.ARM_STOWED, device=dev).expand(n, 7)
    for k in range(500):  # 0-1.5 s: the arm moves from stowed to its pose; 2 s: the command; last 3 s measured
        t = k * dt
        a = stow + min(1.0, t / 1.5) * (arm - stow)
        if t >= 2.0:
            a[:, 0] = torch.where(sweep, torch.full_like(a[:, 0], 0.8 * math.sin(2 * math.pi * 0.25 * (t - 2))), a[:, 0])
            a[:, 1] = torch.where(sweep, torch.full_like(a[:, 1], -0.9 + 0.4 * math.sin(2 * math.pi * 0.2 * (t - 2))), a[:, 1])
        cmd = walker.command(vel if t >= 2.0 else torch.zeros_like(vel), a)
        env.step(walker.targets(cmd))
        d = robot.data
        fell |= (d.root_link_pos_w[:, 2] < 0.25) | (d.projected_gravity_b[:, 2] > -0.5)
        if t >= 7.0:
            acc += torch.cat([d.root_link_lin_vel_b[:, :2], d.root_link_ang_vel_b[:, 2:3]], -1)
            cnt += 1
    got = (acc / cnt).view(len(cases), copies, 3).mean(1)
    fl = fell.view(len(cases), copies).float().mean(1)
    h = robot.data.root_link_pos_w[:, 2].view(len(cases), copies).mean(1)
    rows = []
    for i, (arm_name, name, v) in enumerate(cases):
        err = float(torch.linalg.norm(got[i] - torch.tensor(v, device=dev, dtype=torch.float32)))
        rows.append({"arm": arm_name, "case": name, "cmd": list(v), "achieved": [round(float(x), 3) for x in got[i]],
                     "error": round(err, 3), "fell_share": round(float(fl[i]), 3), "height": round(float(h[i]), 3)})
    env.close()
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--copies", type=int, default=16)
    ap.add_argument("--out", default="evals/spot_arm/warp_check.json")
    a = ap.parse_args()
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    rep, ok_all = {}, True
    for name, ts, dec in (("rai", 0.01, 2), ("quadcoop", 0.005, 4)):
        rows = run(ts, dec, a.copies, device)
        ok = all(r["fell_share"] == 0 and r["error"] <= 0.1 for r in rows)
        rep[name] = {"timestep": ts, "decimation": dec, "pass": ok, "cases": rows}
        ok_all &= ok
        print(f"== timing {name} (timestep {ts}, x{dec}): {'PASS' if ok else 'FAIL'}")
        for r in rows:
            print(f"  arm {r['arm']:6s} {r['case']:26s} cmd {r['cmd']} got {r['achieved']} err {r['error']:.3f} "
                  f"fell {r['fell_share']:.2f} h {r['height']:.2f}")
    rep["pass"] = ok_all
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(rep, indent=1))
    return 0 if ok_all else 1


if __name__ == "__main__":
    raise SystemExit(main())
