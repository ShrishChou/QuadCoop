"""Test 1: does the planner's force model match the physics? No robots, no learning.

The expert planner decides where two robots push and how hard each pushes (its split) from a model:
quasi-static sliding on the floor (a limit surface with the object's friction and ground-contact
radius), pushes inside a friction cone, and a force limit per robot, robot_push_force (250 N, assumed)
against the force that slides the object (mu m g). Nothing has checked that the object then moves
the way the model says. This test applies the forces directly to the object, at the contact points,
with both robots parked 40 m away, and measures what the object does.

Every object x mass x wanted motion is pushed by:

    planner   the contact pair the planner's model rates best for this motion (lowest residual), with
              the planner's split (each robot's direction and share)
    equal     the same pair and directions, both robots equally hard (robots that ignore their share)
    single    each candidate contact alone, direction from the planner's split for one robot
    pair      every usable contact pair (standing points >= 0.85 m apart), each with its own split:
              the best of these is the best any pair-choosing planner could do with these pushes
    none      a control: no push (the object must stay put)

How hard: like a robot that pushes until the object goes, the pushes grow (keeping their directions
and ratio) while the object moves slower than --target-speed and ease off when faster, never past
--fmax N of normal force for the hardest-pressing robot (about 1 s from nothing to the limit). The
pushes stay fixed to the object (a robot on its contact turns with it). After --settle s at rest,
the push lasts --duration s; measured from --measure-from s on: the object's displacement and turn
as one motion vector (dx, dy, r_g x dyaw) (r_g = radius of gyration, so a turn and a move compare in
metres), its cosine with the wanted motion (1 = exactly as asked), whether it moved at all (>= 2 cm),
speed, yaw rate, rolling / tipping (|angular velocity about x, y|), the push level used (force
needed: the hardest robot's normal force, N) and whether the pushes ended at the limit. Object
friction is the middle of the training range (--friction random: randomised as in training).

Wanted motions (object frame; v = push_vmax, w = push_wmax, as the planner asks far from the goal):
    turn       pure turn, +w
    move_x     straight along the object's x (broadside for the long shapes)
    move_y     straight along the object's y (lengthwise)
    move_turn  move_x and turn together
(turns only for objects whose heading matters; the sphere has none)

The planner's predictions per push: residual (0 = the pushes can make the wanted motion, 1 = not at
all) and strength (>= 1: the pushes can slide the object that way within the force limits).

Output: logs/evals/<name>/cases.csv (every pushed case) and evals/<name>/ (summary.md, summary.json,
key.csv: the planner, equal, best single and best pair rows of every object x mass x motion).

    python scripts/planner_physics_test.py                                   # all objects, 20/40/60/80 kg, 250 N
    python scripts/planner_physics_test.py --fmax 150,250,350 --name pp-fsweep
    python scripts/planner_physics_test.py --objects cube,cylinder --masses 40 --pairs none --name pp-quick
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import shutil
import sys
import time
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT))

MOTIONS = ("turn", "move_x", "move_y", "move_turn")
MOVED = 0.02  # m of motion (|(dx, dy, r_g dyaw)|) over the window that counts as moving
GOOD = 0.8  # cosine with the wanted motion that counts as "as asked"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", default="pp-test", help="output folder name under logs/evals/ and evals/")
    ap.add_argument("--objects", default="all")
    ap.add_argument("--masses", default="20,40,60,80")
    ap.add_argument("--motions", default=",".join(MOTIONS))
    ap.add_argument("--fmax", default="250", help="N, one robot's push (normal force); a comma list runs each")
    ap.add_argument("--pairs", choices=("all", "none"), default="all", help="none: skip the every-pair sweep")
    ap.add_argument("--duration", type=float, default=4.0, help="s of pushing")
    ap.add_argument("--measure-from", type=float, default=1.5, help="s into the push when measuring starts")
    ap.add_argument("--target-speed", type=float, default=0.15,
                    help="m/s: the pushes grow until the object moves this fast (any direction), up to the limit")
    ap.add_argument("--friction", choices=("nominal", "random"), default="nominal",
                    help="object friction: the middle of the training range for every env (paired cases see the "
                         "same object), or randomised as in training")
    ap.add_argument("--settle", type=float, default=0.3, help="s at rest before pushing")
    ap.add_argument("--max-envs", type=int, default=4096, help="envs per simulation batch")
    ap.add_argument("--device", default=None)
    a = ap.parse_args()

    from train_coop2 import resolve_models, set_env

    set_env(resolve_models("b", "anymal"))
    import numpy as np
    import torch

    import quadcoop  # noqa: F401
    from mjlab.envs import ManagerBasedRlEnv

    from quadcoop import contacts as C
    from quadcoop.coop2.env_cfg import FRICTION_RANGE, make_coop2_env_cfg
    from quadcoop.stage1.mdp import wrap
    from quadcoop.stage1b.shapes import NOMINAL_MASS
    from quadcoop.stage2 import mdp as m2
    from quadcoop.stage2.shapes import OBJ_NAMES2, SHAPE_NAMES2, SHAPES2, kinds_tensor, nominal_parts

    device = a.device or ("cuda:0" if torch.cuda.is_available() else "cpu")
    objects = list(SHAPE_NAMES2) if a.objects == "all" else [o.strip() for o in a.objects.split(",")]
    bad = [o for o in objects if o not in SHAPE_NAMES2]
    if bad:
        raise SystemExit(f"unknown objects {bad}; known: {list(SHAPE_NAMES2)}")
    masses = [float(x) for x in a.masses.split(",")]
    motions = [m.strip() for m in a.motions.split(",")]
    if any(m not in MOTIONS for m in motions):
        raise SystemExit(f"--motions from {MOTIONS}")
    fmaxs = [float(x) for x in a.fmax.split(",")]

    # candidate contacts at nominal size, exactly as the env's tables build them
    parts_all, rest_all = nominal_parts("cpu")
    kinds_all = kinds_tensor("cpu")
    cands, usable = {}, {}
    for s, nm in enumerate(SHAPE_NAMES2):
        cl = C.candidates(parts_all[s].numpy(), kinds_all[s].numpy(), float(rest_all[s]))
        cands[nm] = cl
        st = np.stack([c.stand for c in cl])
        d = np.linalg.norm(st[:, None] - st[None], axis=-1)
        usable[nm] = [(i, j) for i in range(len(cl)) for j in range(i + 1, len(cl)) if d[i, j] >= 0.85]

    out_logs = ROOT / "logs" / "evals" / a.name
    out_logs.mkdir(parents=True, exist_ok=True)
    rows: list[dict] = []
    t_start = time.time()
    sym_of = {sh.name: sh.symmetry for sh in SHAPES2}

    for mass in masses:
        cases = []  # (object, motion, plan, i, j, fmax)
        for o in objects:
            cases.append((o, motions[0], "none", -1, -1, fmaxs[0]))  # control: no push (does it sit still?)
            for mo in motions:
                if sym_of[o] == 0 and mo in ("turn", "move_turn"):
                    continue  # the heading of this object does not matter (sphere): no turns
                for fm in fmaxs:
                    cases += [(o, mo, "planner", -1, -1, fm), (o, mo, "equal", -1, -1, fm)]
                    cases += [(o, mo, "single", i, -1, fm) for i in range(len(cands[o]))]
                    if a.pairs == "all":
                        cases += [(o, mo, "pair", i, j, fm) for i, j in usable[o]]
        for c0 in range(0, len(cases), a.max_envs):
            chunk = cases[c0:c0 + a.max_envs]
            rows += run_chunk(chunk, mass, a, device, objects, torch, ManagerBasedRlEnv, make_coop2_env_cfg, wrap,
                              NOMINAL_MASS, m2, OBJ_NAMES2, SHAPE_NAMES2, FRICTION_RANGE)
            print(f"[{mass:g} kg] {min(c0 + a.max_envs, len(cases))}/{len(cases)} cases ({time.time() - t_start:.0f} s)",
                  flush=True)

    keys = list(rows[0].keys())
    with open(out_logs / "cases.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)
    summary, md, key_rows = summarise(rows, a, objects, masses, motions, fmaxs)
    stats = ROOT / "evals" / a.name
    stats.mkdir(parents=True, exist_ok=True)
    (stats / "summary.md").write_text("\n".join(md) + "\n")
    (stats / "summary.json").write_text(json.dumps(summary, indent=1))
    with open(stats / "key.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        w.writerows(key_rows)
    shutil.copy2(stats / "summary.md", out_logs / "summary.md")
    print("\n".join(md))
    print(f"\nall cases: {out_logs / 'cases.csv'}\nstats: {stats}  ({time.time() - t_start:.0f} s)")
    return 0


def run_chunk(chunk, mass, a, device, objects, torch, ManagerBasedRlEnv, make_coop2_env_cfg, wrap, NOMINAL_MASS, m2,
              OBJ_NAMES2, SHAPE_NAMES2, FRICTION_RANGE) -> list[dict]:
    n = len(chunk)
    cfg = make_coop2_env_cfg("b", play=True, partner_map=True, reward_set="r7", contacts=True, guide=True,
                             wrench=True, expert=True, push_cmd=True, reselect_s=(0.0, 0.0), reselect_min_dist=0.0)
    cfg.scene.num_envs = n
    cfg.episode_length_s = 1e5
    cfg.terminations = {}
    alpha = 0.5 * math.log(mass / NOMINAL_MASS)
    for name in OBJ_NAMES2:
        cfg.events[f"{name}_mass"].params["alpha_range"] = (alpha, alpha)
        if a.friction == "nominal" and f"{name}_friction" in cfg.events:
            mid = 0.5 * (FRICTION_RANGE[0] + FRICTION_RANGE[1])
            cfg.events[f"{name}_friction"].params["ranges"] = (mid, mid)
    torch.manual_seed(0)
    env = ManagerBasedRlEnv(cfg=cfg, device=device)
    g = env.command_manager.get_term("goal")
    dev = env.device
    ar = torch.arange(n, device=dev)
    for k in range(len(SHAPE_NAMES2)):
        m2.apply_geometry(env, ar, k, torch.ones(n, 3, device=dev))
    obj_idx = torch.tensor([SHAPE_NAMES2.index(c[0]) for c in chunk], device=dev)
    z = torch.zeros(n, device=dev)
    park = torch.ones(n, dtype=torch.bool, device=dev)
    sc = {"shape": obj_idx, "obj_xy_rel": torch.zeros(n, 2, device=dev), "obj_heading": z.clone(),
          "goal_xy_rel": torch.stack([z + 3.0, z], -1), "goal_yaw": z.clone(),
          "bearings": [z + math.pi, z + math.pi], "gaps": [z + 0.5, z + 0.5], "yaw_noise": [z, z],
          "park": [park, park.clone()], "contact_rule": torch.full((n,), 4, dtype=torch.long, device=dev),
          "contact_idx": torch.full((n, 2), -1, dtype=torch.long, device=dev)}
    g.scenario = lambda ids: {k: ([x[ids] for x in v] if isinstance(v, list) else v[ids]) for k, v in sc.items()}
    env.reset()
    g.scenario = None
    act = torch.zeros(n, env.action_manager.total_action_dim, device=dev)
    for _ in range(max(1, int(round(a.settle / env.step_dt)))):  # at rest, no push
        env.step(act)

    # --- the pushes, in the object (contact) frame -------------------------------------------------
    P, N, _, _, valid, sep = g._contact_geom(ar, g.shape)
    com, cg, rg = g.c_cof.clone(), g.c_cg.clone(), g.c_rg.clone()
    mu, ms = g.c_mu.clone(), g.c_mass.clone()
    fmax = torch.tensor([c[5] for c in chunk], device=dev)
    cap = fmax / (mu * ms * 9.81).clamp(min=1e-6)  # one robot's limit, in units of the force that slides it
    vmax, wmax = g.cfg.push_vmax, g.cfg.push_wmax
    mot = [c[1] for c in chunk]
    v_o = torch.tensor([[vmax, 0.0] if m in ("move_x", "move_turn") else [0.0, vmax] if m == "move_y" else [0.0, 0.0]
                        for m in mot], device=dev)
    wz = torch.tensor([wmax if m in ("turn", "move_turn") else 0.0 for m in mot], device=dev)
    wz = torch.where(g.sym[obj_idx] > 0, wz, torch.zeros_like(wz))
    plan = [c[2] for c in chunk]
    ii = torch.tensor([c[3] for c in chunk], device=dev)
    jj = torch.tensor([c[4] for c in chunk], device=dev)
    is_pl = torch.tensor([p in ("planner", "equal") for p in plan], device=dev)
    if bool(is_pl.any()):  # the planner's pick: the usable pair with the lowest residual for this motion
        e = torch.nonzero(is_pl).squeeze(-1)
        use = valid[e].unsqueeze(2) & valid[e].unsqueeze(1) & sep[e]
        res = g._pair_residuals(P[e], N[e], com[e], v_o[e], wz[e], cg[e], use, cap=cap[e])
        K = res.shape[1]
        flat = torch.where(use, res, torch.full_like(res, 9.0)).view(len(e), -1).argmin(-1)
        ii[e], jj[e] = flat // K, flat % K
    single = torch.tensor([p == "single" for p in plan], device=dev)
    j2 = torch.where(single, ii, jj)  # a single robot: the same contact twice, each half the limit
    pp = torch.stack([P[ar, ii], P[ar, j2]], 1)
    nq = torch.stack([N[ar, ii], N[ar, j2]], 1)
    capx = torch.where(single, 0.5 * cap, cap)
    f, resid = g._split(pp, nq, com, v_o, wz, cg, capx)
    strength = g._pair_strength(pp, nq, com, v_o, wz, cg, capx)
    fn = (f * -nq).sum(-1)  # each push's normal component
    # scale: the hardest-pressing robot at fmax, the other in proportion (single: both halves together)
    fs = torch.where(single.view(-1, 1, 1), (f.sum(1, keepdim=True) / 2).expand(-1, 2, -1), f)
    fns = torch.where(single.view(-1, 1), fn.sum(-1, keepdim=True).expand(-1, 2) / 2, fn)
    top = fns.max(-1).values
    scale = torch.where(top > 1e-9, fmax / top.clamp(min=1e-9), torch.zeros_like(top))
    scale = torch.where(single, 0.5 * scale, scale)  # the two halves add up to one robot at fmax
    F = fs * scale.view(-1, 1, 1)
    none = torch.tensor([p == "none" for p in plan], device=dev)
    F = torch.where(none.view(-1, 1, 1), torch.zeros_like(F), F)
    eq = torch.tensor([p == "equal" for p in plan], device=dev)
    if bool(eq.any()):  # both at fmax along their planned directions (-n where the split gives a robot nothing)
        mag = torch.linalg.norm(f, dim=-1, keepdim=True)
        d = torch.where(mag > 1e-6, f / mag.clamp(min=1e-9), -nq)
        dn = (d * -nq).sum(-1, keepdim=True).clamp(min=0.2)
        F = torch.where(eq.view(-1, 1, 1), d * (fmax.view(-1, 1, 1) / dn), F)
    share = torch.where(single, torch.ones_like(fns[:, 0]), fns[:, 0] / fns.sum(-1).clamp(min=1e-9))
    nn_dot = (nq[:, 0] * nq[:, 1]).sum(-1)

    # --- push and watch --------------------------------------------------------------------------
    def state():
        h = g.heading()
        comw = torch.stack([o.data.root_com_pos_w[:, :2] for o in g.objs], 1)[ar, obj_idx]
        return comw.clone(), h.clone()

    objs_here = [obj_idx == k for k in range(len(g.objs))]
    steps = int(round(a.duration / env.step_dt))
    w0 = min(steps - 2, int(round(a.measure_from / env.step_dt)))
    tilt = torch.zeros(n, device=dev)
    lvl_sum = torch.zeros(n, device=dev)
    # how hard to push: a level 0..1 of the full pushes F (the hardest-pressing robot at fmax), raised while the
    # object moves slower than the target speed and lowered while faster - a robot pushing until the object
    # goes, never past its limit. Reaches the limit in about 1 s if the object does not move.
    lvl = torch.zeros(n, device=dev)
    gain = 1.0  # level per second at full speed error
    rgs = rg * (g.sym[obj_idx] > 0).float()
    s0 = None
    for i in range(steps):
        rate = torch.sqrt(g.box_vel()[:, :2].square().sum(-1) + (rgs * g.box_ang_vel()[:, 2]).square())
        err = ((a.target_speed - rate) / a.target_speed).clamp(-1.0, 1.0)
        lvl = (lvl + env.step_dt * gain * err).clamp(0.0, 1.0)
        yaw = g.contact_frame_yaw()
        cs, sn = torch.cos(yaw), torch.sin(yaw)
        rot = lambda v: torch.stack([cs.unsqueeze(-1) * v[..., 0] - sn.unsqueeze(-1) * v[..., 1],  # noqa: E731
                                     sn.unsqueeze(-1) * v[..., 0] + cs.unsqueeze(-1) * v[..., 1]], -1)
        pw = g.box_pos()[:, :2].unsqueeze(1) + rot(pp)  # (n, 2, 2)
        Fw = rot(F) * lvl.view(-1, 1, 1)
        comw = torch.stack([o.data.root_com_pos_w[:, :2] for o in g.objs], 1)[ar, obj_idx]
        rr = pw - comw.unsqueeze(1)
        Ft = Fw.sum(1)
        tq = (rr[..., 0] * Fw[..., 1] - rr[..., 1] * Fw[..., 0]).sum(1)
        for k, o in enumerate(g.objs):
            here = objs_here[k].float().view(-1, 1)
            f3 = torch.zeros(n, 1, 3, device=dev)
            t3 = torch.zeros(n, 1, 3, device=dev)
            f3[:, 0, :2] = Ft * here
            t3[:, 0, 2] = tq * here.squeeze(-1)
            o.write_external_wrench_to_sim(f3, t3)
        env.step(act)
        if i == w0:
            s0 = state()
        if i >= w0:
            tilt = tilt + torch.linalg.norm(g.box_ang_vel()[:, :2], dim=-1)
            lvl_sum = lvl_sum + lvl
    for o in g.objs:  # leave nothing applied
        o.write_external_wrench_to_sim(torch.zeros(n, 1, 3, device=dev), torch.zeros(n, 1, 3, device=dev))
    s1 = state()
    T = (steps - 1 - w0) * env.step_dt
    dp = s1[0] - s0[0]
    dyaw = wrap(s1[1] - s0[1])
    # the object started at heading 0, so the object frame is the world frame; a heading that does not
    # matter (sphere) is left out of the motion
    real = torch.cat([dp, (rg * dyaw * (g.sym[obj_idx] > 0).float()).unsqueeze(-1)], -1)
    want = torch.cat([v_o, (rg * wz).unsqueeze(-1)], -1)
    want = want / torch.linalg.norm(want, dim=-1, keepdim=True).clamp(min=1e-9)
    rn = torch.linalg.norm(real, dim=-1)
    cosv = (real * want).sum(-1) / rn.clamp(min=1e-9)
    moved = rn >= MOVED
    out = []
    for e, c in enumerate(chunk):
        o, mo, pl, _, _, fm = c
        out.append({
            "object": o, "mass": float(mass), "motion": mo, "plan": pl, "fmax": fm,
            "i": int(ii[e]), "j": int(j2[e]) if pl != "single" else -1,
            "geometry": "single" if pl == "single" else ("same side" if nn_dot[e] > 0.7 else "opposite" if nn_dot[e] < -0.7 else "mixed"),
            "sim_mass": round(float(ms[e]), 2), "mu": round(float(mu[e]), 3), "cap": round(float(cap[e]), 3),
            "pred_residual": round(float(resid[e]), 3), "pred_strength": round(min(float(strength[e]), 99.0), 3),
            "share_1": round(float(share[e]), 3),
            "force_1": round(float(torch.linalg.norm(F[e, 0])) * (2.0 if pl == "single" else 1.0), 1),
            "force_2": 0.0 if pl == "single" else round(float(torch.linalg.norm(F[e, 1])), 1),
            "moved": int(moved[e]), "motion_m": round(float(rn[e]), 4),
            "cos": round(float(cosv[e]), 3) if moved[e] else "",
            "speed": round(float(torch.linalg.norm(dp[e]) / T), 4),
            "yaw_rate_deg": round(math.degrees(float(dyaw[e]) / T), 2),
            "tilt_rate": round(float(tilt[e]) / max(1, steps - w0), 3),
            "push_level": round(float(lvl_sum[e]) / max(1, steps - w0), 3),
            "at_limit": int(float(lvl[e]) >= 0.99),
            "force_needed": round(float(fmax[e]) * float(lvl_sum[e]) / max(1, steps - w0), 1),
        })
    env.close() if hasattr(env, "close") else None
    del env
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    return out


def summarise(rows, a, objects, masses, motions, fmaxs):
    """The five questions, each with a verdict; returns (summary, markdown lines, key rows)."""
    def ok(r):  # moved, and the way asked
        return r["moved"] == 1 and r["cos"] != "" and float(r["cos"]) >= GOOD

    def cosf(r):
        return float(r["cos"]) if r["cos"] != "" else 0.0  # did not move: no credit

    ctrl = [r for r in rows if r["plan"] == "none"]
    rows = [r for r in rows if r["plan"] != "none"]
    groups = defaultdict(list)
    for r in rows:
        groups[(r["object"], r["mass"], r["motion"], r["fmax"])].append(r)
    key_rows, cell = [], {}
    for k, rs in groups.items():
        pl = next((r for r in rs if r["plan"] == "planner"), None)
        eq = next((r for r in rs if r["plan"] == "equal"), None)
        sg = [r for r in rs if r["plan"] == "single"]
        pr = [r for r in rs if r["plan"] == "pair"]
        best = lambda xs: max(xs, key=lambda r: (cosf(r), r["motion_m"])) if xs else None  # noqa: E731
        b_single, b_pair = best(sg), best(pr)
        b_same = best([r for r in pr if r["geometry"] == "same side"])
        b_opp = best([r for r in pr if r["geometry"] == "opposite"])
        cell[k] = {"planner": pl, "equal": eq, "single": b_single, "pair": b_pair, "same": b_same, "opp": b_opp,
                   "singles": sg}
        for tag, r in (("planner", pl), ("equal", eq), ("best single", b_single), ("best pair", b_pair)):
            if r is not None:
                key_rows.append({**r, "plan": tag})
    f2 = lambda x: "" if x is None else f"{x:.2f}"  # noqa: E731
    mean = lambda xs: sum(xs) / len(xs) if xs else None  # noqa: E731
    md = [f"# Planner physics test (test 1): {a.name}", "",
          "No robots, no learning: the planner's pushes applied as forces at the contact points, held "
          f"{a.duration:g} s (measured over the last {a.duration - 0.5:g} s). Motion = (dx, dy, r_g x dyaw); "
          f"moved = {MOVED * 100:g} cm or more; 'as asked' = cosine with the wanted motion >= {GOOD}. "
          f"Robot push (normal force): {', '.join(f'{x:g}' for x in fmaxs)} N. Objects at nominal size.", ""]
    summary = {"fmax": fmaxs, "masses": masses, "motions": motions, "objects": objects}
    if ctrl:
        still = max(r["motion_m"] for r in ctrl)
        worst = max(ctrl, key=lambda r: r["motion_m"])
        summary["control_max_motion_m"] = still
        md += [f"Control (no push, every object and mass): largest motion {still * 100:.1f} cm ({worst['object']}, "
               f"{worst['mass']:g} kg) - {'OK' if still < MOVED / 2 else 'CHECK: objects drift without a push'} "
               f"(must stay under {MOVED * 50:g} cm).", ""]
    for fm in fmaxs:
        sub = {k: v for k, v in cell.items() if k[3] == fm}
        tag = f" ({fm:g} N)" if len(fmaxs) > 1 else ""
        S = summary.setdefault(f"{fm:g}", {})

        # 1. the model: where the planner predicts its pushes work, do they?
        md += [f"## 1. Is the planner's force model right?{tag}",
               "Planner pushes the model rates workable (strength >= 1: strong enough to slide it; residual <= 0.3: "
               "the pushes make the wanted motion). Share that moved as asked, by motion and mass; then the cases "
               "the model gets wrong.", "",
               "| motion | " + " | ".join(f"{m:g} kg" for m in masses) + " | all |", "|---" * (len(masses) + 2) + "|"]
        S1 = {}
        for mo in motions:
            vals, allv = [], []
            for m in masses:
                rs = [v["planner"] for k, v in sub.items() if k[1] == m and k[2] == mo and v["planner"]
                      and v["planner"]["pred_strength"] >= 1 and v["planner"]["pred_residual"] <= 0.3]
                x = [ok(r) for r in rs]
                allv += x
                vals.append(f"{mean([float(t) for t in x]):.2f} (n={len(x)})" if x else "-")
                S1[f"{mo} / {m:g}"] = mean([float(t) for t in x])
            S1[mo] = mean([float(t) for t in allv])
            md.append(f"| {mo} | " + " | ".join(vals) + f" | {f2(S1[mo])} |")
        rate = mean([float(ok(v["planner"])) for v in sub.values() if v["planner"] and v["planner"]["pred_strength"] >= 1
                     and v["planner"]["pred_residual"] <= 0.3])
        S["model_ok"] = rate
        S["model"] = S1
        wrong = [v["planner"] for v in sub.values() if v["planner"] and v["planner"]["pred_strength"] >= 1
                 and v["planner"]["pred_residual"] <= 0.3 and not ok(v["planner"])]
        md += ["", f"**Verdict:** {f2(rate)} of the workable planner pushes moved as asked "
               f"({'PASS' if rate is not None and rate >= 0.9 else 'FAIL'}: 0.90 needed).", ""]
        if wrong:
            byo = defaultdict(int)
            for r in wrong:
                byo[r["object"]] += 1
            md += ["Model wrong (predicted workable, did not move as asked), by object: " +
                   ", ".join(f"{o} {c}" for o, c in sorted(byo.items(), key=lambda x: -x[1])), "",
                   "| object | mass | motion | moved | cos | speed (m/s) | yaw rate (deg/s) | tilt (rad/s) | residual | strength |",
                   "|---|---|---|---|---|---|---|---|---|---|"]
            for r in sorted(wrong, key=lambda r: (r["object"], r["mass"], r["motion"]))[:40]:
                md.append(f"| {r['object']} | {r['mass']:g} | {r['motion']} | {r['moved']} | {r['cos']} | {r['speed']} | "
                          f"{r['yaw_rate_deg']} | {r['tilt_rate']} | {r['pred_residual']} | {r['pred_strength']} |")
            md.append("")
        # also: pushes the model rates hopeless that work anyway
        hopeless = [v["planner"] for v in sub.values() if v["planner"] and v["planner"]["pred_strength"] < 1]
        if hopeless:
            md += [f"Planner pushes the model rates too weak to slide the object (strength < 1): {len(hopeless)}; "
                   f"moved as asked anyway: {sum(ok(r) for r in hopeless)}; moved at all: {sum(r['moved'] for r in hopeless)}.", ""]
        S["too_weak_n"] = len(hopeless)
        S["too_weak_but_ok"] = sum(ok(r) for r in hopeless)
        md += ["How hard the planner's pushes pressed (hardest robot's normal force, N, mean over objects) and the share "
               "of objects where they ended at the limit without reaching the target speed.", "",
               "| motion | " + " | ".join(f"{m:g} kg" for m in masses) + " |", "|---" * (len(masses) + 1) + "|"]
        for mo in motions:
            vals = []
            for m in masses:
                rs = [v["planner"] for k, v in sub.items() if k[1] == m and k[2] == mo and v["planner"]]
                vals.append(f"{mean([r['force_needed'] for r in rs]):.0f} N, {mean([float(r['at_limit']) for r in rs]):.2f} at limit"
                            if rs else "-")
            md.append(f"| {mo} | " + " | ".join(vals) + " |")
        md.append("")

        # 2. weight: can one robot do it, as the model says?
        md += [f"## 2. Does the planner judge weight right (one robot or both)?{tag}",
               "Per object x mass x motion: the model says one robot can (some single contact has strength >= 1 and "
               "residual <= 0.3) or cannot; the sim says one can (some single contact moved it as asked) or cannot. Counts: "
               "agree (one can / one cannot) and disagree (model says one can, it cannot / model says it cannot, it can).", "",
               "| mass | agree: one can | agree: one cannot | model too optimistic | model too cautious | agreement |",
               "|---|---|---|---|---|---|"]
        S2 = {}
        for m in masses:
            c4 = [0, 0, 0, 0]
            for k, v in sub.items():
                if k[1] != m or not v["singles"]:
                    continue
                pred = any(r["pred_strength"] >= 1 and r["pred_residual"] <= 0.3 for r in v["singles"])
                real = any(ok(r) for r in v["singles"])
                c4[(0 if real else 2) if pred else (3 if real else 1)] += 1
            tot = sum(c4)
            S2[f"{m:g}"] = {"agree_can": c4[0], "agree_cannot": c4[1], "optimistic": c4[2], "cautious": c4[3],
                            "agreement": (c4[0] + c4[1]) / tot if tot else None}
            md.append(f"| {m:g} kg | {c4[0]} | {c4[1]} | {c4[2]} | {c4[3]} | {f2(S2[f'{m:g}']['agreement'])} |")
        S["weight"] = S2
        md += ["", "Turning with one robot, by mass (best single contact, motion turn): share of objects it turns as asked, "
               "and the mean yaw rate (deg/s) of the best single, against the best pair.", "",
               "| mass | one robot turns it | best single yaw rate | best pair yaw rate | planner yaw rate |", "|---|---|---|---|---|"]
        for m in masses:
            vs = [v for k, v in sub.items() if k[1] == m and k[2] == "turn"]
            if not vs:
                continue
            one = mean([float(ok(v["single"])) for v in vs if v["single"]])
            ys = mean([v["single"]["yaw_rate_deg"] for v in vs if v["single"]])
            yp = mean([v["pair"]["yaw_rate_deg"] for v in vs if v["pair"]])
            ypl = mean([v["planner"]["yaw_rate_deg"] for v in vs if v["planner"]])
            md.append(f"| {m:g} kg | {f2(one)} | {f2(ys)} | {f2(yp)} | {f2(ypl)} |")
        md.append("")

        # 3. turning: which geometry turns it, per object and mass
        md += [f"## 3. Turning: one robot, two on one side, or two on opposite sides?{tag}",
               "Motion turn. Each cell: cosine with a pure turn of the best push of that kind (- = none of that kind exists; "
               "0 = did not move), yaw rate (deg/s) in brackets.", "",
               "| object | mass | best single | best same side | best opposite | best mixed / any pair | planner | equal split |",
               "|---|---|---|---|---|---|---|---|"]
        S3 = []
        for o in objects:
            for m in masses:
                v = sub.get((o, m, "turn", fm))
                if v is None:
                    continue
                cc = lambda r: "-" if r is None else f"{cosf(r):.2f} ({r['yaw_rate_deg']:.0f})"  # noqa: E731
                md.append(f"| {o} | {m:g} | {cc(v['single'])} | {cc(v['same'])} | {cc(v['opp'])} | {cc(v['pair'])} | "
                          f"{cc(v['planner'])} | {cc(v['equal'])} |")
                S3.append({"object": o, "mass": m, **{k2: (None if v[k2] is None else cosf(v[k2]))
                                                       for k2 in ("single", "same", "opp", "pair", "planner", "equal")}})
        S["turning"] = S3
        md.append("")

        # 4. does the split matter (planner shares vs both pushing equally hard)?
        md += [f"## 4. Does following the force split matter?{tag}",
               "Same pair and directions: the planner's shares against both robots pushing equally hard (robots that "
               "ignore their share). Share moved as asked, and mean cosine (no motion = 0).", "",
               "| motion | planner as asked | equal as asked | planner mean cos | equal mean cos | equal fails where planner works |",
               "|---|---|---|---|---|---|"]
        S4 = {}
        for mo in motions:
            vs = [v for k, v in sub.items() if k[2] == mo and v["planner"] and v["equal"]]
            if not vs:
                continue
            a_p = mean([float(ok(v["planner"])) for v in vs])
            a_e = mean([float(ok(v["equal"])) for v in vs])
            c_p = mean([cosf(v["planner"]) for v in vs])
            c_e = mean([cosf(v["equal"]) for v in vs])
            lost = sum(1 for v in vs if ok(v["planner"]) and not ok(v["equal"]))
            S4[mo] = {"planner_ok": a_p, "equal_ok": a_e, "planner_cos": c_p, "equal_cos": c_e, "lost": lost, "n": len(vs)}
            md.append(f"| {mo} | {f2(a_p)} | {f2(a_e)} | {f2(c_p)} | {f2(c_e)} | {lost} of {len(vs)} |")
        S["split"] = S4
        md.append("")

        # 5. does the planner pick the best pair?
        if any(v["pair"] for v in sub.values()):
            md += [f"## 5. Does the planner pick the best pair?{tag}",
                   "The planner's pair against the best of every usable pair (each with its own split), by motion: mean "
                   "cosine, and the share of cases where the planner is within 0.1 of the best.", "",
                   "| motion | planner mean cos | best pair mean cos | planner within 0.1 | best pair moved as asked |",
                   "|---|---|---|---|---|"]
            S5 = {}
            for mo in motions:
                vs = [v for k, v in sub.items() if k[2] == mo and v["planner"] and v["pair"]]
                if not vs:
                    continue
                c_p = mean([cosf(v["planner"]) for v in vs])
                c_b = mean([cosf(v["pair"]) for v in vs])
                near = mean([float(cosf(v["planner"]) >= cosf(v["pair"]) - 0.1) for v in vs])
                b_ok = mean([float(ok(v["pair"])) for v in vs])
                S5[mo] = {"planner_cos": c_p, "best_cos": c_b, "near": near, "best_ok": b_ok}
                md.append(f"| {mo} | {f2(c_p)} | {f2(c_b)} | {f2(near)} | {f2(b_ok)} |")
            S["pick"] = S5
            md.append("")

        # per object: the planner's push for each motion (cos), all masses
        md += [f"## Planner push by object{tag}", "Cosine with the wanted motion (0 = did not move), masses "
               + " / ".join(f"{m:g}" for m in masses) + " kg.", "",
               "| object | " + " | ".join(motions) + " |", "|---" * (len(motions) + 1) + "|"]
        for o in objects:
            cells = []
            for mo in motions:
                xs = [sub.get((o, m, mo, fm)) for m in masses]
                cells.append(" / ".join("-" if x is None or x["planner"] is None else f"{cosf(x['planner']):.2f}" for x in xs))
            md.append(f"| {o} | " + " | ".join(cells) + " |")
        md.append("")
    return summary, md, key_rows


if __name__ == "__main__":
    sys.exit(main())
