# Pair evaluation: of-OFi-it6100-dev7100

policy: checkpoint logs/marl2/ofI_ippo_oppose_s0/model_6100.pt (iteration 6100, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.87 | 0.83 | 0.02 | 0.02 | 18.9 | 0.08 | 0.40 | 0.40 | 0.16 | 0.30 | 0.72 |
| 40 kg | 0.82 | 0.74 | 0.04 | 0.04 | 24.0 | 0.09 | 0.50 | 0.46 | 0.23 | 0.35 | 0.72 |
| 60 kg | 0.57 | 0.47 | 0.09 | 0.10 | 33.5 | 0.10 | 0.55 | 0.50 | 0.26 | 0.37 | 0.71 |
| 80 kg | 0.27 | 0.23 | 0.11 | 0.13 | 33.8 | 0.10 | 0.59 | 0.54 | 0.30 | 0.40 | 0.70 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 1.00 | 0.94 | 0.50 | 0.17 |
| long | 0.88 | 0.89 | 0.65 | 0.39 |
| sphere | 0.83 | 0.97 | 0.96 | 0.94 |
| cylinder | 0.64 | 0.44 | 0.33 | 0.28 |
| arch | 0.60 | 0.47 | 0.24 | 0.00 |
| dumbbell | 0.93 | 0.88 | 0.35 | 0.11 |
| t_shape | 0.99 | 0.92 | 0.71 | 0.17 |
| l_shape (unseen) | 1.00 | 0.94 | 0.81 | 0.22 |
| u_channel (unseen) | 0.99 | 0.94 | 0.62 | 0.19 |
| plus (unseen) | 0.81 | 0.76 | 0.51 | 0.22 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.15 | 0.16 | 0.13 | 0.16 |
| long | 0.29 | 0.34 | 0.33 | 0.37 |
| sphere | 0.08 | 0.17 | 0.24 | 0.28 |
| cylinder | 0.31 | 0.37 | 0.45 | 0.41 |
| arch | 0.02 | 0.02 | 0.02 | 0.02 |
| dumbbell | 0.10 | 0.15 | 0.17 | 0.18 |
| t_shape | 0.20 | 0.29 | 0.33 | 0.39 |
| l_shape | 0.23 | 0.36 | 0.37 | 0.49 |
| u_channel | 0.15 | 0.25 | 0.33 | 0.42 |
| plus | 0.08 | 0.15 | 0.23 | 0.30 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.94 | 0.88 | 0.72 | 0.39 |
| B_left | 0.91 | 0.81 | 0.59 | 0.31 |
| C_backright | 0.85 | 0.83 | 0.51 | 0.20 |
| D_far_turn | 0.77 | 0.75 | 0.46 | 0.17 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| standard | 0.86 | 0.82 | 0.59 | 0.25 |
| standard swapped | 0.83 | 0.80 | 0.65 | 0.28 |
| flank | 0.86 | 0.80 | 0.60 | 0.27 |
| flank swapped | 0.88 | 0.83 | 0.47 | 0.25 |
| goal_behind | 0.88 | 0.82 | 0.56 | 0.30 |
| goal_behind swapped | 0.88 | 0.83 | 0.53 | 0.27 |
