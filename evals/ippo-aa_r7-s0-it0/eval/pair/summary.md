# Pair evaluation: ippo-aa_r7-s0-it0

policy: checkpoint logs/marl2/ippo_aa_r7_s0/model_0.pt (iteration 0, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching |
|---|---|---|---|---|---|---|
| 20 kg | 0.67 | 0.65 | 0.12 | 0.15 | 19.5 | 0.48 |
| 40 kg | 0.51 | 0.47 | 0.19 | 0.17 | 25.3 | 0.53 |
| 60 kg | 0.41 | 0.35 | 0.17 | 0.26 | 32.6 | 0.53 |
| 80 kg | 0.17 | 0.15 | 0.28 | 0.24 | 27.6 | 0.53 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.92 | 0.67 | 0.67 | 0.17 |
| long | 0.92 | 0.83 | 0.58 | 0.17 |
| sphere | 0.67 | 0.67 | 0.92 | 1.00 |
| cylinder | 0.33 | 0.25 | 0.17 | 0.17 |
| arch | 0.50 | 0.25 | 0.00 | 0.00 |
| dumbbell | 0.75 | 0.58 | 0.67 | 0.08 |
| t_shape | 0.83 | 0.75 | 0.33 | 0.08 |
| beam (unseen) | 0.42 | 0.17 | 0.17 | 0.00 |
| l_shape (unseen) | 0.83 | 0.83 | 0.67 | 0.00 |
| asym (unseen) | 0.92 | 0.33 | 0.17 | 0.00 |
| u_channel (unseen) | 0.50 | 0.50 | 0.50 | 0.17 |
| plus (unseen) | 0.50 | 0.25 | 0.08 | 0.17 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.81 | 0.61 | 0.50 | 0.25 |
| B_left | 0.69 | 0.47 | 0.39 | 0.11 |
| C_backright | 0.64 | 0.50 | 0.44 | 0.17 |
| D_far_turn | 0.56 | 0.44 | 0.31 | 0.14 |
