# Pair evaluation: team-ss-mappo-it4000-dev7100

policy: checkpoint logs/marl2/mappo_ss_kl_ten_s0/model_4000.pt (iteration 4000, mappo, pair spot)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | spot1 fell | spot2 fell | time to success (s) | robots touching | spot1 pushing | spot2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.79 | 0.72 | 0.07 | 0.05 | 22.6 | 0.00 | 0.43 | 0.47 | 0.18 | 0.29 | 0.81 |
| 40 kg | 0.73 | 0.64 | 0.12 | 0.09 | 25.6 | 0.01 | 0.57 | 0.55 | 0.31 | 0.42 | 0.78 |
| 60 kg | 0.49 | 0.43 | 0.17 | 0.17 | 32.5 | 0.01 | 0.64 | 0.56 | 0.35 | 0.45 | 0.84 |
| 80 kg | 0.22 | 0.19 | 0.23 | 0.24 | 24.3 | 0.01 | 0.65 | 0.61 | 0.40 | 0.49 | 0.86 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.67 | 0.75 | 0.58 | 0.17 |
| long | 1.00 | 0.83 | 0.33 | 0.08 |
| sphere | 1.00 | 1.00 | 1.00 | 1.00 |
| cylinder | 1.00 | 0.67 | 0.58 | 0.25 |
| arch | 0.25 | 0.42 | 0.17 | 0.08 |
| dumbbell | 0.83 | 0.92 | 0.58 | 0.08 |
| t_shape | 0.83 | 0.83 | 0.50 | 0.00 |
| l_shape (unseen) | 0.67 | 0.50 | 0.25 | 0.17 |
| u_channel (unseen) | 0.83 | 0.83 | 0.67 | 0.25 |
| plus (unseen) | 0.83 | 0.58 | 0.25 | 0.08 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.18 | 0.36 | 0.36 | 0.49 |
| long | 0.35 | 0.41 | 0.43 | 0.49 |
| sphere | 0.19 | 0.21 | 0.30 | 0.30 |
| cylinder | 0.19 | 0.32 | 0.29 | 0.37 |
| arch | 0.09 | 0.04 | 0.13 | 0.12 |
| dumbbell | 0.09 | 0.20 | 0.32 | 0.30 |
| t_shape | 0.21 | 0.41 | 0.53 | 0.62 |
| l_shape | 0.22 | 0.42 | 0.43 | 0.37 |
| u_channel | 0.16 | 0.53 | 0.48 | 0.60 |
| plus | 0.12 | 0.20 | 0.20 | 0.30 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.87 | 0.87 | 0.67 | 0.33 |
| B_left | 0.70 | 0.67 | 0.53 | 0.33 |
| C_backright | 0.77 | 0.60 | 0.43 | 0.10 |
| D_far_turn | 0.83 | 0.80 | 0.33 | 0.10 |
