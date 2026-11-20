# QuadCoop: evaluations worth keeping

A curated copy of the evaluations behind the project's results, under readable names. Stats only (`summary.md`,
`summary.json`, `episodes.csv`, figures); videos are in `presentation_export/`. Each folder's `SOURCE.txt` names the
original under `evals/`. Rebuild with `python scripts/build_evals_present.py` (it copies; `evals/` is untouched).

Success everywhere = the object held at the goal pose (10 cm / 6 deg for 1 s unless a suite says otherwise).

## 00_overview

`comparison_all_systems.md`: single robot, IPPO, MAPPO and the contact planner on the same tasks (12 objects x
4 start positions x 10 trials at 20 / 40 / 60 / 80 kg), success and time per object and weight.

| | 20 kg | 40 kg | 60 kg | 80 kg | all |
|---|---|---|---|---|---|
| single robot | 89% | 64% | 25% | 11% | 47% |
| IPPO pair | 90% | 82% | 53% | 24% | 62% |
| MAPPO pair | 90% | 78% | 53% | 24% | 61% |
| contact planner | 72% | 67% | 50% | 33% | 56% |

## 01_walkers

The frozen low-level walkers (Stage 0 gate: A walk, B resist a 25% body-weight push, C push a 15 kg box).

| folder | A falls / vx err | B falls / speed kept | C falls / moved | gate |
|---|---|---|---|---|
| `anymal_v1` (used by every ANYmal stage) | 0% / 0.04 | 0% / 50% | 0% / 3.30 m | pass |
| `spot_v1_kp500` | 0% / 0.04 | 15% / 32% | 0% / 3.21 m | fail |
| `spot_rai_gains` (real-robot gains) | 0% / 0.04 | 5% / 51% | 0% / 3.19 m | fail |
| `spot_rai_falcon` (+ adaptive push curriculum, history; used by Spot) | 0% / 0.05 | 0% / 72% | 0% / 3.96 m | pass |

## 02_single_robot_push

The single-robot pusher (Stage 2b: velocity commands to the walker, object map read by a CNN).

- `anymal_s2b_map_term80`, `spot_s2b_map_falcon`: the method suites (seen / unseen shapes at 10 / 25 / 40 kg;
  suites `h80`, `precise`, `standard`). ANYmal 0.79 overall (h80), Spot 0.71.
- `benchmark_anymal_<mass>kg` + `benchmark_metrics.md` / `_by_case.csv`: the same ANYmal policy on the shared
  benchmark (the "single robot" row above; per object, position, failure notes).

## 03_cnn_object_map

The perception study: the pusher with a 32 x 32 top-down object map read by a CNN (`map_cnn`, Stage 2b) against
the same pusher without it (`no_map`, Stage 2ctrl, 42 inputs). Suite h80, success overall and on unseen shapes at
40 kg:

| | map + CNN | no map |
|---|---|---|
| ANYmal | 0.76 (unseen 40 kg 0.57) | 0.73 (0.47) |
| ANYmal, continued (term80) | 0.79 (0.55) | 0.73 (0.48) |
| Spot | 0.61 (0.34) | 0.56 (0.26) |
| Spot, rai-falcon walker | 0.71 (0.39) | 0.53 (0.14) |

The map matters most on unseen shapes and heavy objects. No lidar evaluations exist: the robots perceive the object
and partner only through these maps (the pair adds a partner map, `--partner-map`).

## 04_mappo_ippo

- `benchmark480_ippo_it5000`, `benchmark480_mappo_it5000`: the main 480-task benchmark (10 training shapes x 4
  positions x 3 reps x 20-80 kg, seed 7100): both 66%.
- `presentation_*`: the same policies on the 12-object presentation benchmark (+ metrics.md).
- `early_*_kl_it3000`: the first pair runs (iteration 3000; 576 tasks): IPPO 60%, MAPPO 58%.
- `obs_study_A`-`D` (docs/obs_study.md): MAPPO with extra inputs, +2000 iterations from the benchmark policy:
  baseline 65%, contact geometry 65%, interaction history 64%, both 65%. No input helped.

## 05_kl_regularization

The pair policies are kept close to the single-robot pusher by a KL penalty (weight `kl_ref`). MAPPO, iteration
3000, 576 tasks:

| KL weight | success | 20 / 40 / 60 / 80 kg | episodes with a fall |
|---|---|---|---|
| 0 (none) | 35% | 58 / 47 / 24 / 10 | 23% |
| 0.02 | 56% | 89 / 67 / 49 / 19 | 14% |
| **0.05** (used) | 58% (seed 1: 59%) | 88 / 76 / 47 / 20 | 16% |
| 0.2 | 50% | 74 / 60 / 42 / 22 | 34% |

And removing the anchor after training with it (observation study round 2, the KL weight faded to 0 over 1000
iterations, 480-task benchmark): baseline 65% -> 23%, geometry 65% -> 30%. Without the anchor the pair forgets how to
push; too strong an anchor (0.2) stops it adapting.

## 06_contact_planner

- `benchmark_<mass>kg` + `benchmark_metrics.md`: the planner (expert rule + `turn_debug` executor) on the shared
  benchmark ("contact planner" row above).
- `readme_current_system`: the evaluation behind the README's Step 4 table (0.67 / 0.67 / 0.57 / 0.38).

## 07_regret_minimization (docs/subgoal_planner.md)

- `contact_game`: Step 1, the contact game. Independent regret learners (regret matching, RM+, Hedge) pick contact
  pairs that score 0.32 on fresh placements against 0.20 for the hand-made rules; Exp3 (bandit feedback) finds the
  best pair in only 52% of runs.
- `subgoal_*`: Step 2, the Exp3 subgoal planner over the MAPPO pair. `train_pass1-3`: learning on training
  placements (64 / 60 / 63%); `fixed_<arm>`: each subgoal move alone on the benchmark (`fixed_direct` = the pair on
  its own, 64%; `fixed_straight_cmu` = CMU-style intermediate goals); `frozen` / `online`: the trained planner.
  `subgoal_planner.md` in each run shows the learned strategy per situation. Folders appear as the runs finish.
