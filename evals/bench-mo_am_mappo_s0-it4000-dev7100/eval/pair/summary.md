# Pair evaluation: bench-mo_am_mappo_s0-it4000-dev7100

policy: checkpoint logs/marl2/mo_am_mappo_s0/model_4000.pt (iteration 4000, mappo, pair anymal_arm)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal fell | spotarm fell | time to success (s) | robots touching | anymal pushing | spotarm pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.11 | 0.13 | 0.00 | 0.01 | 30.7 | 0.00 | 0.23 | 0.36 | 0.06 | 0.12 | 0.89 |
| 40 kg | 0.11 | 0.11 | 0.01 | 0.01 | 21.6 | 0.00 | 0.30 | 0.32 | 0.07 | 0.15 | 0.87 |
| 60 kg | 0.10 | 0.10 | 0.02 | 0.02 | 34.6 | 0.01 | 0.45 | 0.43 | 0.17 | 0.26 | 0.87 |
| 80 kg | 0.09 | 0.10 | 0.03 | 0.01 | 39.3 | 0.01 | 0.60 | 0.52 | 0.31 | 0.39 | 0.84 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.00 | 0.08 | 0.00 | 0.00 |
| long | 0.00 | 0.00 | 0.00 | 0.00 |
| sphere | 1.00 | 0.83 | 1.00 | 0.92 |
| cylinder | 0.08 | 0.17 | 0.00 | 0.00 |
| arch | 0.00 | 0.00 | 0.00 | 0.00 |
| dumbbell | 0.00 | 0.00 | 0.00 | 0.00 |
| t_shape | 0.00 | 0.00 | 0.00 | 0.00 |
| l_shape (unseen) | 0.00 | 0.00 | 0.00 | 0.00 |
| u_channel (unseen) | 0.00 | 0.00 | 0.00 | 0.00 |
| plus (unseen) | 0.00 | 0.00 | 0.00 | 0.00 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.16 | 0.08 | 0.30 | 0.49 |
| long | 0.06 | 0.08 | 0.29 | 0.57 |
| sphere | 0.08 | 0.09 | 0.05 | 0.03 |
| cylinder | 0.07 | 0.12 | 0.25 | 0.32 |
| arch | 0.06 | 0.09 | 0.17 | 0.32 |
| dumbbell | 0.03 | 0.06 | 0.30 | 0.45 |
| t_shape | 0.02 | 0.07 | 0.07 | 0.18 |
| l_shape | 0.02 | 0.03 | 0.06 | 0.20 |
| u_channel | 0.05 | 0.05 | 0.09 | 0.19 |
| plus | 0.02 | 0.06 | 0.15 | 0.34 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.10 | 0.13 | 0.10 | 0.10 |
| B_left | 0.10 | 0.07 | 0.10 | 0.07 |
| C_backright | 0.10 | 0.10 | 0.10 | 0.10 |
| D_far_turn | 0.13 | 0.13 | 0.10 | 0.10 |
