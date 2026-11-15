# Pair evaluation: team-mx-frozen

policy: frozen pair (mixed): s2b-anymal-term80 + s2b-spot-falcon

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal fell | spot fell | time to success (s) | robots touching | anymal pushing | spot pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.63 | 0.58 | 0.08 | 0.24 | 17.5 | 0.31 | 0.38 | 0.37 | 0.15 | 0.28 | 0.51 |
| 40 kg | 0.55 | 0.50 | 0.12 | 0.28 | 22.5 | 0.33 | 0.46 | 0.51 | 0.27 | 0.44 | 0.51 |
| 60 kg | 0.40 | 0.37 | 0.16 | 0.33 | 26.9 | 0.33 | 0.53 | 0.54 | 0.34 | 0.52 | 0.50 |
| 80 kg | 0.23 | 0.20 | 0.17 | 0.42 | 28.8 | 0.33 | 0.56 | 0.59 | 0.37 | 0.51 | 0.52 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.92 | 0.50 | 0.67 | 0.25 |
| long | 0.75 | 0.83 | 0.58 | 0.08 |
| sphere | 0.75 | 1.00 | 0.75 | 0.83 |
| cylinder | 0.33 | 0.33 | 0.33 | 0.42 |
| arch | 0.25 | 0.25 | 0.08 | 0.00 |
| dumbbell | 0.58 | 0.17 | 0.17 | 0.00 |
| t_shape | 0.75 | 0.83 | 0.42 | 0.25 |
| l_shape (unseen) | 0.75 | 0.67 | 0.42 | 0.33 |
| u_channel (unseen) | 0.75 | 0.75 | 0.33 | 0.00 |
| plus (unseen) | 0.50 | 0.17 | 0.25 | 0.17 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.28 | 0.43 | 0.36 | 0.38 |
| long | 0.28 | 0.46 | 0.48 | 0.47 |
| sphere | 0.11 | 0.22 | 0.26 | 0.31 |
| cylinder | 0.13 | 0.31 | 0.38 | 0.49 |
| arch | 0.03 | 0.04 | 0.13 | 0.15 |
| dumbbell | 0.12 | 0.16 | 0.20 | 0.13 |
| t_shape | 0.10 | 0.30 | 0.44 | 0.57 |
| l_shape | 0.15 | 0.28 | 0.40 | 0.43 |
| u_channel | 0.21 | 0.34 | 0.48 | 0.39 |
| plus | 0.08 | 0.17 | 0.28 | 0.36 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.77 | 0.60 | 0.53 | 0.33 |
| B_left | 0.70 | 0.57 | 0.47 | 0.23 |
| C_backright | 0.50 | 0.47 | 0.37 | 0.27 |
| D_far_turn | 0.57 | 0.57 | 0.23 | 0.10 |
