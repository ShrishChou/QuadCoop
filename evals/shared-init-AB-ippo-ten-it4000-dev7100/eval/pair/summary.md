# Pair evaluation: shared-init-AB-ippo-ten-it4000-dev7100

policy: checkpoint logs/marl2/ippo_aa_kl_ten_s0/model_4000.pt (iteration 4000, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.87 | 0.85 | 0.02 | 0.03 | 17.5 | 0.10 | 0.43 | 0.38 | 0.16 | 0.28 | 0.71 |
| 40 kg | 0.82 | 0.75 | 0.05 | 0.04 | 23.0 | 0.10 | 0.50 | 0.45 | 0.22 | 0.34 | 0.71 |
| 60 kg | 0.58 | 0.52 | 0.09 | 0.08 | 32.3 | 0.10 | 0.55 | 0.46 | 0.24 | 0.35 | 0.69 |
| 80 kg | 0.29 | 0.23 | 0.11 | 0.13 | 35.5 | 0.10 | 0.60 | 0.50 | 0.28 | 0.37 | 0.69 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.97 | 0.94 | 0.58 | 0.11 |
| long | 0.94 | 0.96 | 0.72 | 0.38 |
| sphere | 0.90 | 0.97 | 0.97 | 0.94 |
| cylinder | 0.56 | 0.46 | 0.35 | 0.22 |
| arch | 0.67 | 0.56 | 0.24 | 0.03 |
| dumbbell | 0.97 | 0.78 | 0.38 | 0.11 |
| t_shape | 1.00 | 0.99 | 0.64 | 0.28 |
| l_shape (unseen) | 0.97 | 0.90 | 0.71 | 0.31 |
| u_channel (unseen) | 0.99 | 0.88 | 0.68 | 0.18 |
| plus (unseen) | 0.72 | 0.76 | 0.56 | 0.35 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.16 | 0.17 | 0.12 | 0.10 |
| long | 0.32 | 0.34 | 0.34 | 0.40 |
| sphere | 0.07 | 0.16 | 0.24 | 0.31 |
| cylinder | 0.26 | 0.31 | 0.33 | 0.33 |
| arch | 0.01 | 0.02 | 0.02 | 0.02 |
| dumbbell | 0.11 | 0.16 | 0.19 | 0.21 |
| t_shape | 0.22 | 0.32 | 0.30 | 0.35 |
| l_shape | 0.17 | 0.31 | 0.34 | 0.43 |
| u_channel | 0.18 | 0.25 | 0.33 | 0.38 |
| plus | 0.07 | 0.16 | 0.21 | 0.28 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.90 | 0.89 | 0.66 | 0.46 |
| B_left | 0.87 | 0.80 | 0.65 | 0.32 |
| C_backright | 0.88 | 0.87 | 0.54 | 0.18 |
| D_far_turn | 0.83 | 0.71 | 0.48 | 0.20 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| standard | 0.88 | 0.84 | 0.64 | 0.28 |
| standard swapped | 0.88 | 0.88 | 0.57 | 0.33 |
| flank | 0.87 | 0.81 | 0.62 | 0.33 |
| flank swapped | 0.84 | 0.78 | 0.58 | 0.26 |
| goal_behind | 0.88 | 0.84 | 0.58 | 0.27 |
| goal_behind swapped | 0.88 | 0.77 | 0.50 | 0.28 |
