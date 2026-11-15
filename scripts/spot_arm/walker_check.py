"""Spot + arm pilot, step 1: does RAI's released whole-body walker work in plain MuJoCo, and can it push? CPU only.

    python scripts/spot_arm/walker_check.py --judo ~/ext/judo [--out evals/spot_arm/walker_check.json]

Uses RAI Judo's files read as data (MIT): the Spot + arm model (judo/models/xml/spot_primitive, visual meshes
stripped; collision is primitives) and the locomotion policy (judo/models/policies/spot_locomotion.onnx, an MLP
84 -> 512 -> 256 -> 128 -> 12, ELU), rebuilt in torch from the ONNX weights (no onnxruntime, no code from the
repo is imported or run). Interface as judo/controller/batched_spot_locomotion.py:
  obs (84) = body-frame linear velocity, angular velocity, projected gravity, command (25), 19 joint positions
             minus the default offsets (Isaac order), 19 joint velocities, previous 12 leg actions
  command (25) = base velocity (vx, vy, wz), arm joint targets (7), leg joint overrides (12, 0 = policy),
                 torso roll, pitch, height (default 0, 0, 0.52 m)
  leg targets = action x 0.2 + default leg offsets; arm targets = command[3:10]; position actuators (PD)
  50 Hz policy: timestep 0.01, 2 substeps (Judo's Spot tasks)
Tests (one env each, fixed seeds):
  tracking   stand; forward 0.5 / 1.0 m/s; lateral 0.3; turn 0.5 rad/s; arm stowed and arm out (RAI's unstowed
             pose), and forward 0.5 with the arm sweeping: achieved vs commanded velocity over the last 3 s, falls
  push       a 0.6 m cube (20 / 40 kg, friction 0.5) 1.2 m ahead; walk at 0.5 m/s for 10 s, arm stowed vs out;
             box displacement along the walking direction, its yaw change, the robot's contact with it, falls
"""
from __future__ import annotations

import argparse
import ast
import json
import math
from pathlib import Path

import mujoco
import numpy as np
import onnx
import torch
from onnx import numpy_helper

NAMES = ("ISAAC_TO_MUJOCO_INDICES_12", "MUJOCO_TO_ISAAC_INDICES_19", "LOCOMOTION_DEFAULT_JOINTS_OFFSET",
         "LOCOMOTION_DEFAULT_LEGS_OFFSET", "GRIPPER_CLOSED_POS")


def constants(judo: Path) -> dict:
    """Literal constants from judo/tasks/spot/spot_constants.py, parsed (never executed)."""
    tree = ast.parse((judo / "judo/tasks/spot/spot_constants.py").read_text())
    out = {}
    for node in tree.body:
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            tg = node.targets[0] if isinstance(node, ast.Assign) else node.target
            if isinstance(tg, ast.Name) and tg.id in NAMES:
                out[tg.id] = ast.literal_eval(node.value)
    missing = set(NAMES) - set(out)
    assert not missing, missing
    g = out["GRIPPER_CLOSED_POS"]
    out["LEGS_STAND"] = np.array([0.12, 0.5, -1.0, -0.12, 0.5, -1.0, 0.12, 0.5, -1.0, -0.12, 0.5, -1.0])
    out["ARM_STOWED"] = np.array([0, -3.11, 3.13, 1.56, 0, -1.56, g])
    out["ARM_OUT"] = np.array([0, -0.9, 1.8, 0, -0.9, 0, g])
    return out


def policy(judo: Path) -> torch.nn.Module:
    m = onnx.load(str(judo / "judo/models/policies/spot_locomotion.onnx"))
    w = {t.name: torch.tensor(numpy_helper.to_array(t).copy()) for t in m.graph.initializer}
    assert [n.op_type for n in m.graph.node] == ["Gemm", "Elu"] * 3 + ["Gemm"]
    net = torch.nn.Sequential(torch.nn.Linear(84, 512), torch.nn.ELU(), torch.nn.Linear(512, 256), torch.nn.ELU(),
                              torch.nn.Linear(256, 128), torch.nn.ELU(), torch.nn.Linear(128, 12))
    for i in (0, 2, 4, 6):
        net[i].weight.data.copy_(w[f"actor.{i}.weight"])
        net[i].bias.data.copy_(w[f"actor.{i}.bias"])
    return net.eval()


