# Pair evaluation: reach-s4b_aa_s0-spread

policy: Stage 4 contact policy logs/marl2/s4b_aa_s0/model_6000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.31 | 0.30 | 0.08 | 0.08 | 23.2 | 0.04 | 0.26 | 0.31 | 0.15 | 0.40 | 0.94 |
| 40 kg | 0.24 | 0.26 | 0.11 | 0.05 | 22.5 | 0.04 | 0.30 | 0.37 | 0.17 | 0.37 | 0.93 |
| 60 kg | 0.21 | 0.20 | 0.19 | 0.14 | 26.6 | 0.04 | 0.37 | 0.45 | 0.21 | 0.37 | 0.91 |
| 80 kg | 0.15 | 0.14 | 0.24 | 0.17 | 28.7 | 0.03 | 0.41 | 0.49 | 0.25 | 0.40 | 0.94 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x-y + part 0 corner -x+y | 0.58 | 0.33 | 0.17 | 0.08 |
| long | part 0 corner -x-y + part 0 corner -x+y | 0.42 | 0.42 | 0.25 | 0.25 |
| sphere | sector 135 + sector 225 | 0.83 | 0.92 | 0.92 | 0.75 |
| cylinder | part 0 corner -x+y + part 0 corner -x-y | 0.08 | 0.08 | 0.33 | 0.25 |
| arch | part 3 -x + part 2 -x | 0.42 | 0.33 | 0.17 | 0.25 |
| dumbbell | part 0 -x + part 1 -x | 0.08 | 0.00 | 0.17 | 0.08 |
| t_shape | part 0 corner -x+y + part 0 corner -x-y | 0.25 | 0.17 | 0.25 | 0.08 |
| beam (unseen) | part 0 -x seg 5/5 + part 0 -x seg 1/5 | 0.17 | 0.17 | 0.00 | 0.00 |
| l_shape (unseen) | part 0 corner -x-y + part 0 corner -x+y | 0.17 | 0.08 | 0.00 | 0.00 |
| asym (unseen) | part 0 corner -x+y + part 1 corner -x-y | 0.25 | 0.00 | 0.00 | 0.00 |
| u_channel (unseen) | part 0 corner -x-y + part 0 corner -x+y | 0.00 | 0.08 | 0.00 | 0.00 |
| plus (unseen) | part 0 corner -x-y + part 0 corner -x+y | 0.42 | 0.33 | 0.25 | 0.08 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.31 | 0.53 | 0.16 | 0.00 | 0.00 | 0.16 | 1.84 |
| 40 kg | 0.24 | 0.59 | 0.16 | 0.01 | 0.00 | 0.12 | 1.61 |
| 60 kg | 0.21 | 0.47 | 0.33 | 0.00 | 0.00 | 0.02 | 1.12 |
| 80 kg | 0.15 | 0.44 | 0.40 | 0.00 | 0.00 | 0.00 | 0.72 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.98 | 0.22 | 0.41 | 0.00 | 1.00 | 0.85 | 0.24 | 0.42 | 0.00 |
| 40 kg | 1.00 | 0.85 | 0.24 | 0.41 | 0.00 | 1.00 | 0.81 | 0.24 | 0.44 | 0.00 |
| 60 kg | 1.00 | 0.75 | 0.23 | 0.45 | 0.00 | 1.00 | 0.79 | 0.23 | 0.44 | 0.00 |
| 80 kg | 1.00 | 0.69 | 0.23 | 0.47 | 0.00 | 1.00 | 0.71 | 0.28 | 0.48 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change); object shoved in 0.5 of episodes

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.57 | 9.53 | 0.15 | 0.59 | 14.00 | 0.15 |
| 40 kg | 0.62 | 10.93 | 0.21 | 0.57 | 12.47 | 0.22 |
| 60 kg | 0.63 | 11.27 | 0.25 | 0.53 | 9.44 | 0.31 |
| 80 kg | 0.57 | 8.44 | 0.28 | 0.50 | 8.75 | 0.32 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.20 | 0.15 | 0.05 | 0.14 |
| long | 0.26 | 0.31 | 0.32 | 0.43 |
| sphere | 0.35 | 0.35 | 0.34 | 0.39 |
| cylinder | 0.12 | 0.21 | 0.30 | 0.30 |
| arch | 0.13 | 0.17 | 0.18 | 0.28 |
| dumbbell | 0.07 | 0.10 | 0.20 | 0.18 |
| t_shape | 0.10 | 0.13 | 0.19 | 0.20 |
| beam | 0.21 | 0.15 | 0.22 | 0.36 |
| l_shape | 0.09 | 0.08 | 0.13 | 0.08 |
| asym | 0.12 | 0.08 | 0.17 | 0.19 |
| u_channel | 0.03 | 0.06 | 0.09 | 0.16 |
| plus | 0.17 | 0.24 | 0.33 | 0.28 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.61 | 0.44 | 0.47 | 0.44 |
| B_left | 0.33 | 0.22 | 0.19 | 0.06 |
| C_backright | 0.14 | 0.11 | 0.08 | 0.08 |
| D_far_turn | 0.14 | 0.19 | 0.08 | 0.03 |
