# Pair evaluation: mappo-aa_kl-s1-it3000

policy: checkpoint logs/marl2/mappo_aa_kl_s1/model_3000.pt (iteration 3000, mappo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching |
|---|---|---|---|---|---|---|
| 20 kg | 0.84 | 0.77 | 0.03 | 0.03 | 18.9 | 0.13 |
| 40 kg | 0.80 | 0.76 | 0.05 | 0.06 | 24.8 | 0.13 |
| 60 kg | 0.50 | 0.44 | 0.13 | 0.07 | 31.6 | 0.13 |
| 80 kg | 0.23 | 0.20 | 0.15 | 0.13 | 32.7 | 0.14 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 1.00 | 0.92 | 0.58 | 0.08 |
| long | 1.00 | 1.00 | 0.58 | 0.33 |
| sphere | 0.92 | 0.83 | 1.00 | 1.00 |
| cylinder | 0.58 | 0.58 | 0.25 | 0.33 |
| arch | 0.58 | 0.58 | 0.00 | 0.00 |
| dumbbell | 1.00 | 0.83 | 0.67 | 0.17 |
| t_shape | 1.00 | 1.00 | 0.50 | 0.08 |
| beam (unseen) | 0.67 | 0.58 | 0.17 | 0.08 |
| l_shape (unseen) | 1.00 | 0.83 | 0.75 | 0.33 |
| asym (unseen) | 1.00 | 0.75 | 0.50 | 0.00 |
| u_channel (unseen) | 0.92 | 1.00 | 0.67 | 0.08 |
| plus (unseen) | 0.42 | 0.67 | 0.33 | 0.25 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.94 | 0.92 | 0.75 | 0.50 |
| B_left | 0.83 | 0.83 | 0.56 | 0.22 |
| C_backright | 0.86 | 0.78 | 0.36 | 0.08 |
| D_far_turn | 0.72 | 0.67 | 0.33 | 0.11 |
