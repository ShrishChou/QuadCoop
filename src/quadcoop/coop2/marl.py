"""IPPO and MAPPO for the two-robot Stage 2 task, in one trainer.

Both use the same environment, rollouts, PPO losses, hyperparameters and warm start; they differ
only in the critic:

    ippo   each robot has its own critic on its own observation (+ the object's mass and
           friction, which both critics get): V_i(o_i, z). Each critic starts as that robot's
           Stage 2b critic (partner inputs at zero weight).
    mappo  one centralized critic sees both robots' observations and maps (+ the same physics)
           and outputs one value per robot: V(o_1, o_2, z). It starts fresh.

Actors are always decentralized and separate (the robots differ): each sees only its own
observation (its Stage 2b input + the partner's 9 numbers). Each starts as that robot's Stage 2b
policy - CNN encoders, MLP, normalizer and action noise - with the partner inputs at zero
weight, so iteration 0 is exactly the two single-robot policies side by side (model_0.pt, the
"frozen pair" baseline). Loading is strict: anything that does not map is an error.

Stage 4 (``contacts``): each actor's input also has the robot's assigned contact and the
partner's (9 numbers after the partner's 9), at zero weight after the warm start like the partner
inputs; ``kl_ramp`` fades the Stage 2b anchor out, since Stage 2b would rather push from its own
favourite spot than from an assigned contact.

Rewards: each robot gets the env's team terms plus its own terms (reward terms whose names end
in _anymal / _spot), read from the reward manager every step.

Stability around the warm start: critics train alone for ``critic_warmup`` iterations; the
actors' observation normalizers stay as loaded (the partner inputs are O(1) already); actor
learning rates start low and adapt to the KL target; the action noise is floored at
``min_std``. Checkpoints: logs/marl2/<run>/model_<iter>.pt (with the curriculum state).

Exploration where outputs are saturated (``mean_clip``, ``bound_coef``; r6): the warm-started
policies put many outputs far past the walker's [-1, 1] clip (ANYmal: 4-8), where sampling noise
changes nothing the robot does, so those outputs get no learning signal. With ``mean_clip`` the
Gaussian that actions are sampled from (and scored under) is centred on the mean clamped to
+-mean_clip, with the gradient passed straight through the clamp, so the noise acts on the
command again. The deterministic output (evaluation) is the raw mean, unchanged: iteration 0
still acts exactly like the Stage 2b policies. ``bound_coef`` adds a penalty on the raw mean
past +-mean_clip so it comes back inside instead of sitting where the clamp hides it.

Anchored to the Stage 2 policies (``kl_ref`` = beta > 0): each actor's loss adds
beta * KL(pi || pi_2b), the KL divergence from that robot's frozen Stage 2b policy (the warm-start
source, rebuilt from cfg.init on every start and resume), on the same observations. This is
KL-regularized RL (the objective behind RLHF): maximize reward while staying close to a reference
policy, so fine-tuning cannot drift away from the single-robot skill unless the reward clearly
pays for it. Both means are clamped to +-1.1 first: outputs past the walker's clip do the same
thing whatever their value, so only differences in what the robots actually do count.
With ``kl_partner_scale`` < 1 the anchor is partner-aware: per sample, beta is multiplied by
kl_partner_scale while the partner is within kl_partner_near m, rising linearly to full beta at
kl_partner_far m (partner distance from the noise-free state input). Alone, each robot stays its
Stage 2b self; near its partner it is free to change (e.g. to take another contact point).

From scratch (``scratch``): no Stage 2 policies at all. Actors and critics start from random
weights on top of the same frozen walkers, the actors' observation normalizers learn from the
data (they are frozen only after a warm start), and the action noise is capped at
max_std_factor x its starting value (``_dist_cfg``'s init_std). Same environment, rewards and PPO
settings otherwise, so it isolates what the single-robot warm start contributes.
"""

from __future__ import annotations

import re
import time
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from pathlib import Path

import torch
from tensordict import TensorDict

from quadcoop.coop2.mdp import AGENTS

N_SINGLE = 42  # Stage 2 actor numbers (the critic's are these + 3 physics)
N_PARTNER = 9
N_PHYS = 3
CNN = {"output_channels": (16, 32, 16), "kernel_size": (5, 3, 3), "stride": 2, "padding": "zeros",
       "activation": "elu"}  # Stage 2's encoder (quadcoop/stage2/rl_cfg.py)


