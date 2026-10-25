"""Stage 2 env: Stage 1b's push-to-pose task with object shape profiles.

Built from Stage 1b's config, so the robot, the frozen walker, the 42-number policy
observation and the reward terms are Stage 1b's (a Stage 1b policy warm-starts it).
Changes:

* objects: twelve shapes (seven trained, five held out), sizes randomized per env;
* policy input: the 42 numbers + profile images (variant "a": object-frame top + front;
  "b": robot-frame top + object-frame front; "ctrl": no images, same everything else);
* approach reward measured to the object's surface (``near_surface``) instead of its centre;
* shapes practised in proportion to how badly each is going;
* falls by body pose (quadcoop/falls.py), masses uniform in 5-40 kg, 45 s episodes,
  curriculum starting at level 3;
* optional (QUADCOOP_ACTION_FIX=1, off by default): actions kept inside the walker's range: the
  action-rate penalty and the last-action input use the clipped command, and outputs past the
  clip are penalized (``action_limit``);
* episode length QUADCOOP_EPISODE_S (default 45 s);
* optional (QUADCOOP_SUCCESS_MODE=terminate): end the episode on a precise, settled success,
  with a success bonus that decays with time;
* curriculum start level QUADCOOP_START_LEVEL (default 3 = warm start from Stage 1c; 0 = from scratch).

Rates: physics 200 Hz, policy and walker 50 Hz, robot-frame map ("b") 10 Hz by default
(``QUADCOOP_MAP_HZ``); object-frame images ("a") are fixed per episode.
"""

from __future__ import annotations

import math
import os

from mjlab.envs import mdp as envs_mdp
from mjlab.managers.curriculum_manager import CurriculumTermCfg
from mjlab.managers.event_manager import EventTermCfg
from mjlab.managers.observation_manager import ObservationGroupCfg, ObservationTermCfg
from mjlab.managers.reward_manager import RewardTermCfg
from mjlab.managers.scene_entity_config import SceneEntityCfg
from mjlab.managers.termination_manager import TerminationTermCfg
from mjlab.utils.noise import UniformNoiseCfg as Unoise

from quadcoop import falls
from quadcoop.robots.spec import RobotSpec
from quadcoop.stage1 import mdp as s1
from quadcoop.stage1.push_env_cfg import make_push_env_cfg
from quadcoop.stage1b import mdp as hb
from quadcoop.stage1b.shapes import NOMINAL_MASS
from quadcoop.stage1c.env_cfg import UNIFORM_MASS
from quadcoop.stage2 import mdp
from quadcoop.stage2.shapes import FACTOR_RANGE, OBJ_NAMES2, SHAPES2, get_goal_cfgs, get_object_cfgs

MASS_RANGE = (5.0, 40.0)
FRICTION_RANGE = (0.4, 0.6)
EPISODE_S = float(os.environ.get("QUADCOOP_EPISODE_S", "45"))  # training episode length (s)
# QUADCOOP_ACTION_FIX=1: clipped last-action input + clipped action-rate penalty + penalty on
# outputs past the walker's clip. Off by default: the policies trained so far saw the raw last
# action, and evaluating them with a different input changes their behaviour.
ACTION_FIX = os.environ.get("QUADCOOP_ACTION_FIX", "0") == "1"
# QUADCOOP_SUCCESS_MODE=terminate: success = within 10 cm / 3 deg with the object at rest
# (QUADCOOP_SUCCESS_POS / QUADCOOP_SUCCESS_YAW override), the episode then ends and a new one
# starts; reward = potential-based progress + a success bonus that shrinks the later it comes,
# with no reward for lingering near the goal. Default "hold" = the original Stage 1b rule.
SUCCESS_MODE = os.environ.get("QUADCOOP_SUCCESS_MODE", "hold")
BONUS = float(os.environ.get("QUADCOOP_GOAL_BONUS", "50"))  # bonus for an immediate success
# curriculum level a new run starts at: 3 for runs warm-started from Stage 1c (the default),
# 0 for runs trained from scratch (QUADCOOP_START_LEVEL=0). On resume the saved level is restored
# (Push2Runner), so this only matters for the first job of a run.
START_LEVEL = int(os.environ.get("QUADCOOP_START_LEVEL", "3"))
VARIANTS = ("a", "b", "ctrl")


