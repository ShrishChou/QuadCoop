"""Scripted turn-in-place for the Spot-arm pair (docs/spot_arm_pair.md, "Turn in place"): demonstrations and the
scripted reference. Outputs the env action in the policy's own action space (--arm hand_rate: 7 per robot, or
--arm stowed: 3), so recorded (observation, action) pairs can initialize a policy.

Per robot, every step (closed loop on the object's pose):
  - face the object: yaw toward the face the robot is on (behind the object's -x face or in front of its +x face);
  - turn sign s = sign(goal heading - heading). A couple turns the object in place: the robot behind pushes +x at one
    end, the robot in front pushes -x at the other. For s > 0 (counter-clockwise) that is each robot's right-hand
    end, for s < 0 its left. With its hand: stay centred on the face and reach to that end (hand point
    (0.80, -0.35 s, -0.05) m, body frame). Without (stowed or not allowed): side-step so the trunk is 0.30 m toward
    that end;
  - wait until the hand is out, walk in until the hand (or trunk) touches, then push: 0.2-0.5 m/s, slower near the
    goal heading, plus a drift correction (the robot on the side the centre moved away from pushes harder);
  - within ``done_deg`` of the goal heading: retract, step back, stand; re-engage beyond ``redo_deg``.
"""
from __future__ import annotations

import math

import torch

from quadcoop.coop2 import spot_arm_term as sat
from quadcoop.coop2.mdp import AGENTS
from quadcoop.robots import spot_arm as sa
from quadcoop.stage1.mdp import wrap

LONG_HALF_X = 0.25  # the long object's half depth (the pushed faces are 1 m wide)


class TurnScript:
    def __init__(self, env, use_hand: dict[str, torch.Tensor] | None = None, done_deg: float = 2.5,
                 redo_deg: float = 5.0, reach_y: float = 0.35, trunk_y: float = 0.30, drift_gain: float = 2.0):
        self.env, self.n, self.dev = env, env.num_envs, env.device
        self.g = env.command_manager.get_term("goal")
        self.terms = {a: env.action_manager.get_term(f"walker_{a}") for a in AGENTS}
        self.mode = {a: t.cfg.arm for a, t in self.terms.items()}
        assert all(m in ("hand_rate", "stowed") for m in self.mode.values()), self.mode
        self.use_hand = {a: (use_hand[a] if use_hand is not None else torch.ones(self.n, dtype=torch.bool, device=self.dev))
                         & torch.tensor(self.mode[a] == "hand_rate", device=self.dev) for a in AGENTS}
        self.done_deg, self.redo_deg = done_deg, redo_deg
        self.reach_y, self.trunk_y, self.kd = reach_y, trunk_y, drift_gain
        self.active = torch.ones(self.n, dtype=torch.bool, device=self.dev)
        self.engaged = {a: torch.zeros(self.n, dtype=torch.bool, device=self.dev) for a in AGENTS}

    def reset(self, ids=None) -> None:
        ids = slice(None) if ids is None else ids
        self.active[ids] = True
        for a in AGENTS:
            self.engaged[a][ids] = False

    def _norm(self, term, v: torch.Tensor, k: int) -> torch.Tensor:
        lo = (term.cfg.vx_range, term.cfg.vy_range, term.cfg.wz_range)[k]
        return (2 * (v - lo[0]) / (lo[1] - lo[0]) - 1).clamp(-1, 1)

    def act(self) -> torch.Tensor:
        g, env = self.g, self.env
        c = g.box_pos()[:, :2]
        psi = g.heading()
        e = g.errors()[1]  # goal - heading, folded
        ed = torch.rad2deg(e).abs()
        self.active = torch.where(ed > self.redo_deg, torch.ones_like(self.active),
                                  torch.where(ed < self.done_deg, torch.zeros_like(self.active), self.active))
        s = torch.where(e >= 0, torch.ones_like(e), -torch.ones_like(e))
        xh = torch.stack([torch.cos(psi), torch.sin(psi)], -1)
        d_n = ((c - g.goal_xy) * xh).sum(-1)  # centre drift along the face normal
        out = []
        for a in AGENTS:
            t, r = self.terms[a], env.scene[a].data
            p = r.root_link_pos_w[:, :2]
            qw = r.root_link_quat_w
            th = torch.atan2(2 * (qw[:, 0] * qw[:, 3] + qw[:, 1] * qw[:, 2]), 1 - 2 * (qw[:, 2] ** 2 + qw[:, 3] ** 2))
            sig = torch.where(((p - c) * xh).sum(-1) >= 0, torch.ones_like(psi), -torch.ones_like(psi))
            th_d = torch.where(sig < 0, psi, psi + math.pi)
            ct, st = torch.cos(th), torch.sin(th)
            dc = c - p
            qx, qy = ct * dc[:, 0] + st * dc[:, 1], -st * dc[:, 0] + ct * dc[:, 1]  # object centre, robot frame
            face = qx - LONG_HALF_X
            hand = self.use_hand[a]
            act_k = self.active
            # lateral: hand -> centred on the face; trunk -> offset toward the pushing end
            qy_goal = torch.where(hand, torch.zeros_like(qy), self.trunk_y * s)
            vy = (1.5 * (qy - qy_goal)).clamp(-0.4, 0.4)
            wz = (2.0 * wrap(th_d - th)).clamp(-0.7, 0.7)
            touching = sat.touch(env, f"arm_{a}") | sat.touch(env, f"trunk_{a}")
            self.engaged[a] = (self.engaged[a] | touching) & act_k
            if self.mode[a] == "hand_rate":
                arm_out = (t.arm_target - t.arm_goal).abs().max(-1).values < 0.1
                ready = ~hand | (arm_out & (t.blend > 0.95))
            else:
                ready = torch.ones_like(act_k)
            push = (0.2 + 0.006 * ed).clamp(max=0.5) + self.kd * sig * d_n
            vx = torch.where(self.engaged[a], push.clamp(0.0, 0.6),
                             torch.where(ready, torch.full_like(qx, 0.3), torch.zeros_like(qx)))
            # done: step back from the face, then stand
            vx = torch.where(act_k, vx, torch.where(face < 0.95, torch.full_like(qx, -0.25), torch.zeros_like(qx)))
            vy = torch.where(act_k, vy, torch.zeros_like(vy))
            base = torch.stack([self._norm(t, vx, 0), self._norm(t, vy, 1), self._norm(t, wz, 2)], -1)
            if self.mode[a] == "hand_rate":
                dt = env.step_dt
                h_des = torch.stack([torch.full_like(qx, sa.HAND_CENTER[0]), -self.reach_y * s,
                                     torch.full_like(qx, sa.HAND_CENTER[2])], -1)
                w_des = (hand & act_k).float()
                a_h = ((h_des - t.hand_cmd) / (t.cfg.hand_speed * dt)).clamp(-1, 1)
                a_h = torch.where((hand & act_k).unsqueeze(-1), a_h, torch.zeros_like(a_h))  # retracting: hold
                a_e = ((w_des - t.blend) / (t.cfg.ext_rate * dt)).clamp(-1, 1)
                out.append(torch.cat([base, a_h, a_e.unsqueeze(-1)], -1))
            else:
                out.append(base)
        return torch.cat(out, -1)
