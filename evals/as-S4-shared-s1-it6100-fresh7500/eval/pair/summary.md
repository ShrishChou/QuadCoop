# Pair evaluation: as-S4-shared-s1-it6100-fresh7500

policy: checkpoint logs/marl2/asS4_shared_s1/model_6100.pt (iteration 6100, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.87 | 0.83 | 0.02 | 0.02 | 18.9 | 0.09 | 0.39 | 0.41 | 0.15 | 0.28 | 0.72 |
| 40 kg | 0.82 | 0.74 | 0.05 | 0.05 | 23.0 | 0.09 | 0.47 | 0.49 | 0.22 | 0.34 | 0.74 |
| 60 kg | 0.59 | 0.50 | 0.08 | 0.08 | 33.5 | 0.09 | 0.52 | 0.53 | 0.27 | 0.37 | 0.72 |
| 80 kg | 0.27 | 0.22 | 0.12 | 0.13 | 33.8 | 0.09 | 0.57 | 0.57 | 0.31 | 0.40 | 0.70 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.97 | 0.92 | 0.62 | 0.21 |
| long | 0.92 | 0.92 | 0.71 | 0.32 |
| sphere | 0.88 | 0.99 | 0.96 | 0.96 |
| cylinder | 0.56 | 0.50 | 0.35 | 0.25 |
| arch | 0.69 | 0.61 | 0.26 | 0.07 |
| dumbbell | 0.93 | 0.82 | 0.47 | 0.08 |
| t_shape | 0.99 | 0.90 | 0.62 | 0.26 |
| l_shape (unseen) | 0.99 | 0.90 | 0.79 | 0.21 |
| u_channel (unseen) | 1.00 | 0.90 | 0.61 | 0.17 |
| plus (unseen) | 0.82 | 0.71 | 0.50 | 0.14 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.13 | 0.12 | 0.12 | 0.09 |
| long | 0.26 | 0.30 | 0.35 | 0.37 |
| sphere | 0.07 | 0.19 | 0.29 | 0.37 |
| cylinder | 0.29 | 0.38 | 0.43 | 0.40 |
| arch | 0.01 | 0.02 | 0.01 | 0.01 |
| dumbbell | 0.10 | 0.17 | 0.15 | 0.20 |
| t_shape | 0.20 | 0.26 | 0.30 | 0.40 |
| l_shape | 0.19 | 0.31 | 0.40 | 0.42 |
| u_channel | 0.20 | 0.27 | 0.37 | 0.45 |
| plus | 0.10 | 0.16 | 0.24 | 0.34 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.91 | 0.92 | 0.72 | 0.42 |
| B_left | 0.90 | 0.84 | 0.67 | 0.26 |
| C_backright | 0.87 | 0.82 | 0.56 | 0.26 |
| D_far_turn | 0.81 | 0.69 | 0.41 | 0.13 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| standard | 0.90 | 0.83 | 0.60 | 0.28 |
| standard swapped | 0.88 | 0.85 | 0.57 | 0.24 |
| flank | 0.83 | 0.84 | 0.58 | 0.23 |
| flank swapped | 0.88 | 0.82 | 0.57 | 0.27 |
| goal_behind | 0.86 | 0.72 | 0.58 | 0.28 |
| goal_behind swapped | 0.90 | 0.82 | 0.63 | 0.31 |
