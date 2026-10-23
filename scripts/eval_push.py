"""Evaluate a Stage 1b pushing policy on a fixed grid of tasks, with a mass ablation.

For every object x mass x scenario (goal distance, goal direction, goal yaw change,
object start yaw), it runs the policy deterministically from the same start and
records, per episode:

    success_strict   object held inside --pos-tol / --yaw-tol for --hold seconds
    success_loose    same with 2x the tolerances (how often it is "almost" there)
    t_reach          first time inside the strict tolerance (s)
    t_success        time the strict hold was completed (s)
    final_pos_err    object-goal distance at the end (m)   [end = success, termination or horizon]
    final_yaw_err    folded heading error at the end (deg)
    min_pos_err      closest the object ever got (m)
    path_ratio       distance the object travelled / straight-line distance
    outcome          success | horizon | fell | tipped | lost  (training's termination rules)

A fall is judged by the body's pose only (quadcoop/falls.py): on its side or upside
down (tilt > 60 deg), or collapsed (base below 40% of standing height). Contacts do
not count. A fall ends the official episode but not the simulation, so the same
episode is also scored as if falls did not end it:

    fall_detail               "on its side (tilt 95 deg)", "upside down ...", "collapsed ..."
    t_fall                    when (s)
    tilt_at_end               robot tilt at the very end (deg): small = it was standing again
    success_ignoring_falls    success if the fall had not ended the episode
    outcome_ignoring_falls
    success_train_rule / outcome_train_rule / t_fall_train_rule / train_rule_detail
                              what the rule the policy was TRAINED with (tilt > 70 deg or
                              listed collision geoms on the ground) would have said

Videos (--videos K, default 4): the full rollout of up to K episodes per object, mass
and outcome, rendered after the rollout from the recorded states (so they show exactly
what was scored): overview on the left, robot close-up on the right, with the
scenario, errors, hold timer and robot tilt overlaid. They run on after a counted fall
(touching geoms painted red), until the "ignoring falls" outcome plus 2 s.
Snapshots (--snapshots N): still images of every counted fall, tip-over and loss, and
of N successes and N time-ups per object and mass. Browse both from snapshots/index.html.

Outputs (default: next to the checkpoint, in eval_<ckpt>/):
    episodes.csv     one row per episode
    summary.json     aggregates by object, mass, distance, direction, yaw change, fall triggers
    summary.md       the same as readable tables
    vs_mass.png      success / time / accuracy vs mass per object (if matplotlib is there)
    snapshots/       stills, sorted by outcome, plus index.html to browse them and the videos
    videos/          MP4s, sorted by outcome

    QUADCOOP_WALKER_CKPT=<walker.pt> MUJOCO_GL=egl python scripts/eval_push.py \\
        --task QuadCoop-PushHard-AnymalC --checkpoint <pushhard model_N.pt> 
"""

from __future__ import annotations

import argparse
import csv
import itertools
import json
import math
import sys
import time
from collections import defaultdict
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import torch  # noqa: E402

END_TERMS = ("fell_over", "fell_contact", "box_tipped", "box_lost")


