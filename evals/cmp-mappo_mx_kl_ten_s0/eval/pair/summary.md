# Pair evaluation: cmp-mappo_mx_kl_ten_s0

policy: checkpoint logs/marl2/mappo_mx_kl_ten_s0/model_4000.pt (iteration 4000, mappo, pair mixed)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 12 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal fell | spot fell | time to success (s) | robots touching | anymal pushing | spot pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.94 | 0.93 | 0.00 | 0.06 | 17.0 | 0.03 | 0.64 | 0.35 | 0.22 | 0.32 | 0.64 |
| 40 kg | 0.92 | 0.84 | 0.01 | 0.04 | 22.7 | 0.03 | 0.71 | 0.43 | 0.31 | 0.40 | 0.65 |

## success by object and mass

| object | 20 kg | 40 kg |
|---|---|---|
| long | 0.94 | 0.92 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg |
|---|---|---|
| long | 0.22 | 0.31 |

## success by scenario and mass

| scenario | 20 kg | 40 kg |
|---|---|---|
| A_straight | 0.96 | 0.96 |
| B_left | 0.88 | 0.88 |
| C_backright | 0.96 | 0.96 |
| D_far_turn | 0.96 | 0.88 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg |
|---|---|---|
| standard | 0.94 | 0.90 |
| standard swapped | 0.94 | 0.94 |