def model(judo: Path, box_mass: float | None) -> mujoco.MjModel:
    spec = mujoco.MjSpec.from_file(str(judo / "judo/models/xml/spot_primitive/robot.xml"))
    for gm in list(spec.geoms):
        if gm.type == mujoco.mjtGeom.mjGEOM_MESH:
            spec.delete(gm)
    for ms in list(spec.meshes):
        spec.delete(ms)
    for tx in list(spec.textures):
        if tx.file:
            spec.delete(tx)
    for mt in spec.materials:  # textures removed above may be referenced
        mt.textures = [""] * len(mt.textures)
    if box_mass is not None:
        b = spec.worldbody.add_body(name="box", pos=[1.2 + 0.3, 0, 0.3])
        b.add_freejoint(name="box_free")
        b.add_geom(name="box_geom", type=mujoco.mjtGeom.mjGEOM_BOX, size=[0.3, 0.3, 0.3], mass=box_mass,
                   friction=[0.5, 0.005, 0.0001], priority=6, rgba=[0.8, 0.5, 0.2, 1])  # priority above the ground's (5,
        # friction 0.7) and the robot's (4, 0.15): the box's 0.5 applies to both of its contacts
    return spec.compile()


class Walker:
    def __init__(self, m: mujoco.MjModel, net, C: dict, arm: np.ndarray):
        self.m, self.net, self.C = m, net, C
        self.d = mujoco.MjData(m)
        self.i2m = np.array(C["ISAAC_TO_MUJOCO_INDICES_12"])
        self.m2i = np.array(C["MUJOCO_TO_ISAAC_INDICES_19"])
        self.joff = np.array(C["LOCOMOTION_DEFAULT_JOINTS_OFFSET"], dtype=np.float64)
        self.loff = np.array(C["LOCOMOTION_DEFAULT_LEGS_OFFSET"], dtype=np.float64)
        jn = [m.joint(i).name for i in range(m.njnt)]
        assert jn[0] == "base" and jn[1:20] == ["fl_hx", "fl_hy", "fl_kn", "fr_hx", "fr_hy", "fr_kn", "hl_hx", "hl_hy",
                                                "hl_kn", "hr_hx", "hr_hy", "hr_kn", "arm_sh0", "arm_sh1", "arm_el0",
                                                "arm_el1", "arm_wr0", "arm_wr1", "arm_f1x"], jn
        assert m.nu == 19 and abs(m.opt.timestep - 0.01) < 1e-9
        self.d.qpos[2] = 0.55
        self.d.qpos[7:19] = C["LEGS_STAND"]
        self.d.qpos[19:26] = arm
        self.prev = np.zeros(12)
        self.ctrl = np.concatenate([C["LEGS_STAND"], arm])
        mujoco.mj_forward(m, self.d)

    def obs(self, cmd: np.ndarray) -> np.ndarray:
        q, v = self.d.qpos, self.d.qvel
        R = np.zeros(9)
        mujoco.mju_quat2Mat(R, q[3:7])
        R = R.reshape(3, 3)
        return np.concatenate([R.T @ v[0:3], v[3:6], R.T @ np.array([0, 0, -1.0]), cmd,
                               q[7 + self.m2i] - self.joff, v[6 + self.m2i], self.prev]).astype(np.float32)

    def step(self, cmd: np.ndarray) -> None:
        with torch.no_grad():
            act = self.net(torch.from_numpy(self.obs(cmd))[None])[0].numpy().astype(np.float64)
        tgt = np.zeros(19)
        tgt[:12] = act[self.i2m] * 0.2 + self.loff[self.i2m]
        tgt[12:] = cmd[3:10]
        self.prev = act
        self.d.ctrl[:] = tgt
        for _ in range(2):
            mujoco.mj_step(self.m, self.d)

    def fallen(self) -> bool:
        R = np.zeros(9)
        mujoco.mju_quat2Mat(R, self.d.qpos[3:7])
        return bool(self.d.qpos[2] < 0.25 or R.reshape(3, 3)[2, 2] < 0.5)

    def body_vel(self) -> np.ndarray:
        R = np.zeros(9)
        mujoco.mju_quat2Mat(R, self.d.qpos[3:7])
        lv = R.reshape(3, 3).T @ self.d.qvel[0:3]
        return np.array([lv[0], lv[1], self.d.qvel[5]])


def command(vel, arm) -> np.ndarray:
    c = np.zeros(25)
    c[0:3] = vel
    c[3:10] = arm
    c[24] = 0.52  # torso (roll, pitch, height): Judo's default command stands at STANDING_HEIGHT_CMD = 0.52 m
    return c


