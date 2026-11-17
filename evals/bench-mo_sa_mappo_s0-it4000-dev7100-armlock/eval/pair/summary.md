# Pair evaluation: bench-mo_sa_mappo_s0-it4000-dev7100-armlock

policy: checkpoint logs/marl2/mo_sa_mappo_s0/model_4000.pt (iteration 4000, mappo, pair spot_arm)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | spotarm1 fell | spotarm2 fell | time to success (s) | robots touching | spotarm1 pushing | spotarm2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.09 | 0.07 | 0.02 | 0.05 | 18.6 | 0.00 | 0.42 | 0.34 | 0.13 | 0.21 | 0.84 |
| 40 kg | 0.07 | 0.07 | 0.01 | 0.07 | 35.1 | 0.00 | 0.63 | 0.45 | 0.26 | 0.33 | 0.88 |
| 60 kg | 0.03 | 0.03 | 0.00 | 0.03 | 54.6 | 0.00 | 0.75 | 0.56 | 0.46 | 0.54 | 0.99 |
| 80 kg | 0.05 | 0.05 | 0.00 | 0.02 | 58.6 | 0.00 | 0.77 | 0.67 | 0.56 | 0.65 | 1.00 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.17 | 0.00 | 0.00 | 0.00 |
| long | 0.25 | 0.17 | 0.00 | 0.00 |
| sphere | 0.25 | 0.33 | 0.25 | 0.50 |
| cylinder | 0.08 | 0.08 | 0.00 | 0.00 |
| arch | 0.00 | 0.00 | 0.00 | 0.00 |
| dumbbell | 0.08 | 0.08 | 0.00 | 0.00 |
| t_shape | 0.00 | 0.00 | 0.00 | 0.00 |
| l_shape (unseen) | 0.00 | 0.00 | 0.00 | 0.00 |
| u_channel (unseen) | 0.08 | 0.00 | 0.00 | 0.00 |
| plus (unseen) | 0.00 | 0.00 | 0.00 | 0.00 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.14 | 0.32 | 0.50 | 0.53 |
| long | 0.11 | 0.29 | 0.78 | 0.88 |
| sphere | 0.10 | 0.18 | 0.15 | 0.23 |
| cylinder | 0.24 | 0.34 | 0.52 | 0.59 |
| arch | 0.11 | 0.33 | 0.50 | 0.50 |
| dumbbell | 0.09 | 0.26 | 0.39 | 0.58 |
| t_shape | 0.10 | 0.12 | 0.18 | 0.54 |
| l_shape | 0.17 | 0.31 | 0.40 | 0.58 |
| u_channel | 0.13 | 0.23 | 0.62 | 0.45 |
| plus | 0.06 | 0.23 | 0.52 | 0.74 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.10 | 0.10 | 0.00 | 0.10 |
| B_left | 0.10 | 0.00 | 0.00 | 0.00 |
| C_backright | 0.03 | 0.10 | 0.03 | 0.00 |
| D_far_turn | 0.13 | 0.07 | 0.07 | 0.10 |
