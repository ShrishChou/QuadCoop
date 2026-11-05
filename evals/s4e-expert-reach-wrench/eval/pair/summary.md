# Pair evaluation: s4e-expert-reach-wrench

policy: Stage 4 contact policy logs/marl2/s4e_aa_s0/model_12000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.58 | 0.53 | 0.00 | 0.01 | 33.7 | 0.01 | 0.40 | 0.38 | 0.13 | 0.24 | 1.05 |
| 40 kg | 0.53 | 0.49 | 0.02 | 0.03 | 34.9 | 0.03 | 0.45 | 0.45 | 0.19 | 0.30 | 1.05 |
| 60 kg | 0.31 | 0.25 | 0.03 | 0.05 | 39.0 | 0.02 | 0.52 | 0.54 | 0.24 | 0.31 | 1.00 |
| 80 kg | 0.17 | 0.13 | 0.05 | 0.08 | 38.1 | 0.02 | 0.61 | 0.60 | 0.35 | 0.42 | 1.03 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x-y + part 0 corner -x+y | 0.58 | 0.67 | 0.33 | 0.00 |
| long | part 0 corner -x+y + part 0 -x seg 1/2 | 0.75 | 0.75 | 0.50 | 0.33 |
| sphere | sector 225 + sector 135 | 0.83 | 0.92 | 0.75 | 0.75 |
| cylinder | part 0 corner -x+y + part 0 -x seg 1/2 | 0.42 | 0.33 | 0.25 | 0.17 |
| arch | part 2 -x + part 3 -x | 0.58 | 0.58 | 0.42 | 0.25 |
| dumbbell | part 1 -x + part 0 -x | 0.42 | 0.33 | 0.17 | 0.17 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.58 | 0.58 | 0.50 | 0.08 |
| beam (unseen) | part 0 -x seg 4/5 + part 0 -x seg 2/5 | 0.33 | 0.33 | 0.00 | 0.00 |
| l_shape (unseen) | part 0 corner -x-y + part 1 -x | 0.75 | 0.75 | 0.33 | 0.00 |
| asym (unseen) | part 1 corner -x-y + part 0 -x | 0.67 | 0.42 | 0.00 | 0.00 |
| u_channel (unseen) | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.42 | 0.33 | 0.33 | 0.08 |
| plus (unseen) | part 1 corner -x+y + part 1 corner -x-y | 0.58 | 0.33 | 0.17 | 0.25 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.58 | 0.41 | 0.01 | 0.01 | 0.00 | 0.01 | 6.06 |
| 40 kg | 0.53 | 0.42 | 0.05 | 0.00 | 0.00 | 0.01 | 4.49 |
| 60 kg | 0.31 | 0.60 | 0.08 | 0.00 | 0.00 | 0.00 | 2.58 |
| 80 kg | 0.17 | 0.70 | 0.12 | 0.00 | 0.00 | 0.00 | 1.61 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.46 | 0.60 | 0.76 | 0.00 | 1.00 | 0.46 | 0.58 | 0.73 | 0.00 |
| 40 kg | 1.00 | 0.41 | 0.65 | 0.82 | 0.00 | 1.00 | 0.47 | 0.62 | 0.76 | 0.00 |
| 60 kg | 1.00 | 0.34 | 0.71 | 0.88 | 0.00 | 1.00 | 0.39 | 0.66 | 0.82 | 0.00 |
| 80 kg | 1.00 | 0.30 | 0.74 | 0.89 | 0.00 | 1.00 | 0.34 | 0.70 | 0.86 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change); object shoved in 0.5 of episodes

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.89 | 5.61 | 0.03 | 0.89 | 5.70 | 0.04 |
| 40 kg | 0.92 | 6.47 | 0.04 | 0.87 | 5.74 | 0.04 |
| 60 kg | 0.91 | 6.87 | 0.04 | 0.86 | 6.07 | 0.05 |
| 80 kg | 0.91 | 6.97 | 0.04 | 0.90 | 6.09 | 0.05 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.52 | 0.47 | 0.25 |
| 40 kg | 0.57 | 0.53 | 0.22 |
| 60 kg | 0.63 | 0.57 | 0.19 |
| 80 kg | 0.66 | 0.62 | 0.17 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|
| 20 kg | 9.49 | 0.32 | 32.26 | 6.06 | 0.00 | 0.00 | 0.00 | 0.44 |
| 40 kg | 9.90 | 0.42 | 29.92 | 4.49 | 0.00 | 0.00 | 0.00 | 0.36 |
| 60 kg | 8.21 | 0.48 | 30.42 | 2.58 | 0.00 | 0.00 | 0.00 | 0.32 |
| 80 kg | 7.01 | 0.52 | 28.96 | 1.61 | 0.00 | 0.00 | 0.00 | 0.31 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.07 | 0.05 | 0.11 | 0.21 |
| long | 0.06 | 0.21 | 0.35 | 0.49 |
| sphere | 0.18 | 0.27 | 0.30 | 0.26 |
| cylinder | 0.24 | 0.24 | 0.35 | 0.39 |
| arch | 0.15 | 0.16 | 0.21 | 0.31 |
| dumbbell | 0.14 | 0.13 | 0.15 | 0.20 |
| t_shape | 0.16 | 0.25 | 0.29 | 0.69 |
| beam | 0.16 | 0.34 | 0.34 | 0.43 |
| l_shape | 0.11 | 0.13 | 0.08 | 0.10 |
| asym | 0.17 | 0.25 | 0.32 | 0.53 |
| u_channel | 0.09 | 0.20 | 0.20 | 0.34 |
| plus | 0.05 | 0.06 | 0.15 | 0.19 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.72 | 0.75 | 0.50 | 0.36 |
| B_left | 0.58 | 0.53 | 0.25 | 0.11 |
| C_backright | 0.56 | 0.44 | 0.25 | 0.11 |
| D_far_turn | 0.44 | 0.39 | 0.25 | 0.11 |
