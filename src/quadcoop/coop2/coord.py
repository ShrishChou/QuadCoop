"""Contact-assignment coordinators over the frozen executor (design: docs/coordinator_design.md).

The env's command term (mdp.CoopPush2Command) keeps its decision schedule: at each eligible re-planning event it
calls g.coordinator(g, ids) for the expert-rule envs in ids instead of the expert's own re-selection. A coordinator

  1. builds the decision context (decision_context): the expert's proposal (the teacher label, computed without
     changing state), the candidate geometry and the joint validity mask, which always includes KEEP (the current
     pair);
  2. chooses a joint assignment autoregressively: robot 1 from its marginal mask (contacts with at least one valid
     partner), then robot 2 from the row of the joint mask fixed by robot 1's choice, so every sampled pair is valid;
  3. applies it through g.apply_assignment (the same function the expert uses) and logs the decision.

Withdraw (action index K) is reserved in the action layout. It is masked out until its execution exists
(design doc, stage W).
"""
from __future__ import annotations

import torch


def decision_context(g, ids: torch.Tensor) -> dict:
    """Everything a coordinator needs for envs ids (expert rule). Pure (no state change)."""
    prop = g._propose_expert(ids)
    m, K = prop["p"].shape[0], prop["p"].shape[1]
    ar = torch.arange(m, device=ids.device)
    cur = prop["cur"]
    joint = prop["use"].clone()
    joint[ar, cur[:, 0], cur[:, 1]] = True  # KEEP is always available
    prop.update(ids=ids, K=K, joint=joint, teacher=prop["new"], t=g.c_time[ids].clone())
    return prop


def first_mask(joint: torch.Tensor) -> torch.Tensor:
    """(m, K) robot 1's valid contacts: those with at least one valid partner contact."""
    return joint.any(2)


def second_mask(joint: torch.Tensor, a0: torch.Tensor) -> torch.Tensor:
    """(m, K) robot 2's valid contacts given robot 1's choice a0 (m,)."""
    return joint[torch.arange(len(a0), device=a0.device), a0]


