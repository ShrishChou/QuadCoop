# Pair evaluation: sg-fixed-straight-dev7100

policy: checkpoint logs/marl2/nwB_mappo_uniform_s0/model_5000.pt (iteration 5000, mappo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.88 | 0.82 | 0.00 | 0.04 | 18.9 | 0.09 | 0.48 | 0.30 | 0.14 | 0.25 | 0.70 |
| 40 kg | 0.82 | 0.73 | 0.03 | 0.06 | 24.3 | 0.10 | 0.52 | 0.40 | 0.20 | 0.32 | 0.67 |
| 60 kg | 0.61 | 0.50 | 0.12 | 0.06 | 34.8 | 0.11 | 0.56 | 0.44 | 0.23 | 0.33 | 0.69 |
| 80 kg | 0.29 | 0.25 | 0.17 | 0.08 | 33.3 | 0.10 | 0.58 | 0.48 | 0.26 | 0.36 | 0.66 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 1.00 | 1.00 | 0.75 | 0.17 |
| long | 0.92 | 0.92 | 0.75 | 0.25 |
| sphere | 0.92 | 1.00 | 1.00 | 1.00 |
| cylinder | 0.75 | 0.58 | 0.25 | 0.25 |
| arch | 0.58 | 0.58 | 0.08 | 0.00 |
| dumbbell | 1.00 | 0.75 | 0.33 | 0.25 |
| t_shape | 1.00 | 1.00 | 0.83 | 0.08 |
| l_shape (unseen) | 1.00 | 0.92 | 0.75 | 0.42 |
| u_channel (unseen) | 1.00 | 0.83 | 0.67 | 0.25 |
| plus (unseen) | 0.58 | 0.67 | 0.67 | 0.25 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.15 | 0.19 | 0.18 | 0.17 |
| long | 0.26 | 0.32 | 0.32 | 0.34 |
| sphere | 0.05 | 0.15 | 0.24 | 0.26 |
| cylinder | 0.22 | 0.30 | 0.42 | 0.34 |
| arch | 0.00 | 0.01 | 0.01 | 0.00 |
| dumbbell | 0.10 | 0.18 | 0.19 | 0.24 |
| t_shape | 0.20 | 0.22 | 0.21 | 0.35 |
| l_shape | 0.23 | 0.29 | 0.41 | 0.49 |
| u_channel | 0.10 | 0.15 | 0.16 | 0.18 |
| plus | 0.09 | 0.24 | 0.17 | 0.24 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.90 | 0.90 | 0.83 | 0.43 |
| B_left | 0.83 | 0.77 | 0.70 | 0.40 |
| C_backright | 1.00 | 0.90 | 0.53 | 0.20 |
| D_far_turn | 0.77 | 0.73 | 0.37 | 0.13 |
