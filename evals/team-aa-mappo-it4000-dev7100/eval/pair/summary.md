# Pair evaluation: team-aa-mappo-it4000-dev7100

policy: checkpoint logs/marl2/mappo_aa_kl_ten_s0/model_4000.pt (iteration 4000, mappo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.86 | 0.78 | 0.03 | 0.03 | 16.5 | 0.13 | 0.53 | 0.35 | 0.21 | 0.35 | 0.65 |
| 40 kg | 0.82 | 0.72 | 0.01 | 0.03 | 20.5 | 0.14 | 0.57 | 0.44 | 0.27 | 0.40 | 0.67 |
| 60 kg | 0.62 | 0.54 | 0.07 | 0.04 | 30.5 | 0.13 | 0.61 | 0.47 | 0.28 | 0.38 | 0.64 |
| 80 kg | 0.31 | 0.29 | 0.15 | 0.07 | 34.1 | 0.12 | 0.58 | 0.58 | 0.32 | 0.41 | 0.64 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 1.00 | 0.92 | 0.58 | 0.17 |
| long | 1.00 | 1.00 | 0.75 | 0.42 |
| sphere | 1.00 | 1.00 | 1.00 | 0.83 |
| cylinder | 0.67 | 0.50 | 0.42 | 0.33 |
| arch | 0.42 | 0.50 | 0.08 | 0.00 |
| dumbbell | 0.92 | 0.83 | 0.58 | 0.17 |
| t_shape | 1.00 | 1.00 | 0.83 | 0.42 |
| l_shape (unseen) | 1.00 | 1.00 | 0.83 | 0.42 |
| u_channel (unseen) | 1.00 | 1.00 | 0.75 | 0.08 |
| plus (unseen) | 0.58 | 0.42 | 0.42 | 0.25 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.17 | 0.15 | 0.16 | 0.15 |
| long | 0.36 | 0.40 | 0.31 | 0.37 |
| sphere | 0.13 | 0.23 | 0.34 | 0.35 |
| cylinder | 0.45 | 0.32 | 0.50 | 0.45 |
| arch | 0.02 | 0.02 | 0.02 | 0.01 |
| dumbbell | 0.07 | 0.20 | 0.20 | 0.22 |
| t_shape | 0.32 | 0.42 | 0.34 | 0.47 |
| l_shape | 0.25 | 0.44 | 0.48 | 0.63 |
| u_channel | 0.22 | 0.32 | 0.26 | 0.35 |
| plus | 0.12 | 0.16 | 0.17 | 0.16 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.97 | 0.93 | 0.83 | 0.57 |
| B_left | 0.90 | 0.80 | 0.83 | 0.50 |
| C_backright | 0.83 | 0.80 | 0.43 | 0.07 |
| D_far_turn | 0.73 | 0.73 | 0.40 | 0.10 |
