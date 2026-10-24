"""Final per-object videos of a registered method, for the report and the multi-agent work.

Push policies (Stage 2): every object x mass x goal scenario is run with up to 3 attempts that
differ only by a small, fixed perturbation of the object's start (same for every method, so
2b and ctrl face identical tasks). The first successful attempt is filmed; if all 3 fail, the
failure of attempt 1 is filmed. Objects use their nominal size.

    eval_videos/<name>/<object>/<mass>kg/<scenario>__<outcome>.mp4
    eval_videos/<name>/index.html        browse everything (object x mass x scenario grid)
    eval_videos/<name>/showcase.csv      one row per object x mass x scenario (also copied, with
                                         showcase.md, to evals/<id>/eval/showcase/ for the repo)

Scenarios, relative to where the object starts (the robot starts behind it, facing it):
    A_straight   goal 2.5 m straight ahead, no turn
    B_left       goal 3 m at 60 deg to the left, turned +30 deg
    C_backright  goal 3 m at 135 deg to the right (behind the object's right side, so the robot
                 has to go around), turned -60 deg
Turns are capped at what training asks of each shape (e.g. 40 deg for 4-fold shapes).
Success: object within 10 cm / 6 deg, held 1 s, within 80 s. A fall, tip-over or lost object
ends the attempt.

Walkers: copies the method's standard-eval videos (walk, steady push, object pushes) from
logs/evals/<id>/standard/videos/ into eval_videos/<name>/ (run the standard eval first).

    python scripts/showcase.py --id s2b-anymal-term80 --name s2b_anymal
    ID=s2b-anymal-term80 NAME=s2b_anymal sbatch slurm/showcase.sbatch
"""

from __future__ import annotations

import argparse
import csv
import html
import math
import os
import shutil
import sys
import time
from collections import defaultdict
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
os.environ.setdefault("QUADCOOP_SHAPES", "v2")

import torch  # noqa: E402

from methods import EVALS, STORE, resolve  # noqa: E402

SCENARIOS = (  # name, distance (m), direction (deg, + = left), turn (deg), object start yaw (deg)
    ("A_straight", 2.5, 0.0, 0.0, 0.0),
    ("B_left", 3.0, 60.0, 30.0, 0.0),
    ("C_backright", 3.0, -135.0, -60.0, 0.0),
)
ATTEMPTS = ((0.0, 0.0), (0.15, 7.0), (-0.15, -7.0))  # object start: lateral offset (m), yaw (deg)
OUT_ROOT = ROOT / "eval_videos"


