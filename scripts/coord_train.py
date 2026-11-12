"""Train the learned contact-assignment coordinator (docs/coordinator_design.md, section 6) over the frozen backend.

Rollouts run through scripts/contact_test.py in this process (--coordinator external), so the coordinator sees
exactly the evaluator's tasks, success and failure definitions. Frozen backend: walker v1, the turn_debug
executor, QUADCOOP_PLANNER=ends, QUADCOOP_CONTACT=train, QUADCOOP_CMD_IF=raw, expert planner settings as
trained (reselect 3-6 s), plus the slow-arrival limit (--slow-min-s, 1 s) for teacher and learner alike.

  collect   teacher (or a policy, sampled = DAgger) rollouts with the teacher's label at every decision
            python scripts/coord_train.py collect --out logs/coord/bc0 --seeds 100-111
  bc        imitation (keep/select, both robots active) + critic on discounted returns; held-out seeds
            python scripts/coord_train.py bc --data logs/coord/bc0 --heldout 110,111 --out logs/coord/bc0/bc.pt
  rl        PPO from the BC weights (semi-MDP GAE), budget and checkpoint rule fixed in run.json before the start
            python scripts/coord_train.py rl --init logs/coord/bc0/bc.pt --run logs/coord/rl_s0 --iters 24

Task cells: long, arch, dumbbell x the 4 standard scenarios x 20/40/60 kg, start behind, minus the cells where the
reference (e1s-A + e1s-Aw pooled) succeeded in under 25% of episodes: dumbbell / D_far_turn / 60 kg. Excluded
cells still run (contact_test runs the full cross product) but their decisions are not recorded.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "src"))

import torch  # noqa: E402

TD = "logs/keep/marl2/turn_debug/model_15000.pt"
OBJECTS = "long,arch,dumbbell"
EXCLUDED = {("dumbbell", "D_far_turn", 60.0)}  # reference success < 25% (declared rule)


def seeds_of(s: str) -> list[int]:
    out = []
    for part in s.split(","):
        if "-" in part:
            lo, hi = part.split("-")
            out += list(range(int(lo), int(hi) + 1))
        elif part.strip():
            out.append(int(part))
    return out


def env_setup():
    for k, v in (("QUADCOOP_PLANNER", "ends"), ("QUADCOOP_CONTACT", "train"), ("QUADCOOP_CMD_IF", "raw")):
        if os.environ.get(k, v) != v:
            raise SystemExit(f"{k}={os.environ[k]!r}: the backend is frozen at {k}={v}")
        os.environ[k] = v
    os.environ.setdefault("MUJOCO_GL", "egl")


def rollout(net, mode: str, seed: int, masses: str, reps: int, prefix: str, ro, rc, horizon: float = 80.0,
            tasks: str = "standard", start: str = "behind", slow_min_s: float = 1.0) -> dict:
    """One contact_test run (every mass in masses, one env batch per mass) with a LearnedCoordinator recording into
    ro. Returns the coordinator's decision statistics, summed over masses."""
    import contact_test as CT
    from quadcoop.coop2 import coord_learn as CL
    stats = dict(decisions=0, switches=0, teacher_switches=0, agree=0, invalid=0)

    def factory(n, dev, cases, mass, dt):
        names = CT.SCENARIOS
        rec = torch.tensor([(o, names[s][0], float(mass)) not in EXCLUDED for _, o, s, _, _ in cases], device=dev)
        c = CL.LearnedCoordinator(n, dev, net, mode, ro, rc, dt, record=rec,
                                  key_fn=lambda j, m_=mass: (seed, float(m_), j), seed=seed)
        factory.made.append(c)
        return c
    factory.made = []
    CT.EXTERNAL_COORD = factory
    argv = ["contact_test.py", "--executor", "stage4", "--checkpoint", TD, "--rules", "expert", "--objects", OBJECTS,
            "--masses", masses, "--reps", str(reps), "--seed", str(seed), "--start", start, "--reselect-s", "auto",
            "--videos", "0", "--diag", "0", "--trace", "0", "--horizon", str(horizon), "--tasks", tasks,
            "--slow-min-s", str(slow_min_s), "--coordinator", "external", "--prefix", prefix]
    old = sys.argv
    sys.argv = argv
    try:
        CT.main()
    finally:
        sys.argv = old
        CT.EXTERNAL_COORD = None
    for c in factory.made:
        for k in ("decisions", "switches", "teacher_switches", "agree"):
            stats[k] += c.stats[k]
        stats["invalid"] += c.invalid
    return stats


