# Pair evaluation: cmp-sa_mappo_learned60_s0

policy: checkpoint logs/marl2/sa_mappo_learned60_s0/model_2000.pt (iteration 2000, mappo, pair spot_arm)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 12 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | spotarm1 fell | spotarm2 fell | time to success (s) | robots touching | spotarm1 pushing | spotarm2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.64 | 0.62 | 0.03 | 0.03 | 25.5 | 0.04 | 0.41 | 0.19 | 0.08 | 0.18 | 0.63 |
| 40 kg | 0.08 | 0.06 | 0.02 | 0.09 | 57.1 | 0.10 | 0.52 | 0.12 | 0.06 | 0.12 | 0.71 |

## success by object and mass

| object | 20 kg | 40 kg |
|---|---|---|
| long | 0.64 | 0.08 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg |
|---|---|---|
| long | 0.08 | 0.06 |

## success by scenario and mass

| scenario | 20 kg | 40 kg |
|---|---|---|
| A_straight | 0.92 | 0.04 |
| B_left | 0.83 | 0.00 |
| C_backright | 0.79 | 0.29 |
| D_far_turn | 0.00 | 0.00 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg |
|---|---|---|
| standard | 0.62 | 0.06 |
| standard swapped | 0.65 | 0.10 |
