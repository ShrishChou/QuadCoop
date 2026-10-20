"""Stage 1b env: Stage 1's robot + frozen walker, with the harder ten-shape task.

Built from Stage 1's config (so the walker interface is identical), then the scene,
task, observations, rewards, terminations and curriculum are swapped for Stage 1b.
Observation terms that mean the same thing keep Stage 1's names and sizes, so a
Stage 1 policy can be warm-started (scripts/warmstart_push.py).
"""

from __future__ import annotations

import copy
import math

from mjlab.envs import mdp as envs_mdp
from mjlab.managers.curriculum_manager import CurriculumTermCfg
from mjlab.managers.event_manager import EventTermCfg
from mjlab.managers.observation_manager import ObservationGroupCfg, ObservationTermCfg
from mjlab.managers.reward_manager import RewardTermCfg
from mjlab.managers.scene_entity_config import SceneEntityCfg
from mjlab.managers.termination_manager import TerminationTermCfg
from mjlab.tasks.velocity import mdp as vel_mdp
from mjlab.utils.noise import UniformNoiseCfg as Unoise

from quadcoop.robots.spec import RobotSpec
from quadcoop.stage1 import mdp as s1
from quadcoop.stage1.push_env_cfg import make_push_env_cfg
from quadcoop.stage1b import mdp
from quadcoop.stage1b.shapes import NOMINAL_MASS, OBJ_NAMES, SHAPES, get_goal_cfgs, get_object_cfgs

MASS_RANGE = (5.0, 40.0)  # per object, per env, fixed for the run; the level picks a window
FRICTION_RANGE = (0.4, 0.6)


def make_hard_env_cfg(robot: RobotSpec, play: bool = False):
    cfg = make_push_env_cfg(robot, play=play)

    cfg.scene.entities = {"robot": cfg.scene.entities["robot"], **get_object_cfgs(), **get_goal_cfgs()}
    cfg.sim.njmax = 800
    cfg.episode_length_s = 30.0

    cfg.commands["goal"] = mdp.HardGoalCommandCfg(robot_reach=robot.half_length)

    # -- events: drop Stage 1's box randomization, add per-object mass and friction -------
    cfg.events = {k: v for k, v in cfg.events.items() if not k.startswith("box_")}
    alpha = (0.5 * math.log(MASS_RANGE[0] / NOMINAL_MASS), 0.5 * math.log(MASS_RANGE[1] / NOMINAL_MASS))
    for name, shape in zip(OBJ_NAMES, SHAPES, strict=True):
        cfg.events[f"{name}_mass"] = EventTermCfg(
            mode="startup", func=envs_mdp.dr.pseudo_inertia,
            params={"alpha_range": alpha, "asset_cfg": SceneEntityCfg(name)})
        if not shape.fixed_friction:
            cfg.events[f"{name}_friction"] = EventTermCfg(
                mode="startup", func=envs_mdp.dr.geom_friction,
                params={"asset_cfg": SceneEntityCfg(name, geom_names=(".*",)), "operation": "abs",
                        "ranges": FRICTION_RANGE, "shared_random": True})

    # -- observations: Stage 1 names where the meaning is unchanged --------------------
    hl = {
        "base_lin_vel": cfg.observations["actor"].terms["base_lin_vel"],
        "base_ang_vel": cfg.observations["actor"].terms["base_ang_vel"],
        "projected_gravity": cfg.observations["actor"].terms["projected_gravity"],
        "box": ObservationTermCfg(func=mdp.box_in_robot_frame, noise=Unoise(n_min=-0.02, n_max=0.02)),
        "goal": ObservationTermCfg(func=mdp.goal_in_robot_frame, noise=Unoise(n_min=-0.02, n_max=0.02)),
        "walker_command": ObservationTermCfg(func=s1.walker_command),
        "last_action": ObservationTermCfg(func=envs_mdp.last_action),
        # new in Stage 1b (start at zero weight when warm-started)
        "object_desc": ObservationTermCfg(func=mdp.object_descriptor),
        "hold_progress": ObservationTermCfg(func=mdp.hold_progress),
    }
    critic = {**copy.deepcopy(hl), "box_physics": ObservationTermCfg(func=mdp.box_physics)}
    cfg.observations["actor"] = ObservationGroupCfg(terms=hl, concatenate_terms=True,
                                                    enable_corruption=not play)
    cfg.observations["critic"] = ObservationGroupCfg(terms=critic, concatenate_terms=True,
                                                     enable_corruption=False)

    # -- rewards (Stage 1's, plus a bonus for completing the hold) ------------------------
    R = RewardTermCfg
    cfg.rewards = {
        "box_progress": R(func=mdp.box_progress, weight=3.0),
        "box_near_goal": R(func=mdp.box_near_goal, weight=1.0),
        "yaw_progress": R(func=mdp.yaw_progress, weight=0.5),
        "yaw_aligned": R(func=mdp.yaw_aligned, weight=1.0),
        "robot_near_box": R(func=mdp.robot_near_box, weight=0.5),
        "robot_behind_box": R(func=mdp.robot_behind_box, weight=0.3),
        "at_goal": R(func=mdp.at_goal, weight=4.0),
        "held": R(func=mdp.held, weight=2.0),
        # precision: exponentially sharper reward for the last few cm / degrees
        "precise_pose": R(func=mdp.precise_pose, weight=4.0),
        # calm: no fast or spinning object near the goal, no object running away
        "box_settle": R(func=mdp.box_settle, weight=-1.0),
        "box_runaway": R(func=mdp.box_runaway, weight=-3.0),
        "action_rate": R(func=s1.hl_action_rate, weight=-0.05),
        "terminated": R(func=envs_mdp.is_terminated, weight=-20.0),
    }

    cfg.terminations = {
        "time_out": TerminationTermCfg(func=envs_mdp.time_out, time_out=True),
        "fell_over": TerminationTermCfg(func=vel_mdp.bad_orientation,
                                        params={"limit_angle": math.radians(70.0)}),
        "fell_contact": TerminationTermCfg(func=vel_mdp.illegal_contact,
                                           params={"sensor_name": "fall_contact"}),
        "box_tipped": TerminationTermCfg(func=mdp.box_tipped),
        "box_lost": TerminationTermCfg(func=mdp.box_lost),
    }
    cfg.curriculum = {"push": CurriculumTermCfg(func=mdp.hard_curriculum)}
    cfg.viewer.distance = 6.0

    if play:
        import os

        cfg.curriculum = {}
        cfg.episode_length_s = 40.0
        cfg.commands["goal"].start_level = int(os.environ.get("QUADCOOP_PUSH_LEVEL", "3"))
        cfg.commands["goal"].replay_frac = 0.0
        only = os.environ.get("QUADCOOP_PUSH_OBJECT")
        if only:
            cfg.commands["goal"].only = only if only.startswith("obj_") else f"obj_{only}"
    return cfg