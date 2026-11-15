# Pair evaluation: team-mx-ippo-it4000-dev7100-r2

policy: checkpoint logs/marl2/ippo_mx_kl_ten_s0/model_4000.pt (iteration 4000, ippo, pair mixed)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal fell | spot fell | time to success (s) | robots touching | anymal pushing | spot pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.89 | 0.85 | 0.00 | 0.07 | 18.0 | 0.02 | 0.52 | 0.34 | 0.18 | 0.31 | 0.78 |
| 40 kg | 0.78 | 0.72 | 0.03 | 0.10 | 22.6 | 0.03 | 0.58 | 0.43 | 0.26 | 0.39 | 0.75 |
| 60 kg | 0.51 | 0.46 | 0.06 | 0.23 | 30.8 | 0.02 | 0.63 | 0.48 | 0.31 | 0.41 | 0.80 |
| 80 kg | 0.28 | 0.28 | 0.07 | 0.30 | 34.3 | 0.03 | 0.65 | 0.54 | 0.36 | 0.47 | 0.81 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 1.00 | 0.83 | 0.50 | 0.17 |
| long | 1.00 | 0.83 | 0.75 | 0.25 |
| sphere | 0.92 | 0.92 | 1.00 | 1.00 |
| cylinder | 0.75 | 0.58 | 0.33 | 0.25 |
| arch | 0.58 | 0.33 | 0.33 | 0.08 |
| dumbbell | 1.00 | 0.67 | 0.50 | 0.08 |
| t_shape | 0.92 | 0.92 | 0.42 | 0.25 |
| l_shape (unseen) | 0.92 | 0.83 | 0.42 | 0.17 |
| u_channel (unseen) | 0.83 | 1.00 | 0.67 | 0.25 |
| plus (unseen) | 1.00 | 0.92 | 0.17 | 0.25 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.11 | 0.20 | 0.40 | 0.42 |
| long | 0.30 | 0.30 | 0.23 | 0.39 |
| sphere | 0.11 | 0.19 | 0.19 | 0.19 |
| cylinder | 0.17 | 0.30 | 0.30 | 0.44 |
| arch | 0.04 | 0.04 | 0.12 | 0.25 |
| dumbbell | 0.11 | 0.21 | 0.22 | 0.23 |
| t_shape | 0.26 | 0.37 | 0.56 | 0.49 |
| l_shape | 0.16 | 0.31 | 0.39 | 0.50 |
| u_channel | 0.25 | 0.42 | 0.38 | 0.45 |
| plus | 0.27 | 0.25 | 0.25 | 0.26 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.93 | 0.87 | 0.77 | 0.43 |
| B_left | 0.93 | 0.77 | 0.47 | 0.33 |
| C_backright | 0.90 | 0.80 | 0.50 | 0.23 |
| D_far_turn | 0.80 | 0.70 | 0.30 | 0.10 |
