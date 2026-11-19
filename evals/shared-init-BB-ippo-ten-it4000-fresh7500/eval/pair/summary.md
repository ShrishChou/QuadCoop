# Pair evaluation: shared-init-BB-ippo-ten-it4000-fresh7500

policy: checkpoint logs/shared_init/BB_ippo_ten_4000.pt (iteration 4000, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.89 | 0.85 | 0.03 | 0.02 | 17.7 | 0.09 | 0.39 | 0.40 | 0.15 | 0.26 | 0.71 |
| 40 kg | 0.83 | 0.77 | 0.05 | 0.04 | 23.7 | 0.08 | 0.46 | 0.47 | 0.20 | 0.31 | 0.72 |
| 60 kg | 0.58 | 0.51 | 0.08 | 0.11 | 36.4 | 0.09 | 0.50 | 0.51 | 0.24 | 0.34 | 0.70 |
| 80 kg | 0.24 | 0.21 | 0.13 | 0.13 | 34.0 | 0.08 | 0.54 | 0.54 | 0.27 | 0.36 | 0.69 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.96 | 0.90 | 0.50 | 0.07 |
| long | 0.94 | 0.96 | 0.57 | 0.24 |
| sphere | 0.99 | 0.99 | 0.93 | 0.94 |
| cylinder | 0.51 | 0.51 | 0.38 | 0.22 |
| arch | 0.65 | 0.57 | 0.19 | 0.01 |
| dumbbell | 0.96 | 0.74 | 0.49 | 0.11 |
| t_shape | 0.97 | 0.97 | 0.71 | 0.18 |
| l_shape (unseen) | 1.00 | 0.90 | 0.79 | 0.25 |
| u_channel (unseen) | 0.97 | 0.90 | 0.58 | 0.18 |
| plus (unseen) | 0.92 | 0.83 | 0.68 | 0.24 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.12 | 0.12 | 0.10 | 0.08 |
| long | 0.29 | 0.32 | 0.32 | 0.39 |
| sphere | 0.08 | 0.16 | 0.26 | 0.32 |
| cylinder | 0.22 | 0.31 | 0.33 | 0.28 |
| arch | 0.01 | 0.01 | 0.01 | 0.01 |
| dumbbell | 0.10 | 0.17 | 0.24 | 0.25 |
| t_shape | 0.20 | 0.27 | 0.28 | 0.34 |
| l_shape | 0.15 | 0.24 | 0.30 | 0.35 |
| u_channel | 0.18 | 0.24 | 0.28 | 0.35 |
| plus | 0.10 | 0.20 | 0.22 | 0.30 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.92 | 0.91 | 0.68 | 0.36 |
| B_left | 0.92 | 0.84 | 0.58 | 0.23 |
| C_backright | 0.89 | 0.85 | 0.64 | 0.21 |
| D_far_turn | 0.83 | 0.72 | 0.43 | 0.18 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| standard | 0.92 | 0.82 | 0.61 | 0.25 |
| standard swapped | 0.88 | 0.83 | 0.53 | 0.23 |
| flank | 0.88 | 0.88 | 0.57 | 0.27 |
| flank swapped | 0.88 | 0.82 | 0.58 | 0.22 |
| goal_behind | 0.87 | 0.76 | 0.57 | 0.24 |
| goal_behind swapped | 0.89 | 0.84 | 0.62 | 0.27 |
