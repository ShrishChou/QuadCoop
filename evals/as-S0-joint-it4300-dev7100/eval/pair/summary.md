# Pair evaluation: as-S0-joint-it4300-dev7100

policy: checkpoint logs/marl2/asS0_joint_s0/model_4300.pt (iteration 4300, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.88 | 0.82 | 0.02 | 0.01 | 17.9 | 0.07 | 0.44 | 0.37 | 0.15 | 0.27 | 0.71 |
| 40 kg | 0.82 | 0.71 | 0.04 | 0.05 | 24.6 | 0.08 | 0.50 | 0.44 | 0.20 | 0.32 | 0.72 |
| 60 kg | 0.57 | 0.47 | 0.09 | 0.07 | 33.3 | 0.09 | 0.56 | 0.47 | 0.25 | 0.37 | 0.69 |
| 80 kg | 0.26 | 0.20 | 0.11 | 0.11 | 34.2 | 0.08 | 0.61 | 0.50 | 0.29 | 0.38 | 0.68 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.97 | 0.94 | 0.50 | 0.06 |
| long | 0.94 | 0.94 | 0.75 | 0.42 |
| sphere | 0.97 | 0.99 | 1.00 | 0.96 |
| cylinder | 0.54 | 0.46 | 0.32 | 0.22 |
| arch | 0.61 | 0.57 | 0.17 | 0.00 |
| dumbbell | 0.92 | 0.68 | 0.46 | 0.08 |
| t_shape | 0.99 | 0.89 | 0.76 | 0.10 |
| l_shape (unseen) | 1.00 | 0.96 | 0.76 | 0.32 |
| u_channel (unseen) | 0.99 | 0.96 | 0.67 | 0.26 |
| plus (unseen) | 0.86 | 0.79 | 0.36 | 0.19 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.15 | 0.14 | 0.14 | 0.09 |
| long | 0.29 | 0.29 | 0.34 | 0.38 |
| sphere | 0.09 | 0.18 | 0.23 | 0.29 |
| cylinder | 0.23 | 0.29 | 0.42 | 0.38 |
| arch | 0.01 | 0.01 | 0.01 | 0.00 |
| dumbbell | 0.11 | 0.15 | 0.17 | 0.25 |
| t_shape | 0.21 | 0.30 | 0.33 | 0.34 |
| l_shape | 0.21 | 0.31 | 0.38 | 0.46 |
| u_channel | 0.16 | 0.24 | 0.34 | 0.39 |
| plus | 0.07 | 0.14 | 0.19 | 0.30 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.96 | 0.88 | 0.73 | 0.44 |
| B_left | 0.90 | 0.82 | 0.54 | 0.24 |
| C_backright | 0.85 | 0.83 | 0.54 | 0.20 |
| D_far_turn | 0.81 | 0.74 | 0.49 | 0.16 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| standard | 0.90 | 0.84 | 0.57 | 0.26 |
| standard swapped | 0.89 | 0.90 | 0.64 | 0.29 |
| flank | 0.84 | 0.80 | 0.61 | 0.28 |
| flank swapped | 0.88 | 0.82 | 0.55 | 0.19 |
| goal_behind | 0.90 | 0.78 | 0.55 | 0.26 |
| goal_behind swapped | 0.87 | 0.78 | 0.53 | 0.29 |
