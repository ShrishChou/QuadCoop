# Pair evaluation: shared-init-AB-ippo-ten-it4000-fresh7500

policy: checkpoint logs/marl2/ippo_aa_kl_ten_s0/model_4000.pt (iteration 4000, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.88 | 0.85 | 0.03 | 0.02 | 18.1 | 0.09 | 0.43 | 0.36 | 0.15 | 0.27 | 0.71 |
| 40 kg | 0.80 | 0.74 | 0.05 | 0.05 | 22.6 | 0.10 | 0.50 | 0.44 | 0.21 | 0.33 | 0.70 |
| 60 kg | 0.58 | 0.49 | 0.10 | 0.10 | 34.0 | 0.10 | 0.55 | 0.46 | 0.25 | 0.36 | 0.69 |
| 80 kg | 0.28 | 0.25 | 0.12 | 0.14 | 35.1 | 0.10 | 0.61 | 0.51 | 0.29 | 0.39 | 0.68 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.96 | 0.96 | 0.57 | 0.14 |
| long | 0.90 | 0.86 | 0.68 | 0.35 |
| sphere | 0.97 | 0.97 | 0.94 | 0.93 |
| cylinder | 0.58 | 0.47 | 0.35 | 0.22 |
| arch | 0.75 | 0.42 | 0.17 | 0.01 |
| dumbbell | 0.90 | 0.76 | 0.39 | 0.06 |
| t_shape | 0.97 | 0.94 | 0.68 | 0.29 |
| l_shape (unseen) | 0.94 | 0.89 | 0.76 | 0.29 |
| u_channel (unseen) | 0.97 | 0.94 | 0.64 | 0.12 |
| plus (unseen) | 0.88 | 0.82 | 0.58 | 0.35 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.15 | 0.14 | 0.09 | 0.08 |
| long | 0.31 | 0.28 | 0.34 | 0.42 |
| sphere | 0.07 | 0.15 | 0.25 | 0.30 |
| cylinder | 0.22 | 0.35 | 0.36 | 0.37 |
| arch | 0.01 | 0.01 | 0.01 | 0.01 |
| dumbbell | 0.10 | 0.15 | 0.20 | 0.24 |
| t_shape | 0.21 | 0.32 | 0.34 | 0.37 |
| l_shape | 0.16 | 0.30 | 0.37 | 0.42 |
| u_channel | 0.19 | 0.29 | 0.32 | 0.42 |
| plus | 0.08 | 0.15 | 0.23 | 0.32 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.95 | 0.84 | 0.69 | 0.41 |
| B_left | 0.89 | 0.84 | 0.59 | 0.28 |
| C_backright | 0.87 | 0.82 | 0.58 | 0.25 |
| D_far_turn | 0.82 | 0.71 | 0.44 | 0.17 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| standard | 0.88 | 0.85 | 0.57 | 0.30 |
| standard swapped | 0.88 | 0.78 | 0.57 | 0.28 |
| flank | 0.89 | 0.78 | 0.56 | 0.28 |
| flank swapped | 0.90 | 0.79 | 0.61 | 0.27 |
| goal_behind | 0.88 | 0.80 | 0.55 | 0.28 |
| goal_behind swapped | 0.88 | 0.82 | 0.61 | 0.26 |
