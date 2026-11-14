# Pair evaluation: ten-ippo-source-dev7100-recovery

policy: checkpoint logs/marl2/ippo_aa_kl_s0/model_3000.pt (iteration 3000, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.93 | 0.87 | 0.03 | 0.01 | 17.2 | 0.09 | 0.52 | 0.27 | 0.12 | 0.21 | 0.72 |
| 40 kg | 0.85 | 0.82 | 0.05 | 0.03 | 24.1 | 0.10 | 0.54 | 0.34 | 0.16 | 0.25 | 0.70 |
| 60 kg | 0.56 | 0.53 | 0.11 | 0.07 | 38.2 | 0.10 | 0.60 | 0.37 | 0.19 | 0.28 | 0.65 |
| 80 kg | 0.24 | 0.23 | 0.12 | 0.06 | 31.7 | 0.10 | 0.58 | 0.43 | 0.23 | 0.32 | 0.65 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 1.00 | 0.92 | 0.58 | 0.00 |
| long | 1.00 | 1.00 | 0.83 | 0.33 |
| sphere | 1.00 | 1.00 | 0.92 | 1.00 |
| cylinder | 0.75 | 0.67 | 0.08 | 0.25 |
| arch | 0.75 | 0.67 | 0.25 | 0.00 |
| dumbbell | 1.00 | 0.83 | 0.58 | 0.08 |
| t_shape | 1.00 | 0.92 | 0.58 | 0.08 |
| l_shape (unseen) | 0.92 | 0.92 | 0.67 | 0.25 |
| u_channel (unseen) | 1.00 | 0.92 | 0.58 | 0.08 |
| plus (unseen) | 0.83 | 0.67 | 0.50 | 0.33 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.12 | 0.11 | 0.12 | 0.08 |
| long | 0.33 | 0.37 | 0.38 | 0.46 |
| sphere | 0.05 | 0.10 | 0.16 | 0.29 |
| cylinder | 0.17 | 0.33 | 0.36 | 0.37 |
| arch | 0.01 | 0.01 | 0.00 | 0.00 |
| dumbbell | 0.04 | 0.10 | 0.11 | 0.17 |
| t_shape | 0.17 | 0.16 | 0.20 | 0.25 |
| l_shape | 0.03 | 0.15 | 0.27 | 0.18 |
| u_channel | 0.15 | 0.15 | 0.18 | 0.26 |
| plus | 0.14 | 0.15 | 0.17 | 0.25 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.93 | 0.87 | 0.60 | 0.43 |
| B_left | 0.93 | 0.90 | 0.57 | 0.23 |
| C_backright | 0.97 | 0.93 | 0.57 | 0.17 |
| D_far_turn | 0.87 | 0.70 | 0.50 | 0.13 |
