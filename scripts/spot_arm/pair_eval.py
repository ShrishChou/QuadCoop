"""Spot-arm pair, turn-pilot evaluation on held-out starts (docs/spot_arm_pair.md).

    python scripts/spot_arm/pair_eval.py --checkpoint logs/marl2/<run>/model_<n>.pt --name sa-pilot-<run>
    python scripts/spot_arm/pair_eval.py --report sa-pilot-<run1>,sa-pilot-<run2>,...     # systems side by side

Tasks (the same for every checkpoint: --seed): one elongated object ("long", --mass 20 kg), goal 1 m ahead with the
heading turned left (+--turn deg, default 30), straight (0) or right (---turn deg); the robots start behind it at -35 / +35 deg
(+-10 deg jitter, 0.3-0.6 m clear, object heading jittered +-10 deg), each task also with the two start places
exchanged; --reps placements per turn. Success: within 0.10 m and 6 deg for 1 s inside --horizon; a fall ends
the episode as a failure.
Arm modes, all in one build for a learned-arm checkpoint (joint targets or hand position) (the policy is the same, only what its arm outputs may
do differs): both (as trained), only_1 / only_2 (the other robot's arm held stowed), none (both held stowed).
A stowed-arm checkpoint has the mode "stowed". Every checkpoint also runs solo_1 / solo_2 (teamwork test: only robot k
acts, the other is parked 40 m away and stands still; its falls are ignored).
Per episode: success, time, final position and signed heading error, falls, each robot's arm and trunk contact
share and mean arm contact force, the goal heading change as placed (realized), the hand's mean extension. Videos: rep 0, unswapped, of each turn, in every arm mode (captions: wanted and
actual object heading). Writes evals/<name>/episodes.csv and summary.md; videos to logs/evals/<name>/.

Arm mechanism and integration (docs/spot_arm_pair.md, "Arm mechanism, torso, release"):
  --modes M1,M2,..       only these arm modes. Extra modes: hold_out (both arms held at RAI's "out" pose),
                         hold_mean (each arm held at the mean arm target its policy used while touching the object in
                         mode "both" of an earlier run of this script: --hold-pose-from <name>; every run of mode
                         "both" writes evals/<name>/arm_pose.json).
  --arm-object-collide off  arm and object geoms do not collide (contype / conaffinity only: the arm keeps its mass,
                         inertia and actuators, and still collides with the ground and the robots).
  --torso P,H            every Spot-arm's torso command held at pitch P rad, height H m (rate-limited from default).
  --torso-interface      build the env with the 2 torso outputs and inputs; an older checkpoint is expanded (new
                         inputs and outputs zero: unchanged actions at the default posture).
  --release policy|zero|retract --release-s 5   after a success the episode continues for release-s: continued
                         policy; zero base velocity with the arm held where it is; or arm retracted (stowed, rate-
                         limited) with 0.2 m/s back-off for 2 s, then zero. Records object displacement and heading
                         change during the release, retention (within tolerance at its end; and at every step of
                         it), falls. Success must come inside --horizon; the simulation runs release-s longer so
                         every success gets its full window (release_complete marks it).
The walker is QUADCOOP_SPOT_ARM_WALKER (default RAI's), recorded in the summary.
"""
from __future__ import annotations

import argparse
import csv
import math
import os
import random
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
TURNS = [("left", 30.0), ("straight", 0.0), ("right", -30.0)]  # --turn sets the magnitude
POS_TOL, YAW_TOL_DEG, HOLD_S = 0.10, 6.0, 1.0


def ci(d, n=4000, seed=0):
    rng = random.Random(seed)
    m = sum(d) / len(d)
    bs = sorted(sum(rng.choice(d) for _ in d) / len(d) for _ in range(n))
    return m, bs[int(0.025 * n)], bs[int(0.975 * n) - 1]


def load(name: str) -> list[dict]:
    return list(csv.DictReader(open(ROOT / "evals" / name / "episodes.csv")))


