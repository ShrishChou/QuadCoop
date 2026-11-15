# Pair evaluation: place-nwF-ippo-mixstart-it5000-fresh7300-r2

policy: checkpoint logs/marl2/nwF_ippo_uniform_mixstart_s0/model_5000.pt (iteration 5000, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.89 | 0.85 | 0.01 | 0.02 | 19.3 | 0.09 | 0.41 | 0.38 | 0.15 | 0.27 | 0.70 |
| 40 kg | 0.82 | 0.75 | 0.03 | 0.03 | 24.0 | 0.09 | 0.51 | 0.45 | 0.22 | 0.35 | 0.72 |
| 60 kg | 0.58 | 0.49 | 0.07 | 0.08 | 33.0 | 0.09 | 0.54 | 0.50 | 0.25 | 0.36 | 0.70 |
| 80 kg | 0.29 | 0.23 | 0.11 | 0.12 | 36.2 | 0.09 | 0.58 | 0.53 | 0.29 | 0.39 | 0.70 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.99 | 1.00 | 0.53 | 0.14 |
| long | 0.94 | 0.89 | 0.75 | 0.40 |
| sphere | 0.94 | 1.00 | 0.99 | 0.93 |
| cylinder | 0.61 | 0.47 | 0.40 | 0.26 |
| arch | 0.64 | 0.49 | 0.12 | 0.00 |
| dumbbell | 0.92 | 0.72 | 0.42 | 0.12 |
| t_shape | 0.97 | 0.92 | 0.60 | 0.17 |
| l_shape (unseen) | 1.00 | 1.00 | 0.79 | 0.40 |
| u_channel (unseen) | 0.99 | 0.94 | 0.74 | 0.24 |
| plus (unseen) | 0.89 | 0.81 | 0.49 | 0.22 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.16 | 0.18 | 0.14 | 0.09 |
| long | 0.26 | 0.29 | 0.32 | 0.37 |
| sphere | 0.07 | 0.16 | 0.25 | 0.29 |
| cylinder | 0.24 | 0.36 | 0.41 | 0.38 |
| arch | 0.01 | 0.01 | 0.01 | 0.01 |
| dumbbell | 0.10 | 0.16 | 0.18 | 0.23 |
| t_shape | 0.20 | 0.29 | 0.30 | 0.36 |
| l_shape | 0.20 | 0.34 | 0.37 | 0.46 |
| u_channel | 0.16 | 0.28 | 0.33 | 0.39 |
| plus | 0.08 | 0.17 | 0.20 | 0.30 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.90 | 0.92 | 0.76 | 0.44 |
| B_left | 0.94 | 0.86 | 0.61 | 0.31 |
| C_backright | 0.89 | 0.80 | 0.53 | 0.22 |
| D_far_turn | 0.83 | 0.71 | 0.43 | 0.18 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| standard | 0.87 | 0.83 | 0.58 | 0.26 |
| standard swapped | 0.88 | 0.87 | 0.59 | 0.34 |
| flank | 0.90 | 0.80 | 0.60 | 0.28 |
| flank swapped | 0.88 | 0.82 | 0.56 | 0.28 |
| goal_behind | 0.90 | 0.82 | 0.62 | 0.32 |
| goal_behind swapped | 0.92 | 0.81 | 0.54 | 0.26 |