def floats(s: str) -> list[float]:
    return [float(x) for x in s.split(",") if x.strip()]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--task", required=True)
    ap.add_argument("--checkpoint", default=None,
                    help="pushhard model_N.pt (default: newest dated run in logs/rsl_rl/pushhard_<robot>, "
                         "highest N)")
    ap.add_argument("--walker", default=None,
                    help="walker model_N.pt (default: $QUADCOOP_WALKER_CKPT, else the newest run in "
                         "logs/rsl_rl/walker_<robot>, highest N)")
    ap.add_argument("--objects", default="all", help="comma list, e.g. cube,arch,sphere (default all)")
    ap.add_argument("--masses", default="10,20,30,40", help="kg, one env build per mass")
    ap.add_argument("--distances", default="2,4,6", help="goal distance from the object start (m)")
    ap.add_argument("--directions", default="0,60,120,180",
                    help="goal direction in deg relative to robot->object (0 = straight past it, "
                         "180 = back toward the robot's side, so it has to go around)")
    ap.add_argument("--yaw-changes", default="0,45,90", help="goal heading change (deg); folded by symmetry")
    ap.add_argument("--start-yaws", default="0,45", help="object start heading rel. to the robot (deg)")
    ap.add_argument("--reps", type=int, default=2, help="repeats of every scenario")
    ap.add_argument("--horizon", type=float, default=40.0, help="seconds per episode")
    ap.add_argument("--pos-tol", type=float, default=0.10)
    ap.add_argument("--yaw-tol", type=float, default=6.0)
    ap.add_argument("--hold", type=float, default=1.0)
    ap.add_argument("--obs-level", type=int, default=5,
                    help="curriculum level the policy is told it is at (sets its hold-progress input)")
    ap.add_argument("--snapshots", type=int, default=3,
                    help="snapshot images: every counted fall, tip-over and loss, plus this many "
                         "successes and this many time-ups per object per mass (0 = no snapshots)")
    ap.add_argument("--videos", type=int, default=4,
                    help="full-rollout MP4s: up to this many episodes per object, mass and outcome "
                         "(fell / tipped / lost / horizon / success), picked at random (0 = none)")
    ap.add_argument("--video-size", default="480x360", help="size of each of the two video panels")
    ap.add_argument("--shapes", default=None, choices=("v1", "v2"),
                    help="object geometry (default: v2 for PushHard2 tasks, else $QUADCOOP_SHAPES or v1)")
    ap.add_argument("--out", default=None)
    ap.add_argument("--device", default=None)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--selftest-teleport", type=float, default=None,
                    help="harness self-test: at this time (s) put every object on its goal; "
                         "success_ignoring_falls should then be 1 everywhere")
    a = ap.parse_args()
    device = a.device or ("cuda:0" if torch.cuda.is_available() else "cpu")

    # -- checkpoints: default to the newest runs ------------------------------------------
    import os

    robot_name = "spot" if "spot" in a.task.lower() else "anymal_c"
    os.environ["QUADCOOP_SHAPES"] = a.shapes or ("v2" if "PushHard2" in a.task
                                                 else os.environ.get("QUADCOOP_SHAPES", "v1"))
    exp_dir = ("pushhard2_" if "PushHard2" in a.task else "pushhard_") + robot_name
    per_robot = f"QUADCOOP_WALKER_CKPT_{robot_name.upper()}"
    if a.walker:
        os.environ["QUADCOOP_WALKER_CKPT"] = a.walker
        os.environ.pop(per_robot, None)
    elif not (os.environ.get("QUADCOOP_WALKER_CKPT") or os.environ.get(per_robot)):
        os.environ["QUADCOOP_WALKER_CKPT"] = str(newest_checkpoint(ROOT / "logs/rsl_rl" / f"walker_{robot_name}"))
    if a.checkpoint is None:
        a.checkpoint = str(newest_checkpoint(ROOT / "logs/rsl_rl" / exp_dir))
    walker = os.environ.get(per_robot) or os.environ["QUADCOOP_WALKER_CKPT"]
    print(f"policy: {a.checkpoint}\nwalker: {walker}\nshapes: {os.environ['QUADCOOP_SHAPES']}", flush=True)

    import quadcoop  # noqa: F401
    import quadcoop.stage1  # noqa: F401
    import quadcoop.stage1b  # noqa: F401
    import quadcoop.stage1c  # noqa: F401
    from mjlab.envs import ManagerBasedRlEnv
    from mjlab.rl import MjlabOnPolicyRunner, RslRlVecEnvWrapper
    from mjlab.tasks.registry import load_env_cfg, load_rl_cfg
    from mjlab.utils.lab_api.math import quat_from_euler_xyz

    from quadcoop.stage1.mdp import wrap, yaw_of
    from quadcoop.stage1b.mdp import fold
    from quadcoop.stage1b.shapes import NOMINAL_MASS, OBJ_NAMES, SHAPES, SHAPE_NAMES

    objects = list(SHAPE_NAMES) if a.objects == "all" else [o.strip() for o in a.objects.split(",")]
    for o in objects:
        assert o in SHAPE_NAMES, f"unknown object {o}; choose from {SHAPE_NAMES}"
    scen = list(itertools.product(floats(a.distances), floats(a.directions),
                                  floats(a.yaw_changes), floats(a.start_yaws), range(a.reps)))
    ckpt = Path(a.checkpoint)
    out = Path(a.out) if a.out else ckpt.parent / f"eval_{ckpt.stem}"
    out.mkdir(parents=True, exist_ok=True)
    vw, vh = (int(x) for x in a.video_size.lower().split("x"))
    rows: list[dict] = []
    t0 = time.time()

    for mass in floats(a.masses):
        torch.manual_seed(a.seed)
        cfg = load_env_cfg(a.task, play=True)  # no curriculum, no observation noise
        n = len(objects) * len(scen)
        cfg.scene.num_envs = n
        cfg.episode_length_s = a.horizon + 10.0
        cfg.events["reset_base"].params["pose_range"]["yaw"] = (0.0, 0.0)
        alpha = 0.5 * math.log(mass / NOMINAL_MASS)
        for name in OBJ_NAMES:
            cfg.events[f"{name}_mass"].params["alpha_range"] = (alpha, alpha)
        # Terminations are evaluated here (same functions, same parameters) instead of by
        # the env, so nothing is reset mid-episode and the simulation runs on after a fall:
        # that is what lets us score "ignoring falls" and film what happens next.
        end_cfgs = {k: cfg.terminations.pop(k) for k in END_TERMS if k in cfg.terminations}
        # Falls are scored by the body's pose (quadcoop/falls.py: on its side, upside down
        # or collapsed). What the policy's own training rule (contacts / tilt) would have
        # said is reported alongside, in the *_train_rule columns.
        from quadcoop.falls import NOMINAL_HEIGHT, fall_reason, fallen as pose_fallen
        nom_h = NOMINAL_HEIGHT[robot_name]
        base = ManagerBasedRlEnv(cfg=cfg, device=device)
        env = RslRlVecEnvWrapper(base)
        runner = MjlabOnPolicyRunner(env, asdict(load_rl_cfg(a.task)), device=device)
        runner.load(str(ckpt), load_cfg={"actor": True}, strict=True, map_location=device)
        policy = runner.get_inference_policy(device=device)
        env.reset()

        g = base.command_manager.get_term("goal")
        robot = base.scene["robot"]
        dev = base.device
        ids = torch.arange(n, device=dev)

        def term(name: str) -> torch.Tensor:
            c = end_cfgs.get(name)
            if c is None:
                return torch.zeros(n, dtype=torch.bool, device=dev)
            return c.func(base, **(c.params or {})).bool()

        def tilt_deg() -> torch.Tensor:
            return torch.rad2deg(torch.acos((-robot.data.projected_gravity_b[:, 2]).clamp(-1, 1)))

        fall_sensor = base.scene["fall_contact"] if "fell_contact" in end_cfgs else None

        def fall_detail(j: int, over: bool) -> str:
            parts = []
            if over:
                parts.append(f"tilt {float(tilt_deg()[j]):.0f}deg")
            if fall_sensor is not None:
                found = fall_sensor.data.found[j].view(len(fall_sensor.primary_names), -1).any(-1)
                names = [fall_sensor.primary_names[i] for i in found.nonzero().flatten().tolist()]
                if names:
                    parts.append("contact: " + " ".join(names))
            return "; ".join(parts) or "?"

        # -- lay out every env's scenario -------------------------------------------------
        obj_idx = torch.tensor([SHAPE_NAMES.index(o) for o in objects for _ in scen], device=dev)
        S = torch.tensor([s[:4] for _ in objects for s in scen], device=dev, dtype=torch.float)
        dist_g, dir_g, dyaw_g, yaw0 = S[:, 0], torch.deg2rad(S[:, 1]), torch.deg2rad(S[:, 2]), torch.deg2rad(S[:, 3])
        q_adr = robot.indexing.free_joint_q_adr
        qpos = robot.data.data.qpos
        root = qpos[:, q_adr[0:3]]
        ryaw = yaw_of(qpos[:, q_adr[3:7]])
        reach = g.cfg.robot_reach + g.radius[obj_idx] + 0.4
        obj_xy = root[:, :2] + reach.unsqueeze(-1) * torch.stack([torch.cos(ryaw), torch.sin(ryaw)], -1)
        obj_h = ryaw + yaw0
        gdir = ryaw + dir_g
        goal_xy = obj_xy + dist_g.unsqueeze(-1) * torch.stack([torch.cos(gdir), torch.sin(gdir)], -1)
        goal_h = wrap(obj_h + dyaw_g)

        g.shape[:] = obj_idx
        g.env_level[:] = a.obs_level
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
            st[:, 2] = float(SHAPES[k].rest_height) + 0.005
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
        d0, e0 = g.errors()
        g.prev_dist[:] = d0
        g.prev_yaw_err[:] = e0.abs()
        obs = TensorDictFromEnv(base, n)

        # -- state recording for videos (rendered after the rollout, for chosen episodes) ---
        dt = base.step_dt
        rec = StateRecorder(base, dt) if a.videos > 0 else None
        if rec is not None:
            rec.add(0.0, d0, torch.rad2deg(e0.abs()), torch.zeros_like(d0), tilt_deg())
        snap = None
        if a.snapshots > 0:
            snap = Snapper(base, robot, g, q_adr, goal_xy, out / "snapshots", a.snapshots, dt,
                           fall_sensor.primary_names if fall_sensor is not None else [])
            for j in range(n):
                o = objects[j // len(scen)]
                dist, direc, dyaw, y0, rep = scen[j % len(scen)]
                snap.label[j] = (f"{o}  {mass:g} kg   goal {dist:g} m at {direc:g} deg, turn {dyaw:g} deg   "
                                 f"start yaw {y0:g}   rep {rep}")
                snap.stem[j] = f"{o}_{mass:g}kg_d{dist:g}_dir{direc:g}_turn{dyaw:g}_s{y0:g}_r{rep}"
                snap.obj[j] = o

        # -- roll out ------------------------------------------------------------------------
        # Track "b": falls do not end the episode. The official track ("a", the training
        # rules) is identical to b up to the first fall and ends there.
        steps = int(a.horizon / dt)
        pt, yt = a.pos_tol, math.radians(a.yaw_tol)
        nan = lambda: torch.full((n,), float("nan"), device=dev)  # noqa: E731
        done_b = torch.zeros(n, dtype=torch.bool, device=dev)
        fallen = torch.zeros(n, dtype=torch.bool, device=dev)
        fallen_t = torch.zeros(n, dtype=torch.bool, device=dev)  # under the policy's training rule
        t_fall_t = torch.full((n,), float("nan"), device=dev)
        detail_t = [""] * n
        how_b = ["horizon"] * n
        detail = [""] * n
        t_fall, t_reach, t_succ_b = nan(), nan(), nan()
        hold_b = torch.zeros(n, device=dev)
        hold_loose = torch.zeros(n, device=dev)
        succ_loose = torch.zeros(n, dtype=torch.bool, device=dev)
        last_da, last_ea = d0.clone(), e0.abs().clone()
        last_db = d0.clone()
        min_d = d0.clone()
        path = torch.zeros(n, device=dev)
        prev_xy = g.box_pos()[:, :2].clone()
        tele_step = None if a.selftest_teleport is None else int(a.selftest_teleport / dt)
        last_i = steps - 1
        b_end = torch.full((n,), steps - 1, dtype=torch.long, device=dev)  # step the b track ended
        all_done_at = None
        tail = int(2.0 / dt) if rec is not None else 0  # videos run on 2 s after the outcome
        with torch.no_grad():
            for i in range(steps):
                if i == tele_step:
                    for k, o in enumerate(g.objs):
                        sel = (obj_idx == k).nonzero().flatten()
                        if len(sel) == 0:
                            continue
                        st = torch.zeros(len(sel), 13, device=dev)
                        st[:, :2] = goal_xy[sel]
                        st[:, 2] = float(SHAPES[k].rest_height) + 0.005
                        st[:, 3:7] = gq[sel]
                        o.write_root_state_to_sim(st, sel)
                obs, _, _, _ = env.step(policy(obs))
                t = (i + 1) * dt
                live_b = ~done_b

                # falls (pose): recorded; the official track ends; the simulation goes on
                new_fall = pose_fallen(base, "robot", nom_h) & live_b & ~fallen
                for j in new_fall.nonzero().flatten().tolist():
                    detail[j] = fall_reason(base, j, "robot", nom_h)
                t_fall = torch.where(new_fall, torch.full_like(t_fall, t), t_fall)
                fallen |= new_fall
                # what the training rule (tilt > 70 deg or a listed geom on the ground) says
                f_over, f_cont = term("fell_over"), term("fell_contact")
                new_tfall = (f_over | f_cont) & live_b & ~fallen_t
                for j in new_tfall.nonzero().flatten().tolist():
                    detail_t[j] = fall_detail(j, bool(f_over[j]))
                t_fall_t = torch.where(new_tfall, torch.full_like(t_fall_t, t), t_fall_t)
                fallen_t |= new_tfall
                live_a = live_b & ~fallen

                # object tipped over / lost: ends both tracks
                tip, lost = term("box_tipped") & live_b, term("box_lost") & live_b
                for j in (tip | lost).nonzero().flatten().tolist():
                    how_b[j] = "tipped" if bool(tip[j]) else "lost"
                ended = tip | lost

                d, e = g.errors()
                ea = e.abs()
                xy = g.box_pos()[:, :2]
                path += torch.where(live_a, torch.linalg.norm(xy - prev_xy, dim=-1), torch.zeros_like(path))
                prev_xy = xy.clone()
                last_da = torch.where(live_a, d, last_da)
                last_ea = torch.where(live_a, ea, last_ea)
                last_db = torch.where(live_b, d, last_db)
                min_d = torch.where(live_a, torch.minimum(min_d, d), min_d)
                live_b2 = live_b & ~ended
                inside = live_b2 & (d < pt) & (ea < yt)
                inside_l = live_a & ~ended & (d < 2 * pt) & (ea < 2 * yt)
                t_reach = torch.where(inside & live_a & torch.isnan(t_reach), torch.full_like(t_reach, t), t_reach)
                hold_b = torch.where(inside, hold_b + dt, torch.zeros_like(hold_b))
                hold_loose = torch.where(inside_l, hold_loose + dt, torch.zeros_like(hold_loose))
                succ_loose |= hold_loose >= a.hold
                new_succ = (hold_b >= a.hold) & live_b2
                t_succ_b = torch.where(new_succ, torch.full_like(t_succ_b, t), t_succ_b)
                for j in new_succ.nonzero().flatten().tolist():
                    how_b[j] = "success"
                b_end = torch.where((ended | new_succ) & ~done_b, torch.full_like(b_end, i), b_end)
                done_b |= ended | new_succ

                if snap is not None:
                    snap.shoot(i, t, new_fall.nonzero().flatten().tolist(),
                               (ended | new_succ).nonzero().flatten().tolist(), detail, how_b, fallen, d, ea)

                if rec is not None and (i + 1) % rec.stride == 0:
                    rec.add(t, d, torch.rad2deg(ea), hold_b, tilt_deg())
                if all_done_at is None and bool(done_b.all()):
                    all_done_at = i
                if all_done_at is not None and i >= all_done_at + tail:
                    last_i = i
                    break
        tilt_end = tilt_deg()
        if snap is not None:
            d, e = g.errors()
            snap.shoot(last_i, (last_i + 1) * dt, [], (~done_b).nonzero().flatten().tolist(), detail, how_b,
                       fallen, d, e.abs(), final=True)

        first = len(rows)
        for j in range(n):
            o = objects[j // len(scen)]
            dist, direc, dyaw, y0, rep = scen[j % len(scen)]
            sym = SHAPES[SHAPE_NAMES.index(o)].symmetry
            eff = abs(math.degrees(float(fold(torch.tensor(math.radians(dyaw)), torch.tensor(float(sym))))))
            straight = float(d0[j])
            tf, tsb = float(t_fall[j]), float(t_succ_b[j])
            official = "fell" if bool(fallen[j]) else how_b[j]
            rnd = lambda x: "" if math.isnan(x) else round(x, 2)  # noqa: E731
            rows.append({
                "object": o, "mass": mass, "distance": dist, "direction": direc,
                "yaw_change": dyaw, "yaw_change_effective": round(eff, 1), "start_yaw": y0, "rep": rep,
                "success_strict": int(official == "success"), "success_loose": int(bool(succ_loose[j])),
                "outcome": official,
                "t_reach": rnd(float(t_reach[j])),
                "t_success": rnd(tsb) if official == "success" else "",
                "final_pos_err": round(float(last_da[j]), 3),
                "final_yaw_err": round(math.degrees(float(last_ea[j])), 1),
                "min_pos_err": round(float(min_d[j]), 3),
                "path_ratio": round(float(path[j]) / max(straight, 1e-3), 2),
                "t_fall": rnd(tf), "fall_detail": detail[j],
                "tilt_at_end": round(float(tilt_end[j]), 1),
                "success_ignoring_falls": int(how_b[j] == "success"),
                # what the policy's training rule (contacts / tilt) would have said
                "outcome_train_rule": "fell" if bool(fallen_t[j]) else how_b[j],
                "success_train_rule": int(how_b[j] == "success" and not bool(fallen_t[j])),
                "t_fall_train_rule": rnd(float(t_fall_t[j])),
                "train_rule_detail": detail_t[j],
                "outcome_ignoring_falls": how_b[j],
                "t_success_ignoring_falls": rnd(tsb),
                "final_pos_err_ignoring_falls": round(float(last_db[j]), 3),
                "snapshot": "",
                "video": "",
            })
        if snap is not None:
            for j, fn in snap.write([rows[first + j] for j in range(n)]).items():
                rows[first + j]["snapshot"] = fn
        if rec is not None:
            # pick up to --videos episodes per (object, outcome), at random but reproducibly
            import random

            groups = defaultdict(list)
            for j in range(n):
                groups[(rows[first + j]["object"], rows[first + j]["outcome"])].append(j)
            pick = []
            for key in sorted(groups):
                js = groups[key]
                random.Random(f"{a.seed}-{mass}-{key}").shuffle(js)
                pick += js[:a.videos]
            maker = VideoMaker(base, robot, g, q_adr, goal_xy, out / "videos", vw, vh, rec,
                               SHAPES, obj_idx)
            tv = time.time()
            for j in sorted(pick):
                r = rows[first + j]
                o = r["object"]
                label = (f"{o}  {mass:g} kg   goal {r['distance']:g} m at {r['direction']:g} deg, "
                         f"turn {r['yaw_change']:g} deg   start yaw {r['start_yaw']:g}   rep {r['rep']}")
                stem = (f"{o}_{mass:g}kg_d{r['distance']:g}_dir{r['direction']:g}_turn{r['yaw_change']:g}"
                        f"_s{r['start_yaw']:g}_r{r['rep']}")
                r["video"] = maker.make(j, label, stem, r, int(b_end[j]) + tail)
            maker.close()
            print(f"[mass {mass:g} kg] wrote {len(pick)} videos in {time.time() - tv:.0f} s", flush=True)
            del rec
        mine = rows[first:]
        print(f"[mass {mass:g} kg] {n} episodes: {sum(r['success_strict'] for r in mine)} strict successes, "
              f"{sum(r['success_ignoring_falls'] for r in mine)} if falls are ignored, "
              f"{sum(r['outcome'] == 'fell' for r in mine)} counted falls "
              f"({last_i + 1} steps, {time.time() - t0:.0f} s elapsed)", flush=True)
        env.close()
        del env, base, runner, policy

    write_outputs(rows, out, a)
    return 0


def newest_checkpoint(exp_dir: Path) -> Path:
    """Highest model_N.pt in the newest dated run (YYYY-MM-DD_...) of an experiment folder."""
    runs = sorted(p for p in exp_dir.glob("2*") if p.is_dir() and any(p.glob("model_*.pt")))
    if not runs:
        raise SystemExit(f"no dated run with model_*.pt in {exp_dir}; pass the path explicitly")
    return max(runs[-1].glob("model_*.pt"), key=lambda p: int(p.stem.split("_")[1]))


def TensorDictFromEnv(base, n):
    from tensordict import TensorDict

    return TensorDict(base.observation_manager.compute(update_history=True), batch_size=[n])


# -------------------------------------------------------------------------------------
class Snapper:
    """Still images of the moments that decide an episode.

    Counted fall:  overview + robot close-up at the fall (the ground-touching geoms in
                   red), close-up 2 s later (did it really go down?), overview at the end.
    Otherwise:     overview + robot close-up at the end (success / time up / tipped / lost).
    Every fall, tip-over and loss is kept; successes and time-ups up to ``quota`` per
    object (per mass build).
    """

    W, H = 480, 360

    def __init__(self, base, robot, g, q_adr, goal_xy, folder: Path, quota: int, dt: float,
                 contact_names: list[str]):
        import mujoco
        from PIL import ImageFont

        self.mj, self.base, self.robot, self.g, self.q_adr = mujoco, base, robot, g, q_adr
        self.folder, self.quota, self.after = folder, quota, int(round(2.0 / dt))
        m = base.sim.mj_model
        from mjlab.viewer.model_sync import disable_model_sameframe_shortcuts

        disable_model_sameframe_shortcuts(m)  # else rotated geoms (lying cylinder) render wrongly
        m.vis.global_.offwidth = max(int(m.vis.global_.offwidth), self.W)
        m.vis.global_.offheight = max(int(m.vis.global_.offheight), self.H)
        m.stat.extent = 12.0
        self.m, self.d = m, mujoco.MjData(m)
        self.r = mujoco.Renderer(m, height=self.H, width=self.W)
        self.cam = mujoco.MjvCamera()
        self.cam.type = mujoco.mjtCamera.mjCAMERA_FREE
        self.opt = mujoco.MjvOption()
        # robot geom ids by short name, to paint the ones that touched the ground
        self.geom_id = {}
        for gid in range(m.ngeom):
            nm = mujoco.mj_id2name(m, mujoco.mjtObj.mjOBJ_GEOM, gid) or ""
            if nm.startswith("robot/") or nm in contact_names:
                self.geom_id[nm.split("/")[-1]] = gid
        try:
            self.font, self.big = ImageFont.load_default(size=14), ImageFont.load_default(size=16)
        except TypeError:
            self.font = self.big = ImageFont.load_default()
        n = base.num_envs
        self.goal = goal_xy.cpu()
        start = robot.data.data.qpos[:, q_adr[0:2]].cpu()
        dxy = self.goal - start
        self.az = torch.rad2deg(torch.atan2(dxy[:, 1], dxy[:, 0])) + 90.0
        self.label, self.stem, self.obj = {}, {}, {}
        self.panels: dict[int, list] = defaultdict(list)
        self.pending: dict[int, int] = {}  # env -> step of the "2 s after the fall" shot
        self.sync = None  # optional callable(env) run before rendering that env
        self.count: dict[tuple, int] = defaultdict(int)
        self.keep: set[int] = set()
        self.n = n

    def shoot(self, i, t, falls, ends, detail, how, fallen, d, e, final=False):
        jobs = []  # (env, view, caption, red geoms)
        for j in falls:
            names = [s for part in detail[j].split("; ") if part.startswith("contact: ")
                     for s in part[len("contact: "):].split()]
            jobs += [(j, "over", f"counted fall at {t:.1f} s", []),
                     (j, "close", f"robot at the fall ({detail[j]})", names)]
            self.pending[j] = i + self.after
            self.keep.add(j)
        due = [j for j, s in self.pending.items() if s <= i or final]
        for j in due:
            when = "end of the episode" if final else "2 s after the fall"
            jobs.append((j, "close", f"robot at {t:.1f} s ({when})", []))
            del self.pending[j]
        for j in ends:
            oc = "fell" if bool(fallen[j]) else how[j]
            if oc in ("success", "horizon"):
                key = (self.obj[j], oc)
                if self.count[key] >= self.quota:
                    continue
                self.count[key] += 1
            self.keep.add(j)
            what = {"success": "success", "horizon": "time up", "tipped": "object tipped over",
                    "lost": "object lost"}[how[j]]
            if oc == "fell":
                what += " (simulation went on after the fall)"
            jobs.append((j, "over", f"end at {t:.1f} s: {what}", []))
            if oc != "fell":
                jobs.append((j, "close", f"robot at the end ({what})", []))
        if not jobs:
            return
        envs = sorted({j for j, *_ in jobs})
        idx = torch.tensor(envs, device=self.base.device)
        sd = self.base.sim.data
        qpos = sd.qpos[idx].cpu().numpy()
        mpos = sd.mocap_pos[idx].cpu().numpy() if self.m.nmocap else None
        mquat = sd.mocap_quat[idx].cpu().numpy() if self.m.nmocap else None
        from quadcoop.stage1.mdp import yaw_of
        rq = sd.qpos[idx]
        rpos = rq[:, self.q_adr[0:3]].cpu()
        ryaw = torch.rad2deg(yaw_of(rq[:, self.q_adr[3:7]])).cpu()
        bxy = self.g.box_pos()[idx][:, :2].cpu()
        err = torch.stack([d[idx], torch.rad2deg(e[idx])], -1).cpu()
        row = {j: k for k, j in enumerate(envs)}
        for j, view, caption, red in jobs:
            k = row[j]
            if self.sync is not None:
                self.sync(j)  # per-env geometry (Stage 2 randomizes object sizes per env)
            self.d.qpos[:] = qpos[k]
            if mpos is not None:
                self.d.mocap_pos[:] = mpos[k]
                self.d.mocap_quat[:] = mquat[k]
            self.mj.mj_forward(self.m, self.d)
            if view == "over":
                pts = torch.stack([rpos[k, :2], bxy[k], self.goal[j]])
                c = pts.mean(0)
                self.cam.lookat[:] = [float(c[0]), float(c[1]), 0.3]
                self.cam.distance = max(4.0, min(14.0, 1.1 * float(torch.cdist(pts, pts).max()) + 3.0))
                self.cam.azimuth, self.cam.elevation = float(self.az[j]), -35.0
                caption += f"   pos err {float(err[k, 0]):.2f} m  yaw err {float(err[k, 1]):.1f} deg"
            else:
                self.cam.lookat[:] = [float(rpos[k, 0]), float(rpos[k, 1]), 0.25]
                # side view from the side of the geoms that touched (left legs -> from the left)
                side = -90.0 if red and all(nm.lower()[:2] in ("lf", "lh", "fl", "hl") for nm in red) else 90.0
                self.cam.distance, self.cam.azimuth, self.cam.elevation = 1.9, float(ryaw[k]) + side, -18.0
            saved = []
            for nm in red:
                gid = self.geom_id.get(nm)
                if gid is not None:
                    saved.append((gid, int(self.m.geom_group[gid]), self.m.geom_rgba[gid].copy()))
                    self.m.geom_group[gid] = 0
                    self.m.geom_rgba[gid] = (1.0, 0.1, 0.1, 1.0)
            self.r.update_scene(self.d, camera=self.cam, scene_option=self.opt)
            img = self.r.render().copy()
            for gid, grp, rgba in saved:
                self.m.geom_group[gid] = grp
                self.m.geom_rgba[gid] = rgba
            self.panels[j].append((caption, img))

    def write(self, rows: list[dict]) -> dict[int, str]:
        from PIL import Image, ImageDraw

        names = {}
        for j in sorted(self.keep):
            panels = self.panels.get(j)
            if not panels:
                continue
            r = rows[j]
            head = 52
            sheet = Image.new("RGB", (self.W * len(panels), self.H + head), (20, 20, 20))
            dr = ImageDraw.Draw(sheet)
            dr.text((8, 4), self.label[j], font=self.big, fill=(255, 255, 255))
            line = f"official: {r['outcome'].upper()}"
            if r["outcome"] == "fell":
                line += f" at {r['t_fall']} s ({r['fall_detail']}), robot tilt at end {r['tilt_at_end']} deg"
                line += f"   |   ignoring falls: {r['outcome_ignoring_falls']}"
            elif r["outcome"] == "success":
                line += f" at {r['t_success']} s"
            line += f"   |   final pos err {r['final_pos_err']} m, yaw err {r['final_yaw_err']} deg"
            color = (110, 255, 120) if r["outcome"] == "success" else (255, 140, 90)
            dr.text((8, 28), line, font=self.font, fill=color)
            for p, (cap, img) in enumerate(panels):
                im = Image.fromarray(img)
                pd = ImageDraw.Draw(im, "RGBA")
                pd.rectangle([0, 0, self.W, 20], fill=(0, 0, 0, 160))
                pd.text((5, 2), cap, font=self.font, fill=(255, 255, 255))
                sheet.paste(im, (p * self.W, head))
            sub = self.folder / r["outcome"]
            sub.mkdir(parents=True, exist_ok=True)
            fn = sub / f"{self.stem[j]}.jpg"
            sheet.save(fn, quality=85)
            names[j] = f"snapshots/{r['outcome']}/{fn.name}"
        self.r.close()
        return names


class StateRecorder:
    """Keeps every env's full qpos at ~25 fps (plus the overlay numbers) during the rollout,
    so any episode can be rendered afterwards exactly as it happened."""

    def __init__(self, base, dt: float):
        self.base, self.dt = base, dt
        self.stride = max(1, round(1.0 / (25.0 * dt)))
        self.fps = 1.0 / (self.stride * dt)
        sd = base.sim.data
        nm = base.sim.mj_model.nmocap
        self.mocap_pos = sd.mocap_pos.cpu().numpy() if nm else None  # goals do not move
        self.mocap_quat = sd.mocap_quat.cpu().numpy() if nm else None
        self.q: list[torch.Tensor] = []
        self.info: list[torch.Tensor] = []
        self.t: list[float] = []

    def add(self, t: float, d, e_deg, hold, tilt) -> None:
        self.q.append(self.base.sim.data.qpos.detach().to("cpu", torch.float32))
        self.info.append(torch.stack([d, e_deg, hold, tilt], -1).cpu())
        self.t.append(t)


class VideoMaker:
    """Renders one recorded episode to MP4: overview (left) and robot close-up (right).

    The overlay shows the scenario, time, errors, hold timer and robot tilt; from the
    moment a fall is counted it says so, and the ground-touching geoms are painted red
    for a moment in the close-up. The video runs on to the end of the "ignoring falls"
    outcome plus 2 s, so you can see whether the robot really went down.
    """

    def __init__(self, base, robot, g, q_adr, goal_xy, folder: Path, w: int, h: int, rec: StateRecorder,
                 shapes, obj_idx):
        import mujoco
        from PIL import ImageFont

        self.mj, self.rec, self.folder, self.w, self.h = mujoco, rec, folder, w, h
        folder.mkdir(parents=True, exist_ok=True)
        m = base.sim.mj_model
        from mjlab.viewer.model_sync import disable_model_sameframe_shortcuts

        disable_model_sameframe_shortcuts(m)  # else rotated geoms (lying cylinder) render wrongly
        m.vis.global_.offwidth = max(int(m.vis.global_.offwidth), w)
        m.vis.global_.offheight = max(int(m.vis.global_.offheight), h)
        m.stat.extent = 12.0
        self.m, self.d = m, mujoco.MjData(m)
        self.r = mujoco.Renderer(m, height=h, width=w)
        self.cam = mujoco.MjvCamera()
        self.cam.type = mujoco.mjtCamera.mjCAMERA_FREE
        self.opt = mujoco.MjvOption()
        self.rq = [int(x) for x in q_adr[0:7].tolist()] if hasattr(q_adr, "tolist") else list(q_adr[0:7])
        self.obj_q = [[int(x) for x in (o.indexing.free_joint_q_adr[0:2].tolist())] for o in g.objs]
        self.obj_idx = obj_idx.cpu().tolist()
        self.goal = goal_xy.cpu().numpy()
        self.geom_id = {}
        for gid in range(m.ngeom):
            nm = mujoco.mj_id2name(m, mujoco.mjtObj.mjOBJ_GEOM, gid) or ""
            if nm.startswith("robot/"):
                self.geom_id[nm.split("/")[-1]] = gid
        self.sync = None  # optional callable(env) run before rendering that env (per-env geometry)
        self.overlay = None  # optional callable(env, frame index, PIL image) to draw extra panels
        try:
            self.font, self.big = ImageFont.load_default(size=13), ImageFont.load_default(size=20)
        except TypeError:
            self.font = self.big = ImageFont.load_default()

    def make(self, j: int, label: str, stem: str, row: dict, end_step: int) -> str:
        import imageio_ffmpeg
        import numpy as np
        from PIL import Image, ImageDraw

        rec, w, h = self.rec, self.w, self.h
        nf = min(len(rec.q), (end_step + 1) // rec.stride + 1)
        sub = self.folder / row["outcome"]
        sub.mkdir(parents=True, exist_ok=True)
        path = sub / f"{stem}.mp4"
        wr = imageio_ffmpeg.write_frames(str(path), (2 * w, h), fps=rec.fps, quality=6, macro_block_size=8,
                                         ffmpeg_log_level="error")
        wr.send(None)
        tf = float(row["t_fall"]) if row["t_fall"] != "" else float("nan")
        # the geoms the old (training) contact rule flagged, painted red around that moment
        tft = float(row["t_fall_train_rule"]) if row["t_fall_train_rule"] != "" else float("nan")
        red = [s for part in row["train_rule_detail"].split("; ") if part.startswith("contact: ")
               for s in part[len("contact: "):].split()]
        red_ids = [self.geom_id[nm] for nm in red if nm in self.geom_id]
        side = -90.0 if red and all(nm.lower()[:2] in ("lf", "lh", "fl", "hl") for nm in red) else 90.0
        t_end_b = (end_step - int(2.0 / rec.dt) + 1) * rec.dt  # when the b-track outcome was decided
        gx, gy = self.goal[j]
        k_obj = self.obj_idx[j]
        rx0, ry0 = (float(rec.q[0][j, self.rq[0]]), float(rec.q[0][j, self.rq[1]]))
        az = math.degrees(math.atan2(gy - ry0, gx - rx0)) + 90.0
        look = None
        if self.sync is not None:
            self.sync(j)
        for f in range(nf):
            q = rec.q[f][j].numpy().astype(np.float64)
            t = rec.t[f]
            self.d.qpos[:] = q
            if rec.mocap_pos is not None:
                self.d.mocap_pos[:] = rec.mocap_pos[j]
                self.d.mocap_quat[:] = rec.mocap_quat[j]
            self.mj.mj_forward(self.m, self.d)
            rx, ry = q[self.rq[0]], q[self.rq[1]]
            bx, by = q[self.obj_q[k_obj][0]], q[self.obj_q[k_obj][1]]
            pts = np.array([[rx, ry], [bx, by], [gx, gy]])
            c = pts.mean(0)
            spread = max(np.linalg.norm(pts[a_] - pts[b_]) for a_ in range(3) for b_ in range(3))
            want = (c, max(4.0, min(14.0, 1.1 * spread + 3.0)))
            look = want if look is None else (0.92 * look[0] + 0.08 * want[0], 0.96 * look[1] + 0.04 * want[1])
            self.cam.lookat[:] = [look[0][0], look[0][1], 0.3]
            self.cam.distance, self.cam.azimuth, self.cam.elevation = look[1], az, -35.0
            self.r.update_scene(self.d, camera=self.cam, scene_option=self.opt)
            left = self.r.render().copy()
            # close-up: side view of the robot
            qw, qx, qy, qz = q[self.rq[3]], q[self.rq[4]], q[self.rq[5]], q[self.rq[6]]
            yaw = math.degrees(math.atan2(2 * (qw * qz + qx * qy), 1 - 2 * (qy * qy + qz * qz)))
            self.cam.lookat[:] = [rx, ry, 0.25]
            self.cam.distance, self.cam.azimuth, self.cam.elevation = 2.0, yaw + side, -18.0
            paint = red_ids and not math.isnan(tft) and tft - 0.3 <= t <= tft + 1.5
            saved = []
            if paint:
                for gid in red_ids:
                    saved.append((gid, int(self.m.geom_group[gid]), self.m.geom_rgba[gid].copy()))
                    self.m.geom_group[gid] = 0
                    self.m.geom_rgba[gid] = (1.0, 0.1, 0.1, 1.0)
            self.r.update_scene(self.d, camera=self.cam, scene_option=self.opt)
            right = self.r.render().copy()
            for gid, grp, rgba in saved:
                self.m.geom_group[gid] = grp
                self.m.geom_rgba[gid] = rgba

            im = Image.fromarray(np.concatenate([left, right], axis=1))
            dr = ImageDraw.Draw(im, "RGBA")
            dist, yerr, hold, tilt = rec.info[f][j].tolist()
            dr.rectangle([0, 0, 2 * w, 44], fill=(0, 0, 0, 160))
            dr.text((6, 3), label, font=self.font, fill=(255, 255, 255))
            dr.text((6, 23), f"t {t:5.1f} s   pos err {dist:5.2f} m   yaw err {yerr:5.1f} deg   "
                             f"hold {hold:3.1f} s   robot tilt {tilt:3.0f} deg", font=self.font, fill=(220, 220, 220))
            dr.text((w + 6, 23), "robot close-up" + ("  (red = what the old contact rule flagged)" if paint else ""),
                    font=self.font, fill=(220, 220, 220))
            if not math.isnan(tft) and t >= tft and (math.isnan(tf) or t < tf):
                dr.rectangle([0, 44, 2 * w, 64], fill=(60, 60, 0, 150))
                dr.text((6, 47), f"old training rule would have ended the episode at {tft:.1f} s "
                                 f"({row['train_rule_detail']}); not a fall by pose", font=self.font,
                        fill=(255, 240, 150))
            if not math.isnan(tf) and t >= tf:
                dr.rectangle([0, 44, 2 * w, 64], fill=(120, 30, 0, 170))
                dr.text((6, 47), f"FELL at {tf:.1f} s: {row['fall_detail']}; the official episode "
                                 f"ends here; still simulating", font=self.font, fill=(255, 200, 160))
            if t >= t_end_b - 1e-6 and f > 0 and (row["outcome_ignoring_falls"] != "horizon" or f == nf - 1):
                oc = row["outcome_ignoring_falls"]
                msg, col = {"success": ("SUCCESS", (110, 255, 120)), "tipped": ("OBJECT TIPPED OVER", (255, 90, 90)),
                            "lost": ("OBJECT LOST", (255, 90, 90)), "horizon": ("TIME UP", (255, 200, 80)),
                            "fell": ("FELL", (255, 90, 90))}[oc]
                if oc == "success" and not math.isnan(tf):
                    msg += " (after the counted fall, so officially a failure)"
                dr.rectangle([0, h - 32, 2 * w, h], fill=(0, 0, 0, 170))
                dr.text((8, h - 29), msg, font=self.big, fill=col)
            if self.overlay is not None:
                self.overlay(j, f, im)
            wr.send(im.tobytes())
        wr.close()
        return f"videos/{row['outcome']}/{path.name}"

    def close(self) -> None:
        self.r.close()


# -------------------------------------------------------------------------------------
def write_outputs(rows: list[dict], out: Path, a) -> None:
    with open(out / "episodes.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    def agg(sel: list[dict]) -> dict:
        n = len(sel)
        succ = [r for r in sel if r["success_strict"]]
        ts = sorted(float(r["t_success"]) for r in succ)
        tr = sorted(float(r["t_reach"]) for r in sel if r["t_reach"] != "")
        med = lambda v: v[len(v) // 2] if v else None  # noqa: E731
        fell = [r for r in sel if r["outcome"] == "fell"]
        return {
            "episodes": n,
            "success": round(len(succ) / n, 3) if n else None,
            "success_loose": round(sum(r["success_loose"] for r in sel) / n, 3) if n else None,
            "success_ignoring_falls": round(sum(r["success_ignoring_falls"] for r in sel) / n, 3) if n else None,
            "t_success_median": med(ts),
            "t_reach_median": med(tr),
            "final_pos_err_mean": round(sum(r["final_pos_err"] for r in sel) / n, 3) if n else None,
            "final_yaw_err_mean": round(sum(r["final_yaw_err"] for r in sel) / n, 1) if n else None,
            "final_pos_err_success": round(sum(r["final_pos_err"] for r in succ) / len(succ), 3) if succ else None,
            "path_ratio_success": round(sum(r["path_ratio"] for r in succ) / len(succ), 2) if succ else None,
            "fell": round(len(fell) / n, 3) if n else None,
            "success_train_rule": round(sum(r["success_train_rule"] for r in sel) / n, 3) if n else None,
            "fell_train_rule": round(sum(r["outcome_train_rule"] == "fell" for r in sel) / n, 3) if n else None,
            # of the counted falls, the share whose robot was still down (tilt > 45 deg) at the end
            "fell_stayed_down": round(sum(float(r["tilt_at_end"]) > 45 for r in fell) / len(fell), 2) if fell else None,
            "tipped": round(sum(r["outcome"] == "tipped" for r in sel) / n, 3) if n else None,
            "lost": round(sum(r["outcome"] == "lost" for r in sel) / n, 3) if n else None,
        }

    def by(*keys):
        groups = defaultdict(list)
        for r in rows:
            groups[tuple(r[k] for k in keys)].append(r)
        return {" / ".join(str(x) for x in k): agg(v) for k, v in sorted(groups.items())}

    triggers: dict[str, int] = defaultdict(int)
    for r in rows:
        if r["outcome"] == "fell":  # real falls, by pose
            triggers["FALL: " + r["fall_detail"].split(" (")[0]] += 1
        if r["outcome_train_rule"] == "fell":  # what the old training rule flagged
            for part in r["train_rule_detail"].split("; "):
                if part.startswith("contact: "):
                    for gname in part[len("contact: "):].split():
                        triggers[f"training rule: ground contact {gname}"] += 1
                elif part.startswith("tilt"):
                    triggers["training rule: tilt > 70 deg"] += 1
        if r["outcome_train_rule"] == "fell" and r["outcome"] != "fell":
            triggers["training rule flagged a fall, but the robot never fell by pose"] += 1

    summary = {
        "config": {k: v for k, v in vars(a).items()},
        "overall": agg(rows),
        "by_object": by("object"),
        "by_mass": by("mass"),
        "by_object_mass": by("object", "mass"),
        "by_distance": by("distance"),
        "by_direction": by("direction"),
        "by_yaw_change_effective": by("yaw_change_effective"),
        "fall_triggers": dict(sorted(triggers.items(), key=lambda kv: -kv[1])),
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2))
    write_snapshot_index(rows, out)

    cols = ["episodes", "success", "success_loose", "success_ignoring_falls", "success_train_rule",
            "t_success_median", "t_reach_median", "final_pos_err_mean", "final_yaw_err_mean", "fell",
            "fell_train_rule", "fell_stayed_down",
            "tipped", "lost"]
    lines = [f"# Push evaluation: {a.checkpoint}",
             f"tolerance {a.pos_tol} m / {a.yaw_tol} deg, hold {a.hold} s, horizon {a.horizon} s\n"]
    for title in ("overall", "by_object", "by_mass", "by_distance", "by_direction",
                  "by_yaw_change_effective", "by_object_mass"):
        block = summary[title] if title != "overall" else {"all": summary["overall"]}
        lines.append(f"## {title}\n")
        lines.append("| group | " + " | ".join(cols) + " |")
        lines.append("|---" * (len(cols) + 1) + "|")
        for k, v in block.items():
            lines.append(f"| {k} | " + " | ".join("" if v[c] is None else str(v[c]) for c in cols) + " |")
        lines.append("")
    lines.append("## fall_triggers\n")
    lines.append("(FALL = real falls by body pose; 'training rule' = what the rule the policy was trained "
                 "with flagged, one fall can have several geoms)\n")
    for k, v in summary["fall_triggers"].items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    (out / "summary.md").write_text("\n".join(lines))
    print("\n".join(summary_sections(lines, ("overall", "by_object", "by_mass", "fall_triggers"))))
    print(f"\nwrote {out}/episodes.csv, summary.json, summary.md")

    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:  # noqa: BLE001
        print("(matplotlib not installed: skipping plots)")
        return
    objs = sorted({r["object"] for r in rows})
    masses = sorted({r["mass"] for r in rows})
    som = summary["by_object_mass"]
    fig, axes = plt.subplots(1, 4, figsize=(21, 4.5))
    for o in objs:
        get = lambda key: [np_nan(som[f"{o} / {m}"][key]) for m in masses]  # noqa: E731
        axes[0].plot(masses, get("success"), marker="o", label=o)
        axes[1].plot(masses, get("success_ignoring_falls"), marker="o", label=o)
        axes[2].plot(masses, get("t_success_median"), marker="o", label=o)
        axes[3].plot(masses, get("final_pos_err_mean"), marker="o", label=o)
    for ax, title, yl in zip(axes, ("success rate (strict, held)", "success if falls did not end it",
                                    "median time to success", "final position error"),
                             ("fraction", "fraction", "s", "m"), strict=True):
        ax.set_title(title)
        ax.set_xlabel("object mass (kg)")
        ax.set_ylabel(yl)
        ax.grid(alpha=0.3)
    axes[0].legend(fontsize=7, ncol=2)
    fig.tight_layout()
    fig.savefig(out / "vs_mass.png", dpi=130)
    print(f"wrote {out}/vs_mass.png")


def write_snapshot_index(rows: list[dict], out: Path) -> None:
    """snapshots/index.html: every snapshot, grouped by outcome, then object and mass."""
    shots = [r for r in rows if r.get("snapshot")]
    if not shots:
        return
    order = ("fell", "tipped", "lost", "horizon", "success")
    html = ["<html><head><meta charset='utf-8'><title>push eval snapshots</title><style>"
            "body{font-family:sans-serif;background:#111;color:#ddd;margin:16px}"
            "img{max-width:100%;margin:4px 0 18px}h2{border-bottom:1px solid #444}"
            "a{color:#8cf}</style></head><body><h1>Snapshots</h1><p>"]
    html.append(" | ".join(f"<a href='#{o}'>{o} ({sum(r['outcome'] == o for r in shots)})</a>"
                           for o in order if any(r["outcome"] == o for r in shots)))
    html.append("</p>")
    for o in order:
        sel = sorted((r for r in shots if r["outcome"] == o), key=lambda r: (r["object"], r["mass"]))
        if not sel:
            continue
        html.append(f"<h2 id='{o}'>{o}</h2>")
        for r in sel:
            vid = f" <a href='../{r['video']}'>[video]</a>" if r.get("video") else ""
            html.append(f"<div>{r['object']} {r['mass']:g} kg, goal {r['distance']:g} m at "
                        f"{r['direction']:g} deg, turn {r['yaw_change']:g} deg {r['fall_detail']}{vid}</div>")
            html.append(f"<img loading='lazy' src='{r['snapshot'][len('snapshots/'):]}'>")
    html.append("</body></html>")
    (out / "snapshots").mkdir(exist_ok=True)
    (out / "snapshots" / "index.html").write_text("\n".join(html))


def summary_sections(lines: list[str], names: tuple[str, ...]) -> list[str]:
    out, on = lines[:2], False
    for ln in lines[2:]:
        if ln.startswith("## "):
            on = ln[3:].strip() in names
        if on:
            out.append(ln)
    return out


def np_nan(x):
    return float("nan") if x is None else x


if __name__ == "__main__":
    raise SystemExit(main())