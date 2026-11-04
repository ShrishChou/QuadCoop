# Pair evaluation: reach-s4d_aa_s0-spread

policy: Stage 4 contact policy logs/marl2/s4d_aa_s0/model_9000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.47 | 0.42 | 0.03 | 0.02 | 30.7 | 0.03 | 0.38 | 0.35 | 0.17 | 0.35 | 1.02 |
| 40 kg | 0.32 | 0.29 | 0.05 | 0.05 | 36.0 | 0.03 | 0.47 | 0.48 | 0.24 | 0.38 | 1.01 |
| 60 kg | 0.24 | 0.21 | 0.08 | 0.07 | 39.8 | 0.02 | 0.54 | 0.50 | 0.28 | 0.39 | 1.01 |
| 80 kg | 0.12 | 0.10 | 0.06 | 0.07 | 33.3 | 0.01 | 0.64 | 0.62 | 0.42 | 0.51 | 1.03 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x-y + part 0 corner -x+y | 0.83 | 0.58 | 0.42 | 0.08 |
| long | part 0 corner -x-y + part 0 corner -x+y | 0.83 | 0.50 | 0.42 | 0.17 |
| sphere | sector 135 + sector 225 | 1.00 | 0.92 | 0.83 | 0.75 |
| cylinder | part 0 corner -x+y + part 0 corner -x-y | 0.08 | 0.00 | 0.08 | 0.08 |
| arch | part 3 -x + part 2 -x | 0.33 | 0.25 | 0.17 | 0.08 |
| dumbbell | part 0 -x + part 1 -x | 0.58 | 0.25 | 0.08 | 0.00 |
| t_shape | part 0 corner -x+y + part 0 corner -x-y | 0.25 | 0.08 | 0.17 | 0.00 |
| beam (unseen) | part 0 -x seg 5/5 + part 0 -x seg 1/5 | 0.33 | 0.08 | 0.08 | 0.08 |
| l_shape (unseen) | part 0 corner -x-y + part 0 corner -x+y | 0.42 | 0.00 | 0.08 | 0.00 |
| asym (unseen) | part 0 corner -x+y + part 1 corner -x-y | 0.33 | 0.50 | 0.08 | 0.00 |
| u_channel (unseen) | part 0 corner -x-y + part 0 corner -x+y | 0.25 | 0.25 | 0.08 | 0.00 |
| plus (unseen) | part 0 corner -x-y + part 0 corner -x+y | 0.42 | 0.42 | 0.33 | 0.25 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.47 | 0.48 | 0.05 | 0.00 | 0.00 | 0.01 | 4.98 |
| 40 kg | 0.32 | 0.58 | 0.10 | 0.01 | 0.00 | 0.01 | 3.59 |
| 60 kg | 0.24 | 0.62 | 0.15 | 0.00 | 0.00 | 0.01 | 2.17 |
| 80 kg | 0.12 | 0.74 | 0.13 | 0.00 | 0.00 | 0.00 | 1.78 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.56 | 0.59 | 0.79 | 0.00 | 1.00 | 0.49 | 0.55 | 0.72 | 0.00 |
| 40 kg | 1.00 | 0.49 | 0.65 | 0.84 | 0.00 | 1.00 | 0.48 | 0.58 | 0.75 | 0.00 |
| 60 kg | 1.00 | 0.52 | 0.65 | 0.86 | 0.00 | 1.00 | 0.44 | 0.61 | 0.76 | 0.00 |
| 80 kg | 1.00 | 0.37 | 0.73 | 0.90 | 0.00 | 1.00 | 0.37 | 0.65 | 0.81 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change); object shoved in 0.5 of episodes

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.90 | 4.92 | 0.02 | 0.87 | 5.64 | 0.02 |
| 40 kg | 0.91 | 4.66 | 0.01 | 0.86 | 6.70 | 0.02 |
| 60 kg | 0.92 | 4.98 | 0.02 | 0.81 | 5.07 | 0.02 |
| 80 kg | 0.96 | 4.67 | 0.02 | 0.84 | 5.62 | 0.02 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.18 | 0.44 | 0.55 | 0.79 |
| long | 0.24 | 0.31 | 0.25 | 0.39 |
| sphere | 0.30 | 0.31 | 0.37 | 0.47 |
| cylinder | 0.26 | 0.39 | 0.45 | 0.58 |
| arch | 0.18 | 0.08 | 0.14 | 0.20 |
| dumbbell | 0.06 | 0.15 | 0.09 | 0.18 |
| t_shape | 0.18 | 0.22 | 0.46 | 0.70 |
| beam | 0.20 | 0.22 | 0.11 | 0.27 |
| l_shape | 0.11 | 0.22 | 0.27 | 0.33 |
| asym | 0.12 | 0.24 | 0.24 | 0.47 |
| u_channel | 0.12 | 0.13 | 0.21 | 0.43 |
| plus | 0.05 | 0.21 | 0.18 | 0.18 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.58 | 0.47 | 0.33 | 0.28 |
| B_left | 0.42 | 0.22 | 0.25 | 0.11 |
| C_backright | 0.50 | 0.28 | 0.19 | 0.06 |
| D_far_turn | 0.39 | 0.31 | 0.17 | 0.06 |
