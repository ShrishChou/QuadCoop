"""Brace press check with whole-body balance (step 2 of the press-skill plan): no learning, CPU MuJoCo.

Does the static LP (scripts/brace_posture_search.py) hold up in contact physics? ANYmal C stands in a
posture from evals/brace-lp/summary.json, bumper 1 cm from a wall, feet planted, no stepping. A
scripted whole-body controller presses:

  every 0.01 s  solve the min-peak-torque LP (plus a 0.2 Nm-per-N cost on tangential foot forces: without it the
                optimum parks feet on the friction-cone edge and they slip) at the *current* state for F_cmd, with the base
                also asked for a balance wrench (PD on base position / orientation, the standard
                whole-body-control loop: without it, feedforward LP torques leave the floating base
                uncontrolled and it drifts off, see scripts/brace_press_sim.py's open-loop variant)
  actuators     the training PD (kp 19.7 Nm/rad, kd 1.26, armature 0.005, 80 Nm) used as a torque
                source: target = q_measured + tau / kp
  force loop    F_cmd = F_des + an integral on the measured wall force

Cases, per posture (nominal stance, feasible brace; lp_best on request) x foot friction:
  wall      immovable wall; desired push steps 50 -> 100 -> ... -> 400 N, 2.5 s each, measured over the
            second half: force, swing (raw / 0.4 s average, as walker_test.py), torque saturation,
            foot slip, base drift, falls
  giveway   pressing 200 N, then the wall backs away at 0.05 / 0.2 m/s for 3 s (an object starting to
            slide): stays up without stepping? keeps contact?
Output: evals/brace-wbc/summary.md, summary.json.
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
from brace_posture_search import EFFORT, JOINTS, LEGS, XML, Model  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
ARMATURE = 0.005
OMEGA = 10 * 2.0 * math.pi
KP = ARMATURE * OMEGA ** 2
KD = 2 * 2.0 * ARMATURE * OMEGA
DT = 0.005
LEVELS = (50, 100, 150, 200, 250, 300, 350, 400)


CONTACT = {  # name: (cone, impratio); foot solimp stays (0.015, 1, 0.03) as in robots/anymal_c.py
    "train": (mujoco.mjtCone.mjCONE_PYRAMIDAL, 1.0),   # the walker env (mjlab defaults): feet creep under load,
                                                       # see evals/contact-creep
    "nocreep": (mujoco.mjtCone.mjCONE_ELLIPTIC, 10.0),  # creep 30-70x smaller
}


def build(mu_foot: float, contact: str = "train"):
    spec = mujoco.MjSpec.from_file(str(XML))
    spec.option.timestep = DT
    spec.option.integrator = mujoco.mjtIntegrator.mjINT_IMPLICITFAST
    spec.option.cone, spec.option.impratio = CONTACT[contact]
    wb = spec.worldbody
    wb.add_geom(name="floor", type=mujoco.mjtGeom.mjGEOM_PLANE, size=[20, 20, 0.1], friction=[1.0, 0.005, 0.0001])
    wall = wb.add_body(name="wall", mocap=True, pos=[5.0, 0, 0.5])
    wall.add_geom(name="wall", type=mujoco.mjtGeom.mjGEOM_BOX, size=[0.1, 1.0, 0.5], friction=[0.5, 0.005, 0.0001],
                  priority=2)
    for g in spec.geoms:
        if g.name.endswith("_foot"):
            g.friction = [mu_foot, 0.005, 0.0001]
            g.priority = 1
            g.condim = 3
            g.solimp = [0.015, 1, 0.03, 0.5, 2]
        elif "_collision" in (g.name or ""):
            g.priority = 1
            g.condim = 3
    for leg in LEGS:
        for j in JOINTS:
            jn = f"{leg}_{j}"
            spec.joint(jn).armature = ARMATURE
            spec.add_actuator(name=jn, target=jn, trntype=mujoco.mjtTrn.mjTRN_JOINT,
                              gainprm=[KP] + [0] * 9, biasprm=[0, -KP, -KD] + [0] * 7,
                              gaintype=mujoco.mjtGain.mjGAIN_FIXED, biastype=mujoco.mjtBias.mjBIAS_AFFINE,
                              forcelimited=True, forcerange=[-EFFORT, EFFORT])
    m = spec.compile()
    return m, mujoco.MjData(m)


def posture_state(post: dict):
    """Base pose and joint angles of a posture row (feet on the floor by IK)."""
    M = Model()
    nominal = M.nominal_feet()
    assert M.pose(post["h"], math.radians(post["pitch_deg"]), post["dx_front"], post["dx_hind"], post["dwidth"], nominal)
    return M.d.qpos[0:7].copy(), M.joint_q()


def bumper_face_x(m, d, base_id) -> float:
    """Largest world x of the base body's collision geoms (exact for boxes and cylinders)."""
    xs = []
    for g in range(m.ngeom):
        if m.geom_bodyid[g] != base_id or not m.geom_contype[g]:
            continue
        R = d.geom_xmat[g].reshape(3, 3)
        hs = m.geom_size[g]
        t = m.geom_type[g]
        if t == mujoco.mjtGeom.mjGEOM_BOX:
            ext = np.abs(R[0]) @ hs
        elif t in (mujoco.mjtGeom.mjGEOM_CYLINDER, mujoco.mjtGeom.mjGEOM_CAPSULE):
            ax = abs(R[0, 2])
            rad = hs[0] if t == mujoco.mjtGeom.mjGEOM_CAPSULE else hs[0] * math.sqrt(max(0.0, 1 - ax * ax))
            ext = ax * hs[1] + rad
        else:
            ext = hs[0]
        xs.append(d.geom_xpos[g][0] + ext)
    return float(max(xs))


