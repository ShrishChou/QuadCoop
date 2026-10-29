# Pair evaluation: contact-aa-re4-spread

policy: scripted contacts, rule 'spread' (two robots), pair anymal, re-chosen every 4 s

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.10 | 0.09 | 0.02 | 0.17 | 41.9 | 0.09 | 0.46 | 0.27 | 0.11 | 0.19 | 1.01 |
| 40 kg | 0.06 | 0.06 | 0.01 | 0.08 | 48.7 | 0.10 | 0.56 | 0.35 | 0.20 | 0.30 | 0.96 |
| 60 kg | 0.05 | 0.05 | 0.03 | 0.03 | 47.2 | 0.08 | 0.62 | 0.41 | 0.24 | 0.32 | 0.99 |
| 80 kg | 0.02 | 0.02 | 0.03 | 0.04 | 31.9 | 0.04 | 0.70 | 0.48 | 0.34 | 0.41 | 1.03 |

tasks using both robots: 0.79 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 -x | 0.00 | 0.00 | 0.00 | 0.00 |
| long | part 0 -x seg 1/2 | 0.00 | 0.00 | 0.00 | 0.00 |
| sphere | sector 135 + sector 225 | 0.67 | 0.67 | 0.58 | 0.25 |
| cylinder | part 0 -x seg 2/2 | 0.00 | 0.00 | 0.00 | 0.00 |
| arch | part 2 -x + part 3 -x | 0.08 | 0.00 | 0.00 | 0.00 |
| dumbbell | part 0 -x + part 1 -x | 0.00 | 0.00 | 0.00 | 0.00 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.17 | 0.00 | 0.00 | 0.00 |
| beam (unseen) | part 0 -x seg 5/5 + part 0 -x seg 1/5 | 0.08 | 0.00 | 0.00 | 0.00 |
| l_shape (unseen) | part 1 -x + part 0 -x seg 1/2 | 0.08 | 0.00 | 0.00 | 0.00 |
| asym (unseen) | part 0 -x | 0.00 | 0.00 | 0.00 | 0.00 |
| u_channel (unseen) | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.00 | 0.00 | 0.00 | 0.00 |
| plus (unseen) | part 1 -x | 0.08 | 0.00 | 0.00 | 0.00 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.16 | 0.30 | 0.38 | 0.42 |
| long | 0.03 | 0.12 | 0.22 | 0.35 |
| sphere | 0.19 | 0.14 | 0.23 | 0.30 |
| cylinder | 0.05 | 0.15 | 0.14 | 0.17 |
| arch | 0.08 | 0.14 | 0.15 | 0.22 |
| dumbbell | 0.04 | 0.05 | 0.10 | 0.19 |
| t_shape | 0.20 | 0.33 | 0.39 | 0.55 |
| beam | 0.07 | 0.26 | 0.07 | 0.26 |
| l_shape | 0.14 | 0.20 | 0.38 | 0.39 |
| asym | 0.12 | 0.22 | 0.29 | 0.41 |
| u_channel | 0.15 | 0.33 | 0.23 | 0.38 |
| plus | 0.03 | 0.12 | 0.30 | 0.39 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.08 | 0.06 | 0.06 | 0.00 |
| B_left | 0.17 | 0.03 | 0.03 | 0.03 |
| C_backright | 0.11 | 0.06 | 0.06 | 0.06 |
| D_far_turn | 0.03 | 0.08 | 0.06 | 0.00 |
