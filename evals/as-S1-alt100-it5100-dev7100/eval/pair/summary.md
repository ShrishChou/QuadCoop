# Pair evaluation: as-S1-alt100-it5100-dev7100

policy: checkpoint logs/marl2/asS1_alt100_s0/model_5100.pt (iteration 5100, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.87 | 0.83 | 0.02 | 0.03 | 19.4 | 0.09 | 0.40 | 0.37 | 0.14 | 0.26 | 0.72 |
| 40 kg | 0.83 | 0.75 | 0.04 | 0.03 | 23.2 | 0.10 | 0.49 | 0.44 | 0.21 | 0.33 | 0.72 |
| 60 kg | 0.58 | 0.49 | 0.08 | 0.08 | 32.5 | 0.10 | 0.54 | 0.48 | 0.25 | 0.36 | 0.70 |
| 80 kg | 0.28 | 0.23 | 0.13 | 0.09 | 34.3 | 0.10 | 0.61 | 0.49 | 0.28 | 0.37 | 0.69 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.97 | 0.96 | 0.67 | 0.17 |
| long | 0.90 | 0.94 | 0.69 | 0.29 |
| sphere | 0.92 | 0.94 | 0.99 | 0.96 |
| cylinder | 0.56 | 0.47 | 0.33 | 0.24 |
| arch | 0.68 | 0.51 | 0.19 | 0.01 |
| dumbbell | 0.92 | 0.83 | 0.38 | 0.14 |
| t_shape | 0.94 | 0.92 | 0.61 | 0.14 |
| l_shape (unseen) | 1.00 | 0.97 | 0.79 | 0.28 |
| u_channel (unseen) | 1.00 | 0.93 | 0.71 | 0.32 |
| plus (unseen) | 0.78 | 0.83 | 0.46 | 0.22 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.14 | 0.16 | 0.13 | 0.08 |
| long | 0.28 | 0.30 | 0.33 | 0.39 |
| sphere | 0.05 | 0.14 | 0.22 | 0.29 |
| cylinder | 0.22 | 0.30 | 0.39 | 0.36 |
| arch | 0.02 | 0.02 | 0.01 | 0.01 |
| dumbbell | 0.09 | 0.14 | 0.20 | 0.18 |
| t_shape | 0.15 | 0.29 | 0.27 | 0.36 |
| l_shape | 0.19 | 0.31 | 0.37 | 0.41 |
| u_channel | 0.15 | 0.26 | 0.36 | 0.39 |
| plus | 0.08 | 0.15 | 0.18 | 0.31 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.91 | 0.89 | 0.71 | 0.43 |
| B_left | 0.88 | 0.86 | 0.63 | 0.29 |
| C_backright | 0.87 | 0.86 | 0.51 | 0.19 |
| D_far_turn | 0.82 | 0.72 | 0.47 | 0.19 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| standard | 0.91 | 0.88 | 0.61 | 0.30 |
| standard swapped | 0.88 | 0.83 | 0.59 | 0.26 |
| flank | 0.86 | 0.81 | 0.60 | 0.28 |
| flank swapped | 0.88 | 0.83 | 0.59 | 0.30 |
| goal_behind | 0.84 | 0.82 | 0.57 | 0.21 |
| goal_behind swapped | 0.84 | 0.82 | 0.53 | 0.31 |
