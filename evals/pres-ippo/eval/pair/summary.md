# Pair evaluation: pres-ippo

policy: checkpoint logs/marl2/ippo_aa_kl_ten_s0/model_4000.pt (iteration 4000, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 10 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.90 | 0.86 | 0.01 | 0.04 | 18.0 | 0.10 | 0.53 | 0.32 | 0.17 | 0.29 | 0.69 |
| 40 kg | 0.82 | 0.76 | 0.04 | 0.04 | 23.4 | 0.10 | 0.58 | 0.41 | 0.24 | 0.36 | 0.67 |
| 60 kg | 0.53 | 0.48 | 0.10 | 0.14 | 36.2 | 0.11 | 0.61 | 0.47 | 0.29 | 0.40 | 0.67 |
| 80 kg | 0.24 | 0.21 | 0.13 | 0.13 | 36.0 | 0.09 | 0.64 | 0.51 | 0.33 | 0.44 | 0.65 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.97 | 0.97 | 0.55 | 0.10 |
| long | 0.97 | 1.00 | 0.70 | 0.35 |
| sphere | 0.93 | 0.90 | 0.90 | 0.95 |
| cylinder | 0.62 | 0.68 | 0.30 | 0.30 |
| arch | 0.55 | 0.53 | 0.28 | 0.07 |
| dumbbell | 1.00 | 0.82 | 0.45 | 0.15 |
| t_shape | 0.97 | 0.97 | 0.72 | 0.28 |
| beam (unseen) | 0.95 | 0.68 | 0.15 | 0.03 |
| l_shape (unseen) | 1.00 | 0.95 | 0.65 | 0.12 |
| asym (unseen) | 0.95 | 0.68 | 0.38 | 0.05 |
| u_channel (unseen) | 1.00 | 0.97 | 0.78 | 0.10 |
| plus (unseen) | 0.85 | 0.75 | 0.53 | 0.33 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.16 | 0.21 | 0.10 | 0.11 |
| long | 0.38 | 0.39 | 0.36 | 0.43 |
| sphere | 0.07 | 0.17 | 0.26 | 0.34 |
| cylinder | 0.21 | 0.32 | 0.39 | 0.39 |
| arch | 0.01 | 0.01 | 0.01 | 0.01 |
| dumbbell | 0.07 | 0.16 | 0.21 | 0.20 |
| t_shape | 0.22 | 0.27 | 0.28 | 0.25 |
| beam | 0.12 | 0.23 | 0.41 | 0.57 |
| l_shape | 0.18 | 0.29 | 0.33 | 0.44 |
| asym | 0.36 | 0.47 | 0.62 | 0.59 |
| u_channel | 0.15 | 0.25 | 0.28 | 0.31 |
| plus | 0.12 | 0.15 | 0.21 | 0.31 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.90 | 0.86 | 0.65 | 0.39 |
| B_left | 0.93 | 0.86 | 0.48 | 0.19 |
| C_backright | 0.94 | 0.81 | 0.52 | 0.17 |
| D_far_turn | 0.82 | 0.78 | 0.47 | 0.18 |
