"""Stage 0 walker: track (vx, vy, wz) while objects and forces push back.

Built on mjlab's ``make_velocity_env_cfg()`` with the same flat-ground edits as
mjlab's Unitree Go1 flat task, then:

1. ``push_force`` command: sustained horizontal resistance acting at the front
   bumper (``mdp/push_force.py``). Privileged: in the critic, not the actor.
2. Four pushable objects (cube, long prism, cylinder, sphere; ``robots/objects.py``)
   with per-env masses. At most one is dropped in the commanded direction of travel
   (forward, sideways or backward) at reset and every 4-8 s (``mdp/object_events.py``).
3. Curriculum, all in PPO iterations:
     0 - warmup              plain walking: no force, no objects
     warmup - +push_iters    force intensity 0.2 -> 1.0 of its peak
     warmup - +obj_ramp      object placement probability 0 -> obj_pmax
     after warmup            heaviest allowed object starts at 8 kg and rises
                             (to 30 kg) only while robots that touch objects
                             rarely fall and keep tracking their command
4. A command mix tilted toward pushing: more standing envs (bracing) and a speed
   curriculum capped at 1.5 m/s instead of 3 m/s.

The actor observation is exactly the stock velocity task's (IMU, gravity, joints,
last action, command), so the frozen walker drops into later stages unchanged.

Env-var knobs (read when the config is built, i.e. at ``train.py`` start):

* ``QUADCOOP_WARMUP_ITERS``  plain-walking iterations before any disturbance (1000)
* ``QUADCOOP_PUSH_FORCE``    1/0 -- force field on (default) / off (ablation)
* ``QUADCOOP_PUSH_MAX_FRAC`` peak force as fraction of robot weight (0.4)
* ``QUADCOOP_PUSH_START``    force intensity right after warm-up (0.2)
* ``QUADCOOP_PUSH_ITERS``    iterations after warm-up to reach full force (2000)
* ``QUADCOOP_OBJ_PMAX``      final probability a placement puts an object in the path (0.5)
* ``QUADCOOP_OBJ_RAMP``      iterations after warm-up to reach that probability (1500)
* ``QUADCOOP_OBJ_MASS``      "start,final" allowed object mass in kg ("8,30")
"""

from __future__ import annotations

import math
import os

from mjlab.envs import ManagerBasedRlEnvCfg
from mjlab.envs import mdp as envs_mdp
from mjlab.envs.mdp.actions import JointPositionActionCfg
from mjlab.managers.curriculum_manager import CurriculumTermCfg
from mjlab.managers.event_manager import EventTermCfg
from mjlab.managers.metrics_manager import MetricsTermCfg
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

from quadcoop.mdp.metrics import object_contact, velocity_error_xy
from quadcoop.mdp.object_events import STEPS_PER_ITER, object_curriculum, place_object_in_path
from quadcoop.mdp.push_force import PushForceCommandCfg, push_force_enabled
from quadcoop.robots.objects import NOMINAL_MASS, OBJECT_NAMES, get_object_cfgs
from quadcoop.robots.spec import RobotSpec

OBJECT_MASS_RANGE = (3.0, 30.0)  # kg, per env per object, fixed for the run


def _env_float(name: str, default: float) -> float:
    return float(os.environ.get(name, str(default)))


def _mass_alpha(kg: tuple[float, float]) -> tuple[float, float]:
    """pseudo_inertia scales mass (and inertia) by exp(2*alpha)."""
    return (0.5 * math.log(kg[0] / NOMINAL_MASS), 0.5 * math.log(kg[1] / NOMINAL_MASS))


