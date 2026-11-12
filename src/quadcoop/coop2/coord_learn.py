"""Learned contact-assignment coordinator (design: docs/coordinator_design.md): observation, policy / critic,
semi-MDP rollout buffer, and the imitation (BC) and PPO losses.

Policy: one score s(i, j) per ordered contact pair (robot 1 at i, robot 2 at j), masked by the joint validity
mask (KEEP = the current pair, always valid). The joint distribution is the masked softmax over the K x K scores.
It is sampled autoregressively: robot 1 from its marginal (logsumexp over its valid partners), then robot 2 from
the row fixed by robot 1's choice. The joint log-probability = robot 1's + robot 2's conditional
log-probability = the masked joint log-softmax, which is what PPO recomputes. Every sampled pair is valid by
construction.

Rewards are accumulated per env step by on_step (called by the rollout loop) and discounted by elapsed time,
gamma per second: transition d (decision at t_d, next decision or episode end at t_d + D) has
R_d = sum_tau gamma^(t_tau - t_d) r_tau, bootstrap gamma^D V(s_{d+1}), GAE weight (gamma lambda)^D.
"""
from __future__ import annotations

from dataclasses import dataclass

import torch
import torch.nn as nn
import torch.nn.functional as F

from quadcoop.coop2.coord import Coordinator, decision_context

N_REASON = 8  # c_plan_reason codes 0..7
PAIR_F = 4  # res, J - J(current pair), slower arrival, is current pair


@dataclass
class RewardCfg:
    """Team reward per env step (declared before training; deployed robot-seconds cost 0 in this stage)."""
    w_progress: float = 1.0  # per metre of pose-error decrease (pose_error = distance + rho_g x |yaw error|)
    r_success: float = 2.0  # once, at the evaluator's success (10 cm / 6 deg held 1 s)
    r_fail: float = 2.0  # once, at a fall, tipped or lost object (terminal)
    w_time: float = 0.02  # per second
    w_collide: float = 0.1  # per second while the robots touch each other
    w_deploy: float = 0.0  # per active robot-second (stage W2)
    gamma: float = 0.98  # per second
    lam: float = 0.95  # per second


def _to_obj(v, cs, sn):
    """World (m, 2) -> object frame (rotate by -yaw)."""
    return torch.stack([cs * v[..., 0] + sn * v[..., 1], -sn * v[..., 0] + cs * v[..., 1]], -1)


def observe(g, ctx: dict, last_t: torch.Tensor) -> dict:
    """Features for the envs of ctx (all from the env state and the expert's proposal; nothing from the
    expert's decision itself except its cost terms)."""
    ids = ctx["ids"]
    m, K = len(ids), ctx["K"]
    dev = ids.device
    yaw = g.contact_frame_yaw()[ids]
    cs, sn = torch.cos(yaw), torch.sin(yaw)
    obj = g.box_pos()[ids, :2]
    _, e = g.errors()
    e = torch.where(g.symmetry() > 0, e, torch.zeros_like(e))[ids]
    S = g.c_p.shape[0]
    rob = []
    for k in range(2):
        rob.append(_to_obj(g.robot_xy(k)[ids] - obj, cs, sn) / 3.0)
        ry = g.robot_yaw(k)[ids] - yaw
        rob.append(torch.stack([torch.cos(ry), torch.sin(ry)], -1))
    since = (ctx["t"] - last_t[ids]).nan_to_num(nan=10.0).clamp(0.0, 10.0) / 10.0
    col = lambda x: x.float().unsqueeze(-1)  # noqa: E731
    shared = torch.cat([
        _to_obj(g.goal_xy[ids] - obj, cs, sn) / 3.0, col(e),
        _to_obj(g.box_vel()[ids, :2], cs, sn), col(g.box_ang_vel()[ids, 2]),
        _to_obj(g.c_vdes[ids], cs, sn), col(g.c_wdes[ids]),
        col(g.c_mass[ids] / 60.0), col(g.c_mu[ids]), col(g.c_rg[ids]),
        F.one_hot(g.shape[ids], S).float(), *rob,
        g.c_engaged[ids].float(), ctx["on"].float(),
        col(ctx["t"] / 80.0), col(since),
        F.one_hot(g.c_plan_reason[ids].clamp(0, N_REASON - 1), N_REASON).float(),
        col(ctx["zone"]), col(g.c_stalled[ids]), col(ctx["need_more"]),
    ], -1)
    kk = torch.arange(K, device=dev).unsqueeze(0)
    cand = [ctx["p"], ctx["nn"], ctx["pre"]]
    for k in range(2):
        same = kk == ctx["cur"][:, k : k + 1]
        cand += [col(ctx["t_route"][k].clamp(0.0, 30.0) / 10.0), col(same),
                 col((ctx["t_arr"][k] >= 1e5) & ~same), col(ctx["stop"][k])]
    cand = torch.cat(cand, -1)
    joint = ctx["joint"]
    ar = torch.arange(m, device=dev)
    jrel = (ctx["J"] - ctx["j_cur"].clamp(max=1e3)[:, None, None]).clamp(-3.0, 3.0)
    tmax = torch.maximum(ctx["t_arr"][0].unsqueeze(2), ctx["t_arr"][1].unsqueeze(1)).clamp(0.0, 30.0) / 10.0
    curp = torch.zeros(m, K, K, device=dev)
    curp[ar, ctx["cur"][:, 0], ctx["cur"][:, 1]] = 1.0
    pair = torch.stack([ctx["res"].clamp(0.0, 2.0), jrel, tmax, curp], -1)
    pair = torch.where(joint.unsqueeze(-1), pair, torch.zeros_like(pair))
    return dict(shared=shared, cand=cand, pair=pair, joint=joint, cur=ctx["cur"], teacher=ctx["teacher"])


