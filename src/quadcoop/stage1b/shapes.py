"""Stage 1b objects: ten shapes, each a single rigid body built from simple parts.

Every env holds one of each (unused ones parked far away). All parts get contact
priority 2, so the object's own friction (randomized 0.4-0.6, shared by its parts)
governs its contacts, except the asymmetric-friction box whose two halves are fixed
at 0.15 and 0.9.

``symmetry`` = how many yaw angles per turn look identical (0 = any yaw is fine).
``heading`` of an object is the world yaw of its body x axis, except for the lying
cylinder, whose heading is measured from its rolling axis (body y) so that rolling
does not change it. ``roller`` objects may legitimately rotate about other axes.

    cube        0.6 x 0.6 x 0.6         sym 4
    long        0.5 x 1.0               sym 2
    sphere      r 0.35                  sym 0, rolls in any direction
    cylinder    r 0.30, 1.2 long, lying sym 2, rolls across its axis
    beam        0.3 x 2.4               sym 2, spins when pushed off-centre
    l_shape     L, arm toward +x        sym 1, centre of mass off the geometry
    t_shape     T, stem toward +x       sym 1
    arch        standing doorway, 2.1 m wide, bar 1 m up   sym 2, pushing one pillar swings it
    dumbbell    two blocks on a bar     sym 2, mass at the ends
    asym        0.6 x 1.2, slick/grippy halves   sym 2, turns toward the grippy side
"""

from __future__ import annotations

import math
import os
from dataclasses import dataclass, field, replace

import mujoco
from mjlab.entity import EntityCfg

NOMINAL_MASS = 15.0
PRIORITY = 2
# Rolling resistance for the sphere and lying cylinder (MuJoCo rolling friction, in m:
# resisting torque = coef x normal force). 0.03 resists with roughly 9-10% of the
# object's weight, so a pushed roller coasts well under a metre instead of rolling away.
# Needs condim 6 contacts (sliding + torsional + rolling); the others keep condim 3.
ROLLING_FRICTION = 0.03
TORSIONAL_FRICTION = 0.02
BOX, CYL, SPH = mujoco.mjtGeom.mjGEOM_BOX, mujoco.mjtGeom.mjGEOM_CYLINDER, mujoco.mjtGeom.mjGEOM_SPHERE


@dataclass(frozen=True)
class Part:
    kind: int
    size: tuple[float, ...]
    pos: tuple[float, float, float] = (0.0, 0.0, 0.0)
    mass_frac: float = 1.0
    axis_y: bool = False  # cylinder lying with its axis along body y
    friction: float | None = None  # fixed friction (asym box); None = randomized


@dataclass(frozen=True)
class Shape:
    name: str
    parts: tuple[Part, ...]
    symmetry: int
    rest_height: float  # z of the body origin when resting
    rgba: tuple[float, float, float, float]
    roller: bool = False
    heading_axis_y: bool = False  # heading measured from body y (lying cylinder)
    fixed_friction: bool = False

    # -- derived geometry (body frame, xy) ------------------------------------------------
    def footprint(self) -> list[tuple[float, float, float, float]]:
        """(cx, cy, hx, hy) rectangles; spheres give their bounding square."""
        out = []
        for p in self.parts:
            if p.kind == BOX:
                out.append((p.pos[0], p.pos[1], p.size[0], p.size[1]))
            elif p.kind == CYL:
                r, hl = p.size
                out.append((p.pos[0], p.pos[1], r, hl) if p.axis_y else (p.pos[0], p.pos[1], r, r))
            else:
                out.append((p.pos[0], p.pos[1], p.size[0], p.size[0]))
        return out

    def bbox_half(self) -> tuple[float, float, float, float]:
        """(centre x, centre y, half x, half y) of the footprint's bounding box."""
        xs = [c - h for c, _, h, _ in self.footprint()] + [c + h for c, _, h, _ in self.footprint()]
        ys = [c - h for _, c, _, h in self.footprint()] + [c + h for _, c, _, h in self.footprint()]
        return (0.5 * (min(xs) + max(xs)), 0.5 * (min(ys) + max(ys)),
                0.5 * (max(xs) - min(xs)), 0.5 * (max(ys) - min(ys)))

    def radius(self) -> float:
        """Largest xy distance of any part corner from the body origin."""
        r = 0.0
        for cx, cy, hx, hy in self.footprint():
            for sx in (-1, 1):
                for sy in (-1, 1):
                    r = max(r, math.hypot(cx + sx * hx, cy + sy * hy))
        return r


