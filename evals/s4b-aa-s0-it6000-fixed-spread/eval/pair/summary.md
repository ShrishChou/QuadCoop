# Pair evaluation: s4b-aa-s0-it6000-fixed-spread

policy: Stage 4 contact policy logs/marl2/s4b_aa_s0/model_6000.pt (robots start at their contacts; contact rule re-applied: never)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.44 | 0.45 | 0.07 | 0.02 | 13.8 | 0.02 | 0.40 | 0.44 | 0.27 | 0.52 | 1.05 |
| 40 kg | 0.34 | 0.32 | 0.07 | 0.09 | 16.1 | 0.01 | 0.47 | 0.52 | 0.32 | 0.50 | 1.07 |
| 60 kg | 0.23 | 0.19 | 0.14 | 0.13 | 21.3 | 0.01 | 0.55 | 0.59 | 0.36 | 0.48 | 1.09 |
| 80 kg | 0.15 | 0.14 | 0.17 | 0.19 | 28.1 | 0.00 | 0.57 | 0.65 | 0.39 | 0.50 | 1.11 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x-y + part 0 corner -x+y | 1.00 | 0.75 | 0.25 | 0.08 |
| long | part 0 corner -x-y + part 0 corner -x+y | 0.58 | 0.25 | 0.33 | 0.17 |
| sphere | sector 135 + sector 225 | 1.00 | 1.00 | 1.00 | 0.83 |
| cylinder | part 0 corner -x+y + part 0 corner -x-y | 0.08 | 0.00 | 0.08 | 0.08 |
| arch | part 3 -x + part 2 -x | 0.33 | 0.33 | 0.33 | 0.25 |
| dumbbell | part 0 -x + part 1 -x | 0.25 | 0.17 | 0.33 | 0.17 |
| t_shape | part 0 corner -x+y + part 0 corner -x-y | 0.58 | 0.42 | 0.00 | 0.00 |
| beam (unseen) | part 0 -x seg 5/5 + part 0 -x seg 1/5 | 0.33 | 0.17 | 0.00 | 0.00 |
| l_shape (unseen) | part 0 corner -x-y + part 0 corner -x+y | 0.25 | 0.00 | 0.00 | 0.00 |
| asym (unseen) | part 0 corner -x+y + part 1 corner -x-y | 0.25 | 0.25 | 0.00 | 0.00 |
| u_channel (unseen) | part 0 corner -x-y + part 0 corner -x+y | 0.17 | 0.17 | 0.00 | 0.00 |
| plus (unseen) | part 0 corner -x-y + part 0 corner -x+y | 0.50 | 0.58 | 0.42 | 0.17 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.44 | 0.46 | 0.09 | 0.01 | 0.00 | 0.26 | 0.00 |
| 40 kg | 0.34 | 0.49 | 0.16 | 0.01 | 0.00 | 0.22 | 0.00 |
| 60 kg | 0.23 | 0.49 | 0.27 | 0.01 | 0.00 | 0.05 | 0.00 |
| 80 kg | 0.15 | 0.49 | 0.36 | 0.00 | 0.00 | 0.01 | 0.00 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.35 | 0.58 | 0.68 | 0.00 | 1.00 | 0.34 | 0.52 | 0.70 | 0.00 |
| 40 kg | 1.00 | 0.29 | 0.60 | 0.72 | 0.00 | 1.00 | 0.33 | 0.53 | 0.70 | 0.00 |
| 60 kg | 1.00 | 0.31 | 0.58 | 0.73 | 0.00 | 1.00 | 0.32 | 0.56 | 0.73 | 0.00 |
| 80 kg | 1.00 | 0.30 | 0.58 | 0.74 | 0.00 | 1.00 | 0.33 | 0.52 | 0.74 | 0.00 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.42 | 0.42 | 0.40 | 0.31 |
| long | 0.28 | 0.29 | 0.40 | 0.36 |
| sphere | 0.64 | 0.77 | 0.86 | 0.74 |
| cylinder | 0.17 | 0.24 | 0.33 | 0.32 |
| arch | 0.28 | 0.31 | 0.32 | 0.40 |
| dumbbell | 0.28 | 0.27 | 0.34 | 0.41 |
| t_shape | 0.30 | 0.29 | 0.15 | 0.34 |
| beam | 0.23 | 0.25 | 0.40 | 0.55 |
| l_shape | 0.11 | 0.12 | 0.12 | 0.30 |
| asym | 0.22 | 0.37 | 0.42 | 0.50 |
| u_channel | 0.12 | 0.17 | 0.14 | 0.30 |
| plus | 0.19 | 0.32 | 0.39 | 0.23 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.67 | 0.67 | 0.42 | 0.36 |
| B_left | 0.39 | 0.22 | 0.25 | 0.08 |
| C_backright | 0.33 | 0.25 | 0.14 | 0.08 |
| D_far_turn | 0.39 | 0.22 | 0.11 | 0.06 |
