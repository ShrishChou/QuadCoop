"""Evaluate a Stage 2 policy (2a / 2b / ctrl): seen vs unseen shapes and sizes, and
ablations that show whether the policy actually uses its heading input and its profiles.

For every mass (one env build each), size set and condition, every object x scenario
(goal distance, direction, turn, object start yaw) is run deterministically from the
same start (robot pose, object pose and object size are identical across conditions):

size sets   in    size factors uniform in 0.8-1.2 per axis (the training range)
            out   factors in 0.6-0.75 or 1.25-1.4 per axis (one side per object): outside it
objects     seen = the 7 training shapes; unseen = beam, l_shape, asym, u_channel, plus
conditions  normal         what the policy was trained with
            heading_zero   object heading relative to the robot reads 0 in the numeric input
                           (box sin/cos); the goal's yaw error stays true. For 2b the map still
                           shows the true orientation, so 2b can recover it from the map.
            heading_zero_map  (2b) heading 0 in the numeric input AND the map drawn unrotated
            profile_zero   profile images all zero
            profile_roll   every env gets another env's images (a different object / size /
                           pose), so the images are realistic but wrong

Per episode: success (held inside --pos-tol / --yaw-tol for --hold s), outcome (success /
horizon / fell / tipped / lost; falls by body pose, quadcoop/falls.py), errors, times.

Does the output change at all? During every "normal" rollout, every --probe-every steps
the same observation is also built under each ablation and fed to the policy: the mean
|action change| (per walker-command component and relative to the mean |action|) is in
summary.md "action sensitivity". Near zero = the policy ignores that input.

Outputs (default: next to the checkpoint, in eval2_<ckpt>/):
    episodes.csv, summary.json, summary.md (success by object group x condition, per object,
    arch by start yaw, action sensitivity), videos/<condition>/<size>/<outcome>/*.mp4 with
    the images the policy sees drawn in the corner, videos/index.html.

    QUADCOOP_WALKER_CKPT=<walker.pt> MUJOCO_GL=egl python scripts/eval_push2.py \\
        --task QuadCoop-Push2a-AnymalC                 # newest push2a_anymal_c run
"""

from __future__ import annotations

import argparse
import csv
import itertools
import json
import math
import os
import random
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

from eval_push import StateRecorder, VideoMaker, newest_checkpoint  # noqa: E402

CONDITIONS = ("normal", "heading_zero", "heading_zero_map", "profile_zero", "profile_roll")
SIZE_SETS = ("in", "out")


def floats(s: str) -> list[float]:
    return [float(x) for x in s.split(",") if x.strip()]


