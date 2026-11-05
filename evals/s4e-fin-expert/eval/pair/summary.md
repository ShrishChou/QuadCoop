# Pair evaluation: s4e-fin-expert

policy: Stage 4 contact policy logs/marl2/s4e_aa_s0/model_12000.pt (robots start at their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.66 | 0.61 | 0.00 | 0.00 | 23.0 | 0.01 | 0.54 | 0.52 | 0.27 | 0.37 | 1.06 |
| 40 kg | 0.58 | 0.50 | 0.00 | 0.03 | 26.1 | 0.01 | 0.60 | 0.58 | 0.32 | 0.39 | 1.03 |
| 60 kg | 0.47 | 0.40 | 0.06 | 0.01 | 31.0 | 0.01 | 0.70 | 0.71 | 0.49 | 0.56 | 1.05 |
| 80 kg | 0.24 | 0.19 | 0.05 | 0.01 | 28.1 | 0.01 | 0.78 | 0.80 | 0.63 | 0.68 | 1.01 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x+y + part 0 corner -x-y | 0.83 | 0.83 | 0.67 | 0.17 |
| long | part 0 -x seg 2/2 + part 0 corner -x-y | 0.58 | 0.67 | 0.50 | 0.17 |
| sphere | sector 135 + sector 225 | 1.00 | 1.00 | 1.00 | 1.00 |
| cylinder | part 0 corner -x-y + part 0 -x seg 2/2 | 0.25 | 0.33 | 0.25 | 0.25 |
| arch | part 3 -x + part 2 -x | 0.58 | 0.58 | 0.58 | 0.33 |
| dumbbell | part 0 -x + part 1 -x | 0.58 | 0.50 | 0.67 | 0.25 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.58 | 0.58 | 0.50 | 0.08 |
| beam (unseen) | part 0 -x seg 2/5 + part 0 -x seg 4/5 | 0.42 | 0.33 | 0.00 | 0.00 |
| l_shape (unseen) | part 1 -x + part 0 corner -x-y | 0.83 | 0.50 | 0.50 | 0.00 |
| asym (unseen) | part 1 -x + part 0 corner -x+y | 0.75 | 0.42 | 0.08 | 0.00 |
| u_channel (unseen) | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.58 | 0.33 | 0.50 | 0.17 |
| plus (unseen) | part 0 corner -x-y + part 0 corner -x+y | 0.92 | 0.83 | 0.42 | 0.42 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.66 | 0.33 | 0.00 | 0.01 | 0.00 | 0.02 | 6.90 |
| 40 kg | 0.58 | 0.39 | 0.03 | 0.01 | 0.00 | 0.01 | 5.74 |
| 60 kg | 0.47 | 0.46 | 0.07 | 0.00 | 0.00 | 0.00 | 6.98 |
| 80 kg | 0.24 | 0.70 | 0.06 | 0.00 | 0.00 | 0.00 | 5.74 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.21 | 0.80 | 0.88 | 0.00 | 1.00 | 0.15 | 0.86 | 0.91 | 0.00 |
| 40 kg | 1.00 | 0.15 | 0.87 | 0.93 | 0.00 | 1.00 | 0.16 | 0.84 | 0.95 | 0.00 |
| 60 kg | 1.00 | 0.13 | 0.90 | 0.96 | 0.00 | 1.00 | 0.15 | 0.88 | 0.97 | 0.00 |
| 80 kg | 1.00 | 0.13 | 0.88 | 0.98 | 0.00 | 1.00 | 0.13 | 0.89 | 0.99 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.95 | 1.27 | 0.04 | 0.97 | 1.03 | 0.03 |
| 40 kg | 0.96 | 0.96 | 0.04 | 0.97 | 0.88 | 0.05 |
| 60 kg | 0.97 | 0.73 | 0.04 | 0.97 | 0.91 | 0.04 |
| 80 kg | 0.97 | 0.45 | 0.05 | 0.98 | 0.63 | 0.05 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.67 | 0.72 | 0.32 |
| 40 kg | 0.76 | 0.74 | 0.31 |
| 60 kg | 0.83 | 0.81 | 0.29 |
| 80 kg | 0.81 | 0.82 | 0.25 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 2.90 | 0.60 | 20.18 | 6.90 | 3.25 | 0.24 | 7.24 | 0.00 | 0.21 |
| 40 kg | 0.68 | 0.67 | 20.82 | 5.74 | 4.00 | 1.56 | 3.80 | 0.00 | 0.17 |
| 60 kg | 0.56 | 0.74 | 21.54 | 6.98 | 3.60 | 3.47 | 2.13 | 0.00 | 0.13 |
| 80 kg | 0.23 | 0.71 | 23.77 | 5.74 | 2.66 | 8.05 | 0.49 | 0.00 | 0.15 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 88 | 237 | 165 |
| 40 kg | 127 | 294 | 226 |
| 60 kg | 155 | 321 | 271 |
| 80 kg | 181 | 342 | 318 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.32 | 0.35 | 0.63 | 0.74 |
| long | 0.20 | 0.34 | 0.58 | 0.62 |
| sphere | 0.48 | 0.55 | 0.69 | 0.79 |
| cylinder | 0.16 | 0.33 | 0.47 | 0.59 |
| arch | 0.29 | 0.32 | 0.40 | 0.50 |
| dumbbell | 0.24 | 0.27 | 0.47 | 0.75 |
| t_shape | 0.35 | 0.45 | 0.51 | 0.76 |
| beam | 0.26 | 0.30 | 0.55 | 0.69 |
| l_shape | 0.26 | 0.22 | 0.35 | 0.58 |
| asym | 0.28 | 0.30 | 0.63 | 0.53 |
| u_channel | 0.24 | 0.22 | 0.36 | 0.65 |
| plus | 0.15 | 0.15 | 0.24 | 0.37 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.83 | 0.81 | 0.78 | 0.50 |
| B_left | 0.67 | 0.53 | 0.44 | 0.14 |
| C_backright | 0.53 | 0.56 | 0.39 | 0.22 |
| D_far_turn | 0.61 | 0.42 | 0.28 | 0.08 |
