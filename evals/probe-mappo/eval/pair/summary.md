# Pair evaluation: probe-mappo

policy: checkpoint logs/marl2/nwB_mappo_uniform_s0/model_5000.pt (iteration 5000, mappo, pair anymal)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 10 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.90 | 0.85 | 0.00 | 0.04 | 22.5 | 0.07 | 0.37 | 0.39 | 0.16 | 0.29 | 0.71 |
| 40 kg | 0.76 | 0.70 | 0.00 | 0.07 | 30.4 | 0.08 | 0.38 | 0.43 | 0.15 | 0.24 | 0.65 |
| 60 kg | 0.45 | 0.42 | 0.10 | 0.10 | 38.8 | 0.09 | 0.44 | 0.40 | 0.15 | 0.24 | 0.63 |
| 80 kg | 0.17 | 0.14 | 0.10 | 0.16 | 55.0 | 0.11 | 0.45 | 0.44 | 0.15 | 0.21 | 0.55 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| arch | 0.82 | 0.55 | 0.17 | 0.00 |
| long | 0.97 | 0.97 | 0.72 | 0.35 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| arch | 0.02 | 0.01 | 0.01 | 0.00 |
| long | 0.30 | 0.28 | 0.30 | 0.29 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.85 | 0.75 | 0.50 | 0.30 |
| B_left | 0.95 | 0.60 | 0.40 | 0.20 |
| C_backright | 0.95 | 1.00 | 0.55 | 0.05 |
| D_far_turn | 0.85 | 0.70 | 0.35 | 0.15 |
