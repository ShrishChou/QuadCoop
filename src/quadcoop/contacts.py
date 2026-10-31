"""Candidate contact regions of an object, from its geometry (the same part list the shape
profiles use), in one format for every shape.

A pushing contact is one-way: a robot standing in front of a surface pushes *into* it, along the
inward normal. So each candidate is a force primitive: a point p on the object's surface (object
frame, x/y), its outward normal n (the robot pushes along -n), the usable width of the surface
there, and the arm r = p - centre of mass (the torque of a push is r x (-n)).

How candidates are found (``candidates``):

* only surface a robot body can touch: parts that reach into the body-height band (0.12-0.70 m
  above the ground; not the arch's floor plates or its top bar), seen from above;
* boxes (and the lying cylinder, whose slice at body height is a rectangle) contribute their four
  vertical faces; spheres contribute ``sphere_sectors`` directions around their circumference;
* a face counts only where it is exposed: points just outside it must not lie inside another part
  (the inner side of a T junction is not a surface);
* exposed stretches narrower than ``min_width`` are dropped (the dumbbell's bar), longer ones are
  cut into segments of about ``seg_len`` m (two robots can share a long face);
* with ``corners``, every exposed convex corner of a box adds a contact pushed along the diagonal
  (normal = the bisector of its two faces): two robots can push a small box together from its two
  back corners, where its back face only has room for one;
* a candidate is kept only if a robot fits in front of it, facing it, with its front a few cm
  from the surface (its whole footprint clear of the object): the arch's inner pillar faces count
  if the doorway is wide enough, the inside corner of an L counts, a slot too narrow does not;
* each candidate gets an approach point ``pre``: the robot, facing the contact, can slide from
  ``pre`` straight to its standing point without touching the object (the clear lane in front
  of an outer face; sideways out of a doorway for the arch's inner faces).

Shapes in object frame: x forward, y left; normals point out of the object. ``label`` names the
face by its normal (+x / -x / +y / -y, or the sector angle) and the segment.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np

BAND = (0.12, 0.70)  # m above the ground: what a robot body can touch (profiles.TOP_BAND-like)
KIND_NONE, KIND_BOX, KIND_SPHERE, KIND_CYL_Y = -1, 0, 1, 2


@dataclass
class Contact:
    index: int
    p: np.ndarray  # (2,) point on the surface, object frame
    n: np.ndarray  # (2,) outward unit normal (push along -n)
    width: float  # usable width of the surface segment (m)
    r: np.ndarray  # (2,) p - centre of mass
    part: int
    label: str
    reachable: bool = True
    clearance: float = 0.0  # smallest distance from the standing robot's footprint to the object (m)
    stand: np.ndarray = field(default_factory=lambda: np.zeros(2))  # robot centre when pushing it
    pre: np.ndarray = field(default_factory=lambda: np.zeros(2))  # approach point: from here straight in

    @property
    def torque_dir(self) -> float:
        """z torque of a unit push at this contact: r x (-n)."""
        return float(self.r[0] * -self.n[1] - self.r[1] * -self.n[0])

    def descriptor(self) -> list[float]:
        """Common-format features: p (2), n (2), width, r (2), torque of a unit push, clearance."""
        return [*map(float, self.p), *map(float, self.n), self.width, *map(float, self.r), self.torque_dir,
                self.clearance]


def band_parts(parts: np.ndarray, kinds: np.ndarray, rest: float, band=BAND) -> list[int]:
    """Indices of parts that reach into the body-height band."""
    out = []
    for i, (p, k) in enumerate(zip(parts, kinds, strict=True)):
        if k == KIND_NONE:
            continue
        zc = rest + p[2]
        if zc + p[5] > band[0] and zc - p[5] < band[1]:
            out.append(i)
    return out


def sdf2d(pts: np.ndarray, parts: np.ndarray, kinds: np.ndarray, idx: list[int]) -> np.ndarray:
    """Signed distance (m, negative inside) from points (M, 2) to the union of the footprints of
    parts idx (boxes and the cylinder's rectangle; spheres as circles)."""
    d = np.full(len(pts), 1e3)
    for i in idx:
        cx, cy, _, hx, hy, _ = parts[i]
        q = pts - np.array([cx, cy])
        if kinds[i] == KIND_SPHERE:
            di = np.linalg.norm(q, axis=1) - hx
        else:
            a = np.abs(q) - np.array([hx, hy])
            di = np.linalg.norm(np.maximum(a, 0.0), axis=1) + np.minimum(np.max(a, axis=1), 0.0)
        d = np.minimum(d, di)
    return d


def centre_of_mass(parts: np.ndarray, kinds: np.ndarray) -> np.ndarray:
    """Volume-weighted centroid (x, y) of all parts (uniform density)."""
    w, c = 0.0, np.zeros(2)
    for p, k in zip(parts, kinds, strict=True):
        if k == KIND_NONE:
            continue
        hx, hy, hz = p[3], p[4], p[5]
        v = (4.0 / 3.0) * math.pi * hx ** 3 if k == KIND_SPHERE else (
            math.pi * hx * hx * 2 * hy if k == KIND_CYL_Y else 8 * hx * hy * hz)
        w += v
        c += v * p[:2]
    return c / max(w, 1e-9)


def _intervals(mask: np.ndarray) -> list[tuple[int, int]]:
    out, start = [], None
    for i, m in enumerate(mask):
        if m and start is None:
            start = i
        if not m and start is not None:
            out.append((start, i - 1))
            start = None
    if start is not None:
        out.append((start, len(mask) - 1))
    return out


def robot_clearance(stand: np.ndarray, facing: np.ndarray, sdf, half_len: float = 0.55,
                    half_w: float = 0.30) -> float:
    """Smallest object distance over a robot footprint centred at `stand`, facing `facing`."""
    fwd = facing / np.linalg.norm(facing)
    lat = np.array([-fwd[1], fwd[0]])
    xs = np.linspace(-half_len, half_len - 0.04, 9)
    ys = np.linspace(-half_w, half_w, 5)
    pts = np.array([stand + x * fwd + y * lat for x in xs for y in ys])
    return float(sdf(pts).min())


def approach_point(c: Contact, sdf, reach: float, half_w: float, min_clearance: float, max_run: float = 1.2,
                   dirs: int = 24) -> np.ndarray:
    """A point the robot (facing -n) can slide from straight to c.stand without touching the
    object: the free direction with the longest clear run (preferring directions along n)."""
    best, best_score = c.stand + c.n * max_run, -1e9
    for k in range(dirs):
        a = 2 * math.pi * k / dirs
        d = np.array([math.cos(a), math.sin(a)])
        run = 0.0
        while run < max_run:
            nxt = run + 0.1
            if robot_clearance(c.stand + nxt * d, -c.n, sdf, reach, half_w) < min_clearance:
                break
            run = nxt
        score = run + 0.3 * float(d @ c.n)
        if run >= 0.3 and score > best_score:
            best, best_score = c.stand + run * d, score
    return best


def candidates(parts: np.ndarray, kinds: np.ndarray, rest: float, seg_len: float = 0.5, min_width: float = 0.2,
               sphere_sectors: int = 8, reach: float = 0.55, standoff: float = 0.06, half_w: float = 0.30,
               min_clearance: float = 0.02, keep_unreachable: bool = False, corners: bool = True) -> list[Contact]:
    """Candidate contacts of one object (nominal or randomized parts; see the module docstring).

    parts (P, 6) = (cx, cy, cz, hx, hy, hz) object frame; kinds (P,); rest = height of the object
    origin above the ground. reach / half_w: the robot's half-length (front at reach from its
    centre) and half-width, used for the clearance test."""
    parts, kinds = np.asarray(parts, float), np.asarray(kinds, int)
    idx = band_parts(parts, kinds, rest)
    sdf = lambda q: sdf2d(np.atleast_2d(q), parts, kinds, idx)  # noqa: E731
    com = centre_of_mass(parts, kinds)
    out: list[Contact] = []
    step = 0.02
    for i in idx:
        cx, cy, _, hx, hy, _ = parts[i]
        if kinds[i] == KIND_SPHERE:
            for k in range(sphere_sectors):
                a = 2 * math.pi * k / sphere_sectors
                n = np.array([math.cos(a), math.sin(a)])
                p = np.array([cx, cy]) + hx * n
                if sdf(p + 0.03 * n)[0] <= 0.0:
                    continue
                out.append(Contact(0, p, n, 2 * math.pi * hx / sphere_sectors, p - com, i, f"sector {math.degrees(a):.0f}"))
            continue
        for axis, sign, name in ((0, 1, "+x"), (0, -1, "-x"), (1, 1, "+y"), (1, -1, "-y")):
            n = np.zeros(2)
            n[axis] = sign
            along = 1 - axis
            half_face = (hx, hy)[along]
            ts = np.arange(-half_face + step / 2, half_face, step)
            base = np.array([cx, cy], float)
            base[axis] += sign * (hx, hy)[axis]
            pts = np.repeat(base[None], len(ts), 0)
            pts[:, along] += ts
            exposed = sdf(pts + 0.03 * n) > 0.0
            for a0, a1 in _intervals(exposed):
                lo, hi = ts[a0] - step / 2, ts[a1] + step / 2
                length = hi - lo
                if length < min_width:
                    continue
                nseg = max(1, int(round(length / seg_len)))
                w = length / nseg
                for s in range(nseg):
                    p = base.copy()
                    p[along] += lo + (s + 0.5) * w
                    lab = f"part {i} {name}" + (f" seg {s + 1}/{nseg}" if nseg > 1 else "")
                    out.append(Contact(0, p, n.copy(), float(w), p - com, i, lab))
        if corners:
            for sx in (1, -1):
                for sy in (1, -1):
                    cpt = np.array([cx + sx * hx, cy + sy * hy])
                    n = np.array([sx, sy], float) / math.sqrt(2.0)
                    faces_ok = (sdf(cpt + np.array([0.0, -sy * 0.03]) + np.array([sx * 0.03, 0.0]))[0] > 0.0 and
                                sdf(cpt + np.array([-sx * 0.03, 0.0]) + np.array([0.0, sy * 0.03]))[0] > 0.0)
                    if not faces_ok or sdf(cpt + 0.05 * n)[0] <= 0.0:
                        continue
                    lab = f"part {i} corner {'+' if sx > 0 else '-'}x{'+' if sy > 0 else '-'}y"
                    out.append(Contact(0, cpt, n, 0.1, cpt - com, i, lab))
    keep = []
    for c in out:
        c.stand = c.p + c.n * (reach + standoff)
        c.clearance = robot_clearance(c.stand, -c.n, sdf, reach, half_w)
        c.reachable = c.clearance >= min_clearance
        c.pre = approach_point(c, sdf, reach, half_w, min_clearance) if c.reachable else c.stand.copy()
        if c.reachable or keep_unreachable:
            keep.append(c)
    keep.sort(key=lambda c: math.atan2(c.p[1] - com[1], c.p[0] - com[0]))
    for k, c in enumerate(keep):
        c.index = k
    return keep


# -- goal-relative assignment rules for two robots ------------------------------------------------
def back_contacts(cands: list[Contact], u: np.ndarray, max_angle_deg: float = 45.0) -> list[Contact]:
    """Candidates whose push (-n) points within max_angle of the desired motion u (object frame)."""
    u = u / max(np.linalg.norm(u), 1e-9)
    cos = math.cos(math.radians(max_angle_deg))
    back = [c for c in cands if float(-c.n @ u) >= cos]
    if not back and cands:  # nothing faces the goal well enough: the best-aligned one
        back = [max(cands, key=lambda c: float(-c.n @ u))]
    return back


def match(cands: list[Contact], pair: tuple[int | None, int | None], robots_obj: np.ndarray) -> tuple[int | None, int | None]:
    """Give the two contacts of `pair` to the two robots so the total walk is shortest (robots_obj:
    (2, 2) robot positions in the object frame), so their paths do not cross."""
    a, b = pair
    if a is None or b is None:
        return pair
    by = {c.index: c for c in cands}
    keep = np.linalg.norm(robots_obj[0] - by[a].pre) + np.linalg.norm(robots_obj[1] - by[b].pre)
    swap = np.linalg.norm(robots_obj[0] - by[b].pre) + np.linalg.norm(robots_obj[1] - by[a].pre)
    return (b, a) if swap < keep else (a, b)


def assign(cands: list[Contact], u: np.ndarray, rule: str, wide_angle_deg: float = 75.0,
           min_sep: float = 0.75) -> tuple[int | None, int | None]:
    """Contact indices (robot 1, robot 2) for motion direction u (object frame).

    centre   robot 1 at the back contact pushing closest to the centre of mass; robot 2 none (solo)
    adjacent both robots on back contacts as close to the centre line as they fit side by side
    spread   the two back contacts farthest apart across the motion (one per end / pillar / half)

    Two contacts form a usable pair only if the robots' standing points are min_sep apart (robots are
    ~0.6 m wide). If no pair faces the goal within 45 deg, the two-robot rules look within
    wide_angle_deg (neighbouring faces, which push partly sideways); if there is still no pair, robot
    2 gets None (it stands aside: the object has no room for two pushers that way). Which robot takes
    which contact is decided by ``match``, from where the robots are.
    """
    u = u / max(np.linalg.norm(u), 1e-9)
    lat = np.array([-u[1], u[0]])
    back = back_contacts(cands, u)
    if not back:
        return None, None
    by_centre = sorted(back, key=lambda c: abs(c.torque_dir))
    if rule == "centre":
        return by_centre[0].index, None
    if rule not in ("adjacent", "spread"):
        raise ValueError(rule)

    def pairs(group):
        return [(a, b) for i, a in enumerate(group) for b in group[i + 1:]
                if np.linalg.norm(a.stand - b.stand) >= min_sep]

    ok = pairs(back) or pairs(back_contacts(cands, u, wide_angle_deg))
    if not ok:
        return by_centre[0].index, None
    if rule == "adjacent":
        a, b = min(ok, key=lambda ab: abs(float(ab[0].r @ lat)) + abs(float(ab[1].r @ lat)))
    else:
        a, b = max(ok, key=lambda ab: abs(float((ab[0].p - ab[1].p) @ lat)))
    if float(a.p @ lat) < float(b.p @ lat):  # robot 1 on the left of the motion
        a, b = b, a
    return a.index, b.index


def random_pair(cands: list[Contact], u: np.ndarray, rng, min_sep: float = 0.85) -> tuple[int | None, int | None]:
    """A random usable pair (standing points min_sep apart) of contacts pushing within 46 deg of u,
    else within 75 deg, else any; as the Stage 4 training draws its random pairs."""
    u = u / max(np.linalg.norm(u), 1e-9)
    for ang in (46.0, 75.0, 180.0):
        cos = math.cos(math.radians(ang))
        back = [c for c in cands if float(-c.n @ u) >= cos - 1e-9]
        pairs = [(a, b) for i, a in enumerate(back) for b in back[i + 1:] if np.linalg.norm(a.stand - b.stand) >= min_sep]
        if pairs:
            a, b = pairs[rng.randrange(len(pairs))]
            return (a.index, b.index) if rng.random() < 0.5 else (b.index, a.index)
    return (cands[0].index if cands else None), None
