# Pair evaluation: mappo-r7scratch-s0-it20000

policy: checkpoint logs/marl2/mappo_r7scratch_s0/model_20000.pt (iteration 20000, mappo, pair mixed)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal fell | spot fell | time to success (s) | robots touching |
|---|---|---|---|---|---|---|
| 20 kg | 0.37 | 0.49 | 0.01 | 0.06 | 39.4 | 0.00 |
| 40 kg | 0.39 | 0.39 | 0.03 | 0.08 | 34.0 | 0.00 |
| 60 kg | 0.24 | 0.20 | 0.08 | 0.10 | 34.5 | 0.01 |
| 80 kg | 0.10 | 0.08 | 0.15 | 0.16 | 21.4 | 0.01 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.83 | 0.92 | 0.67 | 0.17 |
| long | 0.58 | 0.83 | 0.50 | 0.00 |
| sphere | 0.83 | 1.00 | 0.92 | 0.83 |
| cylinder | 0.83 | 0.83 | 0.75 | 0.25 |
| arch | 0.17 | 0.08 | 0.00 | 0.00 |
| dumbbell | 0.00 | 0.08 | 0.00 | 0.00 |
| t_shape | 0.00 | 0.00 | 0.00 | 0.00 |
| beam (unseen) | 0.17 | 0.42 | 0.00 | 0.00 |
| l_shape (unseen) | 0.42 | 0.25 | 0.00 | 0.00 |
| asym (unseen) | 0.58 | 0.25 | 0.00 | 0.00 |
| u_channel (unseen) | 0.00 | 0.00 | 0.00 | 0.00 |
| plus (unseen) | 0.00 | 0.00 | 0.00 | 0.00 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.33 | 0.36 | 0.31 | 0.19 |
| B_left | 0.36 | 0.53 | 0.22 | 0.08 |
| C_backright | 0.39 | 0.33 | 0.17 | 0.06 |
| D_far_turn | 0.39 | 0.33 | 0.25 | 0.08 |
