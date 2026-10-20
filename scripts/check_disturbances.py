#!/usr/bin/env python3
"""Prove that the disturbances and resets reach the physics, not just the config.

    python scripts/check_disturbances.py --task QuadCoop-Walker-AnymalC
    python scripts/check_disturbances.py --task QuadCoop-Walker-Spot

Checks, each on the real training environment:

  1. Force routing.   MuJoCo's xfrc_applied on the base equals the force and lever
                      torque the PushForce term intends, every step, every env, and
                      no other robot body or object receives a force.
  2. Physical effect. Same seed, same everything, force on vs off: the robot moves
                      along the force direction (cosine > 0.8) and clearly farther.
  3. Resets.          After a partial reset: episode counters restart, the push force
                      restarts at zero (no force leaks across episodes), joints return
                      to the standing pose, base yaw is randomized, and at most one
                      object is in front of the robot with the rest parked;
                      non-reset envs are untouched.
  4. Randomization.   Per-env foot friction, base COM offset and object masses are actually
                      different across envs and inside their configured ranges; foot
                      friction is shared across a robot's feet; impulse pushes and
                      object re-placement events are scheduled.
  5. Curriculum.      Force is zero during warm-up, then ramps 0.2 -> 1; object
                      placement ramps 0 -> p_max; the mass cap rises only when
                      engaged robots succeed and falls back when they fall.

Exit code 0 = all passed. Runs on CPU or GPU (slurm/smoke.sbatch runs it on GPU).
"""

from __future__ import annotations

import argparse
import gc
import math
import os
import sys

# These checks exercise the bumper force field, which training leaves off by default.
os.environ.setdefault("QUADCOOP_PUSH_FORCE", "1")
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import torch  # noqa: E402

FAILS: list[str] = []


def check(ok: bool, msg: str) -> None:
    print(f"  {'ok  ' if ok else 'FAIL'} {msg}")
    if not ok:
        FAILS.append(msg)


def make_env(task: str, n: int, device: str, edit=None):
    from mjlab.envs import ManagerBasedRlEnv
    from mjlab.tasks.registry import load_env_cfg

    cfg = load_env_cfg(task)
    cfg.scene.num_envs = n
    cfg.seed = 0
    if edit is not None:
        edit(cfg)
    # These tests hold zero action, so the robot is not expected to stand. Fall
    # terminations would reset envs mid-test (and restart the force); they are
    # tested separately in check_termination.py.
    cfg.terminations.pop("illegal_contact", None)
    cfg.terminations.pop("fell_over", None)
    torch.manual_seed(0)
    env = ManagerBasedRlEnv(cfg=cfg, device=device)
    env.reset()
    return env


def close(env) -> None:
    env.close()
    del env
    gc.collect()


def fast_force(cfg) -> None:
    pf = cfg.commands["push_force"]
    pf.gap_s, pf.ramp_s, pf.hold_s = (0.0, 0.2), (0.1, 0.3), (1.0, 2.0)
    pf.curriculum_start_scale = 1.0
    pf.warmup_env_steps = 0.0  # Training has a plain-walking warm-up; skip it here.


