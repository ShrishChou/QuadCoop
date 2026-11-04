# Pair evaluation: step0-s4d-wrench

policy: Stage 4 contact policy logs/marl2/s4d_aa_s0/model_9000.pt (robots start at their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.69 | 0.58 | 0.00 | 0.02 | 23.3 | 0.01 | 0.49 | 0.52 | 0.25 | 0.37 | 1.01 |
| 40 kg | 0.53 | 0.44 | 0.03 | 0.00 | 27.5 | 0.01 | 0.60 | 0.51 | 0.31 | 0.41 | 1.00 |
| 60 kg | 0.39 | 0.33 | 0.04 | 0.03 | 40.2 | 0.01 | 0.68 | 0.59 | 0.38 | 0.44 | 0.96 |
| 80 kg | 0.19 | 0.16 | 0.06 | 0.08 | 38.1 | 0.01 | 0.73 | 0.67 | 0.48 | 0.54 | 0.95 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x+y + part 0 corner -x-y | 0.92 | 0.75 | 0.67 | 0.08 |
| long | part 0 -x seg 2/2 + part 0 corner -x-y | 0.83 | 0.75 | 0.58 | 0.17 |
| sphere | sector 135 + sector 225 | 1.00 | 1.00 | 0.83 | 0.83 |
| cylinder | part 0 corner -x-y + part 0 -x seg 2/2 | 0.42 | 0.25 | 0.25 | 0.25 |
| arch | part 3 -x + part 2 -x | 0.67 | 0.75 | 0.67 | 0.50 |
| dumbbell | part 0 -x + part 1 -x | 0.67 | 0.25 | 0.25 | 0.17 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.67 | 0.75 | 0.42 | 0.00 |
| beam (unseen) | part 0 -x seg 2/5 + part 0 -x seg 4/5 | 0.25 | 0.25 | 0.00 | 0.00 |
| l_shape (unseen) | part 1 -x + part 0 corner -x-y | 0.83 | 0.50 | 0.25 | 0.00 |
| asym (unseen) | part 1 -x + part 0 corner -x+y | 0.83 | 0.33 | 0.00 | 0.00 |
| u_channel (unseen) | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.50 | 0.42 | 0.33 | 0.08 |
| plus (unseen) | part 0 corner -x-y + part 0 corner -x+y | 0.75 | 0.42 | 0.42 | 0.25 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.69 | 0.28 | 0.02 | 0.00 | 0.00 | 0.00 | 6.17 |
| 40 kg | 0.53 | 0.44 | 0.03 | 0.00 | 0.00 | 0.01 | 4.53 |
| 60 kg | 0.39 | 0.53 | 0.08 | 0.00 | 0.00 | 0.01 | 3.08 |
| 80 kg | 0.19 | 0.67 | 0.14 | 0.00 | 0.00 | 0.00 | 1.61 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.29 | 0.75 | 0.84 | 0.00 | 1.00 | 0.26 | 0.73 | 0.84 | 0.00 |
| 40 kg | 1.00 | 0.26 | 0.79 | 0.89 | 0.00 | 1.00 | 0.28 | 0.75 | 0.85 | 0.00 |
| 60 kg | 1.00 | 0.24 | 0.81 | 0.92 | 0.00 | 1.00 | 0.27 | 0.74 | 0.87 | 0.00 |
| 80 kg | 1.00 | 0.19 | 0.84 | 0.95 | 0.00 | 1.00 | 0.20 | 0.82 | 0.93 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.96 | 1.42 | 0.01 | 0.97 | 1.76 | 0.03 |
| 40 kg | 0.95 | 1.20 | 0.02 | 0.94 | 1.26 | 0.03 |
| 60 kg | 0.95 | 0.97 | 0.02 | 0.93 | 1.12 | 0.03 |
| 80 kg | 0.97 | 0.32 | 0.02 | 0.96 | 0.41 | 0.01 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.67 | 0.65 | 0.25 |
| 40 kg | 0.73 | 0.65 | 0.22 |
| 60 kg | 0.79 | 0.70 | 0.20 |
| 80 kg | 0.82 | 0.78 | 0.18 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.29 | 0.44 | 0.53 | 0.54 |
| long | 0.30 | 0.43 | 0.64 | 0.79 |
| sphere | 0.36 | 0.56 | 0.59 | 0.64 |
| cylinder | 0.27 | 0.29 | 0.37 | 0.65 |
| arch | 0.10 | 0.27 | 0.28 | 0.22 |
| dumbbell | 0.09 | 0.13 | 0.05 | 0.21 |
| t_shape | 0.38 | 0.43 | 0.62 | 0.77 |
| beam | 0.21 | 0.21 | 0.34 | 0.46 |
| l_shape | 0.18 | 0.18 | 0.14 | 0.20 |
| asym | 0.44 | 0.37 | 0.42 | 0.54 |
| u_channel | 0.22 | 0.23 | 0.35 | 0.44 |
| plus | 0.17 | 0.14 | 0.20 | 0.29 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.83 | 0.75 | 0.58 | 0.39 |
| B_left | 0.67 | 0.42 | 0.33 | 0.11 |
| C_backright | 0.69 | 0.64 | 0.39 | 0.19 |
| D_far_turn | 0.58 | 0.33 | 0.25 | 0.08 |
