# Pair evaluation: sg-check

policy: checkpoint logs/marl2/nwB_mappo_uniform_s0/model_5000.pt (iteration 5000, mappo, pair anymal)

success = 10 cm / 6 deg held 1 s within 30 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 1 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 40 kg | 0.62 | 0.75 | 0.12 | 0.00 | 18.9 | 0.11 | 0.68 | 0.49 | 0.32 | 0.44 | 0.65 |

## success by object and mass

| object | 40 kg |
|---|---|
| cube | 1.00 |
| beam (unseen) | 0.25 |

## both robots pushing (share of time) by object and mass

| object | 40 kg |
|---|---|
| cube | 0.25 |
| beam | 0.40 |

## success by scenario and mass

| scenario | 40 kg |
|---|---|
| A_straight | 1.00 |
| B_left | 0.50 |
| C_backright | 0.50 |
| D_far_turn | 0.50 |
