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
