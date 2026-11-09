"""Hand-assigned contacts: can two robots, deliberately given different useful contacts, beat the
learned pairs, on the same walkers and the same tasks?

    python scripts/contact_test.py --pair anymal                    # rules centre / adjacent / spread
    python scripts/contact_test.py --pair anymal --rules spread --objects beam,arch,dumbbell --masses 60
    python scripts/contact_test.py --pair mixed --reassign-s 4      # re-choose contacts every 4 s

Executors (--executor):

    script   (default) no learning above the walkers: each robot runs the scripted contact controller
             (approach and push) - see below
    policy   hand-off test: the scripted controller only walks each robot to its assigned contact
             (standing point, facing it); from there the robot's frozen Stage 2b push policy takes
             over. If the robot's front drifts more than --return-dist from its contact point (0 =
             never), the script takes it back to the contact and hands over again. Logged per robot:
             share of time under the policy, mean distance from its front to the assigned contact
             while under the policy, share of that time within 0.25 m, and the number of returns.

    stage4   the Stage 4 contact-conditioned policy (train_coop2.py --contacts, --checkpoint): the
             robots start at their assigned contacts and the policy (told the contacts) does the
             rest. Rules spread / adjacent / random (a seeded random valid pair, as in training), and
             allpairs: every usable ordered contact pair of every task (both contacts pushing within
             75 deg of the goal direction, standing points 0.85 m apart), contacts fixed - the payoff
             sweep for the contact game (scripts/contact_game.py reads it).

    python scripts/contact_test.py --executor policy                       # prefix handoff-aa
    python scripts/contact_test.py --executor policy --return-dist 0 --prefix handoff-aa-free
    python scripts/contact_test.py --executor stage4 --checkpoint logs/marl2/s4_aa_s0/model_3000.pt \
        --prefix s4-aa-s0-it3000                                  # rules spread,adjacent,random
    python scripts/contact_test.py --executor stage4 --checkpoint logs/marl2/s4b_aa_s0/model_6000.pt \
        --rules allpairs --masses 40,70 --prefix game-s4b         # payoff sweep -> evals/game-s4b-allpairs

In script mode each robot runs the scripted contact controller
(quadcoop/contact_control.py) on a contact from the object's candidate set
(quadcoop/contacts.py), chosen by a goal-relative rule that is the same for every object:

    centre    one robot on the back contact pushing closest through the centre of mass; the other
              parked far away (the one-robot reference)
    adjacent  both robots on the two back contacts closest to the centre line, side by side (what
              the learned pairs tend to do)
    spread    the two back contacts farthest apart across the motion: one per end / pillar / block

Two contacts only form a pair if the robots' standing points are 0.75 m apart; if no pair faces the
goal within 45 deg, neighbouring faces within 75 deg are allowed; if there is still no pair (straight
behind the cube, the long box's end, the lying cylinder) robot 2 is parked and the task is done by
one robot (column robots_used).

"Back" = the push (into the surface) points within 45 deg of the object -> goal direction. Which
robot takes which contact is decided by where they stand (shortest total walk). With
--reassign-s the rule is applied again every so many seconds from the object's current pose (an
object that has turned gets new back contacts).

Tasks, placements and scoring are exactly scripts/eval_coop2.py's (12 objects x 4 scenarios x
--reps placements x masses, the same seeded robot placements; success = 10 cm / 6 deg held 1 s
within 80 s; a fall of either robot, the object tipping or being lost ends the episode), so the
results sit in the same table as the trained pairs: stats in evals/<prefix>-<rule>/eval/pair/
(summary.md/json, episodes.csv), videos in logs/evals/<prefix>-<rule>/pair/videos/.

Walker comparisons: QUADCOOP_WALKER_OVERRIDE_ANYMAL_C=<model.pt> runs the ANYmals on another walker (a
compliant one gets its contact-force input wired automatically; run scripts/walker_coop_check.py on it
first). The walkers used are recorded in summary.json ("walkers") and results from different walkers are
never merged. Use a different --prefix per walker. The two controlled comparisons:

    # the existing (v1-trained) executor, zero-shot on the new walker vs on v1: does swapping help as is?
    python scripts/contact_test.py --executor stage4 --checkpoint <exec.pt> --prefix ex-v1 ...
    QUADCOOP_WALKER_OVERRIDE_ANYMAL_C=<v22k.pt> python scripts/contact_test.py --executor stage4 \
        --checkpoint <exec.pt> --prefix ex-v22k ...
    # the same scripted executor on both walkers: which walker better supports a fixed controller?
    python scripts/contact_test.py --executor script --prefix sc-v1 ...
    QUADCOOP_WALKER_OVERRIDE_ANYMAL_C=<v22k.pt> python scripts/contact_test.py --executor script --prefix sc-v22k ...

(The third, matched fine-tuning of the executor on each walker, is a train_coop2.py run with the same
override; train_coop2.py reads it too.)
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
import shutil
import sys
import time
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT))

SCENARIOS = (  # as scripts/eval_coop2.py
    ("A_straight", 3.0, 0.0, 0.0),
    ("B_left", 3.0, 60.0, 30.0),
    ("C_backright", 3.0, -135.0, -60.0),
    ("D_far_turn", 5.0, 0.0, 90.0),
)
TURN_SCENARIOS = (  # --tasks turn (test 3): the object already at the goal position, its heading off by this much
    ("T15", 0.0, 0.0, 15.0),
    ("T30", 0.0, 0.0, -30.0),
    ("T60", 0.0, 0.0, 60.0),
    ("T90", 0.0, 0.0, -90.0),
)
RULES = ("centre", "adjacent", "spread")
SHARE_BINS = 5  # commanded share of robot 1, in bins of 0.2 (following the force split)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pair", choices=("mixed", "anymal", "spot"), default="anymal")
    ap.add_argument("--prefix", default=None, help="output names <prefix>-<rule> (default contact-<pair>)")
    ap.add_argument("--rules", default=None, help="default centre,adjacent,spread (stage4: spread,adjacent,random)")
    ap.add_argument("--objects", default="all")
    ap.add_argument("--masses", default="20,40,60,80")
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--horizon", type=float, default=80.0)
    ap.add_argument("--reassign-s", type=float, default=0.0, help="re-choose contacts every so many seconds (0 = once)")
    ap.add_argument("--executor", choices=("script", "policy", "stage4"), default="script",
                    help="who pushes once a robot is at its contact: the scripted controller or the frozen Stage 2b policy")
    ap.add_argument("--checkpoint", default=None, help="stage4 executor: a train_coop2.py --contacts model_<iter>.pt")
    ap.add_argument("--reselect-s", default="auto",
                    help="stage4 executor: re-apply the contact rule every so many seconds ('lo,hi' or one value; "
                         "0 = contacts fixed for the episode; auto = as the checkpoint was trained)")
    ap.add_argument("--return-dist", type=float, default=0.5,
                    help="policy executor: hand back to the script when the front is this far from the contact (0 = never)")
    ap.add_argument("--start", choices=("contact", "behind"), default="contact",
                    help="stage4: robots start at their contacts, or at scripts/eval_coop2.py's placements behind the "
                         "object and walk to their contacts first (tests reaching)")
    ap.add_argument("--reselect-min-dist", default="auto",
                    help="stage4: no contact re-choice with the object this close to its goal (m); auto = as trained")
    ap.add_argument("--disturb-frac", type=float, default=0.0,
                    help="stage4: share of episodes in which the object is shoved (scripted motion, 1.5-3 s at 0.15-0.35 m/s "
                         "some time in 1-8 s), to test reaching moving contacts")
    ap.add_argument("--video-objects", default="cube,sphere,beam,dumbbell,arch,t_shape",
                    help="objects to film ('all' = every object); filmed: A_straight and D_far_turn, rep 0, --video-mass")
    ap.add_argument("--videos", type=int, default=1, help="1 = film rule x object (A_straight and D_far_turn) at --video-mass")
    ap.add_argument("--video-mass", type=float, default=60.0)
    ap.add_argument("--video-masses", default=None, help="film at these masses (comma list; default --video-mass)")
    ap.add_argument("--video-scenarios", default="A_straight,D_far_turn",
                    help="scenarios to film (comma list of names, or 'all')")
    ap.add_argument("--video-reps", default="0", help="placements to film (comma list of rep indices, or 'all')")
    ap.add_argument("--video-dir", default=None,
                    help="write the videos to <video-dir>/<prefix>-<rule>/ (e.g. eval_videos) instead of "
                         "logs/evals/<prefix>-<rule>/pair/videos/; either way the folder gets index.html / index.csv")
    ap.add_argument("--video-size", default="640x480")
    ap.add_argument("--diag", type=int, default=1,
                    help="stage4: executor diagnosis (commands vs what the robots do, the push, the object, every "
                         "standstill by cause; quadcoop.coop2.diag) in the episodes and the summary")
    ap.add_argument("--cmd-mode", choices=("planner", "always_push"), default="planner",
                    help="executor v2 checkpoints: 'always_push' = a robot on its contact is told to push (no hold, no "
                         "team-ready wait), as Stage 4e; to tell the waiting rules from the push itself")
    ap.add_argument("--replay", default="",
                    help="open-loop replay diagnostic: a pair folder with trace_<mass>kg.csv.gz (from a --trace 1 run). Each "
                         "episode starts from the same task reset and both walkers get the recorded walker commands (10 Hz, "
                         "held) instead of the executor's, through the command interface QUADCOOP_CMD_IF (raw | proj | "
                         "proj_rate). Only falls end an episode. Writes replay_<mass>kg.csv (falls, progress along the "
                         "recorded command, yaw-rate error, heading drift, response delay). An approximation: the robots "
                         "drift from the recorded run's states, and commands are 10 Hz samples of the smoothed command")
    ap.add_argument("--trace", type=int, default=0,
                    help="1 = per-step traces (10 Hz) of the rep-0 episodes in logs/evals/<prefix>-<rule>/pair/trace_<mass>kg.csv.gz")
    ap.add_argument("--tasks", choices=("standard", "turn"), default="standard",
                    help="standard: scripts/eval_coop2.py's 4 scenarios; turn: turn in place (the object starts at the goal "
                         "position with its heading off by 15 / 30 / 60 / 90 deg, capped by the object's symmetry)")
    ap.add_argument("--set", default="",
                    help="planner settings to override, comma list key=value on the goal command's config, e.g. "
                         "'finish_dist=0' or 'robot_push_force=320'")
    ap.add_argument("--swap-actors", action="store_true",
                    help="stage4: robot 1 runs the network trained as robot 2 and vice versa (does a failure follow the "
                         "learned network or the robot's place?)")
    ap.add_argument("--device", default=None)
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    global SCENARIOS
    if a.tasks == "turn":
        SCENARIOS = TURN_SCENARIOS
    overrides = {}
    for kv in [x for x in a.set.split(",") if x.strip()]:
        k_, v_ = kv.split("=", 1)
        overrides[k_.strip()] = float(v_)

    from train_coop2 import resolve_models, set_env

    models = resolve_models("b", a.pair)
    set_env(models)
    import os
    import numpy as np
    import torch
    from tensordict import TensorDict

    import quadcoop  # noqa: F401
    from mjlab.envs import ManagerBasedRlEnv

    from quadcoop import contacts as C
    from quadcoop import falls
    from quadcoop.contact_control import IDLE_ACTION, ContactController, to_action
    from quadcoop.coop2 import mdp as cm
    from quadcoop.coop2 import diag as dgm
    from quadcoop.coop2.env_cfg import SPECS, make_coop2_env_cfg
    from quadcoop.coop2.marl import PairPolicy
    from quadcoop.coop2.mdp import AGENTS
    from quadcoop.coop2.video import Camera, render_episode
    from quadcoop.stage1.mdp import wrap, yaw_of
    from quadcoop.stage1b import mdp as hb
    from quadcoop.stage1b.shapes import NOMINAL_MASS
    from quadcoop.stage2 import mdp as m2
    from quadcoop.stage2.shapes import OBJ_NAMES2, SHAPE_NAMES2, SHAPES2, TRAIN_NAMES, kinds_tensor, nominal_parts

    device = a.device or ("cuda:0" if torch.cuda.is_available() else "cpu")
    tag = {'anymal': 'aa', 'spot': 'ss', 'mixed': 'mx'}[a.pair]
    prefix = a.prefix or {"script": f"contact-{tag}", "policy": f"handoff-{tag}", "stage4": f"s4-{tag}"}[a.executor]
    use_policy = a.executor == "policy"
    stage4 = a.executor == "stage4"
    ck_cfg = {}
    if stage4:
        if not a.checkpoint:
            raise SystemExit("--executor stage4 needs --checkpoint")
        ck_cfg = torch.load(a.checkpoint, map_location="cpu", weights_only=False).get("cfg", {})
        if not ck_cfg.get("contacts"):
            raise SystemExit(f"{a.checkpoint} was not trained with --contacts")
    if a.reselect_s == "auto":
        reselect_s = tuple(float(x) for x in ck_cfg.get("reselect_s", (0.0, 0.0)))
    else:
        rs_ = [float(x) for x in a.reselect_s.split(",")]
        reselect_s = (rs_[0], rs_[-1])
    video_objects = None if a.video_objects == "all" else {o.strip() for o in a.video_objects.split(",")}
    video_masses = {a.video_mass} if a.video_masses is None else {float(x) for x in a.video_masses.split(",")}
    video_scen = None if a.video_scenarios == "all" else {x.strip() for x in a.video_scenarios.split(",")}
    video_reps = None if a.video_reps == "all" else {int(x) for x in a.video_reps.split(",")}
    rules = [r.strip() for r in (a.rules or ("spread,adjacent,random" if stage4 else ",".join(RULES))).split(",")]
    if stage4 and "centre" in rules:
        raise SystemExit("the stage4 executor runs two robots: rules spread, adjacent, random, wrench, expert, allpairs")
    if ("wrench" in rules or "expert" in rules) and not stage4:
        raise SystemExit("the wrench and expert rules are Stage 4 contact rules: --executor stage4")
    min_dist = float(ck_cfg.get("reselect_min_dist", 0.15)) if a.reselect_min_dist == "auto" else float(a.reselect_min_dist)
    if "allpairs" in rules:
        if not stage4:
            raise SystemExit("rule allpairs needs --executor stage4")
        if reselect_s[1] > 0:
            if a.reselect_s != "auto":
                raise SystemExit("allpairs is the one-shot contact game: contacts stay fixed (--reselect-s 0)")
            print("allpairs: contacts fixed for the episode (re-selection off)")
            reselect_s = (0.0, 0.0)
            a.reselect_s = "0"
    objects = list(SHAPE_NAMES2) if a.objects == "all" else [o.strip() for o in a.objects.split(",")]
    masses = [float(x) for x in a.masses.split(",")]
    vw, vh = (int(x) for x in a.video_size.lower().split("x"))

    # candidate contacts per shape (nominal sizes, as the evaluation uses)
    parts_all, rest_all = nominal_parts("cpu")
    kinds_all = kinds_tensor("cpu")
    cands = {}
    for s, nm in enumerate(SHAPE_NAMES2):
        cands[nm] = C.candidates(parts_all[s].numpy(), kinds_all[s].numpy(), float(rest_all[s]))
    com = {nm: C.centre_of_mass(parts_all[s].numpy(), kinds_all[s].numpy()) for s, nm in enumerate(SHAPE_NAMES2)}

    base_cases = [(o, s, r) for o in objects for s in range(len(SCENARIOS)) for r in range(a.reps)]
    rng = random.Random(f"{a.seed}-coop2")  # the same placements as scripts/eval_coop2.py
    jit_b = [[rng.uniform(-10, 10) for _ in AGENTS] for _ in base_cases]
    gap_b = [[rng.uniform(0.3, 0.6) for _ in AGENTS] for _ in base_cases]
    def usable_pairs(o, s):
        """Ordered contact pairs for robot 1 / robot 2 that the policy can be given for this task:
        both pushing within 75 deg of the goal direction, standing points >= 0.85 m apart."""
        gd = math.radians(SCENARIOS[s][2])
        u = np.array([math.cos(gd), math.sin(gd)])
        use = [c for c in cands[o] if float(-c.n @ u) >= math.cos(math.radians(75.0)) - 1e-9]
        return [(x.index, y.index) for x in use for y in use
                if x.index != y.index and np.linalg.norm(x.stand - y.stand) >= 0.85]

    cases, pair_of = [], []
    for rule in rules:
        for k, (o, s, r) in enumerate(base_cases):
            for pr in (usable_pairs(o, s) if rule == "allpairs" else [None]):
                cases.append((rule, o, s, r, k))
                pair_of.append(pr)
    n_of = {rule: sum(1 for c in cases if c[0] == rule) for rule in rules}  # envs (= rows) per rule and mass
    n = len(cases)
    print(f"pair {a.pair}: rules {rules}; {len(objects)} objects x {len(SCENARIOS)} scenarios x {a.reps} reps = "
          f"{len(base_cases)} tasks per rule, {n} envs per mass; masses {masses}; reassign every "
          f"{a.reassign_s or 'never'} s; executor {a.executor}"
          + (f" (contact rule re-applied every {reselect_s[0]:g}-{reselect_s[1]:g} s)" if stage4 and reselect_s[1] > 0 else "")
          + (f" (back to the script beyond {a.return_dist:g} m)" if use_policy and a.return_dist > 0 else ""), flush=True)
    rows = {rule: [] for rule in rules}
    t_start = time.time()

    for mass in masses:
        cfg = make_coop2_env_cfg("b", play=True) if not stage4 else make_coop2_env_cfg(
            "b", play=True, partner_map=bool(ck_cfg.get("partner_map", False)), reward_set=ck_cfg.get("reward_set", "r7"),
            contacts=True, tol_levels=tuple(tuple(x) for x in ck_cfg.get("tol_levels", ())),
            drift_dist=float(ck_cfg.get("drift_dist", 0.35)), drift_heading_deg=float(ck_cfg.get("drift_heading_deg", 45.0)),
            reselect_s=reselect_s, guide=bool(ck_cfg.get("guide", False)),
            off_contact=ck_cfg.get("off_contact", "soft") if ck_cfg.get("guide") else "soft",
            disturb_frac=a.disturb_frac, push_sensors=True, push_cmd=bool(ck_cfg.get("push_cmd", False)),
            wrench="wrench" in rules or "expert" in rules, walk_cost=float(ck_cfg.get("walk_cost", 0.3)),
            reselect_min_dist=min_dist, expert="expert" in rules, exec_v2=bool(ck_cfg.get("exec_v2", False)),
            effort=bool(ck_cfg.get("effort", False)))
        cfg.scene.num_envs = n
        cfg.episode_length_s = 1e5
        cfg.terminations = {}
        for k_, v_ in overrides.items():
            gc = cfg.commands["goal"]
            if not hasattr(gc, k_):
                raise SystemExit(f"--set: the goal command has no setting '{k_}'")
            setattr(gc, k_, type(getattr(gc, k_))(v_))
            print(f"[set] goal.{k_} = {getattr(gc, k_)}", flush=True)
        alpha = 0.5 * math.log(mass / NOMINAL_MASS)
        for name in OBJ_NAMES2:
            cfg.events[f"{name}_mass"].params["alpha_range"] = (alpha, alpha)
        torch.manual_seed(a.seed)
        base = ManagerBasedRlEnv(cfg=cfg, device=device)
        g = base.command_manager.get_term("goal")
        dev = base.device
        ids = torch.arange(n, device=dev)
        for k in range(len(SHAPES2)):
            m2.apply_geometry(base, ids, k, torch.ones(n, 3, device=dev))

        obj_idx = torch.tensor([SHAPE_NAMES2.index(o) for _, o, _, _, _ in cases], device=dev)
        dist = torch.tensor([SCENARIOS[s][1] for _, _, s, _, _ in cases], device=dev)
        gdir = torch.deg2rad(torch.tensor([SCENARIOS[s][2] for _, _, s, _, _ in cases], device=dev))
        turn = torch.deg2rad(torch.tensor([SCENARIOS[s][3] for _, _, s, _, _ in cases], device=dev))
        sym = g.sym[obj_idx]
        cap = torch.where(sym > 0, (math.pi / sym.clamp(min=1)) * g.cfg.max_yaw_frac_of_symmetry, torch.zeros_like(sym))
        turn = torch.sign(turn) * torch.minimum(turn.abs(), cap)
        jit = torch.tensor([jit_b[k] for *_, k in cases], device=dev)
        gap = torch.tensor([gap_b[k] for *_, k in cases], device=dev)
        bearings = [math.pi + torch.deg2rad(sgn * 35.0 + jit[:, i]) for i, sgn in enumerate((-1.0, 1.0))]
        # robot 2 is parked far away for 'centre', and for a two-robot rule when the object has no room for
        # two pushers toward the goal (no pair of contacts whose standing points are 0.75 m apart, e.g.
        # straight behind the cube): the object starts unrotated, so the start assignment is known here
        def one_only(rule, o, s):
            if stage4:
                return False
            if rule == "centre":
                return True
            gd = math.radians(SCENARIOS[s][2])
            return C.assign(cands[o], np.array([math.cos(gd), math.sin(gd)]), rule)[1] is None
        solo = torch.tensor([one_only(rule, o, s) for rule, o, s, _, _ in cases], device=dev)
        park = [torch.zeros(n, dtype=torch.bool, device=dev), solo.clone()]
        z = torch.zeros(n, device=dev)
        sc = {"shape": obj_idx, "obj_xy_rel": torch.zeros(n, 2, device=dev), "obj_heading": z.clone(),
              "goal_xy_rel": dist.unsqueeze(-1) * torch.stack([torch.cos(gdir), torch.sin(gdir)], -1),
              "goal_yaw": wrap(turn), "bearings": bearings, "gaps": [gap[:, 0], gap[:, 1]], "yaw_noise": [z, z],
              "park": park}
        if stage4:  # the env picks each env's pair with its own (training) rule code and places the robots there
            rule_id = {"spread": 0, "adjacent": 1, "random": 2, "allpairs": 0, "wrench": 3, "expert": 4}
            sc["contact_rule"] = torch.tensor([rule_id[rule] for rule, *_ in cases], dtype=torch.long, device=dev)
            sc["contact_idx"] = torch.tensor([pr if pr is not None else (-1, -1) for pr in pair_of], dtype=torch.long, device=dev)
            if a.start == "behind":
                sc["start_behind"] = torch.ones(n, dtype=torch.bool, device=dev)
        g.scenario = lambda env_ids: {k: ([x[env_ids] for x in v] if isinstance(v, list) else v[env_ids])
                                      for k, v in sc.items()}
        obs, _ = base.reset()
        g.scenario = None
        obs = TensorDict({k: v for k, v in obs.items() if not k.startswith("walker_")}, batch_size=[n])
        policy = PairPolicy(obs, device, "b", singles=models["policy"]) if use_policy else \
            PairPolicy(obs, device, "b", checkpoint=a.checkpoint) if stage4 else None
        if stage4 and a.swap_actors:  # each robot gets the other's trained network (names in the weights swapped)
            ck_sw = torch.load(a.checkpoint, map_location=device, weights_only=False)["actors"]
            x_, y_ = AGENTS
            ren = lambda d: {k.replace(x_, "@@").replace(y_, x_).replace("@@", y_): v for k, v in d.items()}  # noqa: E731
            policy.actors[x_].load_state_dict(ren(ck_sw[y_]))
            policy.actors[y_].load_state_dict(ren(ck_sw[x_]))
            print(f"[swap] {x_} runs the network trained as {y_}, and vice versa", flush=True)
        robots = [base.scene[ag] for ag in AGENTS]
        handed = [torch.zeros(n, dtype=torch.bool, device=dev) for _ in AGENTS]  # under the push policy
        present = [torch.ones(n, dtype=torch.bool, device=dev), ~solo]  # robot 2 not parked
        if stage4 and getattr(g.cfg, "exec_v2", False):
            g.c_in_group[:, 1] = ~solo  # a parked robot is not waited for
            g.cfg.exec_cmd_mode = a.cmd_mode
        active = [x.clone() for x in present]  # has a contact to work on
        ctrl = [ContactController(n, dev, reach=SPECS[ag].half_length) for ag in AGENTS]
        p_obj = [torch.zeros(n, 2, device=dev) for _ in AGENTS]
        n_obj = [torch.zeros(n, 2, device=dev) for _ in AGENTS]
        pre_obj = [torch.zeros(n, 2, device=dev) for _ in AGENTS]
        com_t = torch.tensor(np.stack([com[o] for _, o, *_ in cases]), device=dev, dtype=torch.float)
        radius = g.radius_env[ids, obj_idx]
        chosen = [[None] * n, [None] * n]

        def assign_all(env_ids):
            """Apply each env's rule from the object's current pose and goal."""
            obj = g.box_pos()[:, :2].cpu().numpy()
            yaw = g.heading().cpu().numpy()
            goal = g.goal_xy.cpu().numpy()
            rp = [r.data.root_link_pos_w[:, :2].cpu().numpy() for r in robots]
            for j in env_ids:
                rule, o = cases[j][0], cases[j][1]
                c, s_ = math.cos(-yaw[j]), math.sin(-yaw[j])
                to_obj_frame = lambda v: np.array([c * v[0] - s_ * v[1], s_ * v[0] + c * v[1]])  # noqa: E731
                u = to_obj_frame(goal[j] - obj[j])
                pair = C.assign(cands[o], u, rule)
                pair = C.match(cands[o], pair, np.stack([to_obj_frame(rp[0][j] - obj[j]), to_obj_frame(rp[1][j] - obj[j])]))
                for k in range(2):
                    idx = pair[k]
                    active[k][j] = idx is not None and bool(present[k][j])
                    if idx is None or not bool(present[k][j]):
                        chosen[k][j] = None
                        continue
                    if chosen[k][j] != idx:
                        ctrl[k].reset(torch.tensor([j], device=dev))
                        handed[k][j] = False
                    chosen[k][j] = idx
                    cc = cands[o][idx]
                    p_obj[k][j] = torch.tensor(cc.p, dtype=torch.float)
                    n_obj[k][j] = torch.tensor(cc.n, dtype=torch.float)
                    pre_obj[k][j] = torch.tensor(cc.pre, dtype=torch.float)
        if stage4:
            s4_idx = g.c_idx.tolist()  # the env's candidate lists are contacts.candidates' (same order as cands)
            for j, (i1, i2) in enumerate(s4_idx):
                chosen[0][j], chosen[1][j] = i1, i2
        else:
            assign_all(range(n))
        first_choice = [list(chosen[0]), list(chosen[1])]

        dt = base.step_dt
        dg = dgm.ExecDiag(n, dev, dt) if stage4 and a.diag else None
        tr_ids = [j for j, cs in enumerate(cases) if cs[3] == 0] if (dg is not None and a.trace) else []
        tr_rows = []
        rp = None
        if a.replay:  # recorded walker commands per (object, scenario), rep 0 of the traced run
            import gzip
            rec = {}
            pth_ = Path(a.replay) / f"trace_{mass:g}kg.csv.gz"
            last_t, key_, rows_ = 1e9, None, []
            for row_ in csv.DictReader(gzip.open(pth_, "rt")):
                tt = float(row_["t"])
                if tt < last_t and rows_:
                    rec.setdefault(key_, rows_); rows_ = []  # noqa: E702
                key_ = (row_["object"], row_["scenario"]); last_t = tt
                rows_.append(row_)
            if rows_:
                rec.setdefault(key_, rows_)
            tmax = max(len(v) for v in rec.values())
            rcmd = torch.zeros(n, tmax, 2, 3, device=dev)
            rlen = torch.zeros(n, device=dev)
            rinfo = []
            for j, (rule_, o_n, s_i, r_, _) in enumerate(cases):
                rr = rec.get((str(o_n), SCENARIOS[s_i][0]), [])
                for ti_, row_ in enumerate(rr):
                    for k, ag in enumerate(AGENTS):
                        rcmd[j, ti_, k] = torch.tensor([float(row_[f"wcmd_{x}_{ag}"]) for x in ("vx", "vy", "wz")])
                rlen[j] = len(rr)
                rinfo.append((rr[0]["outcome"] if rr else "", [max((float(x[f"fell_{ag}"]) for x in rr), default=0.0) for ag in AGENTS]))
            print(f"replay: {pth_}: {int((rlen > 0).sum())}/{n} episodes, interface {os.environ.get('QUADCOOP_CMD_IF', 'raw')}", flush=True)
            terms_ = [base.action_manager.get_term(f"walker_{ag}") for ag in AGENTS]
            rp = dict(pn=torch.zeros(n, 2, device=dev), pd=torch.zeros(n, 2, device=dev), yerr=torch.zeros(n, 2, device=dev),
                      ycum=torch.zeros(n, 2, device=dev), win=torch.zeros(n, 2, device=dev),
                      tfall=torch.full((n, 2), -1.0, device=dev), seq_c=[], seq_v=[])
        steps = int(a.horizon / dt)
        reassign_every = int(round(a.reassign_s / dt)) if a.reassign_s > 0 else 0
        film_ids = [j for j, (rule, o, s, r, _) in enumerate(cases) if rule != "allpairs"
                    if a.videos > 0 and mass in video_masses and (video_reps is None or r in video_reps)
                    and (video_scen is None or SCENARIOS[s][0] in video_scen)
                    and (video_objects is None or o in video_objects)]
        stride = 2
        rec_q, rec_mp, rec_mq, rec_pts = [], [], [], []
        rec_mark, rec_cap = [], []  # per frame: each robot's contact / push direction / waypoint / on it; errors
        nmocap = base.sim.mj_model.nmocap
        fid = torch.tensor(film_ids, dtype=torch.long, device=dev) if film_ids else None

        def record():
            sd = base.sim.data
            rec_q.append(sd.qpos[fid].cpu().numpy().copy())
            if nmocap:
                rec_mp.append(sd.mocap_pos[fid].cpu().numpy().copy())
                rec_mq.append(sd.mocap_quat[fid].cpu().numpy().copy())
            pts = [r.data.root_link_pos_w[fid, :2] for r in robots]
            pts[1] = torch.where(solo[fid].unsqueeze(-1), pts[0], pts[1])
            rec_pts.append(np.stack([p.cpu().numpy() for p in pts] + [g.box_pos()[fid, :2].cpu().numpy(),
                                                                       g.goal_xy[fid].cpu().numpy()], 1))
            if stage4:
                mk = []
                for k in range(2):
                    pw, nw = g.contact_world(k)
                    dk = g.push_dir_world(k) if g.cfg.wrench else -nw  # push direction (into the object)
                    wp = g.guide(k)[0] if g.cfg.guide else pw
                    mk.append(torch.cat([pw, dk, wp, g.on_contact(k).float().unsqueeze(-1)], -1)[fid])
                rec_mark.append(torch.stack(mk, 1).cpu().numpy())
                d_, e_ = g.errors()
                e_ = torch.where(g.symmetry() > 0, e_, torch.zeros_like(e_))
                ex = [torch.full_like(d_, -1.0)] * 5
                if getattr(g.cfg, "exec_v2", False):  # executor v2: each robot's command, team ready, contact force
                    ex = [g.c_cmd[:, 0].float(), g.c_cmd[:, 1].float(), g.c_team_ready.float()] + \
                         [torch.linalg.norm(cm.object_force_from(base, ag), dim=-1) for ag in AGENTS]
                elif getattr(g.cfg, "guide", False):
                    ex = ex[:3] + [torch.linalg.norm(cm.object_force_from(base, ag), dim=-1) for ag in AGENTS]
                rule_now = g.c_rule.float() if hasattr(g, "c_rule") else torch.full_like(d_, -1.0)
                rec_cap.append(torch.stack([d_, torch.rad2deg(e_), g.c_switches, *ex, rule_now], -1)[fid].cpu().numpy())
        if fid is not None:
            record()

        done = torch.zeros(n, dtype=torch.bool, device=dev)
        how = ["horizon"] * n
        t_succ = torch.full((n,), float("nan"), device=dev)
        t_end = torch.full((n,), a.horizon, device=dev)
        fell = [torch.zeros(n, dtype=torch.bool, device=dev) for _ in AGENTS]
        precise = torch.zeros(n, dtype=torch.bool, device=dev)
        hold = torch.zeros(n, device=dev)
        touch = torch.zeros(n, device=dev)
        live_steps = torch.zeros(n, device=dev)
        # who pushes, measured exactly as scripts/eval_coop2.py does (front within 8 cm of the object and
        # behind it relative to the goal), plus the controller's own phase (in push mode)
        push_steps = [torch.zeros(n, device=dev) for _ in AGENTS]
        mode_steps = [torch.zeros(n, device=dev) for _ in AGENTS]
        copush = torch.zeros(n, device=dev)
        spread_sum = torch.zeros(n, device=dev)
        min_rd = torch.full((n,), 1e9, device=dev)
        two = ~solo
        # holding the assigned contact: while engaged (policy: handed over; script: in push mode), the
        # distance from the robot's front to the contact point, and how often it is within 0.25 m
        eng_steps = [torch.zeros(n, device=dev) for _ in AGENTS]
        cdist_sum = [torch.zeros(n, device=dev) for _ in AGENTS]
        on_steps = [torch.zeros(n, device=dev) for _ in AGENTS]
        face_steps = [torch.zeros(n, device=dev) for _ in AGENTS]  # facing the contact's push direction (45 deg)
        returns = [torch.zeros(n, device=dev) for _ in AGENTS]
        # stage4 reaching: each time a robot's contact is (re)assigned, the time until it is first on it,
        # the assignments never reached, and the time spent touching the object anywhere but its contact
        bump_steps = [torch.zeros(n, device=dev) for _ in AGENTS]
        press_steps = [torch.zeros(n, device=dev) for _ in AGENTS]  # front on the object while on its contact
        resid_sum = torch.zeros(n, device=dev)  # wrench rule: residual of the current pair
        # coordination (stage4): time a robot presses while its partner is > 1 m from its own contact, the share of
        # pressing time with both pressing, metres walked, and (expert) the share of on-contact time spent holding
        solo_far = torch.zeros(n, device=dev)
        press_any = torch.zeros(n, device=dev)
        press_both = torch.zeros(n, device=dev)
        walked = torch.zeros(n, device=dev)
        hold_steps = torch.zeros(n, device=dev)
        on_any_steps = torch.zeros(n, device=dev)
        last_xy = [r.data.root_link_pos_w[:, :2].clone() for r in robots]
        # push force (stage4): histogram (20 N bins, last = 1000 N+) of each robot's horizontal contact force on the
        # object while it presses its contact and touches it, both robots pooled; and the same while the object is nearly still
        # (speed < 0.05 m/s: the robot meets the object's full resistance, so this is what it can sustain)
        FB = 20.0
        fb_all = torch.zeros(n, 51, device=dev)
        fb_still = torch.zeros(n, 51, device=dev)
        # following the force split (stage4 with push commands): while both robots press their contacts and push
        # 20 N+ in total along their commanded directions, robot 1's measured share of that push against its
        # commanded share (seconds, sum of |measured - commanded|, and by commanded-share bin: seconds and sum of
        # measured share)
        sh_t = torch.zeros(n, device=dev)
        sh_err = torch.zeros(n, device=dev)
        sh_bt = torch.zeros(n, SHARE_BINS, device=dev)
        sh_bm = torch.zeros(n, SHARE_BINS, device=dev)
        # push effort (force_track models): while a robot presses its contact with a target of 10 N+, its target
        # against the force it applies along its commanded direction (robot-seconds, sums)
        ef_t = torch.zeros(n, device=dev)
        ef_cmd = torch.zeros(n, device=dev)
        ef_meas = torch.zeros(n, device=dev)
        ef_err = torch.zeros(n, device=dev)
        # executor v2: time every robot of the push group is told to hold, the object's speed then (sum, and
        # time above 2 cm/s), each robot's contact force while told to hold, and the delay from team ready to
        # both robots pressing
        allhold_t = torch.zeros(n, device=dev)
        allhold_v = torch.zeros(n, device=dev)
        allhold_mv = torch.zeros(n, device=dev)
        holdf_sum = torch.zeros(n, device=dev)
        holdf_t = torch.zeros(n, device=dev)
        tr_wait = torch.full((n,), -1.0, device=dev)  # s since team ready while not both pressing; -1 = not waiting
        tr_sum = torch.zeros(n, device=dev)
        tr_n = torch.zeros(n, device=dev)

        def hist_q(h, q):
            """q-quantile (N, bin centre) of a force histogram; "" when empty."""
            tot = float(h.sum())
            if tot <= 0:
                return ""
            b = int((torch.cumsum(h, 0) >= q * tot).nonzero()[0])
            return round((b + 0.5) * FB, 0)
        reach_sum = [torch.zeros(n, device=dev) for _ in AGENTS]
        reach_n = [torch.zeros(n, device=dev) for _ in AGENTS]
        miss_n = [torch.zeros(n, device=dev) for _ in AGENTS]
        t_assign = [torch.zeros(n, device=dev) for _ in AGENTS]
        waiting = [present[k].clone() if stage4 else torch.zeros(n, dtype=torch.bool, device=dev) for k in range(2)]
        prev_c = [g.c_pobj[:, k].clone() for k in range(2)] if stage4 else None

        def geo_pushing(k):
            ag, r = AGENTS[k], robots[k]
            to_goal = g.goal_xy - g.box_pos()[:, :2]
            u = to_goal / torch.linalg.norm(to_goal, dim=-1, keepdim=True).clamp(min=1e-6)
            to_obj = g.box_pos()[:, :2] - r.data.root_link_pos_w[:, :2]
            behind = (to_obj * u).sum(-1) / torch.linalg.norm(to_obj, dim=-1).clamp(min=1e-6) > 0.0
            return (g.surface_distance(ag) < 0.08) & behind & present[k]

        def front_point(k):
            r = robots[k]
            yaw = yaw_of(r.data.root_link_quat_w)
            return r.data.root_link_pos_w[:, :2] + SPECS[AGENTS[k]].half_length * torch.stack([torch.cos(yaw), torch.sin(yaw)], -1)
        d0, _ = g.errors()
        last_d, last_e, min_d = d0.clone(), torch.zeros(n, device=dev), d0.clone()
        pt, yt = 0.10, math.radians(6.0)
        all_done_at = None
        tail = int(2.0 / dt)
        idle = torch.tensor(IDLE_ACTION, device=dev)
        t_loop, t_pol, t_env = time.time(), 0.0, 0.0
        ctrl_push = [torch.zeros(n, dtype=torch.bool, device=dev) for _ in AGENTS]
        sync = (lambda: torch.cuda.synchronize()) if str(dev).startswith("cuda") else (lambda: None)  # noqa: E731
        with torch.no_grad():
            for i in range(steps):
                if i > 0 and i % 1000 == 0:
                    print(f"  [{mass:g} kg] step {i}/{steps} ({i * dt:.0f} s sim): {i / (time.time() - t_loop):.1f} steps/s, "
                          f"policy {t_pol:.0f} s, env step {t_env:.0f} s, live {int((~done).sum())}/{n}, "
                          f"engaged {[int(x.sum()) for x in (handed if use_policy else present if stage4 else ctrl_push)]}", flush=True)
                if reassign_every and i > 0 and i % reassign_every == 0 and not stage4:
                    assign_all([j for j in range(n) if not bool(done[j])])
                obj_pos, obj_yaw = g.box_pos()[:, :2], g.heading()
                _, e = g.errors()
                e = torch.where(g.symmetry() > 0, e, torch.zeros_like(e))
                act = torch.zeros(n, 6, device=dev)
                pushing, engaged, cdist, herr = [], [], [], []
                if use_policy or stage4:
                    sync(); t0 = time.time()  # noqa: E702
                    pol_act = policy(obs)
                    sync(); t_pol += time.time() - t0  # noqa: E702
                else:
                    pol_act = None
                c_o, s_o = torch.cos(obj_yaw), torch.sin(obj_yaw)
                for k, ag in enumerate(AGENTS):
                    r = robots[k]
                    tw, ph = ctrl[k](r.data.root_link_pos_w[:, :2], yaw_of(r.data.root_link_quat_w), obj_pos, obj_yaw,
                                     radius, p_obj[k], n_obj[k], com_t, g.goal_xy, e, pre_obj=pre_obj[k],
                                     partner_pos=robots[1 - k].data.root_link_pos_w[:, :2], active=active[k])
                    a_k = to_action(tw)
                    p_w = obj_pos + torch.stack([c_o * p_obj[k][:, 0] - s_o * p_obj[k][:, 1],
                                                 s_o * p_obj[k][:, 0] + c_o * p_obj[k][:, 1]], -1)
                    dk = torch.linalg.norm(front_point(k) - p_w, dim=-1)
                    n_w = torch.stack([c_o * n_obj[k][:, 0] - s_o * n_obj[k][:, 1], s_o * n_obj[k][:, 0] + c_o * n_obj[k][:, 1]], -1)
                    hk = wrap(yaw_of(r.data.root_link_quat_w) - torch.atan2(-n_w[:, 1], -n_w[:, 0])).abs()
                    if stage4:  # the contact policy drives both robots from the start
                        a_k = pol_act[:, 3 * k:3 * k + 3]
                        dk = g.contact_dist(k)
                        hk = g.contact_heading_err(k)
                        engaged.append(present[k].clone())
                    elif use_policy:
                        if a.return_dist > 0:  # drifted off the contact: back to the script
                            back = handed[k] & (dk > a.return_dist)
                            returns[k] += back.float() * (~done).float()
                            if bool(back.any()):
                                ctrl[k].reset(back)
                            handed[k] &= ~back
                        handed[k] |= ph & active[k] & ~handed[k] & (dk < a.return_dist if a.return_dist > 0 else True)
                        handed[k] &= active[k]
                        a_k = torch.where(handed[k].unsqueeze(-1), pol_act[:, 3 * k:3 * k + 3], a_k)
                        engaged.append(handed[k].clone())
                    else:
                        engaged.append(ph & active[k])
                    act[:, 3 * k:3 * k + 3] = torch.where(active[k].unsqueeze(-1), a_k, idle.expand(n, 3))
                    pushing.append(ph & active[k])
                    cdist.append(dk)
                    herr.append(hk)
                if rp is not None:  # replay: the recorded command instead of the executor's
                    ridx = min(int(i * dt / 0.1), rcmd.shape[1] - 1)
                    rwin = (i * dt) < rlen * 0.1
                    for k in range(2):
                        tm = terms_[k]
                        c_rec = torch.where(rwin.unsqueeze(-1), rcmd[:, ridx, k], torch.zeros_like(rcmd[:, ridx, k]))
                        act[:, 3 * k:3 * k + 3] = 2.0 * (c_rec - tm._lo) / (tm._hi - tm._lo) - 1.0
                sync(); t0 = time.time()  # noqa: E702
                o_, _, _, _, _ = base.step(act)
                sync(); t_env += time.time() - t0  # noqa: E702
                ctrl_push = pushing
                obs = TensorDict({kk: v for kk, v in o_.items() if not kk.startswith("walker_")}, batch_size=[n])
                t = (i + 1) * dt
                live = ~done
                f_any = torch.zeros(n, dtype=torch.bool, device=dev)
                for k, ag in enumerate(AGENTS):
                    f = falls.fallen(base, asset_name=ag, nominal_height=SPECS[ag].nominal_height) & live & present[k]
                    fell[k] |= f
                    f_any |= f
                tip = hb.box_tipped(base) & live & ~f_any
                lost = cm.box_lost(base) & live & ~f_any & ~tip
                d, e2 = g.errors()
                ea = e2.abs()
                ok = live & ~f_any & ~tip & ~lost
                last_d = torch.where(ok, d, last_d)
                last_e = torch.where(ok, ea, last_e)
                min_d = torch.where(ok, torch.minimum(min_d, d), min_d)
                precise |= ok & g.success_flag
                inside = ok & (d < pt) & (ea < yt)
                hold = torch.where(inside, hold + dt, torch.zeros_like(hold))
                succ = ok & (hold >= 1.0)
                t_succ = torch.where(succ, torch.full_like(t_succ, t), t_succ)
                touch += (cm.robots_touching(base) > 0).float() * live.float() * two.float()
                live_steps += live.float()
                pu = [geo_pushing(k) & live for k in range(2)]
                for k in range(2):
                    push_steps[k] += pu[k].float()
                    mode_steps[k] += (pushing[k] & live).float()
                    el = (engaged[k] & live).float()
                    eng_steps[k] += el
                    cdist_sum[k] += el * cdist[k]
                    on_steps[k] += el * (cdist[k] < 0.25).float()
                    face_steps[k] += el * (herr[k] < math.radians(45.0)).float()
                if stage4:
                    for k, ag in enumerate(AGENTS):
                        lk = live & present[k]
                        onk = g.on_contact(k)
                        touching = base.scene[f"push_{ag}"].data.found.view(n, -1).any(-1)
                        bump_steps[k] += (lk & touching & ~onk).float()
                        press_steps[k] += (lk & onk & (g.surface_distance(ag) < 0.08)).float()
                        changed = (g.c_pobj[:, k] - prev_c[k]).abs().sum(-1) > 1e-6
                        prev_c[k] = g.c_pobj[:, k].clone()
                        miss_n[k] += (changed & waiting[k] & lk).float()
                        t_assign[k] = torch.where(changed, torch.full_like(t_assign[k], t), t_assign[k])
                        waiting[k] = torch.where(changed, lk, waiting[k])
                        got = waiting[k] & onk & lk
                        reach_sum[k] += torch.where(got, t - t_assign[k], torch.zeros_like(t_assign[k]))
                        reach_n[k] += got.float()
                        waiting[k] &= ~got
                if stage4:
                    pr = [live & present[k] & g.on_contact(k) & (g.surface_distance(AGENTS[k]) < 0.08) for k in range(2)]
                    far = [present[k] & (g.contact_dist(k) > 1.0) for k in range(2)]
                    still = torch.linalg.norm(g.box_vel()[:, :2], dim=-1) < 0.05
                    for k, ag in enumerate(AGENTS):
                        fk = torch.linalg.norm(cm.object_force_from(base, ag), dim=-1)
                        bk = (fk / FB).long().clamp(0, 50).view(-1, 1)
                        tk = pr[k] & base.scene[f"push_{ag}"].data.found.view(n, -1).any(-1)  # pressing and in contact
                        fb_all.scatter_add_(1, bk, tk.float().view(-1, 1))
                        fb_still.scatter_add_(1, bk, (tk & still).float().view(-1, 1))
                    if hasattr(g, "push_share"):
                        fa = [(cm.object_force_from(base, AGENTS[k]) * g.push_dir_world(k)).sum(-1).clamp(min=0.0)
                              for k in range(2)]
                        tot_c = g.push_share[:, 0] + g.push_share[:, 1]
                        ok_s = pr[0] & pr[1] & (fa[0] + fa[1] > 20.0) & (tot_c > 1e-6)
                        s_cmd = g.push_share[:, 0] / tot_c.clamp(min=1e-6)
                        s_meas = fa[0] / (fa[0] + fa[1]).clamp(min=1e-6)
                        w_s = ok_s.float() * dt
                        sh_t += w_s
                        sh_err += w_s * (s_meas - s_cmd).abs()
                        bi = (s_cmd * SHARE_BINS).long().clamp(0, SHARE_BINS - 1).view(-1, 1)
                        sh_bt.scatter_add_(1, bi, w_s.view(-1, 1))
                        sh_bm.scatter_add_(1, bi, (w_s * s_meas).view(-1, 1))
                    if getattr(g.cfg, "effort", False):
                        for k in range(2):
                            tg = cm.push_effort(base, k)
                            fk = (cm.object_force_from(base, AGENTS[k]) * g.push_dir_world(k)).sum(-1).clamp(min=0.0)
                            w_e = (pr[k] & (tg > 10.0)).float() * dt
                            ef_t += w_e
                            ef_cmd += w_e * tg
                            ef_meas += w_e * fk
                            ef_err += w_e * (fk - tg).abs()
                    solo_far += sum((pr[k] & far[1 - k]).float() for k in range(2)) * dt
                    press_any += (pr[0] | pr[1]).float()
                    press_both += (pr[0] & pr[1]).float()
                    for k in range(2):
                        xy = robots[k].data.root_link_pos_w[:, :2]
                        stepm = torch.linalg.norm(xy - last_xy[k], dim=-1)
                        walked += torch.where(live & present[k] & (stepm < 0.5), stepm, torch.zeros_like(stepm))  # (< 0.5: not a reset)
                        last_xy[k] = xy.clone()
                    if getattr(g.cfg, "exec_v2", False):
                        grp = torch.stack(present, -1)
                        cmd = g.c_cmd
                        ah = live & ((cmd == 1) | ~grp).all(-1) & grp.any(-1)
                        spd = torch.linalg.norm(g.box_vel()[:, :2], dim=-1)
                        allhold_t += ah.float() * dt
                        allhold_v += torch.where(ah, spd, torch.zeros_like(spd)) * dt
                        allhold_mv += (ah & (spd > 0.02)).float() * dt
                        for k, ag in enumerate(AGENTS):
                            hk = live & present[k] & (cmd[:, k] == 1)
                            fk = torch.linalg.norm(cm.object_force_from(base, ag), dim=-1)
                            holdf_sum += torch.where(hk, fk, torch.zeros_like(fk)) * dt
                            holdf_t += hk.float() * dt
                        tch = [pr[k] & base.scene[f"push_{AGENTS[k]}"].data.found.view(n, -1).any(-1) for k in range(2)]
                        allp = (tch[0] | ~present[0]) & (tch[1] | ~present[1])
                        tr = g.c_team_ready & live
                        start = tr & (tr_wait < 0)
                        tr_wait = torch.where(start, torch.zeros_like(tr_wait), tr_wait)
                        done_w = (tr_wait >= 0) & allp
                        tr_sum += torch.where(done_w, tr_wait, torch.zeros_like(tr_wait))
                        tr_n += done_w.float()
                        tr_wait = torch.where(done_w | ~tr, torch.full_like(tr_wait, -1.0), tr_wait)
                        tr_wait = torch.where(tr_wait >= 0, tr_wait + dt, tr_wait)
                    if getattr(g.cfg, "expert", False):
                        onb = torch.stack([g.on_contact(k) for k in range(2)], -1) & live.unsqueeze(-1)
                        hold_steps += ((g.c_phase == 1) & onb).float().sum(-1)
                        on_any_steps += onb.float().sum(-1)
                if dg is not None:
                    dgi = dgm.gather(g, base, robots, AGENTS, torch.stack(present, -1), live, cm.object_force_from,
                                     (d < pt) & (ea < yt))
                    dg.observe(**dgi)
                    if tr_ids and i % 5 == 0:
                        ti = torch.tensor(tr_ids, device=dev)
                        bp, hd = g.box_pos()[ti, :2], g.heading()[ti]
                        fm = torch.linalg.norm(dgi["force"][ti], dim=-1)
                        cosf = (dgi["force"][ti] * dgi["push_dir"][ti]).sum(-1) / fm.clamp(min=1e-6)
                        cols = [torch.full_like(hd, t), bp[:, 0], bp[:, 1], torch.rad2deg(hd), d[ti], torch.rad2deg(ea[ti]),
                                dgi["pe"][ti], torch.linalg.norm(dgi["v_obj"][ti], dim=-1), dgi["w_obj"][ti],
                                live[ti].float(), (dgi["go"][ti].float() if dgi["go"] is not None else torch.full_like(hd, -1))]
                        has_sh = hasattr(g, "push_share") and getattr(g.cfg, "wrench", False)
                        cols += [torch.linalg.norm(g.c_vdes[ti], dim=-1) if has_sh else torch.full_like(hd, -1),
                                 torch.rad2deg(g.c_wdes[ti]) if has_sh else torch.full_like(hd, -1),
                                 g.c_resid[ti] if has_sh else torch.full_like(hd, -1)]
                        for k in range(2):
                            cols += [dgi["cmd"][ti, k].float(), dgi["on"][ti, k].float(), dgi["engaged"][ti, k].float(),
                                     dgi["cdist"][ti, k], torch.rad2deg(dgi["herr"][ti, k]), dgi["touch"][ti, k].float(),
                                     fm[:, k], cosf[:, k], dgi["base_speed"][ti, k],
                                     g.push_share[ti, k] if has_sh else torch.full_like(hd, -1), fm[:, k] * cosf[:, k]]
                        for k, ag in enumerate(AGENTS):  # the walker interface: what it is told vs what it does
                            wc = base.command_manager.get_command(f"twist_{ag}")[ti]
                            rd_ = robots[k].data
                            cols += [wc[:, 0], wc[:, 1], wc[:, 2], rd_.root_link_lin_vel_b[ti, 0], rd_.root_link_lin_vel_b[ti, 1],
                                     rd_.root_link_ang_vel_b[ti, 2], fell[k][ti].float()]
                        tr_rows.append(torch.stack(cols, -1).cpu().numpy())
                if stage4 and g.cfg.wrench:
                    resid_sum += g.c_resid * live.float()
                both = pu[0] & pu[1]
                copush += both.float()
                spread_sum += torch.where(both, torch.linalg.norm(front_point(0) - front_point(1), dim=-1), torch.zeros(n, device=dev))
                rd = torch.linalg.norm(robots[0].data.root_link_pos_w[:, :2] - robots[1].data.root_link_pos_w[:, :2], dim=-1)
                min_rd = torch.where(live & two, torch.minimum(min_rd, rd), min_rd)
                for j in f_any.nonzero().flatten().tolist():
                    how[j] = "fell_" + "+".join(ag for k, ag in enumerate(AGENTS) if bool(fell[k][j]))
                for j in tip.nonzero().flatten().tolist():
                    how[j] = "tipped"
                for j in lost.nonzero().flatten().tolist():
                    how[j] = "lost"
                for j in succ.nonzero().flatten().tolist():
                    how[j] = "success"
                if rp is not None:
                    tip = tip & False; lost = lost & False; succ = succ & False  # noqa: E702  (only falls end a replay)
                    for k in range(2):
                        rd_ = robots[k].data
                        vb, wb = rd_.root_link_lin_vel_b[:, :2], rd_.root_link_ang_vel_b[:, 2]
                        c_rec = rcmd[:, ridx, k]
                        m_ = (rwin & live & ~fell[k]).float()
                        sp_ = torch.linalg.norm(c_rec[:, :2], dim=-1)
                        mv = m_ * (sp_ >= 0.1).float()
                        rp["pn"][:, k] += mv * (vb * c_rec[:, :2]).sum(-1) / sp_.clamp(min=1e-6) * dt
                        rp["pd"][:, k] += mv * sp_ * dt
                        rp["yerr"][:, k] += m_ * (wb - c_rec[:, 2]).abs() * dt
                        rp["ycum"][:, k] += m_ * (wb - c_rec[:, 2]) * dt
                        rp["win"][:, k] += m_ * dt
                        newf = fell[k] & (rp["tfall"][:, k] < 0)
                        rp["tfall"][:, k] = torch.where(newf, torch.full_like(rp["tfall"][:, k], t), rp["tfall"][:, k])
                    if i % 5 == 0:
                        rp["seq_c"].append(torch.stack([rcmd[:, ridx, k, 0] for k in range(2)], -1).cpu())
                        rp["seq_v"].append(torch.stack([robots[k].data.root_link_lin_vel_b[:, 0] for k in range(2)], -1).cpu())
                    if i * dt > float(rlen.max()) * 0.1 + 0.5:
                        break
                ended = f_any | tip | lost | succ
                t_end = torch.where(ended & ~done, torch.full_like(t_end, t), t_end)
                done |= ended
                if fid is not None and (i + 1) % stride == 0:
                    record()
                if all_done_at is None and bool(done.all()):
                    all_done_at = i
                if all_done_at is not None and i >= all_done_at + tail:
                    break

        if rp is not None:
            sc, sv = torch.stack(rp["seq_c"], 1).numpy(), torch.stack(rp["seq_v"], 1).numpy()  # (n, T, 2)
            outp = ROOT / "logs" / "evals" / f"{prefix}-{cases[0][0]}" / "pair" / f"replay_{mass:g}kg.csv"
            outp.parent.mkdir(parents=True, exist_ok=True)
            with open(outp, "w", newline="") as fh:
                wr = csv.writer(fh)
                wr.writerow(["object", "scenario", "mass", "robot", "interface", "rec_s", "orig_outcome", "orig_fell", "fell", "t_fall",
                             "window_s", "progress", "yaw_rate_err", "heading_drift_deg", "delay_s"])
                for j, (rule_, o_n, s_i, r_, _) in enumerate(cases):
                    L_ = int(rlen[j])
                    if L_ == 0:
                        continue
                    for k, ag in enumerate(AGENTS):
                        T_ = min(L_, sc.shape[1])
                        tf = float(rp["tfall"][j, k])
                        if tf > 0:
                            T_ = min(T_, int(tf / 0.1))
                        cx, vx_ = sc[j, :T_, k], sv[j, :T_, k]
                        delay = ""
                        if T_ > 30 and cx.std() > 0.05 and vx_.std() > 0.02:
                            cc = [np.corrcoef(cx[:T_ - lg], vx_[lg:T_])[0, 1] for lg in range(16)]
                            delay = f"{0.1 * int(np.nanargmax(cc)):.1f}"
                        w_ = float(rp["win"][j, k])
                        wr.writerow([o_n, SCENARIOS[s_i][0], f"{mass:g}", ag, os.environ.get("QUADCOOP_CMD_IF", "raw"),
                                     f"{L_ * 0.1:.1f}", rinfo[j][0], int(rinfo[j][1][k] > 0.5), int(tf > 0), f"{tf:.2f}" if tf > 0 else "",
                                     f"{w_:.1f}", f"{float(rp['pn'][j, k] / rp['pd'][j, k].clamp(min=1e-6)):.3f}",
                                     f"{float(rp['yerr'][j, k]) / max(w_, 1e-6):.3f}", f"{math.degrees(float(rp['ycum'][j, k])):.1f}", delay])
            print(f"replay: {outp}", flush=True)
        if tr_rows:  # per-step traces of the rep-0 episodes, one file per rule
            import gzip
            arr = np.stack(tr_rows, 1)  # (episodes, samples, fields)
            head = ["t", "obj_x", "obj_y", "obj_yaw_deg", "goal_dist", "goal_yaw_err_deg", "pose_err", "obj_speed", "obj_yaw_rate",
                    "live", "team_pushing", "want_speed", "want_yaw_rate_deg", "pair_residual"] + [
                        f"{x}_{ag}" for ag in AGENTS for x in
                        ("cmd", "on", "engaged", "contact_dist", "heading_err_deg", "touching", "force",
                         "force_align", "base_speed", "share_cmd", "force_along_cmd")] + [
                        f"{x}_{ag}" for ag in AGENTS for x in ("wcmd_vx", "wcmd_vy", "wcmd_wz", "vx", "vy", "wz", "fell")]
            for rule_ in dict.fromkeys(cases[j][0] for j in tr_ids):
                pth = ROOT / "logs" / "evals" / f"{prefix}-{rule_}" / "pair" / f"trace_{mass:g}kg.csv.gz"
                pth.parent.mkdir(parents=True, exist_ok=True)
                with gzip.open(pth, "wt", newline="") as fh:
                    wr = csv.writer(fh)
                    wr.writerow(["object", "scenario", "outcome"] + head)
                    for ei, j in enumerate(tr_ids):
                        if cases[j][0] != rule_:
                            continue
                        for row_ in arr[ei]:
                            if row_[9] < 0.5 and row_[0] > float(t_end[j]) + 0.2:
                                break
                            wr.writerow([cases[j][1], SCENARIOS[cases[j][2]][0], how[j]] + [f"{v:.3f}" for v in row_])
                print(f"trace: {pth}", flush=True)
        for j, (rule, o, s, r, _) in enumerate(cases):
            ls = float(live_steps[j].clamp(min=1))
            duo = rule != "centre"  # (a two-robot rule may still have parked robot 2: contact_2 empty)
            cl = cands[o]
            c1, c2 = first_choice[0][j], first_choice[1][j]
            sep = ""
            if c1 is not None and c2 is not None:
                sep = round(float(np.linalg.norm(cl[c1].p - cl[c2].p)), 2)
            rows[rule].append({
                "object": o, "seen_shape": int(o in TRAIN_NAMES), "mass": mass, "scenario": SCENARIOS[s][0],
                "distance": SCENARIOS[s][1], "direction": SCENARIOS[s][2], "turn": round(math.degrees(float(turn[j])), 1),
                "rep": r, "success": int(how[j] == "success"), "precise": int(bool(precise[j])), "outcome": how[j],
                "t_success": round(float(t_succ[j]), 2) if how[j] == "success" else "",
                **{f"fell_{ag}": int(bool(fell[k][j])) for k, ag in enumerate(AGENTS)},
                "final_pos_err": round(float(last_d[j]), 3), "final_yaw_err": round(math.degrees(float(last_e[j])), 1),
                "min_pos_err": round(float(min_d[j]), 3),
                "touch_frac": round(float(touch[j]) / ls, 3) if duo else "",
                **{f"push_frac_{ag}": round(float(push_steps[k][j]) / ls, 3) if duo or k == 0 else ""
                   for k, ag in enumerate(AGENTS)},
                "copush_frac": round(float(copush[j]) / ls, 3) if duo else "",
                "copush_spread": round(float(spread_sum[j] / copush[j]), 2) if duo and float(copush[j]) > 0 else "",
                "min_robot_dist": round(float(min_rd[j]), 2) if duo and not bool(solo[j]) else "",
                **{f"push_mode_frac_{ag}": round(float(mode_steps[k][j]) / ls, 3) if duo or k == 0 else ""
                   for k, ag in enumerate(AGENTS)},
                "robots_used": 1 if bool(solo[j]) else 2,
                "switches": int(g.c_switches[j]) if stage4 else "",
                "overshoot": int(how[j] != "success" and float(min_d[j]) < 0.20 and float(last_d[j]) >= 0.30),
                **{f"engaged_frac_{ag}": round(float(eng_steps[k][j]) / ls, 3) if (duo and not bool(solo[j])) or k == 0 else ""
                   for k, ag in enumerate(AGENTS)},
                **{f"contact_dist_{ag}": (round(float(cdist_sum[k][j] / eng_steps[k][j]), 3) if float(eng_steps[k][j]) > 0 else "")
                   for k, ag in enumerate(AGENTS)},
                **{f"on_contact_{ag}": (round(float(on_steps[k][j] / eng_steps[k][j]), 3) if float(eng_steps[k][j]) > 0 else "")
                   for k, ag in enumerate(AGENTS)},
                **{f"facing_{ag}": (round(float(face_steps[k][j] / eng_steps[k][j]), 3) if float(eng_steps[k][j]) > 0 else "")
                   for k, ag in enumerate(AGENTS)},
                **{f"returns_{ag}": int(returns[k][j]) for k, ag in enumerate(AGENTS)},
                **({f"bump_frac_{ag}": round(float(bump_steps[k][j]) / ls, 3) for k, ag in enumerate(AGENTS)} if stage4 else {}),
                **(dg.row(j) if dg is not None else {}),
                **({f"press_frac_{ag}": round(float(press_steps[k][j]) / ls, 3) for k, ag in enumerate(AGENTS)} if stage4 else {}),
                "mean_residual": round(float(resid_sum[j]) / ls, 3) if stage4 and g.cfg.wrench else "",
                "solo_far_s": round(float(solo_far[j]), 2) if stage4 else "",
                "both_press_share": (round(float(press_both[j] / press_any[j]), 3) if float(press_any[j]) > 0 else "") if stage4 else "",
                "walked_m": round(float(walked[j]), 1) if stage4 else "",
                "stall_replans": int(g.c_replans[j]) if stage4 and getattr(g.cfg, "expert", False) else "",
                "limit_replans": int(g.c_replan_weak[j]) if stage4 and getattr(g.cfg, "expert", False) else "",
                "finish_stalls": int(g.c_fin_stalls[j]) if stage4 and getattr(g.cfg, "expert", False) else "",
                "push_force_med": hist_q(fb_all[j], 0.5) if stage4 else "",
                **({"all_hold_s": round(float(allhold_t[j]), 2),
                    "all_hold_speed": round(float(allhold_v[j] / allhold_t[j]), 3) if float(allhold_t[j]) > 0 else "",
                    "all_hold_moving_share": round(float(allhold_mv[j] / allhold_t[j]), 3) if float(allhold_t[j]) > 0 else "",
                    "hold_force": round(float(holdf_sum[j] / holdf_t[j]), 1) if float(holdf_t[j]) > 0 else "",
                    "ready_to_push_s": round(float(tr_sum[j] / tr_n[j]), 2) if float(tr_n[j]) > 0 else ""}
                   if stage4 and getattr(g.cfg, "exec_v2", False) else {}),
                "push_force_p90": hist_q(fb_all[j], 0.9) if stage4 else "",
                "effort_s": round(float(ef_t[j]), 2) if stage4 else "",
                "effort_target": round(float(ef_cmd[j] / ef_t[j]), 1) if stage4 and float(ef_t[j]) > 0 else "",
                "effort_applied": round(float(ef_meas[j] / ef_t[j]), 1) if stage4 and float(ef_t[j]) > 0 else "",
                "effort_abs_err": round(float(ef_err[j] / ef_t[j]), 1) if stage4 and float(ef_t[j]) > 0 else "",
                "share_s": round(float(sh_t[j]), 2) if stage4 else "",
                "share_err": round(float(sh_err[j] / sh_t[j]), 3) if stage4 and float(sh_t[j]) > 0 else "",
                **({f"share_b{b_}_s": round(float(sh_bt[j, b_]), 3) for b_ in range(SHARE_BINS)} if stage4 else {}),
                **({f"share_b{b_}_m": round(float(sh_bm[j, b_] / sh_bt[j, b_]), 3) if float(sh_bt[j, b_]) > 0 else ""
                    for b_ in range(SHARE_BINS)} if stage4 else {}),
                "push_force_still_p90": hist_q(fb_still[j], 0.9) if stage4 else "",
                "needs_more_s": round(float(g.c_need_more_t[j]), 1) if stage4 and getattr(g.cfg, "expert", False) else "",
                "hold_share": (round(float(hold_steps[j] / on_any_steps[j]), 3) if float(on_any_steps[j]) > 0 else "")
                if stage4 and getattr(g.cfg, "expert", False) else "",
                **({f"reach_time_{ag}": (round(float(reach_sum[k][j] / reach_n[k][j]), 2) if float(reach_n[k][j]) > 0 else "")
                    for k, ag in enumerate(AGENTS)} if stage4 else {}),
                **({f"reached_{ag}": (round(float(reach_n[k][j]) / float(reach_n[k][j] + miss_n[k][j] + float(waiting[k][j])), 3)
                                      if float(reach_n[k][j] + miss_n[k][j] + float(waiting[k][j])) > 0 else "")
                    for k, ag in enumerate(AGENTS)} if stage4 else {}),
                "disturbed": int(stage4 and float(g.d_t1[j]) > 0 and float(g.d_t0[j]) < float(t_end[j])) if stage4 else "",
                "contact_1": "" if c1 is None else cl[c1].label, "contact_2": "" if c2 is None else cl[c2].label,
                "contact_sep": sep, "contact_idx_1": "" if c1 is None else int(c1),
                "contact_idx_2": "" if c2 is None else int(c2), "video": ""})
        if fid is not None:
            try:
                cam = Camera(base, vw, vh)
                Q, P = np.stack(rec_q, 1), np.stack(rec_pts, 1)
                MP = np.stack(rec_mp, 1) if rec_mp else None
                MQ = np.stack(rec_mq, 1) if rec_mq else None
                MK = np.stack(rec_mark, 1) if rec_mark else None
                CP = np.stack(rec_cap, 1) if rec_cap else None
                touched = set()
                for fi, j in enumerate(film_ids):
                    rule, o, s, r, _ = cases[j]
                    F = min(Q.shape[1], int(float(t_end[j]) / (stride * dt)) + int(1.0 / (stride * dt)) + 1)
                    vdir = (ROOT / a.video_dir / f"{prefix}-{rule}") if a.video_dir else \
                        ROOT / "logs" / "evals" / f"{prefix}-{rule}" / "pair" / "videos"
                    stem = f"{o}_{mass:g}kg_{SCENARIOS[s][0]}_r{r}"
                    name = f"{stem}__{how[j]}.mp4"
                    row = rows[rule][-n_of[rule]:][[(oo, ss, rr) for oo, ss, rr in base_cases].index((o, s, r))]
                    head = f"{rule}: {o} {mass:g} kg {SCENARIOS[s][0]} rep {r} -> {how[j]}"
                    legend = (f"cyan {AGENTS[0]}, yellow {AGENTS[1]} | post = contact (faint: not on it), "
                              "arrow = push, dot = waypoint") if MK is not None else ""

                    def cap(f, fi=fi, head=head, legend=legend):
                        txt = f"{head} | t {f * stride * dt:4.1f} s"
                        if CP is not None:
                            d_, e_, sw, c0, c1, trd, f0, f1, rl = CP[fi, f]
                            on = MK[fi, f, :, 6]
                            cmd = {0.0: "WALK", 1.0: "HOLD", 2.0: "PUSH"}
                            r0 = f" {cmd.get(float(c0), '')}" if c0 >= 0 else ""
                            r1 = f" {cmd.get(float(c1), '')}" if c1 >= 0 else ""
                            ff0 = f" {f0:.0f} N" if f0 >= 0 else ""
                            ff1 = f" {f1:.0f} N" if f1 >= 0 else ""
                            team = (" | team READY" if trd > 0.5 else " | team not ready") if trd >= 0 else ""
                            txt += (f"\nto goal {d_:.2f} m, {e_:+.0f} deg | cyan {'ON' if on[0] > 0.5 else 'off'}{r0}{ff0}, "
                                    f"yellow {'ON' if on[1] > 0.5 else 'off'}{r1}{ff1}{team} | contact changes {sw:.0f}"
                                    f" | rule {int(rl)}\n{legend}")
                        return txt

                    def marks(f, fi=fi):
                        if MK is None:
                            return None
                        out = []
                        for k, col in enumerate(((0.0, 0.95, 0.95), (1.0, 0.85, 0.0))):
                            px, py, dx, dy, wx, wy, on = MK[fi, f, k]
                            alpha = 1.0 if on > 0.5 else 0.4
                            # a post standing on the contact point (visible above the robot when it is there),
                            # the push direction at its top, and the route waypoint on the ground
                            out.append(("arrow", (px, py, 0.25), (px, py, 1.05), 0.012, (*col, alpha)))
                            out.append(("sphere", (px, py, 1.05), 0.07, (*col, alpha)))
                            out.append(("arrow", (px - 0.6 * dx, py - 0.6 * dy, 1.05), (px - 0.1 * dx, py - 0.1 * dy, 1.05),
                                        0.035, (*col, alpha)))
                            out.append(("sphere", (wx, wy, 0.05), 0.06, (*col, 0.9)))
                            rx, ry = P[fi, f, k]
                            out.append(("sphere", (rx, ry, 1.45), 0.11, (*col, 1.0)))  # which robot is which
                        return out

                    render_episode(cam, j, Q[fi, :F], None if MP is None else MP[fi, :F], None if MQ is None else MQ[fi, :F],
                                   P[fi, :F], vdir / name, 1.0 / (stride * dt), caption=cap, marks=marks)
                    row["video"] = str(vdir / name) if a.video_dir else f"videos/{name}"
                    keep = ("object", "scenario", "mass", "rep", "turn", "outcome", "success", "t_success", "final_pos_err",
                            "final_yaw_err", "min_pos_err", "switches", "copush_frac", "disturbed", "contact_1", "contact_2",
                            "mean_residual", "solo_far_s", "both_press_share", "walked_m", "stall_replans", "limit_replans", "finish_stalls", "needs_more_s", "hold_share",
                            "push_force_med", "push_force_p90", "push_force_still_p90",
                            *[f"{x}_{ag}" for x in ("on_contact", "press_frac", "reached", "reach_time", "bump_frac", "push_frac")
                              for ag in AGENTS])
                    (vdir / f"{stem}.json").write_text(json.dumps({**{k: row.get(k, "") for k in keep}, "rule": rule,
                                                                   "file": name, "checkpoint": a.checkpoint}))
                    touched.add(vdir)
                for vd in touched:
                    _video_index(vd)
            except Exception as ex:  # noqa: BLE001
                print(f"videos skipped: {ex}")
        for rule in rules:
            mine = rows[rule][-n_of[rule]:]
            print(f"[{mass:g} kg] {rule:8s} success {sum(x['success'] for x in mine) / len(mine):.2f}  falls "
                  + " ".join(f"{ag} {sum(x[f'fell_{ag}'] for x in mine) / len(mine):.2f}" for ag in AGENTS)
                  + (f"  both pushing {sum(x['copush_frac'] for x in mine) / len(mine):.2f}" if rule != "centre" else "")
                  + f"  ({time.time() - t_start:.0f} s)",
                  flush=True)
        base.close()
        del base
        for rule in rules:  # saved after every mass (merged with other masses already saved for this name)
            write(rows[rule], f"{prefix}-{rule}", rule, a, objects, AGENTS, TRAIN_NAMES, quiet=mass != masses[-1])
    return 0


def walker_record() -> dict:
    """Which walker each robot type ran on (and its kind), for the summary and for keeping results of
    different walkers apart."""
    import os

    from quadcoop.coop2.env_cfg import walker_kind

    out = {}
    for robot in ("anymal_c", "spot"):
        p = os.environ.get(f"QUADCOOP_WALKER_CKPT_{robot.upper()}", "")
        if p:
            out[robot] = {"checkpoint": p, "kind": walker_kind(robot),
                          "override": bool(os.environ.get(f"QUADCOOP_WALKER_OVERRIDE_{robot.upper()}", ""))}
    return out


def _num(v):
    if v == "":
        return v
    for f in (int, float):
        try:
            return f(v)
        except ValueError:
            pass
    return v


def _get(d, key):
    """d[key], or None when that object / scenario was not run at that mass (partial jobs)."""
    return None if d is None else d.get(key)


def write(rows, name, rule, a, objects, agents, train_names, quiet=False) -> None:
    """Write the summary for this rule. Rows of other (mass, object) combinations already saved under
    the same name with the same settings (another job, or an earlier mass of this one) are kept, so
    masses and objects can be run as separate jobs into one result. Jobs writing the same result at
    the same moment take turns (a lock file)."""
    import fcntl

    out = ROOT / "logs" / "evals" / name / "pair"
    out.mkdir(parents=True, exist_ok=True)
    with open(out / ".write.lock", "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        try:
            _write(rows, name, rule, a, objects, agents, train_names, quiet)
        finally:
            fcntl.flock(lock, fcntl.LOCK_UN)


def _video_index(vdir: Path) -> None:
    """index.csv / index.html of every filmed episode in vdir (from the per-episode .json files): failures
    first, then by object, scenario and mass; open index.html in a browser next to the videos."""
    import html
    recs = []
    for f in sorted(vdir.glob("*.json")):
        try:
            recs.append(json.loads(f.read_text()))
        except ValueError:
            continue
    if not recs:
        return
    recs.sort(key=lambda r: (int(r.get("success") or 0), str(r["object"]), str(r["scenario"]), float(r["mass"]), int(r["rep"])))
    cols = [k for k in recs[0] if k not in ("file", "checkpoint")]
    with open(vdir / "index.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols + ["file"], extrasaction="ignore")
        w.writeheader()
        w.writerows(recs)
    short = {"final_pos_err": "pos err (m)", "final_yaw_err": "yaw err (deg)", "min_pos_err": "closest (m)",
             "copush_frac": "both pushing"}
    show = ["outcome", "object", "scenario", "mass", "rep", "turn", "final_pos_err", "final_yaw_err", "min_pos_err",
            "switches", "copush_frac", "mean_residual", "solo_far_s", "both_press_share", "walked_m"] + [c for c in cols if c.startswith(("on_contact_", "press_frac_", "reached_", "bump_frac_"))]
    out = ["<!doctype html><meta charset='utf-8'><title>" + html.escape(vdir.name) + "</title>",
           "<style>body{font:13px sans-serif;margin:16px}table{border-collapse:collapse}td,th{border:1px solid #ccc;"
           "padding:3px 6px;text-align:center}tr.ok{background:#eefbe9}tr.bad{background:#fdecec}</style>",
           f"<h2>{html.escape(vdir.name)}</h2><p>{len(recs)} filmed episodes; checkpoint {html.escape(str(recs[0].get('checkpoint')))}. "
           "Cyan = robot 1, yellow = robot 2: post = assigned contact (faint when not on it), arrow = push direction, "
           "dot = route waypoint, ball high above a robot = which robot it is.</p><table><tr>"
           + "".join(f"<th>{html.escape(short.get(c, c))}</th>" for c in show) + "<th>video</th></tr>"]
    for r in recs:
        cls = "ok" if int(r.get("success") or 0) else "bad"
        out.append(f"<tr class='{cls}'>" + "".join(f"<td>{html.escape(str(r.get(c, '')))}</td>" for c in show)
                   + f"<td><video src='{html.escape(r['file'])}' controls preload='none' width='360'></video></td></tr>")
    out.append("</table>")
    (vdir / "index.html").write_text("\n".join(out) + "\n")


DIAG_KEYS = ("dg_walk", "dg_hold", "dg_push", "dg_push_press", "dg_push_light", "dg_push_notouch", "dg_hold_press", "dg_hold_move",
             "dg_drift", "dg_drift_dist", "dg_drift_head", "dg_edge", "dg_push_force", "dg_push_align", "dg_misaligned",
             "dg_both_press", "dg_one_press", "dg_none_press", "dg_obj_moving", "dg_obj_speed", "dg_obj_align", "dg_progress",
             "dg_still_n", "dg_still_s", "dg_still_force", "dg_go_breaks", "dg_flips_min",
             "dg_st_push_hard", "dg_st_push_soft", "dg_st_wait", "dg_st_hold", "dg_st_walk")


def _diag_md(summary, masses, objects) -> list:
    """The diagnosis tables (quadcoop.coop2.diag): means over episodes."""
    f2 = lambda x: "" if x is None else f"{x:.2f}"  # noqa: E731
    f0 = lambda x: "" if x is None else f"{x:.0f}"  # noqa: E731
    pc = lambda x: "" if x is None else f"{100 * x:.0f}%"  # noqa: E731
    bm = lambda m: summary["by_mass"][f"{m:g}"]  # noqa: E731
    md = ["", "## diagnosis 1: what each robot is told, and what it does then",
          "(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the "
          "time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the "
          "on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. "
          "Stage 4e has no commands: on its contact = told to push)", "",
          "| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving "
          "| drifted off | ... by distance | ... by heading | near zone edge |", "|---|" + "---|" * 12]
    for m in masses:
        s = bm(m)
        md.append(f"| {m:g} kg | " + " | ".join(pc(_get(s, k)) for k in (
            "dg_walk", "dg_hold", "dg_push", "dg_push_press", "dg_push_light", "dg_push_notouch", "dg_hold_press", "dg_hold_move",
            "dg_drift", "dg_drift_dist", "dg_drift_head", "dg_edge")) + " |")
    md += ["", "## diagnosis 2: the push (while told to push and pressing) and the team",
           "(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = "
           "exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)", "",
           "| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |", "|---|---|---|---|---|---|---|"]
    for m in masses:
        s = bm(m)
        md.append(f"| {m:g} kg | {f0(_get(s, 'dg_push_force'))} | {f2(_get(s, 'dg_push_align'))} | {pc(_get(s, 'dg_misaligned'))} | "
                  f"{pc(_get(s, 'dg_both_press'))} | {pc(_get(s, 'dg_one_press'))} | {pc(_get(s, 'dg_none_press'))} |")
    md += ["", "## diagnosis 3: the object and every standstill",
           "(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted "
           "motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its "
           "seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft "
           "= told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and "
           "holding, walk = nobody on a contact; per episode)", "",
           "| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait "
           "| hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |", "|---|" + "---|" * 14]
    for m in masses:
        s = bm(m)
        md.append(f"| {m:g} kg | {pc(_get(s, 'dg_obj_moving'))} | {f2(_get(s, 'dg_obj_speed'))} | {f2(_get(s, 'dg_obj_align'))} | "
                  f"{f2(_get(s, 'dg_progress'))} | {f2(_get(s, 'dg_still_n'))} | {f0(_get(s, 'dg_still_s'))} | "
                  + " | ".join(f0(_get(s, f"dg_st_{c}")) for c in ("push_hard", "push_soft", "wait", "hold", "walk"))
                  + f" | {f0(_get(s, 'dg_still_force'))} | {f2(_get(s, 'dg_go_breaks'))} | {f2(_get(s, 'dg_flips_min'))} |")
    md += ["", "## diagnosis 4: by object (all masses)", "",
           "| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) "
           "| push hard | push soft | wait | hold | walk |", "|---|" + "---|" * 12]
    for o in objects:
        s = summary["by_object"].get(o)
        if not s:
            continue
        md.append(f"| {o} | {f2(_get(s, 'success'))} | {pc(_get(s, 'dg_push_press'))} | {pc(_get(s, 'dg_both_press'))} | "
                  f"{f2(_get(s, 'dg_push_align'))} | {pc(_get(s, 'dg_obj_moving'))} | {f2(_get(s, 'dg_progress'))} | "
                  f"{f0(_get(s, 'dg_still_s'))} | " + " | ".join(f0(_get(s, f"dg_st_{c}")) for c in ("push_hard", "push_soft", "wait", "hold", "walk"))
                  + " |")
    return md


def _write(rows, name, rule, a, objects, agents, train_names, quiet=False) -> None:
    out = ROOT / "logs" / "evals" / name / "pair"
    stats = ROOT / "evals" / name / "eval" / "pair"
    mine = {(float(r["mass"]), r["object"]) for r in rows}
    try:
        old_meta = json.loads((out / "summary.json").read_text())
        same = all(old_meta.get(k) == v for k, v in (("executor", a.executor), ("return_dist", a.return_dist),
                                                       ("checkpoint", a.checkpoint), ("reselect", a.reselect_s), ("cmd_mode", getattr(a, "cmd_mode", "planner")),
                                                       ("reassign_s", a.reassign_s), ("reps", a.reps), ("agents", list(agents)))) and \
            old_meta.get("disturb_frac", 0.0) == a.disturb_frac and old_meta.get("start", "contact") == a.start and \
            old_meta.get("reselect_min_dist", "auto") == a.reselect_min_dist and \
            old_meta.get("tasks", "standard") == getattr(a, "tasks", "standard") and old_meta.get("set", "") == getattr(a, "set", "") and \
            bool(old_meta.get("swap_actors", False)) == bool(getattr(a, "swap_actors", False)) and \
            old_meta.get("walkers", walker_record()) == walker_record()
        old = [{k: _num(v) for k, v in r.items()} for r in csv.DictReader(open(out / "episodes.csv"))] if same else []
    except (OSError, ValueError):
        old = []
    rows = [r for r in old if (float(r["mass"]), r["object"]) not in mine] + list(rows)
    rows.sort(key=lambda r: float(r["mass"]))
    masses = sorted({float(r["mass"]) for r in rows})
    objects = [o for o in objects if any(r["object"] == o for r in rows)] + \
        [o for o in dict.fromkeys(r["object"] for r in rows) if o not in objects]
    with open(out / "episodes.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(dict.fromkeys(k for r in rows for k in r)), restval="")
        w.writeheader()
        w.writerows(rows)
    solo = rule == "centre"

    def mean(sel, key):
        v = [r.get(key, "") for r in sel if r.get(key, "") != ""]
        return sum(v) / len(v) if v else None

    def agg(sel):
        k = len(sel)
        if not k:
            return None
        ok = [r for r in sel if r["success"]]
        anyp = sum(max(r[f"push_frac_{agents[0]}"], r[f"push_frac_{agents[1]}"]) for r in sel) if not solo else 0
        outs = {}
        for r in sel:
            key = "fell" if str(r["outcome"]).startswith("fell") else str(r["outcome"])
            outs[key] = outs.get(key, 0) + 1
        return {"n": k, "two_robot_share": sum(r["robots_used"] == 2 for r in sel) / k,
                "outcome": {kk: v / k for kk, v in sorted(outs.items())},
                "overshoot": sum(int(r.get("overshoot") or 0) for r in sel) / k,
                "switches": mean(sel, "switches"),
                "mean_residual": mean(sel, "mean_residual"),
                **{key: mean(sel, key) for key in ("solo_far_s", "both_press_share", "walked_m", "stall_replans", "limit_replans", "finish_stalls",
                                                  "needs_more_s", "hold_share", "push_force_med", "push_force_p90",
                                                  "push_force_still_p90", "all_hold_s", "all_hold_speed",
                                                  "all_hold_moving_share", "hold_force", "ready_to_push_s")},
                **{key: mean(sel, key) for key in DIAG_KEYS},
                "success": sum(r["success"] for r in sel) / k, "precise": sum(r["precise"] for r in sel) / k,
                **{f"fell_{ag}": sum(r[f"fell_{ag}"] for r in sel) / k for ag in agents},
                "t_success": (sum(r["t_success"] for r in ok) / len(ok)) if ok else None,
                "touch_frac": mean(sel, "touch_frac"),
                **{f"push_frac_{ag}": mean(sel, f"push_frac_{ag}") for ag in agents},
                "copush_frac": mean(sel, "copush_frac"),
                "copush_share": None if solo else sum(r["copush_frac"] for r in sel) / max(1e-9, anyp),
                "copush_spread": mean(sel, "copush_spread"),
                **{f"push_mode_frac_{ag}": mean(sel, f"push_mode_frac_{ag}") for ag in agents},
                **{f"{key}_{ag}": mean(sel, f"{key}_{ag}") for key in ("engaged_frac", "contact_dist", "on_contact", "facing", "returns",
                                                                       "bump_frac", "reach_time", "reached", "press_frac")
                   for ag in agents}}

    by = defaultdict(list)
    for r in rows:
        by[("mass", r["mass"])].append(r)
        by[("obj_mass", r["object"], r["mass"])].append(r)
        by[("group_mass", "seen" if r["seen_shape"] else "unseen", r["mass"])].append(r)
        by[("scen_mass", r["scenario"], r["mass"])].append(r)
        by[("obj", r["object"])].append(r)
    what = (f"Stage 4 contact policy {a.checkpoint} (robots start {'at their contacts' if a.start == 'contact' else 'behind the object and walk to their contacts'}; contact rule re-applied: "
            f"{a.reselect_s if a.reselect_s != '0' else 'never'})" if a.executor == "stage4" else
            f"{'scripted contacts' if a.executor == 'script' else 'hand-off (script to the contact, then the frozen Stage 2b policy'}"
            + ("" if a.executor == "script" else (f", back to the script beyond {a.return_dist:g} m)" if a.return_dist > 0 else ", never back)"))
            + f", rule '{rule}' ({'one robot' if solo else 'two robots'}), pair {a.pair}") + \
           (f", re-chosen every {a.reassign_s:g} s" if a.reassign_s > 0 else "")
    if getattr(a, "tasks", "standard") == "turn":
        what += "; TASKS: turn in place (object at the goal position, heading off 15/30/60/90 deg, capped by symmetry)"
    if getattr(a, "set", ""):
        what += f"; planner settings changed: {a.set}"
    if getattr(a, "swap_actors", False):
        what += "; ACTORS SWAPPED (each robot runs the other's trained network)"
    ov = {r: v for r, v in walker_record().items() if v["override"]}
    if ov:
        what += "; WALKER OVERRIDE: " + ", ".join(f"{r} = {v['checkpoint']} ({v['kind']})" for r, v in ov.items())
    summary = {"policy": what, "name": name, "agents": list(agents), "masses": masses, "reps": a.reps,
               "horizon_s": a.horizon, "rule": rule, "reassign_s": a.reassign_s, "executor": a.executor,
               "return_dist": a.return_dist, "checkpoint": a.checkpoint, "reselect": a.reselect_s, "disturb_frac": a.disturb_frac,
               "start": a.start, "reselect_min_dist": a.reselect_min_dist, "cmd_mode": getattr(a, "cmd_mode", "planner"),
               "tasks": getattr(a, "tasks", "standard"), "set": getattr(a, "set", ""),
               "swap_actors": bool(getattr(a, "swap_actors", False)),
               "walkers": walker_record(),
               "overall": agg(rows),
               "by_mass": {f"{m:g}": agg(by[("mass", m)]) for m in masses},
               "by_group_mass": {f"{gname} / {m:g} kg": agg(by[("group_mass", gname, m)])
                                 for gname in ("seen", "unseen") for m in masses},
               "by_object_mass": {f"{o} / {m:g} kg": agg(by[("obj_mass", o, m)]) for o in objects for m in masses},
               "by_scenario_mass": {f"{s[0]} / {m:g} kg": agg(by[("scen_mass", s[0], m)]) for s in SCENARIOS for m in masses},
               "by_object": {o: agg(by[("obj", o)]) for o in objects}}
    (out / "summary.json").write_text(json.dumps(summary, indent=1))
    f2 = lambda x: "" if x is None else f"{x:.2f}"  # noqa: E731
    f0 = lambda x: "" if x is None else f"{x:.0f}"  # noqa: E731
    md = [f"# Pair evaluation: {name}", "", f"policy: {what}", "",
          f"success = 10 cm / 6 deg held 1 s within {a.horizon:g} s; precise = 10 cm / 3 deg with the object at rest; "
          f"{a.reps} placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as "
          "scripts/eval_coop2.py", "",
          "## by mass", "", f"| mass | success | precise | {agents[0]} fell | {agents[1]} fell | time to success (s) | robots touching "
          f"| {agents[0]} pushing | {agents[1]} pushing | both pushing | co-push share | contact spread (m) |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for m in masses:
        s = summary["by_mass"][f"{m:g}"]
        md.append(f"| {m:g} kg | {f2(s['success'])} | {f2(s['precise'])} | {f2(s[f'fell_{agents[0]}'])} | {f2(s[f'fell_{agents[1]}'])} | "
                  f"{'' if s['t_success'] is None else f'{s['t_success']:.1f}'} | {f2(s['touch_frac'])} | "
                  f"{f2(s[f'push_frac_{agents[0]}'])} | {f2(s[f'push_frac_{agents[1]}'])} | {f2(s['copush_frac'])} | "
                  f"{f2(s['copush_share'])} | {f2(s['copush_spread'])} |")
    md += ["", f"tasks using both robots: {summary['overall']['two_robot_share']:.2f} (the rest: no room for two "
           "pushers toward the goal, robot 2 parked)" if not solo else "",
           "", "## success by object and mass", "", "| object | contacts (A_straight, rep 0) | " +
           " | ".join(f"{m:g} kg" for m in masses) + " |", "|---|---|" + "---|" * len(masses)]
    for o in objects:
        ex = next((r for r in rows if r["object"] == o and r["scenario"] == "A_straight"), None)
        cdesc = "" if ex is None else (ex["contact_1"] + ("" if not ex["contact_2"] else f" + {ex['contact_2']}"))
        md.append(f"| {o}{'' if o in train_names else ' (unseen)'} | {cdesc} | "
                  + " | ".join(f2(_get(summary["by_object_mass"][f"{o} / {m:g} kg"], "success")) for m in masses) + " |")
    md += ["", "## how episodes ended (share) by mass", "",
           "| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |",
           "|---|---|---|---|---|---|---|---|"]
    for m in masses:
        s = summary["by_mass"][f"{m:g}"]
        oc = s["outcome"]
        md.append(f"| {m:g} kg | {f2(oc.get('success', 0.0))} | {f2(oc.get('horizon', 0.0))} | {f2(oc.get('fell', 0.0))} | "
                  f"{f2(oc.get('tipped', 0.0))} | {f2(oc.get('lost', 0.0))} | {f2(s['overshoot'])} | {f2(s['switches'])} |")
    eng = {"policy": "under the push policy", "stage4": "all the time"}.get(a.executor, "in push mode")
    md += ["", f"## holding the assigned contact (while {eng})", "",
           "| mass | " + " | ".join(f"{ag} engaged | {ag} front-contact dist (m) | {ag} within 0.25 m | {ag} facing it (45 deg) | {ag} returns"
                                   for ag in (agents if not solo else agents[:1])) + " |",
           "|---|" + "---|---|---|---|---|" * (2 if not solo else 1)]
    for m in masses:
        s = summary["by_mass"][f"{m:g}"]
        md.append(f"| {m:g} kg | " + " | ".join(
            f"{f2(s[f'engaged_frac_{ag}'])} | {f2(s[f'contact_dist_{ag}'])} | {f2(s[f'on_contact_{ag}'])} | "
            f"{f2(s.get(f'facing_{ag}'))} | {f2(s[f'returns_{ag}'])}"
            for ag in (agents if not solo else agents[:1])) + " |")
    if a.executor == "stage4":
        md += ["", "## reaching the assigned contact (each assignment: at the start and at every contact change)"
               + (f"; object shoved in {a.disturb_frac:g} of episodes" if a.disturb_frac > 0 else ""), "",
               "| mass | " + " | ".join(f"{ag} reached | {ag} time to reach (s) | {ag} bumping off-contact"
                                       for ag in (agents if not solo else agents[:1])) + " |",
               "|---|" + "---|---|---|" * (2 if not solo else 1)]
        for m in masses:
            s = summary["by_mass"][f"{m:g}"]
            md.append(f"| {m:g} kg | " + " | ".join(
                f"{f2(s.get(f'reached_{ag}'))} | {f2(s.get(f'reach_time_{ag}'))} | {f2(s.get(f'bump_frac_{ag}'))}"
                for ag in (agents if not solo else agents[:1])) + " |")
        md += ["", "## pressing the contact (front on the object while on its contact, share of time)"
               + ("; mean pair residual (wrench rule)" if any(r.get("mean_residual", "") != "" for r in rows) else ""), "",
               "| mass | " + " | ".join(f"{ag} pressing" for ag in (agents if not solo else agents[:1])) + " | residual |",
               "|---|" + "---|" * (2 if not solo else 1) + "---|"]
        for m in masses:
            s = summary["by_mass"][f"{m:g}"]
            md.append(f"| {m:g} kg | " + " | ".join(f"{f2(s.get(f'press_frac_{ag}'))}" for ag in (agents if not solo else agents[:1]))
                      + f" | {f2(s.get('mean_residual'))} |")
    if a.executor == "stage4" and not solo:
        md += ["", "## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with "
               "both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, "
               "re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no "
               "penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)", "",
               "| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | "
               "at-limit re-plans | finishing stalls | needs more robots (s) | holding |",
               "|---|---|---|---|---|---|---|---|---|---|"]
        for m in masses:
            s = summary["by_mass"][f"{m:g}"]
            md.append(f"| {m:g} kg | {f2(s.get('solo_far_s'))} | {f2(s.get('both_press_share'))} | {f2(s.get('walked_m'))} | "
                      f"{f2(s.get('switches'))} | {f2(s.get('stall_replans'))} | {f2(s.get('limit_replans'))} | "
                      f"{f2(s.get('finish_stalls'))} | {f2(s.get('needs_more_s'))} | {f2(s.get('hold_share'))} |")
        md += ["", "## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both "
               "robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile "
               "while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full "
               "resistance: the planner's robot_push_force should come from this)", "",
               "| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |", "|---|---|---|---|"]
        for m in masses:
            s = summary["by_mass"][f"{m:g}"]
            md.append(f"| {m:g} kg | {f0(s.get('push_force_med'))} | {f0(s.get('push_force_p90'))} | "
                      f"{f0(s.get('push_force_still_p90'))} |")
        if any(r.get("share_s") not in ("", None) for r in rows):
            md += ["", "## following the force split (while both robots press their contacts: robot 1's measured share of the "
                   "pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot "
                   "that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)", "",
                   "| mass | seconds | mean abs error | " + " | ".join(
                       f"told {b_ / SHARE_BINS:.1f}-{(b_ + 1) / SHARE_BINS:.1f}: measured (s)" for b_ in range(SHARE_BINS)) + " |",
                   "|---|---|---|" + "---|" * SHARE_BINS]
            share_sum = {}
            for m in masses:
                sel = [r for r in rows if r["mass"] == m and r.get("share_s") not in ("", None)]
                tt = sum(r["share_s"] for r in sel)
                err = sum(r["share_err"] * r["share_s"] for r in sel if r["share_err"] != "") / tt if tt > 0 else None
                cells, bins = [], []
                for b_ in range(SHARE_BINS):
                    bt = sum(r[f"share_b{b_}_s"] for r in sel)
                    bm_ = sum(r[f"share_b{b_}_m"] * r[f"share_b{b_}_s"] for r in sel if r[f"share_b{b_}_m"] != "")
                    cells.append(f"{bm_ / bt:.2f} ({bt:.0f})" if bt > 0 else "-")
                    bins.append({"seconds": bt, "measured": bm_ / bt if bt > 0 else None})
                share_sum[f"{m:g}"] = {"seconds": tt, "mean_abs_error": err, "bins": bins}
                md.append(f"| {m:g} kg | {tt:.0f} | {'' if err is None else f'{err:.2f}'} | " + " | ".join(cells) + " |")
            summary["share_following"] = share_sum
        if any(r.get("effort_s") not in ("", None, 0, 0.0) for r in rows):
            md += ["", "## push effort (force_track: while pressing with a target of 10 N+, the robot's push target against "
                   "the force it applies along its commanded direction; pooled robot-seconds)", "",
                   "| mass | robot-seconds | mean target (N) | mean applied (N) | mean abs error (N) |", "|---|---|---|---|---|"]
            eff_sum = {}
            for m in masses:
                sel = [r for r in rows if r["mass"] == m and r.get("effort_s") not in ("", None) and r.get("effort_target") != ""]
                tt = sum(r["effort_s"] for r in sel)
                wm_ = lambda key: sum(r[key] * r["effort_s"] for r in sel) / tt if tt > 0 else None  # noqa: E731
                eff_sum[f"{m:g}"] = {"seconds": tt, "target": wm_("effort_target"), "applied": wm_("effort_applied"),
                                     "abs_err": wm_("effort_abs_err")}
                e_ = eff_sum[f"{m:g}"]
                md.append(f"| {m:g} kg | {tt:.0f} | " + " | ".join("" if e_[x] is None else f"{e_[x]:.0f}"
                                                                   for x in ("target", "applied", "abs_err")) + " |")
            summary["effort_tracking"] = eff_sum
        if any(summary["by_mass"][f"{m:g}"].get("all_hold_s") is not None for m in masses):
            md += ["", "## executor v2: holding and the team-ready barrier (time every robot of the push group is told to "
                   "hold; the object's mean speed then and the share of it above 2 cm/s (gate: under 2 cm/s); each robot's "
                   "contact force while told to hold; delay from team ready to both robots pressing (gate: under 0.2 s))", "",
                   "| mass | all holding (s) | object speed (m/s) | moving > 2 cm/s | force while holding (N) | ready to push (s) |",
                   "|---|---|---|---|---|---|"]
            for m in masses:
                s = summary["by_mass"][f"{m:g}"]
                md.append(f"| {m:g} kg | {f2(s.get('all_hold_s'))} | {f2(s.get('all_hold_speed'))} | "
                          f"{f2(s.get('all_hold_moving_share'))} | {f0(s.get('hold_force'))} | {f2(s.get('ready_to_push_s'))} |")
    if not solo:
        md += ["", "## both robots pushing (share of time) by object and mass", "",
               "| object | " + " | ".join(f"{m:g} kg" for m in masses) + " |", "|---|" + "---|" * len(masses)]
        for o in objects:
            md.append(f"| {o} | " + " | ".join(f2(_get(summary["by_object_mass"][f"{o} / {m:g} kg"], "copush_frac"))
                                               for m in masses) + " |")
    md += ["", "## success by scenario and mass", "", "| scenario | " + " | ".join(f"{m:g} kg" for m in masses) + " |",
           "|---|" + "---|" * len(masses)]
    for s in SCENARIOS:
        md.append(f"| {s[0]} | " + " | ".join(f2(_get(summary["by_scenario_mass"][f"{s[0]} / {m:g} kg"], "success"))
                                             for m in masses) + " |")
    if any(_get(summary["by_mass"][f"{m:g}"], "dg_push") is not None for m in masses):
        md += _diag_md(summary, masses, objects)
    (out / "summary.json").write_text(json.dumps(summary, indent=1))  # again: with the sections added above
    (out / "summary.md").write_text("\n".join(md) + "\n")
    stats.mkdir(parents=True, exist_ok=True)
    for f in ("summary.md", "summary.json", "episodes.csv"):
        shutil.copy2(out / f, stats / f)
    if not quiet:
        print("\n".join(md[:14]))
    print(f"{name}: masses {', '.join(f'{m:g}' for m in masses)} saved in {stats}", flush=True)


if __name__ == "__main__":
    raise SystemExit(main())
