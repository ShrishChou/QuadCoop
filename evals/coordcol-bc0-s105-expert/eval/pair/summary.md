# Pair evaluation: coordcol-bc0-s105-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 12 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.85 | 0.78 | 0.00 | 0.01 | 25.5 | 0.00 | 0.42 | 0.36 | 0.14 | 0.26 | 1.33 |
| 40 kg | 0.76 | 0.60 | 0.01 | 0.01 | 30.8 | 0.00 | 0.46 | 0.42 | 0.14 | 0.21 | 1.43 |
| 60 kg | 0.65 | 0.57 | 0.01 | 0.01 | 43.1 | 0.00 | 0.57 | 0.45 | 0.21 | 0.27 | 1.43 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg |
|---|---|---|---|---|
| long | part 0 -x seg 1/2 + part 0 corner -x+y | 0.77 | 0.73 | 0.69 |
| arch | part 2 -x + part 3 -x | 0.90 | 0.98 | 0.67 |
| dumbbell | part 0 -x + part 1 -x | 0.88 | 0.56 | 0.58 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.85 | 0.15 | 0.01 | 0.00 | 0.00 | 0.01 | 12.55 |
| 40 kg | 0.76 | 0.22 | 0.02 | 0.01 | 0.00 | 0.01 | 10.01 |
| 60 kg | 0.65 | 0.33 | 0.02 | 0.00 | 0.00 | 0.00 | 8.42 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.28 | 0.67 | 0.84 | 0.00 | 1.00 | 0.28 | 0.70 | 0.83 | 0.00 |
| 40 kg | 1.00 | 0.26 | 0.74 | 0.88 | 0.00 | 1.00 | 0.21 | 0.79 | 0.90 | 0.00 |
| 60 kg | 1.00 | 0.24 | 0.78 | 0.93 | 0.00 | 1.00 | 0.20 | 0.82 | 0.94 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.80 | 2.21 | 0.07 | 0.80 | 2.03 | 0.05 |
| 40 kg | 0.81 | 2.22 | 0.07 | 0.78 | 1.92 | 0.05 |
| 60 kg | 0.79 | 2.24 | 0.07 | 0.77 | 1.92 | 0.06 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.51 | 0.55 | 0.31 |
| 40 kg | 0.55 | 0.61 | 0.32 |
| 60 kg | 0.62 | 0.62 | 0.31 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.12 | 0.44 | 23.91 | 12.55 | 0.11 | 0.24 | 7.77 | 0.00 | 0.27 |
| 40 kg | 1.09 | 0.45 | 23.94 | 10.01 | 0.58 | 1.43 | 5.02 | 0.00 | 0.22 |
| 60 kg | 1.70 | 0.47 | 27.25 | 8.42 | 0.40 | 3.12 | 1.49 | 0.00 | 0.20 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 98 | 258 | 187 |
| 40 kg | 140 | 326 | 247 |
| 60 kg | 178 | 363 | 307 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 1112 | 0.36 | 0.43 (283) | 0.52 (141) | 0.51 (300) | 0.52 (202) | 0.62 (186) |
| 40 kg | 1477 | 0.31 | 0.31 (450) | 0.48 (181) | 0.50 (235) | 0.53 (241) | 0.72 (371) |
| 60 kg | 2281 | 0.29 | 0.26 (553) | 0.47 (377) | 0.51 (385) | 0.53 (267) | 0.74 (698) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg |
|---|---|---|---|
| long | 0.12 | 0.11 | 0.22 |
| arch | 0.17 | 0.17 | 0.21 |
| dumbbell | 0.14 | 0.14 | 0.21 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg |
|---|---|---|---|
| A_straight | 0.94 | 0.83 | 0.94 |
| B_left | 0.81 | 0.69 | 0.78 |
| C_backright | 0.81 | 0.81 | 0.44 |
| D_far_turn | 0.83 | 0.69 | 0.42 |
