# Pair evaluation: mappo-aa_kl002-s0-it3000

policy: checkpoint logs/marl2/mappo_aa_kl002_s0/model_3000.pt (iteration 3000, mappo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching |
|---|---|---|---|---|---|---|
| 20 kg | 0.89 | 0.83 | 0.00 | 0.02 | 21.5 | 0.07 |
| 40 kg | 0.67 | 0.62 | 0.02 | 0.08 | 25.4 | 0.10 |
| 60 kg | 0.49 | 0.42 | 0.12 | 0.06 | 31.9 | 0.10 |
| 80 kg | 0.19 | 0.17 | 0.15 | 0.12 | 31.8 | 0.08 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.92 | 1.00 | 0.67 | 0.00 |
| long | 1.00 | 0.92 | 0.67 | 0.25 |
| sphere | 1.00 | 1.00 | 1.00 | 1.00 |
| cylinder | 0.75 | 0.50 | 0.67 | 0.42 |
| arch | 0.67 | 0.25 | 0.17 | 0.17 |
| dumbbell | 0.92 | 0.75 | 0.42 | 0.08 |
| t_shape | 1.00 | 0.92 | 0.25 | 0.00 |
| beam (unseen) | 0.67 | 0.33 | 0.17 | 0.00 |
| l_shape (unseen) | 1.00 | 0.83 | 0.75 | 0.33 |
| asym (unseen) | 0.92 | 0.42 | 0.25 | 0.00 |
| u_channel (unseen) | 1.00 | 0.83 | 0.67 | 0.00 |
| plus (unseen) | 0.83 | 0.25 | 0.25 | 0.00 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.97 | 0.67 | 0.56 | 0.28 |
| B_left | 0.92 | 0.75 | 0.69 | 0.17 |
| C_backright | 0.89 | 0.72 | 0.44 | 0.19 |
| D_far_turn | 0.78 | 0.53 | 0.28 | 0.11 |
