"""Scripted contact execution: drive a robot to an assigned contact on the object and push there.

No learning. Each robot gets one candidate contact (quadcoop/contacts.py: a surface point p and
outward normal n in the object frame) and, every step, a velocity command for its frozen walker:

approach  Go to the contact's approach point (quadcoop/contacts.py: a point from which the robot,
          facing the contact, can slide straight to its standing point without touching the
          object), orbiting the object at a safe radius (facing it, moving sideways) if the
          approach point is on another side; then slide straight in to the standing point
          (p + n * (reach + standoff)) facing -n. A robot keeps clear of its partner (repulsion
          within 1.2 m) while approaching.
push      Once at the standing point and facing the contact, walk into it along -n. Speed is set by
          how far the object still has to travel along the push direction (stops when that is
          done, backs off slightly on overshoot), and is raised or lowered by whether this
          robot's push turns the object toward its goal heading (its torque r x (-n) has the
          sign of the remaining heading error) - so two robots at different contacts steer by
          pushing harder or softer. Lateral drift along the face is corrected to stay on p.
          A robot that gets pushed off (> 0.45 m from the standing point) goes back to approach.

Everything is vectorized over environments (torch); inputs are world-frame poses. The output is
the walker command (vx, vy, wz) in the robot's frame, clipped to the walkers' trained ranges.
"""

from __future__ import annotations

import math

import torch

VX, VY, WZ = (-0.6, 0.8), (-0.5, 0.5), (-0.7, 0.7)  # walker command ranges (stage1 WalkerCommandActionCfg)


def wrap(a: torch.Tensor) -> torch.Tensor:
    return torch.atan2(torch.sin(a), torch.cos(a))


def rot(v: torch.Tensor, yaw: torch.Tensor) -> torch.Tensor:
    c, s = torch.cos(yaw), torch.sin(yaw)
    return torch.stack([c * v[..., 0] - s * v[..., 1], s * v[..., 0] + c * v[..., 1]], -1)


def to_action(twist: torch.Tensor) -> torch.Tensor:
    """Walker command (vx, vy, wz) -> policy action in [-1, 1] (the action term's affine map)."""
    lo = torch.tensor([VX[0], VY[0], WZ[0]], device=twist.device)
    hi = torch.tensor([VX[1], VY[1], WZ[1]], device=twist.device)
    return 2.0 * (twist - lo) / (hi - lo) - 1.0


IDLE_ACTION = (2.0 * (0.0 - VX[0]) / (VX[1] - VX[0]) - 1.0, 0.0, 0.0)  # stand still


