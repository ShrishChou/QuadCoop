# Pair evaluation: bench-sa_heavy_learned_s0-it4000-dev7100

policy: checkpoint logs/marl2/sa_heavy_learned_s0/model_4000.pt (iteration 4000, mappo, pair spot_arm)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | spotarm1 fell | spotarm2 fell | time to success (s) | robots touching | spotarm1 pushing | spotarm2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.08 | 0.08 | 0.01 | 0.02 | 29.1 | 0.08 | 0.19 | 0.17 | 0.04 | 0.14 | 0.79 |
| 40 kg | 0.03 | 0.03 | 0.01 | 0.00 | 40.5 | 0.07 | 0.19 | 0.23 | 0.03 | 0.08 | 0.71 |
| 60 kg | 0.00 | 0.00 | 0.01 | 0.00 |  | 0.07 | 0.21 | 0.24 | 0.05 | 0.13 | 0.77 |
| 80 kg | 0.00 | 0.00 | 0.02 | 0.00 |  | 0.06 | 0.25 | 0.24 | 0.06 | 0.16 | 0.68 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.00 | 0.00 | 0.00 | 0.00 |
| long | 0.75 | 0.25 | 0.00 | 0.00 |
| sphere | 0.00 | 0.00 | 0.00 | 0.00 |
| cylinder | 0.00 | 0.00 | 0.00 | 0.00 |
| arch | 0.08 | 0.00 | 0.00 | 0.00 |
| dumbbell | 0.00 | 0.00 | 0.00 | 0.00 |
| t_shape | 0.00 | 0.00 | 0.00 | 0.00 |
| l_shape (unseen) | 0.00 | 0.00 | 0.00 | 0.00 |
| u_channel (unseen) | 0.00 | 0.00 | 0.00 | 0.00 |
| plus (unseen) | 0.00 | 0.00 | 0.00 | 0.00 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.00 | 0.00 | 0.00 | 0.00 |
| long | 0.26 | 0.16 | 0.31 | 0.55 |
| sphere | 0.00 | 0.00 | 0.00 | 0.00 |
| cylinder | 0.00 | 0.00 | 0.01 | 0.01 |
| arch | 0.01 | 0.01 | 0.01 | 0.01 |
| dumbbell | 0.07 | 0.09 | 0.08 | 0.00 |
| t_shape | 0.01 | 0.00 | 0.00 | 0.00 |
| l_shape | 0.03 | 0.00 | 0.00 | 0.00 |
| u_channel | 0.01 | 0.01 | 0.00 | 0.01 |
| plus | 0.01 | 0.02 | 0.08 | 0.07 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.10 | 0.07 | 0.00 | 0.00 |
| B_left | 0.10 | 0.03 | 0.00 | 0.00 |
| C_backright | 0.07 | 0.00 | 0.00 | 0.00 |
| D_far_turn | 0.07 | 0.00 | 0.00 | 0.00 |
