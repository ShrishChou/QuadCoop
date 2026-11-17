"""Spot with its arm, on RAI's released whole-body walker (docs/spot_arm.md).

Model and policy are RAI Judo's (MIT), read from a checkout (QUADCOOP_JUDO, default ~/ext/judo; not vendored):
``judo/models/xml/spot_primitive`` (12 leg + 7 arm joints, primitive collision shapes, position actuators with the
walker's training gains) and ``judo/models/policies/spot_locomotion.onnx`` (MLP 84 -> 512 -> 256 -> 128 -> 12, ELU).
``get_spec`` edits the model in code: the scene's own ground, lights, sensors and textures are removed, the visual
meshes are read from QuadCoop's copy of MuJoCo Menagerie's Spot (the same files Judo maps them to), and
the feet get the friction RAI's ground gave them (0.7; RAI's ground had priority over the robot's 0.15). Every
collision geom gets QuadCoop's robot contact priority (1, as ANYmal C and the armless Spot; RAI's was 4): the
ground (0) leaves the feet their 0.7, and a pushed object (2) sets the robot-object friction, as for the other
robots (with RAI's priority the robot's 0.15 would have overridden the object's 0.4-0.6).

``RaiWalker`` is the frozen walker (interface of judo/controller/batched_spot_locomotion.py), 50 Hz:
  command (25) = base velocity (vx, vy, wz), arm joint targets (7), leg overrides (12, 0 = walk), torso roll,
                 pitch, height (0, 0, 0.52 by default)
  obs (84)     = body-frame linear velocity, angular velocity, projected gravity, command, 19 joint positions
                 minus the default offsets and 19 joint velocities (Isaac order), previous 12 leg actions
  targets (19) = legs: action x 0.2 + default offsets; arm: command[3:10]
"""
from __future__ import annotations

import ast
import math
import os
from pathlib import Path

import mujoco
import numpy as np
import torch
from mjlab.actuator.xml_actuator import XmlActuatorCfg
from mjlab.entity import EntityArticulationInfoCfg, EntityCfg

JUDO = Path(os.environ.get("QUADCOOP_JUDO", str(Path.home() / "ext/judo"))).expanduser()
LEG_JOINTS = tuple(f"{leg}_{j}" for leg in ("fl", "fr", "hl", "hr") for j in ("hx", "hy", "kn"))
ARM_JOINTS = ("arm_sh0", "arm_sh1", "arm_el0", "arm_el1", "arm_wr0", "arm_wr1", "arm_f1x")
JOINTS = LEG_JOINTS + ARM_JOINTS
LEGS_STAND = (0.12, 0.5, -1.0, -0.12, 0.5, -1.0, 0.12, 0.5, -1.0, -0.12, 0.5, -1.0)
ARM_STOWED = (0.0, -3.11, 3.13, 1.56, 0.0, -1.56, 0.0)
ARM_OUT = (0.0, -0.9, 1.8, 0.0, -0.9, 0.0, 0.0)
STAND_HEIGHT_CMD = 0.52
FOOT_FRICTION = 0.7
MESH_DIR = Path(__file__).resolve().parents[1] / "assets" / "spot" / "assets"
CONTACT_PRIORITY = 1
# learned arm control (quadcoop/coop2/spot_arm_term.py): the six arm joints (gripper held closed)
ARM_LO = (-2.618, -3.1416, 0.0, -2.7925, -1.8326, -2.8798)
ARM_HI = (3.1416, 0.5236, 3.1416, 2.7925, 1.8326, 2.8798)
ARM_SPAN = (1.5, 2.6, -2.6, 1.5, 1.5, 1.5)  # rad per unit action from the stowed pose (+ = unfold on sh1 / el0)
ARM_BASE_BODY = "arm_link_sh0"
GRIPPER_BODY = "arm_link_fngr"
# hand-position control (spot_arm_term.py, arm "hand"): planar two-link IK of the model's arm. Body frame; sh0 yaws
# about z at the shoulder, sh1 / el0 pitch about y (pitch q points a link along (cos q, 0, -sin q)); el1 and wr1 roll
# (held 0); wr0 keeps the gripper level (wr0 = -(sh1 + el0)).
SHOULDER_B = (0.292, 0.0, 0.188)  # arm_link_sh0 in the body frame
UPPER_ARM = 0.3385  # sh1 -> el0, along the link
FOREARM = (0.4033, 0.075)  # el0 -> wrist (el1 / wr0 origin): along the link, up
WRIST_BODY = "arm_link_wr1"
HAND_OFF = (0.20, 0.0, -0.04)  # the hand point (between the closed jaws, near their front) in the wrist frame
HAND_CENTER = (0.80, 0.0, -0.05)  # hand action 0 (body frame, m): ahead of the trunk front (0.42), bumper height
HAND_SPAN = (0.25, 0.45, 0.25)  # m per unit action: x 0.55-1.05, y +-0.45, z -0.30..+0.20 (world ~0.2-0.7 m)


