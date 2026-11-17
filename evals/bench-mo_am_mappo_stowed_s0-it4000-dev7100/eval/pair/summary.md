# Pair evaluation: bench-mo_am_mappo_stowed_s0-it4000-dev7100

policy: checkpoint logs/marl2/mo_am_mappo_stowed_s0/model_4000.pt (iteration 4000, mappo, pair anymal_arm)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal fell | spotarm fell | time to success (s) | robots touching | anymal pushing | spotarm pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.15 | 0.23 | 0.00 | 0.00 | 23.5 | 0.00 | 0.25 | 0.43 | 0.05 | 0.09 | 1.03 |
| 40 kg | 0.15 | 0.11 | 0.01 | 0.01 | 24.5 | 0.00 | 0.28 | 0.46 | 0.08 | 0.14 | 1.08 |
| 60 kg | 0.11 | 0.11 | 0.06 | 0.03 | 24.8 | 0.00 | 0.41 | 0.40 | 0.12 | 0.19 | 1.08 |
| 80 kg | 0.10 | 0.10 | 0.07 | 0.03 | 26.3 | 0.01 | 0.52 | 0.44 | 0.18 | 0.24 | 1.05 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.25 | 0.00 | 0.00 | 0.00 |
| long | 0.00 | 0.08 | 0.00 | 0.00 |
| sphere | 0.92 | 1.00 | 1.00 | 1.00 |
| cylinder | 0.17 | 0.25 | 0.08 | 0.00 |
| arch | 0.08 | 0.08 | 0.00 | 0.00 |
| dumbbell | 0.00 | 0.00 | 0.00 | 0.00 |
| t_shape | 0.08 | 0.00 | 0.00 | 0.00 |
| l_shape (unseen) | 0.00 | 0.00 | 0.00 | 0.00 |
| u_channel (unseen) | 0.00 | 0.00 | 0.00 | 0.00 |
| plus (unseen) | 0.00 | 0.08 | 0.00 | 0.00 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.07 | 0.04 | 0.05 | 0.14 |
| long | 0.04 | 0.10 | 0.14 | 0.25 |
| sphere | 0.03 | 0.09 | 0.13 | 0.08 |
| cylinder | 0.09 | 0.19 | 0.13 | 0.12 |
| arch | 0.08 | 0.13 | 0.13 | 0.26 |
| dumbbell | 0.05 | 0.06 | 0.22 | 0.38 |
| t_shape | 0.07 | 0.04 | 0.05 | 0.12 |
| l_shape | 0.02 | 0.03 | 0.04 | 0.05 |
| u_channel | 0.01 | 0.03 | 0.06 | 0.15 |
| plus | 0.02 | 0.12 | 0.28 | 0.28 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.23 | 0.27 | 0.13 | 0.10 |
| B_left | 0.17 | 0.10 | 0.10 | 0.10 |
| C_backright | 0.07 | 0.13 | 0.10 | 0.10 |
| D_far_turn | 0.13 | 0.10 | 0.10 | 0.10 |