# ---------------------------------------------------------------------------
def test_routing(task: str, device: str, steps: int) -> None:
    from mjlab.utils.lab_api.math import quat_apply, yaw_quat

    print("\n[1] force routing: xfrc_applied == intended wrench")

    def edit(cfg):
        fast_force(cfg)
        cfg.events.pop("push_robot", None)

    env = make_env(task, 8, device, edit)
    from quadcoop.robots.objects import OBJECT_NAMES

    robot = env.scene["robot"]
    objects = [env.scene[name] for name in OBJECT_NAMES]
    term = env.command_manager.get_term("push_force")
    base_local = robot.find_bodies((term.cfg.body_name,), preserve_order=True)[0][0]
    zero = torch.zeros(env.action_space.shape, device=device)
    max_err_f = max_err_t = max_other = max_box = 0.0
    max_f = 0.0
    for _ in range(steps):
        env.step(zero)
        q = robot.data.root_link_quat_w
        f_exp = quat_apply(yaw_quat(q), term.applied_force_yaw)
        point = robot.data.root_link_pos_w + quat_apply(q, term.push_point_b)
        com = robot.data.body_com_pos_w[:, base_local]
        t_exp = torch.linalg.cross(point - com, f_exp)
        w = robot.data.body_external_wrench  # (B, nbodies, 6) world frame
        max_err_f = max(max_err_f, (w[:, base_local, :3] - f_exp).abs().max().item())
        max_err_t = max(max_err_t, (w[:, base_local, 3:] - t_exp).abs().max().item())
        others = torch.cat([w[:, :base_local], w[:, base_local + 1:]], dim=1)
        max_other = max(max_other, others.abs().max().item() if others.numel() else 0.0)
        max_box = max(max_box, max(o.data.body_external_wrench.abs().max().item() for o in objects))
        max_f = max(max_f, torch.linalg.norm(f_exp, dim=-1).max().item())
    check(max_f > 10.0, f"force actually on during the test (peak {max_f:.0f} N)")
    check(max_err_f < 1e-3, f"base force matches intended (max err {max_err_f:.1e} N)")
    check(max_err_t < 1e-3, f"base torque = (bumper - COM) x force (max err {max_err_t:.1e} N m)")
    check(max_other == 0.0, "no other robot body receives an external force")
    check(max_box == 0.0, "no object receives an external force")
    close(env)


# ---------------------------------------------------------------------------
def _fixed_command(cfg, vx: float) -> None:
    twist = cfg.commands["twist"]
    twist.ranges.lin_vel_x = (vx, vx)
    twist.ranges.lin_vel_y = (0.0, 0.0)
    twist.ranges.ang_vel_z = (0.0, 0.0)
    twist.ranges.heading = None
    twist.heading_command = False
    twist.rel_standing_envs = 0.0
    twist.rel_heading_envs = 0.0
    twist.rel_forward_envs = 0.0
    twist.resampling_time_range = (1e9, 1e9)


