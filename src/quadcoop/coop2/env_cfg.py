"""Two-robot environment on Stage 2: ANYmal C ("anymal") and Spot ("spot") push one object.

Which two robots is set by QUADCOOP_PAIR (quadcoop/coop2/pairs.py): "mixed" (default, as above),
"anymal" (two ANYmal C, entities "anymal1"/"anymal2") or "spot" (two Spot). Everything below
applies per robot slot.

Each robot is driven exactly as in Stage 2: a high-level (vx, vy, wz) action -> its own frozen
walker -> its 12 joints. The env action is (anymal vx, vy, wz, spot vx, vy, wz).

Observation groups (the trainer picks what each network sees):

    actor_<robot>   Stage 2's 42 numbers in that robot's frame (same terms, order and noise, so
                    a Stage 2 policy drops in) + the partner (9): its pose and velocity in this
                    robot's frame and the command it last sent its walker
    state_<robot>   the same without noise (critics)
    top_<robot>     that robot's robot-frame top map (variant "b"; Stage 2b's profile_top)
    front           the object-frame front profile (Stage 2b's profile_front; same for both)
    privileged      object mass, friction, level (critics only; Stage 2's box_physics)
    walker_<robot>  the frozen walkers' inputs (not for the trainer)

With ``contacts`` (Stage 4) actor_ / state_<robot> end with 9 more numbers: the robot's assigned
contact and its partner's (quadcoop/coop2/mdp.py contact_obs), and each robot has an
off-contact termination (a failure, like a fall) with its own penalty.

Reward = Stage 2's terminate-rule reward split into
  team terms (both robots get them): object progress, yaw progress, precise progress, the
    time-decaying success bonus, settle / runaway penalties, -25 for a failure (either robot
    falls, the object tips or is lost), and two new ones: robots too close, robots touching;
  per-robot terms (names end in _anymal / _spot; the trainer gives each robot its own):
    Stage 2's surface approach and behind-the-object terms, the action rate of the command the
    walker actually gets (clipped) with a small penalty on outputs past the clip, and two new
    ones: pushing along the object -> goal direction while at the object, and an extra penalty
    for its own fall.
At iteration 0 each robot's reward is exactly its Stage 2 reward (plus the two small new
terms), so the warm-started policies (and IPPO's warm-started critics) start in familiar units.

Walker checkpoints: QUADCOOP_WALKER_CKPT_ANYMAL_C / QUADCOOP_WALKER_CKPT_SPOT; their history
lengths: QUADCOOP_WALKER_HISTORY_ANYMAL_C / _SPOT (train_coop2.py sets all four from
evals/models.yaml). Spot's joint gains follow QUADCOOP_SPOT_PROFILE (set before import).
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

from quadcoop import falls
from quadcoop.coop2 import mdp
from quadcoop.coop2.mdp import AGENTS, PARTNER
from quadcoop.coop2.pairs import ROBOT_TYPE
from quadcoop.robots.anymal_c import ROBOT as ANYMAL_C
from quadcoop.robots.spot import ROBOT as SPOT
from quadcoop.stage1 import mdp as s1
from quadcoop.stage1b import mdp as hb
from quadcoop.stage1b.shapes import NOMINAL_MASS
from quadcoop.stage1c.env_cfg import UNIFORM_MASS
from quadcoop.stage2 import mdp as m2
from quadcoop.stage2.shapes import FACTOR_RANGE, OBJ_NAMES2, SHAPES2, get_goal_cfgs, get_object_cfgs
from quadcoop.walker_env_cfg import make_walker_env_cfg

SPECS = {a: {"anymal_c": ANYMAL_C, "spot": SPOT}[ROBOT_TYPE[a]] for a in AGENTS}  # per slot (QUADCOOP_PAIR)
MASS_RANGE = (10.0, 90.0)  # kg per object copy per env (uniform); the level picks a window
FRICTION_RANGE = (0.4, 0.6)  # Stage 2's
EPISODE_S = float(os.environ.get("QUADCOOP_COOP_EPISODE_S", "80"))
BONUS = 50.0  # Stage 2's success bonus (for an immediate success)
KEEP_EVENTS = ("foot_friction", "base_com", "encoder_bias", "reset_base", "reset_robot_joints")
START_OFFSET = {AGENTS[0]: (0.0, -2.0), AGENTS[1]: (0.0, 2.0)}  # before the first reset places them


def _rename_entity(params: dict, name: str) -> dict:
    out = copy.deepcopy(params)
    for k, v in out.items():
        if isinstance(v, SceneEntityCfg) and v.name == "robot":
            v.name = name
        if k == "sensor_name" and isinstance(v, str) and v.startswith("robot/"):
            out[k] = f"{name}/" + v[len("robot/"):]
    return out


def _walker_group(wcfg: ManagerBasedRlEnvCfg, name: str) -> ObservationGroupCfg:
    """Robot `name`'s frozen-walker input: its walker's actor observation, re-pointed at the
    robot (history settings kept)."""
    grp = copy.deepcopy(wcfg.observations["actor"])
    grp.terms.pop("height_scan", None)
    for tname, term in grp.terms.items():
        term.params = _rename_entity(term.params, name)
        if tname in ("projected_gravity", "joint_pos", "joint_vel"):
            term.params.setdefault("asset_cfg", SceneEntityCfg(name))
    old = grp.terms["actions"]
    grp.terms["actions"] = ObservationTermCfg(func=s1.walker_last_action, params={"action_name": f"walker_{name}"},
                                              history_length=old.history_length,
                                              flatten_history_dim=old.flatten_history_dim)
    grp.terms["command"] = ObservationTermCfg(func=envs_mdp.generated_commands,
                                              params={"command_name": f"twist_{name}"})
    return grp


def _agent_terms(name: str, other: str, noisy: bool, contacts: bool = False) -> dict:
    """Stage 2's 42 actor terms (names, order, sizes, noise) for robot `name`, + the partner
    (+ the assigned contacts in contact mode)."""
    def nz(lim):
        return Unoise(n_min=-lim, n_max=lim) if noisy else None

    T = ObservationTermCfg
    return {
        "base_lin_vel": T(func=vel_mdp.builtin_sensor, params={"sensor_name": f"{name}/imu_lin_vel"}, noise=nz(0.1)),
        "base_ang_vel": T(func=vel_mdp.builtin_sensor, params={"sensor_name": f"{name}/imu_ang_vel"}, noise=nz(0.1)),
        "projected_gravity": T(func=vel_mdp.projected_gravity, params={"asset_cfg": SceneEntityCfg(name)}),
        "box": T(func=mdp.box_obs, params={"robot": name}, noise=nz(0.02)),
        "goal": T(func=mdp.goal_obs, params={"robot": name}, noise=nz(0.02)),
        "walker_command": T(func=mdp.walker_command_of, params={"twist_name": f"twist_{name}"}),
        "last_action": T(func=envs_mdp.last_action, params={"action_name": f"walker_{name}"}),
        "object_desc": T(func=m2.object_desc),
        "hold_progress": T(func=hb.hold_progress),
        "partner": T(func=mdp.partner_obs, params={"robot": name, "other": other, "other_action": f"walker_{other}"},
                     noise=nz(0.05)),
        **({"contact": T(func=mdp.contact_obs, params={"robot": name}, noise=nz(0.02))} if contacts else {}),
    }


def walker_history(robot_name: str) -> int:
    return int(float(os.environ.get(f"QUADCOOP_WALKER_HISTORY_{robot_name.upper()}", "0")))


REWARD_SETS = ("r3", "r4", "r5", "r7", "r8")
GOAL_ERROR_COST = 0.25  # r7: per second at the start error (distance fraction 1 + heading fraction)


def make_coop2_env_cfg(variant: str = "b", play: bool = False, partner_map: bool = False,
                       reward_set: str = "r3", start_mode: str = "behind", need_frac: float = 0.0,
                       need_mass: float = 45.0, contacts: bool = False, tol_levels: tuple = (),
                       contact_mix: tuple = (1.0, 1.0, 1.0), contact_start_at: float = 0.7) -> ManagerBasedRlEnvCfg:
    """partner_map: each robot's top map gets a second channel with the partner's footprint.
    reward_set:
      "r3" first runs.
      "r4" no per-robot "behind the object" term (it sent both robots to the same spot); proximity
           penalty exponential below 0.6 m instead of linear from 1 m (which punished pushing
           side by side).
      "r5" r4, plus: the surface-approach reward pays for getting closer (potential-based, weight 2)
           instead of 0.5/s for standing there (camping paid each robot up to 40 per episode,
           more than a whole successful push); a team time cost of 0.2/s (running out of time
           was free); push_along 0.3 -> 1.0 (the only per-robot credit for pushing);
           yaw_progress 0.5 -> 1.0 (turning objects).
      "r7" outcome-based: every dense term measures the object against its goal, plus one
           credit-assignment term; everything else is an outcome cost.
           - goal-error cost (team, 0.25/s x [distance / start distance + heading error / max
             heading error]): the area under the error curve, so faster and more direct pushing
             and no needless turning cost less; replaces r5's flat time cost;
           - a failure also pays that cost for the time left (failing early is never cheaper);
           - push_credit (per robot) replaces push_along: the object's speed toward the goal,
             credited while the robot's front is on the object and it is behind it (push_along
             paid the robot's own speed near the object: walking past the object toward the goal
             earned more than pushing a heavy one);
           - proximity on the gap between the bodies (exponential below 0.15 m) instead of the
             centre distance (which was ~0.6 m shoulder to shoulder, where r4's penalty was ~0);
           - kept from r5: object / heading / precise progress (potential-based), the success
             bonus, settle / runaway, failure -25, robots touching, approach (potential-based),
             action terms, own fall.
      "r8" r7 for cooperation: work_credit (per robot, weight 3) replaces push_credit: each robot's
           contact force on the object along the goal direction (contact sensors robot <-> object)
           x the object's speed toward the goal, so a robot earns only for the work it does, and
           two pushers share it by effort; no body-gap proximity cost (shoulder to shoulder is
           free), only actual contact between the robots is penalized (robots_touch).
    start_mode: "behind" (level table) or "around" (anywhere around the object; training only).
    need_frac / need_mass: share of training episodes with a wide object above need_mass kg.
    contacts: Stage 4 contact mode (assigned contacts, contact inputs, off-contact failure);
    contact_mix (spread, adjacent, random) and contact_start_at: see CoopPush2CommandCfg.
    tol_levels: success-tolerance curriculum ((pos m, yaw deg), ...), loose -> fine; () = fixed."""
    assert variant in ("b", "ctrl"), variant
    assert reward_set in REWARD_SETS, reward_set
    assert not (partner_map and variant != "b"), "the partner map needs variant b (maps)"
    wcfg = {a: make_walker_env_cfg(SPECS[a], history=walker_history(SPECS[a].name)) for a in AGENTS}
    cfg = wcfg[AGENTS[0]]  # sim, terrain and viewer settings; everything task-related is replaced

    # -- scene: two robots, the Stage 2 objects and goal markers, a robot-robot contact sensor --
    robots = {}
    for a in AGENTS:
        rc = SPECS[a].get_robot_cfg()
        x, y = START_OFFSET[a]
        rc.init_state = copy.deepcopy(rc.init_state)
        rc.init_state.pos = (x, y, rc.init_state.pos[2])
        robots[a] = rc
    cfg.scene.entities = {**robots, **get_object_cfgs(), **get_goal_cfgs()}
    cfg.scene.sensors = (ContactSensorCfg(
        name="robots_touch",
        primary=ContactMatch(mode="subtree", pattern=SPECS[AGENTS[0]].base_body, entity=AGENTS[0]),
        secondary=ContactMatch(mode="subtree", pattern=SPECS[AGENTS[1]].base_body, entity=AGENTS[1]),
        fields=("found",), reduce="none", num_slots=1,
    ),)
    if reward_set == "r8":  # contact force between each robot and the object (work_credit)
        cfg.scene.sensors += tuple(ContactSensorCfg(
            name=f"push_{a}",
            primary=ContactMatch(mode="body", pattern=tuple(f"{o}/body" for o in OBJ_NAMES2)),
            secondary=ContactMatch(mode="subtree", pattern=SPECS[a].base_body, entity=a),
            fields=("found", "force"), reduce="netforce", num_slots=1,
        ) for a in AGENTS)
    cfg.sim.njmax = 1500
    cfg.episode_length_s = EPISODE_S
    cfg.metrics = {}

    # -- actions: one high-level (vx, vy, wz) per robot -> its frozen walker -------------------------
    joint_cfgs = {a: copy.deepcopy(wcfg[a].actions["joint_pos"]) for a in AGENTS}
    walker_groups = {a: _walker_group(wcfg[a], a) for a in AGENTS}
    walker_events = {a: copy.deepcopy(wcfg[a].events) for a in AGENTS}
    cfg.actions = {}
    for a in AGENTS:
        joint_cfgs[a].entity_name = a
        cfg.actions[f"walker_{a}"] = s1.WalkerCommandActionCfg(
            entity_name=a, joint_cfg=joint_cfgs[a],
            checkpoint_env=f"QUADCOOP_WALKER_CKPT_{SPECS[a].name.upper()}",
            twist_name=f"twist_{a}", walker_obs_group=f"walker_{a}",
        )

    # -- commands ---------------------------------------------------------------------------------
    cfg.commands = {f"twist_{a}": s1.HighLevelTwistCfg() for a in AGENTS}
    cfg.commands["goal"] = mdp.CoopPush2CommandCfg(
        variant=variant, reach=tuple(SPECS[a].half_length for a in AGENTS), robot_reach=SPECS[AGENTS[0]].half_length,
        map_hz=float(os.environ.get("QUADCOOP_MAP_HZ", "10")), start_level=0, success_mode="terminate",
        partner_map=partner_map, track_approach=reward_set in ("r5", "r7", "r8"),
        start_mode=start_mode, need_frac=need_frac, need_mass=need_mass,
        contact_mode=contacts, contact_mix=tuple(contact_mix), contact_start_at=contact_start_at,
        tol_levels=tuple(tuple(x) for x in tol_levels))

    # -- observations -------------------------------------------------------------------------------
    T = ObservationTermCfg
    obs = {}
    for a, o in PARTNER.items():
        obs[f"actor_{a}"] = ObservationGroupCfg(terms=_agent_terms(a, o, noisy=True, contacts=contacts),
                                                concatenate_terms=True, enable_corruption=not play)
        obs[f"state_{a}"] = ObservationGroupCfg(terms=_agent_terms(a, o, noisy=False, contacts=contacts),
                                                concatenate_terms=True, enable_corruption=False)
        if variant == "b":
            obs[f"top_{a}"] = ObservationGroupCfg(terms={"top": T(func=mdp.top_map, params={"robot": a})},
                                                  concatenate_terms=True, enable_corruption=False)
        obs[f"walker_{a}"] = walker_groups[a]
    if variant == "b":
        obs["front"] = ObservationGroupCfg(terms={"front": T(func=m2.profile_front)}, concatenate_terms=True,
                                           enable_corruption=False)
    obs["privileged"] = ObservationGroupCfg(terms={"box_physics": T(func=hb.box_physics)},
                                            concatenate_terms=True, enable_corruption=False)
    cfg.observations = obs

    # -- events: each robot's walker randomization; object geometry, mass and friction -------------
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
            if k == "foot_friction":  # Stage 1/2: enough grip to push heavy objects
                ev.params["ranges"] = (0.6, 1.2)
            events[f"{k}_{a}"] = ev
    alpha = (0.5 * math.log(MASS_RANGE[0] / NOMINAL_MASS), 0.5 * math.log(MASS_RANGE[1] / NOMINAL_MASS))
    for name, shape in zip(OBJ_NAMES2, SHAPES2, strict=True):
        events[f"{name}_mass"] = EventTermCfg(
            mode="startup", func=envs_mdp.dr.pseudo_inertia,
            params={"alpha_range": alpha, "asset_cfg": SceneEntityCfg(name), "distribution": UNIFORM_MASS})
        if not shape.fixed_friction:
            events[f"{name}_friction"] = EventTermCfg(
                mode="startup", func=envs_mdp.dr.geom_friction,
                params={"asset_cfg": SceneEntityCfg(name, geom_names=(".*",)), "operation": "abs",
                        "ranges": FRICTION_RANGE, "shared_random": True})
    events["object_geometry"] = EventTermCfg(mode="startup", func=m2.randomize_geometry,
                                             params={"factor_range": FACTOR_RANGE})
    cfg.events = events

    # -- rewards ------------------------------------------------------------------------------------
    R = RewardTermCfg
    step_dt = cfg.sim.mujoco.timestep * cfg.decimation
    fails = tuple(f"{a}_fell" for a in AGENTS) + ("box_tipped", "box_lost") + \
        (tuple(f"{a}_off_contact" for a in AGENTS) if contacts else ())
    rewards = {
        # team (Stage 2, terminate rule)
        "box_progress": R(func=hb.box_progress, weight=3.0),
        "yaw_progress": R(func=hb.yaw_progress, weight=1.0 if reward_set in ("r5", "r7", "r8") else 0.5),
        "precise_progress": R(func=m2.precise_progress, weight=4.0),
        "goal_bonus": R(func=m2.goal_bonus, weight=BONUS / step_dt, params={"horizon_s": EPISODE_S}),
        "box_settle": R(func=hb.box_settle, weight=-1.0),
        "box_runaway": R(func=hb.box_runaway, weight=-3.0),
        "terminated": R(func=m2.failed, weight=-0.5 * BONUS / step_dt, params={"names": fails}),
        # team (new): keep out of each other's way
        "robots_close": (R(func=mdp.robots_close, weight=-1.0) if reward_set == "r3" else
                         R(func=mdp.robots_gap_exp, weight=-1.0, params={"threshold": 0.15, "rate": 20.0})
                         if reward_set == "r7" else
                         R(func=mdp.robots_close_exp, weight=-1.0, params={"threshold": 0.6, "rate": 8.0})),
        "robots_touch": R(func=mdp.robots_touching, weight=-1.0),
    }
    if reward_set == "r5":
        rewards["time_cost"] = R(func=mdp.time_cost, weight=-0.2)
    if reward_set == "r8":
        rewards.pop("robots_close")  # only actual contact counts (robots_touch)
    if reward_set in ("r7", "r8"):
        rewards["goal_error"] = R(func=mdp.goal_error, weight=-GOAL_ERROR_COST)
        rewards["fail_remaining"] = R(func=mdp.failed_remaining, weight=-GOAL_ERROR_COST,
                                      params={"names": fails, "horizon_s": EPISODE_S})
    for k, a in enumerate(AGENTS):
        if reward_set in ("r5", "r7", "r8"):
            rewards[f"approach_{a}"] = R(func=mdp.approach, weight=2.0, params={"robot": a})
        else:
            rewards[f"near_surface_{a}"] = R(func=mdp.near_surface, weight=0.5, params={"robot": a})
        if reward_set == "r3":
            rewards[f"behind_box_{a}"] = R(func=mdp.behind_box, weight=0.3, params={"robot": a})
        rewards[f"action_rate_{a}"] = R(func=mdp.agent_action_rate, weight=-0.05, params={"agent": k})
        rewards[f"action_limit_{a}"] = R(func=mdp.agent_action_limit, weight=-0.02, params={"agent": k})
        if reward_set == "r8":
            rewards[f"work_credit_{a}"] = R(func=mdp.work_credit, weight=3.0, params={"robot": a})
        elif reward_set == "r7":
            rewards[f"push_credit_{a}"] = R(func=mdp.push_credit, weight=1.0, params={"robot": a})
        else:
            rewards[f"push_along_{a}"] = R(func=mdp.push_along, weight=1.0 if reward_set == "r5" else 0.3,
                                           params={"robot": a})
        rewards[f"own_fall_{a}"] = R(func=mdp.own_fall, weight=-0.2 * BONUS / step_dt,
                                     params={"robot": a, "nominal_height": SPECS[a].nominal_height})
        if contacts:  # leaving its contact costs the robot that left as much as its own fall
            rewards[f"own_off_contact_{a}"] = R(func=mdp.own_off_contact, weight=-0.2 * BONUS / step_dt,
                                                params={"robot": a})
    cfg.rewards = rewards

    # -- terminations ----------------------------------------------------------------------------------
    cfg.terminations = {"time_out": TerminationTermCfg(func=envs_mdp.time_out, time_out=True)}
    for a in AGENTS:
        cfg.terminations[f"{a}_fell"] = TerminationTermCfg(
            func=falls.fallen, params={"asset_name": a, "nominal_height": SPECS[a].nominal_height})
    cfg.terminations["box_tipped"] = TerminationTermCfg(func=hb.box_tipped)
    cfg.terminations["box_lost"] = TerminationTermCfg(func=mdp.box_lost)
    cfg.terminations["goal_reached"] = TerminationTermCfg(func=m2.goal_reached)
    cfg.terminations["unstable"] = TerminationTermCfg(func=mdp.unstable)  # sim glitch: ends, no penalty
    if contacts:
        for a in AGENTS:
            cfg.terminations[f"{a}_off_contact"] = TerminationTermCfg(func=mdp.off_contact, params={"robot": a})
    cfg.curriculum = {"push": CurriculumTermCfg(func=mdp.contact_curriculum if tol_levels else m2.push2_curriculum)}

    cfg.viewer.body_name = None
    cfg.viewer.distance = 8.0
    cfg.viewer.elevation = -35.0
    if play:
        cfg.curriculum = {}
        cfg.commands["goal"].start_level = int(os.environ.get("QUADCOOP_PUSH_LEVEL", "4"))
        cfg.commands["goal"].replay_frac = 0.0
        cfg.commands["goal"].tol_start_finest = True
        cfg.commands["goal"].contact_start_at = 1.0
    return cfg
