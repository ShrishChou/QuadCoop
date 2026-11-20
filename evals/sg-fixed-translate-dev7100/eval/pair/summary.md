# Pair evaluation: sg-fixed-translate-dev7100

policy: checkpoint logs/marl2/nwB_mappo_uniform_s0/model_5000.pt (iteration 5000, mappo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.93 | 0.88 | 0.02 | 0.03 | 20.4 | 0.09 | 0.45 | 0.32 | 0.15 | 0.28 | 0.74 |
| 40 kg | 0.80 | 0.68 | 0.06 | 0.04 | 23.4 | 0.10 | 0.49 | 0.38 | 0.17 | 0.29 | 0.68 |
| 60 kg | 0.53 | 0.47 | 0.08 | 0.04 | 31.6 | 0.11 | 0.50 | 0.45 | 0.21 | 0.32 | 0.66 |
| 80 kg | 0.26 | 0.22 | 0.10 | 0.06 | 30.6 | 0.10 | 0.51 | 0.47 | 0.22 | 0.32 | 0.66 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 1.00 | 0.92 | 0.58 | 0.17 |
| long | 1.00 | 0.75 | 0.67 | 0.25 |
| sphere | 0.92 | 1.00 | 1.00 | 1.00 |
| cylinder | 0.75 | 0.58 | 0.25 | 0.33 |
| arch | 0.83 | 0.33 | 0.08 | 0.00 |
| dumbbell | 0.83 | 0.75 | 0.25 | 0.00 |
| t_shape | 1.00 | 0.92 | 0.58 | 0.08 |
| l_shape (unseen) | 1.00 | 1.00 | 0.58 | 0.25 |
| u_channel (unseen) | 1.00 | 0.92 | 0.58 | 0.25 |
| plus (unseen) | 0.92 | 0.83 | 0.67 | 0.25 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.17 | 0.22 | 0.07 | 0.04 |
| long | 0.22 | 0.25 | 0.33 | 0.32 |
| sphere | 0.10 | 0.12 | 0.27 | 0.27 |
| cylinder | 0.26 | 0.27 | 0.35 | 0.29 |
| arch | 0.01 | 0.01 | 0.00 | 0.00 |
| dumbbell | 0.08 | 0.10 | 0.17 | 0.18 |
| t_shape | 0.20 | 0.24 | 0.28 | 0.28 |
| l_shape | 0.22 | 0.34 | 0.33 | 0.44 |
| u_channel | 0.12 | 0.07 | 0.19 | 0.30 |
| plus | 0.12 | 0.13 | 0.14 | 0.12 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 1.00 | 0.77 | 0.70 | 0.50 |
| B_left | 0.97 | 0.80 | 0.63 | 0.33 |
| C_backright | 0.90 | 0.90 | 0.50 | 0.10 |
| D_far_turn | 0.83 | 0.73 | 0.27 | 0.10 |
