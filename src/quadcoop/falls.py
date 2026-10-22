"""One fall rule for both robots, based on the body's pose only.

A robot has fallen when its body is on its side or upside down (tilted more than
``FALL_TILT_DEG`` from upright), or has collapsed to the ground (base lower than
``FALL_HEIGHT_FRAC`` x its normal standing height). Nothing about contacts: in a push
task legs and body touch things all the time, and a lower leg grazing the ground
while the robot walks is not a fall.

Why this replaces the contact rule Stages 0-1b used:

* ANYmal's old rule counted any non-foot collision geom touching the ground,
  including its lower-leg (shank) collision cylinders, whose bottom ends sit about
  2 cm above the sole. Eval videos show ANYmal "falling" while walking normally; in
  Stage 1b training ANYmal had contact falls but essentially no tilt falls, and every
  one of them ended the episode with a -20 penalty.
* Spot's old rule counted only its body and upper legs, so the two robots were not
  judged by the same standard.

The high-level policies only send velocity commands to frozen walkers, so a pose
rule cannot be gamed by crawling: the walker never learned to crawl.
"""

from __future__ import annotations

import torch

FALL_TILT_DEG = 60.0  # on its side is 90, upside down 180; pushing never tilts the body past ~30
FALL_HEIGHT_FRAC = 0.4  # base below 40% of standing height = collapsed onto the ground

NOMINAL_HEIGHT = {"anymal_c": 0.53, "spot": 0.45}  # RobotSpec.nominal_height

# The contact rule Stages 0-1b were trained with (kept to report what it would have said).
OLD_FALL_GEOMS = {
    "anymal_c": r".*_collision\d*$",
    "spot": r"^(body|.*_uleg)_collision$",
}


def tilt_deg(env, asset_name: str = "robot") -> torch.Tensor:
    g = env.scene[asset_name].data.projected_gravity_b
    return torch.rad2deg(torch.acos((-g[:, 2]).clamp(-1.0, 1.0)))


def base_height(env, asset_name: str = "robot") -> torch.Tensor:
    """Base height above the (flat) ground under the env."""
    return env.scene[asset_name].data.root_link_pos_w[:, 2] - env.scene.env_origins[:, 2]


def fallen(env, asset_name: str = "robot", nominal_height: float = 0.5,
           tilt_limit_deg: float = FALL_TILT_DEG, height_frac: float = FALL_HEIGHT_FRAC) -> torch.Tensor:
    """Termination / check: on its side, upside down, or collapsed."""
    return (tilt_deg(env, asset_name) > tilt_limit_deg) | (base_height(env, asset_name) < height_frac * nominal_height)


def fall_reason(env, j: int, asset_name: str = "robot", nominal_height: float = 0.5) -> str:
    t = float(tilt_deg(env, asset_name)[j])
    h = float(base_height(env, asset_name)[j])
    if t > FALL_TILT_DEG:
        return f"{'upside down' if t > 120 else 'on its side'} (tilt {t:.0f} deg)"
    return f"collapsed (base {h:.2f} m, normal {nominal_height:.2f} m)"

