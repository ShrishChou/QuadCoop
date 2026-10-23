"""Stage 2 objects: twelve shapes with per-environment size randomization.

Seven are trained on; five are held out (never chosen during training, but present in
every scene so the evaluation can use them):

    train     cube, long, sphere, cylinder, arch, dumbbell, t_shape
    held out  beam, l_shape, asym (split friction), u_channel (new), plus (new)

Every shape is a function of up to three size factors f0, f1, f2 (1.0 = nominal), drawn
per environment at startup from ``FACTOR_RANGE`` (training: 0.8-1.2; the eval can
widen it to test sizes never seen). The factors set each part's half-size and position
in the object frame, so gaps, thicknesses and lengths vary, not just a uniform scale:

    cube       f0: side (square, so 90 deg symmetry holds)
    long       f0: depth, f1: length
    sphere     f0: radius
    cylinder   f0: radius, f1: length
    arch       f0: doorway width (1.56 m nominal), f1: pillar thickness
    dumbbell   f0: block size, f1: bar length
    t_shape    f0: stem length, f1: bar length
    beam       f0: depth, f1: length
    l_shape    f0: foot length, f1: upright length
    asym       f0: size
    u_channel  f0: arm length, f1: width
    plus       f0: arm length (equal arms, so 90 deg symmetry holds)

Heights stay nominal except the sphere and cylinder, whose radius sets how high the
object's origin rests. Part layout is static per shape (padded to MAX_PARTS); the sizes
live in a (num_envs, num_shapes, MAX_PARTS, 6) tensor the command term owns.
"""

from __future__ import annotations

import torch
from mjlab.entity import EntityCfg

from quadcoop.stage1b import shapes as s1b
from quadcoop.stage1b.shapes import BOX, CYL, SPH, Part, Shape

MAX_PARTS = 5
FACTOR_RANGE = (0.8, 1.2)
KIND_NONE, KIND_BOX, KIND_SPHERE, KIND_CYL_Y = -1, 0, 1, 2

# -- shapes (v2 geometry from Stage 1b for the existing ones) ----------------------------------
_by_name = {s.name: s for s in s1b.SHAPES_V2}
U_CHANNEL = Shape("u_channel", (Part(BOX, (0.12, 0.70, 0.30), (0.0, 0.0, 0.0), 0.4),
                                Part(BOX, (0.40, 0.12, 0.30), (0.52, 0.58, 0.0), 0.3),
                                Part(BOX, (0.40, 0.12, 0.30), (0.52, -0.58, 0.0), 0.3)),
                  1, 0.30, (0.30, 0.70, 0.70, 1.0))
PLUS = Shape("plus", (Part(BOX, (0.15, 0.70, 0.30), (0.0, 0.0, 0.0), 0.5),
                      Part(BOX, (0.70, 0.15, 0.30), (0.0, 0.0, 0.0), 0.5)),
             4, 0.30, (0.85, 0.55, 0.85, 1.0))

TRAIN_NAMES = ("cube", "long", "sphere", "cylinder", "arch", "dumbbell", "t_shape")
HELDOUT_NAMES = ("beam", "l_shape", "asym", "u_channel", "plus")
SHAPES2: tuple[Shape, ...] = tuple(_by_name[n] for n in TRAIN_NAMES + ("beam", "l_shape", "asym")) + (U_CHANNEL, PLUS)
SHAPE_NAMES2 = tuple(s.name for s in SHAPES2)
OBJ_NAMES2 = tuple(f"obj_{n}" for n in SHAPE_NAMES2)
GOAL_NAMES2 = tuple(f"goal_{n}" for n in SHAPE_NAMES2)
TRAIN_MASK = tuple(n in TRAIN_NAMES for n in SHAPE_NAMES2)


def part_kinds(shape: Shape) -> list[int]:
    out = []
    for p in shape.parts:
        if p.kind == SPH:
            out.append(KIND_SPHERE)
        elif p.kind == CYL:
            assert p.axis_y, "only lying (axis along body y) cylinders are supported"
            out.append(KIND_CYL_Y)
        else:
            out.append(KIND_BOX)
    return out + [KIND_NONE] * (MAX_PARTS - len(out))


def kinds_tensor(device) -> torch.Tensor:
    """(S, MAX_PARTS) part kinds."""
    return torch.tensor([part_kinds(s) for s in SHAPES2], device=device, dtype=torch.long)


# -- size factors -> parts ----------------------------------------------------------------------
def _box(cx, cy, cz, hx, hy, hz):
    return torch.stack(torch.broadcast_tensors(cx, cy, cz, hx, hy, hz), -1)


