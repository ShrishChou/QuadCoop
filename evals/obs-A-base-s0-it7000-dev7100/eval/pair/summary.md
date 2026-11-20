# Pair evaluation: obs-A-base-s0-it7000-dev7100

policy: checkpoint logs/marl2/obsA_mappo_base_s0/model_7000.pt (iteration 7000, mappo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.88 | 0.81 | 0.01 | 0.05 | 17.6 | 0.11 | 0.53 | 0.31 | 0.17 | 0.29 | 0.63 |
| 40 kg | 0.82 | 0.71 | 0.03 | 0.03 | 22.4 | 0.11 | 0.58 | 0.39 | 0.24 | 0.38 | 0.66 |
| 60 kg | 0.57 | 0.49 | 0.11 | 0.05 | 28.5 | 0.11 | 0.61 | 0.46 | 0.28 | 0.39 | 0.66 |
| 80 kg | 0.33 | 0.28 | 0.14 | 0.07 | 33.1 | 0.11 | 0.62 | 0.52 | 0.32 | 0.43 | 0.64 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 1.00 | 0.92 | 0.67 | 0.25 |
| long | 0.92 | 0.92 | 0.58 | 0.50 |
| sphere | 0.92 | 1.00 | 0.92 | 1.00 |
| cylinder | 0.58 | 0.58 | 0.25 | 0.25 |
| arch | 0.42 | 0.42 | 0.17 | 0.00 |
| dumbbell | 1.00 | 0.92 | 0.50 | 0.08 |
| t_shape | 1.00 | 1.00 | 0.67 | 0.17 |
| l_shape (unseen) | 1.00 | 1.00 | 0.83 | 0.42 |
| u_channel (unseen) | 1.00 | 0.92 | 0.67 | 0.25 |
| plus (unseen) | 0.92 | 0.58 | 0.50 | 0.33 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.15 | 0.22 | 0.20 | 0.13 |
| long | 0.27 | 0.36 | 0.34 | 0.46 |
| sphere | 0.11 | 0.22 | 0.34 | 0.34 |
| cylinder | 0.32 | 0.50 | 0.41 | 0.49 |
| arch | 0.03 | 0.00 | 0.00 | 0.01 |
| dumbbell | 0.06 | 0.12 | 0.22 | 0.21 |
| t_shape | 0.22 | 0.28 | 0.35 | 0.37 |
| l_shape | 0.23 | 0.42 | 0.42 | 0.52 |
| u_channel | 0.20 | 0.13 | 0.22 | 0.34 |
| plus | 0.10 | 0.19 | 0.27 | 0.31 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.90 | 0.87 | 0.77 | 0.57 |
| B_left | 0.90 | 0.83 | 0.63 | 0.33 |
| C_backright | 0.93 | 0.83 | 0.53 | 0.23 |
| D_far_turn | 0.77 | 0.77 | 0.37 | 0.17 |
