"""Stage 1 boxes and the green goal markers.

Boxes: two shapes, three copies each, so every env holds 6 boxes with different
(randomized) masses and the task can pick one whose mass fits the current curriculum
window. Unused boxes are parked far away (each env is its own MuJoCo world).

    box_cube_*   0.6 x 0.6 x 0.6 m   looks the same every 90 deg   (symmetry 4)
    box_long_*   0.5 x 1.0 x 0.6 m   looks the same every 180 deg  (symmetry 2)

The long box starts with its long side facing the robot (x = depth along the push).

Goal markers: one per shape, a flat translucent green footprint of that box (plus a
darker strip on its +x edge), with no collision. They are mocap bodies, moved at
every reset to the episode's goal pose.
"""

from __future__ import annotations

from dataclasses import dataclass

import mujoco
from mjlab.entity import EntityCfg

NOMINAL_MASS = 10.0
N_COPIES = 3
PRIORITY = 2  # the box's own friction governs its contacts (ground is 1.0, robot 1)


@dataclass(frozen=True)
class BoxShape:
    name: str
    half: tuple[float, float, float]  # half sizes x (along the push), y, z
    symmetry: int  # number of yaw angles per turn that look identical
    rgba: tuple[float, float, float, float]


SHAPES: tuple[BoxShape, ...] = (
    BoxShape("cube", (0.30, 0.30, 0.30), 4, (0.90, 0.55, 0.20, 1.0)),
    BoxShape("long", (0.25, 0.50, 0.30), 2, (0.25, 0.60, 0.85, 1.0)),
)
BOX_NAMES: tuple[str, ...] = tuple(f"box_{s.name}_{i}" for s in SHAPES for i in range(N_COPIES))
BOX_SHAPE_INDEX: tuple[int, ...] = tuple(k for k, _ in enumerate(SHAPES) for _ in range(N_COPIES))
GOAL_NAMES: tuple[str, ...] = tuple(f"goal_{s.name}" for s in SHAPES)


def _box_spec(shape: BoxShape):
    def get_spec() -> mujoco.MjSpec:
        spec = mujoco.MjSpec()
        body = spec.worldbody.add_body(name="body")
        body.add_freejoint(name="joint")
        body.add_geom(
            name="geom", type=mujoco.mjtGeom.mjGEOM_BOX, size=list(shape.half),
            mass=NOMINAL_MASS, friction=(0.5, 0.005, 0.0001), priority=PRIORITY,
            rgba=shape.rgba, group=1,
        )
        return spec

    return get_spec


def _goal_spec(shape: BoxShape):
    def get_spec() -> mujoco.MjSpec:
        spec = mujoco.MjSpec()
        body = spec.worldbody.add_body(name="body", mocap=True)
        hx, hy, _ = shape.half
        body.add_geom(  # footprint
            name="area", type=mujoco.mjtGeom.mjGEOM_BOX, size=[hx + 0.03, hy + 0.03, 0.002],
            rgba=(0.10, 0.85, 0.25, 0.35), contype=0, conaffinity=0, group=2,
        )
        body.add_geom(  # +x edge strip, shows the goal yaw
            name="edge", type=mujoco.mjtGeom.mjGEOM_BOX, size=[0.03, hy + 0.03, 0.003],
            pos=[hx + 0.03, 0.0, 0.001], rgba=(0.0, 0.45, 0.10, 0.8),
            contype=0, conaffinity=0, group=2,
        )
        return spec

    return get_spec


def get_box_cfgs() -> dict[str, EntityCfg]:
    cfgs = {}
    for k, (name, s) in enumerate(zip(BOX_NAMES, BOX_SHAPE_INDEX, strict=True)):
        shape = SHAPES[s]
        cfgs[name] = EntityCfg(
            init_state=EntityCfg.InitialStateCfg(pos=(30.0 + 3.0 * k, 0.0, shape.half[2])),
            spec_fn=_box_spec(shape),
        )
    return cfgs


def get_goal_cfgs() -> dict[str, EntityCfg]:
    return {
        name: EntityCfg(init_state=EntityCfg.InitialStateCfg(pos=(0.0, 0.0, -5.0)),
                        spec_fn=_goal_spec(shape))
        for name, shape in zip(GOAL_NAMES, SHAPES, strict=True)
    }