# Pair evaluation: as-S0-joint-s1-it6100-dev7100

policy: checkpoint logs/marl2/asS0_joint_s1/model_6100.pt (iteration 6100, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.88 | 0.83 | 0.02 | 0.03 | 18.4 | 0.09 | 0.42 | 0.40 | 0.16 | 0.29 | 0.70 |
| 40 kg | 0.82 | 0.74 | 0.04 | 0.04 | 23.4 | 0.09 | 0.49 | 0.48 | 0.23 | 0.35 | 0.71 |
| 60 kg | 0.57 | 0.47 | 0.07 | 0.10 | 30.9 | 0.10 | 0.54 | 0.51 | 0.27 | 0.39 | 0.69 |
| 80 kg | 0.28 | 0.23 | 0.13 | 0.12 | 34.2 | 0.10 | 0.60 | 0.53 | 0.31 | 0.41 | 0.68 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 1.00 | 0.97 | 0.56 | 0.15 |
| long | 0.93 | 0.92 | 0.72 | 0.35 |
| sphere | 0.94 | 0.97 | 0.97 | 0.94 |
| cylinder | 0.67 | 0.47 | 0.36 | 0.21 |
| arch | 0.62 | 0.49 | 0.22 | 0.00 |
| dumbbell | 0.94 | 0.76 | 0.38 | 0.11 |
| t_shape | 0.94 | 0.93 | 0.69 | 0.26 |
| l_shape (unseen) | 1.00 | 0.89 | 0.71 | 0.31 |
| u_channel (unseen) | 0.97 | 0.96 | 0.71 | 0.28 |
| plus (unseen) | 0.82 | 0.81 | 0.43 | 0.17 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.17 | 0.18 | 0.18 | 0.15 |
| long | 0.28 | 0.33 | 0.33 | 0.39 |
| sphere | 0.09 | 0.17 | 0.25 | 0.27 |
| cylinder | 0.27 | 0.37 | 0.41 | 0.45 |
| arch | 0.02 | 0.03 | 0.02 | 0.02 |
| dumbbell | 0.11 | 0.14 | 0.19 | 0.18 |
| t_shape | 0.19 | 0.30 | 0.36 | 0.44 |
| l_shape | 0.23 | 0.32 | 0.39 | 0.48 |
| u_channel | 0.16 | 0.23 | 0.36 | 0.47 |
| plus | 0.12 | 0.18 | 0.20 | 0.26 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.93 | 0.84 | 0.73 | 0.42 |
| B_left | 0.91 | 0.86 | 0.63 | 0.32 |
| C_backright | 0.87 | 0.84 | 0.53 | 0.19 |
| D_far_turn | 0.83 | 0.73 | 0.41 | 0.18 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| standard | 0.87 | 0.84 | 0.57 | 0.30 |
| standard swapped | 0.91 | 0.83 | 0.62 | 0.33 |
| flank | 0.88 | 0.82 | 0.57 | 0.23 |
| flank swapped | 0.88 | 0.84 | 0.63 | 0.24 |
| goal_behind | 0.91 | 0.78 | 0.56 | 0.28 |
| goal_behind swapped | 0.88 | 0.78 | 0.50 | 0.29 |
