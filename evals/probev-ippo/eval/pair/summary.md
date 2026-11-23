# Pair evaluation: probev-ippo

policy: checkpoint logs/marl2/ippo_aa_kl_ten_s0/model_4000.pt (iteration 4000, ippo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 10 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.81 | 0.76 | 0.04 | 0.04 | 23.3 | 0.13 | 0.42 | 0.37 | 0.20 | 0.38 | 0.68 |
| 40 kg | 0.78 | 0.75 | 0.03 | 0.07 | 29.9 | 0.10 | 0.43 | 0.40 | 0.18 | 0.30 | 0.61 |
| 60 kg | 0.49 | 0.42 | 0.01 | 0.14 | 40.7 | 0.12 | 0.49 | 0.39 | 0.19 | 0.30 | 0.57 |
| 80 kg | 0.19 | 0.16 | 0.05 | 0.14 | 54.2 | 0.11 | 0.54 | 0.44 | 0.24 | 0.36 | 0.52 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| arch | 0.62 | 0.62 | 0.23 | 0.00 |
| long | 1.00 | 0.93 | 0.75 | 0.38 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| arch | 0.01 | 0.01 | 0.00 | 0.00 |
| long | 0.40 | 0.35 | 0.37 | 0.48 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.70 | 0.75 | 0.60 | 0.40 |
| B_left | 0.75 | 0.75 | 0.40 | 0.15 |
| C_backright | 1.00 | 0.90 | 0.60 | 0.10 |
| D_far_turn | 0.80 | 0.70 | 0.35 | 0.10 |