def batch_obs(obs: dict, idx: torch.Tensor, dev) -> dict:
    return {k: v[idx].to(dev) for k, v in obs.items()}


def episode_outcomes(rows) -> dict:
    out = {}
    for r in rows:
        if r.get("done"):
            out[r["key"]] = r.get("outcome", "")
    n = max(len(out), 1)
    return dict(episodes=len(out), success=sum(v == "success" for v in out.values()) / n,
                fail=sum(v == "fail" for v in out.values()) / n)


# ---------------------------------------------------------------------------------------------------- collect
def cmd_collect(a):
    env_setup()
    from quadcoop.coop2 import coord_learn as CL
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    net = CL.load_policy(a.policy, dev) if a.policy else None
    mode = "teacher" if net is None else a.mode
    rc = CL.RewardCfg()
    for s in seeds_of(a.seeds):
        f = out / f"ro_seed{s}.pt"
        if f.exists():
            print(f"{f} exists, skipped", flush=True)
            continue
        ro = CL.Rollout()
        t0 = time.time()
        st = rollout(net, mode, s, a.masses, a.reps, f"coordcol-{out.name}-s{s}", ro, rc, horizon=a.horizon, tasks=a.tasks,
                     start=a.start)
        ro.save(f)
        print(f"seed {s}: {len(ro)} decisions, {st}, {episode_outcomes(ro.rows)} ({time.time() - t0:.0f} s) -> {f}",
              flush=True)


# --------------------------------------------------------------------------------------------------------- bc
def load_dir(d: Path, seeds=None):
    from quadcoop.coop2 import coord_learn as CL
    fs = sorted(d.glob("ro_seed*.pt"))
    if seeds is not None:
        fs = [f for f in fs if int(f.stem.replace("ro_seed", "")) in seeds]
    return CL.Rollout.load([str(f) for f in fs])