@dataclass
class MarlCfg:
    algo: str = "mappo"  # "ippo" | "mappo"
    variant: str = "b"  # "b" (maps, CNN) | "ctrl" (numbers only)
    partner_map: bool = False  # env option (recorded so evaluations rebuild the same env)
    reward_set: str = "r3"  # env option, see quadcoop/coop2/env_cfg.py
    pair: str = "mixed"  # which two robots (quadcoop/coop2/pairs.py), recorded for evaluations
    num_envs: int = 4096
    num_steps_per_env: int = 24
    max_iterations: int = 6000
    num_learning_epochs: int = 5
    num_mini_batches: int = 4
    clip_param: float = 0.2
    gamma: float = 0.99
    lam: float = 0.95
    actor_learning_rate: float = 1.0e-4  # starting value; adapted to desired_kl
    critic_learning_rate: float = 3.0e-4
    desired_kl: float = 0.01
    # No entropy bonus by default: the warm-started policies' outputs sit mostly past the walker's
    # clip, where extra noise costs nothing, so a bonus only inflated the action noise (r2: std
    # 1 -> 2 in 700 iterations). Noise is also capped at its warm-start value (max_std_factor).
    entropy_coef: float = 0.0
    value_loss_coef: float = 1.0
    max_grad_norm: float = 1.0
    hidden_dims: tuple[int, ...] = (256, 128, 64)  # Stage 2's (actors and IPPO critics)
    central_hidden_dims: tuple[int, ...] = (512, 256, 128)  # MAPPO's critic
    min_std: float = 0.2
    mean_clip: float = 0.0  # > 0: sample around the mean clamped to +-this (straight-through); r6: 1.1
    bound_coef: float = 0.0  # penalty on the raw mean past +-mean_clip (or +-1.1 if mean_clip is 0); r6: 0.01
    scratch: bool = False  # random initial actors and critics (no Stage 2 warm start); see the module docstring
    kl_ref: float = 0.0  # beta of the KL penalty to the frozen Stage 2b policies (0 = off); see the module docstring
    kl_ref_clip: float = 1.1  # means clamped to +-this before the KL (the walker clips at 1)
    kl_partner_scale: float = 1.0  # < 1: beta x this near the partner (partner-aware anchor; 1 = off)
    kl_partner_near: float = 1.5  # m: full relaxation within this partner distance
    kl_partner_far: float = 3.0  # m: full beta beyond this partner distance
    start_mode: str = "behind"  # env option (recorded): robots' start, "behind" or "around"
    need_frac: float = 0.0  # env option (recorded): share of episodes that need both robots
    contacts: bool = False  # env option (recorded): Stage 4 contact mode (assigned contacts as inputs)
    contact_mix: tuple = (1.0, 1.0, 1.0)  # env option (recorded): spread / adjacent / random pairs
    contact_start_at: float = 0.7  # env option (recorded)
    tol_levels: tuple = ()  # env option (recorded): success-tolerance curriculum
    kl_ramp: int = 0  # > 0: the KL anchor's beta falls linearly from kl_ref to 0 over this many iterations
    max_std_factor: float = 1.0  # action noise may fall, but not rise above factor x its starting value
    max_actor_learning_rate: float = 3.0e-4
    reward_clip: float = 100.0  # per robot per step (a success is +50 at most, a fall -35)
    obs_clip: float = 100.0  # observations are clamped to +-this (and NaN/inf -> 0) before use
    critic_warmup: int = 100
    save_interval: int = 100
    video_interval: int = 500
    video_length: int = 1000
    seed: int = 0
    init: dict = field(default_factory=dict)  # agent -> Stage 2 checkpoint
    inputs: dict = field(default_factory=dict)  # what was used (models.yaml roles), for the record


def _dist_cfg(init_std: float = 0.6) -> dict:
    return {"class_name": "GaussianDistribution", "init_std": init_std, "std_type": "scalar"}


def actor_groups(a: str, variant: str) -> list[str]:
    return [f"actor_{a}"] + ([f"top_{a}", "front"] if variant == "b" else [])


def critic_groups(algo: str, variant: str, a: str | None = None) -> list[str]:
    if algo == "ippo":
        return [f"state_{a}", "privileged"] + ([f"top_{a}", "front"] if variant == "b" else [])
    return [f"state_{x}" for x in AGENTS] + ["privileged"] + \
        ([f"top_{x}" for x in AGENTS] + ["front"] if variant == "b" else [])


def make_model(obs: TensorDict, groups: list[str], out: int, hidden, variant: str, stochastic: bool):
    from rsl_rl.models.cnn_model import CNNModel
    from rsl_rl.models.mlp_model import MLPModel

    kw = dict(hidden_dims=hidden, activation="elu", obs_normalization=True,
              distribution_cfg=_dist_cfg() if stochastic else None)
    if variant == "b":
        return CNNModel(obs, {"x": groups}, "x", out, cnn_cfg=dict(CNN), **kw)
    return MLPModel(obs, {"x": groups}, "x", out, **kw)


def clamp_sampling_mean(model, limit: float) -> None:
    """Sample (and score) actions around the mean clamped to +-limit, the gradient passing straight
    through the clamp. The raw mean stays available as ``model.distribution.raw_mean`` and is
    still the deterministic output. Weights and checkpoints are unchanged."""
    dist = model.distribution
    plain_update = dist.update

    def update(mlp_output: torch.Tensor) -> None:
        dist.raw_mean = mlp_output
        plain_update(mlp_output + (mlp_output.clamp(-limit, limit) - mlp_output).detach())

    dist.update = update


