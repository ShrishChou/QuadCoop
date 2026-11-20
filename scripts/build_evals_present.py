"""Collect the evaluations that matter into evals_present/ under readable names (the stats only: summary.md/json,
episodes.csv, figures; videos stay in presentation_export/ and logs/evals/). Sources are copied from evals/<id>/eval/
(and a few files from logs/evals/ and presentation_export/); evals/ itself is not changed. Safe to re-run.

    python scripts/build_evals_present.py

The layout and the source of every folder are listed in evals_present/README.md (written by hand; this script only
copies). A source that does not exist yet is reported and skipped.
"""
from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EV, LE, PE = ROOT / "evals", ROOT / "logs" / "evals", ROOT / "presentation_export"
OUT = ROOT / "evals_present"

# (destination under evals_present/, source eval id under evals/)
MAP = [
    # 1. walkers (Stage 0 gate: walk, resist a push, push a 15 kg box)
    ("01_walkers/anymal_v1", "walker-anymal-v1"),
    ("01_walkers/spot_v1_kp500", "walker-spot-v1"),
    ("01_walkers/spot_rai_gains", "walker-spot-rai"),
    ("01_walkers/spot_rai_falcon", "walker-spot-rai-falcon"),
    # 2. single-robot push (the policy used from then on: Stage 2b, map + CNN)
    ("02_single_robot_push/anymal_s2b_map_term80", "s2b-anymal-term80"),
    ("02_single_robot_push/spot_s2b_map_falcon", "s2b-spot-falcon"),
    ("02_single_robot_push/benchmark_anymal_20kg", "pres-solo-20kg"),
    ("02_single_robot_push/benchmark_anymal_40kg", "pres-solo-40kg"),
    ("02_single_robot_push/benchmark_anymal_60kg", "pres-solo-60kg"),
    ("02_single_robot_push/benchmark_anymal_80kg", "pres-solo-80kg"),
    # 3. perception: object map read by a CNN (2b) vs no map (2ctrl, 42 inputs)
    ("03_cnn_object_map/anymal_map_cnn", "s2b-anymal"),
    ("03_cnn_object_map/anymal_no_map", "s2ctrl-anymal"),
    ("03_cnn_object_map/anymal_map_cnn_term80", "s2b-anymal-term80"),
    ("03_cnn_object_map/anymal_no_map_term80", "s2ctrl-anymal-term80"),
    ("03_cnn_object_map/spot_map_cnn", "s2b-spot"),
    ("03_cnn_object_map/spot_no_map", "s2ctrl-spot"),
    ("03_cnn_object_map/spot_map_cnn_falcon", "s2b-spot-falcon"),
    ("03_cnn_object_map/spot_no_map_falcon", "s2ctrl-spot-falcon"),
    # 4. learned cooperation
    ("04_mappo_ippo/benchmark480_ippo_it5000", "nw-A-ippo-uniform-it5000-dev7100"),
    ("04_mappo_ippo/benchmark480_mappo_it5000", "nw-B-mappo-uniform-it5000-dev7100"),
    ("04_mappo_ippo/presentation_ippo_it4000", "pres-ippo"),
    ("04_mappo_ippo/presentation_mappo_it5000", "pres-mappo"),
    ("04_mappo_ippo/early_ippo_kl_it3000", "ippo-aa_kl-s0-it3000"),
    ("04_mappo_ippo/early_mappo_kl_it3000", "mappo-aa_kl-s0-it3000"),
    ("04_mappo_ippo/obs_study_A_baseline", "obs-A-base-s0-it7000-dev7100"),
    ("04_mappo_ippo/obs_study_B_contact_geometry", "obs-B-geom-s0-it7000-dev7100"),
    ("04_mappo_ippo/obs_study_C_history", "obs-C-hist-s0-it7000-dev7100"),
    ("04_mappo_ippo/obs_study_D_geometry_history", "obs-D-geom_hist-s0-it7000-dev7100"),
    # 5. KL regularization toward the single-robot policy
    ("05_kl_regularization/mappo_kl_0_none", "mappo-aa_nokl-s0-it3000"),
    ("05_kl_regularization/mappo_kl_0.02", "mappo-aa_kl002-s0-it3000"),
    ("05_kl_regularization/mappo_kl_0.05_seed0", "mappo-aa_kl-s0-it3000"),
    ("05_kl_regularization/mappo_kl_0.05_seed1", "mappo-aa_kl-s1-it3000"),
    ("05_kl_regularization/mappo_kl_0.2", "mappo-aa_kl02-s0-it3000"),
    ("05_kl_regularization/anchor_kept_A_baseline", "obs-A-base-s0-it7000-dev7100"),
    ("05_kl_regularization/anchor_kept_B_geometry", "obs-B-geom-s0-it7000-dev7100"),
    ("05_kl_regularization/anchor_removed_A_baseline", "obs-Ar2-base-s0-it7000-dev7100"),
    ("05_kl_regularization/anchor_removed_B_geometry", "obs-Br2-geom-s0-it7000-dev7100"),
    # 6. contact planner + executor
    ("06_contact_planner/benchmark_20kg", "pres-planner-20kg-expert"),
    ("06_contact_planner/benchmark_40kg", "pres-planner-40kg-expert"),
    ("06_contact_planner/benchmark_60kg", "pres-planner-60kg-expert"),
    ("06_contact_planner/benchmark_80kg", "pres-planner-80kg-expert"),
    ("06_contact_planner/readme_current_system", "turn_debug-fair-expert"),
    # 7. regret minimization
    ("07_regret_minimization/contact_game", "game-hvB-game"),
    ("07_regret_minimization/subgoal_train_pass1", "sg-train-s1001"),
    ("07_regret_minimization/subgoal_train_pass2", "sg-train-s1002"),
    ("07_regret_minimization/subgoal_train_pass3", "sg-train-s1003"),
    ("07_regret_minimization/subgoal_fixed_direct", "sg-fixed-direct-dev7100"),
    ("07_regret_minimization/subgoal_fixed_straight_cmu", "sg-fixed-straight-dev7100"),
    ("07_regret_minimization/subgoal_fixed_translate", "sg-fixed-translate-dev7100"),
    ("07_regret_minimization/subgoal_fixed_rotate", "sg-fixed-rotate-dev7100"),
    ("07_regret_minimization/subgoal_fixed_arc_left", "sg-fixed-arc_left-dev7100"),
    ("07_regret_minimization/subgoal_fixed_arc_right", "sg-fixed-arc_right-dev7100"),
    ("07_regret_minimization/subgoal_frozen", "sg-frozen-dev7100"),
    ("07_regret_minimization/subgoal_online", "sg-online-dev7100"),
]
# whole-folder presentation metrics (system comparison across objects / weights)
PRES = [("00_overview/comparison_all_systems.md", "comparison.md"),
        ("02_single_robot_push/benchmark_metrics.md", "02_anymal_single_robot_push/metrics.md"),
        ("02_single_robot_push/benchmark_metrics_by_case.csv", "02_anymal_single_robot_push/metrics_by_case.csv"),
        ("04_mappo_ippo/presentation_ippo_metrics.md", "03_anymal_ippo_pair/metrics.md"),
        ("04_mappo_ippo/presentation_mappo_metrics.md", "04_anymal_mappo_pair/metrics.md"),
        ("06_contact_planner/benchmark_metrics.md", "05_contact_planner/metrics.md"),
        ("06_contact_planner/benchmark_metrics_by_case.csv", "05_contact_planner/metrics_by_case.csv")]
