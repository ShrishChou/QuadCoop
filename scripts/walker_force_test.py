"""Test A: can the frozen walker push at distinct, sustained force levels? No planner, no learned executor.

Everything above the walker (the planner's force split, any future push-effort command) assumes a
robot can be made to press harder or softer. The walker only takes velocity commands. This test
puts one ANYmal squarely in front of a cube face (the other robot parked 40 m away), commands a
fixed forward speed, and measures the contact force it then sustains on the object:

    speeds    commanded forward speed (m/s); the walker accepts -0.6..0.8
    offsets   the robot's heading relative to the face normal (deg): 0 = square on, 15 / 30 = at an angle
    masses    5000 kg (immovable: the force the robot can hold against a wall) and movable masses

Each case starts 10 cm short of the face, settles 0.4 s, then walks in at the commanded speed for
--duration s. Measured from --measure-from s on: the force on the object along the face normal (N),
its spread over time (sustained = a steady level, not taps), the share of time touching (> 5 N),
the force direction relative to the robot's heading, the robot's sideways drift and turn, whether it
fell, and (movable masses) how fast the object moved.

Output: logs/evals/<name>/cases.csv and evals/<name>/ (summary.md, summary.json).

    python scripts/walker_force_test.py                       # 8 speeds x 3 angles x 4 masses x 3 repeats
    python scripts/walker_force_test.py --masses 5000 --name wf-quick --reps 1
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
import time
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

TOUCH_N = 5.0  # N: touching
FELL_Z = 0.25  # m: base below this = fallen


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", default="wf-test")
    ap.add_argument("--speeds", default="0.05,0.1,0.2,0.3,0.4,0.5,0.6,0.8")
    ap.add_argument("--offsets", default="0,15,30", help="deg between the robot's heading and the face normal")
    ap.add_argument("--masses", default="5000,80,40,20")
    ap.add_argument("--reps", type=int, default=3, help="repeats per case (small start jitter)")
    ap.add_argument("--duration", type=float, default=6.0)
    ap.add_argument("--measure-from", type=float, default=3.0)
    ap.add_argument("--device", default=None)
    ap.add_argument("--debug", action="store_true", help="print env 0 as it goes")
    a = ap.parse_args()

    from train_coop2 import resolve_models, set_env

    set_env(resolve_models("b", "anymal"))
    import numpy as np
    import torch

    import quadcoop  # noqa: F401
    from mjlab.envs import ManagerBasedRlEnv

    from quadcoop import contacts as C
    from quadcoop.coop2 import mdp as cm
    from quadcoop.coop2.env_cfg import AGENTS, FRICTION_RANGE, make_coop2_env_cfg
    from quadcoop.stage1b.shapes import NOMINAL_MASS
    from quadcoop.stage2 import mdp as m2
    from quadcoop.stage2.shapes import OBJ_NAMES2, SHAPE_NAMES2, kinds_tensor, nominal_parts

    device = a.device or ("cuda:0" if torch.cuda.is_available() else "cpu")
    speeds = [float(x) for x in a.speeds.split(",")]
    offsets = [float(x) for x in a.offsets.split(",")]
    masses = [float(x) for x in a.masses.split(",")]
    # the cube's face facing -x: its centre contact (normal (-1, 0))
    s_cube = SHAPE_NAMES2.index("cube")
    parts, rest = nominal_parts("cpu")
    cl = C.candidates(parts[s_cube].numpy(), kinds_tensor("cpu")[s_cube].numpy(), float(rest[s_cube]))
    face = min(cl, key=lambda c: np.linalg.norm(np.asarray(c.n) - np.array([-1.0, 0.0])) + abs(c.p[1]))
    px = float(face.p[0])
    print(f"cube face at x = {px:.3f} m (contact {face.index}, normal {np.round(face.n, 2)})", flush=True)

    out_logs = ROOT / "logs" / "evals" / a.name
    out_logs.mkdir(parents=True, exist_ok=True)
    rows = []
    t0 = time.time()
    for mass in masses:
        cases = [(v, off, r) for v in speeds for off in offsets for r in range(a.reps)]
        n = len(cases)
        cfg = make_coop2_env_cfg("b", play=True, partner_map=True, reward_set="r7", contacts=True, guide=True,
                                 wrench=True, expert=True, push_cmd=True, reselect_s=(0.0, 0.0), reselect_min_dist=0.0)
        cfg.scene.num_envs = n
        cfg.episode_length_s = 1e5
        cfg.terminations = {}
        alpha = 0.5 * math.log(mass / NOMINAL_MASS)
        mid = 0.5 * (FRICTION_RANGE[0] + FRICTION_RANGE[1])
        for nm in OBJ_NAMES2:
            cfg.events[f"{nm}_mass"].params["alpha_range"] = (alpha, alpha)
            if f"{nm}_friction" in cfg.events:
                cfg.events[f"{nm}_friction"].params["ranges"] = (mid, mid)
        torch.manual_seed(0)
        env = ManagerBasedRlEnv(cfg=cfg, device=device)
        g = env.command_manager.get_term("goal")
        dev = env.device
        ar = torch.arange(n, device=dev)
        for k in range(len(SHAPE_NAMES2)):
            m2.apply_geometry(env, ar, k, torch.ones(n, 3, device=dev))
        z = torch.zeros(n, device=dev)
        sc = {"shape": torch.full((n,), s_cube, dtype=torch.long, device=dev), "obj_xy_rel": torch.zeros(n, 2, device=dev),
              "obj_heading": z.clone(), "goal_xy_rel": torch.stack([z + 3.0, z], -1), "goal_yaw": z.clone(),
              "bearings": [z + math.pi, z + math.pi], "gaps": [z + 0.6, z + 0.6], "yaw_noise": [z, z],
              "park": [torch.zeros(n, dtype=torch.bool, device=dev), torch.ones(n, dtype=torch.bool, device=dev)],
              "contact_rule": torch.full((n,), 3, dtype=torch.long, device=dev),
              "contact_idx": torch.full((n, 2), -1, dtype=torch.long, device=dev)}
        g.scenario = lambda ids: {k: ([x[ids] for x in v] if isinstance(v, list) else v[ids]) for k, v in sc.items()}
        env.reset()
        g.scenario = None
        rob = env.scene[AGENTS[0]]
        reach = float(g.reach[AGENTS[0]])
        if a.debug:
            print("[debug] after reset: robot z", float(rob.data.root_link_pos_w[0, 2]), "xy", g.robot_xy(0)[0].tolist(),
                  "parked robot z", float(env.scene[AGENTS[1]].data.root_link_pos_w[0, 2]), "reach", reach, flush=True)
        # place robot 1: its front 10 cm short of the face centre (+ a little jitter), heading `offset` off the normal
        gen = torch.Generator(device="cpu").manual_seed(1)
        off = torch.deg2rad(torch.tensor([c[1] for c in cases], device=dev))
        jit = (torch.rand(n, 2, generator=gen) - 0.5).to(dev) * torch.tensor([0.04, 0.06], device=dev)
        obj0 = g.box_pos()[:, :2].clone()
        tip = obj0 + torch.stack([z + px - 0.10, z], -1) + jit
        ctr = tip - reach * torch.stack([torch.cos(off), torch.sin(off)], -1)
        pose = rob.data.root_link_pose_w.clone()
        pose[:, 0:2] = ctr
        pose[:, 3:7] = torch.stack([torch.cos(off / 2), z, z, torch.sin(off / 2)], -1)  # w x y z
        rob.write_root_link_pose_to_sim(pose)
        rob.write_root_link_velocity_to_sim(torch.zeros(n, 6, device=dev))
        lo = torch.tensor([-0.6, -0.5, -0.7], device=dev)
        hi = torch.tensor([0.8, 0.5, 0.7], device=dev)
        to_act = lambda tw: 2.0 * (tw - lo) / (hi - lo) - 1.0  # noqa: E731
        vcmd = torch.tensor([c[0] for c in cases], device=dev)
        act_go = torch.zeros(n, env.action_manager.total_action_dim, device=dev)
        act_go[:, 0:3] = to_act(torch.stack([vcmd, z, z], -1))
        act_go[:, 3:6] = to_act(torch.zeros(n, 3, device=dev))
        act_stop = act_go.clone()
        act_stop[:, 0:3] = to_act(torch.zeros(n, 3, device=dev))
        dt = env.step_dt
        for _ in range(int(round(0.4 / dt))):
            env.step(act_stop)
        steps = int(round(a.duration / dt))
        w0 = int(round(a.measure_from / dt))
        acc = defaultdict(lambda: torch.zeros(n, device=dev))
        fn_hist = []
        fell = torch.zeros(n, dtype=torch.bool, device=dev)
        s_xy = s_yaw = s_obj = None
        if a.debug:
            print("[debug] after settle: robot", g.robot_xy(0)[0].tolist(), "yaw", float(g.robot_yaw(0)[0]), "z",
                  float(rob.data.root_link_pos_w[0, 2]), "object", g.box_pos()[0].tolist(), "target tip", tip[0].tolist(),
                  "vel cmd", env.command_manager.get_term(f"twist_{AGENTS[0]}").vel_command_b[0].tolist(), flush=True)
        for i in range(steps):
            env.step(act_go)
            if a.debug and i % 25 == 0:
                print(f"[debug] t {i * dt:.1f} robot {g.robot_xy(0)[0].tolist()} front {g.front_point(AGENTS[0])[0].tolist()} "
                      f"force {cm.object_force_from(env, AGENTS[0])[0].tolist()} cmd "
                      f"{env.command_manager.get_term(f'twist_{AGENTS[0]}').vel_command_b[0].tolist()}", flush=True)
            fell |= rob.data.root_link_pos_w[:, 2] < FELL_Z
            if i == w0:
                s_xy = g.robot_xy(0).clone()
                s_yaw = g.robot_yaw(0).clone()
                s_obj = g.box_pos()[:, :2].clone()
            if i >= w0:
                f = cm.object_force_from(env, AGENTS[0])  # (n, 2) on the object, world
                fn = f[:, 0]  # along the face normal, into the object (+x)
                yaw = g.robot_yaw(0)
                fmag = torch.linalg.norm(f, dim=-1)
                fang = torch.atan2(f[:, 1], f[:, 0]) - yaw
                acc["fn"] += fn
                acc["fn2"] += fn * fn
                acc["fmag"] += fmag
                acc["touch"] += (fmag > TOUCH_N).float()
                acc["cosh"] += torch.where(fmag > TOUCH_N, torch.cos(fang), torch.zeros_like(fmag))
                fn_hist.append(fn.clone())
        k = max(1, steps - w0)
        T = (steps - 1 - w0) * dt
        H = torch.stack(fn_hist, 0)  # (k, n)
        mean = acc["fn"] / k
        std = torch.sqrt((acc["fn2"] / k - mean * mean).clamp(min=0.0))
        p10 = torch.quantile(H, 0.1, dim=0)
        p90 = torch.quantile(H, 0.9, dim=0)
        side = (g.robot_xy(0) - s_xy)[:, 1]
        turn = torch.rad2deg(torch.atan2(torch.sin(g.robot_yaw(0) - s_yaw), torch.cos(g.robot_yaw(0) - s_yaw)))
        objv = torch.linalg.norm(g.box_pos()[:, :2] - s_obj, dim=-1) / max(T, 1e-6)
        for e, (v, o, r) in enumerate(cases):
            tf = float(acc["touch"][e]) / k
            rows.append({"mass": mass, "speed_cmd": v, "offset_deg": o, "rep": r,
                         "force_normal_mean": round(float(mean[e]), 1), "force_normal_std": round(float(std[e]), 1),
                         "force_normal_p10": round(float(p10[e]), 1), "force_normal_p90": round(float(p90[e]), 1),
                         "force_mag_mean": round(float(acc["fmag"][e]) / k, 1), "touching": round(tf, 3),
                         "force_vs_heading_cos": round(float(acc["cosh"][e]) / max(1, float(acc["touch"][e])), 3),
                         "side_drift_m": round(float(side[e]), 3), "turn_deg": round(float(turn[e]), 1),
                         "object_speed": round(float(objv[e]), 3), "fell": int(fell[e])})
        print(f"[{mass:g} kg] {n} cases ({time.time() - t0:.0f} s)", flush=True)
        env.close() if hasattr(env, "close") else None
        del env
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    with open(out_logs / "cases.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    summary, md = summarise(rows, speeds, offsets, masses, a)
    stats = ROOT / "evals" / a.name
    stats.mkdir(parents=True, exist_ok=True)
    (stats / "summary.md").write_text("\n".join(md) + "\n")
    (stats / "summary.json").write_text(json.dumps(summary, indent=1))
    with open(stats / "cases.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print("\n".join(md))
    return 0


def summarise(rows, speeds, offsets, masses, a):
    def cell(m, v, o):
        return [r for r in rows if r["mass"] == m and r["speed_cmd"] == v and r["offset_deg"] == o]

    mean = lambda xs: sum(xs) / len(xs) if xs else float("nan")  # noqa: E731
    md = [f"# Walker force test (test A): {a.name}", "",
          f"One ANYmal walking into a cube face at a fixed commanded speed; force on the object along the face normal, "
          f"measured from {a.measure_from:g} s to {a.duration:g} s. Each cell: mean force (N) over {a.reps} repeats; "
          f"in brackets its typical swing over time (std, N). 'sustained' = touching > 90% of the time and std < 30% of "
          f"the mean.", ""]
    summary = {"speeds": speeds, "offsets": offsets, "masses": masses, "cells": []}
    for m in masses:
        md += [f"## {m:g} kg" + (" (immovable: what the robot holds against a wall)" if m >= 1000 else ""), "",
               "| speed cmd (m/s) | " + " | ".join(f"{o:g} deg: force (swing)" for o in offsets) +
               " | touching | force along heading (cos) | fell | " + ("object speed (m/s) |" if m < 1000 else "turned (deg) |"),
               "|---" * (len(offsets) + 5) + "|"]
        for v in speeds:
            cells, extra = [], []
            for o in offsets:
                rs = cell(m, v, o)
                fm, sd = mean([r["force_normal_mean"] for r in rs]), mean([r["force_normal_std"] for r in rs])
                cells.append(f"{fm:.0f} ({sd:.0f})")
                summary["cells"].append({"mass": m, "speed": v, "offset": o, "force": fm, "swing": sd,
                                         "touching": mean([r["touching"] for r in rs]),
                                         "fell": mean([r["fell"] for r in rs]),
                                         "object_speed": mean([r["object_speed"] for r in rs]),
                                         "turn": mean([r["turn_deg"] for r in rs])})
            rs0 = [r for o in offsets for r in cell(m, v, o)]
            last = (f"{mean([r['object_speed'] for r in rs0]):.2f}" if m < 1000 else
                    " / ".join(f"{mean([r['turn_deg'] for r in cell(m, v, o)]):.0f}" for o in offsets))
            md.append(f"| {v:g} | " + " | ".join(cells) + f" | {mean([r['touching'] for r in rs0]):.2f} | "
                      f"{mean([r['force_vs_heading_cos'] for r in rs0]):.2f} | {mean([r['fell'] for r in rs0]):.2f} | {last} |")
        md.append("")
        # verdict per mass at 0 deg: distinct and sustained levels
        f0 = [mean([r["force_normal_mean"] for r in cell(m, v, offsets[0])]) for v in speeds]
        sus = [mean([float(r["touching"] > 0.9 and r["force_normal_std"] < 0.3 * max(r["force_normal_mean"], 1.0))
                     for r in cell(m, v, offsets[0])]) for v in speeds]
        mono = all(f0[i + 1] >= f0[i] - 15 for i in range(len(f0) - 1))
        spread = max(f0) - min(f0)
        verdict = ("DISTINCT LEVELS" if mono and spread >= 100 else "NOT DISTINCT") + \
                  f": {min(f0):.0f} to {max(f0):.0f} N across speeds ({'rising' if mono else 'not monotonic'}), " \
                  f"sustained in {mean(sus):.0%} of square-on cases"
        summary[f"verdict_{m:g}"] = verdict
        md += [f"**{m:g} kg, square on:** {verdict}.", ""]
    return summary, md


if __name__ == "__main__":
    sys.exit(main())
