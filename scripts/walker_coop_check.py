"""Integration check: a compliant walker (v2 / v2.1 / v2.2 / v22k) inside the two-robot environment.
Measurement only; nothing is trained. Run it before any downstream comparison with a new walker.

1. Inputs. For each robot: the walker's input group in the two-robot env has the same terms in the
   same order and sizes as the walker's training config (actor group), its size matches the
   checkpoint's first layer, and the checkpoint's input normalizer is finite with positive spread.
   The contact-force input reads this robot's push_<robot> sensor (objects only), robot frame, / 200 N,
   nothing synthetic added.
2. Force wiring, numerically. The two force inputs (x, y) x 200 N are compared, as a vector, with
   an independent recomputation: CPU MuJoCo on the same state (the env's per-world model fields
   copied in), summing mj_contactForce over every contact between this robot's bodies and the object
   bodies, rotated into the robot's yaw frame. Same comparison in the walker's own training env
   (one robot pressing a cube), so both sides are checked against the same formula. Physical sign:
   a robot pressing an object ahead of it must feel a force pointing backward (x < 0).
   Both are taken at the same instant: the simulation is re-evaluated at the current state (no
   integration) before reading the input, so only CPU vs GPU solver differences remain; agreement
   is reported, not assumed.
   To get contact whatever the walker does, one scenario also pushes the cube into a standing robot
   (600 N on the 80 kg cube, more than its ~350 N sliding friction, toward the robot), in both envs. The comparison uses the input term's value
   before observation noise; the walker group's noise (the walker was trained with +-0.02 = +-4 N
   per component on this input) is reported separately.
3. Exclusions. Robot B walks sideways into robot A (both away from the object): A's force input must
   stay ~0 while the robots touch. A robot standing alone: ~0 (feet on the ground are not in it).
4. Smoke run, with the walker driving: robot A presses the cube face (80 kg) at 0.2 m/s for 4 s,
   stops 2 s, presses 3 s. Recorded, not assumed: falls, time touching, force, inputs finite and
   within the clip (+-2.5), force-input z-scores under the checkpoint's normalizer.

    QUADCOOP_WALKER_OVERRIDE_ANYMAL_C=<v22 model.pt> python scripts/walker_coop_check.py --name wiring-v22
    python scripts/walker_coop_check.py --walker <model.pt> --name wiring-v22      # same thing

Output: evals/<name>/summary.md, summary.json.
"""

from __future__ import annotations

import argparse
import copy
import json
import math
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

FELL_Z = 0.25
TOUCH_N = 5.0
F_REF = 200.0
AGREE_N = 10.0  # |difference| below this (N), or
AGREE_REL = 0.15  # within this fraction of the force, counts as agreeing
WINDOW = 10  # samples per block for the averaged comparison (with --every 1: 0.2 s)
PUSH_N = 600.0  # N on the 80 kg cube (sliding friction ~350 N) to drive it into a standing robot


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--walker", default="", help="compliant ANYmal walker checkpoint (else QUADCOOP_WALKER_OVERRIDE_ANYMAL_C)")
    ap.add_argument("--name", default="wiring-check")
    ap.add_argument("--reps", type=int, default=4, help="environments per scenario")
    ap.add_argument("--every", type=int, default=1, help="recompute the force every so many steps")
    ap.add_argument("--device", default=None)
    a = ap.parse_args()
    if a.walker:
        os.environ["QUADCOOP_WALKER_OVERRIDE_ANYMAL_C"] = str(Path(a.walker).resolve())
    if not os.environ.get("QUADCOOP_WALKER_OVERRIDE_ANYMAL_C"):
        raise SystemExit("give --walker <compliant walker model.pt> (or QUADCOOP_WALKER_OVERRIDE_ANYMAL_C)")

    from train_coop2 import resolve_models, set_env

    models = resolve_models("b", "anymal")
    set_env(models)
    import torch

    import quadcoop  # noqa: F401
    from quadcoop.coop2.env_cfg import walker_kind

    kind = walker_kind("anymal_c")
    print(f"walker {os.environ['QUADCOOP_WALKER_CKPT_ANYMAL_C']} -> kind {kind}", flush=True)
    if kind != "compliant":
        raise SystemExit("this walker is not a compliant walker (no contact-force input): nothing to check")
    device = a.device or ("cuda:0" if torch.cuda.is_available() else "cpu")
    res = {"walker": os.environ["QUADCOOP_WALKER_CKPT_ANYMAL_C"], "kind": kind}
    res["walker_env"] = check_walker_env(a, device)
    res.update(check_coop(a, device))
    md = report(res, a)
    out = ROOT / "evals" / a.name
    out.mkdir(parents=True, exist_ok=True)
    (out / "summary.md").write_text("\n".join(md) + "\n")
    (out / "summary.json").write_text(json.dumps(res, indent=1, default=float))
    print("\n".join(md))
    print(f"\nwrote {out}/")
    return 0


