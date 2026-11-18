# Pair evaluation: of-OFm-it6100-dev7100

policy: checkpoint logs/marl2/ofM_mappo_oppose_s0/model_6100.pt (iteration 6100, mappo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.88 | 0.83 | 0.02 | 0.02 | 19.2 | 0.10 | 0.39 | 0.40 | 0.14 | 0.26 | 0.70 |
| 40 kg | 0.82 | 0.74 | 0.03 | 0.05 | 24.4 | 0.10 | 0.49 | 0.45 | 0.21 | 0.32 | 0.71 |
| 60 kg | 0.56 | 0.48 | 0.07 | 0.09 | 33.2 | 0.10 | 0.52 | 0.49 | 0.25 | 0.36 | 0.70 |
| 80 kg | 0.25 | 0.21 | 0.13 | 0.14 | 31.8 | 0.10 | 0.57 | 0.52 | 0.29 | 0.39 | 0.69 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 1.00 | 0.93 | 0.50 | 0.08 |
| long | 0.96 | 0.90 | 0.72 | 0.42 |
| sphere | 0.96 | 0.94 | 0.99 | 0.89 |
| cylinder | 0.64 | 0.47 | 0.35 | 0.22 |
| arch | 0.54 | 0.50 | 0.26 | 0.00 |
| dumbbell | 0.93 | 0.85 | 0.31 | 0.03 |
| t_shape | 0.99 | 0.96 | 0.62 | 0.22 |
| l_shape (unseen) | 1.00 | 0.96 | 0.74 | 0.25 |
| u_channel (unseen) | 0.96 | 0.94 | 0.62 | 0.14 |
| plus (unseen) | 0.82 | 0.78 | 0.47 | 0.21 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.15 | 0.15 | 0.12 | 0.12 |
| long | 0.28 | 0.31 | 0.33 | 0.42 |
| sphere | 0.06 | 0.12 | 0.22 | 0.25 |
| cylinder | 0.24 | 0.34 | 0.42 | 0.40 |
| arch | 0.02 | 0.02 | 0.03 | 0.02 |
| dumbbell | 0.09 | 0.16 | 0.14 | 0.15 |
| t_shape | 0.19 | 0.28 | 0.29 | 0.39 |
| l_shape | 0.19 | 0.30 | 0.38 | 0.44 |
| u_channel | 0.14 | 0.26 | 0.29 | 0.37 |
| plus | 0.08 | 0.15 | 0.23 | 0.29 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.90 | 0.84 | 0.65 | 0.39 |
| B_left | 0.88 | 0.86 | 0.56 | 0.26 |
| C_backright | 0.89 | 0.86 | 0.56 | 0.18 |
| D_far_turn | 0.84 | 0.73 | 0.47 | 0.16 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| standard | 0.87 | 0.88 | 0.58 | 0.24 |
| standard swapped | 0.92 | 0.86 | 0.63 | 0.27 |
| flank | 0.84 | 0.83 | 0.58 | 0.24 |
| flank swapped | 0.87 | 0.77 | 0.58 | 0.24 |
| goal_behind | 0.89 | 0.86 | 0.52 | 0.22 |
| goal_behind swapped | 0.89 | 0.75 | 0.45 | 0.27 |
