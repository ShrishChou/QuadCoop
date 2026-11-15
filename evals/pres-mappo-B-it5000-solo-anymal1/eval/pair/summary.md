# Pair evaluation: pres-mappo-B-it5000-solo-anymal1

policy: anymal1 alone, trained actor from checkpoint logs/marl2/nwB_mappo_uniform_s0/model_5000.pt (iteration 5000, mappo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.04 | 0.04 | 0.01 | 0.00 | 37.5 |  |  |  |  |  |  |
| 40 kg | 0.11 | 0.12 | 0.04 | 0.00 | 43.1 |  |  |  |  |  |  |
| 60 kg | 0.02 | 0.02 | 0.11 | 0.00 | 40.9 |  |  |  |  |  |  |
| 80 kg | 0.00 | 0.00 | 0.12 | 0.00 |  |  |  |  |  |  |  |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.17 | 0.17 | 0.00 | 0.00 |
| long | 0.08 | 0.08 | 0.00 | 0.00 |
| sphere | 0.00 | 0.08 | 0.08 | 0.00 |
| cylinder | 0.00 | 0.17 | 0.00 | 0.00 |
| arch | 0.08 | 0.00 | 0.00 | 0.00 |
| dumbbell | 0.00 | 0.08 | 0.00 | 0.00 |
| t_shape | 0.00 | 0.17 | 0.00 | 0.00 |
| l_shape (unseen) | 0.00 | 0.00 | 0.00 | 0.00 |
| u_channel (unseen) | 0.00 | 0.17 | 0.08 | 0.00 |
| plus (unseen) | 0.08 | 0.17 | 0.00 | 0.00 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.07 | 0.20 | 0.00 | 0.00 |
| B_left | 0.03 | 0.17 | 0.07 | 0.00 |
| C_backright | 0.00 | 0.00 | 0.00 | 0.00 |
| D_far_turn | 0.07 | 0.07 | 0.00 | 0.00 |
