# Pair evaluation: mappo-aa_kl-s0-it3000

policy: checkpoint logs/marl2/mappo_aa_kl_s0/model_3000.pt (iteration 3000, mappo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.88 | 0.82 | 0.01 | 0.01 | 19.6 | 0.12 | 0.50 | 0.37 | 0.19 | 0.31 | 0.66 |
| 40 kg | 0.76 | 0.70 | 0.01 | 0.06 | 23.9 | 0.14 | 0.55 | 0.45 | 0.25 | 0.38 | 0.66 |
| 60 kg | 0.47 | 0.43 | 0.14 | 0.12 | 32.3 | 0.14 | 0.54 | 0.56 | 0.30 | 0.42 | 0.66 |
| 80 kg | 0.20 | 0.17 | 0.15 | 0.13 | 31.8 | 0.13 | 0.59 | 0.58 | 0.34 | 0.43 | 0.66 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 1.00 | 1.00 | 0.33 | 0.00 |
| long | 0.92 | 0.83 | 0.58 | 0.42 |
| sphere | 1.00 | 1.00 | 1.00 | 1.00 |
| cylinder | 0.67 | 0.67 | 0.33 | 0.25 |
| arch | 0.42 | 0.33 | 0.25 | 0.08 |
| dumbbell | 1.00 | 0.92 | 0.67 | 0.00 |
| t_shape | 1.00 | 0.92 | 0.50 | 0.25 |
| beam (unseen) | 0.92 | 0.50 | 0.08 | 0.08 |
| l_shape (unseen) | 1.00 | 0.92 | 0.42 | 0.25 |
| asym (unseen) | 0.92 | 0.75 | 0.33 | 0.00 |
| u_channel (unseen) | 1.00 | 0.83 | 0.75 | 0.00 |
| plus (unseen) | 0.67 | 0.50 | 0.42 | 0.08 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.13 | 0.20 | 0.11 | 0.03 |
| long | 0.38 | 0.38 | 0.42 | 0.50 |
| sphere | 0.09 | 0.18 | 0.30 | 0.41 |
| cylinder | 0.25 | 0.34 | 0.49 | 0.42 |
| arch | 0.01 | 0.01 | 0.02 | 0.01 |
| dumbbell | 0.14 | 0.20 | 0.19 | 0.23 |
| t_shape | 0.25 | 0.34 | 0.39 | 0.47 |
| beam | 0.15 | 0.25 | 0.47 | 0.56 |
| l_shape | 0.21 | 0.36 | 0.34 | 0.43 |
| asym | 0.33 | 0.38 | 0.51 | 0.50 |
| u_channel | 0.22 | 0.26 | 0.27 | 0.36 |
| plus | 0.07 | 0.11 | 0.12 | 0.11 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.97 | 0.89 | 0.58 | 0.39 |
| B_left | 0.92 | 0.78 | 0.61 | 0.11 |
| C_backright | 0.83 | 0.72 | 0.31 | 0.17 |
| D_far_turn | 0.78 | 0.67 | 0.39 | 0.14 |