def walker(mid: str, m: dict, name: str) -> int:
    src = STORE / mid / "standard" / "videos"
    vids = sorted(src.glob("*.mp4"))
    if not vids:
        raise SystemExit(f"no videos in {src}: run `ID={mid} SUITE=standard sbatch slurm/eval_method.sbatch` first")
    dst = OUT_ROOT / name
    dst.mkdir(parents=True, exist_ok=True)
    for v in vids:
        shutil.copy2(v, dst / v.name)
    for f in ("validation.json", "eval.json"):
        if (STORE / mid / "standard" / f).exists():
            shutil.copy2(STORE / mid / "standard" / f, dst / f)
    print(f"copied {len(vids)} videos to {dst}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--id", required=True, help="registered method (scripts/methods.py list)")
    ap.add_argument("--name", required=True, help="folder under eval_videos/, e.g. s2b_anymal")
    ap.add_argument("--objects", default="all")
    ap.add_argument("--masses", default="10,25,40")
    ap.add_argument("--horizon", type=float, default=80.0)
    ap.add_argument("--video-size", default="480x360")
    ap.add_argument("--device", default=None)
    a = ap.parse_args()
    m = resolve(a.id)
    if m["stage"] == "walker":
        return walker(a.id, m, a.name)
    if m["stage"] != "stage2":
        raise SystemExit("showcase supports walkers and Stage 2 policies")

    # environment exactly as registered (walker, its profile/history, shapes)
    for k, v in m["env_all"].items():
        os.environ[k] = v
    os.environ["QUADCOOP_WALKER_CKPT"] = m["walker_checkpoint"]
    for k in ("QUADCOOP_WALKER_CKPT_ANYMAL_C", "QUADCOOP_WALKER_CKPT_SPOT", "QUADCOOP_PUSH_FORCE",
              "QUADCOOP_SUCCESS_MODE"):
        os.environ.pop(k, None)
    device = a.device or ("cuda:0" if torch.cuda.is_available() else "cpu")

    import quadcoop  # noqa: F401
    import quadcoop.stage1  # noqa: F401
    import quadcoop.stage1b  # noqa: F401
    import quadcoop.stage2  # noqa: F401
    from mjlab.envs import ManagerBasedRlEnv
    from mjlab.rl import MjlabOnPolicyRunner, RslRlVecEnvWrapper
    from mjlab.tasks.registry import load_env_cfg, load_rl_cfg
    from mjlab.utils.lab_api.math import quat_from_euler_xyz
    from mjlab.viewer.model_sync import VIEWER_MODEL_FIELDS, sync_model_fields
    from tensordict import TensorDict

    from eval_push import StateRecorder, VideoMaker
    from eval_push2 import make_overlay
    from quadcoop.falls import NOMINAL_HEIGHT, fall_reason, fallen as pose_fallen
    from quadcoop.stage1.mdp import wrap, yaw_of
    from quadcoop.stage1b.shapes import NOMINAL_MASS
    from quadcoop.stage2 import mdp as m2
    from quadcoop.stage2.shapes import OBJ_NAMES2, SHAPE_NAMES2, SHAPES2, TRAIN_NAMES

    task = m["task"]
    variant = "ctrl" if "ctrl" in task.lower() else ("b" if "push2b" in task.lower() else "a")
    robot_name = "spot" if "spot" in task.lower() else "anymal_c"
    nom_h = NOMINAL_HEIGHT[robot_name]
    objects = list(SHAPE_NAMES2) if a.objects == "all" else [o.strip() for o in a.objects.split(",")]
    masses = [float(x) for x in a.masses.split(",")]
    vw, vh = (int(x) for x in a.video_size.lower().split("x"))
    out = OUT_ROOT / a.name
    out.mkdir(parents=True, exist_ok=True)
    cases = [(o, s, k) for o in objects for s in range(len(SCENARIOS)) for k in range(len(ATTEMPTS))]
    n = len(cases)
    rows: list[dict] = []
    t0 = time.time()
    print(f"{a.id}: {task}, walker {m['walker_checkpoint']}\n{len(objects)} objects x {len(SCENARIOS)} scenarios "
          f"x {len(ATTEMPTS)} attempts = {n} envs per mass", flush=True)

    for mass in masses:
        cfg = load_env_cfg(task, play=True)
        cfg.scene.num_envs = n
        cfg.episode_length_s = 1e5
        cfg.events["reset_base"].params["pose_range"]["yaw"] = (0.0, 0.0)
        alpha = 0.5 * math.log(mass / NOMINAL_MASS)
        for name in OBJ_NAMES2:
            cfg.events[f"{name}_mass"].params["alpha_range"] = (alpha, alpha)
        ends = {k: cfg.terminations.pop(k) for k in ("box_tipped", "box_lost")}
        for k in ("fell_over", "goal_reached"):
            cfg.terminations.pop(k, None)
        torch.manual_seed(0)
        base = ManagerBasedRlEnv(cfg=cfg, device=device)
        env = RslRlVecEnvWrapper(base)
        runner = MjlabOnPolicyRunner(env, asdict(load_rl_cfg(task)), device=device)
        runner.load(m["checkpoint_abs"], load_cfg={"actor": True}, strict=True, map_location=device)
        policy = runner.get_inference_policy(device=device)
        g = base.command_manager.get_term("goal")
        robot = base.scene["robot"]
        dev = base.device
        ids = torch.arange(n, device=dev)
        for k in range(len(SHAPES2)):  # nominal sizes for every object
            m2.apply_geometry(base, ids, k, torch.ones(n, 3, device=dev))

        obj_idx = torch.tensor([SHAPE_NAMES2.index(o) for o, _, _ in cases], device=dev)
        sc = torch.tensor([SCENARIOS[s][1:] for _, s, _ in cases], device=dev, dtype=torch.float)
        at = torch.tensor([ATTEMPTS[k] for _, _, k in cases], device=dev, dtype=torch.float)
        dist_g, dir_g, dyaw_g, yaw0 = sc[:, 0], torch.deg2rad(sc[:, 1]), torch.deg2rad(sc[:, 2]), torch.deg2rad(sc[:, 3])
        sym = g.sym[obj_idx]
        cap = torch.where(sym > 0, (math.pi / sym.clamp(min=1)) * g.cfg.max_yaw_frac_of_symmetry, torch.zeros_like(sym))
        dyaw_g = torch.sign(dyaw_g) * torch.minimum(dyaw_g.abs(), cap)
        turn_used = torch.rad2deg(dyaw_g).tolist()

        torch.manual_seed(1)
        env.reset()
        q_adr = robot.indexing.free_joint_q_adr
        qpos = robot.data.data.qpos
        root = qpos[:, q_adr[0:3]]
        ryaw = yaw_of(qpos[:, q_adr[3:7]])
        fwd = torch.stack([torch.cos(ryaw), torch.sin(ryaw)], -1)
        left = torch.stack([-torch.sin(ryaw), torch.cos(ryaw)], -1)
        reach = g.cfg.robot_reach + g.radius_env[ids, obj_idx] + 0.4
        obj_xy = root[:, :2] + reach.unsqueeze(-1) * fwd + at[:, 0:1] * left
        obj_h = ryaw + yaw0 + torch.deg2rad(at[:, 1])
        # the goal is defined from the unperturbed start, so every attempt has the same goal
        nominal_xy = root[:, :2] + reach.unsqueeze(-1) * fwd
        gdir = ryaw + dir_g
        goal_xy = nominal_xy + dist_g.unsqueeze(-1) * torch.stack([torch.cos(gdir), torch.sin(gdir)], -1)
        goal_h = wrap(ryaw + yaw0 + dyaw_g)
        g.shape[:] = obj_idx
        g.env_level[:] = 5
        g.goal_xy[:] = goal_xy
        g.goal_yaw[:] = goal_h
        g.in_goal_time[:] = 0.0
        z = torch.zeros(n, device=dev)
        oq = quat_from_euler_xyz(z, z, obj_h)
        for k, o in enumerate(g.objs):
            st = torch.zeros(n, 13, device=dev)
            here = obj_idx == k
            st[:, :2] = torch.where(here.unsqueeze(-1), obj_xy,
                                    root[:, :2] + torch.tensor([g.cfg.park_distance + 4.0 * k, 0.0], device=dev))
            st[:, 2] = g.rest_env[:, k] + 0.005
            st[:, 3:7] = oq
            o.write_root_state_to_sim(st, ids)
        gq = quat_from_euler_xyz(z, z, goal_h)
        for k, gm in enumerate(g.goals):
            pose = torch.zeros(n, 7, device=dev)
            pose[:, :2] = goal_xy
            pose[:, 2] = torch.where(obj_idx == k, torch.full_like(z, 0.002), torch.full_like(z, -5.0))
            pose[:, 3:7] = gq
            gm.write_mocap_pose_to_sim(pose, ids)
        base.sim.forward()
        g.refresh_profiles(ids)
        g.steps = 0
        d0, e0 = g.errors()
        g.prev_dist[:] = d0
        g.prev_yaw_err[:] = e0.abs()
        om = base.observation_manager
        obs = TensorDict({k: om.compute_group(k) for k in om.active_terms}, batch_size=[n])

        dt = base.step_dt
        rec = StateRecorder(base, dt)
        tilt = lambda: torch.rad2deg(torch.acos((-robot.data.projected_gravity_b[:, 2]).clamp(-1, 1)))  # noqa: E731
        imgs = []

        def grab():
            if variant != "ctrl":
                imgs.append((g.profile_top.to("cpu", torch.float16), g.profile_front.to("cpu", torch.float16)))
        rec.add(0.0, d0, torch.rad2deg(e0.abs()), torch.zeros_like(d0), tilt())
        grab()
        steps = int(a.horizon / dt)
        pt, yt = 0.10, math.radians(6.0)
        done = torch.zeros(n, dtype=torch.bool, device=dev)
        how, detail = ["horizon"] * n, [""] * n
        t_succ = torch.full((n,), float("nan"), device=dev)
        t_fall = torch.full((n,), float("nan"), device=dev)
        hold = torch.zeros(n, device=dev)
        last_d, last_e, min_d = d0.clone(), e0.abs().clone(), d0.clone()
        end_step = torch.full((n,), steps - 1, dtype=torch.long, device=dev)
        tail = int(2.0 / dt)
        all_done_at = None
        with torch.no_grad():
            for i in range(steps):
                obs, _, _, _ = env.step(policy(obs))
                t = (i + 1) * dt
                live = ~done
                fell = pose_fallen(base, "robot", nom_h) & live
                for j in fell.nonzero().flatten().tolist():
                    how[j], detail[j] = "fell", fall_reason(base, j, "robot", nom_h)
                t_fall = torch.where(fell, torch.full_like(t_fall, t), t_fall)
                tip = ends["box_tipped"].func(base, **(ends["box_tipped"].params or {})).bool() & live & ~fell
                lost = ends["box_lost"].func(base, **(ends["box_lost"].params or {})).bool() & live & ~fell & ~tip
                for j in tip.nonzero().flatten().tolist():
                    how[j] = "tipped"
                for j in lost.nonzero().flatten().tolist():
                    how[j] = "lost"
                d, e = g.errors()
                ea = e.abs()
                ok = live & ~fell & ~tip & ~lost
                last_d = torch.where(ok, d, last_d)
                last_e = torch.where(ok, ea, last_e)
                min_d = torch.where(ok, torch.minimum(min_d, d), min_d)
                inside = ok & (d < pt) & (ea < yt)
                hold = torch.where(inside, hold + dt, torch.zeros_like(hold))
                succ = ok & (hold >= 1.0)
                t_succ = torch.where(succ, torch.full_like(t_succ, t), t_succ)
                for j in succ.nonzero().flatten().tolist():
                    how[j] = "success"
                ended = fell | tip | lost | succ
                end_step = torch.where(ended & ~done, torch.full_like(end_step, i), end_step)
                done |= ended
                if (i + 1) % rec.stride == 0:
                    rec.add(t, d, torch.rad2deg(ea), hold, tilt())
                    if variant == "b" and len(rec.t) % 5 == 1:
                        grab()
                if all_done_at is None and bool(done.all()):
                    all_done_at = i
                if all_done_at is not None and i >= all_done_at + tail:
                    break

        # pick per object x scenario: first successful attempt, else attempt 1's failure
        maker = VideoMaker(base, robot, g, q_adr, goal_xy, out / "_tmp", vw, vh, rec, SHAPES2, obj_idx)
        hmj = base.sim.mj_model
        fields = base.sim.expanded_fields & VIEWER_MODEL_FIELDS
        maker.sync = lambda j: sync_model_fields(hmj, base.sim.model, fields, j)
        if imgs:
            maker.overlay = make_overlay(imgs, variant, vw, vh, "normal")
        by = defaultdict(list)
        for j, (o, s, k) in enumerate(cases):
            by[(o, s)].append(j)
        for (o, s), js in by.items():
            wins = [j for j in js if how[j] == "success"]
            j = wins[0] if wins else js[0]
            name, dist, direc, _, y0 = SCENARIOS[s]
            turn = round(turn_used[j])
            fmt = lambda x: "" if math.isnan(x) else round(x, 2)  # noqa: E731
            row = {
                "object": o, "seen_shape": int(o in TRAIN_NAMES), "mass": mass, "scenario": name,
                "distance": dist, "direction": direc, "turn": turn, "start_yaw": y0,
                "attempts_succeeded": f"{len(wins)}/{len(js)}",
                "filmed_attempt": js.index(j) + 1, "outcome": how[j],
                "t_success": fmt(float(t_succ[j])), "final_pos_err": round(float(last_d[j]), 3),
                "final_yaw_err": round(math.degrees(float(last_e[j])), 1),
                "closest_pos_err": round(float(min_d[j]), 3), "fall_detail": detail[j],
                "attempt_outcomes": " ".join(how[x] for x in js),
                # fields the shared video maker reads
                "t_fall": fmt(float(t_fall[j])), "outcome_ignoring_falls": how[j],
                "t_fall_train_rule": "", "train_rule_detail": "",
            }
            label = (f"[{a.name}]  {o}  {mass:g} kg  {name}: goal {dist:g} m at {direc:g} deg, turn {turn} deg  "
                     f"(attempt {row['filmed_attempt']}/3, {row['attempts_succeeded']} succeeded)")
            rel = maker.make(j, label, f"{o}_{mass:g}_{name}", row, int(end_step[j]) + tail)
            dst = out / o / f"{mass:g}kg" / f"{name}__{how[j]}.mp4"
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(out / "_tmp" / rel[len('videos/'):]), dst)
            row["video"] = str(dst.relative_to(out))
            rows.append(row)
        maker.close()
        shutil.rmtree(out / "_tmp", ignore_errors=True)
        mine = [r for r in rows if r["mass"] == mass]
        print(f"[{mass:g} kg] {sum(r['outcome'] == 'success' for r in mine)}/{len(mine)} object-scenarios succeeded "
              f"within 3 attempts ({time.time() - t0:.0f} s elapsed)", flush=True)
        env.close()
        del env, base, runner, policy, rec, imgs

    write(rows, out, a, masses)
    return 0


