"""Brace posture search (step 1 of the press-skill plan): no learning, no simulation run.

Question: how hard can ANYmal C push, standing still, and in which posture? The walkers top out at
~150-180 N, in taps, at 100% joint-torque saturation (evals/wt-v22k). The planner needs ~250 N per
robot sustained (evals/pp-fsweep). This finds the physical ceiling for a quasi-static press.

For each posture on a grid (base height, base pitch, front / hind foot fore-aft offset, stance
width), the feet are placed on the floor by inverse kinematics, and a linear program finds the
largest push the bumper can deliver to the object:

    maximise   F                                    (push on the object along d = (cos a, 0, sin a))
    subject to 0 = g_base - sum_i J_i,base^T f_i + J_p,base^T d F      (base: unactuated, static)
               |g_j - sum_i J_i,j^T f_i + J_p,j^T d F| <= tau_max     (every joint, both ways)
               f_i in the foot friction cone (8-sided inner pyramid), f_i,z >= fz_min

g = gravity generalized force (qfrc_bias at rest, leg masses included); J_i = foot-site Jacobians,
J_p = the bumper point's Jacobian (base frame (0.50, 0, 0), robots/anymal_c.py push_point_b). The
force on the robot is -d F. The base rows encode force and moment balance, so tipping and
unloading a foot pair are covered.

Also reported: the same LP with one foot lifted (a step while pressing; two diagonal feet alone
cannot hold any static push, so mid-trot is not a static case) and the
heaviest object of friction mu_o one robot can slide with that push, F (cos a + mu_o sin a) / (mu_o g)
(an upward tilt a also unloads the object; it needs tan a <= the bumper-object friction).

Output: evals/brace-lp/summary.md, summary.json (all feasible postures, best per case, the best
posture's joint angles and torques for scripts/brace_press_sim.py).
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path

import mujoco
import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[1]
XML = ROOT / "src/quadcoop/assets/anymal_c/anymal_c.xml"
LEGS = ("LF", "RF", "LH", "RH")
JOINTS = ("HAA", "HFE", "KFE")
DEFAULT_Q = {"HAA": 0.0, "LF_HFE": 0.4, "RF_HFE": 0.4, "LH_HFE": -0.4, "RH_HFE": -0.4,
             "LF_KFE": -0.8, "RF_KFE": -0.8, "LH_KFE": 0.8, "RH_KFE": 0.8}
PUSH_POINT_B = np.array([0.50, 0.0, 0.0])
EFFORT = 80.0
G = 9.81


def quat_pitch(theta: float) -> np.ndarray:  # rotation about +y: theta > 0 = nose down
    return np.array([math.cos(theta / 2), 0.0, math.sin(theta / 2), 0.0])


class Model:
    def __init__(self, m: mujoco.MjModel | None = None, d: mujoco.MjData | None = None):
        """Robot-only model by default; pass a sim model (robot first in it) to reuse the IK / LP there."""
        self.m = m if m is not None else mujoco.MjSpec.from_file(str(XML)).compile()
        self.d = d if d is not None else mujoco.MjData(self.m)
        m = self.m
        self.site = {l: m.site(l).id for l in LEGS}
        self.qadr = {l: [m.joint(f"{l}_{j}").qposadr[0] for j in JOINTS] for l in LEGS}
        self.vadr = {l: [m.joint(f"{l}_{j}").dofadr[0] for j in JOINTS] for l in LEGS}
        self.base = m.body("base").id
        self.mass = float(m.body_subtreemass[self.base])
        self.foot_r = float(m.geom_size[m.geom("LF_foot").id][0])
        self.lo = {l: m.jnt_range[[m.joint(f"{l}_{j}").id for j in JOINTS]][:, 0] for l in LEGS}
        self.hi = {l: m.jnt_range[[m.joint(f"{l}_{j}").id for j in JOINTS]][:, 1] for l in LEGS}

    def reset_pose(self, h: float, pitch: float):
        d = self.d
        d.qpos[:] = self.m.qpos0
        d.qpos[0:3] = (0.0, 0.0, h)
        d.qpos[3:7] = quat_pitch(pitch)
        for l in LEGS:
            for j, a in zip(JOINTS, self.qadr[l]):
                d.qpos[a] = DEFAULT_Q.get(f"{l}_{j}", DEFAULT_Q.get(j, 0.0))
        d.qvel[:] = 0.0
        mujoco.mj_kinematics(self.m, d)
        mujoco.mj_comPos(self.m, d)

    def nominal_feet(self) -> dict[str, np.ndarray]:
        """Foot sites (world) at the default pose, base at 0.55 m, level."""
        self.reset_pose(0.55, 0.0)
        return {l: self.d.site_xpos[self.site[l]].copy() for l in LEGS}

    def ik_leg(self, leg: str, target: np.ndarray, iters: int = 60) -> float:
        m, d = self.m, self.d
        jp = np.zeros((3, m.nv))
        qa, va = self.qadr[leg], self.vadr[leg]
        for _ in range(iters):
            mujoco.mj_kinematics(m, d)
            mujoco.mj_comPos(m, d)
            err = target - d.site_xpos[self.site[leg]]
            if np.linalg.norm(err) < 1e-4:
                break
            mujoco.mj_jacSite(m, d, jp, None, self.site[leg])
            J = jp[:, va]
            dq = J.T @ np.linalg.solve(J @ J.T + 1e-4 * np.eye(3), err)
            dq = np.clip(dq, -0.2, 0.2)
            d.qpos[qa] = np.clip(d.qpos[qa] + dq, self.lo[leg], self.hi[leg])
        mujoco.mj_kinematics(m, d)
        mujoco.mj_comPos(m, d)
        return float(np.linalg.norm(target - d.site_xpos[self.site[leg]]))

    def pose(self, h, pitch, dx_front, dx_hind, dwidth, nominal) -> bool:
        """Base at height h / pitch, feet on the floor shifted from nominal; False if unreachable."""
        self.reset_pose(h, pitch)
        for l in LEGS:
            t = nominal[l].copy()
            t[0] += dx_front if l[1] == "F" else dx_hind
            t[1] += math.copysign(dwidth, t[1])
            t[2] = self.foot_r
            if self.ik_leg(l, t) > 0.005:
                return False
        # knees must stay well above the floor and the base clear of it
        d = self.d
        for l in LEGS:
            shank = self.m.body(f"{l}_SHANK").id
            if d.xpos[shank][2] < 0.08:
                return False
        return True

    def lp(self, mu: float, alpha: float, feet=LEGS, tau_max: float = EFFORT, fz_min: float = 10.0):
        """Largest static push F (N) in the current pose; returns (F, f per foot, joint torques)."""
        m, d = self.m, self.d
        mujoco.mj_forward(m, d)  # qvel = 0: qfrc_bias = gravity
        g = d.qfrc_bias.copy()
        nf = len(feet)
        Jf = []
        jp = np.zeros((3, m.nv))
        for l in feet:
            mujoco.mj_jacSite(m, d, jp, None, self.site[l])
            Jf.append(jp.copy())
        pw = d.xpos[self.base] + d.xmat[self.base].reshape(3, 3) @ PUSH_POINT_B
        mujoco.mj_jac(m, d, jp, None, pw, self.base)
        Jp = jp.copy()
        dvec = np.array([math.cos(alpha), 0.0, math.sin(alpha)])
        # variables x = [f_1 (3) ... f_nf (3), F]; actuator torque tau = g - sum J_i^T f_i + Jp^T d F
        nx = 3 * nf + 1
        A = np.zeros((m.nv, nx))
        for i, J in enumerate(Jf):
            A[:, 3 * i:3 * i + 3] = -J.T
        A[:, -1] = Jp.T @ dvec
        # tau = g + A x
        A_eq, b_eq = A[:6], -g[:6]
        act = list(range(6, m.nv))
        A_ub = [A[act], -A[act]]
        b_ub = [tau_max - g[act], tau_max + g[act]]
        k = 8
        ce = mu * math.cos(math.pi / k)
        for i in range(nf):
            for th in np.arange(k) * 2 * math.pi / k:
                row = np.zeros(nx)
                row[3 * i:3 * i + 3] = (math.cos(th), math.sin(th), -ce)
                A_ub.append(row[None])
                b_ub.append(np.zeros(1))
        A_ub = np.vstack(A_ub)
        b_ub = np.concatenate(b_ub)
        bounds = []
        for _ in range(nf):
            bounds += [(None, None), (None, None), (fz_min, None)]
        bounds.append((0.0, None))
        c = np.zeros(nx)
        c[-1] = -1.0
        r = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method="highs")
        if r.status != 0:
            return None
        x = r.x
        tau = g + A @ x
        return float(x[-1]), x[:-1].reshape(nf, 3), tau[6:]

    def lp_min_torque(self, mu: float, F: float, feet=LEGS, fz_min: float = 10.0, w_base: np.ndarray | None = None,
                      tang_weight: float = 0.0):
        """Hold a push of F N (a = 0) with the smallest peak joint torque; returns (t, f per foot, tau) or None.

        w_base: a generalized force the feet must also put on the base (free-joint dofs: world force, body-frame
        torque), e.g. a balance PD's correction in the sim check; None = static (0)."""
        m, d = self.m, self.d
        mujoco.mj_forward(m, d)
        g = d.qfrc_bias.copy()
        nf = len(feet)
        jp = np.zeros((3, m.nv))
        nx = 3 * nf + 1  # foot forces, then t = peak |tau|
        A = np.zeros((m.nv, nx))
        for i, l in enumerate(feet):
            mujoco.mj_jacSite(m, d, jp, None, self.site[l])
            A[:, 3 * i:3 * i + 3] = -jp.T
        pw = d.xpos[self.base] + d.xmat[self.base].reshape(3, 3) @ PUSH_POINT_B
        mujoco.mj_jac(m, d, jp, None, pw, self.base)
        c0 = g + (jp.T @ np.array([1.0, 0.0, 0.0])) * F  # tau = c0 + A[:, :3nf] f
        act = list(range(6, m.nv))
        Af = A[:, :-1]
        A_ub = [np.hstack([Af[act], -np.ones((len(act), 1))]), np.hstack([-Af[act], -np.ones((len(act), 1))])]
        b_ub = [-c0[act], c0[act]]
        k = 8
        ce = mu * math.cos(math.pi / k)
        for i in range(nf):
            for th in np.arange(k) * 2 * math.pi / k:
                row = np.zeros(nx)
                row[3 * i:3 * i + 3] = (math.cos(th), math.sin(th), -ce)
                A_ub.append(row[None])
                b_ub.append(np.zeros(1))
        A_eq = np.hstack([Af[:6], np.zeros((6, 1))])
        bounds = [b for _ in range(nf) for b in ((None, None), (None, None), (fz_min, None))] + [(0.0, None)]
        c = np.zeros(nx)
        c[-1] = 1.0
        A_ub = np.vstack(A_ub)
        b_ub = np.concatenate(b_ub)
        if tang_weight > 0:
            # slack s_i,x >= |f_i,x|, s_i,y >= |f_i,y|; cost tang_weight (Nm per N) on their sum. Without it the
            # min-peak-torque optimum is degenerate in the internal foot forces and parks feet on the cone edge,
            # which in contact physics means slipping (the sim check's robot did the splits).
            ns = 2 * nf
            A_ub = np.hstack([A_ub, np.zeros((A_ub.shape[0], ns))])
            rows = []
            for i in range(nf):
                for a_ in range(2):
                    for sg in (1.0, -1.0):
                        row = np.zeros(nx + ns)
                        row[3 * i + a_] = sg
                        row[nx + 2 * i + a_] = -1.0
                        rows.append(row)
            A_ub = np.vstack([A_ub, np.array(rows)])
            b_ub = np.concatenate([b_ub, np.zeros(len(rows))])
            A_eq = np.hstack([A_eq, np.zeros((6, ns))])
            bounds = bounds + [(0.0, None)] * ns
            c = np.concatenate([c, np.full(ns, tang_weight)])
        b_eq = -c0[:6] if w_base is None else -c0[:6] - w_base
        r = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method="highs")
        if r.status != 0:
            return None
        f = r.x[:3 * nf]
        return float(r.x[3 * nf]), f.reshape(nf, 3), (c0 + Af @ f)[6:]

    def joint_q(self) -> dict[str, float]:
        return {f"{l}_{j}": float(self.d.qpos[a]) for l in LEGS for j, a in zip(JOINTS, self.qadr[l])}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "evals/brace-lp"))
    ap.add_argument("--mus", default="0.6,0.8,1.0")
    ap.add_argument("--alphas_deg", default="0,10,20")
    ap.add_argument("--tau_margins", default="1.0,0.8")
    ap.add_argument("--mu_obj", type=float, default=0.45)
    ap.add_argument("--f_ref", type=float, default=250.0, help="push held for the torque-headroom ranking (N)")
    ap.add_argument("--mu_ref", type=float, default=0.8)
    a = ap.parse_args()
    mus = [float(x) for x in a.mus.split(",")]
    alphas = [math.radians(float(x)) for x in a.alphas_deg.split(",")]
    margins = [float(x) for x in a.tau_margins.split(",")]

    M = Model()
    nominal = M.nominal_feet()
    heights = np.round(np.arange(0.38, 0.575, 0.03), 3)
    pitches = np.radians([-10, -5, 0, 5, 10])
    dfs = np.round(np.arange(-0.15, 0.151, 0.05), 3)
    dhs = np.round(np.arange(-0.30, 0.101, 0.05), 3)
    dws = (0.0, 0.05, 0.10)

    rows = []
    for h, p, df, dh, dw in itertools.product(heights, pitches, dfs, dhs, dws):
        if not M.pose(h, p, df, dh, dw, nominal):
            continue
        rec = {"h": float(h), "pitch_deg": round(math.degrees(p), 1), "dx_front": float(df), "dx_hind": float(dh),
               "dwidth": float(dw)}
        for mu in mus:
            for al in alphas:
                for tm in margins:
                    r4 = M.lp(mu, al, tau_max=tm * EFFORT)
                    rec[f"F4_mu{mu}_a{round(math.degrees(al))}_t{tm}"] = None if r4 is None else round(r4[0], 1)
            # one foot lifted (a step while pressing): the worse of lifting a front or a hind foot
            r3f = M.lp(mu, 0.0, feet=("LF", "LH", "RH"), tau_max=EFFORT)
            r3h = M.lp(mu, 0.0, feet=("LF", "RF", "LH"), tau_max=EFFORT)
            rec[f"F3f_mu{mu}"] = None if r3f is None else round(r3f[0], 1)
            rec[f"F3h_mu{mu}"] = None if r3h is None else round(r3h[0], 1)
        rt = M.lp_min_torque(a.mu_ref, a.f_ref)
        rec["tau_peak_ref"] = None if rt is None else round(rt[0], 1)
        rows.append(rec)
    print(f"{len(rows)} reachable postures")

    def best(key):
        ok = [r for r in rows if r.get(key) is not None]
        return max(ok, key=lambda r: r[key]) if ok else None

    def nominal_row():
        cand = [r for r in rows if r["dx_front"] == 0 and r["dx_hind"] == 0 and r["dwidth"] == 0 and r["pitch_deg"] == 0]
        return min(cand, key=lambda r: abs(r["h"] - 0.53)) if cand else None

    nom = nominal_row()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    md = ["# Brace posture search: evals/brace-lp", "",
          "Static LP, no simulation: the largest push the front bumper can hold with the feet planted, joint torques "
          f"within the limit (80 Nm x margin), feet inside their friction cone (min 10 N each). Robot {M.mass:.1f} kg "
          f"(weight {M.mass * G:.0f} N). {len(rows)} reachable postures on the grid (base height 0.38-0.56 m, pitch "
          "-10..10 deg, front feet -0.15..+0.15 m, hind feet -0.30..+0.10 m fore-aft from nominal, stance +0/5/10 cm "
          "wider each side). 'slides' = heaviest object of friction "
          f"{a.mu_obj} this push slides: F (cos a + mu_o sin a) / (mu_o g).", "",
          "## Ceiling by foot friction (push level, a = 0)", "",
          "| foot mu | friction bound mu m g (N) | nominal stance, 4 feet, full torque (N) | best brace, full torque (N) | best brace, 80% torque (N) | best, front foot lifted (N) | best, hind foot lifted (N) |",
          "|---|---|---|---|---|---|---|"]
    summary = {"mass": M.mass, "n_postures": len(rows), "best": {}, "nominal": nom}
    for mu in mus:
        k1, k8, kf, kh = f"F4_mu{mu}_a0_t1.0", f"F4_mu{mu}_a0_t0.8", f"F3f_mu{mu}", f"F3h_mu{mu}"
        b1, b8, bf, bh = best(k1), best(k8), best(kf), best(kh)
        summary["best"].update({k1: b1, k8: b8, kf: bf, kh: bh})
        f = lambda r, k: "-" if (r is None or r.get(k) is None) else f"{r[k]:.0f}"
        md.append(f"| {mu} | {mu * M.mass * G:.0f} | {f(nom, k1)} | {f(b1, k1)} | {f(b8, k8)} | {f(bf, kf)} | {f(bh, kh)} |")

    # the ceiling ties across postures (friction-bound), so rank postures by torque headroom at a fixed push
    okt = sorted([r for r in rows if r["tau_peak_ref"] is not None], key=lambda r: r["tau_peak_ref"])
    md += ["", f"## Torque headroom: smallest peak joint torque that holds {a.f_ref:.0f} N (foot mu {a.mu_ref}, a = 0)", "",
           f"{len(okt)} of {len(rows)} postures can hold it at all.", "",
           "| posture | height (m) | pitch (deg) | front feet dx (m) | hind feet dx (m) | wider (m) | peak torque (Nm) | % of 80 Nm |",
           "|---|---|---|---|---|---|---|---|"]
    show = [("nominal", nom)] + [(f"#{i + 1}", r) for i, r in enumerate(okt[:8])] + [("worst feasible", okt[-1] if okt else None)]
    for name, r in show:
        if r is None or r.get("tau_peak_ref") is None:
            md.append(f"| {name} | - | - | - | - | - | infeasible | - |")
            continue
        md.append(f"| {name} | {r['h']} | {r['pitch_deg']} | {r['dx_front']:+} | {r['dx_hind']:+} | {r['dwidth']} | "
                  f"{r['tau_peak_ref']:.0f} | {100 * r['tau_peak_ref'] / EFFORT:.0f}% |")
    summary["min_torque"] = okt[:20]

    md += ["", "## Upward push component (best brace, full torque): push N / heaviest object it slides (kg)", "",
           "| foot mu | " + " | ".join(f"a = {round(math.degrees(x))} deg" for x in alphas) + " |",
           "|---|" + "---|" * len(alphas)]
    for mu in mus:
        cells = []
        for al in alphas:
            k = f"F4_mu{mu}_a{round(math.degrees(al))}_t1.0"
            b = best(k)
            if b is None:
                cells.append("-")
            else:
                F = b[k]
                cells.append(f"{F:.0f} N / {F * (math.cos(al) + a.mu_obj * math.sin(al)) / (a.mu_obj * G):.0f} kg")
        md.append(f"| {mu} | " + " | ".join(cells) + " |")

    # sensitivity: smallest peak torque at f_ref as each posture variable is fixed (others free)
    mu_s = a.mu_ref
    md += ["", f"## What matters: smallest peak torque (Nm) holding {a.f_ref:.0f} N with one variable fixed, the rest free "
           "(lower = more headroom)", ""]
    for var, vals in (("h", heights), ("pitch_deg", [round(math.degrees(x), 1) for x in pitches]),
                      ("dx_front", dfs), ("dx_hind", dhs), ("dwidth", dws)):
        cells = []
        for v in vals:
            ok = [r["tau_peak_ref"] for r in rows if abs(r[var] - float(v)) < 1e-6 and r.get("tau_peak_ref") is not None]
            cells.append(f"{float(v):g}: {min(ok):.0f}" if ok else f"{float(v):g}: -")
        md.append(f"- **{var}**: " + ", ".join(cells))

    # the most-headroom brace posture and the nominal stance, for scripts/brace_press_sim.py
    def for_sim(r):
        M.pose(r["h"], math.radians(r["pitch_deg"]), r["dx_front"], r["dx_hind"], r["dwidth"], nominal)
        q = M.joint_q()
        base = {"pos": M.d.qpos[0:3].tolist(), "quat": M.d.qpos[3:7].tolist()}
        Fmax = M.lp(mu_s, 0.0, tau_max=EFFORT)
        return {**r, "mu": mu_s, "q": q, "base": base, "F_max": None if Fmax is None else Fmax[0]}
    if okt:
        b = okt[0]
        summary["brace_for_sim"] = for_sim(b)
        t, fs, tau = M.lp_min_torque(mu_s, a.f_ref)
        md += ["", f"## Posture handed to the sim check (most headroom at {a.f_ref:.0f} N)", "",
               f"height {b['h']} m, pitch {b['pitch_deg']} deg, front feet {b['dx_front']:+} m, hind feet {b['dx_hind']:+} m, "
               f"{b['dwidth']} m wider; static ceiling {summary['brace_for_sim']['F_max']:.0f} N at foot mu {mu_s}. "
               f"At {a.f_ref:.0f} N: foot normal forces (N) LF/RF/LH/RH " + ", ".join(f"{x:.0f}" for x in fs[:, 2]) +
               f", peak joint torque {t:.0f} Nm."]
    if nom is not None:
        summary["nominal_for_sim"] = for_sim(nom)

    (out / "summary.md").write_text("\n".join(md) + "\n")
    (out / "summary.json").write_text(json.dumps({**summary, "rows": rows}, indent=1))
    print("\n".join(md))


if __name__ == "__main__":
    main()
