# Pair evaluation: s4d-aa-s0-random

policy: Stage 4 contact policy logs/marl2/s4d_aa_s0/model_9000.pt (robots start at their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.47 | 0.40 | 0.01 | 0.02 | 26.5 | 0.02 | 0.46 | 0.54 | 0.28 | 0.42 | 0.93 |
| 40 kg | 0.38 | 0.32 | 0.01 | 0.01 | 28.7 | 0.02 | 0.54 | 0.60 | 0.37 | 0.53 | 0.95 |
| 60 kg | 0.22 | 0.19 | 0.05 | 0.06 | 30.5 | 0.01 | 0.65 | 0.69 | 0.47 | 0.57 | 0.94 |
| 80 kg | 0.17 | 0.15 | 0.03 | 0.07 | 33.9 | 0.01 | 0.72 | 0.74 | 0.54 | 0.61 | 0.94 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x-y + part 0 corner -x+y | 0.92 | 0.58 | 0.25 | 0.00 |
| long | part 0 -x seg 2/2 + part 0 corner -x-y | 0.50 | 0.50 | 0.08 | 0.33 |
| sphere | sector 225 + sector 135 | 1.00 | 1.00 | 0.75 | 1.00 |
| cylinder | part 0 -x seg 1/2 + part 0 corner -x+y | 0.25 | 0.08 | 0.17 | 0.17 |
| arch | part 3 corner -x+y + part 2 -x | 0.25 | 0.42 | 0.25 | 0.08 |
| dumbbell | part 0 -x + part 1 corner -x-y | 0.50 | 0.25 | 0.17 | 0.08 |
| t_shape | part 0 corner -x-y + part 0 -x seg 3/3 | 0.25 | 0.17 | 0.17 | 0.00 |
| beam (unseen) | part 0 -x seg 5/5 + part 0 -x seg 3/5 | 0.08 | 0.00 | 0.00 | 0.00 |
| l_shape (unseen) | part 0 corner -x+y + part 0 corner -x-y | 0.25 | 0.25 | 0.17 | 0.08 |
| asym (unseen) | part 1 corner -x-y + part 0 -x | 0.67 | 0.33 | 0.00 | 0.00 |
| u_channel (unseen) | part 0 -x seg 3/3 + part 0 corner -x-y | 0.33 | 0.58 | 0.08 | 0.00 |
| plus (unseen) | part 1 corner -x+y + part 0 corner -x-y | 0.67 | 0.33 | 0.50 | 0.33 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.47 | 0.50 | 0.03 | 0.00 | 0.00 | 0.00 | 5.41 |
| 40 kg | 0.38 | 0.61 | 0.01 | 0.00 | 0.00 | 0.00 | 4.25 |
| 60 kg | 0.22 | 0.67 | 0.11 | 0.00 | 0.00 | 0.00 | 2.70 |
| 80 kg | 0.17 | 0.73 | 0.10 | 0.00 | 0.00 | 0.00 | 2.28 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.32 | 0.71 | 0.88 | 0.00 | 1.00 | 0.28 | 0.76 | 0.88 | 0.00 |
| 40 kg | 1.00 | 0.32 | 0.74 | 0.89 | 0.00 | 1.00 | 0.29 | 0.73 | 0.90 | 0.00 |
| 60 kg | 1.00 | 0.24 | 0.81 | 0.95 | 0.00 | 1.00 | 0.24 | 0.78 | 0.94 | 0.00 |
| 80 kg | 1.00 | 0.17 | 0.84 | 0.98 | 0.00 | 1.00 | 0.19 | 0.83 | 0.96 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.96 | 2.07 | 0.01 | 0.98 | 1.80 | 0.01 |
| 40 kg | 0.96 | 1.84 | 0.01 | 0.96 | 1.96 | 0.02 |
| 60 kg | 0.96 | 1.20 | 0.02 | 0.96 | 1.05 | 0.02 |
| 80 kg | 0.98 | 0.80 | 0.01 | 0.97 | 0.58 | 0.02 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.50 | 0.64 | 0.60 | 0.92 |
| long | 0.21 | 0.42 | 0.60 | 0.65 |
| sphere | 0.48 | 0.58 | 0.71 | 0.80 |
| cylinder | 0.40 | 0.53 | 0.62 | 0.65 |
| arch | 0.20 | 0.22 | 0.32 | 0.32 |
| dumbbell | 0.12 | 0.12 | 0.14 | 0.24 |
| t_shape | 0.14 | 0.24 | 0.34 | 0.28 |
| beam | 0.23 | 0.52 | 0.76 | 0.71 |
| l_shape | 0.29 | 0.25 | 0.44 | 0.50 |
| asym | 0.30 | 0.42 | 0.57 | 0.59 |
| u_channel | 0.28 | 0.36 | 0.41 | 0.50 |
| plus | 0.16 | 0.15 | 0.12 | 0.28 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.64 | 0.39 | 0.36 | 0.28 |
| B_left | 0.50 | 0.39 | 0.14 | 0.08 |
| C_backright | 0.33 | 0.31 | 0.14 | 0.25 |
| D_far_turn | 0.42 | 0.42 | 0.22 | 0.08 |
