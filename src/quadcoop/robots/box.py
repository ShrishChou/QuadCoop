"""A free-floating box the walker bumps into and pushes.

The walker never observes it. It exists so that some fraction of training sees
real body contact (friction, a load that moves away, a corner catching a leg)
rather than only an idealized force.

The geom is in group 1 so the terrain-height raycasts (group 0 only) ignore it:
otherwise a foot over the box would read "high clearance" and corrupt the
foot-clearance reward.
"""

from __future__ import annotations

import mujoco
from mjlab.entity import EntityCfg

BOX_HALF_SIZE = (0.30, 0.30, 0.35)
"""0.6 x 0.6 x 0.7 m: tall enough that both robots meet it with their bodies."""
BOX_NOMINAL_MASS = 12.0
BOX_FRICTION = 0.5


def get_box_spec() -> mujoco.MjSpec:
    spec = mujoco.MjSpec()
    body = spec.worldbody.add_body(name="box")
    body.add_freejoint(name="box_joint")
    body.add_geom(
        name="box_geom",
        type=mujoco.mjtGeom.mjGEOM_BOX,
        size=BOX_HALF_SIZE,
        mass=BOX_NOMINAL_MASS,
        friction=(BOX_FRICTION, 0.005, 0.0001),
        rgba=(0.85, 0.55, 0.2, 1.0),
        group=1,
    )
    return spec


def get_box_cfg() -> EntityCfg:
    # Starts parked far away; the placement event moves it per episode.
    return EntityCfg(
        init_state=EntityCfg.InitialStateCfg(pos=(30.0, 0.0, BOX_HALF_SIZE[2])),
        spec_fn=get_box_spec,
    )
