# Pair evaluation: trio-smoke

policy: checkpoint logs/marl2/mappo_aa_kl_ten_s0/model_4000.pt (iteration 4000, mappo, pair anymal), run as a team of three (anymal3 uses anymal1's actor)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 1 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | anymal3 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | anymal3 pushing | two or more pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 40 kg | 0.62 | 0.62 | 0.00 | 0.38 | 0.00 | 22.3 | 0.81 | 0.21 | 0.19 | 0.55 | 0.17 | 0.27 | 0.56 |

## success by object and mass

| object | 40 kg |
|---|---|
| cube | 0.75 |
| long | 0.50 |

## both robots pushing (share of time) by object and mass

| object | 40 kg |
|---|---|
| cube | 0.12 |
| long | 0.23 |

## success by scenario and mass

| scenario | 40 kg |
|---|---|
| A_straight | 1.00 |
| B_left | 1.00 |
| C_backright | 0.50 |
| D_far_turn | 0.00 |
