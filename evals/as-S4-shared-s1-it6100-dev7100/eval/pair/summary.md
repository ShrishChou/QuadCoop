# Pair evaluation: as-S4-shared-s1-it6100-dev7100

policy: checkpoint logs/marl2/asS4_shared_s1/model_6100.pt (iteration 6100, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.86 | 0.83 | 0.03 | 0.02 | 19.4 | 0.09 | 0.40 | 0.40 | 0.16 | 0.29 | 0.72 |
| 40 kg | 0.83 | 0.76 | 0.03 | 0.03 | 23.0 | 0.09 | 0.49 | 0.49 | 0.23 | 0.35 | 0.71 |
| 60 kg | 0.61 | 0.52 | 0.06 | 0.08 | 33.5 | 0.09 | 0.54 | 0.52 | 0.26 | 0.36 | 0.72 |
| 80 kg | 0.27 | 0.23 | 0.11 | 0.12 | 33.9 | 0.09 | 0.58 | 0.55 | 0.30 | 0.40 | 0.71 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.96 | 1.00 | 0.54 | 0.14 |
| long | 0.92 | 0.92 | 0.75 | 0.42 |
| sphere | 0.86 | 0.96 | 0.97 | 0.96 |
| cylinder | 0.53 | 0.54 | 0.32 | 0.24 |
| arch | 0.75 | 0.60 | 0.31 | 0.03 |
| dumbbell | 0.89 | 0.74 | 0.51 | 0.08 |
| t_shape | 0.96 | 0.96 | 0.72 | 0.21 |
| l_shape (unseen) | 0.99 | 0.96 | 0.75 | 0.21 |
| u_channel (unseen) | 1.00 | 0.89 | 0.71 | 0.26 |
| plus (unseen) | 0.78 | 0.76 | 0.53 | 0.19 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.14 | 0.15 | 0.11 | 0.08 |
| long | 0.30 | 0.34 | 0.35 | 0.41 |
| sphere | 0.09 | 0.20 | 0.31 | 0.32 |
| cylinder | 0.28 | 0.41 | 0.40 | 0.44 |
| arch | 0.02 | 0.02 | 0.01 | 0.00 |
| dumbbell | 0.10 | 0.16 | 0.18 | 0.17 |
| t_shape | 0.18 | 0.29 | 0.29 | 0.40 |
| l_shape | 0.20 | 0.34 | 0.37 | 0.45 |
| u_channel | 0.17 | 0.27 | 0.34 | 0.43 |
| plus | 0.08 | 0.15 | 0.25 | 0.32 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.92 | 0.91 | 0.73 | 0.42 |
| B_left | 0.88 | 0.85 | 0.68 | 0.29 |
| C_backright | 0.81 | 0.84 | 0.59 | 0.23 |
| D_far_turn | 0.83 | 0.73 | 0.45 | 0.15 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| standard | 0.91 | 0.83 | 0.66 | 0.31 |
| standard swapped | 0.90 | 0.86 | 0.66 | 0.28 |
| flank | 0.82 | 0.83 | 0.59 | 0.25 |
| flank swapped | 0.82 | 0.85 | 0.62 | 0.26 |
| goal_behind | 0.86 | 0.82 | 0.61 | 0.29 |
| goal_behind swapped | 0.87 | 0.80 | 0.53 | 0.25 |
