# Pair evaluation: place-nwA-ippo-it5000-r2

policy: checkpoint logs/marl2/nwA_ippo_uniform_s0/model_5000.pt (iteration 5000, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.86 | 0.82 | 0.02 | 0.03 | 19.0 | 0.09 | 0.41 | 0.40 | 0.16 | 0.29 | 0.71 |
| 40 kg | 0.82 | 0.74 | 0.04 | 0.03 | 23.8 | 0.09 | 0.49 | 0.46 | 0.21 | 0.32 | 0.72 |
| 60 kg | 0.58 | 0.50 | 0.08 | 0.08 | 32.4 | 0.09 | 0.54 | 0.50 | 0.25 | 0.35 | 0.72 |
| 80 kg | 0.27 | 0.25 | 0.12 | 0.11 | 34.5 | 0.09 | 0.59 | 0.52 | 0.28 | 0.37 | 0.71 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.99 | 0.97 | 0.54 | 0.15 |
| long | 0.88 | 0.92 | 0.81 | 0.36 |
| sphere | 0.94 | 0.99 | 0.99 | 0.97 |
| cylinder | 0.54 | 0.47 | 0.31 | 0.22 |
| arch | 0.60 | 0.40 | 0.19 | 0.01 |
| dumbbell | 0.94 | 0.79 | 0.47 | 0.10 |
| t_shape | 0.97 | 0.94 | 0.64 | 0.18 |
| l_shape (unseen) | 0.99 | 0.97 | 0.75 | 0.32 |
| u_channel (unseen) | 0.94 | 0.92 | 0.62 | 0.21 |
| plus (unseen) | 0.79 | 0.81 | 0.44 | 0.21 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.18 | 0.16 | 0.16 | 0.12 |
| long | 0.29 | 0.30 | 0.31 | 0.37 |
| sphere | 0.06 | 0.15 | 0.24 | 0.27 |
| cylinder | 0.29 | 0.38 | 0.37 | 0.35 |
| arch | 0.02 | 0.03 | 0.02 | 0.01 |
| dumbbell | 0.10 | 0.16 | 0.19 | 0.20 |
| t_shape | 0.22 | 0.27 | 0.29 | 0.38 |
| l_shape | 0.20 | 0.31 | 0.35 | 0.44 |
| u_channel | 0.15 | 0.22 | 0.31 | 0.39 |
| plus | 0.08 | 0.12 | 0.23 | 0.27 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.89 | 0.86 | 0.69 | 0.38 |
| B_left | 0.89 | 0.84 | 0.67 | 0.33 |
| C_backright | 0.87 | 0.86 | 0.51 | 0.21 |
| D_far_turn | 0.78 | 0.72 | 0.43 | 0.17 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| standard | 0.92 | 0.81 | 0.57 | 0.25 |
| standard swapped | 0.85 | 0.84 | 0.57 | 0.34 |
| flank | 0.85 | 0.82 | 0.60 | 0.25 |
| flank swapped | 0.84 | 0.84 | 0.54 | 0.21 |
| goal_behind | 0.84 | 0.80 | 0.66 | 0.28 |
| goal_behind swapped | 0.85 | 0.79 | 0.53 | 0.32 |
