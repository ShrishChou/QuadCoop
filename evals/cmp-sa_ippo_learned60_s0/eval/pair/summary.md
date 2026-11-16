# Pair evaluation: cmp-sa_ippo_learned60_s0

policy: checkpoint logs/marl2/sa_ippo_learned60_s0/model_2000.pt (iteration 2000, ippo, pair spot_arm)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 12 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | spotarm1 fell | spotarm2 fell | time to success (s) | robots touching | spotarm1 pushing | spotarm2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.29 | 0.29 | 0.02 | 0.01 | 23.1 | 0.01 | 0.16 | 0.16 | 0.07 | 0.31 | 0.82 |
| 40 kg | 0.08 | 0.08 | 0.02 | 0.00 | 48.4 | 0.01 | 0.27 | 0.32 | 0.12 | 0.25 | 0.78 |

## success by object and mass

| object | 20 kg | 40 kg |
|---|---|---|
| long | 0.29 | 0.08 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg |
|---|---|---|
| long | 0.07 | 0.12 |

## success by scenario and mass

| scenario | 20 kg | 40 kg |
|---|---|---|
| A_straight | 0.71 | 0.25 |
| B_left | 0.29 | 0.08 |
| C_backright | 0.00 | 0.00 |
| D_far_turn | 0.17 | 0.00 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg |
|---|---|---|
| standard | 0.27 | 0.04 |
| standard swapped | 0.31 | 0.12 |
