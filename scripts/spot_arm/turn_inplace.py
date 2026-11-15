"""Spot-arm pair, turn in place: the scripted maneuver on mirrored starts (docs/spot_arm_pair.md, "Turn in place").

    python scripts/spot_arm/turn_inplace.py [--turn 40] [--reps 8] [--out evals/spot_arm/turn_inplace]
    python scripts/spot_arm/turn_inplace.py --checkpoint logs/marl2/<run>/model_<n>.pt --out evals/<name>

Task: the 20 kg elongated object ("long") starts at its goal centre; the goal heading is turned --turn deg clockwise
or counter-clockwise. One Spot starts behind the 1 m face, the other in front (bearing +-15 deg, 0.3-0.6 m clear,
object heading +-10 deg), each placement also with the two robots exchanged. Success: centre within 0.10 m and
heading within 6 deg, held 1 s, inside --horizon s; the maneuver keeps running after it (to show it settles).
Conditions (the same script, quadcoop/coop2/spot_arm_script.py, env built with --arm hand_rate --hand-obs):
  both_hands; hand_1 / hand_2 (the other robot's arm held stowed, it pushes with its trunk); stowed (both trunks);
  solo_1 / solo_2 (the other robot parked far away; the remaining one uses its hand).
With --checkpoint the trained pair acts instead of the script (deterministic, the same tasks): an --arm hand_rate
checkpoint runs every condition (hand_1 / hand_2 / stowed: the named robots' arms are held stowed whatever the policy
outputs); an --arm stowed checkpoint runs stowed, solo_1, solo_2. The policy keeps acting after success.
Per episode: success, time, final centre error and signed heading error (at success and at the horizon), largest
centre drift, falls, each robot's hand and trunk contact share. Videos: both_hands and stowed, both turn directions,
placement 0 (captions: wanted / actual heading, centre drift, each robot's requested / executed / measured hand).
Writes episodes.csv, summary.md, videos to --out.
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
CONDS = ("both_hands", "hand_1", "hand_2", "stowed", "solo_1", "solo_2")
TURN_LEVEL = lambda deg: (0.0, 0.0, 15, 0, 10, deg, 0.10, 6, 1.0, 22, 18)  # noqa: E731
POS_TOL, YAW_TOL_DEG, HOLD_S = 0.10, 6.0, 1.0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--turn", type=float, default=40.0)
    ap.add_argument("--reps", type=int, default=8)
    ap.add_argument("--horizon", type=float, default=20.0)
    ap.add_argument("--mass", type=float, default=20.0)
    ap.add_argument("--seed", type=int, default=7200)
    ap.add_argument("--out", default="evals/spot_arm/turn_inplace")
    ap.add_argument("--conds", default="")
    ap.add_argument("--checkpoint", default="")
    ap.add_argument("--videos", type=int, default=1)
    a = ap.parse_args()
    os.environ["QUADCOOP_SHAPES"] = "v2"
    os.environ["QUADCOOP_PAIR"] = "spot_arm"
    import numpy as np
    import torch
    from tensordict import TensorDict

    import quadcoop  # noqa: F401
    from mjlab.envs import ManagerBasedRlEnv

    from quadcoop import falls
    from quadcoop.coop2 import spot_arm_term as sat
    from quadcoop.coop2.env_cfg import SPECS, make_coop2_env_cfg
    from quadcoop.coop2.marl import PairPolicy
    from quadcoop.coop2.mdp import AGENTS
    from quadcoop.coop2.spot_arm_script import TurnScript
    from quadcoop.coop2.video import Camera, key_points, render_episode
    from quadcoop.stage1.mdp import wrap
    from quadcoop.stage1b.shapes import NOMINAL_MASS
    from quadcoop.stage2 import mdp as m2
    from quadcoop.stage2.shapes import OBJ_NAMES2, SHAPE_NAMES2, SHAPES2

    arm, hand_obs, label = "hand_rate", True, "scripted"
    if a.checkpoint:
        ck = torch.load(a.checkpoint, map_location="cpu", weights_only=False)
        rc = ck.get("cfg", {})
        arm, hand_obs = rc.get("arm") or "stowed", bool(rc.get("hand_obs"))
        assert arm in ("hand_rate", "stowed"), arm
        label = f"{ck['algo'].upper()} it {ck['iter']} ({arm})"
    default = CONDS if arm == "hand_rate" else ("stowed", "solo_1", "solo_2")
    conds = [c.strip() for c in a.conds.split(",")] if a.conds else list(default)
    turns = (("ccw", abs(a.turn)), ("cw", -abs(a.turn)))
    cases = [(cn, ti, r, w) for cn in conds for ti in range(2) for r in range(a.reps) for w in (0, 1)]
    n = len(cases)
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    cfg = make_coop2_env_cfg("b", play=True, partner_map=True, reward_set="r7", arm=arm, hand_obs=hand_obs,
                             pilot_level=TURN_LEVEL(abs(a.turn)), turn_signs=True)
    cfg.commands["goal"].start_level = 0
    cfg.scene.num_envs = n
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
    rng = random.Random(f"{a.seed}-turn-inplace")
    draw = {(ti, r): {"jit": [rng.uniform(-15, 15) for _ in AGENTS], "gap": [rng.uniform(0.3, 0.6) for _ in AGENTS],
                      "head": rng.uniform(-10, 10)} for ti in range(2) for r in range(a.reps)}
    T = lambda fn: torch.tensor([fn(c) for c in cases], device=dev, dtype=torch.float32)  # noqa: E731
    sw = lambda c, k: (1 - k) if c[3] else k  # noqa: E731
    head = torch.deg2rad(T(lambda c: draw[c[1], c[2]]["head"]))
    turn = torch.deg2rad(T(lambda c: turns[c[1]][1]))
    # unswapped: robot 0 behind (bearing 180 deg), robot 1 in front (0 deg); swapped: exchanged
    bearings = [torch.deg2rad(T(lambda c, k=k: (180.0, 0.0)[sw(c, k)] + draw[c[1], c[2]]["jit"][sw(c, k)])) + head
                for k in range(2)]
    gaps = [T(lambda c, k=k: draw[c[1], c[2]]["gap"][sw(c, k)]) for k in range(2)]
    z = torch.zeros(n, device=dev)
    cond = [c[0] for c in cases]
    park = [torch.tensor([cn == "solo_2" for cn in cond], device=dev), torch.tensor([cn == "solo_1" for cn in cond], device=dev)]
    sc = {"shape": torch.full((n,), SHAPE_NAMES2.index("long"), device=dev), "obj_xy_rel": torch.zeros(n, 2, device=dev),
          "obj_heading": head, "goal_xy_rel": torch.zeros(n, 2, device=dev), "goal_yaw": wrap(head + turn),
          "bearings": bearings, "gaps": gaps, "yaw_noise": [z, z], "park": park}
    g.scenario = lambda env_ids: {k: ([x[env_ids] for x in v] if isinstance(v, list) else v[env_ids]) for k, v in sc.items()}
    obs, _ = env.reset()
    g.scenario = None
    hand = {AGENTS[0]: torch.tensor([cn in ("both_hands", "hand_1", "solo_1") for cn in cond], device=dev),
            AGENTS[1]: torch.tensor([cn in ("both_hands", "hand_2", "solo_2") for cn in cond], device=dev)}
    terms = {ag: env.action_manager.get_term(f"walker_{ag}") for ag in AGENTS}
    for ag in AGENTS:
        terms[ag].arm_locked[:] = ~hand[ag]
    td = lambda o: TensorDict({k: v for k, v in o.items() if not k.startswith("walker_")}, batch_size=[n])  # noqa: E731
    if a.checkpoint:
        policy = PairPolicy(td(obs), device, ck.get("variant", "b"), checkpoint=a.checkpoint)
        act_fn = lambda: policy(td(obs), env=env)  # noqa: E731
    else:
        script = TurnScript(env, use_hand=hand)
        act_fn = script.act
    print(f"turn in place +-{abs(a.turn):g} deg, {a.mass:g} kg long object; {n} episodes "
          f"({len(conds)} conditions x 2 directions x {a.reps} placements x swap)", flush=True)

    c0 = g.box_pos()[:, :2].clone()
    succ = torch.zeros(n, dtype=torch.bool, device=dev)
    t_succ = torch.full((n,), float("nan"), device=dev)
    hold = torch.zeros(n, device=dev)
    fell = torch.zeros(n, dtype=torch.bool, device=dev)
    drift_max = torch.zeros(n, device=dev)
    err_at_succ = torch.zeros(n, 2, device=dev)
    acc = {f"{p}_{ag}": torch.zeros(n, device=dev) for ag in AGENTS for p in ("hand", "trunk")}
    film = [j for j, c in enumerate(cases) if c[0] in ("both_hands", "stowed") and c[2] == 0 and c[3] == 0] if a.videos else []
    rec = {j: {"q": [], "mp": [], "mq": [], "pts": [], "cap": []} for j in film}
    nmocap = env.sim.mj_model.nmocap
    steps = int(a.horizon / dt)
    with torch.no_grad():
        for i in range(steps):
            obs, *_ = env.step(act_fn())
            t = (i + 1) * dt
            d, e = g.errors()
            drift = torch.linalg.norm(g.box_pos()[:, :2] - c0, dim=-1)
            drift_max = torch.maximum(drift_max, drift)
            for k, ag in enumerate(AGENTS):
                fell |= falls.fallen(env, asset_name=ag, nominal_height=SPECS[ag].nominal_height) & ~park[k]
                acc[f"hand_{ag}"] += sat.touch(env, f"arm_{ag}").float()
                acc[f"trunk_{ag}"] += sat.touch(env, f"trunk_{ag}").float()
            inside = (d < POS_TOL) & (e.abs() < math.radians(YAW_TOL_DEG)) & ~fell
            hold = torch.where(inside, hold + dt, torch.zeros_like(hold))
            new = ~succ & (hold >= HOLD_S)
            err_at_succ = torch.where(new.unsqueeze(-1), torch.stack([d, torch.rad2deg(e)], -1), err_at_succ)
            t_succ = torch.where(new, torch.full_like(t_succ, t), t_succ)
            succ |= new
            if i % 2 == 0:
                sd = env.sim.data
                for j in film:
                    c = cases[j]
                    rec[j]["q"].append(sd.qpos[j].cpu().numpy().copy())
                    if nmocap:
                        rec[j]["mp"].append(sd.mocap_pos[j].cpu().numpy().copy())
                        rec[j]["mq"].append(sd.mocap_quat[j].cpu().numpy().copy())
                    rec[j]["pts"].append(key_points(env, j))
                    lines = [f"{label} turn in place, {c[0]} | {turns[c[1]][0]} {turns[c[1]][1]:+.0f} deg | t {t:4.1f} s"
                             + (" | SUCCESS" if bool(succ[j]) else "") + (" | FELL" if bool(fell[j]) else ""),
                             f"heading wanted {math.degrees(float(g.goal_yaw[j])):+.0f} deg, error {math.degrees(float(e[j])):+.1f} deg"
                             f" | centre drift {float(drift[j]):.2f} m (max {float(drift_max[j]):.2f})"]
                    for ag in AGENTS:
                        tm = terms[ag]
                        hb = sat.hand_pos_b(env, ag)[j].cpu().numpy()
                        lag = float((tm.arm_goal[j] - tm.arm_target[j]).abs().max())
                        lines.append(f"{ag}: hand requested {np.round(tm.hand_cmd[j].cpu().numpy(), 2)} ext {float(tm.blend[j]):.2f}"
                                     f" | executed lag {lag:.2f} rad | measured {np.round(hb, 2)} | "
                                     f"hand {'ON' if bool(sat.touch(env, f'arm_{ag}')[j]) else '--'} "
                                     f"trunk {'ON' if bool(sat.touch(env, f'trunk_{ag}')[j]) else '--'}")
                    rec[j]["cap"].append("\n".join(lines))
    d, e = g.errors()
    rows = []
    for j, c in enumerate(cases):
        rows.append({"cond": c[0], "turn": turns[c[1]][0], "turn_deg": turns[c[1]][1],
                     "turn_realized_deg": round(math.degrees(float(g.goal_turn[j])), 2), "rep": c[2], "swap": c[3],
                     "success": int(bool(succ[j])), "t_success": "" if not bool(succ[j]) else round(float(t_succ[j]), 2),
                     "fell": int(bool(fell[j])), "drift_max_m": round(float(drift_max[j]), 3),
                     "pos_err_end_m": round(float(d[j]), 3), "yaw_err_end_deg": round(math.degrees(float(e[j])), 2),
                     **{f"hand_touch_{ag}": round(float(acc[f'hand_{ag}'][j]) / steps, 3) for ag in AGENTS},
                     **{f"trunk_touch_{ag}": round(float(acc[f'trunk_{ag}'][j]) / steps, 3) for ag in AGENTS}})
    out = ROOT / a.out
    out.mkdir(parents=True, exist_ok=True)
    with open(out / "episodes.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    med = lambda v: sorted(v)[len(v) // 2] if v else float("nan")  # noqa: E731
    md = [f"# Turn in place, {label}{(' ' + a.checkpoint) if a.checkpoint else ''}: +-{abs(a.turn):g} deg, "
          f"{a.mass:g} kg long object", "",
          f"{a.reps} placements per direction x swap, horizon {a.horizon:g} s, seed {a.seed}. Success: centre < "
          f"{POS_TOL} m and heading < {YAW_TOL_DEG:g} deg held {HOLD_S:g} s.", "",
          "| condition | turn | episodes | success | falls | time to success, median s | largest centre drift, median m | "
          "end centre error, median m | end heading error, median abs deg | hand contact (robot 1 / 2) | trunk contact (1 / 2) |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    by = defaultdict(list)
    for r in rows:
        by[(r["cond"], r["turn"])].append(r)
        by[(r["cond"], "both")].append(r)
    for cn in conds:
        for tn in ("ccw", "cw", "both"):
            sel = by[(cn, tn)]
            ts = [float(r["t_success"]) for r in sel if r["t_success"] != ""]
            mean = lambda k: sum(float(r[k]) for r in sel) / len(sel)  # noqa: E731
            md.append(f"| {cn} | {tn} | {len(sel)} | {mean('success'):.0%} | {mean('fell'):.0%} | "
                      f"{med(ts):.1f} | {med([r['drift_max_m'] for r in sel]):.2f} | {med([r['pos_err_end_m'] for r in sel]):.3f} | "
                      f"{med([abs(r['yaw_err_end_deg']) for r in sel]):.1f} | "
                      f"{mean(f'hand_touch_{AGENTS[0]}'):.0%} / {mean(f'hand_touch_{AGENTS[1]}'):.0%} | "
                      f"{mean(f'trunk_touch_{AGENTS[0]}'):.0%} / {mean(f'trunk_touch_{AGENTS[1]}'):.0%} |")
    (out / "summary.md").write_text("\n".join(md) + "\n")
    print("\n".join(md), flush=True)
    try:
        cam = Camera(env, 960, 720)
        for j in film:
            c = cases[j]
            render_episode(cam, j, np.stack(rec[j]["q"]), np.stack(rec[j]["mp"]) if nmocap else None,
                           np.stack(rec[j]["mq"]) if nmocap else None, np.stack(rec[j]["pts"]),
                           out / f"{c[0]}_{turns[c[1]][0]}.mp4", fps=1.0 / (2 * dt), caption=lambda f, j=j: rec[j]["cap"][f])
        print(f"videos: {out}")
    except Exception as ex:  # noqa: BLE001
        print(f"videos failed: {ex!r}")
    env.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
