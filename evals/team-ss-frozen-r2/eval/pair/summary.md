# Pair evaluation: team-ss-frozen-r2

policy: frozen pair (spot): s2b-spot-falcon + s2b-spot-falcon

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | spot1 fell | spot2 fell | time to success (s) | robots touching | spot1 pushing | spot2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.48 | 0.47 | 0.28 | 0.21 | 21.3 | 0.22 | 0.39 | 0.43 | 0.18 | 0.30 | 0.55 |
| 40 kg | 0.33 | 0.28 | 0.36 | 0.25 | 20.0 | 0.23 | 0.51 | 0.54 | 0.32 | 0.47 | 0.56 |
| 60 kg | 0.24 | 0.23 | 0.39 | 0.30 | 23.9 | 0.21 | 0.62 | 0.59 | 0.42 | 0.56 | 0.59 |
| 80 kg | 0.12 | 0.12 | 0.39 | 0.35 | 25.0 | 0.24 | 0.66 | 0.60 | 0.47 | 0.63 | 0.58 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.67 | 0.25 | 0.58 | 0.33 |
| long | 0.67 | 0.25 | 0.08 | 0.00 |
| sphere | 0.42 | 0.67 | 0.50 | 0.42 |
| cylinder | 0.67 | 0.50 | 0.17 | 0.25 |
| arch | 0.25 | 0.17 | 0.08 | 0.00 |
| dumbbell | 0.42 | 0.25 | 0.17 | 0.08 |
| t_shape | 0.50 | 0.50 | 0.33 | 0.08 |
| l_shape (unseen) | 0.17 | 0.17 | 0.08 | 0.00 |
| u_channel (unseen) | 0.50 | 0.33 | 0.08 | 0.08 |
| plus (unseen) | 0.58 | 0.25 | 0.33 | 0.00 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.27 | 0.46 | 0.65 | 0.44 |
| long | 0.26 | 0.47 | 0.56 | 0.69 |
| sphere | 0.20 | 0.28 | 0.44 | 0.58 |
| cylinder | 0.14 | 0.40 | 0.54 | 0.64 |
| arch | 0.13 | 0.09 | 0.17 | 0.23 |
| dumbbell | 0.13 | 0.20 | 0.23 | 0.25 |
| t_shape | 0.20 | 0.39 | 0.57 | 0.47 |
| l_shape | 0.17 | 0.34 | 0.36 | 0.45 |
| u_channel | 0.12 | 0.34 | 0.35 | 0.47 |
| plus | 0.14 | 0.21 | 0.35 | 0.45 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.40 | 0.43 | 0.37 | 0.20 |
| B_left | 0.53 | 0.27 | 0.17 | 0.13 |
| C_backright | 0.33 | 0.17 | 0.30 | 0.10 |
| D_far_turn | 0.67 | 0.47 | 0.13 | 0.07 |
