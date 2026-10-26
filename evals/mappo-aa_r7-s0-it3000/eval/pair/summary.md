# Pair evaluation: mappo-aa_r7-s0-it3000

policy: checkpoint logs/marl2/mappo_aa_r7_s0/model_3000.pt (iteration 3000, mappo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching |
|---|---|---|---|---|---|---|
| 20 kg | 0.15 | 0.17 | 0.01 | 0.02 | 35.6 | 0.00 |
| 40 kg | 0.12 | 0.10 | 0.01 | 0.06 | 42.1 | 0.00 |
| 60 kg | 0.12 | 0.12 | 0.06 | 0.06 | 38.7 | 0.01 |
| 80 kg | 0.08 | 0.07 | 0.08 | 0.08 | 35.3 | 0.00 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.25 | 0.17 | 0.33 | 0.00 |
| long | 0.17 | 0.25 | 0.08 | 0.08 |
| sphere | 0.92 | 0.83 | 0.92 | 0.83 |
| cylinder | 0.00 | 0.00 | 0.00 | 0.00 |
| arch | 0.00 | 0.00 | 0.00 | 0.00 |
| dumbbell | 0.00 | 0.00 | 0.00 | 0.08 |
| t_shape | 0.08 | 0.00 | 0.00 | 0.00 |
| beam (unseen) | 0.00 | 0.00 | 0.00 | 0.00 |
| l_shape (unseen) | 0.00 | 0.08 | 0.00 | 0.00 |
| asym (unseen) | 0.17 | 0.08 | 0.08 | 0.00 |
| u_channel (unseen) | 0.00 | 0.00 | 0.00 | 0.00 |
| plus (unseen) | 0.17 | 0.00 | 0.00 | 0.00 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.25 | 0.19 | 0.08 | 0.11 |
| B_left | 0.08 | 0.08 | 0.14 | 0.08 |
| C_backright | 0.06 | 0.06 | 0.06 | 0.06 |
| D_far_turn | 0.19 | 0.14 | 0.19 | 0.08 |
