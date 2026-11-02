# Pair evaluation: s4b-aa-s0-it6000-fixed-random

policy: Stage 4 contact policy logs/marl2/s4b_aa_s0/model_6000.pt (robots start at their contacts; contact rule re-applied: never)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.41 | 0.40 | 0.05 | 0.06 | 12.9 | 0.02 | 0.39 | 0.42 | 0.25 | 0.49 | 0.95 |
| 40 kg | 0.35 | 0.33 | 0.08 | 0.07 | 15.8 | 0.02 | 0.42 | 0.50 | 0.28 | 0.46 | 0.94 |
| 60 kg | 0.21 | 0.18 | 0.14 | 0.11 | 21.5 | 0.01 | 0.50 | 0.56 | 0.30 | 0.42 | 0.97 |
| 80 kg | 0.15 | 0.15 | 0.20 | 0.18 | 22.3 | 0.01 | 0.58 | 0.62 | 0.38 | 0.48 | 0.98 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x-y + part 0 corner -x+y | 0.92 | 0.83 | 0.25 | 0.08 |
| long | part 0 -x seg 2/2 + part 0 corner -x-y | 0.50 | 0.42 | 0.17 | 0.08 |
| sphere | sector 225 + sector 135 | 1.00 | 1.00 | 0.83 | 0.92 |
| cylinder | part 0 -x seg 1/2 + part 0 corner -x+y | 0.00 | 0.17 | 0.08 | 0.08 |
| arch | part 3 corner -x+y + part 2 -x | 0.33 | 0.33 | 0.25 | 0.25 |
| dumbbell | part 0 -x + part 1 corner -x-y | 0.25 | 0.17 | 0.25 | 0.17 |
| t_shape | part 0 corner -x-y + part 0 -x seg 3/3 | 0.25 | 0.33 | 0.25 | 0.08 |
| beam (unseen) | part 0 -x seg 5/5 + part 0 -x seg 3/5 | 0.00 | 0.08 | 0.00 | 0.00 |
| l_shape (unseen) | part 0 corner -x+y + part 0 corner -x-y | 0.33 | 0.00 | 0.00 | 0.00 |
| asym (unseen) | part 1 corner -x-y + part 0 -x | 0.50 | 0.17 | 0.00 | 0.00 |
| u_channel (unseen) | part 0 -x seg 3/3 + part 0 corner -x-y | 0.25 | 0.33 | 0.00 | 0.00 |
| plus (unseen) | part 1 corner -x+y + part 0 corner -x-y | 0.58 | 0.42 | 0.42 | 0.17 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.41 | 0.47 | 0.11 | 0.01 | 0.00 | 0.19 | 0.00 |
| 40 kg | 0.35 | 0.49 | 0.15 | 0.01 | 0.00 | 0.12 | 0.00 |
| 60 kg | 0.21 | 0.54 | 0.25 | 0.00 | 0.00 | 0.04 | 0.00 |
| 80 kg | 0.15 | 0.47 | 0.38 | 0.00 | 0.00 | 0.03 | 0.00 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.39 | 0.55 | 0.71 | 0.00 | 1.00 | 0.33 | 0.56 | 0.71 | 0.00 |
| 40 kg | 1.00 | 0.38 | 0.54 | 0.72 | 0.00 | 1.00 | 0.32 | 0.57 | 0.74 | 0.00 |
| 60 kg | 1.00 | 0.37 | 0.50 | 0.73 | 0.00 | 1.00 | 0.32 | 0.56 | 0.75 | 0.00 |
| 80 kg | 1.00 | 0.35 | 0.51 | 0.72 | 0.00 | 1.00 | 0.32 | 0.57 | 0.80 | 0.00 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.40 | 0.37 | 0.32 | 0.41 |
| long | 0.26 | 0.25 | 0.29 | 0.34 |
| sphere | 0.71 | 0.73 | 0.70 | 0.70 |
| cylinder | 0.15 | 0.30 | 0.29 | 0.31 |
| arch | 0.24 | 0.26 | 0.27 | 0.37 |
| dumbbell | 0.15 | 0.34 | 0.29 | 0.43 |
| t_shape | 0.18 | 0.17 | 0.22 | 0.32 |
| beam | 0.05 | 0.16 | 0.35 | 0.40 |
| l_shape | 0.13 | 0.09 | 0.14 | 0.26 |
| asym | 0.39 | 0.26 | 0.33 | 0.33 |
| u_channel | 0.11 | 0.22 | 0.17 | 0.37 |
| plus | 0.19 | 0.22 | 0.23 | 0.28 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.67 | 0.58 | 0.36 | 0.31 |
| B_left | 0.42 | 0.28 | 0.17 | 0.08 |
| C_backright | 0.28 | 0.28 | 0.19 | 0.11 |
| D_far_turn | 0.28 | 0.28 | 0.11 | 0.11 |
