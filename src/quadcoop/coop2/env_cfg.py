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
evals/models.yaml; QUADCOOP_WALKER_OVERRIDE_<ROBOT>=<model.pt> replaces the walker for a test).
Spot's joint gains follow QUADCOOP_SPOT_PROFILE (set before import). Each walker's kind (see
walker_kind): 'v1' (velocity walker) or 'compliant' (walker v2 / v2.1 / v2.2: two more inputs, the
contact force from objects, wired to this robot's push_<robot> sensor).
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
    if "bumper_force" in grp.terms:  # compliant walker: the contact force from objects on this robot,
        # robot yaw frame, / 200 N, from its push_<robot> sensor (objects only: the partner and the
        # ground are not in it, as in training), nothing synthetic added
        t = grp.terms["bumper_force"]
        t.params = {**t.params, "sensor_name": f"push_{name}", "entity": name, "felt_load_term": None}
    return grp


def _agent_terms(name: str, other: str, noisy: bool, contacts: bool = False, guide: bool = False,
                 push_cmd: bool = False, exec_v2: bool = False, effort: bool = False,
                 contact_sense: bool = False) -> dict:
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
        **({"guide": T(func=mdp.guide_obs, params={"robot": name}, noise=nz(0.02))} if guide else {}),
        **({"push": T(func=mdp.push_obs, params={"robot": name}, noise=nz(0.02))} if push_cmd else {}),
        **({"cmd": T(func=mdp.cmd_obs, params={"robot": name})} if exec_v2 else {}),
        **({"effort": T(func=mdp.effort_obs, params={"robot": name}, noise=nz(0.02))} if effort else {}),
        **({"contact_sense": T(func=mdp.contact_sense_obs, params={"robot": name}, noise=nz(0.02))} if contact_sense else {}),
        # new terms go last: init_from widens at the end
    }


def walker_history(robot_name: str) -> int:
    return int(float(os.environ.get(f"QUADCOOP_WALKER_HISTORY_{robot_name.upper()}", "0")))


def walker_kind(robot_name: str) -> str:
    """'v1' or 'compliant'. QUADCOOP_WALKER_KIND_<ROBOT> = v1 | compliant | auto (default). auto: the
    walker's training config (params/env.yaml next to the checkpoint) has the contact-force input
    (bumper_force) -> compliant; without that file, a first layer with 50 inputs on ANYmal C ->
    compliant (v1 has 48)."""
    kind = os.environ.get(f"QUADCOOP_WALKER_KIND_{robot_name.upper()}", "auto")
    if kind in ("v1", "compliant"):
        return kind
    assert kind == "auto", f"QUADCOOP_WALKER_KIND_{robot_name.upper()}={kind}: use v1, compliant or auto"
    path = os.environ.get(f"QUADCOOP_WALKER_CKPT_{robot_name.upper()}", "")
    if not path or not os.path.exists(path):
        return "v1"
    yml = os.path.join(os.path.dirname(os.path.abspath(path)), "params", "env.yaml")
    if os.path.exists(yml):
        return "compliant" if "bumper_force" in open(yml).read() else "v1"
    import torch

    sd = torch.load(path, map_location="cpu", weights_only=False)
    sd = sd.get("actor_state_dict", sd.get("model_state_dict", {}))
    w = sd.get("mlp.0.weight")
    return "compliant" if (w is not None and robot_name == "anymal_c" and w.shape[1] == 50) else "v1"


REWARD_SETS = ("r3", "r4", "r5", "r7", "r8", "rmin")
GOAL_ERROR_COST = 0.25  # r7: per second at the start error (distance fraction 1 + heading fraction)


