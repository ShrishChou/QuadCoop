# Pair evaluation: team-aa-ippo-it4000-dev7100-heavy

policy: checkpoint logs/marl2/ippo_aa_kl_ten_s0/model_4000.pt (iteration 4000, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 100 kg | 0.15 | 0.17 | 0.14 | 0.12 | 21.9 | 0.10 | 0.63 | 0.48 | 0.30 | 0.41 | 0.64 |
| 120 kg | 0.12 | 0.12 | 0.14 | 0.14 | 15.5 | 0.10 | 0.62 | 0.53 | 0.32 | 0.40 | 0.65 |

## success by object and mass

| object | 100 kg | 120 kg |
|---|---|---|
| cube | 0.00 | 0.00 |
| long | 0.00 | 0.00 |
| sphere | 1.00 | 1.00 |
| cylinder | 0.25 | 0.25 |
| arch | 0.00 | 0.00 |
| dumbbell | 0.08 | 0.00 |
| t_shape | 0.00 | 0.00 |
| l_shape (unseen) | 0.08 | 0.00 |
| u_channel (unseen) | 0.00 | 0.00 |
| plus (unseen) | 0.08 | 0.00 |

## both robots pushing (share of time) by object and mass

| object | 100 kg | 120 kg |
|---|---|---|
| cube | 0.07 | 0.06 |
| long | 0.48 | 0.44 |
| sphere | 0.24 | 0.22 |
| cylinder | 0.42 | 0.41 |
| arch | 0.00 | 0.00 |
| dumbbell | 0.19 | 0.17 |
| t_shape | 0.41 | 0.45 |
| l_shape | 0.49 | 0.58 |
| u_channel | 0.32 | 0.31 |
| plus | 0.42 | 0.51 |

## success by scenario and mass

| scenario | 100 kg | 120 kg |
|---|---|---|
| A_straight | 0.20 | 0.20 |
| B_left | 0.17 | 0.10 |
| C_backright | 0.13 | 0.10 |
| D_far_turn | 0.10 | 0.10 |
