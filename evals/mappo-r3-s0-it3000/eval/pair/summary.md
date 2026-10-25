# Pair evaluation: mappo-r3-s0-it3000

policy: checkpoint logs/marl2/mappo_r3_s0/model_3000.pt (iteration 3000, mappo)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | ANYmal fell | Spot fell | time to success (s) | robots touching |
|---|---|---|---|---|---|---|
| 20 kg | 0.61 | 0.64 | 0.02 | 0.09 | 30.1 | 0.06 |
| 40 kg | 0.40 | 0.34 | 0.08 | 0.12 | 32.7 | 0.05 |
| 60 kg | 0.24 | 0.19 | 0.14 | 0.06 | 35.2 | 0.03 |
| 80 kg | 0.10 | 0.09 | 0.24 | 0.05 | 29.9 | 0.03 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.75 | 0.42 | 0.58 | 0.08 |
| long | 0.67 | 0.83 | 0.17 | 0.00 |
| sphere | 0.92 | 1.00 | 0.92 | 0.83 |
| cylinder | 0.50 | 0.42 | 0.50 | 0.08 |
| arch | 0.17 | 0.17 | 0.00 | 0.00 |
| dumbbell | 0.92 | 0.42 | 0.08 | 0.00 |
| t_shape | 0.33 | 0.17 | 0.08 | 0.00 |
| beam (unseen) | 0.42 | 0.00 | 0.00 | 0.00 |
| l_shape (unseen) | 0.75 | 0.75 | 0.08 | 0.00 |
| asym (unseen) | 0.92 | 0.17 | 0.00 | 0.00 |
| u_channel (unseen) | 0.50 | 0.08 | 0.08 | 0.00 |
| plus (unseen) | 0.50 | 0.33 | 0.42 | 0.17 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.67 | 0.42 | 0.28 | 0.11 |
| B_left | 0.78 | 0.56 | 0.39 | 0.14 |
| C_backright | 0.61 | 0.36 | 0.17 | 0.06 |
| D_far_turn | 0.39 | 0.25 | 0.14 | 0.08 |
