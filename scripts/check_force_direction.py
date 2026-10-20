"""Where does the push force point, and does it tip the robot?

Steps a batch of envs with the force on and reports, from what is actually written to
MuJoCo (xfrc_applied on the base):
  * vertical component of the force (must be 0: the push is horizontal)
  * angle between the force and the commanded walking direction (should mostly be ~180 deg)
  * the pitch/roll torque the force makes, and the lever arm it implies (bumper vs COM)

    python scripts/check_force_direction.py --task QuadCoop-Walker-AnymalC
"""

from __future__ import annotations

import argparse
import math
import os
import sys

# These checks exercise the bumper force field, which training leaves off by default.
os.environ.setdefault("QUADCOOP_PUSH_FORCE", "1")
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import torch  # noqa: E402

import quadcoop  # noqa: E402,F401


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True)
    ap.add_argument("--device", default=None)
    ap.add_argument("--envs", type=int, default=32)
    a = ap.parse_args()
    device = a.device or ("cuda:0" if torch.cuda.is_available() else "cpu")
    from mjlab.envs import ManagerBasedRlEnv
    from mjlab.tasks.registry import load_env_cfg
    from mjlab.utils.lab_api.math import quat_apply, yaw_quat

    cfg = load_env_cfg(a.task)
    cfg.scene.num_envs = a.envs
    pf = cfg.commands["push_force"]
    pf.warmup_env_steps = 0.0
    pf.curriculum_start_scale = 1.0
    pf.gap_s, pf.ramp_s, pf.hold_s = (0.0, 0.1), (0.1, 0.2), (1.0, 2.0)
    cfg.commands["twist"].p_override = 0.0
    cfg.commands["twist"].rel_standing_envs = 0.0
    cfg.events.pop("push_robot", None)
    for k in ("illegal_contact", "fell_over"):
        cfg.terminations.pop(k, None)
    env = ManagerBasedRlEnv(cfg=cfg, device=device)
    env.reset()
    robot = env.scene["robot"]
    term = env.command_manager.get_term("push_force")
    body = term._body_local  # noqa: SLF001
    zero = torch.zeros(env.action_space.shape, device=device)

    fz_max, f_max, angles, levers, tilt = 0.0, 0.0, [], [], []
    for _ in range(150):
        env.step(zero)
        w = robot.data.body_external_wrench[:, body]  # (n, 6): force, torque (world)
        f, tq = w[:, :3], w[:, 3:]
        fn = torch.linalg.norm(f, dim=-1)
        on = fn > 1.0
        if not on.any():
            continue
        f_max = max(f_max, float(fn.max()))
        fz_max = max(fz_max, float(f[on, 2].abs().max()))
        cmd = env.command_manager.get_command("twist")[:, :2]
        cmd_w = quat_apply(yaw_quat(robot.data.root_link_quat_w),
                           torch.cat([cmd, torch.zeros_like(cmd[:, :1])], -1))[:, :2]
        cos = (f[:, :2] * cmd_w).sum(-1) / (fn * torch.linalg.norm(cmd_w, dim=-1)).clamp(min=1e-6)
        angles.append(torch.rad2deg(torch.acos(cos.clamp(-1, 1)))[on])
        # Torque about horizontal axes per newton = vertical lever arm of the push point.
        levers.append((torch.linalg.norm(tq[:, :2], dim=-1) / fn)[on])
        tilt.append(torch.rad2deg(torch.acos(torch.clamp(-robot.data.projected_gravity_b[:, 2], -1, 1)))[on])

    ang = torch.cat(angles)
    lev = torch.cat(levers)
    print(f"[{a.task}] force on in {len(ang)} env-steps, peak {f_max:.0f} N "
          f"({f_max / term.robot_weight_n:.2f} x body weight)")
    print(f"  vertical component: max |Fz| = {fz_max:.2e} N  -> "
          f"{'horizontal (ok)' if fz_max < 1e-3 else 'NOT horizontal'}")
    opp = (ang > 150).float().mean().item()
    print(f"  angle to commanded direction: {opp:.0%} within 30 deg of straight-against "
          f"(target ~70%), median {ang.median():.0f} deg")
    print(f"  tipping torque per newton (vertical lever of bumper vs COM): "
          f"median {lev.median()*100:.1f} cm, max {lev.max()*100:.1f} cm")
    print(f"  (for scale: a 100 N push with a {lev.median()*100:.1f} cm lever = "
          f"{100*lev.median():.1f} N m of pitch torque)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())