# Pair evaluation: ippo-r7scratch-s0-it20000

policy: checkpoint logs/marl2/ippo_r7scratch_s0/model_20000.pt (iteration 20000, ippo, pair mixed)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal fell | spot fell | time to success (s) | robots touching |
|---|---|---|---|---|---|---|
| 20 kg | 0.49 | 0.53 | 0.01 | 0.02 | 30.8 | 0.00 |
| 40 kg | 0.44 | 0.40 | 0.01 | 0.04 | 32.7 | 0.00 |
| 60 kg | 0.29 | 0.25 | 0.06 | 0.12 | 34.2 | 0.00 |
| 80 kg | 0.12 | 0.11 | 0.12 | 0.10 | 23.9 | 0.00 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 1.00 | 1.00 | 0.75 | 0.00 |
| long | 0.83 | 0.92 | 0.17 | 0.00 |
| sphere | 1.00 | 1.00 | 1.00 | 1.00 |
| cylinder | 0.58 | 0.83 | 0.50 | 0.25 |
| arch | 0.25 | 0.08 | 0.17 | 0.08 |
| dumbbell | 0.17 | 0.17 | 0.50 | 0.17 |
| t_shape | 0.00 | 0.00 | 0.08 | 0.00 |
| beam (unseen) | 0.33 | 0.25 | 0.00 | 0.00 |
| l_shape (unseen) | 0.25 | 0.42 | 0.17 | 0.00 |
| asym (unseen) | 0.92 | 0.25 | 0.00 | 0.00 |
| u_channel (unseen) | 0.17 | 0.17 | 0.00 | 0.00 |
| plus (unseen) | 0.42 | 0.25 | 0.17 | 0.00 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.56 | 0.44 | 0.36 | 0.14 |
| B_left | 0.56 | 0.50 | 0.31 | 0.14 |
| C_backright | 0.44 | 0.47 | 0.22 | 0.08 |
| D_far_turn | 0.42 | 0.36 | 0.28 | 0.14 |