def make_walker_env_cfg(robot: RobotSpec, play: bool = False) -> ManagerBasedRlEnvCfg:
    cfg = make_velocity_env_cfg()
    warmup = int(_env_float("QUADCOOP_WARMUP_ITERS", 1000))

    # -- simulation: flat ground, robot + 4 objects ------------------------------
    cfg.sim.njmax = 800
    cfg.sim.nconmax = None
    cfg.sim.mujoco.ccd_iterations = 50
    cfg.sim.contact_sensor_maxmatch = 64

    assert cfg.scene.terrain is not None
    cfg.scene.terrain.terrain_type = "plane"
    cfg.scene.terrain.terrain_generator = None
    cfg.scene.entities = {"robot": robot.get_robot_cfg(), **get_object_cfgs()}

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
    # Any non-foot robot geom (body, hips, thighs, shanks) touching the ground ends the
    # episode. Without this a policy can crawl on its knees/elbows and never "fall".
    sensors.append(
        ContactSensorCfg(
            name="nonfoot_ground_touch",
            primary=ContactMatch(mode="geom", pattern=robot.nonfoot_collision_regex, entity="robot"),
            secondary=ContactMatch(mode="body", pattern="terrain"),
            fields=("found",),
            reduce="none",
            num_slots=1,
        )
    )
    contact_sensors = []
    for name in OBJECT_NAMES:
        sensors.append(
            ContactSensorCfg(
                name=f"robot_{name}_contact",
                primary=ContactMatch(mode="subtree", pattern=robot.base_body, entity="robot"),
                secondary=ContactMatch(mode="body", pattern="body", entity=name),
                fields=("found",),
                reduce="none",
                num_slots=1,
            )
        )
        contact_sensors.append(f"robot_{name}_contact")
    cfg.scene.sensors = tuple(sensors)
    for group in ("actor", "critic"):
        cfg.observations[group].terms.pop("height_scan", None)

    # Logged as Episode_Metrics/<name>.
    cfg.metrics["object_contact"] = MetricsTermCfg(
        func=object_contact, params={"sensor_names": tuple(contact_sensors)}
    )
    cfg.metrics["vel_error_xy"] = MetricsTermCfg(func=velocity_error_xy)

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

    # -- terminations: a bad orientation or any non-foot ground contact is a fall -------------
    cfg.terminations.pop("out_of_terrain_bounds", None)
    cfg.terminations["illegal_contact"] = TerminationTermCfg(
        func=mdp.illegal_contact, params={"sensor_name": "nonfoot_ground_touch"}
    )
    cfg.terminations["fell_over"] = TerminationTermCfg(
        func=mdp.bad_orientation, params={"limit_angle": math.radians(70.0)}
    )

    # -- commands: omnidirectional, more bracing, no sprinting ------------------
    twist = cfg.commands["twist"]
    assert isinstance(twist, UniformVelocityCommandCfg)
    twist.rel_standing_envs = 0.15
    twist.viz.z_offset = 0.6
    cfg.curriculum.pop("terrain_levels", None)
    cfg.curriculum["command_vel"].params["velocity_stages"] = [
        {"step": 0, "lin_vel_x": (-1.0, 1.0), "ang_vel_z": (-0.5, 0.5)},
        {"step": (warmup + 2000) * STEPS_PER_ITER, "lin_vel_x": (-1.0, 1.5),
         "ang_vel_z": (-0.7, 0.7)},
    ]

    # -- sustained push resistance at the bumper (privileged) --------------------
    if push_force_enabled():
        cfg.commands["push_force"] = PushForceCommandCfg(
            resampling_time_range=(1e9, 1e9),  # Schedule is internal.
            body_name=robot.base_body,
            push_point_b=robot.push_point_b,
            max_frac_of_weight=_env_float("QUADCOOP_PUSH_MAX_FRAC", 0.4),
            curriculum_start_scale=_env_float("QUADCOOP_PUSH_START", 0.2),
            curriculum_env_steps=_env_float("QUADCOOP_PUSH_ITERS", 2000) * STEPS_PER_ITER,
            warmup_env_steps=warmup * STEPS_PER_ITER,
        )
        cfg.observations["critic"].terms["push_force"] = ObservationTermCfg(
            func=envs_mdp.generated_commands, params={"command_name": "push_force"}
        )

    # -- objects ------------------------------------------------------------------
    for name in OBJECT_NAMES:
        cfg.events[f"{name}_mass"] = EventTermCfg(
            mode="startup",
            func=envs_mdp.dr.pseudo_inertia,
            params={"alpha_range": _mass_alpha(OBJECT_MASS_RANGE),
                    "asset_cfg": SceneEntityCfg(name)},
        )
    place = {"robot_half_length": robot.half_length}
    cfg.events["object_reset"] = EventTermCfg(
        mode="reset", func=place_object_in_path, params=dict(place)
    )
    cfg.events["object_interval"] = EventTermCfg(
        mode="interval", interval_range_s=(4.0, 8.0), func=place_object_in_path,
        params=dict(place),
    )
    mass_start, mass_final = (
        float(x) for x in os.environ.get("QUADCOOP_OBJ_MASS", "8,30").split(",")
    )
    cfg.curriculum["objects"] = CurriculumTermCfg(
        func=object_curriculum,
        params={
            "warmup_iters": warmup,
            "ramp_iters": int(_env_float("QUADCOOP_OBJ_RAMP", 1500)),
            "p_max": _env_float("QUADCOOP_OBJ_PMAX", 0.5),
            "mass_start": mass_start,
            "mass_final": mass_final,
        },
    )

    cfg.viewer.body_name = robot.base_body
    cfg.viewer.distance = robot.viewer_distance
    cfg.viewer.elevation = -10.0

    if play:
        cfg.episode_length_s = int(1e9)
        cfg.observations["actor"].enable_corruption = False
        cfg.events.pop("push_robot", None)
        cfg.curriculum = {}
        # Invisible forces make a confusing viewer; the eval scripts test them.
        cfg.commands.pop("push_force", None)
        cfg.observations["critic"].terms.pop("push_force", None)
        # In the viewer, always put an object (up to 15 kg) in front.
        for ev in ("object_reset", "object_interval"):
            cfg.events[ev].params.update(p_override=1.0, max_mass_override=15.0)
        twist.ranges.lin_vel_x = (-1.0, 1.5)

    return cfg