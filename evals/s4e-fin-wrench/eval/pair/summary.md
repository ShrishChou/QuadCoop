# Pair evaluation: s4e-fin-wrench

policy: Stage 4 contact policy logs/marl2/s4e_aa_s0/model_12000.pt (robots start at their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.63 | 0.51 | 0.01 | 0.00 | 25.3 | 0.02 | 0.49 | 0.48 | 0.24 | 0.37 | 1.01 |
| 40 kg | 0.58 | 0.45 | 0.03 | 0.01 | 29.7 | 0.02 | 0.55 | 0.59 | 0.29 | 0.37 | 1.00 |
| 60 kg | 0.36 | 0.33 | 0.03 | 0.03 | 31.9 | 0.01 | 0.60 | 0.68 | 0.36 | 0.40 | 0.98 |
| 80 kg | 0.17 | 0.15 | 0.04 | 0.06 | 30.7 | 0.01 | 0.65 | 0.73 | 0.42 | 0.46 | 0.94 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x-y + part 0 corner -x+y | 0.83 | 0.83 | 0.42 | 0.00 |
| long | part 0 corner -x+y + part 0 -x seg 1/2 | 0.67 | 0.67 | 0.42 | 0.25 |
| sphere | sector 225 + sector 135 | 1.00 | 1.00 | 0.92 | 0.92 |
| cylinder | part 0 corner -x+y + part 0 -x seg 1/2 | 0.17 | 0.42 | 0.25 | 0.17 |
| arch | part 2 -x + part 3 -x | 0.75 | 0.58 | 0.33 | 0.25 |
| dumbbell | part 1 -x + part 0 -x | 0.83 | 0.67 | 0.42 | 0.17 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.58 | 0.42 | 0.42 | 0.08 |
| beam (unseen) | part 0 -x seg 4/5 + part 0 -x seg 2/5 | 0.33 | 0.33 | 0.00 | 0.00 |
| l_shape (unseen) | part 0 corner -x-y + part 1 -x | 0.75 | 0.75 | 0.17 | 0.00 |
| asym (unseen) | part 1 corner -x-y + part 0 -x | 0.33 | 0.42 | 0.17 | 0.00 |
| u_channel (unseen) | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.58 | 0.58 | 0.33 | 0.00 |
| plus (unseen) | part 1 corner -x+y + part 1 corner -x-y | 0.75 | 0.33 | 0.50 | 0.25 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.63 | 0.36 | 0.01 | 0.00 | 0.00 | 0.02 | 6.93 |
| 40 kg | 0.58 | 0.38 | 0.03 | 0.00 | 0.00 | 0.01 | 4.93 |
| 60 kg | 0.36 | 0.58 | 0.06 | 0.00 | 0.00 | 0.00 | 3.02 |
| 80 kg | 0.17 | 0.72 | 0.10 | 0.00 | 0.00 | 0.00 | 1.78 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.28 | 0.77 | 0.81 | 0.00 | 1.00 | 0.28 | 0.74 | 0.82 | 0.00 |
| 40 kg | 1.00 | 0.26 | 0.78 | 0.84 | 0.00 | 1.00 | 0.23 | 0.82 | 0.89 | 0.00 |
| 60 kg | 1.00 | 0.19 | 0.85 | 0.91 | 0.00 | 1.00 | 0.26 | 0.81 | 0.90 | 0.00 |
| 80 kg | 1.00 | 0.19 | 0.87 | 0.94 | 0.00 | 1.00 | 0.22 | 0.83 | 0.92 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.95 | 2.09 | 0.03 | 0.94 | 1.97 | 0.04 |
| 40 kg | 0.92 | 1.75 | 0.04 | 0.95 | 1.33 | 0.03 |
| 60 kg | 0.94 | 1.07 | 0.04 | 0.94 | 1.17 | 0.04 |
| 80 kg | 0.96 | 0.47 | 0.04 | 0.93 | 0.26 | 0.04 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.64 | 0.63 | 0.27 |
| 40 kg | 0.66 | 0.71 | 0.24 |
| 60 kg | 0.73 | 0.74 | 0.20 |
| 80 kg | 0.78 | 0.76 | 0.18 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 6.65 | 0.43 | 24.83 | 6.93 | 0.00 | 0.00 | 0.00 | 0.00 | 0.37 |
| 40 kg | 5.85 | 0.50 | 24.07 | 4.93 | 0.00 | 0.00 | 0.00 | 0.00 | 0.30 |
| 60 kg | 7.47 | 0.55 | 25.10 | 3.02 | 0.00 | 0.00 | 0.00 | 0.00 | 0.26 |
| 80 kg | 7.37 | 0.59 | 24.64 | 1.78 | 0.00 | 0.00 | 0.00 | 0.00 | 0.24 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 89 | 237 | 158 |
| 40 kg | 132 | 299 | 222 |
| 60 kg | 164 | 327 | 278 |
| 80 kg | 186 | 346 | 318 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.17 | 0.25 | 0.22 | 0.49 |
| long | 0.23 | 0.33 | 0.52 | 0.60 |
| sphere | 0.63 | 0.63 | 0.75 | 0.73 |
| cylinder | 0.39 | 0.50 | 0.52 | 0.58 |
| arch | 0.18 | 0.19 | 0.20 | 0.21 |
| dumbbell | 0.11 | 0.19 | 0.19 | 0.20 |
| t_shape | 0.33 | 0.38 | 0.68 | 0.79 |
| beam | 0.18 | 0.22 | 0.40 | 0.38 |
| l_shape | 0.08 | 0.12 | 0.06 | 0.07 |
| asym | 0.31 | 0.36 | 0.41 | 0.58 |
| u_channel | 0.15 | 0.24 | 0.25 | 0.35 |
| plus | 0.07 | 0.11 | 0.08 | 0.11 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.81 | 0.72 | 0.58 | 0.33 |
| B_left | 0.69 | 0.67 | 0.36 | 0.08 |
| C_backright | 0.56 | 0.42 | 0.28 | 0.14 |
| D_far_turn | 0.47 | 0.53 | 0.22 | 0.14 |
