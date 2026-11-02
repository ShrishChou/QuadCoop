# Pair evaluation: s4b-aa-s0-it6000-spread

policy: Stage 4 contact policy logs/marl2/s4b_aa_s0/model_6000.pt (robots start at their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.53 | 0.52 | 0.03 | 0.03 | 17.3 | 0.02 | 0.42 | 0.50 | 0.30 | 0.53 | 1.03 |
| 40 kg | 0.48 | 0.46 | 0.05 | 0.05 | 22.0 | 0.02 | 0.48 | 0.55 | 0.34 | 0.54 | 1.03 |
| 60 kg | 0.28 | 0.24 | 0.10 | 0.17 | 26.6 | 0.01 | 0.51 | 0.63 | 0.35 | 0.47 | 1.05 |
| 80 kg | 0.14 | 0.13 | 0.13 | 0.19 | 23.4 | 0.00 | 0.58 | 0.64 | 0.37 | 0.46 | 1.09 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x-y + part 0 corner -x+y | 0.92 | 0.92 | 0.50 | 0.00 |
| long | part 0 corner -x-y + part 0 corner -x+y | 0.67 | 0.50 | 0.33 | 0.08 |
| sphere | sector 135 + sector 225 | 1.00 | 1.00 | 0.92 | 0.92 |
| cylinder | part 0 corner -x+y + part 0 corner -x-y | 0.08 | 0.25 | 0.17 | 0.17 |
| arch | part 3 -x + part 2 -x | 0.25 | 0.67 | 0.25 | 0.25 |
| dumbbell | part 0 -x + part 1 -x | 0.42 | 0.42 | 0.42 | 0.17 |
| t_shape | part 0 corner -x+y + part 0 corner -x-y | 0.50 | 0.58 | 0.17 | 0.00 |
| beam (unseen) | part 0 -x seg 5/5 + part 0 -x seg 1/5 | 0.42 | 0.33 | 0.08 | 0.00 |
| l_shape (unseen) | part 0 corner -x-y + part 0 corner -x+y | 0.67 | 0.08 | 0.00 | 0.00 |
| asym (unseen) | part 0 corner -x+y + part 1 corner -x-y | 0.42 | 0.17 | 0.08 | 0.00 |
| u_channel (unseen) | part 0 corner -x-y + part 0 corner -x+y | 0.33 | 0.33 | 0.08 | 0.00 |
| plus (unseen) | part 0 corner -x-y + part 0 corner -x+y | 0.67 | 0.50 | 0.42 | 0.08 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.53 | 0.40 | 0.06 | 0.01 | 0.00 | 0.19 | 3.51 |
| 40 kg | 0.48 | 0.42 | 0.10 | 0.00 | 0.00 | 0.16 | 2.89 |
| 60 kg | 0.28 | 0.44 | 0.28 | 0.00 | 0.00 | 0.03 | 1.88 |
| 80 kg | 0.14 | 0.54 | 0.32 | 0.00 | 0.00 | 0.01 | 1.38 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.46 | 0.48 | 0.65 | 0.00 | 1.00 | 0.41 | 0.48 | 0.66 | 0.00 |
| 40 kg | 1.00 | 0.42 | 0.50 | 0.67 | 0.00 | 1.00 | 0.45 | 0.47 | 0.66 | 0.00 |
| 60 kg | 1.00 | 0.44 | 0.44 | 0.64 | 0.00 | 1.00 | 0.41 | 0.46 | 0.70 | 0.00 |
| 80 kg | 1.00 | 0.35 | 0.52 | 0.69 | 0.00 | 1.00 | 0.40 | 0.45 | 0.70 | 0.00 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.44 | 0.53 | 0.42 | 0.38 |
| long | 0.28 | 0.38 | 0.47 | 0.37 |
| sphere | 0.77 | 0.82 | 0.74 | 0.76 |
| cylinder | 0.16 | 0.39 | 0.22 | 0.41 |
| arch | 0.28 | 0.33 | 0.30 | 0.40 |
| dumbbell | 0.28 | 0.32 | 0.37 | 0.35 |
| t_shape | 0.26 | 0.17 | 0.31 | 0.25 |
| beam | 0.26 | 0.38 | 0.44 | 0.48 |
| l_shape | 0.20 | 0.09 | 0.16 | 0.20 |
| asym | 0.20 | 0.26 | 0.35 | 0.35 |
| u_channel | 0.15 | 0.16 | 0.19 | 0.21 |
| plus | 0.27 | 0.24 | 0.23 | 0.28 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.83 | 0.72 | 0.58 | 0.33 |
| B_left | 0.39 | 0.36 | 0.19 | 0.08 |
| C_backright | 0.44 | 0.44 | 0.28 | 0.08 |
| D_far_turn | 0.44 | 0.39 | 0.08 | 0.06 |
