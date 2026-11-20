# Pair evaluation: obs-Br2-geom-s0-it7000-dev7100

policy: checkpoint logs/marl2/obsBr2_mappo_geom_s0/model_7000.pt (iteration 7000, mappo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.43 | 0.53 | 0.00 | 0.03 | 31.5 | 0.02 | 0.40 | 0.32 | 0.08 | 0.14 | 0.88 |
| 40 kg | 0.38 | 0.36 | 0.03 | 0.05 | 37.5 | 0.01 | 0.42 | 0.31 | 0.10 | 0.19 | 0.90 |
| 60 kg | 0.26 | 0.24 | 0.06 | 0.05 | 39.6 | 0.01 | 0.49 | 0.35 | 0.13 | 0.21 | 0.86 |
| 80 kg | 0.12 | 0.10 | 0.07 | 0.04 | 28.5 | 0.01 | 0.58 | 0.41 | 0.22 | 0.29 | 0.81 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.92 | 0.83 | 0.50 | 0.08 |
| long | 0.33 | 0.67 | 0.25 | 0.00 |
| sphere | 0.75 | 0.83 | 0.75 | 0.75 |
| cylinder | 0.58 | 0.33 | 0.25 | 0.08 |
| arch | 0.00 | 0.17 | 0.08 | 0.00 |
| dumbbell | 0.00 | 0.08 | 0.08 | 0.00 |
| t_shape | 0.33 | 0.17 | 0.25 | 0.08 |
| l_shape (unseen) | 0.67 | 0.33 | 0.25 | 0.17 |
| u_channel (unseen) | 0.17 | 0.08 | 0.00 | 0.00 |
| plus (unseen) | 0.58 | 0.33 | 0.17 | 0.00 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.17 | 0.22 | 0.40 | 0.41 |
| long | 0.05 | 0.15 | 0.22 | 0.50 |
| sphere | 0.06 | 0.16 | 0.14 | 0.30 |
| cylinder | 0.12 | 0.20 | 0.18 | 0.23 |
| arch | 0.01 | 0.01 | 0.01 | 0.01 |
| dumbbell | 0.03 | 0.03 | 0.05 | 0.13 |
| t_shape | 0.06 | 0.06 | 0.13 | 0.24 |
| l_shape | 0.10 | 0.09 | 0.08 | 0.08 |
| u_channel | 0.05 | 0.05 | 0.05 | 0.16 |
| plus | 0.10 | 0.09 | 0.10 | 0.11 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.50 | 0.33 | 0.27 | 0.10 |
| B_left | 0.50 | 0.53 | 0.40 | 0.20 |
| C_backright | 0.40 | 0.30 | 0.20 | 0.10 |
| D_far_turn | 0.33 | 0.37 | 0.17 | 0.07 |
