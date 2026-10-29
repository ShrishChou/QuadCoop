# Pair evaluation: mappo-aa_r8-s0-it3000

policy: checkpoint logs/marl2/mappo_aa_r8_s0/model_3000.pt (iteration 3000, mappo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.77 | 0.76 | 0.06 | 0.07 | 23.9 | 0.32 | 0.39 | 0.31 | 0.12 | 0.25 | 0.60 |
| 40 kg | 0.62 | 0.59 | 0.07 | 0.15 | 24.2 | 0.39 | 0.45 | 0.41 | 0.21 | 0.37 | 0.54 |
| 60 kg | 0.42 | 0.35 | 0.12 | 0.26 | 28.4 | 0.35 | 0.52 | 0.50 | 0.29 | 0.44 | 0.54 |
| 80 kg | 0.24 | 0.20 | 0.18 | 0.23 | 41.3 | 0.39 | 0.59 | 0.57 | 0.35 | 0.45 | 0.53 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 1.00 | 0.92 | 0.75 | 0.33 |
| long | 1.00 | 1.00 | 0.58 | 0.17 |
| sphere | 0.92 | 0.83 | 0.75 | 0.92 |
| cylinder | 0.67 | 0.50 | 0.25 | 0.00 |
| arch | 0.58 | 0.42 | 0.00 | 0.00 |
| dumbbell | 0.67 | 0.67 | 0.17 | 0.00 |
| t_shape | 0.92 | 0.67 | 0.50 | 0.25 |
| beam (unseen) | 0.83 | 0.08 | 0.08 | 0.00 |
| l_shape (unseen) | 0.83 | 0.92 | 0.92 | 0.67 |
| asym (unseen) | 0.83 | 0.50 | 0.25 | 0.00 |
| u_channel (unseen) | 0.75 | 0.83 | 0.67 | 0.42 |
| plus (unseen) | 0.25 | 0.17 | 0.08 | 0.08 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.15 | 0.30 | 0.21 | 0.34 |
| long | 0.18 | 0.28 | 0.26 | 0.36 |
| sphere | 0.11 | 0.13 | 0.23 | 0.19 |
| cylinder | 0.14 | 0.26 | 0.42 | 0.41 |
| arch | 0.06 | 0.01 | 0.02 | 0.03 |
| dumbbell | 0.12 | 0.19 | 0.23 | 0.27 |
| t_shape | 0.12 | 0.28 | 0.25 | 0.31 |
| beam | 0.16 | 0.39 | 0.43 | 0.55 |
| l_shape | 0.13 | 0.25 | 0.48 | 0.65 |
| asym | 0.13 | 0.24 | 0.61 | 0.63 |
| u_channel | 0.12 | 0.10 | 0.17 | 0.24 |
| plus | 0.04 | 0.12 | 0.20 | 0.19 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.89 | 0.67 | 0.50 | 0.36 |
| B_left | 0.72 | 0.69 | 0.50 | 0.17 |
| C_backright | 0.78 | 0.67 | 0.44 | 0.28 |
| D_far_turn | 0.69 | 0.47 | 0.22 | 0.14 |