def test_effect(task: str, device: str, seconds: float = 0.4) -> None:
    """Impulse-momentum check in free fall, where no ground contact can hide the force.

    The robot starts 2 m up, so for ~0.6 s the only horizontal external force on it is
    ours. Then (total momentum change) on-run minus off-run must equal the impulse
    sum(F dt) we applied, in both size and direction.
    """
    print("\n[2] physical effect: free-fall impulse-momentum check")

    def edit(on: bool):
        def _e(cfg):
            pf = cfg.commands["push_force"]
            pf.fixed_frac = 0.35 if on else 0.0
            pf.p_oppose, pf.oppose_jitter_deg = 0.0, 0.0  # random horizontal directions
            pf.gap_s, pf.ramp_s, pf.hold_s = (0.05, 0.05), (0.05, 0.05), (1e9, 1e9)
            pf.curriculum_start_scale = 1.0
            pf.warmup_env_steps = 0.0
            cfg.events.pop("push_robot", None)
            cfg.commands["twist"].p_override = 0.0
            cfg.events["reset_base"].params["pose_range"]["z"] = (1.5, 1.5)
        return _e

    def momentum(env):
        robot = env.scene["robot"]
        m = env.sim.model.body_mass[:, robot.indexing.body_ids]  # (B, nb)
        v = robot.data.body_com_lin_vel_w  # (B, nb, 3)
        return (m.unsqueeze(-1) * v).sum(1)

    def ang_momentum(env):
        """Whole-robot angular momentum about the robot's COM, from first principles:
        sum_i  m_i (c_i - c) x v_i  +  R_i I_i R_i^T w_i."""
        robot = env.scene["robot"]
        ids = robot.indexing.body_ids
        m = env.sim.model.body_mass[:, ids]  # (B, nb)
        inertia = env.sim.model.body_inertia[:, ids]  # (B, nb, 3) principal moments
        c_i = robot.data.body_com_pos_w  # (B, nb, 3)
        v_i = robot.data.body_com_lin_vel_w
        w_i = robot.data.body_com_ang_vel_w
        R = robot.data.data.ximat[:, ids].reshape(c_i.shape[0], -1, 3, 3)  # inertial frames
        c = (m.unsqueeze(-1) * c_i).sum(1, keepdim=True) / m.sum(1, keepdim=True).unsqueeze(-1)
        orbital = (m.unsqueeze(-1) * torch.linalg.cross(c_i - c, v_i)).sum(1)
        w_local = torch.einsum("bnji,bnj->bni", R, w_i)  # R^T w
        spin = torch.einsum("bnij,bnj->bni", R, inertia * w_local).sum(1)
        return orbital + spin

    res = {}
    for on in (True, False):
        env = make_env(task, 8, device, edit(on))
        robot = env.scene["robot"]
        term = env.command_manager.get_term("push_force")
        zero = torch.zeros(env.action_space.shape, device=device)
        from mjlab.utils.lab_api.math import quat_apply as qa

        p0, l0 = momentum(env), ang_momentum(env)
        impulse = torch.zeros(8, 3, device=device)
        ang_impulse = torch.zeros(8, 3, device=device)
        ang_impulse_com = torch.zeros(8, 3, device=device)  # if it acted at the base COM
        z_min = float("inf")
        for _ in range(int(seconds / env.step_dt)):
            # The wrench written at the end of the previous step acts during this one.
            f = robot.data.body_external_wrench[:, :, :3].sum(1)
            impulse += f * env.step_dt
            # Torque about the whole robot's COM of a force acting AT THE BUMPER.
            bumper = robot.data.root_link_pos_w + qa(robot.data.root_link_quat_w, term.push_point_b)
            ids = robot.indexing.body_ids
            m = env.sim.model.body_mass[:, ids]
            c_sys = (m.unsqueeze(-1) * robot.data.body_com_pos_w).sum(1) / m.sum(1, keepdim=True)
            ang_impulse += torch.linalg.cross(bumper - c_sys, f) * env.step_dt
            base_com = robot.data.body_com_pos_w[:, 0]
            ang_impulse_com += torch.linalg.cross(base_com - c_sys, f) * env.step_dt
            env.step(zero)
            z_min = min(z_min, robot.data.root_link_pos_w[:, 2].min().item())
        res[on] = (momentum(env) - p0, impulse, z_min, ang_momentum(env) - l0, ang_impulse, ang_impulse_com)
        del term
        close(env)
    (dp_on, imp, z_on, dl_on, ang_imp, ang_com), (dp_off, _, _, dl_off, _, _) = res[True], res[False]
    dp = (dp_on - dp_off)[:, :2]
    imp = imp[:, :2]
    rel = (torch.linalg.norm(dp - imp, dim=-1) / torch.linalg.norm(imp, dim=-1).clamp(min=1e-6))
    cos = (dp * imp).sum(-1) / (torch.linalg.norm(dp, dim=-1) * torch.linalg.norm(imp, dim=-1)).clamp(min=1e-9)
    print(f"       applied impulse {torch.linalg.norm(imp, dim=-1).mean():.1f} N s, "
          f"momentum change {torch.linalg.norm(dp, dim=-1).mean():.1f} N s, "
          f"lowest base height {z_on:.2f} m")
    check(z_on > 0.6, "robot stayed airborne for the whole window (no ground contact)")
    check(bool((rel < 0.05).all()), f"momentum change = applied impulse (max rel err {rel.max():.1%})")
    check(bool((cos > 0.99).all()), f"same direction (min cosine {cos.min():.3f})")
    # Angular: if the force acted at the COM (or a fixed world point) this would not match.
    dl = dl_on - dl_off
    rel_l = torch.linalg.norm(dl - ang_imp, dim=-1) / torch.linalg.norm(ang_imp, dim=-1).clamp(min=1e-6)
    print(f"       expected angular impulse (force at bumper) {torch.linalg.norm(ang_imp, dim=-1).mean():.2f} N m s, "
          f"measured {torch.linalg.norm(dl, dim=-1).mean():.2f} N m s "
          f"(if it acted at the COM instead: {torch.linalg.norm(ang_com, dim=-1).mean():.2f})")
    check(bool((rel_l < 0.10).all()),
          f"angular momentum change matches a force acting at the bumper (max rel err {rel_l.max():.1%})")


