# Pair evaluation: ippo-r5-s0-it3000

policy: checkpoint logs/marl2/ippo_r5_s0/model_3000.pt (iteration 3000, ippo)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | ANYmal fell | Spot fell | time to success (s) | robots touching |
|---|---|---|---|---|---|---|
| 20 kg | 0.43 | 0.40 | 0.01 | 0.06 | 21.3 | 0.06 |
| 40 kg | 0.28 | 0.28 | 0.07 | 0.09 | 24.8 | 0.05 |
| 60 kg | 0.14 | 0.13 | 0.11 | 0.08 | 25.0 | 0.05 |
| 80 kg | 0.08 | 0.08 | 0.15 | 0.04 | 21.6 | 0.05 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.50 | 0.50 | 0.08 | 0.00 |
| long | 0.42 | 0.17 | 0.00 | 0.00 |
| sphere | 0.75 | 0.67 | 0.75 | 0.75 |
| cylinder | 0.42 | 0.33 | 0.17 | 0.00 |
| arch | 0.17 | 0.00 | 0.00 | 0.00 |
| dumbbell | 0.33 | 0.33 | 0.08 | 0.00 |
| t_shape | 0.33 | 0.17 | 0.08 | 0.00 |
| beam (unseen) | 0.33 | 0.33 | 0.00 | 0.00 |
| l_shape (unseen) | 0.50 | 0.25 | 0.17 | 0.00 |
| asym (unseen) | 0.58 | 0.25 | 0.00 | 0.00 |
| u_channel (unseen) | 0.42 | 0.25 | 0.25 | 0.00 |
| plus (unseen) | 0.42 | 0.17 | 0.08 | 0.17 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.81 | 0.42 | 0.22 | 0.08 |
| B_left | 0.78 | 0.64 | 0.22 | 0.14 |
| C_backright | 0.00 | 0.00 | 0.00 | 0.00 |
| D_far_turn | 0.14 | 0.08 | 0.11 | 0.08 |
