# Pair evaluation: pair-regress

policy: checkpoint logs/marl2/mappo_aa_kl_ten_s0/model_4000.pt (iteration 4000, mappo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 40 kg | 1.00 | 1.00 | 0.00 | 0.00 | 21.3 | 0.22 | 0.58 | 0.46 | 0.12 | 0.15 | 0.50 |

## success by object and mass

| object | 40 kg |
|---|---|
| cube | 1.00 |

## both robots pushing (share of time) by object and mass

| object | 40 kg |
|---|---|
| cube | 0.12 |

## success by scenario and mass

| scenario | 40 kg |
|---|---|
| A_straight | 1.00 |
| B_left | 1.00 |
| C_backright | 1.00 |
| D_far_turn | 1.00 |
