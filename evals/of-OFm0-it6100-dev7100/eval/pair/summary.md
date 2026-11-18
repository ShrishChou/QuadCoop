# Pair evaluation: of-OFm0-it6100-dev7100

policy: checkpoint logs/marl2/ofM0_mappo_joint_s0/model_6100.pt (iteration 6100, mappo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.88 | 0.83 | 0.02 | 0.03 | 18.8 | 0.11 | 0.41 | 0.42 | 0.17 | 0.31 | 0.70 |
| 40 kg | 0.82 | 0.76 | 0.04 | 0.05 | 23.3 | 0.11 | 0.49 | 0.49 | 0.24 | 0.36 | 0.71 |
| 60 kg | 0.59 | 0.52 | 0.08 | 0.08 | 30.3 | 0.11 | 0.55 | 0.53 | 0.29 | 0.42 | 0.69 |
| 80 kg | 0.28 | 0.23 | 0.12 | 0.15 | 34.3 | 0.11 | 0.58 | 0.55 | 0.32 | 0.42 | 0.68 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.99 | 0.96 | 0.64 | 0.17 |
| long | 0.94 | 0.92 | 0.72 | 0.35 |
| sphere | 0.94 | 0.93 | 0.99 | 0.92 |
| cylinder | 0.58 | 0.46 | 0.32 | 0.21 |
| arch | 0.61 | 0.54 | 0.18 | 0.03 |
| dumbbell | 0.94 | 0.85 | 0.32 | 0.06 |
| t_shape | 0.97 | 0.93 | 0.74 | 0.29 |
| l_shape (unseen) | 0.99 | 0.99 | 0.76 | 0.24 |
| u_channel (unseen) | 0.99 | 0.94 | 0.69 | 0.26 |
| plus (unseen) | 0.86 | 0.72 | 0.54 | 0.31 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.20 | 0.19 | 0.22 | 0.18 |
| long | 0.32 | 0.33 | 0.43 | 0.42 |
| sphere | 0.06 | 0.14 | 0.23 | 0.29 |
| cylinder | 0.29 | 0.34 | 0.45 | 0.45 |
| arch | 0.02 | 0.04 | 0.02 | 0.02 |
| dumbbell | 0.11 | 0.18 | 0.19 | 0.19 |
| t_shape | 0.22 | 0.33 | 0.40 | 0.45 |
| l_shape | 0.26 | 0.37 | 0.40 | 0.49 |
| u_channel | 0.17 | 0.31 | 0.34 | 0.38 |
| plus | 0.09 | 0.15 | 0.27 | 0.30 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.91 | 0.88 | 0.71 | 0.48 |
| B_left | 0.93 | 0.82 | 0.63 | 0.33 |
| C_backright | 0.88 | 0.84 | 0.53 | 0.17 |
| D_far_turn | 0.81 | 0.75 | 0.49 | 0.14 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| standard | 0.88 | 0.86 | 0.61 | 0.23 |
| standard swapped | 0.92 | 0.83 | 0.63 | 0.33 |
| flank | 0.88 | 0.79 | 0.62 | 0.27 |
| flank swapped | 0.85 | 0.78 | 0.63 | 0.32 |
| goal_behind | 0.90 | 0.88 | 0.55 | 0.27 |
| goal_behind swapped | 0.88 | 0.79 | 0.50 | 0.28 |
