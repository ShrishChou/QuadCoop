# Pair evaluation: team-ss-ippo-it4000-dev7100-r2

policy: checkpoint logs/marl2/ippo_ss_kl_ten_s0/model_4000.pt (iteration 4000, ippo, pair spot)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | spot1 fell | spot2 fell | time to success (s) | robots touching | spot1 pushing | spot2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.85 | 0.82 | 0.03 | 0.04 | 20.0 | 0.00 | 0.43 | 0.50 | 0.20 | 0.32 | 0.82 |
| 40 kg | 0.75 | 0.71 | 0.07 | 0.06 | 21.5 | 0.01 | 0.52 | 0.59 | 0.30 | 0.41 | 0.81 |
| 60 kg | 0.47 | 0.42 | 0.17 | 0.18 | 28.0 | 0.01 | 0.59 | 0.55 | 0.30 | 0.38 | 0.82 |
| 80 kg | 0.24 | 0.23 | 0.22 | 0.24 | 29.3 | 0.01 | 0.64 | 0.60 | 0.38 | 0.49 | 0.85 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.75 | 1.00 | 0.42 | 0.25 |
| long | 1.00 | 0.83 | 0.75 | 0.17 |
| sphere | 1.00 | 1.00 | 0.92 | 1.00 |
| cylinder | 0.92 | 0.75 | 0.33 | 0.25 |
| arch | 0.42 | 0.17 | 0.25 | 0.00 |
| dumbbell | 0.67 | 0.83 | 0.42 | 0.08 |
| t_shape | 1.00 | 0.83 | 0.67 | 0.25 |
| l_shape (unseen) | 0.83 | 0.42 | 0.17 | 0.17 |
| u_channel (unseen) | 0.92 | 0.92 | 0.50 | 0.25 |
| plus (unseen) | 1.00 | 0.75 | 0.25 | 0.00 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.15 | 0.24 | 0.25 | 0.41 |
| long | 0.28 | 0.34 | 0.48 | 0.55 |
| sphere | 0.10 | 0.21 | 0.25 | 0.26 |
| cylinder | 0.22 | 0.35 | 0.36 | 0.40 |
| arch | 0.13 | 0.29 | 0.15 | 0.30 |
| dumbbell | 0.16 | 0.22 | 0.27 | 0.36 |
| t_shape | 0.28 | 0.34 | 0.41 | 0.50 |
| l_shape | 0.23 | 0.48 | 0.22 | 0.35 |
| u_channel | 0.21 | 0.37 | 0.42 | 0.52 |
| plus | 0.21 | 0.14 | 0.20 | 0.18 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.93 | 0.90 | 0.63 | 0.37 |
| B_left | 0.73 | 0.77 | 0.50 | 0.33 |
| C_backright | 0.90 | 0.63 | 0.43 | 0.17 |
| D_far_turn | 0.83 | 0.70 | 0.30 | 0.10 |
