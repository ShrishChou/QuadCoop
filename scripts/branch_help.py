"""Late help: does a second robot called in mid-push change the outcome? (docs/late_help.md)

Each task (object x start position x mass x placement) runs in two twin envs. The single-robot pusher (the pair's
own parent policy, s2b-anymal-term80, through the pair evaluation wrapper) pushes alone for --probe-s seconds with
the partner parked far away (exactly the solo evaluation). At the branch time the full state of every solo env is
copied into its twin (simulator data, per-world model fields, every manager / entity / sensor tensor, the last
observation), then:
  solo branch  the solo robot continues alone
  help branch  the partner is placed at a staging point --stage-dist m behind the object (relative to the goal, on
               the side away from the pushing robot), facing it; both robots switch to the trained pair policy
               (--checkpoint, IPPO ippo_aa_kl_ten_s0 it 4000 by default) and the partner walks in
Both branches keep the original deadline (--horizon, from the episode start), so the help branch pays its travel.

Per task: outcome of each branch (rescue = solo fails, help succeeds; disruption = solo succeeds, help fails),
time to success, what the probe saw (distance / heading progress, contact time, object speed) for a later help
predictor, and when the helper first reached the object. Tasks that end during the probe are recorded and excluded
from the branch counts. --check also verifies the clone: both twins continue with the SOLO policy for 5 s and the
object / robot divergence is reported (should be ~0).

    python scripts/branch_help.py --name lh-p8 --probe-s 8
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import random
import sys
import time
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT))

from eval_coop2 import FORMATIONS, SCENARIOS, models_for  # noqa: E402

OBJ12 = "cube,long,sphere,cylinder,arch,dumbbell,t_shape,beam,l_shape,asym,u_channel,plus"


def clone_envs(base, obs, src, dst) -> int:
    """Copy env src -> dst (index tensors): everything per-env. Returns the number of tensors copied."""
    import torch
    import warp as wp

    n = base.num_envs
    cnt = 0
    wd = base.sim.wp_data
    for name in dir(wd):
        if name.startswith("_"):
            continue
        try:
            arr = getattr(wd, name)
        except Exception:  # noqa: BLE001
            continue
        if isinstance(arr, wp.array) and arr.ndim >= 1 and arr.shape[0] == n:
            t = wp.to_torch(arr)
            t[dst] = t[src]
            cnt += 1
    for f in base.sim.expanded_fields:
        arr = getattr(base.sim.model, f)
        arr[dst] = arr[src]
        cnt += 1
    seen = set()

    def copy_obj(o, depth=0):
        nonlocal cnt
        if depth > 2 or id(o) in seen:
            return
        seen.add(id(o))
        items = vars(o).items() if hasattr(o, "__dict__") else (o.items() if isinstance(o, dict) else [])
        for _, v in items:
            if isinstance(v, torch.Tensor):
                if v.dim() >= 1 and v.shape[0] == n:
                    try:
                        v[dst] = v[src]
                        cnt += 1
                    except RuntimeError:
                        pass
            elif isinstance(v, dict):
                copy_obj(v, depth + 1)
            elif hasattr(v, "__dict__") and type(v).__module__.startswith("mjlab.utils.buffers"):
                for v2 in vars(v).values():  # circular / delay buffers: (history, env, ...)
                    if isinstance(v2, torch.Tensor) and v2.dim() >= 2 and v2.shape[1] == n and v2.shape[0] != n:
                        v2[:, dst] = v2[:, src]
                        cnt += 1
                    elif isinstance(v2, torch.Tensor) and v2.dim() >= 1 and v2.shape[0] == n:
                        v2[dst] = v2[src]
                        cnt += 1
    for mgr in (base.command_manager, base.action_manager, base.observation_manager):
        for term in (mgr._terms.values() if hasattr(mgr, "_terms") else []):
            copy_obj(term)
        if mgr is base.observation_manager:
            copy_obj(mgr)
    for ent in list(base.scene.entities.values()) if hasattr(base.scene, "entities") else []:
        copy_obj(ent.data)
    for s in (base.scene.sensors.values() if hasattr(base.scene, "sensors") else []):
        copy_obj(s)
        if hasattr(s, "data"):
            copy_obj(s.data)
    base.episode_length_buf[dst] = base.episode_length_buf[src]
    for k in obs.keys():
        obs[k][dst] = obs[k][src]
    return cnt


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True, help="output: logs/evals/<name>/ (branches.csv, summary.md/json)")
    ap.add_argument("--checkpoint", default="logs/marl2/ippo_aa_kl_ten_s0/model_4000.pt",
                    help="the policy after help arrives: the pair (1 -> 2) or the trio (2 -> 3)")
    ap.add_argument("--from-team", type=int, default=1, choices=(1, 2),
                    help="robots pushing in the probe: 1 (the solo parent; help makes a pair) or 2 (--probe-checkpoint, "
                         "a pair; help makes a trio, --pair anymal3)")
    ap.add_argument("--probe-checkpoint", default=None, help="--from-team 2: the pair policy that pushes in the probe")
    ap.add_argument("--pair", default="anymal", choices=("anymal", "anymal3"), help="env team (anymal3 for 2 -> 3)")
    ap.add_argument("--objects", default=OBJ12)
    ap.add_argument("--masses", default="20,40,60,80")
    ap.add_argument("--reps", type=int, default=5)
    ap.add_argument("--seed", type=int, default=7100)
    ap.add_argument("--probe-s", type=float, default=8.0, help="solo probe before the branch (s)")
    ap.add_argument("--stage-dist", type=float, default=3.0, help="helper staging distance behind the object (m)")
    ap.add_argument("--horizon", type=float, default=80.0)
    ap.add_argument("--check", action="store_true", help="clone check: both twins stay solo for 5 s, report divergence")
    ap.add_argument("--device", default=None)
    a = ap.parse_args()

    K = a.from_team
    if K == 2 and (a.pair != "anymal3" or not a.probe_checkpoint):
        raise SystemExit("--from-team 2 needs --pair anymal3 and --probe-checkpoint (the pair)")
    ns = argparse.Namespace(checkpoint=a.checkpoint, solo=None, pair=a.pair, variant="b", frozen_pair=False)
    from train_coop2 import set_env
    models, what = models_for(ns)
    set_env(models)
    import numpy as np  # noqa: F401
    import torch
    from tensordict import TensorDict

    import quadcoop  # noqa: F401
    from mjlab.envs import ManagerBasedRlEnv
    from mjlab.utils.lab_api.math import quat_from_euler_xyz

    from quadcoop import falls
    from quadcoop.coop2 import mdp as cm
    from quadcoop.coop2.env_cfg import SPECS, make_coop2_env_cfg
    from quadcoop.coop2.marl import PairPolicy, action_slices
    from quadcoop.coop2.mdp import AGENTS
    from quadcoop.stage1.mdp import wrap, yaw_of
    from quadcoop.stage1b import mdp as hb
    from quadcoop.stage1b.shapes import NOMINAL_MASS
    from quadcoop.stage2 import mdp as m2
    from quadcoop.stage2.shapes import OBJ_NAMES2, SHAPE_NAMES2, SHAPES2

    device = a.device or ("cuda:0" if torch.cuda.is_available() else "cpu")
    ck = torch.load(a.checkpoint, map_location="cpu", weights_only=False)
    variant = ck.get("variant", "b")
    partner_map = bool(ck["cfg"].get("partner_map", False))
    reward_set = ck["cfg"].get("reward_set", "r3")
    del ck
    objects = [o.strip() for o in a.objects.split(",")]
    masses = [float(x) for x in a.masses.split(",")]
    base_cases = [(o, s, r) for o in objects for s in range(len(SCENARIOS)) for r in range(a.reps)]
    N = len(base_cases)
    n = 2 * N  # env j: solo branch, env N + j: help branch
    out = ROOT / "logs" / "evals" / a.name
    out.mkdir(parents=True, exist_ok=True)
    print(f"late help: {what}\nsolo parent: {models['policy']}\n{N} tasks x {len(masses)} masses, probe {a.probe_s} s, "
          f"staging {a.stage_dist} m, horizon {a.horizon} s", flush=True)
    rows = []
    t0 = time.time()
    active0 = list(AGENTS[:K])  # pushing from the start
    k1, k2 = AGENTS[0], AGENTS[K]  # k2: the helper
    for mass in masses:
        cfg = make_coop2_env_cfg(variant, play=True, partner_map=partner_map, reward_set=reward_set)
        cfg.scene.num_envs = n
        cfg.episode_length_s = 1e5
        cfg.terminations = {}
        alpha = 0.5 * math.log(mass / NOMINAL_MASS)
        for nm in OBJ_NAMES2:
            cfg.events[f"{nm}_mass"].params["alpha_range"] = (alpha, alpha)
        torch.manual_seed(a.seed)
        base = ManagerBasedRlEnv(cfg=cfg, device=device)
        g = base.command_manager.get_term("goal")
        dev = base.device
        ids = torch.arange(n, device=dev)
        for k in range(len(SHAPES2)):
            m2.apply_geometry(base, ids, k, torch.ones(n, 3, device=dev))
        # placements exactly as scripts/eval_coop2.py (same rng stream -> the same tasks as Benchmark B)
        rng = random.Random(f"{a.seed}-coop2")
        jit0 = [[rng.uniform(-10, 10) for _ in range(2)] for _ in base_cases]  # the pair benchmark's draws, also
        gap0 = [[rng.uniform(0.3, 0.6) for _ in range(2)] for _ in base_cases]  # for a trio env (robot 3 parked)
        cases = base_cases + base_cases
        obj_idx = torch.tensor([SHAPE_NAMES2.index(c[0]) for c in cases], device=dev)
        dist = torch.tensor([SCENARIOS[c[1]][1] for c in cases], device=dev)
        gdir = torch.deg2rad(torch.tensor([SCENARIOS[c[1]][2] for c in cases], device=dev))
        turn = torch.deg2rad(torch.tensor([SCENARIOS[c[1]][3] for c in cases], device=dev))
        sym = g.sym[obj_idx]
        cap = torch.where(sym > 0, (math.pi / sym.clamp(min=1)) * g.cfg.max_yaw_frac_of_symmetry, torch.zeros_like(sym))
        turn = torch.sign(turn) * torch.minimum(turn.abs(), cap)
        jit = torch.tensor([jit0[j % N] for j in range(n)], device=dev)
        gap = torch.tensor([gap0[j % N] for j in range(n)], device=dev)
        off_ = list(FORMATIONS["standard"][0]) + [0.0] * (len(AGENTS) - 2)
        jit = torch.cat([jit, torch.zeros(n, len(AGENTS) - jit.shape[1], device=dev)], 1)
        gap = torch.cat([gap, torch.full((n, len(AGENTS) - gap.shape[1]), 0.45, device=dev)], 1)
        bearings = [math.pi + torch.deg2rad(off_[k] + jit[:, k]) for k in range(len(AGENTS))]
        park = [torch.full((n,), k >= K, dtype=torch.bool, device=dev) for k in range(len(AGENTS))]
        z = torch.zeros(n, device=dev)
        sc = {"shape": obj_idx, "obj_xy_rel": torch.zeros(n, 2, device=dev), "obj_heading": z.clone(),
              "goal_xy_rel": dist.unsqueeze(-1) * torch.stack([torch.cos(gdir), torch.sin(gdir)], -1),
              "goal_yaw": wrap(turn), "bearings": bearings, "gaps": [gap[:, k] for k in range(len(AGENTS))],
              "yaw_noise": [z] * len(AGENTS), "park": park}
        g.scenario = lambda env_ids: {k: ([x[env_ids] for x in v] if isinstance(v, list) else v[env_ids])
                                      for k, v in sc.items()}
        obs, _ = base.reset()
        g.scenario = None
        obs = TensorDict({k: v for k, v in obs.items() if not k.startswith("walker_")}, batch_size=[n])
        if K == 1:
            solo = PairPolicy(obs, device, variant, singles=models["policy"])  # the parent in every slot
        else:
            solo = PairPolicy(obs, device, variant, checkpoint=a.probe_checkpoint)  # the pair (robot 3 parked)
        pair = PairPolicy(obs, device, variant, checkpoint=a.checkpoint)  # the team after help arrives
        sl = action_slices(base)
        dt = base.step_dt
        steps = int(a.horizon / dt)
        n_probe = int(round(a.probe_s / dt))
        S, H = torch.arange(N, device=dev), torch.arange(N, 2 * N, device=dev)
        is_help = torch.zeros(n, dtype=torch.bool, device=dev)
        done = torch.zeros(n, dtype=torch.bool, device=dev)
        how = ["horizon"] * n
        t_succ = torch.full((n,), float("nan"), device=dev)
        hold = torch.zeros(n, device=dev)
        d0, e0 = g.errors()
        d0, e0 = d0.clone(), e0.abs().clone()
        touch1 = torch.zeros(n, device=dev)
        t_arrive = torch.full((n,), float("nan"), device=dev)
        feats = {}
        div = []

        def pushing(ag):
            r = base.scene[ag]
            to_goal = g.goal_xy - g.box_pos()[:, :2]
            u = to_goal / torch.linalg.norm(to_goal, dim=-1, keepdim=True).clamp(min=1e-6)
            to_obj = g.box_pos()[:, :2] - r.data.root_link_pos_w[:, :2]
            behind = (to_obj * u).sum(-1) / torch.linalg.norm(to_obj, dim=-1).clamp(min=1e-6) > 0.0
            return (g.surface_distance(ag) < 0.08) & behind

        with torch.no_grad():
            for i in range(steps):
                t = i * dt
                if i == n_probe:  # ---- branch ----
                    d, e = g.errors()
                    feats = {"d_probe": d.clone(), "e_probe": e.abs().clone(), "touch_probe": touch1.clone() / max(n_probe, 1),
                             "speed_probe": torch.linalg.norm(g.box_vel()[:, :2], dim=-1).clone(),
                             "yawrate_probe": g.box_ang_vel()[:, 2].abs().clone(), "done_probe": done.clone()}
                    cnt = clone_envs(base, obs, S, H)
                    done[H] = done[S]
                    for j in range(N):
                        how[N + j] = how[j]
                    t_succ[H], hold[H] = t_succ[S], hold[S]
                    print(f"[{mass:g} kg] branch at {t:.1f} s: {cnt} per-env tensors cloned; "
                          f"{int(done[S].sum())}/{N} tasks already ended", flush=True)
                    if not a.check:
                        is_help[H] = True
                        bp = g.box_pos()[H, :2]
                        u = g.goal_xy[H] - bp
                        u = u / torch.linalg.norm(u, dim=-1, keepdim=True).clamp(min=1e-6)
                        lat = torch.stack([-u[:, 1], u[:, 0]], -1)
                        r1 = torch.stack([base.scene[x].data.root_link_pos_w[H, :2] for x in active0]).mean(0) - bp
                        side = torch.where((r1 * lat).sum(-1) >= 0, -1.0, 1.0).unsqueeze(-1)
                        pos = bp - a.stage_dist * u + 0.8 * side * lat
                        yaw = torch.atan2(bp[:, 1] - pos[:, 1], bp[:, 0] - pos[:, 0])
                        rob = base.scene[k2]
                        st = torch.zeros(N, 13, device=dev)
                        st[:, :2] = pos
                        st[:, 2] = rob.data.root_link_pos_w[H, 2]
                        zz = torch.zeros(N, device=dev)
                        st[:, 3:7] = quat_from_euler_xyz(zz, zz, yaw)
                        rob.write_root_state_to_sim(st, H)
                act = solo(obs, env=base)
                for x in AGENTS[K:]:
                    act[:, sl[x]] = 0.0  # parked robots stand still
                if bool(is_help.any()):
                    act_p = pair(obs, env=base)
                    for x in AGENTS[K + 1:]:
                        act_p[:, sl[x]] = 0.0
                    act = torch.where(is_help.unsqueeze(-1), act_p, act)
                o, _, _, _, _ = base.step(act)
                obs = TensorDict({k: v for k, v in o.items() if not k.startswith("walker_")}, batch_size=[n])
                tt = (i + 1) * dt
                live = ~done
                f_any = torch.zeros(n, dtype=torch.bool, device=dev)
                for x in active0:
                    f_any |= falls.fallen(base, asset_name=x, nominal_height=SPECS[x].nominal_height) & live
                f_any |= falls.fallen(base, asset_name=k2, nominal_height=SPECS[k2].nominal_height) & live & is_help
                tip = hb.box_tipped(base) & live & ~f_any
                lost = cm.box_lost(base) & live & ~f_any & ~tip
                d, e = g.errors()
                ok = live & ~f_any & ~tip & ~lost
                inside = ok & (d < 0.10) & (e.abs() < math.radians(6.0))
                hold = torch.where(inside, hold + dt, torch.zeros_like(hold))
                succ = ok & (hold >= 1.0)
                t_succ = torch.where(succ, torch.full_like(t_succ, tt), t_succ)
                if i < n_probe:
                    touch1 += (sum(pushing(x).float() for x in active0).clamp(max=1.0) * live.float())
                if bool(is_help.any()):
                    arr = is_help & torch.isnan(t_arrive) & pushing(k2)
                    t_arrive = torch.where(arr, torch.full_like(t_arrive, tt), t_arrive)
                for j in f_any.nonzero().flatten().tolist():
                    how[j] = "fell"
                for j in tip.nonzero().flatten().tolist():
                    how[j] = "tipped"
                for j in lost.nonzero().flatten().tolist():
                    how[j] = "lost"
                for j in succ.nonzero().flatten().tolist():
                    how[j] = "success"
                done |= f_any | tip | lost | succ
                if a.check and n_probe <= i < n_probe + int(5.0 / dt):
                    bpos = g.box_pos()[:, :2]
                    rp = base.scene[k1].data.root_link_pos_w[:, :2]
                    div.append((float(torch.linalg.norm(bpos[S] - bpos[H], dim=-1).max()),
                                float(torch.linalg.norm(rp[S] - rp[H], dim=-1).max())))
                    if i == n_probe + int(5.0 / dt) - 1:
                        break
                if bool(done.all()):
                    break
        if a.check:
            ob = [x[0] for x in div]
            rb = [x[1] for x in div]
            print(f"[{mass:g} kg] CLONE CHECK: max object divergence 0.1 s after branch {ob[min(4, len(ob) - 1)]:.4f} m, "
                  f"after 1 s {ob[min(int(1 / dt), len(ob) - 1)]:.4f} m, after 5 s {ob[-1]:.4f} m; "
                  f"robot after 5 s {rb[-1]:.4f} m", flush=True)
            base.close()
            continue
        for j, (o, s, r) in enumerate(base_cases):
            jh = N + j
            rows.append({"object": o, "mass": mass, "scenario": SCENARIOS[s][0], "rep": r, "seed": a.seed,
                         "team_from": K, "team_to": K + 1, "probe_s": a.probe_s,
                         "ended_in_probe": int(bool(feats["done_probe"][j])), "outcome_solo": how[j],
                         "outcome_help": how[jh], "success_solo": int(how[j] == "success"),
                         "success_help": int(how[jh] == "success"),
                         "t_solo": round(float(t_succ[j]), 2) if how[j] == "success" else "",
                         "t_help": round(float(t_succ[jh]), 2) if how[jh] == "success" else "",
                         "helper_arrive_s": "" if math.isnan(float(t_arrive[jh])) else round(float(t_arrive[jh]) - a.probe_s, 2),
                         "d0": round(float(d0[j]), 3), "e0_deg": round(math.degrees(float(e0[j])), 1),
                         "d_probe": round(float(feats["d_probe"][j]), 3),
                         "e_probe_deg": round(math.degrees(float(feats["e_probe"][j])), 1),
                         "touch_probe": round(float(feats["touch_probe"][j]), 3),
                         "speed_probe": round(float(feats["speed_probe"][j]), 3),
                         "yawrate_probe": round(float(feats["yawrate_probe"][j]), 3)})
        mine = [r_ for r_ in rows if r_["mass"] == mass and not r_["ended_in_probe"]]
        resc = sum(1 for r_ in mine if not r_["success_solo"] and r_["success_help"])
        disr = sum(1 for r_ in mine if r_["success_solo"] and not r_["success_help"])
        print(f"[{mass:g} kg] branched {len(mine)}: solo {sum(r_['success_solo'] for r_ in mine) / max(len(mine), 1):.2f}, "
              f"help {sum(r_['success_help'] for r_ in mine) / max(len(mine), 1):.2f}; rescues {resc}, disruptions {disr} "
              f"({time.time() - t0:.0f} s)", flush=True)
        base.close()
        del base
    if a.check:
        return 0
    with open(out / "branches.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    # summary: per mass and per object x mass
    by = defaultdict(list)
    for r_ in rows:
        by[("mass", r_["mass"])].append(r_)
        by[("om", r_["object"], r_["mass"])].append(r_)

    def agg(rs):
        b = [r_ for r_ in rs if not r_["ended_in_probe"]]
        k = max(len(b), 1)
        return {"tasks": len(rs), "ended_in_probe": len(rs) - len(b),
                "solo_success_all": sum(r_["success_solo"] for r_ in rs) / max(len(rs), 1),
                "help_success_all": sum(r_["success_help"] for r_ in rs) / max(len(rs), 1),
                "branched": len(b), "rescue": sum(1 for r_ in b if not r_["success_solo"] and r_["success_help"]) / k,
                "disruption": sum(1 for r_ in b if r_["success_solo"] and not r_["success_help"]) / k,
                "both": sum(1 for r_ in b if r_["success_solo"] and r_["success_help"]) / k,
                "neither": sum(1 for r_ in b if not r_["success_solo"] and not r_["success_help"]) / k}
    summ = {"probe_s": a.probe_s, "stage_dist": a.stage_dist, "checkpoint": a.checkpoint, "solo": models["policy"],
            "by_mass": {f"{m:g}": agg(by[("mass", m)]) for m in masses},
            "by_object_mass": {f"{o} / {m:g}": agg(by[("om", o, m)]) for o in objects for m in masses}}
    (out / "summary.json").write_text(json.dumps(summ, indent=1))
    L = [f"# Late help, probe {a.probe_s:g} s, staging {a.stage_dist:g} m", "",
         "Branched tasks only for rescue / disruption (tasks that ended during the probe excluded). Success columns are "
         "over all tasks (a task that ended in the probe counts the same in both branches).", "",
         "| mass | tasks | ended in probe | solo success | help success | rescue | disruption | both | neither |",
         "|---|---|---|---|---|---|---|---|---|"]
    f = lambda x: f"{100 * x:.0f}%"  # noqa: E731
    for m in masses:
        s_ = summ["by_mass"][f"{m:g}"]
        L.append(f"| {m:g} kg | {s_['tasks']} | {s_['ended_in_probe']} | {f(s_['solo_success_all'])} | "
                 f"{f(s_['help_success_all'])} | {f(s_['rescue'])} | {f(s_['disruption'])} | {f(s_['both'])} | {f(s_['neither'])} |")
    L += ["", "## By object and mass (rescue / disruption among branched tasks)", "",
          "| object | " + " | ".join(f"{m:g} kg" for m in masses) + " |", "|---|" + "---|" * len(masses)]
    for o in objects:
        cells = []
        for m in masses:
            s_ = summ["by_object_mass"][f"{o} / {m:g}"]
            cells.append(f"{f(s_['rescue'])} / {f(s_['disruption'])} (n {s_['branched']})")
        L.append(f"| {o} | " + " | ".join(cells) + " |")
    (out / "summary.md").write_text("\n".join(L) + "\n")
    print(f"wrote {out}/branches.csv, summary.md", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
