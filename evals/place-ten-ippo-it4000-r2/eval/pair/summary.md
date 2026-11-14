# Pair evaluation: place-ten-ippo-it4000-r2

policy: checkpoint logs/marl2/ippo_aa_kl_ten_s0/model_4000.pt (iteration 4000, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.87 | 0.84 | 0.02 | 0.02 | 17.4 | 0.09 | 0.43 | 0.38 | 0.15 | 0.27 | 0.71 |
| 40 kg | 0.84 | 0.77 | 0.03 | 0.05 | 23.3 | 0.10 | 0.51 | 0.44 | 0.22 | 0.34 | 0.71 |
| 60 kg | 0.59 | 0.53 | 0.07 | 0.09 | 32.2 | 0.10 | 0.55 | 0.48 | 0.25 | 0.35 | 0.69 |
| 80 kg | 0.28 | 0.23 | 0.11 | 0.13 | 34.1 | 0.10 | 0.59 | 0.50 | 0.28 | 0.37 | 0.68 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 1.00 | 0.96 | 0.54 | 0.07 |
| long | 0.96 | 0.97 | 0.76 | 0.36 |
| sphere | 0.96 | 0.99 | 0.97 | 0.96 |
| cylinder | 0.51 | 0.49 | 0.38 | 0.28 |
| arch | 0.57 | 0.53 | 0.18 | 0.01 |
| dumbbell | 0.94 | 0.81 | 0.53 | 0.07 |
| t_shape | 0.97 | 0.93 | 0.65 | 0.26 |
| l_shape (unseen) | 0.99 | 0.97 | 0.72 | 0.28 |
| u_channel (unseen) | 0.99 | 0.92 | 0.62 | 0.21 |
| plus (unseen) | 0.85 | 0.81 | 0.58 | 0.26 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.15 | 0.15 | 0.12 | 0.08 |
| long | 0.35 | 0.33 | 0.32 | 0.37 |
| sphere | 0.07 | 0.16 | 0.24 | 0.30 |
| cylinder | 0.21 | 0.34 | 0.37 | 0.34 |
| arch | 0.02 | 0.02 | 0.02 | 0.01 |
| dumbbell | 0.10 | 0.17 | 0.21 | 0.19 |
| t_shape | 0.21 | 0.30 | 0.30 | 0.37 |
| l_shape | 0.19 | 0.31 | 0.36 | 0.42 |
| u_channel | 0.16 | 0.25 | 0.31 | 0.42 |
| plus | 0.07 | 0.16 | 0.22 | 0.26 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.92 | 0.86 | 0.68 | 0.43 |
| B_left | 0.89 | 0.87 | 0.68 | 0.29 |
| C_backright | 0.89 | 0.87 | 0.51 | 0.19 |
| D_far_turn | 0.79 | 0.74 | 0.52 | 0.19 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| standard | 0.88 | 0.86 | 0.58 | 0.25 |
| standard swapped | 0.91 | 0.82 | 0.63 | 0.33 |
| flank | 0.87 | 0.87 | 0.63 | 0.30 |
| flank swapped | 0.85 | 0.85 | 0.57 | 0.25 |
| goal_behind | 0.88 | 0.85 | 0.59 | 0.27 |
| goal_behind swapped | 0.86 | 0.78 | 0.56 | 0.27 |
