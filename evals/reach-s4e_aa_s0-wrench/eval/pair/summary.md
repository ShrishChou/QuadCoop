# Pair evaluation: reach-s4e_aa_s0-wrench

policy: Stage 4 contact policy logs/marl2/s4e_aa_s0/model_12000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.65 | 0.60 | 0.00 | 0.02 | 31.9 | 0.01 | 0.43 | 0.36 | 0.14 | 0.25 | 1.08 |
| 40 kg | 0.54 | 0.47 | 0.02 | 0.03 | 35.9 | 0.01 | 0.48 | 0.42 | 0.18 | 0.29 | 1.03 |
| 60 kg | 0.40 | 0.33 | 0.03 | 0.04 | 37.3 | 0.02 | 0.58 | 0.50 | 0.25 | 0.32 | 1.03 |
| 80 kg | 0.20 | 0.16 | 0.06 | 0.06 | 38.9 | 0.02 | 0.64 | 0.57 | 0.34 | 0.41 | 0.99 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x+y + part 0 corner -x-y | 0.83 | 0.67 | 0.42 | 0.08 |
| long | part 0 -x seg 2/2 + part 0 corner -x-y | 0.75 | 0.50 | 0.42 | 0.25 |
| sphere | sector 135 + sector 225 | 1.00 | 0.92 | 1.00 | 0.92 |
| cylinder | part 0 corner -x-y + part 0 -x seg 2/2 | 0.25 | 0.17 | 0.33 | 0.25 |
| arch | part 3 -x + part 2 -x | 0.67 | 0.67 | 0.58 | 0.25 |
| dumbbell | part 0 -x + part 1 -x | 0.75 | 0.42 | 0.50 | 0.08 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.92 | 0.58 | 0.33 | 0.08 |
| beam (unseen) | part 0 -x seg 2/5 + part 0 -x seg 4/5 | 0.33 | 0.42 | 0.08 | 0.00 |
| l_shape (unseen) | part 1 -x + part 0 corner -x-y | 0.75 | 0.67 | 0.42 | 0.00 |
| asym (unseen) | part 1 -x + part 0 corner -x+y | 0.50 | 0.42 | 0.00 | 0.00 |
| u_channel (unseen) | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.42 | 0.58 | 0.33 | 0.17 |
| plus (unseen) | part 0 corner -x-y + part 0 corner -x+y | 0.67 | 0.50 | 0.42 | 0.33 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.65 | 0.32 | 0.02 | 0.01 | 0.00 | 0.00 | 6.67 |
| 40 kg | 0.54 | 0.40 | 0.06 | 0.01 | 0.00 | 0.00 | 4.62 |
| 60 kg | 0.40 | 0.52 | 0.08 | 0.00 | 0.00 | 0.00 | 3.19 |
| 80 kg | 0.20 | 0.67 | 0.12 | 0.00 | 0.00 | 0.00 | 1.77 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.40 | 0.63 | 0.79 | 0.00 | 1.00 | 0.49 | 0.58 | 0.74 | 0.00 |
| 40 kg | 1.00 | 0.36 | 0.68 | 0.83 | 0.00 | 1.00 | 0.47 | 0.61 | 0.75 | 0.00 |
| 60 kg | 1.00 | 0.32 | 0.72 | 0.87 | 0.00 | 1.00 | 0.36 | 0.71 | 0.83 | 0.00 |
| 80 kg | 1.00 | 0.28 | 0.76 | 0.90 | 0.00 | 1.00 | 0.32 | 0.73 | 0.87 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change); object shoved in 0.5 of episodes

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.89 | 4.29 | 0.04 | 0.85 | 4.92 | 0.03 |
| 40 kg | 0.90 | 4.69 | 0.04 | 0.86 | 5.00 | 0.04 |
| 60 kg | 0.90 | 5.88 | 0.04 | 0.91 | 6.59 | 0.03 |
| 80 kg | 0.93 | 6.22 | 0.04 | 0.91 | 6.91 | 0.04 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.51 | 0.47 | 0.25 |
| 40 kg | 0.60 | 0.52 | 0.22 |
| 60 kg | 0.63 | 0.61 | 0.19 |
| 80 kg | 0.69 | 0.64 | 0.18 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.04 | 0.07 | 0.08 | 0.11 |
| long | 0.11 | 0.21 | 0.51 | 0.55 |
| sphere | 0.20 | 0.30 | 0.42 | 0.43 |
| cylinder | 0.14 | 0.31 | 0.30 | 0.39 |
| arch | 0.13 | 0.14 | 0.16 | 0.21 |
| dumbbell | 0.15 | 0.17 | 0.14 | 0.13 |
| t_shape | 0.15 | 0.28 | 0.46 | 0.64 |
| beam | 0.10 | 0.11 | 0.17 | 0.32 |
| l_shape | 0.13 | 0.12 | 0.09 | 0.14 |
| asym | 0.26 | 0.23 | 0.31 | 0.57 |
| u_channel | 0.17 | 0.14 | 0.23 | 0.36 |
| plus | 0.05 | 0.10 | 0.14 | 0.23 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.86 | 0.75 | 0.72 | 0.42 |
| B_left | 0.64 | 0.39 | 0.33 | 0.11 |
| C_backright | 0.67 | 0.58 | 0.31 | 0.17 |
| D_far_turn | 0.44 | 0.44 | 0.25 | 0.11 |
