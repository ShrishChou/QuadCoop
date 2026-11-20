# Pair evaluation: sg-train-s1002

policy: checkpoint logs/marl2/nwB_mappo_uniform_s0/model_5000.pt (iteration 5000, mappo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.89 | 0.89 | 0.02 | 0.02 | 22.5 | 0.09 | 0.46 | 0.35 | 0.16 | 0.30 | 0.69 |
| 40 kg | 0.83 | 0.87 | 0.07 | 0.04 | 28.2 | 0.09 | 0.53 | 0.39 | 0.21 | 0.34 | 0.70 |
| 60 kg | 0.51 | 0.66 | 0.13 | 0.07 | 41.6 | 0.09 | 0.50 | 0.45 | 0.20 | 0.31 | 0.69 |
| 80 kg | 0.18 | 0.42 | 0.21 | 0.10 | 29.6 | 0.10 | 0.53 | 0.45 | 0.21 | 0.31 | 0.70 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 1.00 | 0.92 | 0.67 | 0.08 |
| long | 1.00 | 0.92 | 0.50 | 0.17 |
| sphere | 0.83 | 1.00 | 1.00 | 0.92 |
| cylinder | 0.58 | 0.58 | 0.42 | 0.25 |
| arch | 0.75 | 0.58 | 0.08 | 0.00 |
| dumbbell | 1.00 | 0.75 | 0.33 | 0.08 |
| t_shape | 1.00 | 0.92 | 0.58 | 0.08 |
| l_shape (unseen) | 1.00 | 1.00 | 0.83 | 0.08 |
| u_channel (unseen) | 1.00 | 0.92 | 0.25 | 0.17 |
| plus (unseen) | 0.75 | 0.75 | 0.42 | 0.00 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.21 | 0.23 | 0.18 | 0.20 |
| long | 0.39 | 0.35 | 0.29 | 0.28 |
| sphere | 0.10 | 0.17 | 0.18 | 0.29 |
| cylinder | 0.25 | 0.27 | 0.24 | 0.19 |
| arch | 0.01 | 0.02 | 0.02 | 0.00 |
| dumbbell | 0.10 | 0.11 | 0.19 | 0.15 |
| t_shape | 0.19 | 0.26 | 0.23 | 0.21 |
| l_shape | 0.17 | 0.29 | 0.27 | 0.26 |
| u_channel | 0.14 | 0.16 | 0.25 | 0.22 |
| plus | 0.06 | 0.19 | 0.17 | 0.27 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.87 | 0.77 | 0.67 | 0.33 |
| B_left | 0.87 | 0.93 | 0.50 | 0.13 |
| C_backright | 0.93 | 0.83 | 0.47 | 0.17 |
| D_far_turn | 0.90 | 0.80 | 0.40 | 0.10 |
