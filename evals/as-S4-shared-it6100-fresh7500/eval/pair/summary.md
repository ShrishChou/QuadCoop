# Pair evaluation: as-S4-shared-it6100-fresh7500

policy: checkpoint logs/marl2/asS4_shared_s0/model_6100.pt (iteration 6100, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.88 | 0.82 | 0.02 | 0.03 | 19.2 | 0.08 | 0.40 | 0.40 | 0.16 | 0.29 | 0.72 |
| 40 kg | 0.85 | 0.78 | 0.04 | 0.03 | 22.7 | 0.08 | 0.48 | 0.47 | 0.22 | 0.34 | 0.73 |
| 60 kg | 0.61 | 0.52 | 0.09 | 0.08 | 33.8 | 0.08 | 0.53 | 0.52 | 0.26 | 0.37 | 0.72 |
| 80 kg | 0.26 | 0.21 | 0.13 | 0.13 | 33.8 | 0.08 | 0.56 | 0.57 | 0.30 | 0.39 | 0.71 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.97 | 0.97 | 0.65 | 0.18 |
| long | 0.93 | 0.90 | 0.72 | 0.22 |
| sphere | 0.89 | 1.00 | 0.94 | 0.96 |
| cylinder | 0.62 | 0.50 | 0.35 | 0.28 |
| arch | 0.67 | 0.65 | 0.28 | 0.01 |
| dumbbell | 0.97 | 0.81 | 0.38 | 0.12 |
| t_shape | 0.99 | 0.90 | 0.72 | 0.26 |
| l_shape (unseen) | 0.97 | 0.97 | 0.79 | 0.24 |
| u_channel (unseen) | 0.99 | 0.93 | 0.75 | 0.12 |
| plus (unseen) | 0.82 | 0.85 | 0.47 | 0.19 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.13 | 0.13 | 0.12 | 0.12 |
| long | 0.33 | 0.26 | 0.30 | 0.34 |
| sphere | 0.08 | 0.16 | 0.25 | 0.33 |
| cylinder | 0.27 | 0.42 | 0.44 | 0.39 |
| arch | 0.02 | 0.02 | 0.01 | 0.01 |
| dumbbell | 0.10 | 0.16 | 0.20 | 0.23 |
| t_shape | 0.19 | 0.27 | 0.33 | 0.37 |
| l_shape | 0.17 | 0.32 | 0.39 | 0.45 |
| u_channel | 0.18 | 0.29 | 0.35 | 0.46 |
| plus | 0.09 | 0.15 | 0.23 | 0.30 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.92 | 0.93 | 0.74 | 0.39 |
| B_left | 0.92 | 0.88 | 0.60 | 0.24 |
| C_backright | 0.88 | 0.83 | 0.62 | 0.24 |
| D_far_turn | 0.81 | 0.75 | 0.46 | 0.16 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| standard | 0.88 | 0.84 | 0.61 | 0.28 |
| standard swapped | 0.89 | 0.92 | 0.62 | 0.24 |
| flank | 0.88 | 0.83 | 0.67 | 0.27 |
| flank swapped | 0.88 | 0.89 | 0.64 | 0.22 |
| goal_behind | 0.86 | 0.78 | 0.57 | 0.28 |
| goal_behind swapped | 0.91 | 0.83 | 0.52 | 0.28 |