# ---------------------------------------------------------------------------
def test_resets(task: str, device: str) -> None:
    from mjlab.utils.lab_api.math import quat_apply_inverse, yaw_quat

    print("\n[3] resets: partial reset of half the envs")
    n = 16
    def edit(cfg):
        pf = cfg.commands["push_force"]
        pf.gap_s = (0.5, 1.0)  # Training uses 0.5-2 s; the gap is what keeps a reset force-free.
        pf.ramp_s, pf.hold_s = (0.1, 0.2), (2.0, 3.0)
        pf.curriculum_start_scale = 1.0
        pf.warmup_env_steps = 0.0
        cfg.events.pop("push_robot", None)
        cfg.commands["twist"].p_override = 0.6
        cfg.commands["twist"].max_mass_override = 30.0
        cfg.commands["twist"].push_yaw_prob = 0.0

    from quadcoop.robots.objects import OBJECT_NAMES

    env = make_env(task, n, device, edit)
    robot = env.scene["robot"]
    objects = [env.scene[name] for name in OBJECT_NAMES]
    term = env.command_manager.get_term("push_force")
    zero = torch.zeros(env.action_space.shape, device=device)
    for _ in range(60):
        env.step(zero)
    on_before = torch.linalg.norm(term.applied_force_yaw, dim=-1)  # after 1.2 s
    check(bool((on_before > 0).any()), f"forces active before reset in {(on_before > 0).sum()}/{n} envs")

    ids = torch.arange(0, n, 2, device=device)
    keep = torch.arange(1, n, 2, device=device)
    len_keep_before = env.episode_length_buf[keep].clone()
    env.reset(env_ids=ids)
    env.step(zero)  # one real step: physics, command update, events

    check(bool((env.episode_length_buf[ids] == 1).all()), "reset envs restart their episode counter")
    check(bool((env.episode_length_buf[keep] == len_keep_before + 1).all()),
          "non-reset envs keep counting (not reset by accident)")
    f_after = torch.linalg.norm(term.applied_force_yaw[ids], dim=-1)
    xfrc = robot.data.body_external_wrench[ids].abs().max().item()
    check(bool((f_after == 0).all()) and xfrc == 0.0,
          "push force restarts at zero after reset (no force leaks across episodes)")
    jerr = (robot.data.joint_pos[ids] - robot.data.default_joint_pos[ids]).abs().max().item()
    check(jerr < 0.15, f"joints back at the standing pose (max dev {jerr:.3f} rad after 1 step)")
    q = yaw_quat(robot.data.root_link_quat_w[ids])
    yaw = 2.0 * torch.atan2(q[:, 3], q[:, 0])
    check(yaw.std().item() > 0.5, f"base yaw randomized across reset envs (std {yaw.std():.2f} rad)")
    dist = torch.stack([torch.linalg.norm(o.data.root_link_pos_w[ids, :2]
                                          - robot.data.root_link_pos_w[ids, :2], dim=-1)
                        for o in objects], dim=-1)  # (n_reset, K)
    near = dist < 2.5
    parked = dist > 20.0
    check(bool((near | parked).all()), "every object is either in front of the robot or parked")
    check(bool((near.sum(-1) <= 1).all()), "at most one object in front of each robot")
    choice = env.qc_choice[ids]
    match = torch.where(choice >= 0, near.gather(1, choice.clamp(min=0).unsqueeze(-1)).squeeze(-1),
                        ~near.any(-1))
    check(bool(match.all()), f"the object in front is the one chosen ({int((choice >= 0).sum())} "
          f"of {len(ids)} envs got one; shapes {sorted(set(choice[choice >= 0].tolist()))})")
    # The object sits on the line the command points along, and the command is held.
    tw = env.command_manager.get_term("twist")
    cmd = tw.vel_command_b[ids]
    rel = torch.stack([o.data.root_link_pos_w[ids] for o in objects], dim=1)
    rel = rel[torch.arange(len(ids)), choice.clamp(min=0)] - robot.data.root_link_pos_w[ids]
    rel_b = quat_apply_inverse(yaw_quat(robot.data.root_link_quat_w[ids]), rel)
    bearing = torch.atan2(rel_b[:, 1], rel_b[:, 0])
    heading_cmd = torch.atan2(cmd[:, 1], cmd[:, 0])
    diff = torch.atan2(torch.sin(bearing - heading_cmd), torch.cos(bearing - heading_cmd)).abs()
    has = choice >= 0
    check(bool(has.any()) and float(diff[has].max()) < 0.8,
          f"command points at the object (max bearing error {float(diff[has].max()):.2f} rad)")
    check(bool((tw.time_left[ids][has] > 3.0).all()), "command is held for the push (>3 s left)")
    check(bool((cmd[has, 2] == 0).all()), "no turning commanded while pushing")
    gap = dist.min(-1).values[near.any(-1)]
    if gap.numel():
        check(bool((gap > 0.85).all()), f"objects start clear of the body (closest {gap.min():.2f} m)")
    close(env)


