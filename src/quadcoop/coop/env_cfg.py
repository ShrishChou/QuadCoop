"""Two-robot environment: ANYmal C ("anymal") and Spot ("spot") push one object.

Each robot is driven exactly as in Stages 1-1b: a high-level (vx, vy, wz) action ->
its own frozen Stage 0 walker -> its 12 joints. The env action is the two high-level
actions side by side: (anymal vx, vy, wz, spot vx, vy, wz).

Observation groups (the trainer picks what each network sees):

    actor_anymal / actor_spot   per-robot policy input: Stage 1b's 42 numbers in that
                                robot's frame (same names, order and sizes, so a Stage 1b
                                policy drops in) + the partner's pose and velocity (6)
    state_anymal / state_spot   the same without observation noise (critics)
    privileged                  object mass, friction, level (critics only)
    walker_anymal / walker_spot the frozen walkers' inputs (not for the trainer)

Reward: one team reward (Stage 1b's object terms + each robot's approach terms, minus
action changes, robot-robot contact and terminations). Episodes end when either robot
falls (on its side / upside down / collapsed, quadcoop/falls.py), the object tips over
or is lost, or after 45 s.

Walker checkpoints: QUADCOOP_WALKER_CKPT_ANYMAL_C and QUADCOOP_WALKER_CKPT_SPOT
(train_coop.py sets them to the newest walker runs by default).
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

from quadcoop.coop import mdp
from quadcoop.coop.mdp import AGENTS
from quadcoop import falls
from quadcoop.robots.anymal_c import ROBOT as ANYMAL_C
from quadcoop.robots.spot import ROBOT as SPOT
from quadcoop.stage1 import mdp as s1
from quadcoop.stage1b import mdp as hb
from quadcoop.stage1b.shapes import NOMINAL_MASS, OBJ_NAMES, SHAPES, get_goal_cfgs, get_object_cfgs
from quadcoop.stage1c.env_cfg import UNIFORM_MASS
from quadcoop.walker_env_cfg import make_walker_env_cfg

SPECS = {"anymal": ANYMAL_C, "spot": SPOT}
# Approximate weights (N), for the effort measure only.
ROBOT_WEIGHT_N = {"anymal": 50.0 * 9.81, "spot": 32.7 * 9.81}
MASS_RANGE = (10.0, 120.0)  # kg per object per env (uniform); the level picks a window
FRICTION_RANGE = (0.4, 0.6)
EPISODE_S = 45.0
KEEP_EVENTS = ("foot_friction", "base_com", "encoder_bias", "reset_base", "reset_robot_joints")
START_OFFSET = {"anymal": (0.0, -2.0), "spot": (0.0, 2.0)}  # before the first reset places them


def _rename_entity(params: dict, name: str) -> dict:
    out = copy.deepcopy(params)
    for k, v in out.items():
        if isinstance(v, SceneEntityCfg) and v.name == "robot":
            v.name = name
        if k == "sensor_name" and isinstance(v, str) and v.startswith("robot/"):
            out[k] = f"{name}/" + v[len("robot/"):]
    return out


def _walker_group(wcfg: ManagerBasedRlEnvCfg, name: str) -> ObservationGroupCfg:
    """The frozen walker's input for robot `name`: its Stage 0 actor observation, re-pointed."""
    grp = copy.deepcopy(wcfg.observations["actor"])
    grp.terms.pop("height_scan", None)
    for tname, term in grp.terms.items():
        term.params = _rename_entity(term.params, name)
        if tname in ("projected_gravity", "joint_pos", "joint_vel"):
            term.params.setdefault("asset_cfg", SceneEntityCfg(name))
    grp.terms["actions"] = ObservationTermCfg(func=s1.walker_last_action, params={"action_name": f"walker_{name}"})
    grp.terms["command"] = ObservationTermCfg(func=envs_mdp.generated_commands,
                                              params={"command_name": f"twist_{name}"})
    return grp


