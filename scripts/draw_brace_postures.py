"""Draw candidate press postures from evals/brace-lp (no GL needed): side and top views from the kinematics.

Each posture: legs (hip -> thigh -> knee -> foot), the base collision box, the bumper push point, the
250 N push on the object (orange) and the LP's foot reaction forces that hold it (green, 1 m per 500 N),
plus joint angles vs the default stance. Output: evals/brace-lp/postures.png
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from brace_posture_search import LEGS, PUSH_POINT_B, Model  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
F_REF, MU = 250.0, 0.8
SCALE = 1.0 / 500.0  # m per N for force arrows


def moderate(lp, h_max=0.53, pitch_min=-5.0, hind_min=-0.20):
    rows = [r for r in lp["rows"] if r.get("tau_peak_ref") is not None and r["h"] <= h_max + 1e-9
            and r["pitch_deg"] >= pitch_min and r["dx_hind"] >= hind_min - 1e-9]
    return min(rows, key=lambda r: r["tau_peak_ref"])


def chain(M, leg):
    d, m = M.d, M.m
    names = [f"{leg}_HIP", f"{leg}_THIGH", f"{leg}_SHANK"]
    pts = [d.xpos[m.body(n).id].copy() for n in names]
    pts.append(d.site_xpos[M.site[leg]].copy())
    return np.array(pts)


def base_box(M):
    d, m = M.d, M.m
    g = m.geom("base_collision0").id
    R, c, hs = d.geom_xmat[g].reshape(3, 3), d.geom_xpos[g], m.geom_size[g]
    corners = np.array([c + R @ (hs * np.array(s)) for s in
                        [(-1, -1, -1), (1, -1, -1), (1, -1, 1), (-1, -1, 1), (-1, 1, -1), (1, 1, -1), (1, 1, 1), (-1, 1, 1)]])
    return corners


def main():
    lp = json.loads((ROOT / "evals/brace-lp/summary.json").read_text())
    fe = json.loads((ROOT / "evals/brace-lp/feasible.json").read_text())
    # feasible pick: within 1 Nm of the best feasible torque, the most bent knees (evals/brace-lp/feasible.md)
    best_t = fe["top"][0]["tau_peak_ref"]
    pick = max([r for r in fe["top"] if r["tau_peak_ref"] <= best_t + 1.0], key=lambda r: (r["knee_min_deg"], -r["tau_peak_ref"]))
    posts = [("nominal stance", lp["nominal_for_sim"]), ("FEASIBLE BRACE (pick)", pick),
             ("best LP brace - REJECTED (push too high, straight hind legs)", lp["brace_for_sim"])]
    M = Model()
    nominal_feet = M.nominal_feet()
    M.reset_pose(0.55, 0.0)
    q_def = M.joint_q()
    fig, axes = plt.subplots(2, 3, figsize=(16, 9.5), gridspec_kw={"height_ratios": [1.25, 1]})
    for col, (title, p) in enumerate(posts):
        assert M.pose(p["h"], math.radians(p["pitch_deg"]), p["dx_front"], p["dx_hind"], p["dwidth"], nominal_feet)
        r = M.lp_min_torque(MU, F_REF)
        t_peak, fs, tau = r
        d = M.d
        pw = d.xpos[M.base] + d.xmat[M.base].reshape(3, 3) @ PUSH_POINT_B
        box = base_box(M)
        q = M.joint_q()
        for row, (i, j, lab) in enumerate([(0, 2, "z (m)"), (0, 1, "y (m)")]):
            ax = axes[row, col]
            ax.axhline(0.0, color="0.5", lw=1) if row == 0 else None
            # base box outline (projection)
            hull = box[:, [i, j]]
            from scipy.spatial import ConvexHull
            hv = ConvexHull(hull).vertices
            ax.fill(hull[hv, 0], hull[hv, 1], color="#c9d6e8", ec="#3b5b8a", lw=1.5, zorder=2)
            for k, leg in enumerate(LEGS):
                c = chain(M, leg)
                near = (leg[0] == "R") if row == 0 else True
                style = dict(color="#1f3b63" if leg[1] == "F" else "#8a3b3b", lw=3 if near else 1.5,
                             alpha=1.0 if near else 0.45, zorder=4 if near else 3, marker="o", ms=4)
                ax.plot(c[:, i], c[:, j], **style)
                # foot reaction force (on the robot), green
                f = fs[k]
                ax.annotate("", xy=(c[-1, i] + f[i] * SCALE, c[-1, j] + f[j] * SCALE), xytext=(c[-1, i], c[-1, j]),
                            arrowprops=dict(arrowstyle="->", color="#2e8b57", lw=2, alpha=1.0 if near else 0.5), zorder=5)
            # push on the object at the bumper, orange
            ax.annotate("", xy=(pw[i] + F_REF * SCALE * (1 if i == 0 else 0), pw[j]), xytext=(pw[i], pw[j]),
                        arrowprops=dict(arrowstyle="->", color="#e07b00", lw=3), zorder=6)
            ax.plot(pw[i], pw[j], "o", color="#e07b00", zorder=6)
            if row == 0:  # object face, 0.60 m tall (cube / long box)
                ax.add_patch(plt.Rectangle((pw[0] + 0.005, 0.0), 0.6, 0.60, color="#f3c58a", alpha=0.5, zorder=1))
                ax.text(pw[0] + 0.05, 0.62, "object, 0.60 m tall", fontsize=8, color="#a05a00")
                com = d.subtree_com[M.base]
                ax.plot(com[0], com[2], "kx", ms=9, mew=2, zorder=7)
            ax.set_aspect("equal")
            ax.set_xlim(-0.95, 1.15)
            ax.set_ylim((-0.08, 0.85) if row == 0 else (-0.55, 0.55))
            ax.set_xlabel("x (m), forward = object")
            ax.set_ylabel(lab)
            ax.grid(alpha=0.3)
        fz = ", ".join(f"{x:.0f}" for x in fs[:, 2])
        knee = {l: math.degrees(q[f"{l}_KFE"]) for l in LEGS}
        axes[0, col].set_title(
            f"{title}\nheight {p['h']} m, pitch {p['pitch_deg']:+.0f} deg (- = nose up), feet front {p['dx_front']:+.2f} / "
            f"hind {p['dx_hind']:+.2f} m, +{p['dwidth']:.2f} m wide\n"
            f"push at z = {pw[2]:.2f} m; at {F_REF:.0f} N: peak torque {t_peak:.0f} Nm ({100 * t_peak / 80:.0f}%)\n"
            f"foot normal LF/RF/LH/RH {fz} N", fontsize=9)
        axes[1, col].set_title("top view; knee bend (deg, default 46): front " + f"{abs(knee['LF']):.0f}, hind {abs(knee['LH']):.0f}",
                               fontsize=9)
    fig.suptitle("ANYmal C press postures from the static LP (side view: near legs bold; blue = front legs, red = hind; "
                 "green = ground force on each foot, orange = 250 N push on the object, x = centre of mass)", fontsize=10)
    fig.tight_layout()
    out = ROOT / "evals/brace-lp/postures.png"
    fig.savefig(out, dpi=110)
    print(out)


if __name__ == "__main__":
    main()
