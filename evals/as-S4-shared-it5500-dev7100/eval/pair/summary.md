# Pair evaluation: as-S4-shared-it5500-dev7100

policy: checkpoint logs/marl2/asS4_shared_s0/model_5500.pt (iteration 5500, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.91 | 0.85 | 0.02 | 0.01 | 18.7 | 0.07 | 0.39 | 0.40 | 0.15 | 0.28 | 0.72 |
| 40 kg | 0.82 | 0.76 | 0.05 | 0.05 | 23.7 | 0.07 | 0.47 | 0.47 | 0.21 | 0.32 | 0.73 |
| 60 kg | 0.58 | 0.48 | 0.08 | 0.07 | 34.4 | 0.07 | 0.49 | 0.50 | 0.22 | 0.32 | 0.72 |
| 80 kg | 0.28 | 0.22 | 0.12 | 0.13 | 34.7 | 0.08 | 0.55 | 0.54 | 0.27 | 0.36 | 0.71 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.97 | 0.96 | 0.54 | 0.18 |
| long | 0.92 | 0.96 | 0.78 | 0.40 |
| sphere | 1.00 | 0.99 | 1.00 | 0.96 |
| cylinder | 0.61 | 0.47 | 0.32 | 0.25 |
| arch | 0.82 | 0.53 | 0.28 | 0.01 |
| dumbbell | 0.89 | 0.78 | 0.46 | 0.11 |
| t_shape | 0.99 | 0.92 | 0.68 | 0.14 |
| l_shape (unseen) | 1.00 | 0.90 | 0.72 | 0.18 |
| u_channel (unseen) | 0.99 | 0.88 | 0.67 | 0.25 |
| plus (unseen) | 0.89 | 0.81 | 0.39 | 0.28 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.15 | 0.17 | 0.10 | 0.10 |
| long | 0.32 | 0.32 | 0.32 | 0.41 |
| sphere | 0.07 | 0.13 | 0.21 | 0.21 |
| cylinder | 0.21 | 0.35 | 0.36 | 0.35 |
| arch | 0.01 | 0.02 | 0.01 | 0.01 |
| dumbbell | 0.11 | 0.16 | 0.18 | 0.21 |
| t_shape | 0.19 | 0.26 | 0.29 | 0.37 |
| l_shape | 0.22 | 0.27 | 0.29 | 0.37 |
| u_channel | 0.16 | 0.25 | 0.28 | 0.37 |
| plus | 0.10 | 0.15 | 0.17 | 0.29 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.95 | 0.89 | 0.66 | 0.42 |
| B_left | 0.93 | 0.88 | 0.64 | 0.32 |
| C_backright | 0.90 | 0.82 | 0.57 | 0.21 |
| D_far_turn | 0.84 | 0.68 | 0.46 | 0.16 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| standard | 0.93 | 0.82 | 0.59 | 0.34 |
| standard swapped | 0.93 | 0.82 | 0.68 | 0.28 |
| flank | 0.92 | 0.83 | 0.58 | 0.25 |
| flank swapped | 0.90 | 0.84 | 0.64 | 0.28 |
| goal_behind | 0.88 | 0.81 | 0.53 | 0.28 |
| goal_behind swapped | 0.88 | 0.78 | 0.47 | 0.23 |
