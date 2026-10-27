# Pair evaluation: ippo-aa_r7-s0-it1000

policy: checkpoint logs/marl2/ippo_aa_r7_s0/model_1000.pt (iteration 1000, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching |
|---|---|---|---|---|---|---|
| 20 kg | 0.23 | 0.20 | 0.03 | 0.01 | 41.9 | 0.02 |
| 40 kg | 0.24 | 0.19 | 0.09 | 0.01 | 35.6 | 0.01 |
| 60 kg | 0.15 | 0.13 | 0.04 | 0.08 | 27.9 | 0.01 |
| 80 kg | 0.10 | 0.09 | 0.10 | 0.10 | 21.1 | 0.00 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.50 | 0.75 | 0.25 | 0.00 |
| long | 0.17 | 0.42 | 0.00 | 0.00 |
| sphere | 1.00 | 1.00 | 1.00 | 0.92 |
| cylinder | 0.50 | 0.17 | 0.25 | 0.25 |
| arch | 0.00 | 0.00 | 0.00 | 0.00 |
| dumbbell | 0.00 | 0.08 | 0.00 | 0.00 |
| t_shape | 0.00 | 0.08 | 0.00 | 0.00 |
| beam (unseen) | 0.17 | 0.00 | 0.00 | 0.00 |
| l_shape (unseen) | 0.17 | 0.00 | 0.00 | 0.00 |
| asym (unseen) | 0.17 | 0.17 | 0.08 | 0.00 |
| u_channel (unseen) | 0.00 | 0.08 | 0.08 | 0.08 |
| plus (unseen) | 0.08 | 0.17 | 0.08 | 0.00 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.25 | 0.31 | 0.25 | 0.17 |
| B_left | 0.22 | 0.25 | 0.11 | 0.11 |
| C_backright | 0.19 | 0.25 | 0.08 | 0.06 |
| D_far_turn | 0.25 | 0.17 | 0.14 | 0.08 |
