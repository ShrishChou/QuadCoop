# Pair evaluation: sg-train-s1003

policy: checkpoint logs/marl2/nwB_mappo_uniform_s0/model_5000.pt (iteration 5000, mappo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.91 | 0.90 | 0.01 | 0.00 | 23.8 | 0.09 | 0.46 | 0.31 | 0.13 | 0.25 | 0.70 |
| 40 kg | 0.80 | 0.78 | 0.07 | 0.05 | 27.8 | 0.08 | 0.49 | 0.37 | 0.17 | 0.29 | 0.69 |
| 60 kg | 0.55 | 0.65 | 0.10 | 0.07 | 41.3 | 0.10 | 0.50 | 0.47 | 0.22 | 0.34 | 0.68 |
| 80 kg | 0.25 | 0.45 | 0.17 | 0.09 | 42.0 | 0.10 | 0.54 | 0.46 | 0.23 | 0.35 | 0.69 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 1.00 | 1.00 | 0.50 | 0.00 |
| long | 1.00 | 1.00 | 0.75 | 0.33 |
| sphere | 0.92 | 1.00 | 0.92 | 1.00 |
| cylinder | 0.67 | 0.58 | 0.42 | 0.33 |
| arch | 0.75 | 0.42 | 0.08 | 0.00 |
| dumbbell | 1.00 | 0.67 | 0.42 | 0.08 |
| t_shape | 1.00 | 0.92 | 0.75 | 0.08 |
| l_shape (unseen) | 1.00 | 1.00 | 0.50 | 0.17 |
| u_channel (unseen) | 1.00 | 0.83 | 0.50 | 0.17 |
| plus (unseen) | 0.75 | 0.58 | 0.67 | 0.33 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.15 | 0.21 | 0.15 | 0.16 |
| long | 0.29 | 0.28 | 0.39 | 0.39 |
| sphere | 0.11 | 0.17 | 0.22 | 0.28 |
| cylinder | 0.25 | 0.22 | 0.37 | 0.26 |
| arch | 0.00 | 0.01 | 0.01 | 0.01 |
| dumbbell | 0.05 | 0.10 | 0.14 | 0.18 |
| t_shape | 0.16 | 0.27 | 0.27 | 0.27 |
| l_shape | 0.20 | 0.17 | 0.26 | 0.31 |
| u_channel | 0.09 | 0.19 | 0.17 | 0.25 |
| plus | 0.04 | 0.12 | 0.18 | 0.20 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.93 | 0.87 | 0.60 | 0.43 |
| B_left | 0.93 | 0.70 | 0.67 | 0.23 |
| C_backright | 0.97 | 0.87 | 0.50 | 0.23 |
| D_far_turn | 0.80 | 0.77 | 0.43 | 0.10 |
