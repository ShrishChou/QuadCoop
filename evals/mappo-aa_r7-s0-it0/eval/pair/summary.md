# Pair evaluation: mappo-aa_r7-s0-it0

policy: checkpoint logs/marl2/mappo_aa_r7_s0/model_0.pt (iteration 0, mappo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching |
|---|---|---|---|---|---|---|
| 20 kg | 0.74 | 0.72 | 0.10 | 0.08 | 19.2 | 0.44 |
| 40 kg | 0.46 | 0.46 | 0.24 | 0.19 | 24.4 | 0.52 |
| 60 kg | 0.34 | 0.30 | 0.21 | 0.27 | 31.8 | 0.54 |
| 80 kg | 0.17 | 0.14 | 0.24 | 0.28 | 30.3 | 0.52 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.83 | 0.50 | 0.58 | 0.17 |
| long | 1.00 | 0.67 | 0.33 | 0.25 |
| sphere | 0.83 | 1.00 | 0.83 | 0.83 |
| cylinder | 0.42 | 0.25 | 0.33 | 0.17 |
| arch | 0.50 | 0.25 | 0.17 | 0.08 |
| dumbbell | 0.75 | 0.50 | 0.33 | 0.00 |
| t_shape | 0.75 | 0.67 | 0.33 | 0.08 |
| beam (unseen) | 0.50 | 0.08 | 0.00 | 0.00 |
| l_shape (unseen) | 1.00 | 0.67 | 0.67 | 0.17 |
| asym (unseen) | 0.92 | 0.25 | 0.08 | 0.00 |
| u_channel (unseen) | 0.83 | 0.58 | 0.33 | 0.17 |
| plus (unseen) | 0.58 | 0.08 | 0.08 | 0.08 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.86 | 0.58 | 0.53 | 0.31 |
| B_left | 0.75 | 0.39 | 0.28 | 0.06 |
| C_backright | 0.67 | 0.53 | 0.39 | 0.19 |
| D_far_turn | 0.69 | 0.33 | 0.17 | 0.11 |
