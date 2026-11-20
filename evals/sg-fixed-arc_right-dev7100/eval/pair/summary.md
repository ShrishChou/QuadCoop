# Pair evaluation: sg-fixed-arc_right-dev7100

policy: checkpoint logs/marl2/nwB_mappo_uniform_s0/model_5000.pt (iteration 5000, mappo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.89 | 0.85 | 0.02 | 0.01 | 26.9 | 0.09 | 0.42 | 0.31 | 0.13 | 0.26 | 0.73 |
| 40 kg | 0.74 | 0.71 | 0.07 | 0.04 | 26.1 | 0.11 | 0.49 | 0.42 | 0.22 | 0.35 | 0.70 |
| 60 kg | 0.53 | 0.47 | 0.12 | 0.07 | 33.7 | 0.10 | 0.51 | 0.46 | 0.24 | 0.37 | 0.71 |
| 80 kg | 0.28 | 0.25 | 0.15 | 0.09 | 39.5 | 0.12 | 0.56 | 0.50 | 0.27 | 0.38 | 0.68 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 1.00 | 0.83 | 0.75 | 0.08 |
| long | 0.92 | 0.92 | 0.67 | 0.42 |
| sphere | 1.00 | 1.00 | 0.92 | 1.00 |
| cylinder | 0.58 | 0.42 | 0.17 | 0.00 |
| arch | 0.75 | 0.42 | 0.25 | 0.00 |
| dumbbell | 1.00 | 0.42 | 0.42 | 0.25 |
| t_shape | 1.00 | 0.92 | 0.75 | 0.33 |
| l_shape (unseen) | 0.92 | 0.92 | 0.58 | 0.33 |
| u_channel (unseen) | 1.00 | 0.83 | 0.42 | 0.25 |
| plus (unseen) | 0.75 | 0.75 | 0.33 | 0.17 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.21 | 0.30 | 0.18 | 0.19 |
| long | 0.30 | 0.37 | 0.31 | 0.41 |
| sphere | 0.06 | 0.14 | 0.38 | 0.48 |
| cylinder | 0.26 | 0.40 | 0.55 | 0.39 |
| arch | 0.01 | 0.01 | 0.02 | 0.00 |
| dumbbell | 0.05 | 0.17 | 0.13 | 0.26 |
| t_shape | 0.14 | 0.19 | 0.22 | 0.36 |
| l_shape | 0.12 | 0.36 | 0.43 | 0.31 |
| u_channel | 0.07 | 0.13 | 0.13 | 0.23 |
| plus | 0.04 | 0.09 | 0.07 | 0.06 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.83 | 0.80 | 0.57 | 0.30 |
| B_left | 0.93 | 0.77 | 0.53 | 0.27 |
| C_backright | 0.90 | 0.73 | 0.47 | 0.27 |
| D_far_turn | 0.90 | 0.67 | 0.53 | 0.30 |
