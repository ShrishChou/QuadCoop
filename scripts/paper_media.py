"""Build paper_media/: video stills and filmstrips, object-map renders, and graphs for the paper.

CPU only (ffmpeg from imageio-ffmpeg, matplotlib, torch on CPU). Sources: presentation_export/ and
presentation_videos/ (films), evals_present/ and logs/evals/ (numbers). Re-run to rebuild; existing outputs are
overwritten.

    python scripts/paper_media.py [frames] [maps] [graphs] [copy] [objects] [starts] [intro] [library]     (default: all)

objects and starts render in MuJoCo with software EGL (no GPU): the twelve objects, and the single robot's start positions.
"""

from __future__ import annotations

import csv
import io
import re
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "paper_media"
PE = ROOT / "presentation_export"
PV = ROOT / "presentation_videos"


def ffmpeg() -> str:
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def duration(v: Path) -> float:
    err = subprocess.run([ffmpeg(), "-i", str(v)], capture_output=True, text=True).stderr
    h, m, s = re.search(r"Duration: (\d+):(\d+):([\d.]+)", err).groups()
    return int(h) * 3600 + int(m) * 60 + float(s)


def grab(v: Path, t: float) -> Image.Image:
    b = subprocess.run([ffmpeg(), "-v", "error", "-ss", f"{t:.2f}", "-i", str(v), "-frames:v", "1", "-f", "image2pipe",
                        "-vcodec", "png", "-"], capture_output=True, check=True).stdout
    return Image.open(io.BytesIO(b)).convert("RGB")