def warm_start_model(model, single: dict, cols: list[tuple[slice, slice]], n1d_new: int, cnn_names: dict[str, str],
                     min_std: float | None, what: str) -> list[str]:
    """Copy a Stage 2 network (state dict `single`) into `model`.

    cols: (old columns, new columns) pairs for the 1D inputs; every other new 1D column starts at
    zero weight (normalizer mean 0, std 1). The CNN-feature columns follow the 1D ones in both.
    cnn_names: old CNN name -> new (e.g. profile_top -> top_spot). Raises if any weight of
    either network is left unmatched."""
    new = model.state_dict()
    used, done = set(), set()
    padded = []
    W_old, W_new = single["mlp.0.weight"], new["mlp.0.weight"]
    n1d_old = single["obs_normalizer._mean"].shape[-1]
    n_cnn_old, n_cnn_new = W_old.shape[1] - n1d_old, W_new.shape[1] - n1d_new
    if n_cnn_old != n_cnn_new:
        raise RuntimeError(f"{what}: CNN features {n_cnn_old} in the checkpoint, {n_cnn_new} here")
    W = torch.zeros_like(W_new)
    for o, nw in cols:
        W[:, nw] = W_old[:, o]
    W[:, n1d_new:] = W_old[:, n1d_old:]
    new["mlp.0.weight"] = W
    used.add("mlp.0.weight"), done.add("mlp.0.weight")
    for key in ("obs_normalizer._mean", "obs_normalizer._var", "obs_normalizer._std"):
        v = torch.zeros_like(new[key]) if key.endswith("_mean") else torch.ones_like(new[key])
        for o, nw in cols:
            v[..., nw] = single[key][..., o]
        new[key] = v
        used.add(key), done.add(key)
    new["obs_normalizer.count"] = single["obs_normalizer.count"].clone()
    used.add("obs_normalizer.count"), done.add("obs_normalizer.count")
    for key, val in single.items():
        if key in used:
            continue
        nk = key
        m = re.match(r"cnns\.([^.]+)\.(.*)", key)
        if m:
            if m.group(1) not in cnn_names:
                raise RuntimeError(f"{what}: checkpoint CNN {m.group(1)!r} has no counterpart here")
            nk = f"cnns.{cnn_names[m.group(1)]}.{m.group(2)}"
        if (m and nk in new and val.dim() == 4 and new[nk].dim() == 4 and val.shape[0] == new[nk].shape[0]
                and val.shape[2:] == new[nk].shape[2:] and val.shape[1] < new[nk].shape[1]):
            # first conv layer of a map that gained channels (the partner map): old channels
            # copied, new ones at zero weight, so the output is unchanged
            w = torch.zeros_like(new[nk])
            w[:, :val.shape[1]] = val
            new[nk] = w
            used.add(key), done.add(nk)
            padded.append(nk.split(".")[1])
            continue
        if nk not in new or new[nk].shape != val.shape:
            raise RuntimeError(f"{what}: checkpoint weight {key} {tuple(val.shape)} does not fit "
                               f"{nk} {tuple(new[nk].shape) if nk in new else '(missing)'}")
        new[nk] = val.clone()
        used.add(key), done.add(nk)
    missing = [k for k in new if k not in done]
    if missing:
        raise RuntimeError(f"{what}: not filled from the checkpoint: {missing}")
    if min_std is not None and "distribution.std_param" in new:
        new["distribution.std_param"] = new["distribution.std_param"].clamp(min=min_std)
    model.load_state_dict(new, strict=True)
    zero = n1d_new - sum(s.stop - s.start for _, s in cols)
    out = [f"{len(done)} tensors copied", f"{zero} new inputs at zero weight"]
    if padded:
        out.append(f"new map channel(s) at zero weight in {', '.join(padded)}")
    return out