def hand_ik(h: torch.Tensor) -> torch.Tensor:
    """(..., 3) hand point in the body frame -> (..., 6) arm joint targets (gripper level, rolls 0), clamped to the
    joint limits; an out-of-reach target gets the reachable point on the line from the shoulder to it."""
    sx, _, sz = SHOULDER_B
    L1 = UPPER_ARM
    L2 = math.hypot(*FOREARM)
    phi2 = math.atan2(FOREARM[1], FOREARM[0])
    px, py = h[..., 0] - sx, h[..., 1]
    sh0 = torch.atan2(py, px)
    rw = torch.sqrt(px * px + py * py) - HAND_OFF[0]  # wrist, in the arm's vertical plane (gripper level)
    zw = h[..., 2] - sz - HAND_OFF[2]
    D = torch.sqrt(rw * rw + zw * zw).clamp(min=1e-6)
    Dc = D.clamp(abs(L1 - L2) + 0.05, 0.97 * (L1 + L2))
    rw, zw = rw * Dc / D, zw * Dc / D
    c = ((Dc * Dc - L1 * L1 - L2 * L2) / (2 * L1 * L2)).clamp(-1.0, 1.0)
    beta = -torch.acos(c)  # forearm below the upper arm: elbow up
    el0 = phi2 - beta
    alpha1 = torch.atan2(zw, rw) - torch.atan2(L2 * torch.sin(beta), L1 + L2 * torch.cos(beta))
    sh1 = -alpha1
    z = torch.zeros_like(sh0)
    q = torch.stack([sh0, sh1, el0, z, -(sh1 + el0), z], -1)
    lo = torch.tensor(ARM_LO, device=h.device, dtype=h.dtype)
    hi = torch.tensor(ARM_HI, device=h.device, dtype=h.dtype)
    return torch.maximum(torch.minimum(q, hi), lo)
_NAMES = ("ISAAC_TO_MUJOCO_INDICES_12", "MUJOCO_TO_ISAAC_INDICES_19", "LOCOMOTION_DEFAULT_JOINTS_OFFSET",
          "LOCOMOTION_DEFAULT_LEGS_OFFSET")


def get_spec() -> mujoco.MjSpec:
    xml = JUDO / "judo/models/xml/spot_primitive/robot.xml"
    if not xml.exists():
        raise FileNotFoundError(f"{xml} missing: clone github.com/rai-opensource/judo (branch dta/fix_for_sumo) and "
                                "set QUADCOOP_JUDO")
    spec = mujoco.MjSpec.from_file(str(xml))
    for s in list(spec.sensors):
        spec.delete(s)
    for g in list(spec.geoms):
        if g.name == "ground":
            spec.delete(g)
        elif g.type == mujoco.mjtGeom.mjGEOM_MESH:
            continue  # visual only (no contacts; every body has an explicit inertia, so no mass either)
        else:
            g.priority = CONTACT_PRIORITY
            if g.name.endswith("_foot_collision"):
                g.friction[0] = FOOT_FRICTION
    # the visual meshes are not in Judo's git: they are MuJoCo Menagerie's Spot meshes (as Judo maps them), which
    # QuadCoop already has for the armless Spot (scripts/fetch_assets.py)
    for m in spec.meshes:
        f = MESH_DIR / Path(m.file).name
        if not f.exists():
            raise FileNotFoundError(f"{f} missing -- run `python scripts/fetch_assets.py` first.")
        m.file = str(f)
    for t in list(spec.textures):
        spec.delete(t)
    for mt in spec.materials:
        mt.textures = [""] * len(mt.textures)
    for light in list(spec.lights):
        spec.delete(light)
    for s in list(spec.worldbody.sites):
        spec.delete(s)
    return spec


def get_robot_cfg(arm: tuple[float, ...] = ARM_STOWED) -> EntityCfg:
    return EntityCfg(
        init_state=EntityCfg.InitialStateCfg(
            pos=(0.0, 0.0, 0.55),
            joint_pos={**dict(zip(LEG_JOINTS, LEGS_STAND)), **dict(zip(ARM_JOINTS, arm))},
            joint_vel={".*": 0.0}),
        spec_fn=get_spec,
        articulation=EntityArticulationInfoCfg(actuators=(XmlActuatorCfg(target_names_expr=(".*",)),)),
    )


