# Pair evaluation: coordcol-bc0-s102-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 12 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.83 | 0.78 | 0.01 | 0.00 | 25.4 | 0.00 | 0.40 | 0.39 | 0.15 | 0.28 | 1.34 |
| 40 kg | 0.81 | 0.65 | 0.00 | 0.01 | 31.2 | 0.00 | 0.47 | 0.40 | 0.14 | 0.21 | 1.43 |
| 60 kg | 0.60 | 0.51 | 0.01 | 0.03 | 43.3 | 0.00 | 0.51 | 0.48 | 0.21 | 0.28 | 1.37 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg |
|---|---|---|---|---|
| long | part 0 -x seg 1/2 + part 0 corner -x+y | 0.77 | 0.79 | 0.62 |
| arch | part 2 -x + part 3 -x | 0.92 | 0.92 | 0.69 |
| dumbbell | part 1 -x + part 0 -x | 0.79 | 0.71 | 0.50 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.83 | 0.17 | 0.01 | 0.00 | 0.00 | 0.01 | 12.64 |
| 40 kg | 0.81 | 0.17 | 0.01 | 0.01 | 0.00 | 0.01 | 10.10 |
| 60 kg | 0.60 | 0.35 | 0.04 | 0.00 | 0.00 | 0.00 | 7.88 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.33 | 0.64 | 0.84 | 0.00 | 1.00 | 0.30 | 0.71 | 0.84 | 0.00 |
| 40 kg | 1.00 | 0.30 | 0.71 | 0.88 | 0.00 | 1.00 | 0.23 | 0.78 | 0.88 | 0.00 |
| 60 kg | 1.00 | 0.24 | 0.79 | 0.93 | 0.00 | 1.00 | 0.21 | 0.81 | 0.93 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.81 | 2.48 | 0.07 | 0.77 | 1.94 | 0.05 |
| 40 kg | 0.80 | 2.60 | 0.08 | 0.76 | 1.81 | 0.05 |
| 60 kg | 0.79 | 2.51 | 0.07 | 0.76 | 2.16 | 0.06 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.48 | 0.57 | 0.30 |
| 40 kg | 0.53 | 0.62 | 0.31 |
| 60 kg | 0.63 | 0.64 | 0.32 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.65 | 0.42 | 25.08 | 12.64 | 0.45 | 0.24 | 7.03 | 0.00 | 0.31 |
| 40 kg | 1.78 | 0.44 | 24.53 | 10.10 | 0.21 | 0.68 | 4.68 | 0.00 | 0.25 |
| 60 kg | 1.47 | 0.52 | 28.05 | 7.88 | 0.19 | 3.55 | 2.00 | 0.00 | 0.21 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 95 | 257 | 171 |
| 40 kg | 135 | 317 | 236 |
| 60 kg | 175 | 359 | 296 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 1138 | 0.34 | 0.40 (188) | 0.51 (270) | 0.50 (320) | 0.52 (184) | 0.61 (176) |
| 40 kg | 1401 | 0.31 | 0.30 (326) | 0.47 (204) | 0.49 (220) | 0.53 (204) | 0.71 (447) |
| 60 kg | 2594 | 0.29 | 0.24 (865) | 0.48 (429) | 0.52 (357) | 0.58 (356) | 0.72 (588) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg |
|---|---|---|---|
| long | 0.14 | 0.13 | 0.20 |
| arch | 0.17 | 0.14 | 0.20 |
| dumbbell | 0.14 | 0.15 | 0.22 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg |
|---|---|---|---|
| A_straight | 0.97 | 0.83 | 0.69 |
| B_left | 0.83 | 0.89 | 0.69 |
| C_backright | 0.69 | 0.81 | 0.44 |
| D_far_turn | 0.81 | 0.69 | 0.58 |
