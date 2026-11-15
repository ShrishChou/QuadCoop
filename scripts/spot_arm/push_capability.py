"""Spot + arm pilot, step 2 (CPU): can RAI's frozen walker push a heavy box with ANY constant command?

    python scripts/spot_arm/push_capability.py --judo ~/ext/judo [--samples 150] [--workers 8]

Decides the fork in docs/spot_arm.md: if some arm / torso / speed command moves 40-60 kg, a pusher policy over
those commands is worth training on the frozen walker; if nothing does, the walker itself needs push fine-tuning.
Per mass (20, 40, 60 kg; 0.6 m cube, friction 0.5, 1.2 m ahead): --samples random constant commands held for 10 s
after 1 s standing, plus the two fixed baselines (0.5 m/s, arm stowed / out):
  forward speed 0.3-1.2 m/s, torso pitch +-0.3 rad, torso height 0.35-0.55 m,
  arm shoulder yaw +-0.4, shoulder pitch -2.6..-0.3, elbow 0.5..2.9, wrist pitch -1.5..0.8 (gripper closed)
Reported: box travel along the walking direction, its yaw change, falls. One seed; plain MuJoCo, not MuJoCo Warp.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from multiprocessing import Pool
from pathlib import Path

import mujoco
import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import walker_check as wc  # noqa: E402

_S = {}


def _init(judo):
    torch.set_num_threads(1)
    j = Path(judo)
    _S.update(judo=j, C=wc.constants(j), net=wc.policy(j), models={})


def rollout(job):
    mass, p = job
    if mass not in _S["models"]:
        _S["models"][mass] = wc.model(_S["judo"], mass)
    m, C = _S["models"][mass], _S["C"]
    bid = mujoco.mj_name2id(m, mujoco.mjtObj.mjOBJ_BODY, "box")
    arm = np.array(p["arm"])
    w = wc.Walker(m, _S["net"], C, C["ARM_STOWED"])
    p0 = w.d.xpos[bid].copy()
    y0 = math.atan2(w.d.xmat[bid][3], w.d.xmat[bid][0])
    fell = None
    for k in range(550):
        t = k * 0.02
        c = wc.command((p["vx"], 0, 0) if t >= 1.0 else (0, 0, 0), arm if t >= 0.5 else C["ARM_STOWED"])
        if t >= 1.0:
            c[23], c[24] = p["pitch"], p["height"]
        w.step(c)
        if fell is None and w.fallen():
            fell = round(t, 2)
            break
    y1 = math.atan2(w.d.xmat[bid][3], w.d.xmat[bid][0])
    return {"mass": mass, **p, "box_dx": round(float(w.d.xpos[bid][0] - p0[0]), 3),
            "box_dyaw_deg": round(math.degrees(math.atan2(math.sin(y1 - y0), math.cos(y1 - y0))), 1), "fell_at": fell}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--judo", default=str(Path.home() / "ext/judo"))
    ap.add_argument("--samples", type=int, default=150)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--out", default="evals/spot_arm/push_capability.json")
    a = ap.parse_args()
    C = wc.constants(Path(a.judo).expanduser())
    rng = np.random.default_rng(0)
    g = float(C["ARM_STOWED"][6])
    base = [{"name": "stowed 0.5", "vx": 0.5, "pitch": 0.0, "height": 0.52, "arm": C["ARM_STOWED"].tolist()},
            {"name": "out 0.5", "vx": 0.5, "pitch": 0.0, "height": 0.52, "arm": C["ARM_OUT"].tolist()}]
    rand = [{"name": f"r{i}", "vx": float(rng.uniform(0.3, 1.2)), "pitch": float(rng.uniform(-0.3, 0.3)),
             "height": float(rng.uniform(0.35, 0.55)),
             "arm": [float(rng.uniform(-0.4, 0.4)), float(rng.uniform(-2.6, -0.3)), float(rng.uniform(0.5, 2.9)), 0.0,
                     float(rng.uniform(-1.5, 0.8)), 0.0, g]} for i in range(a.samples)]
    jobs = [(m, p) for m in (20.0, 40.0, 60.0) for p in base + rand]
    with Pool(a.workers, initializer=_init, initargs=(str(Path(a.judo).expanduser()),)) as pool:
        rows = pool.map(rollout, jobs, chunksize=4)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(rows, indent=1))
    for mass in (20.0, 40.0, 60.0):
        R = [r for r in rows if r["mass"] == mass]
        ok = sorted([r for r in R if r["fell_at"] is None and not r["name"].startswith(("stowed", "out"))],
                    key=lambda r: -r["box_dx"])
        b = {r["name"]: r for r in R if r["name"] in ("stowed 0.5", "out 0.5")}
        dx = [r["box_dx"] for r in ok]
        print(f"{mass:.0f} kg: baselines stowed {b['stowed 0.5']['box_dx']:+.2f} m, arm out {b['out 0.5']['box_dx']:+.2f} m | "
              f"random commands: {len(R) - 2 - len(ok)}/{len(R) - 2} fell; of the rest, box travel median "
              f"{np.median(dx):.2f} m, best {dx[0]:.2f} m; moved > 1 m: {sum(x > 1 for x in dx)}, > 2 m: {sum(x > 2 for x in dx)}")
        for r in ok[:3]:
            print(f"    {r['box_dx']:+.2f} m, yaw {r['box_dyaw_deg']:+.0f} deg: vx {r['vx']:.2f}, pitch {r['pitch']:+.2f}, "
                  f"height {r['height']:.2f}, arm {[round(x, 2) for x in r['arm'][:5]]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
