# Pair evaluation: mappo-aa_kl-s0-it3000

policy: checkpoint logs/marl2/mappo_aa_kl_s0/model_3000.pt (iteration 3000, mappo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching |
|---|---|---|---|---|---|---|
| 20 kg | 0.84 | 0.81 | 0.03 | 0.03 | 20.2 | 0.11 |
| 40 kg | 0.77 | 0.71 | 0.04 | 0.03 | 24.1 | 0.13 |
| 60 kg | 0.53 | 0.46 | 0.10 | 0.09 | 35.2 | 0.14 |
| 80 kg | 0.25 | 0.22 | 0.15 | 0.09 | 33.0 | 0.12 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 1.00 | 0.92 | 0.50 | 0.17 |
| long | 0.92 | 1.00 | 0.67 | 0.42 |
| sphere | 1.00 | 0.92 | 0.92 | 1.00 |
| cylinder | 0.58 | 0.58 | 0.25 | 0.33 |
| arch | 0.25 | 0.42 | 0.17 | 0.00 |
| dumbbell | 1.00 | 0.83 | 0.42 | 0.17 |
| t_shape | 1.00 | 1.00 | 0.50 | 0.08 |
| beam (unseen) | 1.00 | 0.75 | 0.33 | 0.08 |
| l_shape (unseen) | 1.00 | 0.92 | 0.67 | 0.33 |
| asym (unseen) | 0.67 | 0.67 | 0.75 | 0.00 |
| u_channel (unseen) | 1.00 | 0.83 | 0.67 | 0.25 |
| plus (unseen) | 0.67 | 0.42 | 0.50 | 0.17 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.86 | 0.78 | 0.72 | 0.47 |
| B_left | 0.86 | 0.78 | 0.64 | 0.28 |
| C_backright | 0.86 | 0.78 | 0.39 | 0.08 |
| D_far_turn | 0.78 | 0.75 | 0.36 | 0.17 |
