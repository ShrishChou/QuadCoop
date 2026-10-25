# Pair evaluation: mappo-r4-s0-it3000

policy: checkpoint logs/marl2/mappo_r4_s0/model_3000.pt (iteration 3000, mappo)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | ANYmal fell | Spot fell | time to success (s) | robots touching |
|---|---|---|---|---|---|---|
| 20 kg | 0.65 | 0.68 | 0.05 | 0.08 | 35.4 | 0.04 |
| 40 kg | 0.53 | 0.49 | 0.04 | 0.13 | 41.0 | 0.03 |
| 60 kg | 0.22 | 0.19 | 0.15 | 0.12 | 35.6 | 0.03 |
| 80 kg | 0.12 | 0.10 | 0.18 | 0.10 | 37.2 | 0.02 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.92 | 0.75 | 0.42 | 0.08 |
| long | 0.92 | 0.58 | 0.17 | 0.00 |
| sphere | 1.00 | 0.92 | 1.00 | 1.00 |
| cylinder | 0.67 | 0.67 | 0.42 | 0.17 |
| arch | 0.25 | 0.17 | 0.00 | 0.00 |
| dumbbell | 0.33 | 0.42 | 0.00 | 0.08 |
| t_shape | 0.42 | 0.42 | 0.08 | 0.17 |
| beam (unseen) | 0.17 | 0.33 | 0.00 | 0.00 |
| l_shape (unseen) | 0.83 | 0.75 | 0.17 | 0.00 |
| asym (unseen) | 0.92 | 0.25 | 0.08 | 0.00 |
| u_channel (unseen) | 0.67 | 0.58 | 0.17 | 0.00 |
| plus (unseen) | 0.67 | 0.50 | 0.17 | 0.00 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.67 | 0.56 | 0.25 | 0.14 |
| B_left | 0.69 | 0.64 | 0.39 | 0.19 |
| C_backright | 0.72 | 0.61 | 0.17 | 0.08 |
| D_far_turn | 0.50 | 0.31 | 0.08 | 0.08 |
