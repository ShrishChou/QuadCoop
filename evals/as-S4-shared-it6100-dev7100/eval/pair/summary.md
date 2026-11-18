# Pair evaluation: as-S4-shared-it6100-dev7100

policy: checkpoint logs/marl2/asS4_shared_s0/model_6100.pt (iteration 6100, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.90 | 0.84 | 0.02 | 0.02 | 18.3 | 0.08 | 0.41 | 0.40 | 0.16 | 0.29 | 0.71 |
| 40 kg | 0.83 | 0.76 | 0.04 | 0.04 | 23.3 | 0.09 | 0.49 | 0.48 | 0.23 | 0.35 | 0.72 |
| 60 kg | 0.60 | 0.50 | 0.08 | 0.07 | 32.8 | 0.09 | 0.53 | 0.52 | 0.26 | 0.37 | 0.72 |
| 80 kg | 0.30 | 0.23 | 0.11 | 0.12 | 36.8 | 0.08 | 0.55 | 0.55 | 0.29 | 0.39 | 0.71 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 1.00 | 0.94 | 0.65 | 0.17 |
| long | 0.86 | 0.89 | 0.71 | 0.43 |
| sphere | 0.97 | 0.99 | 0.97 | 0.96 |
| cylinder | 0.58 | 0.44 | 0.32 | 0.25 |
| arch | 0.75 | 0.60 | 0.24 | 0.06 |
| dumbbell | 0.99 | 0.85 | 0.38 | 0.15 |
| t_shape | 0.97 | 0.99 | 0.74 | 0.18 |
| l_shape (unseen) | 1.00 | 0.94 | 0.82 | 0.29 |
| u_channel (unseen) | 0.99 | 0.90 | 0.67 | 0.33 |
| plus (unseen) | 0.85 | 0.79 | 0.56 | 0.19 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.14 | 0.17 | 0.12 | 0.13 |
| long | 0.30 | 0.32 | 0.30 | 0.34 |
| sphere | 0.07 | 0.15 | 0.24 | 0.29 |
| cylinder | 0.25 | 0.40 | 0.44 | 0.40 |
| arch | 0.01 | 0.01 | 0.01 | 0.01 |
| dumbbell | 0.09 | 0.17 | 0.21 | 0.20 |
| t_shape | 0.22 | 0.30 | 0.32 | 0.36 |
| l_shape | 0.23 | 0.35 | 0.40 | 0.47 |
| u_channel | 0.19 | 0.28 | 0.32 | 0.41 |
| plus | 0.09 | 0.14 | 0.24 | 0.29 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.93 | 0.91 | 0.78 | 0.50 |
| B_left | 0.92 | 0.86 | 0.63 | 0.31 |
| C_backright | 0.87 | 0.82 | 0.51 | 0.22 |
| D_far_turn | 0.86 | 0.74 | 0.49 | 0.18 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| standard | 0.93 | 0.82 | 0.64 | 0.33 |
| standard swapped | 0.89 | 0.89 | 0.60 | 0.29 |
| flank | 0.91 | 0.85 | 0.60 | 0.28 |
| flank swapped | 0.88 | 0.82 | 0.68 | 0.30 |
| goal_behind | 0.90 | 0.79 | 0.58 | 0.36 |
| goal_behind swapped | 0.87 | 0.82 | 0.53 | 0.24 |