# ---------------------------------------------------------------------------
def test_randomization(task: str, device: str) -> None:
    from mjlab.tasks.registry import load_env_cfg

    print("\n[4] domain randomization: per-env values")
    n = 64
    env = make_env(task, n, device)
    cfg = load_env_cfg(task)
    from quadcoop.robots.objects import OBJECT_NAMES

    robot = env.scene["robot"]
    model = env.sim.model

    feet_local, _ = robot.find_geoms(cfg.events["foot_friction"].params["asset_cfg"].geom_names,
                                     preserve_order=True)
    feet = robot.indexing.geom_ids[feet_local]
    fr = model.geom_friction[:, feet, 0]  # (n, nfeet)
    lo, hi = cfg.events["foot_friction"].params["ranges"]
    check(bool(((fr >= lo - 1e-6) & (fr <= hi + 1e-6)).all()),
          f"foot friction in [{lo}, {hi}] (got {fr.min():.2f}-{fr.max():.2f})")
    check(fr[:, 0].std().item() > 0.1, f"foot friction differs across envs (std {fr[:, 0].std():.2f})")
    check((fr - fr[:, :1]).abs().max().item() < 1e-6, "all feet of one robot share a friction value")

    base_local = robot.find_bodies(cfg.events["base_com"].params["asset_cfg"].body_names)[0][0]
    base = robot.indexing.body_ids[base_local]
    ipos = model.body_ipos[:, base]
    nominal = torch.as_tensor(env.sim.mj_model.body_ipos[int(base)], device=ipos.device, dtype=ipos.dtype)
    off = ipos - nominal
    ranges = cfg.events["base_com"].params["ranges"]
    ok = all(bool(((off[:, a] >= r[0] - 1e-5) & (off[:, a] <= r[1] + 1e-5)).all()) for a, r in ranges.items())
    check(ok and off.std(0).max().item() > 1e-3,
          f"base COM offset randomized within ranges (x std {off[:, 0].std() * 100:.1f} cm)")

    for name in OBJECT_NAMES:
        m = model.body_mass[:, env.scene[name].indexing.body_ids[0]]
        check(bool(((m > 2.9) & (m < 30.5)).all()) and m.std().item() > 1.0,
              f"{name} mass randomized in 3-30 kg (got {m.min():.1f}-{m.max():.1f}, std {m.std():.1f})")
        gid = env.scene[name].indexing.geom_ids[0]
        mu = env.sim.model.geom_friction[:, gid, 0].cpu()
        prio = int(env.sim.mj_model.geom_priority[int(gid)])
        check(bool(((mu >= 0.3 - 1e-6) & (mu <= 0.6 + 1e-6)).all()) and mu.std() > 0.01 and prio > 1,
              f"  friction {mu.min():.2f}-{mu.max():.2f}, contact priority {prio} (object friction governs)")

    bias = robot.data.encoder_bias
    check(bias.abs().max().item() <= 0.015 + 1e-6 and bias.std().item() > 1e-4,
          f"encoder bias randomized within +/-0.015 rad (std {bias.std():.4f})")

    ev = env.event_manager.active_terms
    interval = ev.get("interval", []) if isinstance(ev, dict) else []
    check("push_robot" in interval, f"interval events scheduled: {interval}")
    close(env)

