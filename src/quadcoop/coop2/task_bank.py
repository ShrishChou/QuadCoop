"""Fixed training task bank: uniform or Success-Guided Sampling (SGS) over the same tasks.

A task is (env slot, column k): the slot fixes the physics (object masses, friction and sizes are
startup draws, one per slot and object for the whole run), the column fixes one training draw on
that slot - shape, object pose, goal, robot bearings / gaps / yaw noise, the turn and heavy-pair
flags. Replaying a task id on its slot reproduces all of them; only the walker's joint noise at
reset (reset_robot_joints) stays random.

    bank = generate(env, per_env=16, seed=9100)  # training-rule draws, saved with a physics snapshot
    tb = TaskBank(bank, "sgs"); tb.check_physics(env)
    env.command_manager.get_term("goal").scenario = tb   # every reset now draws a bank task

Sampling at a reset of slot e: uniform over its K tasks, or SGS: weight max(4 p (1 - p), floor),
p = the task's success estimate (EMA over its own attempts, 0.5 before the first), so tasks the
policy sometimes solves are practised most and none is dropped. Every draw and outcome is counted
(tries / succ per task), saved with each checkpoint, so a difference between arms can be traced to
which tasks were practised.

Evaluations never use the bank: scripts/eval_coop2.py builds its own env (play mode, nominal sizes,
one mass per build, scripted placements) and sets its own scenario.
"""
from __future__ import annotations

import math

import torch

KEYS = ("level", "shape", "obj_xy_rel", "obj_heading", "goal_xy_rel", "goal_yaw", "bearings", "gaps", "yaw_noise",
        "turn", "need")
PAIRED = ("bearings", "gaps", "yaw_noise")  # (.., 2): one per robot, handed to the env as a list
PHYS = ("mass", "friction", "radius", "rest")


def _goal(env):
    return env.command_manager.get_term("goal")


def _yaw(q: torch.Tensor) -> torch.Tensor:  # wxyz
    w, x, y, z = q.unbind(-1)
    return torch.atan2(2 * (w * z + x * y), 1 - 2 * (y * y + z * z))


def snapshot(env, ids: torch.Tensor, shape: torch.Tensor) -> dict:
    """What a task fixes, read back from the simulation: physics of the slot's chosen object, its
    placed pose, the goal, both robots' placed poses (xy, yaw)."""
    g = _goal(env)
    dev = ids.device
    model = env.sim.model
    body = torch.tensor([o.indexing.body_ids[0] for o in g.objs], device=dev)[shape]
    geom = torch.tensor([o.indexing.geom_ids[0] for o in g.objs], device=dev)[shape]
    gf = model.geom_friction
    out = {"mass": model.body_mass[ids, body].clone(),
           "friction": (gf[ids, geom, 0] if gf.dim() == 3 else gf[geom, 0]).clone(),
           "radius": g.radius_env[ids, shape].clone(), "rest": g.rest_env[ids, shape].clone()}
    qpos = next(iter(g.robots.values())).data.data.qpos  # the shared simulation state (as the command reads it)
    oxy = torch.zeros(len(ids), 2, device=dev)
    oyaw = torch.zeros(len(ids), device=dev)
    for k, o in enumerate(g.objs):
        here = shape == k
        if here.any():
            adr = o.indexing.free_joint_q_adr
            q = qpos[ids[here]]
            oxy[here] = q[:, adr[:2]]
            oyaw[here] = _yaw(q[:, adr[3:7]])
    out["obj_xy"], out["obj_yaw"] = oxy, oyaw
    out["goal_xy"], out["goal_yaw"] = g.goal_xy[ids].clone(), g.goal_yaw[ids].clone()
    for a, robot in g.robots.items():
        adr = robot.indexing.free_joint_q_adr
        q = qpos[ids]
        out[f"xy_{a}"] = q[:, adr[:2]].clone()
        out[f"yaw_{a}"] = _yaw(q[:, adr[3:7]])
    return out


