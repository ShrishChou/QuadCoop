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

    python scripts/contact_test.py --executor policy                       # prefix handoff-aa
    python scripts/contact_test.py --executor policy --return-dist 0 --prefix handoff-aa-free

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
RULES = ("centre", "adjacent", "spread")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pair", choices=("mixed", "anymal", "spot"), default="anymal")
    ap.add_argument("--prefix", default=None, help="output names <prefix>-<rule> (default contact-<pair>)")
    ap.add_argument("--rules", default=",".join(RULES))
    ap.add_argument("--objects", default="all")
    ap.add_argument("--masses", default="20,40,60,80")
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--horizon", type=float, default=80.0)
    ap.add_argument("--reassign-s", type=float, default=0.0, help="re-choose contacts every so many seconds (0 = once)")
    ap.add_argument("--executor", choices=("script", "policy"), default="script",
                    help="who pushes once a robot is at its contact: the scripted controller or the frozen Stage 2b policy")
    ap.add_argument("--return-dist", type=float, default=0.5,
                    help="policy executor: hand back to the script when the front is this far from the contact (0 = never)")
    ap.add_argument("--video-objects", default="cube,sphere,beam,dumbbell,arch,t_shape",
                    help="objects to film ('all' = every object); filmed: A_straight and D_far_turn, rep 0, --video-mass")
    ap.add_argument("--videos", type=int, default=1, help="1 = film rule x object (A_straight and D_far_turn) at --video-mass")
    ap.add_argument("--video-mass", type=float, default=60.0)
    ap.add_argument("--video-size", default="640x480")
    ap.add_argument("--device", default=None)
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()

    from train_coop2 import resolve_models, set_env

    models = resolve_models("b", a.pair)
    set_env(models)
    import numpy as np
    import torch
    from tensordict import TensorDict

    import quadcoop  # noqa: F401
    from mjlab.envs import ManagerBasedRlEnv

    from quadcoop import contacts as C
    from quadcoop import falls
    from quadcoop.contact_control import IDLE_ACTION, ContactController, to_action
    from quadcoop.coop2 import mdp as cm
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
    prefix = a.prefix or (f"contact-{tag}" if a.executor == "script" else f"handoff-{tag}")
    use_policy = a.executor == "policy"
    video_objects = None if a.video_objects == "all" else {o.strip() for o in a.video_objects.split(",")}
    rules = [r.strip() for r in a.rules.split(",")]
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
    cases = [(rule, o, s, r, k) for rule in rules for k, (o, s, r) in enumerate(base_cases)]
    n = len(cases)
    print(f"pair {a.pair}: rules {rules}; {len(objects)} objects x {len(SCENARIOS)} scenarios x {a.reps} reps = "
          f"{len(base_cases)} tasks per rule, {n} envs per mass; masses {masses}; reassign every "
          f"{a.reassign_s or 'never'} s; executor {a.executor}"
          + (f" (back to the script beyond {a.return_dist:g} m)" if use_policy and a.return_dist > 0 else ""), flush=True)
    rows = {rule: [] for rule in rules}
    t_start = time.time()

    for mass in masses:
        cfg = make_coop2_env_cfg("b", play=True)
        cfg.scene.num_envs = n
        cfg.episode_length_s = 1e5
        cfg.terminations = {}
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
        g.scenario = lambda env_ids: {k: ([x[env_ids] for x in v] if isinstance(v, list) else v[env_ids])
                                      for k, v in sc.items()}
        obs, _ = base.reset()
        g.scenario = None
        obs = TensorDict({k: v for k, v in obs.items() if not k.startswith("walker_")}, batch_size=[n])
        policy = PairPolicy(obs, device, "b", singles=models["policy"]) if use_policy else None
        robots = [base.scene[ag] for ag in AGENTS]
        handed = [torch.zeros(n, dtype=torch.bool, device=dev) for _ in AGENTS]  # under the push policy
        present = [torch.ones(n, dtype=torch.bool, device=dev), ~solo]  # robot 2 not parked
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
        assign_all(range(n))
        first_choice = [list(chosen[0]), list(chosen[1])]

        dt = base.step_dt
        steps = int(a.horizon / dt)
        reassign_every = int(round(a.reassign_s / dt)) if a.reassign_s > 0 else 0
        film_ids = [j for j, (rule, o, s, r, _) in enumerate(cases)
                    if a.videos > 0 and mass == a.video_mass and r == 0 and SCENARIOS[s][0] in ("A_straight", "D_far_turn")
                    and (video_objects is None or o in video_objects)]
        stride = 2
        rec_q, rec_mp, rec_mq, rec_pts = [], [], [], []
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
        returns = [torch.zeros(n, device=dev) for _ in AGENTS]

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
        with torch.no_grad():
            for i in range(steps):
                if reassign_every and i > 0 and i % reassign_every == 0:
                    assign_all([j for j in range(n) if not bool(done[j])])
                obj_pos, obj_yaw = g.box_pos()[:, :2], g.heading()
                _, e = g.errors()
                e = torch.where(g.symmetry() > 0, e, torch.zeros_like(e))
                act = torch.zeros(n, 6, device=dev)
                pushing, engaged, cdist = [], [], []
                pol_act = policy(obs) if use_policy else None
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
                    if use_policy:
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
                o_, _, _, _, _ = base.step(act)
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
                ended = f_any | tip | lost | succ
                t_end = torch.where(ended & ~done, torch.full_like(t_end, t), t_end)
                done |= ended
                if fid is not None and (i + 1) % stride == 0:
                    record()
                if all_done_at is None and bool(done.all()):
                    all_done_at = i
                if all_done_at is not None and i >= all_done_at + tail:
                    break

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
                **{f"engaged_frac_{ag}": round(float(eng_steps[k][j]) / ls, 3) if (duo and not bool(solo[j])) or k == 0 else ""
                   for k, ag in enumerate(AGENTS)},
                **{f"contact_dist_{ag}": (round(float(cdist_sum[k][j] / eng_steps[k][j]), 3) if float(eng_steps[k][j]) > 0 else "")
                   for k, ag in enumerate(AGENTS)},
                **{f"on_contact_{ag}": (round(float(on_steps[k][j] / eng_steps[k][j]), 3) if float(eng_steps[k][j]) > 0 else "")
                   for k, ag in enumerate(AGENTS)},
                **{f"returns_{ag}": int(returns[k][j]) for k, ag in enumerate(AGENTS)},
                "contact_1": "" if c1 is None else cl[c1].label, "contact_2": "" if c2 is None else cl[c2].label,
                "contact_sep": sep, "video": ""})
        if fid is not None:
            try:
                cam = Camera(base, vw, vh)
                Q, P = np.stack(rec_q, 1), np.stack(rec_pts, 1)
                MP = np.stack(rec_mp, 1) if rec_mp else None
                MQ = np.stack(rec_mq, 1) if rec_mq else None
                for fi, j in enumerate(film_ids):
                    rule, o, s, r, _ = cases[j]
                    F = min(Q.shape[1], int(float(t_end[j]) / (stride * dt)) + int(1.0 / (stride * dt)) + 1)
                    vdir = ROOT / "logs" / "evals" / f"{prefix}-{rule}" / "pair" / "videos"
                    name = f"{o}_{mass:g}kg_{SCENARIOS[s][0]}__{how[j]}.mp4"
                    row = rows[rule][-len(base_cases):][[(oo, ss, rr) for oo, ss, rr in base_cases].index((o, s, r))]
                    cap_txt = f"{rule}: {o} {mass:g}kg {SCENARIOS[s][0].split('_')[0]} -> {how[j]}"
                    render_episode(cam, j, Q[fi, :F], None if MP is None else MP[fi, :F], None if MQ is None else MQ[fi, :F],
                                   P[fi, :F], vdir / name, 1.0 / (stride * dt),
                                   caption=lambda f, c=cap_txt: f"{c} | t {f * stride * dt:4.1f}s")
                    row["video"] = f"videos/{name}"
            except Exception as ex:  # noqa: BLE001
                print(f"videos skipped: {ex}")
        for rule in rules:
            mine = rows[rule][-len(base_cases):]
            print(f"[{mass:g} kg] {rule:8s} success {sum(x['success'] for x in mine) / len(mine):.2f}  falls "
                  + " ".join(f"{ag} {sum(x[f'fell_{ag}'] for x in mine) / len(mine):.2f}" for ag in AGENTS)
                  + (f"  both pushing {sum(x['copush_frac'] for x in mine) / len(mine):.2f}" if rule != "centre" else "")
                  + f"  ({time.time() - t_start:.0f} s)",
                  flush=True)
        base.close()
        del base

    for rule in rules:
        write(rows[rule], f"{prefix}-{rule}", rule, a, masses, objects, AGENTS, TRAIN_NAMES)
    return 0


