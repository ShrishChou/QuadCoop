# Pair evaluation: ten-ippo-it4000-dev7100-recovery

policy: checkpoint logs/marl2/ippo_aa_kl_ten_s0/model_4000.pt (iteration 4000, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.90 | 0.87 | 0.01 | 0.03 | 17.5 | 0.11 | 0.50 | 0.33 | 0.17 | 0.31 | 0.63 |
| 40 kg | 0.84 | 0.80 | 0.01 | 0.07 | 22.0 | 0.12 | 0.54 | 0.39 | 0.21 | 0.32 | 0.64 |
| 60 kg | 0.60 | 0.53 | 0.12 | 0.03 | 36.8 | 0.11 | 0.61 | 0.40 | 0.24 | 0.35 | 0.68 |
| 80 kg | 0.25 | 0.23 | 0.06 | 0.11 | 31.4 | 0.09 | 0.60 | 0.42 | 0.25 | 0.35 | 0.65 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 1.00 | 0.83 | 0.50 | 0.00 |
| long | 1.00 | 1.00 | 0.58 | 0.33 |
| sphere | 1.00 | 1.00 | 0.92 | 0.92 |
| cylinder | 0.58 | 0.50 | 0.25 | 0.25 |
| arch | 0.75 | 0.67 | 0.25 | 0.00 |
| dumbbell | 1.00 | 0.67 | 0.50 | 0.08 |
| t_shape | 0.92 | 1.00 | 0.75 | 0.17 |
| l_shape (unseen) | 1.00 | 1.00 | 0.83 | 0.42 |
| u_channel (unseen) | 1.00 | 1.00 | 0.67 | 0.08 |
| plus (unseen) | 0.75 | 0.75 | 0.75 | 0.25 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.20 | 0.29 | 0.15 | 0.02 |
| long | 0.40 | 0.32 | 0.36 | 0.38 |
| sphere | 0.12 | 0.22 | 0.31 | 0.25 |
| cylinder | 0.23 | 0.30 | 0.36 | 0.26 |
| arch | 0.01 | 0.01 | 0.00 | 0.00 |
| dumbbell | 0.05 | 0.09 | 0.21 | 0.16 |
| t_shape | 0.26 | 0.29 | 0.22 | 0.31 |
| l_shape | 0.19 | 0.26 | 0.28 | 0.48 |
| u_channel | 0.13 | 0.20 | 0.25 | 0.33 |
| plus | 0.13 | 0.09 | 0.25 | 0.29 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.90 | 0.97 | 0.80 | 0.43 |
| B_left | 0.87 | 0.83 | 0.53 | 0.23 |
| C_backright | 0.93 | 0.87 | 0.70 | 0.23 |
| D_far_turn | 0.90 | 0.70 | 0.37 | 0.10 |
