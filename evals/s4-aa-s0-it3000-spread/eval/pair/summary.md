# Pair evaluation: s4-aa-s0-it3000-spread

policy: Stage 4 contact policy logs/marl2/s4_aa_s0/model_3000.pt (robots start at their contacts)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.35 | 0.41 | 0.02 | 0.01 | 18.0 | 0.02 | 0.41 | 0.37 | 0.15 | 0.29 | 1.06 |
| 40 kg | 0.28 | 0.28 | 0.01 | 0.06 | 15.6 | 0.02 | 0.37 | 0.51 | 0.18 | 0.29 | 1.09 |
| 60 kg | 0.16 | 0.17 | 0.06 | 0.10 | 14.5 | 0.01 | 0.39 | 0.58 | 0.20 | 0.28 | 1.07 |
| 80 kg | 0.10 | 0.09 | 0.12 | 0.15 | 24.9 | 0.01 | 0.51 | 0.67 | 0.31 | 0.37 | 1.08 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x+y + part 0 corner -x-y | 0.83 | 0.92 | 0.50 | 0.25 |
| long | part 0 corner -x+y + part 0 corner -x-y | 0.25 | 0.33 | 0.00 | 0.08 |
| sphere | sector 135 + sector 225 | 0.83 | 0.83 | 0.92 | 0.58 |
| cylinder | part 0 corner -x+y + part 0 corner -x-y | 0.08 | 0.17 | 0.08 | 0.08 |
| arch | part 2 -x + part 3 -x | 0.50 | 0.42 | 0.25 | 0.08 |
| dumbbell | part 0 -x + part 1 -x | 0.17 | 0.33 | 0.00 | 0.00 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.17 | 0.08 | 0.08 | 0.00 |
| beam (unseen) | part 0 -x seg 5/5 + part 0 -x seg 1/5 | 0.17 | 0.00 | 0.00 | 0.00 |
| l_shape (unseen) | part 0 corner -x+y + part 0 corner -x-y | 0.08 | 0.08 | 0.00 | 0.00 |
| asym (unseen) | part 0 corner -x+y + part 1 corner -x-y | 0.42 | 0.00 | 0.00 | 0.00 |
| u_channel (unseen) | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.33 | 0.08 | 0.00 | 0.08 |
| plus (unseen) | part 0 corner -x+y + part 0 corner -x-y | 0.33 | 0.17 | 0.08 | 0.08 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 returns |
|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.26 | 0.65 | 0.00 | 1.00 | 0.21 | 0.71 | 0.00 |
| 40 kg | 1.00 | 0.28 | 0.63 | 0.00 | 1.00 | 0.21 | 0.72 | 0.00 |
| 60 kg | 1.00 | 0.29 | 0.60 | 0.00 | 1.00 | 0.20 | 0.75 | 0.00 |
| 80 kg | 1.00 | 0.27 | 0.61 | 0.00 | 1.00 | 0.20 | 0.74 | 0.00 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.31 | 0.28 | 0.22 | 0.32 |
| long | 0.09 | 0.18 | 0.15 | 0.35 |
| sphere | 0.35 | 0.45 | 0.45 | 0.34 |
| cylinder | 0.06 | 0.17 | 0.06 | 0.29 |
| arch | 0.20 | 0.26 | 0.18 | 0.13 |
| dumbbell | 0.09 | 0.21 | 0.08 | 0.20 |
| t_shape | 0.18 | 0.15 | 0.29 | 0.54 |
| beam | 0.07 | 0.05 | 0.17 | 0.47 |
| l_shape | 0.06 | 0.06 | 0.19 | 0.16 |
| asym | 0.06 | 0.07 | 0.27 | 0.45 |
| u_channel | 0.28 | 0.13 | 0.14 | 0.27 |
| plus | 0.08 | 0.12 | 0.14 | 0.16 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.44 | 0.44 | 0.28 | 0.17 |
| B_left | 0.39 | 0.25 | 0.08 | 0.11 |
| C_backright | 0.36 | 0.33 | 0.17 | 0.11 |
| D_far_turn | 0.19 | 0.11 | 0.11 | 0.03 |
