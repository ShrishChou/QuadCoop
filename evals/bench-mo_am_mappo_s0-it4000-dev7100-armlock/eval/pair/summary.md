# Pair evaluation: bench-mo_am_mappo_s0-it4000-dev7100-armlock

policy: checkpoint logs/marl2/mo_am_mappo_s0/model_4000.pt (iteration 4000, mappo, pair anymal_arm)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal fell | spotarm fell | time to success (s) | robots touching | anymal pushing | spotarm pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.14 | 0.16 | 0.00 | 0.00 | 30.8 | 0.00 | 0.22 | 0.27 | 0.05 | 0.14 | 0.90 |
| 40 kg | 0.12 | 0.12 | 0.01 | 0.02 | 26.1 | 0.00 | 0.30 | 0.31 | 0.07 | 0.15 | 0.94 |
| 60 kg | 0.07 | 0.07 | 0.03 | 0.03 | 20.1 | 0.00 | 0.40 | 0.40 | 0.15 | 0.24 | 0.88 |
| 80 kg | 0.07 | 0.07 | 0.04 | 0.01 | 25.9 | 0.01 | 0.57 | 0.50 | 0.28 | 0.37 | 0.86 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.25 | 0.08 | 0.00 | 0.00 |
| long | 0.00 | 0.00 | 0.00 | 0.00 |
| sphere | 1.00 | 0.92 | 0.67 | 0.75 |
| cylinder | 0.17 | 0.17 | 0.08 | 0.00 |
| arch | 0.00 | 0.08 | 0.00 | 0.00 |
| dumbbell | 0.00 | 0.00 | 0.00 | 0.00 |
| t_shape | 0.00 | 0.00 | 0.00 | 0.00 |
| l_shape (unseen) | 0.00 | 0.00 | 0.00 | 0.00 |
| u_channel (unseen) | 0.00 | 0.00 | 0.00 | 0.00 |
| plus (unseen) | 0.00 | 0.00 | 0.00 | 0.00 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.03 | 0.05 | 0.27 | 0.46 |
| long | 0.04 | 0.09 | 0.29 | 0.57 |
| sphere | 0.13 | 0.14 | 0.05 | 0.04 |
| cylinder | 0.13 | 0.10 | 0.13 | 0.13 |
| arch | 0.07 | 0.10 | 0.15 | 0.26 |
| dumbbell | 0.03 | 0.07 | 0.23 | 0.43 |
| t_shape | 0.03 | 0.03 | 0.13 | 0.18 |
| l_shape | 0.02 | 0.03 | 0.06 | 0.19 |
| u_channel | 0.03 | 0.08 | 0.06 | 0.23 |
| plus | 0.02 | 0.04 | 0.10 | 0.34 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.27 | 0.20 | 0.13 | 0.10 |
| B_left | 0.10 | 0.10 | 0.07 | 0.10 |
| C_backright | 0.10 | 0.10 | 0.07 | 0.07 |
| D_far_turn | 0.10 | 0.10 | 0.03 | 0.03 |