class ContactController:
    def __init__(self, n: int, device, reach: float = 0.55, standoff: float = 0.08, v_approach: float = 0.6,
                 v_push: float = 0.5, k_yaw: float = 1.5, orbit_margin: float = 0.45):
        self.reach, self.standoff = reach, standoff
        self.v_approach, self.v_push, self.k_yaw, self.orbit_margin = v_approach, v_push, k_yaw, orbit_margin
        self.pushing = torch.zeros(n, dtype=torch.bool, device=device)
        self.final = torch.zeros(n, dtype=torch.bool, device=device)  # sliding in from the approach point

    def reset(self, mask: torch.Tensor | None = None) -> None:
        if mask is None:
            self.pushing[:] = False
            self.final[:] = False
        else:
            self.pushing[mask] = False
            self.final[mask] = False

    def __call__(self, pos, yaw, obj_pos, obj_yaw, obj_radius, p_obj, n_obj, com_obj, goal_xy, yaw_err,
                 pre_obj=None, partner_pos=None, active=None):
        """pos (n,2), yaw (n,) robot; obj_pos (n,2), obj_yaw (n,), obj_radius (n,) object; p_obj, n_obj,
        com_obj, pre_obj (n,2) contact, centre of mass and approach point (object frame; pre_obj
        None = straight out along n); goal_xy (n,2); yaw_err (n,) signed
        remaining heading error (goal - object, folded by symmetry; 0 if irrelevant). Returns the
        walker command (n,3) in the robot frame and the phase (True = pushing)."""
        p = obj_pos + rot(p_obj, obj_yaw)
        nn = rot(n_obj, obj_yaw)
        f = -nn
        lat = torch.stack([-f[:, 1], f[:, 0]], -1)
        stand = p + nn * (self.reach + self.standoff)
        to_stand = stand - pos
        d_stand = torch.linalg.norm(to_stand, dim=-1)
        head_push = torch.atan2(f[:, 1], f[:, 0])

        pre = obj_pos + rot(pre_obj, obj_yaw) if pre_obj is not None else stand + 0.6 * nn
        # -- approach: orbit to the approach point when on another side, then slide in -------------
        d_pre = torch.linalg.norm(pre - pos, dim=-1)
        self.final = (self.final | (d_pre < 0.25)) & (d_stand < 1.8)
        rel_r, rel_s = pos - obj_pos, pre - obj_pos
        ang_r, ang_s = torch.atan2(rel_r[:, 1], rel_r[:, 0]), torch.atan2(rel_s[:, 1], rel_s[:, 0])
        diff = wrap(ang_s - ang_r)
        r_orbit = torch.maximum(torch.linalg.norm(rel_s, dim=-1), obj_radius + self.reach + self.orbit_margin)
        step = torch.sign(diff) * torch.clamp(diff.abs(), max=0.6)
        orbit_pt = obj_pos + r_orbit.unsqueeze(-1) * torch.stack([torch.cos(ang_r + step), torch.sin(ang_r + step)], -1)
        far_side = diff.abs() > math.radians(30.0)
        target = torch.where(far_side.unsqueeze(-1), orbit_pt, pre)
        target = torch.where(self.final.unsqueeze(-1), stand, target)
        v_app = 1.5 * (target - pos)
        if partner_pos is not None:  # keep clear of the partner while approaching (not in the final slide-in:
            away = pos - partner_pos  # assigned standing points are >= 0.75 m apart, so side by side is fine)
            d = torch.linalg.norm(away, dim=-1, keepdim=True).clamp(min=1e-3)
            w = torch.where(self.final, 0.0, 1.0).unsqueeze(-1)
            v_app = v_app + w * torch.clamp(1.0 - d / 1.2, min=0.0) * away / d
        sp = torch.linalg.norm(v_app, dim=-1, keepdim=True)
        v_app = v_app * torch.clamp(self.v_approach / sp.clamp(min=1e-6), max=1.0)
        to_obj = obj_pos - pos
        head_app = torch.where(self.final | (d_pre < 0.8), head_push, torch.atan2(to_obj[:, 1], to_obj[:, 0]))

        # -- push --------------------------------------------------------------------------------------
        enter = (d_stand < 0.25) & (wrap(head_push - yaw).abs() < 0.35)
        off_line = ((pos - stand) * lat).sum(-1).abs() > 0.45  # pushed sideways off the contact
        behind = ((stand - pos) * f).sum(-1) > 0.45  # fell back from the contact
        self.pushing = (self.pushing | enter) & ~(off_line | behind)
        e_l = ((p - pos) * lat).sum(-1)
        d_rem = ((goal_xy - obj_pos) * f).sum(-1)
        v = torch.clamp(1.0 * d_rem, 0.0, self.v_push)
        v = torch.where(d_rem < 0.03, torch.zeros_like(v), v)
        v = torch.where(d_rem < -0.06, torch.full_like(v, -0.15), v)
        r_w = rot(p_obj - com_obj, obj_yaw)
        tau = r_w[:, 0] * f[:, 1] - r_w[:, 1] * f[:, 0]  # z torque of a unit push here
        tau_n = tau / torch.linalg.norm(r_w, dim=-1).clamp(min=0.1)
        help_turn = yaw_err * tau_n  # > 0: pushing here turns the object the right way
        v = v * torch.clamp(1.0 + self.k_yaw * help_turn, 0.3, 1.6)
        v = torch.maximum(v, 0.2 * torch.clamp(3.0 * help_turn, 0.0, 1.0))  # turn-only pushes near the goal
        v_push = v.unsqueeze(-1) * f + torch.clamp(1.5 * e_l, -0.25, 0.25).unsqueeze(-1) * lat

        v_w = torch.where(self.pushing.unsqueeze(-1), v_push, v_app)
        head = torch.where(self.pushing, head_push, head_app)
        c, s = torch.cos(yaw), torch.sin(yaw)
        vx = c * v_w[:, 0] + s * v_w[:, 1]
        vy = -s * v_w[:, 0] + c * v_w[:, 1]
        wz = torch.clamp(2.0 * wrap(head - yaw), *WZ)
        twist = torch.stack([vx.clamp(*VX), vy.clamp(*VY), wz], -1)
        if active is not None:
            idle = torch.zeros_like(twist)
            twist = torch.where(active.unsqueeze(-1), twist, idle)
        return twist, self.pushing.clone()
