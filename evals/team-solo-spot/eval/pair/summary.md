# Pair evaluation: team-solo-spot

policy: spot1 alone (s2b-spot-falcon)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | spot1 fell | spot2 fell | time to success (s) | robots touching | spot1 pushing | spot2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.74 | 0.64 | 0.10 | 0.00 | 21.4 |  |  |  |  |  |  |
| 40 kg | 0.61 | 0.50 | 0.23 | 0.00 | 33.0 |  |  |  |  |  |  |
| 60 kg | 0.17 | 0.16 | 0.34 | 0.00 | 30.8 |  |  |  |  |  |  |
| 80 kg | 0.10 | 0.10 | 0.36 | 0.00 | 16.2 |  |  |  |  |  |  |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.92 | 0.67 | 0.17 | 0.00 |
| long | 0.75 | 0.58 | 0.00 | 0.00 |
| sphere | 1.00 | 1.00 | 0.92 | 0.83 |
| cylinder | 0.58 | 0.42 | 0.25 | 0.17 |
| arch | 0.17 | 0.00 | 0.00 | 0.00 |
| dumbbell | 0.58 | 0.50 | 0.00 | 0.00 |
| t_shape | 0.92 | 0.58 | 0.17 | 0.00 |
| l_shape (unseen) | 0.75 | 0.58 | 0.08 | 0.00 |
| u_channel (unseen) | 0.83 | 0.83 | 0.00 | 0.00 |
| plus (unseen) | 0.92 | 0.92 | 0.08 | 0.00 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.87 | 0.77 | 0.17 | 0.17 |
| B_left | 0.70 | 0.63 | 0.23 | 0.07 |
| C_backright | 0.57 | 0.57 | 0.17 | 0.07 |
| D_far_turn | 0.83 | 0.47 | 0.10 | 0.10 |
