# Pair evaluation: s4d-aa-s0-adjacent

policy: Stage 4 contact policy logs/marl2/s4d_aa_s0/model_9000.pt (robots start at their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.38 | 0.31 | 0.01 | 0.04 | 25.6 | 0.02 | 0.46 | 0.55 | 0.29 | 0.45 | 0.90 |
| 40 kg | 0.42 | 0.36 | 0.03 | 0.02 | 33.6 | 0.02 | 0.54 | 0.61 | 0.37 | 0.53 | 0.87 |
| 60 kg | 0.22 | 0.17 | 0.06 | 0.08 | 32.9 | 0.02 | 0.65 | 0.71 | 0.48 | 0.59 | 0.88 |
| 80 kg | 0.10 | 0.08 | 0.08 | 0.06 | 23.4 | 0.01 | 0.70 | 0.76 | 0.55 | 0.64 | 0.90 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x-y + part 0 corner -x+y | 0.58 | 1.00 | 0.25 | 0.00 |
| long | part 0 -x seg 2/2 + part 0 corner -x-y | 0.25 | 0.25 | 0.17 | 0.00 |
| sphere | sector 135 + sector 225 | 0.92 | 0.92 | 0.67 | 0.67 |
| cylinder | part 0 corner -x-y + part 0 -x seg 2/2 | 0.08 | 0.17 | 0.25 | 0.17 |
| arch | part 2 -x + part 3 -x | 0.25 | 0.50 | 0.25 | 0.17 |
| dumbbell | part 2 -x seg 2/3 + part 0 -x | 0.25 | 0.42 | 0.25 | 0.00 |
| t_shape | part 0 corner -x-y + part 0 -x seg 2/3 | 0.25 | 0.33 | 0.25 | 0.08 |
| beam (unseen) | part 0 -x seg 1/5 + part 0 -x seg 3/5 | 0.25 | 0.00 | 0.00 | 0.00 |
| l_shape (unseen) | part 0 corner -x-y + part 0 -x seg 2/2 | 0.25 | 0.25 | 0.00 | 0.00 |
| asym (unseen) | part 1 -x + part 0 corner -x+y | 0.58 | 0.33 | 0.08 | 0.00 |
| u_channel (unseen) | part 0 corner -x+y + part 0 -x seg 2/3 | 0.25 | 0.25 | 0.08 | 0.00 |
| plus (unseen) | part 1 corner -x-y + part 1 corner -x+y | 0.67 | 0.58 | 0.42 | 0.08 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.38 | 0.57 | 0.05 | 0.00 | 0.00 | 0.01 | 4.67 |
| 40 kg | 0.42 | 0.53 | 0.06 | 0.00 | 0.00 | 0.00 | 3.95 |
| 60 kg | 0.22 | 0.64 | 0.14 | 0.00 | 0.00 | 0.00 | 2.68 |
| 80 kg | 0.10 | 0.76 | 0.15 | 0.00 | 0.00 | 0.00 | 1.70 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.34 | 0.69 | 0.87 | 0.00 | 1.00 | 0.35 | 0.67 | 0.87 | 0.00 |
| 40 kg | 1.00 | 0.34 | 0.71 | 0.89 | 0.00 | 1.00 | 0.33 | 0.70 | 0.91 | 0.00 |
| 60 kg | 1.00 | 0.30 | 0.75 | 0.94 | 0.00 | 1.00 | 0.24 | 0.77 | 0.94 | 0.00 |
| 80 kg | 1.00 | 0.23 | 0.80 | 0.96 | 0.00 | 1.00 | 0.22 | 0.78 | 0.95 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.96 | 2.34 | 0.01 | 0.96 | 2.66 | 0.01 |
| 40 kg | 0.96 | 1.86 | 0.03 | 0.96 | 2.43 | 0.02 |
| 60 kg | 0.98 | 1.50 | 0.02 | 0.97 | 1.66 | 0.02 |
| 80 kg | 0.98 | 1.29 | 0.02 | 0.98 | 1.19 | 0.02 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.45 | 0.74 | 0.71 | 0.76 |
| long | 0.27 | 0.26 | 0.38 | 0.59 |
| sphere | 0.55 | 0.70 | 0.76 | 0.80 |
| cylinder | 0.42 | 0.56 | 0.54 | 0.65 |
| arch | 0.18 | 0.21 | 0.32 | 0.44 |
| dumbbell | 0.13 | 0.14 | 0.36 | 0.42 |
| t_shape | 0.32 | 0.34 | 0.46 | 0.59 |
| beam | 0.52 | 0.60 | 0.69 | 0.73 |
| l_shape | 0.22 | 0.23 | 0.40 | 0.41 |
| asym | 0.17 | 0.38 | 0.61 | 0.65 |
| u_channel | 0.10 | 0.20 | 0.23 | 0.30 |
| plus | 0.19 | 0.12 | 0.28 | 0.27 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.56 | 0.58 | 0.39 | 0.19 |
| B_left | 0.33 | 0.50 | 0.17 | 0.06 |
| C_backright | 0.42 | 0.33 | 0.19 | 0.11 |
| D_far_turn | 0.22 | 0.25 | 0.14 | 0.03 |
