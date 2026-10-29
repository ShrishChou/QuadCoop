# Pair evaluation: contact-aa-re4-adjacent

policy: scripted contacts, rule 'adjacent' (two robots), pair anymal, re-chosen every 4 s

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.08 | 0.08 | 0.03 | 0.19 | 51.7 | 0.11 | 0.47 | 0.26 | 0.13 | 0.25 | 0.81 |
| 40 kg | 0.06 | 0.06 | 0.01 | 0.18 | 41.5 | 0.11 | 0.55 | 0.37 | 0.25 | 0.41 | 0.74 |
| 60 kg | 0.05 | 0.05 | 0.01 | 0.08 | 46.3 | 0.09 | 0.63 | 0.44 | 0.33 | 0.48 | 0.72 |
| 80 kg | 0.03 | 0.03 | 0.02 | 0.07 | 46.7 | 0.05 | 0.73 | 0.51 | 0.43 | 0.54 | 0.74 |

tasks using both robots: 0.79 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 -x | 0.00 | 0.00 | 0.00 | 0.00 |
| long | part 0 -x seg 1/2 | 0.00 | 0.00 | 0.00 | 0.00 |
| sphere | sector 135 + sector 225 | 0.83 | 0.67 | 0.58 | 0.42 |
| cylinder | part 0 -x seg 2/2 | 0.00 | 0.00 | 0.00 | 0.00 |
| arch | part 2 -x + part 3 -x | 0.08 | 0.00 | 0.00 | 0.00 |
| dumbbell | part 0 -x + part 2 -x seg 2/3 | 0.00 | 0.00 | 0.00 | 0.00 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.00 | 0.00 | 0.00 | 0.00 |
| beam (unseen) | part 0 -x seg 5/5 + part 0 -x seg 3/5 | 0.08 | 0.00 | 0.00 | 0.00 |
| l_shape (unseen) | part 1 -x + part 0 -x seg 1/2 | 0.00 | 0.00 | 0.00 | 0.00 |
| asym (unseen) | part 0 -x | 0.00 | 0.00 | 0.00 | 0.00 |
| u_channel (unseen) | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.00 | 0.00 | 0.00 | 0.00 |
| plus (unseen) | part 1 -x | 0.00 | 0.00 | 0.00 | 0.00 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.17 | 0.18 | 0.34 | 0.41 |
| long | 0.18 | 0.33 | 0.44 | 0.44 |
| sphere | 0.10 | 0.23 | 0.25 | 0.38 |
| cylinder | 0.03 | 0.14 | 0.24 | 0.28 |
| arch | 0.16 | 0.10 | 0.09 | 0.25 |
| dumbbell | 0.17 | 0.35 | 0.14 | 0.17 |
| t_shape | 0.15 | 0.39 | 0.35 | 0.49 |
| beam | 0.11 | 0.28 | 0.38 | 0.51 |
| l_shape | 0.15 | 0.33 | 0.49 | 0.66 |
| asym | 0.25 | 0.31 | 0.40 | 0.39 |
| u_channel | 0.12 | 0.33 | 0.65 | 0.80 |
| plus | 0.02 | 0.08 | 0.25 | 0.35 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.08 | 0.08 | 0.06 | 0.03 |
| B_left | 0.06 | 0.06 | 0.06 | 0.06 |
| C_backright | 0.11 | 0.03 | 0.08 | 0.03 |
| D_far_turn | 0.08 | 0.06 | 0.00 | 0.03 |
