# Pair evaluation: place-nwF-ippo-mixstart-it5000

policy: checkpoint logs/marl2/nwF_ippo_uniform_mixstart_s0/model_5000.pt (iteration 5000, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.86 | 0.82 | 0.03 | 0.02 | 18.9 | 0.09 | 0.40 | 0.38 | 0.15 | 0.27 | 0.72 |
| 40 kg | 0.81 | 0.73 | 0.04 | 0.04 | 23.9 | 0.09 | 0.48 | 0.46 | 0.22 | 0.34 | 0.73 |
| 60 kg | 0.58 | 0.50 | 0.07 | 0.10 | 32.6 | 0.09 | 0.54 | 0.49 | 0.25 | 0.37 | 0.70 |
| 80 kg | 0.28 | 0.21 | 0.12 | 0.12 | 34.6 | 0.09 | 0.60 | 0.52 | 0.29 | 0.39 | 0.70 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.96 | 0.96 | 0.50 | 0.10 |
| long | 0.94 | 0.89 | 0.79 | 0.31 |
| sphere | 0.96 | 0.96 | 0.97 | 0.97 |
| cylinder | 0.56 | 0.54 | 0.28 | 0.17 |
| arch | 0.61 | 0.42 | 0.19 | 0.03 |
| dumbbell | 0.93 | 0.75 | 0.33 | 0.15 |
| t_shape | 0.94 | 0.92 | 0.71 | 0.24 |
| l_shape (unseen) | 0.99 | 0.94 | 0.82 | 0.33 |
| u_channel (unseen) | 0.96 | 0.93 | 0.69 | 0.24 |
| plus (unseen) | 0.76 | 0.78 | 0.50 | 0.22 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.17 | 0.15 | 0.12 | 0.10 |
| long | 0.31 | 0.33 | 0.35 | 0.39 |
| sphere | 0.06 | 0.15 | 0.22 | 0.28 |
| cylinder | 0.25 | 0.37 | 0.37 | 0.41 |
| arch | 0.01 | 0.02 | 0.01 | 0.00 |
| dumbbell | 0.09 | 0.15 | 0.20 | 0.19 |
| t_shape | 0.16 | 0.29 | 0.34 | 0.41 |
| l_shape | 0.19 | 0.33 | 0.39 | 0.48 |
| u_channel | 0.15 | 0.26 | 0.34 | 0.38 |
| plus | 0.07 | 0.13 | 0.20 | 0.30 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.92 | 0.87 | 0.68 | 0.43 |
| B_left | 0.88 | 0.83 | 0.61 | 0.31 |
| C_backright | 0.84 | 0.81 | 0.53 | 0.21 |
| D_far_turn | 0.80 | 0.72 | 0.49 | 0.15 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| standard | 0.85 | 0.82 | 0.62 | 0.24 |
| standard swapped | 0.89 | 0.84 | 0.54 | 0.37 |
| flank | 0.87 | 0.86 | 0.58 | 0.26 |
| flank swapped | 0.84 | 0.79 | 0.59 | 0.23 |
| goal_behind | 0.86 | 0.78 | 0.62 | 0.30 |
| goal_behind swapped | 0.86 | 0.76 | 0.53 | 0.25 |
