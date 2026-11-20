# Pair evaluation: trio-mappo-it5600-dev7100

policy: checkpoint logs/marl2/trio_mappo_s0/model_5600.pt (iteration 5600, mappo, pair anymal3)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | anymal3 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | anymal3 pushing | two or more pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.67 | 0.64 | 0.08 | 0.05 | 0.19 | 17.9 | 0.63 | 0.31 | 0.21 | 0.34 | 0.21 | 0.41 | 0.65 |
| 40 kg | 0.61 | 0.56 | 0.12 | 0.07 | 0.14 | 21.0 | 0.71 | 0.34 | 0.27 | 0.41 | 0.29 | 0.49 | 0.64 |
| 60 kg | 0.47 | 0.46 | 0.16 | 0.14 | 0.14 | 26.3 | 0.73 | 0.33 | 0.29 | 0.46 | 0.30 | 0.48 | 0.64 |
| 80 kg | 0.35 | 0.30 | 0.21 | 0.16 | 0.17 | 26.6 | 0.75 | 0.35 | 0.35 | 0.53 | 0.37 | 0.53 | 0.63 |
| 100 kg | 0.26 | 0.24 | 0.21 | 0.22 | 0.14 | 33.2 | 0.77 | 0.38 | 0.37 | 0.52 | 0.37 | 0.52 | 0.63 |
| 120 kg | 0.13 | 0.11 | 0.28 | 0.23 | 0.16 | 32.3 | 0.75 | 0.36 | 0.39 | 0.55 | 0.40 | 0.55 | 0.63 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg | 100 kg | 120 kg |
|---|---|---|---|---|---|---|
| cube | 0.83 | 0.58 | 0.33 | 0.25 | 0.00 | 0.00 |
| long | 0.83 | 0.75 | 0.50 | 0.08 | 0.00 | 0.08 |
| sphere | 0.58 | 0.67 | 0.67 | 0.83 | 0.75 | 0.50 |
| cylinder | 0.58 | 0.50 | 0.17 | 0.17 | 0.17 | 0.08 |
| arch | 0.42 | 0.17 | 0.08 | 0.00 | 0.00 | 0.00 |
| dumbbell | 0.58 | 0.42 | 0.33 | 0.17 | 0.25 | 0.25 |
| t_shape | 0.75 | 0.83 | 0.75 | 0.58 | 0.58 | 0.17 |
| l_shape (unseen) | 0.75 | 0.83 | 0.67 | 0.75 | 0.50 | 0.08 |
| u_channel (unseen) | 0.67 | 0.67 | 0.67 | 0.42 | 0.17 | 0.17 |
| plus (unseen) | 0.67 | 0.67 | 0.50 | 0.25 | 0.17 | 0.00 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg | 100 kg | 120 kg |
|---|---|---|---|---|---|---|
| cube | 0.20 | 0.18 | 0.24 | 0.21 | 0.31 | 0.29 |
| long | 0.27 | 0.38 | 0.28 | 0.39 | 0.51 | 0.48 |
| sphere | 0.14 | 0.16 | 0.21 | 0.20 | 0.19 | 0.19 |
| cylinder | 0.36 | 0.40 | 0.36 | 0.53 | 0.56 | 0.58 |
| arch | 0.02 | 0.00 | 0.01 | 0.03 | 0.02 | 0.02 |
| dumbbell | 0.14 | 0.35 | 0.32 | 0.36 | 0.39 | 0.40 |
| t_shape | 0.34 | 0.36 | 0.32 | 0.49 | 0.40 | 0.49 |
| l_shape | 0.25 | 0.38 | 0.51 | 0.49 | 0.55 | 0.54 |
| u_channel | 0.21 | 0.28 | 0.41 | 0.52 | 0.40 | 0.47 |
| plus | 0.21 | 0.36 | 0.38 | 0.48 | 0.42 | 0.54 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg | 100 kg | 120 kg |
|---|---|---|---|---|---|---|
| A_straight | 0.73 | 0.70 | 0.53 | 0.50 | 0.47 | 0.23 |
| B_left | 0.57 | 0.53 | 0.47 | 0.23 | 0.20 | 0.07 |
| C_backright | 0.73 | 0.63 | 0.43 | 0.33 | 0.20 | 0.17 |
| D_far_turn | 0.63 | 0.57 | 0.43 | 0.33 | 0.17 | 0.07 |
