# Pair evaluation: as-S4-shared-it4300-dev7100

policy: checkpoint logs/marl2/asS4_shared_s0/model_4300.pt (iteration 4300, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.87 | 0.82 | 0.03 | 0.03 | 18.7 | 0.07 | 0.40 | 0.38 | 0.13 | 0.24 | 0.71 |
| 40 kg | 0.83 | 0.76 | 0.04 | 0.04 | 24.9 | 0.08 | 0.45 | 0.46 | 0.18 | 0.28 | 0.72 |
| 60 kg | 0.54 | 0.46 | 0.07 | 0.09 | 36.8 | 0.07 | 0.48 | 0.49 | 0.20 | 0.30 | 0.70 |
| 80 kg | 0.24 | 0.19 | 0.11 | 0.10 | 32.8 | 0.08 | 0.53 | 0.52 | 0.25 | 0.35 | 0.69 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.99 | 0.93 | 0.53 | 0.04 |
| long | 0.88 | 0.93 | 0.64 | 0.35 |
| sphere | 1.00 | 0.97 | 0.97 | 0.97 |
| cylinder | 0.53 | 0.50 | 0.31 | 0.25 |
| arch | 0.65 | 0.50 | 0.10 | 0.01 |
| dumbbell | 0.90 | 0.82 | 0.44 | 0.10 |
| t_shape | 0.99 | 0.96 | 0.65 | 0.12 |
| l_shape (unseen) | 1.00 | 0.96 | 0.76 | 0.14 |
| u_channel (unseen) | 0.97 | 0.93 | 0.56 | 0.22 |
| plus (unseen) | 0.82 | 0.85 | 0.49 | 0.19 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.14 | 0.14 | 0.09 | 0.07 |
| long | 0.30 | 0.29 | 0.29 | 0.40 |
| sphere | 0.04 | 0.10 | 0.17 | 0.26 |
| cylinder | 0.19 | 0.31 | 0.30 | 0.28 |
| arch | 0.01 | 0.01 | 0.00 | 0.00 |
| dumbbell | 0.09 | 0.17 | 0.19 | 0.20 |
| t_shape | 0.19 | 0.22 | 0.25 | 0.34 |
| l_shape | 0.18 | 0.26 | 0.30 | 0.37 |
| u_channel | 0.12 | 0.18 | 0.23 | 0.33 |
| plus | 0.07 | 0.13 | 0.20 | 0.29 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.95 | 0.86 | 0.63 | 0.39 |
| B_left | 0.89 | 0.88 | 0.55 | 0.22 |
| C_backright | 0.84 | 0.86 | 0.52 | 0.20 |
| D_far_turn | 0.81 | 0.74 | 0.47 | 0.16 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| standard | 0.88 | 0.85 | 0.57 | 0.27 |
| standard swapped | 0.87 | 0.90 | 0.60 | 0.25 |
| flank | 0.86 | 0.83 | 0.57 | 0.26 |
| flank swapped | 0.83 | 0.83 | 0.51 | 0.22 |
| goal_behind | 0.91 | 0.80 | 0.53 | 0.25 |
| goal_behind swapped | 0.89 | 0.79 | 0.48 | 0.20 |