def crop_caption(img: Image.Image) -> Image.Image:
    """Drop the burned-in caption bar at the top: rows that are mostly near-black / navy background with text (the
    rendered scene's floor and sky are lighter blue). Cut below the last such row in the top third."""
    a = np.asarray(img).astype(np.int16)
    dark = (a.max(-1) < 70).mean(1)  # share of near-black / navy pixels per row
    cap = np.nonzero(dark[: len(dark) // 3] > 0.5)[0]
    top = int(cap.max()) + 3 if len(cap) else 0
    return img.crop((0, top, img.width, img.height)) if top > 2 else img


def panel(img: Image.Image, which: str | None) -> Image.Image:
    if which is None:
        return img
    w = img.width // 2
    return img.crop((0, 0, w, img.height)) if which == "left" else img.crop((w, 0, img.width, img.height))


def label(img: Image.Image, text: str) -> Image.Image:
    d = ImageDraw.Draw(img)
    size = max(14, img.width // 28)
    try:
        import matplotlib
        font = ImageFont.truetype(str(Path(matplotlib.get_data_path()) / "fonts/ttf/DejaVuSans-Bold.ttf"), size)
    except (OSError, ImportError):
        font = ImageFont.load_default()
    x0, y0, x1, y1 = d.textbbox((0, 0), text, font=font)
    pad = size // 3
    d.rectangle((0, 0, x1 - x0 + 2 * pad, y1 - y0 + 2 * pad), fill=(255, 255, 255))
    d.text((pad - x0, pad - y0), text, fill=(0, 0, 0), font=font)
    return img


def frames_at(v: Path, times, which=None, crop=True):
    d = duration(v)
    out = []
    for t in times:
        t = t * d if t <= 1.0 else min(t, d - 0.1)
        f = panel(grab(v, t), which)
        out.append((crop_caption(f) if crop else f, t))
    return out


def save_still(v, t, name, which=None, crop=True):
    (img, _), = frames_at(v, [t], which, crop)
    p = OUT / name
    p.parent.mkdir(parents=True, exist_ok=True)
    img.save(p, quality=93)
    return p


def save_strip(v, times, name, which=None, crop=True, width=640, stamp=True, t0=0.0):
    """times: fractions of the clip (<= 1) or seconds into it (> 1). t0 is added to the stamped time (a branch film
    starts 4 s before its 20 s decision, so t0 = 16 stamps episode time)."""
    fr = frames_at(v, times, which, crop)
    ims = []
    for img, t in fr:
        img = img.resize((width, round(img.height * width / img.width)), Image.LANCZOS)
        ims.append(label(img, f"t = {t + t0:.0f} s") if stamp else img)
    gap = 6
    h = min(i.height for i in ims)
    strip = Image.new("RGB", (len(ims) * width + (len(ims) - 1) * gap, h), (255, 255, 255))
    for i, im in enumerate(ims):
        strip.paste(im.crop((0, 0, width, h)), (i * (width + gap), 0))
    p = OUT / name
    p.parent.mkdir(parents=True, exist_ok=True)
    strip.save(p, quality=93)
    return p


def grid_stills(items, name, cols, width=640):
    """items: (video, t, which, label). One labelled still per cell."""
    ims = []
    for v, t, which, lab in items:
        (img, _), = frames_at(v, [t], which)
        img = img.resize((width, round(img.height * width / img.width)), Image.LANCZOS)
        ims.append(label(img, lab))
    h = min(i.height for i in ims)
    rows = (len(ims) + cols - 1) // cols
    gap = 6
    g = Image.new("RGB", (cols * width + (cols - 1) * gap, rows * h + (rows - 1) * gap), (255, 255, 255))
    for i, im in enumerate(ims):
        g.paste(im.crop((0, 0, width, h)), ((i % cols) * (width + gap), (i // cols) * (h + gap)))
    p = OUT / name
    p.parent.mkdir(parents=True, exist_ok=True)
    g.save(p, quality=93)
    return p


def _one(folder: Path, prefix: str) -> Path:
    """The first successful clip in folder whose name starts with prefix."""
    return sorted(folder.glob(f"{prefix}*__success.mp4"))[0]


def _joined(v: Path, key: str) -> None:
    """A team clip must show the added robot: its JSON's right-hand arm has key (t_add3 / t_add4) set."""
    import json
    js = json.loads(v.with_suffix(".json").read_text())
    if not re.findall(rf'"{key}": (\d)', json.dumps(js)):
        raise SystemExit(f"{v.name}: the added robot never joined ({key} empty), pick another clip")


# ---------------------------------------------------------------- frames
def build_frames():
    W = PE / "01_walkers"
    # robots and walkers (1080p renders, no captions)
    save_still(W / "anymal_walk_forward.mp4", 0.5, "01_robots_walkers/anymal_walking.jpg", crop=False)
    save_still(W / "spot_walk_forward.mp4", 0.5, "01_robots_walkers/spot_walking.jpg", crop=False)
    save_still(W / "anymal_push_cube_30kg.mp4", 0.5, "01_robots_walkers/anymal_walker_into_30kg_cube.jpg", crop=False)
    save_still(W / "anymal_push_cube_30kg_side.mp4", 0.5, "01_robots_walkers/anymal_walker_into_30kg_cube_side.jpg",
               crop=False)
    save_still(W / "spot_push_cube_30kg.mp4", 0.5, "01_robots_walkers/spot_walker_into_30kg_cube.jpg", crop=False)
    save_still(W / "anymal_resist_push.mp4", 0.5, "01_robots_walkers/anymal_resisting_push.jpg", crop=False)
    save_still(W / "anymal_fleet_corner.mp4", 0.75, "01_robots_walkers/parallel_training_envs.jpg", crop=False)
    save_still(W / "anymal_fleet_flyover.mp4", 0.5, "01_robots_walkers/parallel_training_envs_flyover.jpg", crop=False)
    grid_stills([(W / "anymal_walk_forward.mp4", 0.5, None, "ANYmal"),
                 (W / "spot_walk_forward.mp4", 0.5, None, "Spot")], "01_robots_walkers/robots_side_by_side.jpg", 2, 960)
    save_strip(W / "anymal_walk_forward.mp4", [0.05, 0.35, 0.65, 0.95], "01_robots_walkers/anymal_walk_strip.jpg",
               crop=False)
    save_strip(W / "anymal_push_cube_30kg_side.mp4", [0.05, 0.35, 0.65, 0.95],
               "01_robots_walkers/anymal_cube_push_strip.jpg", crop=False)

    # Objects are spread across the folders (not only the arch and the long box). Every clip below is a success, and
    # every team clip is one where the added robot joined (checked against the clip's JSON).
    Q = [0.02, 0.33, 0.66, 0.98]

    # single robot with its push policy (map + CNN)
    S = PE / "02_anymal_single_robot_push"
    save_strip(S / "60kg" / "cube_60kg_D_far_turn_rep7__success.mp4", Q, "02_single_robot/single_anymal_cube_60kg_far_turn_strip.jpg")
    save_strip(S / "80kg" / "t_shape_80kg_C_backright_rep4__success.mp4", Q,
               "02_single_robot/single_anymal_t_shape_80kg_backright_strip.jpg")
    save_strip(S / "80kg" / "sphere_80kg_D_far_turn_rep3__success.mp4", Q,
               "02_single_robot/single_anymal_sphere_80kg_far_turn_strip.jpg")
    save_strip(S / "40kg" / "arch_40kg_C_backright_rep0__success.mp4", Q, "02_single_robot/single_anymal_arch_40kg_strip.jpg")
    grid_stills([(_one(S / "60kg", "cube_60kg_A"), 0.5, None, "cube 60 kg"),
                 (_one(S / "80kg", "sphere_80kg_B"), 0.5, None, "sphere 80 kg"),
                 (_one(S / "80kg", "cylinder_80kg_A"), 0.5, None, "cylinder 80 kg"),
                 (_one(S / "60kg", "dumbbell_60kg_A"), 0.5, None, "dumbbell 60 kg"),
                 (_one(S / "60kg", "l_shape_60kg_A"), 0.5, None, "L shape 60 kg"),
                 (_one(S / "40kg", "u_channel_40kg_A"), 0.5, None, "U channel 40 kg")],
                "02_single_robot/single_anymal_objects_grid.jpg", 3)

    # IPPO / MAPPO pairs
    F = PV / "05_ippo_mappo_final_trained"
    I, M = PE / "03_anymal_ippo_pair", PE / "04_anymal_mappo_pair"
    save_strip(M / "mappo_dumbbell_80kg_A_straight_rep0__success.mp4", Q, "03_ippo_mappo/mappo_dumbbell_80kg_strip.jpg")
    save_strip(M / "mappo_plus_80kg_B_left_rep0__success.mp4", Q, "03_ippo_mappo/mappo_plus_80kg_left_strip.jpg")
    save_strip(I / "ippo_cube_80kg_D_far_turn_rep0__success.mp4", Q, "03_ippo_mappo/ippo_cube_80kg_far_turn_strip.jpg")
    save_strip(I / "ippo_sphere_80kg_C_backright_rep0__success.mp4", Q, "03_ippo_mappo/ippo_sphere_80kg_backright_strip.jpg")
    save_strip(F / "ippo_l_shape_80kg__success.mp4", Q, "03_ippo_mappo/ippo_l_shape_80kg_strip.jpg")
    save_strip(F / "mappo_long_40kg_far_turn__success.mp4", Q, "03_ippo_mappo/mappo_long_40kg_far_turn_strip.jpg")
    save_still(M / "mappo_dumbbell_80kg_A_straight_rep0__success.mp4", 0.5, "03_ippo_mappo/mappo_pair_pushing.jpg")
    save_still(F / "ippo_l_shape_80kg__success.mp4", 0.5, "03_ippo_mappo/ippo_pair_pushing.jpg")
    grid_stills([(M / "mappo_cylinder_80kg_A_straight_rep0__success.mp4", 0.5, None, "MAPPO cylinder 80 kg"),
                 (M / "mappo_dumbbell_80kg_A_straight_rep0__success.mp4", 0.5, None, "MAPPO dumbbell 80 kg"),
                 (M / "mappo_plus_80kg_B_left_rep0__success.mp4", 0.5, None, "MAPPO plus 80 kg"),
                 (I / "ippo_cube_80kg_D_far_turn_rep0__success.mp4", 0.5, None, "IPPO cube 80 kg"),
                 (I / "ippo_sphere_80kg_C_backright_rep0__success.mp4", 0.5, None, "IPPO sphere 80 kg"),
                 (I / "ippo_l_shape_80kg_A_straight_rep0__success.mp4", 0.5, None, "IPPO L shape 80 kg")],
                "03_ippo_mappo/ippo_mappo_objects_grid.jpg", 3)
    save_strip(PV / "03_frozen_pair_untrained" / sorted(p.name for p in (PV / "03_frozen_pair_untrained").glob("*.mp4"))[0],
               Q, "03_ippo_mappo/frozen_pair_untrained_strip.jpg")

    # contact planner, two robots
    C, C8 = PV / "06_contact_planner", PE / "05_contact_planner" / "80kg"
    save_strip(C / "planner_long_40kg_far_turn__success.mp4", [0.02, 0.3, 0.6, 0.98],
               "04_contact_planner/planner_long_40kg_far_turn_strip.jpg")
    save_strip(C8 / "dumbbell_80kg_D_far_turn_r4__success.mp4", Q, "04_contact_planner/planner_dumbbell_80kg_far_turn_strip.jpg")
    save_strip(C8 / "t_shape_80kg_C_backright_r9__success.mp4", Q, "04_contact_planner/planner_t_shape_80kg_backright_strip.jpg")
    save_strip(C8 / "u_channel_80kg_B_left_r0__success.mp4", Q, "04_contact_planner/planner_u_channel_80kg_left_strip.jpg")
    save_still(C8 / "plus_80kg_D_far_turn_r4__success.mp4", 0.4, "04_contact_planner/planner_pair_contacts.jpg")
    grid_stills([(C8 / "cube_80kg_B_left_r3__success.mp4", 0.4, None, "cube 80 kg"),
                 (C8 / "cylinder_80kg_A_straight_r3__success.mp4", 0.4, None, "cylinder 80 kg"),
                 (C8 / "sphere_80kg_C_backright_r7__success.mp4", 0.4, None, "sphere 80 kg"),
                 (C8 / "l_shape_80kg_D_far_turn_r3__success.mp4", 0.4, None, "L shape 80 kg"),
                 (C8 / "plus_80kg_A_straight_r0__success.mp4", 0.4, None, "plus 80 kg"),
                 (C8 / "u_channel_80kg_C_backright_r6__success.mp4", 0.4, None, "U channel 80 kg")],
                "04_contact_planner/planner_objects_grid.jpg", 3)

    # teams of 2, 3, 4 (contact posts: cyan / yellow pair, magenta robot 3, orange robot 4)
    T = PE / "05_contact_planner" / "3_vs_4_robots"
    t23 = T / "2_vs_3" / "100kg" / "plus_100kg_B_left_r0__k2-success__k3b-success.mp4"
    t34 = T / "40kg" / "cylinder_40kg_A_straight_r2__k3-horizon__k4-success.mp4"
    _joined(t23, "t_add3")
    _joined(t34, "t_add4")
    H3 = PE / "10_planner_three_robots"
    h3 = H3 / "sphere_100kg_B_left_r0_helper__success.mp4"
    save_strip(h3, Q, "05_teams_2_3_4/three_robots_sphere_100kg_strip.jpg")
    save_strip(H3 / "u_channel_80kg_C_backright_r0_helper__success.mp4", Q,
               "05_teams_2_3_4/three_robots_u_channel_80kg_strip.jpg")
    save_strip(H3 / "arch_80kg_B_left_r0_helper__success.mp4", [0.02, 0.3, 0.6, 0.98],
               "05_teams_2_3_4/three_robots_arch_80kg_strip.jpg")
    save_still(H3 / "dumbbell_80kg_B_left_r0_helper__success.mp4", 0.6, "05_teams_2_3_4/three_robots_dumbbell_80kg.jpg")
    # branch films start at 16 s (4 s before the decision); every frame is inside its own panel's episode:
    # plus 100 kg: pair success at 45.9 s, robot 3 at 20 s -> success at 38.9 s;
    # cylinder 40 kg: trio times out at 80 s, robot 4 at 20 s -> success at 27.1 s (no falls)
    save_strip(t23, [1.5, 10, 20, 29], "05_teams_2_3_4/two_robots_plus_100kg_strip.jpg", which="left", t0=16)
    save_strip(t23, [1.5, 8, 15, 22.5], "05_teams_2_3_4/three_robots_branch_plus_100kg_strip.jpg", which="right", t0=16)
    save_strip(t34, [1.5, 5, 8, 11], "05_teams_2_3_4/three_robots_cylinder_40kg_strip.jpg", which="left", t0=16)
    save_strip(t34, [1.5, 5, 8, 11], "05_teams_2_3_4/four_robots_cylinder_40kg_strip.jpg", which="right", t0=16)
    grid_stills([(t23, 20, "left", "2 robots"), (h3, 0.6, None, "3 robots"), (t34, 9, "right", "4 robots")],
                "05_teams_2_3_4/team_sizes_2_3_4.jpg", 3)

    # online learning: penalty after repeated failed pushes
    P = PE / "06_contact_planner_online_learning" / "turning_test_mirror" / "penalty_acted" / "long_80kg_T60_m_r1"
    if P.exists():
        a = next(P.glob("A_original__*.mp4"))
        b = next(P.glob("B2_penalty__*.mp4"))
        save_strip(a, [0.02, 0.3, 0.6, 0.98], "06_online_learning/original_planner_long_80kg_turn60_strip.jpg")
        save_strip(b, [0.02, 0.3, 0.6, 0.98], "06_online_learning/penalty_planner_long_80kg_turn60_strip.jpg")
    BW = PE / "06_contact_planner_online_learning" / "benchmark" / "B2_won"
    for task, tag in (("l_shape_80kg_A_straight_r0", "l_shape_80kg"), ("u_channel_40kg_C_backright_r0", "u_channel_40kg")):
        if (BW / task).exists():
            save_strip(next((BW / task).glob("A_original__*.mp4")), Q, f"06_online_learning/original_planner_{tag}_strip.jpg")
            save_strip(next((BW / task).glob("B2_penalty__*.mp4")), Q, f"06_online_learning/penalty_planner_{tag}_strip.jpg")
    print("frames done")


# ---------------------------------------------------------------- object maps (the CNN's input)
def build_maps():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import torch

    from quadcoop.stage2 import profiles as pf
    from quadcoop.stage2.shapes import HELDOUT_NAMES, SHAPES2, kinds_tensor, shape_parts

    kinds = kinds_tensor("cpu")
    names = [s.name for s in SHAPES2]
    ones = torch.ones(1, 3)
    tops, fronts = [], []
    for i, nm in enumerate(names):
        parts, rest = shape_parts(nm, ones)
        k = kinds[i:i + 1]
        tops.append(pf.top_object_frame(parts, k, rest)[0, 0].numpy())
        fronts.append(pf.front_object_frame(parts, k, rest)[0, 0].numpy())
    d = OUT / "02_single_robot"
    d.mkdir(parents=True, exist_ok=True)
    vmin, vmax = pf.CLIP[0] / pf.SCALE, pf.CLIP[1] / pf.SCALE
    fig, ax = plt.subplots(2, 6, figsize=(12, 4.6))
    for a, nm, im in zip(ax.ravel(), names, tops, strict=True):
        h = a.imshow(im, cmap="RdBu", vmin=vmin, vmax=vmax, extent=(1.8, -1.8, -1.8, 1.8))
        a.contour(np.flipud(im), levels=[0.0], colors="k", linewidths=1.0, extent=(1.8, -1.8, -1.8, 1.8))
        a.set_title(nm + (" (held out)" if nm in HELDOUT_NAMES else ""), fontsize=9)
        a.set_xticks([])
        a.set_yticks([])
    fig.colorbar(h, ax=ax, shrink=0.8, label="signed distance / 0.5 m (negative inside)")
    fig.suptitle("Top-down object maps (32 x 32, 3.6 x 3.6 m, body-height slice 0.12-0.75 m): the CNN's input")
    fig.savefig(d / "object_maps_top.png", dpi=200, bbox_inches="tight")
    fig.savefig(d / "object_maps_top.pdf", bbox_inches="tight")
    plt.close(fig)
    fig, ax = plt.subplots(3, 4, figsize=(10, 4.4))
    for a, nm, im in zip(ax.ravel(), names, fronts, strict=True):
        a.imshow(im, cmap="RdBu", vmin=vmin, vmax=vmax, extent=(1.8, -1.8, 0.0, 1.2), aspect="auto")
        a.set_title(nm, fontsize=9)
        a.set_xticks([])
        a.set_yticks([])
    fig.suptitle("Front silhouettes (16 x 32: height 0-1.2 m by lateral -1.8..1.8 m)")
    fig.savefig(d / "object_maps_front.png", dpi=200, bbox_inches="tight")
    plt.close(fig)

    # the encoder (src/quadcoop/stage2/rl_cfg.py)
    fig, ax = plt.subplots(figsize=(11, 3.2))
    ax.axis("off")
    boxes = [(0.0, "top map\n1x32x32"), (0.14, "conv 5x5/2\n16 ch"), (0.28, "conv 3x3/2\n32 ch"),
             (0.42, "conv 3x3/2\n16 ch"), (0.56, "flatten\n256")]
    for x, t in boxes:
        ax.add_patch(plt.Rectangle((x, 0.55), 0.11, 0.3, fc="#dbe9f6", ec="k"))
        ax.text(x + 0.055, 0.7, t, ha="center", va="center", fontsize=9)
    for x, t in [(0.0, "front map\n1x16x32"), (0.14, "same three\nconv layers"), (0.56, "flatten\n128")]:
        ax.add_patch(plt.Rectangle((x, 0.1), 0.11, 0.3, fc="#dbe9f6", ec="k"))
        ax.text(x + 0.055, 0.25, t, ha="center", va="center", fontsize=9)
    for x in (0.11, 0.25, 0.39, 0.53):
        ax.annotate("", (x + 0.03, 0.7), (x, 0.7), arrowprops=dict(arrowstyle="->"))
    ax.annotate("", (0.56, 0.25), (0.25, 0.25), arrowprops=dict(arrowstyle="->"))
    ax.annotate("", (0.14, 0.25), (0.11, 0.25), arrowprops=dict(arrowstyle="->"))
    ax.add_patch(plt.Rectangle((0.56, 0.9), 0.11, 0.1, fc="#f2f2f2", ec="k"))
    ax.text(0.615, 0.95, "42 state inputs", ha="center", va="center", fontsize=8)
    ax.add_patch(plt.Rectangle((0.73, 0.35), 0.12, 0.35, fc="#fde5c8", ec="k"))
    ax.text(0.79, 0.525, "MLP\n256-128-64", ha="center", va="center", fontsize=9)
    ax.add_patch(plt.Rectangle((0.9, 0.4), 0.1, 0.25, fc="#e3f1dc", ec="k"))
    ax.text(0.95, 0.525, "velocity\ncommand to\nfrozen walker", ha="center", va="center", fontsize=8)
    for y in (0.7, 0.25, 0.95):
        ax.annotate("", (0.73, 0.525), (0.67, y), arrowprops=dict(arrowstyle="->"))
    ax.annotate("", (0.9, 0.525), (0.85, 0.525), arrowprops=dict(arrowstyle="->"))
    ax.set_xlim(-0.01, 1.01)
    ax.set_ylim(0.0, 1.05)
    fig.savefig(d / "cnn_push_policy_architecture.png", dpi=200, bbox_inches="tight")
    fig.savefig(d / "cnn_push_policy_architecture.pdf", bbox_inches="tight")
    plt.close(fig)

    # what the deployed pusher sees (Stage 2b): the same slice on a 4 x 4 m grid around the robot, x forward = up
    views = [("long", 1.2, 0.0, 0.0), ("long", 1.4, 0.3, 30.0), ("t_shape", 1.6, -0.2, -45.0), ("arch", 1.75, 0.0, 90.0),
             ("u_channel", 2.0, 0.0, 180.0), ("plus", 1.8, 0.4, 20.0)]
    fig, ax = plt.subplots(1, len(views), figsize=(2.1 * len(views), 2.6))
    ex = (ROBOT := pf.ROBOT_TOP)["y"][1], ROBOT["y"][0], ROBOT["x"][0], ROBOT["x"][1]
    for a, (nm, ox, oy, yaw) in zip(ax, views, strict=True):
        i = names.index(nm)
        parts, rest = shape_parts(nm, ones)
        im = pf.top_robot_frame(parts, kinds[i:i + 1], rest, torch.tensor([[ox, oy]]),
                                torch.tensor([np.deg2rad(yaw)], dtype=torch.float32))[0, 0].numpy()
        a.imshow(im, cmap="RdBu", vmin=vmin, vmax=vmax, extent=ex)
        a.contour(np.flipud(im), levels=[0.0], colors="k", linewidths=1.0, extent=ex)
        a.add_patch(plt.Rectangle((-0.3, -0.55), 0.6, 1.1, fc="none", ec="#2ca02c", lw=1.5))  # the robot itself
        a.set_title(f"{nm}, {yaw:+.0f} deg", fontsize=8)
        a.set_xticks([])
        a.set_yticks([])
    fig.suptitle("Robot-frame object map (32 x 32 over 4 x 4 m, forward = up; green = the robot)", fontsize=10)
    fig.savefig(d / "object_maps_robot_frame.png", dpi=200, bbox_inches="tight")
    fig.savefig(d / "object_maps_robot_frame.pdf", bbox_inches="tight")
    plt.close(fig)
    print("maps done")


# ---------------------------------------------------------------- graphs
def _style(plt):
    plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
                         "axes.grid": True, "grid.alpha": 0.3, "savefig.dpi": 200})


COL = {"Single robot": "#7f7f7f", "IPPO": "#1f77b4", "MAPPO": "#ff7f0e", "Contact planner": "#2ca02c"}


def _md_table(text: str, header_start: str):
    lines = text.splitlines()
    for i, ln in enumerate(lines):
        if ln.startswith(header_start):
            head = [c.strip() for c in ln.strip("|").split("|")]
            rows = []
            for r in lines[i + 2:]:
                if not r.startswith("|"):
                    break
                rows.append([c.strip() for c in r.strip("|").split("|")])
            return head, rows
    raise KeyError(header_start)


def _pct(s: str) -> float:
    return float(s.split("%")[0])


def _save(fig, name):
    p = OUT / "07_graphs" / name
    p.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(p.with_suffix(".png"), bbox_inches="tight")
    fig.savefig(p.with_suffix(".pdf"), bbox_inches="tight")


def build_graphs():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    _style(plt)
    txt = (ROOT / "evals_present/00_overview/comparison_all_systems.md").read_text()

    # 1. success vs mass, four systems
    head, rows = _md_table(txt, "| mass | Single robot success")
    systems = ["Single robot", "IPPO", "MAPPO", "Contact planner"]
    masses = [int(r[0].split()[0]) for r in rows]
    fig, ax = plt.subplots(figsize=(5.2, 3.4))
    for s in systems:
        y = [_pct(r[head.index(f"{s} success")]) for r in rows]
        ax.plot(masses, y, "o-", label=s, color=COL[s])
    ax.set_xlabel("object mass (kg)")
    ax.set_ylabel("success (%)")
    ax.set_xticks(masses)
    ax.set_ylim(0, 100)
    ax.legend(frameon=False)
    ax.set_title("Benchmark: 12 objects x 4 starts x 10 trials per mass")
    _save(fig, "success_vs_mass_all_systems")
    plt.close(fig)

    # 2. falls vs mass
    fig, ax = plt.subplots(figsize=(5.2, 3.4))
    for s in systems:
        y = [_pct(r[head.index(f"{s} fell")]) for r in rows]
        ax.plot(masses, y, "o-", label=s, color=COL[s])
    ax.set_xlabel("object mass (kg)")
    ax.set_ylabel("episodes with a fall (%)")
    ax.set_xticks(masses)
    ax.legend(frameon=False)
    _save(fig, "falls_vs_mass_all_systems")
    plt.close(fig)

    # 3. success by object, averaged over masses
    per = {}
    for m in masses:
        h2, r2 = _md_table(txt.split(f"## {m} kg: by object")[1], "| object |")
        for r in r2:
            for s in systems:
                per.setdefault(r[0], {}).setdefault(s, []).append(_pct(r[h2.index(s)]))
    objs = list(per)
    fig, ax = plt.subplots(figsize=(10, 3.4))
    w = 0.2
    x = np.arange(len(objs))
    for i, s in enumerate(systems):
        ax.bar(x + (i - 1.5) * w, [np.mean(per[o][s]) for o in objs], w, label=s, color=COL[s])
    ax.set_xticks(x)
    ax.set_xticklabels(objs, rotation=30, ha="right")
    ax.set_ylabel("success (%), mean of 20-80 kg")
    ax.set_ylim(0, 100)
    ax.legend(frameon=False, ncol=4, loc="upper center", bbox_to_anchor=(0.5, 1.15))
    _save(fig, "success_by_object_all_systems")
    plt.close(fig)

    # 4. CNN object map vs no map (evals_present README table)
    rd = (ROOT / "evals_present/README.md").read_text()
    h4, r4 = _md_table(rd.split("## 03_cnn_object_map")[1], "| | map + CNN | no map |")
    lab = [r[0] for r in r4]
    m_all = [float(r[1].split()[0]) for r in r4]
    n_all = [float(r[2].split()[0]) for r in r4]
    m_un = [float(re.search(r"\(.*?([\d.]+)\)", r[1]).group(1)) for r in r4]
    n_un = [float(re.search(r"\(([\d.]+)\)", r[2]).group(1)) for r in r4]
    fig, axs = plt.subplots(1, 2, figsize=(10, 3.4), sharey=True)
    for a, (mm, nn, t) in zip(axs, [(m_all, n_all, "all suites (h80)"), (m_un, n_un, "unseen shapes, 40 kg")],
                              strict=True):
        x = np.arange(len(lab))
        a.bar(x - 0.18, mm, 0.36, label="object map + CNN", color="#1f77b4")
        a.bar(x + 0.18, nn, 0.36, label="no map", color="#bbbbbb")
        a.set_xticks(x)
        a.set_xticklabels([s.replace(", ", ",\n") for s in lab], fontsize=8)
        a.set_title(t)
        a.set_ylim(0, 1)
    axs[0].set_ylabel("success rate")
    axs[0].legend(frameon=False)
    _save(fig, "cnn_object_map_vs_no_map")
    plt.close(fig)

    # 5. team size: 2 / 3 / 4 robots in the same branched states (chain4 trees, original footprint)
    team_graph(plt)
    # 6. penalty after repeated failed pushes
    penalty_graph(plt)
    # 7. 80 s vs 140 s; every turning-test arm; robot 4 placed vs walking in
    horizon_graph(plt)
    turning_arms_graph(plt)
    place_graph(plt)
    print("graphs done")


def _boot(d, n=4000):
    """Mean and 95% bootstrap interval (over tasks) of a paired difference, in points."""
    d = np.asarray(d, float)
    b = np.random.default_rng(0).choice(d, (n, len(d))).mean(1)
    return 100 * d.mean(), 100 * np.percentile(b, 2.5), 100 * np.percentile(b, 97.5)


def _pair_runs(*names):
    """Task -> success averaged over runs (logs/evals/<name>/pair/episodes.csv)."""
    acc = {}
    for nm in names:
        for r in _rows(ROOT / "logs/evals" / nm / "pair/episodes.csv"):
            acc.setdefault((r["object"], int(float(r["mass"])), r["scenario"], r["rep"]), []).append(float(r["success"]))
    return {k: np.mean(v) for k, v in acc.items()}


def horizon_graph(plt):
    """The 480-task planner benchmark at 80 s and 140 s, original planner (A) and penalty (B2), two runs each."""
    runs = {(a, h): [f"{p}-{a}-r{r}-expert" for r in (1, 2)] for a in ("A", "B2") for h, p in ((80, "olp"), (140, "olp140"))}
    if not all((ROOT / "logs/evals" / n / "pair/episodes.csv").exists() for v in runs.values() for n in v):
        return
    S = {k: _pair_runs(*v) for k, v in runs.items()}
    masses = sorted({k[1] for k in S[("A", 80)]})
    fig, ax = plt.subplots(figsize=(5.4, 3.4))
    for (a, h), c, ls in ((("A", 80), "#999999", "--"), (("B2", 80), "#2ca02c", "--"),
                          (("A", 140), "#555555", "-"), (("B2", 140), "#1a7f1a", "-")):
        y = [100 * np.mean([v for k, v in S[(a, h)].items() if k[1] == m]) for m in masses]
        lab = ("original planner" if a == "A" else "penalty after repeated failures") + f", {h} s"
        ax.plot(masses, y, "o" + ls, color=c, label=lab)
    ax.set_xlabel("object mass (kg)")
    ax.set_ylabel("success (%)")
    ax.set_xticks(masses)
    ax.set_ylim(0, 100)
    ax.legend(frameon=False, fontsize=8, loc="lower left")
    d80 = _boot([S[("B2", 80)][k] - S[("A", 80)][k] for k in S[("A", 80)]])
    d140 = _boot([S[("B2", 140)][k] - S[("A", 140)][k] for k in S[("A", 140)]])
    ax.set_title(f"Planner time limit (480 tasks, 2 runs). Penalty - original: 80 s {d80[0]:+.1f} "
                 f"[{d80[1]:+.1f}, {d80[2]:+.1f}], 140 s {d140[0]:+.1f} [{d140[1]:+.1f}, {d140[2]:+.1f}]", fontsize=8)
    _save(fig, "planner_time_limit_80_vs_140")
    plt.close(fig)


def turning_arms_graph(plt):
    """Held-out turning test (seed 7300): every planner arm minus the original planner, paired by task, with 95%
    bootstrap intervals; turns in both directions."""
    arms = [("B", "exact-pair penalty"), ("C", "similar-push penalty"), ("D", "one forced switch"),
            ("B2", "penalty after 2 failures")]
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    x = np.arange(len(arms))
    done = False
    for j, (t, lab, c) in enumerate((("turn", "turns", "#1f77b4"), ("turn_mirror", "mirrored turns", "#ff7f0e"))):
        names = [f"fm-test-{a}-{t}-expert" for a, _ in [("A", "")] + arms]
        if not all((ROOT / "logs/evals" / n / "pair/episodes.csv").exists() for n in names):
            continue
        A = _pair_runs(names[0])
        res = []
        for a, _ in arms:
            B = _pair_runs(f"fm-test-{a}-{t}-expert")
            res.append(_boot([B[k] - A[k] for k in A if k in B]))
        m = np.array([r[0] for r in res])
        err = np.array([[r[0] - r[1] for r in res], [r[2] - r[0] for r in res]])
        ax.bar(x + (j - 0.5) * 0.36, m, 0.36, yerr=err, capsize=3, color=c,
               label=f"{lab} (original planner {100 * np.mean(list(A.values())):.0f}%)")
        done = True
    if not done:
        plt.close(fig)
        return
    ax.axhline(0, color="black", lw=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels([lab for _, lab in arms], fontsize=8)
    ax.set_ylabel("success gain over original (pp)")
    ax.legend(frameon=False, fontsize=8)
    ax.set_title("Turning test, fresh placements (long and arch, 60-80 kg, 160 tasks per bar)", fontsize=9)
    _save(fig, "penalty_turning_test_all_arms")
    plt.close(fig)


def place_graph(plt):
    """The ten 3 -> 4 place trees (k4p-*): 2, 3, 4 robots and robot 4 placed at its contact, from the same branched
    states, per mass and footprint."""
    for tag, sc, title in (("original", "s10", "original footprint"), ("enlarged_1p5", "s15", "footprint x 1.5")):
        acc = {}
        for s in (1001, 1002, 1003, 8401, 8402):
            p = ROOT / "logs/evals" / f"k4p-{sc}-s{s}" / "episodes.csv"
            if p.exists():
                for r in _rows(p):
                    acc.setdefault((r["arm"], int(float(r["mass"]))), []).append(float(r["success"]))
        if not acc:
            continue
        masses = sorted({m for _, m in acc})
        fig, ax = plt.subplots(figsize=(5.4, 3.4))
        for a, lab, c, ls in (("k2", "2 robots", "#7f7f7f", "-"), ("k3", "3 robots", "#1f77b4", "-"),
                              ("k4", "4 robots, robot 4 walks in", "#d62728", "-"),
                              ("k4p", "4 robots, robot 4 placed at its contact", "#d62728", "--")):
            ax.plot(masses, [100 * np.mean(acc[(a, m)]) for m in masses], "o" + ls, color=c, label=lab,
                    mfc="white" if a == "k4p" else c)
        ax.set_xlabel("object mass (kg)")
        ax.set_ylabel("success (%)")
        ax.set_xticks(masses)
        ax.set_ylim(0, 100)
        ax.legend(frameon=False, fontsize=8)
        ax.set_title(f"Robot 4 placed vs walking in ({title}, 5 seeds, n = {len(acc[('k3', masses[0])])} per point)",
                     fontsize=9)
        _save(fig, f"team_size_placed_vs_walkin_{tag}")
        plt.close(fig)


def _rows(path: Path):
    with open(path) as f:
        return list(csv.DictReader(f))


def team_graph(plt):
    seeds = ["1001a", "1001b", "1002a", "1002b", "1003a", "1003b", "8401a", "8401b", "8402a", "8402b"]
    for tag, prefix, title in (("original", "k4c", "original footprint"), ("enlarged_1p5", "k4s15", "footprint x 1.5")):
        acc = {}
        for s in seeds:
            p = ROOT / "logs/evals" / f"{prefix}-s{s}" / "episodes.csv"
            if not p.exists():
                continue
            for r in _rows(p):
                acc.setdefault((r["arm"], float(r["mass"])), []).append(float(r["success"]))
        if not acc:
            continue
        masses = sorted({m for _, m in acc})
        arms = [("k2", "2 robots", "#7f7f7f"), ("k3", "3 robots (robot 3 called at 8 s)", "#1f77b4"),
                ("k4", "4 robots (robot 4 called at 20 s)", "#d62728")]
        fig, ax = plt.subplots(figsize=(5.4, 3.4))
        for a, lab, c in arms:
            y = [100 * np.mean(acc[(a, m)]) if (a, m) in acc else np.nan for m in masses]
            n = [len(acc.get((a, m), [])) for m in masses]
            ax.plot(masses, y, "o-", label=lab, color=c)
        ax.set_xlabel("object mass (kg)")
        ax.set_ylabel("success (%)")
        ax.set_xticks(masses)
        ax.set_ylim(0, 100)
        ax.legend(frameon=False, fontsize=8)
        ax.set_title(f"Team size from the same branched states ({title}, n = {n[0]} per point)", fontsize=9)
        _save(fig, f"team_size_2_3_4_{tag}")
        plt.close(fig)


def penalty_graph(plt):
    def load(d):
        p = ROOT / "logs/evals" / d / "pair/episodes.csv"
        return {(r["object"], r["mass"], r["scenario"], r["rep"]): float(r["success"]) for r in _rows(p)} if p.exists() else None
    A1, A2, B1, B2 = (load(f"olp-{a}-r{r}-expert") for a in ("A", "B2") for r in (1, 2))
    if A1 and A2 and B1 and B2:
        objs = sorted({k[0] for k in A1})
        a_ = [100 * np.mean([(A1[k] + A2[k]) / 2 for k in A1 if k[0] == o]) for o in objs]
        b_ = [100 * np.mean([(B1[k] + B2[k]) / 2 for k in B1 if k[0] == o]) for o in objs]
        fig, ax = plt.subplots(figsize=(9, 3.2))
        x = np.arange(len(objs))
        ax.bar(x - 0.18, a_, 0.36, label="original planner", color="#bbbbbb")
        ax.bar(x + 0.18, b_, 0.36, label="penalty after repeated failed pushes", color="#2ca02c")
        ax.set_xticks(x)
        ax.set_xticklabels(objs, rotation=30, ha="right")
        ax.set_ylabel("success (%)")
        ax.set_ylim(0, 100)
        ax.legend(frameon=False, ncol=2, loc="upper center", bbox_to_anchor=(0.5, 1.02))
        ax.set_title("Ordinary deliveries (480 tasks, 2 runs each): overall 62.3% vs 62.4%", fontsize=9, pad=22)
        _save(fig, "penalty_benchmark_by_object")
        plt.close(fig)
    TA, TB = load("fm-test-A-turn_mirror-expert"), load("fm-test-B2-turn_mirror-expert")
    if TA and TB:
        fig, axs = plt.subplots(1, 2, figsize=(9, 3.2), sharey=True)
        for a, o in zip(axs, ("arch", "long"), strict=True):
            sc = sorted({k[2] for k in TA if k[0] == o}, key=lambda s: int(re.search(r"\d+", s).group()))
            ya = [100 * np.mean([v for k, v in TA.items() if k[0] == o and k[2] == s]) for s in sc]
            yb = [100 * np.mean([v for k, v in TB.items() if k[0] == o and k[2] == s]) for s in sc]
            x = np.arange(len(sc))
            a.bar(x - 0.18, ya, 0.36, label="original planner", color="#bbbbbb")
            a.bar(x + 0.18, yb, 0.36, label="penalty", color="#2ca02c")
            a.set_xticks(x)
            a.set_xticklabels([re.search(r"\d+", s).group() + " deg" for s in sc])
            a.set_title(f"{o}, turn in place (fresh placements)", fontsize=9)
            a.set_ylim(0, 100)
        axs[0].set_ylabel("success (%)")
        axs[0].legend(frameon=False)
        _save(fig, "penalty_turning_test")
        plt.close(fig)


# ---------------------------------------------------------------- copies of existing figures
def build_copy():
    d = OUT / "04_contact_planner"
    d.mkdir(parents=True, exist_ok=True)
    shutil.copy(ROOT / "evals/contacts/all.png", d / "candidate_contacts_all_objects.png")
    for nm in ("long", "arch", "cylinder"):
        shutil.copy(ROOT / f"evals/contacts/{nm}.png", d / f"candidate_contacts_{nm}.png")
    g = OUT / "07_graphs"
    g.mkdir(parents=True, exist_ok=True)
    rm = ROOT / "evals_present/07_regret_minimization/contact_game"
    for nm in ("learning_curves.png", "payoff_examples.png"):
        if (rm / nm).exists():
            shutil.copy(rm / nm, g / f"regret_contact_game_{nm}")
    print("copies done")


# ---------------------------------------------------------------- object renders
def build_objects():
    """Each of the twelve objects at nominal size, rendered in MuJoCo from a raised three-quarter view (camera 45°
    off the object's x and y axes, 30° above the floor), on 0.5 m floor squares for scale. Software EGL (Mesa
    llvmpipe), so it runs without a GPU."""
    import os
    os.environ.setdefault("MUJOCO_GL", "egl")
    os.environ.setdefault("EGL_PLATFORM", "surfaceless")
    mesa = Path("/usr/share/glvnd/egl_vendor.d/50_mesa.json")
    if mesa.exists():
        os.environ.setdefault("__EGL_VENDOR_LIBRARY_FILENAMES", str(mesa))
    import mujoco

    from quadcoop.stage1b.shapes import _Q_AXIS_Y
    from quadcoop.stage2.shapes import SHAPES2

    W = H = 900
    kinds = {0: "plane", 2: "sphere", 3: "capsule", 5: "cylinder", 6: "box"}  # mjtGeom ids used by Part.kind
    pretty = {"t_shape": "T shape", "l_shape": "L shape", "u_channel": "U channel", "asym": "split-friction box"}
    out = OUT / "object"
    out.mkdir(parents=True, exist_ok=True)
    tiles = []
    for s in SHAPES2:
        geoms, reach, top = [], 0.0, 0.0
        for i, p in enumerate(s.parts):
            size = list(p.size) + [0.0] * (3 - len(p.size))
            if int(p.kind) == 6 and i:
                size[2] -= 0.001 * i   # overlapping boxes share a top face: drop later parts 1 mm (no z-fighting)
            rgb = s.rgba[:3]
            if p.friction is not None and p.friction > 0.5:   # split-friction box: the high-friction half darker
                rgb = tuple(0.55 * c for c in rgb)
            q = f' quat="{" ".join(map(str, _Q_AXIS_Y))}"' if p.axis_y else ""
            geoms.append(f'<geom type="{kinds[int(p.kind)]}" size="{" ".join(map(str, size))}" '
                         f'pos="{" ".join(map(str, p.pos))}"{q} rgba="{" ".join(map(str, rgb))} 1"/>')
            ext = max(size[:2]) if int(p.kind) == 6 else max(size[0], size[1] if p.axis_y else size[0])
            reach = max(reach, float(np.hypot(p.pos[0], p.pos[1])) + ext)
            hz = size[2] if int(p.kind) == 6 else size[0]
            top = max(top, s.rest_height + p.pos[2] + hz)
        xml = f"""<mujoco><visual><global offwidth="{W}" offheight="{H}"/><quality shadowsize="4096" offsamples="8"/>
<headlight ambient=".35 .35 .35" diffuse=".35 .35 .35" specular="0 0 0"/></visual>
<asset><texture type="skybox" builtin="flat" rgb1="1 1 1" rgb2="1 1 1" width="32" height="32"/>
<texture name="g" type="2d" builtin="checker" rgb1=".93 .93 .93" rgb2=".82 .82 .82" width="64" height="64"/>
<material name="g" texture="g" texuniform="true" texrepeat="1 1"/></asset>
<worldbody><light pos="2.5 -1.5 5" dir="-.45 .3 -1" directional="true" castshadow="true" diffuse=".6 .6 .6"/>
<geom type="plane" size="6 6 .1" material="g"/>
<body pos="0 0 {s.rest_height}">{"".join(geoms)}</body></worldbody></mujoco>"""
        m = mujoco.MjModel.from_xml_string(xml)
        d = mujoco.MjData(m)
        mujoco.mj_forward(m, d)
        cam = mujoco.MjvCamera()
        cam.lookat[:] = (0.0, 0.0, 0.45 * top)
        cam.azimuth, cam.elevation = 225.0, -30.0   # looking from (+x, +y) toward the object, down 30°
        cam.distance = 1.0 + 2.6 * max(reach, top, 0.6)
        r = mujoco.Renderer(m, H, W)
        r.update_scene(d, camera=cam)
        img = Image.fromarray(r.render())
        r.close()
        img.save(out / f"{s.name}.png")
        name = pretty.get(s.name, s.name.replace("_", " "))
        tiles.append(label(img.copy(), name))
        print("object", s.name)
    cols, gap, tw = 4, 8, 600
    tiles = [t.resize((tw, tw), Image.LANCZOS) for t in tiles]
    rows = (len(tiles) + cols - 1) // cols
    g = Image.new("RGB", (cols * tw + (cols - 1) * gap, rows * tw + (rows - 1) * gap), (255, 255, 255))
    for i, t in enumerate(tiles):
        g.paste(t, ((i % cols) * (tw + gap), (i // cols) * (tw + gap)))
    g.save(out / "objects_grid.png")
    g.save(out / "objects_grid.jpg", quality=93)


def _egl_software():
    import os
    os.environ.setdefault("MUJOCO_GL", "egl")
    os.environ.setdefault("EGL_PLATFORM", "surfaceless")
    mesa = Path("/usr/share/glvnd/egl_vendor.d/50_mesa.json")
    if mesa.exists():
        os.environ.setdefault("__EGL_VENDOR_LIBRARY_FILENAMES", str(mesa))


# the single-robot benchmark (pres-solo-*: scripts/eval_coop2.py --solo anymal1, standard formation): the object at the
# origin, heading 0; the robot behind it at bearing 180 - 35 deg + U(-10, 10) deg, its base (object reach radius
# + ANYmal half length 0.55 m + a U(0.3, 0.6) m gap) from the object's centre, facing the centre
START_SCENARIOS = (  # name, goal distance (m), goal direction (deg, + = left), turn (deg), caption
    ("A_straight", 3.0, 0.0, 0.0, "A: goal 3 m ahead, no turn"),
    ("B_left", 3.0, 60.0, 30.0, "B: goal 3 m at 60\u00b0 left, turn +30\u00b0"),
    ("C_backright", 3.0, -135.0, -60.0, "C: goal 3 m at 135\u00b0 right, turn \u221260\u00b0"),
    ("D_far_turn", 5.0, 0.0, 90.0, "D: goal 5 m ahead, turn 90\u00b0"),
)


def build_starts(obj="t_shape"):
    """The single robot's start relative to the object in each of the four benchmark scenarios: ANYmal (standing
    pose) at its nominal start, the band of possible starts (bearing +-10 deg, gap 0.3-0.6 m) in translucent blue,
    the goal pose as a translucent green copy of the object, and a dashed line from the object to the goal. Also
    scenario A for every object."""
    import math
    _egl_software()
    import mujoco

    from quadcoop.stage1b.shapes import _Q_AXIS_Y
    from quadcoop.stage2.shapes import SHAPES2

    kinds = {2: "sphere", 5: "cylinder", 6: "box"}
    HALF, B0, JIT, GAP = 0.55, 145.0, 10.0, (0.3, 0.6)

    def obj_geoms(shape, x, y, yaw, rgba, tag):
        out = []
        for i, p in enumerate(shape.parts):
            size = list(p.size) + [0.0] * (3 - len(p.size))
            if int(p.kind) == 6 and i:
                size[2] -= 0.001 * i
            px, py = p.pos[0], p.pos[1]
            cx, cy = x + px * math.cos(yaw) - py * math.sin(yaw), y + px * math.sin(yaw) + py * math.cos(yaw)
            q = (math.cos(yaw / 2), 0.0, 0.0, math.sin(yaw / 2))
            if p.axis_y:  # q_yaw * q_axis_y
                a = _Q_AXIS_Y
                q = (q[0] * a[0] - q[3] * a[3], q[0] * a[1] - q[3] * a[2], q[0] * a[2] + q[3] * a[1], q[0] * a[3] + q[3] * a[0])
            out.append(f'<geom name="{tag}{i}" type="{kinds[int(p.kind)]}" size="{" ".join(map(str, size))}" '
                       f'pos="{cx} {cy} {shape.rest_height + p.pos[2]}" quat="{" ".join(map(str, q))}" '
                       f'rgba="{" ".join(map(str, rgba))}" contype="0" conaffinity="0"/>')
        return "".join(out)

    W, H = 1200, 900
    out = OUT / "02_single_robot" / "start_positions"
    out.mkdir(parents=True, exist_ok=True)

    def render(obj_name, scen):
        name, gd, gdir, turn, _ = scen
        shape = next(s for s in SHAPES2 if s.name == obj_name)
        rad = max(float(np.hypot(abs(p.pos[0]) + p.size[0], abs(p.pos[1]) + (p.size[1] if len(p.size) > 1 and
                  (int(p.kind) == 6 or p.axis_y) else p.size[0]))) for p in shape.parts)
        cap = math.degrees(math.pi / shape.symmetry * 0.9) if shape.symmetry else 0.0
        t = math.copysign(min(abs(turn), cap), turn) if shape.symmetry else 0.0
        gx, gy, gyaw = gd * math.cos(math.radians(gdir)), gd * math.sin(math.radians(gdir)), math.radians(t)
        # start band: tiles over bearing x gap
        band = []
        for k in range(16):
            b = math.radians(B0 - JIT + (2 * JIT) * (k + 0.5) / 16)
            r0, r1 = rad + HALF + GAP[0], rad + HALF + GAP[1]
            w = (r0 + r1) / 2 * math.radians(2 * JIT) / 16 / 2 + 0.003
            band.append(f'<geom type="box" size="{(r1 - r0) / 2} {w} 0.002" pos="{(r0 + r1) / 2 * math.cos(b)} '
                        f'{(r0 + r1) / 2 * math.sin(b)} 0.002" euler="0 0 {b}" rgba=".15 .45 .95 .35" '
                        f'contype="0" conaffinity="0"/>')
        dash = []
        n = int(gd / 0.25)
        for k in range(1, n):
            f = k / n
            if k % 2:
                dash.append(f'<geom type="box" size="0.08 0.02 0.002" pos="{f * gx} {f * gy} 0.003" '
                            f'euler="0 0 {math.atan2(gy, gx)}" rgba=".2 .2 .2 1" contype="0" conaffinity="0"/>')
        scene = mujoco.MjSpec.from_string(f"""<mujoco><compiler angle="radian"/>
<visual><global offwidth="{W}" offheight="{H}"/><quality shadowsize="4096" offsamples="8"/>
<headlight ambient=".35 .35 .35" diffuse=".35 .35 .35" specular="0 0 0"/><map shadowclip="12" shadowscale=".5" znear=".05"/></visual>
<statistic center="{gx / 2} {gy / 2} 0" extent="5"/>
<asset><texture type="skybox" builtin="flat" rgb1="1 1 1" rgb2="1 1 1" width="32" height="32"/>
<texture name="g" type="2d" builtin="checker" rgb1=".93 .93 .93" rgb2=".82 .82 .82" width="64" height="64"/>
<material name="g" texture="g" texuniform="true" texrepeat="1 1" specular="0" shininess="0"/></asset>
<worldbody><light pos="{gx / 2} {gy / 2} 6" dir="-.3 .45 -1" directional="true" castshadow="true" diffuse=".6 .6 .6"/>
<geom type="plane" size="7 7 .1" pos="{gx / 2} {gy / 2} 0" material="g"/>
{obj_geoms(shape, 0, 0, 0, (*shape.rgba[:3], 1), "obj")}{obj_geoms(shape, gx, gy, gyaw, (.10, .85, .25, .35), "goal")}
{"".join(band)}{"".join(dash)}<frame name="rf"/></worldbody></mujoco>""")
        robot = mujoco.MjSpec.from_file(str(ROOT / "src/quadcoop/assets/anymal_c/anymal_c.xml"))
        for li in list(robot.lights):  # the model's own tracking spotlight would wash out the floor around the robot
            robot.delete(li)
        scene.attach(robot, prefix="r_", frame=scene.frame("rf"))
        m = scene.compile()
        d = mujoco.MjData(m)
        init = {"HAA": 0.0, "LF_HFE": 0.4, "RF_HFE": 0.4, "LH_HFE": -0.4, "RH_HFE": -0.4,
                "LF_KFE": -0.8, "RF_KFE": -0.8, "LH_KFE": 0.8, "RH_KFE": 0.8}
        for j in range(m.njnt):
            jn = mujoco.mj_id2name(m, mujoco.mjtObj.mjOBJ_JOINT, j) or ""
            for key, v in init.items():
                if jn.endswith(key):
                    d.qpos[m.jnt_qposadr[j]] = v
        b = math.radians(B0)
        dist = rad + HALF + sum(GAP) / 2
        yaw = b + math.pi
        fj = next(j for j in range(m.njnt) if m.jnt_type[j] == mujoco.mjtJoint.mjJNT_FREE)
        a0 = m.jnt_qposadr[fj]
        d.qpos[a0:a0 + 7] = [dist * math.cos(b), dist * math.sin(b), 0.6, math.cos(yaw / 2), 0, 0, math.sin(yaw / 2)]
        mujoco.mj_forward(m, d)
        feet = [i for i in range(m.ngeom) if (mujoco.mj_id2name(m, mujoco.mjtObj.mjOBJ_GEOM, i) or "").endswith("_foot")]
        low = min(d.geom_xpos[i][2] - m.geom_size[i][0] for i in feet) if feet else 0.0
        d.qpos[a0 + 2] -= low
        mujoco.mj_forward(m, d)
        pts = np.array([[0, 0], [gx, gy], [dist * math.cos(b), dist * math.sin(b)]])
        lo, hi = pts.min(0) - 0.8, pts.max(0) + 0.8
        cam = mujoco.MjvCamera()
        cam.lookat[:] = (*((lo + hi) / 2), 0.2)
        cam.azimuth, cam.elevation = 15.0, -50.0   # from behind the robot's left shoulder, looking down 50 deg
        cam.distance = 1.0 + 1.05 * float(np.hypot(*(hi - lo)))
        opt = mujoco.MjvOption()
        opt.geomgroup[:] = [1, 1, 1, 0, 0, 0]
        r = mujoco.Renderer(m, H, W)
        r.update_scene(d, camera=cam, scene_option=opt)
        img = Image.fromarray(r.render())
        r.close()
        print("start", obj_name, name)
        return img

    def grid(tiles, cols, stem, tw):
        th = round(tw * H / W)
        tiles = [t.resize((tw, th), Image.LANCZOS) for t in tiles]
        rows = (len(tiles) + cols - 1) // cols
        g = Image.new("RGB", (cols * tw + (cols - 1) * 8, rows * th + (rows - 1) * 8), (255, 255, 255))
        for i, t in enumerate(tiles):
            g.paste(t, ((i % cols) * (tw + 8), (i // cols) * (th + 8)))
        g.save(out / f"{stem}.png")
        g.save(out / f"{stem}.jpg", quality=93)

    # 1. the four scenarios, one object (the T shape: no symmetry, so every turn is visible)
    tiles = []
    for sc in START_SCENARIOS:
        img = render(obj, sc)
        img.save(out / f"single_robot_start_{sc[0]}.png")
        tiles.append(label(img.copy(), sc[4]))
    grid(tiles, 2, "single_robot_start_positions", 900)
    # 2. scenario A for all twelve objects: the start distance grows with the object's reach radius
    pretty = {"t_shape": "T shape", "l_shape": "L shape", "u_channel": "U channel", "asym": "split-friction box"}
    tiles = []
    for s_ in SHAPES2:
        img = render(s_.name, START_SCENARIOS[0])
        img.save(out / f"single_robot_start_A_{s_.name}.png")
        tiles.append(label(img.copy(), pretty.get(s_.name, s_.name)))
    grid(tiles, 4, "single_robot_start_A_all_objects", 600)


def build_intro():
    """Intro figure from real evaluation films: the cube at 80 kg, goal 3 m straight ahead, pushed by one, two, three
    and four ANYmals, one frame each, mid-push.
      1 robot   the single-robot push policy (02_anymal_single_robot_push, success)
      2 robots  the contact planner's pair (05_contact_planner, success)
      3 / 4     one branched contact-planner run at the same instant, 26 s (10 s into the film): left panel the trio
                continues (success at 49.6 s), right panel robot 4 joined at 20 s (R2, R3, R4 pushing, R1 at its
                contact; this branch timed out 0.08 m short)
    Each frame is cropped (boxes set by eye) to the team, the cube and the goal, at a similar robot size."""
    P = PE
    B = P / "05_contact_planner" / "3_vs_4_robots" / "80kg" / "cube_80kg_A_straight_r2__k3-success__k4-horizon.mp4"
    _joined(B, "t_add4")
    src = [(P / "02_anymal_single_robot_push" / "80kg" / "cube_80kg_A_straight_rep4__success.mp4", 0.5, None, "1 robot"),
           (P / "05_contact_planner" / "80kg" / "cube_80kg_A_straight_r5__success.mp4", 0.6, None, "2 robots"),
           (B, 10.0, "left", "3 robots"), (B, 10.0, "right", "4 robots")]
    frames = [frames_at(v, [t], w)[0][0] for v, t, w, _ in src]
    # crop boxes (fractions of the frame, 4:3 in pixels), set by eye: team, object and goal square, with a robot
    # about a fifth of the panel wide in every panel
    crops = [(0.31, 0.17, 0.73, 0.78), (0.24, 0.0, 0.76, 0.79), (0.25, 0.0, 0.86, 0.76), (0.25, 0.0, 0.86, 0.76)]
    out = OUT / "intro"
    out.mkdir(parents=True, exist_ok=True)
    tiles = []
    for (v, t, w, lab), f, (fx0, fy0, fx1, fy1) in zip(src, frames, crops):
        x0, x1 = fx0 * f.width, fx1 * f.width
        y0 = fy0 * f.height
        y1 = y0 + (x1 - x0) * 3 / 4
        im = f.crop((int(x0), int(y0), int(x1), int(min(y1, f.height)))).resize((900, 675), Image.LANCZOS)
        im.save(out / f"{lab.replace(' ', '_')}_cube_80kg.jpg", quality=95)
        tiles.append(im)
    try:
        import matplotlib
        font = ImageFont.truetype(str(Path(matplotlib.get_data_path()) / "fonts/ttf/DejaVuSans-Bold.ttf"), 48)
    except (OSError, ImportError):
        font = ImageFont.load_default()

    def titled(img, txt):
        band = 76
        t_ = Image.new("RGB", (img.width, img.height + band), (255, 255, 255))
        t_.paste(img, (0, band))
        dr = ImageDraw.Draw(t_)
        x0, y0, x1, y1 = dr.textbbox((0, 0), txt, font=font)
        dr.text(((img.width - (x1 - x0)) // 2 - x0, (band - (y1 - y0)) // 2 - y0), txt, fill=(20, 20, 20), font=font)
        return t_

    tiles = [titled(i, s_[3]) for i, s_ in zip(tiles, src)]
    gap = 16
    tw, th = tiles[0].size
    row = Image.new("RGB", (4 * tw + 3 * gap, th), (255, 255, 255))
    for i, t_ in enumerate(tiles):
        row.paste(t_, (i * (tw + gap), 0))
    sq = Image.new("RGB", (2 * tw + gap, 2 * th + gap), (255, 255, 255))
    for i, t_ in enumerate(tiles):
        sq.paste(t_, ((i % 2) * (tw + gap), (i // 2) * (th + gap)))
    for im, nm in ((row, "row"), (sq, "grid")):
        im.save(out / f"intro_1_2_3_4_robots_cube_80kg_{nm}.png")
        im.save(out / f"intro_1_2_3_4_robots_cube_80kg_{nm}.jpg", quality=95)
        im.save(out / f"intro_1_2_3_4_robots_cube_80kg_{nm}.pdf", resolution=300)
    print("intro done")


# ---------------------------------------------------------------- one strip per object, per method
LIB = ("cube", "long", "sphere", "cylinder", "arch", "dumbbell", "t_shape", "beam", "l_shape", "asym", "u_channel",
       "plus")  # the twelve objects, in the order of paper_media/object
PRETTY = {"t_shape": "T shape", "l_shape": "L shape", "u_channel": "U channel", "asym": "split-friction box"}
SCEN = ("A_straight", "B_left", "C_backright", "D_far_turn")
SCEN_TXT = {"A_straight": "straight", "B_left": "left", "C_backright": "back right", "D_far_turn": "far turn"}
OUTC = {"success": "success", "horizon": "timed out", "fell": "a robot fell"}
_CLIP = re.compile(r"^(?:mappo_|ippo_)?(?P<obj>[a-z_]+?)_(?P<m>\d+)kg_(?P<scen>[A-D]_[a-z_]+?)_(?:rep|r)(?P<rep>\d+)"
                   r"(?:_helper)?__(?P<out>success|horizon|fell)")


def _clips(paths):
    out = []
    for p in paths:
        m = _CLIP.match(p.name)
        if m:
            out.append(dict(path=p, obj=m["obj"], m=int(m["m"]), scen=m["scen"], out=m["out"]))
    return out


def _pick(cands, i, masses):
    """Best clip for the object at position i: a success if there is one, then a time-out, then a fall; heavier
    masses first in the order given; the scenario order is rotated by i so the set covers all four scenarios."""
    rot = SCEN[i % 4:] + SCEN[:i % 4]
    key = lambda c: (c.get("q", 0), ["success", "horizon", "fell"].index(c["out"]),
                     masses.index(c["m"]) if c["m"] in masses else 99, rot.index(c["scen"]), c["path"].name)
    return min(cands, key=key) if cands else None


def _k4_films():
    """Three-vs-four branch films (left k3, right k4) where robot 4 joined, arrived and pushed. Searched in
    presentation_export and every chain4 run's videos; one entry per unique film name."""
    import json
    seen, out = set(), []
    roots = [PE / "05_contact_planner" / "3_vs_4_robots"] + sorted((ROOT / "logs/evals").glob("k4*"))
    for r in roots:
        for p in sorted(list(r.glob("*/*.mp4")) + list(r.glob("videos/k3_vs_k4/*.mp4"))):
            if "__k3-" not in p.name or "__k4-" not in p.name or p.name in seen or not p.with_suffix(".json").exists():
                continue
            k4 = json.loads(p.with_suffix(".json").read_text()).get("k4", {})
            if not isinstance(k4.get("t_add4"), (int, float)):
                continue  # robot 4 never called in / no feasible assignment: not a four-robot film
            arrived = isinstance(k4.get("arrive4"), (int, float))
            press = k4["press_frac4"] if isinstance(k4.get("press_frac4"), (int, float)) else 0.0
            q = 0 if arrived and press >= 0.3 else 1 if arrived else 2  # pushing, reached the object, never reached
            seen.add(p.name)
            tf = [k4[c] for c in k4 if c.startswith("t_fall_") and isinstance(k4[c], (int, float))]
            end = k4["t_success"] if isinstance(k4.get("t_success"), (int, float)) else min(tf + [80.0])
            m = re.match(r"^(?P<obj>[a-z_]+?)_(?P<m>\d+)kg_(?P<scen>[A-D]_[a-z_]+?)_r\d+", p.name)
            out.append(dict(path=p, obj=m["obj"], m=int(m["m"]), scen=m["scen"], out=OUTC_KEY(k4["outcome"]),
                            arrive=k4["arrive4"] if arrived else None, end=end, press=press, q=q))
    return out


def OUTC_KEY(o: str) -> str:
    return "fell" if o.startswith("fell") else o


def _sheet(rows, name, width=420):
    """rows: (strip image, row label). Label column on the left, strips scaled to 4 x width."""
    gap, lw = 6, 290
    ims = []
    for img, _ in rows:
        s = width * 4 + 3 * gap
        ims.append(img.resize((s, round(img.height * s / img.width)), Image.LANCZOS))
    h = max(i.height for i in ims)
    g = Image.new("RGB", (lw + ims[0].width, len(ims) * h + (len(ims) - 1) * gap), (255, 255, 255))
    import matplotlib
    font = ImageFont.truetype(str(Path(matplotlib.get_data_path()) / "fonts/ttf/DejaVuSans-Bold.ttf"), 26)
    small = ImageFont.truetype(str(Path(matplotlib.get_data_path()) / "fonts/ttf/DejaVuSans.ttf"), 21)
    d = ImageDraw.Draw(g)
    for k, (im, (lab, sub)) in enumerate(zip(ims, (r[1] for r in rows))):
        y = k * (h + gap)
        g.paste(im, (lw, y))
        lines, cur = [], ""
        for part in sub.split(", "):  # wrap the description at commas to fit the label column
            nxt = f"{cur}, {part}" if cur else part
            if cur and d.textlength(nxt, font=small) > lw - 24:
                lines.append(cur + ",")
                nxt = part
            cur = nxt
        lines.append(cur)
        y0 = y + h // 2 - (36 + 26 * len(lines)) // 2
        d.text((14, y0), lab, fill=(0, 0, 0), font=font)
        for n, ln in enumerate(lines):
            d.text((14, y0 + 38 + 26 * n), ln, fill=(70, 70, 70), font=small)
    p = OUT / name
    g.save(p, quality=92)
    return p


def build_library():
    """One four-frame strip per object for each method, plus a contact sheet per method (all objects, and two halves
    of six for a page each). A success is used wherever the method has one filmed for that object; otherwise the
    best failure, named and labelled as such. Writes <folder>/all_objects/ and paper_media/library_index.csv.
    The last frame is at 92% of the clip, before the clip's tail after the episode ends."""
    Q = [0.02, 0.32, 0.62, 0.92]
    S = PE / "02_anymal_single_robot_push"
    C = PE / "05_contact_planner"
    sets = [
        ("02_single_robot", "single_robot", "One ANYmal, push policy",
         _clips(p for m in (20, 40, 60, 80) for p in (S / f"{m}kg").glob("*.mp4")), [60, 80, 40, 20]),
        ("03_ippo_mappo", "ippo", "IPPO pair", _clips((PE / "03_anymal_ippo_pair").glob("*.mp4")), [80, 40]),
        ("03_ippo_mappo", "mappo", "MAPPO pair", _clips((PE / "04_anymal_mappo_pair").glob("*.mp4")), [80, 40]),
        ("04_contact_planner", "planner_pair", "Contact planner, two robots",
         _clips(p for m in (20, 40, 60, 80) for p in (C / f"{m}kg").glob("*.mp4")), [80, 60, 40, 20]),
        ("05_teams_2_3_4", "three_robots", "Contact planner, three robots",
         _clips((PE / "10_planner_three_robots").glob("*.mp4")), [80, 100]),
        ("05_teams_2_3_4", "four_robots", "Contact planner, four robots", _k4_films(), [80, 60, 100, 40, 20]),
    ]
    index = [("method", "object", "mass_kg", "scenario", "outcome", "strip", "source")]
    for folder, tag, title, cands, masses in sets:
        rows = []
        for i, obj in enumerate(LIB):
            c = _pick([x for x in cands if x["obj"] == obj], i, masses)
            nm = PRETTY.get(obj, obj.replace("_", " "))
            if c is None:
                index.append((tag, obj, "", "", "not filmed", "", ""))
                print(f"  {tag}: no film of {obj}")
                continue
            suffix = "" if c["out"] == "success" else f"_{c['out']}"
            fn = f"{folder}/all_objects/{tag}_{obj}_{c['m']}kg_{c['scen']}{suffix}_strip.jpg"
            if c.get("q") == 2:
                fn = fn.replace("_strip.jpg", "_r4_not_at_contact_strip.jpg")
            if tag == "four_robots":
                # right panel (k4); film time 0 = episode 16 s; every frame inside k4's episode, the second just
                # after robot 4 reaches the object
                t_last = min(c["end"] - 16 - 0.5, duration(c["path"]) - 0.2)
                ta = min((c["arrive"] if c["arrive"] else 24.0) - 16 + 1.0, t_last - 1.0)
                times = [1.5, ta, (ta + t_last) / 2, t_last]
                p = save_strip(c["path"], times, fn, which="right", t0=16)
            else:
                p = save_strip(c["path"], Q, fn)
            sub = f"{c['m']} kg, {SCEN_TXT[c['scen']]}" + ("" if c["out"] == "success" else f", {OUTC[c['out']]}")
            if c.get("q") == 2:
                sub += ", R4 never at contact"
            elif c.get("q") == 1:
                sub += ", R4 barely pushed"
            rows.append((Image.open(p), (nm, sub)))
            index.append((tag, obj, c["m"], c["scen"], c["out"], fn, str(c["path"].relative_to(ROOT))))
        _sheet(rows, f"{folder}/{tag}_all_objects.jpg")
        _sheet(rows[:6], f"{folder}/{tag}_all_objects_part1.jpg")
        if rows[6:]:
            _sheet(rows[6:], f"{folder}/{tag}_all_objects_part2.jpg")
        print(f"{title}: {len(rows)} objects")
    with open(OUT / "library_index.csv", "w", newline="") as f:
        csv.writer(f).writerows(index)
    print("library done")


if __name__ == "__main__":
    what = sys.argv[1:] or ["frames", "maps", "graphs", "copy", "objects", "starts", "intro", "library"]
    for w in what:
        {"frames": build_frames, "maps": build_maps, "graphs": build_graphs, "copy": build_copy,
         "objects": build_objects, "starts": build_starts, "intro": build_intro, "library": build_library}[w]()