def _agent_terms(name: str, other: str, noisy: bool) -> dict:
    """Stage 1b's actor terms (same names/order/sizes) for robot `name`, + the partner."""
    def nz(lim):
        return Unoise(n_min=-lim, n_max=lim) if noisy else None

    T = ObservationTermCfg
    return {
        "base_lin_vel": T(func=vel_mdp.builtin_sensor, params={"sensor_name": f"{name}/imu_lin_vel"}, noise=nz(0.1)),
        "base_ang_vel": T(func=vel_mdp.builtin_sensor, params={"sensor_name": f"{name}/imu_ang_vel"}, noise=nz(0.1)),
        "projected_gravity": T(func=vel_mdp.projected_gravity, params={"asset_cfg": SceneEntityCfg(name)}),
        "box": T(func=mdp.box_in_frame, params={"robot": name}, noise=nz(0.02)),
        "goal": T(func=mdp.goal_in_frame, params={"robot": name}, noise=nz(0.02)),
        "walker_command": T(func=mdp.walker_command_of, params={"twist_name": f"twist_{name}"}),
        "last_action": T(func=envs_mdp.last_action, params={"action_name": f"walker_{name}"}),
        "object_desc": T(func=hb.object_descriptor),
        "hold_progress": T(func=hb.hold_progress),
        "partner": T(func=mdp.partner_in_frame, params={"robot": name, "other": other}, noise=nz(0.05)),
    }


