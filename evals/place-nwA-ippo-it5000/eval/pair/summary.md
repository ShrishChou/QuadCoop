# Pair evaluation: place-nwA-ippo-it5000

policy: checkpoint logs/marl2/nwA_ippo_uniform_s0/model_5000.pt (iteration 5000, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.88 | 0.82 | 0.02 | 0.02 | 19.1 | 0.08 | 0.41 | 0.40 | 0.15 | 0.27 | 0.71 |
| 40 kg | 0.82 | 0.76 | 0.04 | 0.04 | 24.4 | 0.09 | 0.48 | 0.46 | 0.21 | 0.33 | 0.72 |
| 60 kg | 0.59 | 0.51 | 0.08 | 0.07 | 33.3 | 0.09 | 0.54 | 0.50 | 0.25 | 0.36 | 0.72 |
| 80 kg | 0.28 | 0.22 | 0.09 | 0.16 | 34.1 | 0.09 | 0.59 | 0.53 | 0.29 | 0.39 | 0.70 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.99 | 0.92 | 0.54 | 0.12 |
| long | 0.93 | 0.93 | 0.78 | 0.35 |
| sphere | 0.99 | 0.97 | 0.94 | 0.96 |
| cylinder | 0.56 | 0.47 | 0.26 | 0.25 |
| arch | 0.67 | 0.53 | 0.22 | 0.01 |
| dumbbell | 0.96 | 0.75 | 0.54 | 0.14 |
| t_shape | 0.96 | 0.93 | 0.61 | 0.26 |
| l_shape (unseen) | 1.00 | 0.97 | 0.79 | 0.22 |
| u_channel (unseen) | 0.97 | 0.94 | 0.68 | 0.26 |
| plus (unseen) | 0.81 | 0.78 | 0.53 | 0.17 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.19 | 0.16 | 0.16 | 0.14 |
| long | 0.27 | 0.29 | 0.32 | 0.33 |
| sphere | 0.05 | 0.17 | 0.24 | 0.26 |
| cylinder | 0.28 | 0.36 | 0.40 | 0.40 |
| arch | 0.02 | 0.02 | 0.01 | 0.01 |
| dumbbell | 0.09 | 0.14 | 0.22 | 0.20 |
| t_shape | 0.18 | 0.26 | 0.28 | 0.38 |
| l_shape | 0.21 | 0.33 | 0.35 | 0.47 |
| u_channel | 0.16 | 0.25 | 0.33 | 0.38 |
| plus | 0.08 | 0.15 | 0.23 | 0.31 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.92 | 0.92 | 0.77 | 0.38 |
| B_left | 0.89 | 0.84 | 0.64 | 0.33 |
| C_backright | 0.89 | 0.82 | 0.53 | 0.19 |
| D_far_turn | 0.83 | 0.69 | 0.42 | 0.19 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| standard | 0.90 | 0.86 | 0.67 | 0.28 |
| standard swapped | 0.91 | 0.82 | 0.58 | 0.28 |
| flank | 0.86 | 0.83 | 0.57 | 0.29 |
| flank swapped | 0.88 | 0.80 | 0.58 | 0.24 |
| goal_behind | 0.88 | 0.79 | 0.61 | 0.29 |
| goal_behind swapped | 0.87 | 0.82 | 0.53 | 0.27 |
