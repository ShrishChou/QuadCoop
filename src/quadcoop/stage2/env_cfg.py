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
  curriculum starting at level 3.

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
EPISODE_S = 45.0
START_LEVEL = 3
VARIANTS = ("a", "b", "ctrl")


def make_push2_env_cfg(robot: RobotSpec, variant: str, play: bool = False):
    assert variant in VARIANTS, variant
    cfg = make_push_env_cfg(robot, play=play)  # robot, walker, walker observation, robot events
    cfg.scene.entities = {"robot": cfg.scene.entities["robot"], **get_object_cfgs(), **get_goal_cfgs()}
    cfg.sim.njmax = 900
    cfg.episode_length_s = EPISODE_S

    cfg.commands["goal"] = mdp.Push2CommandCfg(
        robot_reach=robot.half_length, variant=variant,
        map_hz=float(os.environ.get("QUADCOOP_MAP_HZ", "10")), start_level=START_LEVEL)

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
        "last_action": T(func=envs_mdp.last_action),
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
        "action_rate": R(func=s1.hl_action_rate, weight=-0.05),
        "terminated": R(func=envs_mdp.is_terminated, weight=-20.0),
    }
    cfg.terminations = {
        "time_out": TerminationTermCfg(func=envs_mdp.time_out, time_out=True),
        "fell_over": TerminationTermCfg(func=falls.fallen, params={"asset_name": "robot",
                                                                   "nominal_height": robot.nominal_height}),
        "box_tipped": TerminationTermCfg(func=hb.box_tipped),
        "box_lost": TerminationTermCfg(func=hb.box_lost),
    }
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
