# Pair evaluation: solo-spot

policy: spot alone (s2b-spot-falcon)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | ANYmal fell | Spot fell | time to success (s) | robots touching |
|---|---|---|---|---|---|---|
| 20 kg | 0.74 | 0.69 | 0.00 | 0.08 | 25.6 |  |
| 40 kg | 0.47 | 0.41 | 0.00 | 0.23 | 32.0 |  |
| 60 kg | 0.13 | 0.13 | 0.00 | 0.31 | 28.6 |  |
| 80 kg | 0.10 | 0.10 | 0.00 | 0.32 | 15.4 |  |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 1.00 | 0.75 | 0.08 | 0.00 |
| long | 0.83 | 0.67 | 0.08 | 0.00 |
| sphere | 1.00 | 1.00 | 0.92 | 1.00 |
| cylinder | 0.83 | 0.50 | 0.25 | 0.25 |
| arch | 0.17 | 0.08 | 0.00 | 0.00 |
| dumbbell | 0.50 | 0.33 | 0.00 | 0.00 |
| t_shape | 0.83 | 0.67 | 0.00 | 0.00 |
| beam (unseen) | 0.42 | 0.00 | 0.00 | 0.00 |
| l_shape (unseen) | 0.75 | 0.42 | 0.00 | 0.00 |
| asym (unseen) | 0.83 | 0.08 | 0.00 | 0.00 |
| u_channel (unseen) | 0.92 | 0.50 | 0.00 | 0.00 |
| plus (unseen) | 0.83 | 0.58 | 0.25 | 0.00 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.89 | 0.53 | 0.22 | 0.17 |
| B_left | 0.69 | 0.53 | 0.14 | 0.08 |
| C_backright | 0.61 | 0.53 | 0.11 | 0.08 |
| D_far_turn | 0.78 | 0.28 | 0.06 | 0.08 |
