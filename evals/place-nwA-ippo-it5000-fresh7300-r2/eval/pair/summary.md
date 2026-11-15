# Pair evaluation: place-nwA-ippo-it5000-fresh7300-r2

policy: checkpoint logs/marl2/nwA_ippo_uniform_s0/model_5000.pt (iteration 5000, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.88 | 0.85 | 0.02 | 0.02 | 19.0 | 0.08 | 0.40 | 0.39 | 0.14 | 0.25 | 0.71 |
| 40 kg | 0.83 | 0.75 | 0.04 | 0.04 | 24.2 | 0.09 | 0.47 | 0.46 | 0.20 | 0.31 | 0.72 |
| 60 kg | 0.57 | 0.50 | 0.07 | 0.09 | 33.3 | 0.09 | 0.52 | 0.50 | 0.24 | 0.35 | 0.71 |
| 80 kg | 0.28 | 0.23 | 0.12 | 0.10 | 34.3 | 0.09 | 0.57 | 0.53 | 0.27 | 0.36 | 0.71 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.99 | 0.96 | 0.53 | 0.17 |
| long | 0.92 | 0.92 | 0.78 | 0.32 |
| sphere | 1.00 | 0.99 | 0.97 | 1.00 |
| cylinder | 0.56 | 0.49 | 0.33 | 0.28 |
| arch | 0.69 | 0.51 | 0.15 | 0.03 |
| dumbbell | 0.90 | 0.75 | 0.39 | 0.19 |
| t_shape | 0.97 | 0.94 | 0.64 | 0.22 |
| l_shape (unseen) | 0.96 | 0.99 | 0.68 | 0.29 |
| u_channel (unseen) | 1.00 | 0.97 | 0.71 | 0.18 |
| plus (unseen) | 0.78 | 0.76 | 0.49 | 0.15 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.14 | 0.15 | 0.13 | 0.14 |
| long | 0.26 | 0.26 | 0.33 | 0.31 |
| sphere | 0.05 | 0.12 | 0.24 | 0.27 |
| cylinder | 0.25 | 0.31 | 0.39 | 0.33 |
| arch | 0.02 | 0.01 | 0.01 | 0.01 |
| dumbbell | 0.07 | 0.15 | 0.18 | 0.19 |
| t_shape | 0.21 | 0.25 | 0.29 | 0.42 |
| l_shape | 0.15 | 0.33 | 0.34 | 0.40 |
| u_channel | 0.15 | 0.27 | 0.32 | 0.37 |
| plus | 0.08 | 0.16 | 0.21 | 0.29 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.94 | 0.88 | 0.69 | 0.43 |
| B_left | 0.88 | 0.86 | 0.57 | 0.25 |
| C_backright | 0.90 | 0.81 | 0.55 | 0.26 |
| D_far_turn | 0.79 | 0.76 | 0.46 | 0.20 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| standard | 0.88 | 0.83 | 0.59 | 0.22 |
| standard swapped | 0.89 | 0.82 | 0.60 | 0.34 |
| flank | 0.90 | 0.81 | 0.64 | 0.29 |
| flank swapped | 0.87 | 0.87 | 0.62 | 0.30 |
| goal_behind | 0.86 | 0.83 | 0.43 | 0.26 |
| goal_behind swapped | 0.86 | 0.80 | 0.52 | 0.29 |
