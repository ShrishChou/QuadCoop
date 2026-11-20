# Pair evaluation: sg-train-s1001

policy: checkpoint logs/marl2/nwB_mappo_uniform_s0/model_5000.pt (iteration 5000, mappo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.91 | 0.93 | 0.01 | 0.02 | 24.8 | 0.09 | 0.48 | 0.31 | 0.14 | 0.27 | 0.67 |
| 40 kg | 0.82 | 0.87 | 0.02 | 0.07 | 27.9 | 0.10 | 0.50 | 0.43 | 0.20 | 0.32 | 0.71 |
| 60 kg | 0.58 | 0.72 | 0.11 | 0.08 | 40.7 | 0.09 | 0.52 | 0.44 | 0.22 | 0.35 | 0.71 |
| 80 kg | 0.26 | 0.47 | 0.16 | 0.13 | 42.4 | 0.10 | 0.55 | 0.48 | 0.24 | 0.35 | 0.67 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 1.00 | 1.00 | 0.75 | 0.42 |
| long | 1.00 | 1.00 | 0.58 | 0.17 |
| sphere | 0.83 | 0.83 | 1.00 | 1.00 |
| cylinder | 0.75 | 0.50 | 0.33 | 0.17 |
| arch | 0.75 | 0.42 | 0.17 | 0.00 |
| dumbbell | 0.92 | 0.83 | 0.33 | 0.00 |
| t_shape | 1.00 | 1.00 | 0.75 | 0.08 |
| l_shape (unseen) | 1.00 | 1.00 | 0.75 | 0.17 |
| u_channel (unseen) | 1.00 | 0.92 | 0.58 | 0.17 |
| plus (unseen) | 0.83 | 0.67 | 0.58 | 0.42 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.23 | 0.27 | 0.22 | 0.26 |
| long | 0.29 | 0.34 | 0.41 | 0.39 |
| sphere | 0.15 | 0.11 | 0.15 | 0.23 |
| cylinder | 0.19 | 0.33 | 0.33 | 0.23 |
| arch | 0.01 | 0.01 | 0.00 | 0.00 |
| dumbbell | 0.05 | 0.10 | 0.20 | 0.16 |
| t_shape | 0.14 | 0.25 | 0.21 | 0.24 |
| l_shape | 0.15 | 0.28 | 0.28 | 0.32 |
| u_channel | 0.13 | 0.16 | 0.19 | 0.29 |
| plus | 0.09 | 0.14 | 0.19 | 0.24 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.90 | 0.80 | 0.73 | 0.37 |
| B_left | 0.93 | 0.87 | 0.73 | 0.20 |
| C_backright | 1.00 | 0.87 | 0.57 | 0.33 |
| D_far_turn | 0.80 | 0.73 | 0.30 | 0.13 |
