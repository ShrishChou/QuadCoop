# Pair evaluation: bench-mo_aa_mappo_s0-it4000-dev7100

policy: checkpoint logs/marl2/mo_aa_mappo_s0/model_4000.pt (iteration 4000, mappo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.27 | 0.34 | 0.04 | 0.05 | 15.0 | 0.02 | 0.32 | 0.29 | 0.12 | 0.27 | 0.91 |
| 40 kg | 0.25 | 0.26 | 0.05 | 0.08 | 17.3 | 0.02 | 0.35 | 0.29 | 0.13 | 0.28 | 0.96 |
| 60 kg | 0.23 | 0.24 | 0.08 | 0.07 | 24.8 | 0.03 | 0.44 | 0.35 | 0.15 | 0.26 | 0.96 |
| 80 kg | 0.10 | 0.09 | 0.14 | 0.17 | 21.2 | 0.03 | 0.49 | 0.37 | 0.16 | 0.25 | 0.94 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.83 | 0.58 | 0.50 | 0.08 |
| long | 0.25 | 0.25 | 0.25 | 0.00 |
| sphere | 0.75 | 1.00 | 1.00 | 0.75 |
| cylinder | 0.17 | 0.25 | 0.17 | 0.17 |
| arch | 0.25 | 0.17 | 0.25 | 0.00 |
| dumbbell | 0.00 | 0.08 | 0.00 | 0.00 |
| t_shape | 0.17 | 0.00 | 0.00 | 0.00 |
| l_shape (unseen) | 0.00 | 0.00 | 0.08 | 0.00 |
| u_channel (unseen) | 0.00 | 0.00 | 0.00 | 0.00 |
| plus (unseen) | 0.25 | 0.17 | 0.08 | 0.00 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.13 | 0.10 | 0.09 | 0.06 |
| long | 0.14 | 0.14 | 0.19 | 0.23 |
| sphere | 0.18 | 0.26 | 0.19 | 0.16 |
| cylinder | 0.05 | 0.13 | 0.29 | 0.25 |
| arch | 0.13 | 0.13 | 0.17 | 0.08 |
| dumbbell | 0.34 | 0.11 | 0.11 | 0.19 |
| t_shape | 0.05 | 0.07 | 0.07 | 0.10 |
| l_shape | 0.02 | 0.05 | 0.17 | 0.32 |
| u_channel | 0.10 | 0.14 | 0.11 | 0.09 |
| plus | 0.04 | 0.13 | 0.10 | 0.15 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.33 | 0.40 | 0.37 | 0.17 |
| B_left | 0.27 | 0.27 | 0.27 | 0.10 |
| C_backright | 0.13 | 0.10 | 0.13 | 0.10 |
| D_far_turn | 0.33 | 0.23 | 0.17 | 0.03 |
