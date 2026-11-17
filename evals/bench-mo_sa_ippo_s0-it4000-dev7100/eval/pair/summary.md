# Pair evaluation: bench-mo_sa_ippo_s0-it4000-dev7100

policy: checkpoint logs/marl2/mo_sa_ippo_s0/model_4000.pt (iteration 4000, ippo, pair spot_arm)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest (the training rule); 3 placements per object x scenario x mass; nominal object sizes

## by mass

| mass | success | precise | spotarm1 fell | spotarm2 fell | time to success (s) | robots touching | spotarm1 pushing | spotarm2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.10 | 0.10 | 0.00 | 0.00 | 29.9 | 0.00 | 0.35 | 0.37 | 0.10 | 0.19 | 0.97 |
| 40 kg | 0.08 | 0.10 | 0.00 | 0.03 | 23.5 | 0.00 | 0.61 | 0.39 | 0.19 | 0.24 | 0.99 |
| 60 kg | 0.10 | 0.10 | 0.02 | 0.01 | 30.4 | 0.00 | 0.69 | 0.55 | 0.37 | 0.43 | 0.98 |
| 80 kg | 0.10 | 0.10 | 0.00 | 0.04 | 40.6 | 0.00 | 0.73 | 0.65 | 0.47 | 0.52 | 0.97 |

## success by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.08 | 0.00 | 0.00 | 0.00 |
| long | 0.00 | 0.00 | 0.00 | 0.00 |
| sphere | 0.67 | 0.83 | 1.00 | 1.00 |
| cylinder | 0.17 | 0.00 | 0.00 | 0.00 |
| arch | 0.08 | 0.00 | 0.00 | 0.00 |
| dumbbell | 0.00 | 0.00 | 0.00 | 0.00 |
| t_shape | 0.00 | 0.00 | 0.00 | 0.00 |
| l_shape (unseen) | 0.00 | 0.00 | 0.00 | 0.00 |
| u_channel (unseen) | 0.00 | 0.00 | 0.00 | 0.00 |
| plus (unseen) | 0.00 | 0.00 | 0.00 | 0.00 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.05 | 0.17 | 0.55 | 0.47 |
| long | 0.05 | 0.19 | 0.47 | 0.78 |
| sphere | 0.21 | 0.27 | 0.30 | 0.27 |
| cylinder | 0.21 | 0.42 | 0.53 | 0.42 |
| arch | 0.16 | 0.49 | 0.54 | 0.49 |
| dumbbell | 0.02 | 0.03 | 0.24 | 0.49 |
| t_shape | 0.04 | 0.13 | 0.32 | 0.49 |
| l_shape | 0.17 | 0.06 | 0.12 | 0.41 |
| u_channel | 0.06 | 0.07 | 0.41 | 0.57 |
| plus | 0.03 | 0.05 | 0.22 | 0.29 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.13 | 0.07 | 0.10 | 0.10 |
| B_left | 0.10 | 0.07 | 0.10 | 0.10 |
| C_backright | 0.07 | 0.10 | 0.10 | 0.10 |
| D_far_turn | 0.10 | 0.10 | 0.10 | 0.10 |
