# Pair evaluation: s4e-expert-expert

policy: Stage 4 contact policy logs/marl2/s4e_aa_s0/model_12000.pt (robots start at their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.70 | 0.67 | 0.01 | 0.00 | 23.6 | 0.01 | 0.49 | 0.54 | 0.24 | 0.33 | 1.05 |
| 40 kg | 0.56 | 0.48 | 0.01 | 0.00 | 27.1 | 0.01 | 0.60 | 0.59 | 0.31 | 0.37 | 1.07 |
| 60 kg | 0.45 | 0.38 | 0.04 | 0.02 | 31.8 | 0.01 | 0.68 | 0.70 | 0.47 | 0.54 | 1.05 |
| 80 kg | 0.28 | 0.22 | 0.05 | 0.05 | 35.5 | 0.01 | 0.79 | 0.82 | 0.65 | 0.69 | 1.00 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x+y + part 0 corner -x-y | 0.75 | 0.75 | 0.75 | 0.00 |
| long | part 0 -x seg 2/2 + part 0 corner -x-y | 0.83 | 0.67 | 0.50 | 0.25 |
| sphere | sector 135 + sector 225 | 1.00 | 1.00 | 1.00 | 1.00 |
| cylinder | part 0 corner -x-y + part 0 -x seg 2/2 | 0.42 | 0.33 | 0.17 | 0.25 |
| arch | part 3 -x + part 2 -x | 0.58 | 0.58 | 0.67 | 0.33 |
| dumbbell | part 0 -x + part 1 -x | 0.58 | 0.50 | 0.58 | 0.42 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.67 | 0.75 | 0.17 | 0.17 |
| beam (unseen) | part 0 -x seg 2/5 + part 0 -x seg 4/5 | 0.83 | 0.42 | 0.00 | 0.00 |
| l_shape (unseen) | part 1 -x + part 0 corner -x-y | 0.67 | 0.58 | 0.50 | 0.00 |
| asym (unseen) | part 1 -x + part 0 corner -x+y | 0.58 | 0.08 | 0.08 | 0.00 |
| u_channel (unseen) | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.50 | 0.42 | 0.67 | 0.25 |
| plus (unseen) | part 0 corner -x-y + part 0 corner -x+y | 1.00 | 0.67 | 0.33 | 0.67 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.70 | 0.28 | 0.01 | 0.00 | 0.00 | 0.01 | 7.24 |
| 40 kg | 0.56 | 0.42 | 0.01 | 0.01 | 0.00 | 0.00 | 6.09 |
| 60 kg | 0.45 | 0.49 | 0.06 | 0.00 | 0.00 | 0.01 | 7.51 |
| 80 kg | 0.28 | 0.62 | 0.10 | 0.00 | 0.00 | 0.00 | 5.80 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.17 | 0.83 | 0.88 | 0.00 | 1.00 | 0.17 | 0.83 | 0.90 | 0.00 |
| 40 kg | 1.00 | 0.16 | 0.88 | 0.94 | 0.00 | 1.00 | 0.14 | 0.88 | 0.96 | 0.00 |
| 60 kg | 1.00 | 0.13 | 0.89 | 0.96 | 0.00 | 1.00 | 0.15 | 0.86 | 0.97 | 0.00 |
| 80 kg | 1.00 | 0.13 | 0.89 | 0.98 | 0.00 | 1.00 | 0.13 | 0.89 | 0.98 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.95 | 1.06 | 0.04 | 0.97 | 1.24 | 0.04 |
| 40 kg | 0.97 | 0.91 | 0.04 | 0.96 | 0.76 | 0.04 |
| 60 kg | 0.97 | 0.79 | 0.05 | 0.97 | 0.89 | 0.05 |
| 80 kg | 0.97 | 0.42 | 0.06 | 0.97 | 0.52 | 0.05 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.66 | 0.71 | 0.31 |
| 40 kg | 0.76 | 0.77 | 0.30 |
| 60 kg | 0.80 | 0.79 | 0.28 |
| 80 kg | 0.82 | 0.82 | 0.24 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.90 | 0.58 | 20.49 | 7.24 | 8.33 | 0.29 | 0.00 | 0.23 |
| 40 kg | 1.68 | 0.67 | 20.42 | 6.09 | 7.35 | 3.40 | 0.00 | 0.17 |
| 60 kg | 0.45 | 0.72 | 22.35 | 7.51 | 3.90 | 4.19 | 0.00 | 0.16 |
| 80 kg | 0.40 | 0.72 | 24.07 | 5.80 | 3.19 | 7.07 | 0.00 | 0.15 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.27 | 0.35 | 0.63 | 0.84 |
| long | 0.23 | 0.34 | 0.54 | 0.59 |
| sphere | 0.45 | 0.65 | 0.73 | 0.79 |
| cylinder | 0.14 | 0.22 | 0.46 | 0.61 |
| arch | 0.26 | 0.25 | 0.36 | 0.48 |
| dumbbell | 0.19 | 0.26 | 0.45 | 0.69 |
| t_shape | 0.36 | 0.46 | 0.51 | 0.76 |
| beam | 0.23 | 0.33 | 0.47 | 0.69 |
| l_shape | 0.19 | 0.23 | 0.34 | 0.60 |
| asym | 0.21 | 0.22 | 0.59 | 0.78 |
| u_channel | 0.21 | 0.27 | 0.36 | 0.62 |
| plus | 0.13 | 0.12 | 0.19 | 0.35 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.75 | 0.69 | 0.69 | 0.58 |
| B_left | 0.83 | 0.58 | 0.44 | 0.17 |
| C_backright | 0.58 | 0.53 | 0.44 | 0.22 |
| D_far_turn | 0.64 | 0.44 | 0.22 | 0.14 |
