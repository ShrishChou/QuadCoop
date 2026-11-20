# Pair evaluation: obs-D-geom_hist-s0-it7000-dev7100

policy: checkpoint logs/marl2/obsD_mappo_geom_hist_s0/model_7000.pt (iteration 7000, mappo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.82 | 0.78 | 0.03 | 0.04 | 17.4 | 0.13 | 0.52 | 0.29 | 0.16 | 0.29 | 0.63 |
| 40 kg | 0.85 | 0.72 | 0.02 | 0.04 | 23.2 | 0.11 | 0.57 | 0.38 | 0.22 | 0.34 | 0.65 |
| 60 kg | 0.62 | 0.56 | 0.09 | 0.06 | 35.2 | 0.11 | 0.59 | 0.43 | 0.25 | 0.35 | 0.63 |
| 80 kg | 0.31 | 0.26 | 0.10 | 0.07 | 35.1 | 0.12 | 0.61 | 0.48 | 0.29 | 0.40 | 0.62 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.92 | 1.00 | 0.50 | 0.17 |
| long | 1.00 | 1.00 | 0.83 | 0.42 |
| sphere | 0.92 | 1.00 | 1.00 | 1.00 |
| cylinder | 0.75 | 0.67 | 0.42 | 0.25 |
| arch | 0.17 | 0.50 | 0.25 | 0.08 |
| dumbbell | 0.92 | 0.83 | 0.42 | 0.00 |
| t_shape | 1.00 | 1.00 | 0.75 | 0.17 |
| l_shape (unseen) | 1.00 | 1.00 | 0.92 | 0.42 |
| u_channel (unseen) | 0.92 | 0.92 | 0.75 | 0.33 |
| plus (unseen) | 0.67 | 0.58 | 0.42 | 0.25 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.19 | 0.24 | 0.13 | 0.13 |
| long | 0.31 | 0.36 | 0.36 | 0.38 |
| sphere | 0.11 | 0.16 | 0.29 | 0.32 |
| cylinder | 0.24 | 0.31 | 0.40 | 0.31 |
| arch | 0.04 | 0.03 | 0.01 | 0.01 |
| dumbbell | 0.07 | 0.13 | 0.15 | 0.18 |
| t_shape | 0.23 | 0.31 | 0.25 | 0.34 |
| l_shape | 0.17 | 0.33 | 0.33 | 0.45 |
| u_channel | 0.14 | 0.17 | 0.23 | 0.36 |
| plus | 0.14 | 0.20 | 0.31 | 0.36 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.87 | 0.87 | 0.73 | 0.50 |
| B_left | 0.80 | 0.87 | 0.63 | 0.43 |
| C_backright | 0.83 | 0.93 | 0.60 | 0.20 |
| D_far_turn | 0.80 | 0.73 | 0.53 | 0.10 |
