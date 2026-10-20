"""Stage 0 walker: hold a commanded velocity while walking through objects.

Built on mjlab's ``make_velocity_env_cfg()`` with the same flat-ground edits as
mjlab's Unitree Go1 flat task, then:

1. Episodes (``mdp/push_command.py``), chosen at every reset:
   * push episode (75%): walk at 0.3-0.7 m/s in a direction from the full circle
     (forward, sideways, backward, diagonal), 30% of the time while turning slowly;
     every 5-10 s the direction is nudged by up to 45 deg. Objects are put on the line
     of travel; when the robot has passed one, or it slid/rolled away, a new one appears.
   * free walk (25%): no objects, the command changes every few seconds and may turn,
     so the walker stays responsive to the commands Stage 1 will send it.
2. Six pushable objects (cube, long prism, cylinder, sphere, tall box, low wide box;
   ``robots/objects.py``), each with a per-env mass (3-30 kg) and ground friction
   (0.3-0.6). The object's friction governs its contacts (contact priority).
3. Curriculum, in PPO iterations:
     0 - warmup              plain walking (push episodes walk straight, no objects)
     warmup - +obj_ramp      chance an object is put in a clear path: 0 -> obj_pmax
     after warmup            heaviest allowed object starts at 5 kg and rises (to 30)
                             only while robots that touch objects rarely fall and
                             keep tracking their command
4. Rewards: stock velocity tracking + linear progress, gait (foot air time), base
   height, smooth base, posture, clean feet; plus pushing the touched object along the
   commanded direction (so going around it is worse than pushing through).
5. Optional bumper force field (``mdp/push_force.py``), off by default.

The actor observation is exactly the stock velocity task's (IMU, gravity, joints,
last action, command), so the frozen walker drops into later stages unchanged.

Env-var knobs (read when the config is built, i.e. at ``train.py`` start):

* ``QUADCOOP_WARMUP_ITERS``   plain-walking iterations before objects appear (1000)
* ``QUADCOOP_OBJ_PMAX``       final chance an object is put in a clear path (0.8)
* ``QUADCOOP_OBJ_RAMP``       iterations after warm-up to reach it (1500)
* ``QUADCOOP_OBJ_MASS``       "start,final" allowed object mass in kg ("5,30")
* ``QUADCOOP_FREE_WALK``      share of episodes without objects, changing commands (0.25)
* ``QUADCOOP_PUSH_REWARD``    weight of the object-push-progress reward (0.5)
* ``QUADCOOP_PROGRESS_REWARD`` weight of the linear velocity-progress reward (1.5)
* ``QUADCOOP_GAIT_REWARD``    weight of the foot air-time (stepping) reward (0.5)
* ``QUADCOOP_HEIGHT_REWARD``  weight of the base-height reward (0.5)
* ``QUADCOOP_SMOOTH_REWARD``  weight of the smooth-base (COM) reward (0.5)
* ``QUADCOOP_PUSH_FORCE``     1 turns on the bumper force field (off)
* ``QUADCOOP_PUSH_MAX_FRAC`` / ``_START`` / ``_ITERS``  force field peak (0.4 x weight),
  starting intensity (0.2), iterations to full (2000)
"""

from __future__ import annotations

import dataclasses
import math
import os

from mjlab.envs import ManagerBasedRlEnvCfg
from mjlab.envs import mdp as envs_mdp
from mjlab.envs.mdp.actions import JointPositionActionCfg
from mjlab.managers.curriculum_manager import CurriculumTermCfg
from mjlab.managers.event_manager import EventTermCfg
from mjlab.managers.metrics_manager import MetricsTermCfg
from mjlab.managers.observation_manager import ObservationTermCfg
from mjlab.managers.reward_manager import RewardTermCfg
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
from quadcoop.mdp.object_events import STEPS_PER_ITER, object_curriculum
from quadcoop.mdp.push_command import PushTaskCommandCfg
from quadcoop.mdp.rewards import (
    base_height,
    base_smoothness,
    object_push_progress,
    velocity_progress,
)
from quadcoop.mdp.push_force import PushForceCommandCfg, push_force_enabled
from quadcoop.robots.objects import NOMINAL_MASS, OBJECT_NAMES, get_object_cfgs
from quadcoop.robots.spec import RobotSpec