SKIP = {"videos"}


def copy_tree(src: Path, dst: Path) -> int:
    n = 0
    for p in src.rglob("*"):
        if p.is_dir() or any(part in SKIP for part in p.relative_to(src).parts) or p.suffix in (".mp4", ".pt", ".npz"):
            continue
        q = dst / p.relative_to(src)
        q.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, q)
        n += 1
    return n


def main() -> int:
    missing = []
    for dst, sid in MAP:
        src = EV / sid / "eval" if (EV / sid / "eval").is_dir() else EV / sid
        if not src.is_dir():
            missing.append(sid)
            continue
        d = OUT / dst
        if d.exists():
            shutil.rmtree(d)
        n = copy_tree(src, d)
        planner = LE / sid / "pair" / "subgoal_planner.md"  # the learned strategy (regret planner runs)
        if planner.exists():
            shutil.copy2(planner, d / "subgoal_planner.md")
        (d / "SOURCE.txt").write_text(f"evals/{sid}\n")
        print(f"{dst:60s} <- evals/{sid} ({n} files)")
    for dst, src in PRES:
        if (PE / src).exists():
            (OUT / dst).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(PE / src, OUT / dst)
        else:
            missing.append(f"presentation_export/{src}")
    if missing:
        print("not there yet (skipped):", ", ".join(missing))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
