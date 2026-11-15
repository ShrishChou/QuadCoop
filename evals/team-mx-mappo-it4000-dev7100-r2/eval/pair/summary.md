# Pair evaluation: team-mx-mappo-it4000-dev7100-r2

policy: checkpoint logs/marl2/mappo_mx_kl_ten_s0/model_4000.pt (iteration 4000, mappo, pair mixed)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal fell | spot fell | time to success (s) | robots touching | anymal pushing | spot pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.89 | 0.85 | 0.01 | 0.04 | 21.0 | 0.02 | 0.49 | 0.32 | 0.15 | 0.28 | 0.76 |
| 40 kg | 0.79 | 0.71 | 0.01 | 0.10 | 24.0 | 0.02 | 0.55 | 0.44 | 0.26 | 0.41 | 0.78 |
| 60 kg | 0.57 | 0.47 | 0.03 | 0.17 | 33.5 | 0.02 | 0.58 | 0.50 | 0.30 | 0.41 | 0.78 |
| 80 kg | 0.24 | 0.23 | 0.08 | 0.28 | 33.6 | 0.02 | 0.65 | 0.56 | 0.37 | 0.47 | 0.79 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 1.00 | 0.83 | 0.67 | 0.08 |
| long | 1.00 | 0.75 | 0.67 | 0.33 |
| sphere | 0.92 | 1.00 | 1.00 | 1.00 |
| cylinder | 0.75 | 0.50 | 0.42 | 0.25 |
| arch | 0.42 | 0.42 | 0.00 | 0.08 |
| dumbbell | 1.00 | 0.75 | 0.42 | 0.00 |
| t_shape | 1.00 | 1.00 | 0.67 | 0.25 |
| l_shape (unseen) | 0.83 | 0.83 | 0.50 | 0.17 |
| u_channel (unseen) | 1.00 | 1.00 | 0.83 | 0.17 |
| plus (unseen) | 1.00 | 0.83 | 0.50 | 0.08 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.10 | 0.23 | 0.41 | 0.54 |
| long | 0.28 | 0.28 | 0.38 | 0.41 |
| sphere | 0.14 | 0.24 | 0.24 | 0.24 |
| cylinder | 0.18 | 0.33 | 0.36 | 0.40 |
| arch | 0.02 | 0.04 | 0.10 | 0.25 |
| dumbbell | 0.11 | 0.18 | 0.18 | 0.28 |
| t_shape | 0.22 | 0.42 | 0.48 | 0.53 |
| l_shape | 0.14 | 0.26 | 0.34 | 0.38 |
| u_channel | 0.19 | 0.43 | 0.30 | 0.43 |
| plus | 0.14 | 0.25 | 0.19 | 0.28 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.93 | 0.80 | 0.77 | 0.40 |
| B_left | 0.97 | 0.77 | 0.60 | 0.23 |
| C_backright | 0.83 | 0.83 | 0.53 | 0.23 |
| D_far_turn | 0.83 | 0.77 | 0.37 | 0.10 |
