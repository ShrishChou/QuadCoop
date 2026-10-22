"""Stage 1c env: Stage 1b with the fixes its evaluation pointed to.

1. One fall rule for both robots, by body pose only (``quadcoop/falls.py``): on its
   side or upside down (tilt > 60 deg) or collapsed. No contact checks, so a leg
   grazing the ground while pushing no longer ends the episode.
2. Object masses uniform in 5-40 kg (Stage 1b drew them log-uniformly, so only ~14%
   of objects were over 30 kg and the heavy end was rarely practised).
3. 45 s episodes (Stage 1b: 30 s, shorter than a heavy push over 6 m takes).
4. Geometry v2 (QUADCOOP_SHAPES=v2): a beam that slides instead of tipping, arch feet
   2 cm thick (see stage1b/shapes.py).
5. The curriculum starts at level 3: the warm-started policy already handles 0-2.

Observation, action and network are unchanged, so a Stage 1b checkpoint warm-starts
it directly.
"""

from __future__ import annotations

import torch
from mjlab.envs.mdp.dr._types import Distribution
from mjlab.managers.termination_manager import TerminationTermCfg

from quadcoop import falls
from quadcoop.robots.spec import RobotSpec
from quadcoop.stage1b.env_cfg import make_hard_env_cfg
from quadcoop.stage1b.shapes import OBJ_NAMES, SHAPE_VERSION

EPISODE_S = 45.0
START_LEVEL = 3


def _uniform_mass(lo: torch.Tensor, hi: torch.Tensor, shape, device) -> torch.Tensor:
    """For pseudo_inertia's alpha (mass scales by exp(2 alpha)): mass uniform, not log-uniform."""
    s_lo, s_hi = torch.exp(2 * lo), torch.exp(2 * hi)
    s = s_lo + (s_hi - s_lo) * torch.rand(shape, device=device)
    return 0.5 * torch.log(s)


UNIFORM_MASS = Distribution(name="uniform_mass", sample=_uniform_mass)


def make_v2_env_cfg(robot: RobotSpec, play: bool = False):
    if SHAPE_VERSION != "v2":
        print("[stage1c] warning: QUADCOOP_SHAPES is not v2; using the Stage 1b geometry")
    cfg = make_hard_env_cfg(robot, play=play)

    # 1. fall = body pose (on its side / upside down / collapsed); no contact rule
    cfg.terminations.pop("fell_contact", None)
    cfg.terminations["fell_over"] = TerminationTermCfg(
        func=falls.fallen, params={"asset_name": "robot", "nominal_height": robot.nominal_height})

    # 2. uniform object masses
    for name in OBJ_NAMES:
        cfg.events[f"{name}_mass"].params["distribution"] = UNIFORM_MASS

    # 3. longer episodes, 5. start further up the curriculum
    if not play:
        cfg.episode_length_s = EPISODE_S
        cfg.commands["goal"].start_level = START_LEVEL
    return cfg
