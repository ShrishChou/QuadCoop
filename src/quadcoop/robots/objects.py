"""Pushable objects: one entity per shape, every env has all of them.

Each env's world contains one of each shape. The placement event puts at most one
in the robot's path and parks the rest far away (each env is its own MuJoCo world,
so parked objects never interact). Masses are randomized per env, per object at
startup; the object curriculum decides how heavy an object may be before it's
allowed into the path.

Geoms are in group 1 so the terrain-height raycasts (group 0) ignore them.
Sizes vary on purpose: most meet the robot at the bumper, ``obj_low`` meets the legs.
"""

from __future__ import annotations

from dataclasses import dataclass

import mujoco
from mjlab.entity import EntityCfg

NOMINAL_MASS = 12.0
FRICTION = 0.5  # nominal; randomized per env in [0.3, 0.6] by the walker config
# Higher than the ground (0) and the robot (1), so the object's own friction is what
# acts at object-ground and object-robot contacts. Without it MuJoCo takes the max of
# the pair, i.e. the ground's 1.0, and a 30 kg box would need ~300 N to slide.
PRIORITY = 2


@dataclass(frozen=True)
class ObjectSpec:
    name: str  # entity name in the scene
    geom: int  # mujoco.mjtGeom
    size: tuple[float, ...]  # MuJoCo geom size
    half_extent_x: float  # half depth along the push direction (for placement)
    half_height: float
    rgba: tuple[float, float, float, float]


OBJECTS: tuple[ObjectSpec, ...] = (
    ObjectSpec("obj_cube", mujoco.mjtGeom.mjGEOM_BOX, (0.30, 0.30, 0.35), 0.30, 0.35,
               (0.90, 0.55, 0.20, 1.0)),
    # Long side faces the robot: a rotation/steering challenge.
    ObjectSpec("obj_prism", mujoco.mjtGeom.mjGEOM_BOX, (0.25, 0.60, 0.30), 0.25, 0.30,
               (0.25, 0.60, 0.85, 1.0)),
    ObjectSpec("obj_cylinder", mujoco.mjtGeom.mjGEOM_CYLINDER, (0.30, 0.35), 0.30, 0.35,
               (0.35, 0.75, 0.40, 1.0)),
    # Rolls away when pushed: the contact load comes and goes.
    ObjectSpec("obj_sphere", mujoco.mjtGeom.mjGEOM_SPHERE, (0.35,), 0.35, 0.35,
               (0.80, 0.30, 0.60, 1.0)),
    # Tall and narrow: contact high on the body, can tip over if pushed hard.
    ObjectSpec("obj_tall", mujoco.mjtGeom.mjGEOM_BOX, (0.18, 0.18, 0.45), 0.18, 0.45,
               (0.95, 0.85, 0.30, 1.0)),
    # Low and wide: hits the legs and the lower body, not the bumper.
    ObjectSpec("obj_low", mujoco.mjtGeom.mjGEOM_BOX, (0.30, 0.50, 0.18), 0.30, 0.18,
               (0.55, 0.55, 0.60, 1.0)),
)
OBJECT_NAMES = tuple(o.name for o in OBJECTS)


def _spec_fn(obj: ObjectSpec):
    def get_spec() -> mujoco.MjSpec:
        spec = mujoco.MjSpec()
        body = spec.worldbody.add_body(name="body")
        body.add_freejoint(name="joint")
        body.add_geom(
            name="geom",
            type=obj.geom,
            size=list(obj.size) + [0.0] * (3 - len(obj.size)),
            mass=NOMINAL_MASS,
            friction=(FRICTION, 0.005, 0.0001),
            priority=PRIORITY,
            rgba=obj.rgba,
            group=1,
        )
        return spec

    return get_spec


def get_object_cfgs() -> dict[str, EntityCfg]:
    cfgs = {}
    for k, obj in enumerate(OBJECTS):
        cfgs[obj.name] = EntityCfg(
            # Parked far away until the placement event moves it.
            init_state=EntityCfg.InitialStateCfg(pos=(30.0 + 3.0 * k, 0.0, obj.half_height)),
            spec_fn=_spec_fn(obj),
        )
    return cfgs