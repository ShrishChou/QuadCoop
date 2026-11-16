"""Presentation-quality rendering, switched on with QUADCOOP_HD=1 (slurm/render_presentation.sbatch).

Off (the default) every evaluator renders exactly as before. On, every renderer that calls in here
(coop2/video.py: pair, planner and Spot-arm evaluations; eval_push.VideoMaker: push policies;
validate_walker: walkers) switches to:
  - QUADCOOP_HD_SIZE (default 1920x1080), whatever size the caller asked for;
  - 8x multisampling and 8192 px shadow maps;
  - H.264 at CRF 16 (preset slow) instead of imageio quality 6;
  - a lower three-quarter camera: azimuth + QUADCOOP_HD_CAM[0], elevation [1], distance x [2]
    (default "45,-22,0.75");
  - caption fonts scaled to the frame height;
  - push policies: one clean overview panel instead of overview + debug close-up.
"""
from __future__ import annotations

import os

ON = os.environ.get("QUADCOOP_HD", "") == "1"
SIZE = tuple(int(x) for x in os.environ.get("QUADCOOP_HD_SIZE", "1920x1080").lower().split("x"))
AZ_OFFSET, ELEVATION, DIST_SCALE = (float(x) for x in os.environ.get("QUADCOOP_HD_CAM", "45,-22,0.75").split(","))


def size(w: int, h: int) -> tuple[int, int]:
    return SIZE if ON else (w, h)


def tune(m) -> None:
    """Offscreen buffer large enough for the frame; antialiasing and sharper shadows when HD."""
    w, h = SIZE if ON else (0, 0)
    m.vis.global_.offwidth = max(int(m.vis.global_.offwidth), w)
    m.vis.global_.offheight = max(int(m.vis.global_.offheight), h)
    if ON:
        m.vis.quality.offsamples = 8
        m.vis.quality.shadowsize = 8192


def writer_kwargs() -> dict:
    """Extra imageio_ffmpeg.write_frames arguments (replace quality=6)."""
    if not ON:
        return {"quality": 6}
    return {"quality": None, "macro_block_size": 8,
            "output_params": ["-crf", "16", "-preset", "slow"]}


def view(azimuth: float, elevation: float, distance: float) -> tuple[float, float, float]:
    if not ON:
        return azimuth, elevation, distance
    return azimuth + AZ_OFFSET, ELEVATION, distance * DIST_SCALE


def font_px(base: int, height: int) -> int:
    return max(base, int(round(base * height / 480))) if ON else base
