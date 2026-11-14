# Pair evaluation: place-nwB-mappo-it5000

policy: checkpoint logs/marl2/nwB_mappo_uniform_s0/model_5000.pt (iteration 5000, mappo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.88 | 0.83 | 0.02 | 0.03 | 20.5 | 0.08 | 0.41 | 0.38 | 0.15 | 0.27 | 0.73 |
| 40 kg | 0.84 | 0.76 | 0.04 | 0.04 | 24.5 | 0.09 | 0.48 | 0.47 | 0.22 | 0.34 | 0.74 |
| 60 kg | 0.60 | 0.52 | 0.07 | 0.08 | 32.9 | 0.09 | 0.55 | 0.49 | 0.26 | 0.36 | 0.72 |
| 80 kg | 0.27 | 0.22 | 0.12 | 0.12 | 34.6 | 0.09 | 0.60 | 0.52 | 0.29 | 0.38 | 0.70 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.97 | 0.97 | 0.58 | 0.11 |
| long | 0.92 | 0.93 | 0.78 | 0.35 |
| sphere | 0.99 | 0.97 | 0.99 | 0.93 |
| cylinder | 0.57 | 0.50 | 0.36 | 0.22 |
| arch | 0.68 | 0.56 | 0.21 | 0.01 |
| dumbbell | 0.96 | 0.86 | 0.43 | 0.11 |
| t_shape | 0.92 | 0.92 | 0.72 | 0.24 |
| l_shape (unseen) | 1.00 | 0.97 | 0.79 | 0.31 |
| u_channel (unseen) | 0.94 | 1.00 | 0.65 | 0.28 |
| plus (unseen) | 0.86 | 0.71 | 0.44 | 0.15 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.13 | 0.13 | 0.10 | 0.11 |
| long | 0.32 | 0.31 | 0.33 | 0.33 |
| sphere | 0.05 | 0.11 | 0.20 | 0.26 |
| cylinder | 0.23 | 0.37 | 0.42 | 0.33 |
| arch | 0.02 | 0.02 | 0.01 | 0.02 |
| dumbbell | 0.10 | 0.15 | 0.21 | 0.25 |
| t_shape | 0.20 | 0.32 | 0.31 | 0.39 |
| l_shape | 0.20 | 0.35 | 0.44 | 0.52 |
| u_channel | 0.15 | 0.28 | 0.34 | 0.45 |
| plus | 0.09 | 0.14 | 0.20 | 0.26 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.93 | 0.87 | 0.69 | 0.42 |
| B_left | 0.89 | 0.87 | 0.68 | 0.34 |
| C_backright | 0.86 | 0.84 | 0.53 | 0.19 |
| D_far_turn | 0.84 | 0.77 | 0.48 | 0.13 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| standard | 0.90 | 0.82 | 0.63 | 0.26 |
| standard swapped | 0.93 | 0.86 | 0.65 | 0.34 |
| flank | 0.89 | 0.85 | 0.55 | 0.28 |
| flank swapped | 0.88 | 0.84 | 0.61 | 0.23 |
| goal_behind | 0.86 | 0.85 | 0.57 | 0.24 |
| goal_behind swapped | 0.83 | 0.82 | 0.56 | 0.28 |
