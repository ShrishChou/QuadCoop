"""Walker acceptance test: one robot, its own walker environment, scripted commands. Runs any
number of walkers on identical cases (e.g. the v1 walker against the compliant v2) and checks
what the planner and executor above it need:

  free     open ground, no objects: forward / backward / sideways / turning commands from 0.02 to
           0.7 m/s (0.05-0.4 rad/s), standing still, and walking at 0.3 m/s while kicked every
           2 s. Achieved velocity (last half of each run), tracking error, falls.
           Pass: small commands (0.02-0.2) move the robot (>= half the commanded speed, error
           <= max(0.03, 30%)); normal commands error <= 0.1 m/s; no falls.
  wall     an immovable cube (3000 kg) 10 cm ahead, square on and at 20 deg; forward commands
           0.02-0.4 m/s. Push force on the object along the robot's heading, its swing over
           time (std), time touching. A compliant walker (stiffness k) should settle at k x speed.
           Pass: force within 25% of k x speed for 0.05-0.3 m/s, rising with speed, steady
           (swing <= 25% of the mean), touching >= 95% of the time.
  objects  a 20 / 40 / 80 kg cube 10 cm ahead, forward commands 0.1-0.5 m/s. Robot and object
           speed and force. A compliant walker should move at max(0, v - mu m g / k).
           Pass: robot speed within 0.05 m/s of that; no falls.

The verdicts are computed for every walker, so the v1 walker shows what it fails.

    python scripts/walker_test.py --walkers v1=logs/evals/walker-anymal-v1/model.pt,v2=logs/rsl_rl/walker_anymal_c_compliant/<run>/model_3000.pt
    python scripts/walker_test.py --walkers v1=logs/evals/walker-anymal-v1/model.pt --groups free --reps 1 --name wt-quick

Output: evals/<name>/ (summary.md, summary.json, cases.csv).

Videos (optional, first repeat of each chosen case, with the command / achieved velocity / force
written on top): --videos all, or a list of groups and case names, e.g.
    --videos yaw,side,wall          (free-walk turns and sideways steps, and every wall case)
    --videos fwd,objects
-> eval_videos/<name>/<walker>/<group>_<case>_<command>[...].mp4 (git-ignored; needs MUJOCO_GL=egl on the cluster).
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import subprocess
import sys
import time
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

FRICTION = 0.45  # objects: the middle of the training range (0.3-0.6)
GAP = 0.10  # m from the nose to the object face at the start of a push
TOUCH_N = 5.0


def free_cases(quick):
    c = [("fwd", v, 0.0, 0.0) for v in ((0.02, 0.05, 0.1, 0.2, 0.3, 0.5) if quick else (0.02, 0.05, 0.1, 0.15, 0.2, 0.3, 0.5, 0.7))]
    c += [("back", -v, 0.0, 0.0) for v in (0.05, 0.1, 0.3)]
    c += [("side", 0.0, v, 0.0) for v in (0.05, 0.1, 0.2, 0.4)]
    c += [("yaw", 0.0, 0.0, w) for w in (0.05, 0.1, 0.2, 0.4)]
    c += [("stand", 0.0, 0.0, 0.0), ("kicked", 0.3, 0.0, 0.0)]
    return c


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--walkers", required=True, help="label=checkpoint, comma separated")
    ap.add_argument("--name", default="wt-test")
    ap.add_argument("--groups", default="free,wall,objects")
    ap.add_argument("--reps", type=int, default=2)
    ap.add_argument("--duration", type=float, default=8.0, help="s per case (measured over the second half)")
    ap.add_argument("--stiffness", type=float, default=1000.0, help="k of the compliant walker (N per m/s)")
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--device", default=None)
    ap.add_argument("--videos", default="", help="'all' or groups / case names to film (see above)")
    ap.add_argument("--video-dir", default="eval_videos")
    ap.add_argument("--_task", default="", help=argparse.SUPPRESS)  # internal: one (walker, group, mass) in this process
    a = ap.parse_args()

    import torch

    import quadcoop  # noqa: F401
    from mjlab.envs import ManagerBasedRlEnv
    from mjlab.sensor import ContactMatch, ContactSensorCfg

    from quadcoop.mdp.compliance import contact_force_on_robot_w
    from quadcoop.robots.anymal_c import ROBOT
    from quadcoop.robots.objects import NOMINAL_MASS, OBJECT_NAMES, OBJECTS
    from quadcoop.stage1.walker_policy import FrozenWalker
    from quadcoop.walker_env_cfg import make_walker_env_cfg

    device = a.device or ("cuda:0" if torch.cuda.is_available() else "cpu")
    walkers = [w.split("=", 1) for w in a.walkers.split(",")]
    groups = a.groups.split(",")
    cube = OBJECTS[0]
    rows = []
    t0 = time.time()

    def build(compliant, n, mass):
        cfg = make_walker_env_cfg(ROBOT, play=True, compliant=compliant)
        cfg.scene.num_envs = n
        tw = cfg.commands["twist"]
        tw.sample_from_ranges = True
        tw.resampling_time_range = (1e9, 1e9)
        tw.rel_standing_envs = 0.0
        if hasattr(tw, "rel_heading_envs"):
            tw.rel_heading_envs = 0.0
        alpha = 0.5 * math.log(mass / NOMINAL_MASS)
        for nm in OBJECT_NAMES:
            cfg.events[f"{nm}_mass"].params["alpha_range"] = (alpha, alpha)
            cfg.events[f"{nm}_friction"].params["ranges"] = (FRICTION, FRICTION)
        if not any(s.name == "bumper_force" for s in cfg.scene.sensors):  # v1: measure the force all the same
            cfg.scene.sensors = tuple(cfg.scene.sensors) + (ContactSensorCfg(
                name="bumper_force", primary=ContactMatch(mode="body", pattern=tuple(f"{o}/body" for o in OBJECT_NAMES)),
                secondary=ContactMatch(mode="subtree", pattern=ROBOT.base_body, entity="robot"),
                fields=("found", "force"), reduce="netforce", num_slots=1),)
        torch.manual_seed(0)
        return ManagerBasedRlEnv(cfg=cfg, device=device)

    def run(label, path, group, cases, mass=None):
        pol = FrozenWalker(path, device)
        compliant = pol.obs_dim == 50
        n = len(cases) * a.reps
        env = build(compliant, n, mass or NOMINAL_MASS)
        dev = env.device
        robot = env.scene["robot"]
        tw = env.command_manager.get_term("twist")
        obs, _ = env.reset()
        if obs["actor"].shape[-1] != pol.obs_dim:
            raise SystemExit(f"{label}: walker expects {pol.obs_dim} inputs, env gives {obs['actor'].shape[-1]}")
        cmd = torch.tensor([[c[1], 0.0 if group == "wall" else c[2], c[3]] for c in cases for _ in range(a.reps)],
                           device=dev, dtype=torch.float)  # (wall cases carry the face angle where vy would be)
        kicked = torch.tensor([c[0] == "kicked" for c in cases for _ in range(a.reps)], device=dev)
        off = torch.tensor([math.radians(c[2]) if group == "wall" else 0.0 for c in cases for _ in range(a.reps)], device=dev)

        def set_cmd(v):
            tw.vel_command_b[:] = v
            tw.is_standing_env[:] = False
            tw.is_heading_env[:] = False

        def yaw():
            q = robot.data.root_link_quat_w
            return torch.atan2(2 * (q[:, 0] * q[:, 3] + q[:, 1] * q[:, 2]), 1 - 2 * (q[:, 2] ** 2 + q[:, 3] ** 2))

        dt = env.step_dt
        zero = torch.zeros(n, 3, device=dev)
        set_cmd(zero)
        for _ in range(int(1.0 / dt)):  # settle standing
            obs, *_ = env.step(pol(obs["actor"]))
            set_cmd(zero)
        if group in ("wall", "objects"):  # the cube 10 cm ahead of the nose; for 'wall' its face turned by `off`
            ob = env.scene[cube.name]
            y = yaw()
            fwd = torch.stack([torch.cos(y), torch.sin(y)], -1)
            st = torch.zeros(n, 13, device=dev)
            st[:, :2] = robot.data.root_link_pos_w[:, :2] + fwd * (ROBOT.half_length + cube.half_extent_x + GAP)
            st[:, 2] = cube.half_height + 0.005
            oy = y + off
            st[:, 3:7] = torch.stack([torch.cos(oy / 2), 0 * oy, 0 * oy, torch.sin(oy / 2)], -1)
            ob.write_root_state_to_sim(st)
        steps = int(a.duration / dt)
        w0 = steps // 2
        want = {x.strip() for x in a.videos.split(",") if x.strip()}
        film = [e for e in range(0, n, a.reps)
                if want and ("all" in want or group in want or cases[e // a.reps][0] in want)]
        stride = 2
        rec = {"q": [], "pts": [], "v": [], "f": []}
        fell = torch.zeros(n, dtype=torch.bool, device=dev)
        acc = defaultdict(lambda: torch.zeros(n, device=dev))
        fwd0 = torch.stack([torch.cos(yaw()), torch.sin(yaw())], -1)
        p_obj0 = env.scene[cube.name].data.root_link_pos_w[:, :2].clone()
        p_rob = None
        gen = torch.Generator(device="cpu").manual_seed(3)
        for i in range(steps):
            set_cmd(cmd)
            obs, _, term, trunc, _ = env.step(pol(obs["actor"]))
            fell |= term.bool()
            if i % int(2.0 / dt) == int(1.0 / dt) and bool(kicked.any()):  # a shove every 2 s
                v = robot.data.root_link_vel_w.clone()
                imp = ((torch.rand(n, 2, generator=gen) - 0.5) * 1.2).to(dev)
                v[:, :2] += torch.where(kicked.unsqueeze(-1), imp, torch.zeros_like(imp))
                robot.write_root_link_velocity_to_sim(v)
            if film and i % stride == 0:
                y = yaw()
                c, s = torch.cos(y), torch.sin(y)
                vw = robot.data.root_link_lin_vel_w[:, :2]
                vb = torch.stack([c * vw[:, 0] + s * vw[:, 1], -s * vw[:, 0] + c * vw[:, 1],
                                  robot.data.root_link_ang_vel_w[:, 2]], -1)
                f = contact_force_on_robot_w(env, "bumper_force")
                idx = torch.tensor(film, device=dev)
                rec["q"].append(env.sim.data.qpos[idx].cpu().numpy().copy())
                rec["pts"].append(torch.stack([robot.data.root_link_pos_w[idx, :2],
                                               env.scene[cube.name].data.root_link_pos_w[idx, :2]], 1).cpu().numpy())
                rec["v"].append(vb[idx].cpu().numpy())
                rec["f"].append((-(f * torch.stack([c, s], -1)).sum(-1))[idx].cpu().numpy())
            if i == w0:
                p_rob = robot.data.root_link_pos_w[:, :2].clone()
                p_obj0 = env.scene[cube.name].data.root_link_pos_w[:, :2].clone()
            if i >= w0:
                y = yaw()
                c, s = torch.cos(y), torch.sin(y)
                vw = robot.data.root_link_lin_vel_w[:, :2]
                vb = torch.stack([c * vw[:, 0] + s * vw[:, 1], -s * vw[:, 0] + c * vw[:, 1]], -1)
                acc["vx"] += vb[:, 0]
                acc["vy"] += vb[:, 1]
                acc["wz"] += robot.data.root_link_ang_vel_w[:, 2]
                f = contact_force_on_robot_w(env, "bumper_force")
                fn = -(f * torch.stack([c, s], -1)).sum(-1)  # push on the object along the robot's heading
                acc["fn"] += fn
                acc["fn2"] += fn * fn
                acc["touch"] += (torch.linalg.norm(f, dim=-1) > TOUCH_N).float()
        k = max(1, steps - w0)
        T = (steps - 1 - w0) * dt
        obj_v = torch.linalg.norm(env.scene[cube.name].data.root_link_pos_w[:, :2] - p_obj0, dim=-1) / max(T, 1e-6)
        for e in range(n):
            case = cases[e // a.reps]
            mean_f = float(acc["fn"][e]) / k
            sd_f = math.sqrt(max(0.0, float(acc["fn2"][e]) / k - mean_f ** 2))
            rows.append({"walker": label, "compliant": int(compliant), "group": group, "case": case[0],
                         "mass": mass or "", "vx_cmd": case[1], "vy_cmd": case[2] if group != "wall" else 0.0,
                         "wz_cmd": case[3], "offset_deg": case[2] if group == "wall" else 0.0, "rep": e % a.reps,
                         "vx": round(float(acc["vx"][e]) / k, 4), "vy": round(float(acc["vy"][e]) / k, 4),
                         "wz": round(float(acc["wz"][e]) / k, 4), "force": round(mean_f, 1), "force_swing": round(sd_f, 1),
                         "touching": round(float(acc["touch"][e]) / k, 3), "object_speed": round(float(obj_v[e]), 4),
                         "fell": int(fell[e])})
        print(f"[{label}] {group}{'' if mass is None else f' {mass:g} kg'}: {n} runs ({time.time() - t0:.0f} s)", flush=True)
        if film:
            render_videos(env, label, group, cases, film, rec, stride * dt, mass)
        env.close() if hasattr(env, "close") else None
        del env
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    def render_videos(env, label, group, cases, film, rec, frame_dt, mass):
        import numpy as np

        try:
            from quadcoop.coop2.video import Camera, render_episode

            cam = Camera(env)
        except Exception as e:  # noqa: BLE001
            print(f"videos off: cannot render ({e}); set MUJOCO_GL=egl on a GPU node")
            return
        q, pts, v, f = (np.stack(rec[k]) for k in ("q", "pts", "v", "f"))  # (F, len(film), ...)
        out = ROOT / a.video_dir / a.name / label
        for j, e in enumerate(film):
            case = cases[e // a.reps]
            if group == "wall":
                tag, what = f"{case[1]:g}ms_{case[2]:g}deg", f"wall {case[2]:g} deg, {case[1]:g} m/s (target {a.stiffness * case[1]:.0f} N)"
            elif group == "objects":
                tag, what = f"{mass:g}kg_{case[1]:g}ms", f"{mass:g} kg cube, {case[1]:g} m/s"
            else:
                tag = f"{case[1]:g}_{case[2]:g}_{case[3]:g}"
                what = f"{case[0]}: vx {case[1]:g} vy {case[2]:g} m/s, wz {case[3]:g} rad/s"
            last = max(1, int(1.0 / frame_dt))

            def caption(fr, j=j, what=what):
                lo = max(0, fr - last + 1)
                vm = v[lo:fr + 1, j].mean(0)
                return (f"{label} | {what}\n"
                        f"t {fr * frame_dt:4.1f} s  achieved (1 s mean) vx {vm[0]:+.3f} vy {vm[1]:+.3f} m/s  wz {vm[2]:+.3f} rad/s"
                        f"  push {f[lo:fr + 1, j].mean():5.0f} N")
            # the camera frames the robot (and the cube when there is one in view)
            pp = pts[:, j].copy()  # robot, cube; the camera follows the robot and takes in the cube when it is close
            far = np.linalg.norm(pp[:, 1] - pp[:, 0], axis=-1) > 3.0
            pp[far, 1] = pp[far, 0]
            path = render_episode(cam, e, q[:, j], None, None, pp, out / f"{group}_{case[0]}_{tag}.mp4",
                                  fps=1.0 / frame_dt, caption=caption)
            print(f"  video {path.relative_to(ROOT)}", flush=True)

    wall_speeds = (0.02, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4)
    wall = [("wall", v, off, 0.0) for off in (0.0, 20.0) for v in wall_speeds]
    obj = [("push", v, 0.0, 0.0) for v in (0.1, 0.2, 0.3, 0.5)]
    cases_of = {"free": (free_cases(a.quick), None), "wall": (wall, 3000.0)}
    if a._task:  # child: run one task, write its rows
        label, path, group, mass, out = a._task.split("|")
        cs, m = (obj, float(mass)) if group == "objects" else cases_of[group]
        run(label, path, group, cs, m)
        Path(out).write_text(json.dumps(rows))
        return 0
    tasks = []
    for label, path in walkers:
        p = Path(path)
        path = str(p if p.is_absolute() else ROOT / p)
        if not Path(path).exists():
            raise SystemExit(f"{label}: no checkpoint {path}")
        tasks += [(label, path, g, "") for g in ("free", "wall") if g in groups]
        if "objects" in groups:
            tasks += [(label, path, "objects", f"{m:g}") for m in (20.0, 40.0, 80.0)]
    tmp = ROOT / "logs" / "evals" / a.name / "parts"
    tmp.mkdir(parents=True, exist_ok=True)
    argv = [x for x in sys.argv[1:]]
    for i, (label, path, g, m) in enumerate(tasks):  # each in its own process: memory is freed in between
        out = tmp / f"{i:02d}_{label}_{g}{m}.json"
        r = subprocess.run([sys.executable, str(Path(__file__).resolve()), *argv, "--_task", f"{label}|{path}|{g}|{m}|{out}"])
        if r.returncode != 0 or not out.exists():
            raise SystemExit(f"task {label} {g} {m} failed (exit {r.returncode})")
        rows += json.loads(out.read_text())
    stats = ROOT / "evals" / a.name
    stats.mkdir(parents=True, exist_ok=True)
    with open(stats / "cases.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    summary, md = summarise(rows, [w[0] for w in walkers], a)
    (stats / "summary.md").write_text("\n".join(md) + "\n")
    (stats / "summary.json").write_text(json.dumps(summary, indent=1))
    print("\n".join(md))
    return 0


def summarise(rows, labels, a):
    k = a.stiffness
    mean = lambda xs: sum(xs) / len(xs) if xs else float("nan")  # noqa: E731
    md = [f"# Walker acceptance test: {a.name}", "",
          f"Walkers: {', '.join(labels)}. Each case {a.duration:g} s, measured over the second half, {a.reps} repeats. "
          f"Compliant-walker expectations use k = {k:g} N per m/s and object friction {FRICTION}.", ""]
    summary = {"walkers": labels, "stiffness": k, "verdicts": {}}
    cells = defaultdict(list)
    for r in rows:
        cells[(r["walker"], r["group"], r["case"], r["mass"], r["vx_cmd"], r["vy_cmd"], r["wz_cmd"], r["offset_deg"])].append(r)

    def agg(lbl, g, case, mass, vx, vy, wz, off, key):
        return mean([r[key] for r in cells.get((lbl, g, case, mass, vx, vy, wz, off), [])])

    verdicts = {lbl: {} for lbl in labels}
    groups = {r["group"] for r in rows}
    if "free" in groups:
        md += ["## Free walking (achieved velocity; small commands are the dead-zone test)", "",
               "| case | command | " + " | ".join(f"{l}: achieved (err)" for l in labels) + " | " +
               " | ".join(f"{l}: fell" for l in labels) + " |", "|---|---|" + "---|" * (2 * len(labels))]
        keys = sorted({(r["case"], r["vx_cmd"], r["vy_cmd"], r["wz_cmd"]) for r in rows if r["group"] == "free"},
                      key=lambda x: (x[0], abs(x[1]) + abs(x[2]) + abs(x[3])))
        ok_small = {l: [] for l in labels}
        ok_norm = {l: [] for l in labels}
        falls = {l: [] for l in labels}
        for case, vx, vy, wz in keys:
            ax = 2 if case == "yaw" else (1 if case == "side" else 0)
            want = (vx, vy, wz)[ax]
            name = ("vx", "vy", "wz")[ax]
            cell_txt, fell_txt = [], []
            for l in labels:
                got = agg(l, "free", case, "", vx, vy, wz, 0.0, name)
                fl = agg(l, "free", case, "", vx, vy, wz, 0.0, "fell")
                err = abs(got - want)
                cell_txt.append(f"{got:+.3f} ({err:.3f})")
                fell_txt.append(f"{fl:.2f}")
                falls[l].append(fl)
                if case in ("stand", "kicked"):
                    continue
                if abs(want) <= 0.2 + 1e-9:
                    ok_small[l].append((got * math.copysign(1, want) >= 0.5 * abs(want)) and err <= max(0.03, 0.3 * abs(want)))
                else:
                    ok_norm[l].append(err <= 0.1)
            unit = "rad/s" if case == "yaw" else "m/s"
            md.append(f"| {case} | {want:+g} {unit} | " + " | ".join(cell_txt) + " | " + " | ".join(fell_txt) + " |")
        md.append("")
        for l in labels:
            s, nrm, fl = mean([float(x) for x in ok_small[l]]), mean([float(x) for x in ok_norm[l]]), max(falls[l])
            v = {"small_ok": s, "normal_ok": nrm, "max_fall_rate": fl,
                 "pass": s >= 0.99 and nrm >= 0.99 and fl == 0}
            verdicts[l]["free"] = v
            md.append(f"**{l}, free walking: {'PASS' if v['pass'] else 'FAIL'}** - small commands moved as asked "
                      f"{s:.0%}, normal commands within 0.1 m/s {nrm:.0%}, worst fall rate {fl:.2f}.")
        md.append("")
    if "wall" in groups:
        md += [f"## Pressing an immovable cube (force on it along the heading, N; swing = std over time; target k x speed)", ""]
        for off in sorted({r["offset_deg"] for r in rows if r["group"] == "wall"}):
            md += [f"### {off:g} deg", "", "| speed (m/s) | target (N) | " +
                   " | ".join(f"{l}: force (swing), touching" for l in labels) + " |", "|---|---|" + "---|" * len(labels)]
            speeds = sorted({r["vx_cmd"] for r in rows if r["group"] == "wall" and r["offset_deg"] == off})
            for v in speeds:
                md.append(f"| {v:g} | {k * v:.0f} | " + " | ".join(
                    f"{agg(l, 'wall', 'wall', 3000.0, v, 0.0, 0.0, off, 'force'):.0f} "
                    f"({agg(l, 'wall', 'wall', 3000.0, v, 0.0, 0.0, off, 'force_swing'):.0f}), "
                    f"{agg(l, 'wall', 'wall', 3000.0, v, 0.0, 0.0, off, 'touching'):.2f}" for l in labels) + " |")
            md.append("")
        for l in labels:
            sp = [v for v in sorted({r["vx_cmd"] for r in rows if r["group"] == "wall"}) if 0.05 - 1e-9 <= v <= 0.3 + 1e-9]
            fs = [agg(l, "wall", "wall", 3000.0, v, 0.0, 0.0, 0.0, "force") for v in sp]
            sw = [agg(l, "wall", "wall", 3000.0, v, 0.0, 0.0, 0.0, "force_swing") for v in sp]
            tc = [agg(l, "wall", "wall", 3000.0, v, 0.0, 0.0, 0.0, "touching") for v in sp]
            within = mean([float(abs(f - k * v) <= 0.25 * k * v) for f, v in zip(fs, sp)])
            rising = all(fs[i + 1] >= fs[i] - 10 for i in range(len(fs) - 1))
            steady = mean([float(s <= 0.25 * max(f, 1.0)) for s, f in zip(sw, fs)])
            touch = mean(tc)
            v = {"within_25pct": within, "rising": rising, "steady": steady, "touching": touch,
                 "pass": within >= 0.99 and rising and steady >= 0.99 and touch >= 0.95}
            verdicts[l]["wall"] = v
            md.append(f"**{l}, force control (square on, 0.05-0.3 m/s): {'PASS' if v['pass'] else 'FAIL'}** - within 25% "
                      f"of k x speed {within:.0%}, {'rising' if rising else 'not rising'}, steady {steady:.0%}, "
                      f"touching {touch:.0%}.")
        md.append("")
    if "objects" in groups:
        md += ["## Pushing movable cubes (robot speed; a compliant walker should go at max(0, v - mu m g / k))", "",
               "| mass | speed cmd | expected (m/s) | " + " | ".join(f"{l}: robot speed, object speed, force (N), fell" for l in labels) + " |",
               "|---|---|---|" + "---|" * len(labels)]
        oks = {l: [] for l in labels}
        fl = {l: [] for l in labels}
        for m in sorted({r["mass"] for r in rows if r["group"] == "objects"}):
            for v in sorted({r["vx_cmd"] for r in rows if r["group"] == "objects"}):
                exp = max(0.0, v - FRICTION * m * 9.81 / k)
                cells_ = []
                for l in labels:
                    rv = agg(l, "objects", "push", m, v, 0.0, 0.0, 0.0, "vx")
                    ov = agg(l, "objects", "push", m, v, 0.0, 0.0, 0.0, "object_speed")
                    f = agg(l, "objects", "push", m, v, 0.0, 0.0, 0.0, "force")
                    fe = agg(l, "objects", "push", m, v, 0.0, 0.0, 0.0, "fell")
                    oks[l].append(abs(rv - exp) <= 0.05)
                    fl[l].append(fe)
                    cells_.append(f"{rv:.2f}, {ov:.2f}, {f:.0f}, {fe:.2f}")
                md.append(f"| {m:g} kg | {v:g} | {exp:.2f} | " + " | ".join(cells_) + " |")
        md.append("")
        for l in labels:
            v = {"speed_ok": mean([float(x) for x in oks[l]]), "max_fall_rate": max(fl[l]),
                 "pass": mean([float(x) for x in oks[l]]) >= 0.9 and max(fl[l]) == 0}
            verdicts[l]["objects"] = v
            md.append(f"**{l}, pushing objects: {'PASS' if v['pass'] else 'FAIL'}** - speed within 0.05 m/s of the "
                      f"compliant expectation {v['speed_ok']:.0%}, worst fall rate {v['max_fall_rate']:.2f}.")
        md.append("")
    summary["verdicts"] = verdicts
    md += ["## Verdicts", "", "| walker | " + " | ".join(sorted(groups)) + " |", "|---|" + "---|" * len(groups)]
    for l in labels:
        md.append(f"| {l} | " + " | ".join("PASS" if verdicts[l].get(g, {}).get("pass") else "FAIL" for g in sorted(groups)) + " |")
    return summary, md


if __name__ == "__main__":
    sys.exit(main())
