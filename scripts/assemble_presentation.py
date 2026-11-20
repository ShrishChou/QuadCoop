"""Build presentation_export/01-05 from the presentation v2 runs (slurm/submit_presentation_v2.sh). Videos are hard
links (no copy, never re-encoded); metrics come from scripts/presentation_metrics.py. Safe to re-run: missing inputs
are reported and skipped.

    python scripts/assemble_presentation.py

01_walkers                       ANYmal and Spot walkers: fleet corner + flyover, 4 single-robot clips each
02_anymal_single_robot_push      best single-robot ANYmal pusher: best-of-10 video per mass x object x position
                                 (<mass>kg/ subfolders), metrics.md, metrics_by_case.csv, episodes.csv
03_anymal_ippo_pair              IPPO pair videos (moved from 12_pairs_all_objects), metrics, comparison vs single robot
04_anymal_mappo_pair             MAPPO pair videos (moved from 12), metrics, comparison vs single robot and IPPO
05_contact_planner               contact planner best-of-10 videos with the arrow overlay, metrics, comparison of all four
comparison.md                    all four systems side by side
"""
from __future__ import annotations

import csv
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PE = ROOT / "presentation_export"
LE = ROOT / "logs" / "evals"
MASSES = (20, 40, 60, 80)
PY = sys.executable
PM = str(ROOT / "scripts" / "presentation_metrics.py")


def link(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        dst.unlink()
    os.link(src, dst)


def concat(paths: list[Path], out: Path) -> Path | None:
    paths = [p for p in paths if p.exists()]
    if not paths:
        return None
    rows, cols = [], []
    for p in paths:
        for r in csv.DictReader(open(p)):
            rows.append(r)
            for k in r:
                if k not in cols:
                    cols.append(k)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, restval="")
        w.writeheader()
        w.writerows(rows)
    return out


def metrics(csv_path: Path | None, name: str, folder: Path, videos: bool) -> None:
    if csv_path is None:
        print(f"!! no episodes for {name}")
        return
    subprocess.run([PY, PM, "metrics", "--csv", str(csv_path), "--name", name, "--out", str(folder)]
                   + (["--videos"] if videos else []), check=True)


def compare(runs: list[tuple[str, Path | None]], out: Path) -> None:
    runs = [(n, p) for n, p in runs if p is not None]
    if len(runs) >= 2:
        subprocess.run([PY, PM, "compare", *sum((["--csv", f"{n}={p}"] for n, p in runs), []), "--out", str(out)],
                       check=True)


def main() -> int:
    agg = LE / "pres-aggregate"
    # 01 walkers
    f1 = PE / "01_walkers"
    clips = sorted((LE / "pres-walkers").glob("*.mp4"))
    for c in clips:
        link(c, f1 / c.name)
    print(f"01: {len(clips)} walker clips")
    # 02 single robot
    f2 = PE / "02_anymal_single_robot_push"
    n = 0
    for m in MASSES:
        for v in sorted((LE / f"pres-solo-{m}kg" / "pair" / "videos").glob("*.mp4")):
            link(v, f2 / f"{m}kg" / v.name)
            n += 1
    solo = concat([LE / f"pres-solo-{m}kg" / "pair" / "episodes.csv" for m in MASSES], agg / "solo_episodes.csv")
    metrics(solo, "ANYmal single-robot pusher (s2b-anymal-term80)", f2, videos=True)
    print(f"02: {n} videos")
    # 03 / 04 pairs: videos moved from folder 12
    f12 = PE / "12_pairs_all_objects"
    f3, f4 = PE / "03_anymal_ippo_pair", PE / "04_anymal_mappo_pair"
    for algo, dst in (("ippo", f3), ("mappo", f4)):
        dst.mkdir(parents=True, exist_ok=True)
        for v in sorted(f12.glob(f"{algo}_*.mp4")) if f12.exists() else []:
            shutil.move(str(v), str(dst / v.name))
    if f12.exists() and not any(f12.iterdir()):
        f12.rmdir()
    ippo = LE / "pres-ippo" / "pair" / "episodes.csv"
    mappo = LE / "pres-mappo" / "pair" / "episodes.csv"
    ippo = ippo if ippo.exists() else None
    mappo = mappo if mappo.exists() else None
    metrics(ippo, "ANYmal IPPO pair (ippo_aa_kl_ten_s0, iteration 4000)", f3, videos=False)
    metrics(mappo, "ANYmal MAPPO pair (nwB_mappo_uniform_s0, iteration 5000)", f4, videos=False)
    compare([("Single robot", solo), ("IPPO", ippo)], f3 / "comparison.md")
    compare([("Single robot", solo), ("IPPO", ippo), ("MAPPO", mappo)], f4 / "comparison.md")
    # 05 planner
    f5 = PE / "05_contact_planner"
    n = 0
    for m in MASSES:
        for v in sorted((LE / f"pres-planner-{m}kg-expert" / "pair" / "videos").glob("*.mp4")):
            link(v, f5 / f"{m}kg" / v.name)
            n += 1
    plan = concat([LE / f"pres-planner-{m}kg-expert" / "pair" / "episodes.csv" for m in MASSES], agg / "planner_episodes.csv")
    metrics(plan, "Contact planner (expert rule + turn_debug executor)", f5, videos=True)
    allr = [("Single robot", solo), ("IPPO", ippo), ("MAPPO", mappo), ("Contact planner", plan)]
    compare(allr, f5 / "comparison.md")
    compare(allr, PE / "comparison.md")
    print(f"05: {n} videos")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
