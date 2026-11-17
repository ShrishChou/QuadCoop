# Pair evaluation: bench-mo_am_ippo_s0-it4000-dev7100

policy: checkpoint logs/marl2/mo_am_ippo_s0/model_4000.pt (iteration 4000, ippo, pair anymal_arm)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal fell | spotarm fell | time to success (s) | robots touching | anymal pushing | spotarm pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.05 | 0.05 | 0.05 | 0.00 | 31.3 | 0.01 | 0.20 | 0.19 | 0.04 | 0.11 | 1.10 |
| 40 kg | 0.07 | 0.08 | 0.07 | 0.02 | 20.0 | 0.01 | 0.22 | 0.40 | 0.07 | 0.13 | 1.05 |
| 60 kg | 0.07 | 0.07 | 0.12 | 0.06 | 24.8 | 0.01 | 0.33 | 0.43 | 0.18 | 0.32 | 1.07 |
| 80 kg | 0.07 | 0.07 | 0.20 | 0.08 | 34.1 | 0.00 | 0.41 | 0.50 | 0.27 | 0.45 | 1.04 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.00 | 0.17 | 0.00 | 0.00 |
| long | 0.00 | 0.00 | 0.00 | 0.00 |
| sphere | 0.42 | 0.50 | 0.75 | 0.75 |
| cylinder | 0.00 | 0.00 | 0.00 | 0.00 |
| arch | 0.00 | 0.00 | 0.00 | 0.00 |
| dumbbell | 0.00 | 0.00 | 0.00 | 0.00 |
| t_shape | 0.00 | 0.00 | 0.00 | 0.00 |
| l_shape (unseen) | 0.08 | 0.00 | 0.00 | 0.00 |
| u_channel (unseen) | 0.00 | 0.00 | 0.00 | 0.00 |
| plus (unseen) | 0.00 | 0.00 | 0.00 | 0.00 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.02 | 0.03 | 0.05 | 0.06 |
| long | 0.04 | 0.13 | 0.54 | 0.59 |
| sphere | 0.08 | 0.13 | 0.07 | 0.05 |
| cylinder | 0.04 | 0.06 | 0.07 | 0.10 |
| arch | 0.02 | 0.04 | 0.10 | 0.27 |
| dumbbell | 0.04 | 0.05 | 0.20 | 0.42 |
| t_shape | 0.03 | 0.04 | 0.14 | 0.31 |
| l_shape | 0.03 | 0.05 | 0.11 | 0.17 |
| u_channel | 0.06 | 0.11 | 0.23 | 0.37 |
| plus | 0.03 | 0.07 | 0.25 | 0.39 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.07 | 0.13 | 0.10 | 0.10 |
| B_left | 0.00 | 0.00 | 0.00 | 0.00 |
| C_backright | 0.03 | 0.03 | 0.10 | 0.10 |
| D_far_turn | 0.10 | 0.10 | 0.10 | 0.10 |
