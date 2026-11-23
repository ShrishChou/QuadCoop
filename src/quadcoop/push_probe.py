"""Push probe: what each robot's contact does to the object, split into transport and final alignment.

The same measurements for every system (scripts/eval_coop2.py --probe for the learned policies, scripts/contact_test.py
--probe for the contact planner), so a planner win and a planner loss can be compared on matched tasks.

Per step, while the episode is live (`ok`):
  phase       transport while the object is >= `region` m from the goal, alignment once inside (fixed per step)
  force       the robot's horizontal contact force on the object (push sensor, world frame)
  touching    |force| > 5 N
  goal force  force . unit vector from the object to the goal
  torque      z moment of that force about the object's centre of mass, applied at the nearest point of the true
              shape to the robot's front point (g.surface_geometry; the contact point itself is not logged by the
              sensor)
  useful      torque x sign(remaining heading error) when the heading error is > 2 deg (> 0: turns the object toward
              the goal heading); with the heading within 2 deg, every torque counts as misdirected
  side        which way the touched face points (object frame: +x, -x, +y, -y, by the larger component of the
              outward surface normal at that nearest point). Not the bounding box: on the arch the pillar faces
              lie well inside the feet's box, so a box test labels a push from behind as a side touch.
Per episode and phase: seconds, progress (distance gained, m) and heading gained (deg); per robot: touching seconds,
mean goal force and mean useful torque over the phase (N, N m; integral / phase seconds), mean |torque|, and the
touching seconds on each side. `t_align` = first entry into the alignment region.
"""
from __future__ import annotations

import math

import torch

PHASES = ("tr", "al")
SIDES = ("px", "nx", "py", "ny")


class PushProbe:
    def __init__(self, env, g, agents, half_length, region: float = 0.5, touch_n: float = 5.0):
        from quadcoop.coop2 import mdp as cm

        self.env, self.g, self.agents, self.cm = env, g, list(agents), cm
        self.hl = [float(x) for x in half_length]
        self.region, self.touch_n = region, touch_n
        n, dev = g.num_envs, g.device
        self.n, self.dev = n, dev
        self.ar = torch.arange(n, device=dev)
        self.bids = torch.tensor([o.indexing.body_ids[0] for o in g.objs], device=dev)
        R = len(self.agents)
        z = lambda *s: torch.zeros(*s, device=dev)  # noqa: E731
        self.T = {p: z(n) for p in PHASES}
        self.prog = {p: z(n) for p in PHASES}
        self.dyaw = {p: z(n) for p in PHASES}
        self.touch = {p: z(n, R) for p in PHASES}
        self.fgoal = {p: z(n, R) for p in PHASES}
        self.tuse = {p: z(n, R) for p in PHASES}
        self.tabs = {p: z(n, R) for p in PHASES}
        self.side = {p: z(n, 4) for p in PHASES}
        self.t_align = torch.full((n,), float("nan"), device=dev)
        d, e = g.errors()
        self.prev_d, self.prev_e = d.clone(), e.abs().clone()

    def _yaw(self, q):
        return torch.atan2(2.0 * (q[:, 0] * q[:, 3] + q[:, 1] * q[:, 2]), 1.0 - 2.0 * (q[:, 2] ** 2 + q[:, 3] ** 2))

    def step(self, ok: torch.Tensor, dt: float, t: float) -> None:
        g, cm = self.g, self.cm
        d, e = g.errors()
        ea = e.abs()
        okf = ok.float()
        al = d < self.region
        self.t_align = torch.where(ok & al & torch.isnan(self.t_align), torch.full_like(self.t_align, t), self.t_align)
        bp = g.box_pos()[:, :2]
        com = self.env.sim.data.xipos[self.ar, self.bids[g.shape], :2]
        ug = g.goal_xy - bp
        ug = ug / torch.linalg.norm(ug, dim=-1, keepdim=True).clamp(min=1e-6)
        by = self._yaw(g.box_quat())
        cb, sb = torch.cos(by), torch.sin(by)
        need = torch.where(ea > math.radians(2.0), torch.sign(e), torch.zeros_like(e))
        for p, m in (("tr", ~al), ("al", al)):
            w = okf * m.float()
            self.T[p] += w * dt
            self.prog[p] += w * (self.prev_d - d)
            self.dyaw[p] += w * torch.rad2deg(self.prev_e - ea)
        for k, ag in enumerate(self.agents):
            r = self.env.scene[ag]
            F = cm.object_force_from(self.env, ag)
            touching = torch.linalg.norm(F, dim=-1) > self.touch_n
            _, sw, nw, _, _ = g.surface_geometry(ag)
            rr = sw - com
            tau = rr[:, 0] * F[:, 1] - rr[:, 1] * F[:, 0]
            use = torch.where(need != 0, tau * need, -tau.abs())
            fg = (F * ug).sum(-1)
            ox, oy = cb * nw[:, 0] + sb * nw[:, 1], -sb * nw[:, 0] + cb * nw[:, 1]
            sd = torch.where(ox.abs() >= oy.abs(), torch.where(ox >= 0, 0, 1), torch.where(oy >= 0, 2, 3))
            for p, m in (("tr", ~al), ("al", al)):
                w = okf * m.float()
                self.touch[p][:, k] += w * touching.float() * dt
                self.fgoal[p][:, k] += w * fg * dt
                self.tuse[p][:, k] += w * use * dt
                self.tabs[p][:, k] += w * tau.abs() * dt
                self.side[p][self.ar, sd] += w * touching.float() * dt
        self.prev_d = torch.where(ok, d, self.prev_d)
        self.prev_e = torch.where(ok, ea, self.prev_e)

    def row(self, j: int) -> dict:
        out = {"t_align": "" if math.isnan(float(self.t_align[j])) else round(float(self.t_align[j]), 2)}
        for p in PHASES:
            T = float(self.T[p][j])
            out[f"{p}_s"] = round(T, 2)
            out[f"{p}_prog"] = round(float(self.prog[p][j]), 3)
            out[f"{p}_dyaw"] = round(float(self.dyaw[p][j]), 1)
            for k in range(len(self.agents)):
                out[f"{p}_touch{k + 1}"] = round(float(self.touch[p][j, k]), 2)
                out[f"{p}_fgoal{k + 1}"] = round(float(self.fgoal[p][j, k]) / T, 1) if T > 0 else ""
                out[f"{p}_tuse{k + 1}"] = round(float(self.tuse[p][j, k]) / T, 2) if T > 0 else ""
                out[f"{p}_tabs{k + 1}"] = round(float(self.tabs[p][j, k]) / T, 2) if T > 0 else ""
            for q, s in enumerate(SIDES):
                out[f"{p}_side_{s}"] = round(float(self.side[p][j, q]), 2)
        return out
