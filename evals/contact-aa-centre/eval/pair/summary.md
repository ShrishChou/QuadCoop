# Pair evaluation: contact-aa-centre

policy: scripted contacts, rule 'centre' (one robot), pair anymal

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.00 | 0.00 | 0.00 | 0.00 |  |  | 0.53 |  |  |  |  |
| 40 kg | 0.00 | 0.00 | 0.01 | 0.00 |  |  | 0.71 |  |  |  |  |
| 60 kg | 0.00 | 0.00 | 0.01 | 0.00 |  |  | 0.76 |  |  |  |  |
| 80 kg | 0.00 | 0.00 | 0.01 | 0.00 |  |  | 0.78 |  |  |  |  |



## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 -x | 0.00 | 0.00 | 0.00 | 0.00 |
| long | part 0 -x seg 1/2 | 0.00 | 0.00 | 0.00 | 0.00 |
| sphere | sector 225 | 0.00 | 0.00 | 0.00 | 0.00 |
| cylinder | part 0 -x seg 2/2 | 0.00 | 0.00 | 0.00 | 0.00 |
| arch | part 3 -x | 0.00 | 0.00 | 0.00 | 0.00 |
| dumbbell | part 2 -x seg 2/3 | 0.00 | 0.00 | 0.00 | 0.00 |
| t_shape | part 0 -x seg 2/3 | 0.00 | 0.00 | 0.00 | 0.00 |
| beam (unseen) | part 0 -x seg 3/5 | 0.00 | 0.00 | 0.00 | 0.00 |
| l_shape (unseen) | part 0 -x seg 2/2 | 0.00 | 0.00 | 0.00 | 0.00 |
| asym (unseen) | part 0 -x | 0.00 | 0.00 | 0.00 | 0.00 |
| u_channel (unseen) | part 0 -x seg 2/3 | 0.00 | 0.00 | 0.00 | 0.00 |
| plus (unseen) | part 1 -x | 0.00 | 0.00 | 0.00 | 0.00 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.00 | 0.00 | 0.00 | 0.00 |
| B_left | 0.00 | 0.00 | 0.00 | 0.00 |
| C_backright | 0.00 | 0.00 | 0.00 | 0.00 |
| D_far_turn | 0.00 | 0.00 | 0.00 | 0.00 |
