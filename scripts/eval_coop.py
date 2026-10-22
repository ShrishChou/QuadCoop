"""Evaluate two-robot pushing: one robot alone vs. both single-robot policies side by side
vs. the trained IPPO / MAPPO policies, on the same grid of tasks and object masses.

Conditions (--conditions, any subset, in this order):

    anymal    ANYmal alone (its Stage 1b/1c policy); Spot parked 25 m away, standing
    spot      Spot alone
    pair      both single-robot policies at once, no coordination training
              (= the run's model_0.pt: the warm start, before any update)
    trained   the run's checkpoint (--checkpoint, default: its newest model_N.pt)

Every condition runs every object x mass x scenario from exactly the same start:
object at the centre, goal --distances away, both robots behind the object
(--arrangements: "behind" = within +-30 deg of straight behind, "spread" = +-75 deg),
goal heading change --yaw-changes, deterministic actions. Success = held inside
--pos-tol / --yaw-tol for --hold s. A robot falling (quadcoop/falls.py), the object
tipping over or getting lost ends the episode.

Per episode (episodes.csv): success, t_success, final position / heading error,
outcome (success | horizon | anymal_fell | spot_fell | tipped | lost), each robot's
mean effort (joint power / weight), how much of the time the robots touched each
other. summary.md / summary.json: by condition x object x mass; vs_mass.png: success
vs mass per condition. M50 (mass at which success crosses 50%) per condition/object.

    MUJOCO_GL=egl python scripts/eval_coop.py --run mappo_seed0
    python scripts/eval_coop.py --run ippo_seed1 --conditions pair,trained --masses 40,80 --videos 2
"""

from __future__ import annotations

import argparse
import csv
import itertools
import json
import math
import os
import sys
import time
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
os.environ.setdefault("QUADCOOP_SHAPES", "v2")

import torch  # noqa: E402

CONDITIONS = ("anymal", "spot", "pair", "trained")
ARRANGE = {"behind": 30.0, "spread": 75.0}


def floats(s: str) -> list[float]:
    return [float(x) for x in s.split(",") if x.strip()]


