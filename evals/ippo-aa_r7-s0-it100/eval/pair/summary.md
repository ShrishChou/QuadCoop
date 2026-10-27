# Pair evaluation: ippo-aa_r7-s0-it100

policy: checkpoint logs/marl2/ippo_aa_r7_s0/model_100.pt (iteration 100, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching |
|---|---|---|---|---|---|---|
| 20 kg | 0.70 | 0.69 | 0.09 | 0.12 | 19.8 | 0.45 |
| 40 kg | 0.50 | 0.44 | 0.17 | 0.27 | 24.8 | 0.50 |
| 60 kg | 0.29 | 0.28 | 0.25 | 0.28 | 31.2 | 0.52 |
| 80 kg | 0.20 | 0.17 | 0.31 | 0.19 | 34.3 | 0.52 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.83 | 0.50 | 0.42 | 0.17 |
| long | 0.92 | 0.58 | 0.42 | 0.25 |
| sphere | 0.83 | 0.83 | 0.75 | 0.92 |
| cylinder | 0.08 | 0.33 | 0.08 | 0.25 |
| arch | 0.50 | 0.25 | 0.17 | 0.00 |
| dumbbell | 0.83 | 0.50 | 0.33 | 0.17 |
| t_shape | 0.92 | 0.75 | 0.25 | 0.17 |
| beam (unseen) | 0.67 | 0.25 | 0.00 | 0.00 |
| l_shape (unseen) | 0.75 | 0.67 | 0.42 | 0.17 |
| asym (unseen) | 0.83 | 0.75 | 0.17 | 0.00 |
| u_channel (unseen) | 0.92 | 0.25 | 0.42 | 0.08 |
| plus (unseen) | 0.33 | 0.33 | 0.08 | 0.25 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.83 | 0.72 | 0.42 | 0.31 |
| B_left | 0.78 | 0.39 | 0.25 | 0.11 |
| C_backright | 0.50 | 0.53 | 0.36 | 0.25 |
| D_far_turn | 0.69 | 0.36 | 0.14 | 0.14 |
