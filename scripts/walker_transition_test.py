"""Walker transition test: what the executor needs beyond steady-state tracking. One robot in its
own walker environment, scripted commands, any number of walkers on identical cases (each in its
own process). Nothing learned above the walker: the same fixed controller runs on every walker.

  transitions  free space. Per axis (forward, sideways, turning) and level: rest 1 s -> +v 4 s ->
               0 3 s -> -v 4 s -> 0 2 s. Start delay (command step -> the 0.4 s average holds >= 50%
               of the command for 1 s; '-' = never within the segment), stop time (-> it holds below
               20%) and stop distance / angle (moved after the stop command), reversal delay, drift
               off the commanded axis (yaw while translating, translation while turning).
  corrections  free space, a fixed position controller (the same for every walker) makes 0.3 m moves
               forward / sideways, and 30 deg turns, in both directions, twice: +d, 0, -d, 0, +d, 0,
               -d, 0. Command = sign(e) x clip(kp |e|, min, max) along the move axis (world frame, so
               yaw drift does not bend the path), engaged above e_on and released below e_off
               (hysteresis); translation 0.1-0.3 m/s, kp 1 /s, e_on 6 cm, e_off 2 cm; turning
               0.2-0.5 rad/s, kp 1.5 /s, e_on 6 deg, e_off 2 deg. A move must settle (|e| < 4 cm / 4 deg
               held 1 s) within 8 s. Per move: initiated (moved 3 cm / 3 deg toward the target within
               3 s), settled, settle time, final error, overshoot, command sign flips, unintended motion
               (yaw during translation, translation during turns). Failures are counted, not averaged.
  loaded       contact. A movable 20 / 40 kg cube 10 cm ahead: push at 0.2 m/s 4 s -> stop 2 s ->
               push 4 s -> back off at -0.1 m/s 2 s. An immovable cube (3000 kg): press at 0.2 m/s 4 s
               -> relax (0) 3 s -> press 3 s -> release (-0.1 m/s) 3 s. Per phase: force, time touching,
               robot and cube speed; restart delay (cube moving at >= 50% of the command, held 1 s),
               contact kept while stopped, re-contact time, release time (force < 5 N held 0.5 s) and
               back-off distance; the stance while standing (pitch, share of time a joint is at >= 95%
               of its torque limit).

    python scripts/walker_transition_test.py --walkers v21=<model.pt>,v22=<model.pt> --name tt-v22
    python scripts/walker_transition_test.py --walkers v1=logs/evals/walker-anymal-v1/model.pt --groups transitions --reps 1

Output: evals/<name>/ (summary.md, summary.json, transitions.csv, corrections.csv, loaded.csv).
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

FRICTION = 0.45
GAP = 0.10
TOUCH_N = 5.0
EFFORT_NM = 80.0
AVG_S = 0.4  # moving-average window (one stride)
HOLD_S = 1.0  # a crossing must hold this long to count

# free transitions: (axis, level); phases (command multiplier, seconds)
TRANS_LEVELS = (("fwd", 0.1), ("fwd", 0.2), ("side", 0.1), ("side", 0.2), ("yaw", 0.2), ("yaw", 0.4))
TRANS_PHASES = ((0.0, 1.0), (1.0, 4.0), (0.0, 3.0), (-1.0, 4.0), (0.0, 2.0))
# corrections: the fixed controller
CORR = {"fwd": dict(d=0.3, kp=1.0, lo=0.1, hi=0.3, on=0.06, off=0.02, tol=0.04, init=0.03),
        "side": dict(d=0.3, kp=1.0, lo=0.1, hi=0.3, on=0.06, off=0.02, tol=0.04, init=0.03),
        "yaw": dict(d=math.radians(30), kp=1.5, lo=0.2, hi=0.5, on=math.radians(6), off=math.radians(2),
                    tol=math.radians(4), init=math.radians(3))}
CORR_MOVES = (1, 0, -1, 0, 1, 0, -1, 0)  # target offsets in units of d
MOVE_MAX_S, INIT_S = 8.0, 3.0
# loaded: (command m/s, seconds, phase name)
LOAD_MOVABLE = ((0.2, 4.0, "push"), (0.0, 2.0, "stop"), (0.2, 4.0, "restart"), (-0.1, 2.0, "back_off"))
LOAD_WALL = ((0.2, 4.0, "press"), (0.0, 3.0, "relax"), (0.2, 3.0, "press_again"), (-0.1, 3.0, "release"))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--walkers", required=True, help="label=checkpoint, comma separated")
    ap.add_argument("--name", default="tt-test")
    ap.add_argument("--groups", default="transitions,corrections,loaded")
    ap.add_argument("--reps", type=int, default=2)
    ap.add_argument("--device", default=None)
    ap.add_argument("--_task", default="", help=argparse.SUPPRESS)
    a = ap.parse_args()

    walkers = [w.split("=", 1) for w in a.walkers.split(",")]
    groups = [g for g in a.groups.split(",") if g]
    if a._task:
        label, path, group, mass, out = a._task.split("|")
        rows = run_task(a, label, path, group, float(mass) if mass else None)
        Path(out).write_text(json.dumps(rows))
        return 0
    tasks = []
    for label, path in walkers:
        p = Path(path)
        path = str(p if p.is_absolute() else ROOT / p)
        if not Path(path).exists():
            raise SystemExit(f"{label}: no checkpoint {path}")
        for g in groups:
            if g == "loaded":
                tasks += [(label, path, g, f"{m:g}") for m in (20.0, 40.0, 3000.0)]
            else:
                tasks.append((label, path, g, ""))
    tmp = ROOT / "logs" / "evals" / a.name / "parts"
    tmp.mkdir(parents=True, exist_ok=True)
    rows = {g: [] for g in ("transitions", "corrections", "loaded")}
    t0 = time.time()
    for i, (label, path, g, m) in enumerate(tasks):
        out = tmp / f"{i:02d}_{label}_{g}{m}.json"
        r = subprocess.run([sys.executable, str(Path(__file__).resolve()), *sys.argv[1:], "--_task",
                            f"{label}|{path}|{g}|{m}|{out}"])
        if r.returncode != 0 or not out.exists():
            raise SystemExit(f"task {label} {g} {m} failed (exit {r.returncode})")
        rows[g] += json.loads(out.read_text())
        print(f"[{label}] {g} {m} done ({time.time() - t0:.0f} s)", flush=True)
    stats = ROOT / "evals" / a.name
    stats.mkdir(parents=True, exist_ok=True)
    for g, rs in rows.items():
        if rs:
            with open(stats / f"{g}.csv", "w", newline="") as f:
                keys = list(dict.fromkeys(k for r in rs for k in r))  # movable and wall rows have different phases
                w = csv.DictWriter(f, fieldnames=keys, restval="")
                w.writeheader()
                w.writerows(rs)
    md, summary = summarise(rows, [w[0] for w in walkers], a, dict(walkers))
    (stats / "summary.md").write_text("\n".join(md) + "\n")
    (stats / "summary.json").write_text(json.dumps(summary, indent=1))
    print("\n".join(md))
    print(f"\nwrote {stats}/")
    return 0


# -- one (walker, group[, mass]) in this process -----------------------------------------------------
def run_task(a, label, path, group, mass):
    import torch

    import quadcoop  # noqa: F401
    from mjlab.envs import ManagerBasedRlEnv
    from mjlab.sensor import ContactMatch, ContactSensorCfg

    from quadcoop.mdp.compliance import contact_force_on_robot_w
    from quadcoop.robots.anymal_c import ROBOT
    from quadcoop.robots.objects import NOMINAL_MASS, OBJECT_NAMES, OBJECTS
    from quadcoop.stage1.walker_policy import FrozenWalker
    from quadcoop.walker_env_cfg import make_walker_env_cfg

    device = a.device or ("cuda:0" if torch.cuda.is_available() else "cpu")
    pol = FrozenWalker(path, device)
    compliant = pol.obs_dim == 50
    cube = OBJECTS[0]

    if group == "transitions":
        cases = [(ax, lv) for ax, lv in TRANS_LEVELS]
    elif group == "corrections":
        cases = [(ax, CORR[ax]["d"]) for ax in ("fwd", "side", "yaw")]
    else:
        cases = [("wall" if mass >= 1000 else "movable", mass)]
    n = len(cases) * a.reps

    cfg = make_walker_env_cfg(ROBOT, play=True, compliant=compliant)
    cfg.scene.num_envs = n
    cfg.episode_length_s = 1e6
    cfg.terminations = {k: v for k, v in cfg.terminations.items() if k != "time_out"}
    tw = cfg.commands["twist"]
    tw.sample_from_ranges = True
    tw.resampling_time_range = (1e9, 1e9)
    tw.rel_standing_envs = 0.0
    if hasattr(tw, "rel_heading_envs"):
        tw.rel_heading_envs = 0.0
    m_ = mass or NOMINAL_MASS
    alpha = 0.5 * math.log(m_ / NOMINAL_MASS)
    for nm in OBJECT_NAMES:
        cfg.events[f"{nm}_mass"].params["alpha_range"] = (alpha, alpha)
        cfg.events[f"{nm}_friction"].params["ranges"] = (FRICTION, FRICTION)
    if not any(s.name == "bumper_force" for s in cfg.scene.sensors):  # v1: measure the force all the same
        cfg.scene.sensors = tuple(cfg.scene.sensors) + (ContactSensorCfg(
            name="bumper_force", primary=ContactMatch(mode="body", pattern=tuple(f"{o}/body" for o in OBJECT_NAMES)),
            secondary=ContactMatch(mode="subtree", pattern=ROBOT.base_body, entity="robot"),
            fields=("found", "force"), reduce="netforce", num_slots=1),)
    torch.manual_seed(0)
    env = ManagerBasedRlEnv(cfg=cfg, device=device)
    dev = env.device
    robot = env.scene["robot"]
    twc = env.command_manager.get_term("twist")
    obs, _ = env.reset()
    if obs["actor"].shape[-1] != pol.obs_dim:
        raise SystemExit(f"{label}: walker expects {pol.obs_dim} inputs, env gives {obs['actor'].shape[-1]}")
    dt = env.step_dt
    nw = max(1, int(round(AVG_S / dt)))
    nh = max(1, int(round(HOLD_S / dt)))

    def set_cmd(v):
        twc.vel_command_b[:] = v
        twc.is_standing_env[:] = False
        twc.is_heading_env[:] = False

    def yaw():
        q = robot.data.root_link_quat_w
        return torch.atan2(2 * (q[:, 0] * q[:, 3] + q[:, 1] * q[:, 2]), 1 - 2 * (q[:, 2] ** 2 + q[:, 3] ** 2))

    def pitch_deg():
        q = robot.data.root_link_quat_w
        return torch.rad2deg(torch.asin((2 * (q[:, 0] * q[:, 2] - q[:, 3] * q[:, 1])).clamp(-1, 1)))

    def body_vel():
        y = yaw()
        c, s = torch.cos(y), torch.sin(y)
        vw = robot.data.root_link_lin_vel_w[:, :2]
        return torch.stack([c * vw[:, 0] + s * vw[:, 1], -s * vw[:, 0] + c * vw[:, 1], robot.data.root_link_ang_vel_w[:, 2]], -1)

    def push_force():  # on the cube along the robot's heading, N
        y = yaw()
        f = contact_force_on_robot_w(env, "bumper_force")
        return -(f[:, 0] * torch.cos(y) + f[:, 1] * torch.sin(y)), torch.linalg.norm(f, dim=-1)

    def is_fallen():
        return (env.termination_manager.terminated if hasattr(env.termination_manager, "terminated")
                else torch.zeros(n, dtype=torch.bool, device=dev))

    def step(cmd):
        nonlocal obs
        set_cmd(cmd)
        obs, *_ = env.step(pol(obs["actor"]))
        set_cmd(cmd)

    zero = torch.zeros(n, 3, device=dev)
    for _ in range(int(1.0 / dt)):  # settle standing
        step(zero)

    case_of = [cases[e // a.reps] for e in range(n)]
    rep_of = [e % a.reps for e in range(n)]
    rows = []
    fell = torch.zeros(n, dtype=torch.bool, device=dev)

    if group == "transitions":
        ax = torch.tensor([{"fwd": 0, "side": 1, "yaw": 2}[c[0]] for c in case_of], device=dev)
        lv = torch.tensor([c[1] for c in case_of], device=dev)
        V, P, Y = [], [], []
        seg_start = []
        t = 0
        for mult, secs in TRANS_PHASES:
            seg_start.append(t)
            for _ in range(int(round(secs / dt))):
                cmd = torch.zeros(n, 3, device=dev)
                cmd[torch.arange(n), ax] = mult * lv
                step(cmd)
                fell |= is_fallen()
                V.append(body_vel().gather(1, ax.unsqueeze(1)).squeeze(1) / lv)  # in units of the command
                P.append(robot.data.root_link_pos_w[:, :2].clone())
                Y.append(yaw())
                t += 1
        V = torch.stack(V)  # (T, n), command units
        P, Y = torch.stack(P), torch.stack(Y)
        avg = moving_average(V, nw)  # avg[k] = mean of V[k : k + nw]

        def first_hold(seg, cond):  # first step in segment `seg` from which `cond` (on the average) holds HOLD_S
            lo, hi = seg_start[seg], (seg_start[seg + 1] if seg + 1 < len(seg_start) else V.shape[0])
            out = torch.full((n,), float("nan"), device=dev)
            c = cond(avg[lo:max(lo + 1, hi - nw + 1)]).float()  # (k, n)
            if c.shape[0] < nh:
                return out
            win = moving_average(c, nh) >= 1.0 - 1e-6  # holds for nh consecutive windows
            got = win.any(0)
            idx = win.float().argmax(0).float()
            return torch.where(got, (idx + nw) * dt, out)  # + window: the average lags the motion

        start = first_hold(1, lambda x: x >= 0.5)
        stop = first_hold(2, lambda x: x.abs() <= 0.2)
        rev = first_hold(3, lambda x: x <= -0.5)
        s2, s3 = seg_start[2], seg_start[3]
        for e in range(n):
            axis, level = case_of[e]
            if axis == "yaw":
                stop_dist = math.degrees(abs(wrap(float(Y[s3 - 1, e] - Y[s2 - 1, e]))))
                drift = float(torch.linalg.norm(P[s2 - 1, e] - P[seg_start[1], e]))  # translation while turning
                drift_unit = "m"
            else:
                u = P[s3 - 1, e] - P[s2 - 1, e]
                y0 = float(Y[s2 - 1, e])
                axv = torch.tensor([math.cos(y0), math.sin(y0)] if axis == "fwd" else [-math.sin(y0), math.cos(y0)], device=dev)
                stop_dist = abs(float((u * axv).sum()))
                drift = math.degrees(abs(wrap(float(Y[s2 - 1, e] - Y[seg_start[1], e]))))  # yaw while translating
                drift_unit = "deg"
            achieved = float(V[seg_start[1] + int(2.0 / dt):seg_start[2], e].mean()) * level
            moving = not math.isnan(float(start[e]))  # stopping is only measured if it got going
            rows.append({"walker": label, "axis": axis, "level": level, "rep": rep_of[e],
                         "start_s": nanr(start[e]), "achieved": round(achieved, 4), "stop_s": nanr(stop[e]) if moving else "n/a",
                         "stop_dist": round(stop_dist, 4) if moving else "n/a", "stop_unit": "deg" if axis == "yaw" else "m",
                         "reverse_s": nanr(rev[e]), "drift": round(drift, 3), "drift_unit": drift_unit,
                         "fell": int(fell[e])})
        return rows

    if group == "corrections":
        axn = [c[0] for c in case_of]
        prm = {k: torch.tensor([CORR[x][k] for x in axn], device=dev) for k in CORR["fwd"]}
        is_yaw = torch.tensor([x == "yaw" for x in axn], device=dev)
        is_side = torch.tensor([x == "side" for x in axn], device=dev)
        p0, y0 = robot.data.root_link_pos_w[:, :2].clone(), yaw().clone()
        axis_w = torch.where(is_side.unsqueeze(1), torch.stack([-torch.sin(y0), torch.cos(y0)], -1),
                             torch.stack([torch.cos(y0), torch.sin(y0)], -1))
        perp_w = torch.stack([-axis_w[:, 1], axis_w[:, 0]], -1)
        mv = torch.zeros(n, dtype=torch.long, device=dev)  # current move index
        t_mv = torch.zeros(n, device=dev)  # time in move
        held = torch.zeros(n, device=dev)  # time |e| < tol
        engaged = torch.zeros(n, dtype=torch.bool, device=dev)
        done = torch.zeros(n, dtype=torch.bool, device=dev)
        moves = torch.tensor(CORR_MOVES, device=dev, dtype=torch.float)
        # per-move records
        rec = []
        cur = None

        def pos_err():
            tgt_off = moves[mv.clamp(max=len(CORR_MOVES) - 1)] * prm["d"]
            pos = robot.data.root_link_pos_w[:, :2]
            along = ((pos - p0) * axis_w).sum(-1)
            return torch.where(is_yaw, wrap_t(y0 + tgt_off - yaw()), tgt_off - along), along

        def new_move_state():
            e, along = pos_err()
            return {"e0": e.clone(), "along0": along.clone(), "yaw0": yaw().clone(),
                    "p0": robot.data.root_link_pos_w[:, :2].clone(), "init": torch.full((n,), float("nan"), device=dev),
                    "settle": torch.full((n,), float("nan"), device=dev), "over": torch.zeros(n, device=dev),
                    "flips": torch.zeros(n, device=dev), "last_sign": torch.zeros(n, device=dev),
                    "yaw_dev": torch.zeros(n, device=dev), "cross": torch.zeros(n, device=dev)}

        cur = new_move_state()
        limit = int((MOVE_MAX_S * len(CORR_MOVES) + 5) / dt)
        for _ in range(limit):
            e, along = pos_err()
            mag = e.abs()
            engaged = torch.where(mag > prm["on"], torch.ones_like(engaged), torch.where(mag < prm["off"], torch.zeros_like(engaged), engaged))
            sp = torch.clamp(prm["kp"] * mag, min=prm["lo"], max=prm["hi"]) * torch.sign(e) * engaged.float()
            sp = torch.where(done, torch.zeros_like(sp), sp)
            y = yaw()
            u_w = axis_w * sp.unsqueeze(1)  # world-frame translation command
            cmd = torch.zeros(n, 3, device=dev)
            cmd[:, 0] = torch.where(is_yaw, 0.0, torch.cos(y) * u_w[:, 0] + torch.sin(y) * u_w[:, 1])
            cmd[:, 1] = torch.where(is_yaw, 0.0, -torch.sin(y) * u_w[:, 0] + torch.cos(y) * u_w[:, 1])
            cmd[:, 2] = torch.where(is_yaw, sp, 0.0)
            step(cmd)
            fell |= is_fallen()
            t_mv += dt
            # bookkeeping on the state after the step
            e, along = pos_err()
            d0 = torch.sign(cur["e0"])
            progress = torch.where(is_yaw, wrap_t(yaw() - cur["yaw0"]) * d0, (along - cur["along0"]) * d0)
            cur["init"] = torch.where(torch.isnan(cur["init"]) & (progress >= prm["init"]), t_mv, cur["init"])
            cur["over"] = torch.maximum(cur["over"], (-e * d0).clamp(min=0.0))
            s = torch.sign(sp)
            flip = (s != 0) & (cur["last_sign"] != 0) & (s != cur["last_sign"])
            cur["flips"] += flip.float()
            cur["last_sign"] = torch.where(s != 0, s, cur["last_sign"])
            cur["yaw_dev"] = torch.maximum(cur["yaw_dev"], wrap_t(yaw() - cur["yaw0"]).abs())
            cur["cross"] = torch.maximum(cur["cross"], torch.where(
                is_yaw, torch.linalg.norm(robot.data.root_link_pos_w[:, :2] - cur["p0"], dim=-1),
                ((robot.data.root_link_pos_w[:, :2] - cur["p0"]) * perp_w).sum(-1).abs()))
            held = torch.where(e.abs() < prm["tol"], held + dt, torch.zeros_like(held))
            settled_now = held >= HOLD_S
            cur["settle"] = torch.where(torch.isnan(cur["settle"]) & settled_now, t_mv - HOLD_S, cur["settle"])
            finish = (~done) & (settled_now | (t_mv >= MOVE_MAX_S))
            if finish.any():
                for ei in finish.nonzero().flatten().tolist():
                    k = int(mv[ei])
                    rec.append({"walker": label, "axis": axn[ei], "rep": rep_of[ei], "move": k,
                                "target": round(float(moves[k] * prm["d"][ei]) * (180 / math.pi if axn[ei] == "yaw" else 1.0), 3),
                                "unit": "deg" if axn[ei] == "yaw" else "m",
                                "initiated": int(not math.isnan(float(cur["init"][ei]))),
                                "init_s": nanr(cur["init"][ei]),
                                "settled": int(not math.isnan(float(cur["settle"][ei]))),
                                "settle_s": nanr(cur["settle"][ei]),
                                "final_err": round(float(e[ei].abs()) * (180 / math.pi if axn[ei] == "yaw" else 1.0), 4),
                                "overshoot": round(float(cur["over"][ei]) * (180 / math.pi if axn[ei] == "yaw" else 1.0), 4),
                                "flips": int(cur["flips"][ei]),
                                "unintended": round(float(cur["cross"][ei]) if axn[ei] == "yaw" else math.degrees(float(cur["yaw_dev"][ei])), 4),
                                "unintended_unit": "m (translation)" if axn[ei] == "yaw" else "deg (yaw)",
                                "fell": int(fell[ei])})
                mv = torch.where(finish, mv + 1, mv)
                done |= mv >= len(CORR_MOVES)
                t_mv = torch.where(finish, torch.zeros_like(t_mv), t_mv)
                held = torch.where(finish, torch.zeros_like(held), held)
                fresh = new_move_state()
                for k_ in cur:
                    f_ = finish.view(-1, *([1] * (cur[k_].dim() - 1)))
                    cur[k_] = torch.where(f_, fresh[k_], cur[k_])
            if bool(done.all()):
                break
        return rec

    # loaded
    kind = case_of[0][0]
    phases = LOAD_WALL if kind == "wall" else LOAD_MOVABLE
    ob = env.scene[cube.name]
    y = yaw()
    fwd = torch.stack([torch.cos(y), torch.sin(y)], -1)
    st = torch.zeros(n, 13, device=dev)
    st[:, :2] = robot.data.root_link_pos_w[:, :2] + fwd * (ROBOT.half_length + cube.half_extent_x + GAP)
    st[:, 2] = cube.half_height + 0.005
    st[:, 3:7] = torch.stack([torch.cos(y / 2), 0 * y, 0 * y, torch.sin(y / 2)], -1)
    ob.write_root_state_to_sim(st)
    F, TOUCH, RV, OV, P, PITCH, SAT = [], [], [], [], [], [], []
    seg = []
    t = 0
    for v, secs, nm in phases:
        seg.append((nm, t, v))
        for _ in range(int(round(secs / dt))):
            cmd = torch.zeros(n, 3, device=dev)
            cmd[:, 0] = v
            step(cmd)
            fell |= is_fallen()
            fh, fm = push_force()
            F.append(fh)
            TOUCH.append((fm > TOUCH_N).float())
            RV.append(body_vel()[:, 0])
            yy = yaw()
            ovw = ob.data.root_link_lin_vel_w[:, :2]
            OV.append(ovw[:, 0] * torch.cos(yy) + ovw[:, 1] * torch.sin(yy))
            P.append(robot.data.root_link_pos_w[:, :2].clone())
            PITCH.append(pitch_deg())
            SAT.append((robot.data.actuator_force.abs() >= 0.95 * EFFORT_NM).any(-1).float())
            t += 1
    F, TOUCH, RV, OV, P = torch.stack(F), torch.stack(TOUCH), torch.stack(RV), torch.stack(OV), torch.stack(P)
    PITCH, SAT = torch.stack(PITCH), torch.stack(SAT)
    T = F.shape[0]
    bounds = [(nm, lo, (seg[i + 1][1] if i + 1 < len(seg) else T), v) for i, (nm, lo, v) in enumerate(seg)]

    def hold_time(series, lo, hi, cond, hold):  # first time in [lo, hi) from which cond(series) holds `hold` steps
        c = cond(series[lo:hi]).float()
        out = torch.full((n,), float("nan"), device=dev)
        if c.shape[0] < hold:
            return out
        win = moving_average(c, hold) >= 1.0 - 1e-6
        return torch.where(win.any(0), win.float().argmax(0).float() * dt, out)

    for e in range(n):
        row = {"walker": label, "case": kind, "mass": mass, "rep": rep_of[e], "fell": int(fell[e])}
        for nm, lo, hi, v in bounds:
            half = lo + (hi - lo) // 2
            row[f"{nm}_force"] = round(float(F[half:hi, e].mean()), 1)
            row[f"{nm}_touch"] = round(float(TOUCH[lo:hi, e].mean()), 3)
            row[f"{nm}_robot_v"] = round(float(RV[half:hi, e].mean()), 4)
            row[f"{nm}_cube_v"] = round(float(OV[half:hi, e].mean()), 4)
            if v == 0.0:
                row[f"{nm}_pitch_deg"] = round(float(PITCH[half:hi, e].mean()), 1)
                row[f"{nm}_torque_sat"] = round(float(SAT[half:hi, e].mean()), 3)
        rows.append(row)
    # transition times (per env)
    for nm, lo, hi, v in bounds:
        if nm == "restart":
            tt = hold_time(moving_average_full(OV, nw), lo, hi, lambda x: x >= 0.5 * v, nh)
            tc = hold_time(TOUCH, lo, hi, lambda x: x > 0.5, int(0.5 / dt))
            for e in range(n):
                rows[-n + e]["restart_cube_moving_s"] = nanr(tt[e])
                rows[-n + e]["restart_recontact_s"] = nanr(tc[e])
        if nm in ("press_again",):
            tc = hold_time(TOUCH, lo, hi, lambda x: x > 0.5, int(0.5 / dt))
            for e in range(n):
                rows[-n + e]["press_again_recontact_s"] = nanr(tc[e])
        if nm in ("back_off", "release"):
            tr = hold_time(TOUCH, lo, hi, lambda x: x < 0.5, int(0.5 / dt))
            was = TOUCH[max(0, lo - int(0.5 / dt)):lo].mean(0) > 0.5  # touching just before: else nothing to release
            for e in range(n):
                y0 = float(yaw()[e])
                d = P[hi - 1, e] - P[lo, e]
                rows[-n + e][f"{nm}_release_s"] = nanr(tr[e]) if bool(was[e]) else "n/a"
                rows[-n + e][f"{nm}_backed_m"] = round(-float(d[0] * math.cos(y0) + d[1] * math.sin(y0)), 3)
    return rows


# -- helpers -------------------------------------------------------------------------------------------
def moving_average(x, k):
    """(T, ...) -> (T - k + 1, ...): means of k consecutive rows (x itself if T < k)."""
    import torch

    if x.shape[0] < k:
        return x.mean(0, keepdim=True)
    c = torch.cumsum(torch.cat([torch.zeros_like(x[:1]), x], 0), 0)
    return (c[k:] - c[:-k]) / k


def moving_average_full(x, k):
    """Same length as x: trailing average (shorter at the start)."""
    import torch

    c = torch.cumsum(torch.cat([torch.zeros_like(x[:1]), x], 0), 0)
    idx = torch.arange(1, x.shape[0] + 1, device=x.device)
    lo = (idx - k).clamp(min=0)
    return (c[idx] - c[lo]) / (idx - lo).unsqueeze(-1).to(x.dtype)


def wrap(a):
    return (a + math.pi) % (2 * math.pi) - math.pi


def wrap_t(a):
    import torch

    return torch.remainder(a + math.pi, 2 * math.pi) - math.pi


def nanr(x, nd=2):
    x = float(x)
    return "" if math.isnan(x) else round(x, nd)


# -- summary ---------------------------------------------------------------------------------------------
def summarise(rows, labels, a, paths):
    def mean(xs):
        xs = [float(x) for x in xs if x not in ("", "n/a") and x is not None]
        return sum(xs) / len(xs) if xs else float("nan")

    def fmt(x, nd=2):
        return "-" if x != x else f"{x:.{nd}f}"

    def timing(rs, k):  # mean over trials that got there, and how many did ('n/a' trials left out)
        rs = [r for r in rs if r[k] != "n/a"]
        if not rs:
            return "n/a"
        got = [r[k] for r in rs if r[k] != ""]
        return f"{fmt(mean(got))} ({len(got)}/{len(rs)})" if got else f"never (0/{len(rs)})"

    md = [f"# Walker transition test: {a.name}", "",
          "Checkpoints: " + "; ".join(f"{l} = `{paths[l]}`" for l in labels), "",
          f"Times include about {AVG_S / 2:g} s of averaging lag; a crossing counts only if it holds {HOLD_S:g} s. "
          "(n/m) = trials that got there out of all trials; failures are listed, not averaged in.", ""]
    summary = {"walkers": labels, "checkpoints": paths}
    tr = rows["transitions"]
    if tr:
        md += ["## Transitions in free space (start from rest, stop, reverse)", "",
               "| axis | level | " + " | ".join(f"{l}: start s / achieved / stop s, stop dist / reverse s / drift" for l in labels) + " |",
               "|---|---|" + "---|" * len(labels)]
        for ax, lv in TRANS_LEVELS:
            cells = []
            for l in labels:
                rs = [r for r in tr if r["walker"] == l and r["axis"] == ax and abs(r["level"] - lv) < 1e-9]
                if not rs:
                    cells.append("-")
                    continue
                cells.append(f"{timing(rs, 'start_s')} / {mean([r['achieved'] for r in rs]):+.3f} / "
                             f"{timing(rs, 'stop_s')}, {mean([r['stop_dist'] for r in rs]):.3f} {rs[0]['stop_unit']} / "
                             f"{timing(rs, 'reverse_s')} / {mean([r['drift'] for r in rs]):.2f} {rs[0]['drift_unit']}"
                             + (" FELL" if any(r["fell"] for r in rs) else ""))
            md.append(f"| {ax} | {lv:g} {'rad/s' if ax == 'yaw' else 'm/s'} | " + " | ".join(cells) + " |")
        md.append("")
        summary["transitions"] = {l: {"start_failures": sum(r["start_s"] == "" for r in tr if r["walker"] == l),
                                      "reverse_failures": sum(r["reverse_s"] == "" for r in tr if r["walker"] == l),
                                      "stop_failures": sum(r["stop_s"] == "" for r in tr if r["walker"] == l),
                                      "stop_not_measured": sum(r["stop_s"] == "n/a" for r in tr if r["walker"] == l),
                                      "trials": sum(r["walker"] == l for r in tr),
                                      "falls": sum(r["fell"] for r in tr if r["walker"] == l)} for l in labels}
        for l in labels:
            s = summary["transitions"][l]
            md.append(f"**{l}:** failed to start {s['start_failures']}/{s['trials']}, to stop {s['stop_failures']}/"
                      f"{s['trials'] - s['stop_not_measured']} (of those that started), "
                      f"to reverse {s['reverse_failures']}/{s['trials']}; falls {s['falls']}.")
        md.append("")
    co = rows["corrections"]
    if co:
        md += ["## Position corrections with one fixed controller (0.3 m moves, 30 deg turns; both directions, twice)", "",
               "| axis | " + " | ".join(f"{l}: not initiated / not settled / moves" for l in labels) + " | "
               + " | ".join(f"{l}: settle s / final err / overshoot / flips / unintended" for l in labels) + " |",
               "|---|" + "---|" * (2 * len(labels))]
        summary["corrections"] = {}
        for ax in ("fwd", "side", "yaw"):
            c1, c2 = [], []
            for l in labels:
                rs = [r for r in co if r["walker"] == l and r["axis"] == ax]
                if not rs:
                    c1.append("-")
                    c2.append("-")
                    continue
                ni = sum(1 - r["initiated"] for r in rs)
                ns = sum(1 - r["settled"] for r in rs)
                u = rs[0]["unit"]
                c1.append(f"{ni} / {ns} / {len(rs)}")
                ok = [r for r in rs if r["settled"]]
                c2.append(f"{fmt(mean([r['settle_s'] for r in ok]))} / {fmt(mean([r['final_err'] for r in rs]), 3)} {u} / "
                          f"{fmt(mean([r['overshoot'] for r in rs]), 3)} {u} / {fmt(mean([r['flips'] for r in rs]), 1)} / "
                          f"{fmt(mean([r['unintended'] for r in rs]), 3)} {rs[0]['unintended_unit']}"
                          + (" FELL" if any(r["fell"] for r in rs) else ""))
                summary["corrections"].setdefault(l, {})[ax] = {"moves": len(rs), "not_initiated": ni, "not_settled": ns}
            md.append(f"| {ax} | " + " | ".join(c1) + " | " + " | ".join(c2) + " |")
        md += ["", "Settle time is over settled moves only; final error, overshoot and flips are over all moves.", ""]
        fails = [r for r in co if not r["initiated"] or not r["settled"]]
        if fails:
            md += ["Failed moves (walker, axis, rep, move, target): " + "; ".join(
                f"{r['walker']} {r['axis']} r{r['rep']} m{r['move']} {r['target']:+g}{'d' if r['unit'] == 'deg' else 'm'}"
                f"{'' if r['initiated'] else ' (never started)'}" for r in fails), ""]
    lo = rows["loaded"]
    if lo:
        md += ["## Under load", ""]
        summary["loaded"] = {}
        for kind, phases in (("movable", LOAD_MOVABLE), ("wall", LOAD_WALL)):
            rs_k = [r for r in lo if r["case"] == kind]
            if not rs_k:
                continue
            for m in sorted({r["mass"] for r in rs_k}):
                md += [f"### {'immovable cube' if kind == 'wall' else f'{m:g} kg cube'}: "
                       + " -> ".join(f"{nm} {v:+g} m/s {s:g} s" for v, s, nm in phases), "",
                       "| phase | " + " | ".join(f"{l}: force N / touching / robot v / cube v" for l in labels) + " |",
                       "|---|" + "---|" * len(labels)]
                for v, s, nm in phases:
                    cells = []
                    for l in labels:
                        rs = [r for r in rs_k if r["walker"] == l and r["mass"] == m]
                        cells.append(f"{mean([r[f'{nm}_force'] for r in rs]):.0f} / {mean([r[f'{nm}_touch'] for r in rs]):.2f} / "
                                     f"{mean([r[f'{nm}_robot_v'] for r in rs]):+.3f} / {mean([r[f'{nm}_cube_v'] for r in rs]):+.3f}"
                                     if rs else "-")
                    md.append(f"| {nm} | " + " | ".join(cells) + " |")
                md.append("")
                for l in labels:
                    rs = [r for r in rs_k if r["walker"] == l and r["mass"] == m]
                    if not rs:
                        continue
                    bits = []
                    if kind == "movable":
                        bits += [f"cube moving again after restart {timing(rs, 'restart_cube_moving_s')} s",
                                 f"re-contact {timing(rs, 'restart_recontact_s')} s",
                                 f"contact kept while stopped {mean([r['stop_touch'] for r in rs]):.2f}",
                                 f"backing off: contact released {timing(rs, 'back_off_release_s')} s, "
                                 f"backed {mean([r['back_off_backed_m'] for r in rs]):.3f} m",
                                 f"stance while stopped: pitch {mean([r['stop_pitch_deg'] for r in rs]):+.1f} deg, "
                                 f"torque at limit {mean([r['stop_torque_sat'] for r in rs]):.2f}"]
                    else:
                        bits += [f"force while relaxed {mean([r['relax_force'] for r in rs]):.0f} N",
                                 f"re-contact on pressing again {timing(rs, 'press_again_recontact_s')} s",
                                 f"release {timing(rs, 'release_release_s')} s, backed {mean([r['release_backed_m'] for r in rs]):.3f} m",
                                 f"stance while relaxed: pitch {mean([r['relax_pitch_deg'] for r in rs]):+.1f} deg, "
                                 f"torque at limit {mean([r['relax_torque_sat'] for r in rs]):.2f}"]
                    falls = sum(r["fell"] for r in rs)
                    md.append(f"**{l}:** " + "; ".join(bits) + f"; falls {falls}/{len(rs)}.")
                    summary["loaded"].setdefault(l, {})[f"{kind}_{m:g}"] = {"falls": falls, "trials": len(rs)}
                md.append("")
    return md, summary


if __name__ == "__main__":
    sys.exit(main())
