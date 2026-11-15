# Pair evaluation: place-nwA-ippo-it5000-fresh7300

policy: checkpoint logs/marl2/nwA_ippo_uniform_s0/model_5000.pt (iteration 5000, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.86 | 0.83 | 0.02 | 0.02 | 18.2 | 0.08 | 0.39 | 0.40 | 0.15 | 0.26 | 0.72 |
| 40 kg | 0.80 | 0.74 | 0.05 | 0.05 | 23.5 | 0.09 | 0.49 | 0.47 | 0.22 | 0.33 | 0.72 |
| 60 kg | 0.57 | 0.49 | 0.09 | 0.10 | 35.1 | 0.09 | 0.53 | 0.48 | 0.23 | 0.33 | 0.71 |
| 80 kg | 0.28 | 0.23 | 0.12 | 0.12 | 35.7 | 0.09 | 0.58 | 0.54 | 0.28 | 0.38 | 0.71 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.96 | 0.92 | 0.61 | 0.14 |
| long | 0.89 | 0.88 | 0.64 | 0.38 |
| sphere | 0.97 | 1.00 | 0.96 | 0.94 |
| cylinder | 0.53 | 0.49 | 0.35 | 0.22 |
| arch | 0.68 | 0.35 | 0.18 | 0.00 |
| dumbbell | 0.89 | 0.82 | 0.42 | 0.12 |
| t_shape | 0.96 | 0.90 | 0.64 | 0.26 |
| l_shape (unseen) | 0.97 | 1.00 | 0.76 | 0.33 |
| u_channel (unseen) | 1.00 | 0.86 | 0.71 | 0.15 |
| plus (unseen) | 0.78 | 0.75 | 0.46 | 0.21 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.14 | 0.16 | 0.13 | 0.11 |
| long | 0.26 | 0.30 | 0.27 | 0.34 |
| sphere | 0.06 | 0.14 | 0.24 | 0.28 |
| cylinder | 0.25 | 0.39 | 0.36 | 0.33 |
| arch | 0.02 | 0.01 | 0.01 | 0.01 |
| dumbbell | 0.08 | 0.14 | 0.15 | 0.22 |
| t_shape | 0.20 | 0.27 | 0.29 | 0.42 |
| l_shape | 0.19 | 0.31 | 0.35 | 0.43 |
| u_channel | 0.18 | 0.28 | 0.32 | 0.37 |
| plus | 0.08 | 0.17 | 0.20 | 0.32 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.93 | 0.91 | 0.67 | 0.45 |
| B_left | 0.86 | 0.80 | 0.61 | 0.28 |
| C_backright | 0.85 | 0.76 | 0.58 | 0.20 |
| D_far_turn | 0.82 | 0.72 | 0.43 | 0.18 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| standard | 0.88 | 0.82 | 0.62 | 0.24 |
| standard swapped | 0.88 | 0.80 | 0.64 | 0.37 |
| flank | 0.86 | 0.77 | 0.56 | 0.27 |
| flank swapped | 0.86 | 0.80 | 0.55 | 0.27 |
| goal_behind | 0.86 | 0.80 | 0.55 | 0.25 |
| goal_behind swapped | 0.84 | 0.79 | 0.52 | 0.27 |
