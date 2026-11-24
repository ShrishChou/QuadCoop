# Paper media

Figures for the paper: video stills and filmstrips of the set-up, object-map renders, an encoder diagram, and graphs.
Rebuild everything with `python scripts/paper_media.py` (CPU only). It reads the films in `presentation_export/` and
`presentation_videos/` and the numbers in `evals_present/` and `logs/evals/`.

- **Stills** are `.jpg`, taken from the evaluation films with the burned-in caption bar cropped off. Filmstrips show
  four moments of one episode, each stamped with its time.
- **Graphs** come as `.png` (200 dpi) and `.pdf` (vector, for LaTeX).
- **Robot colours:** all teams are ANYmal unless named; Spot is yellow.
- **Contact markers in planner films:**
  - posts and arrows mark the assigned contacts (cyan = robot 1, yellow = robot 2, magenta = robot 3, orange = robot 4);
  - a ball above each robot shows which robot it is;
  - the green patch is the goal pose.

## intro: one, two, three and four robots on the same task

One frame from real evaluation films for each team size, all on the same task: the **cube at 80 kg, goal 3 m
straight ahead** (the green square). Rebuild with `python scripts/paper_media.py intro`.

| panel | source | moment shown |
|---|---|---|
| 1 robot | the single-robot push policy with the object-map CNN (`02_anymal_single_robot_push`) | mid-push; this run succeeds |
| 2 robots | the contact planner's pair (`05_contact_planner`) | both robots on the cube; the arrows above them are the planner's assigned push directions; this run succeeds |
| 3 robots | one branched contact-planner run (`3_vs_4_robots/80kg/cube_80kg_A_straight_r2`), left panel: the trio continues | 26 s into the episode, robots 1 and 2 pushing; this branch succeeds at 49.6 s |
| 4 robots | the same run and the same instant, right panel: robot 4 (orange ball) called at 20 s | robots 2, 3 and 4 pushing, robot 1 at its contact; this branch times out 0.08 m short |

| file | use |
|---|---|
| `intro_1_2_3_4_robots_cube_80kg_row.png/.jpg/.pdf` | 1 × 4 strip, for a full-width figure under the title |
| `intro_1_2_3_4_robots_cube_80kg_grid.png/.jpg/.pdf` | 2 × 2, for a single column |
| `<n>_robot(s)_cube_80kg.jpg` | each panel alone, unlabelled (900 × 675) |

- **Crops:** set by eye to show the team, the cube and the goal, with a robot about a fifth of the panel wide.
  The single-robot and pair films are 1080p; the branched film is 960 × 720 per panel, so panels 3 and 4 are a
  little softer.
- **Markers:** the coloured balls and arrows in panels 2–4 are the planner's markers (see the top of this file).

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
| `single_anymal_objects_grid.jpg` | one ANYmal pushing six objects: cube, sphere, cylinder, dumbbell, L shape, U channel (all successes, 40–80 kg) |
| `single_anymal_cube_60kg_far_turn_strip.jpg` | cube, 60 kg, 5 m with a 90° turn |
| `single_anymal_t_shape_80kg_backright_strip.jpg` | T shape, 80 kg, goal behind on the right (the robot goes around) |
| `single_anymal_sphere_80kg_far_turn_strip.jpg` | sphere, 80 kg, far turn |
| `single_anymal_arch_40kg_strip.jpg` | arch, 40 kg, goal behind on the right |

### 02_single_robot/start_positions: where the single robot starts

Rendered in MuJoCo, without a GPU (`python scripts/paper_media.py starts`). Each picture uses the single-robot benchmark's
geometry (`pres-solo-*`, `eval_coop2.py --solo anymal1`):
- the object is at the origin;
- ANYmal stands behind it, 145° from the object's forward direction (35° to the left of straight behind);
- its body centre is (object reach radius + 0.55 m + gap) from the object's centre, and it faces the object.

Per trial, the bearing is jittered by ±10° and the gap is 0.3–0.6 m. The **blue band** under the robot shows that
range, and the robot stands at its middle. The **green copy** is the goal pose, and the **dashed line** runs from the
object to the goal. The turn is capped by the object's symmetry, as in the benchmark: for example, 81° for the long
box and 36° for the cube.

| file | shows |
|---|---|
| `single_robot_start_positions.png/.jpg` | the four scenarios on the T shape. A: goal 3 m ahead. B: 3 m at 60° left, turned +30°. C: 3 m at 135° right, turned −60° (the robot has to walk around). D: 5 m ahead, turned 90°. |
| `single_robot_start_<scenario>.png` | each scenario alone, 1200 × 900 |
| `single_robot_start_A_all_objects.png/.jpg` | scenario A for all twelve objects: the start distance grows with the object's reach radius |
| `single_robot_start_A_<object>.png` | each object alone |

