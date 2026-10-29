# Pair evaluation: contact-aa-adjacent

policy: scripted contacts, rule 'adjacent' (two robots), pair anymal

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.03 | 0.03 | 0.01 | 0.01 | 18.7 | 0.07 | 0.41 | 0.31 | 0.12 | 0.20 | 0.73 |
| 40 kg | 0.01 | 0.01 | 0.01 | 0.01 | 19.1 | 0.07 | 0.59 | 0.35 | 0.19 | 0.26 | 0.77 |
| 60 kg | 0.01 | 0.01 | 0.01 | 0.02 | 25.8 | 0.06 | 0.65 | 0.43 | 0.30 | 0.39 | 0.75 |
| 80 kg | 0.01 | 0.01 | 0.01 | 0.02 | 22.8 | 0.06 | 0.75 | 0.51 | 0.41 | 0.49 | 0.74 |

tasks using both robots: 0.79 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 -x | 0.00 | 0.00 | 0.00 | 0.00 |
| long | part 0 -x seg 1/2 | 0.00 | 0.00 | 0.00 | 0.00 |
| sphere | sector 135 + sector 225 | 0.17 | 0.08 | 0.08 | 0.17 |
| cylinder | part 0 -x seg 2/2 | 0.08 | 0.00 | 0.00 | 0.00 |
| arch | part 2 -x + part 3 -x | 0.00 | 0.00 | 0.00 | 0.00 |
| dumbbell | part 0 -x + part 2 -x seg 2/3 | 0.00 | 0.00 | 0.00 | 0.00 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.00 | 0.00 | 0.00 | 0.00 |
| beam (unseen) | part 0 -x seg 5/5 + part 0 -x seg 3/5 | 0.00 | 0.00 | 0.00 | 0.00 |
| l_shape (unseen) | part 1 -x + part 0 -x seg 1/2 | 0.00 | 0.00 | 0.00 | 0.00 |
| asym (unseen) | part 0 -x | 0.00 | 0.00 | 0.00 | 0.00 |
| u_channel (unseen) | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.00 | 0.00 | 0.00 | 0.00 |
| plus (unseen) | part 1 -x | 0.08 | 0.00 | 0.00 | 0.00 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.19 | 0.25 | 0.44 | 0.44 |
| long | 0.25 | 0.41 | 0.41 | 0.45 |
| sphere | 0.10 | 0.07 | 0.16 | 0.22 |
| cylinder | 0.21 | 0.25 | 0.26 | 0.34 |
| arch | 0.03 | 0.06 | 0.07 | 0.23 |
| dumbbell | 0.17 | 0.08 | 0.07 | 0.17 |
| t_shape | 0.02 | 0.04 | 0.13 | 0.25 |
| beam | 0.01 | 0.20 | 0.35 | 0.44 |
| l_shape | 0.04 | 0.26 | 0.47 | 0.70 |
| asym | 0.13 | 0.33 | 0.41 | 0.40 |
| u_channel | 0.23 | 0.27 | 0.50 | 0.84 |
| plus | 0.02 | 0.12 | 0.27 | 0.40 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.00 | 0.00 | 0.00 | 0.00 |
| B_left | 0.11 | 0.03 | 0.00 | 0.06 |
| C_backright | 0.00 | 0.00 | 0.03 | 0.00 |
| D_far_turn | 0.00 | 0.00 | 0.00 | 0.00 |
