# Pair evaluation: as-S1-alt100-it6100-dev7100

policy: checkpoint logs/marl2/asS1_alt100_s0/model_6100.pt (iteration 6100, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.86 | 0.83 | 0.03 | 0.02 | 19.4 | 0.09 | 0.39 | 0.39 | 0.15 | 0.27 | 0.71 |
| 40 kg | 0.82 | 0.75 | 0.03 | 0.04 | 24.2 | 0.10 | 0.48 | 0.45 | 0.22 | 0.34 | 0.71 |
| 60 kg | 0.57 | 0.49 | 0.07 | 0.10 | 32.7 | 0.10 | 0.53 | 0.48 | 0.25 | 0.36 | 0.69 |
| 80 kg | 0.28 | 0.22 | 0.11 | 0.14 | 33.8 | 0.10 | 0.60 | 0.53 | 0.31 | 0.41 | 0.69 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.99 | 0.96 | 0.57 | 0.18 |
| long | 0.93 | 0.89 | 0.74 | 0.44 |
| sphere | 0.93 | 0.97 | 0.92 | 0.93 |
| cylinder | 0.58 | 0.47 | 0.33 | 0.19 |
| arch | 0.64 | 0.49 | 0.19 | 0.06 |
| dumbbell | 0.90 | 0.82 | 0.42 | 0.04 |
| t_shape | 0.97 | 0.97 | 0.68 | 0.26 |
| l_shape (unseen) | 0.96 | 0.93 | 0.76 | 0.29 |
| u_channel (unseen) | 0.99 | 0.90 | 0.62 | 0.21 |
| plus (unseen) | 0.74 | 0.76 | 0.50 | 0.17 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.15 | 0.16 | 0.14 | 0.14 |
| long | 0.26 | 0.32 | 0.30 | 0.44 |
| sphere | 0.05 | 0.13 | 0.24 | 0.30 |
| cylinder | 0.27 | 0.35 | 0.38 | 0.38 |
| arch | 0.02 | 0.02 | 0.01 | 0.02 |
| dumbbell | 0.08 | 0.14 | 0.15 | 0.17 |
| t_shape | 0.18 | 0.33 | 0.34 | 0.42 |
| l_shape | 0.20 | 0.32 | 0.39 | 0.51 |
| u_channel | 0.16 | 0.25 | 0.33 | 0.43 |
| plus | 0.09 | 0.15 | 0.21 | 0.33 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.93 | 0.90 | 0.72 | 0.44 |
| B_left | 0.86 | 0.84 | 0.61 | 0.32 |
| C_backright | 0.86 | 0.81 | 0.56 | 0.20 |
| D_far_turn | 0.81 | 0.72 | 0.41 | 0.15 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| standard | 0.88 | 0.82 | 0.57 | 0.29 |
| standard swapped | 0.84 | 0.82 | 0.59 | 0.29 |
| flank | 0.88 | 0.83 | 0.61 | 0.27 |
| flank swapped | 0.93 | 0.87 | 0.58 | 0.22 |
| goal_behind | 0.82 | 0.78 | 0.57 | 0.31 |
| goal_behind swapped | 0.83 | 0.77 | 0.51 | 0.29 |
