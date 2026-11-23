# Pair evaluation: probe-ippo

policy: checkpoint logs/marl2/ippo_aa_kl_ten_s0/model_4000.pt (iteration 4000, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 10 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.75 | 0.70 | 0.03 | 0.11 | 21.0 | 0.16 | 0.41 | 0.36 | 0.20 | 0.40 | 0.72 |
| 40 kg | 0.75 | 0.68 | 0.03 | 0.10 | 27.4 | 0.13 | 0.43 | 0.41 | 0.21 | 0.36 | 0.64 |
| 60 kg | 0.44 | 0.36 | 0.04 | 0.19 | 37.5 | 0.10 | 0.44 | 0.43 | 0.19 | 0.31 | 0.56 |
| 80 kg | 0.17 | 0.11 | 0.11 | 0.14 | 50.5 | 0.11 | 0.50 | 0.45 | 0.24 | 0.37 | 0.54 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| arch | 0.55 | 0.53 | 0.15 | 0.03 |
| long | 0.95 | 0.97 | 0.72 | 0.33 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| arch | 0.00 | 0.01 | 0.01 | 0.01 |
| long | 0.40 | 0.41 | 0.37 | 0.48 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.70 | 0.75 | 0.50 | 0.45 |
| B_left | 0.65 | 0.65 | 0.45 | 0.10 |
| C_backright | 0.90 | 0.95 | 0.55 | 0.10 |
| D_far_turn | 0.75 | 0.65 | 0.25 | 0.05 |
