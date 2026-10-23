"""Shape profiles: 2D signed-distance images of an object, computed exactly from its parts.

Every object is a union of boxes, a sphere or a lying cylinder, so the signed distance
(metres to the nearest surface; negative inside) has a closed form. Values are clipped
to [-0.3, 1.0] m and divided by 0.5, so they lie in about [-0.6, 2.0].

    top (object frame, Stage 2a)   32 x 32 over 3.6 x 3.6 m centred on the object origin.
                                    Slice at body height (0.12-0.75 m above the ground):
                                    what a robot body can touch. The arch's 2 cm feet and
                                    its 1 m top bar are not in the slice, so its doorway
                                    shows as open space between two pillars.
    top (robot frame, Stage 2b)    32 x 32 over x in [-1, 3] m, y in [-2, 2] m around the
                                    robot (x forward): the same slice, placed where the
                                    object is relative to the robot. This is what an ideal
                                    2D scan of the object would show; it is recomputed at
                                    ``map_hz`` (10 Hz by default) and held in between.
    front (object frame, both)     16 x 32: height 0-1.2 m (rows, top row = highest) by
                                    lateral position -1.8..1.8 m (columns), looking along
                                    the object's x axis: the silhouette with heights, e.g.
                                    the opening under the arch's bar.

Image layout: row 0 is the far / top edge, column 0 the left (+y) edge, so a picture of
the array looks like a map with "forward" up.
"""

from __future__ import annotations

import torch

from quadcoop.stage2.shapes import KIND_NONE, KIND_SPHERE

TOP_BAND = (0.12, 0.75)  # m above the ground
CLIP = (-0.3, 1.0)
SCALE = 0.5
OBJ_TOP = {"x": (-1.8, 1.8), "y": (-1.8, 1.8), "hw": (32, 32)}
ROBOT_TOP = {"x": (-1.0, 3.0), "y": (-2.0, 2.0), "hw": (32, 32)}
FRONT = {"y": (-1.8, 1.8), "z": (0.0, 1.2), "hw": (16, 32)}


def grid(a_range, b_range, hw, device) -> torch.Tensor:
    """(H*W, 2) sample points: rows run from a_hi down to a_lo, columns from b_hi down to b_lo."""
    h, w = hw
    a = torch.linspace(a_range[1], a_range[0], h, device=device)
    b = torch.linspace(b_range[1], b_range[0], w, device=device)
    aa, bb = torch.meshgrid(a, b, indexing="ij")
    return torch.stack([aa.reshape(-1), bb.reshape(-1)], -1)


def sdf_union(pts: torch.Tensor, centre: torch.Tensor, half: torch.Tensor, circle: torch.Tensor,
              valid: torch.Tensor) -> torch.Tensor:
    """Signed distance from points (B, M, 2) to a union of rectangles / circles (B, P, ...).

    circle: (B, P) bool, radius = half[..., 0]. valid: (B, P) bool. Returns (B, M).
    """
    d = pts.unsqueeze(2) - centre.unsqueeze(1)  # (B, M, P, 2)
    q = d.abs() - half.unsqueeze(1)
    box = torch.linalg.norm(q.clamp(min=0.0), dim=-1) + q.max(-1).values.clamp(max=0.0)
    circ = torch.linalg.norm(d, dim=-1) - half[..., 0].unsqueeze(1)
    sd = torch.where(circle.unsqueeze(1), circ, box)
    sd = torch.where(valid.unsqueeze(1), sd, torch.full_like(sd, 1e3))
    return sd.min(-1).values


def _top_inputs(parts: torch.Tensor, kinds: torch.Tensor, rest: torch.Tensor):
    """Footprints of the parts that reach into the body-height band."""
    zc = rest.unsqueeze(-1) + parts[..., 2]
    zlo, zhi = zc - parts[..., 5], zc + parts[..., 5]
    valid = (kinds != KIND_NONE) & (zhi > TOP_BAND[0]) & (zlo < TOP_BAND[1])
    return parts[..., 0:2], parts[..., 3:5], kinds == KIND_SPHERE, valid


def _to_image(sd: torch.Tensor, hw) -> torch.Tensor:
    return (sd.clamp(*CLIP) / SCALE).view(-1, 1, *hw)


def top_object_frame(parts: torch.Tensor, kinds: torch.Tensor, rest: torch.Tensor) -> torch.Tensor:
    """parts (B, P, 6), kinds (B, P), rest (B,) -> (B, 1, 32, 32)."""
    pts = grid(OBJ_TOP["x"], OBJ_TOP["y"], OBJ_TOP["hw"], parts.device).expand(parts.shape[0], -1, -1)
    c, h, circ, valid = _top_inputs(parts, kinds, rest)
    return _to_image(sdf_union(pts, c, h, circ, valid), OBJ_TOP["hw"])


def top_robot_frame(parts: torch.Tensor, kinds: torch.Tensor, rest: torch.Tensor, obj_xy_r: torch.Tensor,
                    obj_yaw_r: torch.Tensor) -> torch.Tensor:
    """Same slice on a grid around the robot. obj_xy_r: object origin in the robot's yaw
    frame (B, 2); obj_yaw_r: object heading relative to the robot (B,)."""
    b = parts.shape[0]
    pts = grid(ROBOT_TOP["x"], ROBOT_TOP["y"], ROBOT_TOP["hw"], parts.device).expand(b, -1, -1)
    rel = pts - obj_xy_r.unsqueeze(1)
    cs, sn = torch.cos(obj_yaw_r).unsqueeze(1), torch.sin(obj_yaw_r).unsqueeze(1)
    p_obj = torch.stack([cs * rel[..., 0] + sn * rel[..., 1], -sn * rel[..., 0] + cs * rel[..., 1]], -1)
    c, h, circ, valid = _top_inputs(parts, kinds, rest)
    return _to_image(sdf_union(p_obj, c, h, circ, valid), ROBOT_TOP["hw"])


def front_object_frame(parts: torch.Tensor, kinds: torch.Tensor, rest: torch.Tensor) -> torch.Tensor:
    """Silhouette looking along the object's x axis: (B, 1, 16, 32), rows = height."""
    b = parts.shape[0]
    pz = grid(FRONT["z"], FRONT["y"], FRONT["hw"], parts.device)  # (M, 2) = (z, y)
    pts = torch.stack([pz[:, 1], pz[:, 0]], -1).expand(b, -1, -1)  # (y, z)
    centre = torch.stack([parts[..., 1], rest.unsqueeze(-1) + parts[..., 2]], -1)
    half = torch.stack([parts[..., 4], parts[..., 5]], -1)
    circ = kinds == KIND_SPHERE
    half = torch.where(circ.unsqueeze(-1), parts[..., 3:4].expand_as(half), half)
    return _to_image(sdf_union(pts, centre, half, circ, kinds != KIND_NONE), FRONT["hw"])


def point_distance(parts: torch.Tensor, kinds: torch.Tensor, rest: torch.Tensor, p_obj: torch.Tensor) -> torch.Tensor:
    """Signed distance (B,) from one point per env (object frame, (B, 2)) to the body-height slice."""
    c, h, circ, valid = _top_inputs(parts, kinds, rest)
    return sdf_union(p_obj.unsqueeze(1), c, h, circ, valid)[:, 0]
