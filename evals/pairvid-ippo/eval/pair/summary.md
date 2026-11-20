# Pair evaluation: pairvid-ippo

policy: checkpoint logs/marl2/ippo_aa_kl_ten_s0/model_4000.pt (iteration 4000, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 1 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 40 kg | 0.81 | 0.81 | 0.04 | 0.06 | 23.8 | 0.11 | 0.60 | 0.41 | 0.24 | 0.35 | 0.69 |
| 80 kg | 0.19 | 0.17 | 0.15 | 0.12 | 25.0 | 0.10 | 0.65 | 0.47 | 0.32 | 0.43 | 0.61 |

## success by object and mass

| object | 40 kg | 80 kg |
|---|---|---|
| cube | 0.75 | 0.25 |
| long | 1.00 | 0.00 |
| sphere | 1.00 | 1.00 |
| cylinder | 0.25 | 0.25 |
| arch | 0.75 | 0.00 |
| dumbbell | 0.50 | 0.25 |
| t_shape | 1.00 | 0.00 |
| beam (unseen) | 0.75 | 0.00 |
| l_shape (unseen) | 1.00 | 0.25 |
| asym (unseen) | 0.75 | 0.00 |
| u_channel (unseen) | 1.00 | 0.00 |
| plus (unseen) | 1.00 | 0.25 |

## both robots pushing (share of time) by object and mass

| object | 40 kg | 80 kg |
|---|---|---|
| cube | 0.20 | 0.25 |
| long | 0.49 | 0.46 |
| sphere | 0.17 | 0.35 |
| cylinder | 0.32 | 0.41 |
| arch | 0.01 | 0.00 |
| dumbbell | 0.17 | 0.17 |
| t_shape | 0.31 | 0.30 |
| beam | 0.35 | 0.45 |
| l_shape | 0.05 | 0.36 |
| asym | 0.40 | 0.50 |
| u_channel | 0.30 | 0.24 |
| plus | 0.15 | 0.38 |

## success by scenario and mass

| scenario | 40 kg | 80 kg |
|---|---|---|
| A_straight | 0.83 | 0.42 |
| B_left | 0.92 | 0.08 |
| C_backright | 0.58 | 0.08 |
| D_far_turn | 0.92 | 0.17 |
