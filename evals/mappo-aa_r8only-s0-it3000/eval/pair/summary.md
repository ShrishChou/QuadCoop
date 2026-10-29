# Pair evaluation: mappo-aa_r8only-s0-it3000

policy: checkpoint logs/marl2/mappo_aa_r8only_s0/model_3000.pt (iteration 3000, mappo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.78 | 0.73 | 0.08 | 0.11 | 21.3 | 0.40 | 0.43 | 0.33 | 0.16 | 0.31 | 0.54 |
| 40 kg | 0.65 | 0.59 | 0.08 | 0.17 | 22.5 | 0.44 | 0.51 | 0.43 | 0.27 | 0.44 | 0.49 |
| 60 kg | 0.42 | 0.39 | 0.15 | 0.24 | 29.7 | 0.44 | 0.53 | 0.52 | 0.31 | 0.45 | 0.52 |
| 80 kg | 0.24 | 0.22 | 0.24 | 0.27 | 36.3 | 0.45 | 0.59 | 0.55 | 0.34 | 0.45 | 0.52 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.92 | 0.83 | 0.67 | 0.33 |
| long | 0.92 | 1.00 | 0.50 | 0.17 |
| sphere | 0.92 | 0.92 | 0.67 | 0.92 |
| cylinder | 0.42 | 0.58 | 0.42 | 0.17 |
| arch | 0.50 | 0.33 | 0.08 | 0.08 |
| dumbbell | 0.83 | 0.75 | 0.25 | 0.00 |
| t_shape | 1.00 | 0.75 | 0.58 | 0.25 |
| beam (unseen) | 0.75 | 0.17 | 0.00 | 0.00 |
| l_shape (unseen) | 1.00 | 1.00 | 0.58 | 0.42 |
| asym (unseen) | 0.83 | 0.58 | 0.33 | 0.00 |
| u_channel (unseen) | 0.83 | 0.67 | 0.50 | 0.33 |
| plus (unseen) | 0.50 | 0.25 | 0.42 | 0.17 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.27 | 0.22 | 0.25 | 0.38 |
| long | 0.26 | 0.44 | 0.32 | 0.43 |
| sphere | 0.12 | 0.15 | 0.15 | 0.15 |
| cylinder | 0.08 | 0.29 | 0.34 | 0.38 |
| arch | 0.04 | 0.02 | 0.02 | 0.04 |
| dumbbell | 0.15 | 0.19 | 0.18 | 0.31 |
| t_shape | 0.20 | 0.35 | 0.51 | 0.47 |
| beam | 0.19 | 0.50 | 0.41 | 0.45 |
| l_shape | 0.10 | 0.26 | 0.42 | 0.48 |
| asym | 0.31 | 0.40 | 0.55 | 0.34 |
| u_channel | 0.09 | 0.17 | 0.23 | 0.27 |
| plus | 0.12 | 0.19 | 0.35 | 0.32 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.92 | 0.78 | 0.64 | 0.31 |
| B_left | 0.78 | 0.53 | 0.22 | 0.17 |
| C_backright | 0.69 | 0.78 | 0.47 | 0.31 |
| D_far_turn | 0.75 | 0.53 | 0.33 | 0.17 |
