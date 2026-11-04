# Pair evaluation: s4e-aa-s0-spread

policy: Stage 4 contact policy logs/marl2/s4e_aa_s0/model_12000.pt (robots start at their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.41 | 0.38 | 0.00 | 0.03 | 22.6 | 0.03 | 0.48 | 0.45 | 0.27 | 0.45 | 1.07 |
| 40 kg | 0.40 | 0.35 | 0.03 | 0.03 | 21.4 | 0.02 | 0.58 | 0.56 | 0.35 | 0.48 | 1.06 |
| 60 kg | 0.34 | 0.28 | 0.03 | 0.03 | 30.2 | 0.02 | 0.69 | 0.64 | 0.43 | 0.49 | 1.07 |
| 80 kg | 0.20 | 0.17 | 0.06 | 0.04 | 31.8 | 0.01 | 0.74 | 0.78 | 0.56 | 0.60 | 1.09 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x-y + part 0 corner -x+y | 0.67 | 0.75 | 0.58 | 0.17 |
| long | part 0 corner -x-y + part 0 corner -x+y | 0.50 | 0.33 | 0.42 | 0.17 |
| sphere | sector 135 + sector 225 | 0.92 | 1.00 | 0.92 | 0.92 |
| cylinder | part 0 corner -x+y + part 0 corner -x-y | 0.25 | 0.25 | 0.25 | 0.25 |
| arch | part 3 -x + part 2 -x | 0.25 | 0.25 | 0.17 | 0.17 |
| dumbbell | part 0 -x + part 1 -x | 0.33 | 0.25 | 0.25 | 0.17 |
| t_shape | part 0 corner -x+y + part 0 corner -x-y | 0.25 | 0.42 | 0.33 | 0.17 |
| beam (unseen) | part 0 -x seg 5/5 + part 0 -x seg 1/5 | 0.33 | 0.25 | 0.08 | 0.00 |
| l_shape (unseen) | part 0 corner -x-y + part 0 corner -x+y | 0.42 | 0.42 | 0.17 | 0.00 |
| asym (unseen) | part 0 corner -x+y + part 1 corner -x-y | 0.25 | 0.17 | 0.08 | 0.00 |
| u_channel (unseen) | part 0 corner -x-y + part 0 corner -x+y | 0.33 | 0.58 | 0.42 | 0.25 |
| plus (unseen) | part 0 corner -x-y + part 0 corner -x+y | 0.42 | 0.17 | 0.42 | 0.17 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.41 | 0.56 | 0.03 | 0.00 | 0.00 | 0.06 | 7.66 |
| 40 kg | 0.40 | 0.54 | 0.06 | 0.00 | 0.00 | 0.01 | 6.45 |
| 60 kg | 0.34 | 0.59 | 0.07 | 0.00 | 0.00 | 0.00 | 4.56 |
| 80 kg | 0.20 | 0.70 | 0.10 | 0.00 | 0.00 | 0.01 | 3.42 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.41 | 0.67 | 0.77 | 0.00 | 1.00 | 0.43 | 0.64 | 0.74 | 0.00 |
| 40 kg | 1.00 | 0.37 | 0.72 | 0.81 | 0.00 | 1.00 | 0.39 | 0.68 | 0.79 | 0.00 |
| 60 kg | 1.00 | 0.28 | 0.78 | 0.88 | 0.00 | 1.00 | 0.31 | 0.76 | 0.86 | 0.00 |
| 80 kg | 1.00 | 0.25 | 0.81 | 0.89 | 0.00 | 1.00 | 0.21 | 0.84 | 0.92 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.91 | 1.72 | 0.03 | 0.90 | 1.62 | 0.03 |
| 40 kg | 0.91 | 1.61 | 0.03 | 0.92 | 1.79 | 0.03 |
| 60 kg | 0.93 | 1.25 | 0.04 | 0.91 | 0.86 | 0.03 |
| 80 kg | 0.94 | 0.78 | 0.04 | 0.93 | 0.77 | 0.04 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.57 | 0.52 | 0.39 |
| 40 kg | 0.62 | 0.61 | 0.31 |
| 60 kg | 0.71 | 0.68 | 0.26 |
| 80 kg | 0.75 | 0.79 | 0.20 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.25 | 0.41 | 0.58 | 0.77 |
| long | 0.41 | 0.43 | 0.54 | 0.69 |
| sphere | 0.48 | 0.55 | 0.66 | 0.69 |
| cylinder | 0.37 | 0.73 | 0.80 | 0.81 |
| arch | 0.14 | 0.20 | 0.24 | 0.38 |
| dumbbell | 0.11 | 0.18 | 0.16 | 0.53 |
| t_shape | 0.33 | 0.29 | 0.44 | 0.62 |
| beam | 0.45 | 0.35 | 0.42 | 0.54 |
| l_shape | 0.23 | 0.21 | 0.28 | 0.30 |
| asym | 0.26 | 0.38 | 0.28 | 0.51 |
| u_channel | 0.17 | 0.31 | 0.41 | 0.51 |
| plus | 0.10 | 0.20 | 0.31 | 0.39 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.67 | 0.81 | 0.72 | 0.47 |
| B_left | 0.28 | 0.28 | 0.25 | 0.06 |
| C_backright | 0.36 | 0.42 | 0.22 | 0.19 |
| D_far_turn | 0.33 | 0.11 | 0.17 | 0.08 |
