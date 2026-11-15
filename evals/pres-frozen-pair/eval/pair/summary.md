# Pair evaluation: pres-frozen-pair

policy: frozen pair (anymal): s2b-anymal-term80 + s2b-anymal-term80

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.72 | 0.68 | 0.08 | 0.12 | 21.1 | 0.49 | 0.37 | 0.32 | 0.12 | 0.25 | 0.47 |
| 40 kg | 0.57 | 0.50 | 0.18 | 0.16 | 25.4 | 0.54 | 0.41 | 0.44 | 0.21 | 0.38 | 0.49 |
| 60 kg | 0.35 | 0.29 | 0.23 | 0.19 | 30.1 | 0.54 | 0.42 | 0.49 | 0.21 | 0.35 | 0.48 |
| 80 kg | 0.17 | 0.16 | 0.30 | 0.25 | 26.2 | 0.57 | 0.49 | 0.50 | 0.25 | 0.38 | 0.47 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.75 | 0.75 | 0.33 | 0.08 |
| long | 1.00 | 0.83 | 0.42 | 0.00 |
| sphere | 0.92 | 0.92 | 1.00 | 0.92 |
| cylinder | 0.50 | 0.25 | 0.08 | 0.25 |
| arch | 0.33 | 0.33 | 0.00 | 0.00 |
| dumbbell | 0.67 | 0.50 | 0.17 | 0.00 |
| t_shape | 0.92 | 0.67 | 0.42 | 0.00 |
| l_shape (unseen) | 0.92 | 0.58 | 0.50 | 0.33 |
| u_channel (unseen) | 0.92 | 0.42 | 0.42 | 0.00 |
| plus (unseen) | 0.33 | 0.50 | 0.17 | 0.17 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.21 | 0.34 | 0.43 | 0.36 |
| long | 0.26 | 0.42 | 0.40 | 0.43 |
| sphere | 0.09 | 0.12 | 0.14 | 0.13 |
| cylinder | 0.13 | 0.31 | 0.36 | 0.34 |
| arch | 0.02 | 0.04 | 0.04 | 0.06 |
| dumbbell | 0.15 | 0.29 | 0.18 | 0.16 |
| t_shape | 0.11 | 0.20 | 0.18 | 0.35 |
| l_shape | 0.05 | 0.20 | 0.13 | 0.34 |
| u_channel | 0.08 | 0.16 | 0.15 | 0.21 |
| plus | 0.10 | 0.07 | 0.14 | 0.12 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.77 | 0.77 | 0.40 | 0.27 |
| B_left | 0.73 | 0.43 | 0.37 | 0.17 |
| C_backright | 0.77 | 0.67 | 0.47 | 0.13 |
| D_far_turn | 0.63 | 0.43 | 0.17 | 0.13 |
