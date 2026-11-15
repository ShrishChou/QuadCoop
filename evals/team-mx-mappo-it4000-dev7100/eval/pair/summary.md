# Pair evaluation: team-mx-mappo-it4000-dev7100

policy: checkpoint logs/marl2/mappo_mx_kl_ten_s0/model_4000.pt (iteration 4000, mappo, pair mixed)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal fell | spot fell | time to success (s) | robots touching | anymal pushing | spot pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.89 | 0.84 | 0.00 | 0.06 | 21.7 | 0.02 | 0.49 | 0.32 | 0.16 | 0.28 | 0.81 |
| 40 kg | 0.75 | 0.68 | 0.03 | 0.12 | 22.9 | 0.03 | 0.58 | 0.46 | 0.29 | 0.42 | 0.79 |
| 60 kg | 0.55 | 0.49 | 0.05 | 0.18 | 31.4 | 0.03 | 0.63 | 0.51 | 0.33 | 0.45 | 0.81 |
| 80 kg | 0.28 | 0.28 | 0.06 | 0.26 | 35.2 | 0.02 | 0.63 | 0.55 | 0.36 | 0.47 | 0.84 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 1.00 | 0.92 | 0.58 | 0.25 |
| long | 1.00 | 0.67 | 0.58 | 0.33 |
| sphere | 1.00 | 0.92 | 1.00 | 1.00 |
| cylinder | 0.67 | 0.42 | 0.50 | 0.25 |
| arch | 0.67 | 0.67 | 0.17 | 0.17 |
| dumbbell | 1.00 | 0.58 | 0.58 | 0.08 |
| t_shape | 0.92 | 0.92 | 0.67 | 0.25 |
| l_shape (unseen) | 0.67 | 0.83 | 0.67 | 0.17 |
| u_channel (unseen) | 1.00 | 1.00 | 0.42 | 0.25 |
| plus (unseen) | 1.00 | 0.58 | 0.33 | 0.08 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.14 | 0.28 | 0.46 | 0.43 |
| long | 0.25 | 0.35 | 0.41 | 0.34 |
| sphere | 0.12 | 0.26 | 0.29 | 0.28 |
| cylinder | 0.15 | 0.41 | 0.40 | 0.42 |
| arch | 0.02 | 0.04 | 0.14 | 0.22 |
| dumbbell | 0.09 | 0.16 | 0.27 | 0.22 |
| t_shape | 0.28 | 0.41 | 0.43 | 0.55 |
| l_shape | 0.16 | 0.35 | 0.37 | 0.44 |
| u_channel | 0.23 | 0.41 | 0.31 | 0.42 |
| plus | 0.12 | 0.19 | 0.27 | 0.27 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.93 | 0.80 | 0.67 | 0.50 |
| B_left | 0.93 | 0.73 | 0.63 | 0.37 |
| C_backright | 0.90 | 0.77 | 0.57 | 0.17 |
| D_far_turn | 0.80 | 0.70 | 0.33 | 0.10 |