def set_condition(g, cond: str) -> None:
    g.heading_zero = cond in ("heading_zero", "heading_zero_map")
    g.heading_zero_map = cond == "heading_zero_map"
    g.profile_mode = {"profile_zero": "zero", "profile_roll": "roll"}.get(cond, "normal")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--task", required=True, help="QuadCoop-Push2{a,b,ctrl}-{AnymalC,Spot}")
    ap.add_argument("--checkpoint", default=None, help="default: newest dated run of push2<v>_<robot>, highest N")
    ap.add_argument("--walker", default=None)
    ap.add_argument("--objects", default="all")
    ap.add_argument("--conditions", default=None,
                    help=f"comma list from {CONDITIONS} (default: all that apply to the variant)")
    ap.add_argument("--sizes", default="in,out", help="size sets: in,out")
    ap.add_argument("--masses", default="10,25,40")
    ap.add_argument("--distances", default="2,4")
    ap.add_argument("--directions", default="0,90,180")
    ap.add_argument("--yaw-changes", default="0,90")
    ap.add_argument("--start-yaws", default="0,45,90")
    ap.add_argument("--reps", type=int, default=1)
    ap.add_argument("--horizon", type=float, default=40.0)
    ap.add_argument("--pos-tol", type=float, default=0.10)
    ap.add_argument("--yaw-tol", type=float, default=6.0)
    ap.add_argument("--hold", type=float, default=1.0)
    ap.add_argument("--obs-level", type=int, default=5)
    ap.add_argument("--probe-every", type=int, default=10, help="steps between action-sensitivity probes")
    ap.add_argument("--videos", type=int, default=2,
                    help="normal condition: MP4s per (size set, object, outcome) for --video-mass")
    ap.add_argument("--ablation-videos", type=int, default=1,
                    help="ablations: MP4s per (object, outcome), size set 'in' only")
    ap.add_argument("--video-mass", type=float, default=None, help="mass build to film (default: middle one)")
    ap.add_argument("--video-size", default="480x360")
    ap.add_argument("--out", default=None)
    ap.add_argument("--device", default=None)
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    device = a.device or ("cuda:0" if torch.cuda.is_available() else "cpu")

    variant = "ctrl" if "ctrl" in a.task.lower() else ("b" if "push2b" in a.task.lower() else "a")
    robot_name = "spot" if "spot" in a.task.lower() else "anymal_c"
    per_robot = f"QUADCOOP_WALKER_CKPT_{robot_name.upper()}"
    if a.walker:
        os.environ["QUADCOOP_WALKER_CKPT"] = a.walker
        os.environ.pop(per_robot, None)
    elif not (os.environ.get("QUADCOOP_WALKER_CKPT") or os.environ.get(per_robot)):
        os.environ["QUADCOOP_WALKER_CKPT"] = str(newest_checkpoint(ROOT / "logs/rsl_rl" / f"walker_{robot_name}"))
    if a.checkpoint is None:
        a.checkpoint = str(newest_checkpoint(ROOT / "logs/rsl_rl" / f"push2{variant}_{robot_name}"))
    applicable = {"a": ("normal", "heading_zero", "profile_zero", "profile_roll"),
                  "b": CONDITIONS, "ctrl": ("normal", "heading_zero")}[variant]
    conds = list(applicable) if a.conditions is None else [c.strip() for c in a.conditions.split(",")]
    for c in conds:
        assert c in applicable, f"condition {c} does not apply to variant {variant} ({applicable})"
    if "normal" in conds:
        conds = ["normal"] + [c for c in conds if c != "normal"]
    sizes = [s.strip() for s in a.sizes.split(",")]
    assert all(s in SIZE_SETS for s in sizes), sizes
    print(f"variant {variant}\npolicy: {a.checkpoint}\nwalker: "
          f"{os.environ.get(per_robot) or os.environ['QUADCOOP_WALKER_CKPT']}\nconditions: {conds}", flush=True)

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

    from quadcoop.falls import NOMINAL_HEIGHT, fall_reason, fallen as pose_fallen
    from quadcoop.stage1.mdp import wrap, yaw_of
    from quadcoop.stage1b.mdp import fold
    from quadcoop.stage1b.shapes import NOMINAL_MASS
    from quadcoop.stage2 import mdp as m2
    from quadcoop.stage2.shapes import FACTOR_RANGE, HELDOUT_NAMES, OBJ_NAMES2, SHAPE_NAMES2, SHAPES2, TRAIN_NAMES

    objects = list(SHAPE_NAMES2) if a.objects == "all" else [o.strip() for o in a.objects.split(",")]
    for o in objects:
        assert o in SHAPE_NAMES2, f"unknown object {o}; choose from {SHAPE_NAMES2}"
    scen = list(itertools.product(floats(a.distances), floats(a.directions), floats(a.yaw_changes),
                                  floats(a.start_yaws), range(a.reps)))
    masses = floats(a.masses)
    video_mass = a.video_mass if a.video_mass is not None else masses[len(masses) // 2]
    ckpt = Path(a.checkpoint)
    out = Path(a.out) if a.out else ckpt.parent / f"eval2_{ckpt.stem}"
    out.mkdir(parents=True, exist_ok=True)
    vw, vh = (int(x) for x in a.video_size.lower().split("x"))
    nom_h = NOMINAL_HEIGHT[robot_name]
    rows: list[dict] = []
    sens: dict[str, list[torch.Tensor]] = defaultdict(list)  # condition -> |da| samples (k, 3)
    act_mag: list[torch.Tensor] = []
    t0 = time.time()

    for mass in masses:
        cfg = load_env_cfg(a.task, play=True)
        n = len(objects) * len(scen)
        cfg.scene.num_envs = n
        cfg.episode_length_s = 1e5  # episodes are ended here, never by a time-out reset
        cfg.events["reset_base"].params["pose_range"]["yaw"] = (0.0, 0.0)
        alpha = 0.5 * math.log(mass / NOMINAL_MASS)
        for name in OBJ_NAMES2:
            cfg.events[f"{name}_mass"].params["alpha_range"] = (alpha, alpha)
        end_cfgs = {k: cfg.terminations.pop(k) for k in ("fell_over", "box_tipped", "box_lost")}
        torch.manual_seed(a.seed)
        base = ManagerBasedRlEnv(cfg=cfg, device=device)
        env = RslRlVecEnvWrapper(base)
        runner = MjlabOnPolicyRunner(env, asdict(load_rl_cfg(a.task)), device=device)
        runner.load(str(ckpt), load_cfg={"actor": True}, strict=True, map_location=device)
        policy = runner.get_inference_policy(device=device)
        g = base.command_manager.get_term("goal")
        robot = base.scene["robot"]
        dev = base.device
        ids = torch.arange(n, device=dev)
        obj_idx = torch.tensor([SHAPE_NAMES2.index(o) for o in objects for _ in scen], device=dev)
        S = torch.tensor([s[:4] for _ in objects for s in scen], device=dev, dtype=torch.float)
        dist_g, dir_g, dyaw_g, yaw0 = S[:, 0], torch.deg2rad(S[:, 1]), torch.deg2rad(S[:, 2]), torch.deg2rad(S[:, 3])
        fields = base.sim.expanded_fields & VIEWER_MODEL_FIELDS
        hmj = base.sim.mj_model

        def term(name: str) -> torch.Tensor:
            c = end_cfgs[name]
            return c.func(base, **(c.params or {})).bool()

        def tilt_deg() -> torch.Tensor:
            return torch.rad2deg(torch.acos((-robot.data.projected_gravity_b[:, 2]).clamp(-1, 1)))

        def obs_now() -> TensorDict:
            # compute every group afresh (compute() without update_history returns its cache)
            om = base.observation_manager
            return TensorDict({k: om.compute_group(k) for k in om.active_terms}, batch_size=[n])

        for size_set in sizes:
            # -- object sizes: identical for every condition of this size set ----------------
            gen = torch.Generator(device="cpu").manual_seed(a.seed * 100003 + int(mass * 10) + 7919 * SIZE_SETS.index(size_set))
            factors = {}
            for k in range(len(SHAPES2)):
                if size_set == "in":
                    f = FACTOR_RANGE[0] + (FACTOR_RANGE[1] - FACTOR_RANGE[0]) * torch.rand(n, 3, generator=gen)
                else:
                    big = torch.rand(n, 1, generator=gen) < 0.5
                    u = torch.rand(n, 3, generator=gen)
                    f = torch.where(big, 1.25 + 0.15 * u, 0.60 + 0.15 * u)
                factors[k] = f
                m2.apply_geometry(base, ids, k, f.to(dev))
            mean_f = torch.stack([factors[int(k)][j].mean() for j, k in enumerate(obj_idx.tolist())]).tolist()

            for cond in conds:
                set_condition(g, cond)
                g.profile_roll = max(1, len(scen))  # roll by one object block: always a different object
                # -- same start every time: reset with the same seed, then lay out the scenario --
                torch.manual_seed(a.seed + 1)
                env.reset()
                q_adr = robot.indexing.free_joint_q_adr
                qpos = robot.data.data.qpos
                root = qpos[:, q_adr[0:3]]
                ryaw = yaw_of(qpos[:, q_adr[3:7]])
                reach = g.cfg.robot_reach + g.radius_env[ids, obj_idx] + 0.4
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
                obs = obs_now()

                film = (mass == video_mass) and (a.videos > 0 if cond == "normal"
                                                 else (a.ablation_videos > 0 and size_set == "in"))
                dt = base.step_dt
                rec = StateRecorder(base, dt) if film else None
                imgs: list[tuple[torch.Tensor, torch.Tensor]] = []  # what the policy sees, ~5 Hz

                def grab():
                    if variant == "ctrl":
                        return
                    imgs.append((m2._image(g, g.profile_top).to("cpu", torch.float16),
                                 m2._image(g, g.profile_front).to("cpu", torch.float16)))
                if rec is not None:
                    rec.add(0.0, d0, torch.rad2deg(e0.abs()), torch.zeros_like(d0), tilt_deg())
                    grab()

                steps = int(a.horizon / dt)
                pt, yt = a.pos_tol, math.radians(a.yaw_tol)
                nan = lambda: torch.full((n,), float("nan"), device=dev)  # noqa: E731
                done = torch.zeros(n, dtype=torch.bool, device=dev)
                fallen = torch.zeros(n, dtype=torch.bool, device=dev)
                how = ["horizon"] * n
                detail = [""] * n
                t_fall, t_reach, t_succ = nan(), nan(), nan()
                hold = torch.zeros(n, device=dev)
                last_d, last_e, min_d = d0.clone(), e0.abs().clone(), d0.clone()
                path = torch.zeros(n, device=dev)
                prev_xy = g.box_pos()[:, :2].clone()
                end_step = torch.full((n,), steps - 1, dtype=torch.long, device=dev)
                tail = int(2.0 / dt) if rec is not None else 0
                all_done_at, last_i = None, steps - 1
                probe_conds = [c for c in applicable if c != "normal"] if cond == "normal" else []
                with torch.no_grad():
                    for i in range(steps):
                        act = policy(obs)
                        if probe_conds and i % a.probe_every == 0 and bool((~done).any()):
                            live = ~done
                            act_mag.append(act[live].abs().cpu())
                            keep_top, keep_front = g.profile_top.clone(), g.profile_front.clone()
                            for pc in probe_conds:
                                set_condition(g, pc)
                                if pc == "heading_zero_map":
                                    g.refresh_profiles(ids)
                                alt = policy(obs_now())
                                sens[pc].append((alt - act)[live].abs().cpu())
                                g.profile_top.copy_(keep_top)
                                g.profile_front.copy_(keep_front)
                            set_condition(g, "normal")
                        obs, _, _, _ = env.step(act)
                        t = (i + 1) * dt
                        live = ~done
                        live_a = live & ~fallen
                        new_fall = pose_fallen(base, "robot", nom_h) & live_a
                        for j in new_fall.nonzero().flatten().tolist():
                            detail[j] = fall_reason(base, j, "robot", nom_h)
                            how[j] = "fell"
                        t_fall = torch.where(new_fall, torch.full_like(t_fall, t), t_fall)
                        fallen |= new_fall
                        tip, lost = term("box_tipped") & live_a, term("box_lost") & live_a
                        for j in (tip | lost).nonzero().flatten().tolist():
                            how[j] = "tipped" if bool(tip[j]) else "lost"
                        d, e = g.errors()
                        ea = e.abs()
                        xy = g.box_pos()[:, :2]
                        path += torch.where(live_a, torch.linalg.norm(xy - prev_xy, dim=-1), torch.zeros_like(path))
                        prev_xy = xy.clone()
                        last_d = torch.where(live_a, d, last_d)
                        last_e = torch.where(live_a, ea, last_e)
                        min_d = torch.where(live_a, torch.minimum(min_d, d), min_d)
                        ok = live_a & ~tip & ~lost
                        inside = ok & (d < pt) & (ea < yt)
                        t_reach = torch.where(inside & torch.isnan(t_reach), torch.full_like(t_reach, t), t_reach)
                        hold = torch.where(inside, hold + dt, torch.zeros_like(hold))
                        succ = (hold >= a.hold) & ok
                        t_succ = torch.where(succ, torch.full_like(t_succ, t), t_succ)
                        for j in succ.nonzero().flatten().tolist():
                            how[j] = "success"
                        ended = new_fall | tip | lost | succ
                        end_step = torch.where(ended & ~done, torch.full_like(end_step, i), end_step)
                        done |= ended
                        if rec is not None and (i + 1) % rec.stride == 0:
                            rec.add(t, d, torch.rad2deg(ea), hold, tilt_deg())
                            if variant == "b" and len(rec.t) % 5 == 1:
                                grab()
                        if all_done_at is None and bool(done.all()):
                            all_done_at = i
                        if all_done_at is not None and i >= all_done_at + tail:
                            last_i = i
                            break

                first = len(rows)
                for j in range(n):
                    o = objects[j // len(scen)]
                    dist, direc, dyaw, y0, rep = scen[j % len(scen)]
                    sym = SHAPES2[SHAPE_NAMES2.index(o)].symmetry
                    eff = abs(math.degrees(float(fold(torch.tensor(math.radians(dyaw)), torch.tensor(float(sym))))))
                    rnd = lambda x: "" if math.isnan(x) else round(x, 2)  # noqa: E731
                    seen = o in TRAIN_NAMES
                    rows.append({
                        "condition": cond, "size_set": size_set,
                        "group": ("seen" if seen else "unseen") + ("" if size_set == "in" else "_out_of_range"),
                        "object": o, "seen_shape": int(seen), "size_factor_mean": round(mean_f[j], 3),
                        "mass": mass, "distance": dist, "direction": direc, "yaw_change": dyaw,
                        "yaw_change_effective": round(eff, 1), "start_yaw": y0, "rep": rep,
                        "success": int(how[j] == "success"), "outcome": how[j],
                        "t_reach": rnd(float(t_reach[j])),
                        "t_success": rnd(float(t_succ[j])) if how[j] == "success" else "",
                        "final_pos_err": round(float(last_d[j]), 3),
                        "final_yaw_err": round(math.degrees(float(last_e[j])), 1),
                        "min_pos_err": round(float(min_d[j]), 3),
                        "path_ratio": round(float(path[j]) / max(float(d0[j]), 1e-3), 2),
                        "t_fall": rnd(float(t_fall[j])), "fall_detail": detail[j],
                        "video": "",
                        # fields the shared video maker reads
                        "outcome_ignoring_falls": how[j],  # Stage 2 eval ends the episode at a fall
                        "t_fall_train_rule": "", "train_rule_detail": "",
                    })
                if rec is not None:
                    quota = a.videos if cond == "normal" else a.ablation_videos
                    groups = defaultdict(list)
                    for j in range(n):
                        groups[(rows[first + j]["object"], rows[first + j]["outcome"])].append(j)
                    pick = []
                    for key in sorted(groups):
                        js = groups[key]
                        random.Random(f"{a.seed}-{mass}-{size_set}-{cond}-{key}").shuffle(js)
                        pick += js[:quota]
                    maker = VideoMaker(base, robot, g, q_adr, goal_xy, out / "videos" / cond / size_set,
                                       vw, vh, rec, SHAPES2, obj_idx)
                    maker.sync = lambda j: sync_model_fields(hmj, base.sim.model, fields, j)
                    if imgs:
                        maker.overlay = make_overlay(imgs, variant, vw, vh, cond)
                    tv = time.time()
                    for j in sorted(pick):
                        r = rows[first + j]
                        label = (f"[{variant} | {cond} | size {size_set} x{r['size_factor_mean']:.2f}]  {r['object']} "
                                 f"{mass:g} kg  goal {r['distance']:g} m at {r['direction']:g} deg, turn "
                                 f"{r['yaw_change']:g}, start yaw {r['start_yaw']:g}")
                        stem = (f"{r['object']}_{mass:g}kg_d{r['distance']:g}_dir{r['direction']:g}"
                                f"_turn{r['yaw_change']:g}_s{r['start_yaw']:g}_r{r['rep']}")
                        end = int(end_step[j]) + tail
                        rel = maker.make(j, label, stem, r, end)  # "videos/<outcome>/<file>"
                        r["video"] = f"videos/{cond}/{size_set}/" + rel[len("videos/"):]
                    maker.close()
                    print(f"  wrote {len(pick)} videos in {time.time() - tv:.0f} s", flush=True)
                mine = rows[first:]
                print(f"[{mass:g} kg | size {size_set} | {cond}] success {sum(r['success'] for r in mine)}/{n}"
                      f" (seen {sum(r['success'] for r in mine if r['seen_shape'])}/"
                      f"{sum(r['seen_shape'] for r in mine)}), falls {sum(r['outcome'] == 'fell' for r in mine)}"
                      f"  ({last_i + 1} steps, {time.time() - t0:.0f} s elapsed)", flush=True)
                del rec, imgs
        set_condition(g, "normal")
        env.close()
        del env, base, runner, policy

    sens_summary = {}
    if act_mag:
        mag = torch.cat(act_mag).mean(0)
        for c, v in sens.items():
            dv = torch.cat(v)
            sens_summary[c] = {"mean_abs_change": [round(float(x), 4) for x in dv.mean(0)],
                               "relative_to_mean_abs_action": round(float(dv.mean() / mag.mean().clamp(min=1e-6)), 3),
                               "share_of_samples_changed_gt_0.05": round(float((dv.max(-1).values > 0.05).float().mean()), 3)}
        sens_summary["_mean_abs_action"] = [round(float(x), 4) for x in mag]
    write_outputs(rows, out, a, variant, conds, sens_summary, HELDOUT_NAMES)
    return 0


def make_overlay(imgs, variant: str, w: int, h: int, cond: str):
    """Draws the profile images the policy sees (top, front) in the right panel's lower-left."""
    import numpy as np
    from PIL import Image, ImageDraw

    def colour(x: np.ndarray) -> np.ndarray:  # same scale as the check sheets: red inside, blue->yellow outside
        x = np.clip(x, -0.6, 2.0)
        r = np.where(x < 0, 220, np.clip(40 + 215 * x / 2.0, 0, 255))
        gch = np.where(x < 0, 30, np.clip(40 + 200 * x / 2.0, 0, 255))
        b = np.where(x < 0, 30, np.clip(200 - 200 * x / 2.0, 0, 255))
        return np.stack([r, gch, b], -1).astype(np.uint8)

    size = max(64, h // 3)

    def draw(j: int, f: int, im) -> None:
        k = 0 if variant != "b" else min(len(imgs) - 1, f // 5)
        top = imgs[k][0][j, 0].float().numpy()
        front = imgs[k][1][j, 0].float().numpy()
        ti = Image.fromarray(colour(top)).resize((size, size), Image.NEAREST)
        fi = Image.fromarray(colour(front)).resize((size, size // 2), Image.NEAREST)
        x0, y0 = w + 6, h - 40 - size - size // 2 - 18
        dr = ImageDraw.Draw(im, "RGBA")
        dr.rectangle([x0 - 4, y0 - 16, x0 + size + 4, y0 + size + size // 2 + 6], fill=(0, 0, 0, 170))
        what = "robot-frame map (10 Hz)" if variant == "b" else "top (object frame)"
        dr.text((x0, y0 - 14), f"policy sees: {what}" + ("" if cond == "normal" else f" [{cond}]"),
                fill=(255, 255, 255))
        im.paste(ti, (x0, y0))
        im.paste(fi, (x0, y0 + size + 4))
    return draw


def write_outputs(rows, out: Path, a, variant: str, conds, sens_summary: dict, heldout) -> None:
    with open(out / "episodes.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    def agg(sel):
        n = len(sel)
        if not n:
            return None
        succ = [r for r in sel if r["success"]]
        ts = sorted(float(r["t_success"]) for r in succ)
        return {"episodes": n, "success": round(len(succ) / n, 3),
                "t_success_median": ts[len(ts) // 2] if ts else None,
                "final_pos_err_mean": round(sum(r["final_pos_err"] for r in sel) / n, 3),
                "final_yaw_err_mean": round(sum(r["final_yaw_err"] for r in sel) / n, 1),
                "fell": round(sum(r["outcome"] == "fell" for r in sel) / n, 3),
                "tipped": round(sum(r["outcome"] == "tipped" for r in sel) / n, 3),
                "lost": round(sum(r["outcome"] == "lost" for r in sel) / n, 3)}

    def pivot(row_key):
        table = defaultdict(dict)
        for r in rows:
            table[row_key(r)].setdefault(r["condition"], []).append(r)
        return {k: {c: agg(v.get(c, [])) for c in conds} for k, v in sorted(table.items())}

    groups = pivot(lambda r: r["group"])
    objects = pivot(lambda r: f"{r['object']} / {r['size_set']}")
    arch = pivot(lambda r: f"{r['object']} start yaw {r['start_yaw']:g} / {r['size_set']}")
    arch = {k: v for k, v in arch.items() if k.startswith(("arch", "u_channel"))}
    by_mass = pivot(lambda r: f"{r['group']} / {r['mass']:g} kg")
    summary = {"config": vars(a), "variant": variant, "by_group": groups, "by_object": objects,
               "by_start_yaw_arch_u": arch, "by_group_mass": by_mass, "action_sensitivity": sens_summary,
               "overall_normal": agg([r for r in rows if r["condition"] == "normal"])}
    (out / "summary.json").write_text(json.dumps(summary, indent=2))

    def table(title, data, note=""):
        lines = [f"## {title}\n", note] if note else [f"## {title}\n"]
        lines.append("| | " + " | ".join(conds) + " |")
        lines.append("|---" * (len(conds) + 1) + "|")
        for k, v in data.items():
            cells = []
            for c in conds:
                s = v.get(c)
                if s is None:
                    cells.append("")
                elif c == "normal":
                    cells.append(f"{s['success']:.2f} (n={s['episodes']}, fell {s['fell']:.2f})")
                else:
                    base = v.get("normal")
                    delta = "" if base is None else f" ({s['success'] - base['success']:+.2f})"
                    cells.append(f"{s['success']:.2f}{delta}")
            lines.append(f"| {k} | " + " | ".join(cells) + " |")
        lines.append("")
        return lines

    lines = [f"# Stage 2{variant} evaluation: {a.checkpoint}",
             f"success = held within {a.pos_tol} m / {a.yaw_tol} deg for {a.hold} s inside {a.horizon} s; "
             f"ablation cells show success (change vs normal)\n",
             f"unseen shapes: {', '.join(heldout)} (asym = long box with split friction: same geometry as a seen "
             f"shape, different physics)\n"]
    lines += table("success by object group", groups)
    if sens_summary:
        lines.append("## action sensitivity (does the output change at all?)\n")
        lines.append("Same observation, one input ablated; |action change| per walker command (vx, vy, yaw rate), "
                     f"averaged over live envs every {a.probe_every} steps of the normal rollouts. "
                     f"Mean |action| = {sens_summary.get('_mean_abs_action')}.\n")
        lines.append("| ablation | mean abs change (vx, vy, wz) | relative to mean abs action | share of samples changed > 0.05 |")
        lines.append("|---|---|---|---|")
        for c, s in sens_summary.items():
            if c.startswith("_"):
                continue
            lines.append(f"| {c} | {s['mean_abs_change']} | {s['relative_to_mean_abs_action']} | "
                         f"{s['share_of_samples_changed_gt_0.05']} |")
        lines.append("")
    lines += table("success by object and size set", objects)
    lines += table("arch / u_channel by object start yaw", arch,
                   "(start yaw 0 = doorway facing the robot)\n")
    lines += table("by group and mass", by_mass)
    (out / "summary.md").write_text("\n".join(lines))
    print("\n".join(lines[: 6 + len(groups) + 3 + (len(sens_summary) + 5 if sens_summary else 0)]))
    print(f"\nwrote {out}/episodes.csv, summary.json, summary.md")

    vids = [r for r in rows if r["video"]]
    if vids:
        html = ["<html><head><meta charset='utf-8'><title>stage 2 eval videos</title><style>"
                "body{font-family:sans-serif;background:#111;color:#ddd;margin:16px}a{color:#8cf}"
                "video{width:100%;max-width:960px;margin:4px 0 18px}</style></head><body>"
                f"<h1>Stage 2{variant} eval videos</h1>"]
        for c in conds:
            sel = sorted((r for r in vids if r["condition"] == c),
                         key=lambda r: (r["size_set"], r["seen_shape"] == 0, r["object"], r["outcome"]))
            if not sel:
                continue
            html.append(f"<h2>{c}</h2>")
            for r in sel:
                html.append(f"<div>{r['size_set']} | {r['object']} | {r['outcome']} {r['fall_detail']} | "
                            f"start yaw {r['start_yaw']:g}, goal {r['distance']:g} m at {r['direction']:g} deg</div>")
                html.append(f"<video controls preload='none' src='../{r['video']}'></video>")
        html.append("</body></html>")
        (out / "videos").mkdir(exist_ok=True)
        (out / "videos" / "index.html").write_text("\n".join(html))


if __name__ == "__main__":
    raise SystemExit(main())
