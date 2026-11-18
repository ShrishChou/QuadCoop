"""Demonstrations from the contact planner for the S4 pair policy (docs/planner_distill.md).

    python scripts/distill/collect_planner_demos.py --out logs/demos/planner_s4_r0.pt \
        --student logs/marl2/asS4_shared_s0/model_6100.pt [--objects arch,cylinder,dumbbell,plus] [--masses 20,40,60,80]

Teacher: the contact planner's expert rule (contacts chosen and re-chosen inside the env, as trained: reselect,
minimum distance, slow-arrival limit 1 s) driving the Stage 4 contact-conditioned executor (--teacher, default
logs/keep/marl2/turn_debug/model_15000.pt; MAPPO, contacts + guide + push command, partner map). Robots start
behind the object and walk to their contacts, as in the planner's evaluations. Object geometry nominal (the
planner's contact tables are built from it).

Student inputs are a prefix of the teacher's: actor_<a> = the teacher's first 51 numbers (Stage 2's 42 + the
partner's 9; the contact / guide / push inputs come after them), top_<a> (2 channels: object, partner footprint)
and front are the same groups. Every --every steps each live env records the student's inputs (fp16) and the
teacher's action (clamped to [-1, 1], as the walker receives it), whoever drives.

DAgger-style mixing: in a --student-frac share of the envs (fixed per env) the student checkpoint drives and the
teacher only labels, so the data covers states the student itself reaches. Tasks: random goal distance (2-5 m),
direction (-150..150 deg) and heading change (+-90 deg, capped by the object's symmetry), seeded robot placements
behind; --seed must differ from the evaluation seeds (7100, 7500). An env stops recording at success (10 cm / 6 deg
held 1 s), a fall, the object tipping or getting lost, or --horizon.

Writes {"obs": {group: fp16 (N, ...)}, "act": (N, 6), "driver": (N,) 0 teacher / 1 student, "object", "mass",
"episodes", "success": {driver: {object: rate}}, ...}: the format train_coop2.py --bc-data reads.
"""
from __future__ import annotations

import argparse
import math
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