def make_coop_env_cfg(play: bool = False) -> ManagerBasedRlEnvCfg:
    wcfg = {a: make_walker_env_cfg(SPECS[a]) for a in AGENTS}
    cfg = wcfg["anymal"]  # sim, terrain and viewer settings; everything task-related is replaced

    # -- scene ------------------------------------------------------------------------------
    robots = {}
    for a in AGENTS:
        rc = SPECS[a].get_robot_cfg()
        x, y = START_OFFSET[a]
        rc.init_state = copy.deepcopy(rc.init_state)
        rc.init_state.pos = (x, y, rc.init_state.pos[2])
        robots[a] = rc
    cfg.scene.entities = {**robots, **get_object_cfgs(), **get_goal_cfgs()}
    sensors = []
    sensors.append(ContactSensorCfg(
        name="robots_touch",
        primary=ContactMatch(mode="subtree", pattern=SPECS["anymal"].base_body, entity="anymal"),
        secondary=ContactMatch(mode="subtree", pattern=SPECS["spot"].base_body, entity="spot"),
        fields=("found",), reduce="none", num_slots=1,
    ))
    cfg.scene.sensors = tuple(sensors)
    cfg.sim.njmax = 1500
    cfg.episode_length_s = EPISODE_S
    cfg.metrics = {}

    # -- actions: one high-level (vx, vy, wz) per robot -> its frozen walker -----------------
    joint_cfgs = {a: copy.deepcopy(wcfg[a].actions["joint_pos"]) for a in AGENTS}
    walker_groups = {a: _walker_group(wcfg[a], a) for a in AGENTS}
    walker_events = {a: copy.deepcopy(wcfg[a].events) for a in AGENTS}
    cfg.actions = {}
    for a in AGENTS:
        joint_cfg = joint_cfgs[a]
        joint_cfg.entity_name = a
        cfg.actions[f"walker_{a}"] = s1.WalkerCommandActionCfg(
            entity_name=a, joint_cfg=joint_cfg,
            checkpoint_env=f"QUADCOOP_WALKER_CKPT_{SPECS[a].name.upper()}",
            twist_name=f"twist_{a}", walker_obs_group=f"walker_{a}",
        )

    # -- commands ------------------------------------------------------------------------------
    cfg.commands = {f"twist_{a}": s1.HighLevelTwistCfg() for a in AGENTS}
    cfg.commands["goal"] = mdp.CoopGoalCommandCfg(reach=tuple(SPECS[a].half_length for a in AGENTS))

    # -- observations ----------------------------------------------------------------------------
    obs = {}
    for a, o in (("anymal", "spot"), ("spot", "anymal")):
        obs[f"actor_{a}"] = ObservationGroupCfg(terms=_agent_terms(a, o, noisy=True), concatenate_terms=True,
                                                enable_corruption=not play)
        obs[f"state_{a}"] = ObservationGroupCfg(terms=_agent_terms(a, o, noisy=False), concatenate_terms=True,
                                                enable_corruption=False)
        obs[f"walker_{a}"] = walker_groups[a]
    obs["privileged"] = ObservationGroupCfg(terms={"box_physics": ObservationTermCfg(func=hb.box_physics)},
                                            concatenate_terms=True, enable_corruption=False)
    cfg.observations = obs

    # -- events: each robot's walker randomization; objects' mass and friction --------------------
    events = {}
    for a in AGENTS:
        for k, ev in walker_events[a].items():
            if k not in KEEP_EVENTS:
                continue
            ev = copy.deepcopy(ev)
            ev.params = _rename_entity(ev.params, a)
            if k == "reset_base":
                ev.params["asset_cfg"] = SceneEntityCfg(a)
                ev.params["pose_range"] = {"x": (0.0, 0.0), "y": (0.0, 0.0), "z": (0.01, 0.03), "yaw": (0.0, 0.0)}
                ev.params["velocity_range"] = {}
            events[f"{k}_{a}"] = ev
    alpha = (0.5 * math.log(MASS_RANGE[0] / NOMINAL_MASS), 0.5 * math.log(MASS_RANGE[1] / NOMINAL_MASS))
    for name, shape in zip(OBJ_NAMES, SHAPES, strict=True):
        events[f"{name}_mass"] = EventTermCfg(
            mode="startup", func=envs_mdp.dr.pseudo_inertia,
            params={"alpha_range": alpha, "asset_cfg": SceneEntityCfg(name), "distribution": UNIFORM_MASS})
        if not shape.fixed_friction:
            events[f"{name}_friction"] = EventTermCfg(
                mode="startup", func=envs_mdp.dr.geom_friction,
                params={"asset_cfg": SceneEntityCfg(name, geom_names=(".*",)), "operation": "abs",
                        "ranges": FRICTION_RANGE, "shared_random": True})
    cfg.events = events

    # -- rewards: one team reward ------------------------------------------------------------------
    R = RewardTermCfg
    rewards = {
        "box_progress": R(func=hb.box_progress, weight=3.0),
        "box_near_goal": R(func=hb.box_near_goal, weight=1.0),
        "yaw_progress": R(func=hb.yaw_progress, weight=0.5),
        "yaw_aligned": R(func=hb.yaw_aligned, weight=1.0),
        "at_goal": R(func=hb.at_goal, weight=4.0),
        "held": R(func=hb.held, weight=2.0),
        "precise_pose": R(func=hb.precise_pose, weight=4.0),
        "box_settle": R(func=hb.box_settle, weight=-1.0),
        "box_runaway": R(func=hb.box_runaway, weight=-3.0),
        "robots_touch": R(func=mdp.robots_touching, weight=-0.5),
        "terminated": R(func=envs_mdp.is_terminated, weight=-20.0),
    }
    for k, a in enumerate(AGENTS):  # Stage 1b's per-robot terms, half weight each
        rewards[f"near_box_{a}"] = R(func=mdp.robot_near_box, weight=0.25,
                                     params={"robot": a, "reach": SPECS[a].half_length})
        rewards[f"behind_box_{a}"] = R(func=mdp.robot_behind_box, weight=0.15, params={"robot": a})
        rewards[f"action_rate_{a}"] = R(func=mdp.agent_action_rate, weight=-0.05, params={"agent": k})
    cfg.rewards = rewards

    # -- terminations ----------------------------------------------------------------------------
    cfg.terminations = {"time_out": TerminationTermCfg(func=envs_mdp.time_out, time_out=True)}
    for a in AGENTS:
        cfg.terminations[f"{a}_fell"] = TerminationTermCfg(
            func=falls.fallen, params={"asset_name": a, "nominal_height": SPECS[a].nominal_height})
    cfg.terminations["box_tipped"] = TerminationTermCfg(func=hb.box_tipped)
    cfg.terminations["box_lost"] = TerminationTermCfg(func=mdp.box_lost)
    cfg.curriculum = {"push": CurriculumTermCfg(func=hb.hard_curriculum)}

    cfg.viewer.body_name = None
    cfg.viewer.distance = 8.0
    cfg.viewer.elevation = -35.0

    if play:
        cfg.curriculum = {}
        cfg.episode_length_s = 60.0
        cfg.commands["goal"].start_level = int(os.environ.get("QUADCOOP_PUSH_LEVEL", "2"))
        cfg.commands["goal"].replay_frac = 0.0
        only = os.environ.get("QUADCOOP_PUSH_OBJECT")
        if only:
            cfg.commands["goal"].only = only if only.startswith("obj_") else f"obj_{only}"
    return cfg
