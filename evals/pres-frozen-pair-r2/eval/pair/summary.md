# Pair evaluation: pres-frozen-pair-r2

policy: frozen pair (anymal): s2b-anymal-term80 + s2b-anymal-term80

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.69 | 0.62 | 0.12 | 0.14 | 18.8 | 0.51 | 0.37 | 0.36 | 0.14 | 0.27 | 0.48 |
| 40 kg | 0.57 | 0.48 | 0.17 | 0.12 | 20.8 | 0.55 | 0.42 | 0.41 | 0.20 | 0.37 | 0.48 |
| 60 kg | 0.41 | 0.38 | 0.26 | 0.15 | 29.0 | 0.52 | 0.44 | 0.49 | 0.23 | 0.37 | 0.49 |
| 80 kg | 0.20 | 0.17 | 0.28 | 0.23 | 26.3 | 0.56 | 0.51 | 0.47 | 0.25 | 0.38 | 0.48 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 1.00 | 0.67 | 0.50 | 0.08 |
| long | 0.83 | 0.75 | 0.25 | 0.08 |
| sphere | 0.92 | 0.92 | 1.00 | 0.92 |
| cylinder | 0.50 | 0.25 | 0.08 | 0.17 |
| arch | 0.25 | 0.08 | 0.08 | 0.00 |
| dumbbell | 0.92 | 0.75 | 0.25 | 0.00 |
| t_shape | 0.75 | 0.83 | 0.42 | 0.08 |
| l_shape (unseen) | 0.83 | 0.58 | 0.67 | 0.42 |
| u_channel (unseen) | 0.50 | 0.33 | 0.50 | 0.25 |
| plus (unseen) | 0.42 | 0.50 | 0.33 | 0.00 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.22 | 0.37 | 0.47 | 0.33 |
| long | 0.36 | 0.44 | 0.39 | 0.51 |
| sphere | 0.11 | 0.11 | 0.12 | 0.14 |
| cylinder | 0.13 | 0.19 | 0.36 | 0.40 |
| arch | 0.03 | 0.03 | 0.04 | 0.05 |
| dumbbell | 0.13 | 0.26 | 0.19 | 0.18 |
| t_shape | 0.11 | 0.17 | 0.32 | 0.36 |
| l_shape | 0.04 | 0.18 | 0.13 | 0.27 |
| u_channel | 0.11 | 0.14 | 0.18 | 0.22 |
| plus | 0.16 | 0.12 | 0.09 | 0.04 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.73 | 0.70 | 0.60 | 0.27 |
| B_left | 0.67 | 0.60 | 0.40 | 0.17 |
| C_backright | 0.70 | 0.53 | 0.47 | 0.27 |
| D_far_turn | 0.67 | 0.43 | 0.17 | 0.10 |
