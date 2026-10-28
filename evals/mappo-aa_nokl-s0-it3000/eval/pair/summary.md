# Pair evaluation: mappo-aa_nokl-s0-it3000

policy: checkpoint logs/marl2/mappo_aa_nokl_s0/model_3000.pt (iteration 3000, mappo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching |
|---|---|---|---|---|---|---|
| 20 kg | 0.58 | 0.59 | 0.03 | 0.07 | 29.2 | 0.01 |
| 40 kg | 0.47 | 0.41 | 0.10 | 0.07 | 33.9 | 0.01 |
| 60 kg | 0.24 | 0.19 | 0.15 | 0.14 | 35.3 | 0.01 |
| 80 kg | 0.10 | 0.10 | 0.19 | 0.18 | 21.1 | 0.01 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.92 | 0.92 | 0.42 | 0.00 |
| long | 0.67 | 0.83 | 0.33 | 0.00 |
| sphere | 1.00 | 1.00 | 1.00 | 1.00 |
| cylinder | 0.42 | 0.25 | 0.08 | 0.08 |
| arch | 0.33 | 0.25 | 0.08 | 0.00 |
| dumbbell | 0.33 | 0.17 | 0.17 | 0.00 |
| t_shape | 0.50 | 0.42 | 0.25 | 0.00 |
| beam (unseen) | 0.25 | 0.00 | 0.00 | 0.00 |
| l_shape (unseen) | 0.92 | 0.50 | 0.33 | 0.08 |
| asym (unseen) | 0.75 | 0.50 | 0.00 | 0.00 |
| u_channel (unseen) | 0.58 | 0.58 | 0.17 | 0.08 |
| plus (unseen) | 0.33 | 0.25 | 0.08 | 0.00 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.64 | 0.47 | 0.25 | 0.11 |
| B_left | 0.67 | 0.56 | 0.33 | 0.14 |
| C_backright | 0.42 | 0.44 | 0.19 | 0.08 |
| D_far_turn | 0.61 | 0.42 | 0.19 | 0.08 |
