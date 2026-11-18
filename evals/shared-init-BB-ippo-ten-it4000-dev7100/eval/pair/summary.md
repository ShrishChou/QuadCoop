# Pair evaluation: shared-init-BB-ippo-ten-it4000-dev7100

policy: checkpoint logs/shared_init/BB_ippo_ten_4000.pt (iteration 4000, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.88 | 0.83 | 0.03 | 0.02 | 17.3 | 0.08 | 0.39 | 0.39 | 0.14 | 0.26 | 0.71 |
| 40 kg | 0.82 | 0.75 | 0.04 | 0.05 | 23.6 | 0.09 | 0.46 | 0.46 | 0.19 | 0.30 | 0.71 |
| 60 kg | 0.58 | 0.49 | 0.09 | 0.09 | 35.8 | 0.09 | 0.50 | 0.49 | 0.23 | 0.33 | 0.70 |
| 80 kg | 0.24 | 0.20 | 0.13 | 0.11 | 33.0 | 0.09 | 0.54 | 0.54 | 0.27 | 0.37 | 0.69 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.99 | 0.94 | 0.47 | 0.07 |
| long | 0.90 | 0.99 | 0.65 | 0.38 |
| sphere | 0.94 | 0.99 | 0.96 | 0.96 |
| cylinder | 0.60 | 0.47 | 0.35 | 0.21 |
| arch | 0.65 | 0.60 | 0.28 | 0.04 |
| dumbbell | 0.94 | 0.65 | 0.49 | 0.14 |
| t_shape | 0.94 | 0.96 | 0.69 | 0.15 |
| l_shape (unseen) | 0.99 | 0.97 | 0.76 | 0.15 |
| u_channel (unseen) | 1.00 | 0.86 | 0.61 | 0.11 |
| plus (unseen) | 0.85 | 0.82 | 0.54 | 0.19 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.12 | 0.13 | 0.10 | 0.07 |
| long | 0.29 | 0.30 | 0.33 | 0.41 |
| sphere | 0.08 | 0.14 | 0.24 | 0.33 |
| cylinder | 0.20 | 0.26 | 0.32 | 0.31 |
| arch | 0.01 | 0.01 | 0.00 | 0.00 |
| dumbbell | 0.11 | 0.15 | 0.21 | 0.26 |
| t_shape | 0.20 | 0.26 | 0.28 | 0.33 |
| l_shape | 0.18 | 0.25 | 0.32 | 0.37 |
| u_channel | 0.17 | 0.25 | 0.26 | 0.34 |
| plus | 0.08 | 0.15 | 0.19 | 0.26 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.92 | 0.88 | 0.69 | 0.41 |
| B_left | 0.91 | 0.87 | 0.58 | 0.20 |
| C_backright | 0.87 | 0.84 | 0.55 | 0.20 |
| D_far_turn | 0.82 | 0.71 | 0.50 | 0.16 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| standard | 0.88 | 0.82 | 0.62 | 0.23 |
| standard swapped | 0.89 | 0.83 | 0.58 | 0.26 |
| flank | 0.85 | 0.82 | 0.61 | 0.23 |
| flank swapped | 0.90 | 0.82 | 0.57 | 0.28 |
| goal_behind | 0.88 | 0.85 | 0.56 | 0.23 |
| goal_behind swapped | 0.88 | 0.79 | 0.54 | 0.22 |
