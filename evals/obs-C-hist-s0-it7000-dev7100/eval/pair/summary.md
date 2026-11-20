# Pair evaluation: obs-C-hist-s0-it7000-dev7100

policy: checkpoint logs/marl2/obsC_mappo_hist_s0/model_7000.pt (iteration 7000, mappo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.91 | 0.83 | 0.02 | 0.02 | 17.6 | 0.12 | 0.53 | 0.31 | 0.18 | 0.31 | 0.63 |
| 40 kg | 0.84 | 0.78 | 0.03 | 0.04 | 22.2 | 0.12 | 0.59 | 0.36 | 0.20 | 0.30 | 0.66 |
| 60 kg | 0.55 | 0.47 | 0.12 | 0.06 | 33.3 | 0.11 | 0.60 | 0.41 | 0.22 | 0.31 | 0.62 |
| 80 kg | 0.27 | 0.23 | 0.13 | 0.09 | 30.8 | 0.11 | 0.66 | 0.46 | 0.30 | 0.40 | 0.63 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 1.00 | 1.00 | 0.75 | 0.00 |
| long | 1.00 | 0.92 | 0.67 | 0.42 |
| sphere | 1.00 | 0.83 | 1.00 | 1.00 |
| cylinder | 0.67 | 0.58 | 0.33 | 0.17 |
| arch | 0.58 | 0.42 | 0.17 | 0.00 |
| dumbbell | 1.00 | 0.92 | 0.42 | 0.08 |
| t_shape | 1.00 | 0.92 | 0.75 | 0.17 |
| l_shape (unseen) | 1.00 | 1.00 | 0.58 | 0.33 |
| u_channel (unseen) | 1.00 | 1.00 | 0.42 | 0.33 |
| plus (unseen) | 0.83 | 0.83 | 0.42 | 0.17 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.24 | 0.15 | 0.16 | 0.09 |
| long | 0.43 | 0.41 | 0.39 | 0.53 |
| sphere | 0.12 | 0.19 | 0.25 | 0.45 |
| cylinder | 0.30 | 0.32 | 0.34 | 0.38 |
| arch | 0.01 | 0.02 | 0.01 | 0.01 |
| dumbbell | 0.07 | 0.16 | 0.18 | 0.20 |
| t_shape | 0.22 | 0.22 | 0.21 | 0.36 |
| l_shape | 0.19 | 0.25 | 0.26 | 0.41 |
| u_channel | 0.15 | 0.21 | 0.19 | 0.30 |
| plus | 0.08 | 0.09 | 0.21 | 0.26 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.97 | 0.83 | 0.73 | 0.40 |
| B_left | 0.80 | 0.83 | 0.60 | 0.33 |
| C_backright | 1.00 | 0.93 | 0.57 | 0.23 |
| D_far_turn | 0.87 | 0.77 | 0.30 | 0.10 |