def write(rows, name, rule, a, masses, objects, agents, train_names) -> None:
    out = ROOT / "logs" / "evals" / name / "pair"
    stats = ROOT / "evals" / name / "eval" / "pair"
    out.mkdir(parents=True, exist_ok=True)
    with open(out / "episodes.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    solo = rule == "centre"

    def mean(sel, key):
        v = [r[key] for r in sel if r[key] != ""]
        return sum(v) / len(v) if v else None

    def agg(sel):
        k = len(sel)
        if not k:
            return None
        ok = [r for r in sel if r["success"]]
        anyp = sum(max(r[f"push_frac_{agents[0]}"], r[f"push_frac_{agents[1]}"]) for r in sel) if not solo else 0
        return {"n": k, "two_robot_share": sum(r["robots_used"] == 2 for r in sel) / k,
                "success": sum(r["success"] for r in sel) / k, "precise": sum(r["precise"] for r in sel) / k,
                **{f"fell_{ag}": sum(r[f"fell_{ag}"] for r in sel) / k for ag in agents},
                "t_success": (sum(r["t_success"] for r in ok) / len(ok)) if ok else None,
                "touch_frac": mean(sel, "touch_frac"),
                **{f"push_frac_{ag}": mean(sel, f"push_frac_{ag}") for ag in agents},
                "copush_frac": mean(sel, "copush_frac"),
                "copush_share": None if solo else sum(r["copush_frac"] for r in sel) / max(1e-9, anyp),
                "copush_spread": mean(sel, "copush_spread"),
                **{f"push_mode_frac_{ag}": mean(sel, f"push_mode_frac_{ag}") for ag in agents},
                **{f"{key}_{ag}": mean(sel, f"{key}_{ag}") for key in ("engaged_frac", "contact_dist", "on_contact", "returns")
                   for ag in agents}}

    by = defaultdict(list)
    for r in rows:
        by[("mass", r["mass"])].append(r)
        by[("obj_mass", r["object"], r["mass"])].append(r)
        by[("group_mass", "seen" if r["seen_shape"] else "unseen", r["mass"])].append(r)
        by[("scen_mass", r["scenario"], r["mass"])].append(r)
    what = (f"{'scripted contacts' if a.executor == 'script' else 'hand-off (script to the contact, then the frozen Stage 2b policy'}"
            + ("" if a.executor == "script" else (f", back to the script beyond {a.return_dist:g} m)" if a.return_dist > 0 else ", never back)"))
            + f", rule '{rule}' ({'one robot' if solo else 'two robots'}), pair {a.pair}") + \
           (f", re-chosen every {a.reassign_s:g} s" if a.reassign_s > 0 else "")
    summary = {"policy": what, "name": name, "agents": list(agents), "masses": masses, "reps": a.reps,
               "horizon_s": a.horizon, "rule": rule, "reassign_s": a.reassign_s, "executor": a.executor,
               "return_dist": a.return_dist, "overall": agg(rows),
               "by_mass": {f"{m:g}": agg(by[("mass", m)]) for m in masses},
               "by_group_mass": {f"{gname} / {m:g} kg": agg(by[("group_mass", gname, m)])
                                 for gname in ("seen", "unseen") for m in masses},
               "by_object_mass": {f"{o} / {m:g} kg": agg(by[("obj_mass", o, m)]) for o in objects for m in masses},
               "by_scenario_mass": {f"{s[0]} / {m:g} kg": agg(by[("scen_mass", s[0], m)]) for s in SCENARIOS for m in masses}}
    (out / "summary.json").write_text(json.dumps(summary, indent=1))
    f2 = lambda x: "" if x is None else f"{x:.2f}"  # noqa: E731
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
                  + " | ".join(f2(summary["by_object_mass"][f"{o} / {m:g} kg"]["success"]) for m in masses) + " |")
    eng = "under the push policy" if a.executor == "policy" else "in push mode"
    md += ["", f"## holding the assigned contact (while {eng})", "",
           "| mass | " + " | ".join(f"{ag} engaged | {ag} front-contact dist (m) | {ag} within 0.25 m | {ag} returns"
                                   for ag in (agents if not solo else agents[:1])) + " |",
           "|---|" + "---|---|---|---|" * (2 if not solo else 1)]
    for m in masses:
        s = summary["by_mass"][f"{m:g}"]
        md.append(f"| {m:g} kg | " + " | ".join(
            f"{f2(s[f'engaged_frac_{ag}'])} | {f2(s[f'contact_dist_{ag}'])} | {f2(s[f'on_contact_{ag}'])} | {f2(s[f'returns_{ag}'])}"
            for ag in (agents if not solo else agents[:1])) + " |")
    if not solo:
        md += ["", "## both robots pushing (share of time) by object and mass", "",
               "| object | " + " | ".join(f"{m:g} kg" for m in masses) + " |", "|---|" + "---|" * len(masses)]
        for o in objects:
            md.append(f"| {o} | " + " | ".join(f2(summary["by_object_mass"][f"{o} / {m:g} kg"]["copush_frac"])
                                               for m in masses) + " |")
    md += ["", "## success by scenario and mass", "", "| scenario | " + " | ".join(f"{m:g} kg" for m in masses) + " |",
           "|---|" + "---|" * len(masses)]
    for s in SCENARIOS:
        md.append(f"| {s[0]} | " + " | ".join(f2(summary["by_scenario_mass"][f"{s[0]} / {m:g} kg"]["success"])
                                             for m in masses) + " |")
    (out / "summary.md").write_text("\n".join(md) + "\n")
    stats.mkdir(parents=True, exist_ok=True)
    for f in ("summary.md", "summary.json", "episodes.csv"):
        shutil.copy2(out / f, stats / f)
    print("\n".join(md[:14]))
    print(f"stats in {stats}")


if __name__ == "__main__":
    raise SystemExit(main())
