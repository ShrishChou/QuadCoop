# Pair evaluation: coordcol-bc0-s100-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 12 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.81 | 0.70 | 0.01 | 0.01 | 26.5 | 0.00 | 0.40 | 0.37 | 0.13 | 0.24 | 1.40 |
| 40 kg | 0.74 | 0.60 | 0.01 | 0.01 | 34.8 | 0.00 | 0.46 | 0.40 | 0.12 | 0.19 | 1.41 |
| 60 kg | 0.52 | 0.40 | 0.01 | 0.01 | 39.2 | 0.00 | 0.55 | 0.45 | 0.20 | 0.27 | 1.39 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg |
|---|---|---|---|---|
| long | part 0 -x seg 2/2 + part 0 corner -x-y | 0.73 | 0.83 | 0.67 |
| arch | part 3 -x + part 2 -x | 0.88 | 0.81 | 0.52 |
| dumbbell | part 1 -x + part 0 -x | 0.81 | 0.56 | 0.38 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.81 | 0.17 | 0.02 | 0.00 | 0.00 | 0.01 | 11.66 |
| 40 kg | 0.74 | 0.24 | 0.01 | 0.01 | 0.00 | 0.01 | 9.85 |
| 60 kg | 0.52 | 0.45 | 0.03 | 0.00 | 0.00 | 0.00 | 7.88 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.28 | 0.66 | 0.85 | 0.00 | 1.00 | 0.27 | 0.72 | 0.86 | 0.00 |
| 40 kg | 1.00 | 0.26 | 0.73 | 0.89 | 0.00 | 1.00 | 0.22 | 0.78 | 0.90 | 0.00 |
| 60 kg | 1.00 | 0.20 | 0.82 | 0.94 | 0.00 | 1.00 | 0.21 | 0.80 | 0.94 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.81 | 2.36 | 0.07 | 0.79 | 2.04 | 0.05 |
| 40 kg | 0.80 | 2.29 | 0.08 | 0.77 | 1.99 | 0.06 |
| 60 kg | 0.78 | 2.02 | 0.07 | 0.76 | 2.05 | 0.07 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.51 | 0.57 | 0.31 |
| 40 kg | 0.56 | 0.60 | 0.33 |
| 60 kg | 0.67 | 0.59 | 0.33 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.87 | 0.45 | 25.28 | 11.66 | 0.14 | 0.01 | 8.56 | 0.00 | 0.29 |
| 40 kg | 1.46 | 0.46 | 26.03 | 9.85 | 0.74 | 1.91 | 4.74 | 0.00 | 0.22 |
| 60 kg | 1.29 | 0.48 | 28.26 | 7.88 | 0.39 | 3.51 | 1.90 | 0.00 | 0.19 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 100 | 264 | 192 |
| 40 kg | 139 | 321 | 255 |
| 60 kg | 180 | 363 | 309 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 1327 | 0.34 | 0.44 (285) | 0.52 (223) | 0.49 (415) | 0.51 (230) | 0.66 (174) |
| 40 kg | 1675 | 0.34 | 0.36 (427) | 0.52 (219) | 0.50 (228) | 0.50 (191) | 0.68 (610) |
| 60 kg | 2497 | 0.30 | 0.29 (792) | 0.49 (363) | 0.51 (353) | 0.56 (365) | 0.73 (623) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg |
|---|---|---|---|
| long | 0.11 | 0.10 | 0.22 |
| arch | 0.16 | 0.14 | 0.19 |
| dumbbell | 0.13 | 0.13 | 0.19 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg |
|---|---|---|---|
| A_straight | 0.94 | 0.81 | 0.67 |
| B_left | 0.75 | 0.81 | 0.72 |
| C_backright | 0.69 | 0.67 | 0.47 |
| D_far_turn | 0.83 | 0.67 | 0.22 |
