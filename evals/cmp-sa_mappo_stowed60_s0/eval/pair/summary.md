# Pair evaluation: cmp-sa_mappo_stowed60_s0

policy: checkpoint logs/marl2/sa_mappo_stowed60_s0/model_2000.pt (iteration 2000, mappo, pair spot_arm)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 12 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | spotarm1 fell | spotarm2 fell | time to success (s) | robots touching | spotarm1 pushing | spotarm2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.60 | 0.53 | 0.03 | 0.01 | 35.1 | 0.10 | 0.15 | 0.33 | 0.04 | 0.10 | 0.55 |
| 40 kg | 0.23 | 0.14 | 0.06 | 0.03 | 50.4 | 0.18 | 0.12 | 0.53 | 0.07 | 0.13 | 0.57 |

## success by object and mass

| object | 20 kg | 40 kg |
|---|---|---|
| long | 0.60 | 0.23 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg |
|---|---|---|
| long | 0.04 | 0.07 |

## success by scenario and mass

| scenario | 20 kg | 40 kg |
|---|---|---|
| A_straight | 0.75 | 0.08 |
| B_left | 0.54 | 0.33 |
| C_backright | 0.71 | 0.50 |
| D_far_turn | 0.42 | 0.00 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg |
|---|---|---|
| standard | 0.67 | 0.10 |
| standard swapped | 0.54 | 0.35 |
