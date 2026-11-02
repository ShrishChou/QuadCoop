# Pair evaluation: game-s4b-allpairs

policy: Stage 4 contact policy logs/marl2/s4b_aa_s0/model_6000.pt (robots start at their contacts; contact rule re-applied: never)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 40 kg | 0.20 | 0.18 | 0.10 | 0.07 | 24.8 | 0.01 | 0.32 | 0.39 | 0.17 | 0.34 | 1.08 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 40 kg |
|---|---|---|
| cube | part 0 corner -x-y + part 0 corner -x+y | 0.69 |
| long | part 0 -x seg 1/2 + part 0 corner -x+y | 0.47 |
| sphere | sector 225 + sector 135 | 0.94 |
| cylinder | part 0 -x seg 1/2 + part 0 corner -x+y | 0.13 |
| arch | part 3 corner -x+y + part 3 corner -x-y | 0.26 |
| dumbbell | part 1 corner -x+y + part 1 corner -x-y | 0.15 |
| t_shape | part 0 -x seg 1/3 + part 0 corner -x+y | 0.25 |
| beam (unseen) | part 0 -x seg 3/5 + part 0 -x seg 1/5 | 0.07 |
| l_shape (unseen) | part 0 -x seg 1/2 + part 0 corner -x+y | 0.10 |
| asym (unseen) | part 1 -x + part 0 corner -x+y | 0.21 |
| u_channel (unseen) | part 0 -x seg 1/3 + part 0 corner -x+y | 0.14 |
| plus (unseen) | part 1 -x + part 0 corner -x-y | 0.30 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 40 kg | 0.20 | 0.63 | 0.17 | 0.00 | 0.00 | 0.14 | 0.00 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 40 kg | 1.00 | 0.47 | 0.44 | 0.65 | 0.00 | 1.00 | 0.43 | 0.44 | 0.70 | 0.00 |

## both robots pushing (share of time) by object and mass

| object | 40 kg |
|---|---|
| cube | 0.38 |
| long | 0.27 |
| sphere | 0.73 |
| cylinder | 0.25 |
| arch | 0.14 |
| dumbbell | 0.15 |
| t_shape | 0.16 |
| beam | 0.19 |
| l_shape | 0.10 |
| asym | 0.22 |
| u_channel | 0.11 |
| plus | 0.16 |

## success by scenario and mass

| scenario | 40 kg |
|---|---|
| A_straight | 0.42 |
| B_left | 0.17 |
| C_backright | 0.13 |
| D_far_turn | 0.11 |
