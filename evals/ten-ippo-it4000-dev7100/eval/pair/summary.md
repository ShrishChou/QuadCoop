# Pair evaluation: ten-ippo-it4000-dev7100

policy: checkpoint logs/marl2/ippo_aa_kl_ten_s0/model_4000.pt (iteration 4000, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.88 | 0.82 | 0.03 | 0.03 | 17.0 | 0.13 | 0.51 | 0.33 | 0.16 | 0.27 | 0.65 |
| 40 kg | 0.88 | 0.81 | 0.01 | 0.03 | 22.6 | 0.11 | 0.57 | 0.36 | 0.21 | 0.33 | 0.69 |
| 60 kg | 0.59 | 0.55 | 0.09 | 0.05 | 35.1 | 0.10 | 0.61 | 0.40 | 0.23 | 0.33 | 0.64 |
| 80 kg | 0.28 | 0.25 | 0.12 | 0.09 | 32.6 | 0.11 | 0.61 | 0.46 | 0.27 | 0.36 | 0.64 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.92 | 1.00 | 0.58 | 0.00 |
| long | 1.00 | 1.00 | 0.67 | 0.25 |
| sphere | 1.00 | 1.00 | 0.92 | 1.00 |
| cylinder | 0.75 | 0.58 | 0.25 | 0.25 |
| arch | 0.42 | 0.58 | 0.25 | 0.08 |
| dumbbell | 0.92 | 0.83 | 0.58 | 0.08 |
| t_shape | 1.00 | 1.00 | 0.67 | 0.17 |
| l_shape (unseen) | 1.00 | 0.92 | 0.83 | 0.42 |
| u_channel (unseen) | 0.92 | 1.00 | 0.75 | 0.08 |
| plus (unseen) | 0.92 | 0.83 | 0.42 | 0.42 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.20 | 0.31 | 0.16 | 0.10 |
| long | 0.39 | 0.41 | 0.37 | 0.44 |
| sphere | 0.15 | 0.21 | 0.27 | 0.26 |
| cylinder | 0.12 | 0.32 | 0.34 | 0.45 |
| arch | 0.01 | 0.01 | 0.01 | 0.01 |
| dumbbell | 0.06 | 0.14 | 0.13 | 0.17 |
| t_shape | 0.28 | 0.27 | 0.16 | 0.32 |
| l_shape | 0.15 | 0.26 | 0.29 | 0.36 |
| u_channel | 0.14 | 0.13 | 0.30 | 0.27 |
| plus | 0.13 | 0.08 | 0.24 | 0.29 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.83 | 0.90 | 0.73 | 0.53 |
| B_left | 0.93 | 0.87 | 0.53 | 0.27 |
| C_backright | 0.97 | 0.87 | 0.57 | 0.17 |
| D_far_turn | 0.80 | 0.87 | 0.53 | 0.13 |
