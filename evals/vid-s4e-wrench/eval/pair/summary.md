# Pair evaluation: vid-s4e-wrench

policy: Stage 4 contact policy logs/marl2/s4e_aa_s0/model_12000.pt (robots start at their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 1 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 40 kg | 0.54 | 0.52 | 0.00 | 0.02 | 27.8 | 0.02 | 0.64 | 0.49 | 0.31 | 0.43 | 1.01 |
| 60 kg | 0.52 | 0.35 | 0.02 | 0.00 | 37.3 | 0.01 | 0.69 | 0.57 | 0.33 | 0.38 | 0.96 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 40 kg | 60 kg |
|---|---|---|---|
| cube | part 0 corner -x+y + part 0 corner -x-y | 0.50 | 0.50 |
| long | part 0 -x seg 2/2 + part 0 corner -x-y | 0.50 | 1.00 |
| sphere | sector 225 + sector 135 | 1.00 | 1.00 |
| cylinder | part 0 -x seg 2/2 + part 0 corner -x-y | 0.50 | 0.25 |
| arch | part 2 -x + part 3 -x | 0.75 | 0.50 |
| dumbbell | part 0 -x + part 1 -x | 0.25 | 0.50 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.50 | 0.50 |
| beam (unseen) | part 0 -x seg 2/5 + part 0 -x seg 4/5 | 0.00 | 0.00 |
| l_shape (unseen) | part 0 corner -x-y + part 1 -x | 0.75 | 0.75 |
| asym (unseen) | part 1 corner -x-y + part 0 -x | 0.50 | 0.50 |
| u_channel (unseen) | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.75 | 0.25 |
| plus (unseen) | part 1 corner -x+y + part 1 corner -x-y | 0.50 | 0.50 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 40 kg | 0.54 | 0.44 | 0.02 | 0.00 | 0.00 | 0.00 | 4.83 |
| 60 kg | 0.52 | 0.46 | 0.02 | 0.00 | 0.00 | 0.00 | 3.38 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 40 kg | 1.00 | 0.23 | 0.80 | 0.87 | 0.00 | 1.00 | 0.28 | 0.77 | 0.85 | 0.00 |
| 60 kg | 1.00 | 0.23 | 0.84 | 0.90 | 0.00 | 1.00 | 0.15 | 0.89 | 0.96 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 40 kg | 0.94 | 1.28 | 0.04 | 0.93 | 0.97 | 0.03 |
| 60 kg | 0.95 | 1.31 | 0.03 | 0.99 | 0.88 | 0.03 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 40 kg | 0.70 | 0.67 | 0.23 |
| 60 kg | 0.77 | 0.78 | 0.21 |

## both robots pushing (share of time) by object and mass

| object | 40 kg | 60 kg |
|---|---|---|
| cube | 0.11 | 0.23 |
| long | 0.15 | 0.45 |
| sphere | 0.64 | 0.66 |
| cylinder | 0.73 | 0.63 |
| arch | 0.20 | 0.14 |
| dumbbell | 0.07 | 0.13 |
| t_shape | 0.52 | 0.69 |
| beam | 0.30 | 0.36 |
| l_shape | 0.23 | 0.08 |
| asym | 0.41 | 0.24 |
| u_channel | 0.31 | 0.28 |
| plus | 0.10 | 0.12 |

## success by scenario and mass

| scenario | 40 kg | 60 kg |
|---|---|---|
| A_straight | 0.75 | 0.75 |
| B_left | 0.67 | 0.50 |
| C_backright | 0.42 | 0.58 |
| D_far_turn | 0.33 | 0.25 |
