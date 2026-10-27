# Pair evaluation: ippo-aa_r7-s0-it500

policy: checkpoint logs/marl2/ippo_aa_r7_s0/model_500.pt (iteration 500, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching |
|---|---|---|---|---|---|---|
| 20 kg | 0.10 | 0.09 | 0.02 | 0.02 | 39.7 | 0.01 |
| 40 kg | 0.09 | 0.10 | 0.02 | 0.01 | 38.9 | 0.01 |
| 60 kg | 0.08 | 0.06 | 0.03 | 0.03 | 46.8 | 0.02 |
| 80 kg | 0.02 | 0.01 | 0.07 | 0.03 | 13.3 | 0.01 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.50 | 0.50 | 0.42 | 0.00 |
| long | 0.00 | 0.00 | 0.00 | 0.08 |
| sphere | 0.00 | 0.08 | 0.00 | 0.00 |
| cylinder | 0.25 | 0.08 | 0.08 | 0.17 |
| arch | 0.08 | 0.00 | 0.00 | 0.00 |
| dumbbell | 0.17 | 0.17 | 0.08 | 0.00 |
| t_shape | 0.00 | 0.00 | 0.00 | 0.00 |
| beam (unseen) | 0.00 | 0.00 | 0.00 | 0.00 |
| l_shape (unseen) | 0.00 | 0.00 | 0.00 | 0.00 |
| asym (unseen) | 0.00 | 0.25 | 0.25 | 0.00 |
| u_channel (unseen) | 0.00 | 0.00 | 0.00 | 0.00 |
| plus (unseen) | 0.17 | 0.00 | 0.08 | 0.00 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.19 | 0.06 | 0.14 | 0.08 |
| B_left | 0.06 | 0.17 | 0.06 | 0.00 |
| C_backright | 0.08 | 0.08 | 0.08 | 0.00 |
| D_far_turn | 0.06 | 0.06 | 0.03 | 0.00 |
