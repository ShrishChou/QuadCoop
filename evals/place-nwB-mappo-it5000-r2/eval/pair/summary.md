# Pair evaluation: place-nwB-mappo-it5000-r2

policy: checkpoint logs/marl2/nwB_mappo_uniform_s0/model_5000.pt (iteration 5000, mappo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.87 | 0.84 | 0.03 | 0.02 | 19.9 | 0.08 | 0.41 | 0.38 | 0.15 | 0.28 | 0.72 |
| 40 kg | 0.82 | 0.76 | 0.04 | 0.04 | 24.7 | 0.09 | 0.49 | 0.46 | 0.21 | 0.33 | 0.72 |
| 60 kg | 0.57 | 0.48 | 0.07 | 0.09 | 32.0 | 0.09 | 0.54 | 0.49 | 0.25 | 0.36 | 0.71 |
| 80 kg | 0.26 | 0.21 | 0.12 | 0.14 | 33.4 | 0.09 | 0.60 | 0.51 | 0.29 | 0.38 | 0.71 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.96 | 0.96 | 0.51 | 0.15 |
| long | 0.93 | 0.92 | 0.71 | 0.33 |
| sphere | 0.99 | 0.99 | 0.99 | 0.96 |
| cylinder | 0.56 | 0.49 | 0.33 | 0.24 |
| arch | 0.61 | 0.50 | 0.21 | 0.01 |
| dumbbell | 0.94 | 0.74 | 0.42 | 0.07 |
| t_shape | 0.97 | 0.94 | 0.65 | 0.15 |
| l_shape (unseen) | 0.99 | 0.99 | 0.76 | 0.28 |
| u_channel (unseen) | 1.00 | 0.94 | 0.67 | 0.19 |
| plus (unseen) | 0.79 | 0.79 | 0.44 | 0.25 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.14 | 0.13 | 0.10 | 0.10 |
| long | 0.34 | 0.32 | 0.32 | 0.36 |
| sphere | 0.04 | 0.11 | 0.20 | 0.25 |
| cylinder | 0.26 | 0.34 | 0.39 | 0.35 |
| arch | 0.01 | 0.02 | 0.02 | 0.01 |
| dumbbell | 0.11 | 0.18 | 0.19 | 0.22 |
| t_shape | 0.20 | 0.29 | 0.29 | 0.39 |
| l_shape | 0.21 | 0.35 | 0.43 | 0.50 |
| u_channel | 0.15 | 0.27 | 0.35 | 0.41 |
| plus | 0.08 | 0.13 | 0.21 | 0.31 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.88 | 0.86 | 0.72 | 0.41 |
| B_left | 0.92 | 0.84 | 0.59 | 0.30 |
| C_backright | 0.88 | 0.83 | 0.52 | 0.17 |
| D_far_turn | 0.81 | 0.77 | 0.45 | 0.17 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| standard | 0.91 | 0.87 | 0.60 | 0.24 |
| standard swapped | 0.90 | 0.81 | 0.58 | 0.27 |
| flank | 0.88 | 0.87 | 0.56 | 0.26 |
| flank swapped | 0.85 | 0.84 | 0.61 | 0.26 |
| goal_behind | 0.80 | 0.79 | 0.54 | 0.28 |
| goal_behind swapped | 0.90 | 0.78 | 0.53 | 0.28 |
