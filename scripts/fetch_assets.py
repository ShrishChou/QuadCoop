#!/usr/bin/env python3
"""Copy the two robot models into src/quadcoop/assets/ (run once, on a node with internet).

    python scripts/fetch_assets.py

* ANYmal C: the MJCF from mujocolab/anymal_c_velocity (Menagerie's model with named
  collision geoms, an IMU site and sensors), plus its meshes.
* Spot: Menagerie's boston_dynamics_spot as-is; robots/spot.py edits it in code.

Both repos are pinned to a commit so every machine gets identical models.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src" / "quadcoop" / "assets"

SOURCES = {
    "anymal_c": {
        "repo": "https://github.com/mujocolab/anymal_c_velocity.git",
        "commit": "248ee73af83ac466a525758469e653217cdc5322",
        "subdir": "src/anymal_c_velocity/anymal_c/xmls",
        "check": "anymal_c.xml",
    },
    "spot": {
        "repo": "https://github.com/google-deepmind/mujoco_menagerie.git",
        "commit": "62ab00f2bc44f6f20c1c9b7a13f3fb1dd41a4e35",
        "subdir": "boston_dynamics_spot",
        "check": "spot.xml",
    },
}


def fetch(name: str, repo: str, commit: str, subdir: str, check: str) -> None:
    dest = ASSETS / name
    if (dest / check).exists():
        print(f"  ok   {name}: already present at {dest}")
        return
    with tempfile.TemporaryDirectory() as tmp:
        clone = Path(tmp) / "repo"
        subprocess.run(
            ["git", "clone", "-q", "--filter=blob:none", "--sparse", "--no-checkout", repo, str(clone)],
            check=True,
        )
        subprocess.run(["git", "-C", str(clone), "sparse-checkout", "set", subdir], check=True)
        subprocess.run(["git", "-C", str(clone), "checkout", "-q", commit], check=True)
        src = clone / subdir
        if not (src / check).exists():
            sys.exit(f"  FAIL {name}: {check} not found in {repo}/{subdir}")
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(src, dest)
        (dest / "SOURCE.txt").write_text(f"{repo}\n{subdir}\ncommit {commit}\n")
    print(f"  ok   {name}: copied to {dest}")


def main() -> int:
    for name, src in SOURCES.items():
        fetch(name, **src)
    print("Assets ready.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
