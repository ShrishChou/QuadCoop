# Pair evaluation: pres-mappo-B-it5000

policy: checkpoint logs/marl2/nwB_mappo_uniform_s0/model_5000.pt (iteration 5000, mappo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.88 | 0.84 | 0.03 | 0.02 | 19.1 | 0.09 | 0.51 | 0.31 | 0.17 | 0.29 | 0.67 |
| 40 kg | 0.81 | 0.76 | 0.04 | 0.06 | 21.5 | 0.09 | 0.55 | 0.40 | 0.23 | 0.35 | 0.66 |
| 60 kg | 0.66 | 0.55 | 0.07 | 0.11 | 34.5 | 0.09 | 0.59 | 0.45 | 0.24 | 0.33 | 0.66 |
| 80 kg | 0.24 | 0.18 | 0.14 | 0.10 | 31.2 | 0.10 | 0.60 | 0.49 | 0.29 | 0.39 | 0.65 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 1.00 | 1.00 | 0.50 | 0.00 |
| long | 1.00 | 1.00 | 0.83 | 0.25 |
| sphere | 0.92 | 1.00 | 0.92 | 0.92 |
| cylinder | 0.75 | 0.42 | 0.25 | 0.33 |
| arch | 0.58 | 0.33 | 0.25 | 0.00 |
| dumbbell | 0.83 | 0.75 | 0.58 | 0.17 |
| t_shape | 1.00 | 1.00 | 0.92 | 0.25 |
| l_shape (unseen) | 0.92 | 1.00 | 0.75 | 0.25 |
| u_channel (unseen) | 1.00 | 1.00 | 0.92 | 0.25 |
| plus (unseen) | 0.83 | 0.58 | 0.67 | 0.00 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.09 | 0.21 | 0.10 | 0.15 |
| long | 0.37 | 0.36 | 0.30 | 0.36 |
| sphere | 0.03 | 0.08 | 0.21 | 0.26 |
| cylinder | 0.28 | 0.39 | 0.35 | 0.39 |
| arch | 0.01 | 0.01 | 0.01 | 0.00 |
| dumbbell | 0.05 | 0.13 | 0.20 | 0.12 |
| t_shape | 0.32 | 0.35 | 0.25 | 0.39 |
| l_shape | 0.21 | 0.33 | 0.42 | 0.47 |
| u_channel | 0.19 | 0.26 | 0.24 | 0.39 |
| plus | 0.11 | 0.20 | 0.30 | 0.33 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.90 | 0.83 | 0.90 | 0.43 |
| B_left | 0.93 | 0.80 | 0.70 | 0.27 |
| C_backright | 0.93 | 0.80 | 0.57 | 0.17 |
| D_far_turn | 0.77 | 0.80 | 0.47 | 0.10 |
