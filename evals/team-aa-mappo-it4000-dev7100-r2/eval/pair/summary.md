# Pair evaluation: team-aa-mappo-it4000-dev7100-r2

policy: checkpoint logs/marl2/mappo_aa_kl_ten_s0/model_4000.pt (iteration 4000, mappo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.86 | 0.82 | 0.01 | 0.03 | 16.7 | 0.14 | 0.51 | 0.37 | 0.20 | 0.35 | 0.64 |
| 40 kg | 0.82 | 0.74 | 0.05 | 0.03 | 21.4 | 0.12 | 0.60 | 0.42 | 0.26 | 0.39 | 0.65 |
| 60 kg | 0.57 | 0.46 | 0.12 | 0.07 | 30.7 | 0.12 | 0.61 | 0.50 | 0.30 | 0.41 | 0.65 |
| 80 kg | 0.30 | 0.23 | 0.11 | 0.14 | 36.6 | 0.13 | 0.62 | 0.59 | 0.36 | 0.47 | 0.63 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 1.00 | 0.92 | 0.42 | 0.17 |
| long | 1.00 | 0.83 | 0.75 | 0.42 |
| sphere | 0.92 | 1.00 | 1.00 | 0.75 |
| cylinder | 0.67 | 0.58 | 0.33 | 0.17 |
| arch | 0.58 | 0.50 | 0.08 | 0.00 |
| dumbbell | 0.92 | 1.00 | 0.42 | 0.25 |
| t_shape | 1.00 | 1.00 | 0.75 | 0.42 |
| l_shape (unseen) | 1.00 | 1.00 | 0.92 | 0.42 |
| u_channel (unseen) | 1.00 | 1.00 | 0.75 | 0.25 |
| plus (unseen) | 0.50 | 0.42 | 0.33 | 0.17 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.18 | 0.17 | 0.13 | 0.20 |
| long | 0.35 | 0.43 | 0.35 | 0.46 |
| sphere | 0.15 | 0.20 | 0.34 | 0.35 |
| cylinder | 0.30 | 0.36 | 0.53 | 0.66 |
| arch | 0.01 | 0.01 | 0.01 | 0.01 |
| dumbbell | 0.12 | 0.17 | 0.26 | 0.24 |
| t_shape | 0.36 | 0.37 | 0.40 | 0.39 |
| l_shape | 0.29 | 0.44 | 0.52 | 0.65 |
| u_channel | 0.21 | 0.28 | 0.28 | 0.35 |
| plus | 0.07 | 0.19 | 0.20 | 0.32 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.90 | 0.93 | 0.70 | 0.47 |
| B_left | 0.90 | 0.83 | 0.67 | 0.47 |
| C_backright | 0.87 | 0.80 | 0.47 | 0.17 |
| D_far_turn | 0.77 | 0.73 | 0.47 | 0.10 |