SHAPES_V1: tuple[Shape, ...] = (
    Shape("cube", (Part(BOX, (0.30, 0.30, 0.30)),), 4, 0.30, (0.90, 0.55, 0.20, 1.0)),
    Shape("long", (Part(BOX, (0.25, 0.50, 0.30)),), 2, 0.30, (0.25, 0.60, 0.85, 1.0)),
    Shape("sphere", (Part(SPH, (0.35,)),), 0, 0.35, (0.80, 0.30, 0.60, 1.0), roller=True),
    Shape("cylinder", (Part(CYL, (0.30, 0.60), axis_y=True),), 2, 0.30, (0.35, 0.75, 0.40, 1.0),
          roller=True, heading_axis_y=True),
    Shape("beam", (Part(BOX, (0.15, 1.20, 0.25)),), 2, 0.25, (0.70, 0.45, 0.25, 1.0)),
    Shape("l_shape", (Part(BOX, (0.15, 0.60, 0.30), (0.0, 0.0, 0.0), 0.55),
                      Part(BOX, (0.45, 0.15, 0.30), (0.30, 0.45, 0.0), 0.45)),
          1, 0.30, (0.95, 0.80, 0.30, 1.0)),
    Shape("t_shape", (Part(BOX, (0.15, 0.70, 0.30), (0.0, 0.0, 0.0), 0.6),
                      Part(BOX, (0.40, 0.15, 0.30), (0.55, 0.0, 0.0), 0.4)),
          1, 0.30, (0.60, 0.80, 0.95, 1.0)),
    # Standing arch (a doorway): two pillars on wide feet, joined by a bar 1.0 m up,
    # above the robots. Its centre is open space, so there is nothing to push in the
    # middle: pushing one pillar swings it around; moving it straight takes both
    # pillars pushed together. Feet are 0.7 m deep so it slides (mu <= 0.6) before it
    # tips when a pillar is pushed at bumper height (~0.5 m).
    Shape("arch", (Part(BOX, (0.35, 0.15, 0.04), (0.0, 0.90, -0.46), 0.25),   # feet
                   Part(BOX, (0.35, 0.15, 0.04), (0.0, -0.90, -0.46), 0.25),
                   Part(BOX, (0.12, 0.12, 0.46), (0.0, 0.90, 0.04), 0.15),    # pillars
                   Part(BOX, (0.12, 0.12, 0.46), (0.0, -0.90, 0.04), 0.15),
                   Part(BOX, (0.12, 1.02, 0.08), (0.0, 0.0, 0.58), 0.20)),    # top bar
          2, 0.50, (0.85, 0.35, 0.35, 1.0)),
    Shape("dumbbell", (Part(BOX, (0.25, 0.25, 0.30), (0.0, 0.90, 0.0), 0.45),
                       Part(BOX, (0.25, 0.25, 0.30), (0.0, -0.90, 0.0), 0.45),
                       Part(BOX, (0.06, 0.65, 0.08), (0.0, 0.0, 0.0), 0.10)),
          2, 0.30, (0.45, 0.45, 0.50, 1.0)),
    Shape("asym", (Part(BOX, (0.30, 0.30, 0.30), (0.0, 0.30, 0.0), 0.5, friction=0.15),
                   Part(BOX, (0.30, 0.30, 0.30), (0.0, -0.30, 0.0), 0.5, friction=0.90)),
          2, 0.30, (0.55, 0.55, 0.55, 1.0), fixed_friction=True),
)

# Geometry v2 (QUADCOOP_SHAPES=v2, used by Stage 1c and the two-robot stage):
# * beam 0.5 m wide x 0.4 m tall (was 0.3 x 0.5): it slides instead of tipping when a
#   robot body pushes it (tipping needs half-width / push height < friction; the old
#   beam tipped at bumper height for mu > 0.3, so Spot tipped it in a third of episodes);
# * arch feet 2 cm thick (were 8 cm): the robot no longer has to step onto a sliding
#   8 cm plate to reach a pillar. Same 0.7 m depth, so it still slides before tipping.
_V2 = {
    "beam": dict(parts=(Part(BOX, (0.25, 1.20, 0.20)),), rest_height=0.20),
    "arch": dict(parts=(Part(BOX, (0.35, 0.15, 0.01), (0.0, 0.90, -0.49), 0.25),   # feet
                        Part(BOX, (0.35, 0.15, 0.01), (0.0, -0.90, -0.49), 0.25),
                        Part(BOX, (0.12, 0.12, 0.49), (0.0, 0.90, 0.01), 0.15),    # pillars
                        Part(BOX, (0.12, 0.12, 0.49), (0.0, -0.90, 0.01), 0.15),
                        Part(BOX, (0.12, 1.02, 0.08), (0.0, 0.0, 0.58), 0.20))),   # top bar
}
SHAPES_V2: tuple[Shape, ...] = tuple(replace(s, **_V2[s.name]) if s.name in _V2 else s for s in SHAPES_V1)

