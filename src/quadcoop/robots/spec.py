"""The per-robot facts the walker env config needs, in one place.

Adding a robot = writing one of these. Everything else (force field, box events,
rewards, validation) is shared, so ANYmal C and Spot get identical training
recipes and differ only in body.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from mjlab.entity import EntityCfg


@dataclass(frozen=True)
class RobotSpec:
    name: str
    get_robot_cfg: Callable[[], EntityCfg]
    base_body: str
    foot_geoms: tuple[str, ...]
    foot_sites: tuple[str, ...]
    nonfoot_collision_regex: str
    action_scale: dict[str, float]
    pose_std_standing: dict[str, float]
    pose_std_walking: dict[str, float]
    push_point_b: tuple[float, float, float]
    """Base-frame point where pushing contact happens (front of the body)."""
    half_length: float
    """Base half-length (m); boxes are spawned beyond this."""
    viewer_distance: float = 2.5
