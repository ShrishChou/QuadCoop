# Pair evaluation: as-S4sep-bbsep-it6100-fresh7500

policy: checkpoint logs/marl2/asS4sep_bbsep_s0/model_6100.pt (iteration 6100, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.88 | 0.84 | 0.02 | 0.03 | 19.3 | 0.09 | 0.40 | 0.42 | 0.16 | 0.30 | 0.72 |
| 40 kg | 0.83 | 0.77 | 0.04 | 0.04 | 23.7 | 0.09 | 0.46 | 0.50 | 0.22 | 0.34 | 0.74 |
| 60 kg | 0.56 | 0.46 | 0.07 | 0.09 | 33.5 | 0.10 | 0.50 | 0.54 | 0.25 | 0.35 | 0.72 |
| 80 kg | 0.27 | 0.23 | 0.12 | 0.12 | 35.0 | 0.10 | 0.54 | 0.59 | 0.30 | 0.39 | 0.71 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.97 | 0.93 | 0.54 | 0.15 |
| long | 0.94 | 0.90 | 0.60 | 0.25 |
| sphere | 0.96 | 0.97 | 1.00 | 0.89 |
| cylinder | 0.58 | 0.50 | 0.35 | 0.26 |
| arch | 0.69 | 0.69 | 0.25 | 0.01 |
| dumbbell | 0.90 | 0.76 | 0.33 | 0.14 |
| t_shape | 0.97 | 0.96 | 0.67 | 0.26 |
| l_shape (unseen) | 0.96 | 0.92 | 0.76 | 0.24 |
| u_channel (unseen) | 0.97 | 0.92 | 0.64 | 0.22 |
| plus (unseen) | 0.86 | 0.78 | 0.50 | 0.28 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.13 | 0.15 | 0.11 | 0.10 |
| long | 0.29 | 0.30 | 0.29 | 0.39 |
| sphere | 0.06 | 0.14 | 0.21 | 0.27 |
| cylinder | 0.33 | 0.40 | 0.39 | 0.35 |
| arch | 0.02 | 0.02 | 0.02 | 0.01 |
| dumbbell | 0.12 | 0.15 | 0.24 | 0.23 |
| t_shape | 0.20 | 0.28 | 0.31 | 0.40 |
| l_shape | 0.18 | 0.32 | 0.37 | 0.45 |
| u_channel | 0.20 | 0.29 | 0.35 | 0.46 |
| plus | 0.11 | 0.17 | 0.22 | 0.32 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.89 | 0.89 | 0.70 | 0.40 |
| B_left | 0.93 | 0.89 | 0.61 | 0.29 |
| C_backright | 0.87 | 0.82 | 0.57 | 0.26 |
| D_far_turn | 0.83 | 0.73 | 0.38 | 0.14 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| standard | 0.88 | 0.83 | 0.55 | 0.30 |
| standard swapped | 0.91 | 0.88 | 0.55 | 0.28 |
| flank | 0.89 | 0.82 | 0.63 | 0.26 |
| flank swapped | 0.89 | 0.81 | 0.55 | 0.24 |
| goal_behind | 0.86 | 0.79 | 0.55 | 0.28 |
| goal_behind swapped | 0.86 | 0.87 | 0.55 | 0.27 |
