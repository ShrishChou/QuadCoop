# Pair evaluation: handoff-aa-free-centre

policy: hand-off (script to the contact, then the frozen Stage 2b policy, never back), rule 'centre' (one robot), pair anymal

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 60 kg | 0.26 | 0.24 | 0.14 | 0.00 | 40.4 |  | 0.68 |  |  |  |  |
| 80 kg | 0.10 | 0.10 | 0.13 | 0.00 | 21.1 |  | 0.74 |  |  |  |  |



## success by object and mass

| object | contacts (A_straight, rep 0) | 60 kg | 80 kg |
|---|---|---|---|
| cube | part 0 -x | 0.58 | 0.08 |
| long | part 0 -x seg 1/2 | 0.33 | 0.00 |
| sphere | sector 225 | 1.00 | 0.92 |
| cylinder | part 0 -x seg 2/2 | 0.42 | 0.25 |
| arch | part 3 -x | 0.17 | 0.00 |
| dumbbell | part 2 -x seg 2/3 | 0.17 | 0.00 |
| t_shape | part 0 -x seg 2/3 | 0.00 | 0.00 |
| beam (unseen) | part 0 -x seg 3/5 | 0.00 | 0.00 |
| l_shape (unseen) | part 0 -x seg 2/2 | 0.00 | 0.00 |
| asym (unseen) | part 0 -x | 0.00 | 0.00 |
| u_channel (unseen) | part 0 -x seg 2/3 | 0.17 | 0.00 |
| plus (unseen) | part 1 -x | 0.25 | 0.00 |

## holding the assigned contact (while under the push policy)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 returns |
|---|---|---|---|---|
| 60 kg | 0.87 | 0.33 | 0.58 | 0.00 |
| 80 kg | 0.88 | 0.29 | 0.61 | 0.00 |

## success by scenario and mass

| scenario | 60 kg | 80 kg |
|---|---|---|
| A_straight | 0.39 | 0.19 |
| B_left | 0.22 | 0.08 |
| C_backright | 0.33 | 0.06 |
| D_far_turn | 0.08 | 0.08 |