def _constants() -> dict:
    tree = ast.parse((JUDO / "judo/tasks/spot/spot_constants.py").read_text())
    out = {}
    for node in tree.body:
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            tg = node.targets[0] if isinstance(node, ast.Assign) else node.target
            if isinstance(tg, ast.Name) and tg.id in _NAMES:
                out[tg.id] = ast.literal_eval(node.value)
    assert set(out) == set(_NAMES), set(_NAMES) - set(out)
    return out


class RaiWalker:
    """The frozen walker for one Spot-arm entity (batched over envs)."""

    def __init__(self, entity, device):
        import onnx
        from onnx import numpy_helper
        assert tuple(entity.joint_names) == JOINTS, entity.joint_names
        m = onnx.load(str(JUDO / "judo/models/policies/spot_locomotion.onnx"))
        w = {t.name: torch.tensor(numpy_helper.to_array(t).copy()) for t in m.graph.initializer}
        assert [n.op_type for n in m.graph.node] == ["Gemm", "Elu"] * 3 + ["Gemm"]
        net = torch.nn.Sequential(torch.nn.Linear(84, 512), torch.nn.ELU(), torch.nn.Linear(512, 256), torch.nn.ELU(),
                                  torch.nn.Linear(256, 128), torch.nn.ELU(), torch.nn.Linear(128, 12))
        for i in (0, 2, 4, 6):
            net[i].weight.data.copy_(w[f"actor.{i}.weight"])
            net[i].bias.data.copy_(w[f"actor.{i}.bias"])
        ck = os.environ.get("QUADCOOP_SPOT_ARM_WALKER", "")  # the push-trained walker (spot_arm_walker.py)
        if ck:
            sd = torch.load(ck, map_location="cpu", weights_only=False)["actor_state_dict"]
            assert not any(k.startswith("obs_normalizer") for k in sd), "expected an actor without normalization"
            for i in (0, 2, 4, 6):
                net[i].weight.data.copy_(sd[f"mlp.{i}.weight"])
                net[i].bias.data.copy_(sd[f"mlp.{i}.bias"])
            print(f"[spot_arm] walker weights from {ck}", flush=True)
        self.net = net.to(device).eval()
        C = _constants()
        self.i2m = torch.tensor(C["ISAAC_TO_MUJOCO_INDICES_12"], device=device)
        self.m2i = torch.tensor(C["MUJOCO_TO_ISAAC_INDICES_19"], device=device)
        self.joff = torch.tensor(C["LOCOMOTION_DEFAULT_JOINTS_OFFSET"], device=device, dtype=torch.float32)
        self.loff = torch.tensor(C["LOCOMOTION_DEFAULT_LEGS_OFFSET"], device=device, dtype=torch.float32)
        self.entity = entity
        self.prev = torch.zeros(entity.data.joint_pos.shape[0], 12, device=device)

    @staticmethod
    def command(vel: torch.Tensor, arm: torch.Tensor, torso: torch.Tensor | None = None) -> torch.Tensor:
        c = torch.zeros(vel.shape[0], 25, device=vel.device)
        c[:, 0:3], c[:, 3:10] = vel, arm
        c[:, 24] = STAND_HEIGHT_CMD
        if torso is not None:
            c[:, 22:25] = torso
        return c

    def reset(self, env_ids=None) -> None:
        self.prev[slice(None) if env_ids is None else env_ids] = 0.0

    @torch.no_grad()
    def targets(self, cmd: torch.Tensor) -> torch.Tensor:
        d = self.entity.data
        obs = torch.cat([d.root_link_lin_vel_b, d.root_link_ang_vel_b, d.projected_gravity_b, cmd,
                         d.joint_pos[:, self.m2i] - self.joff, d.joint_vel[:, self.m2i], self.prev], -1)
        act = self.net(obs)
        self.prev[:] = act
        return torch.cat([act[:, self.i2m] * 0.2 + self.loff[self.i2m], cmd[:, 3:10]], -1)


def _spec():
    from quadcoop.robots.spec import RobotSpec
    return RobotSpec(
        name="spot_arm", get_robot_cfg=get_robot_cfg, base_body="body",
        foot_geoms=tuple(f"{leg}_foot_collision" for leg in ("front_left", "front_right", "rear_left", "rear_right")),
        foot_sites=(), nonfoot_collision_regex=r"^(body|.*_upper_leg|arm_.*)_collision.*$",
        action_scale={".*": 0.2}, pose_std_standing={".*": 0.05}, pose_std_walking={".*": 0.3},
        push_point_b=(0.45, 0.0, 0.0), half_length=0.55, viewer_distance=2.5,
        nominal_height=0.5,  # stands at 0.48-0.54 m under the walker (port acceptance)
    )


ROBOT = _spec()  # what the two-robot env reads: size, base body, fall height (it has no QuadCoop walker config)
