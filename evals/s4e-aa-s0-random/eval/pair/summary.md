# Pair evaluation: s4e-aa-s0-random

policy: Stage 4 contact policy logs/marl2/s4e_aa_s0/model_12000.pt (robots start at their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.40 | 0.40 | 0.00 | 0.01 | 24.6 | 0.03 | 0.44 | 0.44 | 0.24 | 0.43 | 0.96 |
| 40 kg | 0.33 | 0.26 | 0.03 | 0.01 | 21.7 | 0.03 | 0.52 | 0.53 | 0.32 | 0.47 | 0.96 |
| 60 kg | 0.31 | 0.26 | 0.03 | 0.02 | 27.0 | 0.02 | 0.64 | 0.64 | 0.42 | 0.51 | 0.95 |
| 80 kg | 0.17 | 0.15 | 0.05 | 0.06 | 27.5 | 0.02 | 0.68 | 0.75 | 0.51 | 0.56 | 0.96 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x-y + part 0 corner -x+y | 0.75 | 0.42 | 0.67 | 0.17 |
| long | part 0 corner -x-y + part 0 -x seg 2/2 | 0.42 | 0.33 | 0.42 | 0.17 |
| sphere | sector 135 + sector 225 | 0.92 | 1.00 | 1.00 | 1.00 |
| cylinder | part 0 -x seg 2/2 + part 0 corner -x-y | 0.17 | 0.08 | 0.25 | 0.25 |
| arch | part 2 -x + part 3 corner -x-y | 0.42 | 0.42 | 0.33 | 0.17 |
| dumbbell | part 0 corner -x-y + part 1 corner -x-y | 0.17 | 0.33 | 0.33 | 0.00 |
| t_shape | part 0 -x seg 2/3 + part 0 corner -x+y | 0.25 | 0.25 | 0.00 | 0.00 |
| beam (unseen) | part 0 corner -x-y + part 0 -x seg 3/5 | 0.25 | 0.08 | 0.00 | 0.00 |
| l_shape (unseen) | part 0 -x seg 1/2 + part 1 corner -x+y | 0.50 | 0.17 | 0.17 | 0.08 |
| asym (unseen) | part 0 corner -x+y + part 1 corner -x-y | 0.33 | 0.33 | 0.08 | 0.00 |
| u_channel (unseen) | part 0 -x seg 1/3 + part 0 corner -x+y | 0.42 | 0.33 | 0.42 | 0.08 |
| plus (unseen) | part 1 corner -x+y + part 0 corner -x-y | 0.25 | 0.25 | 0.08 | 0.17 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.40 | 0.58 | 0.01 | 0.01 | 0.00 | 0.03 | 7.71 |
| 40 kg | 0.33 | 0.62 | 0.04 | 0.00 | 0.00 | 0.00 | 5.55 |
| 60 kg | 0.31 | 0.63 | 0.06 | 0.00 | 0.00 | 0.00 | 3.93 |
| 80 kg | 0.17 | 0.72 | 0.11 | 0.00 | 0.00 | 0.00 | 2.99 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.44 | 0.66 | 0.76 | 0.00 | 1.00 | 0.38 | 0.67 | 0.78 | 0.00 |
| 40 kg | 1.00 | 0.38 | 0.70 | 0.81 | 0.00 | 1.00 | 0.41 | 0.67 | 0.76 | 0.00 |
| 60 kg | 1.00 | 0.33 | 0.77 | 0.87 | 0.00 | 1.00 | 0.34 | 0.73 | 0.82 | 0.00 |
| 80 kg | 1.00 | 0.23 | 0.82 | 0.91 | 0.00 | 1.00 | 0.23 | 0.82 | 0.92 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.91 | 2.46 | 0.02 | 0.91 | 2.24 | 0.02 |
| 40 kg | 0.90 | 1.74 | 0.03 | 0.89 | 1.66 | 0.03 |
| 60 kg | 0.91 | 1.14 | 0.04 | 0.92 | 1.86 | 0.04 |
| 80 kg | 0.93 | 0.87 | 0.04 | 0.94 | 0.95 | 0.05 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.53 | 0.54 | 0.46 |
| 40 kg | 0.58 | 0.57 | 0.38 |
| 60 kg | 0.67 | 0.63 | 0.34 |
| 80 kg | 0.72 | 0.74 | 0.29 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.28 | 0.35 | 0.74 | 0.74 |
| long | 0.24 | 0.35 | 0.65 | 0.55 |
| sphere | 0.65 | 0.69 | 0.72 | 0.77 |
| cylinder | 0.31 | 0.51 | 0.65 | 0.81 |
| arch | 0.12 | 0.12 | 0.22 | 0.31 |
| dumbbell | 0.13 | 0.12 | 0.19 | 0.25 |
| t_shape | 0.16 | 0.25 | 0.15 | 0.44 |
| beam | 0.29 | 0.50 | 0.59 | 0.66 |
| l_shape | 0.24 | 0.24 | 0.23 | 0.42 |
| asym | 0.15 | 0.35 | 0.44 | 0.62 |
| u_channel | 0.26 | 0.28 | 0.39 | 0.39 |
| plus | 0.09 | 0.04 | 0.06 | 0.15 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.50 | 0.44 | 0.47 | 0.31 |
| B_left | 0.36 | 0.31 | 0.25 | 0.08 |
| C_backright | 0.42 | 0.42 | 0.33 | 0.22 |
| D_far_turn | 0.33 | 0.17 | 0.19 | 0.08 |
