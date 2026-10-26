"""Scripted push test: is the two-robot task physically solvable with plain, unlearned pushing?

    python scripts/push_test.py                                   # all objects, 40/60/80/90 kg
    python scripts/push_test.py --objects beam,arch,dumbbell --masses 60,90 --horizon 20

No policy is involved. Every robot runs its frozen walker (evals/models.yaml) under a scripted
command: walk straight ahead (world +x) at --speed, hold heading 0, and keep a fixed lateral slot
relative to the object's centre. The object starts at the origin with heading 0; every Stage 2
shape has its long side along its local y, so the push is broadside, the case where two
contact points matter:

    pair     ANYmal and Spot side by side, each behind its own contact surface: one per arch
             pillar, one per dumbbell end, one per half of the beam, and so on (SLOTS below)
    anymal   ANYmal alone, centred (Spot parked 40 m away); on the arch, behind one pillar (its
             cross-beam is above body height, so there is nothing to push in the middle)
    spot     Spot alone, the same

Each robot starts with its front --gap m behind the object's back face at its slot. Measured over
--horizon s: how far the object moves forward (up to the first fall of a pushing robot), its
average and final speed, how much it turns and drifts sideways, which robot fell, whether it
tipped, and the share of time each robot's front is on the object. The cube, sphere and plus are
in as compact references; they have no room for two side by side.

For scale: training episodes put the goal 3-6 m away with up to 80 s, so the pushing part has to
average roughly 0.1 m/s once approach and turning are counted.

Output: logs/evals/<name>/ (episodes.csv, summary.md/json, videos/: the pair at --video-masses,
one per object); stats copied to evals/<name>/ for the repo.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import shutil
import sys
import time
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT))

# lateral slot (m, object frame y) of each robot in the pair: ANYmal at +y, Spot at -y
SLOTS = {
    "cube": 0.32, "long": 0.35, "sphere": 0.33, "cylinder": 0.40, "arch": 0.90, "dumbbell": 0.90,
    "t_shape": 0.45, "beam": 0.70, "l_shape": 0.40, "asym": 0.35, "u_channel": 0.50, "plus": 0.35,
}
# a robot alone pushes the centre, except where nothing is at body height there (the arch: its
# cross-beam is above the robots), where it pushes one pillar
SOLO_SLOT = {"arch": 0.90}
COMPACT = ("cube", "sphere", "plus")  # no room for two robots side by side
CONFIGS = ("pair", "anymal", "spot")
VX_RANGE, VY_RANGE, WZ_RANGE = (-0.6, 0.8), (-0.5, 0.5), (-0.7, 0.7)  # walker command ranges (stage1)


def to_action(v, lo_hi):
    lo, hi = lo_hi
    return 2.0 * (v - lo) / (hi - lo) - 1.0


def back_face_x(parts, kinds, rest_h: float, y: float, half_width: float = 0.25,
                band: tuple[float, float] = (0.12, 0.70)) -> float:
    """x of the object's back face (object frame) seen by a robot centred at lateral y: the parts
    overlapping the robot's front within the body-height band (not an arch's floor plates, which
    the feet step over, nor its cross-beam, which the robot walks under)."""
    best = None
    for p, k in zip(parts.tolist(), kinds.tolist(), strict=True):
        if k < 0:
            continue
        cx, cy, cz, hx, hy, hz = p
        if rest_h + cz + hz < band[0] or rest_h + cz - hz > band[1] or abs(cy - y) > hy + half_width:
            continue
        best = cx - hx if best is None else min(best, cx - hx)
    if best is None:  # nothing in front at this y: the overall back of the footprint
        best = min(p[0] - p[3] for p, k in zip(parts.tolist(), kinds.tolist(), strict=True) if k >= 0)
    return best


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", default="push-test", help="output id: logs/evals/<name>, evals/<name>")
    ap.add_argument("--objects", default="all")
    ap.add_argument("--masses", default="40,60,80,90")
    ap.add_argument("--configs", default=",".join(CONFIGS))
    ap.add_argument("--reps", type=int, default=2, help="placements per case (object friction is randomized)")
    ap.add_argument("--horizon", type=float, default=20.0)
    ap.add_argument("--speed", type=float, default=0.8, help="commanded forward speed, m/s (0.8 = the most the "
                                                            "pushing policies can command)")
    ap.add_argument("--gap", type=float, default=0.25, help="start: robot front to object, m")
    ap.add_argument("--videos", type=int, default=1)
    ap.add_argument("--video-masses", default="60,90")
    ap.add_argument("--video-size", default="640x480")
    ap.add_argument("--device", default=None)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--verbose", type=int, default=0, help="print the first N envs' state every 0.5 s")
    a = ap.parse_args()

    from train_coop2 import resolve_models, set_env

    set_env(resolve_models("b"))
    import numpy as np
    import torch

    import quadcoop  # noqa: F401
    from mjlab.envs import ManagerBasedRlEnv
    from mjlab.utils.lab_api.math import quat_from_euler_xyz

    from quadcoop import falls
    from quadcoop.coop2.env_cfg import SPECS, make_coop2_env_cfg
    from quadcoop.coop2.mdp import AGENTS
    from quadcoop.coop2.video import Camera, render_episode
    from quadcoop.stage1.mdp import wrap, yaw_of
    from quadcoop.stage1b import mdp as hb
    from quadcoop.stage1b.shapes import NOMINAL_MASS
    from quadcoop.stage2 import mdp as m2
    from quadcoop.stage2.shapes import OBJ_NAMES2, SHAPE_NAMES2, SHAPES2, kinds_tensor, nominal_parts

    device = a.device or ("cuda:0" if torch.cuda.is_available() else "cpu")
    objects = list(SHAPE_NAMES2) if a.objects == "all" else [o.strip() for o in a.objects.split(",")]
    masses = [float(x) for x in a.masses.split(",")]
    configs = [c.strip() for c in a.configs.split(",")]
    video_masses = [float(x) for x in a.video_masses.split(",") if x.strip()]
    vw, vh = (int(x) for x in a.video_size.lower().split("x"))
    out = ROOT / "logs" / "evals" / a.name
    stats_dir = ROOT / "evals" / a.name
    out.mkdir(parents=True, exist_ok=True)
    cases = [(o, c, r) for o in objects for c in configs for r in range(a.reps)]
    n = len(cases)
    nom, nom_rest = nominal_parts("cpu")
    kinds = kinds_tensor("cpu")
    print(f"scripted push: {len(objects)} objects x {configs} x {a.reps} reps = {n} envs per mass; masses {masses}; "
          f"{a.speed} m/s for {a.horizon:g} s", flush=True)

    # per case: each robot's slot y and start x (object frame = world frame here, object at the origin)
    slot = {ag: [] for ag in AGENTS}
    start_x = {ag: [] for ag in AGENTS}
    park = {ag: [] for ag in AGENTS}
    for o, c, _ in cases:
        k = SHAPE_NAMES2.index(o)
        for sgn, ag in zip((1.0, -1.0), AGENTS, strict=True):
            y = sgn * SLOTS[o] if c == "pair" else SOLO_SLOT.get(o, 0.0)
            slot[ag].append(y)
            bx = back_face_x(nom[k], kinds[k], float(nom_rest[k]), y)
            start_x[ag].append(bx - SPECS[ag].half_length - a.gap)
            park[ag].append(not (c == "pair" or c == ag))
    rows: list[dict] = []
    t_start = time.time()

    for mass in masses:
        cfg = make_coop2_env_cfg("b", play=True)
        cfg.scene.num_envs = n
        cfg.episode_length_s = 1e5
        cfg.terminations = {}
        alpha = 0.5 * math.log(mass / NOMINAL_MASS)
        for name in OBJ_NAMES2:
            cfg.events[f"{name}_mass"].params["alpha_range"] = (alpha, alpha)
        torch.manual_seed(a.seed)
        base = ManagerBasedRlEnv(cfg=cfg, device=device)
        g = base.command_manager.get_term("goal")
        dev = base.device
        ids = torch.arange(n, device=dev)
        for k in range(len(SHAPES2)):  # nominal sizes
            m2.apply_geometry(base, ids, k, torch.ones(n, 3, device=dev))
        z = torch.zeros(n, device=dev)
        shape = torch.tensor([SHAPE_NAMES2.index(o) for o, _, _ in cases], device=dev)
        pk = {ag: torch.tensor(park[ag], dtype=torch.bool, device=dev) for ag in AGENTS}
        sc = {"shape": shape, "obj_xy_rel": torch.zeros(n, 2, device=dev), "obj_heading": z.clone(),
              "goal_xy_rel": torch.tensor([[3.0, 0.0]], device=dev).repeat(n, 1), "goal_yaw": z.clone(),
              "bearings": [torch.full((n,), math.pi, device=dev) for _ in AGENTS],
              "gaps": [torch.full((n,), 0.5, device=dev) for _ in AGENTS], "yaw_noise": [z, z],
              "park": [pk[ag] for ag in AGENTS]}
        g.scenario = lambda env_ids: {k: ([x[env_ids] for x in v] if isinstance(v, list) else v[env_ids])
                                      for k, v in sc.items()}
        base.reset()
        g.scenario = None
        origin = base.scene.env_origins[:, :2]
        slot_t = {ag: torch.tensor(slot[ag], device=dev) for ag in AGENTS}
        for k, ag in enumerate(AGENTS):  # put the robots at their slots, facing +x (parked ones stay)
            robot = base.scene[ag]
            q_adr = robot.indexing.free_joint_q_adr
            st = torch.zeros(n, 13, device=dev)
            st[:, 0] = origin[:, 0] + torch.tensor(start_x[ag], device=dev)
            st[:, 1] = origin[:, 1] + slot_t[ag]
            st[:, 2] = robot.data.data.qpos[:, q_adr[2]]
            st[:, 3:7] = quat_from_euler_xyz(z, z, z)
            here = ~pk[ag]
            far = robot.data.root_link_pos_w[:, :2]
            st[:, :2] = torch.where(here.unsqueeze(-1), st[:, :2], far)
            st[:, 3:7] = torch.where(here.unsqueeze(-1), st[:, 3:7], robot.data.root_link_quat_w)
            robot.write_root_state_to_sim(st, ids)
        base.sim.forward()

        dt = base.step_dt
        steps = int(a.horizon / dt)
        film = a.videos > 0 and mass in video_masses and "pair" in configs
        stride = 2
        rec_q, rec_mp, rec_mq, rec_pts = [], [], [], []
        nmocap = base.sim.mj_model.nmocap

        def record():
            sd = base.sim.data
            rec_q.append(sd.qpos.cpu().numpy().copy())
            if nmocap:
                rec_mp.append(sd.mocap_pos.cpu().numpy().copy())
                rec_mq.append(sd.mocap_quat.cpu().numpy().copy())
            rec_pts.append(np.stack([base.scene[x].data.root_link_pos_w[:, :2].cpu().numpy() for x in AGENTS]
                                    + [g.box_pos()[:, :2].cpu().numpy(), g.goal_xy.cpu().numpy()], 1))
        if film:
            record()

        p0 = g.box_pos()[:, :2].clone()
        h0 = g.heading().clone()
        x_hist = []
        fell = {ag: torch.zeros(n, dtype=torch.bool, device=dev) for ag in AGENTS}
        t_fall = torch.full((n,), float("nan"), device=dev)
        stopped = torch.zeros(n, dtype=torch.bool, device=dev)  # a pushing robot fell
        dx_stop = torch.zeros(n, device=dev)
        tipped = torch.zeros(n, dtype=torch.bool, device=dev)
        on = {ag: torch.zeros(n, device=dev) for ag in AGENTS}
        live = torch.zeros(n, device=dev)
        idle = to_action(0.0, VX_RANGE)
        act = torch.zeros(n, 6, device=dev)
        with torch.no_grad():
            for i in range(steps):
                bxy = g.box_pos()[:, :2]
                for k, ag in enumerate(AGENTS):
                    r = base.scene[ag]
                    pos = r.data.root_link_pos_w[:, :2]
                    yaw = yaw_of(r.data.root_link_quat_w)
                    dy_w = (bxy[:, 1] + slot_t[ag]) - pos[:, 1]
                    vy = torch.clamp(2.0 * torch.cos(yaw) * dy_w, -0.3, 0.3)
                    wz = torch.clamp(2.0 * wrap(-yaw), -0.7, 0.7)
                    push = torch.stack([torch.full_like(vy, to_action(a.speed, VX_RANGE)), to_action(vy, VY_RANGE),
                                        to_action(wz, WZ_RANGE)], -1)
                    still = torch.tensor([idle, 0.0, 0.0], device=dev).expand(n, 3)
                    act[:, 3 * k:3 * k + 3] = torch.where(pk[ag].unsqueeze(-1), still, push)
                base.step(act)
                t = (i + 1) * dt
                bxy = g.box_pos()[:, :2]
                dx = bxy[:, 0] - p0[:, 0]
                new_fall = torch.zeros(n, dtype=torch.bool, device=dev)
                for ag in AGENTS:
                    f = falls.fallen(base, asset_name=ag, nominal_height=SPECS[ag].nominal_height) & ~pk[ag]
                    new_fall |= f & ~fell[ag]
                    fell[ag] |= f
                first = new_fall & ~stopped
                t_fall = torch.where(first, torch.full_like(t_fall, t), t_fall)
                dx_stop = torch.where(stopped, dx_stop, dx)
                stopped |= first
                tipped |= hb.box_tipped(base)
                sd = {ag: g.surface_distance(ag) for ag in AGENTS}
                for ag in AGENTS:
                    on[ag] += ((sd[ag] < 0.10) & ~pk[ag] & ~stopped).float()
                if a.verbose and i % 25 == 0:
                    for j in range(min(n, a.verbose)):
                        s = "  ".join(f"{ag} x {float(base.scene[ag].data.root_link_pos_w[j, 0] - origin[j, 0]):5.2f} "
                                      f"v {float(base.scene[ag].data.root_link_lin_vel_b[j, 0]):4.2f} "
                                      f"surf {float(sd[ag][j]):5.2f}" for ag in AGENTS if not bool(pk[ag][j]))
                        print(f"  t {t:5.2f} env {j} {cases[j][0]}/{cases[j][1]}: object dx {float(dx[j]):6.3f}  {s}",
                              flush=True)
                live += (~stopped).float()
                x_hist.append(dx.clone())
                if film and (i + 1) % stride == 0:
                    record()

        X = torch.stack(x_hist, 0)  # (steps, n)
        late = max(1, int(5.0 / dt))
        v_final = (X[-1] - X[-1 - late]) / (late * dt) if steps > late else X[-1] / a.horizon
        dyaw = torch.rad2deg(wrap(g.heading() - h0)).abs()
        dy = (g.box_pos()[:, 1] - p0[:, 1]).abs()
        mine = []
        for j, (o, c, r) in enumerate(cases):
            row = {"object": o, "config": c, "mass": mass, "rep": r, "slot": SLOTS[o] if c == "pair" else SOLO_SLOT.get(o, 0.0),
                   "dx": round(float(dx_stop[j]), 3), "dx_end": round(float(X[-1, j]), 3),
                   "v_mean": round(float(dx_stop[j]) / a.horizon, 3),
                   "v_final": round(float(v_final[j]), 3) if not bool(stopped[j]) else 0.0,
                   "yaw_change_deg": round(float(dyaw[j]), 1), "lateral_drift": round(float(dy[j]), 3),
                   "fell_anymal": int(bool(fell["anymal"][j])), "fell_spot": int(bool(fell["spot"][j])),
                   "t_fall": "" if math.isnan(float(t_fall[j])) else round(float(t_fall[j]), 2),
                   "tipped": int(bool(tipped[j])),
                   "on_anymal": round(float(on["anymal"][j] / live[j].clamp(min=1)), 3) if c != "spot" else "",
                   "on_spot": round(float(on["spot"][j] / live[j].clamp(min=1)), 3) if c != "anymal" else "",
                   "video": ""}
            mine.append(row)
        if film:
            try:
                cam = Camera(base, vw, vh)
                Q, P = np.stack(rec_q, 1), np.stack(rec_pts, 1)
                MP = np.stack(rec_mp, 1) if rec_mp else None
                MQ = np.stack(rec_mq, 1) if rec_mq else None
                for o in objects:
                    j = next(j for j, cs in enumerate(cases) if cs[0] == o and cs[1] == "pair")
                    r_ = mine[j]
                    name = f"{o}_{mass:g}kg_pair.mp4"
                    cap_txt = f"{o} {mass:g} kg, pair, scripted straight push"
                    render_episode(cam, j, Q[j], None if MP is None else MP[j], None if MQ is None else MQ[j],
                                   P[j], out / "videos" / name, 1.0 / (stride * dt),
                                   caption=lambda f, c=cap_txt, jj=j: f"{c}   t = {f * stride * dt:5.1f} s   "
                                   f"moved {float(X[min(len(X) - 1, f * stride), jj]):4.2f} m")
                    r_["video"] = f"videos/{name}"
            except Exception as ex:  # noqa: BLE001
                print(f"videos skipped: {ex}")
        rows += mine
        msg = "  ".join(f"{c} {sum(r['dx'] for r in mine if r['config'] == c) / max(1, sum(r['config'] == c for r in mine)):.2f} m"
                        for c in configs)
        print(f"[{mass:g} kg] mean forward distance in {a.horizon:g} s: {msg}  ({time.time() - t_start:.0f} s)", flush=True)
        base.close()
        del base

    # -- summary --------------------------------------------------------------------------------------
    with open(out / "episodes.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    def agg(sel):
        k = len(sel)
        if not k:
            return None
        mean = lambda key: sum(float(r[key]) for r in sel) / k  # noqa: E731
        return {"n": k, "dx": mean("dx"), "v_mean": mean("v_mean"), "v_final": mean("v_final"),
                "yaw_change_deg": mean("yaw_change_deg"), "lateral_drift": mean("lateral_drift"),
                "fell_anymal": mean("fell_anymal"), "fell_spot": mean("fell_spot"), "tipped": mean("tipped")}

    by = defaultdict(list)
    for r in rows:
        by[(r["object"], r["config"], r["mass"])].append(r)
    summary = {"name": a.name, "masses": masses, "configs": configs, "reps": a.reps, "horizon_s": a.horizon,
               "speed": a.speed, "slots": {o: SLOTS[o] for o in objects},
               "cases": {f"{o} / {c} / {m:g} kg": agg(by[(o, c, m)]) for o in objects for c in configs for m in masses}}
    (out / "summary.json").write_text(json.dumps(summary, indent=1))

    def cell(o, m, key, fmt):
        return " / ".join(fmt(summary["cases"][f"{o} / {c} / {m:g} kg"][key]) for c in configs)

    label = " / ".join({"pair": "pair", "anymal": "ANYmal", "spot": "Spot"}[c] for c in configs)
    order = [o for o in objects if o not in COMPACT] + [o for o in objects if o in COMPACT]
    name_of = lambda o: f"{o} (compact)" if o in COMPACT else f"{o} (+-{SLOTS[o]:g} m)"  # noqa: E731
    md = [f"# Scripted push test: {a.name}", "",
          f"No learning: each robot walks straight at {a.speed} m/s, heading held, keeping its lateral slot "
          f"relative to the object (pair: ANYmal at +slot, Spot at -slot; alone: centred, the arch: one pillar). "
          f"Broadside push, "
          f"{a.horizon:g} s, {a.reps} placements per case, nominal object sizes. Distance counts until the first "
          f"fall of a pushing robot. Training needs about 0.1 m/s on average (3-6 m in at most 80 s, with "
          f"approach and turning).", "",
          f"## forward distance (m) in {a.horizon:g} s: {label}", "",
          "| object (slot) | " + " | ".join(f"{m:g} kg" for m in masses) + " |", "|---|" + "---|" * len(masses)]
    for o in order:
        md.append(f"| {name_of(o)} | " + " | ".join(cell(o, m, "dx", lambda x: f"{x:.2f}") for m in masses) + " |")
    md += ["", f"## speed over the last 5 s (m/s): {label}", "",
           "| object | " + " | ".join(f"{m:g} kg" for m in masses) + " |", "|---|" + "---|" * len(masses)]
    for o in order:
        md.append(f"| {o} | " + " | ".join(cell(o, m, "v_final", lambda x: f"{x:.2f}") for m in masses) + " |")
    md += ["", f"## falls (ANYmal + Spot, share of runs): {label}", "",
           "| object | " + " | ".join(f"{m:g} kg" for m in masses) + " |", "|---|" + "---|" * len(masses)]
    for o in order:
        md.append(f"| {o} | " + " | ".join(
            " / ".join(f"{summary['cases'][f'{o} / {c} / {m:g} kg']['fell_anymal'] + summary['cases'][f'{o} / {c} / {m:g} kg']['fell_spot']:.2f}"
                       for c in configs) for m in masses) + " |")
    if "pair" in configs:
        md += ["", "## pair only: object turn (deg) and sideways drift (m)", "",
               "| object | " + " | ".join(f"{m:g} kg" for m in masses) + " |", "|---|" + "---|" * len(masses)]
        for o in order:
            md.append(f"| {o} | " + " | ".join(
                f"{summary['cases'][f'{o} / pair / {m:g} kg']['yaw_change_deg']:.0f} deg, "
                f"{summary['cases'][f'{o} / pair / {m:g} kg']['lateral_drift']:.2f} m" for m in masses) + " |")
    (out / "summary.md").write_text("\n".join(md) + "\n")
    stats_dir.mkdir(parents=True, exist_ok=True)
    for f in ("summary.md", "summary.json", "episodes.csv"):
        shutil.copy2(out / f, stats_dir / f)
    print("\n".join(md))
    print(f"\nstats in {stats_dir}\nvideos and full output in {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
