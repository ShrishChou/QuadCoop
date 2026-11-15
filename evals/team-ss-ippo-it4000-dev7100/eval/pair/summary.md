# Pair evaluation: team-ss-ippo-it4000-dev7100

policy: checkpoint logs/marl2/ippo_ss_kl_ten_s0/model_4000.pt (iteration 4000, ippo, pair spot)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | spot1 fell | spot2 fell | time to success (s) | robots touching | spot1 pushing | spot2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.93 | 0.82 | 0.02 | 0.03 | 19.4 | 0.00 | 0.46 | 0.49 | 0.20 | 0.31 | 0.82 |
| 40 kg | 0.73 | 0.66 | 0.07 | 0.10 | 22.7 | 0.01 | 0.53 | 0.57 | 0.28 | 0.38 | 0.82 |
| 60 kg | 0.43 | 0.43 | 0.17 | 0.13 | 28.6 | 0.01 | 0.59 | 0.53 | 0.29 | 0.38 | 0.83 |
| 80 kg | 0.28 | 0.24 | 0.21 | 0.17 | 31.8 | 0.01 | 0.66 | 0.57 | 0.36 | 0.46 | 0.85 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.92 | 0.92 | 0.75 | 0.42 |
| long | 0.92 | 0.92 | 0.67 | 0.25 |
| sphere | 1.00 | 1.00 | 0.92 | 1.00 |
| cylinder | 1.00 | 0.75 | 0.33 | 0.25 |
| arch | 0.75 | 0.33 | 0.08 | 0.00 |
| dumbbell | 0.92 | 0.67 | 0.42 | 0.17 |
| t_shape | 1.00 | 0.75 | 0.42 | 0.33 |
| l_shape (unseen) | 0.92 | 0.50 | 0.25 | 0.08 |
| u_channel (unseen) | 0.83 | 0.92 | 0.33 | 0.25 |
| plus (unseen) | 1.00 | 0.58 | 0.17 | 0.08 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.17 | 0.24 | 0.17 | 0.30 |
| long | 0.28 | 0.45 | 0.46 | 0.49 |
| sphere | 0.13 | 0.15 | 0.23 | 0.27 |
| cylinder | 0.22 | 0.33 | 0.36 | 0.39 |
| arch | 0.12 | 0.18 | 0.13 | 0.32 |
| dumbbell | 0.14 | 0.23 | 0.29 | 0.31 |
| t_shape | 0.23 | 0.30 | 0.36 | 0.50 |
| l_shape | 0.26 | 0.40 | 0.28 | 0.33 |
| u_channel | 0.22 | 0.41 | 0.42 | 0.52 |
| plus | 0.20 | 0.15 | 0.20 | 0.22 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 1.00 | 0.77 | 0.60 | 0.47 |
| B_left | 0.87 | 0.77 | 0.47 | 0.33 |
| C_backright | 0.87 | 0.73 | 0.30 | 0.23 |
| D_far_turn | 0.97 | 0.67 | 0.37 | 0.10 |
