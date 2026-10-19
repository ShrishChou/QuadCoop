"""Boston Dynamics Spot (no arm) robot definition.

Geometry comes straight from MuJoCo Menagerie's ``boston_dynamics_spot/spot.xml``
(run ``scripts/fetch_assets.py`` once). ``get_spec`` edits it in code rather than
shipping a modified XML, so the diff from Menagerie is exactly what is below:

* XML actuators and the ``home`` keyframe are removed: mjlab's actuator config
  and ``INIT_STATE`` own those.
* The unnamed collision meshes get names (``body_collision``, ``fl_uleg_collision``,
  ...), so collision settings and contact sensors can address them. Unlike the
  Velocity Hub Spot, the body mesh stays collidable: the torso has to push objects.
* An IMU site, the four sensors the velocity task reads, and per-foot sites are
  added, mirroring the ANYmal C MJCF.
* Joint damping/friction loss are added (see below).

Note: Menagerie's Spot weighs 50.3 kg and its ANYmal C 45.0 kg, so in simulation
Spot is the heavier robot. The capability table is measured, not assumed.

Actuator values and joint damping follow Velocity Hub's mjlab Spot config, which
is a known-trainable starting point; they are the first thing to tune if gait
quality is poor.
"""

from __future__ import annotations

from pathlib import Path

import mujoco
from mjlab.actuator import BuiltinPositionActuatorCfg
from mjlab.entity import EntityArticulationInfoCfg, EntityCfg
from mjlab.utils.spec_config import CollisionCfg

from quadcoop.robots.spec import RobotSpec

ASSET_DIR = Path(__file__).resolve().parents[1] / "assets" / "spot"
XML = ASSET_DIR / "spot.xml"

LEGS = ("fl", "fr", "hl", "hr")
FOOT_GEOMS = ("FL", "FR", "HL", "HR")
FOOT_Z = -0.3365  # Foot sphere centre in the lower-leg frame (Menagerie value).


def get_spec() -> mujoco.MjSpec:
    if not XML.exists():
        raise FileNotFoundError(f"{XML} missing -- run `python scripts/fetch_assets.py` first.")
    spec = mujoco.MjSpec.from_file(str(XML))

    for act in list(spec.actuators):
        spec.delete(act)
    for key in list(spec.keys):
        spec.delete(key)
    for light in list(spec.lights):
        spec.delete(light)

    # Name collision meshes (group 3) after their body.
    for body in spec.bodies:
        for geom in body.geoms:
            if geom.group == 3 and not geom.name:
                geom.name = f"{body.name}_collision"

    # Joint damping/friction as in Velocity Hub's trainable Spot.
    for joint in spec.joints:
        if joint.type != mujoco.mjtJoint.mjJNT_FREE:
            joint.damping[:] = 1.0  # A 3-vector in this MuJoCo version.
            joint.frictionloss = 0.1

    base = spec.body("body")
    base.add_site(name="imu", pos=[0.0, 0.0, 0.0], group=5)
    for leg in LEGS:
        spec.body(f"{leg}_lleg").add_site(name=f"{leg}_foot", pos=[0.0, 0.0, FOOT_Z], group=5)

    site, body_obj = mujoco.mjtObj.mjOBJ_SITE, mujoco.mjtObj.mjOBJ_BODY
    spec.add_sensor(name="imu_ang_vel", type=mujoco.mjtSensor.mjSENS_GYRO,
                    objtype=site, objname="imu")
    spec.add_sensor(name="imu_lin_vel", type=mujoco.mjtSensor.mjSENS_VELOCIMETER,
                    objtype=site, objname="imu")
    spec.add_sensor(name="imu_lin_acc", type=mujoco.mjtSensor.mjSENS_ACCELEROMETER,
                    objtype=site, objname="imu")
    spec.add_sensor(name="root_angmom", type=mujoco.mjtSensor.mjSENS_SUBTREEANGMOM,
                    objtype=body_obj, objname="body")
    # Base-to-upper-leg contact excludes are already in Menagerie's MJCF.
    return spec


ACTUATOR = BuiltinPositionActuatorCfg(
    target_names_expr=(".*",),
    stiffness=500.0,
    damping=1.0,
    effort_limit=80.0,
    armature=0.05,
)

INIT_STATE = EntityCfg.InitialStateCfg(
    pos=(0.0, 0.0, 0.46),
    joint_pos={".*_hx": 0.0, ".*_hy": 1.04, ".*_kn": -1.8},
    joint_vel={".*": 0.0},
)

_FOOT_REGEX = r"^(FL|FR|HL|HR)$"

COLLISION = CollisionCfg(
    geom_names_expr=(r".*_collision$", _FOOT_REGEX),
    condim=3,
    priority=1,
    friction=(0.6,),
    solimp={_FOOT_REGEX: (0.015, 1, 0.036)},
)


def get_robot_cfg() -> EntityCfg:
    return EntityCfg(
        init_state=INIT_STATE,
        collisions=(COLLISION,),
        spec_fn=get_spec,
        articulation=EntityArticulationInfoCfg(
            actuators=(ACTUATOR,), soft_joint_pos_limit_factor=0.9
        ),
    )


ROBOT = RobotSpec(
    name="spot",
    get_robot_cfg=get_robot_cfg,
    base_body="body",
    foot_geoms=FOOT_GEOMS,
    foot_sites=tuple(f"{leg}_foot" for leg in LEGS),
    nonfoot_collision_regex=r"^(body|.*_uleg)_collision$",
    action_scale={".*": 0.25 * 80.0 / 500.0},
    pose_std_standing={".*": 0.05},
    pose_std_walking={r".*_kn": 0.15, r".*_hy": 0.3, r".*_hx": 0.3},
    # Front of Spot's body collision mesh, mid height (checked by smoke_test.py).
    push_point_b=(0.45, 0.0, 0.0),
    half_length=0.55,
    viewer_distance=2.5,
)