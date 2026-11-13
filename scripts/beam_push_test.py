"""Engaged-start beam push with the frozen walker: can simple commands transport a beam with two ANYmals?

    QUADCOOP_PLANNER=ends QUADCOOP_CONTACT=train QUADCOOP_CMD_IF=raw python scripts/beam_push_test.py
    python scripts/beam_push_test.py --speeds 0.4,0.6,0.8 --masses 40,60,80 --mus 0.4,0.5,0.6 --horizon 20

No policy and no planner. Two ANYmal C robots (QUADCOOP_PAIR=anymal) run the frozen walker (evals/models.yaml) under
a scripted command, adapted from scripts/push_test.py. The beam starts at the origin, broadside (long side along y),
and the robots start engaged: each robot's front is --gap m behind the beam's back face at its slot (y = +/- --slot m
from the beam centre), both facing +x. Every 20 ms each robot commands:
  vx  the case's forward speed (constant)
  vy  2 x (its slot y relative to the beam's current centre - its y), clipped to +/- 0.3 m/s (lateral correction)
  wz  2 x (0 - its heading), clipped to +/- 0.7 rad/s (heading correction)
The walker's command interface is the raw affine map onto vx (-0.6, 0.8), vy (-0.5, 0.5), wz (-0.7, 0.7) m/s, rad/s.

Physics is unchanged except that the beam's friction is set per repeat instead of drawn: each repeat uses one of
--mus (the training range is 0.4-0.6). The floor's friction, both geoms' contact priority and the simulated beam mass
are recorded. In MuJoCo the higher-priority geom sets a contact's friction (equal priority takes the maximum); the
objects have priority 2 (stage1b/shapes.py), so the beam's own friction governs beam-floor sliding. That value is
reported as mu_eff.

Cases: speeds x masses x friction repeats (default 3 x 3 x 3 = 27), --horizon s each. Per case (episodes.csv):
  dx, v_mean          forward beam displacement (m) up to the first fall, and dx / horizon
  v_last              forward speed over the last 10 s (0 if a robot fell)
  yaw_drift, lat      beam turn (deg) and sideways drift (m) at the end
  fell_*, t_fall      falls (a fall stops the distance count)
  F_x                 net force on the beam along +x (the common transport direction) from both robots, averaged
                      over the measured window (t >= --settle s, until the first fall): delivered impulse / time,
                      so it averages over gait cycles; F_x_p10/p50/p90 are percentiles of its 1 s moving mean
  F_x_*               the same per robot; impulse_* (N s) is the integral over the window
  duty_*              share of the window each robot touches the beam; duty_both = both touching at the same step
                      (simultaneous contact, not gait-averaged), duty_any = at least one
  cy_mean_*, cy_sd_*  each robot's front point (root + half body length along its heading) along the beam
                      (object frame y, m) while touching
  mu_obj, mu_floor, mu_eff, mass_sim, mu_m_g = mu_eff x mass x 9.81 (a scale for sliding resistance, not a
                      measured threshold)
Output: logs/evals/<name>/ (episodes.csv, summary.md, summary.json, provenance.json); stats copied to evals/<name>/.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import shutil
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT))

VX_RANGE, VY_RANGE, WZ_RANGE = (-0.6, 0.8), (-0.5, 0.5), (-0.7, 0.7)  # walker command ranges (stage1)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", default="beam-push")
    ap.add_argument("--speeds", default="0.4,0.6,0.8")
    ap.add_argument("--masses", default="40,60,80")
    ap.add_argument("--mus", default="0.4,0.5,0.6", help="beam friction, one repeat per value")
    ap.add_argument("--horizon", type=float, default=20.0)
    ap.add_argument("--settle", type=float, default=2.0, help="force and contact are measured from this time on")
    ap.add_argument("--slot", type=float, default=0.70, help="lateral slot of each robot, m from the beam centre")
    ap.add_argument("--gap", type=float, default=0.05, help="start: robot front to the beam's back face, m")
    ap.add_argument("--device", default=None)
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()

    from train_coop2 import resolve_models, set_env

    models = resolve_models("b", "anymal")
    set_env(models)
    os.environ.setdefault("QUADCOOP_CMD_IF", "raw")
    import numpy as np
    import torch

    import quadcoop  # noqa: F401
    from mjlab.envs import ManagerBasedRlEnv
    from mjlab.utils.lab_api.math import quat_from_euler_xyz
    from push_test import back_face_x, to_action

    from quadcoop import falls
    from quadcoop.coop2 import mdp as cm
    from quadcoop.coop2.env_cfg import SPECS, make_coop2_env_cfg
    from quadcoop.coop2.mdp import AGENTS
    from quadcoop.stage1.mdp import wrap, yaw_of
    from quadcoop.stage1b import mdp as hb
    from quadcoop.stage1b.shapes import NOMINAL_MASS
    from quadcoop.stage2 import mdp as m2
    from quadcoop.stage2.shapes import OBJ_NAMES2, SHAPE_NAMES2, SHAPES2, kinds_tensor, nominal_parts

    assert AGENTS == ("anymal1", "anymal2"), f"expected two ANYmals, got {AGENTS}"
    assert os.environ["QUADCOOP_CMD_IF"] == "raw", "this test commands the walker through the raw interface"
    device = a.device or ("cuda:0" if torch.cuda.is_available() else "cpu")
    speeds = [float(x) for x in a.speeds.split(",")]
    masses = [float(x) for x in a.masses.split(",")]
    mus = [float(x) for x in a.mus.split(",")]
    out = ROOT / "logs" / "evals" / a.name
    stats_dir = ROOT / "evals" / a.name
    out.mkdir(parents=True, exist_ok=True)
    bk = SHAPE_NAMES2.index("beam")
    beam = OBJ_NAMES2[bk]
    nom, nom_rest = nominal_parts("cpu")
    kinds = kinds_tensor("cpu")
    n = len(speeds)  # one env per speed; one env build per (mass, friction)
    slot = {AGENTS[0]: a.slot, AGENTS[1]: -a.slot}
    start_x = {ag: back_face_x(nom[bk], kinds[bk], float(nom_rest[bk]), slot[ag]) - SPECS[ag].half_length - a.gap
               for ag in AGENTS}
    print(f"beam push: speeds {speeds} x masses {masses} x friction {mus}, {a.horizon:g} s, slots +/-{a.slot} m, "
          f"start gap {a.gap} m", flush=True)
    rows, t0 = [], time.time()

    for mass in masses:
        for rep, mu in enumerate(mus):
            cfg = make_coop2_env_cfg("b", play=True, push_sensors=True)  # robot-object force sensors (push_<robot>)
            cfg.scene.num_envs = n
            cfg.episode_length_s = 1e5
            cfg.terminations = {}
            alpha = 0.5 * math.log(mass / NOMINAL_MASS)
            for name in OBJ_NAMES2:
                cfg.events[f"{name}_mass"].params["alpha_range"] = (alpha, alpha)
            assert f"{beam}_friction" in cfg.events, "the beam's friction event is missing"
            cfg.events[f"{beam}_friction"].params["ranges"] = (mu, mu)
            torch.manual_seed(a.seed + rep)
            base = ManagerBasedRlEnv(cfg=cfg, device=device)
            g = base.command_manager.get_term("goal")
            dev = base.device
            ids = torch.arange(n, device=dev)
            for k in range(len(SHAPES2)):
                m2.apply_geometry(base, ids, k, torch.ones(n, 3, device=dev))
            z = torch.zeros(n, device=dev)
            sc = {"shape": torch.full((n,), bk, device=dev, dtype=torch.long), "obj_xy_rel": torch.zeros(n, 2, device=dev),
                  "obj_heading": z.clone(), "goal_xy_rel": torch.tensor([[3.0, 0.0]], device=dev).repeat(n, 1),
                  "goal_yaw": z.clone(), "bearings": [torch.full((n,), math.pi, device=dev) for _ in AGENTS],
                  "gaps": [torch.full((n,), 0.5, device=dev) for _ in AGENTS], "yaw_noise": [z, z],
                  "park": [torch.zeros(n, dtype=torch.bool, device=dev) for _ in AGENTS]}
            g.scenario = lambda env_ids: {k: ([x[env_ids] for x in v] if isinstance(v, list) else v[env_ids])
                                          for k, v in sc.items()}
            base.reset()
            g.scenario = None
            origin = base.scene.env_origins[:, :2]
            for ag in AGENTS:  # engaged start: at the slot, facing +x, front --gap behind the beam
                robot = base.scene[ag]
                q_adr = robot.indexing.free_joint_q_adr
                st = torch.zeros(n, 13, device=dev)
                st[:, 0] = origin[:, 0] + start_x[ag]
                st[:, 1] = origin[:, 1] + slot[ag]
                st[:, 2] = robot.data.data.qpos[:, q_adr[2]]
                st[:, 3:7] = quat_from_euler_xyz(z, z, z)
                robot.write_root_state_to_sim(st, ids)
            base.sim.forward()
            # recorded physics: beam friction, floor friction, simulated mass
            mjm = base.sim.mj_model
            gf = base.sim.model.geom_friction
            gid = torch.as_tensor(list(base.scene[beam].indexing.geom_ids), device=dev, dtype=torch.long)
            mu_obj = (gf[:, gid, 0] if gf.dim() == 3 else gf[gid, 0].expand(n, -1)).mean(-1)
            floor = [i for i in range(mjm.ngeom) if int(mjm.geom_type[i]) == 0]  # planes
            mu_floor = (gf[:, floor, 0].amax(-1) if gf.dim() == 3 else gf[floor, 0].amax().expand(n)) if floor \
                else torch.full((n,), float("nan"), device=dev)
            # MuJoCo: the geom with the higher contact priority sets the friction; equal priority takes the maximum
            pr_obj = max(int(mjm.geom_priority[int(i)]) for i in gid.tolist())
            pr_floor = max((int(mjm.geom_priority[i]) for i in floor), default=-1)
            body = base.scene[beam].indexing.body_ids[0]
            bm = base.sim.model.body_mass
            mass_sim = bm[:, body] if bm.dim() == 2 else bm[body].expand(n)

            dt = base.step_dt
            steps = int(a.horizon / dt)
            settle = int(a.settle / dt)
            p0, h0 = g.box_pos()[:, :2].clone(), g.heading().clone()
            fell = {ag: torch.zeros(n, dtype=torch.bool, device=dev) for ag in AGENTS}
            stopped = torch.zeros(n, dtype=torch.bool, device=dev)
            t_fall = torch.full((n,), float("nan"), device=dev)
            dx_stop = torch.zeros(n, device=dev)
            tipped = torch.zeros(n, dtype=torch.bool, device=dev)
            X, FX, TOUCH, CY, MEAS = [], [], [], [], []
            vx_a = torch.tensor([to_action(s, VX_RANGE) for s in speeds], device=dev)
            act = torch.zeros(n, 6, device=dev)
            with torch.no_grad():
                for i in range(steps):
                    bxy = g.box_pos()[:, :2]
                    for k, ag in enumerate(AGENTS):
                        r = base.scene[ag]
                        pos = r.data.root_link_pos_w[:, :2]
                        yaw = yaw_of(r.data.root_link_quat_w)
                        vy = torch.clamp(2.0 * torch.cos(yaw) * ((bxy[:, 1] + slot[ag]) - pos[:, 1]), -0.3, 0.3)
                        wz = torch.clamp(2.0 * wrap(-yaw), -0.7, 0.7)
                        act[:, 3 * k:3 * k + 3] = torch.stack([vx_a, to_action(vy, VY_RANGE), to_action(wz, WZ_RANGE)], -1)
                    base.step(act)
                    t = (i + 1) * dt
                    bxy = g.box_pos()[:, :2]
                    dx = bxy[:, 0] - p0[:, 0]
                    new = torch.zeros(n, dtype=torch.bool, device=dev)
                    for ag in AGENTS:
                        f = falls.fallen(base, asset_name=ag, nominal_height=SPECS[ag].nominal_height)
                        new |= f & ~fell[ag]
                        fell[ag] |= f
                    first = new & ~stopped
                    t_fall = torch.where(first, torch.full_like(t_fall, t), t_fall)
                    dx_stop = torch.where(stopped, dx_stop, dx)
                    stopped |= first
                    tipped |= hb.box_tipped(base)
                    h = g.heading()
                    fx, tc, cy = [], [], []
                    for ag in AGENTS:
                        fx.append(cm.object_force_from(base, ag)[:, 0])
                        tc.append(base.scene[f"push_{ag}"].data.found.view(n, -1).any(-1))
                        r = base.scene[ag]  # front point: root + half the body length along the heading
                        yw = yaw_of(r.data.root_link_quat_w)
                        fp = r.data.root_link_pos_w[:, :2] + SPECS[ag].half_length * torch.stack([torch.cos(yw), torch.sin(yw)], -1)
                        rel = fp - bxy
                        cy.append(-torch.sin(h) * rel[:, 0] + torch.cos(h) * rel[:, 1])
                    X.append(dx.clone())
                    FX.append(torch.stack(fx, -1))
                    TOUCH.append(torch.stack(tc, -1))
                    CY.append(torch.stack(cy, -1))
                    MEAS.append((i >= settle) & ~stopped)

            X = torch.stack(X).cpu().numpy()            # (T, n)
            FX = torch.stack(FX).cpu().numpy()          # (T, n, 2)
            TOUCH = torch.stack(TOUCH).cpu().numpy()    # (T, n, 2)
            CY = torch.stack(CY).cpu().numpy()          # (T, n, 2)
            MEAS = torch.stack(MEAS).cpu().numpy()      # (T, n)
            dyaw = torch.rad2deg(wrap(g.heading() - h0)).abs().cpu().numpy()
            lat = (g.box_pos()[:, 1] - p0[:, 1]).abs().cpu().numpy()
            last = min(int(10.0 / dt), steps - 1)  # final-speed window (shorter on a short smoke run)
            w1 = max(1, int(round(1.0 / dt)))
            for j, sp in enumerate(speeds):
                mj = MEAS[:, j]
                T_m = float(mj.sum()) * dt
                fx = FX[mj, j]                          # (Tm, 2)
                tc = TOUCH[mj, j].astype(bool)
                ftot = fx.sum(-1)
                mov = np.convolve(ftot, np.ones(w1) / w1, mode="valid") if len(ftot) >= w1 else ftot
                q = (lambda p: round(float(np.percentile(mov, p)), 1)) if len(mov) else (lambda p: "")
                st_j = bool(stopped[j])
                me = float(mu_obj[j]), float(mu_floor[j])
                mu_eff = me[0] if (pr_obj > pr_floor or math.isnan(me[1])) else (me[1] if pr_floor > pr_obj else max(me))
                row = {"speed": sp, "mass": mass, "mu_set": mu, "rep": rep, "mu_obj": round(me[0], 3),
                       "mu_floor": round(me[1], 3), "prio_obj": pr_obj, "prio_floor": pr_floor, "mu_eff": round(mu_eff, 3), "mass_sim": round(float(mass_sim[j]), 2),
                       "mu_m_g": round(mu_eff * float(mass_sim[j]) * 9.81, 1),
                       "dx": round(float(dx_stop[j]), 3), "v_mean": round(float(dx_stop[j]) / a.horizon, 3),
                       "v_last": 0.0 if st_j else round(float(X[-1, j] - X[-1 - last, j]) / (last * dt), 3),
                       "yaw_drift": round(float(dyaw[j]), 1), "lat": round(float(lat[j]), 3),
                       "fell_anymal1": int(bool(fell[AGENTS[0]][j])), "fell_anymal2": int(bool(fell[AGENTS[1]][j])),
                       "t_fall": "" if math.isnan(float(t_fall[j])) else round(float(t_fall[j]), 2),
                       "tipped": int(bool(tipped[j])), "measured_s": round(T_m, 2),
                       "F_x": round(float(ftot.sum() * dt / max(T_m, 1e-9)), 1) if T_m else "",
                       "F_x_p10": q(10), "F_x_p50": q(50), "F_x_p90": q(90)}
                for k, ag in enumerate(AGENTS):
                    row[f"F_x_{ag}"] = round(float(fx[:, k].sum() * dt / max(T_m, 1e-9)), 1) if T_m else ""
                    row[f"impulse_{ag}"] = round(float(fx[:, k].sum() * dt), 1)
                    row[f"duty_{ag}"] = round(float(tc[:, k].mean()), 3) if len(tc) else ""
                    ys = CY[mj, j, k][tc[:, k]] if len(tc) else np.zeros(0)
                    row[f"cy_mean_{ag}"] = round(float(ys.mean()), 3) if len(ys) else ""
                    row[f"cy_sd_{ag}"] = round(float(ys.std()), 3) if len(ys) else ""
                row["duty_both"] = round(float((tc[:, 0] & tc[:, 1]).mean()), 3) if len(tc) else ""
                row["duty_any"] = round(float((tc[:, 0] | tc[:, 1]).mean()), 3) if len(tc) else ""
                rows.append(row)
            print(f"[{mass:g} kg, mu {mu}] " + "  ".join(
                f"{r['speed']} m/s: dx {r['dx']:.2f} m F_x {r['F_x']} N both {r['duty_both']} fell "
                f"{r['fell_anymal1'] + r['fell_anymal2']}" for r in rows[-n:]) + f"  ({time.time() - t0:.0f} s)", flush=True)
            base.close()
            del base

    with open(out / "episodes.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    def mean(sel, k):
        v = [float(r[k]) for r in sel if r[k] != ""]
        return sum(v) / len(v) if v else float("nan")

    cells = {}
    for m in masses:
        for s in speeds:
            sel = [r for r in rows if r["mass"] == m and r["speed"] == s]
            cells[f"{m:g} kg / {s} m/s"] = {k: mean(sel, k) for k in (
                "dx", "v_mean", "v_last", "yaw_drift", "lat", "fell_anymal1", "fell_anymal2", "F_x", "F_x_p90",
                "duty_anymal1", "duty_anymal2", "duty_both", "mu_m_g")} | {
                "transported": sum(1 for r in sel if float(r["dx"]) >= 1.0), "n": len(sel),
                "dx_by_mu": {str(r["mu_set"]): r["dx"] for r in sel}}
    summary = {"name": a.name, "speeds": speeds, "masses": masses, "mus": mus, "horizon_s": a.horizon,
               "settle_s": a.settle, "slot_m": a.slot, "gap_m": a.gap, "cells": cells}
    (out / "summary.json").write_text(json.dumps(summary, indent=1))
    prov = {"argv": sys.argv, "models": models, "pair": AGENTS,
            "env": {k: os.environ.get(k, "") for k in ("QUADCOOP_PLANNER", "QUADCOOP_CONTACT", "QUADCOOP_CMD_IF",
                                                        "QUADCOOP_PAIR", "QUADCOOP_SHAPES")}
            | {k: v for k, v in os.environ.items() if k.startswith("QUADCOOP_WALKER")}}
    (out / "provenance.json").write_text(json.dumps(prov, indent=1, default=str))

    md = [f"# Engaged-start beam push: {a.name}", "",
          f"Two ANYmals, frozen walker, scripted: constant forward command, lateral slot +/-{a.slot} m and heading held. "
          f"Beam broadside, robots start {a.gap} m behind it. {a.horizon:g} s per case; force and contact from "
          f"{a.settle:g} s until the first fall. Beam friction per repeat: {mus}. 'transported' = moved >= 1 m "
          f"(0.05 m/s average) before any fall.", "",
          "| mass | speed cmd | transported | dx m (by mu " + "/".join(map(str, mus)) + ") | v last 10 s | yaw drift deg | "
          "falls | F_x N (impulse/time) | F_x 1 s p90 | duty r1 / r2 / both | mu m g N |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for m in masses:
        for s in speeds:
            c = cells[f"{m:g} kg / {s} m/s"]
            md.append(f"| {m:g} | {s} | {c['transported']}/{c['n']} | {' / '.join(f'{float(v):.2f}' for v in c['dx_by_mu'].values())} | "
                      f"{c['v_last']:.3f} | {c['yaw_drift']:.0f} | {c['fell_anymal1'] + c['fell_anymal2']:.2f} | "
                      f"{c['F_x']:.0f} | {c['F_x_p90']:.0f} | {c['duty_anymal1']:.2f} / {c['duty_anymal2']:.2f} / "
                      f"{c['duty_both']:.2f} | {c['mu_m_g']:.0f} |")
    (out / "summary.md").write_text("\n".join(md) + "\n")
    stats_dir.mkdir(parents=True, exist_ok=True)
    for f in ("summary.md", "summary.json", "episodes.csv", "provenance.json"):
        shutil.copy2(out / f, stats_dir / f)
    print("\n".join(md))
    print(f"\nstats in {stats_dir}\nfull output in {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
