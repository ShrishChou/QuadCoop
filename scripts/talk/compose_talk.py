"""Compose the 6.7980 talk media from the renders of scripts/talk/render_talk.sbatch (CPU only; run with nice).

    nice -n 19 .venv/bin/python scripts/talk/compose_talk.py            # everything
    nice -n 19 .venv/bin/python scripts/talk/compose_talk.py --only A    # Part A grids only (or B)

Writes presentation_export/talk/ (git-ignored):
  raw/<method>/<object>_<mass>kg_<goal>_rep<r>[_run<k>]__<outcome>.mp4   full-quality renders (hard links)
  grids/G<n>_<method>.mp4 + .jpg        4 x 3 tiles of 480 x 270, 4x speed, labelled, poster at 80 %
  compare/B<n>_<change>/<object>__<before>_vs_<after>.mp4 + .jpg: panels side by side, 1280 x 720 each
  compare/B<n>_<change>/B<n>_grid.mp4 + .jpg (B2-B6): the comparisons stacked, before | after columns
  manifest.csv, part_b_runs.csv (both runs of every Part B start), B5_three/k2_k3_k4_by_object.csv
and web copies of grids/ and compare/ in presentation_videos/talk/ (grids and change grids 720p, comparisons 1920 px
wide; CRF 28 or higher, <= 8 MB, <= 20 s). Every output is written to a temporary name and renamed when complete.
"""
from __future__ import annotations

import argparse
import csv
import glob
import json
import math
import os
import random
import re
import shutil
import subprocess
import tempfile
from collections import defaultdict
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
EV = ROOT / "logs" / "evals"
OUT = ROOT / "presentation_export" / "talk"
WEB = ROOT / "presentation_videos" / "talk"
FF = str(ROOT / ".venv/lib64/python3.12/site-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2")

PART_A_REP = random.Random(6798).randrange(10)  # = 9, also hard-coded in render_talk.sbatch
assert PART_A_REP == 9
GOALS = {"A_straight": ["cube", "long", "sphere"], "B_left": ["cylinder", "arch", "dumbbell"],
         "C_backright": ["t_shape", "beam", "l_shape"], "D_far_turn": ["asym", "u_channel", "plus"]}
ORDER = [o for v in GOALS.values() for o in v]
LIB = ["cube", "long", "sphere", "cylinder", "arch", "dumbbell", "t_shape", "beam", "l_shape", "asym", "u_channel", "plus"]
PRETTY = {"cube": "cube", "long": "long box", "sphere": "sphere", "cylinder": "cylinder", "arch": "arch",
          "dumbbell": "dumbbell", "t_shape": "T shape", "beam": "beam", "l_shape": "L shape",
          "asym": "split-friction box", "u_channel": "U channel", "plus": "plus"}
GOAL_TXT = {"A_straight": "3 m straight", "B_left": "3 m left, turn 30°", "C_backright": "3 m back-right, turn -60°",
            "D_far_turn": "5 m, turn 90°", "T60_m": "turn 60° in place (mirrored)"}
EXEC = "logs/keep/marl2/turn_debug/model_15000.pt"
MAPPO = "logs/marl2/nwB_mappo_uniform_s0/model_5000.pt"
IPPO = "logs/marl2/ippo_aa_kl_ten_s0/model_4000.pt"
STAGE2 = "Stage 2 push policy (scripts/methods.py default for --solo / --frozen-pair)"

# grid id, method, title, render group, checkpoint, mass
GRIDS = [("G0", "solo_20kg", "One robot", "A0", STAGE2, 20),
         ("G1", "solo", "One robot", "A1", STAGE2, 60),
         ("G2", "copies", "Two untrained copies", "A2", STAGE2, 60),
         ("G3", "ippo", "IPPO pair", "A3", IPPO, 60),
         ("G4", "mappo", "MAPPO pair", "A4", MAPPO, 60),
         ("G5", "planner", "Contact planner", "A5", f"{EXEC} (expert rule, original planner: no --set, as pres-planner-*-expert)", 60),
         ("G6", "trio", "Three robots (planner + helper)", "A6", f"{EXEC} (helper arm)", 80)]
CLIP = re.compile(r"^(?P<obj>[a-z_]+?)_(?P<m>\d+)kg_(?P<scen>[A-D]_[a-z_]+?|T\d+_m)_(?:rep|r)(?P<rep>\d+)(?:_helper)?__(?P<out>[a-z_0-9]+)\.mp4$")


def ff(*args):
    # the login node reports 448 cores: ffmpeg's auto threading then spawns hundreds of threads per decoder and runs
    # out of the slice's memory on the 12-input grids, so cap decoder, filter and encoder threads explicitly
    a = []
    for x in map(str, args):
        if x == "-i":
            a += ["-threads", "2"]
        a.append(x)
    if "-c:v" in a:
        a[a.index("-c:v"):a.index("-c:v")] = ["-threads", "8"]
    subprocess.run(["nice", "-n", "19", FF, "-v", "error", "-y", "-filter_threads", "2", "-filter_complex_threads", "4",
                    *a], check=True)


