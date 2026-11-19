# Pair evaluation: as-S4-shared-it4700-dev7100

policy: checkpoint logs/marl2/asS4_shared_s0/model_4700.pt (iteration 4700, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.88 | 0.83 | 0.02 | 0.02 | 18.5 | 0.07 | 0.39 | 0.41 | 0.15 | 0.27 | 0.72 |
| 40 kg | 0.83 | 0.73 | 0.04 | 0.04 | 25.0 | 0.08 | 0.47 | 0.46 | 0.20 | 0.31 | 0.73 |
| 60 kg | 0.62 | 0.50 | 0.07 | 0.07 | 35.3 | 0.08 | 0.51 | 0.51 | 0.24 | 0.35 | 0.71 |
| 80 kg | 0.26 | 0.20 | 0.12 | 0.11 | 33.4 | 0.08 | 0.56 | 0.54 | 0.29 | 0.39 | 0.69 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 1.00 | 0.96 | 0.64 | 0.17 |
| long | 0.92 | 0.90 | 0.71 | 0.36 |
| sphere | 0.99 | 0.97 | 1.00 | 0.96 |
| cylinder | 0.56 | 0.51 | 0.40 | 0.21 |
| arch | 0.64 | 0.53 | 0.29 | 0.01 |
| dumbbell | 0.94 | 0.85 | 0.44 | 0.14 |
| t_shape | 0.97 | 0.92 | 0.72 | 0.12 |
| l_shape (unseen) | 0.99 | 0.96 | 0.74 | 0.18 |
| u_channel (unseen) | 0.99 | 0.94 | 0.65 | 0.26 |
| plus (unseen) | 0.85 | 0.81 | 0.58 | 0.14 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.16 | 0.15 | 0.14 | 0.16 |
| long | 0.35 | 0.31 | 0.34 | 0.39 |
| sphere | 0.06 | 0.11 | 0.21 | 0.26 |
| cylinder | 0.22 | 0.36 | 0.42 | 0.36 |
| arch | 0.01 | 0.01 | 0.01 | 0.00 |
| dumbbell | 0.10 | 0.14 | 0.19 | 0.21 |
| t_shape | 0.20 | 0.28 | 0.28 | 0.36 |
| l_shape | 0.18 | 0.30 | 0.36 | 0.47 |
| u_channel | 0.17 | 0.21 | 0.30 | 0.39 |
| plus | 0.07 | 0.10 | 0.19 | 0.28 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.94 | 0.89 | 0.72 | 0.41 |
| B_left | 0.91 | 0.91 | 0.69 | 0.26 |
| C_backright | 0.88 | 0.84 | 0.55 | 0.21 |
| D_far_turn | 0.81 | 0.70 | 0.52 | 0.14 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| standard | 0.91 | 0.91 | 0.59 | 0.29 |
| standard swapped | 0.91 | 0.79 | 0.68 | 0.27 |
| flank | 0.86 | 0.88 | 0.59 | 0.27 |
| flank swapped | 0.87 | 0.82 | 0.65 | 0.23 |
| goal_behind | 0.88 | 0.81 | 0.65 | 0.27 |
| goal_behind swapped | 0.88 | 0.80 | 0.54 | 0.22 |
