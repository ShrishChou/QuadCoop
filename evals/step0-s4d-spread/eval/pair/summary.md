# Pair evaluation: step0-s4d-spread

policy: Stage 4 contact policy logs/marl2/s4d_aa_s0/model_9000.pt (robots start at their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.56 | 0.51 | 0.01 | 0.02 | 26.0 | 0.02 | 0.48 | 0.53 | 0.28 | 0.43 | 1.07 |
| 40 kg | 0.51 | 0.42 | 0.02 | 0.02 | 28.4 | 0.02 | 0.60 | 0.63 | 0.40 | 0.53 | 1.05 |
| 60 kg | 0.31 | 0.22 | 0.06 | 0.06 | 33.6 | 0.01 | 0.69 | 0.72 | 0.50 | 0.58 | 1.05 |
| 80 kg | 0.14 | 0.12 | 0.12 | 0.06 | 29.9 | 0.01 | 0.79 | 0.79 | 0.62 | 0.67 | 1.08 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x-y + part 0 corner -x+y | 0.92 | 0.83 | 0.67 | 0.08 |
| long | part 0 corner -x-y + part 0 corner -x+y | 0.67 | 0.42 | 0.25 | 0.17 |
| sphere | sector 135 + sector 225 | 1.00 | 0.92 | 0.67 | 0.83 |
| cylinder | part 0 corner -x+y + part 0 corner -x-y | 0.33 | 0.17 | 0.08 | 0.17 |
| arch | part 3 -x + part 2 -x | 0.42 | 0.33 | 0.17 | 0.17 |
| dumbbell | part 0 -x + part 1 -x | 0.33 | 0.33 | 0.33 | 0.17 |
| t_shape | part 0 corner -x+y + part 0 corner -x-y | 0.33 | 0.33 | 0.17 | 0.00 |
| beam (unseen) | part 0 -x seg 5/5 + part 0 -x seg 1/5 | 0.58 | 0.25 | 0.08 | 0.00 |
| l_shape (unseen) | part 0 corner -x-y + part 0 corner -x+y | 0.58 | 0.67 | 0.25 | 0.00 |
| asym (unseen) | part 0 corner -x+y + part 1 corner -x-y | 0.42 | 0.42 | 0.17 | 0.00 |
| u_channel (unseen) | part 0 corner -x-y + part 0 corner -x+y | 0.42 | 0.75 | 0.50 | 0.08 |
| plus (unseen) | part 0 corner -x-y + part 0 corner -x+y | 0.67 | 0.67 | 0.42 | 0.00 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.56 | 0.42 | 0.03 | 0.00 | 0.00 | 0.04 | 9.39 |
| 40 kg | 0.51 | 0.44 | 0.04 | 0.01 | 0.00 | 0.01 | 7.23 |
| 60 kg | 0.31 | 0.56 | 0.12 | 0.00 | 0.00 | 0.01 | 4.07 |
| 80 kg | 0.14 | 0.68 | 0.18 | 0.00 | 0.00 | 0.00 | 2.76 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.48 | 0.65 | 0.79 | 0.00 | 1.00 | 0.33 | 0.70 | 0.84 | 0.00 |
| 40 kg | 1.00 | 0.36 | 0.72 | 0.87 | 0.00 | 1.00 | 0.31 | 0.74 | 0.89 | 0.00 |
| 60 kg | 1.00 | 0.30 | 0.78 | 0.92 | 0.00 | 1.00 | 0.22 | 0.81 | 0.95 | 0.00 |
| 80 kg | 1.00 | 0.20 | 0.83 | 0.96 | 0.00 | 1.00 | 0.16 | 0.85 | 0.97 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.95 | 2.48 | 0.02 | 0.96 | 1.97 | 0.01 |
| 40 kg | 0.97 | 2.12 | 0.02 | 0.96 | 2.04 | 0.02 |
| 60 kg | 0.96 | 1.24 | 0.02 | 0.96 | 1.21 | 0.01 |
| 80 kg | 0.97 | 0.82 | 0.01 | 0.97 | 0.77 | 0.01 |

## pressing the contact (front on the object while on its contact, share of time)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.56 | 0.59 |  |
| 40 kg | 0.66 | 0.68 |  |
| 60 kg | 0.75 | 0.77 |  |
| 80 kg | 0.85 | 0.85 |  |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.37 | 0.48 | 0.70 | 0.88 |
| long | 0.35 | 0.59 | 0.65 | 0.71 |
| sphere | 0.39 | 0.65 | 0.76 | 0.75 |
| cylinder | 0.33 | 0.49 | 0.77 | 0.80 |
| arch | 0.15 | 0.21 | 0.23 | 0.39 |
| dumbbell | 0.18 | 0.29 | 0.28 | 0.36 |
| t_shape | 0.28 | 0.47 | 0.50 | 0.79 |
| beam | 0.21 | 0.35 | 0.22 | 0.38 |
| l_shape | 0.31 | 0.22 | 0.28 | 0.40 |
| asym | 0.28 | 0.37 | 0.63 | 0.76 |
| u_channel | 0.26 | 0.30 | 0.61 | 0.72 |
| plus | 0.27 | 0.38 | 0.39 | 0.54 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.75 | 0.75 | 0.67 | 0.36 |
| B_left | 0.56 | 0.44 | 0.25 | 0.06 |
| C_backright | 0.50 | 0.42 | 0.28 | 0.08 |
| D_far_turn | 0.42 | 0.42 | 0.06 | 0.06 |
