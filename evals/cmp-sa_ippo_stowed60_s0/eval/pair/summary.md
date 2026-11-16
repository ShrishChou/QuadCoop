# Pair evaluation: cmp-sa_ippo_stowed60_s0

policy: checkpoint logs/marl2/sa_ippo_stowed60_s0/model_2000.pt (iteration 2000, ippo, pair spot_arm)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 12 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | spotarm1 fell | spotarm2 fell | time to success (s) | robots touching | spotarm1 pushing | spotarm2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.90 | 0.78 | 0.01 | 0.00 | 36.2 | 0.02 | 0.35 | 0.33 | 0.17 | 0.37 | 0.72 |
| 40 kg | 0.22 | 0.19 | 0.01 | 0.01 | 55.4 | 0.05 | 0.51 | 0.54 | 0.36 | 0.55 | 0.68 |

## success by object and mass

| object | 20 kg | 40 kg |
|---|---|---|
| long | 0.90 | 0.22 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg |
|---|---|---|
| long | 0.17 | 0.36 |

## success by scenario and mass

| scenario | 20 kg | 40 kg |
|---|---|---|
| A_straight | 1.00 | 0.17 |
| B_left | 0.92 | 0.29 |
| C_backright | 1.00 | 0.42 |
| D_far_turn | 0.67 | 0.00 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg |
|---|---|---|
| standard | 0.98 | 0.25 |
| standard swapped | 0.81 | 0.19 |
