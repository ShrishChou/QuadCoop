# Pair evaluation: coordcol-bc0-s103-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 12 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.83 | 0.72 | 0.00 | 0.01 | 28.0 | 0.00 | 0.40 | 0.38 | 0.12 | 0.23 | 1.38 |
| 40 kg | 0.68 | 0.60 | 0.03 | 0.01 | 30.3 | 0.00 | 0.47 | 0.40 | 0.13 | 0.20 | 1.46 |
| 60 kg | 0.59 | 0.49 | 0.03 | 0.01 | 42.1 | 0.00 | 0.56 | 0.46 | 0.22 | 0.29 | 1.42 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg |
|---|---|---|---|---|
| long | part 0 -x seg 2/2 + part 0 corner -x-y | 0.81 | 0.69 | 0.56 |
| arch | part 2 -x + part 3 -x | 0.88 | 0.79 | 0.71 |
| dumbbell | part 0 -x + part 1 -x | 0.81 | 0.56 | 0.50 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.83 | 0.16 | 0.01 | 0.00 | 0.00 | 0.01 | 11.65 |
| 40 kg | 0.68 | 0.28 | 0.04 | 0.00 | 0.00 | 0.01 | 8.93 |
| 60 kg | 0.59 | 0.35 | 0.05 | 0.01 | 0.00 | 0.01 | 8.35 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.33 | 0.64 | 0.82 | 0.00 | 1.00 | 0.26 | 0.72 | 0.85 | 0.00 |
| 40 kg | 1.00 | 0.25 | 0.73 | 0.90 | 0.00 | 1.00 | 0.23 | 0.78 | 0.88 | 0.00 |
| 60 kg | 1.00 | 0.24 | 0.79 | 0.93 | 0.00 | 1.00 | 0.21 | 0.82 | 0.93 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.82 | 2.34 | 0.07 | 0.79 | 2.11 | 0.05 |
| 40 kg | 0.81 | 2.21 | 0.07 | 0.79 | 2.06 | 0.06 |
| 60 kg | 0.80 | 2.41 | 0.06 | 0.78 | 2.03 | 0.07 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.47 | 0.59 | 0.31 |
| 40 kg | 0.55 | 0.60 | 0.33 |
| 60 kg | 0.62 | 0.63 | 0.32 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.83 | 0.42 | 25.36 | 11.65 | 0.41 | 0.01 | 7.28 | 0.00 | 0.30 |
| 40 kg | 1.69 | 0.44 | 25.61 | 8.93 | 0.49 | 1.68 | 4.62 | 0.00 | 0.24 |
| 60 kg | 1.39 | 0.49 | 27.55 | 8.35 | 0.39 | 2.35 | 2.03 | 0.00 | 0.20 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 99 | 259 | 185 |
| 40 kg | 140 | 320 | 247 |
| 60 kg | 178 | 364 | 304 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 1169 | 0.35 | 0.42 (203) | 0.52 (200) | 0.51 (305) | 0.52 (198) | 0.60 (262) |
| 40 kg | 1364 | 0.30 | 0.28 (349) | 0.50 (134) | 0.51 (241) | 0.53 (148) | 0.72 (492) |
| 60 kg | 2433 | 0.31 | 0.28 (542) | 0.45 (435) | 0.49 (384) | 0.52 (375) | 0.70 (697) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg |
|---|---|---|---|
| long | 0.10 | 0.12 | 0.21 |
| arch | 0.11 | 0.13 | 0.18 |
| dumbbell | 0.16 | 0.14 | 0.26 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg |
|---|---|---|---|
| A_straight | 0.86 | 0.83 | 0.81 |
| B_left | 0.89 | 0.75 | 0.67 |
| C_backright | 0.78 | 0.58 | 0.33 |
| D_far_turn | 0.81 | 0.56 | 0.56 |
