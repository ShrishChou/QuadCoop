# Pair evaluation: as-S3-onlyB-it6100-dev7100

policy: checkpoint logs/marl2/asS3_onlyB_s0/model_6100.pt (iteration 6100, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.87 | 0.83 | 0.02 | 0.03 | 18.7 | 0.09 | 0.42 | 0.36 | 0.14 | 0.26 | 0.70 |
| 40 kg | 0.81 | 0.74 | 0.06 | 0.05 | 23.4 | 0.10 | 0.51 | 0.45 | 0.22 | 0.33 | 0.70 |
| 60 kg | 0.60 | 0.53 | 0.09 | 0.08 | 32.4 | 0.11 | 0.56 | 0.48 | 0.26 | 0.37 | 0.70 |
| 80 kg | 0.25 | 0.21 | 0.12 | 0.15 | 31.6 | 0.10 | 0.60 | 0.51 | 0.29 | 0.38 | 0.69 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.96 | 0.93 | 0.57 | 0.07 |
| long | 0.93 | 0.90 | 0.79 | 0.31 |
| sphere | 0.96 | 0.97 | 0.97 | 0.94 |
| cylinder | 0.60 | 0.50 | 0.32 | 0.18 |
| arch | 0.62 | 0.54 | 0.22 | 0.01 |
| dumbbell | 0.90 | 0.67 | 0.49 | 0.12 |
| t_shape | 0.96 | 0.93 | 0.65 | 0.28 |
| l_shape (unseen) | 0.99 | 0.97 | 0.81 | 0.25 |
| u_channel (unseen) | 0.97 | 0.93 | 0.68 | 0.19 |
| plus (unseen) | 0.81 | 0.74 | 0.53 | 0.10 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.15 | 0.18 | 0.14 | 0.08 |
| long | 0.26 | 0.31 | 0.35 | 0.41 |
| sphere | 0.05 | 0.14 | 0.20 | 0.28 |
| cylinder | 0.20 | 0.32 | 0.36 | 0.36 |
| arch | 0.01 | 0.02 | 0.01 | 0.02 |
| dumbbell | 0.10 | 0.16 | 0.21 | 0.21 |
| t_shape | 0.20 | 0.32 | 0.36 | 0.39 |
| l_shape | 0.22 | 0.34 | 0.42 | 0.45 |
| u_channel | 0.16 | 0.26 | 0.31 | 0.41 |
| plus | 0.08 | 0.14 | 0.21 | 0.25 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.90 | 0.88 | 0.72 | 0.36 |
| B_left | 0.87 | 0.85 | 0.64 | 0.27 |
| C_backright | 0.88 | 0.82 | 0.55 | 0.22 |
| D_far_turn | 0.82 | 0.68 | 0.49 | 0.13 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| standard | 0.92 | 0.82 | 0.63 | 0.28 |
| standard swapped | 0.90 | 0.82 | 0.62 | 0.25 |
| flank | 0.88 | 0.78 | 0.60 | 0.21 |
| flank swapped | 0.83 | 0.82 | 0.60 | 0.23 |
| goal_behind | 0.82 | 0.83 | 0.64 | 0.25 |
| goal_behind swapped | 0.88 | 0.78 | 0.53 | 0.26 |
