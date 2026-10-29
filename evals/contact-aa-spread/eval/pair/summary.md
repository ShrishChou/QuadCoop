# Pair evaluation: contact-aa-spread

policy: scripted contacts, rule 'spread' (two robots), pair anymal

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.03 | 0.03 | 0.00 | 0.00 | 14.8 | 0.03 | 0.42 | 0.31 | 0.07 | 0.10 | 1.08 |
| 40 kg | 0.01 | 0.01 | 0.00 | 0.00 | 29.1 | 0.04 | 0.56 | 0.34 | 0.09 | 0.11 | 1.09 |
| 60 kg | 0.00 | 0.00 | 0.01 | 0.01 |  | 0.02 | 0.64 | 0.39 | 0.16 | 0.19 | 1.05 |
| 80 kg | 0.01 | 0.01 | 0.01 | 0.04 | 23.8 | 0.02 | 0.70 | 0.44 | 0.29 | 0.34 | 1.04 |

tasks using both robots: 0.79 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 -x | 0.08 | 0.00 | 0.00 | 0.00 |
| long | part 0 -x seg 1/2 | 0.00 | 0.00 | 0.00 | 0.00 |
| sphere | sector 135 + sector 225 | 0.00 | 0.00 | 0.00 | 0.08 |
| cylinder | part 0 -x seg 2/2 | 0.00 | 0.00 | 0.00 | 0.00 |
| arch | part 2 -x + part 3 -x | 0.00 | 0.00 | 0.00 | 0.00 |
| dumbbell | part 0 -x + part 1 -x | 0.08 | 0.00 | 0.00 | 0.00 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.00 | 0.00 | 0.00 | 0.00 |
| beam (unseen) | part 0 -x seg 5/5 + part 0 -x seg 1/5 | 0.00 | 0.08 | 0.00 | 0.00 |
| l_shape (unseen) | part 1 -x + part 0 -x seg 1/2 | 0.00 | 0.00 | 0.00 | 0.00 |
| asym (unseen) | part 0 -x | 0.00 | 0.00 | 0.00 | 0.00 |
| u_channel (unseen) | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.00 | 0.00 | 0.00 | 0.00 |
| plus (unseen) | part 1 -x | 0.17 | 0.08 | 0.00 | 0.00 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.06 | 0.27 | 0.38 | 0.45 |
| long | 0.09 | 0.11 | 0.12 | 0.27 |
| sphere | 0.02 | 0.04 | 0.08 | 0.06 |
| cylinder | 0.01 | 0.02 | 0.03 | 0.09 |
| arch | 0.03 | 0.05 | 0.09 | 0.22 |
| dumbbell | 0.16 | 0.04 | 0.05 | 0.19 |
| t_shape | 0.11 | 0.19 | 0.28 | 0.45 |
| beam | 0.03 | 0.02 | 0.04 | 0.22 |
| l_shape | 0.02 | 0.04 | 0.15 | 0.27 |
| asym | 0.08 | 0.05 | 0.23 | 0.36 |
| u_channel | 0.04 | 0.14 | 0.20 | 0.40 |
| plus | 0.15 | 0.12 | 0.32 | 0.45 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.03 | 0.00 | 0.00 | 0.00 |
| B_left | 0.08 | 0.06 | 0.00 | 0.00 |
| C_backright | 0.00 | 0.00 | 0.00 | 0.03 |
| D_far_turn | 0.00 | 0.00 | 0.00 | 0.00 |
