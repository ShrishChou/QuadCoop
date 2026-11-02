# Pair evaluation: s4b-aa-s0-it6000-adjacent

policy: Stage 4 contact policy logs/marl2/s4b_aa_s0/model_6000.pt (robots start at their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.51 | 0.49 | 0.04 | 0.02 | 20.0 | 0.03 | 0.38 | 0.45 | 0.24 | 0.45 | 0.91 |
| 40 kg | 0.44 | 0.39 | 0.08 | 0.06 | 19.5 | 0.03 | 0.47 | 0.56 | 0.33 | 0.51 | 0.90 |
| 60 kg | 0.26 | 0.22 | 0.15 | 0.14 | 31.5 | 0.02 | 0.51 | 0.62 | 0.35 | 0.48 | 0.91 |
| 80 kg | 0.12 | 0.11 | 0.19 | 0.22 | 32.3 | 0.01 | 0.56 | 0.64 | 0.38 | 0.48 | 0.90 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x-y + part 0 corner -x+y | 1.00 | 0.83 | 0.33 | 0.00 |
| long | part 0 -x seg 2/2 + part 0 corner -x-y | 0.58 | 0.33 | 0.25 | 0.17 |
| sphere | sector 135 + sector 225 | 0.92 | 1.00 | 0.92 | 0.58 |
| cylinder | part 0 corner -x-y + part 0 -x seg 2/2 | 0.33 | 0.25 | 0.17 | 0.17 |
| arch | part 2 -x + part 3 -x | 0.67 | 0.50 | 0.42 | 0.25 |
| dumbbell | part 2 -x seg 2/3 + part 0 -x | 0.17 | 0.50 | 0.08 | 0.08 |
| t_shape | part 0 corner -x-y + part 0 -x seg 2/3 | 0.42 | 0.25 | 0.08 | 0.00 |
| beam (unseen) | part 0 -x seg 1/5 + part 0 -x seg 3/5 | 0.17 | 0.17 | 0.00 | 0.00 |
| l_shape (unseen) | part 0 corner -x-y + part 0 -x seg 2/2 | 0.25 | 0.25 | 0.25 | 0.08 |
| asym (unseen) | part 1 -x + part 0 corner -x+y | 0.67 | 0.42 | 0.17 | 0.00 |
| u_channel (unseen) | part 0 corner -x+y + part 0 -x seg 2/3 | 0.42 | 0.50 | 0.17 | 0.00 |
| plus (unseen) | part 1 corner -x-y + part 1 corner -x+y | 0.50 | 0.33 | 0.25 | 0.17 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.51 | 0.43 | 0.06 | 0.00 | 0.00 | 0.22 | 3.21 |
| 40 kg | 0.44 | 0.42 | 0.14 | 0.00 | 0.00 | 0.14 | 2.38 |
| 60 kg | 0.26 | 0.45 | 0.29 | 0.00 | 0.00 | 0.06 | 1.53 |
| 80 kg | 0.12 | 0.47 | 0.40 | 0.00 | 0.00 | 0.02 | 0.95 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.49 | 0.43 | 0.63 | 0.00 | 1.00 | 0.49 | 0.46 | 0.61 | 0.00 |
| 40 kg | 1.00 | 0.48 | 0.42 | 0.68 | 0.00 | 1.00 | 0.44 | 0.46 | 0.67 | 0.00 |
| 60 kg | 1.00 | 0.50 | 0.39 | 0.68 | 0.00 | 1.00 | 0.45 | 0.43 | 0.68 | 0.00 |
| 80 kg | 1.00 | 0.41 | 0.45 | 0.68 | 0.00 | 1.00 | 0.40 | 0.51 | 0.74 | 0.00 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.43 | 0.51 | 0.34 | 0.45 |
| long | 0.25 | 0.23 | 0.35 | 0.31 |
| sphere | 0.76 | 0.77 | 0.82 | 0.81 |
| cylinder | 0.18 | 0.28 | 0.31 | 0.29 |
| arch | 0.30 | 0.28 | 0.39 | 0.39 |
| dumbbell | 0.06 | 0.26 | 0.19 | 0.40 |
| t_shape | 0.15 | 0.19 | 0.17 | 0.20 |
| beam | 0.17 | 0.39 | 0.67 | 0.63 |
| l_shape | 0.06 | 0.16 | 0.24 | 0.22 |
| asym | 0.29 | 0.47 | 0.37 | 0.46 |
| u_channel | 0.09 | 0.17 | 0.16 | 0.21 |
| plus | 0.10 | 0.19 | 0.20 | 0.15 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.67 | 0.67 | 0.44 | 0.28 |
| B_left | 0.53 | 0.44 | 0.19 | 0.03 |
| C_backright | 0.42 | 0.36 | 0.28 | 0.17 |
| D_far_turn | 0.42 | 0.31 | 0.11 | 0.03 |
