# Pair evaluation: place-nwF-ippo-mixstart-it5000-fresh7300

policy: checkpoint logs/marl2/nwF_ippo_uniform_mixstart_s0/model_5000.pt (iteration 5000, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.85 | 0.81 | 0.03 | 0.02 | 18.5 | 0.09 | 0.40 | 0.39 | 0.15 | 0.27 | 0.71 |
| 40 kg | 0.82 | 0.75 | 0.04 | 0.04 | 23.5 | 0.09 | 0.49 | 0.46 | 0.22 | 0.34 | 0.70 |
| 60 kg | 0.60 | 0.50 | 0.08 | 0.09 | 34.4 | 0.09 | 0.53 | 0.50 | 0.26 | 0.37 | 0.70 |
| 80 kg | 0.29 | 0.23 | 0.10 | 0.12 | 35.3 | 0.09 | 0.58 | 0.52 | 0.29 | 0.39 | 0.70 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 1.00 | 0.94 | 0.54 | 0.18 |
| long | 0.85 | 0.94 | 0.78 | 0.38 |
| sphere | 0.89 | 0.99 | 1.00 | 0.99 |
| cylinder | 0.57 | 0.50 | 0.26 | 0.25 |
| arch | 0.64 | 0.42 | 0.14 | 0.00 |
| dumbbell | 0.88 | 0.82 | 0.38 | 0.12 |
| t_shape | 0.96 | 0.97 | 0.75 | 0.19 |
| l_shape (unseen) | 0.96 | 0.93 | 0.82 | 0.33 |
| u_channel (unseen) | 0.99 | 0.96 | 0.78 | 0.21 |
| plus (unseen) | 0.78 | 0.71 | 0.54 | 0.21 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.15 | 0.15 | 0.13 | 0.10 |
| long | 0.24 | 0.27 | 0.30 | 0.37 |
| sphere | 0.08 | 0.15 | 0.24 | 0.30 |
| cylinder | 0.25 | 0.36 | 0.45 | 0.33 |
| arch | 0.01 | 0.02 | 0.01 | 0.01 |
| dumbbell | 0.10 | 0.16 | 0.19 | 0.21 |
| t_shape | 0.19 | 0.30 | 0.33 | 0.38 |
| l_shape | 0.19 | 0.33 | 0.37 | 0.45 |
| u_channel | 0.16 | 0.26 | 0.33 | 0.41 |
| plus | 0.08 | 0.16 | 0.22 | 0.30 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.92 | 0.87 | 0.71 | 0.43 |
| B_left | 0.89 | 0.84 | 0.62 | 0.30 |
| C_backright | 0.85 | 0.84 | 0.61 | 0.23 |
| D_far_turn | 0.74 | 0.72 | 0.45 | 0.19 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| standard | 0.88 | 0.84 | 0.62 | 0.25 |
| standard swapped | 0.86 | 0.88 | 0.58 | 0.33 |
| flank | 0.86 | 0.78 | 0.63 | 0.29 |
| flank swapped | 0.85 | 0.83 | 0.59 | 0.33 |
| goal_behind | 0.82 | 0.79 | 0.58 | 0.25 |
| goal_behind swapped | 0.84 | 0.79 | 0.58 | 0.26 |
