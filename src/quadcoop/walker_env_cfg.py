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
* ``QUADCOOP_PUSH_ADAPTIVE``  1: force scale follows tracking performance instead of time (off)
* ``QUADCOOP_WALKER_HISTORY`` N > 1: actor sees its last N proprioceptive frames (off)

Compliant walker (walker v2, ``compliant=True``, task ``QuadCoop-Walker-AnymalC-Compliant``;
see ``mdp/compliance.py``): the robot senses the contact force from objects (2 more actor
inputs, last) and tracks v_cmd + F / k instead of v_cmd, so against an object it cannot move
the commanded speed sets the push force (k x speed); it is also trained on small commands
(no dead zone below 0.3 m/s), rewarded for steady force (no taps), and meets objects up to
immovable (log-uniform masses up to 3000 kg). Its knobs:

* ``QUADCOOP_STIFFNESS``      k, N per m/s (1000: 0.1 m/s ~ 100 N against a wall)
* ``QUADCOOP_SMALL_SPEED_PROB`` share of command segments at 0.02-0.25 m/s (0.35)
* ``QUADCOOP_OBJ_MASS_RANGE`` "lo,hi" kg of the per-env object masses ("3,3000", log-uniform)
* ``QUADCOOP_FORCE_RATE_W``   weight of the force-change cost (1.0)
* ``QUADCOOP_FINE_TRACK_W``   weight of the tight (0.1 m/s) tracking term (1.5)
  (defaults differ for v2: QUADCOOP_OBJ_MASS "20,3000" grown x1.15 per step, QUADCOOP_PUSH_REWARD 0,
  QUADCOOP_WARMUP_ITERS 50, QUADCOOP_OBJ_RAMP 300 - it is warm-started from v1)
* ``QUADCOOP_PUSH_MAX_FRAC`` / ``_START`` / ``_ITERS``  force field peak (0.4 x weight),
  starting intensity (0.2), iterations to full (2000)

Walker v2.1 (``v21=True``, task ``QuadCoop-Walker-AnymalC-Compliant-v21``; same network as v2,
resumed from it; logs in the same experiment folder): what v2's acceptance test and training
curves showed missing, no new reward terms. Defaults (each overridable):

* force field on (``QUADCOOP_PUSH_FORCE``), ramp-hold-ramp loads up to 0.5 x weight
  (``QUADCOOP_PUSH_MAX_FRAC``), 70% against the command; the walker *feels* it (it is added to the
  contact force in its force input and in the compliant target), so it practises every force
  level on smooth loads (Portela et al. 2024; arXiv 2505.20829)
* mass curriculum from 35 kg (where v2 stopped; ``QUADCOOP_OBJ_MASS``), gate: falls < 0.25 (``QUADCOOP_CURR_FALL``), back off > 0.40
  (``QUADCOOP_CURR_RETREAT``), a decision every 30 iterations (``QUADCOOP_CURR_DWELL``)
* force filter 0.1 per step (``QUADCOOP_FORCE_FILTER``), back-off at most 0.1 m/s
  (``QUADCOOP_MAX_BACKOFF``)
* free walk 40% of episodes; slow speeds log-uniform 0.02-0.3 m/s (``QUADCOOP_SMALL_SPEED_MAX``);
  20% of free-walk segments turn on the spot at 0.05-0.6 rad/s (``QUADCOOP_TURN_IN_PLACE``,
  ``QUADCOOP_TURN_MAX``)
* turn tracking tolerance 0.4 rad/s instead of 0.71 (``QUADCOOP_YAW_STD``)

Walker v2.2 (``v22=True``, task ``QuadCoop-Walker-AnymalC-Compliant-v22``; same network, resumed
from v2.1; same log folder). v2.1's commands, curriculum and force filter, but:

* no synthetic bumper load: v2.1's field pushed against *any* commanded direction at the nose
  (sideways -> a twist, backward -> a pull), and sideways / slow-backward walking regressed. Real
  objects (masses up to immovable) are the front-contact practice; the stock random kicks are the
  disturbances. ``QUADCOOP_PUSH_FORCE=1`` brings the field back as an unfelt disturbance only
