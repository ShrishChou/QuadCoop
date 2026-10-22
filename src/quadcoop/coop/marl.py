"""IPPO and MAPPO for the two-robot task, in one trainer.

Both methods use the same environment, rollouts, PPO losses, hyperparameters and
warm start. They differ only in the critic:

    ippo   each robot has its own critic, which sees only that robot's observation
           (+ the privileged object physics both critics get): V_i(o_i, z)
    mappo  one centralized critic sees both robots' observations (+ the same
           privileged physics) and outputs one value per robot: V(o_1, o_2, z)

Actors are always decentralized: each robot's policy sees only its own observation
(actor_anymal / actor_spot) and acts on its own. Each robot has its own actor,
optimizer and KL-adaptive learning rate. Rewards: the team reward from the env,
minus ``effort_cost`` x the robot's own effort (0 by default = fully cooperative).

Warm start: each actor starts from that robot's Stage 1b (or 1c) policy. The first
42 inputs are Stage 1b's in the same order; the 6 partner inputs start at zero
weight, so iteration 0 is exactly "two single-robot policies run side by side"
(model_0.pt is saved before any update: the frozen-pair baseline). Critics start
fresh and train alone for ``critic_warmup`` iterations before the actors update.

Checkpoints: logs/marl/<run_name>/model_<iter>.pt; ``resume`` continues the newest.
"""

from __future__ import annotations

import re
import time
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from pathlib import Path

import torch
from tensordict import TensorDict

from quadcoop.coop.mdp import AGENTS, agent_effort

ACTOR_GROUPS = {a: f"actor_{a}" for a in AGENTS}
STATE_GROUPS = {a: f"state_{a}" for a in AGENTS}
PRIV = "privileged"
STAGE1B_ACTOR_INPUTS = 42  # Stage 1b actor = the first 42 columns of actor_<robot>


@dataclass
class MarlCfg:
    algo: str = "mappo"  # "ippo" | "mappo"
    num_envs: int = 4096
    num_steps_per_env: int = 24
    max_iterations: int = 6000
    num_learning_epochs: int = 5
    num_mini_batches: int = 4
    clip_param: float = 0.2
    gamma: float = 0.99
    lam: float = 0.95
    learning_rate: float = 3.0e-4
    critic_learning_rate: float = 3.0e-4
    desired_kl: float = 0.01
    entropy_coef: float = 0.004
    value_loss_coef: float = 1.0
    max_grad_norm: float = 1.0
    hidden_dims: tuple[int, ...] = (256, 128, 64)
    critic_hidden_dims: tuple[int, ...] = (512, 256, 128)
    init_std: float = 0.6  # only used without a warm start
    min_std: float = 0.2  # floor on the warm-started action noise
    critic_warmup: int = 100  # iterations with frozen actors while the fresh critics catch up
    effort_cost: float = 0.0  # lambda: r_i = r_team - lambda * effort_i * dt
    save_interval: int = 50
    video_interval: int = 500  # record a training video every this many iterations (0 = never)
    video_length: int = 750  # env steps per video (750 = 15 s)
    seed: int = 0
    init: dict = field(default_factory=dict)  # agent -> Stage 1b/1c checkpoint path


def _dist_cfg(init_std: float) -> dict:
    return {"class_name": "GaussianDistribution", "init_std": init_std, "std_type": "scalar"}