# -- independent force: CPU MuJoCo on a copy of env j's state -------------------------------------------
class ForceRecompute:
    def __init__(self, env, robot_name: str, object_bodies: list[str]):
        import mujoco

        self.mj = mujoco
        self.env = env
        self.m = copy.deepcopy(env.sim.mj_model)
        self.d = mujoco.MjData(self.m)
        rob = env.scene[robot_name]
        ids = [int(i) for i in rob.indexing.body_ids.flatten().tolist()]
        self.robot_bodies = set(ids)
        self.obj_bodies = {self.m.body(nm).id for nm in object_bodies if self._has_body(nm)}
        self.synced = None
        self.missing = set()  # state fields that could not be copied (reported)

    def _has_body(self, nm):
        try:
            self.m.body(nm)
            return True
        except KeyError:
            return False

    def _sync(self, j):
        if self.synced == j:
            return
        from mjlab.viewer.model_sync import sync_model_fields

        for f in self.env.sim.expanded_fields:
            try:
                sync_model_fields(self.m, self.env.sim.model, frozenset({f}), j)
            except Exception:  # noqa: BLE001  a field the helper cannot copy: keep the template value
                pass
        self.synced = j

    def __call__(self, j: int, yaw: float):
        import numpy as np

        self._sync(j)
        sd = self.env.sim.data
        for f in ("qpos", "qvel", "ctrl", "act", "xfrc_applied", "qacc_warmstart", "mocap_pos", "mocap_quat"):
            dst = getattr(self.d, f)
            if dst.size == 0:
                continue
            try:
                src = getattr(sd, f)
                dst[:] = src[j].detach().cpu().numpy().reshape(dst.shape)
            except Exception:  # noqa: BLE001
                try:  # warp vector types: through numpy
                    import numpy as np

                    raw = getattr(object.__getattribute__(sd, "_struct"), f)
                    dst[:] = np.asarray(raw.numpy())[j].reshape(dst.shape)
                except Exception:  # noqa: BLE001
                    self.missing.add(f)
        self.mj.mj_forward(self.m, self.d)
        f = np.zeros(3)
        c6 = np.zeros(6)
        for i in range(self.d.ncon):
            c = self.d.contact[i]
            b1, b2 = int(self.m.geom_bodyid[c.geom1]), int(self.m.geom_bodyid[c.geom2])
            if b1 in self.robot_bodies and b2 in self.obj_bodies:
                sgn = -1.0  # force on geom2 (the object) is +; on the robot (geom1) -
            elif b2 in self.robot_bodies and b1 in self.obj_bodies:
                sgn = 1.0
            else:
                continue
            self.mj.mj_contactForce(self.m, self.d, i, c6)
            f += sgn * (c.frame.reshape(3, 3).T @ c6[:3])
        cy, sy = math.cos(yaw), math.sin(yaw)
        fb = np.array([cy * f[0] + sy * f[1], -sy * f[0] + cy * f[1]])  # on the robot, yaw frame, N
        return np.clip(fb, -2.5 * F_REF, 2.5 * F_REF)  # the input is clipped at +-2.5 (x 200 N): compare like with like


def same_instant(env, sensor_names) -> None:
    """Re-evaluate the simulation at the current state (no integration) and refresh these sensors, so
    the sensor and the CPU recomputation describe the same instant (after a step the sensor holds the
    last substep's contacts, one substep before the current state)."""
    env.sim.forward()
    for nm in sensor_names:
        env.scene[nm].update(0.0)


