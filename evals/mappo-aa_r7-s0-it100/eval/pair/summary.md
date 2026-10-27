# Pair evaluation: mappo-aa_r7-s0-it100

policy: checkpoint logs/marl2/mappo_aa_r7_s0/model_100.pt (iteration 100, mappo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching |
|---|---|---|---|---|---|---|
| 20 kg | 0.69 | 0.68 | 0.10 | 0.12 | 19.2 | 0.48 |
| 40 kg | 0.54 | 0.47 | 0.17 | 0.17 | 24.7 | 0.52 |
| 60 kg | 0.35 | 0.31 | 0.22 | 0.29 | 33.1 | 0.52 |
| 80 kg | 0.20 | 0.18 | 0.28 | 0.24 | 29.8 | 0.51 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 1.00 | 0.67 | 0.42 | 0.17 |
| long | 0.75 | 0.75 | 0.67 | 0.25 |
| sphere | 1.00 | 0.92 | 0.67 | 0.83 |
| cylinder | 0.42 | 0.17 | 0.25 | 0.42 |
| arch | 0.33 | 0.17 | 0.17 | 0.00 |
| dumbbell | 0.83 | 0.58 | 0.42 | 0.08 |
| t_shape | 0.92 | 0.67 | 0.42 | 0.08 |
| beam (unseen) | 0.33 | 0.25 | 0.08 | 0.08 |
| l_shape (unseen) | 0.92 | 0.75 | 0.42 | 0.17 |
| asym (unseen) | 0.75 | 0.58 | 0.17 | 0.00 |
| u_channel (unseen) | 0.58 | 0.50 | 0.42 | 0.17 |
| plus (unseen) | 0.50 | 0.50 | 0.08 | 0.17 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.78 | 0.75 | 0.44 | 0.39 |
| B_left | 0.75 | 0.33 | 0.33 | 0.08 |
| C_backright | 0.53 | 0.58 | 0.47 | 0.19 |
| D_far_turn | 0.72 | 0.50 | 0.14 | 0.14 |
