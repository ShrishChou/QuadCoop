# Pair evaluation: ippo-r4-s0-it3000

policy: checkpoint logs/marl2/ippo_r4_s0/model_3000.pt (iteration 3000, ippo)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | ANYmal fell | Spot fell | time to success (s) | robots touching |
|---|---|---|---|---|---|---|
| 20 kg | 0.52 | 0.49 | 0.02 | 0.06 | 25.6 | 0.05 |
| 40 kg | 0.38 | 0.35 | 0.06 | 0.09 | 27.1 | 0.06 |
| 60 kg | 0.15 | 0.15 | 0.09 | 0.08 | 30.0 | 0.04 |
| 80 kg | 0.08 | 0.08 | 0.12 | 0.08 | 25.9 | 0.03 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.58 | 0.67 | 0.25 | 0.00 |
| long | 0.42 | 0.50 | 0.17 | 0.00 |
| sphere | 0.92 | 0.75 | 0.75 | 0.75 |
| cylinder | 0.50 | 0.50 | 0.25 | 0.17 |
| arch | 0.17 | 0.00 | 0.00 | 0.00 |
| dumbbell | 0.58 | 0.33 | 0.17 | 0.08 |
| t_shape | 0.42 | 0.33 | 0.00 | 0.00 |
| beam (unseen) | 0.50 | 0.17 | 0.00 | 0.00 |
| l_shape (unseen) | 0.50 | 0.33 | 0.00 | 0.00 |
| asym (unseen) | 0.67 | 0.17 | 0.00 | 0.00 |
| u_channel (unseen) | 0.50 | 0.33 | 0.25 | 0.00 |
| plus (unseen) | 0.50 | 0.42 | 0.00 | 0.00 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.86 | 0.69 | 0.19 | 0.17 |
| B_left | 0.89 | 0.56 | 0.31 | 0.06 |
| C_backright | 0.08 | 0.03 | 0.03 | 0.06 |
| D_far_turn | 0.25 | 0.22 | 0.08 | 0.06 |