def agreement(series, window: int = 1):
    """series: {env: [(input vector N, recomputed vector N), ...] in time order}. With window > 1, each env's
    sequence is first averaged over consecutive blocks of `window` samples (the sensor reads the last
    substep's contacts, the recomputation the state after it: per step they are one substep apart, which
    matters while contact is changing fast). Stats over the samples with force > TOUCH_N."""
    import numpy as np

    pairs = []
    for seq in series.values():
        for k in range(0, len(seq) - window + 1, window):
            blk = seq[k:k + window]
            pairs.append((np.mean([b[0] for b in blk], 0), np.mean([b[1] for b in blk], 0)))
    rows = [(np.asarray(o), np.asarray(r)) for o, r in pairs if max(np.linalg.norm(o), np.linalg.norm(r)) > TOUCH_N]
    if not rows:
        return {"samples": 0}
    diff = [float(np.linalg.norm(o - r)) for o, r in rows]
    mag = [float(max(np.linalg.norm(o), np.linalg.norm(r))) for o, r in rows]
    ok = [d <= max(AGREE_N, AGREE_REL * m) for d, m in zip(diff, mag)]
    cos = [float(o @ r / max(1e-9, np.linalg.norm(o) * np.linalg.norm(r))) for o, r in rows]
    both = [(o, r) for o, r in rows if np.linalg.norm(r) > TOUCH_N and np.linalg.norm(o) > TOUCH_N]
    scale = [float(o @ r / (r @ r)) for o, r in both]  # input along the recomputed force, / its size
    return {"samples": len(rows), "agree_frac": sum(ok) / len(ok), "median_diff_N": float(np.median(diff)),
            "p90_diff_N": float(np.percentile(diff, 90)), "median_force_N": float(np.median(mag)),
            "median_cos": float(np.median(cos)), "min_cos": float(min(cos)),
            "median_scale": float(np.median(scale)) if scale else float("nan"),
            "median_angle_deg": float(np.degrees(np.median([math.acos(max(-1.0, min(1.0, c))) for c in cos]))),
            "mean_input_x_N": float(np.mean([o[0] for o, _ in rows])), "mean_recomputed_x_N": float(np.mean([r[0] for _, r in rows])),
            "examples": [[round(float(x), 1) for x in (*o, *r)] for o, r in rows[:: max(1, len(rows) // 5)][:5]]}


def obs_slice(env, group, term):
    """Column range of `term` within observation group `group`."""
    om = env.observation_manager
    names = om.active_terms[group]
    dims = om.group_obs_term_dim[group]
    start = 0
    for nm, d in zip(names, dims):
        size = int(math.prod(d))
        if nm == term:
            return start, start + size
        start += size
    raise KeyError(term)


# -- 2 (walker side): the walker's own training env ------------------------------------------------------
def check_walker_env(a, device):
    import torch
    from mjlab.envs import ManagerBasedRlEnv

    from quadcoop.robots.anymal_c import ROBOT
    from quadcoop.robots.objects import NOMINAL_MASS, OBJECT_NAMES, OBJECTS
    from quadcoop.stage1.walker_policy import FrozenWalker
    from quadcoop.walker_env_cfg import make_walker_env_cfg

    cfg = make_walker_env_cfg(ROBOT, play=True, compliant=True)
    n = a.reps
    cfg.scene.num_envs = n
    cfg.terminations = {}
    cfg.episode_length_s = 1e6
    alpha = 0.5 * math.log(80.0 / NOMINAL_MASS)
    for nm in OBJECT_NAMES:
        cfg.events[f"{nm}_mass"].params["alpha_range"] = (alpha, alpha)
    tw = cfg.commands["twist"]
    tw.sample_from_ranges = True
    tw.resampling_time_range = (1e9, 1e9)
    tw.rel_standing_envs = 0.0
    torch.manual_seed(0)
    env = ManagerBasedRlEnv(cfg=cfg, device=device)
    pol = FrozenWalker(os.environ["QUADCOOP_WALKER_CKPT_ANYMAL_C"], device)
    obs, _ = env.reset()
    robot = env.scene["robot"]
    twc = env.command_manager.get_term("twist")
    cube = OBJECTS[0]
    lo, hi = obs_slice(env, "actor", "bumper_force")
    tcfg_w = env.observation_manager.get_term_cfg("actor", "bumper_force")

    def yaw():
        q = robot.data.root_link_quat_w
        return torch.atan2(2 * (q[:, 0] * q[:, 3] + q[:, 1] * q[:, 2]), 1 - 2 * (q[:, 2] ** 2 + q[:, 3] ** 2))

    def go(v, steps):
        nonlocal obs
        out = []
        for i in range(steps):
            twc.vel_command_b[:] = torch.tensor([v, 0.0, 0.0], device=env.device)
            twc.is_standing_env[:] = False
            obs, *_ = env.step(pol(obs["actor"]))
            if i % a.every == 0:
                out.append(i)
                same_instant(env, ["bumper_force"])
                o = tcfg_w.func(env, **tcfg_w.params) * F_REF
                y = yaw()
                for j in range(n):
                    pairs.setdefault(j, []).append((o[j].cpu().numpy(), rc(j, float(y[j]))))
        return out

    pairs = {}
    rc = ForceRecompute(env, "robot", [f"{o}/body" for o in OBJECT_NAMES])
    for _ in range(50):
        twc.vel_command_b[:] = 0.0
        obs, *_ = env.step(pol(obs["actor"]))
    y = yaw()
    fwd = torch.stack([torch.cos(y), torch.sin(y)], -1)
    st = torch.zeros(n, 13, device=env.device)
    st[:, :2] = robot.data.root_link_pos_w[:, :2] + fwd * (ROBOT.half_length + cube.half_extent_x + 0.05)
    st[:, 2] = cube.half_height + 0.005
    st[:, 3:7] = torch.stack([torch.cos(y / 2), 0 * y, 0 * y, torch.sin(y / 2)], -1)
    env.scene[cube.name].write_root_state_to_sim(st)
    go(0.2, int(3.0 / env.step_dt))
    go(0.0, int(0.5 / env.step_dt))
    y = yaw()  # the cube pushed into the standing robot: contact whatever the walker does
    push = torch.zeros(n, 1, 3, device=env.device)
    push[:, 0, 0] = -PUSH_N * torch.cos(y)
    push[:, 0, 1] = -PUSH_N * torch.sin(y)
    env.scene[cube.name].write_external_wrench_to_sim(push, torch.zeros_like(push))
    go(0.0, int(2.0 / env.step_dt))
    out = {"state_fields_not_copied": sorted(rc.missing), "order": list(env.observation_manager.active_terms["actor"]),
           "dims": [int(math.prod(d)) for d in env.observation_manager.group_obs_term_dim["actor"]],
           "agreement": agreement(pairs), "agreement_window": agreement(pairs, WINDOW),
           "fell": int((robot.data.root_link_pos_w[:, 2] < FELL_Z).sum())}
    env.close() if hasattr(env, "close") else None
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    return out


# -- 1, 2 (two-robot side), 3, 4 ---------------------------------------------------------------------------
def check_coop(a, device):
    import numpy as np
    import torch
    from mjlab.envs import ManagerBasedRlEnv

    from quadcoop import contacts as C
    from quadcoop.coop2.env_cfg import AGENTS, FRICTION_RANGE, make_coop2_env_cfg
    from quadcoop.robots.anymal_c import ROBOT
    from quadcoop.stage1b.shapes import NOMINAL_MASS
    from quadcoop.stage2 import mdp as m2
    from quadcoop.stage2.shapes import OBJ_NAMES2, SHAPE_NAMES2, kinds_tensor, nominal_parts
    from quadcoop.walker_env_cfg import make_walker_env_cfg

    A, B = AGENTS
    scen = ["press"] * a.reps + ["pushed"] * a.reps + ["partner"] * a.reps + ["alone"] * a.reps
    n = len(scen)
    cfg = make_coop2_env_cfg("b", play=True, partner_map=True, reward_set="r7", contacts=True, guide=True,
                             wrench=True, expert=True, push_cmd=True, reselect_s=(0.0, 0.0), reselect_min_dist=0.0)
    cfg.scene.num_envs = n
    cfg.episode_length_s = 1e5
    cfg.terminations = {}
    alpha = 0.5 * math.log(80.0 / NOMINAL_MASS)
    mid = 0.5 * (FRICTION_RANGE[0] + FRICTION_RANGE[1])
    for nm in OBJ_NAMES2:
        cfg.events[f"{nm}_mass"].params["alpha_range"] = (alpha, alpha)
        if f"{nm}_friction" in cfg.events:
            cfg.events[f"{nm}_friction"].params["ranges"] = (mid, mid)
    torch.manual_seed(0)
    env = ManagerBasedRlEnv(cfg=cfg, device=device)
    dev = env.device
    g = env.command_manager.get_term("goal")
    s_cube = SHAPE_NAMES2.index("cube")
    parts, rest = nominal_parts("cpu")
    cl = C.candidates(parts[s_cube].numpy(), kinds_tensor("cpu")[s_cube].numpy(), float(rest[s_cube]))
    face = min(cl, key=lambda c: np.linalg.norm(np.asarray(c.n) - np.array([-1.0, 0.0])) + abs(c.p[1]))
    px = float(face.p[0])
    ar = torch.arange(n, device=dev)
    for k in range(len(SHAPE_NAMES2)):
        m2.apply_geometry(env, ar, k, torch.ones(n, 3, device=dev))
    z = torch.zeros(n, device=dev)
    park_b = torch.tensor([s != "partner" for s in scen], device=dev)
    sc = {"shape": torch.full((n,), s_cube, dtype=torch.long, device=dev), "obj_xy_rel": torch.zeros(n, 2, device=dev),
          "obj_heading": z.clone(), "goal_xy_rel": torch.stack([z + 3.0, z], -1), "goal_yaw": z.clone(),
          "bearings": [z + math.pi, z + math.pi / 2], "gaps": [z + 0.6, z + 0.6], "yaw_noise": [z, z],
          "park": [torch.zeros(n, dtype=torch.bool, device=dev), park_b],
          "contact_rule": torch.full((n,), 3, dtype=torch.long, device=dev),
          "contact_idx": torch.full((n, 2), -1, dtype=torch.long, device=dev)}
    g.scenario = lambda ids: {k: ([x[ids] for x in v] if isinstance(v, list) else v[ids]) for k, v in sc.items()}
    env.reset()
    g.scenario = None

    # -- 1. inputs ----------------------------------------------------------------------------------
    res = {"inputs": {}}
    train_terms = [t for t in make_walker_env_cfg(ROBOT, compliant=True).observations["actor"].terms if t != "height_scan"]
    for r in (A, B):
        grp = f"walker_{r}"
        term = env.action_manager.get_term(grp)
        names = list(env.observation_manager.active_terms[grp])
        dims = [int(math.prod(d)) for d in env.observation_manager.group_obs_term_dim[grp]]
        cfg_t = env.observation_manager._group_obs_term_cfgs[grp][names.index("bumper_force")] \
            if hasattr(env.observation_manager, "_group_obs_term_cfgs") else None
        w = term.walker
        res["inputs"][r] = {
            "order_coop": names, "dims_coop": dims, "order_training": train_terms,
            "same_order": names == train_terms, "size": sum(dims), "checkpoint_inputs": w.obs_dim,
            "size_ok": sum(dims) == w.obs_dim,
            "normalizer_finite": bool(torch.isfinite(w.mean).all() and torch.isfinite(w.std).all()),
            "normalizer_std_positive": bool((w.std > 0).all()),
            "force_normalizer_mean": [round(float(x), 4) for x in w.mean.reshape(-1)[-2:]],
            "force_normalizer_std": [round(float(x), 4) for x in w.std.reshape(-1)[-2:]],
            "force_params": {k: (v if isinstance(v, (str, int, float, type(None))) else str(v))
                             for k, v in (cfg_t.params.items() if cfg_t is not None else [])},
        }

    # placements: A's front 5 cm short of the cube face (press) / 1.8 m short (partner, alone);
    # partner scenario: B 0.75 m to A's left, facing the same way, walking right into A
    robA, robB = env.scene[A], env.scene[B]
    reach = float(g.reach[A])
    obj0 = g.box_pos()[:, :2].clone()
    back = torch.tensor([0.05 if s in ("press", "pushed") else 1.8 for s in scen], device=dev)
    tip = obj0 + torch.stack([z + px, z], -1) - torch.stack([back, z], -1)
    ctr = tip - reach * torch.stack([z + 1.0, z], -1)
    pose = robA.data.root_link_pose_w.clone()
    pose[:, 0:2] = ctr
    pose[:, 3:7] = torch.stack([z + 1.0, z, z, z], -1)
    robA.write_root_link_pose_to_sim(pose)
    robA.write_root_link_velocity_to_sim(torch.zeros(n, 6, device=dev))
    pb = robB.data.root_link_pose_w.clone()
    part = torch.tensor([s == "partner" for s in scen], device=dev)
    pb[part, 0:2] = ctr[part] + torch.tensor([0.0, 0.75], device=dev)
    pb[part, 3:7] = torch.tensor([1.0, 0.0, 0.0, 0.0], device=dev)
    robB.write_root_link_pose_to_sim(pb)
    robB.write_root_link_velocity_to_sim(torch.zeros(n, 6, device=dev))

    lo_ = torch.tensor([-0.6, -0.5, -0.7], device=dev)
    hi_ = torch.tensor([0.8, 0.5, 0.7], device=dev)

    def act(twa, twb):
        x = torch.zeros(n, env.action_manager.total_action_dim, device=dev)
        x[:, 0:3] = 2.0 * (twa - lo_) / (hi_ - lo_) - 1.0
        x[:, 3:6] = 2.0 * (twb - lo_) / (hi_ - lo_) - 1.0
        return x

    is_press = torch.tensor([s == "press" for s in scen], device=dev)
    pushed = torch.tensor([s == "pushed" for s in scen], device=dev)
    cube_ent = env.scene["obj_cube"]
    wf = torch.zeros(n, 1, 3, device=dev)
    wf[pushed, 0, 0] = -PUSH_N  # the cube's -x face is toward robot A
    cube_ent.write_external_wrench_to_sim(wf, torch.zeros_like(wf))
    tcfg = env.observation_manager.get_term_cfg(f"walker_{A}", "bumper_force")
    noise_max = 0.0
    rcA = ForceRecompute(env, A, [f"{o}/body" for o in OBJ_NAMES2])
    lo, hi = obs_slice(env, f"walker_{A}", "bumper_force")
    w = env.action_manager.get_term(f"walker_{A}").walker
    dt = env.step_dt
    plan = [(0.0, 0.4, "settle"), (0.2, 4.0, "press"), (0.0, 2.0, "stop"), (0.2, 3.0, "press_again")]
    pairs = {s: {} for s in ("press", "pushed", "partner", "alone")}
    excl = {"partner_touching_steps": 0, "partner_max_input_N": 0.0, "alone_max_input_N": 0.0}
    smoke = {"steps": 0, "nonfinite": 0, "clipped_frac": 0.0, "max_abs_z": 0.0, "touch": {}, "force": {}, "fell": 0}
    fell = torch.zeros(n, dtype=torch.bool, device=dev)
    clipped = 0
    total = 0
    step_i = 0
    for v, secs, phase in plan:
        tA = torch.zeros(n, 3, device=dev)
        tA[:, 0] = torch.where(is_press, torch.full_like(z, v), z)
        tB = torch.zeros(n, 3, device=dev)
        tB[:, 1] = torch.where(part, torch.full_like(z, -0.15), z)  # walk right, into A
        touch_acc, force_acc, cnt = torch.zeros(n, device=dev), torch.zeros(n, device=dev), 0
        for _ in range(int(round(secs / dt))):
            env.step(act(tA, tB))
            step_i += 1
            ob = env.observation_manager.compute_group(f"walker_{A}")
            noise_max = max(noise_max, float((ob[:, lo:hi] - tcfg.func(env, **tcfg.params)).abs().max()) * F_REF)
            same_instant(env, [f"push_{A}"])
            fin = tcfg.func(env, **tcfg.params)  # the input before observation noise, at the current state
            smoke["nonfinite"] += int((~torch.isfinite(ob)).any(-1).sum())
            clipped += int((fin.abs() >= 2.5 - 1e-6).any(-1).sum())
            total += n
            zsc = ((fin - w.mean.reshape(-1)[lo:hi]) / (w.std.reshape(-1)[lo:hi] + 1e-8)).abs().max()
            smoke["max_abs_z"] = max(smoke["max_abs_z"], float(zsc))
            fell |= robA.data.root_link_pos_w[:, 2] < FELL_Z
            fN = fin * F_REF
            mag = torch.linalg.norm(fN, dim=-1)
            touch_acc += (mag > TOUCH_N).float()
            force_acc += -fN[:, 0]
            cnt += 1
            rt = env.scene["robots_touch"].data.found
            rt = (rt > 0).reshape(n, -1).any(-1)
            for j in range(n):
                if scen[j] == "partner" and bool(rt[j]):
                    excl["partner_touching_steps"] += 1
                    excl["partner_max_input_N"] = max(excl["partner_max_input_N"], float(mag[j]))
                if scen[j] == "alone":
                    excl["alone_max_input_N"] = max(excl["alone_max_input_N"], float(mag[j]))
            if step_i % a.every == 0:
                yA = g.robot_yaw(0)
                for j in range(n):
                    pairs[scen[j]].setdefault(j, []).append((fN[j].cpu().numpy(), rcA(j, float(yA[j]))))
        if phase != "settle":
            smoke["touch"][phase] = round(float(touch_acc[is_press].mean()) / max(cnt, 1), 3)
            smoke["force"][phase] = round(float(force_acc[is_press].mean()) / max(cnt, 1), 1)
    smoke["steps"] = step_i
    smoke["clipped_frac"] = clipped / max(total, 1)
    smoke["fell"] = int(fell.sum())
    smoke["fell_press"] = int(fell[is_press].sum())
    res["agreement"] = {s: agreement(p) for s, p in pairs.items()}
    res["agreement_window"] = {s: agreement(p, WINDOW) for s, p in pairs.items()}
    res["state_fields_not_copied"] = sorted(rcA.missing)
    res["exclusion"] = excl
    res["group_noise_max_N"] = noise_max
    res["smoke"] = smoke
    res["envs_per_scenario"] = a.reps
    return res


def report(res, a):
    md = [f"# Compliant walker in the two-robot env: {a.name}", "", f"Walker: `{res['walker']}` (kind {res['kind']}).", ""]
    md += ["## 1. Inputs", ""]
    ok_all = True
    for r, v in res["inputs"].items():
        ok = v["same_order"] and v["size_ok"] and v["normalizer_finite"] and v["normalizer_std_positive"]
        ok_all &= ok
        md.append(f"- **{r}: {'OK' if ok else 'PROBLEM'}** - terms in the training order: {v['same_order']}; size "
                  f"{v['size']} vs checkpoint {v['checkpoint_inputs']}; normalizer finite {v['normalizer_finite']}, "
                  f"spread > 0 {v['normalizer_std_positive']}; force-input normalizer mean {v['force_normalizer_mean']}, "
                  f"std {v['force_normalizer_std']}; force term params {v['force_params']}.")
        if not v["same_order"]:
            md.append(f"  - two-robot env: {v['order_coop']}; training: {v['order_training']}")
    md += ["", "## 2. Force wiring vs an independent recomputation (CPU MuJoCo contact forces, robot frame)", "",
           f"Agreeing = vector difference <= max({AGREE_N:g} N, {AGREE_REL:.0%} of the force). Samples with force > {TOUCH_N:g} N.", "",
           "Per step:", "",
           "| where | samples | agree | median diff N | p90 diff N | median force N | median cos | input x / recomputed x (N) |",
           "|---|---|---|---|---|---|---|---|"]

    def line(nm, s):
        if not s.get("samples"):
            return f"| {nm} | 0 | - | - | - | - | - | - |"
        return (f"| {nm} | {s['samples']} | {s['agree_frac']:.0%} | {s['median_diff_N']:.1f} | {s['p90_diff_N']:.1f} | "
                f"{s['median_force_N']:.0f} | {s['median_cos']:.3f} | {s['mean_input_x_N']:+.0f} / {s['mean_recomputed_x_N']:+.0f} |")

    md.append(line("walker training env, pressing a cube", res["walker_env"]["agreement"]))
    miss = sorted(set(res["walker_env"].get("state_fields_not_copied", [])) | set(res.get("state_fields_not_copied", [])))
    for s in ("press", "pushed", "partner", "alone"):
        md.append(line(f"two-robot env, {s}", res["agreement"][s]))
    md += ["", f"Averaged over blocks of {WINDOW} samples ({WINDOW * a.every * 0.02:g} s) per env:", "",
           "| where | blocks | agree | median diff N | p90 diff N | median force N | median cos | input x / recomputed x (N) |",
           "|---|---|---|---|---|---|---|---|",
           line("walker training env, pressing a cube", res["walker_env"]["agreement_window"])]
    for s in ("press", "pushed", "partner", "alone"):
        md.append(line(f"two-robot env, {s}", res["agreement_window"][s]))
    pr = res["agreement"]["pushed"] if res["agreement"]["pushed"].get("samples") else res["agreement"]["press"]
    sign_ok = pr.get("samples", 0) > 0 and pr["mean_input_x_N"] < 0
    wa, ca = res["walker_env"]["agreement"], res["agreement"]["pushed"] if res["agreement"]["pushed"].get("samples") else res["agreement"]["press"]
    if wa.get("samples") and ca.get("samples"):
        same = abs(wa["median_scale"] - ca["median_scale"]) <= 0.1 * max(abs(wa["median_scale"]), 1e-6)
        md += ["", "**Same sensing in both envs** (the question this check answers): input / recomputed force along the force "
               f"(median scale) {wa['median_scale']:.2f} in the walker's training env vs {ca['median_scale']:.2f} in the two-robot env; "
               f"median angle between them {wa['median_angle_deg']:.1f} vs {ca['median_angle_deg']:.1f} deg -> "
               f"{'CONSISTENT' if same and ca['median_cos'] > 0.98 else 'NOT CONSISTENT'}. "
               "(The CPU recomputation is an independent physics evaluation, not a replica of the GPU solver: a common scale "
               "offset in both envs is a solver difference; a difference between the envs would be a wiring problem.)"]
    md += ["", f"State fields not copied into the recomputation: {miss or 'none'}. Observation noise on the force input "
           f"in the two-robot walker group (as in the walker's training): up to {res['group_noise_max_N']:.1f} N per component.",
           f"Physical sign (pressing an object ahead -> force on the robot points backward, x < 0): "
           f"{'OK' if sign_ok else 'PROBLEM or no contact'}.",
           f"Same term order in the walker env: {res['walker_env']['order'] == res['inputs'][next(iter(res['inputs']))]['order_coop']}. "
           f"Examples (input x, y | recomputed x, y), two-robot cube pushed into the robot: {pr.get('examples', [])}", ""]
    ex = res["exclusion"]
    md += ["## 3. Exclusions", "",
           f"- partner walking into robot A (away from the object): {ex['partner_touching_steps']} env-steps with the robots "
           f"touching; largest force input on A then {ex['partner_max_input_N']:.1f} N (should be ~0).",
           f"- robot standing alone: largest force input {ex['alone_max_input_N']:.1f} N (should be ~0).", ""]
    sm = res["smoke"]
    md += ["## 4. Smoke run (robot A presses the 80 kg cube: 0.2 m/s 4 s, stop 2 s, 0.2 m/s 3 s)", "",
           f"- falls (robot A, all scenarios): {sm['fell']} of {4 * res['envs_per_scenario']} (pressing: {sm['fell_press']} of {res['envs_per_scenario']})",
           f"- time touching per phase: {sm['touch']}; force on the cube per phase (N): {sm['force']}",
           f"- force inputs: non-finite rows {sm['nonfinite']}, at the clip (+-2.5) {sm['clipped_frac']:.1%} of env-steps, "
           f"largest |z| under the checkpoint's normalizer {sm['max_abs_z']:.1f}", ""]
    md.append(f"Inputs {'OK' if ok_all else 'PROBLEM'}; see the tables for force agreement, exclusions and the smoke run.")
    return md


if __name__ == "__main__":
    sys.exit(main())
