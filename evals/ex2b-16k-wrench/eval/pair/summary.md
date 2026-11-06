# Pair evaluation: ex2b-16k-wrench

policy: Stage 4 contact policy logs/marl2/ex2b_aa_s0/model_16000.pt (robots start at their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.67 | 0.65 | 0.01 | 0.00 | 26.4 | 0.02 | 0.41 | 0.49 | 0.23 | 0.40 | 0.97 |
| 40 kg | 0.50 | 0.44 | 0.01 | 0.01 | 28.0 | 0.01 | 0.50 | 0.52 | 0.26 | 0.37 | 0.98 |
| 60 kg | 0.35 | 0.19 | 0.01 | 0.02 | 31.3 | 0.01 | 0.53 | 0.63 | 0.32 | 0.39 | 0.95 |
| 80 kg | 0.19 | 0.15 | 0.04 | 0.03 | 36.1 | 0.01 | 0.60 | 0.73 | 0.43 | 0.49 | 0.97 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x-y + part 0 corner -x+y | 0.92 | 0.92 | 0.33 | 0.08 |
| long | part 0 corner -x+y + part 0 -x seg 1/2 | 1.00 | 0.58 | 0.58 | 0.25 |
| sphere | sector 225 + sector 135 | 0.92 | 0.92 | 1.00 | 0.75 |
| cylinder | part 0 corner -x+y + part 0 -x seg 1/2 | 0.50 | 0.25 | 0.25 | 0.17 |
| arch | part 2 -x + part 3 -x | 0.75 | 0.67 | 0.33 | 0.25 |
| dumbbell | part 1 -x + part 0 -x | 0.58 | 0.25 | 0.33 | 0.25 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.67 | 0.67 | 0.75 | 0.33 |
| beam (unseen) | part 0 -x seg 4/5 + part 0 -x seg 2/5 | 0.42 | 0.25 | 0.00 | 0.00 |
| l_shape (unseen) | part 0 corner -x-y + part 1 -x | 0.75 | 0.42 | 0.25 | 0.00 |
| asym (unseen) | part 1 corner -x-y + part 0 -x | 0.58 | 0.50 | 0.00 | 0.00 |
| u_channel (unseen) | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.50 | 0.08 | 0.17 | 0.08 |
| plus (unseen) | part 1 corner -x+y + part 1 corner -x-y | 0.42 | 0.50 | 0.17 | 0.08 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.67 | 0.33 | 0.01 | 0.00 | 0.00 | 0.02 | 5.53 |
| 40 kg | 0.50 | 0.48 | 0.02 | 0.00 | 0.00 | 0.01 | 3.51 |
| 60 kg | 0.35 | 0.62 | 0.03 | 0.00 | 0.00 | 0.01 | 2.28 |
| 80 kg | 0.19 | 0.74 | 0.07 | 0.00 | 0.00 | 0.00 | 1.09 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.27 | 0.77 | 0.85 | 0.00 | 1.00 | 0.30 | 0.76 | 0.82 | 0.00 |
| 40 kg | 1.00 | 0.27 | 0.80 | 0.89 | 0.00 | 1.00 | 0.27 | 0.79 | 0.87 | 0.00 |
| 60 kg | 1.00 | 0.20 | 0.86 | 0.94 | 0.00 | 1.00 | 0.23 | 0.86 | 0.91 | 0.00 |
| 80 kg | 1.00 | 0.18 | 0.89 | 0.96 | 0.00 | 1.00 | 0.15 | 0.91 | 0.98 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.94 | 1.28 | 0.02 | 0.94 | 1.32 | 0.01 |
| 40 kg | 0.93 | 1.08 | 0.02 | 0.94 | 0.95 | 0.02 |
| 60 kg | 0.94 | 0.95 | 0.02 | 0.94 | 0.56 | 0.02 |
| 80 kg | 0.97 | 0.49 | 0.02 | 0.97 | 0.32 | 0.02 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.57 | 0.58 | 0.22 |
| 40 kg | 0.65 | 0.65 | 0.20 |
| 60 kg | 0.72 | 0.74 | 0.18 |
| 80 kg | 0.78 | 0.78 | 0.17 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 3.11 | 0.51 | 20.23 | 5.53 | 0.00 | 0.00 | 0.00 | 0.00 | 0.30 |
| 40 kg | 4.10 | 0.59 | 18.68 | 3.51 | 0.00 | 0.00 | 0.00 | 0.00 | 0.27 |
| 60 kg | 2.98 | 0.68 | 20.20 | 2.28 | 0.00 | 0.00 | 0.00 | 0.00 | 0.22 |
| 80 kg | 0.54 | 0.73 | 19.41 | 1.09 | 0.00 | 0.00 | 0.00 | 0.00 | 0.14 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 91 | 245 | 163 |
| 40 kg | 130 | 302 | 230 |
| 60 kg | 161 | 329 | 283 |
| 80 kg | 180 | 339 | 319 |

## executor v2: holding and the team-ready barrier (time every robot of the push group is told to hold; the object's mean speed then and the share of it above 2 cm/s (gate: under 2 cm/s); each robot's contact force while told to hold; delay from team ready to both robots pressing (gate: under 0.2 s))

| mass | all holding (s) | object speed (m/s) | moving > 2 cm/s | force while holding (N) | ready to push (s) |
|---|---|---|---|---|---|
| 20 kg | 1.05 | 0.02 | 0.13 | 6 | 0.13 |
| 40 kg | 0.92 | 0.01 | 0.09 | 10 | 0.07 |
| 60 kg | 0.99 | 0.01 | 0.06 | 12 | 0.38 |
| 80 kg | 0.88 | 0.01 | 0.05 | 11 | 0.07 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.34 | 0.16 | 0.24 | 0.54 |
| long | 0.26 | 0.42 | 0.33 | 0.48 |
| sphere | 0.43 | 0.69 | 0.82 | 0.80 |
| cylinder | 0.21 | 0.16 | 0.41 | 0.54 |
| arch | 0.24 | 0.28 | 0.25 | 0.27 |
| dumbbell | 0.19 | 0.18 | 0.16 | 0.25 |
| t_shape | 0.22 | 0.31 | 0.40 | 0.58 |
| beam | 0.42 | 0.40 | 0.41 | 0.50 |
| l_shape | 0.13 | 0.09 | 0.05 | 0.12 |
| asym | 0.20 | 0.29 | 0.50 | 0.66 |
| u_channel | 0.13 | 0.09 | 0.23 | 0.34 |
| plus | 0.06 | 0.10 | 0.05 | 0.10 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.89 | 0.78 | 0.58 | 0.36 |
| B_left | 0.61 | 0.36 | 0.33 | 0.11 |
| C_backright | 0.78 | 0.58 | 0.31 | 0.17 |
| D_far_turn | 0.39 | 0.28 | 0.17 | 0.11 |