def wall_force(m, d, wall_gid: int) -> float:
    """Force (world x) the robot puts on the wall."""
    f6 = np.zeros(6)
    total = 0.0
    for i in range(d.ncon):
        c = d.contact[i]
        if wall_gid not in (c.geom1, c.geom2):
            continue
        mujoco.mj_contactForce(m, d, i, f6)
        fw = c.frame.reshape(3, 3).T @ f6[:3]  # MuJoCo: the force geom1 exerts on geom2, normal geom1 -> geom2
        total += fw[0] if c.geom2 == wall_gid else -fw[0]
    return float(total)


def run(post: dict, mu: float, case: str, giveway_speed: float = 0.0, f_hold: float = 200.0,
        ki: float = 2.0, kp_lin: float = 100.0, kd_lin: float = 20.0, kp_rot: float = 300.0, kd_rot: float = 30.0,
        ctrl_hz: float = 100.0, tang_weight: float = 0.2, trace: list | None = None, contact: str = "train"):
    m, d = build(mu, contact)
    base, q = posture_state(post)
    M = Model(m, d)
    d.qpos[0:7] = base
    for k, v in q.items():
        d.qpos[m.joint(k).qposadr[0]] = v
    mujoco.mj_forward(m, d)
    base_id = M.base
    wall_gid = m.geom("wall").id
    floor_gid = m.geom("floor").id
    wall_x = bumper_face_x(m, d, base_id) + 0.01 + 0.1  # wall face 1 cm ahead (box half-depth 0.1)
    d.mocap_pos[0] = (wall_x, 0.0, 0.5)
    mujoco.mj_forward(m, d)

    act = [m.actuator(f"{l}_{j}").id for l in LEGS for j in JOINTS]
    act_q = np.array([m.joint(f"{l}_{j}").qposadr[0] for l in LEGS for j in JOINTS])
    foot_g = {m.geom(f"{l}_foot").id for l in LEGS}
    every = max(1, round(1.0 / (ctrl_hz * DT)))
    p0, quat0 = d.qpos[0:3].copy(), d.qpos[3:7].copy()
    sched = [(0.0, 1.5, "press")] + [(float(F), 2.5, "press") for F in LEVELS] if case == "wall" else \
        [(0.0, 1.0, "press"), (f_hold, 3.0, "press"), (f_hold, 3.0, "giveway")]
    integ, tau, fell, lp_fail = 0.0, None, False, 0
    out = []
    for F_des, dur, phase in sched:
        n = int(round(dur / DT))
        rec = {"F": [], "sat": [], "slip": []}
        for k in range(n):
            Fw = wall_force(m, d, wall_gid)
            if k % every == 0:
                if F_des > 0:
                    integ = float(np.clip(integ + ki * (F_des - Fw) * every * DT, -0.5 * F_des, 0.5 * F_des))
                F_cmd = max(0.0, F_des + integ) if F_des > 0 else 0.0
                w = np.zeros(6)
                # no position stiffness along the push (x): the object is the constraint there, a spring to the
                # start pose would subtract from the push; damping only
                w[0:3] = M.mass * (kp_lin * (p0 - d.qpos[0:3]) * np.array([0.0, 1.0, 1.0]) - kd_lin * d.qvel[0:3])
                err = np.zeros(3)
                mujoco.mju_subQuat(err, quat0, d.qpos[3:7])
                w[3:6] = kp_rot * err - kd_rot * d.qvel[3:6]
                r = None
                for s in (1.0, 0.5, 0.0):
                    r = M.lp_min_torque(mu, F_cmd, w_base=s * w, tang_weight=tang_weight)
                    if r is not None:
                        break
                if r is None:
                    lp_fail += 1
                else:
                    tau = r[2]
            d.ctrl[act] = d.qpos[act_q] + (tau if tau is not None else 0.0) / KP
            if trace is not None and k % 20 == 0:
                trace.append((round(F_des), round(Fw, 1), round(F_cmd if F_des > 0 else 0.0, 1), round(float(d.qpos[0] - p0[0]), 4),
                              round(float(d.qpos[2] - p0[2]), 4), lp_fail))
            if phase == "giveway":
                d.mocap_pos[0][0] += giveway_speed * DT
            mujoco.mj_step(m, d)
            up = d.xmat[base_id].reshape(3, 3)[2, 2]
            if up < 0.7 or d.qpos[2] < 0.25 or any(
                    floor_gid in (c.geom1, c.geom2) and (c.geom2 if c.geom1 == floor_gid else c.geom1) not in foot_g
                    and m.geom_bodyid[c.geom2 if c.geom1 == floor_gid else c.geom1] != 0 for c in d.contact[:d.ncon]):
                fell = True
                break
            if k >= n // 2:
                rec["F"].append(wall_force(m, d, wall_gid))
                rec["sat"].append(float((np.abs(d.actuator_force[act]) >= 0.95 * EFFORT).any()))
                v6 = np.zeros(6)
                sl = []
                for l in LEGS:
                    mujoco.mj_objectVelocity(m, d, mujoco.mjtObj.mjOBJ_SITE, M.site[l], v6, 0)
                    sl.append(np.linalg.norm(v6[3:5]))
                rec["slip"].append(float(np.mean(sl)))
        F = np.array(rec["F"]) if rec["F"] else np.array([0.0])
        win = max(1, round(0.4 / DT))
        Fs = np.convolve(F, np.ones(win) / win, mode="valid") if len(F) >= win else F
        out.append({"phase": phase, "F_des": F_des, "F_mean": float(F.mean()), "std_raw": float(F.std()),
                    "std_04": float(Fs.std()), "touch": float((F > 5).mean()),
                    "sat": float(np.mean(rec["sat"])) if rec["sat"] else float("nan"),
                    "slip": float(np.mean(rec["slip"])) if rec["slip"] else float("nan"),
                    "drift": float(np.linalg.norm(d.qpos[0:2] - p0[:2])), "fell": fell, "lp_fail": lp_fail,
                    "peak_tau": float(np.abs(d.actuator_force[act]).max()),
                    "wall_moved": float(d.mocap_pos[0][0] - wall_x)})
        if fell:
            break
    return out


