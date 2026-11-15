# Pair evaluation: team-ss-frozen

policy: frozen pair (spot): s2b-spot-falcon + s2b-spot-falcon

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | spot1 fell | spot2 fell | time to success (s) | robots touching | spot1 pushing | spot2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.55 | 0.52 | 0.26 | 0.17 | 22.1 | 0.22 | 0.41 | 0.44 | 0.19 | 0.33 | 0.57 |
| 40 kg | 0.33 | 0.29 | 0.37 | 0.23 | 19.9 | 0.25 | 0.53 | 0.54 | 0.33 | 0.49 | 0.58 |
| 60 kg | 0.20 | 0.19 | 0.42 | 0.30 | 20.2 | 0.24 | 0.62 | 0.59 | 0.42 | 0.57 | 0.57 |
| 80 kg | 0.12 | 0.12 | 0.47 | 0.26 | 20.1 | 0.22 | 0.65 | 0.59 | 0.46 | 0.62 | 0.61 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.75 | 0.42 | 0.42 | 0.08 |
| long | 0.58 | 0.50 | 0.08 | 0.00 |
| sphere | 0.50 | 0.42 | 0.75 | 0.67 |
| cylinder | 0.67 | 0.42 | 0.33 | 0.25 |
| arch | 0.50 | 0.00 | 0.00 | 0.08 |
| dumbbell | 0.50 | 0.42 | 0.00 | 0.00 |
| t_shape | 0.75 | 0.42 | 0.17 | 0.00 |
| l_shape (unseen) | 0.25 | 0.33 | 0.00 | 0.08 |
| u_channel (unseen) | 0.42 | 0.25 | 0.17 | 0.00 |
| plus (unseen) | 0.58 | 0.17 | 0.08 | 0.00 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.27 | 0.43 | 0.47 | 0.45 |
| long | 0.31 | 0.53 | 0.64 | 0.68 |
| sphere | 0.27 | 0.35 | 0.56 | 0.57 |
| cylinder | 0.23 | 0.45 | 0.49 | 0.64 |
| arch | 0.08 | 0.13 | 0.23 | 0.19 |
| dumbbell | 0.14 | 0.15 | 0.25 | 0.14 |
| t_shape | 0.19 | 0.40 | 0.50 | 0.52 |
| l_shape | 0.15 | 0.34 | 0.42 | 0.48 |
| u_channel | 0.15 | 0.35 | 0.36 | 0.43 |
| plus | 0.14 | 0.21 | 0.32 | 0.51 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.50 | 0.37 | 0.33 | 0.27 |
| B_left | 0.57 | 0.27 | 0.13 | 0.07 |
| C_backright | 0.57 | 0.43 | 0.13 | 0.07 |
| D_far_turn | 0.57 | 0.27 | 0.20 | 0.07 |
