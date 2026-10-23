"""Stage 1: one robot pushes a box to a goal pose, through its frozen Stage 0 walker.

Built from the Stage 0 walker config so the robot, its actuators, its domain
randomization and the walker's observation are exactly what the walker was trained
with. Then: the walker's actor observation becomes the "walker" group (fed to the
frozen walker, not to PPO); the action is the high-level (vx, vy, wz); and the
scene, task, rewards and terminations are replaced by the push-to-goal task.

The walker checkpoint is read when the env is built, from QUADCOOP_WALKER_CKPT (or
the per-robot QUADCOOP_WALKER_CKPT_<ROBOT>).
"""

from __future__ import annotations

import copy
import math
import os

from mjlab.envs import ManagerBasedRlEnvCfg
from mjlab.envs import mdp as envs_mdp
from mjlab.managers.curriculum_manager import CurriculumTermCfg
from mjlab.managers.event_manager import EventTermCfg
from mjlab.managers.observation_manager import ObservationGroupCfg, ObservationTermCfg
from mjlab.managers.reward_manager import RewardTermCfg
from mjlab.managers.scene_entity_config import SceneEntityCfg
from mjlab.managers.termination_manager import TerminationTermCfg
from mjlab.sensor import ContactMatch, ContactSensorCfg
from mjlab.tasks.velocity import mdp as vel_mdp
from mjlab.utils.noise import UniformNoiseCfg as Unoise

from quadcoop.robots.spec import RobotSpec
from quadcoop.stage1 import mdp
from quadcoop.stage1.objects import BOX_NAMES, NOMINAL_MASS, get_box_cfgs, get_goal_cfgs
from quadcoop.walker_env_cfg import make_walker_env_cfg

# Ground contact by these parts = the robot fell (same rule as Stage 0's fixed version).
FALL_CONTACT_REGEX = {
    "anymal_c": r".*_collision\d*$",
    "spot": r"^(body|.*_uleg)_collision$",
}
BOX_MASS_RANGE = (3.0, 25.0)  # kg per box copy; the curriculum picks from a window
BOX_FRICTION_RANGE = (0.4, 0.6)
KEEP_EVENTS = ("foot_friction", "base_com", "encoder_bias", "reset_base", "reset_robot_joints")


