# Pair evaluation: s4d-aa-s0-spread

policy: Stage 4 contact policy logs/marl2/s4d_aa_s0/model_9000.pt (robots start at their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.49 | 0.49 | 0.01 | 0.00 | 25.3 | 0.02 | 0.47 | 0.49 | 0.27 | 0.42 | 1.05 |
| 40 kg | 0.44 | 0.39 | 0.02 | 0.02 | 25.9 | 0.02 | 0.59 | 0.61 | 0.39 | 0.51 | 1.04 |
| 60 kg | 0.31 | 0.24 | 0.04 | 0.07 | 33.8 | 0.01 | 0.71 | 0.71 | 0.51 | 0.59 | 1.06 |
| 80 kg | 0.15 | 0.12 | 0.10 | 0.06 | 30.5 | 0.01 | 0.77 | 0.79 | 0.61 | 0.66 | 1.08 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x-y + part 0 corner -x+y | 0.92 | 0.83 | 0.67 | 0.00 |
| long | part 0 corner -x-y + part 0 corner -x+y | 0.67 | 0.50 | 0.25 | 0.08 |
| sphere | sector 135 + sector 225 | 1.00 | 0.92 | 0.75 | 0.83 |
| cylinder | part 0 corner -x+y + part 0 corner -x-y | 0.17 | 0.25 | 0.25 | 0.08 |
| arch | part 3 -x + part 2 -x | 0.25 | 0.25 | 0.25 | 0.25 |
| dumbbell | part 0 -x + part 1 -x | 0.17 | 0.50 | 0.17 | 0.17 |
| t_shape | part 0 corner -x+y + part 0 corner -x-y | 0.33 | 0.25 | 0.08 | 0.00 |
| beam (unseen) | part 0 -x seg 5/5 + part 0 -x seg 1/5 | 0.42 | 0.25 | 0.08 | 0.00 |
| l_shape (unseen) | part 0 corner -x-y + part 0 corner -x+y | 0.42 | 0.00 | 0.25 | 0.00 |
| asym (unseen) | part 0 corner -x+y + part 1 corner -x-y | 0.42 | 0.25 | 0.17 | 0.00 |
| u_channel (unseen) | part 0 corner -x-y + part 0 corner -x+y | 0.50 | 0.58 | 0.33 | 0.17 |
| plus (unseen) | part 0 corner -x-y + part 0 corner -x+y | 0.58 | 0.75 | 0.42 | 0.17 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.49 | 0.49 | 0.01 | 0.01 | 0.00 | 0.01 | 5.43 |
| 40 kg | 0.44 | 0.51 | 0.04 | 0.00 | 0.00 | 0.01 | 4.12 |
| 60 kg | 0.31 | 0.58 | 0.11 | 0.00 | 0.00 | 0.00 | 2.69 |
| 80 kg | 0.15 | 0.69 | 0.16 | 0.00 | 0.00 | 0.00 | 1.92 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.37 | 0.71 | 0.84 | 0.00 | 1.00 | 0.30 | 0.72 | 0.87 | 0.00 |
| 40 kg | 1.00 | 0.31 | 0.76 | 0.89 | 0.00 | 1.00 | 0.28 | 0.76 | 0.89 | 0.00 |
| 60 kg | 1.00 | 0.24 | 0.83 | 0.94 | 0.00 | 1.00 | 0.22 | 0.83 | 0.94 | 0.00 |
| 80 kg | 1.00 | 0.21 | 0.81 | 0.96 | 0.00 | 1.00 | 0.18 | 0.84 | 0.97 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.96 | 2.30 | 0.02 | 0.97 | 1.53 | 0.01 |
| 40 kg | 0.95 | 1.35 | 0.02 | 0.96 | 1.67 | 0.01 |
| 60 kg | 0.96 | 1.05 | 0.01 | 0.98 | 1.06 | 0.01 |
| 80 kg | 0.98 | 0.90 | 0.02 | 0.97 | 0.77 | 0.02 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.39 | 0.54 | 0.74 | 0.81 |
| long | 0.38 | 0.56 | 0.62 | 0.75 |
| sphere | 0.37 | 0.60 | 0.80 | 0.73 |
| cylinder | 0.34 | 0.61 | 0.71 | 0.91 |
| arch | 0.13 | 0.16 | 0.23 | 0.41 |
| dumbbell | 0.25 | 0.23 | 0.25 | 0.33 |
| t_shape | 0.23 | 0.39 | 0.64 | 0.72 |
| beam | 0.31 | 0.23 | 0.20 | 0.41 |
| l_shape | 0.21 | 0.22 | 0.27 | 0.42 |
| asym | 0.15 | 0.38 | 0.57 | 0.62 |
| u_channel | 0.29 | 0.40 | 0.51 | 0.73 |
| plus | 0.13 | 0.31 | 0.59 | 0.50 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.61 | 0.69 | 0.72 | 0.36 |
| B_left | 0.47 | 0.53 | 0.22 | 0.08 |
| C_backright | 0.44 | 0.33 | 0.14 | 0.11 |
| D_far_turn | 0.42 | 0.22 | 0.14 | 0.03 |