OBJECT_MASS_RANGE = (3.0, 30.0)  # kg, per env per object, fixed for the run
OBJECT_FRICTION_RANGE = (0.3, 0.6)  # object-ground sliding friction, per env per object


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
    # The feet's friction wins at the ground (collision priority 1), so it caps the
    # horizontal force a robot can push against: with mu < ~0.5 the 0.4 x weight bumper
    # force is unbeatable and the only answer is to brace. Floor it at 0.6.
    cfg.events["foot_friction"].params["ranges"] = (0.6, 1.2)
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
    # Gait: reward each foot's swing time (0.05-0.5 s) whenever the robot is told to
    # move, so it steps instead of shuffling or bracing in place.
    cfg.rewards["air_time"].weight = _env_float("QUADCOOP_GAIT_REWARD", 0.5)
    cfg.rewards["air_time"].params["command_threshold"] = 0.2
    # Hold the body at its walking height (no sagging into the push).
    cfg.rewards["base_height"] = RewardTermCfg(
        func=base_height, weight=_env_float("QUADCOOP_HEIGHT_REWARD", 0.5),
        params={"target": robot.nominal_height},
    )
    # The stock random kicks (every 1-3 s, incl. +-0.4 m/s vertical and +-0.5 rad/s
    # roll/pitch) are a different disturbance from the sustained push we care about,
    # and the vertical part shoves the body down. Keep small horizontal kicks only.
    cfg.events["push_robot"].interval_range_s = (4.0, 8.0)
    cfg.events["push_robot"].params["velocity_range"] = {
        "x": (-0.3, 0.3), "y": (-0.3, 0.3), "yaw": (-0.4, 0.4),
    }

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
    # Commands are sampled by PushTaskCommand (constant speed per segment, see
    # push_command.py), so the stock range curriculum has nothing to widen.
    cfg.curriculum.pop("command_vel", None)
    # Pays linearly for actually moving along the command (0 standing, 1 at the
    # commanded speed). See rewards.velocity_progress for why the stock term is not enough.
    cfg.rewards["velocity_progress"] = RewardTermCfg(
        func=velocity_progress, weight=_env_float("QUADCOOP_PROGRESS_REWARD", 1.5),
        params={"command_name": "twist"},
    )
    # Smooth centre-of-mass motion: no bobbing, no rocking.
    cfg.rewards["base_smoothness"] = RewardTermCfg(
        func=base_smoothness, weight=_env_float("QUADCOOP_SMOOTH_REWARD", 0.5),
    )

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
        cfg.events[f"{name}_friction"] = EventTermCfg(
            mode="startup",
            func=envs_mdp.dr.geom_friction,
            params={"asset_cfg": SceneEntityCfg(name, geom_names=("geom",)),
                    "operation": "abs", "ranges": OBJECT_FRICTION_RANGE},
        )
    # The twist command runs the episodes: fixed-direction push episodes with objects
    # put on the line, and free-walk episodes with changing commands.
    twist = cfg.commands["twist"] = PushTaskCommandCfg(
        **{f.name: getattr(twist, f.name) for f in dataclasses.fields(twist) if f.init},
        robot_half_length=robot.half_length,
        p_free_walk=_env_float("QUADCOOP_FREE_WALK", 0.25),
    )
    # Pays for moving the touched object along the commanded direction, so going around
    # it (which still tracks velocity well enough) is worse than pushing it.
    cfg.rewards["object_push"] = RewardTermCfg(
        func=object_push_progress,
        weight=_env_float("QUADCOOP_PUSH_REWARD", 0.5),
        params={"command_name": "twist", "object_names": tuple(OBJECT_NAMES),
                "sensor_names": tuple(contact_sensors)},
    )
    mass_start, mass_final = (
        float(x) for x in os.environ.get("QUADCOOP_OBJ_MASS", "5,30").split(",")
    )
    cfg.curriculum["objects"] = CurriculumTermCfg(
        func=object_curriculum,
        params={
            "warmup_iters": warmup,
            "ramp_iters": int(_env_float("QUADCOOP_OBJ_RAMP", 1500)),
            "p_max": _env_float("QUADCOOP_OBJ_PMAX", 0.8),
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
        twist.p_override, twist.max_mass_override = 1.0, 15.0

    return cfg