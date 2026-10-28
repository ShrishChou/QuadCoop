# Pair evaluation: mappo-aa_kl02-s0-it3000

policy: checkpoint logs/marl2/mappo_aa_kl02_s0/model_3000.pt (iteration 3000, mappo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching |
|---|---|---|---|---|---|---|
| 20 kg | 0.74 | 0.71 | 0.08 | 0.10 | 18.9 | 0.39 |
| 40 kg | 0.60 | 0.53 | 0.10 | 0.18 | 21.7 | 0.45 |
| 60 kg | 0.42 | 0.38 | 0.24 | 0.22 | 30.0 | 0.47 |
| 80 kg | 0.22 | 0.19 | 0.20 | 0.23 | 33.9 | 0.47 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.83 | 0.92 | 0.25 | 0.33 |
| long | 0.83 | 0.75 | 0.50 | 0.17 |
| sphere | 0.83 | 0.92 | 0.83 | 0.92 |
| cylinder | 0.58 | 0.25 | 0.25 | 0.25 |
| arch | 0.50 | 0.33 | 0.08 | 0.00 |
| dumbbell | 0.83 | 0.67 | 0.67 | 0.00 |
| t_shape | 0.83 | 0.83 | 0.58 | 0.08 |
| beam (unseen) | 0.75 | 0.25 | 0.08 | 0.08 |
| l_shape (unseen) | 0.92 | 1.00 | 0.75 | 0.33 |
| asym (unseen) | 0.83 | 0.42 | 0.08 | 0.00 |
| u_channel (unseen) | 0.83 | 0.67 | 0.67 | 0.25 |
| plus (unseen) | 0.33 | 0.25 | 0.25 | 0.25 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.83 | 0.67 | 0.47 | 0.39 |
| B_left | 0.75 | 0.61 | 0.44 | 0.14 |
| C_backright | 0.69 | 0.56 | 0.42 | 0.22 |
| D_far_turn | 0.69 | 0.58 | 0.33 | 0.14 |