SHAPE_VERSION = os.environ.get("QUADCOOP_SHAPES", "v1").lower()
if SHAPE_VERSION not in ("v1", "v2"):
    raise ValueError(f"QUADCOOP_SHAPES must be v1 or v2, got {SHAPE_VERSION!r}")
SHAPES: tuple[Shape, ...] = SHAPES_V2 if SHAPE_VERSION == "v2" else SHAPES_V1
SHAPE_NAMES = tuple(s.name for s in SHAPES)
OBJ_NAMES = tuple(f"obj_{s.name}" for s in SHAPES)
GOAL_NAMES = tuple(f"goal_{s.name}" for s in SHAPES)

_Q_AXIS_Y = (math.cos(math.pi / 4), math.sin(math.pi / 4), 0.0, 0.0)  # geom z -> body y


def _obj_spec(shape: Shape, park: tuple[float, float, float]):
    def get_spec() -> mujoco.MjSpec:
        spec = mujoco.MjSpec()
        # Default pose = parked: before the first reset every object would otherwise sit
        # at the origin, inside the robot and each other.
        body = spec.worldbody.add_body(name="body", pos=list(park))
        body.add_freejoint(name="joint")
        for i, p in enumerate(shape.parts):
            size = list(p.size) + [0.0] * (3 - len(p.size))
            mu = p.friction if p.friction is not None else 0.5
            g = body.add_geom(
                name=f"geom{i}", type=p.kind, size=size, pos=list(p.pos),
                mass=NOMINAL_MASS * p.mass_frac,
                friction=(mu, TORSIONAL_FRICTION, ROLLING_FRICTION) if shape.roller else (mu, 0.005, 0.0001),
                condim=6 if shape.roller else 3,
                priority=PRIORITY, rgba=shape.rgba, group=1,
            )
            if p.axis_y:
                g.quat = list(_Q_AXIS_Y)
        return spec

    return get_spec


def _goal_spec(shape: Shape):
    def get_spec() -> mujoco.MjSpec:
        spec = mujoco.MjSpec()
        body = spec.worldbody.add_body(name="body", mocap=True)
        green = (0.10, 0.85, 0.25, 0.35)
        for i, p in enumerate(shape.parts):
            if p.kind == SPH:
                body.add_geom(name=f"area{i}", type=CYL, size=[p.size[0] + 0.03, 0.002, 0.0],
                              pos=[p.pos[0], p.pos[1], 0.0], rgba=green, contype=0, conaffinity=0, group=2)
            else:
                cx, cy, hx, hy = shape.footprint()[i]
                body.add_geom(name=f"area{i}", type=BOX, size=[hx + 0.03, hy + 0.03, 0.002],
                              pos=[cx, cy, 0.0], rgba=green, contype=0, conaffinity=0, group=2)
        if shape.symmetry != 0:  # dark strip on the +x edge marks the goal heading
            bx, by, hx, hy = shape.bbox_half()
            body.add_geom(name="edge", type=BOX, size=[0.03, min(hy, 0.3) + 0.03, 0.003],
                          pos=[bx + hx + 0.03, by, 0.001], rgba=(0.0, 0.45, 0.10, 0.8),
                          contype=0, conaffinity=0, group=2)
        return spec

    return get_spec


def get_object_cfgs() -> dict[str, EntityCfg]:
    return {
        name: EntityCfg(init_state=EntityCfg.InitialStateCfg(pos=(40.0 + 4.0 * k, 0.0, s.rest_height)),
                        spec_fn=_obj_spec(s, (40.0 + 4.0 * k, 0.0, s.rest_height)))
        for k, (name, s) in enumerate(zip(OBJ_NAMES, SHAPES, strict=True))
    }


def get_goal_cfgs() -> dict[str, EntityCfg]:
    return {
        name: EntityCfg(init_state=EntityCfg.InitialStateCfg(pos=(0.0, 0.0, -5.0)), spec_fn=_goal_spec(s))
        for name, s in zip(GOAL_NAMES, SHAPES, strict=True)
    }