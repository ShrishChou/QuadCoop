# Pair evaluation: as-S4sep-bbsep-it6100-dev7100

policy: checkpoint logs/marl2/asS4sep_bbsep_s0/model_6100.pt (iteration 6100, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.87 | 0.84 | 0.04 | 0.02 | 20.0 | 0.09 | 0.38 | 0.43 | 0.16 | 0.29 | 0.72 |
| 40 kg | 0.82 | 0.77 | 0.03 | 0.04 | 23.2 | 0.09 | 0.46 | 0.50 | 0.23 | 0.36 | 0.72 |
| 60 kg | 0.58 | 0.51 | 0.09 | 0.08 | 33.5 | 0.09 | 0.52 | 0.55 | 0.26 | 0.37 | 0.71 |
| 80 kg | 0.29 | 0.24 | 0.14 | 0.11 | 35.7 | 0.10 | 0.54 | 0.59 | 0.30 | 0.40 | 0.70 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.97 | 0.97 | 0.64 | 0.19 |
| long | 0.89 | 0.92 | 0.69 | 0.39 |
| sphere | 0.93 | 0.94 | 0.94 | 0.93 |
| cylinder | 0.56 | 0.40 | 0.31 | 0.28 |
| arch | 0.76 | 0.54 | 0.29 | 0.01 |
| dumbbell | 0.90 | 0.86 | 0.36 | 0.14 |
| t_shape | 0.99 | 0.93 | 0.71 | 0.24 |
| l_shape (unseen) | 1.00 | 0.97 | 0.75 | 0.21 |
| u_channel (unseen) | 0.96 | 0.93 | 0.65 | 0.24 |
| plus (unseen) | 0.78 | 0.78 | 0.49 | 0.29 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.14 | 0.12 | 0.12 | 0.13 |
| long | 0.31 | 0.34 | 0.33 | 0.41 |
| sphere | 0.06 | 0.16 | 0.24 | 0.27 |
| cylinder | 0.28 | 0.43 | 0.42 | 0.39 |
| arch | 0.02 | 0.01 | 0.01 | 0.01 |
| dumbbell | 0.10 | 0.16 | 0.23 | 0.19 |
| t_shape | 0.23 | 0.28 | 0.32 | 0.41 |
| l_shape | 0.23 | 0.34 | 0.40 | 0.46 |
| u_channel | 0.16 | 0.29 | 0.34 | 0.42 |
| plus | 0.10 | 0.17 | 0.25 | 0.33 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.93 | 0.92 | 0.75 | 0.47 |
| B_left | 0.88 | 0.83 | 0.64 | 0.33 |
| C_backright | 0.88 | 0.79 | 0.52 | 0.18 |
| D_far_turn | 0.81 | 0.76 | 0.42 | 0.18 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| standard | 0.90 | 0.82 | 0.58 | 0.33 |
| standard swapped | 0.86 | 0.84 | 0.59 | 0.30 |
| flank | 0.90 | 0.82 | 0.62 | 0.26 |
| flank swapped | 0.85 | 0.84 | 0.62 | 0.30 |
| goal_behind | 0.87 | 0.82 | 0.57 | 0.32 |
| goal_behind swapped | 0.87 | 0.82 | 0.52 | 0.25 |
