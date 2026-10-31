# Pair evaluation: s4-aa-s0-it3000-adjacent

policy: Stage 4 contact policy logs/marl2/s4_aa_s0/model_3000.pt (robots start at their contacts)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.28 | 0.33 | 0.03 | 0.03 | 11.7 | 0.04 | 0.38 | 0.35 | 0.16 | 0.33 | 0.95 |
| 40 kg | 0.26 | 0.25 | 0.06 | 0.03 | 13.9 | 0.03 | 0.35 | 0.45 | 0.17 | 0.30 | 0.97 |
| 60 kg | 0.12 | 0.10 | 0.08 | 0.14 | 17.0 | 0.02 | 0.40 | 0.59 | 0.23 | 0.32 | 0.96 |
| 80 kg | 0.08 | 0.08 | 0.18 | 0.10 | 11.3 | 0.01 | 0.51 | 0.66 | 0.33 | 0.41 | 0.97 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x+y + part 0 corner -x-y | 0.83 | 0.83 | 0.42 | 0.08 |
| long | part 0 corner -x+y + part 0 -x seg 1/2 | 0.17 | 0.33 | 0.17 | 0.00 |
| sphere | sector 135 + sector 225 | 0.83 | 0.67 | 0.50 | 0.75 |
| cylinder | part 0 -x seg 2/2 + part 0 corner -x-y | 0.17 | 0.08 | 0.00 | 0.00 |
| arch | part 2 -x + part 3 -x | 0.42 | 0.42 | 0.08 | 0.00 |
| dumbbell | part 0 -x + part 2 -x seg 2/3 | 0.08 | 0.00 | 0.08 | 0.00 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.25 | 0.25 | 0.17 | 0.00 |
| beam (unseen) | part 0 -x seg 5/5 + part 0 -x seg 3/5 | 0.00 | 0.00 | 0.00 | 0.00 |
| l_shape (unseen) | part 0 -x seg 2/2 + part 0 corner -x-y | 0.00 | 0.08 | 0.00 | 0.00 |
| asym (unseen) | part 0 -x + part 1 corner -x-y | 0.42 | 0.17 | 0.00 | 0.00 |
| u_channel (unseen) | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.08 | 0.17 | 0.00 | 0.00 |
| plus (unseen) | part 1 corner -x+y + part 1 corner -x-y | 0.08 | 0.08 | 0.00 | 0.17 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 returns |
|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.32 | 0.58 | 0.00 | 1.00 | 0.27 | 0.59 | 0.00 |
| 40 kg | 1.00 | 0.30 | 0.58 | 0.00 | 1.00 | 0.23 | 0.69 | 0.00 |
| 60 kg | 1.00 | 0.35 | 0.53 | 0.00 | 1.00 | 0.24 | 0.67 | 0.00 |
| 80 kg | 1.00 | 0.33 | 0.51 | 0.00 | 1.00 | 0.26 | 0.63 | 0.00 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.31 | 0.22 | 0.30 | 0.48 |
| long | 0.11 | 0.09 | 0.13 | 0.28 |
| sphere | 0.37 | 0.35 | 0.52 | 0.41 |
| cylinder | 0.16 | 0.17 | 0.15 | 0.30 |
| arch | 0.14 | 0.28 | 0.13 | 0.13 |
| dumbbell | 0.10 | 0.07 | 0.11 | 0.22 |
| t_shape | 0.24 | 0.26 | 0.27 | 0.30 |
| beam | 0.04 | 0.04 | 0.29 | 0.64 |
| l_shape | 0.06 | 0.08 | 0.25 | 0.29 |
| asym | 0.24 | 0.34 | 0.30 | 0.48 |
| u_channel | 0.10 | 0.10 | 0.19 | 0.23 |
| plus | 0.08 | 0.06 | 0.11 | 0.22 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.33 | 0.39 | 0.14 | 0.11 |
| B_left | 0.33 | 0.31 | 0.11 | 0.14 |
| C_backright | 0.25 | 0.11 | 0.08 | 0.06 |
| D_far_turn | 0.19 | 0.22 | 0.14 | 0.03 |
