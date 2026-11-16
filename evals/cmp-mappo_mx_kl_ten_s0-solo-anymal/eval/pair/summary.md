# Pair evaluation: cmp-mappo_mx_kl_ten_s0-solo-anymal

policy: anymal alone, trained actor from checkpoint logs/marl2/mappo_mx_kl_ten_s0/model_4000.pt (iteration 4000, mappo, pair mixed)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 12 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal fell | spot fell | time to success (s) | robots touching | anymal pushing | spot pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.01 | 0.01 | 0.01 | 0.00 | 62.5 |  |  |  |  |  |  |
| 40 kg | 0.03 | 0.04 | 0.04 | 0.00 | 62.1 |  |  |  |  |  |  |

## success by object and mass

| object | 20 kg | 40 kg |
|---|---|---|
| long | 0.01 | 0.03 |

## success by scenario and mass

| scenario | 20 kg | 40 kg |
|---|---|---|
| A_straight | 0.04 | 0.04 |
| B_left | 0.00 | 0.00 |
| C_backright | 0.00 | 0.00 |
| D_far_turn | 0.00 | 0.08 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg |
|---|---|---|
| standard | 0.02 | 0.04 |
| standard swapped | 0.00 | 0.02 |
