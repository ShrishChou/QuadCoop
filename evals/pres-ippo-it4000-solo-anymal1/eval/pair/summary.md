# Pair evaluation: pres-ippo-it4000-solo-anymal1

policy: anymal1 alone, trained actor from checkpoint logs/marl2/ippo_aa_kl_ten_s0/model_4000.pt (iteration 4000, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.23 | 0.24 | 0.03 | 0.00 | 19.8 |  |  |  |  |  |  |
| 40 kg | 0.16 | 0.17 | 0.05 | 0.00 | 24.4 |  |  |  |  |  |  |
| 60 kg | 0.09 | 0.11 | 0.11 | 0.00 | 27.0 |  |  |  |  |  |  |
| 80 kg | 0.05 | 0.05 | 0.12 | 0.00 | 35.6 |  |  |  |  |  |  |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.17 | 0.25 | 0.08 | 0.00 |
| long | 0.17 | 0.08 | 0.00 | 0.00 |
| sphere | 0.58 | 0.58 | 0.58 | 0.42 |
| cylinder | 0.25 | 0.25 | 0.25 | 0.08 |
| arch | 0.00 | 0.00 | 0.00 | 0.00 |
| dumbbell | 0.25 | 0.17 | 0.00 | 0.00 |
| t_shape | 0.33 | 0.08 | 0.00 | 0.00 |
| l_shape (unseen) | 0.08 | 0.17 | 0.00 | 0.00 |
| u_channel (unseen) | 0.33 | 0.00 | 0.00 | 0.00 |
| plus (unseen) | 0.17 | 0.00 | 0.00 | 0.00 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.40 | 0.33 | 0.13 | 0.10 |
| B_left | 0.17 | 0.17 | 0.17 | 0.00 |
| C_backright | 0.03 | 0.03 | 0.03 | 0.07 |
| D_far_turn | 0.33 | 0.10 | 0.03 | 0.03 |
