"""Build paper_media/: video stills and filmstrips, object-map renders, and graphs for the paper.

CPU only (ffmpeg from imageio-ffmpeg, matplotlib, torch on CPU). Sources: presentation_export/ and
presentation_videos/ (films), evals_present/ and logs/evals/ (numbers). Re-run to rebuild; existing outputs are
overwritten.

    python scripts/paper_media.py [frames] [maps] [graphs] [copy]     (default: all)
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
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", size)
    except OSError:
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


def save_strip(v, times, name, which=None, crop=True, width=640, stamp=True):
    fr = frames_at(v, times, which, crop)
    ims = []
    for img, t in fr:
        img = img.resize((width, round(img.height * width / img.width)), Image.LANCZOS)
        ims.append(label(img, f"t = {t:.0f} s") if stamp else img)
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

    # single robot with its push policy (map + CNN)
    S = PE / "02_anymal_single_robot_push"
    save_strip(S / "40kg" / "arch_40kg_C_backright_rep0__success.mp4", [0.02, 0.33, 0.66, 0.98],
               "02_single_robot/single_anymal_arch_40kg_strip.jpg")
    save_still(S / "40kg" / "arch_40kg_C_backright_rep0__success.mp4", 0.5, "02_single_robot/single_anymal_arch_40kg.jpg")

    # IPPO / MAPPO pairs
    F = PV / "05_ippo_mappo_final_trained"
    save_strip(F / "mappo_long_80kg__success.mp4", [0.02, 0.33, 0.66, 0.98], "03_ippo_mappo/mappo_long_80kg_strip.jpg")
    save_strip(F / "ippo_l_shape_80kg__success.mp4", [0.02, 0.33, 0.66, 0.98], "03_ippo_mappo/ippo_l_shape_80kg_strip.jpg")
    save_strip(F / "mappo_long_40kg_far_turn__success.mp4", [0.02, 0.33, 0.66, 0.98],
               "03_ippo_mappo/mappo_long_40kg_far_turn_strip.jpg")
    save_still(F / "mappo_long_80kg__success.mp4", 0.66, "03_ippo_mappo/mappo_pair_pushing.jpg")
    save_still(F / "ippo_l_shape_80kg__success.mp4", 0.5, "03_ippo_mappo/ippo_pair_pushing.jpg")
    save_strip(PV / "03_frozen_pair_untrained" / sorted(p.name for p in (PV / "03_frozen_pair_untrained").glob("*.mp4"))[0],
               [0.02, 0.33, 0.66, 0.98], "03_ippo_mappo/frozen_pair_untrained_strip.jpg")

    # contact planner, two robots
    C = PV / "06_contact_planner"
    save_strip(C / "planner_long_40kg_far_turn__success.mp4", [0.02, 0.3, 0.6, 0.98],
               "04_contact_planner/planner_long_40kg_far_turn_strip.jpg")
    save_strip(C / "planner_arch_80kg_far_turn__success.mp4", [0.02, 0.33, 0.66, 0.98],
               "04_contact_planner/planner_arch_80kg_far_turn_strip.jpg")
    save_still(C / "planner_long_40kg_far_turn__success.mp4", 0.6, "04_contact_planner/planner_pair_contacts.jpg")

    # teams of 2, 3, 4 (same task family; contact posts: cyan / yellow pair, magenta helper)
    T = PE / "05_contact_planner" / "3_vs_4_robots"
    t23 = T / "2_vs_3" / "80kg" / "arch_80kg_B_left_r1__k2-success__k3b-success.mp4"
    t34 = T / "100kg" / "cube_100kg_C_backright_r2__k3-success__k4-success.mp4"
    h3 = PE / "10_planner_three_robots" / "arch_80kg_B_left_r0_helper__success.mp4"
    save_strip(h3, [0.02, 0.3, 0.6, 0.98], "05_teams_2_3_4/three_robots_arch_80kg_strip.jpg")
    save_still(h3, 0.98, "05_teams_2_3_4/three_robots_arch_80kg.jpg")
    if t23.exists():
        save_strip(t23, [0.02, 0.35, 0.7, 0.98], "05_teams_2_3_4/two_robots_arch_80kg_strip.jpg", which="left")
        save_strip(t23, [0.02, 0.35, 0.7, 0.98], "05_teams_2_3_4/three_robots_branch_arch_80kg_strip.jpg", which="right")
    save_strip(t34, [0.02, 0.35, 0.7, 0.98], "05_teams_2_3_4/three_robots_cube_100kg_strip.jpg", which="left")
    save_strip(t34, [0.02, 0.35, 0.7, 0.98], "05_teams_2_3_4/four_robots_cube_100kg_strip.jpg", which="right")
    items = []
    if t23.exists():
        items.append((t23, 0.7, "left", "2 robots"))
    items += [(h3, 0.9, None, "3 robots"), (t34, 0.7, "right", "4 robots")]
    grid_stills(items, "05_teams_2_3_4/team_sizes_2_3_4.jpg", len(items))

    # online learning: penalty after repeated failed pushes, long object 80 kg turned 60 deg
    P = PE / "06_contact_planner_online_learning" / "turning_test_mirror" / "penalty_acted" / "long_80kg_T60_m_r1"
    if P.exists():
        a = next(P.glob("A_original__*.mp4"))
        b = next(P.glob("B2_penalty__*.mp4"))
        save_strip(a, [0.02, 0.3, 0.6, 0.98], "06_online_learning/original_planner_long_80kg_turn60_strip.jpg")
        save_strip(b, [0.02, 0.3, 0.6, 0.98], "06_online_learning/penalty_planner_long_80kg_turn60_strip.jpg")
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
    print("graphs done")


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


if __name__ == "__main__":
    what = sys.argv[1:] or ["frames", "maps", "graphs", "copy"]
    for w in what:
        {"frames": build_frames, "maps": build_maps, "graphs": build_graphs, "copy": build_copy}[w]()
