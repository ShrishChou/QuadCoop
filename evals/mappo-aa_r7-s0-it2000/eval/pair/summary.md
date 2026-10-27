# Pair evaluation: mappo-aa_r7-s0-it2000

policy: checkpoint logs/marl2/mappo_aa_r7_s0/model_2000.pt (iteration 2000, mappo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching |
|---|---|---|---|---|---|---|
| 20 kg | 0.00 | 0.00 | 0.00 | 0.01 |  | 0.01 |
| 40 kg | 0.03 | 0.01 | 0.01 | 0.01 | 34.4 | 0.01 |
| 60 kg | 0.03 | 0.03 | 0.04 | 0.08 | 33.1 | 0.01 |
| 80 kg | 0.00 | 0.00 | 0.12 | 0.06 |  | 0.01 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.00 | 0.00 | 0.08 | 0.00 |
| long | 0.00 | 0.08 | 0.08 | 0.00 |
| sphere | 0.00 | 0.00 | 0.17 | 0.00 |
| cylinder | 0.00 | 0.00 | 0.00 | 0.00 |
| arch | 0.00 | 0.00 | 0.00 | 0.00 |
| dumbbell | 0.00 | 0.00 | 0.00 | 0.00 |
| t_shape | 0.00 | 0.00 | 0.00 | 0.00 |
| beam (unseen) | 0.00 | 0.00 | 0.00 | 0.00 |
| l_shape (unseen) | 0.00 | 0.00 | 0.00 | 0.00 |
| asym (unseen) | 0.00 | 0.25 | 0.08 | 0.00 |
| u_channel (unseen) | 0.00 | 0.00 | 0.00 | 0.00 |
| plus (unseen) | 0.00 | 0.00 | 0.00 | 0.00 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.00 | 0.00 | 0.03 | 0.00 |
| B_left | 0.00 | 0.11 | 0.11 | 0.00 |
| C_backright | 0.00 | 0.00 | 0.00 | 0.00 |
| D_far_turn | 0.00 | 0.00 | 0.00 | 0.00 |
