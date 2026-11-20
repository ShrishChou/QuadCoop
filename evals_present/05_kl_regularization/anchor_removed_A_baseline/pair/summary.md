# Pair evaluation: obs-Ar2-base-s0-it7000-dev7100

policy: checkpoint logs/marl2/obsAr2_mappo_base_s0/model_7000.pt (iteration 7000, mappo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.42 | 0.47 | 0.04 | 0.06 | 30.3 | 0.01 | 0.36 | 0.36 | 0.08 | 0.15 | 0.88 |
| 40 kg | 0.29 | 0.33 | 0.07 | 0.04 | 36.6 | 0.01 | 0.40 | 0.31 | 0.09 | 0.16 | 0.87 |
| 60 kg | 0.14 | 0.15 | 0.07 | 0.10 | 28.4 | 0.01 | 0.56 | 0.31 | 0.12 | 0.18 | 0.86 |
| 80 kg | 0.06 | 0.07 | 0.09 | 0.02 | 40.6 | 0.00 | 0.58 | 0.32 | 0.13 | 0.18 | 0.83 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.83 | 0.67 | 0.33 | 0.00 |
| long | 0.67 | 0.42 | 0.00 | 0.00 |
| sphere | 0.50 | 0.50 | 0.58 | 0.33 |
| cylinder | 0.58 | 0.42 | 0.25 | 0.17 |
| arch | 0.33 | 0.08 | 0.08 | 0.00 |
| dumbbell | 0.00 | 0.08 | 0.00 | 0.00 |
| t_shape | 0.25 | 0.17 | 0.08 | 0.00 |
| l_shape (unseen) | 0.67 | 0.50 | 0.08 | 0.08 |
| u_channel (unseen) | 0.33 | 0.08 | 0.00 | 0.00 |
| plus (unseen) | 0.08 | 0.00 | 0.00 | 0.00 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.13 | 0.07 | 0.18 | 0.19 |
| long | 0.12 | 0.14 | 0.18 | 0.27 |
| sphere | 0.07 | 0.16 | 0.13 | 0.13 |
| cylinder | 0.14 | 0.22 | 0.28 | 0.29 |
| arch | 0.01 | 0.00 | 0.00 | 0.00 |
| dumbbell | 0.03 | 0.06 | 0.12 | 0.09 |
| t_shape | 0.07 | 0.06 | 0.14 | 0.14 |
| l_shape | 0.10 | 0.10 | 0.07 | 0.08 |
| u_channel | 0.10 | 0.05 | 0.05 | 0.11 |
| plus | 0.03 | 0.02 | 0.09 | 0.04 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.40 | 0.27 | 0.20 | 0.13 |
| B_left | 0.33 | 0.40 | 0.20 | 0.03 |
| C_backright | 0.57 | 0.23 | 0.10 | 0.03 |
| D_far_turn | 0.40 | 0.27 | 0.07 | 0.03 |
