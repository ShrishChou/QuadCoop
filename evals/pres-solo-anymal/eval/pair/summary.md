# Pair evaluation: pres-solo-anymal

policy: anymal1 alone (s2b-anymal-term80)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.86 | 0.81 | 0.01 | 0.00 | 17.8 |  |  |  |  |  |  |
| 40 kg | 0.79 | 0.68 | 0.03 | 0.00 | 30.6 |  |  |  |  |  |  |
| 60 kg | 0.33 | 0.28 | 0.12 | 0.00 | 35.7 |  |  |  |  |  |  |
| 80 kg | 0.12 | 0.12 | 0.12 | 0.00 | 16.9 |  |  |  |  |  |  |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 1.00 | 1.00 | 0.58 | 0.08 |
| long | 1.00 | 1.00 | 0.17 | 0.00 |
| sphere | 1.00 | 1.00 | 1.00 | 1.00 |
| cylinder | 0.50 | 0.58 | 0.33 | 0.17 |
| arch | 0.42 | 0.25 | 0.17 | 0.00 |
| dumbbell | 0.92 | 0.67 | 0.08 | 0.00 |
| t_shape | 1.00 | 0.83 | 0.17 | 0.00 |
| l_shape (unseen) | 1.00 | 0.92 | 0.50 | 0.00 |
| u_channel (unseen) | 1.00 | 1.00 | 0.17 | 0.00 |
| plus (unseen) | 0.75 | 0.67 | 0.08 | 0.00 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.83 | 0.90 | 0.43 | 0.17 |
| B_left | 0.93 | 0.73 | 0.37 | 0.13 |
| C_backright | 0.83 | 0.97 | 0.40 | 0.10 |
| D_far_turn | 0.83 | 0.57 | 0.10 | 0.10 |
