# Pair evaluation: as-S0-joint-it4700-dev7100

policy: checkpoint logs/marl2/asS0_joint_s0/model_4700.pt (iteration 4700, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.88 | 0.82 | 0.02 | 0.02 | 19.0 | 0.08 | 0.41 | 0.40 | 0.16 | 0.29 | 0.72 |
| 40 kg | 0.82 | 0.75 | 0.04 | 0.04 | 23.7 | 0.08 | 0.48 | 0.46 | 0.20 | 0.31 | 0.72 |
| 60 kg | 0.57 | 0.50 | 0.08 | 0.08 | 33.5 | 0.09 | 0.54 | 0.49 | 0.25 | 0.35 | 0.71 |
| 80 kg | 0.28 | 0.22 | 0.11 | 0.11 | 36.4 | 0.08 | 0.58 | 0.53 | 0.29 | 0.38 | 0.71 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.99 | 0.96 | 0.49 | 0.17 |
| long | 0.92 | 0.93 | 0.72 | 0.40 |
| sphere | 0.94 | 0.99 | 0.97 | 0.96 |
| cylinder | 0.60 | 0.43 | 0.31 | 0.19 |
| arch | 0.62 | 0.47 | 0.24 | 0.00 |
| dumbbell | 0.97 | 0.79 | 0.43 | 0.08 |
| t_shape | 0.97 | 0.97 | 0.71 | 0.24 |
| l_shape (unseen) | 0.99 | 0.94 | 0.72 | 0.28 |
| u_channel (unseen) | 0.97 | 0.92 | 0.62 | 0.24 |
| plus (unseen) | 0.82 | 0.81 | 0.54 | 0.28 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.13 | 0.13 | 0.13 | 0.08 |
| long | 0.32 | 0.31 | 0.33 | 0.41 |
| sphere | 0.10 | 0.12 | 0.20 | 0.26 |
| cylinder | 0.27 | 0.33 | 0.41 | 0.38 |
| arch | 0.01 | 0.02 | 0.01 | 0.01 |
| dumbbell | 0.10 | 0.14 | 0.19 | 0.21 |
| t_shape | 0.22 | 0.28 | 0.31 | 0.37 |
| l_shape | 0.22 | 0.32 | 0.33 | 0.44 |
| u_channel | 0.16 | 0.25 | 0.32 | 0.42 |
| plus | 0.08 | 0.13 | 0.24 | 0.30 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.89 | 0.90 | 0.66 | 0.40 |
| B_left | 0.92 | 0.84 | 0.61 | 0.36 |
| C_backright | 0.86 | 0.84 | 0.55 | 0.18 |
| D_far_turn | 0.84 | 0.71 | 0.48 | 0.19 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| standard | 0.94 | 0.83 | 0.65 | 0.32 |
| standard swapped | 0.88 | 0.84 | 0.60 | 0.37 |
| flank | 0.88 | 0.83 | 0.57 | 0.27 |
| flank swapped | 0.82 | 0.81 | 0.55 | 0.21 |
| goal_behind | 0.84 | 0.81 | 0.54 | 0.26 |
| goal_behind swapped | 0.91 | 0.80 | 0.54 | 0.28 |
