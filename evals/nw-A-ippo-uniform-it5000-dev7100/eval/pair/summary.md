# Pair evaluation: nw-A-ippo-uniform-it5000-dev7100

policy: checkpoint logs/marl2/nwA_ippo_uniform_s0/model_5000.pt (iteration 5000, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.94 | 0.88 | 0.00 | 0.01 | 20.2 | 0.11 | 0.49 | 0.36 | 0.18 | 0.32 | 0.65 |
| 40 kg | 0.82 | 0.75 | 0.03 | 0.03 | 21.8 | 0.12 | 0.54 | 0.41 | 0.21 | 0.33 | 0.66 |
| 60 kg | 0.56 | 0.50 | 0.07 | 0.14 | 34.1 | 0.09 | 0.59 | 0.44 | 0.25 | 0.35 | 0.66 |
| 80 kg | 0.30 | 0.27 | 0.10 | 0.11 | 37.1 | 0.10 | 0.62 | 0.49 | 0.29 | 0.39 | 0.64 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 1.00 | 0.92 | 0.50 | 0.08 |
| long | 1.00 | 0.92 | 0.58 | 0.42 |
| sphere | 1.00 | 0.92 | 1.00 | 0.83 |
| cylinder | 0.75 | 0.67 | 0.25 | 0.25 |
| arch | 0.75 | 0.33 | 0.08 | 0.00 |
| dumbbell | 1.00 | 0.83 | 0.58 | 0.17 |
| t_shape | 1.00 | 1.00 | 0.58 | 0.17 |
| l_shape (unseen) | 1.00 | 1.00 | 0.67 | 0.33 |
| u_channel (unseen) | 1.00 | 1.00 | 0.83 | 0.42 |
| plus (unseen) | 0.92 | 0.67 | 0.50 | 0.33 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.25 | 0.24 | 0.13 | 0.09 |
| long | 0.34 | 0.30 | 0.36 | 0.37 |
| sphere | 0.13 | 0.27 | 0.33 | 0.30 |
| cylinder | 0.24 | 0.28 | 0.47 | 0.37 |
| arch | 0.01 | 0.01 | 0.00 | 0.00 |
| dumbbell | 0.04 | 0.11 | 0.19 | 0.19 |
| t_shape | 0.27 | 0.25 | 0.23 | 0.40 |
| l_shape | 0.27 | 0.31 | 0.25 | 0.41 |
| u_channel | 0.18 | 0.19 | 0.23 | 0.41 |
| plus | 0.10 | 0.18 | 0.25 | 0.32 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.97 | 0.87 | 0.80 | 0.53 |
| B_left | 0.93 | 0.90 | 0.57 | 0.43 |
| C_backright | 1.00 | 0.77 | 0.43 | 0.17 |
| D_far_turn | 0.87 | 0.77 | 0.43 | 0.07 |