def tables(rows: list[dict], label: str = "") -> list[str]:
    """Markdown for one evaluation: per arm mode, by turn; paired arm ablation; swap; who touches with the arm."""
    f = lambda r, k: float(r[k])  # noqa: E731
    modes = list(dict.fromkeys(r["arm_mode"] for r in rows))
    agents = [k[len("fell_"):] for k in rows[0] if k.startswith("fell_")]
    md = [f"## {label}".rstrip(), "", "| arm mode | turn | episodes | success | falls | time to success, median s | "
          "final position error, median m | final heading error, median abs deg | signed heading error, mean deg |",
          "|---|---|---|---|---|---|---|---|---|"]
    for m in modes:
        for t in [x[0] for x in TURNS] + ["all"]:
            sel = [r for r in rows if r["arm_mode"] == m and (t == "all" or r["turn"] == t)]
            ts = sorted(f(r, "t_success") for r in sel if r["t_success"])
            med = lambda v: sorted(v)[len(v) // 2]  # noqa: E731
            md.append(f"| {m} | {t} | {len(sel)} | {sum(int(r['success']) for r in sel) / len(sel):.1%} | "
                      f"{sum(int(r['fell']) for r in sel) / len(sel):.1%} | {(f'{med(ts):.1f}' if ts else '-')} | "
                      f"{med([f(r, 'pos_err') for r in sel]):.3f} | {med([abs(f(r, 'yaw_err_deg')) for r in sel]):.1f} | "
                      f"{sum(f(r, 'yaw_err_deg') for r in sel) / len(sel):+.1f} |")
    key = lambda r: (r["turn"], r["rep"], r["swap"])  # noqa: E731
    b0 = "both" if "both" in modes else modes[0]
    if len(modes) > 1:
        base = {key(r): r for r in rows if r["arm_mode"] == b0}
        md += ["", f"Ablation, paired per task against {b0} (the same policy; a locked arm stays stowed; solo_k: only "
               "robot k, the other parked 40 m away):", "",
               "| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |",
               "|---|---|---|---|---|"]
        for m in modes:
            if m == b0:
                continue
            oth = {key(r): r for r in rows if r["arm_mode"] == m}
            ks = sorted(set(base) & set(oth))
            ds = [int(oth[k]["success"]) - int(base[k]["success"]) for k in ks]
            dh = [abs(f(oth[k], "yaw_err_deg")) - abs(f(base[k], "yaw_err_deg")) for k in ks]
            a, lo, hi = ci(ds)
            b, lo2, hi2 = ci(dh)
            md.append(f"| {m} | {100 * a:+.1f} [{100 * lo:+.1f}, {100 * hi:+.1f}] pts | {sum(d < 0 for d in ds)} | "
                      f"{sum(d > 0 for d in ds)} | {b:+.1f} [{lo2:+.1f}, {hi2:+.1f}] |")
    md += ["", "Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along "
           "the push direction; arm contact = share of the episode with that robot's arm on the object.", "",
           "| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | "
           "arm contact, robot starting right | trunk contact left | trunk contact right |", "|---|---|---|---|---|---|---|---|"]
    for m in modes:
        for t in [x[0] for x in TURNS]:
            sel = [r for r in rows if r["arm_mode"] == m and r["turn"] == t]
            su = [int(r["success"]) for r in sel if r["swap"] == "0"]
            ss = [int(r["success"]) for r in sel if r["swap"] == "1"]
            side = defaultdict(list)
            for r in sel:  # unswapped: agent 0 starts at 180 - 35 deg = left of the push direction
                left, right = (agents[0], agents[1]) if r["swap"] == "0" else (agents[1], agents[0])
                for nm, ag in (("L", left), ("R", right)):
                    side["arm" + nm].append(f(r, f"arm_touch_{ag}"))
                    side["trunk" + nm].append(f(r, f"trunk_touch_{ag}"))
            mean = lambda v: sum(v) / max(len(v), 1)  # noqa: E731
            md.append(f"| {m} | {t} | {mean(su):.1%} | {mean(ss):.1%} | {mean(side['armL']):.1%} | {mean(side['armR']):.1%} | "
                      f"{mean(side['trunkL']):.1%} | {mean(side['trunkR']):.1%} |")
    return md


def release_table(rows: list[dict]) -> list[str]:
    if not rows or rows[0].get("release", "none") == "none":
        return []
    md = ["", f"Release ({rows[0]['release']}), episodes that succeeded (success only inside the task horizon; the "
          "simulation continues for the release window): complete = the follow-up window finished (or a fall ended it); "
          "rates over complete episodes. Inside at end = within tolerance at the end of the window; inside throughout "
          "= within tolerance at every step of it; displacement = object travel during it.", "",
          "| arm mode | successes | complete | inside at end | inside throughout | object displacement, median m | "
          "heading change, median abs deg | falls in release |",
          "|---|---|---|---|---|---|---|---|"]
    for m in dict.fromkeys(r["arm_mode"] for r in rows):
        sel = [r for r in rows if r["arm_mode"] == m and str(r["success"]) == "1"]
        cpl = [r for r in sel if str(r.get("release_complete", "1")) == "1"]
        if not cpl:
            md.append(f"| {m} | {len(sel)} | 0 | - | - | - | - | - |")
            continue
        med = lambda v: sorted(v)[len(v) // 2] if v else float("nan")  # noqa: E731
        fin = lambda k: [float(r[k]) for r in cpl if r[k] != "" and not math.isnan(float(r[k]))]  # noqa: E731
        md.append(f"| {m} | {len(sel)} | {len(cpl)} | {sum(int(r['retained']) for r in cpl) / len(cpl):.1%} | "
                  f"{sum(int(r['retained_all']) for r in cpl) / len(cpl):.1%} | "
                  f"{med(fin('release_disp_m')):.3f} | {med([abs(x) for x in fin('release_yaw_deg')]):.1f} | "
                  f"{sum(int(r['fell_release']) for r in cpl) / len(cpl):.1%} |")
    return md


def arm_object_collisions_off(cfg, arm_robots: list[str], objects: list[str]) -> None:
    """No contact between Spot-arm arm geoms (subtree of arm_link_sh0) and the objects; everything else as before.
    Objects: contype 2, conaffinity 3; arm geoms: contype 4, conaffinity 1; all others keep 1 / 1. Then
    arm-object: (4 & 3) | (2 & 1) = 0; arm-ground / arm-robot: (1 & 1) = 1; object-ground / object-robot: (1 & 3) = 1;
    object-object: (2 & 3) = 2. Only collision bits change (mass, inertia, actuation as before)."""
    import mujoco

    def wrap_obj(fn):
        def f():
            spec = fn()
            for gm in spec.geoms:
                if gm.contype or gm.conaffinity:
                    gm.contype, gm.conaffinity = 2, 3
            return spec
        return f

    def wrap_arm(fn):
        def f():
            spec = fn()
            root = spec.body("arm_link_sh0")
            assert root is not None, "arm_link_sh0 not in the Spot-arm spec"
            stack, n_ = [root], 0
            while stack:
                b = stack.pop()
                for gm in b.geoms:
                    if gm.contype or gm.conaffinity:
                        gm.contype, gm.conaffinity = 4, 1
                        n_ += 1
                stack.extend(b.bodies)
            print(f"[arm-object collisions off] {n_} arm geoms re-masked", flush=True)
            return spec
        return f

    for name, ecfg in cfg.scene.entities.items():
        if name in objects:
            ecfg.spec_fn = wrap_obj(ecfg.spec_fn)
        elif name in arm_robots:
            ecfg.spec_fn = wrap_arm(ecfg.spec_fn)
    del mujoco


def report(names: list[str], out_path: str = "evals/spot_arm/pilot_report.md") -> int:
    md = ["# Spot-arm turn pilot: systems on the same held-out tasks", ""]
    runs = {n: load(n) for n in names}
    md += ["| system | arm mode | success | falls | abs heading error left / straight / right, median deg |", "|---|---|---|---|---|"]
    for n, rows in runs.items():
        for m in dict.fromkeys(r["arm_mode"] for r in rows):
            sel = [r for r in rows if r["arm_mode"] == m]
            med = lambda t: sorted(abs(float(r["yaw_err_deg"])) for r in sel if r["turn"] == t)  # noqa: E731
            md.append(f"| {n} | {m} | {sum(int(r['success']) for r in sel) / len(sel):.1%} | "
                      f"{sum(int(r['fell']) for r in sel) / len(sel):.1%} | "
                      + " / ".join(f"{med(t)[len(med(t)) // 2]:.1f}" for t, _ in TURNS) + " |")
    key = lambda r: (r["turn"], r["rep"], r["swap"])  # noqa: E731
    main_mode = lambda rows: "both" if any(r["arm_mode"] == "both" for r in rows) else rows[0]["arm_mode"]  # noqa: E731
    if len(names) > 1:
        md += ["", "Paired per task, each system as trained (learned arms: both active), against the first:", "",
               "| system | change in success [95% CI] | tasks gained | tasks lost |", "|---|---|---|---|"]
        b = {key(r): int(r["success"]) for r in runs[names[0]] if r["arm_mode"] == main_mode(runs[names[0]])}
        for n in names[1:]:
            o = {key(r): int(r["success"]) for r in runs[n] if r["arm_mode"] == main_mode(runs[n])}
            ks = sorted(set(b) & set(o))
            d = [o[k] - b[k] for k in ks]
            a, lo, hi = ci(d)
            md.append(f"| {n} vs {names[0]} | {100 * a:+.1f} [{100 * lo:+.1f}, {100 * hi:+.1f}] pts | {sum(x > 0 for x in d)} | "
                      f"{sum(x < 0 for x in d)} |")
    for n, rows in runs.items():
        md += [""] + tables(rows, n)
    out = ROOT / out_path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(md) + "\n")
    print("\n".join(md))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--checkpoint")
    ap.add_argument("--name")
    ap.add_argument("--report", default="", help="comma list of evaluation names: write --report-out")
    ap.add_argument("--report-out", default="evals/spot_arm/pilot_report.md")
    ap.add_argument("--object", default="long")
    ap.add_argument("--mass", type=float, default=20.0)
    ap.add_argument("--dist", type=float, default=1.0)
    ap.add_argument("--reps", type=int, default=20)
    ap.add_argument("--horizon", type=float, default=20.0)
    ap.add_argument("--seed", type=int, default=7100)
    ap.add_argument("--videos", type=int, default=1)
    ap.add_argument("--turn", type=float, default=30.0, help="left / right goal heading change, deg")
    ap.add_argument("--modes", default="", help="comma list of arm modes to run (default: all for the checkpoint)")
    ap.add_argument("--hold-pose-from", default="", help="evaluation name whose arm_pose.json gives hold_mean's pose")
    ap.add_argument("--arm-object-collide", choices=("on", "off"), default="on")
    ap.add_argument("--torso", default="", help="P,H: torso pitch (rad) and height (m) held for every Spot-arm")
    ap.add_argument("--torso-interface", action="store_true")
    ap.add_argument("--release", choices=("none", "policy", "zero", "retract"), default="none")
    ap.add_argument("--release-s", type=float, default=5.0)
    a = ap.parse_args()
    TURNS[0], TURNS[2] = ("left", abs(a.turn)), ("right", -abs(a.turn))
    if a.report:
        return report([x.strip() for x in a.report.split(",") if x.strip()], a.report_out)
    if not (a.checkpoint and a.name):
        ap.error("give --checkpoint and --name (or --report)")
    import torch as _torch

    # the team comes from the checkpoint (spot_arm: two Spot-arms; anymal_arm: ANYmal + Spot-arm; armless pairs too);
    # set the env variables exactly as training does (walker checkpoints of non-Spot-arm slots)
    sys.path.insert(0, str(ROOT))
    sys.path.insert(0, str(ROOT / "scripts"))
    from train_coop2 import resolve_models, set_env

    _ck = _torch.load(a.checkpoint, map_location="cpu", weights_only=False)
    set_env(resolve_models(_ck.get("variant", "b"), (_ck.get("cfg") or {}).get("pair", "spot_arm")))
    import numpy as np
    import torch
    from tensordict import TensorDict

    import quadcoop  # noqa: F401
    from mjlab.envs import ManagerBasedRlEnv

    from quadcoop import falls
    from quadcoop.coop2.env_cfg import SPECS, make_coop2_env_cfg
    from quadcoop.coop2.marl import PairPolicy, action_slices
    from quadcoop.robots import spot_arm as sa_mod
    from quadcoop.coop2.mdp import AGENTS
    from quadcoop.coop2.video import Camera, key_points, render_episode
    from quadcoop.stage1.mdp import wrap
    from quadcoop.stage1b.shapes import NOMINAL_MASS
    from quadcoop.stage2 import mdp as m2
    from quadcoop.stage2.shapes import OBJ_NAMES2, SHAPE_NAMES2, SHAPES2

    ck = torch.load(a.checkpoint, map_location="cpu", weights_only=False)
    rc = ck.get("cfg", {})
    from quadcoop.coop2.env_cfg import ARM
    from quadcoop.coop2.pairs import ARM_PAIRS

    assert rc.get("pair") in ARM_PAIRS or rc.get("pair") in ("anymal", "spot", "mixed"), f"{a.checkpoint}: pair {rc.get('pair')}"
    arm = (rc.get("arm") or "stowed") if rc.get("pair") in ARM_PAIRS else "stowed"  # no arm: as trained + solo
    n_arms = sum(ARM[ag] for ag in AGENTS)  # one Spot-arm (with ANYmal): "both" = its arm free, "none" = locked
    free = (["both", "only_1", "only_2", "none"] if n_arms == 2 else ["both", "none"])
    modes = (free if arm in ("learned", "hand") else ["stowed"]) + ["solo_1", "solo_2"]
    lock = {"both": (0, 0), "only_1": (0, 1), "only_2": (1, 0), "none": (1, 1), "stowed": (0, 0),
            "solo_1": (0, 0), "solo_2": (0, 0), "hold_out": (0, 0), "hold_mean": (0, 0)}
    if a.modes:
        modes = [x.strip() for x in a.modes.split(",") if x.strip()]
        assert all(x in lock for x in modes), f"--modes: known {list(lock)}"
    hold_mean = None
    if "hold_mean" in modes:
        import json as _json
        assert a.hold_pose_from, "hold_mean needs --hold-pose-from <evaluation name>"
        hold_mean = _json.loads((ROOT / "evals" / a.hold_pose_from / "arm_pose.json").read_text())
    base_cases = [(t, r) for t in range(len(TURNS)) for r in range(a.reps)]
    cases = [(t, r, w, m) for m in modes for w in (0, 1) for (t, r) in base_cases]
    n = len(cases)
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    cfg = make_coop2_env_cfg(ck.get("variant", "b"), play=True, partner_map=bool(rc.get("partner_map")),
                             reward_set=rc.get("reward_set", "r7"), arm=arm,
                             pilot_level=tuple(rc.get("pilot_level") or ()), dyaw_choices=bool(rc.get("dyaw_choices")),
                             hand_obs=bool(rc.get("hand_obs")), torso=a.torso_interface)
    if a.arm_object_collide == "off":
        arm_object_collisions_off(cfg, [ag for ag in AGENTS if ARM[ag]], list(OBJ_NAMES2))
    if rc.get("pilot_level"):
        cfg.commands["goal"].start_level = 0
    cfg.scene.num_envs = n
    from mjlab.sensor import ContactMatch, ContactSensorCfg

    have = {sc_.name for sc_ in cfg.scene.sensors}
    cfg.scene.sensors += tuple(ContactSensorCfg(  # whole-robot contact with the object (body_touch), every team
        name=f"push_{ag}", primary=ContactMatch(mode="body", pattern=tuple(f"{o}/body" for o in OBJ_NAMES2)),
        secondary=ContactMatch(mode="subtree", pattern=SPECS[ag].base_body, entity=ag),
        fields=("found", "force"), reduce="netforce", num_slots=1) for ag in AGENTS if f"push_{ag}" not in have)
    cfg.episode_length_s = 1e5
    cfg.terminations = {}
    alpha = 0.5 * math.log(a.mass / NOMINAL_MASS)
    for name in OBJ_NAMES2:
        cfg.events[f"{name}_mass"].params["alpha_range"] = (alpha, alpha)
    torch.manual_seed(a.seed)
    env = ManagerBasedRlEnv(cfg=cfg, device=device)
    g = env.command_manager.get_term("goal")
    dev, dt = env.device, env.step_dt
    ids = torch.arange(n, device=dev)
    for k in range(len(SHAPES2)):
        m2.apply_geometry(env, ids, k, torch.ones(n, 3, device=dev))

    rng = random.Random(f"{a.seed}-spot-arm-pilot")
    draw = {c: {"jit": [rng.uniform(-10, 10) for _ in AGENTS], "gap": [rng.uniform(0.3, 0.6) for _ in AGENTS],
                "head": rng.uniform(-10, 10)} for c in base_cases}
    T = lambda fn: torch.tensor([fn(c) for c in cases], device=dev, dtype=torch.float32)  # noqa: E731
    sw = lambda c, k: (1 - k) if c[2] else k  # noqa: E731
    head = torch.deg2rad(T(lambda c: draw[c[:2]]["head"]))
    turn = torch.deg2rad(T(lambda c: TURNS[c[0]][1]))
    bearings = [math.pi + torch.deg2rad(T(lambda c, k=k: (-35.0, 35.0)[sw(c, k)] + draw[c[:2]]["jit"][sw(c, k)])) for k in range(2)]
    gaps = [T(lambda c, k=k: draw[c[:2]]["gap"][sw(c, k)]) for k in range(2)]
    z = torch.zeros(n, device=dev)
    park = [torch.tensor([c[3] == "solo_2" for c in cases], device=dev), torch.tensor([c[3] == "solo_1" for c in cases], device=dev)]
    sc = {"shape": torch.full((n,), SHAPE_NAMES2.index(a.object), device=dev), "obj_xy_rel": torch.zeros(n, 2, device=dev),
          "obj_heading": head, "goal_xy_rel": torch.tensor([a.dist, 0.0], device=dev).repeat(n, 1),
          "goal_yaw": wrap(head + turn), "bearings": bearings, "gaps": gaps, "yaw_noise": [z, z],
          "park": park}
    g.scenario = lambda env_ids: {k: ([x[env_ids] for x in v] if isinstance(v, list) else v[env_ids]) for k, v in sc.items()}
    obs, _ = env.reset()
    g.scenario = None
    td = lambda o: TensorDict({k: v for k, v in o.items() if not k.startswith("walker_")}, batch_size=[n])  # noqa: E731
    obs = td(obs)
    sl = action_slices(env)
    policy = PairPolicy(obs, device, ck.get("variant", "b"), checkpoint=a.checkpoint,
                        act_dims={ag: s_.stop - s_.start for ag, s_ in sl.items()})
    terms = {ag: env.action_manager.get_term(f"walker_{ag}") for ag in AGENTS}
    for k, ag in enumerate(AGENTS):
        if not ARM[ag]:  # ANYmal: no arm to lock
            continue
        terms[ag].arm_locked[:] = torch.tensor([bool(lock[c[3]][k]) for c in cases], device=dev)
        out_m = torch.tensor([c[3] == "hold_out" for c in cases], device=dev)
        mean_m = torch.tensor([c[3] == "hold_mean" for c in cases], device=dev)
        terms[ag].arm_pose_on[:] = out_m | mean_m
        terms[ag].arm_pose[out_m] = torch.tensor(sa_mod.ARM_OUT[:6], device=dev)
        if hold_mean is not None:
            terms[ag].arm_pose[mean_m] = torch.tensor(hold_mean[ag]["pose"], device=dev)
        if a.torso:
            p_, h_ = (float(x) for x in a.torso.split(","))
            terms[ag].torso_override_on[:] = True
            terms[ag].torso_override[:] = torch.tensor([0.0, p_, h_], device=dev)
    walker_name = os.environ.get("QUADCOOP_SPOT_ARM_WALKER", "") or "RAI (spot_locomotion.onnx)"
    print(f"walker: {walker_name}; torso {a.torso or 'default'}; torso interface {a.torso_interface} "
          f"(expanded: {policy.expanded}); arm-object collisions {a.arm_object_collide}; release {a.release}", flush=True)
    arm_ags = [ag for ag in AGENTS if ARM[ag]]
    pose_sum = {ag: torch.zeros(6, device=dev) for ag in arm_ags}
    pose_n = {ag: torch.zeros((), device=dev) for ag in arm_ags}
    pose_all = {ag: torch.zeros(6, device=dev) for ag in arm_ags}
    pose_all_n = {ag: torch.zeros((), device=dev) for ag in arm_ags}
    is_both = torch.tensor([c[3] == "both" for c in cases], device=dev)
    rel_t = torch.zeros(n, device=dev)
    rel_xy0 = torch.zeros(n, 2, device=dev)
    rel_e0 = torch.zeros(n, device=dev)
    rel_disp = torch.full((n,), float("nan"), device=dev)
    rel_yaw = torch.full((n,), float("nan"), device=dev)
    retained = torch.zeros(n, dtype=torch.bool, device=dev)  # inside tolerance at the end of the release window
    left_tol = torch.zeros(n, dtype=torch.bool, device=dev)  # left tolerance at any step of the release window
    rel_done = torch.zeros(n, dtype=torch.bool, device=dev)  # follow-up finished (full window, or a fall)
    fell_rel = torch.zeros(n, dtype=torch.bool, device=dev)

    def base_norm(ag, v):  # base velocity (m/s, rad/s) -> the normalized action that commands it
        t_ = terms[ag]
        return (2.0 * (v - t_._lo) / (t_._hi - t_._lo) - 1.0).clamp(-1.0, 1.0)

    print(f"{a.checkpoint} (iteration {ck['iter']}, {ck['algo']}, arm {arm}; actions { {ag: s.stop - s.start for ag, s in sl.items()} }); "
          f"{len(base_cases)} tasks x swap x modes {modes} = {n} episodes, {a.object} {a.mass:g} kg", flush=True)

    film = [j for j, c in enumerate(cases) if c[1] == 0 and c[2] == 0] if a.videos else []
    rec = {j: {"q": [], "mp": [], "mq": [], "pts": [], "cap": []} for j in film}
    nmocap = env.sim.mj_model.nmocap
    done = torch.zeros(n, dtype=torch.bool, device=dev)
    succ = torch.zeros(n, dtype=torch.bool, device=dev)
    fell = {ag: torch.zeros(n, dtype=torch.bool, device=dev) for ag in AGENTS}
    hold = torch.zeros(n, device=dev)
    t_succ = torch.full((n,), float("nan"), device=dev)
    pos_err, yaw_err = torch.zeros(n, device=dev), torch.zeros(n, device=dev)
    live_steps = torch.zeros(n, device=dev)
    acc = {f"{p}_{ag}": torch.zeros(n, device=dev) for ag in AGENTS for p in ("arm", "trunk", "force", "ext", "body", "walk")}
    last_xy = {ag: env.scene[ag].data.root_link_pos_w[:, :2].clone() for ag in AGENTS}
    realized = torch.rad2deg(g.goal_turn.clone())  # the goal heading change as placed (the object's symmetry caps it)
    with torch.no_grad():
        # with a release, success must come inside --horizon, and the simulation runs release-s longer so a late
        # success still gets its full follow-up window
        n_steps = int(a.horizon / dt) + (int(math.ceil(a.release_s / dt)) if a.release != "none" else 0)
        for i in range(n_steps):
            act = policy(obs, env=env)
            releasing = succ & ~done
            if a.release in ("zero", "retract") and bool(releasing.any()):
                for ag in AGENTS:
                    back = a.release == "retract" and True
                    v = torch.zeros(n, 3, device=dev)
                    if back:
                        v[:, 0] = torch.where(rel_t < 2.0, torch.full_like(rel_t, -0.2), torch.zeros_like(rel_t))
                    s0 = sl[ag].start
                    act[releasing, s0:s0 + 3] = base_norm(ag, v)[releasing]
            act[done] = 0.0  # finished episodes: stand still, arms stowed
            for k, ag in enumerate(AGENTS):  # solo: the parked robot (40 m away) stands still
                act[park[k], sl[ag]] = 0.0
            o, *_ = env.step(act)
            obs = td(o)
            t = (i + 1) * dt
            live = ~done
            d, e = g.errors()
            pos_err = torch.where(live, d, pos_err)
            yaw_err = torch.where(live, e, yaw_err)
            live_steps += live.float()
            for k, ag in enumerate(AGENTS):
                f_ = falls.fallen(env, asset_name=ag, nominal_height=SPECS[ag].nominal_height) & live & ~park[k]
                fell[ag] |= f_
                acc[f"body_{ag}"] += (env.scene[f"push_{ag}"].data.found.view(n, -1).any(-1) & live).float()
                xy = env.scene[ag].data.root_link_pos_w[:, :2]
                acc[f"walk_{ag}"] += torch.linalg.norm(xy - last_xy[ag], dim=-1) * live.float()  # path length walked
                last_xy[ag] = xy.clone()
                if not ARM[ag]:
                    continue
                sd = env.scene[f"arm_{ag}"].data
                on = sd.found.view(n, -1).any(-1) & live
                acc[f"arm_{ag}"] += on.float()
                acc[f"force_{ag}"] += torch.linalg.norm(sd.force.view(n, -1, 3).sum(1), dim=-1) * on.float()
                acc[f"trunk_{ag}"] += (env.scene[f"trunk_{ag}"].data.found.view(n, -1).any(-1) & live).float()
                acc[f"ext_{ag}"] += terms[ag].blend * live.float()
            for ag in arm_ags:  # the arm targets the policy uses (mode both): all live steps, and while touching
                tgt = terms[ag].arm_target
                lb = live & is_both & ~succ
                on = lb & (env.scene[f"arm_{ag}"].data.found.view(n, -1).any(-1)
                           | env.scene[f"trunk_{ag}"].data.found.view(n, -1).any(-1))
                pose_all[ag] += (tgt * lb.unsqueeze(-1).float()).sum(0)
                pose_all_n[ag] += lb.float().sum()
                pose_sum[ag] += (tgt * on.unsqueeze(-1).float()).sum(0)
                pose_n[ag] += on.float().sum()
            inside = (d < POS_TOL) & (e.abs() < math.radians(YAW_TOL_DEG))
            hold = torch.where(inside & live, hold + dt, torch.zeros_like(hold))
            new = live & ~succ & (hold >= HOLD_S) & (t <= a.horizon + 1e-6)
            succ |= new
            t_succ = torch.where(new, torch.full_like(t_succ, t), t_succ)
            anyfell = fell[AGENTS[0]] | fell[AGENTS[1]]
            if a.release == "none":
                done |= new | anyfell
            else:
                if bool(new.any()):
                    rel_xy0[new] = g.box_pos()[new, :2]
                    rel_e0[new] = e[new]
                    for ag in arm_ags:
                        t_ = terms[ag]
                        if a.release == "zero":  # the arm stays where it is
                            t_.arm_pose[new] = t_.arm_target[new]
                            t_.arm_pose_on[new] = True
                        elif a.release == "retract":
                            t_.arm_pose[new] = t_.stow
                            t_.arm_pose_on[new] = True
                rel_t = torch.where(succ & live & ~new, rel_t + dt, rel_t)
                fell_rel |= succ & live & anyfell
                left_tol |= succ & live & ~new & ~inside
                fin = succ & live & ((rel_t >= a.release_s - 1e-6) | anyfell)
                rel_done |= fin
                rel_disp = torch.where(fin, torch.linalg.norm(g.box_pos()[:, :2] - rel_xy0, dim=-1), rel_disp)
                rel_yaw = torch.where(fin, torch.rad2deg(wrap(e - rel_e0)), rel_yaw)
                retained |= fin & inside & ~anyfell
                done |= fin | (anyfell & ~succ) | (live & ~succ & (t >= a.horizon - 1e-6))
            if film and i % 2 == 0:
                sd = env.sim.data
                for j in film:
                    if done[j] and len(rec[j]["q"]) > 0 and rec[j].get("tail", 0) > 25:
                        continue
                    rec[j]["tail"] = rec[j].get("tail", 0) + int(bool(done[j]))
                    rec[j]["q"].append(sd.qpos[j].cpu().numpy().copy())
                    if nmocap:
                        rec[j]["mp"].append(sd.mocap_pos[j].cpu().numpy().copy())
                        rec[j]["mq"].append(sd.mocap_quat[j].cpu().numpy().copy())
                    rec[j]["pts"].append(key_points(env, j))
                    c = cases[j]
                    rec[j]["cap"].append(
                        f"{ck['algo'].upper()} arms {arm}, mode {c[3]} | turn {TURNS[c[0]][0]} ({TURNS[c[0]][1]:+.0f} deg) | t {t:4.1f} s\n"
                        f"object heading: wanted {math.degrees(float(g.goal_yaw[j])):+.0f} deg, error {math.degrees(float(e[j])):+.1f} deg | "
                        f"distance to goal {float(d[j]):.2f} m"
                        + (" | SUCCESS" if bool(succ[j]) else " | FELL" if bool(fell[AGENTS[0]][j] | fell[AGENTS[1]][j]) else ""))
            if bool(done.all()):
                break
    rows = []
    for j, c in enumerate(cases):
        ls = max(float(live_steps[j]), 1.0)
        rows.append({"turn": TURNS[c[0]][0], "turn_deg": TURNS[c[0]][1], "turn_realized_deg": round(float(realized[j]), 2),
                     "rep": c[1], "swap": c[2], "arm_mode": c[3],
                     "success": int(bool(succ[j])), "fell": int(bool(fell[AGENTS[0]][j] | fell[AGENTS[1]][j])),
                     **{f"fell_{ag}": int(bool(fell[ag][j])) for ag in AGENTS},
                     "t_success": "" if not bool(succ[j]) else round(float(t_succ[j]), 2),
                     "pos_err": round(float(pos_err[j]), 4), "yaw_err_deg": round(math.degrees(float(yaw_err[j])), 2),
                     **{f"arm_touch_{ag}": round(float(acc[f'arm_{ag}'][j]) / ls, 4) for ag in AGENTS},
                     **{f"trunk_touch_{ag}": round(float(acc[f'trunk_{ag}'][j]) / ls, 4) for ag in AGENTS},
                     **{f"body_touch_{ag}": round(float(acc[f'body_{ag}'][j]) / ls, 4) for ag in AGENTS},
                     **{f"walked_m_{ag}": round(float(acc[f'walk_{ag}'][j]), 2) for ag in AGENTS},
                     **{f"extension_{ag}": round(float(acc[f'ext_{ag}'][j]) / ls, 4) for ag in AGENTS},
                     **{f"arm_force_{ag}": round(float(acc[f'force_{ag}'][j]) / max(float(acc[f'arm_{ag}'][j]), 1.0), 1)
                        for ag in AGENTS},
                     "release": a.release,
                     "release_disp_m": "" if not bool(succ[j]) or a.release == "none" else round(float(rel_disp[j]), 4),
                     "release_yaw_deg": "" if not bool(succ[j]) or a.release == "none" else round(float(rel_yaw[j]), 2),
                     "release_complete": "" if not bool(succ[j]) or a.release == "none" else int(bool(rel_done[j])),
                     "retained": "" if not bool(succ[j]) or a.release == "none" or not bool(rel_done[j])
                     else int(bool(retained[j])),
                     "retained_all": "" if not bool(succ[j]) or a.release == "none" or not bool(rel_done[j])
                     else int(bool(rel_done[j] & ~left_tol[j] & ~fell_rel[j])),
                     "fell_release": int(bool(fell_rel[j]))})
    out = ROOT / "evals" / a.name
    out.mkdir(parents=True, exist_ok=True)
    with open(out / "episodes.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    if arm_ags and float(sum(pose_all_n.values())) > 0:
        import json as _json
        pose = {ag: {"pose": (pose_sum[ag] / pose_n[ag]).tolist() if float(pose_n[ag]) > 100 else
                     (pose_all[ag] / pose_all_n[ag].clamp(min=1)).tolist(),
                     "from": "object contact" if float(pose_n[ag]) > 100 else "all live steps",
                     "contact_steps": int(pose_n[ag]), "mean_all": (pose_all[ag] / pose_all_n[ag].clamp(min=1)).tolist()}
                for ag in arm_ags}
        (out / "arm_pose.json").write_text(_json.dumps(pose, indent=1))
    srows = [{k: str(v) for k, v in r.items()} for r in rows]
    md = [f"# Spot-arm turn pilot: {a.name}", "",
          f"{a.checkpoint}, iteration {ck['iter']}, {ck['algo']}, arms {arm}. {a.object} {a.mass:g} kg, {a.dist:g} m, "
          f"{a.reps} placements per turn x swap, horizon {a.horizon:g} s, seed {a.seed}. Goal heading change as placed: "
          + ", ".join(f"{t} {min(float(r['turn_realized_deg']) for r in rows if r['turn'] == t):+.1f} to "
                      f"{max(float(r['turn_realized_deg']) for r in rows if r['turn'] == t):+.1f} deg" for t, _ in TURNS) + ".",
          "", f"Walker: {walker_name}. Torso: {a.torso or 'default'} (interface {a.torso_interface}, expanded "
          f"{policy.expanded}). Arm-object collisions: {a.arm_object_collide}. Release: {a.release}"
          + (f" for {a.release_s:g} s" if a.release != "none" else "") + ".", ""] + tables(srows) + release_table(srows)
    (out / "summary.md").write_text("\n".join(md) + "\n")
    print("\n".join(md), flush=True)
    if film:
        try:
            cam = Camera(env, 960, 720)
            vdir = ROOT / "logs" / "evals" / a.name
            for j in film:
                c = cases[j]
                render_episode(cam, j, np.stack(rec[j]["q"]), np.stack(rec[j]["mp"]) if nmocap else None,
                               np.stack(rec[j]["mq"]) if nmocap else None, np.stack(rec[j]["pts"]),
                               vdir / f"{TURNS[c[0]][0]}_{c[3]}.mp4", fps=1.0 / (2 * dt), caption=lambda f, j=j: rec[j]["cap"][f])
            print(f"videos: {vdir}")
        except Exception as e:  # noqa: BLE001
            print(f"videos failed: {e!r}")
    env.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
