# Pair evaluation: pres-mappo-B-it5000-solo-anymal2

policy: anymal2 alone, trained actor from checkpoint logs/marl2/nwB_mappo_uniform_s0/model_5000.pt (iteration 5000, mappo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.37 | 0.41 | 0.00 | 0.02 | 32.5 |  |  |  |  |  |  |
| 40 kg | 0.14 | 0.13 | 0.00 | 0.08 | 31.2 |  |  |  |  |  |  |
| 60 kg | 0.07 | 0.08 | 0.00 | 0.07 | 38.4 |  |  |  |  |  |  |
| 80 kg | 0.01 | 0.01 | 0.00 | 0.09 | 44.1 |  |  |  |  |  |  |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.25 | 0.00 | 0.00 | 0.00 |
| long | 0.33 | 0.00 | 0.00 | 0.00 |
| sphere | 0.83 | 0.58 | 0.58 | 0.00 |
| cylinder | 0.08 | 0.17 | 0.00 | 0.08 |
| arch | 0.08 | 0.08 | 0.00 | 0.00 |
| dumbbell | 0.17 | 0.00 | 0.00 | 0.00 |
| t_shape | 0.75 | 0.17 | 0.08 | 0.00 |
| l_shape (unseen) | 0.33 | 0.17 | 0.00 | 0.00 |
| u_channel (unseen) | 0.67 | 0.25 | 0.00 | 0.00 |
| plus (unseen) | 0.17 | 0.00 | 0.00 | 0.00 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.27 | 0.17 | 0.10 | 0.03 |
| B_left | 0.33 | 0.13 | 0.03 | 0.00 |
| C_backright | 0.43 | 0.13 | 0.03 | 0.00 |
| D_far_turn | 0.43 | 0.13 | 0.10 | 0.00 |