* k = 500 N per m/s (``QUADCOOP_STIFFNESS``): 0.1 m/s -> 50 N, 0.3 m/s -> 150 N, inside the
  speeds the walker can walk at and under its measured ~150-180 N plateau
* retreat bounded along the force (at most 0.1 m/s), not just the speed
* fine tracking planar-only and yaw-only, on the velocity smoothed over ~0.4 s
  (``QUADCOOP_TRACK_TAU``; restarted at each new command): ``track_fine`` (std 0.1 m/s, weight 1.5)
  and ``track_yaw_fine`` (std 0.15 rad/s, ``QUADCOOP_FINE_YAW_STD``, weight 1.0,
  ``QUADCOOP_FINE_YAW_W``); the stock turn term goes back to its own tolerance (0.71)
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
from mjlab.utils.noise import UniformNoiseCfg as Unoise
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

from quadcoop.mdp.compliance import (
    ComplianceTargetCommandCfg,
    bumper_force_obs,
    force_rate_penalty,
    track_planar_fine,
    track_yaw_fine,
    velocity_progress_target,
)
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


def make_walker_env_cfg(robot: RobotSpec, play: bool = False, history: int | None = None,
                        compliant: bool = False, v21: bool = False, v22: bool = False) -> ManagerBasedRlEnvCfg:
    v21 = v21 or v22  # v2.2 keeps v2.1's commands, curriculum and filter; differences marked v22
    compliant = compliant or v21
    cfg = make_velocity_env_cfg()
    warmup = int(_env_float("QUADCOOP_WARMUP_ITERS", 50 if compliant else 1000))

    # -- simulation: flat ground, robot + 4 objects ------------------------------
    cfg.sim.njmax = 800
    cfg.sim.nconmax = None
    cfg.sim.mujoco.ccd_iterations = 50
    cfg.sim.contact_sensor_maxmatch = 64
    # Contact model. Default "train" keeps mjlab's pyramidal cone / impratio 1, under which a loaded foot
    # creeps (12 mm/s at 10% of the friction limit, ~200 mm/s at 75%: evals/contact-creep), so a planted
    # robot cannot hold a sustained push (evals/brace-wbc). QUADCOOP_CONTACT=nocreep: elliptic cone,
    # impratio 10 (creep 30-70x smaller; foot solimp unchanged). Changes the physics every walker so far
    # was trained in: evaluate before training on it.
    contact = os.environ.get("QUADCOOP_CONTACT", "train")
    if contact == "nocreep":
        cfg.sim.mujoco.cone = "elliptic"
        cfg.sim.mujoco.impratio = _env_float("QUADCOOP_IMPRATIO", 10.0)
    elif contact != "train":
        raise ValueError(f"QUADCOOP_CONTACT={contact!r}: expected train or nocreep")

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
    if compliant:  # v2: the contact force between the robot and any object (reading = force on the robot)
        sensors.append(
            ContactSensorCfg(
                name="bumper_force",
                primary=ContactMatch(mode="body", pattern=tuple(f"{n}/body" for n in OBJECT_NAMES)),
                secondary=ContactMatch(mode="subtree", pattern=robot.base_body, entity="robot"),
                fields=("found", "force"),
                reduce="netforce",
                num_slots=1,
            )
        )
    cfg.scene.sensors = tuple(sensors)
    for group in ("actor", "critic"):
        cfg.observations[group].terms.pop("height_scan", None)
    # Proprioceptive history for the actor (FALCON-style force adaptation: a sustained push
    # is inferred from how the body and joints have been responding). QUADCOOP_WALKER_HISTORY=N
    # stacks the last N frames of every actor term except the velocity command. Later stages
    # copy the walker's observation group, so they get the same history automatically.
    # (history=N overrides the env var: the two-robot env builds each robot with its own walker's N)
    hist = int(_env_float("QUADCOOP_WALKER_HISTORY", 0)) if history is None else int(history)
    if hist > 1:
        for name, term in cfg.observations["actor"].terms.items():
            if name != "command":
                term.history_length = hist
                term.flatten_history_dim = True

    # Logged as Episode_Metrics/<name>.
    cfg.metrics["object_contact"] = MetricsTermCfg(
        func=object_contact, params={"sensor_names": tuple(contact_sensors)}
    )
    cfg.metrics["vel_error_xy"] = MetricsTermCfg(func=velocity_error_xy)
    if compliant:
        cfg.metrics["vel_error_target"] = MetricsTermCfg(func=velocity_error_xy, params={"command_name": "compliance"})

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
    cfg.rewards["air_time"].params["command_threshold"] = 0.05 if compliant else 0.2
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
    # (walker v2.1: on by default, and felt by the walker - mdp/compliance.applied_force_b)
    if push_force_enabled(default=v21 and not v22):
        cfg.commands["push_force"] = PushForceCommandCfg(
            resampling_time_range=(1e9, 1e9),  # Schedule is internal.
            body_name=robot.base_body,
            push_point_b=robot.push_point_b,
            max_frac_of_weight=_env_float("QUADCOOP_PUSH_MAX_FRAC", 0.5 if v21 else 0.4),
            curriculum_start_scale=_env_float("QUADCOOP_PUSH_START", 0.3 if v21 else 0.2),
            curriculum_env_steps=_env_float("QUADCOOP_PUSH_ITERS", 1000 if v21 else 2000) * STEPS_PER_ITER,
            warmup_env_steps=(0 if v21 else warmup) * STEPS_PER_ITER,
            # QUADCOOP_PUSH_ADAPTIVE=1: FALCON-style curriculum, the force scale grows only
            # while velocity tracking stays good (and shrinks when it degrades)
            adaptive=os.environ.get("QUADCOOP_PUSH_ADAPTIVE", "0") == "1",
        )
        if not compliant:  # the compliant walker's force input (actor and critic) already includes it
            cfg.observations["critic"].terms["push_force"] = ObservationTermCfg(
                func=envs_mdp.generated_commands, params={"command_name": "push_force"}
            )

    # -- objects ------------------------------------------------------------------
    mass_range = OBJECT_MASS_RANGE
    if compliant:
        mass_range = tuple(float(x) for x in os.environ.get("QUADCOOP_OBJ_MASS_RANGE", "3,3000").split(","))
    for name in OBJECT_NAMES:
        cfg.events[f"{name}_mass"] = EventTermCfg(
            mode="startup",
            func=envs_mdp.dr.pseudo_inertia,
            params={"alpha_range": _mass_alpha(mass_range),
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
        p_free_walk=_env_float("QUADCOOP_FREE_WALK", 0.4 if v21 else 0.25),
        small_speed_prob=_env_float("QUADCOOP_SMALL_SPEED_PROB", 0.35) if compliant else 0.0,
    )
    if v21:  # slow speeds log-uniform 0.02-0.3 m/s in every direction, and pure turns on the spot
        twist.small_speed_range = (0.02, _env_float("QUADCOOP_SMALL_SPEED_MAX", 0.3))
        twist.small_speed_log = True
        twist.turn_in_place_prob = _env_float("QUADCOOP_TURN_IN_PLACE", 0.2)
        twist.turn_in_place_range = (0.05, _env_float("QUADCOOP_TURN_MAX", 0.6))
    # Pays for moving the touched object along the commanded direction, so going around
    # it (which still tracks velocity well enough) is worse than pushing it.
    cfg.rewards["object_push"] = RewardTermCfg(
        func=object_push_progress,
        weight=_env_float("QUADCOOP_PUSH_REWARD", 0.0 if compliant else 0.5),
        params={"command_name": "twist", "object_names": tuple(OBJECT_NAMES),
                "sensor_names": tuple(contact_sensors)},
    )
    mass_start, mass_final = (
        float(x) for x in os.environ.get("QUADCOOP_OBJ_MASS", ("35,3000" if v21 else "20,3000") if compliant else "5,30").split(",")
    )
    cfg.curriculum["objects"] = CurriculumTermCfg(
        func=object_curriculum,
        params={
            "warmup_iters": warmup,
            "ramp_iters": int(_env_float("QUADCOOP_OBJ_RAMP", 300 if compliant else 1500)),
            "p_max": _env_float("QUADCOOP_OBJ_PMAX", 0.8),
            "mass_start": mass_start,
            "mass_final": mass_final,
            **({"err_metric": "vel_error_target", "mass_growth": 1.15} if compliant else {}),
            # v2.1: v2's curriculum stalled at 35-40 kg because training falls (with exploration
            # noise) sat at 0.15-0.2 against a 0.10 gate; the test walker never fell
            **({"advance_fall": _env_float("QUADCOOP_CURR_FALL", 0.25),
                "retreat_fall": _env_float("QUADCOOP_CURR_RETREAT", 0.40),
                "dwell_iters": int(_env_float("QUADCOOP_CURR_DWELL", 30))} if v21 else {}),
        },
    )

    # -- walker v2: compliant target, force sensing, steady pressing -----------------------------
    if compliant:
        k = _env_float("QUADCOOP_STIFFNESS", 500.0 if v22 else 1000.0)
        felt = None if v22 else "push_force"  # v2.2: only real contact is felt (the field, if on, is a disturbance)
        cfg.commands["compliance"] = ComplianceTargetCommandCfg(
            twist_name="twist", sensor_name="bumper_force", stiffness=k,
            # v2.1: slower force filter (~0.2 s) and little back-off, so an impact spike does not
            # tell the robot to retreat (the source of v2's tapping)
            filter_alpha=_env_float("QUADCOOP_FORCE_FILTER", 0.1 if v21 else 0.3),
            max_backoff=_env_float("QUADCOOP_MAX_BACKOFF", 0.1 if v21 else 0.3),
            directional_backoff=v22, felt_load_term=felt,
        )
        # the robot feels the contact force (last input: a v1 walker is widened at the end)
        for group in ("actor", "critic"):
            cfg.observations[group].terms["bumper_force"] = ObservationTermCfg(
                func=bumper_force_obs, params={"sensor_name": "bumper_force", "felt_load_term": felt},
                noise=Unoise(n_min=-0.02, n_max=0.02) if group == "actor" else None,
            )
        # every command-following reward follows the compliant target instead of the raw command
        for name in ("track_linear_velocity", "track_angular_velocity", "pose", "air_time", "foot_clearance",
                     "foot_swing_height", "foot_slip", "soft_landing"):
            if name in cfg.rewards and "command_name" in cfg.rewards[name].params:
                cfg.rewards[name].params["command_name"] = "compliance"
        cfg.rewards["velocity_progress"] = RewardTermCfg(
            func=velocity_progress_target, weight=_env_float("QUADCOOP_PROGRESS_REWARD", 1.5),
            params={"command_name": "compliance"},
        )
        # small commands need tight tracking: the stock term (std 0.5 m/s) barely tells 0.05 from 0
        cfg.rewards["track_fine"] = RewardTermCfg(
            func=mdp.track_linear_velocity, weight=_env_float("QUADCOOP_FINE_TRACK_W", 1.5),
            params={"command_name": "compliance", "std": 0.1},
        )
        if v22:  # planar-only on a 0.4 s smoothed velocity (the stock function also counts vertical
            # velocity: at std 0.1, stepping with 0.1 m/s of bounce scored below standing still), and
            # the same for yaw (the stock turn term also counts roll / pitch rate)
            tau = _env_float("QUADCOOP_TRACK_TAU", 0.4)
            cfg.rewards["track_fine"] = RewardTermCfg(
                func=track_planar_fine, weight=_env_float("QUADCOOP_FINE_TRACK_W", 1.5),
                params={"command_name": "compliance", "std": 0.1, "tau": tau},
            )
            cfg.rewards["track_yaw_fine"] = RewardTermCfg(
                func=track_yaw_fine, weight=_env_float("QUADCOOP_FINE_YAW_W", 1.0),
                params={"command_name": "compliance", "std": _env_float("QUADCOOP_FINE_YAW_STD", 0.15), "tau": tau},
            )
        cfg.rewards["force_rate"] = RewardTermCfg(
            func=force_rate_penalty, weight=-_env_float("QUADCOOP_FORCE_RATE_W", 1.0),
            params={"command_name": "compliance"},
        )
        if v21 and not v22:  # turning: the stock tolerance (std 0.71 rad/s) pays 92% for standing still at 0.2 rad/s
            cfg.rewards["track_angular_velocity"].params["std"] = _env_float("QUADCOOP_YAW_STD", 0.4)

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