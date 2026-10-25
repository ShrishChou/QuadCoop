# Pair evaluation: solo-anymal

policy: anymal alone (s2b-anymal-term80)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | ANYmal fell | Spot fell | time to success (s) | robots touching |
|---|---|---|---|---|---|---|
| 20 kg | 0.89 | 0.80 | 0.00 | 0.00 | 19.5 |  |
| 40 kg | 0.60 | 0.53 | 0.10 | 0.00 | 30.5 |  |
| 60 kg | 0.27 | 0.24 | 0.15 | 0.00 | 37.7 |  |
| 80 kg | 0.11 | 0.11 | 0.16 | 0.00 | 19.5 |  |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 1.00 | 1.00 | 0.67 | 0.08 |
| long | 1.00 | 0.92 | 0.25 | 0.00 |
| sphere | 1.00 | 1.00 | 1.00 | 0.92 |
| cylinder | 0.58 | 0.58 | 0.42 | 0.25 |
| arch | 0.42 | 0.25 | 0.17 | 0.08 |
| dumbbell | 0.92 | 0.33 | 0.17 | 0.00 |
| t_shape | 1.00 | 0.58 | 0.00 | 0.00 |
| beam (unseen) | 0.83 | 0.17 | 0.00 | 0.00 |
| l_shape (unseen) | 1.00 | 0.92 | 0.08 | 0.00 |
| asym (unseen) | 0.92 | 0.08 | 0.00 | 0.00 |
| u_channel (unseen) | 1.00 | 0.83 | 0.08 | 0.00 |
| plus (unseen) | 1.00 | 0.50 | 0.42 | 0.00 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.89 | 0.69 | 0.42 | 0.19 |
| B_left | 0.92 | 0.64 | 0.22 | 0.06 |
| C_backright | 0.92 | 0.67 | 0.33 | 0.11 |
| D_far_turn | 0.83 | 0.39 | 0.11 | 0.08 |
