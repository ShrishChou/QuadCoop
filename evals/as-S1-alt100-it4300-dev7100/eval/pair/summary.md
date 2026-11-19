# Pair evaluation: as-S1-alt100-it4300-dev7100

policy: checkpoint logs/marl2/asS1_alt100_s0/model_4300.pt (iteration 4300, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.89 | 0.86 | 0.01 | 0.03 | 17.8 | 0.08 | 0.44 | 0.37 | 0.15 | 0.28 | 0.71 |
| 40 kg | 0.82 | 0.75 | 0.04 | 0.04 | 23.0 | 0.09 | 0.51 | 0.44 | 0.21 | 0.33 | 0.71 |
| 60 kg | 0.60 | 0.50 | 0.06 | 0.08 | 33.5 | 0.09 | 0.56 | 0.47 | 0.25 | 0.36 | 0.69 |
| 80 kg | 0.25 | 0.21 | 0.11 | 0.14 | 32.6 | 0.08 | 0.59 | 0.48 | 0.27 | 0.36 | 0.68 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.99 | 0.96 | 0.56 | 0.06 |
| long | 0.93 | 0.92 | 0.71 | 0.32 |
| sphere | 0.94 | 0.99 | 1.00 | 0.96 |
| cylinder | 0.58 | 0.44 | 0.33 | 0.21 |
| arch | 0.69 | 0.51 | 0.22 | 0.01 |
| dumbbell | 0.97 | 0.74 | 0.40 | 0.11 |
| t_shape | 0.99 | 0.99 | 0.74 | 0.17 |
| l_shape (unseen) | 0.99 | 0.97 | 0.82 | 0.29 |
| u_channel (unseen) | 0.97 | 0.97 | 0.68 | 0.21 |
| plus (unseen) | 0.88 | 0.71 | 0.50 | 0.19 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.15 | 0.20 | 0.12 | 0.07 |
| long | 0.32 | 0.31 | 0.34 | 0.36 |
| sphere | 0.08 | 0.16 | 0.23 | 0.29 |
| cylinder | 0.24 | 0.29 | 0.36 | 0.31 |
| arch | 0.01 | 0.02 | 0.01 | 0.01 |
| dumbbell | 0.10 | 0.15 | 0.20 | 0.19 |
| t_shape | 0.22 | 0.30 | 0.30 | 0.34 |
| l_shape | 0.22 | 0.33 | 0.41 | 0.43 |
| u_channel | 0.16 | 0.27 | 0.32 | 0.39 |
| plus | 0.06 | 0.13 | 0.20 | 0.28 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.94 | 0.87 | 0.69 | 0.41 |
| B_left | 0.90 | 0.86 | 0.64 | 0.27 |
| C_backright | 0.89 | 0.82 | 0.56 | 0.19 |
| D_far_turn | 0.83 | 0.73 | 0.49 | 0.14 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| standard | 0.89 | 0.82 | 0.62 | 0.31 |
| standard swapped | 0.89 | 0.88 | 0.64 | 0.28 |
| flank | 0.89 | 0.84 | 0.67 | 0.23 |
| flank swapped | 0.87 | 0.84 | 0.55 | 0.23 |
| goal_behind | 0.91 | 0.78 | 0.54 | 0.21 |
| goal_behind swapped | 0.91 | 0.77 | 0.55 | 0.27 |