def cmd_bc(a):
    from quadcoop.coop2 import coord_learn as CL
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    torch.manual_seed(a.seed)
    rc = CL.RewardCfg()
    ro = CL.Rollout.load([str(f) for d in a.data.split(",") for f in sorted(Path(d).glob("ro_seed*.pt"))])
    rows = [r for r in ro.rows]
    K = ro.obs[0]["joint"].shape[1]
    obs = ro.stacked_obs(K)
    keep = torch.tensor([r["closed"] for r in rows])  # closed transitions (critic targets defined)
    ret = CL.mc_returns(rows, rc)
    held = set(seeds_of(a.heldout))
    is_held = torch.tensor([r["key"][0] in held for r in rows])
    tr, te = (~is_held).nonzero().flatten(), is_held.nonzero().flatten()
    teacher = obs["teacher"]
    tsw = (teacher != obs["cur"]).any(-1)
    print(f"{len(rows)} decisions ({len(tr)} train, {len(te)} held-out seeds {sorted(held)}); teacher switches "
          f"{float(tsw.float().mean()):.3f}; K = {K}", flush=True)
    fs, fc = obs["shared"].shape[-1], obs["cand"].shape[-1]
    net = CL.PairPolicy(fs, fc).to(dev)
    opt = torch.optim.Adam(net.parameters(), lr=a.lr)
    # switch decisions are a minority: weight them so that, in total, they count as much as a.switch_share
    w = torch.ones(len(rows))
    sw_tr = float(tsw[tr].float().mean())
    if a.switch_share > 0 and 0 < sw_tr < a.switch_share:
        w[tsw] = a.switch_share / sw_tr * (1 - sw_tr) / (1 - a.switch_share)
    ret_s = float(ret[tr].std().clamp(min=1e-3))
    log = []

    mass_of = torch.tensor([float(r["key"][1]) for r in rows])

    def evaluate(idx, by_mass=False):
        if by_mass:
            out = {"all": evaluate(idx)}
            for m_ in sorted(set(mass_of[idx].tolist())):
                out[f"{m_:g}kg"] = evaluate(idx[mass_of[idx] == m_])
            return out
        net.eval()
        L, V = [], []
        with torch.no_grad():
            for b in idx.split(1024):
                lg, v = net(batch_obs(obs, b, dev))
                L.append(lg.cpu())
                V.append(v.cpu())
        net.train()
        lg = torch.cat(L)
        met = CL.imitation_metrics(lg, teacher[idx], obs["cur"][idx])
        k_ = keep[idx]
        met["value_r2"] = float(1 - ((torch.cat(V)[k_] * ret_s - ret[idx][k_]) ** 2).mean() / ret[idx][k_].var().clamp(min=1e-9))
        return met
    for ep in range(a.epochs):
        perm = tr[torch.randperm(len(tr))]
        tot = 0.0
        for b in perm.split(a.batch):
            ob = batch_obs(obs, b, dev)
            lg, v = net(ob)
            ce = -(CL.joint_logp(lg, ob["teacher"]) * w[b].to(dev)).sum() / w[b].sum().to(dev)
            k_ = keep[b].to(dev)
            vl = (((v - ret[b].to(dev) / ret_s) ** 2) * k_).sum() / k_.sum().clamp(min=1)
            loss = ce + a.vf_coef * vl
            opt.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(net.parameters(), 1.0)
            opt.step()
            tot += float(ce) * len(b)
        if ep % max(1, a.epochs // 10) == 0 or ep == a.epochs - 1:
            m_tr, m_te = evaluate(tr), evaluate(te) if len(te) else {}
            log.append(dict(epoch=ep, ce=tot / len(tr), train=m_tr, heldout=m_te))
            print(f"epoch {ep}: ce {tot / len(tr):.3f} | train {fmt(m_tr)} | held-out {fmt(m_te)}", flush=True)
    final = dict(train=evaluate(tr, True), heldout=evaluate(te, True) if len(te) else {})
    for part in ("train", "heldout"):
        for k_, m_ in final[part].items():
            print(f"final {part} {k_} (n {m_['n']}, teacher switch share {m_['teacher_switch_share']:.3f}): {fmt(m_)}", flush=True)
    log.append(dict(final=final))
    CL.save_policy(a.out, net, dict(ret_scale=ret_s, bc=dict(vars(a)), log=log, reward=asdict(rc)))
    Path(a.out).with_suffix(".json").write_text(json.dumps(log[-1], indent=1))
    print(f"saved {a.out}", flush=True)


def fmt(m: dict) -> str:
    if not m:
        return "-"
    return (f"exact {m['exact']:.3f}, keep {m['exact_on_keep']:.3f}, switch recall {m['switch_recall']:.3f}, "
            f"exact on switch {m['exact_on_switch']:.3f}, false switch {m['false_switch']:.3f}, value R2 {m['value_r2']:.2f}")


# --------------------------------------------------------------------------------------------------------- rl
def cmd_rl(a):
    env_setup()
    from quadcoop.coop2 import coord_learn as CL
    dev = "cuda"
    run = Path(a.run)
    run.mkdir(parents=True, exist_ok=True)
    rc = CL.RewardCfg()
    masses = [m.strip() for m in a.masses.split(",")]
    cfg = dict(vars(a), reward=asdict(rc), backend=dict(executor=TD, planner="ends", contact="train", cmd_if="raw",
                                                     reselect="auto (3-6 s)", slow_min_s=1.0),
               objects=OBJECTS, excluded=sorted(map(list, EXCLUDED)),
               budget=f"{a.iters} iterations x {a.reps} reps x 3 objects x 4 scenarios, one mass per iteration "
                      f"(cycling {masses}); seeds {a.seed0}..{a.seed0 + a.iters - 1}",
               checkpoint_rule="the final checkpoint (model_final.pt) is the result; intermediate checkpoints are "
                               "kept for the record only and are not selected on held-out performance",
               heldout="final comparison on placement seeds 3000-3002 (reserved, never used before), greedy policy, against the teacher and BC")
    if (run / "run.json").exists():
        old = json.loads((run / "run.json").read_text())
        if {k: v for k, v in old.items() if k != "resume"} != {k: v for k, v in cfg.items() if k != "resume"}:
            raise SystemExit(f"{run}/run.json differs from this command's configuration: not resuming a different run")
    else:
        (run / "run.json").write_text(json.dumps(cfg, indent=1))
    ck = CL.load_policy(a.init, dev)
    net = ck
    net.train()
    d0 = torch.load(a.init, map_location="cpu", weights_only=False)
    ret_s = float(d0.get("ret_scale", 1.0))
    opt = torch.optim.Adam(net.parameters(), lr=a.lr)
    it0 = 0
    if (run / "state.pt").exists():
        st = torch.load(run / "state.pt", map_location=dev, weights_only=False)
        net.load_state_dict(st["net"])
        opt.load_state_dict(st["opt"])
        it0 = st["it"] + 1
        print(f"resumed at iteration {it0}", flush=True)
    logf = open(run / "log.jsonl", "a")
    for it in range(it0, a.iters):
        t0 = time.time()
        seed = a.seed0 + it
        mass = masses[it % len(masses)]
        ro = CL.Rollout()
        net.eval()
        st = rollout(net, "sample", seed, mass, a.reps, f"coordrl-{run.name}-it{it:03d}", ro, rc, horizon=a.horizon)
        t_roll = time.time() - t0
        net.train()
        rows = ro.rows
        adv, ret = CL.gae([dict(r, v=r["v"] * ret_s, v_next=r["v_next"] * ret_s) for r in rows], rc)
        ok = torch.tensor([r["closed"] for r in rows])
        idx = ok.nonzero().flatten()
        obs = ro.stacked_obs(ro.obs[0]["joint"].shape[1])
        a_ = torch.tensor([r["a"] for r in rows])
        lp_old = torch.tensor([r["logp"] for r in rows])
        A = adv[idx]
        A = (A - A.mean()) / A.std().clamp(min=1e-6)
        advn = torch.zeros(len(rows))
        advn[idx] = A
        bc_coef = a.bc_coef * max(0.0, 1.0 - it / max(1.0, a.bc_decay * a.iters))
        tot = dict(pg=0.0, vf=0.0, ent=0.0, bc=0.0, kl=0.0, clip=0.0, n=0)
        for _ in range(a.epochs):
            for b in idx[torch.randperm(len(idx))].split(a.batch):
                ob = batch_obs(obs, b, dev)
                lg, v = net(ob)
                lp = CL.joint_logp(lg, a_[b].to(dev))
                ratio = (lp - lp_old[b].to(dev)).exp()
                adb = advn[b].to(dev)
                pg = -torch.minimum(ratio * adb, ratio.clamp(1 - a.clip, 1 + a.clip) * adb).mean()
                vf = ((v - ret[b].to(dev) / ret_s) ** 2).mean()
                ent = CL.joint_entropy(lg, ob["joint"]).mean()
                bc = -CL.joint_logp(lg, ob["teacher"]).mean()
                loss = pg + a.vf_coef * vf - a.ent_coef * ent + bc_coef * bc
                opt.zero_grad()
                loss.backward()
                torch.nn.utils.clip_grad_norm_(net.parameters(), 1.0)
                opt.step()
                with torch.no_grad():
                    kl = (lp_old[b].to(dev) - lp).mean()
                    clipf = ((ratio - 1).abs() > a.clip).float().mean()
                for k_, v_ in (("pg", pg), ("vf", vf), ("ent", ent), ("bc", bc), ("kl", kl), ("clip", clipf)):
                    tot[k_] += float(v_)
                tot["n"] += 1
        nb = max(tot.pop("n"), 1)
        rec = dict(it=it, seed=seed, mass=float(mass), recorded=len(rows), used=len(idx), rollout_s=round(t_roll),
                   update_s=round(time.time() - t0 - t_roll), bc_coef=bc_coef,
                   **{k: v / nb for k, v in tot.items()}, **st, **episode_outcomes(rows),
                   switch_rate=st["switches"] / max(st["decisions"], 1), teacher_agree=st["agree"] / max(st["decisions"], 1),
                   adv_std=float(adv[idx].std()), ret_mean=float(ret[idx].mean()))
        logf.write(json.dumps(rec) + "\n")
        logf.flush()
        print(f"it {it} ({mass} kg, seed {seed}): {rec}", flush=True)
        CL.save_policy(run / f"model_{it:03d}.pt", net, dict(ret_scale=ret_s, it=it))
        torch.save(dict(net=net.state_dict(), opt=opt.state_dict(), it=it), run / "state.pt")
    CL.save_policy(run / "model_final.pt", net, dict(ret_scale=ret_s, it=a.iters - 1))
    print(f"done: {run / 'model_final.pt'}", flush=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("collect")
    c.add_argument("--out", required=True)
    c.add_argument("--seeds", required=True)
    c.add_argument("--policy", default=None, help="a policy to run (DAgger); default the teacher")
    c.add_argument("--mode", choices=("sample", "greedy"), default="sample")
    c.add_argument("--masses", default="20,40,60")
    c.add_argument("--reps", type=int, default=4)
    c.add_argument("--tasks", default="standard")
    c.add_argument("--start", default="behind")
    c.add_argument("--horizon", type=float, default=80.0)
    b = sub.add_parser("bc")
    b.add_argument("--data", required=True, help="collect folders, comma-separated")
    b.add_argument("--heldout", default="", help="seeds kept out of training (reported separately)")
    b.add_argument("--out", required=True)
    b.add_argument("--epochs", type=int, default=40)
    b.add_argument("--batch", type=int, default=256)
    b.add_argument("--lr", type=float, default=3e-4)
    b.add_argument("--vf-coef", type=float, default=0.5)
    b.add_argument("--switch-share", type=float, default=0.3,
                   help="weight teacher switch decisions up to this share of the loss (0 = unweighted)")
    b.add_argument("--seed", type=int, default=0)
    r = sub.add_parser("rl")
    r.add_argument("--init", required=True)
    r.add_argument("--run", required=True)
    r.add_argument("--iters", type=int, default=24)
    r.add_argument("--reps", type=int, default=12)
    r.add_argument("--masses", default="20,40,60")
    r.add_argument("--horizon", type=float, default=80.0)
    r.add_argument("--seed0", type=int, default=200)
    r.add_argument("--epochs", type=int, default=4)
    r.add_argument("--batch", type=int, default=256)
    r.add_argument("--lr", type=float, default=1e-4)
    r.add_argument("--clip", type=float, default=0.2)
    r.add_argument("--vf-coef", type=float, default=0.5)
    r.add_argument("--ent-coef", type=float, default=0.003)
    r.add_argument("--bc-coef", type=float, default=0.5, help="teacher cross-entropy weight at the start")
    r.add_argument("--bc-decay", type=float, default=0.25, help="... decayed linearly to 0 by this fraction of --iters")
    a = ap.parse_args()
    {"collect": cmd_collect, "bc": cmd_bc, "rl": cmd_rl}[a.cmd](a)


if __name__ == "__main__":
    main()