STUDENT_ACTOR = 51  # Stage 2's 42 + partner 9


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", required=True)
    ap.add_argument("--teacher", default="logs/keep/marl2/turn_debug/model_15000.pt")
    ap.add_argument("--student", default="", help="the student checkpoint that drives in --student-frac of the envs")
    ap.add_argument("--student-frac", type=float, default=0.5)
    ap.add_argument("--objects", default="arch,cylinder,dumbbell,plus")
    ap.add_argument("--masses", default="20,40,60,80")
    ap.add_argument("--reps", type=int, default=64, help="tasks per object and mass")
    ap.add_argument("--horizon", type=float, default=60.0)
    ap.add_argument("--every", type=int, default=5, help="record every N policy steps")
    ap.add_argument("--seed", type=int, default=9100)
    a = ap.parse_args()
    if a.seed in (7100, 7500):
        raise SystemExit("--seed: 7100 and 7500 are evaluation seeds")

    from train_coop2 import resolve_models, set_env

    set_env(resolve_models("b", "anymal"))
    import torch
    from tensordict import TensorDict

    import quadcoop  # noqa: F401
    from mjlab.envs import ManagerBasedRlEnv

    from quadcoop import falls
    from quadcoop.coop2 import mdp as cm
    from quadcoop.coop2.env_cfg import SPECS, make_coop2_env_cfg
    from quadcoop.coop2.marl import PairPolicy, actor_groups
    from quadcoop.coop2.mdp import AGENTS
    from quadcoop.stage1.mdp import wrap
    from quadcoop.stage1b import mdp as hb
    from quadcoop.stage1b.shapes import NOMINAL_MASS
    from quadcoop.stage2 import mdp as m2
    from quadcoop.stage2.shapes import OBJ_NAMES2, SHAPE_NAMES2, SHAPES2

    dev = "cuda:0" if torch.cuda.is_available() else "cpu"
    ck_cfg = torch.load(a.teacher, map_location="cpu", weights_only=False).get("cfg", {})
    if not ck_cfg.get("contacts"):
        raise SystemExit(f"{a.teacher} was not trained with --contacts")
    if not ck_cfg.get("partner_map"):
        raise SystemExit("the teacher must have the partner map (its top_<a> groups are the student's)")
    objects = [o.strip() for o in a.objects.split(",")]
    masses = [float(x) for x in a.masses.split(",")]
    reselect_s = tuple(float(x) for x in ck_cfg.get("reselect_s", (0.0, 0.0)))
    min_dist = float(ck_cfg.get("reselect_min_dist", 0.15))
    sgroups = {ag: actor_groups(ag, "b") for ag in AGENTS}
    keys = list(dict.fromkeys(k for ag in AGENTS for k in sgroups[ag]))
    buf = {k: [] for k in keys}
    acts, drivers, objs, mss = [], [], [], []
    succ_tab: dict = {}
    episodes = 0
    rng = random.Random(f"{a.seed}-planner-demos")

    for mass in masses:
        cfg = make_coop2_env_cfg(
            "b", play=True, partner_map=True, reward_set=ck_cfg.get("reward_set", "r7"), contacts=True,
            tol_levels=tuple(tuple(x) for x in ck_cfg.get("tol_levels", ())),
            drift_dist=float(ck_cfg.get("drift_dist", 0.35)), drift_heading_deg=float(ck_cfg.get("drift_heading_deg", 45.0)),
            reselect_s=reselect_s, guide=bool(ck_cfg.get("guide", False)),
            off_contact=ck_cfg.get("off_contact", "soft") if ck_cfg.get("guide") else "soft",
            disturb_frac=0.0, push_sensors=True, push_cmd=bool(ck_cfg.get("push_cmd", False)),
            wrench=True, walk_cost=float(ck_cfg.get("walk_cost", 0.3)), reselect_min_dist=min_dist, expert=True,
            exec_v2=bool(ck_cfg.get("exec_v2", False)), effort=bool(ck_cfg.get("effort", False)),
            contact_sense=bool(ck_cfg.get("contact_sense", False)), track=bool(ck_cfg.get("track", False)))
        tasks = [(o, r) for o in objects for r in range(a.reps)]
        n = len(tasks)
        cfg.scene.num_envs = n
        cfg.episode_length_s = 1e5
        cfg.terminations = {}
        alpha = 0.5 * math.log(mass / NOMINAL_MASS)
        for name in OBJ_NAMES2:
            cfg.events[f"{name}_mass"].params["alpha_range"] = (alpha, alpha)
        torch.manual_seed(a.seed + int(mass))
        env = ManagerBasedRlEnv(cfg=cfg, device=dev)
        g = env.command_manager.get_term("goal")
        ids = torch.arange(n, device=dev)
        for k in range(len(SHAPES2)):
            m2.apply_geometry(env, ids, k, torch.ones(n, 3, device=dev))
        obj_idx = torch.tensor([SHAPE_NAMES2.index(o) for o, _ in tasks], device=dev)
        T = lambda xs: torch.tensor(xs, device=dev, dtype=torch.float)  # noqa: E731
        dist = T([rng.uniform(2.0, 5.0) for _ in tasks])
        gdir = torch.deg2rad(T([rng.uniform(-150.0, 150.0) for _ in tasks]))
        turn = torch.deg2rad(T([rng.uniform(-90.0, 90.0) for _ in tasks]))
        sym = g.sym[obj_idx]
        cap = torch.where(sym > 0, (math.pi / sym.clamp(min=1)) * g.cfg.max_yaw_frac_of_symmetry, torch.zeros_like(sym))
        turn = torch.sign(turn) * torch.minimum(turn.abs(), cap)
        jit = T([[rng.uniform(-10, 10) for _ in AGENTS] for _ in tasks])
        gap = T([[rng.uniform(0.3, 0.6) for _ in AGENTS] for _ in tasks])
        z = torch.zeros(n, device=dev)
        sc = {"shape": obj_idx, "obj_xy_rel": torch.zeros(n, 2, device=dev), "obj_heading": z.clone(),
              "goal_xy_rel": dist.unsqueeze(-1) * torch.stack([torch.cos(gdir), torch.sin(gdir)], -1),
              "goal_yaw": wrap(turn), "bearings": [math.pi + torch.deg2rad(s_ * 35.0 + jit[:, i])
                                                   for i, s_ in enumerate((-1.0, 1.0))],
              "gaps": [gap[:, 0], gap[:, 1]], "yaw_noise": [z, z],
              "park": [torch.zeros(n, dtype=torch.bool, device=dev)] * 2,
              "contact_rule": torch.full((n,), 4, dtype=torch.long, device=dev),  # expert
              "contact_idx": torch.full((n, 2), -1, dtype=torch.long, device=dev),
              "start_behind": torch.ones(n, dtype=torch.bool, device=dev)}
        g.scenario = lambda env_ids: {k: ([x[env_ids] for x in v] if isinstance(v, list) else v[env_ids])
                                      for k, v in sc.items()}
        o_, _ = env.reset()
        g.scenario = None
        g.cfg.expert_first_only = False
        g.cfg.slow_min_s = 1.0
        full = lambda o: TensorDict({k: v for k, v in o.items() if not k.startswith("walker_")}, batch_size=[n])  # noqa: E731

        def student_obs(o):
            d = {k: o[k] for k in keys}
            for ag in AGENTS:
                d[f"actor_{ag}"] = o[f"actor_{ag}"][:, :STUDENT_ACTOR]
            return TensorDict(d, batch_size=[n])

        obs = full(o_)
        teacher = PairPolicy(obs, dev, "b", checkpoint=a.teacher)
        student = PairPolicy(student_obs(obs), dev, "b", checkpoint=a.student) if a.student else None
        drive_s = torch.zeros(n, dtype=torch.bool, device=dev)
        if student is not None:
            k_s = int(round(a.student_frac * a.reps))
            drive_s = torch.tensor([r < k_s for _, r in tasks], device=dev)  # the first k_s reps of each object
        done = torch.zeros(n, dtype=torch.bool, device=dev)
        succ = torch.zeros(n, dtype=torch.bool, device=dev)
        hold = torch.zeros(n, device=dev)
        dt = env.step_dt
        n0 = len(acts)
        with torch.no_grad():
            for i in range(int(a.horizon / dt)):
                t_act = teacher(obs, env=env)
                so = student_obs(obs)
                act = t_act
                if student is not None:
                    act = torch.where(drive_s.unsqueeze(-1), student(so, env=env), t_act)
                live = ~done
                if i % a.every == 0 and bool(live.any()):
                    for k in keys:
                        buf[k].append(so[k][live].half().cpu())
                    acts.append(t_act[live].clamp(-1.0, 1.0).cpu())
                    drivers.append(drive_s[live].to(torch.uint8).cpu())
                    objs.append(obj_idx[live].to(torch.uint8).cpu())
                    mss.append(torch.full((int(live.sum()),), mass))
                act = torch.where(done.unsqueeze(-1), torch.zeros_like(act), act)
                o_, *_ = env.step(act)
                obs = full(o_)
                fell = torch.zeros(n, dtype=torch.bool, device=dev)
                for ag in AGENTS:
                    fell |= falls.fallen(env, asset_name=ag, nominal_height=SPECS[ag].nominal_height)
                bad = (fell | hb.box_tipped(env) | cm.box_lost(env)) & live
                d, e = g.errors()
                inside = live & ~bad & (d < 0.10) & (e.abs() < math.radians(6.0))
                hold = torch.where(inside, hold + dt, torch.zeros_like(hold))
                new = inside & (hold >= 1.0)
                succ |= new
                done |= new | bad
                if bool(done.all()):
                    break
        episodes += n
        for drv, nm in ((False, "teacher"), (True, "student")):
            for o in objects:
                sel = (drive_s == drv) & (obj_idx == SHAPE_NAMES2.index(o))
                if bool(sel.any()):
                    succ_tab.setdefault(nm, {}).setdefault(o, {})[f"{mass:g}"] = round(float(succ[sel].float().mean()), 3)
        print(f"[demos] {mass:g} kg: {n} episodes, {sum(x.shape[0] for x in acts[n0:])} samples; success "
              f"teacher-driven {float(succ[~drive_s].float().mean()):.2f}"
              + (f", student-driven {float(succ[drive_s].float().mean()):.2f}" if student is not None else ""), flush=True)
        env.close()
        del env

    out = {"obs": {k: torch.cat(v) for k, v in buf.items()}, "act": torch.cat(acts), "driver": torch.cat(drivers),
           "object": torch.cat(objs), "mass": torch.cat(mss), "episodes": episodes, "success": succ_tab,
           "objects": objects, "masses": masses, "teacher": a.teacher, "student": a.student, "seed": a.seed,
           "every": a.every, "horizon": a.horizon, "student_actor_inputs": STUDENT_ACTOR}
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    torch.save(out, a.out)
    print(f"[demos] wrote {a.out}: {out['act'].shape[0]} samples; success by driver / object / mass: {succ_tab}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
