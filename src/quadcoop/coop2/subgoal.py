"""Regret-minimizing subgoal planner for a learned pair (scripts/eval_coop2.py --subgoal).

The pair's policy is trained to push the object to a goal 3-5 m away. This planner sits above it and, instead of the
true goal, shows the policy a *subgoal* chosen from a small menu of moves (the arms). The subgoal is a "carrot":
it is recomputed every step from the object's current pose, so the policy never reaches it and stops; once the
object is within the look-ahead of the true goal, every arm hands over the true goal.

Arms (L = look-ahead, u = unit vector object -> goal, e = folded heading error to the goal):
  direct      the true goal (the pair on its own: the baseline)
  straight    L ahead along u; heading eased toward the goal in proportion L / distance
  translate   L ahead along u; keep the current heading (turn only in the last 0.5 m)
  rotate      stay where the object is; turn up to 45 deg toward the goal heading
  arc_left    L ahead along u rotated +35 deg; heading as straight
  arc_right   L ahead along u rotated -35 deg; heading as straight

Every `dt` seconds (an epoch) each live episode picks an arm. The payoff of an epoch is progress on the true goal,
mapped to [0, 1]:  0.5 + 0.25 * (distance gained / (v_ref dt) + heading gained / (w_ref dt)), clipped; a fall,
tip or lost object during the epoch pays 0, success pays 1.

The learner is Exp3 (bandit feedback: only the payoff of the arm actually played is seen) with one weight vector
per context. A context is the situation the choice is made in:
  distance to goal   > 1.5 m | 0.5-1.5 m | < 0.5 m
  heading error      < 15 deg | >= 15 deg
  stalled            the previous epoch paid < 0.55 (made almost no progress): the "stuck" signal
  heavy              object over 50 kg
(3 x 2 x 2 x 2 = 24 contexts.) The episodes run in parallel, so one epoch is one round for every context that has
live episodes in it: the round's reward estimate for arm k is the mean over that context's episodes of
1{played k} * payoff / p(k) (unbiased), and log w[k] += eta * estimate. Play is p = (1 - gamma) softmax(log w)
+ gamma / K. The running average of p (weighted by episodes) is kept as the average strategy.

Modes:  fixed:<arm>  always that arm        exp3     learn while playing (state can be loaded and saved)
        frozen       play softmax(log w) of a loaded state, no exploration, no learning
"""
from __future__ import annotations

import math
from pathlib import Path

import torch

from quadcoop.stage1.mdp import yaw_of

ARMS = ("direct", "straight", "translate", "rotate", "arc_left", "arc_right")
N_CTX = 24


def _wrap(x: torch.Tensor) -> torch.Tensor:
    return torch.atan2(torch.sin(x), torch.cos(x))


def ctx_name(c: int) -> str:
    heavy, r = divmod(c, 12)
    db, r = divmod(r, 4)
    yb, st = divmod(r, 2)
    return (f"{'heavy' if heavy else 'light'} | {('>1.5 m', '0.5-1.5 m', '<0.5 m')[db]} | "
            f"{('yaw<15', 'yaw>=15')[yb]} | {'stalled' if st else 'moving'}")


