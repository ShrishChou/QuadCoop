# Pair evaluation: shared-init-AA-ippo-ten-it4000-dev7100

policy: checkpoint logs/shared_init/AA_ippo_ten_4000.pt (iteration 4000, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.83 | 0.80 | 0.04 | 0.03 | 16.7 | 0.11 | 0.40 | 0.40 | 0.16 | 0.29 | 0.69 |
| 40 kg | 0.81 | 0.75 | 0.04 | 0.04 | 21.9 | 0.12 | 0.48 | 0.49 | 0.24 | 0.38 | 0.69 |
| 60 kg | 0.58 | 0.52 | 0.11 | 0.08 | 29.2 | 0.13 | 0.54 | 0.53 | 0.29 | 0.41 | 0.67 |
| 80 kg | 0.29 | 0.25 | 0.12 | 0.14 | 32.9 | 0.13 | 0.56 | 0.56 | 0.30 | 0.41 | 0.68 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.99 | 0.94 | 0.62 | 0.21 |
| long | 0.94 | 0.93 | 0.74 | 0.39 |
| sphere | 0.96 | 1.00 | 0.97 | 0.97 |
| cylinder | 0.57 | 0.43 | 0.29 | 0.21 |
| arch | 0.43 | 0.44 | 0.12 | 0.01 |
| dumbbell | 0.85 | 0.85 | 0.38 | 0.10 |
| t_shape | 0.93 | 0.92 | 0.69 | 0.29 |
| l_shape (unseen) | 1.00 | 0.93 | 0.85 | 0.25 |
| u_channel (unseen) | 0.96 | 0.94 | 0.69 | 0.22 |
| plus (unseen) | 0.72 | 0.67 | 0.49 | 0.22 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.20 | 0.23 | 0.18 | 0.15 |
| long | 0.34 | 0.36 | 0.36 | 0.33 |
| sphere | 0.07 | 0.16 | 0.27 | 0.32 |
| cylinder | 0.21 | 0.36 | 0.42 | 0.41 |
| arch | 0.01 | 0.02 | 0.02 | 0.02 |
| dumbbell | 0.11 | 0.15 | 0.18 | 0.19 |
| t_shape | 0.20 | 0.35 | 0.38 | 0.42 |
| l_shape | 0.24 | 0.37 | 0.47 | 0.51 |
| u_channel | 0.17 | 0.28 | 0.37 | 0.40 |
| plus | 0.08 | 0.13 | 0.21 | 0.28 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.88 | 0.84 | 0.68 | 0.44 |
| B_left | 0.89 | 0.85 | 0.64 | 0.32 |
| C_backright | 0.83 | 0.81 | 0.53 | 0.21 |
| D_far_turn | 0.73 | 0.72 | 0.49 | 0.18 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| standard | 0.85 | 0.82 | 0.60 | 0.25 |
| standard swapped | 0.83 | 0.82 | 0.61 | 0.33 |
| flank | 0.83 | 0.82 | 0.57 | 0.26 |
| flank swapped | 0.82 | 0.78 | 0.59 | 0.27 |
| goal_behind | 0.83 | 0.82 | 0.59 | 0.30 |
| goal_behind swapped | 0.84 | 0.77 | 0.55 | 0.32 |
