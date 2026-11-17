# Pair evaluation: bench-mo_sa_mappo_s0-it4000-dev7100

policy: checkpoint logs/marl2/mo_sa_mappo_s0/model_4000.pt (iteration 4000, mappo, pair spot_arm)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | spotarm1 fell | spotarm2 fell | time to success (s) | robots touching | spotarm1 pushing | spotarm2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.14 | 0.10 | 0.21 | 0.08 | 25.6 | 0.00 | 0.41 | 0.32 | 0.12 | 0.21 | 0.83 |
| 40 kg | 0.03 | 0.03 | 0.15 | 0.12 | 27.9 | 0.00 | 0.61 | 0.44 | 0.21 | 0.27 | 0.92 |
| 60 kg | 0.00 | 0.00 | 0.14 | 0.12 |  | 0.00 | 0.69 | 0.59 | 0.40 | 0.47 | 0.98 |
| 80 kg | 0.02 | 0.02 | 0.11 | 0.13 | 29.2 | 0.00 | 0.72 | 0.70 | 0.51 | 0.56 | 0.95 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.17 | 0.00 | 0.00 | 0.00 |
| long | 0.17 | 0.00 | 0.00 | 0.00 |
| sphere | 0.25 | 0.17 | 0.00 | 0.17 |
| cylinder | 0.25 | 0.00 | 0.00 | 0.00 |
| arch | 0.17 | 0.00 | 0.00 | 0.00 |
| dumbbell | 0.00 | 0.00 | 0.00 | 0.00 |
| t_shape | 0.00 | 0.00 | 0.00 | 0.00 |
| l_shape (unseen) | 0.17 | 0.08 | 0.00 | 0.00 |
| u_channel (unseen) | 0.08 | 0.00 | 0.00 | 0.00 |
| plus (unseen) | 0.17 | 0.00 | 0.00 | 0.00 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.11 | 0.34 | 0.40 | 0.51 |
| long | 0.12 | 0.25 | 0.89 | 0.89 |
| sphere | 0.14 | 0.13 | 0.12 | 0.15 |
| cylinder | 0.19 | 0.24 | 0.37 | 0.50 |
| arch | 0.07 | 0.31 | 0.43 | 0.49 |
| dumbbell | 0.11 | 0.34 | 0.57 | 0.55 |
| t_shape | 0.04 | 0.07 | 0.40 | 0.68 |
| l_shape | 0.15 | 0.26 | 0.43 | 0.66 |
| u_channel | 0.13 | 0.10 | 0.15 | 0.18 |
| plus | 0.15 | 0.12 | 0.26 | 0.46 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.37 | 0.10 | 0.00 | 0.07 |
| B_left | 0.03 | 0.00 | 0.00 | 0.00 |
| C_backright | 0.10 | 0.00 | 0.00 | 0.00 |
| D_far_turn | 0.07 | 0.00 | 0.00 | 0.00 |
