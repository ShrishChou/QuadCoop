# Pair evaluation: pair-frozen-anymal

policy: frozen pair (anymal): s2b-anymal-term80 + s2b-anymal-term80

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching |
|---|---|---|---|---|---|---|
| 20 kg | 0.65 | 0.64 | 0.10 | 0.15 | 19.4 | 0.48 |
| 40 kg | 0.53 | 0.50 | 0.13 | 0.25 | 24.6 | 0.51 |
| 60 kg | 0.38 | 0.34 | 0.18 | 0.28 | 29.8 | 0.53 |
| 80 kg | 0.19 | 0.18 | 0.26 | 0.24 | 30.8 | 0.53 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.75 | 0.58 | 0.67 | 0.33 |
| long | 0.92 | 0.83 | 0.50 | 0.25 |
| sphere | 0.83 | 0.75 | 0.92 | 0.92 |
| cylinder | 0.17 | 0.25 | 0.17 | 0.25 |
| arch | 0.42 | 0.25 | 0.08 | 0.00 |
| dumbbell | 0.83 | 0.58 | 0.58 | 0.08 |
| t_shape | 0.83 | 0.75 | 0.25 | 0.08 |
| beam (unseen) | 0.58 | 0.33 | 0.08 | 0.00 |
| l_shape (unseen) | 0.75 | 0.83 | 0.58 | 0.08 |
| asym (unseen) | 0.58 | 0.58 | 0.08 | 0.00 |
| u_channel (unseen) | 0.75 | 0.42 | 0.33 | 0.17 |
| plus (unseen) | 0.33 | 0.25 | 0.33 | 0.17 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.72 | 0.69 | 0.58 | 0.33 |
| B_left | 0.64 | 0.36 | 0.31 | 0.14 |
| C_backright | 0.58 | 0.67 | 0.44 | 0.19 |
| D_far_turn | 0.64 | 0.42 | 0.19 | 0.11 |
