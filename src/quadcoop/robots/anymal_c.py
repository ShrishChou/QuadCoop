"""ANYmal C robot definition.

Model and actuator values follow mujocolab/anymal_c_velocity (the official mjlab
custom-robot example), whose MJCF is Menagerie's ANYmal C with named collision
geoms, an IMU site and the sensors the velocity task reads. Run
``scripts/fetch_assets.py`` once to copy that MJCF into ``assets/anymal_c``.

Nothing here is ANYmal-specific beyond names and numbers: ``ROBOT`` is the single
object the walker env config reads.
"""

from __future__ import annotations

from pathlib import Path

import mujoco
from mjlab.actuator import BuiltinPositionActuatorCfg
from mjlab.entity import EntityArticulationInfoCfg, EntityCfg
from mjlab.utils.spec_config import CollisionCfg

from quadcoop.robots.spec import RobotSpec

ASSET_DIR = Path(__file__).resolve().parents[1] / "assets" / "anymal_c"
XML = ASSET_DIR / "anymal_c.xml"


def get_spec() -> mujoco.MjSpec:
    if not XML.exists():
        raise FileNotFoundError(f"{XML} missing -- run `python scripts/fetch_assets.py` first.")
    # meshdir="assets" in the MJCF resolves relative to the file.
    return mujoco.MjSpec.from_file(str(XML))


# Actuators: values from the anymal_c_velocity example (10 Hz natural frequency).
_EFFORT = 80.0
_ARMATURE = 0.005
_OMEGA = 10 * 2.0 * 3.1415926535
_STIFFNESS = _ARMATURE * _OMEGA**2
_DAMPING = 2 * 2.0 * _ARMATURE * _OMEGA

ACTUATOR = BuiltinPositionActuatorCfg(
    target_names_expr=(".*HAA", ".*HFE", ".*KFE"),
    stiffness=_STIFFNESS,
    damping=_DAMPING,
    effort_limit=_EFFORT,
    armature=_ARMATURE,
)

INIT_STATE = EntityCfg.InitialStateCfg(
    pos=(0.0, 0.0, 0.54),
    joint_pos={
        ".*HAA": 0.0,
        "LF_HFE": 0.4,
        "RF_HFE": 0.4,
        "LH_HFE": -0.4,
        "RH_HFE": -0.4,
        "LF_KFE": -0.8,
        "RF_KFE": -0.8,
        "LH_KFE": 0.8,
        "RH_KFE": 0.8,
    },
    joint_vel={".*": 0.0},
)

FOOT_GEOMS = ("LF_foot", "RF_foot", "LH_foot", "RH_foot")
_FOOT_REGEX = r"^[LR][FH]_foot$"

# Every named collision geom collides (body included), so the torso can push
# objects. Self-collision between base and thighs is excluded in the MJCF.
COLLISION = CollisionCfg(
    geom_names_expr=(r".*_collision\d*$", _FOOT_REGEX),
    condim=3,
    priority=1,
    friction=(0.6,),
    solimp={_FOOT_REGEX: (0.015, 1, 0.03)},
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
    name="anymal_c",
    get_robot_cfg=get_robot_cfg,
    base_body="base",
    foot_geoms=FOOT_GEOMS,
    foot_sites=("LF", "RF", "LH", "RH"),
    nonfoot_collision_regex=r".*_collision\d*$",
    action_scale={n: 0.25 * _EFFORT / _STIFFNESS for n in ACTUATOR.target_names_expr},
    pose_std_standing={".*HAA": 0.05, ".*HFE": 0.05, ".*KFE": 0.1},
    pose_std_walking={".*HAA": 0.3, ".*HFE": 0.3, ".*KFE": 0.6},
    # Front bumper (base_collision5 reaches x = 0.52 m) at mid height: where a
    # push on the object lands, so the disturbance torque matches real pushing.
    push_point_b=(0.50, 0.0, 0.0),
    # Base half-length incl. bumpers, used to place boxes clear of the robot.
    half_length=0.55,
    viewer_distance=2.0,
)
