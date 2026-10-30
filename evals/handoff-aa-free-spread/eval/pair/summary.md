# Pair evaluation: handoff-aa-free-spread

policy: hand-off (script to the contact, then the frozen Stage 2b policy, never back), rule 'spread' (two robots), pair anymal

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 60 kg | 0.32 | 0.32 | 0.17 | 0.16 | 33.7 | 0.36 | 0.50 | 0.34 | 0.17 | 0.27 | 0.61 |
| 80 kg | 0.17 | 0.14 | 0.18 | 0.17 | 25.1 | 0.34 | 0.54 | 0.40 | 0.19 | 0.28 | 0.58 |

tasks using both robots: 0.79 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 60 kg | 80 kg |
|---|---|---|---|
| cube | part 0 -x | 0.42 | 0.00 |
| long | part 0 -x seg 1/2 | 0.08 | 0.00 |
| sphere | sector 135 + sector 225 | 0.92 | 0.92 |
| cylinder | part 0 -x seg 2/2 | 0.33 | 0.42 |
| arch | part 2 -x + part 3 -x | 0.00 | 0.00 |
| dumbbell | part 0 -x + part 1 -x | 0.58 | 0.08 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.42 | 0.25 |
| beam (unseen) | part 0 -x seg 5/5 + part 0 -x seg 1/5 | 0.00 | 0.00 |
| l_shape (unseen) | part 1 -x + part 0 -x seg 1/2 | 0.42 | 0.17 |
| asym (unseen) | part 0 -x | 0.00 | 0.00 |
| u_channel (unseen) | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.33 | 0.00 |
| plus (unseen) | part 1 -x | 0.33 | 0.25 |

## holding the assigned contact (while under the push policy)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 returns |
|---|---|---|---|---|---|---|---|---|
| 60 kg | 0.86 | 0.56 | 0.35 | 0.00 | 0.80 | 0.51 | 0.33 | 0.00 |
| 80 kg | 0.87 | 0.52 | 0.37 | 0.00 | 0.80 | 0.45 | 0.39 | 0.00 |

## both robots pushing (share of time) by object and mass

| object | 60 kg | 80 kg |
|---|---|---|
| cube | 0.10 | 0.05 |
| long | 0.02 | 0.08 |
| sphere | 0.09 | 0.13 |
| cylinder | 0.17 | 0.16 |
| arch | 0.02 | 0.01 |
| dumbbell | 0.24 | 0.21 |
| t_shape | 0.25 | 0.27 |
| beam | 0.41 | 0.45 |
| l_shape | 0.21 | 0.19 |
| asym | 0.18 | 0.20 |
| u_channel | 0.25 | 0.39 |
| plus | 0.08 | 0.18 |

## success by scenario and mass

| scenario | 60 kg | 80 kg |
|---|---|---|
| A_straight | 0.47 | 0.28 |
| B_left | 0.33 | 0.22 |
| C_backright | 0.28 | 0.11 |
| D_far_turn | 0.19 | 0.08 |
