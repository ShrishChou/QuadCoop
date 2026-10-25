# Pair evaluation: ippo-r3-s0-it3000

policy: checkpoint logs/marl2/ippo_r3_s0/model_3000.pt (iteration 3000, ippo)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | ANYmal fell | Spot fell | time to success (s) | robots touching |
|---|---|---|---|---|---|---|
| 20 kg | 0.62 | 0.56 | 0.01 | 0.06 | 26.6 | 0.12 |
| 40 kg | 0.46 | 0.41 | 0.03 | 0.08 | 30.6 | 0.08 |
| 60 kg | 0.20 | 0.17 | 0.05 | 0.12 | 34.4 | 0.06 |
| 80 kg | 0.10 | 0.10 | 0.10 | 0.10 | 18.7 | 0.05 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.92 | 0.67 | 0.42 | 0.08 |
| long | 0.75 | 0.67 | 0.25 | 0.00 |
| sphere | 0.83 | 1.00 | 0.75 | 0.83 |
| cylinder | 0.58 | 0.42 | 0.33 | 0.25 |
| arch | 0.25 | 0.08 | 0.00 | 0.00 |
| dumbbell | 0.92 | 0.50 | 0.08 | 0.00 |
| t_shape | 0.25 | 0.50 | 0.25 | 0.00 |
| beam (unseen) | 0.75 | 0.33 | 0.08 | 0.00 |
| l_shape (unseen) | 0.58 | 0.50 | 0.00 | 0.00 |
| asym (unseen) | 0.83 | 0.33 | 0.00 | 0.00 |
| u_channel (unseen) | 0.42 | 0.17 | 0.25 | 0.08 |
| plus (unseen) | 0.42 | 0.33 | 0.00 | 0.00 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.78 | 0.75 | 0.39 | 0.22 |
| B_left | 0.75 | 0.50 | 0.25 | 0.08 |
| C_backright | 0.42 | 0.31 | 0.08 | 0.06 |
| D_far_turn | 0.56 | 0.28 | 0.08 | 0.06 |