def newest_model(d: Path) -> Path | None:
    cks = sorted(d.glob("model_*.pt"), key=lambda p: int(p.stem.split("_")[1]))
    return cks[-1] if cks else None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", default=None, help="run name under logs/marl (e.g. mappo_seed0)")
    ap.add_argument("--checkpoint", default=None, help="coop model_N.pt (default: newest in the run)")
    ap.add_argument("--conditions", default="anymal,spot,pair,trained")
    ap.add_argument("--objects", default="cube,long,beam,arch,dumbbell,t_shape,l_shape,asym,sphere,cylinder")
    ap.add_argument("--masses", default="20,40,60,80,100,120")
    ap.add_argument("--distances", default="2,4")
    ap.add_argument("--arrangements", default="behind,spread")
    ap.add_argument("--yaw-changes", default="0,90")
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--horizon", type=float, default=45.0)
    ap.add_argument("--pos-tol", type=float, default=0.10)
    ap.add_argument("--yaw-tol", type=float, default=6.0)
    ap.add_argument("--hold", type=float, default=1.0)
    ap.add_argument("--obs-level", type=int, default=4, help="level the policy is told (hold-progress input)")
    ap.add_argument("--singles", default=None,
                    help="anymal_ckpt,spot_ckpt single-robot policies for anymal/spot/pair if the run has no "
                         "model_0.pt (default: newest pushhard2_*, else pushhard_*)")
    ap.add_argument("--walker-anymal", default=None)
    ap.add_argument("--walker-spot", default=None)
    ap.add_argument("--videos", type=int, default=0, help="MP4s per condition x object x mass x outcome")
    ap.add_argument("--out", default=None)
    ap.add_argument("--device", default=None)
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    device = a.device or ("cuda:0" if torch.cuda.is_available() else "cpu")

    sys.path.insert(0, str(ROOT))
    from train_coop import newest_run_ckpt

    logs = ROOT / "logs"
    for agent, robot in (("anymal", "anymal_c"), ("spot", "spot")):
        w = getattr(a, f"walker_{agent}") or newest_run_ckpt(logs / "rsl_rl" / f"walker_{robot}")
        os.environ[f"QUADCOOP_WALKER_CKPT_{robot.upper()}"] = str(w)
    conds = [c.strip() for c in a.conditions.split(",") if c.strip()]
    for c in conds:
        assert c in CONDITIONS, f"unknown condition {c}"
    run_dir = logs / "marl" / a.run if a.run else None
    ckpt = Path(a.checkpoint) if a.checkpoint else (newest_model(run_dir) if run_dir else None)
    if "trained" in conds and ckpt is None:
        raise SystemExit("condition 'trained' needs --run or --checkpoint")
    base_ckpt = (run_dir / "model_0.pt") if run_dir and (run_dir / "model_0.pt").exists() else None
    if a.singles:
        sa, ss = a.singles.split(",")
        singles = {"anymal": sa, "spot": ss}
    else:
        singles = {}
        for agent, robot in (("anymal", "anymal_c"), ("spot", "spot")):
            singles[agent] = str(newest_run_ckpt(logs / "rsl_rl" / f"pushhard2_{robot}")
                                 or newest_run_ckpt(logs / "rsl_rl" / f"pushhard_{robot}"))
    out = Path(a.out) if a.out else (ckpt.parent / f"eval_{ckpt.stem}" if ckpt else logs / "marl" / "eval_baselines")
    out.mkdir(parents=True, exist_ok=True)
    print(f"trained: {ckpt}\nbaseline policies: {base_ckpt or singles}\n"
          f"walkers: {os.environ['QUADCOOP_WALKER_CKPT_ANYMAL_C']}, {os.environ['QUADCOOP_WALKER_CKPT_SPOT']}\n"
          f"shapes: {os.environ['QUADCOOP_SHAPES']}  out: {out}", flush=True)

    import quadcoop  # noqa: F401
    from mjlab.envs import ManagerBasedRlEnv
    from tensordict import TensorDict

    from quadcoop.coop.env_cfg import make_coop_env_cfg
    from quadcoop.coop.marl import CoopPolicy
    from quadcoop.coop.mdp import AGENTS, agent_effort
    from quadcoop.stage1.mdp import wrap
    from quadcoop.stage1b.mdp import fold
    from quadcoop.stage1b.shapes import NOMINAL_MASS, OBJ_NAMES, SHAPE_NAMES, SHAPES

    objects = [o.strip() for o in a.objects.split(",") if o.strip()]
    for o in objects:
        assert o in SHAPE_NAMES, f"unknown object {o}"
    scen = list(itertools.product(floats(a.distances), [s.strip() for s in a.arrangements.split(",")],
                                  floats(a.yaw_changes), range(a.reps)))
    rows: list[dict] = []
    t0 = time.time()

    for cond in conds:
        for mass in floats(a.masses):
            torch.manual_seed(a.seed)
            cfg = make_coop_env_cfg(play=True)
            n = len(objects) * len(scen)
            cfg.scene.num_envs = n
            cfg.seed = a.seed
            cfg.episode_length_s = a.horizon + 10.0
            alpha = 0.5 * math.log(mass / NOMINAL_MASS)
            for name in OBJ_NAMES:
                cfg.events[f"{name}_mass"].params["alpha_range"] = (alpha, alpha)
                cfg.events[f"{name}_mass"].params["distribution"] = "uniform"
            ends = {k: cfg.terminations.pop(k) for k in list(cfg.terminations) if k != "time_out"}
            base = ManagerBasedRlEnv(cfg=cfg, device=device)
            g = base.command_manager.get_term("goal")
            dev = base.device
            obj_idx = torch.tensor([SHAPE_NAMES.index(o) for o in objects for _ in scen], device=dev)
            dist_g = torch.tensor([s[0] for _ in objects for s in scen], device=dev)
            spread = torch.tensor([ARRANGE[s[1]] for _ in objects for s in scen], device=dev)
            dyaw = torch.deg2rad(torch.tensor([s[2] for _ in objects for s in scen], device=dev))
            # spread the two robots symmetrically about "behind" (-x), +-spread
            solo = cond in ("anymal", "spot")

            def scenario(env_ids, _n=n):
                m = len(env_ids)
                origin = base.scene.env_origins[env_ids][:, :2]
                z = torch.zeros(m, device=dev)
                sym = g.sym[obj_idx[env_ids]]
                eff = torch.where(sym > 0, fold(dyaw[env_ids], sym), z)
                b0 = math.pi + torch.deg2rad(spread[env_ids])
                b1 = math.pi - torch.deg2rad(spread[env_ids])
                sc = {"shape": obj_idx[env_ids], "obj_xy": origin, "obj_heading": z, "goal_yaw": wrap(eff),
                      "goal_xy": origin + torch.stack([dist_g[env_ids], z], -1),
                      "bearings": [b0, b1], "gaps": [torch.full((m,), 0.5, device=dev)] * 2}
                if solo:  # the active robot straight behind; the other parked far away
                    k_on = AGENTS.index(cond)
                    sc["bearings"][k_on] = torch.full((m,), math.pi, device=dev)
                    sc["bearings"][1 - k_on] = torch.full((m,), math.pi / 2, device=dev)
                    gaps = [torch.full((m,), 0.5, device=dev), torch.full((m,), 0.5, device=dev)]
                    gaps[1 - k_on] = torch.full((m,), 25.0, device=dev)
                    sc["gaps"] = gaps
                return sc

            g.cfg.only = None
            g.cfg.replay_frac = 0.0
            g.level = a.obs_level
            g.scenario = scenario
            obs_dict, _ = base.reset()
            assert bool((g.shape == obj_idx).all()), "scenario object mismatch"
            g.env_level[:] = a.obs_level

            def td(o):
                return TensorDict({k: v for k, v in o.items() if not k.startswith("walker_")}, batch_size=[n])

            obs = td(obs_dict)
            if cond == "trained":
                pol = CoopPolicy(obs, device, checkpoint=str(ckpt))
            elif base_ckpt is not None:
                pol = CoopPolicy(obs, device, checkpoint=str(base_ckpt))
            else:
                pol = CoopPolicy(obs, device, singles=singles)
            neutral = []
            for ag in AGENTS:
                t_ = base.action_manager.get_term(f"walker_{ag}")
                neutral.append(-1.0 + 2.0 * (0.0 - t_._lo) / (t_._hi - t_._lo))  # action giving 0 velocity
            neutral = torch.cat(neutral).to(dev)

            d0, e0 = g.errors()
            dt = base.step_dt
            steps = int(a.horizon / dt)
            done = torch.zeros(n, dtype=torch.bool, device=dev)
            how = ["horizon"] * n
            t_succ = torch.full((n,), float("nan"), device=dev)
            hold = torch.zeros(n, device=dev)
            last_d, last_e = d0.clone(), e0.abs().clone()
            min_d = d0.clone()
            eff_sum = torch.zeros(n, 2, device=dev)
            touch_sum = torch.zeros(n, device=dev)
            n_live = torch.zeros(n, device=dev)
            rec = [] if a.videos > 0 else None
            if rec is not None:
                rec.append((0.0, base.sim.data.qpos.detach().cpu().clone(), d0.cpu(), torch.rad2deg(e0.abs()).cpu()))
            pt, yt = a.pos_tol, math.radians(a.yaw_tol)
            with torch.no_grad():
                for i in range(steps):
                    act = pol(obs)
                    if solo:
                        k_off = 1 - AGENTS.index(cond)
                        act[:, 3 * k_off:3 * k_off + 3] = neutral[3 * k_off:3 * k_off + 3]
                    o, *_ = base.step(act)
                    obs = td(o)
                    t = (i + 1) * dt
                    live = ~done
                    d, e = g.errors()
                    ea = e.abs()
                    for name, c in ends.items():
                        if solo and name == f"{AGENTS[1 - AGENTS.index(cond)]}_fell":
                            continue
                        hit = c.func(base, **(c.params or {})).bool() & live & ~done
                        for j in hit.nonzero().flatten().tolist():
                            how[j] = name.replace("box_", "")
                        done |= hit
                    live = live & ~done
                    last_d = torch.where(live, d, last_d)
                    last_e = torch.where(live, ea, last_e)
                    min_d = torch.where(live, torch.minimum(min_d, d), min_d)
                    eff_sum += agent_effort(base) * live.unsqueeze(-1)
                    touch_sum += base.scene["robots_touch"].data.found.view(n, -1).any(-1).float() * live
                    n_live += live.float()
                    inside = live & (d < pt) & (ea < yt)
                    hold = torch.where(inside, hold + dt, torch.zeros_like(hold))
                    new = (hold >= a.hold) & live
                    t_succ = torch.where(new, torch.full_like(t_succ, t), t_succ)
                    for j in new.nonzero().flatten().tolist():
                        how[j] = "success"
                    done |= new
                    if rec is not None and (i + 1) % 2 == 0:
                        rec.append((t, base.sim.data.qpos.detach().cpu().clone(), d.cpu(), torch.rad2deg(ea).cpu()))
                    if bool(done.all()):
                        break

            first = len(rows)
            for j in range(n):
                o = objects[j // len(scen)]
                dist, arr, dy, rep = scen[j % len(scen)]
                sym = SHAPES[SHAPE_NAMES.index(o)].symmetry
                ts = float(t_succ[j])
                nl = max(float(n_live[j]), 1.0)
                rows.append({
                    "condition": cond, "object": o, "mass": mass, "distance": dist, "arrangement": arr,
                    "yaw_change": dy, "yaw_change_effective": round(abs(math.degrees(float(
                        fold(torch.tensor(math.radians(dy)), torch.tensor(float(sym)))))) if sym else 0.0, 1),
                    "rep": rep, "success": int(how[j] == "success"), "outcome": how[j],
                    "t_success": "" if math.isnan(ts) else round(ts, 2),
                    "final_pos_err": round(float(last_d[j]), 3),
                    "final_yaw_err": round(math.degrees(float(last_e[j])), 1),
                    "min_pos_err": round(float(min_d[j]), 3),
                    "effort_anymal": round(float(eff_sum[j, 0]) / nl, 3),
                    "effort_spot": round(float(eff_sum[j, 1]) / nl, 3),
                    "robots_touch_frac": round(float(touch_sum[j]) / nl, 3),
                    "video": "",
                })
            if rec is not None:
                write_videos(rec, rows[first:], base, g, a.videos, out / "videos", dt * 2, objects, scen, cond, mass)
            mine = rows[first:]
            print(f"[{cond} {mass:g} kg] {n} episodes, {sum(r['success'] for r in mine)} successes "
                  f"({time.time() - t0:.0f} s elapsed)", flush=True)
            base.close()
            del base, pol

    write_outputs(rows, out, a)
    return 0


# -------------------------------------------------------------------------------------
def write_videos(rec, rows, base, g, k_per, folder: Path, frame_dt, objects, scen, cond, mass) -> None:
    """Overview videos (camera follows object, goal and both robots) for up to k_per
    episodes per object and outcome."""
    import random

    import imageio_ffmpeg
    import mujoco
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont

    m = base.sim.mj_model
    w, h = 640, 480
    m.vis.global_.offwidth = max(int(m.vis.global_.offwidth), w)
    m.vis.global_.offheight = max(int(m.vis.global_.offheight), h)
    m.stat.extent = 12.0
    d = mujoco.MjData(m)
    r = mujoco.Renderer(m, height=h, width=w)
    cam = mujoco.MjvCamera()
    cam.type = mujoco.mjtCamera.mjCAMERA_FREE
    try:
        font = ImageFont.load_default(size=14)
    except TypeError:
        font = ImageFont.load_default()
    mpos = base.sim.data.mocap_pos.cpu().numpy()
    mquat = base.sim.data.mocap_quat.cpu().numpy()
    rq = {a: base.scene[a].indexing.free_joint_q_adr[0:2].tolist() for a in ("anymal", "spot")}
    oq = [o.indexing.free_joint_q_adr[0:2].tolist() for o in g.objs]
    goal = g.goal_xy.cpu().numpy()
    shape = g.shape.cpu().tolist()
    groups = defaultdict(list)
    for j, row in enumerate(rows):
        groups[(row["object"], row["outcome"])].append(j)
    pick = []
    for key in sorted(groups):
        js = groups[key]
        random.Random(f"{cond}-{mass}-{key}").shuffle(js)
        pick += js[:k_per]
    for j in sorted(pick):
        row = rows[j]
        sub = folder / cond / row["outcome"]
        sub.mkdir(parents=True, exist_ok=True)
        fn = sub / (f"{row['object']}_{mass:g}kg_d{row['distance']:g}_{row['arrangement']}"
                    f"_turn{row['yaw_change']:g}_r{row['rep']}.mp4")
        wr = imageio_ffmpeg.write_frames(str(fn), (w, h), fps=1.0 / frame_dt, quality=6, macro_block_size=8,
                                         ffmpeg_log_level="error")
        wr.send(None)
        end_t = float(row["t_success"]) + 2.0 if row["t_success"] != "" else 1e9
        look = None
        for t, q, dd, ee in rec:
            if t > end_t:
                break
            qq = q[j].numpy().astype(np.float64)
            d.qpos[:] = qq
            d.mocap_pos[:] = mpos[j]
            d.mocap_quat[:] = mquat[j]
            mujoco.mj_forward(m, d)
            pts = np.array([[qq[rq["anymal"][0]], qq[rq["anymal"][1]]], [qq[rq["spot"][0]], qq[rq["spot"][1]]],
                            [qq[oq[shape[j]][0]], qq[oq[shape[j]][1]]], goal[j]])
            if row["condition"] in ("anymal", "spot"):  # ignore the parked robot
                pts = np.delete(pts, 1 if row["condition"] == "anymal" else 0, axis=0)
            c = pts.mean(0)
            spread = max(np.linalg.norm(p1 - p2) for p1 in pts for p2 in pts)
            want = (c, max(4.0, min(14.0, 1.1 * spread + 3.0)))
            look = want if look is None else (0.92 * look[0] + 0.08 * want[0], 0.96 * look[1] + 0.04 * want[1])
            cam.lookat[:] = [look[0][0], look[0][1], 0.3]
            cam.distance, cam.azimuth, cam.elevation = look[1], 90.0, -40.0
            r.update_scene(d, camera=cam)
            im = Image.fromarray(r.render())
            dr = ImageDraw.Draw(im, "RGBA")
            dr.rectangle([0, 0, w, 44], fill=(0, 0, 0, 160))
            dr.text((6, 3), f"{cond}: {row['object']} {mass:g} kg, goal {row['distance']:g} m, "
                            f"{row['arrangement']}, turn {row['yaw_change']:g} deg", font=font, fill=(255, 255, 255))
            dr.text((6, 23), f"t {t:5.1f} s   pos err {float(dd[j]):5.2f} m   yaw err {float(ee[j]):5.1f} deg   "
                             f"-> {row['outcome']}", font=font, fill=(220, 220, 220))
            wr.send(im.tobytes())
        wr.close()
        row["video"] = str(fn.relative_to(folder.parent))
    r.close()


def write_outputs(rows: list[dict], out: Path, a) -> None:
    with open(out / "episodes.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    def agg(sel):
        n = len(sel)
        succ = [r for r in sel if r["success"]]
        ts = sorted(float(r["t_success"]) for r in succ)
        return {
            "episodes": n,
            "success": round(len(succ) / n, 3),
            "t_success_median": ts[len(ts) // 2] if ts else None,
            "final_pos_err_mean": round(sum(r["final_pos_err"] for r in sel) / n, 3),
            "final_yaw_err_mean": round(sum(r["final_yaw_err"] for r in sel) / n, 1),
            "anymal_fell": round(sum(r["outcome"] == "anymal_fell" for r in sel) / n, 3),
            "spot_fell": round(sum(r["outcome"] == "spot_fell" for r in sel) / n, 3),
            "tipped": round(sum(r["outcome"] == "tipped" for r in sel) / n, 3),
            "lost": round(sum(r["outcome"] == "lost" for r in sel) / n, 3),
            "effort_anymal": round(sum(r["effort_anymal"] for r in sel) / n, 3),
            "effort_spot": round(sum(r["effort_spot"] for r in sel) / n, 3),
            "robots_touch_frac": round(sum(r["robots_touch_frac"] for r in sel) / n, 3),
        }

    def by(*keys):
        groups = defaultdict(list)
        for r in rows:
            groups[tuple(r[k] for k in keys)].append(r)
        return {" / ".join(str(x) for x in k): agg(v) for k, v in sorted(groups.items())}

    som = by("condition", "object", "mass")
    sm = by("condition", "mass")

    def m50(cond, obj=None):
        """Mass at which success first drops below 50% (linear interpolation), None if never."""
        masses = sorted({r["mass"] for r in rows})
        s = [(sm if obj is None else som)[f"{cond} / {m}" if obj is None else f"{cond} / {obj} / {m}"]["success"]
             for m in masses]
        if s[0] < 0.5:
            return f"<{masses[0]:g}"
        for (m0, s0), (m1, s1) in zip(zip(masses, s), zip(masses[1:], s[1:])):
            if s1 < 0.5 <= s0:
                return round(m0 + (s0 - 0.5) / max(s0 - s1, 1e-6) * (m1 - m0), 1)
        return f">{masses[-1]:g}"

    conds = [c for c in CONDITIONS if any(r["condition"] == c for r in rows)]
    objs = sorted({r["object"] for r in rows})
    summary = {
        "config": vars(a),
        "by_condition": by("condition"),
        "by_condition_mass": sm,
        "by_condition_object": by("condition", "object"),
        "by_condition_object_mass": som,
        "by_condition_arrangement": by("condition", "arrangement"),
        "m50": {c: {"all": m50(c), **{o: m50(c, o) for o in objs}} for c in conds},
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2, default=str))
    cols = ["episodes", "success", "t_success_median", "final_pos_err_mean", "final_yaw_err_mean",
            "anymal_fell", "spot_fell", "tipped", "lost", "effort_anymal", "effort_spot", "robots_touch_frac"]
    lines = [f"# Two-robot evaluation", f"tolerance {a.pos_tol} m / {a.yaw_tol} deg, hold {a.hold} s, "
             f"horizon {a.horizon} s\n", "## M50: mass (kg) where success falls below 50%\n",
             "| condition | all | " + " | ".join(objs) + " |", "|---" * (len(objs) + 2) + "|"]
    for c in conds:
        lines.append(f"| {c} | {summary['m50'][c]['all']} | " + " | ".join(str(summary['m50'][c][o]) for o in objs) + " |")
    lines.append("")
    for title in ("by_condition", "by_condition_mass", "by_condition_arrangement", "by_condition_object",
                  "by_condition_object_mass"):
        lines += [f"## {title}\n", "| group | " + " | ".join(cols) + " |", "|---" * (len(cols) + 1) + "|"]
        for k, v in summary[title].items():
            lines.append(f"| {k} | " + " | ".join("" if v[c] is None else str(v[c]) for c in cols) + " |")
        lines.append("")
    (out / "summary.md").write_text("\n".join(lines))
    print("\n".join(lines[:4 + len(conds) + 1]))
    print("\n".join(l for l in lines if l.startswith("| ") and " / " in l and l.count(" / ") == 1
                    and any(l.startswith(f"| {c} / ") for c in conds))[:4000])
    print(f"\nwrote {out}/episodes.csv, summary.json, summary.md")
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:  # noqa: BLE001
        return
    masses = sorted({r["mass"] for r in rows})
    fig, axes = plt.subplots(1, 2, figsize=(13, 4.5))
    for c in conds:
        axes[0].plot(masses, [sm[f"{c} / {m}"]["success"] for m in masses], marker="o", label=c)
        axes[1].plot(masses, [sm[f"{c} / {m}"]["final_pos_err_mean"] for m in masses], marker="o", label=c)
    for ax, t_, yl in zip(axes, ("success rate (all objects)", "final position error"), ("fraction", "m"),
                          strict=True):
        ax.set_title(t_)
        ax.set_xlabel("object mass (kg)")
        ax.set_ylabel(yl)
        ax.grid(alpha=0.3)
        ax.legend()
    fig.tight_layout()
    fig.savefig(out / "vs_mass.png", dpi=130)
    print(f"wrote {out}/vs_mass.png")


if __name__ == "__main__":
    raise SystemExit(main())
