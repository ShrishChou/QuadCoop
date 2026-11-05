# Pair evaluation: s4e-expert-reach-expert

policy: Stage 4 contact policy logs/marl2/s4e_aa_s0/model_12000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.68 | 0.65 | 0.00 | 0.00 | 27.4 | 0.00 | 0.49 | 0.42 | 0.16 | 0.24 | 1.05 |
| 40 kg | 0.51 | 0.44 | 0.03 | 0.02 | 30.0 | 0.00 | 0.59 | 0.45 | 0.22 | 0.28 | 1.08 |
| 60 kg | 0.39 | 0.34 | 0.04 | 0.03 | 33.6 | 0.00 | 0.68 | 0.56 | 0.35 | 0.42 | 1.05 |
| 80 kg | 0.20 | 0.17 | 0.10 | 0.04 | 36.1 | 0.01 | 0.76 | 0.68 | 0.53 | 0.60 | 1.02 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x+y + part 0 corner -x-y | 1.00 | 0.58 | 0.58 | 0.08 |
| long | part 0 -x seg 2/2 + part 0 corner -x-y | 0.75 | 0.58 | 0.50 | 0.25 |
| sphere | sector 135 + sector 225 | 1.00 | 1.00 | 1.00 | 0.83 |
| cylinder | part 0 corner -x-y + part 0 -x seg 2/2 | 0.42 | 0.08 | 0.17 | 0.17 |
| arch | part 3 -x + part 2 -x | 1.00 | 0.92 | 0.67 | 0.25 |
| dumbbell | part 0 -x + part 1 -x | 0.42 | 0.33 | 0.17 | 0.08 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.83 | 0.58 | 0.50 | 0.17 |
| beam (unseen) | part 0 -x seg 2/5 + part 0 -x seg 4/5 | 0.25 | 0.08 | 0.00 | 0.00 |
| l_shape (unseen) | part 1 -x + part 0 corner -x-y | 0.42 | 0.75 | 0.42 | 0.17 |
| asym (unseen) | part 1 -x + part 0 corner -x+y | 0.42 | 0.08 | 0.00 | 0.00 |
| u_channel (unseen) | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.75 | 0.42 | 0.25 | 0.17 |
| plus (unseen) | part 0 corner -x-y + part 0 corner -x+y | 0.92 | 0.67 | 0.42 | 0.25 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.68 | 0.31 | 0.00 | 0.01 | 0.00 | 0.01 | 8.47 |
| 40 kg | 0.51 | 0.44 | 0.05 | 0.01 | 0.00 | 0.00 | 7.00 |
| 60 kg | 0.39 | 0.53 | 0.08 | 0.00 | 0.00 | 0.01 | 8.06 |
| 80 kg | 0.20 | 0.66 | 0.14 | 0.00 | 0.00 | 0.00 | 6.11 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.23 | 0.77 | 0.86 | 0.00 | 1.00 | 0.24 | 0.75 | 0.88 | 0.00 |
| 40 kg | 1.00 | 0.20 | 0.81 | 0.92 | 0.00 | 1.00 | 0.19 | 0.82 | 0.91 | 0.00 |
| 60 kg | 1.00 | 0.17 | 0.84 | 0.94 | 0.00 | 1.00 | 0.20 | 0.83 | 0.93 | 0.00 |
| 80 kg | 1.00 | 0.18 | 0.81 | 0.96 | 0.00 | 1.00 | 0.19 | 0.83 | 0.94 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change); object shoved in 0.5 of episodes

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.83 | 2.34 | 0.04 | 0.79 | 2.15 | 0.03 |
| 40 kg | 0.81 | 2.02 | 0.04 | 0.78 | 2.11 | 0.03 |
| 60 kg | 0.82 | 1.94 | 0.05 | 0.78 | 1.91 | 0.03 |
| 80 kg | 0.78 | 2.10 | 0.06 | 0.76 | 2.40 | 0.04 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.62 | 0.63 | 0.30 |
| 40 kg | 0.69 | 0.68 | 0.31 |
| 60 kg | 0.75 | 0.72 | 0.28 |
| 80 kg | 0.73 | 0.76 | 0.26 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.28 | 0.53 | 24.92 | 8.47 | 7.23 | 0.42 | 0.00 | 0.25 |
| 40 kg | 1.06 | 0.60 | 24.80 | 7.00 | 4.96 | 3.26 | 0.00 | 0.19 |
| 60 kg | 0.46 | 0.65 | 26.73 | 8.06 | 2.94 | 5.29 | 0.00 | 0.16 |
| 80 kg | 0.34 | 0.66 | 25.83 | 6.11 | 1.67 | 8.03 | 0.00 | 0.18 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.15 | 0.13 | 0.51 | 0.60 |
| long | 0.20 | 0.31 | 0.50 | 0.51 |
| sphere | 0.25 | 0.32 | 0.38 | 0.58 |
| cylinder | 0.15 | 0.20 | 0.37 | 0.53 |
| arch | 0.17 | 0.18 | 0.22 | 0.32 |
| dumbbell | 0.15 | 0.25 | 0.36 | 0.52 |
| t_shape | 0.16 | 0.22 | 0.48 | 0.68 |
| beam | 0.06 | 0.25 | 0.27 | 0.56 |
| l_shape | 0.11 | 0.22 | 0.27 | 0.54 |
| asym | 0.22 | 0.15 | 0.39 | 0.63 |
| u_channel | 0.18 | 0.27 | 0.36 | 0.51 |
| plus | 0.14 | 0.11 | 0.15 | 0.40 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.75 | 0.67 | 0.67 | 0.50 |
| B_left | 0.75 | 0.39 | 0.28 | 0.08 |
| C_backright | 0.61 | 0.56 | 0.39 | 0.17 |
| D_far_turn | 0.61 | 0.42 | 0.22 | 0.06 |
