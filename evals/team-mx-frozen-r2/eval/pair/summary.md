# Pair evaluation: team-mx-frozen-r2

policy: frozen pair (mixed): s2b-anymal-term80 + s2b-spot-falcon

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal fell | spot fell | time to success (s) | robots touching | anymal pushing | spot pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.61 | 0.60 | 0.12 | 0.23 | 16.7 | 0.32 | 0.41 | 0.36 | 0.16 | 0.29 | 0.50 |
| 40 kg | 0.59 | 0.55 | 0.08 | 0.25 | 21.7 | 0.35 | 0.46 | 0.48 | 0.27 | 0.45 | 0.50 |
| 60 kg | 0.35 | 0.31 | 0.12 | 0.42 | 23.4 | 0.34 | 0.52 | 0.53 | 0.33 | 0.49 | 0.52 |
| 80 kg | 0.20 | 0.17 | 0.17 | 0.40 | 24.3 | 0.33 | 0.55 | 0.57 | 0.36 | 0.50 | 0.52 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.67 | 0.67 | 0.50 | 0.25 |
| long | 1.00 | 0.83 | 0.17 | 0.17 |
| sphere | 0.58 | 0.75 | 0.75 | 0.83 |
| cylinder | 0.42 | 0.42 | 0.42 | 0.25 |
| arch | 0.17 | 0.25 | 0.08 | 0.00 |
| dumbbell | 0.75 | 0.58 | 0.33 | 0.00 |
| t_shape | 0.75 | 0.58 | 0.33 | 0.08 |
| l_shape (unseen) | 0.67 | 0.83 | 0.42 | 0.17 |
| u_channel (unseen) | 0.50 | 0.67 | 0.17 | 0.17 |
| plus (unseen) | 0.58 | 0.33 | 0.33 | 0.08 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.34 | 0.40 | 0.42 | 0.42 |
| long | 0.25 | 0.47 | 0.53 | 0.53 |
| sphere | 0.12 | 0.21 | 0.30 | 0.30 |
| cylinder | 0.16 | 0.38 | 0.53 | 0.43 |
| arch | 0.03 | 0.05 | 0.06 | 0.15 |
| dumbbell | 0.13 | 0.18 | 0.17 | 0.20 |
| t_shape | 0.13 | 0.26 | 0.51 | 0.44 |
| l_shape | 0.13 | 0.31 | 0.20 | 0.38 |
| u_channel | 0.22 | 0.29 | 0.35 | 0.48 |
| plus | 0.09 | 0.13 | 0.19 | 0.23 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.73 | 0.70 | 0.47 | 0.40 |
| B_left | 0.70 | 0.60 | 0.37 | 0.13 |
| C_backright | 0.50 | 0.67 | 0.37 | 0.17 |
| D_far_turn | 0.50 | 0.40 | 0.20 | 0.10 |
