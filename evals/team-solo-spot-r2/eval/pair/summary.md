# Pair evaluation: team-solo-spot-r2

policy: spot1 alone (s2b-spot-falcon)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | spot1 fell | spot2 fell | time to success (s) | robots touching | spot1 pushing | spot2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.81 | 0.70 | 0.07 | 0.00 | 23.3 |  |  |  |  |  |  |
| 40 kg | 0.57 | 0.54 | 0.21 | 0.00 | 31.5 |  |  |  |  |  |  |
| 60 kg | 0.15 | 0.13 | 0.43 | 0.00 | 22.5 |  |  |  |  |  |  |
| 80 kg | 0.12 | 0.12 | 0.37 | 0.00 | 22.5 |  |  |  |  |  |  |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.92 | 0.83 | 0.08 | 0.00 |
| long | 0.83 | 0.58 | 0.00 | 0.00 |
| sphere | 1.00 | 1.00 | 1.00 | 0.92 |
| cylinder | 0.75 | 0.58 | 0.25 | 0.25 |
| arch | 0.25 | 0.00 | 0.00 | 0.00 |
| dumbbell | 0.83 | 0.33 | 0.00 | 0.00 |
| t_shape | 0.92 | 0.50 | 0.08 | 0.00 |
| l_shape (unseen) | 0.83 | 0.58 | 0.00 | 0.00 |
| u_channel (unseen) | 0.75 | 0.67 | 0.00 | 0.00 |
| plus (unseen) | 1.00 | 0.58 | 0.08 | 0.00 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.90 | 0.67 | 0.23 | 0.20 |
| B_left | 0.80 | 0.63 | 0.13 | 0.10 |
| C_backright | 0.63 | 0.47 | 0.13 | 0.10 |
| D_far_turn | 0.90 | 0.50 | 0.10 | 0.07 |