def write(rows, out: Path, a, masses) -> None:
    keep = [k for k in rows[0] if k not in ("t_fall", "outcome_ignoring_falls", "t_fall_train_rule", "train_rule_detail")]
    with open(out / "showcase.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keep, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    objs = list(dict.fromkeys(r["object"] for r in rows))
    scen = [s[0] for s in SCENARIOS]
    cell = {(r["object"], r["mass"], r["scenario"]): r for r in rows}
    # markdown: per object x mass, which scenarios succeeded (attempts that succeeded)
    md = [f"# Showcase: {a.id}", "",
          "Each cell: scenarios A / B / C as successful attempts out of 3 (S = filmed success, F = all 3 failed).", "",
          "| object | " + " | ".join(f"{m:g} kg" for m in masses) + " |", "|---" * (len(masses) + 1) + "|"]
    for o in objs:
        cells = []
        for m in masses:
            parts = []
            for s in scen:
                r = cell.get((o, m, s))
                parts.append("" if r is None else f"{r['attempts_succeeded'][0]}{'S' if r['outcome'] == 'success' else 'F'}")
            cells.append(" / ".join(parts))
        tag = "" if any(r["seen_shape"] for r in rows if r["object"] == o) else " (unseen)"
        md.append(f"| {o}{tag} | " + " | ".join(cells) + " |")
    tot = {m: sum(cell[(o, m, s)]["outcome"] == "success" for o in objs for s in scen if (o, m, s) in cell) for m in masses}
    md += ["", "Succeeded (any attempt): " + ", ".join(f"{m:g} kg {tot[m]}/{len(objs) * len(scen)}" for m in masses), "",
           "Failures (all 3 attempts failed):", ""]
    for r in rows:
        if r["outcome"] != "success":
            md.append(f"- {r['object']} {r['mass']:g} kg {r['scenario']}: {r['attempt_outcomes']}; final error "
                      f"{r['final_pos_err']} m / {r['final_yaw_err']} deg, closest {r['closest_pos_err']} m {r['fall_detail']}")
    (out / "showcase.md").write_text("\n".join(md) + "\n")
    # html grid: rows = objects, columns = masses, each cell = the 3 scenario videos
    h = ["<html><head><meta charset='utf-8'><title>" + html.escape(a.name) + "</title><style>"
         "body{font-family:sans-serif;background:#111;color:#ddd;margin:12px}td{vertical-align:top;padding:4px}"
         "video{width:300px}.S{color:#7e7}.F{color:#f97}</style></head><body>",
         f"<h1>{html.escape(a.name)} ({html.escape(a.id)})</h1><table><tr><th></th>" +
         "".join(f"<th>{m:g} kg</th>" for m in masses) + "</tr>"]
    for o in objs:
        h.append(f"<tr><td><b>{o}</b></td>")
        for m in masses:
            h.append("<td>")
            for s in scen:
                r = cell.get((o, m, s))
                if r:
                    c = "S" if r["outcome"] == "success" else "F"
                    h.append(f"<div class='{c}'>{s}: {r['outcome']} ({r['attempts_succeeded']})</div>"
                             f"<video controls preload='none' src='{r['video']}'></video>")
            h.append("</td>")
        h.append("</tr>")
    h.append("</table></body></html>")
    (out / "index.html").write_text("\n".join(h))
    stats = EVALS / a.id / "eval" / "showcase"
    stats.mkdir(parents=True, exist_ok=True)
    shutil.copy2(out / "showcase.csv", stats / "showcase.csv")
    shutil.copy2(out / "showcase.md", stats / "showcase.md")
    print("\n".join(md[:len(objs) + 8]))
    print(f"\nvideos: {out}/index.html\nstats: {stats}")


if __name__ == "__main__":
    raise SystemExit(main())