# ---------------------------------------------------------------------------
def test_curriculum(task: str, device: str) -> None:
    """Drive the schedule by setting the env's step counter, and feed the object
    curriculum synthetic episode outcomes, exactly as it sees them at resets."""
    from mjlab.tasks.registry import load_env_cfg

    from quadcoop.mdp.object_events import STEPS_PER_ITER, object_curriculum

    print("\n[5] curriculum: warm-up, force ramp, object ramp, competence-gated mass")
    cfg = load_env_cfg(task)
    env = make_env(task, 64, device)
    term = env.command_manager.get_term("push_force")
    pf = cfg.commands["push_force"]
    oc = dict(cfg.curriculum["objects"].params)
    warm = oc["warmup_iters"]
    push_iters = pf.curriculum_env_steps / STEPS_PER_ITER

    def at(it):
        env.common_step_counter = int(it * STEPS_PER_ITER)

    at(warm - 1)
    s0 = term._curriculum_scale()  # noqa: SLF001
    at(warm)
    s1 = term._curriculum_scale()  # noqa: SLF001
    at(warm + push_iters)
    s2 = term._curriculum_scale()  # noqa: SLF001
    check(s0 == 0.0 and abs(s1 - pf.curriculum_start_scale) < 1e-6 and abs(s2 - 1.0) < 1e-6,
          f"force scale: {s0:.2f} in warm-up, {s1:.2f} right after, {s2:.2f} at +{push_iters:.0f} it")

    if hasattr(env, "qc_objects"):
        del env.qc_objects
    ids = torch.arange(64, device=device)
    mm = env.metrics_manager
    tm = env.termination_manager

    def episodes(contact: float, fell: bool, err: float):
        mm._step_count[:] = 500  # noqa: SLF001
        mm._episode_sums["object_contact"][:] = contact * 500  # noqa: SLF001
        mm._episode_sums["vel_error_xy"][:] = err * 500  # noqa: SLF001
        tm._terminated_buf[:] = fell  # noqa: SLF001  (what object_curriculum reads)

    episodes(0.3, False, 0.1)
    at(warm - 10)
    out = object_curriculum(env, ids, **oc)
    p_warm, m_warm = float(out["p_place"]), float(out["max_mass"])
    at(warm + oc["ramp_iters"] / 2)
    p_mid = float(object_curriculum(env, ids, **oc)["p_place"])
    at(warm + oc["ramp_iters"])
    p_end = float(object_curriculum(env, ids, **oc)["p_place"])
    check(p_warm == 0.0 and abs(p_mid - oc["p_max"] / 2) < 0.02 and abs(p_end - oc["p_max"]) < 1e-6,
          f"object placement prob: {p_warm:.2f} in warm-up, {p_mid:.2f} mid-ramp, {p_end:.2f} at end")

    # Good engaged episodes -> mass cap rises (one step per dwell window).
    m = [m_warm]
    for k in range(1, 6):
        at(warm + oc["ramp_iters"] + 60 * k)
        for _ in range(5):
            out = object_curriculum(env, ids, **oc)
        m.append(float(out["max_mass"]))
    check(m[-1] > m[0], f"mass cap rises with success: {' -> '.join(f'{x:.0f}' for x in m)} kg")
    # Falling engaged episodes -> it comes back down.
    episodes(0.3, True, 0.1)
    for k in range(6, 9):
        at(warm + oc["ramp_iters"] + 60 * k)
        for _ in range(20):
            out = object_curriculum(env, ids, **oc)
        m.append(float(out["max_mass"]))
    check(m[-1] < m[5], f"and drops when robots fall: {' -> '.join(f'{x:.0f}' for x in m[5:])} kg")
    # Episodes with no object contact don't move it.
    episodes(0.0, True, 2.0)
    before = m[-1]
    at(warm + oc["ramp_iters"] + 60 * 12)
    for _ in range(20):
        out = object_curriculum(env, ids, **oc)
    check(float(out["max_mass"]) == before, "episodes without object contact don't move the mass cap")
    close(env)


