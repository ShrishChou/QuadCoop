# Pair evaluation: as-S2-onlyA-it6100-dev7100

policy: checkpoint logs/marl2/asS2_onlyA_s0/model_6100.pt (iteration 6100, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.88 | 0.83 | 0.02 | 0.02 | 18.5 | 0.09 | 0.41 | 0.39 | 0.16 | 0.29 | 0.72 |
| 40 kg | 0.83 | 0.76 | 0.05 | 0.04 | 23.1 | 0.09 | 0.50 | 0.47 | 0.23 | 0.34 | 0.72 |
| 60 kg | 0.60 | 0.51 | 0.07 | 0.09 | 33.0 | 0.09 | 0.56 | 0.49 | 0.27 | 0.38 | 0.70 |
| 80 kg | 0.28 | 0.22 | 0.12 | 0.12 | 36.1 | 0.09 | 0.61 | 0.50 | 0.29 | 0.39 | 0.70 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 1.00 | 0.94 | 0.60 | 0.12 |
| long | 0.90 | 0.93 | 0.74 | 0.38 |
| sphere | 1.00 | 0.99 | 0.99 | 0.99 |
| cylinder | 0.64 | 0.46 | 0.32 | 0.21 |
| arch | 0.64 | 0.53 | 0.26 | 0.03 |
| dumbbell | 0.96 | 0.79 | 0.36 | 0.10 |
| t_shape | 0.94 | 0.96 | 0.75 | 0.26 |
| l_shape (unseen) | 0.99 | 0.94 | 0.72 | 0.24 |
| u_channel (unseen) | 0.99 | 0.93 | 0.74 | 0.25 |
| plus (unseen) | 0.78 | 0.81 | 0.50 | 0.25 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.16 | 0.17 | 0.13 | 0.13 |
| long | 0.29 | 0.34 | 0.42 | 0.39 |
| sphere | 0.12 | 0.18 | 0.28 | 0.31 |
| cylinder | 0.26 | 0.30 | 0.38 | 0.34 |
| arch | 0.02 | 0.02 | 0.01 | 0.01 |
| dumbbell | 0.10 | 0.15 | 0.20 | 0.21 |
| t_shape | 0.20 | 0.33 | 0.31 | 0.40 |
| l_shape | 0.20 | 0.32 | 0.36 | 0.38 |
| u_channel | 0.18 | 0.31 | 0.37 | 0.46 |
| plus | 0.07 | 0.15 | 0.21 | 0.28 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.89 | 0.91 | 0.72 | 0.38 |
| B_left | 0.89 | 0.84 | 0.62 | 0.36 |
| C_backright | 0.89 | 0.83 | 0.57 | 0.21 |
| D_far_turn | 0.85 | 0.73 | 0.47 | 0.18 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| standard | 0.89 | 0.82 | 0.58 | 0.25 |
| standard swapped | 0.89 | 0.87 | 0.57 | 0.27 |
| flank | 0.88 | 0.82 | 0.65 | 0.32 |
| flank swapped | 0.88 | 0.81 | 0.57 | 0.30 |
| goal_behind | 0.87 | 0.82 | 0.57 | 0.27 |
| goal_behind swapped | 0.89 | 0.82 | 0.62 | 0.29 |