def make_coop2_env_cfg(variant: str = "b", play: bool = False, partner_map: bool = False,
                       reward_set: str = "r3", start_mode: str = "behind", need_frac: float = 0.0,
                       need_mass: float = 45.0, contacts: bool = False, tol_levels: tuple = (),
                       contact_mix: tuple = (1.0, 1.0, 1.0), contact_start_at: float = 0.7,
                       drift_dist: float = 0.35, drift_heading_deg: float = 45.0,
                       reselect_s: tuple = (0.0, 0.0), random_start: float = 0.0, off_contact: str = "soft",
                       off_contact_cost: float = 1.0, contact_approach: float = 1.0, guide: bool = False,
                       bump_cost: float = 1.0, disturb_frac: float = 0.0, push_sensors: bool = False,
                       push_cmd: bool = False, wrench: bool = False, walk_cost: float = 0.3,
                       reselect_min_dist: float = 0.15, expert: bool = False, exec_v2: bool = False,
                       hold_rand: float = 0.0, hold_cost_w: float = 1.0, credit_press: float = 0.0,
                       work_w: float = 3.0, effort: bool = False, over_push_w: float = 1.0,
                       contact_sense: bool = False, acq_bonus: float = 0.0, time_cost: float = 0.0,
                       touch_cost: float = 0.0, resid: bool = False, resid_objects: tuple = (),
                       shape_bias: tuple = (), resid_gate_dist: float = 0.0, train_shapes: tuple = (),
                       train_mass: tuple = (), fixed_difficulty: bool = False) -> ManagerBasedRlEnvCfg:
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
    contact_mix (spread, adjacent, random), contact_start_at, drift_dist, drift_heading_deg,
    reselect_s (re-apply the contact rule every U(lo, hi) s; (0, 0) = fixed), random_start: see
    CoopPush2CommandCfg.
    off_contact: "soft" - no contact rule ends an episode and there are no deadlines; each robot is
    pulled to its contact (contact_approach: weight of the potential-based reward, replacing r7's
    approach-the-surface term) and pays off_contact_cost per second while off a contact it had
    reached; "terminate" - Stage 4 / 4b (off-contact ends the episode as a failure, reach limits).
    guide (Stage 4d, needs contacts and soft): a route to the contact as 6 more inputs, the pull pays
    for shortening the route, bump_cost per second for touching the object off the contact;
    disturb_frac: share of episodes with scripted object motion (training; an eval may set it too).
    push_sensors: add the robot-object contact sensors even when no reward uses them (evals).
    effort (force_track, needs push_cmd and rmin): each robot also observes its absolute push target, the
    contact force it applies and the object motion the planner wants (8 inputs, last); rmin's contact_work
    becomes effort_work (paid up to the target only), plus over_push (weight over_push_w) past 1.5 x target.
    push_cmd (Stage 4e, needs guide): a push direction per robot recomputed every step from the
    remaining error (4 more inputs: direction, share, pair residual), on-contact judged against
    it, pose_progress (distance + radius of gyration x angle) replaces box / yaw progress,
    motion_credit replaces push_credit, walk_cost per second on the way to a new contact, and a
    partner-aware route. wrench: only the machinery the wrench contact rule needs (evals of
    older checkpoints with that rule). contact_mix may carry a 4th weight: the wrench rule.
    reselect_min_dist: no contact re-choice with the object this close to its goal (m).
    expert: the expert planner v2 machinery (contact rule 4: pair and robot assignment together at
    least cost incl. walking time, no-progress / slow-arrival re-plans, priorities, go / hold,
    turning that grows as the object nears its goal); contact_mix may carry a 5th weight for it.
    tol_levels: success-tolerance curriculum ((pos m, yaw deg), ...), loose -> fine; () = fixed."""
    assert variant in ("b", "ctrl"), variant
    assert reward_set in REWARD_SETS, reward_set
    assert not (partner_map and variant != "b"), "the partner map needs variant b (maps)"
    kinds = {a: walker_kind(SPECS[a].name) for a in AGENTS}
    wcfg = {a: make_walker_env_cfg(SPECS[a], history=walker_history(SPECS[a].name), compliant=kinds[a] == "compliant")
            for a in AGENTS}
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
    assert not guide or (contacts and off_contact == "soft"), "guide needs contacts with off_contact soft"
    assert not push_cmd or guide, "push_cmd builds on guide (Stage 4d)"
    assert not exec_v2 or push_cmd, "exec_v2 builds on push_cmd (Stage 4e)"
    assert reward_set != "rmin" or (push_cmd and contacts and off_contact == "soft"), "rmin builds on Stage 4e (push_cmd)"
    assert not effort or (push_cmd and contacts and reward_set == "rmin"), \
        "effort (force_track) builds on Stage 4e (push_cmd) with the minimal reward (rmin)"
    expert = contacts and (expert or (len(contact_mix) > 4 and contact_mix[4] > 0))
    wrench = contacts and (wrench or push_cmd or expert or (len(contact_mix) > 3 and contact_mix[3] > 0))
    if reward_set == "r8" or guide or push_sensors or resid or "compliant" in kinds.values():
        # contact between each robot and the object (work_credit, bump cost; a compliant walker's force input)
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
            twist_name=f"twist_{a}", walker_obs_group=f"walker_{a}", agent_index=AGENTS.index(a),
        )

    # -- commands ---------------------------------------------------------------------------------
    cfg.commands = {f"twist_{a}": s1.HighLevelTwistCfg() for a in AGENTS}
    cfg.commands["goal"] = mdp.CoopPush2CommandCfg(
        variant=variant, reach=tuple(SPECS[a].half_length for a in AGENTS), robot_reach=SPECS[AGENTS[0]].half_length,
        map_hz=float(os.environ.get("QUADCOOP_MAP_HZ", "10")), start_level=0, success_mode="terminate",
        partner_map=partner_map, track_approach=reward_set in ("r5", "r7", "r8", "rmin"),
        start_mode=start_mode, need_frac=need_frac, need_mass=need_mass,
        contact_mode=contacts, contact_mix=tuple(contact_mix), contact_start_at=contact_start_at,
        drift_dist=drift_dist, drift_heading_deg=drift_heading_deg,
        reselect_s=tuple(float(x) for x in reselect_s), random_start=random_start,
        off_contact_mode=off_contact if contacts else "terminate",
        guide=guide and contacts, disturb_frac=disturb_frac,
        wrench=wrench, push_cmd=push_cmd and contacts, reselect_min_dist=reselect_min_dist,
        expert=expert, turn_full_dist=1.0 if expert else 0.0, finish_dist=0.5 if expert else 0.0,
        exec_v2=exec_v2 and push_cmd and contacts, hold_rand=hold_rand if exec_v2 else 0.0,
        effort=effort and push_cmd and contacts, tol_levels=tuple(tuple(x) for x in tol_levels),
        resid=resid and contacts and push_cmd, resid_objects=tuple(resid_objects),
        shape_bias=tuple(tuple(x) for x in shape_bias), resid_gate_dist=float(resid_gate_dist),
        train_shapes=tuple(train_shapes), train_mass=tuple(float(x) for x in train_mass),
        fixed_difficulty=bool(fixed_difficulty))
    if fixed_difficulty:  # no replayed lower levels either
        cfg.commands["goal"].replay_frac = 0.0

    # -- observations -------------------------------------------------------------------------------
    T = ObservationTermCfg
    obs = {}
    for a, o in PARTNER.items():
        obs[f"actor_{a}"] = ObservationGroupCfg(terms=_agent_terms(a, o, noisy=True, contacts=contacts, guide=guide,
                                                                   push_cmd=push_cmd, exec_v2=exec_v2 and push_cmd and contacts,
                                                                   effort=effort, contact_sense=contact_sense),
                                                concatenate_terms=True, enable_corruption=not play)
        obs[f"state_{a}"] = ObservationGroupCfg(terms=_agent_terms(a, o, noisy=False, contacts=contacts, guide=guide,
                                                                   push_cmd=push_cmd, exec_v2=exec_v2 and push_cmd and contacts,
                                                                   effort=effort, contact_sense=contact_sense),
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
    if resid:  # residual execution pilot: the correction's own inputs and its per-env gate
        assert contacts and push_cmd, "the residual pilot builds on Stage 4e (push_cmd) contacts"
        for a in AGENTS:
            obs[f"resid_{a}"] = ObservationGroupCfg(terms={"resid": T(func=mdp.resid_obs, params={"robot": a})},
                                                    concatenate_terms=True, enable_corruption=False)
            obs[f"resid_gate_{a}"] = ObservationGroupCfg(terms={"gate": T(func=mdp.resid_gate, params={"robot": a})},
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
    assert off_contact in ("soft", "terminate"), off_contact
    soft = contacts and off_contact == "soft"
    fails = tuple(f"{a}_fell" for a in AGENTS) + ("box_tipped", "box_lost") + \
        (tuple(f"{a}_off_contact" for a in AGENTS) if contacts and not soft else ())
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
    if push_cmd:  # Stage 4e: one progress measure, turning worth the object's radius of gyration in metres
        rewards.pop("box_progress")
        rewards.pop("yaw_progress")
        rewards["pose_progress"] = R(func=mdp.pose_progress, weight=3.0)
    if reward_set == "r5":
        rewards["time_cost"] = R(func=mdp.time_cost, weight=-0.2)
    if reward_set == "r8":
        rewards.pop("robots_close")  # only actual contact counts (robots_touch)
    if reward_set in ("r7", "r8"):
        rewards["goal_error"] = R(func=mdp.goal_error, weight=-GOAL_ERROR_COST)
        rewards["fail_remaining"] = R(func=mdp.failed_remaining, weight=-GOAL_ERROR_COST,
                                      params={"names": fails, "horizon_s": EPISODE_S})
    for k, a in enumerate(AGENTS):
        if soft:  # pulled to its assigned contact instead of to the nearest surface
            rewards[f"contact_approach_{a}"] = R(func=mdp.contact_approach, weight=contact_approach, params={"robot": a})
            rewards[f"off_contact_cost_{a}"] = R(func=mdp.off_contact_cost, weight=-off_contact_cost, params={"robot": a})
            if guide and bump_cost > 0:
                rewards[f"bump_cost_{a}"] = R(func=mdp.bump_cost, weight=-bump_cost, params={"robot": a})
        elif reward_set in ("r5", "r7", "r8"):
            rewards[f"approach_{a}"] = R(func=mdp.approach, weight=2.0, params={"robot": a})
        else:
            rewards[f"near_surface_{a}"] = R(func=mdp.near_surface, weight=0.5, params={"robot": a})
        if reward_set == "r3":
            rewards[f"behind_box_{a}"] = R(func=mdp.behind_box, weight=0.3, params={"robot": a})
        rewards[f"action_rate_{a}"] = R(func=mdp.agent_action_rate, weight=-0.05, params={"agent": k})
        rewards[f"action_limit_{a}"] = R(func=mdp.agent_action_limit, weight=-0.02, params={"agent": k})
        if reward_set == "r8":
            rewards[f"work_credit_{a}"] = R(func=mdp.work_credit, weight=3.0, params={"robot": a})
        elif reward_set == "r7" and push_cmd:
            rewards[f"motion_credit_{a}"] = R(func=mdp.motion_credit, weight=1.0,
                                              params={"robot": a, **({"press_force": credit_press} if credit_press > 0 else {})})
            rewards[f"walk_cost_{a}"] = R(func=mdp.walk_cost, weight=-walk_cost, params={"robot": a})
            if exec_v2:  # Phase 2: told to hold -> stay on the contact without pushing or walking
                rewards[f"hold_cost_{a}"] = R(func=mdp.hold_cost, weight=-hold_cost_w, params={"robot": a})
        elif reward_set == "r7":
            rewards[f"push_credit_{a}"] = R(func=mdp.push_credit, weight=1.0, params={"robot": a})
        else:
            rewards[f"push_along_{a}"] = R(func=mdp.push_along, weight=1.0 if reward_set == "r5" else 0.3,
                                           params={"robot": a})
        rewards[f"own_fall_{a}"] = R(func=mdp.own_fall, weight=-0.2 * BONUS / step_dt,
                                     params={"robot": a, "nominal_height": SPECS[a].nominal_height})
        if contacts and not soft:  # leaving its contact costs the robot that left as much as its own fall
            rewards[f"own_off_contact_{a}"] = R(func=mdp.own_off_contact, weight=-0.2 * BONUS / step_dt,
                                                params={"robot": a})
    if reward_set == "rmin":
        # minimal reward (hovering test, run B): progress (two potential-based terms), success, failure, the
        # robot's own fall, the potential-based pull to its assigned contact, and its own pushing work
        keep = ["pose_progress", "precise_progress", "goal_bonus", "terminated"] + \
               [f"{x}_{a}" for a in AGENTS for x in ("own_fall", "contact_approach")]
        rewards = {k: rewards[k] for k in keep}
        for a in AGENTS:
            if effort:  # force_track: work capped at the push target, and a cost for pushing far past it
                rewards[f"effort_work_{a}"] = R(func=mdp.effort_work, weight=work_w, params={"robot": a})
                if over_push_w > 0:
                    rewards[f"over_push_{a}"] = R(func=mdp.over_push, weight=-over_push_w, params={"robot": a})
            else:
                rewards[f"contact_work_{a}"] = R(func=mdp.contact_work, weight=work_w, params={"robot": a})
    if acq_bonus > 0:  # contact curriculum: a one-time bonus per assignment for reaching real contact (30 N+)
        for a in AGENTS:
            rewards[f"contact_acquired_{a}"] = R(func=mdp.contact_acquired, weight=acq_bonus / step_dt, params={"robot": a})
    if time_cost > 0:
        rewards["time_cost"] = R(func=mdp.time_cost, weight=-time_cost)
    if touch_cost > 0:  # (the minimal reward drops robots_touch; this puts a contact cost back)
        rewards["robots_touch"] = R(func=mdp.robots_touching, weight=-touch_cost)
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
    if contacts and not soft:
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
        cfg.commands["goal"].random_start = 0.0
    return cfg
