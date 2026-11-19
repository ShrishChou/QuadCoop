# Pair evaluation: as-S0-joint-it6100-fresh7500

policy: checkpoint logs/marl2/asS0_joint_s0/model_6100.pt (iteration 6100, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.85 | 0.80 | 0.03 | 0.02 | 18.4 | 0.09 | 0.40 | 0.39 | 0.15 | 0.28 | 0.72 |
| 40 kg | 0.80 | 0.72 | 0.04 | 0.04 | 24.0 | 0.10 | 0.48 | 0.47 | 0.22 | 0.34 | 0.73 |
| 60 kg | 0.57 | 0.48 | 0.09 | 0.09 | 33.5 | 0.10 | 0.51 | 0.52 | 0.26 | 0.37 | 0.71 |
| 80 kg | 0.26 | 0.23 | 0.15 | 0.12 | 33.5 | 0.10 | 0.55 | 0.55 | 0.29 | 0.39 | 0.70 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.99 | 0.93 | 0.58 | 0.17 |
| long | 0.88 | 0.83 | 0.71 | 0.25 |
| sphere | 0.97 | 0.94 | 1.00 | 0.96 |
| cylinder | 0.56 | 0.49 | 0.31 | 0.26 |
| arch | 0.54 | 0.54 | 0.14 | 0.03 |
| dumbbell | 0.90 | 0.76 | 0.33 | 0.08 |
| t_shape | 1.00 | 0.97 | 0.71 | 0.18 |
| l_shape (unseen) | 0.97 | 0.93 | 0.81 | 0.22 |
| u_channel (unseen) | 1.00 | 0.92 | 0.62 | 0.21 |
| plus (unseen) | 0.68 | 0.72 | 0.49 | 0.19 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.16 | 0.12 | 0.13 | 0.14 |
| long | 0.32 | 0.32 | 0.31 | 0.30 |
| sphere | 0.08 | 0.13 | 0.24 | 0.26 |
| cylinder | 0.25 | 0.42 | 0.41 | 0.38 |
| arch | 0.02 | 0.02 | 0.02 | 0.02 |
| dumbbell | 0.09 | 0.16 | 0.17 | 0.20 |
| t_shape | 0.19 | 0.32 | 0.36 | 0.41 |
| l_shape | 0.16 | 0.30 | 0.39 | 0.44 |
| u_channel | 0.17 | 0.25 | 0.33 | 0.40 |
| plus | 0.09 | 0.17 | 0.23 | 0.31 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.91 | 0.87 | 0.71 | 0.37 |
| B_left | 0.86 | 0.83 | 0.60 | 0.31 |
| C_backright | 0.86 | 0.80 | 0.57 | 0.21 |
| D_far_turn | 0.77 | 0.72 | 0.40 | 0.14 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| standard | 0.87 | 0.87 | 0.55 | 0.25 |
| standard swapped | 0.88 | 0.79 | 0.57 | 0.25 |
| flank | 0.88 | 0.78 | 0.54 | 0.26 |
| flank swapped | 0.84 | 0.83 | 0.62 | 0.26 |
| goal_behind | 0.80 | 0.77 | 0.53 | 0.24 |
| goal_behind swapped | 0.83 | 0.79 | 0.59 | 0.28 |