## 03_ippo_mappo: learned pairs

All films are successes at 80 kg unless noted.

| file | shows |
|---|---|
| `ippo_mappo_objects_grid.jpg` | MAPPO on the cylinder, dumbbell and plus; IPPO on the cube, sphere and L shape |
| `mappo_dumbbell_80kg_strip.jpg`, `mappo_pair_pushing.jpg` | MAPPO pair, dumbbell, straight ahead |
| `mappo_plus_80kg_left_strip.jpg` | MAPPO pair, plus, goal 60° left |
| `mappo_long_40kg_far_turn_strip.jpg` | MAPPO pair, long box at 40 kg, 5 m with a 90° turn |
| `ippo_cube_80kg_far_turn_strip.jpg` | IPPO pair, cube, far turn |
| `ippo_sphere_80kg_backright_strip.jpg` | IPPO pair, sphere, goal behind on the right |
| `ippo_l_shape_80kg_strip.jpg`, `ippo_pair_pushing.jpg` | IPPO pair, L shape |
| `frozen_pair_untrained_strip.jpg` | two single-robot policies placed side by side, never trained together |

## 04_contact_planner: two robots with the contact planner

| file | shows |
|---|---|
| `candidate_contacts_all_objects.png` (+ `_long`, `_arch`, `_cylinder`) | the planner's candidate contacts per object: arrows = push direction, faint box = robot standing there |
| `planner_objects_grid.jpg` | the planner at 80 kg on the cube, cylinder, sphere, L shape, plus and U channel (all successes) |
| `planner_dumbbell_80kg_far_turn_strip.jpg` | dumbbell, 80 kg, far turn |
| `planner_t_shape_80kg_backright_strip.jpg` | T shape, 80 kg, goal behind on the right |
| `planner_u_channel_80kg_left_strip.jpg` | U channel, 80 kg, goal 60° left |
| `planner_pair_contacts.jpg` | plus, 80 kg, far turn: posts and arrows on the assigned contacts |
| `planner_long_40kg_far_turn_strip.jpg` | the long box turned 90° on the way to a goal 5 m away |

## 05_teams_2_3_4: team size

Branch films are side by side and start at 16 s, 4 s before the 20 s decision. Strip times are episode times, and
every frame lies inside its own panel's episode. Every team clip was checked in its JSON to confirm that the added
robot actually joined. A requested robot does not join when the planner finds no feasible contact for it, and the
team then keeps its size. The previous four-robot strip (cube, 100 kg) was such a case: robot 4 never joined, so
only three robots appeared, and it has been replaced.

| file | shows |
|---|---|
| `team_sizes_2_3_4.jpg` | 2 robots (plus, 100 kg), 3 robots (sphere, 100 kg), 4 robots (cylinder, 40 kg) |
| `two_robots_plus_100kg_strip.jpg` / `three_robots_branch_plus_100kg_strip.jpg` | the same branched state: the pair continues (success at 45.9 s) vs robot 3 added at 20 s (success at 38.9 s) |
| `three_robots_cylinder_40kg_strip.jpg` / `four_robots_cylinder_40kg_strip.jpg` | the same branched state: stay at three (times out at 80 s) vs call robot 4 at 20 s (success at 27.1 s, no falls). This task is a rescue. Over all tasks, robot 4 does worse than staying at three (07_graphs). |
| `three_robots_sphere_100kg_strip.jpg`, `three_robots_u_channel_80kg_strip.jpg`, `three_robots_arch_80kg_strip.jpg`, `three_robots_dumbbell_80kg.jpg` | the planner with a helper (magenta), all successes |

## 06_online_learning: penalty after repeated failed pushes

Original planner (A) vs the penalty (B2), the same task:
- `*_long_80kg_turn60_strip.jpg`: the long box at 80 kg turned 60° in place, from the turning test. A keeps the same
  diagonal corners and times out. B2 penalises the pair after two failed windows; a robot moves to the long face, and
  the box turns.
- `*_l_shape_80kg_strip.jpg` (straight ahead) and `*_u_channel_40kg_strip.jpg` (goal behind on the right): from the
  ordinary benchmark. Tasks where the penalty acted and B2 succeeded while A did not.

## all_objects: one strip per object for every method

Each method folder has an `all_objects/` subfolder with one four-frame strip per object, plus contact sheets that stack
them with a label column (object, mass, scenario, and the outcome when it is not a success).