@torch.no_grad()
def generate(env, per_env: int, seed: int) -> dict:
    """per_env training-rule draws on every slot (the command's own sampling, recorded), with the
    resulting placement read back. Leaves the envs mid-placement: reset them before stepping."""
    g = _goal(env)
    assert not g.cfg.contact_mode, "task bank: planner-free envs only (contact choices are not part of a task)"
    assert g.scenario is None, "task bank: generate with no scenario installed"
    dev = env.device
    n = env.num_envs
    ids = torch.arange(n, device=dev)
    draws, snaps = [], []
    counts0 = g.reset_counts.clone()
    with torch.random.fork_rng(devices=[torch.device(dev)] if str(dev).startswith("cuda") else []):
        torch.manual_seed(seed)
        for _ in range(per_env):
            g.draw_log = {}
            g._resample_command(ids)
            d = g.draw_log
            assert torch.equal(d["env_ids"], ids)
            draws.append({k: d[k] for k in KEYS})
            snaps.append(snapshot(env, ids, d["shape"]))
    g.draw_log = None
    g.reset_counts.copy_(counts0)  # generation is not training exposure
    tasks = {k: torch.stack([d[k] for d in draws], 1).cpu() for k in KEYS}
    snap = {k: torch.stack([s[k] for s in snaps], 1).cpu() for k in snaps[0]}
    names = [getattr(sh, "name", str(sh)) for sh in g.shape_list]
    return {"tasks": tasks, "snap": snap,
            "meta": {"per_env": per_env, "seed": seed, "num_envs": n, "shapes": names, "level": int(g.level),
                     "train_mass": list(getattr(g.cfg, "train_mass", ())),
                     "train_shapes": list(getattr(g.cfg, "train_shapes", ()))}}


