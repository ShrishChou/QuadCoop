# Pair evaluation: trio-transfer-mappo

policy: checkpoint logs/marl2/mappo_aa_kl_ten_s0/model_4000.pt (iteration 4000, mappo, pair anymal), run as a team of three (anymal3 uses anymal1's actor)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | anymal3 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | anymal3 pushing | two or more pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.62 | 0.58 | 0.12 | 0.09 | 0.12 | 20.4 | 0.65 | 0.37 | 0.18 | 0.31 | 0.20 | 0.36 | 0.63 |
| 40 kg | 0.61 | 0.57 | 0.13 | 0.08 | 0.12 | 22.0 | 0.71 | 0.39 | 0.25 | 0.38 | 0.29 | 0.50 | 0.65 |
| 60 kg | 0.42 | 0.39 | 0.18 | 0.13 | 0.20 | 22.8 | 0.72 | 0.38 | 0.30 | 0.46 | 0.35 | 0.55 | 0.63 |
| 80 kg | 0.35 | 0.31 | 0.20 | 0.14 | 0.12 | 25.7 | 0.76 | 0.40 | 0.36 | 0.51 | 0.40 | 0.58 | 0.64 |
| 100 kg | 0.19 | 0.17 | 0.18 | 0.17 | 0.16 | 27.4 | 0.77 | 0.45 | 0.38 | 0.52 | 0.43 | 0.58 | 0.64 |
| 120 kg | 0.14 | 0.14 | 0.26 | 0.18 | 0.11 | 16.7 | 0.76 | 0.44 | 0.39 | 0.54 | 0.45 | 0.60 | 0.63 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg | 100 kg | 120 kg |
|---|---|---|---|---|---|---|
| cube | 0.58 | 0.83 | 0.33 | 0.08 | 0.00 | 0.00 |
| long | 0.75 | 0.75 | 0.33 | 0.25 | 0.00 | 0.00 |
| sphere | 0.67 | 0.67 | 0.67 | 1.00 | 0.83 | 1.00 |
| cylinder | 0.58 | 0.25 | 0.17 | 0.17 | 0.08 | 0.08 |
| arch | 0.33 | 0.50 | 0.00 | 0.00 | 0.00 | 0.00 |
| dumbbell | 0.42 | 0.58 | 0.17 | 0.17 | 0.17 | 0.25 |
| t_shape | 0.83 | 0.50 | 0.67 | 0.50 | 0.17 | 0.08 |
| l_shape (unseen) | 0.83 | 0.92 | 0.67 | 0.50 | 0.17 | 0.00 |
| u_channel (unseen) | 0.67 | 0.42 | 0.50 | 0.50 | 0.33 | 0.00 |
| plus (unseen) | 0.50 | 0.67 | 0.67 | 0.33 | 0.17 | 0.00 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg | 100 kg | 120 kg |
|---|---|---|---|---|---|---|
| cube | 0.15 | 0.20 | 0.17 | 0.26 | 0.30 | 0.35 |
| long | 0.27 | 0.22 | 0.38 | 0.35 | 0.48 | 0.54 |
| sphere | 0.19 | 0.33 | 0.42 | 0.52 | 0.53 | 0.57 |
| cylinder | 0.26 | 0.34 | 0.35 | 0.49 | 0.41 | 0.54 |
| arch | 0.03 | 0.01 | 0.03 | 0.01 | 0.01 | 0.01 |
| dumbbell | 0.17 | 0.24 | 0.37 | 0.33 | 0.42 | 0.36 |
| t_shape | 0.21 | 0.38 | 0.39 | 0.41 | 0.49 | 0.54 |
| l_shape | 0.29 | 0.44 | 0.47 | 0.57 | 0.56 | 0.56 |
| u_channel | 0.24 | 0.36 | 0.44 | 0.55 | 0.55 | 0.53 |
| plus | 0.16 | 0.39 | 0.46 | 0.53 | 0.58 | 0.52 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg | 100 kg | 120 kg |
|---|---|---|---|---|---|---|
| A_straight | 0.73 | 0.77 | 0.63 | 0.60 | 0.40 | 0.27 |
| B_left | 0.60 | 0.50 | 0.43 | 0.27 | 0.10 | 0.10 |
| C_backright | 0.53 | 0.60 | 0.30 | 0.23 | 0.10 | 0.10 |
| D_far_turn | 0.60 | 0.57 | 0.30 | 0.30 | 0.17 | 0.10 |