def feasible_pick() -> dict:
    """The feasible brace (evals/brace-lp/feasible.json, scripts/brace_feasible_rank.py): push point <= 0.50 m,
    knees >= 30 deg bent; within 1 Nm of the best torque, the most bent knees (same rule as draw_brace_postures.py)."""
    fe = json.loads((ROOT / "evals/brace-lp/feasible.json").read_text())
    best_t = fe["top"][0]["tau_peak_ref"]
    return max([r for r in fe["top"] if r["tau_peak_ref"] <= best_t + 1.0], key=lambda r: (r["knee_min_deg"], -r["tau_peak_ref"]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lp", default=str(ROOT / "evals/brace-lp/summary.json"))
    ap.add_argument("--out", default=str(ROOT / "evals/brace-wbc"))
    ap.add_argument("--mus", default="0.6,0.8,1.0")
    ap.add_argument("--postures", default="nominal,feasible", help="nominal, feasible, lp_best (rejected: too high)")
    ap.add_argument("--no_giveway", action="store_true")
    ap.add_argument("--contacts", default="train,nocreep", help="contact models: train (walker env), nocreep")
    a = ap.parse_args()
    lp = json.loads(Path(a.lp).read_text())
    allp = {"nominal": lp["nominal_for_sim"], "feasible": feasible_pick(), "lp_best": lp["brace_for_sim"]}
    posts = {k: allp[k] for k in a.postures.split(",")}
    mus = [float(x) for x in a.mus.split(",")]
    contacts = a.contacts.split(",")
    cols = [(k, c) for c in contacts for k in posts]  # one column per posture x contact model
    res = {}
    md = ["# Brace press check with whole-body balance: evals/brace-wbc", "",
          "CPU MuJoCo, one ANYmal C, feet planted, no stepping, no learning. Every 0.01 s the min-peak-torque LP "
          "(scripts/brace_posture_search.py) is solved at the current state for the push plus a base balance wrench "
          "(PD on base pose); the training PD actuators deliver the torques; a slow integral closes the loop on the "
          "measured wall force. Each level 2.5 s, measured over the second half. Swing = std of the force, raw / "
          "after a 0.4 s average (as evals/wt-v22k). Contact models: **train** = the walker env (pyramidal cone, "
          "impratio 1: loaded feet creep, evals/contact-creep), **nocreep** = elliptic cone, impratio 10 (same foot "
          "solimp).", ""]
    for k, p in posts.items():
        md.append(f"- **{k}**: height {p['h']} m, pitch {p['pitch_deg']} deg (- = nose up), front feet {p['dx_front']:+} m, "
                  f"hind feet {p['dx_hind']:+} m, {p['dwidth']} m wider; LP peak torque at 250 N: {p['tau_peak_ref']:.0f} Nm")
    passes = []
    for mu in mus:
        md += ["", f"## Immovable wall, foot friction {mu} (LP friction-cone ceiling about "
               f"{mu * lp['mass'] * 9.81 * math.cos(math.pi / 8) - 0:.0f} N)", "",
               "| desired (N) | " + " | ".join(f"{k} / {c}: force (swing raw / 0.4 s), torque-sat, slip m/s" for k, c in cols) + " |",
               "|---|" + "---|" * len(cols)]
        table = {}
        for k, c in cols:
            r = run(posts[k], mu, "wall", contact=c)
            res[f"wall_{k}_{c}_mu{mu}"] = r
            table[(k, c)] = {x["F_des"]: x for x in r if x["F_des"] > 0}
            print(k, c, mu, [(x["F_des"], round(x["F_mean"]), round(x["std_04"]), x["fell"]) for x in r], flush=True)
            ok = [F for F, x in table[(k, c)].items() if not x["fell"] and abs(x["F_mean"] - F) <= 0.15 * F
                  and x["std_04"] <= 0.15 * F and x["touch"] >= 0.95]
            passes.append((f"{k} / {c}", mu, ok, next((x["F_des"] for x in r if x["fell"]), None)))
        for F in LEVELS:
            cells = []
            for kc in cols:
                x = table[kc].get(float(F))
                cells.append("not reached (fell earlier)" if x is None else
                             f"{x['F_mean']:.0f} ({x['std_raw']:.0f} / {x['std_04']:.0f}), {x['sat']:.2f}, {x['slip']:.3f}"
                             + (" FELL" if x["fell"] else ""))
            md.append(f"| {F} | " + " | ".join(cells) + " |")
    md += ["", "## Holds (within 15% of the target, 0.4 s swing under 15%, touching >= 95%, no fall)", ""]
    for k, mu, ok, fell_at in passes:
        md.append(f"- **{k}, foot mu {mu}**: " + (", ".join(f"{F:.0f}" for F in ok) + " N" if ok else "none")
                  + (f"; fell at the {fell_at:.0f} N level" if fell_at else ""))
    if not a.no_giveway:
        md += ["", "## The wall gives way while pressing 200 N (foot friction 0.8; the robot cannot step)", "",
               "| wall speed (m/s) | posture / contact | force before (N) | force during give-way (N) | touching during | fell | base moved (m) |",
               "|---|---|---|---|---|---|---|"]
        for sp in (0.05, 0.2):
            for k, c in cols:
                r = run(posts[k], 0.8, "giveway", giveway_speed=sp, contact=c)
                res[f"giveway_{k}_{c}_{sp}"] = r
                pr = next((x for x in r if x["phase"] == "press" and x["F_des"] > 0), None)
                gw = next((x for x in r if x["phase"] == "giveway"), None)
                f = lambda x, key: "-" if x is None else f"{x[key]:.0f}"
                md.append(f"| {sp} | {k} / {c} | {f(pr, 'F_mean')} | {f(gw, 'F_mean')} | "
                          f"{'-' if gw is None else round(gw['touch'], 2)} | {r[-1]['fell']} | {r[-1]['drift']:.2f} |")
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "summary.md").write_text("\n".join(md) + "\n")
    (out / "summary.json").write_text(json.dumps(res, indent=1))
    print("\n".join(md))


if __name__ == "__main__":
    main()
