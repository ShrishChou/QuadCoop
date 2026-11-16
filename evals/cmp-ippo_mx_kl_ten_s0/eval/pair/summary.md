# Pair evaluation: cmp-ippo_mx_kl_ten_s0

policy: checkpoint logs/marl2/ippo_mx_kl_ten_s0/model_4000.pt (iteration 4000, ippo, pair mixed)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 12 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal fell | spot fell | time to success (s) | robots touching | anymal pushing | spot pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.97 | 0.94 | 0.00 | 0.03 | 15.7 | 0.03 | 0.65 | 0.36 | 0.21 | 0.31 | 0.65 |
| 40 kg | 0.94 | 0.83 | 0.02 | 0.02 | 20.5 | 0.03 | 0.75 | 0.40 | 0.29 | 0.37 | 0.64 |

## success by object and mass

| object | 20 kg | 40 kg |
|---|---|---|
| long | 0.97 | 0.94 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg |
|---|---|---|
| long | 0.21 | 0.29 |

## success by scenario and mass

| scenario | 20 kg | 40 kg |
|---|---|---|
| A_straight | 1.00 | 1.00 |
| B_left | 0.96 | 0.96 |
| C_backright | 0.96 | 0.96 |
| D_far_turn | 0.96 | 0.83 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg |
|---|---|---|
| standard | 0.96 | 0.94 |
| standard swapped | 0.98 | 0.94 |
