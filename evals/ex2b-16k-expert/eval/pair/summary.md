# Pair evaluation: ex2b-16k-expert

policy: Stage 4 contact policy logs/marl2/ex2b_aa_s0/model_16000.pt (robots start at their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.56 | 0.54 | 0.00 | 0.00 | 22.3 | 0.01 | 0.52 | 0.46 | 0.24 | 0.36 | 1.05 |
| 40 kg | 0.47 | 0.42 | 0.01 | 0.01 | 26.3 | 0.01 | 0.60 | 0.50 | 0.26 | 0.33 | 1.06 |
| 60 kg | 0.38 | 0.32 | 0.01 | 0.01 | 34.6 | 0.01 | 0.69 | 0.63 | 0.43 | 0.49 | 1.05 |
| 80 kg | 0.26 | 0.20 | 0.03 | 0.03 | 38.2 | 0.01 | 0.78 | 0.77 | 0.64 | 0.71 | 1.01 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x+y + part 0 corner -x-y | 0.83 | 0.50 | 0.58 | 0.17 |
| long | part 0 -x seg 2/2 + part 0 corner -x-y | 0.67 | 0.75 | 0.58 | 0.25 |
| sphere | sector 135 + sector 225 | 1.00 | 1.00 | 0.92 | 0.83 |
| cylinder | part 0 corner -x-y + part 0 -x seg 2/2 | 0.50 | 0.25 | 0.17 | 0.25 |
| arch | part 3 -x + part 2 -x | 0.75 | 0.67 | 0.67 | 0.58 |
| dumbbell | part 0 -x + part 1 -x | 0.42 | 0.42 | 0.58 | 0.42 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.50 | 0.58 | 0.25 | 0.17 |
| beam (unseen) | part 0 -x seg 2/5 + part 0 -x seg 4/5 | 0.17 | 0.08 | 0.00 | 0.00 |
| l_shape (unseen) | part 1 -x + part 0 corner -x-y | 0.50 | 0.50 | 0.17 | 0.00 |
| asym (unseen) | part 1 -x + part 0 corner -x+y | 0.33 | 0.00 | 0.08 | 0.00 |
| u_channel (unseen) | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.50 | 0.25 | 0.25 | 0.08 |
| plus (unseen) | part 0 corner -x-y + part 0 corner -x+y | 0.50 | 0.67 | 0.25 | 0.33 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.56 | 0.44 | 0.00 | 0.00 | 0.00 | 0.08 | 5.09 |
| 40 kg | 0.47 | 0.51 | 0.02 | 0.00 | 0.00 | 0.03 | 3.88 |
| 60 kg | 0.38 | 0.60 | 0.02 | 0.00 | 0.00 | 0.01 | 3.88 |
| 80 kg | 0.26 | 0.69 | 0.06 | 0.00 | 0.00 | 0.00 | 2.65 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.18 | 0.83 | 0.92 | 0.00 | 1.00 | 0.19 | 0.83 | 0.93 | 0.00 |
| 40 kg | 1.00 | 0.14 | 0.91 | 0.96 | 0.00 | 1.00 | 0.14 | 0.91 | 0.97 | 0.00 |
| 60 kg | 1.00 | 0.13 | 0.92 | 0.97 | 0.00 | 1.00 | 0.15 | 0.89 | 0.98 | 0.00 |
| 80 kg | 1.00 | 0.13 | 0.92 | 0.99 | 0.00 | 1.00 | 0.15 | 0.93 | 0.98 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.94 | 1.12 | 0.02 | 0.96 | 1.29 | 0.02 |
| 40 kg | 0.98 | 1.00 | 0.03 | 0.98 | 0.75 | 0.02 |
| 60 kg | 0.98 | 0.78 | 0.02 | 0.98 | 0.72 | 0.02 |
| 80 kg | 0.98 | 0.35 | 0.02 | 0.99 | 0.60 | 0.02 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.67 | 0.68 | 0.30 |
| 40 kg | 0.76 | 0.81 | 0.33 |
| 60 kg | 0.82 | 0.81 | 0.30 |
| 80 kg | 0.83 | 0.84 | 0.25 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.08 | 0.62 | 21.29 | 5.09 | 3.94 | 0.12 | 4.94 | 0.00 | 0.24 |
| 40 kg | 0.22 | 0.71 | 19.78 | 3.88 | 4.48 | 2.52 | 4.62 | 0.00 | 0.14 |
| 60 kg | 0.12 | 0.78 | 20.81 | 3.88 | 3.10 | 4.15 | 3.44 | 0.00 | 0.12 |
| 80 kg | 0.29 | 0.80 | 21.30 | 2.65 | 2.65 | 6.41 | 1.42 | 0.00 | 0.11 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 96 | 238 | 173 |
| 40 kg | 130 | 294 | 235 |
| 60 kg | 154 | 319 | 273 |
| 80 kg | 179 | 338 | 320 |

## executor v2: holding and the team-ready barrier (time every robot of the push group is told to hold; the object's mean speed then and the share of it above 2 cm/s (gate: under 2 cm/s); each robot's contact force while told to hold; delay from team ready to both robots pressing (gate: under 0.2 s))

| mass | all holding (s) | object speed (m/s) | moving > 2 cm/s | force while holding (N) | ready to push (s) |
|---|---|---|---|---|---|
| 20 kg | 0.27 | 0.03 | 0.22 | 10 | 0.12 |
| 40 kg | 0.24 | 0.01 | 0.12 | 13 | 0.07 |
| 60 kg | 0.22 | 0.01 | 0.08 | 16 | 0.06 |
| 80 kg | 0.21 | 0.01 | 0.05 | 14 | 0.06 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.23 | 0.17 | 0.41 | 0.76 |
| long | 0.30 | 0.31 | 0.49 | 0.66 |
| sphere | 0.37 | 0.57 | 0.80 | 0.86 |
| cylinder | 0.23 | 0.28 | 0.30 | 0.71 |
| arch | 0.31 | 0.35 | 0.38 | 0.49 |
| dumbbell | 0.22 | 0.23 | 0.42 | 0.68 |
| t_shape | 0.29 | 0.27 | 0.43 | 0.73 |
| beam | 0.15 | 0.23 | 0.59 | 0.66 |
| l_shape | 0.26 | 0.16 | 0.31 | 0.63 |
| asym | 0.21 | 0.24 | 0.46 | 0.74 |
| u_channel | 0.23 | 0.19 | 0.43 | 0.51 |
| plus | 0.14 | 0.15 | 0.08 | 0.26 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.75 | 0.67 | 0.58 | 0.50 |
| B_left | 0.56 | 0.42 | 0.31 | 0.19 |
| C_backright | 0.33 | 0.39 | 0.36 | 0.31 |
| D_far_turn | 0.58 | 0.42 | 0.25 | 0.03 |