class SubgoalPlanner:
    def __init__(self, n: int, device, mode: str, dt: float = 2.0, look: float = 1.5, gamma: float = 0.1,
                 eta: float = 0.1, v_ref: float = 0.25, w_ref_deg: float = 10.0, seed: int = 0,
                 load: str | None = None, learn: bool | None = None):
        self.n, self.dev, self.mode = n, device, mode
        self.K = len(ARMS)
        self.fixed = None
        if mode.startswith("fixed:"):
            arm = mode.split(":", 1)[1]
            assert arm in ARMS, f"unknown arm {arm}; choose from {ARMS}"
            self.fixed = ARMS.index(arm)
        else:
            assert mode in ("exp3", "frozen"), f"unknown subgoal mode {mode}"
        self.dt, self.look, self.gamma, self.eta = dt, look, gamma, eta
        self.v_ref, self.w_ref = v_ref, math.radians(w_ref_deg)
        self.learn = (mode == "exp3") if learn is None else learn
        self.gen = torch.Generator(device=device).manual_seed(seed)
        z = lambda *s: torch.zeros(*s, device=device)  # noqa: E731
        self.logw, self.psum, self.plays, self.rsum = z(N_CTX, self.K), z(N_CTX, self.K), z(N_CTX, self.K), z(N_CTX, self.K)
        self.rounds = 0
        if load:
            st = torch.load(load, map_location=device, weights_only=False)
            assert tuple(st["arms"]) == ARMS, "planner state has other arms"
            for k in ("logw", "psum", "plays", "rsum"):
                getattr(self, k).copy_(st[k].to(device))
            self.rounds = int(st.get("rounds", 0))
        self.final_xy = z(n, 2)
        self.final_yaw = z(n)
        self.sym = torch.zeros(n, dtype=torch.long, device=device)
        self.arm = torch.zeros(n, dtype=torch.long, device=device)
        self.p_arm = torch.ones(n, device=device)
        self.ctx = torch.zeros(n, dtype=torch.long, device=device)
        self.stalled = torch.zeros(n, dtype=torch.bool, device=device)
        self.d0, self.e0 = z(n), z(n)
        self.bad = torch.zeros(n, dtype=torch.bool, device=device)  # fell / tipped / lost this epoch
        self.won = torch.zeros(n, dtype=torch.bool, device=device)  # succeeded this epoch
        self.arm_steps = z(n, self.K)
        self.switches = z(n)
        self.payoff_sum, self.epochs = z(n), z(n)
        self.t_next = 0.0
        self.heavy = False
        self.started = False

    # -- the true goal ------------------------------------------------------------------------------
    def begin(self, g, mass: float) -> None:
        """After the env reset: remember the true goal (the subgoal replaces it only inside the policy step)."""
        self.final_xy.copy_(g.goal_xy)
        self.final_yaw.copy_(g.goal_yaw)
        self.heavy = mass > 50.0
        self.arm_steps.zero_()
        self.switches.zero_()
        self.payoff_sum.zero_()
        self.epochs.zero_()
        self.stalled.zero_()
        self.bad.zero_()
        self.won.zero_()
        self.t_next = 0.0
        self.started = False

    def restore(self, g) -> None:
        g.goal_xy.copy_(self.final_xy)
        g.goal_yaw.copy_(self.final_yaw)

    def _final_errors(self, g) -> tuple[torch.Tensor, torch.Tensor]:
        self.restore(g)
        return g.errors()

    # -- choices --------------------------------------------------------------------------------
    def _context(self, d: torch.Tensor, e: torch.Tensor) -> torch.Tensor:
        db = torch.where(d > 1.5, 0, torch.where(d > 0.5, 1, 2))
        yb = (e.abs() >= math.radians(15.0)).long()
        return (12 if self.heavy else 0) + db * 4 + yb * 2 + self.stalled.long()

    def probs(self, ctx: torch.Tensor) -> torch.Tensor:
        if self.fixed is not None:
            p = torch.zeros(ctx.numel(), self.K, device=self.dev)
            p[:, self.fixed] = 1.0
            return p
        p = torch.softmax(self.logw[ctx], -1)
        if self.mode == "exp3":
            p = (1.0 - self.gamma) * p + self.gamma / self.K
        return p

    def _decide(self, g, live: torch.Tensor) -> None:
        d, e = self._final_errors(g)
        self.d0.copy_(d)
        self.e0.copy_(e.abs())
        self.ctx.copy_(self._context(d, e))
        p = self.probs(self.ctx)
        new = torch.multinomial(p, 1, generator=self.gen).squeeze(-1)
        self.switches += ((new != self.arm) & live & torch.tensor(self.started, device=self.dev)).float()
        self.arm = torch.where(live, new, self.arm)
        self.p_arm = p.gather(-1, self.arm.unsqueeze(-1)).squeeze(-1)
        self.bad.zero_()
        self.won.zero_()
        self.started = True

    def _settle(self, g, live: torch.Tensor) -> None:
        """Pay the epoch that just ended and (exp3) update the weights, one round per context."""
        d, e = self._final_errors(g)
        score = (self.d0 - d) / (self.v_ref * self.dt) + (self.e0 - e.abs()) / (self.w_ref * self.dt)
        u = (0.5 + 0.25 * score).clamp(0.0, 1.0)
        u = torch.where(self.bad, torch.zeros_like(u), u)
        u = torch.where(self.won, torch.ones_like(u), u)
        played = live | self.won | self.bad  # episodes that were live when the epoch began
        self.stalled = u < 0.55
        self.payoff_sum += torch.where(played, u, torch.zeros_like(u))
        self.epochs += played.float()
        if self.fixed is not None or not bool(played.any()):
            return
        c, k = self.ctx[played], self.arm[played]
        uu, pp = u[played], self.p_arm[played]
        nc = torch.zeros(N_CTX, device=self.dev).index_add_(0, c, torch.ones_like(uu))
        est = torch.zeros(N_CTX, self.K, device=self.dev)
        est.index_put_((c, k), uu / pp.clamp(min=1e-6), accumulate=True)
        self.plays.index_put_((c, k), torch.ones_like(uu), accumulate=True)
        self.rsum.index_put_((c, k), uu, accumulate=True)
        on = nc > 0
        p_ctx = self.probs(torch.arange(N_CTX, device=self.dev))
        self.psum += p_ctx * nc.unsqueeze(-1)
        if self.learn:
            self.logw[on] += self.eta * est[on] / nc[on].unsqueeze(-1)
            self.logw -= self.logw.max(-1, keepdim=True).values  # keep it bounded
            self.rounds += 1

    def observe(self, succ: torch.Tensor, bad: torch.Tensor) -> None:
        """After each env step: episodes that just succeeded / failed (fell, tipped, lost)."""
        self.won |= succ
        self.bad |= bad

    # -- per step -------------------------------------------------------------------------------
    def apply(self, g, t: float, live: torch.Tensor) -> None:
        """Before the env step at time t: settle / decide at epoch boundaries, then put the subgoal in g."""
        if t + 1e-6 >= self.t_next:
            if self.started:
                self._settle(g, live)
            self._decide(g, live)
            self.t_next = t + self.dt
        self.restore(g)
        bp = g.box_pos()[:, :2]
        _, e = g.errors()  # signed, folded: the turn still wanted
        h = yaw_of(g.box_quat())  # the yaw errors() measures against
        r = self.final_xy - bp
        D = torch.linalg.norm(r, dim=-1)
        u = r / D.clamp(min=1e-6).unsqueeze(-1)
        L = torch.minimum(D, torch.full_like(D, self.look))
        frac = (L / D.clamp(min=1e-6)).clamp(max=1.0)
        near = D <= self.look
        ease = _wrap(h + e * frac)

        def rot(v, deg):
            c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
            return torch.stack([c * v[:, 0] - s * v[:, 1], s * v[:, 0] + c * v[:, 1]], -1)

        cand_xy = torch.stack([self.final_xy, bp + u * L.unsqueeze(-1), bp + u * L.unsqueeze(-1), bp.clone(),
                               bp + rot(u, 35.0) * L.unsqueeze(-1), bp + rot(u, -35.0) * L.unsqueeze(-1)], 1)
        cap = math.radians(45.0)
        cand_yaw = torch.stack([self.final_yaw, ease, torch.where(D > 0.5, h, self.final_yaw),
                                _wrap(h + e.clamp(-cap, cap)), ease, ease], 1)
        sel = self.arm.view(-1, 1, 1).expand(-1, 1, 2)
        sx = cand_xy.gather(1, sel).squeeze(1)
        sy = cand_yaw.gather(1, self.arm.view(-1, 1)).squeeze(1)
        # near the goal every arm but rotate hands over the true goal; finished episodes keep the true goal
        hand = (near & (self.arm != ARMS.index("rotate"))) | ~live
        g.goal_xy.copy_(torch.where(hand.unsqueeze(-1), self.final_xy, sx))
        g.goal_yaw.copy_(torch.where(hand, self.final_yaw, sy))
        self.arm_steps.scatter_add_(1, self.arm.view(-1, 1), live.float().view(-1, 1))

    # -- outputs --------------------------------------------------------------------------------
    def row(self, j: int) -> dict:
        s = self.arm_steps[j]
        tot = float(s.sum())
        out = {f"sg_frac_{a}": (round(float(s[k]) / tot, 3) if tot > 0 else "") for k, a in enumerate(ARMS)}
        out["sg_switches"] = int(self.switches[j])
        out["sg_mean_payoff"] = round(float(self.payoff_sum[j] / self.epochs[j].clamp(min=1)), 3)
        return out

    def state(self) -> dict:
        return {"arms": ARMS, "logw": self.logw.cpu(), "psum": self.psum.cpu(), "plays": self.plays.cpu(),
                "rsum": self.rsum.cpu(), "rounds": self.rounds, "mode": self.mode, "dt": self.dt, "look": self.look,
                "gamma": self.gamma, "eta": self.eta}

    def save(self, path: Path) -> None:
        torch.save(self.state(), path)

    def report(self) -> str:
        """Per context: plays, mean payoff per arm, final and average strategy."""
        pf = torch.softmax(self.logw, -1).cpu()
        pa = (self.psum / self.psum.sum(-1, keepdim=True).clamp(min=1e-9)).cpu()
        pl, rs = self.plays.cpu(), self.rsum.cpu()
        L = [f"rounds {self.rounds}; arms {', '.join(ARMS)}",
             "| context | plays | mean payoff per arm | final strategy | average strategy |", "|---|---|---|---|---|"]
        for c in range(N_CTX):
            n = int(pl[c].sum())
            if n == 0:
                continue
            mp = " ".join("–" if pl[c, k] == 0 else f"{float(rs[c, k] / pl[c, k]):.2f}" for k in range(self.K))
            L.append(f"| {ctx_name(c)} | {n} | {mp} | " + " ".join(f"{float(x):.2f}" for x in pf[c]) + " | "
                     + " ".join(f"{float(x):.2f}" for x in pa[c]) + " |")
        return "\n".join(L)
