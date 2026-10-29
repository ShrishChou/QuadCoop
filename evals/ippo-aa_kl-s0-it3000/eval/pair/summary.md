# Pair evaluation: ippo-aa_kl-s0-it3000

policy: checkpoint logs/marl2/ippo_aa_kl_s0/model_3000.pt (iteration 3000, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.91 | 0.86 | 0.02 | 0.04 | 18.6 | 0.08 | 0.55 | 0.29 | 0.15 | 0.24 | 0.71 |
| 40 kg | 0.80 | 0.76 | 0.03 | 0.05 | 25.5 | 0.11 | 0.59 | 0.36 | 0.18 | 0.27 | 0.68 |
| 60 kg | 0.49 | 0.41 | 0.14 | 0.08 | 37.0 | 0.10 | 0.62 | 0.41 | 0.25 | 0.36 | 0.68 |
| 80 kg | 0.20 | 0.19 | 0.12 | 0.15 | 34.7 | 0.11 | 0.63 | 0.46 | 0.28 | 0.38 | 0.65 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 1.00 | 1.00 | 0.50 | 0.17 |
| long | 1.00 | 0.92 | 0.83 | 0.33 |
| sphere | 0.83 | 1.00 | 1.00 | 1.00 |
| cylinder | 0.58 | 0.67 | 0.42 | 0.08 |
| arch | 0.92 | 0.50 | 0.25 | 0.08 |
| dumbbell | 1.00 | 0.83 | 0.42 | 0.00 |
| t_shape | 1.00 | 0.92 | 0.17 | 0.00 |
| beam (unseen) | 0.83 | 0.50 | 0.17 | 0.08 |
| l_shape (unseen) | 1.00 | 0.92 | 0.42 | 0.17 |
| asym (unseen) | 1.00 | 0.67 | 0.33 | 0.00 |
| u_channel (unseen) | 1.00 | 1.00 | 0.67 | 0.17 |
| plus (unseen) | 0.75 | 0.67 | 0.67 | 0.33 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.13 | 0.04 | 0.08 | 0.11 |
| long | 0.35 | 0.36 | 0.45 | 0.50 |
| sphere | 0.02 | 0.09 | 0.22 | 0.31 |
| cylinder | 0.21 | 0.24 | 0.40 | 0.38 |
| arch | 0.01 | 0.00 | 0.00 | 0.00 |
| dumbbell | 0.03 | 0.10 | 0.14 | 0.08 |
| t_shape | 0.20 | 0.22 | 0.18 | 0.28 |
| beam | 0.15 | 0.31 | 0.47 | 0.47 |
| l_shape | 0.05 | 0.13 | 0.16 | 0.19 |
| asym | 0.35 | 0.36 | 0.57 | 0.54 |
| u_channel | 0.11 | 0.22 | 0.17 | 0.27 |
| plus | 0.16 | 0.16 | 0.21 | 0.27 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.92 | 0.83 | 0.61 | 0.33 |
| B_left | 0.92 | 0.89 | 0.64 | 0.22 |
| C_backright | 0.94 | 0.81 | 0.44 | 0.14 |
| D_far_turn | 0.86 | 0.67 | 0.25 | 0.11 |
