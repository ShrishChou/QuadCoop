"""Brace press sim check (step 2 of the press-skill plan): no learning, CPU MuJoCo, one robot.

Does the static LP (scripts/brace_posture_search.py) hold up in contact physics? ANYmal C is placed
in a posture from evals/brace-lp/summary.json with its bumper against a wall, feet planted, and
pressed by a scripted controller - no stepping:

    joint target = q_posture + tau_ff(F_cmd) / kp        (the same PD as training: kp 19.7 Nm/rad,
                                                           kd 1.26, armature 0.005, 80 Nm limit)

tau_ff(F) are the LP's joint torques that hold a push F with the smallest peak torque (precomputed on
a grid of F at the posture, interpolated), so the PD produces them at the posture. F_cmd follows the
desired push with a slow integral on the measured wall force (closed loop on force, like a press
skill would). Settings match the walker env: dt 0.005 s, control at 50 Hz, pyramidal cone,
impratio 1, foot friction governs at the ground.

Cases (each posture: nominal stance, best brace):
  wall      an immovable wall; desired push steps 0 -> 50 -> ... -> F_max (2.5 s each): achieved
            force, swing, joint-torque saturation, foot slip, base drift, falls
  giveway   pressing 200 N, the wall then backs away at 0.05 / 0.2 m/s (an object that starts to
            slide): does the robot stay up without stepping, how far does it lean before losing contact
Output: evals/brace-sim/summary.md, summary.json.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import mujoco
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from brace_posture_search import EFFORT, LEGS, PUSH_POINT_B, XML, Model  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
ARMATURE = 0.005
OMEGA = 10 * 2.0 * math.pi
KP = ARMATURE * OMEGA ** 2
KD = 2 * 2.0 * ARMATURE * OMEGA
DT, DECIM = 0.005, 4


def build(mu_foot: float):
    spec = mujoco.MjSpec.from_file(str(XML))
    spec.option.timestep = DT
    spec.option.integrator = mujoco.mjtIntegrator.mjINT_IMPLICITFAST
    spec.option.cone = mujoco.mjtCone.mjCONE_PYRAMIDAL
    spec.option.impratio = 1.0
    wb = spec.worldbody
    wb.add_geom(name="floor", type=mujoco.mjtGeom.mjGEOM_PLANE, size=[20, 20, 0.1], friction=[1.0, 0.005, 0.0001],
                priority=0)
    wall = wb.add_body(name="wall", mocap=True, pos=[2.0, 0, 0.5])
    wall.add_geom(name="wall", type=mujoco.mjtGeom.mjGEOM_BOX, size=[0.1, 1.0, 0.5], friction=[0.5, 0.005, 0.0001],
                  priority=2)
    for g in spec.geoms:
        if g.name.endswith("_foot"):
            g.friction = [mu_foot, 0.005, 0.0001]
            g.priority = 1
            g.solimp = [0.015, 1, 0.03, 0.5, 2]
        elif "_collision" in (g.name or ""):
            g.priority = 1
    for leg in LEGS:
        for j in ("HAA", "HFE", "KFE"):
            jn = f"{leg}_{j}"
            spec.joint(jn).armature = ARMATURE
            spec.add_actuator(name=jn, target=jn, trntype=mujoco.mjtTrn.mjTRN_JOINT,
                              gainprm=[KP] + [0] * 9, biasprm=[0, -KP, -KD] + [0] * 7,
                              gaintype=mujoco.mjtGain.mjGAIN_FIXED, biastype=mujoco.mjtBias.mjBIAS_AFFINE,
                              forcelimited=True, forcerange=[-EFFORT, EFFORT])
    m = spec.compile()
    return m, mujoco.MjData(m)


def tau_table(post: dict, mu: float, fmax: float):
    """LP joint torques (actuator order LF..RH x HAA,HFE,KFE) for pushes 0..fmax at the posture."""
    M = Model()
    nominal = M.nominal_feet()
    assert M.pose(post["h"], math.radians(post["pitch_deg"]), post["dx_front"], post["dx_hind"], post["dwidth"], nominal)
    Fs = np.arange(0.0, fmax + 1e-6, 10.0)
    taus = []
    for F in Fs:
        r = M.lp_min_torque(mu, float(F))
        if r is None:
            break
        taus.append(r[2])
    Fs = Fs[:len(taus)]
    feet = {l: M.d.site_xpos[M.site[l]].copy() for l in LEGS}
    return Fs, np.array(taus), M.joint_q(), M.d.qpos[0:7].copy(), feet


def wall_force(m, d, wall_gid: int) -> float:
    """Horizontal force (x, world) the robot puts on the wall."""
    f6 = np.zeros(6)
    total = 0.0
    for i in range(d.ncon):
        c = d.contact[i]
        if wall_gid not in (c.geom1, c.geom2):
            continue
        other = c.geom2 if c.geom1 == wall_gid else c.geom1
        if m.geom_bodyid[other] == 0:
            continue
        mujoco.mj_contactForce(m, d, i, f6)
        fw = c.frame.reshape(3, 3).T @ f6[:3]  # force on geom2 from geom1... sign fixed below
        sgn = 1.0 if c.geom2 == wall_gid else -1.0  # contact force acts on geom2 (MuJoCo: geom1 -> geom2 normal)
        total += sgn * fw[0]
    return total


def run(post: dict, mu: float, case: str, levels=None, giveway_speed=0.0, f_hold=200.0, seed=0):
    m, d = build(mu)
    Fs, taus, q, base, _ = tau_table(post, mu, post["F_max"] or 300.0)
    fmax_tab = float(Fs[-1])
    act_q = np.array([q[m.actuator(i).name] for i in range(m.nu)])
    act_order = [f"{l}_{j}" for l in LEGS for j in ("HAA", "HFE", "KFE")]
    perm = [act_order.index(m.actuator(i).name) for i in range(m.nu)]

    def tff(F):
        F = float(np.clip(F, 0.0, fmax_tab))
        k = np.searchsorted(Fs, F)
        if k == 0:
            t = taus[0]
        else:
            w = (F - Fs[k - 1]) / max(Fs[min(k, len(Fs) - 1)] - Fs[k - 1], 1e-9)
            t = (1 - w) * taus[k - 1] + w * taus[min(k, len(Fs) - 1)]
        return t[perm]

    d.qpos[0:7] = base
    for i in range(m.nu):
        d.qpos[m.jnt_qposadr[m.actuator_trnid[i, 0]]] = act_q[i]
    mujoco.mj_forward(m, d)
    # wall face just touching the bumper: the robot's farthest-forward collision point
    wall_gid = m.geom("wall").id
    xs = []
    for g in range(m.ngeom):
        if m.geom_bodyid[g] == m.body("base").id and m.geom_contype[g]:
            R = d.geom_xmat[g].reshape(3, 3)
            c, half = m.geom_aabb[g][:3], m.geom_aabb[g][3:]
            xs.append(d.geom_xpos[g][0] + (R @ c)[0] + np.abs(R[0]) @ half)
    face = max(xs) + 0.001
    wall_x = face + 0.1
    d.mocap_pos[0] = (wall_x, 0.0, 0.5)
    mujoco.mj_forward(m, d)

    foot_sites = [m.site(l).id for l in LEGS]
    foot_geoms = [m.geom(f"{l}_foot").id for l in LEGS]
    base_id = m.body("base").id
    x0 = d.xpos[base_id].copy()
    if case == "wall":
        sched = [(0.0, 1.5)] + [(F, 2.5) for F in levels]
    else:
        sched = [(0.0, 1.0), (f_hold, 3.0), ("giveway", 3.0)]
    F_cmd, ki = 0.0, 2.0  # integral on force error, N per N*s
    res, t = [], 0.0
    fell = False
    for F_des, dur in sched:
        n_ctrl = int(round(dur / (DT * DECIM)))
        rec = {"F_des": F_des if F_des != "giveway" else f_hold, "phase": "giveway" if F_des == "giveway" else "press",
               "F": [], "sat": 0, "slip": [], "n": 0}
        for k in range(n_ctrl):
            Fw = wall_force(m, d, wall_gid)
            target = rec["F_des"]
            F_cmd += ki * (target - Fw) * DT * DECIM
            F_cmd = float(np.clip(F_cmd, 0.0, fmax_tab))
            d.ctrl[:] = act_q + tff(F_cmd) / KP
            for _ in range(DECIM):
                if F_des == "giveway":
                    d.mocap_pos[0][0] += giveway_speed * DT
                mujoco.mj_step(m, d)
            t += DT * DECIM
            measure = k >= n_ctrl // 2
            # falls: base too low / tilted, or a non-foot geom on the floor
            up = d.xmat[base_id].reshape(3, 3)[:, 2]
            if up[2] < 0.7 or d.xpos[base_id][2] < 0.25:
                fell = True
            for i in range(d.ncon):
                c = d.contact[i]
                if m.geom("floor").id in (c.geom1, c.geom2):
                    o = c.geom2 if c.geom1 == m.geom("floor").id else c.geom1
                    if o not in foot_geoms and m.geom_bodyid[o] != 0 and m.geom_bodyid[o] != m.body("wall").id:
                        fell = True
            if measure:
                rec["F"].append(wall_force(m, d, wall_gid))
                rec["sat"] += int((np.abs(d.actuator_force) >= 0.95 * EFFORT).any())
                v = np.zeros(6)
                sl = []
                for s in foot_sites:
                    mujoco.mj_objectVelocity(m, d, mujoco.mjtObj.mjOBJ_SITE, s, v, 0)
                    sl.append(np.linalg.norm(v[3:5]))
                rec["slip"].append(float(np.mean(sl)))
                rec["n"] += 1
            if fell:
                break
        F = np.array(rec["F"]) if rec["F"] else np.zeros(1)
        res.append({"phase": rec["phase"], "F_des": rec["F_des"], "F_mean": float(F.mean()), "F_std": float(F.std()),
                    "touch": float((F > 5).mean()), "sat": rec["sat"] / max(rec["n"], 1),
                    "slip": float(np.mean(rec["slip"])) if rec["slip"] else float("nan"),
                    "drift": float(np.linalg.norm((d.xpos[base_id] - x0)[:2])), "fell": fell,
                    "wall_moved": float(d.mocap_pos[0][0] - wall_x)})
        if fell:
            break
    return res, fmax_tab


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lp", default=str(ROOT / "evals/brace-lp/summary.json"))
    ap.add_argument("--out", default=str(ROOT / "evals/brace-sim"))
    ap.add_argument("--mus", default="0.6,0.8,1.0")
    a = ap.parse_args()
    lp = json.loads(Path(a.lp).read_text())
    posts = {"nominal": lp["nominal_for_sim"], "brace": lp["brace_for_sim"]}
    mus = [float(x) for x in a.mus.split(",")]
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    allres = {}
    md = ["# Brace press sim check: evals/brace-sim", "",
          "CPU MuJoCo, one ANYmal C, feet planted, scripted press (joint target = posture + LP torques / kp, slow "
          "integral on the measured wall force), no stepping. Same PD, timestep, decimation and cone as the walker "
          "env. Each level 2.5 s, measured over the second half.", ""]
    for p in posts.values():
        md.append(f"- **{'nominal' if p is posts['nominal'] else 'brace'}**: height {p['h']} m, pitch {p['pitch_deg']} deg "
                  f"(- = nose up), front feet {p['dx_front']:+} m, hind feet {p['dx_hind']:+} m, {p['dwidth']} m wider")
    for mu in mus:
        md += ["", f"## Immovable wall, foot friction {mu} (static LP ceiling {mu * lp['mass'] * 9.81 * math.cos(math.pi / 8):.0f} N at the friction cone)", "",
               "| desired (N) | nominal: force (swing), sat, slip m/s, fell | brace: force (swing), sat, slip m/s, fell |", "|---|---|---|"]
        rows = {}
        for name, post in posts.items():
            post = {**post}
            levels = [50, 100, 150, 200, 250, 300, 350, 400]
            r, fmax = run(post, mu, "wall", levels=levels)
            rows[name] = {x["F_des"]: x for x in r if x["phase"] == "press"}
            allres[f"wall_{name}_mu{mu}"] = {"res": r, "fmax_table": fmax}
        for F in [50, 100, 150, 200, 250, 300, 350, 400]:
            cells = []
            for name in posts:
                x = rows[name].get(F)
                cells.append("-" if x is None else f"{x['F_mean']:.0f} ({x['F_std']:.0f}), {x['sat']:.2f}, {x['slip']:.3f}, "
                             f"{'FELL' if x['fell'] else 'no'}")
            md.append(f"| {F} | " + " | ".join(cells) + " |")
    md += ["", "## Wall gives way while pressing 200 N (foot friction 0.8): the robot cannot step", "",
           "| wall speed (m/s) | posture | force while pressing (N) | force during give-way (N) | fell | base moved (m) | wall moved (m) |",
           "|---|---|---|---|---|---|---|"]
    for sp in (0.05, 0.2):
        for name, post in posts.items():
            r, _ = run({**post}, 0.8, "giveway", giveway_speed=sp)
            allres[f"giveway_{name}_{sp}"] = r
            pr = next((x for x in r if x["phase"] == "press" and x["F_des"] > 0), None)
            gw = next((x for x in r if x["phase"] == "giveway"), None)
            md.append(f"| {sp} | {name} | {pr['F_mean'] if pr else float('nan'):.0f} | "
                      f"{gw['F_mean'] if gw else float('nan'):.0f} | {r[-1]['fell']} | {r[-1]['drift']:.2f} | {r[-1]['wall_moved']:.2f} |")
    (out / "summary.md").write_text("\n".join(md) + "\n")
    (out / "summary.json").write_text(json.dumps(allres, indent=1))
    print("\n".join(md))


if __name__ == "__main__":
    main()