| method | folder | sheets | objects |
|---|---|---|---|
| one ANYmal, push policy | `02_single_robot/all_objects/` | `single_robot_all_objects{,_part1,_part2}.jpg` | 12, all successes |
| IPPO pair | `03_ippo_mappo/all_objects/ippo_*` | `ippo_all_objects*.jpg` | 12, all successes |
| MAPPO pair | `03_ippo_mappo/all_objects/mappo_*` | `mappo_all_objects*.jpg` | 12, all successes |
| contact planner, two robots | `04_contact_planner/all_objects/` | `planner_pair_all_objects*.jpg` | 12, all successes |
| contact planner, three robots (helper called at 8 s) | `05_teams_2_3_4/all_objects/three_robots_*` | `three_robots_all_objects*.jpg` | 12: 9 successes; T shape, beam and split-friction box time out |
| contact planner, four robots (three-vs-four branch, right panel) | `05_teams_2_3_4/all_objects/four_robots_*` | `four_robots_all_objects*.jpg` | 10: no four-robot run uses the beam or the split-friction box |

- `_part1` holds cube to dumbbell and `_part2` holds T shape to plus (six rows each, about one page). The full sheet has all twelve rows.
- **How each clip is chosen** (`build_library` in the script):
  - a success when one was filmed for that object;
  - masses in a fixed order per method: single robot 60 → 80 → 40 → 20 kg, pairs 80 → 40, planner 80 → 60 → 40 → 20, three robots 80 → 100;
  - the scenario order rotates by object, so the set covers all four starts.
- A failure is used only when no success exists. Its file name and row label say so (`_horizon` = timed out, `_fell` = a robot fell).
- **Frame times:**
  - single, pair and three-robot strips: 2%, 32%, 62% and 92% of the clip;
  - four-robot strips: episode 17.5 s (robot 4 has just been called at 20 s minus 4), 1 s after robot 4 reaches the object, midway, and 0.5 s before the four-robot episode ends.
  - Every four-robot frame is inside its episode.
- **Four-robot films** come from every three-vs-four tree filmed so far: `presentation_export/05_contact_planner/3_vs_4_robots` and `logs/evals/k4*`, 329 films.
  - A film counts only if robot 4 was called in (`t_add4` set).
  - Films where robot 4 reaches the object and presses at least 30% of the time are ranked first.
- **What the four-robot sheet shows,** and it is a result, not a selection artefact:
  - Robot 4 pushes on the cube, cylinder, arch, dumbbell and L shape.
  - On the T shape it reaches the object but presses only 18% of the time ("R4 barely pushed").
  - On the long box, sphere, U channel and plus, robot 4 was called in every filmed episode but never reached a contact ("R4 never at contact", `_r4_not_at_contact` in the file name). The other three robots do the pushing.
  - The cube strip is the intro film: four robots pushing, timed out 8 cm short.
- `paper_media/library_index.csv` lists each strip with its method, object, mass, scenario, outcome and source film.

Rebuild with `python scripts/paper_media.py library` (CPU only).

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
| `planner_time_limit_80_vs_140` | the planner benchmark at 80 s and 140 s (480 tasks, 2 runs each). 140 s lifts the original planner 62.3% → 71.8% and the penalty 62.4% → 74.8%, almost all at 60–80 kg. The penalty beats the original only at 140 s: +3.0 pp [+0.1, +6.0]. |
| `penalty_turning_test_all_arms` | every planner arm minus the original on the turning test (fresh placements, 160 tasks per bar), both turn directions. B2: +6.9 and +13.8 pp; one forced switch is weakest. |
| `team_size_placed_vs_walkin_{original,enlarged_1p5}` | the ten 3 → 4 place trees (5 seeds × 360 tasks per footprint). Four robots are 7 points below three at both sizes. Placing robot 4 at its contact instead of walking it in changes nothing (+0.8 and −0.3 pp). |
| `regret_contact_game_*` | the regret-minimisation contact game: learning curves and payoff examples |

## object: the twelve objects

Each object at nominal size (size factors 1.0), rendered in MuJoCo with its simulation colour. The camera is raised to a
three-quarter view: 45° between the object's x and y axes, looking down at 30°. The floor squares are 0.5 m. Each
camera is framed to its object, so compare sizes using the squares, not the tile.

| file | shows |
|---|---|
| `objects_grid.png` / `.jpg` | all twelve, 4 × 3 |
| `<name>.png` | one 900 × 900 render per object |

- Single-robot pusher training set: cube, long, sphere, cylinder, arch, dumbbell, T shape.
- Held out for it: beam, L shape, split-friction box, U channel, plus.
- The ten-object pairs and the contact-planner benchmarks use the first seven plus the L shape, U channel and plus.
- Split-friction box: two halves with friction 0.15 (light) and 0.9 (darkened in the render only).

Rebuild with `python scripts/paper_media.py objects`, which uses software EGL and needs no GPU.

Pending, to be added when the runs finish: the learned three- and four-robot teams, with and without the KL anchor (docs/marl_teams.md).
