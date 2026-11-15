"""Spot-arm pair, hand-position preflight (docs/spot_arm_pair.md): can a placed hand steer the object?

    python scripts/spot_arm/hand_reach.py [--checkpoint logs/marl2/<run>/model_<n>.pt] [--out evals/spot_arm/hand_reach]

Builds the two-robot env with --arm hand --hand-obs, the elongated object ("long", 20 kg), and runs each Spot alone
(the partner parked far away) from matched starts: straight behind the object's 1 m face, --reps placements
(bearing +-5 deg, object heading +-3 deg, the same for every hand condition). Scripted actions:
  0-1 s    settle (zero action);
  1-4 s    extend: hand point (0.80, y, -0.05) m in the body frame, extension 1; base still;
  4-10 s   walk forward at --vx m/s (default 0.5) with the hand held there (the same base command in every condition).
Hand conditions: left (y = +0.35 m), right (y = -0.35 m), stowed (extension 0).
Per condition and robot: requested vs measured hand point after the reach (before any contact), hand and trunk
contact share and first-contact time, signed object rotation (deg, + = counter-clockwise), object travel, falls.
Pass (exit 0): hand within 10 cm of the request after the reach (gravity sag is 8.5-9 cm); no falls; the left and right reaches rotate the object
in opposite directions, each by at least 3 deg more than the stowed arm does in that direction; the hand touches first.
With --checkpoint (an --arm hand checkpoint): it is reloaded and outputs 7 actions per robot.
Videos (rep 0 of each robot and condition) and report.json in --out.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
PILOT_LEVEL = (1.0, 1.0, 25, 0, 10, 60, 0.10, 6, 1.0, 22, 18)
LONG_HALF_X = 0.25  # the long object's half depth along its heading (the face the robots push is 1 m wide)
HANDS = (("left", 0.35, 1.0), ("right", -0.35, 1.0), ("stowed", 0.0, 0.0))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--checkpoint", default="")
    ap.add_argument("--out", default="evals/spot_arm/hand_reach")
    ap.add_argument("--reps", type=int, default=6)
    ap.add_argument("--vx", type=float, default=0.5, help="walking command, m/s (0.25 barely moves 20 kg even with "
                    "the trunk; at 0.8 the stowed push alone swings the object 20-40 deg)")
    ap.add_argument("--gap", type=float, default=0.15, help="placement gap (m) on top of the object radius and reach")
    ap.add_argument("--mass", type=float, default=20.0)
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
    from quadcoop.coop2.marl import PairPolicy, action_slices
    from quadcoop.coop2.mdp import AGENTS
    from quadcoop.coop2.video import Camera, key_points, render_episode
    from quadcoop.robots import spot_arm as sa
    from quadcoop.stage1.mdp import wrap
    from quadcoop.stage1b.shapes import NOMINAL_MASS
    from quadcoop.stage2 import mdp as m2
    from quadcoop.stage2.shapes import OBJ_NAMES2, SHAPE_NAMES2, SHAPES2

    cases = [(k, h, r) for k in range(2) for h in range(len(HANDS)) for r in range(a.reps)]
    n = len(cases)
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    cfg = make_coop2_env_cfg("b", play=True, partner_map=True, reward_set="r7", arm="hand", hand_obs=True,
                             pilot_level=PILOT_LEVEL, dyaw_choices=True)
    cfg.commands["goal"].start_level = 0
    cfg.scene.num_envs = n
    cfg.episode_length_s = 1e5
    cfg.terminations = {}
    alpha = 0.5 * math.log(a.mass / NOMINAL_MASS)
    for name in OBJ_NAMES2:
        cfg.events[f"{name}_mass"].params["alpha_range"] = (alpha, alpha)
    env = ManagerBasedRlEnv(cfg=cfg, device=device)
    g = env.command_manager.get_term("goal")
    dev, dt = env.device, env.step_dt
    ids = torch.arange(n, device=dev)
    for k in range(len(SHAPES2)):
        m2.apply_geometry(env, ids, k, torch.ones(n, 3, device=dev))
    rng = random.Random("hand-reach")
    jit = {r: (rng.uniform(-5, 5), rng.uniform(-3, 3)) for r in range(a.reps)}
    T = lambda fn: torch.tensor([fn(c) for c in cases], device=dev, dtype=torch.float32)  # noqa: E731
    head = torch.deg2rad(T(lambda c: jit[c[2]][1]))
    bear = math.pi + torch.deg2rad(T(lambda c: jit[c[2]][0]))
    z = torch.zeros(n, device=dev)
    mover = torch.tensor([c[0] for c in cases], device=dev)
    sc = {"shape": torch.full((n,), SHAPE_NAMES2.index("long"), device=dev), "obj_xy_rel": torch.zeros(n, 2, device=dev),
          "obj_heading": head, "goal_xy_rel": torch.tensor([1.0, 0.0], device=dev).repeat(n, 1), "goal_yaw": wrap(head),
          "bearings": [bear, bear], "gaps": [torch.full((n,), a.gap, device=dev)] * 2, "yaw_noise": [z, z],
          "park": [mover != 0, mover != 1]}
    g.scenario = lambda env_ids: {k: ([x[env_ids] for x in v] if isinstance(v, list) else v[env_ids]) for k, v in sc.items()}
    obs, _ = env.reset()
    g.scenario = None
    sl = action_slices(env)
    terms = {ag: env.action_manager.get_term(f"walker_{ag}") for ag in AGENTS}
    assert all(s.stop - s.start == 7 for s in sl.values()), sl
    print(f"actions {({ag: [s.start, s.stop] for ag, s in sl.items()})}; actor inputs "
          f"{({k: list(v.shape[1:]) for k, v in obs.items() if k.startswith('actor_')})}", flush=True)

    hand_y = T(lambda c: HANDS[c[1]][1])
    ext = T(lambda c: HANDS[c[1]][2])
    vx_a = 2 * (a.vx - terms[AGENTS[0]].cfg.vx_range[0]) / (terms[AGENTS[0]].cfg.vx_range[1] - terms[AGENTS[0]].cfg.vx_range[0]) - 1
    vy_a = 2 * (0.0 - terms[AGENTS[0]].cfg.vy_range[0]) / (terms[AGENTS[0]].cfg.vy_range[1] - terms[AGENTS[0]].cfg.vy_range[0]) - 1
    wz_a = 2 * (0.0 - terms[AGENTS[0]].cfg.wz_range[0]) / (terms[AGENTS[0]].cfg.wz_range[1] - terms[AGENTS[0]].cfg.wz_range[0]) - 1
    still_a = 2 * (0.0 - terms[AGENTS[0]].cfg.vx_range[0]) / (terms[AGENTS[0]].cfg.vx_range[1] - terms[AGENTS[0]].cfg.vx_range[0]) - 1
    C, S = sa.HAND_CENTER, sa.HAND_SPAN

    def action(t: float) -> torch.Tensor:
        act = torch.zeros(n, 14, device=dev)
        for k, ag in enumerate(AGENTS):
            s0 = sl[ag].start
            me = mover == k
            if t >= 1.0:
                act[:, s0 + 3] = torch.where(me, torch.full_like(z, (0.80 - C[0]) / S[0]), z)
                act[:, s0 + 4] = torch.where(me, hand_y / S[1], z)
                act[:, s0 + 5] = torch.where(me, torch.full_like(z, (-0.05 - C[2]) / S[2]), z)
                act[:, s0 + 6] = torch.where(me, ext, z)
            walk = torch.tensor([vx_a if t >= 4.0 else still_a, vy_a, wz_a], device=dev)
            still = torch.tensor([still_a, vy_a, wz_a], device=dev)
            act[:, s0:s0 + 3] = torch.where(me.unsqueeze(-1), walk.expand(n, 3), still.expand(n, 3))
        return act

    yaw0 = pos0 = None
    fell = torch.zeros(n, dtype=torch.bool, device=dev)
    hand_c = torch.zeros(n, device=dev)
    trunk_c = torch.zeros(n, device=dev)
    t_hand = torch.full((n,), float("nan"), device=dev)
    t_trunk = torch.full((n,), float("nan"), device=dev)
    reach_err = torch.zeros(n, device=dev)
    face_gap = torch.zeros(n, device=dev)
    film = [j for j, c in enumerate(cases) if c[2] == 0]
    rec = {j: {"q": [], "mp": [], "mq": [], "pts": [], "cap": []} for j in film}
    nmocap = env.sim.mj_model.nmocap
    steps = int(10.0 / dt)
    with torch.no_grad():
        for i in range(steps):
            t = i * dt
            o, *_ = env.step(action(t))
            if i == int(1.0 / dt):
                yaw0, pos0 = g.heading().clone(), g.box_pos()[:, :2].clone()
            hb = {ag: sat.hand_pos_b(env, ag) for ag in AGENTS}
            hw = {ag: sat.hand_pos_w(env, ag) for ag in AGENTS}
            sel = lambda d: torch.where((mover == 0).unsqueeze(-1), d[AGENTS[0]], d[AGENTS[1]])  # noqa: E731
            h_b, h_w = sel(hb), sel(hw)
            cmd = torch.where((mover == 0).unsqueeze(-1), terms[AGENTS[0]].hand_cmd, terms[AGENTS[1]].hand_cmd)
            if i == int(4.0 / dt) - 1:  # after the reach, before walking: requested vs measured; hand to the face
                reach_err = torch.linalg.norm(h_b - cmd, dim=-1)
                rel = h_w[:, :2] - g.box_pos()[:, :2]
                hd = g.heading()
                face_gap = -(torch.cos(hd) * rel[:, 0] + torch.sin(hd) * rel[:, 1]) - LONG_HALF_X
            on_h = torch.where(mover == 0, sat.touch(env, f"arm_{AGENTS[0]}"), sat.touch(env, f"arm_{AGENTS[1]}"))
            on_t = torch.where(mover == 0, sat.touch(env, f"trunk_{AGENTS[0]}"), sat.touch(env, f"trunk_{AGENTS[1]}"))
            if t >= 1.0:
                hand_c += on_h.float()
                trunk_c += on_t.float()
                t_hand = torch.where(on_h & t_hand.isnan(), torch.full_like(t_hand, t), t_hand)
                t_trunk = torch.where(on_t & t_trunk.isnan(), torch.full_like(t_trunk, t), t_trunk)
            for k, ag in enumerate(AGENTS):
                fell |= falls.fallen(env, asset_name=ag, nominal_height=SPECS[ag].nominal_height) & (mover == k)
            if i % 2 == 0:
                sd = env.sim.data
                dyaw = torch.rad2deg(wrap(g.heading() - yaw0)) if yaw0 is not None else torch.zeros(n, device=dev)
                for j in film:
                    c = cases[j]
                    rec[j]["q"].append(sd.qpos[j].cpu().numpy().copy())
                    if nmocap:
                        rec[j]["mp"].append(sd.mocap_pos[j].cpu().numpy().copy())
                        rec[j]["mq"].append(sd.mocap_quat[j].cpu().numpy().copy())
                    kp = key_points(env, j)
                    kp[1 - c[0]] = kp[c[0]]  # frame the mover, not its partner parked 40 m away
                    rec[j]["pts"].append(kp)
                    phase = "settle" if t < 1 else "reach" if t < 4 else f"walk {a.vx:g} m/s"
                    rec[j]["cap"].append(
                        f"{AGENTS[c[0]]} alone, hand {HANDS[c[1]][0]} | {phase} | t {t:4.1f} s\n"
                        f"hand (body frame) requested {np.round(cmd[j].cpu().numpy(), 2)} measured {np.round(h_b[j].cpu().numpy(), 2)} m"
                        f" | extension {float(terms[AGENTS[c[0]]].blend[j]):.2f}\n"
                        f"hand contact {'YES' if bool(on_h[j]) else 'no '} | trunk contact {'YES' if bool(on_t[j]) else 'no '}"
                        f" | object rotation {float(dyaw[j]):+.1f} deg" + (" | FELL" if bool(fell[j]) else ""))
    dyaw = torch.rad2deg(wrap(g.heading() - yaw0))
    travel = torch.linalg.norm(g.box_pos()[:, :2] - pos0, dim=-1)
    span = steps - int(1.0 / dt)
    rows = []
    for j, c in enumerate(cases):
        rows.append({"robot": AGENTS[c[0]], "hand": HANDS[c[1]][0], "rep": c[2], "reach_err_m": round(float(reach_err[j]), 3),
                     "hand_contact_share": round(float(hand_c[j]) / span, 3), "trunk_contact_share": round(float(trunk_c[j]) / span, 3),
                     "t_hand_contact": None if t_hand[j].isnan() else round(float(t_hand[j]), 2),
                     "t_trunk_contact": None if t_trunk[j].isnan() else round(float(t_trunk[j]), 2),
                     "hand_to_face_m": round(float(face_gap[j]), 3), "rotation_deg": round(float(dyaw[j]), 2), "travel_m": round(float(travel[j]), 3), "fell": bool(fell[j])})
    summ = {}
    for ag in AGENTS:
        for hn, _, _ in HANDS:
            sel = [r for r in rows if r["robot"] == ag and r["hand"] == hn]
            mean = lambda k: sum(float(r[k]) for r in sel) / len(sel)  # noqa: E731
            first = [r for r in sel if r["t_hand_contact"] is not None and
                     (r["t_trunk_contact"] is None or r["t_hand_contact"] < r["t_trunk_contact"])]
            summ[f"{ag}/{hn}"] = {"rotation_deg_mean": round(mean("rotation_deg"), 2),
                                  "rotation_deg": [r["rotation_deg"] for r in sel], "travel_m_mean": round(mean("travel_m"), 3),
                                  "reach_err_m_max": max(r["reach_err_m"] for r in sel),
                                  "hand_to_face_m_mean": round(mean("hand_to_face_m"), 3),
                                  "hand_contact_share": round(mean("hand_contact_share"), 3),
                                  "trunk_contact_share": round(mean("trunk_contact_share"), 3),
                                  "hand_touches_first": f"{len(first)}/{len(sel)}", "falls": sum(r["fell"] for r in sel)}
    ok = {}
    # 10 cm: the arm's position actuators (120 Nm/rad) sag 8.5-9 cm under gravity at full reach before any contact;
    # the policy reads the measured hand point
    ok["hand_reaches_request"] = all(r["reach_err_m"] < 0.10 for r in rows if r["hand"] != "stowed")
    ok["no_falls"] = not any(r["fell"] for r in rows)
    for ag in AGENTS:
        L, R, St = (summ[f"{ag}/{h}"]["rotation_deg_mean"] for h in ("left", "right", "stowed"))
        # pushing the face left of centre turns the object clockwise (-), right of centre counter-clockwise (+)
        ok[f"{ag}_left_turns_cw"] = L < St - 3.0
        ok[f"{ag}_right_turns_ccw"] = R > St + 3.0
        ok[f"{ag}_hand_touches_first"] = all(
            int(summ[f"{ag}/{h}"]["hand_touches_first"].split("/")[0]) == a.reps for h in ("left", "right"))
    rep = {"cases": rows, "summary": summ, "vx": a.vx, "gap": a.gap, "mass": a.mass}
    if a.checkpoint:
        ck = torch.load(a.checkpoint, map_location="cpu", weights_only=False)
        o_td = TensorDict({x: v for x, v in o.items() if not x.startswith("walker_")}, batch_size=[n])
        pol = PairPolicy(o_td, device, "b", checkpoint=a.checkpoint)
        with torch.no_grad():
            act = pol(o_td, env=env)
        rep["checkpoint"] = {"path": a.checkpoint, "iter": int(ck["iter"]), "algo": ck["algo"], "act_dims": ck.get("act_dims"),
                             "arm": ck.get("arm"), "hand_obs": ck.get("cfg", {}).get("hand_obs"), "action_shape": list(act.shape)}
        ok["checkpoint_hand_7_per_robot"] = ck.get("arm") == "hand" and list(act.shape) == [n, 14] \
            and set((ck.get("act_dims") or {}).values()) == {7}
    rep["checks"], rep["pass"] = ok, all(ok.values())
    out = ROOT / a.out
    out.mkdir(parents=True, exist_ok=True)
    try:
        cam = Camera(env, 960, 720)
        for j in film:
            c = cases[j]
            render_episode(cam, j, np.stack(rec[j]["q"]), np.stack(rec[j]["mp"]) if nmocap else None,
                           np.stack(rec[j]["mq"]) if nmocap else None, np.stack(rec[j]["pts"]),
                           out / f"{AGENTS[c[0]]}_{HANDS[c[1]][0]}.mp4", fps=1.0 / (2 * dt), caption=lambda f, j=j: rec[j]["cap"][f])
        rep["videos"] = sorted(str(p) for p in out.glob("*.mp4"))
    except Exception as e:  # noqa: BLE001
        rep["video_error"] = repr(e)
        print(f"video failed: {e!r}")
    (out / "report.json").write_text(json.dumps(rep, indent=1))
    for k_, v in summ.items():
        print(f"  {k_:20s} {json.dumps(v)}")
    for k_, v in ok.items():
        print(f"  {'PASS' if v else 'FAIL'}  {k_}")
    print(f"hand reach: {'PASS' if rep['pass'] else 'FAIL'}  ({out / 'report.json'})")
    env.close()
    return 0 if rep["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
