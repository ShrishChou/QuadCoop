# Pair evaluation: s4e-aa-s0-wrench

policy: Stage 4 contact policy logs/marl2/s4e_aa_s0/model_12000.pt (robots start at their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.68 | 0.60 | 0.01 | 0.01 | 26.3 | 0.01 | 0.48 | 0.44 | 0.20 | 0.33 | 1.02 |
| 40 kg | 0.64 | 0.57 | 0.03 | 0.01 | 26.0 | 0.02 | 0.57 | 0.54 | 0.28 | 0.37 | 1.00 |
| 60 kg | 0.41 | 0.36 | 0.05 | 0.03 | 31.9 | 0.01 | 0.66 | 0.60 | 0.35 | 0.40 | 1.01 |
| 80 kg | 0.25 | 0.17 | 0.06 | 0.06 | 33.2 | 0.01 | 0.70 | 0.69 | 0.45 | 0.48 | 0.97 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x+y + part 0 corner -x-y | 0.92 | 0.67 | 0.50 | 0.17 |
| long | part 0 -x seg 2/2 + part 0 corner -x-y | 0.75 | 0.83 | 0.50 | 0.33 |
| sphere | sector 135 + sector 225 | 1.00 | 1.00 | 0.92 | 1.00 |
| cylinder | part 0 corner -x-y + part 0 -x seg 2/2 | 0.33 | 0.42 | 0.33 | 0.25 |
| arch | part 3 -x + part 2 -x | 0.75 | 0.83 | 0.50 | 0.33 |
| dumbbell | part 0 -x + part 1 -x | 0.50 | 0.42 | 0.42 | 0.17 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.83 | 0.67 | 0.33 | 0.17 |
| beam (unseen) | part 0 -x seg 2/5 + part 0 -x seg 4/5 | 0.25 | 0.17 | 0.00 | 0.00 |
| l_shape (unseen) | part 1 -x + part 0 corner -x-y | 0.75 | 0.67 | 0.17 | 0.00 |
| asym (unseen) | part 1 -x + part 0 corner -x+y | 0.42 | 0.50 | 0.17 | 0.00 |
| u_channel (unseen) | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.83 | 0.75 | 0.50 | 0.17 |
| plus (unseen) | part 0 corner -x-y + part 0 corner -x+y | 0.83 | 0.75 | 0.58 | 0.42 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.68 | 0.30 | 0.01 | 0.01 | 0.00 | 0.01 | 7.62 |
| 40 kg | 0.64 | 0.32 | 0.04 | 0.00 | 0.00 | 0.01 | 5.55 |
| 60 kg | 0.41 | 0.51 | 0.08 | 0.00 | 0.00 | 0.00 | 3.08 |
| 80 kg | 0.25 | 0.64 | 0.11 | 0.00 | 0.00 | 0.00 | 2.31 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.26 | 0.78 | 0.83 | 0.00 | 1.00 | 0.28 | 0.72 | 0.81 | 0.00 |
| 40 kg | 1.00 | 0.23 | 0.81 | 0.86 | 0.00 | 1.00 | 0.26 | 0.79 | 0.87 | 0.00 |
| 60 kg | 1.00 | 0.21 | 0.85 | 0.89 | 0.00 | 1.00 | 0.22 | 0.85 | 0.91 | 0.00 |
| 80 kg | 1.00 | 0.22 | 0.85 | 0.91 | 0.00 | 1.00 | 0.15 | 0.90 | 0.97 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.95 | 1.96 | 0.04 | 0.95 | 2.08 | 0.04 |
| 40 kg | 0.95 | 1.32 | 0.04 | 0.95 | 1.79 | 0.04 |
| 60 kg | 0.94 | 0.73 | 0.04 | 0.95 | 1.15 | 0.03 |
| 80 kg | 0.96 | 0.70 | 0.04 | 0.98 | 0.51 | 0.04 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.63 | 0.62 | 0.27 |
| 40 kg | 0.70 | 0.69 | 0.23 |
| 60 kg | 0.76 | 0.75 | 0.20 |
| 80 kg | 0.76 | 0.81 | 0.17 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.17 | 0.19 | 0.24 | 0.29 |
| long | 0.21 | 0.50 | 0.61 | 0.63 |
| sphere | 0.38 | 0.61 | 0.72 | 0.75 |
| cylinder | 0.22 | 0.34 | 0.53 | 0.59 |
| arch | 0.14 | 0.18 | 0.27 | 0.20 |
| dumbbell | 0.13 | 0.19 | 0.17 | 0.25 |
| t_shape | 0.19 | 0.38 | 0.66 | 0.80 |
| beam | 0.13 | 0.19 | 0.18 | 0.47 |
| l_shape | 0.15 | 0.13 | 0.12 | 0.15 |
| asym | 0.36 | 0.27 | 0.27 | 0.67 |
| u_channel | 0.24 | 0.28 | 0.32 | 0.44 |
| plus | 0.12 | 0.11 | 0.12 | 0.11 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.81 | 0.83 | 0.69 | 0.56 |
| B_left | 0.75 | 0.67 | 0.36 | 0.17 |
| C_backright | 0.64 | 0.61 | 0.39 | 0.17 |
| D_far_turn | 0.53 | 0.44 | 0.19 | 0.11 |
