# Pair evaluation: trio-ippo-it5500-dev7100

policy: checkpoint logs/marl2/trio_ippo_s0/model_5500.pt (iteration 5500, ippo, pair anymal3)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | anymal3 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | anymal3 pushing | two or more pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.68 | 0.68 | 0.07 | 0.06 | 0.13 | 18.6 | 0.49 | 0.41 | 0.09 | 0.32 | 0.18 | 0.33 | 0.58 |
| 40 kg | 0.57 | 0.52 | 0.09 | 0.02 | 0.24 | 22.0 | 0.52 | 0.47 | 0.07 | 0.40 | 0.24 | 0.43 | 0.58 |
| 60 kg | 0.42 | 0.38 | 0.17 | 0.10 | 0.23 | 27.5 | 0.52 | 0.51 | 0.06 | 0.50 | 0.32 | 0.48 | 0.56 |
| 80 kg | 0.23 | 0.21 | 0.23 | 0.10 | 0.23 | 30.4 | 0.50 | 0.51 | 0.03 | 0.57 | 0.34 | 0.49 | 0.57 |
| 100 kg | 0.12 | 0.11 | 0.25 | 0.04 | 0.23 | 24.4 | 0.50 | 0.51 | 0.02 | 0.64 | 0.35 | 0.46 | 0.55 |
| 120 kg | 0.13 | 0.14 | 0.23 | 0.04 | 0.14 | 19.1 | 0.52 | 0.52 | 0.02 | 0.67 | 0.36 | 0.46 | 0.54 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg | 100 kg | 120 kg |
|---|---|---|---|---|---|---|
| cube | 0.67 | 0.67 | 0.50 | 0.25 | 0.08 | 0.00 |
| long | 0.75 | 0.67 | 0.50 | 0.17 | 0.08 | 0.08 |
| sphere | 0.83 | 0.83 | 0.83 | 0.92 | 0.75 | 0.92 |
| cylinder | 0.58 | 0.33 | 0.33 | 0.17 | 0.17 | 0.25 |
| arch | 0.67 | 0.33 | 0.25 | 0.00 | 0.00 | 0.00 |
| dumbbell | 0.75 | 0.50 | 0.33 | 0.00 | 0.00 | 0.00 |
| t_shape | 0.75 | 0.58 | 0.25 | 0.33 | 0.00 | 0.00 |
| l_shape (unseen) | 0.83 | 0.75 | 0.67 | 0.17 | 0.00 | 0.00 |
| u_channel (unseen) | 0.50 | 0.58 | 0.33 | 0.17 | 0.08 | 0.00 |
| plus (unseen) | 0.42 | 0.42 | 0.25 | 0.17 | 0.08 | 0.08 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg | 100 kg | 120 kg |
|---|---|---|---|---|---|---|
| cube | 0.21 | 0.33 | 0.40 | 0.52 | 0.33 | 0.48 |
| long | 0.23 | 0.33 | 0.41 | 0.46 | 0.54 | 0.53 |
| sphere | 0.24 | 0.31 | 0.39 | 0.34 | 0.28 | 0.25 |
| cylinder | 0.26 | 0.34 | 0.48 | 0.55 | 0.47 | 0.47 |
| arch | 0.03 | 0.03 | 0.03 | 0.09 | 0.09 | 0.05 |
| dumbbell | 0.17 | 0.23 | 0.20 | 0.18 | 0.25 | 0.22 |
| t_shape | 0.14 | 0.20 | 0.24 | 0.30 | 0.35 | 0.50 |
| l_shape | 0.21 | 0.27 | 0.40 | 0.45 | 0.45 | 0.34 |
| u_channel | 0.09 | 0.15 | 0.26 | 0.17 | 0.33 | 0.35 |
| plus | 0.16 | 0.24 | 0.35 | 0.36 | 0.40 | 0.43 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg | 100 kg | 120 kg |
|---|---|---|---|---|---|---|
| A_straight | 0.87 | 0.83 | 0.73 | 0.40 | 0.17 | 0.20 |
| B_left | 0.47 | 0.43 | 0.30 | 0.07 | 0.10 | 0.13 |
| C_backright | 0.73 | 0.40 | 0.33 | 0.30 | 0.10 | 0.10 |
| D_far_turn | 0.63 | 0.60 | 0.33 | 0.17 | 0.13 | 0.10 |
