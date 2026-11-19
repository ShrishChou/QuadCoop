# Pair evaluation: as-S0-joint-s1-it6100-fresh7500

policy: checkpoint logs/marl2/asS0_joint_s1/model_6100.pt (iteration 6100, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.87 | 0.81 | 0.02 | 0.02 | 18.9 | 0.09 | 0.39 | 0.40 | 0.16 | 0.29 | 0.70 |
| 40 kg | 0.82 | 0.76 | 0.05 | 0.03 | 22.8 | 0.09 | 0.48 | 0.47 | 0.22 | 0.35 | 0.72 |
| 60 kg | 0.58 | 0.48 | 0.08 | 0.09 | 31.4 | 0.09 | 0.54 | 0.50 | 0.26 | 0.38 | 0.70 |
| 80 kg | 0.26 | 0.23 | 0.12 | 0.14 | 34.4 | 0.10 | 0.60 | 0.54 | 0.31 | 0.41 | 0.70 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.99 | 0.93 | 0.62 | 0.22 |
| long | 0.94 | 0.92 | 0.74 | 0.29 |
| sphere | 0.96 | 0.99 | 0.97 | 0.89 |
| cylinder | 0.57 | 0.50 | 0.35 | 0.25 |
| arch | 0.64 | 0.53 | 0.24 | 0.03 |
| dumbbell | 0.89 | 0.81 | 0.32 | 0.07 |
| t_shape | 0.99 | 0.90 | 0.67 | 0.29 |
| l_shape (unseen) | 0.97 | 0.93 | 0.86 | 0.25 |
| u_channel (unseen) | 0.97 | 0.93 | 0.64 | 0.19 |
| plus (unseen) | 0.78 | 0.82 | 0.44 | 0.15 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.17 | 0.19 | 0.18 | 0.18 |
| long | 0.28 | 0.30 | 0.29 | 0.39 |
| sphere | 0.08 | 0.17 | 0.24 | 0.29 |
| cylinder | 0.32 | 0.38 | 0.42 | 0.44 |
| arch | 0.03 | 0.02 | 0.02 | 0.02 |
| dumbbell | 0.08 | 0.17 | 0.21 | 0.21 |
| t_shape | 0.18 | 0.27 | 0.31 | 0.41 |
| l_shape | 0.19 | 0.32 | 0.39 | 0.45 |
| u_channel | 0.16 | 0.27 | 0.38 | 0.49 |
| plus | 0.08 | 0.14 | 0.20 | 0.26 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.93 | 0.92 | 0.75 | 0.38 |
| B_left | 0.88 | 0.86 | 0.62 | 0.29 |
| C_backright | 0.86 | 0.81 | 0.59 | 0.24 |
| D_far_turn | 0.81 | 0.72 | 0.38 | 0.14 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| standard | 0.93 | 0.87 | 0.57 | 0.28 |
| standard swapped | 0.88 | 0.78 | 0.63 | 0.27 |
| flank | 0.87 | 0.84 | 0.56 | 0.24 |
| flank swapped | 0.86 | 0.87 | 0.55 | 0.19 |
| goal_behind | 0.86 | 0.81 | 0.56 | 0.26 |
| goal_behind swapped | 0.82 | 0.78 | 0.63 | 0.34 |
