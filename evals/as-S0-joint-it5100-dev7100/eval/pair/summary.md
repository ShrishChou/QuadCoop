# Pair evaluation: as-S0-joint-it5100-dev7100

policy: checkpoint logs/marl2/asS0_joint_s0/model_5100.pt (iteration 5100, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.88 | 0.83 | 0.03 | 0.02 | 18.8 | 0.07 | 0.40 | 0.40 | 0.15 | 0.28 | 0.72 |
| 40 kg | 0.82 | 0.74 | 0.05 | 0.04 | 23.9 | 0.08 | 0.48 | 0.46 | 0.21 | 0.32 | 0.72 |
| 60 kg | 0.61 | 0.50 | 0.07 | 0.07 | 33.4 | 0.08 | 0.54 | 0.51 | 0.25 | 0.36 | 0.72 |
| 80 kg | 0.27 | 0.21 | 0.12 | 0.12 | 34.7 | 0.08 | 0.59 | 0.54 | 0.30 | 0.40 | 0.69 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.99 | 0.93 | 0.53 | 0.11 |
| long | 0.92 | 0.96 | 0.76 | 0.35 |
| sphere | 0.93 | 1.00 | 0.99 | 0.96 |
| cylinder | 0.58 | 0.51 | 0.38 | 0.26 |
| arch | 0.68 | 0.49 | 0.24 | 0.01 |
| dumbbell | 0.96 | 0.76 | 0.50 | 0.07 |
| t_shape | 0.97 | 0.96 | 0.76 | 0.26 |
| l_shape (unseen) | 0.96 | 0.90 | 0.76 | 0.32 |
| u_channel (unseen) | 0.96 | 0.94 | 0.68 | 0.21 |
| plus (unseen) | 0.83 | 0.71 | 0.51 | 0.15 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.17 | 0.13 | 0.09 | 0.10 |
| long | 0.28 | 0.32 | 0.33 | 0.37 |
| sphere | 0.08 | 0.14 | 0.25 | 0.30 |
| cylinder | 0.24 | 0.37 | 0.40 | 0.42 |
| arch | 0.01 | 0.01 | 0.02 | 0.01 |
| dumbbell | 0.10 | 0.16 | 0.21 | 0.22 |
| t_shape | 0.21 | 0.27 | 0.30 | 0.39 |
| l_shape | 0.21 | 0.32 | 0.40 | 0.50 |
| u_channel | 0.18 | 0.27 | 0.33 | 0.41 |
| plus | 0.08 | 0.12 | 0.20 | 0.30 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.94 | 0.88 | 0.76 | 0.44 |
| B_left | 0.90 | 0.84 | 0.66 | 0.31 |
| C_backright | 0.88 | 0.84 | 0.56 | 0.20 |
| D_far_turn | 0.79 | 0.71 | 0.47 | 0.13 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| standard | 0.93 | 0.84 | 0.61 | 0.29 |
| standard swapped | 0.88 | 0.85 | 0.60 | 0.28 |
| flank | 0.92 | 0.85 | 0.67 | 0.28 |
| flank swapped | 0.84 | 0.76 | 0.61 | 0.25 |
| goal_behind | 0.82 | 0.79 | 0.62 | 0.23 |
| goal_behind swapped | 0.88 | 0.81 | 0.56 | 0.28 |