class MarlTrainer:
    def __init__(self, env, cfg: MarlCfg, log_dir: Path, device: str, logger: str = "tensorboard",
                 wandb_project: str = "quadcoop"):
        from rsl_rl.models.mlp_model import MLPModel

        assert cfg.algo in ("ippo", "mappo"), cfg.algo
        self.env, self.cfg, self.device = env, cfg, device
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.n = env.num_envs
        self.dt = env.step_dt
        obs, _ = env.reset()
        self.obs = self._td(obs)

        self.actors = {a: MLPModel(self.obs, {"policy": [ACTOR_GROUPS[a]]}, "policy", 3, cfg.hidden_dims, "elu",
                                   obs_normalization=True, distribution_cfg=_dist_cfg(cfg.init_std)).to(device)
                       for a in AGENTS}
        if cfg.algo == "ippo":
            self.critics = {a: MLPModel(self.obs, {"value": [STATE_GROUPS[a], PRIV]}, "value", 1,
                                        cfg.critic_hidden_dims, "elu", obs_normalization=True).to(device)
                            for a in AGENTS}
        else:
            self.critics = {"central": MLPModel(self.obs, {"value": [STATE_GROUPS[a] for a in AGENTS] + [PRIV]},
                                                "value", len(AGENTS), cfg.critic_hidden_dims, "elu",
                                                obs_normalization=True).to(device)}
        self.actor_opt = {a: torch.optim.Adam(self.actors[a].parameters(), lr=cfg.learning_rate) for a in AGENTS}
        self.critic_opt = {k: torch.optim.Adam(c.parameters(), lr=cfg.critic_learning_rate)
                           for k, c in self.critics.items()}
        self.lr = {a: cfg.learning_rate for a in AGENTS}
        self.it = 0
        self.warm_from = {}
        self.writer = None
        self.wandb = None
        self.logger_kind = logger
        self.wandb_project = wandb_project

    # -- helpers --------------------------------------------------------------------------------
    def _td(self, obs: dict) -> TensorDict:
        keep = {k: v for k, v in obs.items() if not k.startswith("walker_")}
        return TensorDict(keep, batch_size=[self.n])

    def values(self, obs: TensorDict) -> torch.Tensor:
        """(n, 2): each robot's value estimate."""
        if self.cfg.algo == "ippo":
            return torch.cat([self.critics[a](obs) for a in AGENTS], -1)
        return self.critics["central"](obs)

    # -- warm start from single-robot checkpoints -------------------------------------------------
    def warm_start(self, paths: dict[str, str]) -> None:
        for a, path in paths.items():
            ck = torch.load(path, map_location=self.device, weights_only=False)
            old = ck["actor_state_dict"]
            new = self.actors[a].state_dict()
            k_old = old["mlp.0.weight"].shape[1]
            assert k_old == STAGE1B_ACTOR_INPUTS, f"{path}: actor has {k_old} inputs, expected Stage 1b's 42"
            w = torch.zeros_like(new["mlp.0.weight"])
            w[:, :k_old] = old["mlp.0.weight"]
            new["mlp.0.weight"] = w
            for key in ("obs_normalizer._mean", "obs_normalizer._var", "obs_normalizer._std"):
                new[key][:, :k_old] = old[key]
            new["obs_normalizer.count"] = old["obs_normalizer.count"]
            for key, val in old.items():
                if key == "mlp.0.weight" or key.startswith("obs_normalizer."):
                    continue
                if key in new and new[key].shape == val.shape:
                    new[key] = val.clone()
            new["distribution.std_param"] = new["distribution.std_param"].clamp(min=self.cfg.min_std)
            self.actors[a].load_state_dict(new)
            self.warm_from[a] = str(path)
            print(f"[marl] {a}: actor warm-started from {path} (42 inputs copied, 6 partner inputs at 0)")

    # -- checkpoints ----------------------------------------------------------------------------------
    def save(self) -> Path:
        g = self.env.command_manager.get_term("goal")
        ck = {
            "iter": self.it, "algo": self.cfg.algo, "cfg": asdict(self.cfg), "agents": list(AGENTS),
            "actors": {a: self.actors[a].state_dict() for a in AGENTS},
            "critics": {k: c.state_dict() for k, c in self.critics.items()},
            "actor_opt": {a: o.state_dict() for a, o in self.actor_opt.items()},
            "critic_opt": {k: o.state_dict() for k, o in self.critic_opt.items()},
            "lr": dict(self.lr), "warm_from": self.warm_from,
            "env_state": {"common_step_counter": int(self.env.common_step_counter), "level": int(g.level),
                          "ema_success": float(g.ema_success)},
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
        print(f"[marl] resumed {path} at iteration {self.it}, curriculum level {g.level}")

    @staticmethod
    def newest(log_dir: Path) -> Path | None:
        cks = [(int(m.group(1)), p) for p in Path(log_dir).glob("model_*.pt")
               if (m := re.match(r"model_(\d+)\.pt$", p.name))]
        return max(cks)[1] if cks else None

    # -- logging -----------------------------------------------------------------------------------------
    def _open_logs(self) -> None:
        from torch.utils.tensorboard import SummaryWriter

        self.writer = SummaryWriter(log_dir=str(self.log_dir))
        if self.logger_kind == "wandb":
            import wandb

            self.wandb = wandb.init(project=self.wandb_project, name=self.log_dir.name, dir=str(self.log_dir),
                                    config=asdict(self.cfg), resume="allow", id=self.log_dir.name.replace("/", "_"))

    def _log_video(self, path: Path, it: int) -> None:
        print(f"[marl] video: {path}", flush=True)
        if self.wandb is not None:
            import wandb

            self.wandb.log({"video/train_env0": wandb.Video(str(path), format="mp4")}, step=self.it)

    def _log(self, scalars: dict[str, float]) -> None:
        for k, v in scalars.items():
            self.writer.add_scalar(k, v, self.it)
        if self.wandb is not None:
            self.wandb.log(scalars, step=self.it)

    # -- training loop ------------------------------------------------------------------------------
    def learn(self) -> None:
        cfg, n, T, dev = self.cfg, self.n, self.cfg.num_steps_per_env, self.device
        self._open_logs()
        video = TrainVideo(self.env, self.log_dir / "videos", cfg.video_length) if cfg.video_interval > 0 else None
        if self.it == 0:
            print(f"[marl] saved {self.save()} (iteration 0 = the warm-started policies, before any update)")
        groups = [ACTOR_GROUPS[a] for a in AGENTS] + [STATE_GROUPS[a] for a in AGENTS] + [PRIV]
        A = len(AGENTS)
        ep_ret = torch.zeros(n, A, device=dev)
        ep_len = torch.zeros(n, device=dev)
        obs = self.obs
        for a in AGENTS:
            self.actors[a].train()
        for c in self.critics.values():
            c.train()

        while self.it < cfg.max_iterations:
            t0 = time.time()
            warm = self.it < cfg.critic_warmup
            buf = {g: torch.zeros(T, n, obs[g].shape[-1], device=dev) for g in groups}
            act = torch.zeros(T, n, 3 * A, device=dev)
            logp = torch.zeros(T, n, A, device=dev)
            mu = torch.zeros(T, n, 3 * A, device=dev)
            sigma = torch.zeros(T, n, 3 * A, device=dev)
            val = torch.zeros(T, n, A, device=dev)
            rew = torch.zeros(T, n, A, device=dev)
            done = torch.zeros(T, n, device=dev)
            logs = defaultdict(list)
            finished_ret, finished_len = [], []
            effort_sum = torch.zeros(A, device=dev)

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
                    o, r, term, trunc, extras = self.env.step(action)
                    if video is not None:
                        if not video.active and self.it % cfg.video_interval == 0 and t == 0:
                            video.start(self.it)
                        path = video.step()
                        if path is not None:
                            self._log_video(path, video.started_at)
                    obs = self._td(o)
                    eff = agent_effort(self.env)
                    effort_sum += eff.mean(0)
                    r_i = r.unsqueeze(-1) - cfg.effort_cost * eff * self.dt
                    d = (term | trunc).float()
                    # bootstrap through time-outs (as rsl_rl does)
                    r_i = r_i + cfg.gamma * v * trunc.float().unsqueeze(-1)
                    rew[t] = r_i
                    done[t] = d
                    if not warm:
                        for a in AGENTS:
                            self.actors[a].update_normalization(obs)
                    for c in self.critics.values():
                        c.update_normalization(obs)
                    ep_ret += r.unsqueeze(-1) - cfg.effort_cost * eff * self.dt
                    ep_len += 1
                    ended = d.bool()
                    if ended.any():
                        finished_ret.append(ep_ret[ended].clone())
                        finished_len.append(ep_len[ended].clone())
                        ep_ret[ended] = 0.0
                        ep_len[ended] = 0.0
                    for k, v_ in extras.get("log", {}).items():
                        logs[k].append(float(v_) if not torch.is_tensor(v_) else float(v_.float().mean()))
                last_v = self.values(obs)

                # GAE per robot
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

            # -- update ------------------------------------------------------------------------------
            B = T * n
            flat = {g_: buf[g_].reshape(B, -1) for g_ in groups}
            f_act, f_logp, f_mu, f_sigma = act.reshape(B, -1), logp.reshape(B, A), mu.reshape(B, -1), sigma.reshape(B, -1)
            f_val, f_ret, f_adv = val.reshape(B, A), ret.reshape(B, A), adv_n.reshape(B, A)
            mb = B // cfg.num_mini_batches
            stats = defaultdict(float)
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
                                        self.lr[a] = min(1e-2, self.lr[a] * 1.5)
                                    for pg in self.actor_opt[a].param_groups:
                                        pg["lr"] = self.lr[a]
                            ratio = torch.exp(lp - f_logp[idx, k])
                            adv_k = f_adv[idx, k]
                            surr = -torch.min(adv_k * ratio,
                                              adv_k * torch.clamp(ratio, 1 - cfg.clip_param, 1 + cfg.clip_param)).mean()
                            loss = surr - cfg.entropy_coef * ent.mean()
                            self.actor_opt[a].zero_grad()
                            loss.backward()
                            torch.nn.utils.clip_grad_norm_(actor.parameters(), cfg.max_grad_norm)
                            self.actor_opt[a].step()
                            stats[f"Loss/surrogate_{a}"] += surr.item()
                            stats[f"Loss/entropy_{a}"] += ent.mean().item()
                            stats[f"Loss/kl_{a}"] += float(kl)
                    # critics
                    if cfg.algo == "ippo":
                        for k, a in enumerate(AGENTS):
                            vl = self._value_loss(self.critics[a](o_mb).squeeze(-1), f_val[idx, k], f_ret[idx, k])
                            self._step_critic(a, vl)
                            stats[f"Loss/value_{a}"] += vl.item()
                    else:
                        vl = self._value_loss(self.critics["central"](o_mb), f_val[idx], f_ret[idx])
                        self._step_critic("central", vl)
                        stats["Loss/value"] += vl.item()
            self.it += 1
            dt_s = time.time() - t0

            # -- logging -------------------------------------------------------------------------------
            out = {k: v / max(n_upd, 1) for k, v in stats.items()}
            for k, v in logs.items():
                out[k] = sum(v) / len(v)
            if finished_ret:
                fr = torch.cat(finished_ret)
                out["Train/mean_episode_length_s"] = float(torch.cat(finished_len).mean()) * self.dt
                for k, a in enumerate(AGENTS):
                    out[f"Train/mean_return_{a}"] = float(fr[:, k].mean())
            for k, a in enumerate(AGENTS):
                out[f"Policy/lr_{a}"] = self.lr[a]
                out[f"Policy/std_{a}"] = float(self.actors[a].distribution.std_param.detach().mean())
                out[f"Effort/{a}"] = float(effort_sum[k] / T)
            out["Perf/steps_per_s"] = B / dt_s
            out["Perf/collect_s"] = collect_s
            out["Perf/iteration_s"] = dt_s
            out["Train/critic_warmup"] = float(warm)
            self._log(out)
            if self.it % 10 == 0 or self.it == 1:
                succ = out.get("Metrics/goal/success", out.get("Episode_Metrics/goal/success", float("nan")))
                lvl = out.get("Curriculum/push/level", float("nan"))
                print(f"[marl {cfg.algo}] it {self.it}/{cfg.max_iterations}  "
                      f"return {out.get('Train/mean_return_anymal', float('nan')):.2f}/"
                      f"{out.get('Train/mean_return_spot', float('nan')):.2f}  success {succ:.2f}  level {lvl}  "
                      f"{B / dt_s:.0f} steps/s{'  (critic warm-up)' if warm else ''}", flush=True)
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
        torch.nn.utils.clip_grad_norm_(self.critics[key].parameters(), self.cfg.max_grad_norm)
        opt.step()


# -- training videos ---------------------------------------------------------------------------------------
class TrainVideo:
    """Films env 0 of the training run (stochastic actions, as trained) for ``length``
    steps, from a camera that follows both robots, the object and the goal; writes
    videos/iter_<N>.mp4. Rendering failures (no EGL) switch it off with a warning."""

    W, H = 640, 480

    def __init__(self, env, folder: Path, length: int):
        self.env, self.folder, self.length = env, Path(folder), length
        self.active, self.ok = False, True
        self.started_at = 0
        self.r = None

    def _setup(self) -> None:
        import mujoco

        m = self.env.sim.mj_model
        m.vis.global_.offwidth = max(int(m.vis.global_.offwidth), self.W)
        m.vis.global_.offheight = max(int(m.vis.global_.offheight), self.H)
        self.m, self.d = m, mujoco.MjData(m)
        self.r = mujoco.Renderer(m, height=self.H, width=self.W)
        self.cam = mujoco.MjvCamera()
        self.cam.type = mujoco.mjtCamera.mjCAMERA_FREE
        self.look = None

    def start(self, it: int) -> None:
        if not self.ok:
            return
        try:
            if self.r is None:
                self._setup()
        except Exception as e:  # noqa: BLE001
            print(f"[marl] training videos off: cannot render ({e}); set MUJOCO_GL=egl on a GPU node")
            self.ok = False
            return
        import imageio_ffmpeg

        self.folder.mkdir(parents=True, exist_ok=True)
        self.path = self.folder / f"iter_{it}.mp4"
        self.wr = imageio_ffmpeg.write_frames(str(self.path), (self.W, self.H), fps=1.0 / self.env.step_dt,
                                              quality=6, ffmpeg_log_level="error")
        self.wr.send(None)
        self.active, self.n_frames, self.started_at, self.look = True, 0, it, None

    def step(self) -> Path | None:
        if not self.active:
            return None
        import mujoco
        import numpy as np

        env, sd = self.env, self.env.sim.data
        self.d.qpos[:] = sd.qpos[0].cpu().numpy()
        if self.m.nmocap:
            self.d.mocap_pos[:] = sd.mocap_pos[0].cpu().numpy()
            self.d.mocap_quat[:] = sd.mocap_quat[0].cpu().numpy()
        mujoco.mj_forward(self.m, self.d)
        g = env.command_manager.get_term("goal")
        pts = np.stack([env.scene[a].data.root_link_pos_w[0, :2].cpu().numpy() for a in AGENTS]
                       + [g.box_pos()[0, :2].cpu().numpy(), g.goal_xy[0].cpu().numpy()])
        c = pts.mean(0)
        dist = max(4.0, min(14.0, 1.1 * float(np.max(np.linalg.norm(pts[:, None] - pts[None], axis=-1))) + 3.0))
        self.look = (c, dist) if self.look is None else (0.9 * self.look[0] + 0.1 * c, 0.95 * self.look[1] + 0.05 * dist)
        self.cam.lookat[:] = [self.look[0][0], self.look[0][1], 0.3]
        self.cam.distance, self.cam.azimuth, self.cam.elevation = self.look[1], 90.0, -40.0
        self.r.update_scene(self.d, camera=self.cam)
        self.wr.send(self.r.render().tobytes())
        self.n_frames += 1
        if self.n_frames < self.length:
            return None
        self.wr.close()
        self.active = False
        return self.path


# -- loading a trained (or warm-start) checkpoint for evaluation ------------------------------------------
class CoopPolicy:
    """Deterministic two-robot policy from a model_<iter>.pt (or from two Stage 1b checkpoints)."""

    def __init__(self, env_obs: TensorDict, device: str, checkpoint: str | None = None,
                 singles: dict[str, str] | None = None):
        from rsl_rl.models.mlp_model import MLPModel

        self.actors = {a: MLPModel(env_obs, {"policy": [ACTOR_GROUPS[a]]}, "policy", 3, (256, 128, 64), "elu",
                                   obs_normalization=True, distribution_cfg=_dist_cfg(0.5)).to(device)
                       for a in AGENTS}
        if checkpoint:
            ck = torch.load(checkpoint, map_location=device, weights_only=False)
            for a in AGENTS:
                self.actors[a].load_state_dict(ck["actors"][a])
            self.iteration = int(ck["iter"])
        else:
            tmp = MarlTrainer.__new__(MarlTrainer)
            tmp.actors, tmp.device, tmp.cfg, tmp.warm_from = self.actors, device, MarlCfg(min_std=0.0), {}
            MarlTrainer.warm_start(tmp, singles or {})
            self.iteration = 0
        for a in AGENTS:
            self.actors[a].eval()

    @torch.no_grad()
    def __call__(self, obs: TensorDict) -> torch.Tensor:
        return torch.cat([self.actors[a](obs) for a in AGENTS], -1)


def newest_single(robot_dir: Path) -> Path:
    runs = sorted(p for p in robot_dir.glob("2*") if p.is_dir() and any(p.glob("model_*.pt")))
    if not runs:
        raise SystemExit(f"no dated run with model_*.pt in {robot_dir}")
    return max(runs[-1].glob("model_*.pt"), key=lambda p: int(p.stem.split("_")[1]))

