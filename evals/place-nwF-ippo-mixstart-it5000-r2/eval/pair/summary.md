# Pair evaluation: place-nwF-ippo-mixstart-it5000-r2

policy: checkpoint logs/marl2/nwF_ippo_uniform_mixstart_s0/model_5000.pt (iteration 5000, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.87 | 0.82 | 0.02 | 0.02 | 19.3 | 0.09 | 0.41 | 0.38 | 0.16 | 0.29 | 0.72 |
| 40 kg | 0.82 | 0.74 | 0.04 | 0.03 | 23.9 | 0.09 | 0.49 | 0.45 | 0.22 | 0.33 | 0.71 |
| 60 kg | 0.58 | 0.48 | 0.08 | 0.09 | 33.3 | 0.09 | 0.54 | 0.49 | 0.25 | 0.36 | 0.71 |
| 80 kg | 0.28 | 0.22 | 0.11 | 0.13 | 34.4 | 0.09 | 0.60 | 0.52 | 0.29 | 0.39 | 0.71 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.97 | 0.99 | 0.49 | 0.17 |
| long | 0.93 | 0.86 | 0.76 | 0.36 |
| sphere | 0.96 | 0.97 | 0.93 | 0.93 |
| cylinder | 0.61 | 0.47 | 0.31 | 0.21 |
| arch | 0.62 | 0.39 | 0.21 | 0.00 |
| dumbbell | 0.96 | 0.88 | 0.36 | 0.08 |
| t_shape | 0.96 | 0.94 | 0.68 | 0.26 |
| l_shape (unseen) | 0.97 | 0.97 | 0.82 | 0.29 |
| u_channel (unseen) | 1.00 | 0.92 | 0.67 | 0.28 |
| plus (unseen) | 0.72 | 0.78 | 0.60 | 0.19 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.17 | 0.15 | 0.11 | 0.10 |
| long | 0.29 | 0.29 | 0.32 | 0.39 |
| sphere | 0.07 | 0.16 | 0.23 | 0.27 |
| cylinder | 0.29 | 0.38 | 0.40 | 0.37 |
| arch | 0.01 | 0.02 | 0.02 | 0.01 |
| dumbbell | 0.10 | 0.17 | 0.17 | 0.19 |
| t_shape | 0.19 | 0.29 | 0.32 | 0.40 |
| l_shape | 0.20 | 0.33 | 0.39 | 0.47 |
| u_channel | 0.16 | 0.23 | 0.34 | 0.41 |
| plus | 0.07 | 0.14 | 0.21 | 0.30 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.93 | 0.86 | 0.69 | 0.39 |
| B_left | 0.91 | 0.83 | 0.66 | 0.32 |
| C_backright | 0.85 | 0.82 | 0.53 | 0.20 |
| D_far_turn | 0.80 | 0.76 | 0.45 | 0.19 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| standard | 0.88 | 0.81 | 0.61 | 0.31 |
| standard swapped | 0.87 | 0.87 | 0.62 | 0.33 |
| flank | 0.87 | 0.86 | 0.61 | 0.24 |
| flank swapped | 0.86 | 0.78 | 0.59 | 0.23 |
| goal_behind | 0.88 | 0.78 | 0.54 | 0.30 |
| goal_behind swapped | 0.88 | 0.81 | 0.52 | 0.27 |
