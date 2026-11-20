# Pair evaluation: pairvid-mappo

policy: checkpoint logs/marl2/nwB_mappo_uniform_s0/model_5000.pt (iteration 5000, mappo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 1 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 40 kg | 0.83 | 0.79 | 0.02 | 0.02 | 23.2 | 0.10 | 0.54 | 0.39 | 0.20 | 0.32 | 0.66 |
| 80 kg | 0.25 | 0.23 | 0.19 | 0.06 | 37.7 | 0.09 | 0.63 | 0.55 | 0.35 | 0.45 | 0.65 |

## success by object and mass

| object | 40 kg | 80 kg |
|---|---|---|
| cube | 1.00 | 0.00 |
| long | 0.75 | 0.50 |
| sphere | 1.00 | 1.00 |
| cylinder | 0.50 | 0.25 |
| arch | 0.50 | 0.00 |
| dumbbell | 0.50 | 0.25 |
| t_shape | 1.00 | 0.00 |
| beam (unseen) | 1.00 | 0.00 |
| l_shape (unseen) | 1.00 | 0.50 |
| asym (unseen) | 1.00 | 0.25 |
| u_channel (unseen) | 1.00 | 0.00 |
| plus (unseen) | 0.75 | 0.25 |

## both robots pushing (share of time) by object and mass

| object | 40 kg | 80 kg |
|---|---|---|
| cube | 0.18 | 0.11 |
| long | 0.26 | 0.54 |
| sphere | 0.18 | 0.32 |
| cylinder | 0.29 | 0.58 |
| arch | 0.01 | 0.00 |
| dumbbell | 0.12 | 0.18 |
| t_shape | 0.24 | 0.22 |
| beam | 0.29 | 0.57 |
| l_shape | 0.21 | 0.63 |
| asym | 0.32 | 0.34 |
| u_channel | 0.19 | 0.35 |
| plus | 0.15 | 0.34 |

## success by scenario and mass

| scenario | 40 kg | 80 kg |
|---|---|---|
| A_straight | 0.83 | 0.42 |
| B_left | 0.83 | 0.33 |
| C_backright | 0.83 | 0.17 |
| D_far_turn | 0.83 | 0.08 |
