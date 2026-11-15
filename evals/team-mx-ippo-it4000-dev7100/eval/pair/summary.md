# Pair evaluation: team-mx-ippo-it4000-dev7100

policy: checkpoint logs/marl2/ippo_mx_kl_ten_s0/model_4000.pt (iteration 4000, ippo, pair mixed)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal fell | spot fell | time to success (s) | robots touching | anymal pushing | spot pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.89 | 0.85 | 0.00 | 0.07 | 18.2 | 0.02 | 0.53 | 0.34 | 0.19 | 0.31 | 0.75 |
| 40 kg | 0.76 | 0.68 | 0.04 | 0.10 | 22.7 | 0.03 | 0.56 | 0.44 | 0.27 | 0.41 | 0.78 |
| 60 kg | 0.56 | 0.52 | 0.07 | 0.18 | 34.1 | 0.02 | 0.64 | 0.46 | 0.30 | 0.41 | 0.78 |
| 80 kg | 0.28 | 0.26 | 0.07 | 0.23 | 34.7 | 0.02 | 0.65 | 0.53 | 0.34 | 0.44 | 0.80 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 1.00 | 0.92 | 0.67 | 0.17 |
| long | 1.00 | 0.92 | 0.58 | 0.08 |
| sphere | 0.92 | 0.92 | 0.92 | 1.00 |
| cylinder | 0.75 | 0.50 | 0.42 | 0.25 |
| arch | 0.50 | 0.58 | 0.25 | 0.08 |
| dumbbell | 0.92 | 0.58 | 0.50 | 0.17 |
| t_shape | 0.83 | 0.75 | 0.83 | 0.25 |
| l_shape (unseen) | 1.00 | 0.83 | 0.33 | 0.33 |
| u_channel (unseen) | 1.00 | 1.00 | 0.67 | 0.33 |
| plus (unseen) | 1.00 | 0.58 | 0.42 | 0.17 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.11 | 0.21 | 0.37 | 0.40 |
| long | 0.34 | 0.31 | 0.29 | 0.31 |
| sphere | 0.13 | 0.20 | 0.22 | 0.23 |
| cylinder | 0.18 | 0.33 | 0.36 | 0.40 |
| arch | 0.03 | 0.06 | 0.14 | 0.21 |
| dumbbell | 0.12 | 0.18 | 0.16 | 0.28 |
| t_shape | 0.27 | 0.41 | 0.51 | 0.49 |
| l_shape | 0.16 | 0.35 | 0.35 | 0.42 |
| u_channel | 0.22 | 0.44 | 0.38 | 0.49 |
| plus | 0.29 | 0.20 | 0.23 | 0.20 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.90 | 0.83 | 0.67 | 0.37 |
| B_left | 0.90 | 0.80 | 0.63 | 0.43 |
| C_backright | 0.87 | 0.70 | 0.57 | 0.23 |
| D_far_turn | 0.90 | 0.70 | 0.37 | 0.10 |
