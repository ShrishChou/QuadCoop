# Pair evaluation: pair-frozen-anymal

policy: frozen pair (anymal): s2b-anymal-term80 + s2b-anymal-term80

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.65 | 0.64 | 0.09 | 0.15 | 19.3 | 0.48 | 0.41 | 0.34 | 0.16 | 0.31 | 0.51 |
| 40 kg | 0.51 | 0.42 | 0.22 | 0.21 | 24.9 | 0.49 | 0.51 | 0.44 | 0.25 | 0.41 | 0.51 |
| 60 kg | 0.40 | 0.35 | 0.25 | 0.15 | 31.2 | 0.55 | 0.48 | 0.48 | 0.27 | 0.43 | 0.48 |
| 80 kg | 0.18 | 0.17 | 0.23 | 0.26 | 33.7 | 0.53 | 0.50 | 0.55 | 0.30 | 0.42 | 0.50 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 1.00 | 0.42 | 0.42 | 0.33 |
| long | 0.83 | 0.83 | 0.50 | 0.00 |
| sphere | 0.92 | 0.67 | 1.00 | 0.92 |
| cylinder | 0.25 | 0.17 | 0.33 | 0.08 |
| arch | 0.42 | 0.33 | 0.17 | 0.08 |
| dumbbell | 0.75 | 0.58 | 0.50 | 0.25 |
| t_shape | 1.00 | 0.67 | 0.33 | 0.08 |
| beam (unseen) | 0.25 | 0.42 | 0.00 | 0.00 |
| l_shape (unseen) | 0.83 | 0.67 | 0.67 | 0.17 |
| asym (unseen) | 0.83 | 0.42 | 0.17 | 0.00 |
| u_channel (unseen) | 0.58 | 0.58 | 0.33 | 0.08 |
| plus (unseen) | 0.17 | 0.33 | 0.33 | 0.17 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.24 | 0.26 | 0.37 | 0.32 |
| long | 0.32 | 0.46 | 0.40 | 0.39 |
| sphere | 0.12 | 0.12 | 0.14 | 0.12 |
| cylinder | 0.17 | 0.27 | 0.28 | 0.36 |
| arch | 0.05 | 0.02 | 0.02 | 0.06 |
| dumbbell | 0.12 | 0.19 | 0.18 | 0.28 |
| t_shape | 0.17 | 0.34 | 0.35 | 0.29 |
| beam | 0.14 | 0.40 | 0.37 | 0.50 |
| l_shape | 0.08 | 0.22 | 0.29 | 0.34 |
| asym | 0.45 | 0.57 | 0.64 | 0.65 |
| u_channel | 0.07 | 0.12 | 0.15 | 0.13 |
| plus | 0.04 | 0.06 | 0.05 | 0.11 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.81 | 0.69 | 0.53 | 0.31 |
| B_left | 0.53 | 0.42 | 0.39 | 0.11 |
| C_backright | 0.56 | 0.53 | 0.42 | 0.19 |
| D_far_turn | 0.72 | 0.39 | 0.25 | 0.11 |
