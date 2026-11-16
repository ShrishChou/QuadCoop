"""Copy the chosen HD renders (slurm/render_presentation.sbatch) into presentation_export/hd/, in talk order, with
the outcome in each name, and write the index (README.md) with the numbers and findings behind each clip.

    python scripts/collect_presentation.py          # missing renders are listed, not fatal
"""
from __future__ import annotations

import csv
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "presentation_export" / "hd"
LE = ROOT / "logs" / "evals"


def first(pattern: str, base: Path = ROOT) -> Path | None:
    hits = sorted(base.glob(pattern))
    return hits[0] if hits else None


def outcome_from_name(p: Path) -> str:
    stem = p.stem
    if "__" not in stem:
        return ""
    oc = stem.split("__")[-1]
    return {"horizon": "fail_timeout"}.get(oc, oc if oc == "success" else f"fail_{oc}")


def outcome_from_csv(csv_path: Path, **match) -> str:
    if not csv_path.exists():
        return ""
    for r in csv.DictReader(open(csv_path)):
        if all(str(r.get(k)) == str(v) for k, v in match.items()):
            return "success" if r["success"] == "1" else ("fail_fell" if r.get("fell") == "1" else "fail_timeout")
    return ""


# (folder, clip name, source glob relative to the repo, outcome source: "name" | (csv, match) | None)
PICKS = []
for robot, mid in (("anymal", "walker-anymal-v1"), ("spot", "walker-spot-rai-falcon")):
    v = f"logs/evals/hd-{mid}/videos"
    PICKS += [("01_walkers", f"{robot}_walk", f"{v}/A_track*.mp4", None),
              ("01_walkers", f"{robot}_resists_push", f"{v}/B_resist*.mp4", None),
              ("01_walkers", f"{robot}_walks_into_cube_30kg", f"{v}/C_obj_cube_30kg_0deg*.mp4", None)]
for robot, mid in (("anymal", "s2b-anymal-term80"), ("spot", "s2b-spot-falcon")):
    for scen, nm in (("A_straight", "straight"), ("C_backright", "around_behind")):
        PICKS.append(("02_single_robot_push", f"{robot}_push_long_40kg_{nm}", f"eval_videos/hd-{mid}/long/40kg/{scen}__*.mp4",
                      "name"))
COOP = (("1_anymal_alone", "hd-anymal-alone", ("80kg_A_straight",)),
        ("2_frozen_pair", "hd-frozen-pair", ("80kg_A_straight",)),
        ("3_ippo_anymal_pair", "hd-ippo-anymal-pair", ("80kg_A_straight", "40kg_D_far_turn")),
        ("4_mappo_anymal_pair", "hd-mappo-anymal-pair", ("80kg_A_straight", "40kg_D_far_turn")),
        ("5_mappo_anymal_spot", "hd-mappo-anymal-spot", ("80kg_A_straight",)),
        ("6_ippo_spot_pair", "hd-ippo-spot-pair", ("80kg_A_straight",)))
for nm, ev, tasks in COOP:
    for t in tasks:
        PICKS.append(("03_coordination", f"{nm}_long_{t.replace('_A_straight', '_straight').replace('_D_far_turn', '_far_turn')}",
                      f"logs/evals/{ev}/pair/videos/long_{t}_*.mp4", "name"))
for t in ("40kg_A_straight", "40kg_D_far_turn", "80kg_A_straight", "80kg_D_far_turn"):
    PICKS.append(("04_contact_planner", f"planner_long_{t.replace('_A_straight', '_straight').replace('_D_far_turn', '_far_turn')}",
                  f"logs/evals/hd-planner-expert/pair/videos/long_{t}_*.mp4", "name"))
tr = ROOT / "evals" / "hd-sa-transport" / "episodes.csv"
for mode, nm in (("both", "arms_active"), ("none", "arms_locked"), ("solo_1", "partner_parked")):
    PICKS.append(("05_spot_arm", f"transport_turn60_{nm}", f"logs/evals/hd-sa-transport/left_{mode}.mp4",
                  (tr, dict(turn="left", rep=0, swap=0, arm_mode=mode))))
