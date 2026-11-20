# Pair evaluation: nw-B-mappo-uniform-it5000-dev7100

policy: checkpoint logs/marl2/nwB_mappo_uniform_s0/model_5000.pt (iteration 5000, mappo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.90 | 0.85 | 0.02 | 0.02 | 21.7 | 0.08 | 0.50 | 0.33 | 0.16 | 0.28 | 0.69 |
| 40 kg | 0.82 | 0.77 | 0.03 | 0.05 | 23.1 | 0.08 | 0.55 | 0.39 | 0.20 | 0.31 | 0.68 |
| 60 kg | 0.62 | 0.53 | 0.05 | 0.09 | 33.4 | 0.09 | 0.57 | 0.46 | 0.25 | 0.36 | 0.66 |
| 80 kg | 0.28 | 0.26 | 0.15 | 0.08 | 37.4 | 0.09 | 0.58 | 0.53 | 0.29 | 0.38 | 0.67 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 1.00 | 1.00 | 0.67 | 0.08 |
| long | 1.00 | 0.92 | 0.67 | 0.33 |
| sphere | 0.92 | 1.00 | 0.92 | 0.92 |
| cylinder | 0.75 | 0.42 | 0.33 | 0.25 |
| arch | 0.67 | 0.50 | 0.33 | 0.00 |
| dumbbell | 0.83 | 0.75 | 0.50 | 0.08 |
| t_shape | 1.00 | 1.00 | 0.67 | 0.25 |
| l_shape (unseen) | 1.00 | 0.83 | 0.83 | 0.33 |
| u_channel (unseen) | 1.00 | 1.00 | 0.83 | 0.25 |
| plus (unseen) | 0.83 | 0.83 | 0.50 | 0.33 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.08 | 0.18 | 0.11 | 0.08 |
| long | 0.37 | 0.33 | 0.33 | 0.36 |
| sphere | 0.04 | 0.09 | 0.28 | 0.29 |
| cylinder | 0.32 | 0.40 | 0.49 | 0.43 |
| arch | 0.02 | 0.00 | 0.01 | 0.01 |
| dumbbell | 0.04 | 0.12 | 0.18 | 0.14 |
| t_shape | 0.28 | 0.30 | 0.28 | 0.36 |
| l_shape | 0.19 | 0.25 | 0.36 | 0.50 |
| u_channel | 0.17 | 0.21 | 0.25 | 0.40 |
| plus | 0.13 | 0.16 | 0.25 | 0.32 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.90 | 0.90 | 0.83 | 0.47 |
| B_left | 0.90 | 0.87 | 0.73 | 0.33 |
| C_backright | 0.93 | 0.83 | 0.57 | 0.27 |
| D_far_turn | 0.87 | 0.70 | 0.37 | 0.07 |
