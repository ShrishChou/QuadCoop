"""Executor diagnosis for scripts/contact_test.py (--diag): what each robot is told to do, what it
actually does, and what the object does, per episode.

ExecDiag.observe() takes plain tensors (so it can be checked without a simulator, scripts/
diag_check.py); gather() reads them from a running coop2 env. Per robot, every live step is filed
under its command (walk / hold / push) and, inside that, under what it does: pressing the object
(touching it with at least F_PRESS N), touching lightly, not touching; moving while told to hold;
drifted off its contact zone (by distance or by heading); near the zone's edge. While pressing on
command, the force and how well its direction matches the commanded push direction. Per episode:
the object's motion (moving share, speed, direction against the planner's wanted motion, pose-error
progress) and every standstill (object still for STILL_S s or more before the goal), with each
standstill step filed by what the robots were doing:
  push_hard  told to push and pressing (the push itself does not move the object)
  push_soft  told to push but touching lightly or not at all (the executor does not push)
  wait       nobody told to push, a robot holds while its partner is off its contact (barrier wait)
  hold       nobody told to push, every robot on its contact and holding
  walk       nobody on a contact (repositioning)
The Stage 4e executor has no commands: a robot on its contact counts as told to push."""
from __future__ import annotations

import math

import torch

F_PRESS = 30.0  # N: pressing
STILL_V, STILL_W = 0.02, 0.05  # m/s, rad/s: the object is still below both
STILL_S = 3.0  # s still before it counts as a standstill
EDGE = 0.8  # on-zone time beyond this share of a threshold = near the edge
CLASSES = ("push_hard", "push_soft", "wait", "hold", "walk")

# per-episode columns (contact_test aggregates each as a mean over episodes)
KEYS = (["dg_walk", "dg_hold", "dg_push", "dg_push_press", "dg_push_light", "dg_push_notouch", "dg_hold_press", "dg_hold_move",
         "dg_drift", "dg_drift_dist", "dg_drift_head", "dg_edge", "dg_push_force", "dg_push_align", "dg_misaligned",
         "dg_both_press", "dg_one_press", "dg_none_press", "dg_obj_moving", "dg_obj_speed", "dg_obj_align", "dg_progress",
         "dg_still_n", "dg_still_s", "dg_still_force", "dg_go_breaks", "dg_flips_min"] + [f"dg_st_{c}" for c in CLASSES])