def tracking(m, net, C) -> list[dict]:
    rows = []
    cases = [("stand", (0, 0, 0)), ("forward 0.5", (0.5, 0, 0)), ("forward 1.0", (1.0, 0, 0)),
             ("lateral 0.3", (0, 0.3, 0)), ("turn 0.5", (0, 0, 0.5))]
    for arm_name in ("stowed", "out"):
        arm = C["ARM_STOWED"] if arm_name == "stowed" else C["ARM_OUT"]
        for name, vel in cases + ([("forward 0.5, arm sweeping", (0.5, 0, 0))] if arm_name == "out" else []):
            w = Walker(m, net, C, arm)
            got, fell_at = [], None
            for k in range(400):  # 8 s at 50 Hz: 1 s standing, then the command
                t = k * 0.02
                a = arm.copy()
                if "sweeping" in name:
                    a[0] = 0.8 * math.sin(2 * math.pi * 0.25 * t)  # shoulder yaw +-0.8 rad at 0.25 Hz
                    a[1] = -0.9 + 0.4 * math.sin(2 * math.pi * 0.2 * t)
                w.step(command(vel if t >= 1.0 else (0, 0, 0), a))
                if fell_at is None and w.fallen():
                    fell_at = round(t, 2)
                if t >= 5.0:
                    got.append(w.body_vel())
            g = np.mean(got, 0)
            rows.append({"arm": arm_name, "case": name, "cmd": list(vel), "achieved": [round(float(x), 3) for x in g],
                         "error": round(float(np.linalg.norm(g - np.array(vel))), 3), "fell_at": fell_at,
                         "height": round(float(w.d.qpos[2]), 3)})
    return rows


def push(judo, net, C) -> list[dict]:
    rows = []
    for mass in (20.0, 40.0):
        m = model(judo, mass)
        gid = mujoco.mj_name2id(m, mujoco.mjtObj.mjOBJ_GEOM, "box_geom")
        bid = mujoco.mj_name2id(m, mujoco.mjtObj.mjOBJ_BODY, "box")
        robot_geoms = {i for i in range(m.ngeom) if m.geom_bodyid[i] not in (0, bid)}
        arm_bodies = {i for i in range(m.nbody) if m.body(i).name.startswith("arm")}
        for arm_name in ("stowed", "out"):
            arm = C["ARM_STOWED"] if arm_name == "stowed" else C["ARM_OUT"]
            w = Walker(m, net, C, arm)
            p0 = w.d.xpos[bid].copy()
            y0 = math.atan2(w.d.xmat[bid][3], w.d.xmat[bid][0])
            touch = arm_touch = 0
            fell_at = None
            for k in range(550):  # 1 s stand, 10 s walk at 0.5 m/s
                t = k * 0.02
                w.step(command((0.5, 0, 0) if t >= 1.0 else (0, 0, 0), arm))
                if fell_at is None and w.fallen():
                    fell_at = round(t, 2)
                hit = arm_hit = False
                for c in w.d.contact[: w.d.ncon]:
                    pair = {c.geom1, c.geom2}
                    if gid in pair and (pair - {gid}) & robot_geoms:
                        hit = True
                        other = (pair - {gid}).pop()
                        arm_hit |= int(m.geom_bodyid[other]) in arm_bodies
                touch += hit
                arm_touch += arm_hit
            dp = w.d.xpos[bid] - p0
            y1 = math.atan2(w.d.xmat[bid][3], w.d.xmat[bid][0])
            rows.append({"mass": mass, "arm": arm_name, "box_dx": round(float(dp[0]), 3), "box_dy": round(float(dp[1]), 3),
                         "box_dyaw_deg": round(math.degrees(math.atan2(math.sin(y1 - y0), math.cos(y1 - y0))), 1),
                         "contact_s": round(touch * 0.02, 2), "arm_contact_s": round(arm_touch * 0.02, 2),
                         "fell_at": fell_at, "robot_x": round(float(w.d.qpos[0]), 3)})
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--judo", default=str(Path.home() / "ext/judo"))
    ap.add_argument("--out", default="evals/spot_arm/walker_check.json")
    a = ap.parse_args()
    judo = Path(a.judo).expanduser()
    torch.manual_seed(0)
    C, net = constants(judo), policy(judo)
    rep = {"tracking": tracking(model(judo, None), net, C), "push": push(judo, net, C)}
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(rep, indent=1))
    for r in rep["tracking"]:
        print(f"track  arm {r['arm']:6s} {r['case']:26s} cmd {r['cmd']} got {r['achieved']} err {r['error']:.3f} "
              f"fell {r['fell_at']} h {r['height']}")
    for r in rep["push"]:
        print(f"push   {r['mass']:3.0f} kg arm {r['arm']:6s} box dx {r['box_dx']:+.2f} dy {r['box_dy']:+.2f} dyaw "
              f"{r['box_dyaw_deg']:+.1f} | contact {r['contact_s']:.1f} s (arm {r['arm_contact_s']:.1f} s) fell "
              f"{r['fell_at']} robot x {r['robot_x']:.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
