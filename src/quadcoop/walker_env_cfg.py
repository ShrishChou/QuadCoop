"""Stage 0 walker: track (vx, vy, wz) while something pushes back.

Built on mjlab's ``make_velocity_env_cfg()`` with the same flat-ground edits as
mjlab's Unitree Go1 flat task, then three additions:

1. ``push_force`` command: sustained horizontal resistance at the front of the
   body (``mdp/push_force.py``). Privileged: in the critic, not the actor.
2. A free ``box`` entity dropped in the robot's path in a fraction of resets and
   again every few seconds (``mdp/box_events.py``), for real contact.
3. A command mix tilted toward what pushing needs: more standing envs (bracing),
   and a speed curriculum capped at 1.5 m/s instead of 3 m/s.

The actor observation is exactly the stock velocity task's (IMU, gravity, joints,
last action, command), so the frozen walker drops into later stages unchanged.

Env-var knobs (read when the config is built, i.e. at ``train.py`` start):

* ``QUADCOOP_PUSH_FORCE``   1/0 -- force field on (default) / off (ablation)
* ``QUADCOOP_PUSH_MAX_FRAC`` peak force as fraction of robot weight (default 0.4)
* ``QUADCOOP_PUSH_START``   curriculum start intensity (default 0.2)
* ``QUADCOOP_PUSH_ITERS``   iterations to reach full intensity (default 2000)
* ``QUADCOOP_BOX_PROB``     fraction of placements that put the box in the path (0.3)
* ``QUADCOOP_BOX_MASS``     "lo,hi" box mass range in kg (default "3,30")
"""

from __future__ import annotations

import math
import os

from mjlab.envs import ManagerBasedRlEnvCfg
from mjlab.envs import mdp as envs_mdp
from mjlab.envs.mdp.actions import JointPositionActionCfg
from mjlab.managers.event_manager import EventTermCfg
from mjlab.managers.observation_manager import ObservationTermCfg
from mjlab.managers.scene_entity_config import SceneEntityCfg
from mjlab.managers.termination_manager import TerminationTermCfg
from mjlab.sensor import (
    ContactMatch,
    ContactSensorCfg,
    ObjRef,
    RingPatternCfg,
    TerrainHeightSensorCfg,
)
from mjlab.tasks.velocity import mdp
from mjlab.tasks.velocity.mdp import UniformVelocityCommandCfg
from mjlab.tasks.velocity.velocity_env_cfg import make_velocity_env_cfg

from quadcoop.mdp.box_events import place_box_in_path
from quadcoop.mdp.push_force import PushForceCommandCfg, push_force_enabled
from quadcoop.robots.box import BOX_HALF_SIZE, BOX_NOMINAL_MASS, get_box_cfg
from quadcoop.robots.spec import RobotSpec


def _env_float(name: str, default: float) -> float:
    return float(os.environ.get(name, str(default)))


def _box_mass_alpha_range() -> tuple[float, float]:
    """pseudo_inertia scales mass by exp(2*alpha); convert a kg range to alpha."""
    lo, hi = (float(x) for x in os.environ.get("QUADCOOP_BOX_MASS", "3,30").split(","))
    return (0.5 * math.log(lo / BOX_NOMINAL_MASS), 0.5 * math.log(hi / BOX_NOMINAL_MASS))