def make_push_env_cfg(robot: RobotSpec, play: bool = False) -> ManagerBasedRlEnvCfg:
    cfg = make_walker_env_cfg(robot)  # exactly what the walker was trained in

    # -- scene: robot + 6 boxes + 2 goal markers ------------------------------------
    cfg.scene.entities = {"robot": cfg.scene.entities["robot"], **get_box_cfgs(), **get_goal_cfgs()}
    cfg.scene.sensors = (
        ContactSensorCfg(
            name="fall_contact",
            primary=ContactMatch(mode="geom", pattern=FALL_CONTACT_REGEX.get(robot.name,
                                                                              robot.nonfoot_collision_regex),
                                 entity="robot"),
            secondary=ContactMatch(mode="body", pattern="terrain"),
            fields=("found",), reduce="none", num_slots=1,
        ),
    )
    cfg.sim.njmax = 600
    cfg.episode_length_s = 20.0

    # -- actions: high-level (vx, vy, wz) -> frozen walker -> joints ---------------------
    joint_cfg = cfg.actions["joint_pos"]
    env_var = f"QUADCOOP_WALKER_CKPT_{robot.name.upper()}"
    cfg.actions = {
        "walker": mdp.WalkerCommandActionCfg(
            entity_name="robot",
            joint_cfg=joint_cfg,
            checkpoint=os.environ.get(env_var, ""),  # per-robot var wins, else the generic one
        )
    }

    # -- commands: the walker's twist (set by the action) + the task -------------------
    cfg.commands = {
        "twist": mdp.HighLevelTwistCfg(),
        "goal": mdp.PushGoalCommandCfg(robot_reach=robot.half_length),
    }

    # -- observations ---------------------------------------------------------------------
    walker_group = copy.deepcopy(cfg.observations["actor"])
    walker_group.terms.pop("height_scan", None)
    old = walker_group.terms["actions"]  # keep the walker's history setting, if any
    walker_group.terms["actions"] = ObservationTermCfg(func=mdp.walker_last_action,
                                                       history_length=old.history_length,
                                                       flatten_history_dim=old.flatten_history_dim)
    walker_group.terms["command"] = ObservationTermCfg(
        func=envs_mdp.generated_commands, params={"command_name": "twist"})
    hl = {
        "base_lin_vel": ObservationTermCfg(func=vel_mdp.builtin_sensor,
                                           params={"sensor_name": "robot/imu_lin_vel"},
                                           noise=Unoise(n_min=-0.1, n_max=0.1)),
        "base_ang_vel": ObservationTermCfg(func=vel_mdp.builtin_sensor,
                                           params={"sensor_name": "robot/imu_ang_vel"},
                                           noise=Unoise(n_min=-0.1, n_max=0.1)),
        "projected_gravity": ObservationTermCfg(func=vel_mdp.projected_gravity),
        "box": ObservationTermCfg(func=mdp.box_in_robot_frame, noise=Unoise(n_min=-0.02, n_max=0.02)),
        "goal": ObservationTermCfg(func=mdp.goal_in_robot_frame, noise=Unoise(n_min=-0.02, n_max=0.02)),
        "box_shape": ObservationTermCfg(func=mdp.box_shape_obs),
        "walker_command": ObservationTermCfg(func=mdp.walker_command),
        "last_action": ObservationTermCfg(func=envs_mdp.last_action),
    }
    critic = {**copy.deepcopy(hl), "box_physics": ObservationTermCfg(func=mdp.box_physics)}
    cfg.observations = {
        "actor": ObservationGroupCfg(terms=hl, concatenate_terms=True, enable_corruption=not play),
        "critic": ObservationGroupCfg(terms=critic, concatenate_terms=True, enable_corruption=False),
        "walker": walker_group,
    }

    # -- events: the walker's robot randomization; robot starts at its spot, facing +x ---
    cfg.events = {k: v for k, v in cfg.events.items() if k in KEEP_EVENTS}
    # Feet need enough grip to push a box: below ~0.5 a robot cannot push its heavier
    # boxes at all, whatever the high-level policy does (older walker configs used 0.3).
    cfg.events["foot_friction"].params["ranges"] = (0.6, 1.2)
    cfg.events["reset_base"].params["pose_range"] = {
        "x": (0.0, 0.0), "y": (0.0, 0.0), "z": (0.01, 0.03), "yaw": (-0.3, 0.3)}
    cfg.events["reset_base"].params["velocity_range"] = {}
    alpha = (0.5 * math.log(BOX_MASS_RANGE[0] / NOMINAL_MASS),
             0.5 * math.log(BOX_MASS_RANGE[1] / NOMINAL_MASS))
    for name in BOX_NAMES:
        cfg.events[f"{name}_mass"] = EventTermCfg(
            mode="startup", func=envs_mdp.dr.pseudo_inertia,
            params={"alpha_range": alpha, "asset_cfg": SceneEntityCfg(name)})
        cfg.events[f"{name}_friction"] = EventTermCfg(
            mode="startup", func=envs_mdp.dr.geom_friction,
            params={"asset_cfg": SceneEntityCfg(name, geom_names=("geom",)),
                    "operation": "abs", "ranges": BOX_FRICTION_RANGE})

    # -- rewards --------------------------------------------------------------------------
    R = RewardTermCfg
    cfg.rewards = {
        "box_progress": R(func=mdp.box_progress, weight=3.0),
        "box_near_goal": R(func=mdp.box_near_goal, weight=1.0),
        "yaw_progress": R(func=mdp.yaw_progress, weight=0.5),
        "yaw_aligned": R(func=mdp.yaw_aligned, weight=1.0),
        "robot_near_box": R(func=mdp.robot_near_box, weight=0.5),
        "robot_behind_box": R(func=mdp.robot_behind_box, weight=0.3),
        "at_goal": R(func=mdp.at_goal, weight=4.0),
        "action_rate": R(func=mdp.hl_action_rate, weight=-0.05),
        "terminated": R(func=envs_mdp.is_terminated, weight=-20.0),
    }

    # -- terminations ---------------------------------------------------------------------
    cfg.terminations = {
        "time_out": TerminationTermCfg(func=envs_mdp.time_out, time_out=True),
        "fell_over": TerminationTermCfg(func=vel_mdp.bad_orientation,
                                        params={"limit_angle": math.radians(70.0)}),
        "fell_contact": TerminationTermCfg(func=vel_mdp.illegal_contact,
                                           params={"sensor_name": "fall_contact"}),
        "box_tipped": TerminationTermCfg(func=mdp.box_tipped),
        "box_lost": TerminationTermCfg(func=mdp.box_lost),
    }

    # -- curriculum / metrics ---------------------------------------------------------------
    cfg.curriculum = {"push": CurriculumTermCfg(func=mdp.push_curriculum)}
    cfg.metrics = {}

    cfg.viewer.body_name = robot.base_body
    cfg.viewer.distance = 4.5
    cfg.viewer.elevation = -25.0

    if play:
        cfg.episode_length_s = 30.0
        cfg.curriculum = {}
        level = int(os.environ.get("QUADCOOP_PUSH_LEVEL", "2"))
        cfg.commands["goal"].start_level = level
        cfg.commands["goal"].replay_frac = 0.0
    return cfg