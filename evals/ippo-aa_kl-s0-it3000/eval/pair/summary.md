# Pair evaluation: ippo-aa_kl-s0-it3000

policy: checkpoint logs/marl2/ippo_aa_kl_s0/model_3000.pt (iteration 3000, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching |
|---|---|---|---|---|---|---|
| 20 kg | 0.90 | 0.82 | 0.01 | 0.03 | 18.5 | 0.09 |
| 40 kg | 0.75 | 0.69 | 0.08 | 0.07 | 25.7 | 0.10 |
| 60 kg | 0.48 | 0.45 | 0.08 | 0.17 | 38.8 | 0.10 |
| 80 kg | 0.17 | 0.16 | 0.14 | 0.12 | 29.9 | 0.11 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 1.00 | 0.92 | 0.58 | 0.08 |
| long | 1.00 | 0.92 | 0.67 | 0.25 |
| sphere | 1.00 | 1.00 | 1.00 | 1.00 |
| cylinder | 0.67 | 0.58 | 0.25 | 0.17 |
| arch | 0.50 | 0.42 | 0.25 | 0.08 |
| dumbbell | 1.00 | 0.67 | 0.42 | 0.08 |
| t_shape | 1.00 | 1.00 | 0.25 | 0.00 |
| beam (unseen) | 0.83 | 0.42 | 0.08 | 0.00 |
| l_shape (unseen) | 0.92 | 0.83 | 0.58 | 0.08 |
| asym (unseen) | 0.92 | 0.58 | 0.50 | 0.00 |
| u_channel (unseen) | 1.00 | 0.92 | 0.67 | 0.08 |
| plus (unseen) | 0.92 | 0.75 | 0.50 | 0.25 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.92 | 0.81 | 0.61 | 0.25 |
| B_left | 0.92 | 0.78 | 0.53 | 0.19 |
| C_backright | 0.89 | 0.78 | 0.42 | 0.14 |
| D_far_turn | 0.86 | 0.64 | 0.36 | 0.11 |
