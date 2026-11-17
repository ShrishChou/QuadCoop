# Pair evaluation: trio-transfer-ippo

policy: checkpoint logs/marl2/ippo_aa_kl_ten_s0/model_4000.pt (iteration 4000, ippo, pair anymal), run as a team of three (anymal3 uses anymal1's actor)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | anymal3 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | anymal3 pushing | two or more pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.57 | 0.56 | 0.13 | 0.04 | 0.21 | 19.6 | 0.66 | 0.36 | 0.15 | 0.37 | 0.22 | 0.42 | 0.61 |
| 40 kg | 0.48 | 0.44 | 0.13 | 0.12 | 0.19 | 24.0 | 0.71 | 0.41 | 0.23 | 0.42 | 0.29 | 0.47 | 0.63 |
| 60 kg | 0.41 | 0.37 | 0.19 | 0.12 | 0.23 | 25.6 | 0.72 | 0.42 | 0.24 | 0.50 | 0.35 | 0.53 | 0.60 |
| 80 kg | 0.21 | 0.19 | 0.24 | 0.12 | 0.23 | 33.2 | 0.73 | 0.40 | 0.27 | 0.51 | 0.35 | 0.51 | 0.59 |
| 100 kg | 0.12 | 0.09 | 0.26 | 0.19 | 0.17 | 24.3 | 0.74 | 0.38 | 0.34 | 0.50 | 0.37 | 0.53 | 0.56 |
| 120 kg | 0.07 | 0.07 | 0.30 | 0.23 | 0.16 | 21.8 | 0.74 | 0.38 | 0.30 | 0.54 | 0.37 | 0.51 | 0.59 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg | 100 kg | 120 kg |
|---|---|---|---|---|---|---|
| cube | 0.67 | 0.75 | 0.33 | 0.33 | 0.00 | 0.00 |
| long | 0.50 | 0.58 | 0.50 | 0.25 | 0.08 | 0.08 |
| sphere | 0.67 | 0.58 | 0.58 | 0.50 | 0.58 | 0.42 |
| cylinder | 0.25 | 0.50 | 0.08 | 0.00 | 0.17 | 0.08 |
| arch | 0.17 | 0.17 | 0.08 | 0.00 | 0.00 | 0.00 |
| dumbbell | 0.50 | 0.67 | 0.42 | 0.25 | 0.08 | 0.08 |
| t_shape | 0.83 | 0.42 | 0.50 | 0.17 | 0.08 | 0.08 |
| l_shape (unseen) | 0.83 | 0.58 | 0.50 | 0.08 | 0.00 | 0.00 |
| u_channel (unseen) | 0.75 | 0.17 | 0.42 | 0.08 | 0.08 | 0.00 |
| plus (unseen) | 0.50 | 0.42 | 0.67 | 0.42 | 0.08 | 0.00 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg | 100 kg | 120 kg |
|---|---|---|---|---|---|---|
| cube | 0.17 | 0.26 | 0.26 | 0.33 | 0.23 | 0.25 |
| long | 0.30 | 0.29 | 0.31 | 0.45 | 0.54 | 0.52 |
| sphere | 0.19 | 0.28 | 0.43 | 0.46 | 0.47 | 0.47 |
| cylinder | 0.30 | 0.37 | 0.42 | 0.45 | 0.50 | 0.35 |
| arch | 0.03 | 0.05 | 0.04 | 0.06 | 0.04 | 0.07 |
| dumbbell | 0.21 | 0.29 | 0.36 | 0.33 | 0.34 | 0.32 |
| t_shape | 0.32 | 0.40 | 0.39 | 0.35 | 0.41 | 0.40 |
| l_shape | 0.26 | 0.37 | 0.46 | 0.35 | 0.42 | 0.44 |
| u_channel | 0.25 | 0.21 | 0.35 | 0.18 | 0.28 | 0.31 |
| plus | 0.21 | 0.38 | 0.51 | 0.50 | 0.43 | 0.53 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg | 100 kg | 120 kg |
|---|---|---|---|---|---|---|
| A_straight | 0.67 | 0.50 | 0.47 | 0.20 | 0.30 | 0.13 |
| B_left | 0.63 | 0.47 | 0.40 | 0.17 | 0.03 | 0.00 |
| C_backright | 0.40 | 0.57 | 0.33 | 0.20 | 0.10 | 0.10 |
| D_far_turn | 0.57 | 0.40 | 0.43 | 0.27 | 0.03 | 0.07 |
