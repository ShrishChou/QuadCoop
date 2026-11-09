"""Does the training contact model let a loaded foot creep? No robot: a 45 kg block (ANYmal C's mass) on
four 3 cm sphere feet, foot friction 0.8, pushed horizontally at a share of the friction limit mu m g for
3 s. A rigid Coulomb contact would not move below share 1. Variants: the walker env's settings (foot solimp
(0.015, 1, 0.03) from robots/anymal_c.py, pyramidal cone, impratio 1 - mjlab defaults) against MuJoCo
default solimp, impratio 10, and the elliptic cone. Output: evals/contact-creep/summary.md
"""
import itertools, sys
from pathlib import Path
import mujoco, numpy as np
ROOT = Path(__file__).resolve().parents[1]

def run(solimp, cone, impratio, share, mu=0.8, mass=45.0, dt=0.005, T=3.0):
    feet = "".join(f'<geom type="sphere" size="0.03" pos="{x} {y} -0.25" friction="{mu} 0.005 0.0001" priority="1" '
                   f'condim="3" solimp="{" ".join(map(str, solimp))}"/>' for x in (-0.45, 0.45) for y in (-0.3, 0.3))
    xml = f"""<mujoco><option timestep="{dt}" integrator="implicitfast" cone="{cone}" impratio="{impratio}"/>
    <worldbody><geom type="plane" size="10 10 .1" friction="1 0.005 0.0001"/>
    <body pos="0 0 0.28"><freejoint/><geom type="box" size="0.3 0.1 0.05" mass="{mass}" contype="0" conaffinity="0"/>{feet}</body>
    </worldbody></mujoco>"""
    m = mujoco.MjModel.from_xml_string(xml); d = mujoco.MjData(m)
    for _ in range(int(1.0 / dt)):
        mujoco.mj_step(m, d)
    x0, z0 = d.qpos[0], d.qpos[2]
    F = share * mu * mass * 9.81
    for _ in range(int(T / dt)):
        d.xfrc_applied[1, 0] = F
        mujoco.mj_step(m, d)
    return (d.qpos[0] - x0) / T, 0.28 - z0  # creep speed, sink (m): foot bottoms touch at body z 0.28

variants = [("walker env: solimp (0.015,1,0.03), pyramidal, impratio 1", (0.015, 1, 0.03), "pyramidal", 1),
            ("same, impratio 10", (0.015, 1, 0.03), "pyramidal", 10),
            ("same, elliptic, impratio 10", (0.015, 1, 0.03), "elliptic", 10),
            ("MuJoCo default solimp (0.9,0.95,0.001), pyramidal, impratio 1", (0.9, 0.95, 0.001), "pyramidal", 1),
            ("default solimp, elliptic, impratio 10", (0.9, 0.95, 0.001), "elliptic", 10)]
shares = (0.1, 0.5, 0.9, 1.1, 1.5)
md = ["# Contact creep test: evals/contact-creep", "", "45 kg block on four 3 cm sphere feet, foot friction 0.8, "
      "a steady horizontal push at a share of mu m g (353 N) for 3 s after settling. Creep = mean sliding speed "
      "(a rigid Coulomb contact: 0 below share 1, sliding above it). Sink = foot penetration at rest.", "",
      "| contact settings | sink (mm) | " + " | ".join(f"push {s:.0%} of the limit ({s * 0.8 * 45 * 9.81:.0f} N): creep mm/s" for s in shares) + " |",
      "|---|---|" + "---|" * len(shares)]
for name, si, cone, ir in variants:
    res = [run(si, cone, ir, s) for s in shares]
    md.append(f"| {name} | {1000 * res[0][1]:.1f} | " + " | ".join(f"{1000 * v:.1f}" for v, _ in res) + " |")
out = ROOT / "evals/contact-creep"; out.mkdir(parents=True, exist_ok=True)
(out / "summary.md").write_text("\n".join(md) + "\n"); print("\n".join(md))