for d, cond, nm in (("hd-sa-turn-stowed", "stowed", "learned_trunk"), ("hd-sa-turn-bc", "both_hands", "learned_from_demos"),
                    ("hd-sa-turn-script", "both_hands", "scripted_hands")):
    for turn in ("ccw", "cw"):
        PICKS.append(("05_spot_arm", f"turn_in_place_{nm}_{turn}", f"logs/evals/{d}/{cond}_{turn}.mp4",
                      (LE / d / "episodes.csv", dict(cond=cond, turn=turn, rep=0, swap=0))))

README = """# QuadCoop presentation clips (HD)

1920x1080, rendered by `slurm/render_presentation.sbatch` (see `src/quadcoop/render_hd.py`) with each stage's best
checkpoint; captions are burned in. File names end in the episode's outcome where one is defined
(`success`, `fail_timeout`, `fail_fell`). Re-render any stage: `STAGES="<stage>" sbatch slurm/render_presentation.sbatch`.

## 01_walkers: the frozen walking policies every team uses
ANYmal C (`walker-anymal-v1`) and Spot (`walker-spot-rai-falcon`): walking on command, resisting a push of 25% of
body weight, walking into a 30 kg cube.

## 02_single_robot_push: one robot, one object (Stage 2b push policies)
ANYmal `s2b-anymal-term80`, Spot `s2b-spot-falcon`; long object, 40 kg, straight 2.5 m and around-behind (135 deg).
On the 480-task benchmark: ANYmal alone 52.4%, Spot alone 40.7%.

## 03_coordination: two robots, the 480-task benchmark's long object (40 / 80 kg)
| clip prefix | system | benchmark success |
|---|---|---|
| 1_anymal_alone | one ANYmal, partner parked | 52.4% |
| 2_frozen_pair | two single-robot policies, never trained together | 46.2% |
| 3_ippo_anymal_pair | IPPO, trained together (`ippo_aa_kl_ten_s0`) | 65.6% |
| 4_mappo_anymal_pair | MAPPO (`nwB_mappo_uniform_s0`) | 65.3% |
| 5_mappo_anymal_spot | MAPPO, ANYmal + Spot (`mappo_mx_kl_ten_s0`) | 62.1% |
| 6_ippo_spot_pair | IPPO, Spot + Spot (`ippo_ss_kl_ten_s0`) | 58.5% |

Findings:
- An untrained pair does worse than one robot: the partners get in each other's way.
- Joint training lifts every team by 16-29 points; the gain is at 60-80 kg (ANYmal: 32% alone -> about 60% as a
  pair at 60 kg), not at 20-40 kg where one robot already succeeds.
- IPPO and MAPPO end within about 2 points of each other on every team.
- The trained pairs start from the single-robot push policies and are held near them by a KL anchor during
  joint training.

## 04_contact_planner: planner + learned executor (ANYmal pair), long object
Successes and failures on the same four tasks as 03.

## 05_spot_arm: two Spots with arms (RAI walker)
- `transport_*`: 1 m, 20 kg long object, goal turned 60 deg. Arms active 99.2%, arms locked 99.2%, either robot
  alone 0%: the task needs both robots but not the arms (arm contact under 1%).
- `turn_in_place_*`: 20 kg long object, centre held at the goal, turned 40 deg clockwise (cw) / counter-clockwise
  (ccw); one robot starts behind it and one in front.
  - scripted_hands: a scripted two-hand maneuver, 78% (trunk-only script 25%, one robot 0%);
  - learned_trunk: MAPPO with arms stowed, 100%, one robot alone 0%;
  - learned_from_demos: MAPPO initialised from the scripted hand demonstrations, 97%. It drops the hands (hand
    contact 1-2%) and pushes with the trunk, like the stowed policy.
  The learned pairs find a two-sided trunk couple that beats the scripted hand maneuver; the arm adds nothing.
"""


def main() -> int:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    missing = []
    for folder, name, pattern, oc_src in PICKS:
        src = first(pattern)
        if src is None:
            missing.append(pattern)
            continue
        oc = outcome_from_name(src) if oc_src == "name" else outcome_from_csv(*oc_src[:1], **oc_src[1]) if oc_src else ""
        dst = OUT / folder / (f"{name}__{oc}.mp4" if oc else f"{name}.mp4")
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    (OUT / "README.md").write_text(README)
    n = len(PICKS) - len(missing)
    size = sum(p.stat().st_size for p in OUT.rglob("*.mp4")) / 1e6
    print(f"{n} clips ({size:.0f} MB) -> {OUT}")
    for m in missing:
        print(f"  missing: {m}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
