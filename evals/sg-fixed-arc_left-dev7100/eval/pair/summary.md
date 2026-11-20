# Pair evaluation: sg-fixed-arc_left-dev7100

policy: checkpoint logs/marl2/nwB_mappo_uniform_s0/model_5000.pt (iteration 5000, mappo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.88 | 0.79 | 0.03 | 0.02 | 25.6 | 0.09 | 0.44 | 0.26 | 0.09 | 0.18 | 0.73 |
| 40 kg | 0.75 | 0.72 | 0.05 | 0.03 | 29.7 | 0.10 | 0.47 | 0.34 | 0.13 | 0.23 | 0.70 |
| 60 kg | 0.40 | 0.34 | 0.12 | 0.08 | 38.9 | 0.11 | 0.52 | 0.36 | 0.16 | 0.25 | 0.70 |
| 80 kg | 0.23 | 0.21 | 0.12 | 0.03 | 33.6 | 0.09 | 0.56 | 0.35 | 0.18 | 0.27 | 0.69 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 1.00 | 0.92 | 0.33 | 0.08 |
| long | 1.00 | 1.00 | 0.67 | 0.00 |
| sphere | 0.92 | 1.00 | 0.92 | 1.00 |
| cylinder | 0.75 | 0.50 | 0.33 | 0.25 |
| arch | 0.58 | 0.25 | 0.00 | 0.00 |
| dumbbell | 0.92 | 0.83 | 0.08 | 0.00 |
| t_shape | 1.00 | 0.75 | 0.83 | 0.33 |
| l_shape (unseen) | 0.92 | 0.92 | 0.25 | 0.17 |
| u_channel (unseen) | 1.00 | 0.75 | 0.33 | 0.33 |
| plus (unseen) | 0.67 | 0.58 | 0.25 | 0.17 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.10 | 0.09 | 0.09 | 0.06 |
| long | 0.16 | 0.29 | 0.28 | 0.25 |
| sphere | 0.04 | 0.08 | 0.08 | 0.11 |
| cylinder | 0.30 | 0.25 | 0.24 | 0.17 |
| arch | 0.00 | 0.00 | 0.00 | 0.00 |
| dumbbell | 0.03 | 0.08 | 0.11 | 0.17 |
| t_shape | 0.06 | 0.16 | 0.21 | 0.33 |
| l_shape | 0.08 | 0.18 | 0.20 | 0.26 |
| u_channel | 0.06 | 0.10 | 0.19 | 0.23 |
| plus | 0.05 | 0.09 | 0.15 | 0.20 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.93 | 0.93 | 0.60 | 0.40 |
| B_left | 0.93 | 0.80 | 0.43 | 0.30 |
| C_backright | 0.93 | 0.73 | 0.30 | 0.13 |
| D_far_turn | 0.70 | 0.53 | 0.27 | 0.10 |