def shape_parts(name: str, f: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
    """Size factors (n, 3) -> parts (n, MAX_PARTS, 6) = (cx, cy, cz, hx, hy, hz) in the
    object frame, and the resting height of the object origin (n,).

    Spheres use hx = hy = hz = radius; a lying cylinder uses (radius, half length, radius).
    """
    n = f.shape[0]
    z = torch.zeros(n, device=f.device)
    f0, f1 = f[:, 0], f[:, 1]
    c = lambda v: torch.full((n,), float(v), device=f.device)  # noqa: E731
    rest = c(0.30)
    if name == "cube":
        parts = [_box(z, z, z, 0.30 * f0, 0.30 * f0, c(0.30))]
    elif name == "long":
        parts = [_box(z, z, z, 0.25 * f0, 0.50 * f1, c(0.30))]
    elif name == "sphere":
        r = 0.35 * f0
        parts, rest = [_box(z, z, z, r, r, r)], r
    elif name == "cylinder":
        r = 0.30 * f0
        parts, rest = [_box(z, z, z, r, 0.60 * f1, r)], r
    elif name == "beam":
        parts, rest = [_box(z, z, z, 0.25 * f0, 1.20 * f1, c(0.20))], c(0.20)
    elif name == "arch":
        t = 0.12 * f1
        py = 0.5 * 1.56 * f0 + t  # pillar centre: half the doorway + half a pillar
        parts = [_box(z, py, c(-0.49), c(0.35), torch.maximum(t + 0.03, c(0.15)), c(0.01)),    # feet
                 _box(z, -py, c(-0.49), c(0.35), torch.maximum(t + 0.03, c(0.15)), c(0.01)),
                 _box(z, py, c(0.01), t, t, c(0.49)),                                          # pillars
                 _box(z, -py, c(0.01), t, t, c(0.49)),
                 _box(z, z, c(0.58), c(0.12), py + t, c(0.08))]                                # bar
        rest = c(0.50)
    elif name == "dumbbell":
        b, half_bar = 0.25 * f0, 0.65 * f1
        parts = [_box(z, half_bar + b, z, b, b, c(0.30)), _box(z, -(half_bar + b), z, b, b, c(0.30)),
                 _box(z, z, z, c(0.06), half_bar, c(0.08))]
    elif name == "t_shape":
        stem, bar = 0.40 * f0, 0.70 * f1
        parts = [_box(z, z, z, c(0.15), bar, c(0.30)), _box(0.15 + stem, z, z, stem, c(0.15), c(0.30))]
    elif name == "l_shape":
        foot, up = 0.45 * f0, 0.60 * f1
        parts = [_box(z, z, z, c(0.15), up, c(0.30)), _box(-0.15 + foot, up - 0.15, z, foot, c(0.15), c(0.30))]
    elif name == "asym":
        h = 0.30 * f0
        parts = [_box(z, h, z, h, h, c(0.30)), _box(z, -h, z, h, h, c(0.30))]
    elif name == "u_channel":
        arm, half_w = 0.40 * f0, 0.70 * f1
        parts = [_box(z, z, z, c(0.12), half_w, c(0.30)),
                 _box(0.12 + arm, half_w - 0.12, z, arm, c(0.12), c(0.30)),
                 _box(0.12 + arm, -(half_w - 0.12), z, arm, c(0.12), c(0.30))]
    elif name == "plus":
        arm = 0.70 * f0
        parts = [_box(z, z, z, c(0.15), arm, c(0.30)), _box(z, z, z, arm, c(0.15), c(0.30))]
    else:
        raise KeyError(name)
    out = torch.zeros(n, MAX_PARTS, 6, device=f.device)
    out[:, :len(parts)] = torch.stack(parts, 1)
    return out, rest


def nominal_parts(device) -> tuple[torch.Tensor, torch.Tensor]:
    """(S, MAX_PARTS, 6) parts and (S,) rest heights at factor 1."""
    ones = torch.ones(1, 3, device=device)
    ps, rs = zip(*(shape_parts(s.name, ones) for s in SHAPES2), strict=True)
    return torch.cat(ps, 0), torch.cat(rs, 0)


def bbox_and_radius(parts: torch.Tensor, kinds: torch.Tensor):
    """Footprint bounding box (cx, cy, hx, hy) and reach radius from parts (..., P, 6)."""
    valid = (kinds >= 0)
    big = torch.full_like(parts[..., 0], 1e6)
    lo_x = torch.where(valid, parts[..., 0] - parts[..., 3], big).min(-1).values
    hi_x = torch.where(valid, parts[..., 0] + parts[..., 3], -big).max(-1).values
    lo_y = torch.where(valid, parts[..., 1] - parts[..., 4], big).min(-1).values
    hi_y = torch.where(valid, parts[..., 1] + parts[..., 4], -big).max(-1).values
    bbox = torch.stack([(lo_x + hi_x) / 2, (lo_y + hi_y) / 2, (hi_x - lo_x) / 2, (hi_y - lo_y) / 2], -1)
    corners = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            corners.append(torch.hypot(parts[..., 0] + sx * parts[..., 3], parts[..., 1] + sy * parts[..., 4]))
    rad = torch.where(valid, torch.stack(corners, -1).max(-1).values, torch.zeros_like(big)).max(-1).values
    return bbox, rad


def geom_size_pos(parts: torch.Tensor, kinds: torch.Tensor):
    """MuJoCo geom_size / geom_pos (..., P, 3) for the parts (padding rows are ignored)."""
    cx, cy, cz, hx, hy, hz = parts.unbind(-1)
    size = torch.stack([hx, hy, hz], -1)
    size = torch.where((kinds == KIND_SPHERE).unsqueeze(-1), torch.stack([hx, hx * 0, hx * 0], -1), size)
    size = torch.where((kinds == KIND_CYL_Y).unsqueeze(-1), torch.stack([hx, hy, hx * 0], -1), size)
    return size, torch.stack([cx, cy, cz], -1)


# -- MuJoCo entities -------------------------------------------------------------------------------
def get_object_cfgs() -> dict[str, EntityCfg]:
    out = {}
    for k, (name, s) in enumerate(zip(OBJ_NAMES2, SHAPES2, strict=True)):
        park = (40.0 + 4.0 * k, 0.0, s.rest_height)
        out[name] = EntityCfg(init_state=EntityCfg.InitialStateCfg(pos=park), spec_fn=s1b._obj_spec(s, park))
    return out


def get_goal_cfgs() -> dict[str, EntityCfg]:
    return {name: EntityCfg(init_state=EntityCfg.InitialStateCfg(pos=(0.0, 0.0, -5.0)), spec_fn=s1b._goal_spec(s))
            for name, s in zip(GOAL_NAMES2, SHAPES2, strict=True)}