class ExecDiag:
    def __init__(self, n: int, dev, dt: float):
        z = lambda *s: torch.zeros(*s, device=dev)  # noqa: E731
        self.n, self.dt = n, dt
        self.live_t = z(n)
        self.cmd_t = z(n, 3)  # robot-seconds per command (pooled over present robots)
        self.robot_t = z(n)
        self.push_press, self.push_light, self.push_notouch = z(n), z(n), z(n)
        self.hold_press, self.hold_move = z(n), z(n)
        self.eng_t, self.drift, self.drift_dist, self.drift_head = z(n), z(n), z(n), z(n)
        self.on_t, self.edge = z(n), z(n)
        self.f_sum, self.align_sum, self.mis = z(n), z(n), z(n)
        self.both, self.one, self.none = z(n), z(n), z(n)
        self.moving, self.speed_sum, self.oalign_sum, self.oalign_t, self.prog = z(n), z(n), z(n), z(n), z(n)
        self.still_t, self.in_still = z(n), torch.zeros(n, dtype=torch.bool, device=dev)
        self.still_n, self.still_s, self.still_f, self.still_ft = z(n), z(n), z(n), z(n)
        self.st = z(n, len(CLASSES))
        self.go_prev = torch.zeros(n, dtype=torch.bool, device=dev)
        self.go_breaks = z(n)
        self.flips0 = None
        self.flips = None
        self.pe_prev = None

    @torch.no_grad()
    def observe(self, *, cmd, on, engaged, cdist, herr, thr_dist, thr_head, touch, force, push_dir, base_speed,
                v_obj, w_obj, v_want, pe, at_goal, live, present, go=None, flips=None):
        """One step. cmd (n,2) 0 walk / 1 hold / 2 push; on, engaged, touch (n,2) bool; cdist (m), herr (rad),
        base_speed (m/s) (n,2); force, push_dir (n,2,2) world, on the object / unit; v_obj, v_want (n,2);
        w_obj, pe (n); at_goal, live (n) bool; present (n,2) bool; go (n) bool or None (team pushing latch);
        flips (n) cumulative push->hold changes or None."""
        dt = self.dt
        lf = live.float()
        self.live_t += lf * dt
        rl = present & live.unsqueeze(-1)  # robot-steps that count
        rf = rl.float()
        self.robot_t += rf.sum(-1) * dt
        for c in range(3):
            self.cmd_t[:, c] += ((cmd == c) & rl).float().sum(-1) * dt
        fmag = torch.linalg.norm(force, dim=-1)
        press = touch & (fmag >= F_PRESS)
        push, hold = (cmd == 2) & rl, (cmd == 1) & rl
        self.push_press += (push & press).float().sum(-1) * dt
        self.push_light += (push & touch & ~press).float().sum(-1) * dt
        self.push_notouch += (push & ~touch).float().sum(-1) * dt
        self.hold_press += (hold & press).float().sum(-1) * dt
        self.hold_move += (hold & (base_speed > 0.15)).float().sum(-1) * dt
        eng = engaged & rl
        drift = eng & ~on
        self.eng_t += eng.float().sum(-1) * dt
        self.drift += drift.float().sum(-1) * dt
        self.drift_dist += (drift & (cdist >= thr_dist)).float().sum(-1) * dt
        self.drift_head += (drift & (herr >= thr_head)).float().sum(-1) * dt
        onr = on & rl
        self.on_t += onr.float().sum(-1) * dt
        self.edge += (onr & ((cdist > EDGE * thr_dist) | (herr > EDGE * thr_head))).float().sum(-1) * dt
        pp = push & press
        cos_f = (force * push_dir).sum(-1) / fmag.clamp(min=1e-6)
        self.f_sum += torch.where(pp, fmag, torch.zeros_like(fmag)).sum(-1) * dt
        self.align_sum += torch.where(pp, cos_f, torch.zeros_like(cos_f)).sum(-1) * dt
        self.mis += (pp & (cos_f < 0.7)).float().sum(-1) * dt
        npres = rl.sum(-1)
        npress = (press & rl).sum(-1)
        self.both += (live & (npres > 0) & (npress == npres)).float() * dt
        self.one += (live & (npress > 0) & (npress < npres)).float() * dt
        self.none += (live & (npress == 0)).float() * dt
        spd = torch.linalg.norm(v_obj, dim=-1)
        mov = live & ((spd > STILL_V) | (w_obj.abs() > STILL_W))
        self.moving += mov.float() * dt
        self.speed_sum += torch.where(live, spd, torch.zeros_like(spd)) * dt
        wn = torch.linalg.norm(v_want, dim=-1)
        ok = mov & (spd > STILL_V) & (wn > 0.02)
        cos_o = (v_obj * v_want).sum(-1) / (spd * wn).clamp(min=1e-9)
        self.oalign_sum += torch.where(ok, cos_o, torch.zeros_like(cos_o)) * dt
        self.oalign_t += ok.float() * dt
        if self.pe_prev is not None:
            self.prog += torch.where(live, self.pe_prev - pe, torch.zeros_like(pe))
        self.pe_prev = pe.clone()
        # standstills
        still = live & ~mov & ~at_goal
        self.still_t = torch.where(still, self.still_t + dt, torch.zeros_like(self.still_t))
        now = self.still_t >= STILL_S - 1e-4
        entering = now & ~self.in_still
        self.still_n += entering.float()
        self.in_still = now
        if bool(now.any()):
            # the time still before it counted as a standstill counts too (filed under the state at that moment)
            w = torch.where(entering, self.still_t, torch.full_like(self.still_t, dt))
            w = torch.where(now, w, torch.zeros_like(w))
            self.still_s += w
            any_push = push.any(-1)
            push_ok = (push & press) | ~push  # every robot told to push presses
            hard = any_push & (push & press).any(-1) & push_ok.all(-1)
            soft = any_push & ~hard
            onall = (on | ~present).all(-1)
            waitc = ~any_push & hold.any(-1) & ~onall
            holdc = ~any_push & hold.any(-1) & onall
            walkc = ~any_push & ~hold.any(-1)
            for ci, cl in enumerate((hard, soft, waitc, holdc, walkc)):
                self.st[:, ci] += torch.where(cl, w, torch.zeros_like(w))
            fh = torch.where(pp, fmag, torch.zeros_like(fmag)).sum(-1) / pp.sum(-1).clamp(min=1)
            self.still_f += torch.where(now & hard, fh, torch.zeros_like(fh)) * dt
            self.still_ft += (now & hard).float() * dt
        if go is not None:
            self.go_breaks += (live & self.go_prev & ~go).float()
            self.go_prev = go.clone()
        if flips is not None:
            if self.flips0 is None:
                self.flips0 = flips.clone()
            self.flips = flips.clone()

    def row(self, j: int) -> dict:
        r = lambda x, d=3: round(float(x), d)  # noqa: E731
        sh = lambda a, b: r(a[j] / b[j]) if float(b[j]) > 1e-9 else ""  # noqa: E731
        ct = self.cmd_t
        out = {"dg_walk": sh(ct[:, 0], self.robot_t), "dg_hold": sh(ct[:, 1], self.robot_t), "dg_push": sh(ct[:, 2], self.robot_t),
               "dg_push_press": sh(self.push_press, ct[:, 2]), "dg_push_light": sh(self.push_light, ct[:, 2]),
               "dg_push_notouch": sh(self.push_notouch, ct[:, 2]),
               "dg_hold_press": sh(self.hold_press, ct[:, 1]), "dg_hold_move": sh(self.hold_move, ct[:, 1]),
               "dg_drift": sh(self.drift, self.eng_t), "dg_drift_dist": sh(self.drift_dist, self.drift),
               "dg_drift_head": sh(self.drift_head, self.drift), "dg_edge": sh(self.edge, self.on_t),
               "dg_push_force": r(self.f_sum[j] / self.push_press[j], 0) if float(self.push_press[j]) > 0 else "",
               "dg_push_align": sh(self.align_sum, self.push_press), "dg_misaligned": sh(self.mis, self.push_press),
               "dg_both_press": sh(self.both, self.live_t), "dg_one_press": sh(self.one, self.live_t),
               "dg_none_press": sh(self.none, self.live_t),
               "dg_obj_moving": sh(self.moving, self.live_t), "dg_obj_speed": sh(self.speed_sum, self.live_t),
               "dg_obj_align": sh(self.oalign_sum, self.oalign_t), "dg_progress": sh(self.prog, self.live_t),
               "dg_still_n": int(self.still_n[j]), "dg_still_s": r(self.still_s[j], 1),
               "dg_still_force": r(self.still_f[j] / self.still_ft[j], 0) if float(self.still_ft[j]) > 0 else "",
               "dg_go_breaks": int(self.go_breaks[j]),
               "dg_flips_min": (r((self.flips[j] - self.flips0[j]) / (self.live_t[j] / 60.0), 2)
                                if self.flips is not None and float(self.live_t[j]) > 0 else "")}
        for ci, c in enumerate(CLASSES):
            out[f"dg_st_{c}"] = r(self.st[j, ci], 1)
        return out


