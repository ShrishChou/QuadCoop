# Pair evaluation: pres-mappo

policy: checkpoint logs/marl2/nwB_mappo_uniform_s0/model_5000.pt (iteration 5000, mappo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 10 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.90 | 0.85 | 0.01 | 0.03 | 20.8 | 0.09 | 0.48 | 0.34 | 0.16 | 0.28 | 0.70 |
| 40 kg | 0.78 | 0.71 | 0.04 | 0.07 | 24.9 | 0.09 | 0.55 | 0.42 | 0.23 | 0.35 | 0.69 |
| 60 kg | 0.53 | 0.45 | 0.10 | 0.11 | 34.7 | 0.09 | 0.60 | 0.48 | 0.29 | 0.40 | 0.68 |
| 80 kg | 0.24 | 0.20 | 0.14 | 0.13 | 36.0 | 0.09 | 0.64 | 0.54 | 0.34 | 0.44 | 0.67 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 1.00 | 0.93 | 0.57 | 0.12 |
| long | 1.00 | 1.00 | 0.75 | 0.42 |
| sphere | 0.95 | 0.93 | 0.93 | 0.95 |
| cylinder | 0.65 | 0.50 | 0.35 | 0.28 |
| arch | 0.72 | 0.57 | 0.17 | 0.03 |
| dumbbell | 1.00 | 0.65 | 0.53 | 0.15 |
| t_shape | 0.97 | 0.95 | 0.78 | 0.20 |
| beam (unseen) | 0.78 | 0.53 | 0.15 | 0.00 |
| l_shape (unseen) | 0.95 | 0.95 | 0.78 | 0.28 |
| asym (unseen) | 0.93 | 0.65 | 0.33 | 0.03 |
| u_channel (unseen) | 1.00 | 0.93 | 0.57 | 0.15 |
| plus (unseen) | 0.88 | 0.80 | 0.47 | 0.28 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.14 | 0.17 | 0.11 | 0.09 |
| long | 0.29 | 0.31 | 0.33 | 0.32 |
| sphere | 0.07 | 0.14 | 0.29 | 0.34 |
| cylinder | 0.23 | 0.41 | 0.44 | 0.47 |
| arch | 0.01 | 0.01 | 0.01 | 0.01 |
| dumbbell | 0.06 | 0.14 | 0.25 | 0.23 |
| t_shape | 0.22 | 0.31 | 0.30 | 0.34 |
| beam | 0.11 | 0.23 | 0.37 | 0.48 |
| l_shape | 0.24 | 0.36 | 0.40 | 0.51 |
| asym | 0.30 | 0.35 | 0.50 | 0.63 |
| u_channel | 0.17 | 0.22 | 0.25 | 0.38 |
| plus | 0.08 | 0.15 | 0.17 | 0.28 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.94 | 0.88 | 0.68 | 0.35 |
| B_left | 0.91 | 0.80 | 0.54 | 0.25 |
| C_backright | 0.87 | 0.76 | 0.47 | 0.18 |
| D_far_turn | 0.89 | 0.69 | 0.43 | 0.17 |
