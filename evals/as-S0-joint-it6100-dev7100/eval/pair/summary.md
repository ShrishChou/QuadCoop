# Pair evaluation: as-S0-joint-it6100-dev7100

policy: checkpoint logs/marl2/asS0_joint_s0/model_6100.pt (iteration 6100, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.87 | 0.83 | 0.02 | 0.02 | 18.3 | 0.09 | 0.41 | 0.40 | 0.16 | 0.29 | 0.71 |
| 40 kg | 0.84 | 0.76 | 0.03 | 0.04 | 23.8 | 0.09 | 0.49 | 0.47 | 0.23 | 0.34 | 0.73 |
| 60 kg | 0.58 | 0.50 | 0.09 | 0.07 | 32.9 | 0.09 | 0.54 | 0.51 | 0.26 | 0.37 | 0.70 |
| 80 kg | 0.29 | 0.25 | 0.12 | 0.13 | 34.6 | 0.09 | 0.58 | 0.54 | 0.30 | 0.40 | 0.70 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 1.00 | 0.99 | 0.58 | 0.17 |
| long | 0.88 | 0.92 | 0.69 | 0.46 |
| sphere | 0.92 | 0.97 | 0.99 | 0.99 |
| cylinder | 0.57 | 0.49 | 0.29 | 0.25 |
| arch | 0.58 | 0.46 | 0.22 | 0.01 |
| dumbbell | 0.93 | 0.83 | 0.39 | 0.08 |
| t_shape | 0.99 | 0.94 | 0.76 | 0.19 |
| l_shape (unseen) | 1.00 | 0.94 | 0.71 | 0.28 |
| u_channel (unseen) | 0.99 | 0.94 | 0.67 | 0.28 |
| plus (unseen) | 0.83 | 0.88 | 0.50 | 0.21 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.17 | 0.19 | 0.12 | 0.11 |
| long | 0.30 | 0.35 | 0.34 | 0.34 |
| sphere | 0.07 | 0.14 | 0.22 | 0.30 |
| cylinder | 0.23 | 0.33 | 0.43 | 0.40 |
| arch | 0.02 | 0.02 | 0.02 | 0.02 |
| dumbbell | 0.10 | 0.15 | 0.17 | 0.19 |
| t_shape | 0.24 | 0.34 | 0.34 | 0.42 |
| l_shape | 0.21 | 0.34 | 0.39 | 0.47 |
| u_channel | 0.17 | 0.23 | 0.32 | 0.40 |
| plus | 0.10 | 0.18 | 0.27 | 0.34 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.90 | 0.89 | 0.71 | 0.43 |
| B_left | 0.89 | 0.84 | 0.63 | 0.37 |
| C_backright | 0.87 | 0.85 | 0.51 | 0.20 |
| D_far_turn | 0.82 | 0.76 | 0.48 | 0.17 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| standard | 0.90 | 0.87 | 0.59 | 0.28 |
| standard swapped | 0.87 | 0.85 | 0.62 | 0.34 |
| flank | 0.84 | 0.82 | 0.60 | 0.32 |
| flank swapped | 0.86 | 0.80 | 0.60 | 0.23 |
| goal_behind | 0.91 | 0.85 | 0.59 | 0.30 |
| goal_behind swapped | 0.83 | 0.83 | 0.48 | 0.28 |