def make_push2_env_cfg(robot: RobotSpec, variant: str, play: bool = False):
    assert variant in VARIANTS, variant
    cfg = make_push_env_cfg(robot, play=play)  # robot, walker, walker observation, robot events
    cfg.scene.entities = {"robot": cfg.scene.entities["robot"], **get_object_cfgs(), **get_goal_cfgs()}
    cfg.sim.njmax = 900
    cfg.episode_length_s = EPISODE_S

    cfg.commands["goal"] = mdp.Push2CommandCfg(
        robot_reach=robot.half_length, variant=variant,
        map_hz=float(os.environ.get("QUADCOOP_MAP_HZ", "10")), start_level=START_LEVEL,
        success_mode=SUCCESS_MODE,
        success_pos_tol=float(os.environ.get("QUADCOOP_SUCCESS_POS", "0.10")),
        success_yaw_tol_deg=float(os.environ.get("QUADCOOP_SUCCESS_YAW", "3")))

    # -- events --------------------------------------------------------------------------
    cfg.events = {k: v for k, v in cfg.events.items() if not k.startswith("box_")}
    alpha = (0.5 * math.log(MASS_RANGE[0] / NOMINAL_MASS), 0.5 * math.log(MASS_RANGE[1] / NOMINAL_MASS))
    for name, shape in zip(OBJ_NAMES2, SHAPES2, strict=True):
        cfg.events[f"{name}_mass"] = EventTermCfg(
            mode="startup", func=envs_mdp.dr.pseudo_inertia,
            params={"alpha_range": alpha, "asset_cfg": SceneEntityCfg(name), "distribution": UNIFORM_MASS})
        if not shape.fixed_friction:
            cfg.events[f"{name}_friction"] = EventTermCfg(
                mode="startup", func=envs_mdp.dr.geom_friction,
                params={"asset_cfg": SceneEntityCfg(name, geom_names=(".*",)), "operation": "abs",
                        "ranges": FRICTION_RANGE, "shared_random": True})
    cfg.events["object_geometry"] = EventTermCfg(
        mode="startup", func=mdp.randomize_geometry, params={"factor_range": FACTOR_RANGE})

    # -- observations: Stage 1b's 42 (same names/order/sizes) + images --------------------------
    T = ObservationTermCfg
    hl = {
        "base_lin_vel": cfg.observations["actor"].terms["base_lin_vel"],
        "base_ang_vel": cfg.observations["actor"].terms["base_ang_vel"],
        "projected_gravity": cfg.observations["actor"].terms["projected_gravity"],
        "box": T(func=mdp.box_obs, noise=Unoise(n_min=-0.02, n_max=0.02)),
        "goal": T(func=hb.goal_in_robot_frame, noise=Unoise(n_min=-0.02, n_max=0.02)),
        "walker_command": T(func=s1.walker_command),
        "last_action": T(func=mdp.last_action_clipped if ACTION_FIX else envs_mdp.last_action),
        "object_desc": T(func=mdp.object_desc),
        "hold_progress": T(func=hb.hold_progress),
    }
    critic = {**{k: T(func=v.func, params=dict(v.params)) for k, v in hl.items()},
              "box_physics": T(func=hb.box_physics)}
    walker = cfg.observations["walker"]
    cfg.observations = {
        "actor": ObservationGroupCfg(terms=hl, concatenate_terms=True, enable_corruption=not play),
        "critic": ObservationGroupCfg(terms=critic, concatenate_terms=True, enable_corruption=False),
        "walker": walker,
    }
    if variant != "ctrl":
        cfg.observations["profile_top"] = ObservationGroupCfg(
            terms={"top": T(func=mdp.profile_top)}, concatenate_terms=True, enable_corruption=False)
        cfg.observations["profile_front"] = ObservationGroupCfg(
            terms={"front": T(func=mdp.profile_front)}, concatenate_terms=True, enable_corruption=False)

    # -- rewards: Stage 1b's, with the approach term measured to the object's surface ---------
    R = RewardTermCfg
    cfg.rewards = {
        "box_progress": R(func=hb.box_progress, weight=3.0),
        "box_near_goal": R(func=hb.box_near_goal, weight=1.0),
        "yaw_progress": R(func=hb.yaw_progress, weight=0.5),
        "yaw_aligned": R(func=hb.yaw_aligned, weight=1.0),
        "near_surface": R(func=mdp.near_surface, weight=0.5),
        "robot_behind_box": R(func=hb.robot_behind_box, weight=0.3),
        "at_goal": R(func=hb.at_goal, weight=4.0),
        "held": R(func=hb.held, weight=2.0),
        "precise_pose": R(func=hb.precise_pose, weight=4.0),
        "box_settle": R(func=hb.box_settle, weight=-1.0),
        "box_runaway": R(func=hb.box_runaway, weight=-3.0),
        "action_rate": R(func=mdp.action_rate_clipped if ACTION_FIX else s1.hl_action_rate, weight=-0.05),
        "terminated": R(func=envs_mdp.is_terminated, weight=-20.0),
    }
    if ACTION_FIX:
        cfg.rewards["action_limit"] = R(func=mdp.action_beyond_limit, weight=-0.1)
    if SUCCESS_MODE == "terminate":
        # rewards for being near / at / held at the goal would pay for lingering instead of
        # finishing; replace them by a potential (precise_progress) and the success bonus
        for k in ("box_near_goal", "yaw_aligned", "at_goal", "held", "precise_pose"):
            cfg.rewards.pop(k)
        cfg.rewards["precise_progress"] = R(func=mdp.precise_progress, weight=4.0)
        # rewards are multiplied by the step length, so the weight is bonus / dt
        step_dt = cfg.sim.mujoco.timestep * cfg.decimation
        cfg.rewards["goal_bonus"] = R(func=mdp.goal_bonus, weight=BONUS / step_dt,
                                      params={"horizon_s": EPISODE_S})
        # a fall / tip / loss costs half an immediate success (the old -20 weight was scaled
        # by the step length too, i.e. only -0.4, negligible next to a 50-point bonus)
        cfg.rewards["terminated"] = R(func=mdp.failed, weight=-0.5 * BONUS / step_dt)
    cfg.terminations = {
        "time_out": TerminationTermCfg(func=envs_mdp.time_out, time_out=True),
        "fell_over": TerminationTermCfg(func=falls.fallen, params={"asset_name": "robot",
                                                                   "nominal_height": robot.nominal_height}),
        "box_tipped": TerminationTermCfg(func=hb.box_tipped),
        "box_lost": TerminationTermCfg(func=hb.box_lost),
    }
    if SUCCESS_MODE == "terminate":
        cfg.terminations["goal_reached"] = TerminationTermCfg(func=mdp.goal_reached)
    cfg.curriculum = {"push": CurriculumTermCfg(func=mdp.push2_curriculum)}
    cfg.viewer.distance = 6.0

    if play:
        cfg.curriculum = {}
        cfg.episode_length_s = 40.0
        cfg.commands["goal"].start_level = int(os.environ.get("QUADCOOP_PUSH_LEVEL", "5"))
        cfg.commands["goal"].replay_frac = 0.0
        only = os.environ.get("QUADCOOP_PUSH_OBJECT")
        if only:
            cfg.commands["goal"].only = only if only.startswith("obj_") else f"obj_{only}"
            cfg.commands["goal"].allow_heldout = True
    return cfg