def obs_dims(obs: dict) -> tuple[int, int]:
    return obs["shared"].shape[-1], obs["cand"].shape[-1]


class PairPolicy(nn.Module):
    """Pair scores s(i, j) = MLP(A cand_i + B cand_j + P pair_ij + Z shared) and a centralized critic."""

    def __init__(self, fs: int, fc: int, h: int = 128):
        super().__init__()
        self.dims = dict(fs=fs, fc=fc, h=h)
        self.sh = nn.Sequential(nn.Linear(fs, h), nn.ELU(), nn.Linear(h, h))
        self.c1, self.c2 = nn.Linear(fc, h), nn.Linear(fc, h, bias=False)
        self.pp = nn.Linear(PAIR_F, h, bias=False)
        self.head = nn.Sequential(nn.ELU(), nn.Linear(h, h), nn.ELU(), nn.Linear(h, 1))
        self.critic = nn.Sequential(nn.Linear(fs + 2 * PAIR_F, 256), nn.ELU(), nn.Linear(256, 256), nn.ELU(),
                                    nn.Linear(256, 1))

    def forward(self, obs: dict) -> tuple[torch.Tensor, torch.Tensor]:
        """-> masked pair logits (m, K, K), value (m,)."""
        z = self.sh(obs["shared"])
        x = self.c1(obs["cand"]).unsqueeze(2) + self.c2(obs["cand"]).unsqueeze(1) + self.pp(obs["pair"]) + \
            z[:, None, None]
        logits = self.head(x).squeeze(-1).masked_fill(~obs["joint"], -1e9)
        m = len(z)
        ar = torch.arange(m, device=z.device)
        cur_f = obs["pair"][ar, obs["cur"][:, 0], obs["cur"][:, 1]]
        best_f = torch.where(obs["joint"].unsqueeze(-1), obs["pair"], torch.full_like(obs["pair"], 1e3)) \
            .view(m, -1, PAIR_F).min(1).values.clamp(max=3.0)
        v = self.critic(torch.cat([obs["shared"], cur_f, best_f], -1)).squeeze(-1)
        return logits, v


def joint_logp(logits: torch.Tensor, a: torch.Tensor) -> torch.Tensor:
    """log pi(a1, a2) under the masked joint softmax = robot 1's marginal + robot 2's conditional log-prob."""
    m, K, _ = logits.shape
    return torch.log_softmax(logits.view(m, -1), -1).gather(1, (a[:, 0] * K + a[:, 1])[:, None]).squeeze(1)


