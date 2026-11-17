# Pair evaluation: team-aa-mappo-it4000-dev7100-heavy

policy: checkpoint logs/marl2/mappo_aa_kl_ten_s0/model_4000.pt (iteration 4000, mappo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 100 kg | 0.16 | 0.16 | 0.17 | 0.10 | 24.0 | 0.12 | 0.56 | 0.62 | 0.33 | 0.40 | 0.65 |
| 120 kg | 0.11 | 0.11 | 0.11 | 0.08 | 14.2 | 0.10 | 0.54 | 0.67 | 0.33 | 0.40 | 0.63 |

## success by object and mass

| object | 100 kg | 120 kg |
|---|---|---|
| cube | 0.00 | 0.00 |
| long | 0.08 | 0.00 |
| sphere | 0.92 | 0.83 |
| cylinder | 0.25 | 0.25 |
| arch | 0.00 | 0.00 |
| dumbbell | 0.08 | 0.00 |
| t_shape | 0.00 | 0.00 |
| l_shape (unseen) | 0.25 | 0.00 |
| u_channel (unseen) | 0.00 | 0.00 |
| plus (unseen) | 0.00 | 0.00 |

## both robots pushing (share of time) by object and mass

| object | 100 kg | 120 kg |
|---|---|---|
| cube | 0.11 | 0.09 |
| long | 0.26 | 0.31 |
| sphere | 0.29 | 0.25 |
| cylinder | 0.47 | 0.42 |
| arch | 0.03 | 0.05 |
| dumbbell | 0.22 | 0.22 |
| t_shape | 0.50 | 0.50 |
| l_shape | 0.71 | 0.62 |
| u_channel | 0.34 | 0.44 |
| plus | 0.34 | 0.44 |

## success by scenario and mass

| scenario | 100 kg | 120 kg |
|---|---|---|
| A_straight | 0.30 | 0.20 |
| B_left | 0.10 | 0.03 |
| C_backright | 0.13 | 0.10 |
| D_far_turn | 0.10 | 0.10 |
