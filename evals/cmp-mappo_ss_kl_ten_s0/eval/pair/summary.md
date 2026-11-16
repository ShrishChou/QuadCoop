# Pair evaluation: cmp-mappo_ss_kl_ten_s0

policy: checkpoint logs/marl2/mappo_ss_kl_ten_s0/model_4000.pt (iteration 4000, mappo, pair spot)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 12 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | spot1 fell | spot2 fell | time to success (s) | robots touching | spot1 pushing | spot2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.90 | 0.85 | 0.04 | 0.04 | 21.0 | 0.01 | 0.54 | 0.60 | 0.34 | 0.49 | 0.63 |
| 40 kg | 0.81 | 0.78 | 0.06 | 0.10 | 22.4 | 0.01 | 0.68 | 0.70 | 0.47 | 0.55 | 0.63 |

## success by object and mass

| object | 20 kg | 40 kg |
|---|---|---|
| long | 0.90 | 0.81 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg |
|---|---|---|
| long | 0.34 | 0.47 |

## success by scenario and mass

| scenario | 20 kg | 40 kg |
|---|---|---|
| A_straight | 0.88 | 0.88 |
| B_left | 1.00 | 1.00 |
| C_backright | 0.83 | 0.54 |
| D_far_turn | 0.88 | 0.83 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg |
|---|---|---|
| standard | 0.88 | 0.90 |
| standard swapped | 0.92 | 0.73 |