class TaskBank:
    def __init__(self, bank: dict, mode: str, device: str | torch.device, ema: float = 0.3, floor: float = 0.05):
        assert mode in ("uniform", "sgs"), mode
        self.mode, self.ema, self.floor, self.device = mode, ema, floor, device
        self.meta = dict(bank["meta"])
        self.t = {k: v.to(device) for k, v in bank["tasks"].items()}
        self.snap = {k: v.to(device) for k, v in bank["snap"].items()}
        n, K = self.t["shape"].shape
        self.n, self.K = n, K
        self.cur = torch.full((n,), -1, dtype=torch.long, device=device)  # task each slot is running
        self.p = torch.full((n, K), 0.5, device=device)
        self.tries = torch.zeros(n, K, dtype=torch.long, device=device)
        self.succ = torch.zeros(n, K, device=device)
        self.forced = None  # check: every slot replays this column
        self._win_draw_shape = torch.zeros(len(self.meta["shapes"]), device=device)
        self._win_end = torch.zeros((), device=device)
        self._win_succ = torch.zeros((), device=device)
        self._win_p = torch.zeros((), device=device)
        self._win_n = torch.zeros((), device=device)

    # -- the env's scenario hook --------------------------------------------------------------------
    def weights(self, env_ids: torch.Tensor) -> torch.Tensor:
        if self.mode == "uniform":
            return torch.ones(len(env_ids), self.K, device=self.device)
        p = self.p[env_ids]
        return (4.0 * p * (1.0 - p)).clamp(min=self.floor)

    def __call__(self, env_ids: torch.Tensor) -> dict:
        if self.forced is not None:
            k = torch.full((len(env_ids),), int(self.forced), dtype=torch.long, device=self.device)
        else:
            k = torch.multinomial(self.weights(env_ids), 1).squeeze(-1)
        self.cur[env_ids] = k
        sh = self.t["shape"][env_ids, k]
        self._win_draw_shape.index_add_(0, sh, torch.ones_like(sh, dtype=torch.float))
        self._win_p += self.p[env_ids, k].sum()
        self._win_n += len(env_ids)
        out = {}
        for key in KEYS:
            if key == "level":
                continue
            v = self.t[key][env_ids, k]
            out[key] = [v[:, 0], v[:, 1]] if key in PAIRED else v
        return out

    def episode_end(self, env_ids: torch.Tensor, success: torch.Tensor) -> None:
        k = self.cur[env_ids]
        ok = k >= 0
        if not bool(ok.any()):
            return
        e, k, s = env_ids[ok], k[ok], (success[ok] > 0.5).float()
        self.tries[e, k] += 1
        self.succ[e, k] += s
        self.p[e, k] = (1.0 - self.ema) * self.p[e, k] + self.ema * s
        self._win_end += len(e)
        self._win_succ += s.sum()

    # -- checks, logging, state ---------------------------------------------------------------------
    def check_physics(self, env) -> None:
        """The slots must carry the physics the bank was drawn with (same seed, env count and config)."""
        assert env.num_envs == self.n, f"task bank: drawn for {self.n} envs, this env has {env.num_envs}"
        g = _goal(env)
        assert int(g.level) == int(self.meta["level"]), f"task bank: level {self.meta['level']}, env at {g.level}"
        assert bool((self.t["level"] == int(g.level)).all()), "task bank: tasks at another level"
        ids = torch.arange(self.n, device=self.device)
        for k in range(self.K):
            now = snapshot(env, ids, self.t["shape"][:, k])
            for key in PHYS:
                d = (now[key] - self.snap[key][:, k]).abs().max().item()
                if d > 1e-5:
                    raise RuntimeError(f"task bank: slot physics changed ({key}, column {k}, max diff {d:.3g}); "
                                       "build the env with the bank's seed / env count / config")

    def scalars(self) -> dict[str, float]:
        """This iteration's draws and outcomes, then the window restarts."""
        out = {}
        nd = float(self._win_n)
        if nd > 0:
            share = self._win_draw_shape / nd
            for i, name in enumerate(self.meta["shapes"]):
                if share[i] > 0 or name in self.meta.get("train_shapes", []):
                    out[f"Bank/draw_share_{name}"] = float(share[i])
            out["Bank/draws"] = nd
            out["Bank/p_of_drawn"] = float(self._win_p) / nd
        if float(self._win_end) > 0:
            out["Bank/success_of_ended"] = float(self._win_succ) / float(self._win_end)
        out["Bank/tasks_tried"] = float((self.tries > 0).float().mean())
        out["Bank/p_mean"] = float(self.p.mean())
        tr = self.tries.float().flatten()
        if tr.sum() > 0:
            q = tr / tr.sum()
            ent = -(q[q > 0] * q[q > 0].log()).sum()
            out["Bank/draw_entropy_norm"] = float(ent / math.log(tr.numel()))
        self._win_draw_shape.zero_()
        for v in (self._win_end, self._win_succ, self._win_p, self._win_n):
            v.zero_()
        return out

    def state(self) -> dict:
        return {"mode": self.mode, "ema": self.ema, "floor": self.floor, "meta": self.meta,
                "p": self.p.cpu(), "tries": self.tries.cpu(), "succ": self.succ.cpu()}

    def load_state(self, st: dict) -> None:
        assert st["mode"] == self.mode, f"task bank: checkpoint used {st['mode']}, this run {self.mode}"
        assert st["meta"]["seed"] == self.meta["seed"] and st["meta"]["per_env"] == self.meta["per_env"], \
            "task bank: checkpoint used another bank"
        self.p.copy_(st["p"].to(self.device))
        self.tries.copy_(st["tries"].to(self.device))
        self.succ.copy_(st["succ"].to(self.device))


@torch.no_grad()
def replay_check(env, tb: TaskBank, columns=(0, -1), tol: float = 1e-4) -> dict:
    """Replay bank columns on every slot twice (full env resets) and compare what the simulation
    holds with the bank's record: shape, physics, object pose, goal, robot placements."""
    g = _goal(env)
    ids = torch.arange(env.num_envs, device=env.device)
    rep, worst = {}, 0.0
    for col in columns:
        k = col % tb.K
        tb.forced = k
        got = []
        for _ in range(2):
            env.reset()
            assert torch.equal(g.shape[ids], tb.t["shape"][:, k]), f"column {k}: another shape"
            got.append(snapshot(env, ids, tb.t["shape"][:, k]))
        tb.forced = None
        for key, want in tb.snap.items():
            ref = want[:, k]
            for j, s in enumerate(got):
                d = s[key] - ref
                if "yaw" in key:
                    d = torch.atan2(torch.sin(d), torch.cos(d))
                m = float(d.abs().max())
                rep[f"col{k}/{key}/replay{j}"] = m
                worst = max(worst, m)
    tb.cur.fill_(-1)
    tb.tries.zero_()
    tb.succ.zero_()
    tb.p.fill_(0.5)
    tb.scalars()
    rep["worst"] = worst
    rep["pass"] = worst <= tol
    return rep