def gather(g, base, robots, agents, present, live, object_force_from, at_goal) -> dict:
    """observe()'s inputs from a coop2 env (g = its CoopPush2Command, base = the env)."""
    n = live.shape[0]
    v2 = bool(getattr(g.cfg, "exec_v2", False))
    on = torch.stack([g.on_contact(k) for k in range(2)], -1)
    cmd = g.c_cmd.clone() if v2 else torch.where(on, torch.full_like(on, 2, dtype=torch.long), torch.zeros_like(on, dtype=torch.long))
    force = torch.stack([object_force_from(base, ag) for ag in agents], 1)
    if hasattr(g, "push_dir_obj"):
        pdir = torch.stack([g.push_dir_world(k) for k in range(2)], 1)
    else:
        pdir = torch.zeros_like(force)
    vw = g.c_vdes.clone() if hasattr(g, "c_vdes") else torch.zeros(n, 2, device=live.device)
    return dict(cmd=cmd, on=on, engaged=g.c_engaged.clone(),
                cdist=torch.stack([g.contact_dist(k) for k in range(2)], -1),
                herr=torch.stack([g.contact_heading_err(k) for k in range(2)], -1),
                thr_dist=g.cfg.drift_dist, thr_head=math.radians(g.cfg.drift_heading_deg),
                touch=torch.stack([base.scene[f"push_{ag}"].data.found.view(n, -1).any(-1) for ag in agents], -1),
                force=force, push_dir=pdir,
                base_speed=torch.stack([torch.linalg.norm(r.data.root_link_lin_vel_w[:, :2], dim=-1) for r in robots], -1),
                v_obj=g.box_vel()[:, :2], w_obj=g.box_ang_vel()[:, 2],
                v_want=vw, pe=g.pose_error(), at_goal=at_goal, live=live, present=present,
                go=g.c_go.clone() if v2 else None, flips=g.c_cmd_flips.clone() if v2 else None)
