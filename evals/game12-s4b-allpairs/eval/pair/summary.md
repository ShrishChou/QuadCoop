# Pair evaluation: game12-s4b-allpairs

policy: Stage 4 contact policy logs/marl2/s4b_aa_s0/model_6000.pt (robots start at their contacts; contact rule re-applied: never)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 12 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 40 kg | 0.17 | 0.15 | 0.10 | 0.08 | 25.2 | 0.01 | 0.30 | 0.36 | 0.15 | 0.32 | 1.14 |
| 70 kg | 0.05 | 0.04 | 0.18 | 0.18 | 37.5 | 0.01 | 0.44 | 0.49 | 0.23 | 0.35 | 1.15 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 40 kg | 70 kg |
|---|---|---|---|
| u_channel (unseen) | part 0 -x seg 1/3 + part 0 corner -x+y | 0.15 | 0.03 |
| l_shape (unseen) | part 0 -x seg 1/2 + part 0 corner -x+y | 0.13 | 0.01 |
| plus (unseen) | part 1 -x + part 0 corner -x-y | 0.31 | 0.12 |
| beam (unseen) | part 0 -x seg 3/5 + part 0 -x seg 1/5 | 0.08 | 0.00 |
| t_shape | part 0 -x seg 1/3 + part 0 corner -x+y | 0.25 | 0.09 |
| arch | part 3 corner -x+y + part 3 corner -x-y | 0.23 | 0.12 |
| dumbbell | part 1 corner -x+y + part 1 corner -x-y | 0.16 | 0.06 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 40 kg | 0.17 | 0.66 | 0.17 | 0.00 | 0.00 | 0.14 | 0.00 |
| 70 kg | 0.05 | 0.58 | 0.36 | 0.00 | 0.00 | 0.01 | 0.00 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 40 kg | 1.00 | 0.49 | 0.42 | 0.64 | 0.00 | 1.00 | 0.44 | 0.41 | 0.69 | 0.00 |
| 70 kg | 1.00 | 0.41 | 0.45 | 0.67 | 0.00 | 1.00 | 0.43 | 0.42 | 0.72 | 0.00 |

## both robots pushing (share of time) by object and mass

| object | 40 kg | 70 kg |
|---|---|---|
| u_channel | 0.11 | 0.17 |
| l_shape | 0.10 | 0.14 |
| plus | 0.17 | 0.22 |
| beam | 0.20 | 0.42 |
| t_shape | 0.16 | 0.21 |
| arch | 0.14 | 0.16 |
| dumbbell | 0.16 | 0.22 |

## success by scenario and mass

| scenario | 40 kg | 70 kg |
|---|---|---|
| A_straight | 0.41 | 0.20 |
| B_left | 0.12 | 0.03 |
| C_backright | 0.12 | 0.02 |
| D_far_turn | 0.09 | 0.01 |
