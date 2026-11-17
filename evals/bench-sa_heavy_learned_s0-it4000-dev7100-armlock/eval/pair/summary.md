# Pair evaluation: bench-sa_heavy_learned_s0-it4000-dev7100-armlock

policy: checkpoint logs/marl2/sa_heavy_learned_s0/model_4000.pt (iteration 4000, mappo, pair spot_arm)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | spotarm1 fell | spotarm2 fell | time to success (s) | robots touching | spotarm1 pushing | spotarm2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.07 | 0.07 | 0.00 | 0.02 | 33.2 | 0.14 | 0.22 | 0.16 | 0.04 | 0.15 | 0.61 |
| 40 kg | 0.01 | 0.01 | 0.01 | 0.01 | 57.4 | 0.13 | 0.21 | 0.18 | 0.02 | 0.06 | 0.58 |
| 60 kg | 0.00 | 0.00 | 0.01 | 0.01 |  | 0.14 | 0.25 | 0.22 | 0.07 | 0.19 | 0.46 |
| 80 kg | 0.00 | 0.00 | 0.01 | 0.00 |  | 0.16 | 0.28 | 0.23 | 0.11 | 0.28 | 0.51 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.00 | 0.00 | 0.00 | 0.00 |
| long | 0.75 | 0.08 | 0.00 | 0.00 |
| sphere | 0.00 | 0.00 | 0.00 | 0.00 |
| cylinder | 0.00 | 0.00 | 0.00 | 0.00 |
| arch | 0.00 | 0.00 | 0.00 | 0.00 |
| dumbbell | 0.00 | 0.00 | 0.00 | 0.00 |
| t_shape | 0.00 | 0.00 | 0.00 | 0.00 |
| l_shape (unseen) | 0.00 | 0.00 | 0.00 | 0.00 |
| u_channel (unseen) | 0.00 | 0.00 | 0.00 | 0.00 |
| plus (unseen) | 0.00 | 0.00 | 0.00 | 0.00 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.00 | 0.00 | 0.00 | 0.00 |
| long | 0.15 | 0.10 | 0.41 | 0.50 |
| sphere | 0.00 | 0.00 | 0.01 | 0.00 |
| cylinder | 0.07 | 0.02 | 0.01 | 0.01 |
| arch | 0.00 | 0.03 | 0.15 | 0.32 |
| dumbbell | 0.01 | 0.01 | 0.04 | 0.12 |
| t_shape | 0.05 | 0.00 | 0.00 | 0.00 |
| l_shape | 0.07 | 0.00 | 0.00 | 0.00 |
| u_channel | 0.06 | 0.02 | 0.01 | 0.01 |
| plus | 0.00 | 0.02 | 0.10 | 0.11 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.10 | 0.03 | 0.00 | 0.00 |
| B_left | 0.10 | 0.00 | 0.00 | 0.00 |
| C_backright | 0.03 | 0.00 | 0.00 | 0.00 |
| D_far_turn | 0.07 | 0.00 | 0.00 | 0.00 |