def dur(v: Path) -> float:
    e = subprocess.run([FF, "-hide_banner", "-i", str(v)], capture_output=True, text=True).stderr
    h, m, s = re.search(r"Duration: (\d+):(\d+):([\d.]+)", e).groups()
    return int(h) * 3600 + int(m) * 60 + float(s)


def size(v: Path) -> tuple[int, int]:
    e = subprocess.run([FF, "-hide_banner", "-i", str(v)], capture_output=True, text=True).stderr
    w, h = re.search(r"Video:.*?(\d{3,5})x(\d{3,5})", e).groups()
    return int(w), int(h)


def frame(v: Path, t: float) -> Image.Image:
    import io
    b = subprocess.run(["nice", "-n", "19", FF, "-v", "error", "-ss", f"{t:.2f}", "-i", str(v), "-frames:v", "1",
                        "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True, check=True).stdout
    return Image.open(io.BytesIO(b)).convert("RGB")


def cap_top(img: Image.Image) -> int:
    """Height of the burned-in caption bar (near-black rows in the top third)."""
    a = np.asarray(img).astype(np.int16)
    dark = (a.max(-1) < 70).mean(1)
    c = np.nonzero(dark[: len(dark) // 3] > 0.5)[0]
    return int(c.max()) + 3 if len(c) else 0


def crop_box(v: Path, half: str | None = None) -> tuple[int, int, int, int]:
    """(w, h, x, y): the 16:9 window under the caption bar (of one half of a side-by-side film)."""
    W, H = size(v)
    x0, pw = 0, W
    if half:
        pw = W // 2
        x0 = 0 if half == "left" else pw
    img = frame(v, dur(v) * 0.3).crop((x0, 0, x0 + pw, H))
    top = cap_top(img)
    top += top % 2
    ch = H - top
    cw = min(pw, int(ch * 16 / 9)) // 2 * 2
    ch = min(ch, int(cw * 9 / 16)) // 2 * 2
    return cw, ch, x0 + (pw - cw) // 2, top


def outcome_word(o: str) -> str:
    return "SUCCESS" if o == "success" else "FELL" if o.startswith("fell") else "TIMEOUT"


def is_fail(o: str) -> bool:
    return o != "success"


FONT = None


def font(px: int):
    import matplotlib
    return ImageFont.truetype(str(Path(matplotlib.get_data_path()) / "fonts/ttf/DejaVuSans-Bold.ttf"), px)


def label_png(lines: list[tuple[str, tuple]], px: int, path: Path) -> Path:
    """A dark rounded box with coloured text lines, for overlay at the top-left of a panel."""
    f = font(px)
    d0 = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    ws = [d0.textbbox((0, 0), t, font=f) for t, _ in lines]
    pad = px // 3
    W = max(b[2] - b[0] for b in ws) + 2 * pad
    lh = px + px // 4
    H = lh * len(lines) + 2 * pad - px // 4
    im = Image.new("RGBA", (W + 2, H + 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, W, H), radius=px // 3, fill=(15, 20, 30, 200))
    for i, ((t, col), b) in enumerate(zip(lines, ws)):
        d.text((pad - b[0], pad + i * lh - b[1]), t, font=f, fill=col)
    im.save(path)
    return path


WHITE, GREEN, AMBER, RED = (255, 255, 255, 255), (110, 230, 120, 255), (255, 200, 70, 255), (255, 110, 100, 255)


def out_col(o: str):
    return GREEN if o == "success" else RED if o.startswith("fell") else AMBER


def panel_chain(i: int, li: int, box, w: int, h: int, speed: float, total: float, cut: float | None = None) -> str:
    """One labelled panel; cut (s of film) freezes the panel there (a branch film runs on after its own end)."""
    cw, ch, cx, cy = box
    tr = f"trim=duration={cut:.2f}," if cut else ""
    return (f"[{i}:v]{tr}crop={cw}:{ch}:{cx}:{cy},scale={w}:{h}:flags=lanczos,setpts=PTS/{speed:g},fps=30,"
            f"tpad=stop_mode=clone:stop_duration={total + 5:.1f},trim=duration={total:.2f},setpts=PTS-STARTPTS[p{i}];"
            f"[p{i}][{li}:v]overlay=8:8[q{i}]")


def tmp_of(out: Path) -> Path:
    return out.with_name(out.stem + ".tmp" + out.suffix)


def finish(out: Path, poster: bool = True):
    """Rename the temporary output into place; write the poster (80 % of the duration) the same way."""
    os.replace(tmp_of(out), out)
    if poster:
        jp = out.with_suffix(".jpg")
        ff("-ss", f"{dur(out) * 0.8:.2f}", "-i", out, "-frames:v", "1", "-q:v", "2", tmp_of(jp))
        os.replace(tmp_of(jp), jp)


def encode(inputs: list[Path], labels: list[Path], chains: list[str], stack: str, out: Path, crf=18):
    args = []
    for p in inputs:
        args += ["-i", p]
    for p in labels:
        args += ["-i", p]
    fc = ";".join(chains) + ";" + stack
    out.parent.mkdir(parents=True, exist_ok=True)
    ff(*args, "-filter_complex", fc, "-map", "[out]", "-an", "-c:v", "libx264", "-preset", "medium", "-crf", crf,
       "-pix_fmt", "yuv420p", "-movflags", "+faststart", tmp_of(out))
    finish(out)


def link(src: Path, dst: Path) -> Path:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        dst.unlink()
    try:
        os.link(src, dst)
    except OSError:
        shutil.copy2(src, dst)
    return dst


# ---------------------------------------------------------------- reading the renders
def eval_dirs(name: str) -> list[Path]:
    return [d for d in (EV / name / "pair", EV / f"{name}-expert" / "pair", EV / name) if d.is_dir()]


def csv_rows(name: str) -> list[dict]:
    for d in eval_dirs(name):
        if (d / "episodes.csv").exists():
            return list(csv.DictReader(open(d / "episodes.csv")))
    return []


def summary_policy(name: str) -> str:
    for d in eval_dirs(name):
        if (d / "summary.json").exists():
            return json.load(open(d / "summary.json")).get("policy", "")
    return ""


def films(name: str) -> list[dict]:
    """Every filmed episode of one render step, with its CSV row (outcome, t_success)."""
    rows = csv_rows(name)
    out = []
    for d in eval_dirs(name):
        for v in sorted((d / "videos").glob("*.mp4")) if (d / "videos").is_dir() else []:
            m = CLIP.match(v.name)
            if not m:
                continue
            o, mass, s, rep = m["obj"], float(m["m"]), m["scen"], int(m["rep"])
            row = next((r for r in rows if r["object"] == o and float(r["mass"]) == mass and r["scenario"] == s
                        and int(r["rep"]) == rep and r.get("formation", "standard") == "standard"
                        and r.get("swap", "0") in ("0", "False", "")
                        and r.get("arm", "helper") in ("helper", "") ), None)
            out.append(dict(path=v, object=o, mass=mass, goal=s, rep=rep, outcome=m["out"],
                            t_success=(row or {}).get("t_success", ""), run_name=name))
        if out:
            break
    return out


def task_outcome(name: str, o: str, mass: float, s: str, rep: int) -> tuple[str, str]:
    for r in csv_rows(name):
        if (r["object"] == o and float(r["mass"]) == mass and r["scenario"] == s and int(r["rep"]) == rep
                and r.get("formation", "standard") == "standard" and r.get("swap", "0") in ("0", "False", "")):
            return r["outcome"], r.get("t_success", "")
    return "", ""


MANIFEST: list[dict] = []
RUNLOG: list[dict] = []


def mrow(**kw):
    base = dict(file="", slide="", method="", checkpoint="", object="", mass="", goal="", seed="", rep="", outcome="",
                t_success="", run="")
    base.update({k: ("" if v is None else v) for k, v in kw.items()})
    MANIFEST.append(base)


def raw_name(c: dict, run: int | None = None) -> str:
    return (f"{c['object']}_{c['mass']:g}kg_{c['goal']}_rep{c['rep']}{'' if run is None else f'_run{run}'}"
            f"__{c['outcome']}.mp4")


# ---------------------------------------------------------------- Part A
def part_a(only=None):
    for gid, meth, title, grp, ck, mass in GRIDS:
        if only and gid not in only:
            continue
        clips = []
        for i in range(4):
            clips += films(f"talk-{grp}-g{i}")
        by = {c["object"]: c for c in clips if c["rep"] == PART_A_REP}
        missing = [o for o in ORDER if o not in by]
        if missing:
            print(f"{gid}: missing {missing}; skipped")
            continue
        tiles = []
        for o in ORDER:
            c = by[o]
            raw = link(c["path"], OUT / "raw" / meth / raw_name(c))
            seed = 7100
            mrow(file=raw.relative_to(OUT), slide=gid, method=title, checkpoint=summary_policy(c["run_name"]) or ck,
                 object=o, mass=c["mass"], goal=c["goal"], seed=seed, rep=c["rep"], outcome=c["outcome"],
                 t_success=c["t_success"], run=c["run_name"])
            tiles.append((raw, c))
        total = min(20.0, max(dur(p) for p, _ in tiles) / 4.0)
        with tempfile.TemporaryDirectory() as td:
            labels, chains = [], []
            for i, (p, c) in enumerate(tiles):
                lab = label_png([(f"{PRETTY[c['object']]} · {GOAL_TXT[c['goal']]}", WHITE),
                                 (outcome_word(c["outcome"]) + (f"  {float(c['t_success']):.0f} s" if c["t_success"] else ""),
                                  out_col(c["outcome"]))], 15, Path(td) / f"l{i}.png")
                labels.append(lab)
                chains.append(panel_chain(i, 12 + i, crop_box(p), 480, 270, 4, total))
            lay = "|".join(f"{(i % 4) * 480}_{(i // 4) * 270}" for i in range(12))
            out = OUT / "grids" / f"{gid}_{meth}.mp4"
            # title strip at the top (135 px) and bottom (135 px): 3 rows x 270 = 810 px of tiles
            tp = label_png([(f"{title}  ·  {mass} kg  ·  seed 7100, rep {PART_A_REP}  ·  4× speed", WHITE)], 30,
                           Path(td) / "title.png")
            # 3 rows x 270 = 810 px of tiles, centred; the title sits in the top band (input 24 = 12 clips + 12 labels)
            stack = ("".join(f"[q{i}]" for i in range(12)) + f"xstack=inputs=12:layout={lay}[g];"
                     f"[g]pad=1920:1080:0:135:color=0x0f141e[g2];[g2][24:v]overlay=(W-w)/2:40[out]")
            encode([p for p, _ in tiles], labels + [tp], chains, stack, out)
        mrow(file=out.relative_to(OUT), slide=gid, method=title, checkpoint=ck, object="12 objects", mass=mass,
             goal="3 per goal", seed=7100, rep=PART_A_REP,
             outcome=";".join(f"{c['object']}:{outcome_word(c['outcome'])}" for _, c in tiles))
        print("wrote", out)


# ---------------------------------------------------------------- Part B
def expect(src, o, mass, s, rep):
    """The outcome the source evaluation recorded for this start (the label a kept run should match).
    src: an evaluation name under logs/evals, or a Path to an episodes.csv."""
    if isinstance(src, Path):
        for r in csv.DictReader(open(src)):
            if (r["object"] == o and float(r["mass"]) == mass and r["scenario"] == s and int(r["rep"]) == rep
                    and r.get("formation", "standard") == "standard"):
                return r["outcome"]
        return ""
    return task_outcome(src, o, mass, s, rep)[0]


def matches(got: str, want: str) -> int:
    """2 = same outcome class (success / fell / timeout), 1 = both failures, 0 = no."""
    if not got:
        return -1
    if outcome_word(got) == outcome_word(want):
        return 2
    return 1 if is_fail(got) and is_fail(want) else 0


def pick_run(change, arm, o, mass, s, rep, step_names, want, method_dir, ck, seed, slide):
    """Choose between the two runs of one arm on one start; log both."""
    cands = []
    for k, n in enumerate(step_names, 1):
        f = [c for c in films(n) if c["object"] == o and c["mass"] == mass and c["goal"] == s and c["rep"] == rep]
        got, ts = task_outcome(n, o, mass, s, rep)
        RUNLOG.append(dict(change=change, arm=arm, object=o, mass=mass, goal=s, rep=rep, seed=seed, run=k, step=n,
                           outcome=got, t_success=ts, label=want, film=bool(f)))
        if f:
            cands.append((matches(f[0]["outcome"], want), -k, k, f[0]))
    if not cands:
        return None
    cands.sort(reverse=True)
    q, _, k, c = cands[0]
    for r in RUNLOG[-len(step_names):]:
        r["kept"] = int(r["run"] == k)
        r["label_match"] = q
    raw = link(c["path"], OUT / "raw" / method_dir / raw_name(c, k))
    mrow(file=raw.relative_to(OUT), slide=slide, method=arm, checkpoint=summary_policy(c["run_name"]) or ck, object=o,
         mass=mass, goal=s, seed=seed, rep=rep, outcome=c["outcome"], t_success=c["t_success"], run=f"{k} ({c['run_name']})")
    c = dict(c, path=raw, run=k)
    return c


def compare_video(rows: list[tuple[str, Path, dict, str | None]], out: Path, title: str):
    """Panels side by side (left to right), 1280 x 720 each, labelled; sped up so the video lasts at most 20 s.
    rows: (arm label, film, clip info, half of a side-by-side film or None)."""
    pw, ph = 1280, 720
    longest = max(dur(p) for _, p, _, _ in rows)
    speed = max(3.0, math.ceil(longest / 20.0 * 2) / 2)
    total = min(20.0, longest / speed)
    with tempfile.TemporaryDirectory() as td:
        labels, chains = [], []
        n = len(rows)
        for i, (arm, p, c, half) in enumerate(rows):
            ts = c.get("t_success") or ""
            lab = label_png([(arm, WHITE), (outcome_word(c["outcome"]) + (f" at {float(ts):.1f} s" if ts else ""),
                                            out_col(c["outcome"]))], 30, Path(td) / f"l{i}.png")
            labels.append(lab)
            chains.append(panel_chain(i, n + i, crop_box(p, half), pw, ph, speed, total, c.get("cut")))
        tp = label_png([(f"{title} · {speed:g}× speed", WHITE)], 24, Path(td) / "t.png")
        stack = "".join(f"[q{i}]" for i in range(n)) + f"hstack=inputs={n}[s];[s][{2 * n}:v]overlay=(W-w)/2:H-h-12[out]"
        encode([p for _, p, _, _ in rows], labels + [tp], chains, stack, out)
    return out


def change_grid(videos: list[Path], out: Path):
    """The side-by-side comparisons of one change stacked top to bottom (columns = before | after), fitted in
    1920 x 1080."""
    n = len(videos)
    w0, h0 = size(videos[0])
    k = min(1920 / w0, 1080 / (n * h0))
    w, h = int(w0 * k) // 2 * 2, int(h0 * k) // 2 * 2
    total = max(dur(v) for v in videos)
    chains = [f"[{i}:v]scale={w}:{h}:flags=lanczos,tpad=stop_mode=clone:stop_duration={total + 2:.1f},"
              f"trim=duration={total:.2f},setpts=PTS-STARTPTS[c{i}]" for i in range(n)]
    stack = "[c0]copy[out]" if n == 1 else "".join(f"[c{i}]" for i in range(n)) + f"vstack=inputs={n}[out]"
    args = []
    for v in videos:
        args += ["-i", v]
    ff(*args, "-filter_complex", ";".join(chains) + ";" + stack, "-map", "[out]", "-an", "-c:v", "libx264",
       "-preset", "medium", "-crf", 18, "-pix_fmt", "yuv420p", "-movflags", "+faststart", tmp_of(out))
    finish(out)
    mrow(file=out.relative_to(OUT), slide=out.parent.name.split("_")[0], method="grid of " + ", ".join(v.stem for v in videos))


def simple_change(change: str, folder: str, starts, arms, seed: int, slug: str, grid: bool = True):
    """starts: (object, mass, goal, rep, step group); arms: (key, label, method_dir, source of the label, ck)."""
    vids = []
    for o, mass, s, rep, grp in starts:
        rows = []
        for key, label, mdir, src, ck in arms:
            want = expect(src(mass) if callable(src) else src, o, mass, s, rep)
            steps = [f"talk-{change}-{key}-{grp}-r{r}" + ("-expert" if key == "plan" else "") for r in (1, 2)]
            c = pick_run(change, label, o, mass, s, rep, steps, want, mdir, ck, seed, change)
            if c is None:
                print(f"{change} {o}: no film for {key}")
                break
            rows.append((label, c["path"], c, None))
        else:
            out = OUT / "compare" / folder / f"{o}_{mass:g}kg_{s}_rep{rep}__{slug}.mp4"
            compare_video(rows, out, f"{PRETTY[o]} · {mass:g} kg · {GOAL_TXT[s]} · same start")
            mrow(file=out.relative_to(OUT), slide=change, method=" | ".join(a[1] for a in arms), object=o, mass=mass,
                 goal=s, seed=seed, rep=rep, outcome=" | ".join(outcome_word(r[2]["outcome"]) for r in rows))
            vids.append(out)
            print("wrote", out)
    if vids and grid:
        change_grid(vids, OUT / "compare" / folder / f"{change}_grid.mp4")


def b4():
    vids = []
    for task in ("arch_60kg_T60_m_r0", "long_60kg_T60_m_r1", "long_80kg_T60_m_r1"):
        rows = []
        for arm, label, d in (("A", "Original planner (fail_mem=0.5)", "planner_original"),
                              ("B2", "Failed-contact penalty (fail_mem=1, fail_act=2)", "planner_penalty")):
            vd = EV / f"fm-test-{arm}-turn_mirror-expert" / "pair" / "videos"
            v = next(vd.glob(f"{task}__*.mp4"), None)
            if v is None:
                print("B4 missing", arm, task)
                return
            j = json.load(open(vd / f"{task}.json"))
            m = CLIP.match(v.name)
            c = dict(object=m["obj"], mass=float(m["m"]), goal=m["scen"], rep=int(m["rep"]), outcome=m["out"],
                     t_success=j.get("t_success", ""))
            raw = link(v, OUT / "raw" / d / raw_name(c))
            mrow(file=raw.relative_to(OUT), slide="B4", method=label, checkpoint=EXEC, object=c["object"], mass=c["mass"],
                 goal=c["goal"], seed=7300, rep=c["rep"], outcome=c["outcome"], t_success=c["t_success"],
                 run=f"fm-test-{arm}-turn_mirror-expert (existing film)")
            rows.append((label, raw, c, None))
        c = rows[0][2]
        out = OUT / "compare" / "B4_penalty" / f"{task}__original_vs_penalty.mp4"
        compare_video(rows, out, f"{PRETTY[c['object']]} · {c['mass']:g} kg · turn 60° in place · same start")
        mrow(file=out.relative_to(OUT), slide="B4", method="original vs penalty", object=c["object"], mass=c["mass"],
             goal=c["goal"], seed=7300, rep=c["rep"], outcome=" | ".join(outcome_word(r[2]["outcome"]) for r in rows))
        vids.append(out)
    change_grid(vids, OUT / "compare" / "B4_penalty" / "B4_grid.mp4")


def branch_compare(v: Path, left_lbl, right_lbl, info_l, info_r, out: Path, slide, seed, method_dir):
    raw = link(v, OUT / "raw" / method_dir / v.name)
    o, mass, s, rep = info_l["object"], info_l["mass"], info_l["goal"], info_l["rep"]
    for lbl, inf in ((left_lbl, info_l), (right_lbl, info_r)):
        mrow(file=raw.relative_to(OUT), slide=slide, method=lbl, checkpoint=EXEC, object=o, mass=mass, goal=s, seed=seed,
             rep=rep, outcome=inf["outcome"], t_success=inf["t_success"], run=inf.get("run", ""))
    for inf in (info_l, info_r):
        if inf["outcome"] == "success" and inf.get("t_success"):
            inf["cut"] = float(inf["t_success"]) - 16.0 + 1.0
    rows = [(left_lbl, raw, info_l, "left"), (right_lbl, raw, info_r, "right")]
    compare_video(rows, out, f"{PRETTY[o]} · {mass:g} kg · {GOAL_TXT[s]} · cloned state, from 16 s")
    mrow(file=out.relative_to(OUT), slide=slide, method=f"{left_lbl} vs {right_lbl}", object=o, mass=mass, goal=s,
         seed=seed, rep=rep, outcome=f"{outcome_word(info_l['outcome'])} | {outcome_word(info_r['outcome'])}")
    return out


BR = re.compile(r"^(?P<obj>[a-z_]+?)_(?P<m>\d+)kg_(?P<scen>[A-D]_[a-z_]+?)_r(?P<rep>\d+)__(?P<l>k\w+?)-(?P<lo>[a-z_0-9]+)__(?P<r>k\w+?)-(?P<ro>[a-z_0-9]+)\.mp4$")


def b5():
    # per-object table from the k4c trees
    S = defaultdict(list)
    for f in sorted(glob.glob(str(EV / "k4c-s*" / "episodes.csv"))):
        for r in csv.DictReader(open(f)):
            S[(r["object"], float(r["mass"]), r["arm"])].append(int(r["success"]))
    tab = OUT / "compare" / "B5_three" / "k2_k3_k4_by_object.csv"
    tab.parent.mkdir(parents=True, exist_ok=True)
    objs = sorted({k[0] for k in S})
    masses = sorted({k[1] for k in S})
    arms = ("k2", "k3", "k3b", "k4")
    head = ["k2: pair only (%)", "k3: robot 3 joins at 8 s (%)", "k3b: robot 3 called at 20 s (%)",
            "k4: robot 4 called at 20 s, on k3 (%)"]
    with open(tmp_of(tab), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["object", "mass_kg", "n_per_arm"] + head + ["k3 - k2 (pp)", "k3b - k2 (pp)", "k4 - k3 (pp)"])
        for m in masses + ["all"]:
            for o in objs + ["all"]:
                p, n = {}, 0
                for a_ in arms:
                    xs = [x for (oo, mm, aa), v in S.items() if (o == "all" or oo == o) and aa == a_
                          and (m == "all" or mm == m) for x in v]
                    p[a_], n = 100 * sum(xs) / len(xs), len(xs)
                w.writerow([o, m if m == "all" else f"{m:g}", n] + [f"{p[a_]:.1f}" for a_ in arms]
                           + [f"{p['k3'] - p['k2']:+.1f}", f"{p['k3b'] - p['k2']:+.1f}", f"{p['k4'] - p['k3']:+.1f}"])
    os.replace(tmp_of(tab), tab)
    gain = sorted(objs, key=lambda o: -(np.mean(S[(o, 80.0, "k3")]) - np.mean(S[(o, 80.0, "k2")])))[:2]
    print("B5 objects (largest k3 - k2 at 80 kg):", gain)
    mrow(file=tab.relative_to(OUT), slide="B5", method="per-mass, per-object success, k4c trees (5 seeds x 4 goals x 3 reps)",
         seed="1001,1002,1003,8401,8402")
    # films: rescues (k2 fails, k3b succeeds) from the two runs
    films_ = []
    eps = {}
    for k in (1, 2):
        n = f"talk-B5-r{k}"
        eps[k] = list(csv.DictReader(open(EV / n / "episodes.csv"))) if (EV / n / "episodes.csv").exists() else []
        for v in sorted((EV / n / "videos" / "k2_vs_k3b").glob("*.mp4")):
            m = BR.match(v.name)
            if m:
                films_.append((k, v, m))

    def outc(k, arm, o, s, rep):
        r = next((r for r in eps[k] if r["arm"] == arm and r["object"] == o and r["scenario"] == s
                  and int(r["rep"]) == rep and float(r["mass"]) == 80.0), None)
        return (r["outcome"], r["t_success"]) if r else ("", "")
    vids = []
    for o in gain:
        cands = []
        for k, v, m in films_:
            if m["obj"] != o:
                continue
            s, rep = m["scen"], int(m["rep"])
            rescue = m["lo"] != "success" and m["ro"] == "success"
            other = 3 - k
            o2 = outc(other, "k2", o, s, rep)[0], outc(other, "k3b", o, s, rep)[0]
            agree = int(o2[0] == m["lo"] and o2[1] == m["ro"])
            cands.append((int(rescue), agree, -k, k, v, m))
        if not cands:
            print("B5: no film for", o)
            continue
        cands.sort(reverse=True)
        rescue, agree, _, k, v, m = cands[0]
        s, rep = m["scen"], int(m["rep"])
        for kk in (1, 2):
            for arm in ("k2", "k3b"):
                got, ts = outc(kk, arm, o, s, rep)
                RUNLOG.append(dict(change="B5", arm=arm, object=o, mass=80, goal=s, rep=rep, seed=1001, run=kk,
                                   step=f"talk-B5-r{kk}", outcome=got, t_success=ts,
                                   label="horizon" if arm == "k2" else "success", film=kk == k, kept=int(kk == k),
                                   label_match=2 if rescue else 0))
        il = dict(object=o, mass=80.0, goal=s, rep=rep, outcome=m["lo"], t_success=outc(k, "k2", o, s, rep)[1], run=k)
        ir = dict(object=o, mass=80.0, goal=s, rep=rep, outcome=m["ro"], t_success=outc(k, "k3b", o, s, rep)[1], run=k)
        out = OUT / "compare" / "B5_three" / f"{o}_80kg_{s}_r{rep}__pair_vs_three.mp4"
        vids.append(branch_compare(v, "Pair continues", "Robot 3 called at 20 s", il, ir, out, "B5", 1001, "branch_k2_vs_k3b"))
        print("wrote", out)
    if vids:
        change_grid(vids, OUT / "compare" / "B5_three" / "B5_grid.mp4")


def b6():
    T = ROOT / "presentation_export" / "05_contact_planner" / "3_vs_4_robots"
    vids = []
    for v in (T / "80kg" / "cube_80kg_A_straight_r2__k3-success__k4-horizon.mp4",
              T / "40kg" / "cylinder_40kg_A_straight_r2__k3-horizon__k4-success.mp4"):
        j = json.load(open(v.with_suffix(".json")))
        base = dict(object=j["object"], mass=float(j["mass"]), goal=j["scenario"], rep=int(j["rep"]), run="k4cf-s1001")
        il = dict(base, outcome=j["k3"]["outcome"], t_success=j["k3"].get("t_success", ""))
        ir = dict(base, outcome=j["k4"]["outcome"], t_success=j["k4"].get("t_success", ""))
        tag = "opener" if j["object"] == "cube" else "rescue"
        out = OUT / "compare" / "B6_four" / f"{j['object']}_{j['mass']:g}kg_{tag}__three_vs_four.mp4"
        vids.append(branch_compare(v, "Stay at three", "Robot 4 called at 20 s", il, ir, out, "B6", 1001, "branch_k3_vs_k4"))
        print("wrote", out)
    change_grid(vids, OUT / "compare" / "B6_four" / "B6_grid.mp4")


def part_b():
    simple_change("B1", "B1_teammate",
                  [("long", 80.0, "A_straight", 0, "a"), ("l_shape", 80.0, "A_straight", 0, "a"),
                   ("t_shape", 60.0, "A_straight", 0, "b"), ("u_channel", 60.0, "B_left", 2, "c")],
                  [("solo", "One robot", "solo", "pres-solo-anymal", STAGE2),
                   ("copies", "Two untrained copies", "copies", "pres-frozen-pair", STAGE2),
                   ("mappo", "MAPPO pair", "mappo", "pres-mappo-B-it5000", MAPPO)], 7100, "solo_vs_copies_vs_mappo", grid=False)
    simple_change("B2", "B2_kl",
                  [("long", 60.0, "A_straight", 0, "a"), ("u_channel", 60.0, "A_straight", 0, "a"),
                   ("dumbbell", 40.0, "A_straight", 0, "b"), ("t_shape", 40.0, "A_straight", 0, "b")],
                  [("nokl", "MAPPO, KL anchor off", "mappo_nokl", "mappo-aa_nokl-s0-it3000", "logs/marl2/mappo_aa_nokl_s0/model_3000.pt"),
                   ("kl", "MAPPO, KL anchor on", "mappo_kl", "mappo-aa_kl-s0-it3000", "logs/marl2/mappo_aa_kl_s0/model_3000.pt")],
                  0, "kl_off_vs_on")
    simple_change("B3", "B3_planner",
                  [("arch", 60.0, "A_straight", 8, "a"), ("u_channel", 80.0, "A_straight", 8, "c"),
                   ("asym", 60.0, "B_left", 9, "b")],
                  [("mappo", "MAPPO pair", "mappo", ROOT / "presentation_export/04_anymal_mappo_pair/episodes.csv", MAPPO),
                   ("plan", "Contact planner", "planner", lambda m: f"pres-planner-{m:g}kg-expert",
                    f"{EXEC} (expert rule, original planner: no --set)")],
                  7100, "mappo_vs_planner")
    b4()
    b5()
    b6()


def web_copies(only=None):
    for src in sorted(list((OUT / "grids").glob("*.mp4")) + list((OUT / "compare").rglob("*.mp4"))):
        if src.stem.endswith(".tmp") or (only and src.stem.split("_")[0] not in only):
            continue
        rel = src.relative_to(OUT)
        dst = WEB / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        w, h = size(src)
        side = "compare" in rel.parts and not src.stem.endswith("_grid")
        k = 1920 / w if side else min(1.0, 720 / min(w, h))  # comparisons 1920 wide, the rest 720p
        W, H = int(w * k) // 2 * 2, int(h * k) // 2 * 2
        for crf in (28, 30, 32, 34, 36):
            ff("-i", src, "-t", 20, "-vf", f"scale={W}:{H}:flags=lanczos", "-an", "-c:v", "libx264", "-preset", "slow",
               "-crf", crf, "-pix_fmt", "yuv420p", "-movflags", "+faststart", tmp_of(dst))
            if tmp_of(dst).stat().st_size <= 8e6:
                break
        os.replace(tmp_of(dst), dst)
        if crf != 28:
            print(f"web copy {rel}: CRF {crf} to stay under 8 MB")
        jp = src.with_suffix(".jpg")
        if jp.exists():
            im = Image.open(jp).convert("RGB")
            im.thumbnail((W, H))
            im.save(tmp_of(dst.with_suffix(".jpg")), quality=88, format="JPEG")
            os.replace(tmp_of(dst.with_suffix(".jpg")), dst.with_suffix(".jpg"))
    for f in ("manifest.csv", "part_b_runs.csv"):
        if (OUT / f).exists():
            shutil.copy2(OUT / f, WEB / f)
    tab = OUT / "compare" / "B5_three" / "k2_k3_k4_by_object.csv"
    if tab.exists():
        (WEB / "compare" / "B5_three").mkdir(parents=True, exist_ok=True)
        shutil.copy2(tab, WEB / "compare" / "B5_three" / tab.name)


def jp_size(p: Path):
    with Image.open(p) as im:
        return im.size


def write_csvs(only=None):
    """only: the grid ids rebuilt this run; their rows replace theirs in the existing manifest, the rest is kept and
    part_b_runs.csv is left as it is."""
    OUT.mkdir(parents=True, exist_ok=True)
    keys = ["file", "slide", "method", "checkpoint", "object", "mass", "goal", "seed", "rep", "outcome", "t_success", "run"]
    rows = MANIFEST
    if only:
        with open(OUT / "manifest.csv", newline="") as fh:
            old = [r for r in csv.DictReader(fh) if r["slide"][:2] not in only]
        rows = sorted(old + MANIFEST, key=lambda r: (str(r["slide"])[0] != "G", str(r["slide"])[:2]))  # stable
    with open(tmp_of(OUT / "manifest.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, keys)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in keys})
    if only:
        os.replace(tmp_of(OUT / "manifest.csv"), OUT / "manifest.csv")
        return
    keys = ["change", "arm", "object", "mass", "goal", "rep", "seed", "run", "step", "outcome", "t_success", "label",
            "label_match", "kept", "film"]
    os.replace(tmp_of(OUT / "manifest.csv"), OUT / "manifest.csv")
    with open(tmp_of(OUT / "part_b_runs.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, keys)
        w.writeheader()
        for r in RUNLOG:
            w.writerow({k: r.get(k, "") for k in keys})
    os.replace(tmp_of(OUT / "part_b_runs.csv"), OUT / "part_b_runs.csv")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="AB", help="A, B or AB")
    ap.add_argument("--web", type=int, default=1)
    ap.add_argument("--grids", default="", help="comma list of grid ids (e.g. G0): build only these, merge their rows "
                                                 "into the existing manifest and make only their web copies")
    a = ap.parse_args()
    only = [g for g in a.grids.split(",") if g] or None
    if only:
        part_a(only)
    else:
        if "A" in a.only:
            part_a()
        if "B" in a.only:
            part_b()
    write_csvs(only)
    if a.web:
        web_copies(only)
