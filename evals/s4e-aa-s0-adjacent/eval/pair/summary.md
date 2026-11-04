# Pair evaluation: s4e-aa-s0-adjacent

policy: Stage 4 contact policy logs/marl2/s4e_aa_s0/model_12000.pt (robots start at their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.35 | 0.34 | 0.00 | 0.00 | 25.6 | 0.04 | 0.43 | 0.42 | 0.22 | 0.40 | 0.88 |
| 40 kg | 0.31 | 0.26 | 0.01 | 0.05 | 23.6 | 0.04 | 0.54 | 0.52 | 0.30 | 0.43 | 0.89 |
| 60 kg | 0.25 | 0.18 | 0.03 | 0.01 | 34.1 | 0.02 | 0.67 | 0.58 | 0.39 | 0.48 | 0.89 |
| 80 kg | 0.19 | 0.18 | 0.03 | 0.04 | 31.9 | 0.02 | 0.72 | 0.71 | 0.49 | 0.55 | 0.88 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x-y + part 0 corner -x+y | 0.67 | 0.75 | 0.75 | 0.17 |
| long | part 0 corner -x-y + part 0 -x seg 2/2 | 0.33 | 0.08 | 0.17 | 0.08 |
| sphere | sector 135 + sector 225 | 0.92 | 1.00 | 1.00 | 1.00 |
| cylinder | part 0 corner -x-y + part 0 -x seg 2/2 | 0.25 | 0.08 | 0.17 | 0.17 |
| arch | part 3 -x + part 2 -x | 0.42 | 0.50 | 0.33 | 0.33 |
| dumbbell | part 2 -x seg 2/3 + part 1 -x | 0.17 | 0.08 | 0.00 | 0.08 |
| t_shape | part 0 -x seg 2/3 + part 0 corner -x-y | 0.25 | 0.17 | 0.08 | 0.17 |
| beam (unseen) | part 0 -x seg 3/5 + part 0 -x seg 5/5 | 0.17 | 0.00 | 0.00 | 0.00 |
| l_shape (unseen) | part 0 corner -x+y + part 0 -x seg 1/2 | 0.58 | 0.33 | 0.08 | 0.08 |
| asym (unseen) | part 0 -x + part 1 corner -x-y | 0.25 | 0.25 | 0.08 | 0.00 |
| u_channel (unseen) | part 0 -x seg 2/3 + part 0 corner -x-y | 0.25 | 0.17 | 0.08 | 0.17 |
| plus (unseen) | part 1 corner -x-y + part 1 corner -x+y | 0.00 | 0.33 | 0.25 | 0.08 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.35 | 0.65 | 0.00 | 0.00 | 0.00 | 0.03 | 6.85 |
| 40 kg | 0.31 | 0.63 | 0.06 | 0.00 | 0.00 | 0.01 | 4.92 |
| 60 kg | 0.25 | 0.70 | 0.05 | 0.00 | 0.00 | 0.01 | 3.95 |
| 80 kg | 0.19 | 0.74 | 0.07 | 0.00 | 0.00 | 0.01 | 2.67 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.41 | 0.65 | 0.78 | 0.00 | 1.00 | 0.46 | 0.60 | 0.72 | 0.00 |
| 40 kg | 1.00 | 0.35 | 0.71 | 0.82 | 0.00 | 1.00 | 0.43 | 0.63 | 0.74 | 0.00 |
| 60 kg | 1.00 | 0.28 | 0.76 | 0.89 | 0.00 | 1.00 | 0.42 | 0.65 | 0.77 | 0.00 |
| 80 kg | 1.00 | 0.22 | 0.83 | 0.92 | 0.00 | 1.00 | 0.29 | 0.74 | 0.86 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.91 | 2.32 | 0.02 | 0.90 | 2.59 | 0.03 |
| 40 kg | 0.91 | 1.72 | 0.03 | 0.89 | 2.01 | 0.04 |
| 60 kg | 0.95 | 2.41 | 0.04 | 0.87 | 2.14 | 0.04 |
| 80 kg | 0.95 | 1.06 | 0.04 | 0.89 | 1.03 | 0.06 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.52 | 0.50 | 0.49 |
| 40 kg | 0.60 | 0.53 | 0.43 |
| 60 kg | 0.69 | 0.59 | 0.36 |
| 80 kg | 0.72 | 0.69 | 0.28 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.35 | 0.46 | 0.73 | 0.65 |
| long | 0.21 | 0.24 | 0.24 | 0.51 |
| sphere | 0.44 | 0.58 | 0.61 | 0.67 |
| cylinder | 0.35 | 0.42 | 0.39 | 0.50 |
| arch | 0.13 | 0.27 | 0.23 | 0.42 |
| dumbbell | 0.23 | 0.11 | 0.39 | 0.31 |
| t_shape | 0.22 | 0.31 | 0.33 | 0.53 |
| beam | 0.30 | 0.54 | 0.67 | 0.66 |
| l_shape | 0.19 | 0.15 | 0.32 | 0.56 |
| asym | 0.08 | 0.35 | 0.46 | 0.58 |
| u_channel | 0.07 | 0.12 | 0.20 | 0.31 |
| plus | 0.10 | 0.05 | 0.08 | 0.25 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.58 | 0.50 | 0.36 | 0.33 |
| B_left | 0.28 | 0.33 | 0.28 | 0.11 |
| C_backright | 0.28 | 0.25 | 0.22 | 0.19 |
| D_far_turn | 0.28 | 0.17 | 0.14 | 0.14 |
