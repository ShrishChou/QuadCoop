# Pair evaluation: ippo-aa_r8-s0-it3000

policy: checkpoint logs/marl2/ippo_aa_r8_s0/model_3000.pt (iteration 3000, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.78 | 0.72 | 0.06 | 0.08 | 18.0 | 0.36 | 0.43 | 0.34 | 0.15 | 0.28 | 0.54 |
| 40 kg | 0.66 | 0.62 | 0.05 | 0.18 | 22.1 | 0.38 | 0.48 | 0.43 | 0.24 | 0.40 | 0.53 |
| 60 kg | 0.49 | 0.40 | 0.17 | 0.17 | 27.4 | 0.38 | 0.55 | 0.50 | 0.29 | 0.41 | 0.55 |
| 80 kg | 0.27 | 0.24 | 0.19 | 0.24 | 35.1 | 0.40 | 0.56 | 0.54 | 0.33 | 0.45 | 0.55 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 1.00 | 0.92 | 0.83 | 0.50 |
| long | 0.92 | 0.83 | 0.75 | 0.50 |
| sphere | 0.92 | 1.00 | 0.92 | 0.83 |
| cylinder | 0.58 | 0.50 | 0.42 | 0.33 |
| arch | 0.25 | 0.25 | 0.08 | 0.00 |
| dumbbell | 0.75 | 0.58 | 0.25 | 0.00 |
| t_shape | 0.92 | 1.00 | 0.75 | 0.25 |
| beam (unseen) | 0.75 | 0.25 | 0.08 | 0.00 |
| l_shape (unseen) | 1.00 | 1.00 | 0.92 | 0.50 |
| asym (unseen) | 0.75 | 0.75 | 0.08 | 0.00 |
| u_channel (unseen) | 0.92 | 0.75 | 0.58 | 0.33 |
| plus (unseen) | 0.58 | 0.08 | 0.25 | 0.00 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.22 | 0.24 | 0.29 | 0.23 |
| long | 0.17 | 0.25 | 0.33 | 0.47 |
| sphere | 0.12 | 0.22 | 0.23 | 0.23 |
| cylinder | 0.18 | 0.27 | 0.36 | 0.38 |
| arch | 0.03 | 0.02 | 0.02 | 0.03 |
| dumbbell | 0.17 | 0.20 | 0.30 | 0.21 |
| t_shape | 0.17 | 0.36 | 0.37 | 0.37 |
| beam | 0.17 | 0.37 | 0.32 | 0.49 |
| l_shape | 0.10 | 0.25 | 0.41 | 0.51 |
| asym | 0.23 | 0.39 | 0.46 | 0.47 |
| u_channel | 0.13 | 0.20 | 0.21 | 0.32 |
| plus | 0.12 | 0.12 | 0.16 | 0.22 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.92 | 0.78 | 0.56 | 0.42 |
| B_left | 0.75 | 0.67 | 0.50 | 0.25 |
| C_backright | 0.75 | 0.61 | 0.50 | 0.28 |
| D_far_turn | 0.69 | 0.58 | 0.42 | 0.14 |
