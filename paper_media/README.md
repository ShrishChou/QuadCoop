# Paper media

Figures for the paper: video stills and filmstrips of the set-up, object-map renders, an encoder diagram, and graphs.
Rebuild everything with `python scripts/paper_media.py` (CPU only). It reads the films in `presentation_export/` and
`presentation_videos/` and the numbers in `evals_present/` and `logs/evals/`.

- **Stills** are `.jpg`, taken from the evaluation films with the burned-in caption bar cropped off. Filmstrips show
  four moments of one episode, each stamped with its time.
- **Graphs** come as `.png` (200 dpi) and `.pdf` (vector, for LaTeX).
- **Robot colours:** all teams are ANYmal unless named; Spot is yellow.
- **Contact markers in planner films:**
  - posts and arrows mark the assigned contacts (cyan = robot 1, yellow = robot 2, magenta = robot 3);
  - a ball above each robot shows which robot it is;
  - the green patch is the goal pose.

## 01_robots_walkers: the robots and the frozen walkers

The walker frames are 1080p renders with no captions.

| file | shows |
|---|---|
| `robots_side_by_side.jpg` | ANYmal (left) and Spot (right) under their walking policies |
| `anymal_walking.jpg`, `spot_walking.jpg`, `anymal_walk_strip.jpg` | velocity tracking |
| `anymal_resisting_push.jpg` | ANYmal recovering from a 25% body-weight shove (Stage 0 gate B) |
| `anymal_walker_into_30kg_cube*.jpg`, `spot_walker_into_30kg_cube.jpg`, `anymal_cube_push_strip.jpg` | the walker alone driven into a 30 kg cube, with no push policy |
| `parallel_training_envs*.jpg` | the massively parallel training scene (hundreds of robots and objects simulated together) |

## 02_single_robot: the pusher and its object-map CNN

| file | shows |
|---|---|
| `object_maps_top.png/.pdf` | the 12 objects' top-down maps: signed distance on a 32 × 32 grid over 3.6 × 3.6 m, in the body-height slice (0.12–0.75 m). The arch shows only its pillars: its bar is above the slice. "Held out" = not in the single-robot pusher's training set (the ten-object pairs train on the L shape, U channel and plus too). |
| `object_maps_robot_frame.png/.pdf` | what the deployed pusher sees: the same slice on a 4 × 4 m grid around the robot, forward up, with the robot drawn in green |
| `object_maps_front.png` | the front silhouettes (16 × 32: height by lateral position), the second CNN input |
| `cnn_push_policy_architecture.png/.pdf` | the encoder from `src/quadcoop/stage2/rl_cfg.py`: top map → conv 5×5/2 (16) → 3×3/2 (32) → 3×3/2 (16) → 256; front map → the same layers → 128; joined with 42 state inputs in an MLP (256-128-64) that outputs the velocity command to the frozen walker |
| `single_anymal_arch_40kg*.jpg` | one ANYmal pushing the arch, 40 kg (success) |

## 03_ippo_mappo: learned pairs

| file | shows |
|---|---|
| `frozen_pair_untrained_strip.jpg` | two single-robot policies placed side by side, never trained together |
| `mappo_long_80kg_strip.jpg`, `mappo_pair_pushing.jpg` | MAPPO pair, long object, 80 kg (success) |
| `mappo_long_40kg_far_turn_strip.jpg` | MAPPO pair, 5 m with a 90° turn (success) |
| `ippo_l_shape_80kg_strip.jpg`, `ippo_pair_pushing.jpg` | IPPO pair, L shape, 80 kg (success) |

## 04_contact_planner: two robots with the contact planner

| file | shows |
|---|---|
| `candidate_contacts_all_objects.png` (+ `_long`, `_arch`, `_cylinder`) | the planner's candidate contacts per object: arrows = push direction, faint box = robot standing there |
| `planner_long_40kg_far_turn_strip.jpg`, `planner_pair_contacts.jpg` | the planner turning the long object 90° on the way to a goal 5 m away (success) |
| `planner_arch_80kg_far_turn_strip.jpg` | the arch at 80 kg, far turn (success) |

## 05_teams_2_3_4: team size

| file | shows |
|---|---|
| `team_sizes_2_3_4.jpg` | one still each of 2, 3 and 4 robots |
| `two_robots_arch_80kg_strip.jpg` / `three_robots_branch_arch_80kg_strip.jpg` | the same branched state: the pair continues (left half of the branch film) vs robot 3 added (right half); both succeed |
| `three_robots_arch_80kg_strip.jpg`, `three_robots_arch_80kg.jpg` | the planner with a helper (magenta) on the arch, 80 kg (success) |
| `three_robots_cube_100kg_strip.jpg` / `four_robots_cube_100kg_strip.jpg` | the same branched state at 100 kg: stay at three vs call robot 4 at 20 s; both succeed (53 s vs 69 s). The four-robot strip shows the crowding at the faces. |

## 06_online_learning: penalty after repeated failed pushes

Long object, 80 kg, turned 60° in place (fresh placements):
- `original_planner_long_80kg_turn60_strip.jpg`: the original planner keeps the same diagonal corners. The object
  barely turns, and it times out.
- `penalty_planner_long_80kg_turn60_strip.jpg`: after two failed windows the pair is penalised. A robot moves to the
  long face, the object turns, and it succeeds.

## 07_graphs

| file | numbers |
|---|---|
| `success_vs_mass_all_systems` | 12 objects × 4 starts × 10 trials per mass, 80 s. Overall success: single robot 47%, IPPO 62%, MAPPO 61%, contact planner 56%. At 80 kg the planner leads (33% vs 24%). |
| `falls_vs_mass_all_systems` | share of episodes with a fall. The planner falls less than either learned pair at every mass (8% vs 22–24% at 60 kg). |
| `success_by_object_all_systems` | the same benchmark per object, mean of 20–80 kg |
| `cnn_object_map_vs_no_map` | the pusher with vs without the object map, ANYmal and Spot: all suites, and unseen shapes at 40 kg |
| `team_size_2_3_4_original` | the same branched states (5 seeds × 120 tasks per point): 2 robots 55.1%, 3 robots 65.1%, 4 robots 57.7% overall. Robot 3 helps from 80 kg; robot 4 does worse than staying at three at every mass. |
| `team_size_2_3_4_enlarged_1p5` | footprint × 1.5, the same design: 2 robots 26.6%, 3 robots 51.7%, 4 robots 45.7% |
| `penalty_benchmark_by_object` | the penalty on ordinary deliveries (480 tasks, 2 runs each): 62.3% vs 62.4%, no change overall |
| `penalty_turning_test` | turning in place on fresh placements (mirrored turns, 160 tasks): 72.5% → 86.2%, +13.8 pp [+6.9, +20.6] |
| `regret_contact_game_*` | the regret-minimisation contact game: learning curves and payoff examples |

Pending, to be added when the runs finish:
- the unmirrored half of the turning test;
- the 140 s benchmark;
- the 3 → 4 size and entry trees (placed vs walk-in robot 4).
