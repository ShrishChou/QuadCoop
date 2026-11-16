# Pair evaluation: cmp-sa_ippo_learned60_s0-armlock

policy: checkpoint logs/marl2/sa_ippo_learned60_s0/model_2000.pt (iteration 2000, ippo, pair spot_arm)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 12 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | spotarm1 fell | spotarm2 fell | time to success (s) | robots touching | spotarm1 pushing | spotarm2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.24 | 0.21 | 0.00 | 0.00 | 15.8 | 0.01 | 0.14 | 0.19 | 0.09 | 0.41 | 0.83 |
| 40 kg | 0.09 | 0.08 | 0.00 | 0.00 | 40.4 | 0.00 | 0.34 | 0.33 | 0.19 | 0.38 | 0.77 |

## success by object and mass

| object | 20 kg | 40 kg |
|---|---|---|
| long | 0.24 | 0.09 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg |
|---|---|---|
| long | 0.09 | 0.19 |

## success by scenario and mass

| scenario | 20 kg | 40 kg |
|---|---|---|
| A_straight | 0.71 | 0.33 |
| B_left | 0.25 | 0.04 |
| C_backright | 0.00 | 0.00 |
| D_far_turn | 0.00 | 0.00 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg |
|---|---|---|
| standard | 0.23 | 0.06 |
| standard swapped | 0.25 | 0.12 |
