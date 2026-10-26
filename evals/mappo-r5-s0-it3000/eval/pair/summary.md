# Pair evaluation: mappo-r5-s0-it3000

policy: checkpoint logs/marl2/mappo_r5_s0/model_3000.pt (iteration 3000, mappo)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | ANYmal fell | Spot fell | time to success (s) | robots touching |
|---|---|---|---|---|---|---|
| 20 kg | 0.31 | 0.31 | 0.00 | 0.07 | 24.1 | 0.05 |
| 40 kg | 0.21 | 0.19 | 0.04 | 0.12 | 22.9 | 0.04 |
| 60 kg | 0.08 | 0.08 | 0.12 | 0.06 | 20.9 | 0.04 |
| 80 kg | 0.03 | 0.04 | 0.17 | 0.10 | 11.5 | 0.04 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.83 | 0.75 | 0.08 | 0.00 |
| long | 0.33 | 0.25 | 0.00 | 0.00 |
| sphere | 1.00 | 0.67 | 0.67 | 0.33 |
| cylinder | 0.25 | 0.25 | 0.25 | 0.08 |
| arch | 0.00 | 0.00 | 0.00 | 0.00 |
| dumbbell | 0.33 | 0.08 | 0.00 | 0.00 |
| t_shape | 0.08 | 0.17 | 0.00 | 0.00 |
| beam (unseen) | 0.00 | 0.00 | 0.00 | 0.00 |
| l_shape (unseen) | 0.17 | 0.00 | 0.00 | 0.00 |
| asym (unseen) | 0.33 | 0.00 | 0.00 | 0.00 |
| u_channel (unseen) | 0.17 | 0.17 | 0.00 | 0.00 |
| plus (unseen) | 0.25 | 0.17 | 0.00 | 0.00 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.39 | 0.19 | 0.11 | 0.03 |
| B_left | 0.50 | 0.44 | 0.08 | 0.03 |
| C_backright | 0.22 | 0.11 | 0.08 | 0.08 |
| D_far_turn | 0.14 | 0.08 | 0.06 | 0.00 |
