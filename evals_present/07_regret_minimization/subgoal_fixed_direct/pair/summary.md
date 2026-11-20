# Pair evaluation: sg-fixed-direct-dev7100

policy: checkpoint logs/marl2/nwB_mappo_uniform_s0/model_5000.pt (iteration 5000, mappo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.93 | 0.88 | 0.01 | 0.02 | 20.8 | 0.08 | 0.50 | 0.31 | 0.16 | 0.28 | 0.67 |
| 40 kg | 0.78 | 0.75 | 0.05 | 0.03 | 24.3 | 0.09 | 0.57 | 0.39 | 0.21 | 0.31 | 0.64 |
| 60 kg | 0.60 | 0.55 | 0.07 | 0.07 | 31.7 | 0.09 | 0.59 | 0.48 | 0.27 | 0.37 | 0.65 |
| 80 kg | 0.26 | 0.20 | 0.14 | 0.11 | 37.9 | 0.10 | 0.59 | 0.51 | 0.30 | 0.40 | 0.65 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 1.00 | 1.00 | 0.75 | 0.17 |
| long | 1.00 | 0.83 | 0.83 | 0.25 |
| sphere | 1.00 | 1.00 | 1.00 | 0.83 |
| cylinder | 0.75 | 0.50 | 0.33 | 0.17 |
| arch | 0.83 | 0.42 | 0.17 | 0.00 |
| dumbbell | 1.00 | 0.75 | 0.42 | 0.08 |
| t_shape | 1.00 | 1.00 | 0.67 | 0.17 |
| l_shape (unseen) | 1.00 | 0.83 | 0.75 | 0.17 |
| u_channel (unseen) | 1.00 | 1.00 | 0.75 | 0.42 |
| plus (unseen) | 0.75 | 0.50 | 0.33 | 0.33 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.13 | 0.17 | 0.18 | 0.07 |
| long | 0.37 | 0.32 | 0.34 | 0.35 |
| sphere | 0.05 | 0.10 | 0.27 | 0.28 |
| cylinder | 0.28 | 0.30 | 0.47 | 0.51 |
| arch | 0.00 | 0.02 | 0.01 | 0.00 |
| dumbbell | 0.04 | 0.15 | 0.21 | 0.23 |
| t_shape | 0.24 | 0.31 | 0.23 | 0.35 |
| l_shape | 0.19 | 0.29 | 0.44 | 0.44 |
| u_channel | 0.16 | 0.26 | 0.27 | 0.42 |
| plus | 0.10 | 0.19 | 0.24 | 0.29 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.97 | 0.80 | 0.83 | 0.37 |
| B_left | 0.90 | 0.83 | 0.57 | 0.37 |
| C_backright | 0.97 | 0.80 | 0.53 | 0.23 |
| D_far_turn | 0.90 | 0.70 | 0.47 | 0.07 |