def masked_logp(logits: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
    return torch.log_softmax(logits.masked_fill(~mask, -1e9), -1)


class DecisionLog:
    """Per-decision record: env, time, time since that env's previous decision, current / teacher / chosen pair,
    number of valid joint pairs, and the log-probability of the chosen pair (nan for deterministic coordinators).
    Kept on the CPU, appended in batches."""

    def __init__(self, n: int, device):
        self.last_t = torch.full((n,), float("nan"), device=device)
        self.rows: list[torch.Tensor] = []

    def add(self, ctx: dict, chosen: torch.Tensor, logp: torch.Tensor | None) -> None:
        ids = ctx["ids"]
        dt = ctx["t"] - self.last_t[ids]
        self.last_t[ids] = ctx["t"]
        lp = logp if logp is not None else torch.full_like(ctx["t"], float("nan"))
        n_valid = ctx["joint"].view(len(ids), -1).sum(-1).float()
        self.rows.append(torch.stack([ids.float(), ctx["t"], dt, *ctx["cur"].T.float(), *ctx["teacher"].T.float(),
                                      *chosen.T.float(), n_valid, lp], -1).cpu())

    def reset_envs(self, env_ids: torch.Tensor) -> None:
        self.last_t[env_ids] = float("nan")

    HEADER = ["env", "t", "dt", "cur_1", "cur_2", "teacher_1", "teacher_2", "chosen_1", "chosen_2", "n_valid", "logp"]

    def table(self) -> torch.Tensor:
        return torch.cat(self.rows) if self.rows else torch.zeros(0, len(self.HEADER))


class Coordinator:
    """Base: choose(ctx) -> (chosen (m, 2), logp (m,) or None); __call__ applies and logs."""

    def __init__(self, n: int, device):
        self.log = DecisionLog(n, device)
        self.invalid = 0  # chosen pairs outside the joint mask (must stay 0)

    def choose(self, ctx: dict):
        raise NotImplementedError

    def __call__(self, g, ids: torch.Tensor) -> None:
        if len(ids) == 0:
            return
        ctx = decision_context(g, ids)
        chosen, logp = self.choose(ctx)
        ar = torch.arange(len(ids), device=ids.device)
        self.invalid += int((~ctx["joint"][ar, chosen[:, 0], chosen[:, 1]]).sum())
        g.c_need_more[ids] = ctx["need_more"]
        g.apply_assignment(ids, chosen, ctx["p"], ctx["nn"], ctx["pre"], ctx["t_route"])
        self.log.add(ctx, chosen, logp)


class TeacherCoordinator(Coordinator):
    """The expert's own choice, routed through the coordinator path (integration check: must reproduce the expert)."""

    def choose(self, ctx):
        return ctx["teacher"], None


class RandomCoordinator(Coordinator):
    """Uniform over valid choices, autoregressive (robot 1, then robot 2 given robot 1); keep_p = probability of
    KEEP. Checks that arbitrary valid assignments execute and that masks hold."""

    def __init__(self, n: int, device, keep_p: float = 0.5, seed: int = 0):
        super().__init__(n, device)
        self.keep_p = keep_p
        self.gen = torch.Generator(device=device).manual_seed(seed)

    def choose(self, ctx):
        joint, cur = ctx["joint"], ctx["cur"]
        m = joint.shape[0]
        z = torch.zeros(joint.shape[:2], device=joint.device)
        m0 = first_mask(joint)
        a0 = torch.multinomial(torch.softmax(z.masked_fill(~m0, -1e9), -1), 1, generator=self.gen).squeeze(-1)
        m1 = second_mask(joint, a0)
        a1 = torch.multinomial(torch.softmax(z.masked_fill(~m1, -1e9), -1), 1, generator=self.gen).squeeze(-1)
        lp = masked_logp(z, m0).gather(1, a0[:, None]).squeeze(1) + masked_logp(z, m1).gather(1, a1[:, None]).squeeze(1)
        keep = torch.rand(m, device=joint.device, generator=self.gen) < self.keep_p
        chosen = torch.where(keep.unsqueeze(-1), cur, torch.stack([a0, a1], -1))
        lp = torch.where(keep, torch.zeros_like(lp), lp)  # mixture: logged for the record only
        return chosen, lp


class ParityCoordinator(Coordinator):
    """Identical-input check of the refactor: at every decision, snapshot every env-state tensor, run the expert's
    own re-selection (g._reselect_expert), record the result, restore the snapshot, then run the teacher through the
    coordinator path (propose -> apply). Both see exactly the same inputs; any difference in the resulting state is a
    refactor error, not physics. The coordinator path's result is kept. self.mismatch counts differing tensors per
    attribute name; self.checked counts decisions."""

    def __init__(self, n: int, device):
        super().__init__(n, device)
        self.mismatch: dict[str, int] = {}
        self.checked = 0

    def choose(self, ctx):
        return ctx["teacher"], None

    @staticmethod
    def _state(g) -> dict:
        return {k: v.clone() for k, v in vars(g).items() if isinstance(v, torch.Tensor)}

    def __call__(self, g, ids: torch.Tensor) -> None:
        if len(ids) == 0:
            return
        pre = self._state(g)
        g._reselect_expert(ids)
        ref = self._state(g)
        for k, v in pre.items():
            getattr(g, k).copy_(v)
        super().__call__(g, ids)
        for k, v in ref.items():
            new = getattr(g, k)
            if new.shape != v.shape or not torch.equal(new, v):
                self.mismatch[k] = self.mismatch.get(k, 0) + 1
        self.checked += len(ids)


class RegretCoordinator(Coordinator):
    """Regret minimization inside the expert's re-planning (docs/regret_replanning.md). The expert's schedule and
    triggers are unchanged (timer, no progress, weak pair, finish, slow arrival); at each re-plan this coordinator
    picks one of A options built from the expert's own cost table J:
      0 expert   the expert's decision (its margin and finishing-zone rules included)
      1 keep     the current pair
      2 second   the cheapest pair other than the expert's choice and the current pair
      3 third    the next cheapest
    (an option that does not exist falls back to the expert's.) Exp3 per context
    (object x heavy x re-plan triggered by a stall x finishing zone): play p = (1 - gamma) softmax(log w) + gamma / A.
    Payoff of a decision, settled at the env's next decision or episode end: progress rate of the pose error
    (distance + rho x heading error) mapped to [0, 1] as 0.5 + 0.25 x rate / v_ref, clipped; failure 0, success 1.
    Settled decisions update log w by eta x the context's importance-weighted mean payoff (one round per context per
    batch). mode exp3 (learn while planning) or frozen (softmax of a loaded state, no exploration, no learning)."""

    ARMS = ("expert", "keep", "second", "third")

    def __init__(self, n: int, device, n_shapes: int, mass: float, mode: str = "exp3", gamma: float = 0.1,
                 eta: float = 0.1, v_ref: float = 0.1, seed: int = 0, state: dict | None = None):
        super().__init__(n, device)
        self.A, self.mode, self.gamma, self.eta, self.v_ref = len(self.ARMS), mode, gamma, eta, v_ref
        self.n_shapes = n_shapes
        self.n_ctx = n_shapes * 8
        self.gen = torch.Generator(device=device).manual_seed(seed)
        z = lambda *s: torch.zeros(*s, device=device)  # noqa: E731
        self.logw, self.plays, self.rsum, self.psum = z(self.n_ctx, self.A), z(self.n_ctx, self.A), z(self.n_ctx, self.A), z(self.n_ctx, self.A)
        self.rounds = 0
        if state is not None:
            for k in ("logw", "plays", "rsum", "psum"):
                getattr(self, k).copy_(state[k].to(device))
            self.rounds = int(state.get("rounds", 0))
        self.heavy = mass > 50.0
        self.pending = torch.zeros(n, dtype=torch.bool, device=device)
        self.p_ctx = torch.zeros(n, dtype=torch.long, device=device)
        self.p_arm = torch.zeros(n, dtype=torch.long, device=device)
        self.p_prob = torch.ones(n, device=device)
        self.p_pe = z(n)
        self.p_t = z(n)
        self.ended = torch.zeros(n, dtype=torch.bool, device=device)
        self.arm_count = z(n, self.A)
        self.differs = z(n)  # decisions where the chosen pair is not the expert's

    def probs(self, ctx_idx: torch.Tensor) -> torch.Tensor:
        p = torch.softmax(self.logw[ctx_idx], -1)
        return (1.0 - self.gamma) * p + self.gamma / self.A if self.mode == "exp3" else p

    def _settle(self, g, ids: torch.Tensor, outcome: torch.Tensor | None = None) -> None:
        """Pay the pending decisions of envs ids; outcome (len ids): None = progress, else 0 (failed) / 1 (success)."""
        sel = self.pending[ids]
        if not bool(sel.any()):
            return
        e = ids[sel]
        pe = g.pose_error()[e]
        dt = (g.c_time[e] - self.p_t[e]).clamp(min=0.5)
        u = (0.5 + 0.25 * (self.p_pe[e] - pe) / dt / self.v_ref).clamp(0.0, 1.0)
        if outcome is not None:
            u = outcome[sel]
        self.pending[e] = False
        c, k = self.p_ctx[e], self.p_arm[e]
        self.plays.index_put_((c, k), torch.ones_like(u), accumulate=True)
        self.rsum.index_put_((c, k), u, accumulate=True)
        if self.mode != "exp3":
            return
        nc = torch.zeros(self.n_ctx, device=u.device).index_add_(0, c, torch.ones_like(u))
        est = torch.zeros(self.n_ctx, self.A, device=u.device)
        est.index_put_((c, k), u / self.p_prob[e].clamp(min=1e-6), accumulate=True)
        on = nc > 0
        self.psum += self.probs(torch.arange(self.n_ctx, device=u.device)) * nc.unsqueeze(-1)
        self.logw[on] += self.eta * est[on] / nc[on].unsqueeze(-1)
        self.logw -= self.logw.max(-1, keepdim=True).values
        self.rounds += 1

    def __call__(self, g, ids: torch.Tensor) -> None:
        if len(ids) == 0:
            return
        live = ids[~self.ended[ids]]
        self._settle(g, live)
        ctx = decision_context(g, ids)
        m, K = len(ids), ctx["K"]
        ar = torch.arange(m, device=ids.device)
        teacher, cur, joint = ctx["teacher"], ctx["cur"], ctx["joint"]
        J = torch.where(ctx["use"], ctx["J"], torch.full_like(ctx["J"], float("inf"))).view(m, -1)
        order = J.argsort(-1)[:, :8]
        tf = teacher[:, 0] * K + teacher[:, 1]
        cf = cur[:, 0] * K + cur[:, 1]
        opts = torch.stack([tf, cf, tf, tf], -1)
        Jo = J.gather(1, order)
        for r in range(m):  # few decisions per call
            got = [int(x) for x, v in zip(order[r].tolist(), Jo[r].tolist())
                   if v < float("inf") and x != int(tf[r]) and x != int(cf[r])][:2]
            for q, x in enumerate(got):
                opts[r, 2 + q] = x
        stalled = g.c_stalled[ids].long()
        zone = ctx["zone"].long()
        cidx = (g.shape[ids] * 8 + int(self.heavy) * 4 + stalled * 2 + zone).clamp(max=self.n_ctx - 1)
        p = self.probs(cidx)
        arm = torch.multinomial(p, 1, generator=self.gen).squeeze(-1)
        pick = opts.gather(1, arm.unsqueeze(-1)).squeeze(-1)
        chosen = torch.stack([pick // K, pick % K], -1)
        ok = joint[ar, chosen[:, 0], chosen[:, 1]]
        chosen = torch.where(ok.unsqueeze(-1), chosen, teacher)
        self.invalid += int((~joint[ar, chosen[:, 0], chosen[:, 1]]).sum())
        g.c_need_more[ids] = ctx["need_more"]
        g.apply_assignment(ids, chosen, ctx["p"], ctx["nn"], ctx["pre"], ctx["t_route"])
        self.log.add(ctx, chosen, torch.log(p.gather(1, arm.unsqueeze(-1)).squeeze(-1)))
        keep = ~self.ended[ids]
        e = ids[keep]
        self.pending[e] = True
        self.p_ctx[e], self.p_arm[e] = cidx[keep], arm[keep]
        self.p_prob[e] = p.gather(1, arm.unsqueeze(-1)).squeeze(-1)[keep]
        self.p_pe[e] = g.pose_error()[e]
        self.p_t[e] = g.c_time[e]
        self.arm_count[e, arm[keep]] += 1.0
        self.differs[e] += (chosen != teacher).any(-1)[keep].float()

    def on_step(self, g, succ, fail, timeout, touching) -> None:
        """Episode ends settle the pending decision: success pays 1, a failure 0, a timeout its progress."""
        new_end = (succ | fail | timeout) & ~self.ended
        if bool(new_end.any()):
            ids = new_end.nonzero().flatten()
            out = torch.where(succ[ids], torch.ones(len(ids), device=ids.device),
                              torch.where(fail[ids], torch.zeros(len(ids), device=ids.device),
                                          torch.full((len(ids),), float("nan"), device=ids.device)))
            to = torch.isnan(out)
            if bool(to.any()):
                self._settle(g, ids[to])
            if bool((~to).any()):
                self._settle(g, ids[~to], out[~to])
            self.ended |= new_end

    def state(self) -> dict:
        return {"arms": self.ARMS, "logw": self.logw.cpu(), "plays": self.plays.cpu(), "rsum": self.rsum.cpu(),
                "psum": self.psum.cpu(), "rounds": self.rounds, "n_shapes": self.n_shapes, "gamma": self.gamma,
                "eta": self.eta, "v_ref": self.v_ref}

    def report(self, shape_names) -> str:
        pf = torch.softmax(self.logw, -1).cpu()
        pl, rs = self.plays.cpu(), self.rsum.cpu()
        L = [f"rounds {self.rounds}; options {', '.join(self.ARMS)}",
             "| object | heavy | stalled | finishing | decisions | mean payoff per option | strategy |", "|---|---|---|---|---|---|---|"]
        for c in range(self.n_ctx):
            n = int(pl[c].sum())
            if n == 0:
                continue
            s, r = divmod(c, 8)
            h, r = divmod(r, 4)
            st, zn = divmod(r, 2)
            mp = " ".join("–" if pl[c, k] == 0 else f"{float(rs[c, k] / pl[c, k]):.2f}" for k in range(self.A))
            L.append(f"| {shape_names[s] if s < len(shape_names) else s} | {h} | {st} | {zn} | {n} | {mp} | "
                     + " ".join(f"{float(x):.2f}" for x in pf[c]) + " |")
        return "\n".join(L)
