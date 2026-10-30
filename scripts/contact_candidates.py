"""Draw every shape's candidate contact regions (quadcoop/contacts.py) from above.

    python scripts/contact_candidates.py                 # nominal sizes -> evals/contacts/
    python scripts/contact_candidates.py --show-unreachable

Per shape: the footprint at body height (dark), parts outside that band (dashed: the arch's feet
and top bar), each candidate's point and push direction (arrow = -n, the way the robot pushes),
its index, and the footprint of a robot standing at it (faint). Unreachable candidates (no room
for a robot) are drawn as red crosses with --show-unreachable. Also writes candidates.json (the
common-format descriptors) and all.png (every shape on one sheet). No simulation; CPU only.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
os.environ.setdefault("QUADCOOP_SHAPES", "v2")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=str(ROOT / "evals" / "contacts"))
    ap.add_argument("--show-unreachable", action="store_true")
    ap.add_argument("--seg-len", type=float, default=0.5)
    a = ap.parse_args()

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle, Rectangle

    from quadcoop.contacts import BAND, KIND_NONE, KIND_SPHERE, band_parts, candidates, centre_of_mass
    from quadcoop.stage2.shapes import SHAPE_NAMES2, TRAIN_NAMES, kinds_tensor, nominal_parts

    parts_all, rest_all = nominal_parts("cpu")
    kinds_all = kinds_tensor("cpu")
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    record = {}
    fig_all, axes = plt.subplots(3, 4, figsize=(20, 15))

    def draw(ax, name, parts, kinds, rest, cands, all_cands):
        band = set(band_parts(parts, kinds, rest))
        for i, (p, k) in enumerate(zip(parts, kinds, strict=True)):
            if k == KIND_NONE:
                continue
            cx, cy, _, hx, hy, _ = p
            style = dict(facecolor="#555", edgecolor="k", lw=1) if i in band else \
                dict(facecolor="none", edgecolor="#888", lw=1, ls="--")
            if k == KIND_SPHERE:
                ax.add_patch(Circle((cx, cy), hx, **style))
            else:
                ax.add_patch(Rectangle((cx - hx, cy - hy), 2 * hx, 2 * hy, **style))
        com = centre_of_mass(parts, kinds)
        ax.plot(*com, "k+", ms=10)
        for c in cands:
            f = -c.n
            lat = [-f[1], f[0]]
            # robot footprint at the standing point (1.1 m x 0.6 m), faint
            corners = [c.stand + sx * 0.55 * f + sy * 0.30 * __import__("numpy").array(lat)
                       for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
            xs, ys = zip(*corners, corners[0], strict=False)
            ax.plot(xs, ys, color="#9cf", lw=0.6)
            ax.annotate("", xy=c.p, xytext=c.p + 0.35 * c.n,
                        arrowprops=dict(arrowstyle="->", color="#d40", lw=1.8))
            ax.plot([c.p[0] - 0.5 * c.width * lat[0], c.p[0] + 0.5 * c.width * lat[0]],
                    [c.p[1] - 0.5 * c.width * lat[1], c.p[1] + 0.5 * c.width * lat[1]], color="#fa0", lw=3)
            ax.text(*(c.p + 0.5 * c.n), str(c.index), ha="center", va="center", fontsize=9, color="#d40",
                    fontweight="bold")
        if a.show_unreachable:
            for c in all_cands:
                if not c.reachable:
                    ax.plot(*c.p, "rx", ms=8)
        ax.set_aspect("equal")
        lim = 2.6
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_title(f"{name}{'' if name in TRAIN_NAMES else ' (held out)'}: {len(cands)} contacts")
        ax.grid(alpha=0.2)

    for s, name in enumerate(SHAPE_NAMES2):
        parts = parts_all[s].numpy()
        kinds = kinds_all[s].numpy()
        rest = float(rest_all[s])
        all_c = candidates(parts, kinds, rest, seg_len=a.seg_len, keep_unreachable=True)
        cands = [c for c in all_c if c.reachable]
        for k, c in enumerate(cands):
            c.index = k
        record[name] = [{"index": c.index, "label": c.label, "p": c.p.round(3).tolist(), "n": c.n.round(3).tolist(),
                         "width": round(c.width, 3), "r": c.r.round(3).tolist(), "torque_of_unit_push": round(c.torque_dir, 3),
                         "clearance": round(c.clearance, 3), "descriptor": [round(x, 3) for x in c.descriptor()]}
                        for c in cands]
        fig, ax = plt.subplots(figsize=(6, 6))
        draw(ax, name, parts, kinds, rest, cands, all_c)
        fig.savefig(out / f"{name}.png", dpi=110, bbox_inches="tight")
        plt.close(fig)
        draw(axes.flat[s], name, parts, kinds, rest, cands, all_c)
        dropped = [c.label for c in all_c if not c.reachable]
        print(f"{name:10s} {len(cands):2d} contacts" + (f"   (no room for a robot: {', '.join(dropped)})" if dropped else ""))
    fig_all.suptitle(f"Candidate contacts at body height ({BAND[0]:.2f}-{BAND[1]:.2f} m): arrow = push direction, "
                     "faint box = robot standing there, + = centre of mass", fontsize=14)
    fig_all.savefig(out / "all.png", dpi=80, bbox_inches="tight")
    (out / "candidates.json").write_text(json.dumps(record, indent=1))
    print(f"\npictures and candidates.json in {out}")
    _ = math
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