class MarlTrainer:
    def __init__(self, env, cfg: MarlCfg, log_dir: Path, device: str, logger: str = "tensorboard",
                 wandb_project: str = "quadcoop"):
        assert cfg.algo in ("ippo", "mappo"), cfg.algo
        self.env, self.cfg, self.device = env, cfg, device
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.n = env.num_envs
        self.dt = env.step_dt
        obs, _ = env.reset()
        self.obs = self._td(obs)
        v = cfg.variant
        self.actors = {a: make_model(self.obs, actor_groups(a, v), 3, cfg.hidden_dims, v, True).to(device)
                       for a in AGENTS}
        self.bound = cfg.mean_clip if cfg.mean_clip > 0 else 1.1
        for m_ in self.actors.values():  # no clamp (inf) still records the raw mean for the bound penalty/logs
            clamp_sampling_mean(m_, cfg.mean_clip if cfg.mean_clip > 0 else float("inf"))
        if cfg.mean_clip > 0 or cfg.bound_coef > 0:
            print(f"[marl2] sampling mean clamped to +-{cfg.mean_clip:g} (straight-through): "
                  f"{cfg.mean_clip > 0}; penalty on the raw mean past +-{self.bound:g}: {cfg.bound_coef:g}; "
                  f"entropy bonus {cfg.entropy_coef:g}")
        if cfg.algo == "ippo":
            self.critics = {a: make_model(self.obs, critic_groups("ippo", v, a), 1, cfg.hidden_dims, v, False).to(device)
                            for a in AGENTS}
        else:
            self.critics = {"central": make_model(self.obs, critic_groups("mappo", v), len(AGENTS),
                                                  cfg.central_hidden_dims, v, False).to(device)}
        self.actor_opt = {a: torch.optim.Adam(self.actors[a].parameters(), lr=cfg.actor_learning_rate) for a in AGENTS}
        self.critic_opt = {k: torch.optim.Adam(c.parameters(), lr=cfg.critic_learning_rate)
                           for k, c in self.critics.items()}
        self.lr = {a: cfg.actor_learning_rate for a in AGENTS}
        self.std_cap = {a: None for a in AGENTS}  # set at warm start (or loaded)
        self.refs = {}  # frozen Stage 2b actors for the KL anchor (build_refs)
        self.it = 0
        self.warm_from = {}
        # reward split: team terms + each robot's own (names ending in _<robot>)
        rm = env.reward_manager
        names = list(rm.active_terms)
        self.own_idx = {a: [i for i, nm in enumerate(names) if nm.endswith(f"_{a}")] for a in AGENTS}
        mine = {i for ix in self.own_idx.values() for i in ix}
        self.team_idx = [i for i in range(len(names)) if i not in mine]
        self.term_names = names
        self.writer = None
        self.wandb = None
        self.logger_kind = logger
        self.wandb_project = wandb_project

    # -- helpers ----------------------------------------------------------------------------------
    def _td(self, obs: dict) -> TensorDict:
        """Trainer observations, sanitized: a simulation glitch in one env must not reach the
        normalizers or the networks."""
        c = self.cfg.obs_clip
        keep = {k: torch.nan_to_num(v, nan=0.0, posinf=c, neginf=-c).clamp(-c, c)
                for k, v in obs.items() if not k.startswith("walker_")}
        return TensorDict(keep, batch_size=[self.n])

    def groups(self) -> list[str]:
        gs = set()
        for a in AGENTS:
            gs.update(actor_groups(a, self.cfg.variant))
        for k in self.critics:
            gs.update(critic_groups(self.cfg.algo, self.cfg.variant, None if k == "central" else k))
        return sorted(gs)

    def values(self, obs: TensorDict) -> torch.Tensor:
        if self.cfg.algo == "ippo":
            return torch.cat([self.critics[a](obs) for a in AGENTS], -1)
        return self.critics["central"](obs)

    def agent_rewards(self) -> torch.Tensor:
        """(n, 2): team terms + each robot's own terms, this step (weights and dt applied)."""
        S = self.env.reward_manager._step_reward
        team = S[:, self.team_idx].sum(-1)
        r = torch.stack([team + S[:, self.own_idx[a]].sum(-1) for a in AGENTS], -1) * self.dt
        c = self.cfg.reward_clip
        return torch.nan_to_num(r, nan=0.0, posinf=c, neginf=-c).clamp(-c, c)

    # -- warm start from the Stage 2 checkpoints ----------------------------------------------------
    def warm_start(self, paths: dict[str, str]) -> None:
        v = self.cfg.variant
        for a, path in paths.items():
            ck = torch.load(path, map_location=self.device, weights_only=False)
            cnn = {"profile_top": f"top_{a}", "profile_front": "front"}
            n_act = int(self.obs[f"actor_{a}"].shape[-1])  # 42 + partner 9 (+ contacts 9)
            rep = warm_start_model(self.actors[a], ck["actor_state_dict"], [(slice(0, N_SINGLE), slice(0, N_SINGLE))],
                                   n_act, cnn if v == "b" else {}, self.cfg.min_std, f"{a} actor <- {path}")
            sp = self.actors[a].distribution.std_param.detach()
            self.std_cap[a] = (sp * self.cfg.max_std_factor).clamp(min=self.cfg.min_std).clone()
            print(f"[marl2] {a}: actor warm-started from {path} ({', '.join(rep)}); action noise "
                  f"{[round(x, 2) for x in sp.tolist()]}, capped at {[round(x, 2) for x in self.std_cap[a].tolist()]}")
            if self.cfg.algo == "ippo":
                n_state = int(self.obs[f"state_{a}"].shape[-1])
                cols = [(slice(0, N_SINGLE), slice(0, N_SINGLE)),
                        (slice(N_SINGLE, N_SINGLE + N_PHYS), slice(n_state, n_state + N_PHYS))]
                rep = warm_start_model(self.critics[a], ck["critic_state_dict"], cols, n_state + N_PHYS,
                                       cnn if v == "b" else {}, None, f"{a} critic <- {path}")
                print(f"[marl2] {a}: critic warm-started from {path} ({', '.join(rep)})")
            self.warm_from[a] = str(path)

    def build_refs(self, paths: dict[str, str]) -> None:
        """Frozen copies of the Stage 2b actors (the warm-start source) for the KL anchor: built
        exactly as the warm start builds the actors (partner inputs at zero weight), never trained."""
        v = self.cfg.variant
        for a, path in paths.items():
            ck = torch.load(path, map_location=self.device, weights_only=False)
            ref = make_model(self.obs, actor_groups(a, v), 3, self.cfg.hidden_dims, v, True).to(self.device)
            cnn = {"profile_top": f"top_{a}", "profile_front": "front"} if v == "b" else {}
            warm_start_model(ref, ck["actor_state_dict"], [(slice(0, N_SINGLE), slice(0, N_SINGLE))],
                             int(self.obs[f"actor_{a}"].shape[-1]), cnn, self.cfg.min_std, f"{a} reference <- {path}")
            ref.eval()
            for p in ref.parameters():
                p.requires_grad_(False)
            self.refs[a] = ref
        print(f"[marl2] KL anchor: beta {self.cfg.kl_ref:g}"
              f"{f' falling to 0 by iteration {self.cfg.kl_ramp}' if self.cfg.kl_ramp > 0 else ''} to the frozen Stage 2b actors "
              f"({', '.join(f'{a} <- {p}' for a, p in paths.items())})")

    def kl_to_ref(self, a: str, o_mb: TensorDict) -> torch.Tensor:
        """KL(pi || pi_ref) per sample for robot a, after the actor's forward pass on o_mb (uses its
        raw mean and noise); both means clamped to +-kl_ref_clip, summed over (vx, vy, wz)."""
        actor, c = self.actors[a], self.cfg.kl_ref_clip
        mu = actor.distribution.raw_mean.clamp(-c, c)
        sd = actor.distribution.std_param.clamp(min=1e-6).expand_as(mu)
        with torch.no_grad():
            ref = self.refs[a]
            mu_r = ref(o_mb).clamp(-c, c)
            sd_r = ref.distribution.std_param.clamp(min=1e-6).expand_as(mu_r)
        kl = torch.log(sd_r / sd) + (sd.square() + (mu - mu_r).square()) / (2.0 * sd_r.square()) - 0.5
        return kl.sum(-1)

    def kl_beta(self) -> float:
        """The anchor's beta this iteration: kl_ref, falling linearly to 0 over kl_ramp iterations."""
        c = self.cfg
        if c.kl_ref <= 0:
            return 0.0
        return c.kl_ref if c.kl_ramp <= 0 else c.kl_ref * max(0.0, 1.0 - self.it / c.kl_ramp)

    def kl_weight(self, a: str, o_mb: TensorDict) -> torch.Tensor:
        """Per-sample anchor weight: 1 with the partner far, kl_partner_scale with it near."""
        c = self.cfg
        if c.kl_partner_scale >= 1.0:
            return torch.ones(o_mb.batch_size[0], device=self.device)
        rel = o_mb[f"state_{a}"][:, N_SINGLE:N_SINGLE + 2]  # partner position in this robot's frame
        d = torch.linalg.norm(rel, dim=-1)
        ramp = ((d - c.kl_partner_near) / max(c.kl_partner_far - c.kl_partner_near, 1e-6)).clamp(0.0, 1.0)
        return c.kl_partner_scale + (1.0 - c.kl_partner_scale) * ramp

    def init_scratch(self) -> None:
        """Random initial actors and critics (as built). Only the noise cap is set here."""
        for a in AGENTS:
            sp = self.actors[a].distribution.std_param
            with torch.no_grad():
                sp.clamp_(min=self.cfg.min_std)
            self.std_cap[a] = (sp.detach() * self.cfg.max_std_factor).clamp(min=self.cfg.min_std).clone()
            print(f"[marl2] {a}: actor from scratch (random weights, normalizer learns from data); action noise "
                  f"{[round(x, 2) for x in sp.tolist()]}, capped at {[round(x, 2) for x in self.std_cap[a].tolist()]}")
        print(f"[marl2] critics from scratch ({', '.join(self.critics)})")
        self.warm_from = {"scratch": "random initial weights"}

    # -- checkpoints ---------------------------------------------------------------------------------
    def save(self) -> Path:
        g = self.env.command_manager.get_term("goal")
        ck = {
            "iter": self.it, "algo": self.cfg.algo, "variant": self.cfg.variant, "cfg": asdict(self.cfg),
            "agents": list(AGENTS),
            "actors": {a: self.actors[a].state_dict() for a in AGENTS},
            "critics": {k: c.state_dict() for k, c in self.critics.items()},
            "actor_opt": {a: o.state_dict() for a, o in self.actor_opt.items()},
            "critic_opt": {k: o.state_dict() for k, o in self.critic_opt.items()},
            "lr": dict(self.lr), "warm_from": self.warm_from,
            "std_cap": {a: (None if c is None else c.tolist()) for a, c in self.std_cap.items()},
            "env_state": {"common_step_counter": int(self.env.common_step_counter), "level": int(g.level),
                          "ema_success": float(g.ema_success), "shape_success": g.shape_success.tolist(),
                          "tol_level": int(getattr(g, "tol_level", 0)), "tol_ema": float(getattr(g, "tol_ema", 0.0))},
        }
        path = self.log_dir / f"model_{self.it}.pt"
        torch.save(ck, path)
        return path

    def load(self, path: str | Path) -> None:
        ck = torch.load(str(path), map_location=self.device, weights_only=False)
        assert ck["algo"] == self.cfg.algo, f"checkpoint is {ck['algo']}, trainer is {self.cfg.algo}"
        for a in AGENTS:
            self.actors[a].load_state_dict(ck["actors"][a])
            self.actor_opt[a].load_state_dict(ck["actor_opt"][a])
        for k in self.critics:
            self.critics[k].load_state_dict(ck["critics"][k])
            self.critic_opt[k].load_state_dict(ck["critic_opt"][k])
        self.lr = dict(ck["lr"])
        for a, c in (ck.get("std_cap") or {}).items():
            if c is not None:
                self.std_cap[a] = torch.tensor(c, device=self.device)
        for a in AGENTS:
            for pg in self.actor_opt[a].param_groups:
                pg["lr"] = self.lr[a]
        self.it = int(ck["iter"])
        self.warm_from = ck.get("warm_from", {})
        es = ck.get("env_state", {})
        self.env.common_step_counter = es.get("common_step_counter", 0)
        g = self.env.command_manager.get_term("goal")
        g.level = es.get("level", g.level)
        g.ema_success = es.get("ema_success", g.ema_success)
        if "shape_success" in es:
            g.shape_success[:] = torch.tensor(es["shape_success"], device=g.shape_success.device)
        g.last_change_iter = self.env.common_step_counter / self.cfg.num_steps_per_env
        if getattr(g, "tol_table", None) is not None:
            g.tol_level = int(es.get("tol_level", g.tol_level))
            g.tol_ema = float(es.get("tol_ema", g.tol_ema))
            g.tol_last_change = g.last_change_iter
        print(f"[marl2] resumed {path} at iteration {self.it}, curriculum level {g.level}"
              f"{f', tolerance level {g.tol_level}' if getattr(g, 'tol_table', None) is not None else ''}")

    @staticmethod
    def newest(log_dir: Path) -> Path | None:
        cks = [(int(m.group(1)), p) for p in Path(log_dir).glob("model_*.pt")
               if (m := re.match(r"model_(\d+)\.pt$", p.name))]
        return max(cks)[1] if cks else None

    # -- logging ----------------------------------------------------------------------------------------
    def _open_logs(self) -> None:
        from torch.utils.tensorboard import SummaryWriter

        self.writer = SummaryWriter(log_dir=str(self.log_dir))
        if self.logger_kind == "wandb":
            import wandb

            self.wandb = wandb.init(project=self.wandb_project, name=self.log_dir.name, dir=str(self.log_dir),
                                    config=asdict(self.cfg), resume="allow", id=self.log_dir.name.replace("/", "_"))

    def _log(self, scalars: dict[str, float]) -> None:
        for k, v in scalars.items():
            self.writer.add_scalar(k, v, self.it)
        if self.wandb is not None:
            self.wandb.log(scalars, step=self.it)

    def _log_video(self, path: Path) -> None:
        print(f"[marl2] video: {path}", flush=True)
        if self.wandb is not None:
            import wandb

            self.wandb.log({"video/train_env0": wandb.Video(str(path), format="mp4")}, step=self.it)

    # -- training loop ----------------------------------------------------------------------------------
    def learn(self) -> None:
        from quadcoop.coop2.video import PairVideo

        cfg, n, T, dev = self.cfg, self.n, self.cfg.num_steps_per_env, self.device
        self._open_logs()
        video = PairVideo(self.env, self.log_dir / "videos", cfg.video_length) if cfg.video_interval > 0 else None
        if self.it == 0:
            what = "random initial policies" if self.cfg.scratch else "the warm-started policies"
            print(f"[marl2] saved {self.save()} (iteration 0 = {what}, before any update)")
        groups = self.groups()
        A = len(AGENTS)
        ep_ret = torch.zeros(n, A, device=dev)
        ep_len = torch.zeros(n, device=dev)
        obs = self.obs
        for m_ in list(self.actors.values()) + list(self.critics.values()):
            m_.train()

        while self.it < cfg.max_iterations:
            t0 = time.time()
            warm = self.it < cfg.critic_warmup
            buf = {g_: torch.zeros(T, *obs[g_].shape, device=dev) for g_ in groups}
            act = torch.zeros(T, n, 3 * A, device=dev)
            logp = torch.zeros(T, n, A, device=dev)
            mu = torch.zeros(T, n, 3 * A, device=dev)
            sigma = torch.zeros(T, n, 3 * A, device=dev)
            val = torch.zeros(T, n, A, device=dev)
            rew = torch.zeros(T, n, A, device=dev)
            done = torch.zeros(T, n, device=dev)
            logs = defaultdict(list)
            finished_ret, finished_len = [], []
            tm = self.env.termination_manager
            outcome = defaultdict(float)
            n_ended = 0.0
            skipped = 0

            with torch.inference_mode():
                for t in range(T):
                    for g_ in groups:
                        buf[g_][t] = obs[g_]
                    acts = []
                    for k, a in enumerate(AGENTS):
                        ak = self.actors[a](obs, stochastic_output=True)
                        logp[t, :, k] = self.actors[a].get_output_log_prob(ak)
                        m_, s_ = self.actors[a].output_distribution_params
                        mu[t, :, 3 * k:3 * k + 3] = m_
                        sigma[t, :, 3 * k:3 * k + 3] = s_.expand_as(m_)
                        acts.append(ak)
                    action = torch.cat(acts, -1)
                    act[t] = action
                    v = self.values(obs)
                    val[t] = v
                    o, _, term, trunc, extras = self.env.step(action)
                    r_i = self.agent_rewards()
                    if video is not None:
                        if not video.active and self.it % cfg.video_interval == 0 and t == 0:
                            video.start(self.it)
                        path = video.step()
                        if path is not None:
                            self._log_video(path)
                    obs = self._td(o)
                    d = (term | trunc).float()
                    ep_ret += r_i
                    ep_len += 1
                    rew[t] = r_i + cfg.gamma * v * trunc.float().unsqueeze(-1)  # bootstrap time-outs
                    done[t] = d
                    for c in self.critics.values():
                        c.update_normalization(obs)
                    if cfg.scratch:  # warm-started actors keep their loaded normalizers
                        for m_ in self.actors.values():
                            m_.update_normalization(obs)
                    ended = d.bool()
                    n_ended += float(ended.sum())
                    for nm in tm.active_terms:
                        outcome[nm] += float((tm.get_term(nm) & ended).sum())
                    if ended.any():
                        finished_ret.append(ep_ret[ended].clone())
                        finished_len.append(ep_len[ended].clone())
                        ep_ret[ended] = 0.0
                        ep_len[ended] = 0.0
                    for k_, v_ in extras.get("log", {}).items():
                        logs[k_].append(float(v_) if not torch.is_tensor(v_) else float(v_.float().mean()))
                last_v = self.values(obs)
                adv = torch.zeros(T, n, A, device=dev)
                gae = torch.zeros(n, A, device=dev)
                for t in reversed(range(T)):
                    nv = last_v if t == T - 1 else val[t + 1]
                    nonterm = (1.0 - done[t]).unsqueeze(-1)
                    delta = rew[t] + nonterm * cfg.gamma * nv - val[t]
                    gae = delta + nonterm * cfg.gamma * cfg.lam * gae
                    adv[t] = gae
                ret = adv + val
                adv_n = (adv - adv.mean((0, 1))) / (adv.std((0, 1)) + 1e-8)
            collect_s = time.time() - t0

            # -- update -------------------------------------------------------------------------------
            B = T * n
            flat = {g_: buf[g_].reshape(B, *buf[g_].shape[2:]) for g_ in groups}
            f_act, f_logp, f_mu, f_sigma = act.reshape(B, -1), logp.reshape(B, A), mu.reshape(B, -1), sigma.reshape(B, -1)
            f_val, f_ret, f_adv = val.reshape(B, A), ret.reshape(B, A), adv_n.reshape(B, A)
            mb = B // cfg.num_mini_batches
            stats = defaultdict(float)
            beta = self.kl_beta()
            n_upd = 0
            for _ in range(cfg.num_learning_epochs):
                perm = torch.randperm(B, device=dev)
                for i in range(cfg.num_mini_batches):
                    idx = perm[i * mb:(i + 1) * mb]
                    o_mb = TensorDict({g_: flat[g_][idx] for g_ in groups}, batch_size=[len(idx)])
                    n_upd += 1
                    if not warm:
                        for k, a in enumerate(AGENTS):
                            actor = self.actors[a]
                            sl = slice(3 * k, 3 * k + 3)
                            actor(o_mb, stochastic_output=True)
                            excess = torch.relu(actor.distribution.raw_mean.abs() - self.bound)
                            bound_loss = excess.pow(2).sum(-1).mean()
                            lp = actor.get_output_log_prob(f_act[idx, sl])
                            ent = actor.output_entropy
                            new_params = actor.output_distribution_params
                            with torch.inference_mode():
                                kl = actor.get_kl_divergence((f_mu[idx, sl], f_sigma[idx, sl]),
                                                             tuple(p.detach() for p in new_params)).mean()
                                if cfg.desired_kl is not None:
                                    if kl > cfg.desired_kl * 2.0:
                                        self.lr[a] = max(1e-5, self.lr[a] / 1.5)
                                    elif 0.0 < kl < cfg.desired_kl / 2.0:
                                        self.lr[a] = min(cfg.max_actor_learning_rate, self.lr[a] * 1.5)
                                    for pg in self.actor_opt[a].param_groups:
                                        pg["lr"] = self.lr[a]
                            ratio = torch.exp(lp - f_logp[idx, k])
                            adv_k = f_adv[idx, k]
                            surr = -torch.min(adv_k * ratio,
                                              adv_k * torch.clamp(ratio, 1 - cfg.clip_param, 1 + cfg.clip_param)).mean()
                            loss = surr - cfg.entropy_coef * ent.mean()
                            if cfg.bound_coef > 0:
                                loss = loss + cfg.bound_coef * bound_loss
                            kl_ref = None
                            if beta > 0 and a in self.refs:
                                kl_s = self.kl_to_ref(a, o_mb)
                                kl_ref = kl_s.mean()
                                loss = loss + beta * (self.kl_weight(a, o_mb) * kl_s).mean()
                            if not torch.isfinite(loss):
                                skipped += 1
                                continue
                            self.actor_opt[a].zero_grad()
                            loss.backward()
                            gn = torch.nn.utils.clip_grad_norm_(actor.parameters(), cfg.max_grad_norm)
                            if not torch.isfinite(gn):
                                self.actor_opt[a].zero_grad()
                                skipped += 1
                                continue
                            self.actor_opt[a].step()
                            with torch.no_grad():
                                cap = self.std_cap[a]
                                if cap is None:
                                    actor.distribution.std_param.clamp_(min=cfg.min_std)
                                else:
                                    actor.distribution.std_param.copy_(
                                        torch.maximum(torch.minimum(actor.distribution.std_param, cap),
                                                      torch.full_like(cap, cfg.min_std)))
                            stats[f"Loss/surrogate_{a}"] += surr.item()
                            stats[f"Loss/entropy_{a}"] += ent.mean().item()
                            stats[f"Loss/kl_{a}"] += float(kl)
                            stats[f"Loss/bound_{a}"] += bound_loss.item()
                            if kl_ref is not None:
                                stats[f"Loss/kl_ref_{a}"] += kl_ref.item()
                            stats[f"Policy/out_of_range_{a}"] += float((excess > 0).float().mean())
                    if cfg.algo == "ippo":
                        for k, a in enumerate(AGENTS):
                            vl = self._value_loss(self.critics[a](o_mb).squeeze(-1), f_val[idx, k], f_ret[idx, k])
                            if not torch.isfinite(vl):
                                skipped += 1
                                continue
                            self._step_critic(a, vl)
                            stats[f"Loss/value_{a}"] += vl.item()
                    else:
                        vl = self._value_loss(self.critics["central"](o_mb), f_val[idx], f_ret[idx])
                        if not torch.isfinite(vl):
                            skipped += 1
                            continue
                        self._step_critic("central", vl)
                        stats["Loss/value"] += vl.item()
            self.it += 1
            dt_s = time.time() - t0

            # -- logging ---------------------------------------------------------------------------------
            out = {k: v / max(n_upd, 1) for k, v in stats.items()}
            for k, v in logs.items():
                out[k] = sum(v) / len(v)
            if finished_ret:
                fr = torch.cat(finished_ret)
                out["Train/mean_episode_length_s"] = float(torch.cat(finished_len).mean()) * self.dt
                for k, a in enumerate(AGENTS):
                    out[f"Train/mean_return_{a}"] = float(fr[:, k].mean())
            for a in AGENTS:
                out[f"Policy/lr_{a}"] = self.lr[a]
                out[f"Policy/std_{a}"] = float(self.actors[a].distribution.std_param.detach().mean())
            out["Perf/steps_per_s"] = B / dt_s
            out["Perf/collect_s"] = collect_s
            out["Perf/iteration_s"] = dt_s
            out["Train/critic_warmup"] = float(warm)
            out["Loss/kl_beta"] = beta
            out["Train/skipped_updates"] = float(skipped)
            # how the episodes that ended this iteration ended (fractions; they sum to 1)
            for nm, cnt in outcome.items():
                out[f"Outcome/{nm}"] = cnt / max(n_ended, 1.0)
            self._log(out)
            if self.it % 10 == 0 or self.it == 1:
                succ = out.get("Outcome/goal_reached", float("nan"))
                lvl = out.get("Curriculum/push/level", float("nan"))
                tol = out.get("Curriculum/push/tol_level")
                if tol is not None:
                    lvl = f"{lvl:g} tol {out.get('Curriculum/push/tol_pos_m', 0):.2f}m/{out.get('Curriculum/push/tol_yaw_deg', 0):.0f}deg"
                    eng = [out.get(f"Curriculum/push/contact_dist_{x}") for x in AGENTS]
                    if eng[0] is not None:
                        lvl += f" contact dist {eng[0]:.2f}/{eng[1]:.2f}m"
                    oc = [out.get(f"Outcome/{x}_off_contact", 0.0) for x in AGENTS]
                    lvl += f" off-contact {oc[0]:.2f}/{oc[1]:.2f}"
                fa = out.get(f"Outcome/{AGENTS[0]}_fell", float("nan"))
                fs = out.get(f"Outcome/{AGENTS[1]}_fell", float("nan"))
                print(f"[marl2 {cfg.algo}] it {self.it}/{cfg.max_iterations}  return "
                      f"{out.get(f'Train/mean_return_{AGENTS[0]}', float('nan')):.2f}/"
                      f"{out.get(f'Train/mean_return_{AGENTS[1]}', float('nan')):.2f}  success {succ:.2f}  level {lvl}  "
                      f"fell {fa:.2f}/{fs:.2f}  {B / dt_s:.0f} steps/s{'  (critic warm-up)' if warm else ''}"
                      f"{f'  skipped {skipped}' if skipped else ''}",
                      flush=True)
            if self.it % cfg.save_interval == 0 or self.it == cfg.max_iterations:
                self.save()
        self.writer.close()
        if self.wandb is not None:
            self.wandb.finish()

    def _value_loss(self, v: torch.Tensor, v_old: torch.Tensor, ret: torch.Tensor) -> torch.Tensor:
        clip = self.cfg.clip_param
        v_clip = v_old + (v - v_old).clamp(-clip, clip)
        return torch.max((v - ret).pow(2), (v_clip - ret).pow(2)).mean()

    def _step_critic(self, key: str, loss: torch.Tensor) -> None:
        opt = self.critic_opt[key]
        opt.zero_grad()
        (self.cfg.value_loss_coef * loss).backward()
        gn = torch.nn.utils.clip_grad_norm_(self.critics[key].parameters(), self.cfg.max_grad_norm)
        if torch.isfinite(gn):
            opt.step()
        else:
            opt.zero_grad()