def joint_entropy(logits: torch.Tensor, joint: torch.Tensor) -> torch.Tensor:
    m = len(logits)
    lp = torch.log_softmax(logits.view(m, -1), -1)
    return -(lp.exp() * lp).masked_fill(~joint.view(m, -1), 0.0).sum(-1)


def sample(logits: torch.Tensor, greedy: bool = False, gen=None) -> tuple[torch.Tensor, torch.Tensor]:
    """Autoregressive: robot 1 from its marginal, robot 2 from its conditional. -> actions (m, 2), joint logp."""
    m, K, _ = logits.shape
    marg = torch.logsumexp(logits, 2)  # robot 1: log sum over its partners (unnormalised)
    if greedy:
        flat = logits.view(m, -1).argmax(-1)
        a = torch.stack([flat // K, flat % K], -1)
    else:
        a0 = torch.multinomial(torch.softmax(marg, -1), 1, generator=gen).squeeze(-1)
        row = logits[torch.arange(m, device=logits.device), a0]
        a1 = torch.multinomial(torch.softmax(row, -1), 1, generator=gen).squeeze(-1)
        a = torch.stack([a0, a1], -1)
    return a, joint_logp(logits, a)


class Rollout:
    """Semi-MDP transitions, one per recorded decision. Observations are stored per decision (CPU); the
    transition fields are filled when the env's next decision (or its episode end) closes the transition."""

    def __init__(self):
        self.obs: list[dict] = []  # chunks
        self.rows: list[dict] = []  # per transition: key, t, a, logp, v, teacher, cur, R, D, v_next, done

    def __len__(self):
        return len(self.rows)

    def add(self, obs: dict, key: list, t, a, logp, v) -> list[int]:
        start = len(self.rows)
        self.obs.append({k: x.detach().cpu() for k, x in obs.items()})
        for i in range(len(key)):
            self.rows.append(dict(key=key[i], t=float(t[i]), a=a[i].tolist(), logp=float(logp[i]), v=float(v[i]),
                                  teacher=obs["teacher"][i].tolist(), cur=obs["cur"][i].tolist(),
                                  R=0.0, D=0.0, v_next=0.0, done=False, closed=False))
        return list(range(start, start + len(key)))

    def stacked_obs(self, K: int) -> dict:
        """Concatenate the chunks, padding the candidate axis to K."""
        out = {}
        for k in self.obs[0]:
            parts = []
            for ch in self.obs:
                x = ch[k]
                if k in ("cand",) and x.shape[1] < K:
                    x = F.pad(x, (0, 0, 0, K - x.shape[1]))
                elif k in ("pair",) and x.shape[1] < K:
                    x = F.pad(x, (0, 0, 0, K - x.shape[2], 0, K - x.shape[1]))
                elif k == "joint" and x.shape[1] < K:
                    x = F.pad(x, (0, K - x.shape[2], 0, K - x.shape[1]), value=False)
                parts.append(x)
            out[k] = torch.cat(parts)
        return out

    def save(self, path):
        torch.save(dict(obs=self.obs, rows=self.rows), path)

    @staticmethod
    def load(paths) -> "Rollout":
        r = Rollout()
        for p in ([paths] if isinstance(paths, str) else paths):
            d = torch.load(p, weights_only=False)
            r.obs += d["obs"]
            r.rows += d["rows"]
        return r


class LearnedCoordinator(Coordinator):
    """Runs a PairPolicy (or the teacher) at every decision and records semi-MDP transitions.

    mode: "teacher" = apply the expert's choice (BC data); "sample" = sample from the policy (PPO / DAgger);
    "greedy" = the policy's most likely pair (evaluation). Every recorded decision also stores the teacher's
    label. record (n,) bool: envs whose decisions are recorded (e.g. excluded task cells are not); key_fn(j)
    gives each env's episode key. Decisions after an env's episode ended are not recorded and apply the
    teacher's choice (the env keeps stepping until the batch ends)."""

    def __init__(self, n: int, device, net: PairPolicy | None, mode: str, rollout: Rollout | None,
                 rcfg: RewardCfg, dt: float, record: torch.Tensor | None = None, key_fn=None, seed: int = 0):
        super().__init__(n, device)
        self.net, self.mode, self.ro, self.rc, self.dt = net, mode, rollout, rcfg, dt
        self.record = record if record is not None else torch.ones(n, dtype=torch.bool, device=device)
        self.key_fn = key_fn or (lambda j: j)
        self.gen = torch.Generator(device=device).manual_seed(seed)
        self.open = [-1] * n  # open transition index per env
        self.t_open = torch.zeros(n, device=device)
        self.R = torch.zeros(n, device=device)
        self.ended = torch.zeros(n, dtype=torch.bool, device=device)
        self.pe_prev = None
        self.stats = dict(decisions=0, switches=0, teacher_switches=0, agree=0)

    @torch.no_grad()
    def choose(self, ctx):
        raise RuntimeError("LearnedCoordinator overrides __call__")

    @torch.no_grad()
    def __call__(self, g, ids: torch.Tensor) -> None:
        if len(ids) == 0:
            return
        ctx = decision_context(g, ids)
        obs = observe(g, ctx, self.log.last_t)
        logp = torch.full((len(ids),), float("nan"), device=ids.device)
        v = torch.zeros(len(ids), device=ids.device)
        if self.net is not None:
            logits, v = self.net(obs)
        if self.mode == "teacher" or self.net is None:
            chosen = ctx["teacher"].clone()
            if self.net is not None:
                logp = joint_logp(logits, chosen)
        else:
            chosen, logp = sample(logits, greedy=self.mode == "greedy", gen=self.gen)
        live = ~self.ended[ids]
        chosen = torch.where(live.unsqueeze(-1), chosen, ctx["teacher"])
        ar = torch.arange(len(ids), device=ids.device)
        self.invalid += int((~ctx["joint"][ar, chosen[:, 0], chosen[:, 1]]).sum())
        g.c_need_more[ids] = ctx["need_more"]
        g.apply_assignment(ids, chosen, ctx["p"], ctx["nn"], ctx["pre"], ctx["t_route"])
        self.log.add(ctx, chosen, logp)
        sw = (chosen != ctx["cur"]).any(-1) & live
        tsw = (ctx["teacher"] != ctx["cur"]).any(-1) & live
        self.stats["decisions"] += int(live.sum())
        self.stats["switches"] += int(sw.sum())
        self.stats["teacher_switches"] += int(tsw.sum())
        self.stats["agree"] += int(((chosen == ctx["teacher"]).all(-1) & live).sum())
        if self.ro is None:
            return
        rec = live & self.record[ids]
        if not bool(rec.any()):
            return
        sel = rec.nonzero().flatten()
        e = ids[sel]
        t = ctx["t"][sel]
        # close each env's previous transition: R so far, elapsed time, bootstrap value of this state
        for i_, env in enumerate(e.tolist()):
            j = self.open[env]
            if j >= 0:
                row = self.ro.rows[j]
                row.update(R=float(self.R[env]), D=float(t[i_] - self.t_open[env]), v_next=float(v[sel[i_]]),
                           done=False, closed=True)
        sub = {k: x[sel] for k, x in obs.items()}
        new = self.ro.add(sub, [self.key_fn(int(x)) for x in e.tolist()], t, chosen[sel], logp[sel], v[sel])
        for env, j in zip(e.tolist(), new):
            self.open[env] = j
        self.t_open[e] = t
        self.R[e] = 0.0

    @torch.no_grad()
    def on_step(self, g, succ: torch.Tensor, fail: torch.Tensor, trunc: torch.Tensor, touching: torch.Tensor) -> None:
        """Per env step, after the evaluator's outcome flags: accumulate the discounted team reward into each
        env's open transition and close it at the episode's end (success, failure or the horizon; all three
        are treated as terminal, no bootstrap)."""
        rc, dt = self.rc, self.dt
        pe = g.pose_error()
        if self.pe_prev is None:
            self.pe_prev = pe.clone()
        live = ~self.ended
        r = rc.w_progress * (self.pe_prev - pe) - rc.w_time * dt - rc.w_collide * touching.float() * dt
        r = r - rc.w_deploy * 2.0 * dt
        r = r + rc.r_success * succ.float() - rc.r_fail * fail.float()
        disc = rc.gamma ** (g.c_time - self.t_open).clamp(min=0.0)
        self.R += torch.where(live, disc * r, torch.zeros_like(r))
        self.pe_prev = pe.clone()
        end = (succ | fail | trunc) & live
        if self.ro is not None and bool(end.any()):
            for env in end.nonzero().flatten().tolist():
                j = self.open[env]
                if j >= 0:
                    self.ro.rows[j].update(R=float(self.R[env]), D=float(g.c_time[env] - self.t_open[env]),
                                           v_next=0.0, done=True, closed=True,
                                           outcome="success" if bool(succ[env]) else "fail" if bool(fail[env]) else "horizon")
                    self.open[env] = -1
        self.ended |= end


def gae(rows: list[dict], rc: RewardCfg) -> tuple[torch.Tensor, torch.Tensor]:
    """Semi-MDP GAE per episode key (transitions in time order). Unclosed transitions (the batch ended
    first) get advantage 0 and are dropped by the caller (mask)."""
    n = len(rows)
    adv = torch.zeros(n)
    ret = torch.zeros(n)
    by = {}
    for i, r in enumerate(rows):
        by.setdefault(r["key"], []).append(i)
    for idx in by.values():
        idx.sort(key=lambda i: rows[i]["t"])
        a_next = 0.0
        for i in reversed(idx):
            r = rows[i]
            if not r["closed"]:
                a_next = 0.0
                continue
            gD = rc.gamma ** r["D"]
            nd = 0.0 if r["done"] else 1.0
            delta = r["R"] + gD * nd * r["v_next"] - r["v"]
            a = delta + (rc.gamma * rc.lam) ** r["D"] * nd * a_next
            adv[i] = a
            ret[i] = a + r["v"]
            a_next = a
    return adv, ret


def mc_returns(rows: list[dict], rc: RewardCfg) -> torch.Tensor:
    """Discounted returns (lambda = 1, no bootstrap) per episode key, for critic pre-training on teacher data."""
    out = torch.zeros(len(rows))
    by = {}
    for i, r in enumerate(rows):
        by.setdefault(r["key"], []).append(i)
    for idx in by.values():
        idx.sort(key=lambda i: rows[i]["t"])
        g_next = 0.0
        for i in reversed(idx):
            r = rows[i]
            g_next = r["R"] + (0.0 if r["done"] else rc.gamma ** r["D"] * g_next)
            out[i] = g_next
    return out


def imitation_metrics(logits: torch.Tensor, teacher: torch.Tensor, cur: torch.Tensor) -> dict:
    """Greedy prediction vs the teacher. KEEP dominates teacher decisions, so report switch decisions
    separately: switch recall (teacher switches, prediction also switches), exact pair accuracy on teacher
    switches, and the false-switch rate on teacher keeps."""
    m, K, _ = logits.shape
    flat = logits.view(m, -1).argmax(-1)
    pred = torch.stack([flat // K, flat % K], -1)
    exact = (pred == teacher).all(-1)
    tsw = (teacher != cur).any(-1)
    psw = (pred != cur).any(-1)
    f = lambda x: float(x.float().mean()) if x.numel() else float("nan")  # noqa: E731
    return dict(n=m, teacher_switch_share=f(tsw), exact=f(exact), exact_on_keep=f(exact[~tsw]),
                switch_recall=f(psw[tsw]), exact_on_switch=f(exact[tsw]), false_switch=f(psw[~tsw]))


def save_policy(path, net: PairPolicy, extra: dict | None = None):
    torch.save(dict(dims=net.dims, state=net.state_dict(), **(extra or {})), path)


def load_policy(path, device) -> PairPolicy:
    d = torch.load(path, map_location=device, weights_only=False)
    net = PairPolicy(**d["dims"]).to(device)
    net.load_state_dict(d["state"])
    net.eval()
    return net