def make_walker_env_cfg(robot: RobotSpec, play: bool = False) -> ManagerBasedRlEnvCfg:
    cfg = make_velocity_env_cfg()

    # -- simulation: flat ground, two entities with contacts ------------------
    cfg.sim.njmax = 600
    cfg.sim.nconmax = None
    cfg.sim.mujoco.ccd_iterations = 50
    cfg.sim.contact_sensor_maxmatch = 64

    assert cfg.scene.terrain is not None
    cfg.scene.terrain.terrain_type = "plane"
    cfg.scene.terrain.terrain_generator = None
    cfg.scene.entities = {"robot": robot.get_robot_cfg(), "box": get_box_cfg()}

    # -- sensors ----------------------------------------------------------------
    sensors = []
    for sensor in cfg.scene.sensors or ():
        if sensor.name == "terrain_scan":
            continue  # No terrain to scan.
        if sensor.name == "foot_height_scan":
            assert isinstance(sensor, TerrainHeightSensorCfg)
            sensor.frame = tuple(
                ObjRef(type="site", name=s, entity="robot") for s in robot.foot_sites
            )
            sensor.pattern = RingPatternCfg.single_ring(radius=0.04, num_samples=4)
        sensors.append(sensor)
    sensors.append(
        ContactSensorCfg(
            name="feet_ground_contact",
            primary=ContactMatch(mode="geom", pattern=robot.foot_geoms, entity="robot"),
            secondary=ContactMatch(mode="body", pattern="terrain"),
            fields=("found", "force"),
            reduce="netforce",
            num_slots=1,
            track_air_time=True,
        )
    )
    cfg.scene.sensors = tuple(sensors)
    for group in ("actor", "critic"):
        cfg.observations[group].terms.pop("height_scan", None)

    # -- robot-specific names and scales ---------------------------------------
    joint_pos_action = cfg.actions["joint_pos"]
    assert isinstance(joint_pos_action, JointPositionActionCfg)
    joint_pos_action.scale = robot.action_scale

    cfg.events["foot_friction"].params["asset_cfg"].geom_names = robot.foot_geoms
    cfg.events["base_com"].params["asset_cfg"].body_names = (robot.base_body,)

    pose = cfg.rewards["pose"].params
    pose["std_standing"] = dict(robot.pose_std_standing)
    pose["std_walking"] = dict(robot.pose_std_walking)
    pose["std_running"] = dict(robot.pose_std_walking)
    cfg.rewards["upright"].params["asset_cfg"].body_names = (robot.base_body,)
    cfg.rewards["upright"].params.pop("terrain_sensor_names", None)
    cfg.rewards["body_ang_vel"].params["asset_cfg"].body_names = (robot.base_body,)
    for name in ("foot_clearance", "foot_slip"):
        cfg.rewards[name].params["asset_cfg"].site_names = robot.foot_sites
    cfg.rewards["body_ang_vel"].weight = 0.0
    cfg.rewards["angular_momentum"].weight = 0.0
    cfg.rewards["air_time"].weight = 0.0

    # -- terminations: flat ground, so a bad orientation is a fall -------------
    cfg.terminations.pop("out_of_terrain_bounds", None)
    cfg.terminations.pop("illegal_contact", None)
    cfg.terminations["fell_over"] = TerminationTermCfg(
        func=mdp.bad_orientation, params={"limit_angle": math.radians(70.0)}
    )

    # -- commands: more bracing, no sprinting ------------------------------------
    twist = cfg.commands["twist"]
    assert isinstance(twist, UniformVelocityCommandCfg)
    twist.rel_standing_envs = 0.15
    twist.viz.z_offset = 0.6
    cfg.curriculum.pop("terrain_levels", None)
    cfg.curriculum["command_vel"].params["velocity_stages"] = [
        {"step": 0, "lin_vel_x": (-1.0, 1.0), "ang_vel_z": (-0.5, 0.5)},
        {"step": 3000 * 24, "lin_vel_x": (-1.0, 1.5), "ang_vel_z": (-0.7, 0.7)},
    ]

    # -- sustained push resistance (privileged) ---------------------------------
    if push_force_enabled():
        cfg.commands["push_force"] = PushForceCommandCfg(
            resampling_time_range=(1e9, 1e9),  # Schedule is internal.
            body_name=robot.base_body,
            push_point_b=robot.push_point_b,
            max_frac_of_weight=_env_float("QUADCOOP_PUSH_MAX_FRAC", 0.4),
            curriculum_start_scale=_env_float("QUADCOOP_PUSH_START", 0.2),
            curriculum_env_steps=_env_float("QUADCOOP_PUSH_ITERS", 2000) * 24,
        )
        cfg.observations["critic"].terms["push_force"] = ObservationTermCfg(
            func=envs_mdp.generated_commands, params={"command_name": "push_force"}
        )

    # -- the box ------------------------------------------------------------------
    box_params = {
        "p_in_path": _env_float("QUADCOOP_BOX_PROB", 0.3),
        "robot_half_length": robot.half_length,
        "box_half_size": BOX_HALF_SIZE,
    }
    cfg.events["box_mass"] = EventTermCfg(
        mode="startup",
        func=envs_mdp.dr.pseudo_inertia,
        params={"alpha_range": _box_mass_alpha_range(), "asset_cfg": SceneEntityCfg("box")},
    )
    cfg.events["box_reset"] = EventTermCfg(
        mode="reset", func=place_box_in_path, params=dict(box_params)
    )
    cfg.events["box_interval"] = EventTermCfg(
        mode="interval",
        interval_range_s=(4.0, 8.0),
        func=place_box_in_path,
        params=dict(box_params),
    )

    cfg.viewer.body_name = robot.base_body
    cfg.viewer.distance = robot.viewer_distance
    cfg.viewer.elevation = -10.0

    if play:
        cfg.episode_length_s = int(1e9)
        cfg.observations["actor"].enable_corruption = False
        cfg.events.pop("push_robot", None)
        cfg.curriculum = {}
        # Invisible forces make a confusing viewer; validate_walker.py tests
        # them explicitly instead.
        cfg.commands.pop("push_force", None)
        cfg.observations["critic"].terms.pop("push_force", None)
        # In the viewer, always put a box in front so you can watch it push.
        cfg.events["box_reset"].params["p_in_path"] = 1.0
        cfg.events["box_interval"].params["p_in_path"] = 1.0
        twist.ranges.lin_vel_x = (-1.0, 1.5)

    return cfg
