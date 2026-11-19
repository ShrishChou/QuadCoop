# Pair evaluation: as-S0-joint-it5500-dev7100

policy: checkpoint logs/marl2/asS0_joint_s0/model_5500.pt (iteration 5500, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.88 | 0.82 | 0.03 | 0.02 | 19.0 | 0.09 | 0.40 | 0.40 | 0.16 | 0.29 | 0.73 |
| 40 kg | 0.82 | 0.73 | 0.04 | 0.04 | 23.4 | 0.09 | 0.48 | 0.48 | 0.22 | 0.35 | 0.72 |
| 60 kg | 0.59 | 0.48 | 0.07 | 0.09 | 32.6 | 0.10 | 0.52 | 0.52 | 0.26 | 0.36 | 0.70 |
| 80 kg | 0.28 | 0.22 | 0.11 | 0.15 | 33.9 | 0.10 | 0.58 | 0.55 | 0.31 | 0.41 | 0.70 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.99 | 0.93 | 0.56 | 0.12 |
| long | 0.89 | 0.89 | 0.75 | 0.44 |
| sphere | 0.96 | 0.99 | 1.00 | 0.94 |
| cylinder | 0.54 | 0.44 | 0.32 | 0.28 |
| arch | 0.72 | 0.46 | 0.18 | 0.00 |
| dumbbell | 0.88 | 0.86 | 0.46 | 0.04 |
| t_shape | 0.93 | 0.94 | 0.65 | 0.18 |
| l_shape (unseen) | 1.00 | 0.99 | 0.76 | 0.25 |
| u_channel (unseen) | 0.97 | 0.92 | 0.72 | 0.29 |
| plus (unseen) | 0.92 | 0.83 | 0.47 | 0.21 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.18 | 0.17 | 0.16 | 0.12 |
| long | 0.29 | 0.31 | 0.32 | 0.40 |
| sphere | 0.06 | 0.15 | 0.27 | 0.31 |
| cylinder | 0.25 | 0.34 | 0.42 | 0.36 |
| arch | 0.02 | 0.03 | 0.02 | 0.01 |
| dumbbell | 0.10 | 0.15 | 0.18 | 0.23 |
| t_shape | 0.21 | 0.33 | 0.29 | 0.39 |
| l_shape | 0.21 | 0.35 | 0.37 | 0.51 |
| u_channel | 0.16 | 0.26 | 0.32 | 0.41 |
| plus | 0.09 | 0.14 | 0.19 | 0.35 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.93 | 0.91 | 0.70 | 0.44 |
| B_left | 0.92 | 0.84 | 0.63 | 0.33 |
| C_backright | 0.87 | 0.81 | 0.56 | 0.20 |
| D_far_turn | 0.81 | 0.74 | 0.46 | 0.13 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| standard | 0.88 | 0.82 | 0.64 | 0.28 |
| standard swapped | 0.92 | 0.87 | 0.60 | 0.32 |
| flank | 0.87 | 0.80 | 0.56 | 0.28 |
| flank swapped | 0.88 | 0.84 | 0.63 | 0.23 |
| goal_behind | 0.87 | 0.86 | 0.58 | 0.28 |
| goal_behind swapped | 0.86 | 0.76 | 0.51 | 0.28 |