class PairPolicy:
    """Deterministic two-robot policy for evaluation: from a trainer checkpoint (model_<iter>.pt),
    or from the two Stage 2 checkpoints (the untrained "frozen pair": iteration 0)."""

    def __init__(self, env_obs: TensorDict, device: str, variant: str = "b", checkpoint: str | None = None,
                 singles: dict[str, str] | None = None):
        self.actors = {a: make_model(env_obs, actor_groups(a, variant), 3, (256, 128, 64), variant, True).to(device)
                       for a in AGENTS}
        if checkpoint:
            ck = torch.load(checkpoint, map_location=device, weights_only=False)
            for a in AGENTS:
                self.actors[a].load_state_dict(ck["actors"][a])
            self.iteration = int(ck["iter"])
        else:
            cnn = lambda a: {"profile_top": f"top_{a}", "profile_front": "front"} if variant == "b" else {}  # noqa: E731
            for a, path in (singles or {}).items():
                ck = torch.load(path, map_location=device, weights_only=False)
                warm_start_model(self.actors[a], ck["actor_state_dict"], [(slice(0, N_SINGLE), slice(0, N_SINGLE))],
                                 int(env_obs[f"actor_{a}"].shape[-1]), cnn(a), None, f"{a} actor <- {path}")
            self.iteration = 0
        for a in AGENTS:
            self.actors[a].eval()

    @torch.no_grad()
    def __call__(self, obs: TensorDict) -> torch.Tensor:
        return torch.cat([self.actors[a](obs) for a in AGENTS], -1)
