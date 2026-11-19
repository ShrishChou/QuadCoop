# Pair evaluation: as-S4-shared-it5100-dev7100

policy: checkpoint logs/marl2/asS4_shared_s0/model_5100.pt (iteration 5100, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.89 | 0.83 | 0.02 | 0.01 | 18.4 | 0.07 | 0.40 | 0.40 | 0.16 | 0.28 | 0.71 |
| 40 kg | 0.83 | 0.76 | 0.03 | 0.05 | 23.7 | 0.08 | 0.48 | 0.48 | 0.22 | 0.33 | 0.73 |
| 60 kg | 0.62 | 0.51 | 0.07 | 0.06 | 34.7 | 0.08 | 0.52 | 0.51 | 0.24 | 0.34 | 0.72 |
| 80 kg | 0.24 | 0.20 | 0.11 | 0.14 | 32.0 | 0.08 | 0.55 | 0.55 | 0.28 | 0.37 | 0.70 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.97 | 0.93 | 0.64 | 0.07 |
| long | 0.94 | 0.92 | 0.69 | 0.31 |
| sphere | 0.99 | 1.00 | 0.99 | 0.93 |
| cylinder | 0.61 | 0.43 | 0.40 | 0.21 |
| arch | 0.71 | 0.58 | 0.25 | 0.03 |
| dumbbell | 0.96 | 0.81 | 0.50 | 0.08 |
| t_shape | 0.96 | 0.92 | 0.74 | 0.14 |
| l_shape (unseen) | 0.99 | 0.99 | 0.81 | 0.21 |
| u_channel (unseen) | 1.00 | 0.94 | 0.68 | 0.26 |
| plus (unseen) | 0.75 | 0.83 | 0.50 | 0.14 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.15 | 0.17 | 0.10 | 0.10 |
| long | 0.28 | 0.32 | 0.31 | 0.40 |
| sphere | 0.10 | 0.18 | 0.22 | 0.28 |
| cylinder | 0.27 | 0.35 | 0.38 | 0.36 |
| arch | 0.01 | 0.02 | 0.01 | 0.00 |
| dumbbell | 0.09 | 0.15 | 0.20 | 0.22 |
| t_shape | 0.20 | 0.27 | 0.30 | 0.37 |
| l_shape | 0.21 | 0.33 | 0.33 | 0.40 |
| u_channel | 0.17 | 0.25 | 0.33 | 0.41 |
| plus | 0.09 | 0.14 | 0.21 | 0.28 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.93 | 0.91 | 0.73 | 0.37 |
| B_left | 0.91 | 0.86 | 0.67 | 0.22 |
| C_backright | 0.88 | 0.84 | 0.53 | 0.19 |
| D_far_turn | 0.83 | 0.73 | 0.55 | 0.17 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| standard | 0.87 | 0.78 | 0.64 | 0.25 |
| standard swapped | 0.89 | 0.88 | 0.65 | 0.23 |
| flank | 0.90 | 0.88 | 0.65 | 0.23 |
| flank swapped | 0.88 | 0.85 | 0.65 | 0.23 |
| goal_behind | 0.88 | 0.81 | 0.57 | 0.28 |
| goal_behind swapped | 0.92 | 0.81 | 0.56 | 0.21 |
