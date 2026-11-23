# Pair evaluation: probev-mappo

policy: checkpoint logs/marl2/nwB_mappo_uniform_s0/model_5000.pt (iteration 5000, mappo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 10 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.82 | 0.75 | 0.01 | 0.03 | 23.3 | 0.09 | 0.35 | 0.37 | 0.14 | 0.27 | 0.75 |
| 40 kg | 0.71 | 0.65 | 0.01 | 0.14 | 27.9 | 0.08 | 0.37 | 0.42 | 0.15 | 0.25 | 0.70 |
| 60 kg | 0.38 | 0.34 | 0.10 | 0.11 | 36.2 | 0.10 | 0.40 | 0.42 | 0.16 | 0.25 | 0.58 |
| 80 kg | 0.17 | 0.16 | 0.07 | 0.14 | 47.8 | 0.09 | 0.44 | 0.45 | 0.14 | 0.21 | 0.57 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| arch | 0.65 | 0.42 | 0.12 | 0.00 |
| long | 1.00 | 1.00 | 0.62 | 0.35 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| arch | 0.02 | 0.01 | 0.01 | 0.00 |
| long | 0.27 | 0.29 | 0.31 | 0.28 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.80 | 0.65 | 0.40 | 0.25 |
| B_left | 0.70 | 0.65 | 0.40 | 0.25 |
| C_backright | 0.95 | 0.85 | 0.45 | 0.05 |
| D_far_turn | 0.85 | 0.70 | 0.25 | 0.15 |
