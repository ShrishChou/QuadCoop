# Pair evaluation: place-ten-ippo-it4000

policy: checkpoint logs/marl2/ippo_aa_kl_ten_s0/model_4000.pt (iteration 4000, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.89 | 0.84 | 0.02 | 0.03 | 17.5 | 0.10 | 0.44 | 0.37 | 0.16 | 0.28 | 0.71 |
| 40 kg | 0.81 | 0.76 | 0.03 | 0.04 | 22.4 | 0.11 | 0.51 | 0.44 | 0.22 | 0.34 | 0.71 |
| 60 kg | 0.59 | 0.50 | 0.09 | 0.10 | 33.2 | 0.10 | 0.56 | 0.48 | 0.25 | 0.36 | 0.69 |
| 80 kg | 0.26 | 0.23 | 0.11 | 0.13 | 33.3 | 0.10 | 0.60 | 0.49 | 0.28 | 0.38 | 0.68 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.99 | 0.94 | 0.58 | 0.08 |
| long | 0.96 | 0.93 | 0.79 | 0.35 |
| sphere | 0.99 | 0.99 | 0.97 | 0.92 |
| cylinder | 0.60 | 0.50 | 0.36 | 0.28 |
| arch | 0.60 | 0.39 | 0.24 | 0.01 |
| dumbbell | 0.93 | 0.76 | 0.47 | 0.10 |
| t_shape | 0.99 | 0.94 | 0.61 | 0.22 |
| l_shape (unseen) | 1.00 | 0.96 | 0.76 | 0.26 |
| u_channel (unseen) | 1.00 | 0.93 | 0.60 | 0.21 |
| plus (unseen) | 0.86 | 0.75 | 0.49 | 0.21 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.17 | 0.17 | 0.12 | 0.09 |
| long | 0.32 | 0.31 | 0.35 | 0.37 |
| sphere | 0.08 | 0.16 | 0.24 | 0.30 |
| cylinder | 0.22 | 0.34 | 0.40 | 0.34 |
| arch | 0.02 | 0.01 | 0.02 | 0.01 |
| dumbbell | 0.10 | 0.15 | 0.18 | 0.22 |
| t_shape | 0.21 | 0.31 | 0.31 | 0.35 |
| l_shape | 0.21 | 0.33 | 0.38 | 0.42 |
| u_channel | 0.18 | 0.25 | 0.32 | 0.39 |
| plus | 0.07 | 0.13 | 0.21 | 0.30 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.94 | 0.87 | 0.71 | 0.44 |
| B_left | 0.91 | 0.86 | 0.66 | 0.28 |
| C_backright | 0.90 | 0.82 | 0.49 | 0.18 |
| D_far_turn | 0.81 | 0.68 | 0.50 | 0.16 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| standard | 0.89 | 0.79 | 0.62 | 0.30 |
| standard swapped | 0.92 | 0.76 | 0.57 | 0.26 |
| flank | 0.91 | 0.84 | 0.58 | 0.27 |
| flank swapped | 0.88 | 0.85 | 0.57 | 0.27 |
| goal_behind | 0.85 | 0.83 | 0.66 | 0.25 |
| goal_behind swapped | 0.89 | 0.78 | 0.53 | 0.24 |
