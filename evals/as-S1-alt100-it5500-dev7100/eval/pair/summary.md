# Pair evaluation: as-S1-alt100-it5500-dev7100

policy: checkpoint logs/marl2/asS1_alt100_s0/model_5500.pt (iteration 5500, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.87 | 0.82 | 0.03 | 0.03 | 18.9 | 0.10 | 0.40 | 0.39 | 0.15 | 0.28 | 0.70 |
| 40 kg | 0.82 | 0.76 | 0.04 | 0.04 | 24.3 | 0.10 | 0.48 | 0.45 | 0.20 | 0.32 | 0.71 |
| 60 kg | 0.58 | 0.50 | 0.08 | 0.09 | 33.2 | 0.10 | 0.56 | 0.46 | 0.24 | 0.35 | 0.70 |
| 80 kg | 0.27 | 0.23 | 0.15 | 0.12 | 32.0 | 0.10 | 0.60 | 0.49 | 0.27 | 0.37 | 0.70 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.96 | 0.90 | 0.62 | 0.11 |
| long | 0.96 | 0.93 | 0.72 | 0.31 |
| sphere | 0.92 | 0.93 | 0.90 | 0.94 |
| cylinder | 0.56 | 0.47 | 0.32 | 0.19 |
| arch | 0.62 | 0.46 | 0.29 | 0.01 |
| dumbbell | 0.92 | 0.81 | 0.49 | 0.07 |
| t_shape | 0.96 | 0.94 | 0.64 | 0.24 |
| l_shape (unseen) | 1.00 | 0.99 | 0.74 | 0.31 |
| u_channel (unseen) | 0.99 | 0.96 | 0.72 | 0.28 |
| plus (unseen) | 0.79 | 0.83 | 0.40 | 0.19 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.15 | 0.16 | 0.13 | 0.08 |
| long | 0.32 | 0.32 | 0.31 | 0.35 |
| sphere | 0.06 | 0.14 | 0.24 | 0.28 |
| cylinder | 0.25 | 0.32 | 0.36 | 0.36 |
| arch | 0.01 | 0.02 | 0.02 | 0.01 |
| dumbbell | 0.10 | 0.13 | 0.17 | 0.21 |
| t_shape | 0.18 | 0.26 | 0.28 | 0.34 |
| l_shape | 0.20 | 0.31 | 0.38 | 0.39 |
| u_channel | 0.16 | 0.24 | 0.37 | 0.43 |
| plus | 0.07 | 0.12 | 0.19 | 0.28 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.92 | 0.88 | 0.74 | 0.42 |
| B_left | 0.91 | 0.83 | 0.62 | 0.31 |
| C_backright | 0.87 | 0.82 | 0.54 | 0.20 |
| D_far_turn | 0.78 | 0.76 | 0.43 | 0.13 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| standard | 0.89 | 0.88 | 0.57 | 0.28 |
| standard swapped | 0.88 | 0.83 | 0.64 | 0.33 |
| flank | 0.87 | 0.83 | 0.60 | 0.27 |
| flank swapped | 0.85 | 0.78 | 0.60 | 0.27 |
| goal_behind | 0.86 | 0.83 | 0.57 | 0.23 |
| goal_behind swapped | 0.85 | 0.78 | 0.53 | 0.23 |
