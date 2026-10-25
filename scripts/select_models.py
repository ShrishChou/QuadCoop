"""Copy the models we use into models/ (git-ignored), so it is always clear which ones they are.

evals/models.yaml (committed) maps each role to a registered method id (evals/registry.yaml):

    walker_anymal: walker-anymal-v1
    walker_spot:   walker-spot-rai-falcon
    push2b_anymal: s2b-anymal-term80
    push2b_spot:   s2b-spot-falcon

This script copies each one's checkpoint (logs/evals/<id>/model.pt, the registered copy) and its
params/ folder to models/<role>/, and writes models/<role>/model.yaml (id, stage, task, walker,
env vars it needs, source checkpoint, SHA-256, note) and models/README.md (the table). The
originals stay where they are; models/ only ever holds copies.

    python scripts/select_models.py                          # copy everything in evals/models.yaml
    python scripts/select_models.py --set push2b_spot=s2b-spot-fs   # change a role, then copy
    python scripts/select_models.py --check                  # only report what is in models/
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import shutil
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from methods import EVALS, load, resolve  # noqa: E402

SELECTION = EVALS / "models.yaml"
OUT = ROOT / "models"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_selection() -> dict[str, str]:
    return yaml.safe_load(SELECTION.read_text()) or {}


def set_roles(pairs: list[str]) -> None:
    """Change roles in evals/models.yaml, keeping its comments for the other lines."""
    reg = load()
    lines = SELECTION.read_text().splitlines()
    for pair in pairs:
        role, _, mid = pair.partition("=")
        if not mid:
            raise SystemExit(f"--set expects role=id, got {pair!r}")
        if mid not in reg:
            raise SystemExit(f"{mid} is not registered (scripts/methods.py list)")
        for i, line in enumerate(lines):
            if line.split(":")[0].strip() == role and not line.lstrip().startswith("#"):
                lines[i] = f"{role}: {mid}"
                break
        else:
            lines.append(f"{role}: {mid}")
        print(f"evals/models.yaml: {role} -> {mid}")
    SELECTION.write_text("\n".join(lines) + "\n")


def copy_role(role: str, mid: str, reg: dict, sel: dict) -> dict:
    m = resolve(mid, reg)
    src = Path(m["checkpoint_abs"])
    if not src.exists():
        raise SystemExit(f"{role}: {src} not found (is {mid} registered on this machine?)")
    dst = OUT / role
    dst.mkdir(parents=True, exist_ok=True)
    old = dst / "model.yaml"
    if old.exists():
        prev = (yaml.safe_load(old.read_text()) or {}).get("id")
        if prev and prev != mid:
            print(f"{role}: replacing {prev} with {mid} (the original stays in logs/evals/{prev}/)")
    shutil.copy2(src, dst / "model.pt")
    if (src.parent / "params").is_dir():
        shutil.copytree(src.parent / "params", dst / "params", dirs_exist_ok=True)
    walker_role = next((r for r, i in sel.items() if i == m.get("walker")), None)
    info = {
        "role": role, "id": mid, "stage": m["stage"], "task": m["task"],
        **({"walker": m["walker"], "walker_role": walker_role} if m.get("walker") else {}),
        "env": m["env_all"], "source": m.get("source", ""), "registered": m.get("registered", ""),
        "sha256": sha256(dst / "model.pt"), "copied": dt.datetime.now().isoformat(timespec="seconds"),
        "note": m.get("note", ""),
    }
    (dst / "model.yaml").write_text(yaml.safe_dump(info, sort_keys=False, width=110))
    return info


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--set", nargs="+", default=[], metavar="ROLE=ID")
    ap.add_argument("--check", action="store_true", help="only list what models/ holds")
    a = ap.parse_args()
    if a.set:
        set_roles(a.set)
    sel = read_selection()
    if a.check:
        for role, mid in sel.items():
            f = OUT / role / "model.yaml"
            have = (yaml.safe_load(f.read_text()) or {}).get("id") if f.exists() else None
            state = "ok" if have == mid else (f"OUT OF DATE (has {have})" if have else "missing")
            print(f"{role:16s} {mid:28s} {state}")
        return 0
    reg = load()
    infos = [copy_role(role, mid, reg, sel) for role, mid in sel.items()]
    rows = ["# Models in use", "",
            "Copied by `scripts/select_models.py` from the roles in `evals/models.yaml`; do not edit by hand.", "",
            "| role | id | stage | task | walker | env | note |", "|---|---|---|---|---|---|---|"]
    for i in infos:
        env = ", ".join(f"{k}={v}" for k, v in i["env"].items())
        rows.append(f"| {i['role']} | {i['id']} | {i['stage']} | {i['task']} | {i.get('walker', '')} | {env} | {i['note']} |")
    (OUT / "README.md").write_text("\n".join(rows) + "\n")
    print("\n".join(rows[4:]))
    print(f"\ncopied {len(infos)} models to {OUT}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
