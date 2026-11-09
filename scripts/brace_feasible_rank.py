"""Re-rank evals/brace-lp postures with the feasibility limits the static LP ignored.

  push height  the bumper point (base frame (0.50, 0, 0)) at most 0.50 m: objects are 0.60 m tall, and a
               push near the top edge rides over it or tips it (a 0.6 m cube at mu 0.45 tips above ~0.67 m)
  knees bent   every knee at least 30 deg from straight (default stance: 46 deg): a straight-leg strut
               holds force cheaply but cannot absorb a slip or step out
  friction use the min-torque solution's worst foot |f_xy| / (mu f_z) at 250 N, foot mu 0.8 (reported)
Output: evals/brace-lp/feasible.md, feasible.json (the pick is drawn by draw_brace_postures.py).
"""
import json, math, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))
from brace_posture_search import LEGS, PUSH_POINT_B, Model

ROOT = Path(__file__).resolve().parents[1]
H_MAX, KNEE_MIN, F, MU = 0.50, 30.0, 250.0, 0.8
lp = json.loads((ROOT / "evals/brace-lp/summary.json").read_text())
M = Model(); nom = M.nominal_feet()
out = []
for r in lp["rows"]:
    if r.get("tau_peak_ref") is None:
        continue
    M.pose(r["h"], math.radians(r["pitch_deg"]), r["dx_front"], r["dx_hind"], r["dwidth"], nom)
    d = M.d
    pz = float((d.xpos[M.base] + d.xmat[M.base].reshape(3, 3) @ PUSH_POINT_B)[2])
    q = M.joint_q()
    knee = min(abs(math.degrees(q[f"{l}_KFE"])) for l in LEGS)
    s = M.lp_min_torque(MU, F)
    fu = float(max(np.linalg.norm(f[:2]) / (MU * f[2]) for f in s[1])) if s else None
    out.append({**r, "push_z": round(pz, 3), "knee_min_deg": round(knee, 1), "friction_use": None if fu is None else round(fu, 2)})
ok = sorted([r for r in out if r["push_z"] <= H_MAX and r["knee_min_deg"] >= KNEE_MIN], key=lambda r: r["tau_peak_ref"])
nomr = next(r for r in out if r["dx_front"] == 0 and r["dx_hind"] == 0 and r["dwidth"] == 0 and r["pitch_deg"] == 0 and r["h"] == 0.53)
md = ["# Feasible press postures: evals/brace-lp/feasible.md", "",
      f"Limits: push point <= {H_MAX} m (objects 0.60 m tall), every knee >= {KNEE_MIN} deg bent (default 46). "
      f"{len(ok)} of {len(out)} postures pass. Torque = smallest peak joint torque holding {F:.0f} N (foot mu {MU}); "
      "friction use = worst foot |f_xy| / (mu f_z) in that solution (1 = at the slip limit).", "",
      "| posture | height | pitch (deg) | front dx | hind dx | wider | push z (m) | min knee (deg) | peak torque (Nm) | friction use |",
      "|---|---|---|---|---|---|---|---|---|---|"]
for name, r in [("nominal", nomr)] + [(f"#{i+1}", r) for i, r in enumerate(ok[:10])]:
    md.append(f"| {name} | {r['h']} | {r['pitch_deg']:+.0f} | {r['dx_front']:+.2f} | {r['dx_hind']:+.2f} | {r['dwidth']} | "
              f"{r['push_z']} | {r['knee_min_deg']} | {r['tau_peak_ref']:.0f} | {r['friction_use']} |")
(ROOT / "evals/brace-lp/feasible.md").write_text("\n".join(md) + "\n")
(ROOT / "evals/brace-lp/feasible.json").write_text(json.dumps({"pick": ok[0] if ok else None, "top": ok[:20], "nominal": nomr}, indent=1))
print("\n".join(md))
