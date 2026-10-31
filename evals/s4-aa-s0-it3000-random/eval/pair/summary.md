# Pair evaluation: s4-aa-s0-it3000-random

policy: Stage 4 contact policy logs/marl2/s4_aa_s0/model_3000.pt (robots start at their contacts)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.30 | 0.35 | 0.03 | 0.02 | 14.8 | 0.02 | 0.36 | 0.32 | 0.13 | 0.30 | 0.98 |
| 40 kg | 0.26 | 0.26 | 0.03 | 0.06 | 18.2 | 0.02 | 0.40 | 0.42 | 0.17 | 0.29 | 0.98 |
| 60 kg | 0.09 | 0.09 | 0.06 | 0.11 | 14.0 | 0.02 | 0.46 | 0.46 | 0.21 | 0.31 | 0.99 |
| 80 kg | 0.09 | 0.08 | 0.14 | 0.11 | 21.7 | 0.01 | 0.55 | 0.59 | 0.34 | 0.44 | 1.01 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x-y + part 0 corner -x+y | 0.67 | 0.92 | 0.17 | 0.00 |
| long | part 0 corner -x+y + part 0 corner -x-y | 0.42 | 0.17 | 0.08 | 0.17 |
| sphere | sector 225 + sector 135 | 0.83 | 0.92 | 0.75 | 0.67 |
| cylinder | part 0 corner -x-y + part 0 corner -x+y | 0.25 | 0.17 | 0.00 | 0.00 |
| arch | part 2 -x + part 3 corner -x-y | 0.25 | 0.42 | 0.00 | 0.00 |
| dumbbell | part 0 corner -x+y + part 0 corner -x-y | 0.00 | 0.00 | 0.00 | 0.08 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.33 | 0.08 | 0.08 | 0.00 |
| beam (unseen) | part 0 -x seg 1/5 + part 0 corner -x+y | 0.08 | 0.00 | 0.00 | 0.00 |
| l_shape (unseen) | part 0 -x seg 1/2 + part 0 corner -x+y | 0.00 | 0.08 | 0.00 | 0.00 |
| asym (unseen) | part 0 -x + part 1 corner -x-y | 0.33 | 0.00 | 0.00 | 0.00 |
| u_channel (unseen) | part 0 -x seg 2/3 + part 0 corner -x-y | 0.25 | 0.17 | 0.00 | 0.17 |
| plus (unseen) | part 0 corner -x+y + part 1 corner -x-y | 0.17 | 0.25 | 0.00 | 0.00 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 returns |
|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.30 | 0.57 | 0.00 | 1.00 | 0.31 | 0.58 | 0.00 |
| 40 kg | 1.00 | 0.28 | 0.60 | 0.00 | 1.00 | 0.27 | 0.60 | 0.00 |
| 60 kg | 1.00 | 0.29 | 0.59 | 0.00 | 1.00 | 0.32 | 0.53 | 0.00 |
| 80 kg | 1.00 | 0.27 | 0.62 | 0.00 | 1.00 | 0.27 | 0.57 | 0.00 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.22 | 0.25 | 0.22 | 0.42 |
| long | 0.10 | 0.17 | 0.11 | 0.45 |
| sphere | 0.35 | 0.42 | 0.45 | 0.34 |
| cylinder | 0.11 | 0.28 | 0.37 | 0.22 |
| arch | 0.14 | 0.11 | 0.05 | 0.17 |
| dumbbell | 0.03 | 0.03 | 0.05 | 0.18 |
| t_shape | 0.17 | 0.16 | 0.24 | 0.26 |
| beam | 0.05 | 0.14 | 0.19 | 0.58 |
| l_shape | 0.05 | 0.10 | 0.23 | 0.32 |
| asym | 0.18 | 0.20 | 0.43 | 0.58 |
| u_channel | 0.12 | 0.10 | 0.14 | 0.41 |
| plus | 0.09 | 0.06 | 0.05 | 0.14 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.33 | 0.33 | 0.14 | 0.14 |
| B_left | 0.42 | 0.28 | 0.08 | 0.08 |
| C_backright | 0.31 | 0.25 | 0.06 | 0.11 |
| D_far_turn | 0.14 | 0.19 | 0.08 | 0.03 |
