# Pair evaluation: as-S1-alt100-it4700-dev7100

policy: checkpoint logs/marl2/asS1_alt100_s0/model_4700.pt (iteration 4700, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.86 | 0.83 | 0.04 | 0.02 | 18.6 | 0.08 | 0.43 | 0.35 | 0.15 | 0.27 | 0.72 |
| 40 kg | 0.83 | 0.76 | 0.04 | 0.03 | 23.0 | 0.09 | 0.51 | 0.42 | 0.21 | 0.32 | 0.72 |
| 60 kg | 0.57 | 0.47 | 0.08 | 0.10 | 32.5 | 0.09 | 0.57 | 0.44 | 0.24 | 0.34 | 0.70 |
| 80 kg | 0.26 | 0.21 | 0.13 | 0.14 | 34.3 | 0.09 | 0.61 | 0.48 | 0.28 | 0.38 | 0.70 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.97 | 0.96 | 0.53 | 0.12 |
| long | 0.96 | 0.96 | 0.72 | 0.38 |
| sphere | 0.99 | 1.00 | 0.97 | 0.96 |
| cylinder | 0.56 | 0.46 | 0.39 | 0.19 |
| arch | 0.67 | 0.46 | 0.17 | 0.03 |
| dumbbell | 0.93 | 0.74 | 0.36 | 0.07 |
| t_shape | 0.92 | 0.99 | 0.74 | 0.21 |
| l_shape (unseen) | 0.97 | 0.97 | 0.76 | 0.22 |
| u_channel (unseen) | 0.99 | 0.93 | 0.58 | 0.28 |
| plus (unseen) | 0.68 | 0.81 | 0.47 | 0.17 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.19 | 0.18 | 0.13 | 0.08 |
| long | 0.29 | 0.31 | 0.33 | 0.45 |
| sphere | 0.07 | 0.15 | 0.23 | 0.28 |
| cylinder | 0.21 | 0.31 | 0.35 | 0.36 |
| arch | 0.01 | 0.01 | 0.01 | 0.01 |
| dumbbell | 0.10 | 0.13 | 0.18 | 0.21 |
| t_shape | 0.18 | 0.28 | 0.30 | 0.33 |
| l_shape | 0.19 | 0.32 | 0.34 | 0.39 |
| u_channel | 0.13 | 0.24 | 0.31 | 0.43 |
| plus | 0.09 | 0.14 | 0.21 | 0.29 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.92 | 0.91 | 0.72 | 0.42 |
| B_left | 0.88 | 0.84 | 0.61 | 0.27 |
| C_backright | 0.89 | 0.82 | 0.53 | 0.19 |
| D_far_turn | 0.75 | 0.73 | 0.42 | 0.17 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| standard | 0.87 | 0.84 | 0.58 | 0.30 |
| standard swapped | 0.89 | 0.83 | 0.57 | 0.29 |
| flank | 0.86 | 0.82 | 0.55 | 0.27 |
| flank swapped | 0.86 | 0.86 | 0.63 | 0.25 |
| goal_behind | 0.84 | 0.82 | 0.56 | 0.23 |
| goal_behind swapped | 0.86 | 0.78 | 0.53 | 0.23 |