def test_push_hold(task: str, device: str) -> None:
    """Push episodes: the command never changes, and a passed object is replaced ahead."""
    from mjlab.utils.lab_api.math import quat_apply_inverse, yaw_quat

    from quadcoop.robots.objects import OBJECT_NAMES

    print("\n[6] push episodes: fixed command, objects keep coming on the same line")
    n = 8

    def edit(cfg):
        tw = cfg.commands["twist"]
        tw.p_override, tw.max_mass_override, tw.p_free_walk = 1.0, 30.0, 0.0
        tw.push_yaw_prob = 0.0
        cfg.events.pop("push_robot", None)
        cfg.commands.pop("push_force", None)
        cfg.observations["critic"].terms.pop("push_force", None)

    env = make_env(task, n, device, edit)
    objects = [env.scene[k] for k in OBJECT_NAMES]
    robot = env.scene["robot"]
    tw = env.command_manager.get_term("twist")
    zero = torch.zeros(env.action_space.shape, device=device)
    cmd0 = tw.vel_command_b.clone()
    check(bool(tw.push_mode.all()), "every env is in a push episode")
    b = tw.bearing
    check(float(b.std()) > 0.5, f"push directions span the circle (bearings {[round(float(x)) for x in torch.rad2deg(b)]} deg)")
    check(bool((cmd0[:, 2] == 0).all()), "no turning in push episodes")
    for _ in range(200):  # 4 s, longer than any free-walk segment
        env.step(zero)
    check(torch.allclose(tw.vel_command_b, cmd0), "command unchanged after 4 s")

    def chosen_rel():
        p = torch.stack([o.data.root_link_pos_w for o in objects], dim=1)
        rel = p[torch.arange(n), env.qc_choice.clamp(min=0)] - robot.data.root_link_pos_w
        rel_b = quat_apply_inverse(yaw_quat(robot.data.root_link_quat_w), rel)
        u = torch.stack([torch.cos(tw.bearing), torch.sin(tw.bearing)], -1)
        return (rel_b[:, :2] * u).sum(-1)

    check(bool((env.qc_choice >= 0).all()) and bool((chosen_rel() > 0).all()),
          "every env has an object ahead on its line")
    # Move each object 2 m behind its robot: it has been "passed".
    old = env.qc_choice.clone()
    for k, o in enumerate(objects):
        ids = (env.qc_choice == k).nonzero().flatten()
        if len(ids) == 0:
            continue
        st = torch.zeros(len(ids), 13, device=device)
        back = torch.stack([-torch.cos(tw.bearing[ids]), -torch.sin(tw.bearing[ids]),
                            torch.zeros(len(ids), device=device)], -1)
        from mjlab.utils.lab_api.math import quat_apply
        st[:, :3] = robot.data.root_link_pos_w[ids] + 2.0 * quat_apply(
            yaw_quat(robot.data.root_link_quat_w[ids]), back)
        st[:, 2] = 0.5
        st[:, 3] = 1.0
        o.write_root_state_to_sim(st, ids)
    env.step(zero)  # the command term notices and places a new object (end of this step)
    env.step(zero)  # positions are read after the next physics step
    ahead = chosen_rel()
    check(bool((env.qc_choice >= 0).all()) and bool((ahead > 0.5).all()),
          f"a passed object is replaced ahead on the same line (closest {float(ahead.min()):.2f} m ahead)")
    print(f"       objects before/after: {old.tolist()} -> {env.qc_choice.tolist()}")
    close(env)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", default=None, help="default: both walkers")
    ap.add_argument("--device", default=None)
    ap.add_argument("--tests", default="123456", help="subset to run, e.g. 13")
    args = ap.parse_args()
    device = args.device or ("cuda:0" if torch.cuda.is_available() else "cpu")

    import quadcoop

    tasks = [args.task] if args.task else list(quadcoop.TASKS)
    for task in tasks:
        print(f"\n===== {task}  (device {device}) =====")
        if "1" in args.tests:
            test_routing(task, device, steps=60)
        if "2" in args.tests:
            test_effect(task, device)
        if "3" in args.tests:
            test_resets(task, device)
        if "4" in args.tests:
            test_randomization(task, device)
        if "5" in args.tests:
            test_curriculum(task, device)
        if "6" in args.tests:
            test_push_hold(task, device)

    print()
    if FAILS:
        print(f"FAILED ({len(FAILS)}):")
        for f in FAILS:
            print(f"  - {f}")
        return 1
    print("All disturbance/reset/randomization checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())