# Pair evaluation: cmp-ippo_ss_kl_ten_s0

policy: checkpoint logs/marl2/ippo_ss_kl_ten_s0/model_4000.pt (iteration 4000, ippo, pair spot)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 12 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | spot1 fell | spot2 fell | time to success (s) | robots touching | spot1 pushing | spot2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.96 | 0.90 | 0.02 | 0.02 | 16.5 | 0.00 | 0.60 | 0.53 | 0.34 | 0.48 | 0.65 |
| 40 kg | 0.86 | 0.85 | 0.06 | 0.07 | 20.7 | 0.00 | 0.68 | 0.65 | 0.45 | 0.54 | 0.66 |

## success by object and mass

| object | 20 kg | 40 kg |
|---|---|---|
| long | 0.96 | 0.86 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg |
|---|---|---|
| long | 0.34 | 0.45 |

## success by scenario and mass

| scenario | 20 kg | 40 kg |
|---|---|---|
| A_straight | 0.96 | 1.00 |
| B_left | 1.00 | 0.92 |
| C_backright | 0.92 | 0.67 |
| D_far_turn | 0.96 | 0.88 |

## success by start formation and mass (the tables above pool every formation)

| formation | 20 kg | 40 kg |
|---|---|---|
| standard | 0.98 | 0.79 |
| standard swapped | 0.94 | 0.94 |
