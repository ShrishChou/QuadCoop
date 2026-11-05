# Pair evaluation: s4e-expert-wrench

policy: Stage 4 contact policy logs/marl2/s4e_aa_s0/model_12000.pt (robots start at their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.67 | 0.56 | 0.00 | 0.01 | 26.2 | 0.03 | 0.50 | 0.47 | 0.25 | 0.39 | 0.97 |
| 40 kg | 0.60 | 0.52 | 0.01 | 0.01 | 30.2 | 0.01 | 0.52 | 0.57 | 0.29 | 0.39 | 0.99 |
| 60 kg | 0.34 | 0.28 | 0.03 | 0.02 | 33.2 | 0.01 | 0.57 | 0.66 | 0.34 | 0.40 | 0.97 |
| 80 kg | 0.22 | 0.18 | 0.03 | 0.05 | 34.9 | 0.01 | 0.65 | 0.71 | 0.42 | 0.46 | 0.93 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x-y + part 0 corner -x+y | 0.75 | 0.83 | 0.25 | 0.00 |
| long | part 0 corner -x+y + part 0 -x seg 1/2 | 0.58 | 0.83 | 0.42 | 0.33 |
| sphere | sector 225 + sector 135 | 1.00 | 0.92 | 1.00 | 0.92 |
| cylinder | part 0 corner -x+y + part 0 -x seg 1/2 | 0.58 | 0.33 | 0.17 | 0.25 |
| arch | part 2 -x + part 3 -x | 0.83 | 0.67 | 0.33 | 0.25 |
| dumbbell | part 1 -x + part 0 -x | 0.75 | 0.58 | 0.42 | 0.17 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.58 | 0.50 | 0.42 | 0.25 |
| beam (unseen) | part 0 -x seg 4/5 + part 0 -x seg 2/5 | 0.42 | 0.33 | 0.00 | 0.00 |
| l_shape (unseen) | part 0 corner -x-y + part 1 -x | 0.75 | 0.50 | 0.25 | 0.00 |
| asym (unseen) | part 1 corner -x-y + part 0 -x | 0.50 | 0.58 | 0.17 | 0.00 |
| u_channel (unseen) | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.67 | 0.58 | 0.25 | 0.08 |
| plus (unseen) | part 1 corner -x+y + part 1 corner -x-y | 0.67 | 0.58 | 0.42 | 0.42 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.67 | 0.32 | 0.01 | 0.00 | 0.00 | 0.00 | 7.08 |
| 40 kg | 0.60 | 0.38 | 0.02 | 0.00 | 0.00 | 0.01 | 5.14 |
| 60 kg | 0.34 | 0.60 | 0.06 | 0.00 | 0.00 | 0.00 | 2.80 |
| 80 kg | 0.22 | 0.69 | 0.08 | 0.00 | 0.00 | 0.00 | 1.89 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.30 | 0.74 | 0.80 | 0.00 | 1.00 | 0.28 | 0.75 | 0.83 | 0.00 |
| 40 kg | 1.00 | 0.28 | 0.77 | 0.84 | 0.00 | 1.00 | 0.26 | 0.79 | 0.88 | 0.00 |
| 60 kg | 1.00 | 0.19 | 0.85 | 0.90 | 0.00 | 1.00 | 0.27 | 0.79 | 0.90 | 0.00 |
| 80 kg | 1.00 | 0.19 | 0.87 | 0.93 | 0.00 | 1.00 | 0.20 | 0.84 | 0.93 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.94 | 1.83 | 0.04 | 0.96 | 1.98 | 0.03 |
| 40 kg | 0.93 | 1.85 | 0.04 | 0.95 | 1.64 | 0.04 |
| 60 kg | 0.94 | 0.90 | 0.04 | 0.95 | 1.50 | 0.05 |
| 80 kg | 0.96 | 0.66 | 0.04 | 0.94 | 0.58 | 0.04 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.62 | 0.63 | 0.26 |
| 40 kg | 0.66 | 0.68 | 0.24 |
| 60 kg | 0.73 | 0.72 | 0.20 |
| 80 kg | 0.78 | 0.75 | 0.18 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|
| 20 kg | 6.52 | 0.44 | 24.64 | 7.08 | 0.00 | 0.00 | 0.00 | 0.35 |
| 40 kg | 7.47 | 0.49 | 24.92 | 5.14 | 0.00 | 0.00 | 0.00 | 0.31 |
| 60 kg | 6.93 | 0.56 | 25.34 | 2.80 | 0.00 | 0.00 | 0.00 | 0.27 |
| 80 kg | 6.55 | 0.60 | 24.62 | 1.89 | 0.00 | 0.00 | 0.00 | 0.22 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.23 | 0.18 | 0.24 | 0.40 |
| long | 0.28 | 0.36 | 0.42 | 0.69 |
| sphere | 0.62 | 0.64 | 0.63 | 0.75 |
| cylinder | 0.30 | 0.46 | 0.48 | 0.59 |
| arch | 0.16 | 0.25 | 0.17 | 0.17 |
| dumbbell | 0.16 | 0.17 | 0.24 | 0.22 |
| t_shape | 0.37 | 0.41 | 0.59 | 0.83 |
| beam | 0.17 | 0.26 | 0.48 | 0.47 |
| l_shape | 0.10 | 0.08 | 0.06 | 0.08 |
| asym | 0.37 | 0.32 | 0.42 | 0.49 |
| u_channel | 0.15 | 0.26 | 0.23 | 0.25 |
| plus | 0.09 | 0.07 | 0.12 | 0.12 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.86 | 0.86 | 0.56 | 0.50 |
| B_left | 0.78 | 0.58 | 0.36 | 0.08 |
| C_backright | 0.58 | 0.56 | 0.22 | 0.17 |
| D_far_turn | 0.47 | 0.42 | 0.22 | 0.14 |
