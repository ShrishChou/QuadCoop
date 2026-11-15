# Pair evaluation: pres-ippo-it4000

policy: checkpoint logs/marl2/ippo_aa_kl_ten_s0/model_4000.pt (iteration 4000, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.88 | 0.84 | 0.01 | 0.03 | 16.6 | 0.12 | 0.51 | 0.29 | 0.15 | 0.27 | 0.64 |
| 40 kg | 0.83 | 0.80 | 0.03 | 0.03 | 22.3 | 0.11 | 0.56 | 0.37 | 0.20 | 0.31 | 0.64 |
| 60 kg | 0.62 | 0.53 | 0.08 | 0.07 | 34.7 | 0.11 | 0.58 | 0.41 | 0.24 | 0.36 | 0.66 |
| 80 kg | 0.28 | 0.27 | 0.12 | 0.12 | 30.8 | 0.11 | 0.61 | 0.42 | 0.26 | 0.37 | 0.64 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 1.00 | 1.00 | 0.75 | 0.00 |
| long | 1.00 | 0.92 | 0.75 | 0.17 |
| sphere | 1.00 | 1.00 | 1.00 | 1.00 |
| cylinder | 0.67 | 0.42 | 0.33 | 0.17 |
| arch | 0.67 | 0.50 | 0.17 | 0.08 |
| dumbbell | 0.92 | 0.92 | 0.42 | 0.17 |
| t_shape | 1.00 | 0.83 | 0.75 | 0.33 |
| l_shape (unseen) | 1.00 | 0.92 | 0.67 | 0.33 |
| u_channel (unseen) | 1.00 | 1.00 | 0.67 | 0.17 |
| plus (unseen) | 0.58 | 0.83 | 0.67 | 0.33 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.16 | 0.25 | 0.20 | 0.05 |
| long | 0.40 | 0.35 | 0.39 | 0.43 |
| sphere | 0.12 | 0.21 | 0.34 | 0.27 |
| cylinder | 0.16 | 0.29 | 0.32 | 0.36 |
| arch | 0.01 | 0.00 | 0.02 | 0.00 |
| dumbbell | 0.06 | 0.10 | 0.18 | 0.22 |
| t_shape | 0.25 | 0.31 | 0.21 | 0.38 |
| l_shape | 0.17 | 0.23 | 0.25 | 0.32 |
| u_channel | 0.14 | 0.16 | 0.28 | 0.31 |
| plus | 0.06 | 0.11 | 0.25 | 0.26 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.87 | 0.83 | 0.80 | 0.50 |
| B_left | 0.97 | 0.90 | 0.70 | 0.30 |
| C_backright | 0.87 | 0.83 | 0.43 | 0.13 |
| D_far_turn | 0.83 | 0.77 | 0.53 | 0.17 |
