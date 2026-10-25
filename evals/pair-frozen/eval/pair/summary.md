# Pair evaluation: pair-frozen

policy: frozen pair: s2b-anymal-term80 + s2b-spot-falcon

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | ANYmal fell | Spot fell | time to success (s) | robots touching |
|---|---|---|---|---|---|---|
| 20 kg | 0.69 | 0.65 | 0.11 | 0.17 | 17.2 | 0.28 |
| 40 kg | 0.57 | 0.55 | 0.10 | 0.26 | 21.5 | 0.32 |
| 60 kg | 0.28 | 0.25 | 0.17 | 0.40 | 26.7 | 0.34 |
| 80 kg | 0.16 | 0.14 | 0.18 | 0.48 | 26.5 | 0.34 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.83 | 0.58 | 0.33 | 0.08 |
| long | 0.92 | 0.67 | 0.25 | 0.08 |
| sphere | 0.83 | 1.00 | 0.83 | 0.83 |
| cylinder | 0.50 | 0.58 | 0.50 | 0.33 |
| arch | 0.17 | 0.08 | 0.08 | 0.00 |
| dumbbell | 0.58 | 0.50 | 0.17 | 0.00 |
| t_shape | 0.67 | 0.67 | 0.25 | 0.08 |
| beam (unseen) | 0.58 | 0.42 | 0.25 | 0.08 |
| l_shape (unseen) | 1.00 | 0.75 | 0.25 | 0.00 |
| asym (unseen) | 0.75 | 0.50 | 0.08 | 0.00 |
| u_channel (unseen) | 0.92 | 0.58 | 0.33 | 0.25 |
| plus (unseen) | 0.58 | 0.50 | 0.08 | 0.17 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.81 | 0.72 | 0.39 | 0.28 |
| B_left | 0.81 | 0.58 | 0.33 | 0.17 |
| C_backright | 0.56 | 0.53 | 0.25 | 0.08 |
| D_far_turn | 0.61 | 0.44 | 0.17 | 0.11 |
