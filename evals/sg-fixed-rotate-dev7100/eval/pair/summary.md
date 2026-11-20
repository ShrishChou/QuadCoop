# Pair evaluation: sg-fixed-rotate-dev7100

policy: checkpoint logs/marl2/nwB_mappo_uniform_s0/model_5000.pt (iteration 5000, mappo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.03 | 0.92 | 0.00 | 0.01 | 44.8 | 0.08 | 0.46 | 0.25 | 0.14 | 0.26 | 0.67 |
| 40 kg | 0.00 | 0.88 | 0.01 | 0.03 |  | 0.06 | 0.54 | 0.24 | 0.12 | 0.19 | 0.69 |
| 60 kg | 0.00 | 0.83 | 0.07 | 0.01 |  | 0.05 | 0.60 | 0.25 | 0.14 | 0.20 | 0.70 |
| 80 kg | 0.00 | 0.71 | 0.04 | 0.04 |  | 0.05 | 0.56 | 0.27 | 0.13 | 0.19 | 0.76 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.00 | 0.00 | 0.00 | 0.00 |
| long | 0.08 | 0.00 | 0.00 | 0.00 |
| sphere | 0.00 | 0.00 | 0.00 | 0.00 |
| cylinder | 0.00 | 0.00 | 0.00 | 0.00 |
| arch | 0.00 | 0.00 | 0.00 | 0.00 |
| dumbbell | 0.00 | 0.00 | 0.00 | 0.00 |
| t_shape | 0.08 | 0.00 | 0.00 | 0.00 |
| l_shape (unseen) | 0.08 | 0.00 | 0.00 | 0.00 |
| u_channel (unseen) | 0.00 | 0.00 | 0.00 | 0.00 |
| plus (unseen) | 0.00 | 0.00 | 0.00 | 0.00 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.56 | 0.50 | 0.51 | 0.42 |
| long | 0.12 | 0.10 | 0.08 | 0.03 |
| sphere | 0.32 | 0.30 | 0.28 | 0.26 |
| cylinder | 0.03 | 0.03 | 0.05 | 0.06 |
| arch | 0.00 | 0.00 | 0.00 | 0.00 |
| dumbbell | 0.14 | 0.05 | 0.11 | 0.06 |
| t_shape | 0.03 | 0.03 | 0.02 | 0.02 |
| l_shape | 0.11 | 0.08 | 0.14 | 0.04 |
| u_channel | 0.05 | 0.10 | 0.14 | 0.29 |
| plus | 0.02 | 0.01 | 0.05 | 0.07 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.07 | 0.00 | 0.00 | 0.00 |
| B_left | 0.03 | 0.00 | 0.00 | 0.00 |
| C_backright | 0.00 | 0.00 | 0.00 | 0.00 |
| D_far_turn | 0.00 | 0.00 | 0.00 | 0.00 |
