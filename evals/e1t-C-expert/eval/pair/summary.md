# Pair evaluation: e1t-C-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: never); TASKS: turn in place (object at the goal position, heading off 15/30/60/90 deg, capped by symmetry)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.34 | 0.35 | 0.02 | 0.02 | 13.7 | 0.06 | 0.25 | 0.31 | 0.03 | 0.05 | 1.24 |
| 40 kg | 0.44 | 0.44 | 0.00 | 0.03 | 16.3 | 0.05 | 0.24 | 0.35 | 0.04 | 0.08 | 1.35 |
| 60 kg | 0.49 | 0.41 | 0.00 | 0.03 | 18.8 | 0.04 | 0.24 | 0.34 | 0.03 | 0.06 | 1.42 |
| 80 kg | 0.46 | 0.31 | 0.05 | 0.03 | 17.6 | 0.06 | 0.23 | 0.33 | 0.02 | 0.05 | 1.47 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube |  | 0.83 | 0.67 | 0.83 | 0.83 |
| long |  | 0.58 | 0.75 | 0.75 | 0.50 |
| sphere |  | 1.00 | 1.00 | 1.00 | 1.00 |
| cylinder |  | 0.25 | 0.50 | 0.25 | 0.17 |
| arch |  | 0.08 | 0.33 | 0.58 | 0.58 |
| dumbbell |  | 0.00 | 0.17 | 0.33 | 0.42 |
| t_shape |  | 0.00 | 0.00 | 0.00 | 0.00 |
| beam (unseen) |  | 0.50 | 0.58 | 0.58 | 0.33 |
| l_shape (unseen) |  | 0.08 | 0.25 | 0.33 | 0.33 |
| asym (unseen) |  | 0.17 | 0.50 | 0.50 | 0.58 |
| u_channel (unseen) |  | 0.25 | 0.08 | 0.00 | 0.25 |
| plus (unseen) |  | 0.33 | 0.42 | 0.67 | 0.50 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.34 | 0.62 | 0.04 | 0.00 | 0.00 | 0.17 | 0.00 |
| 40 kg | 0.44 | 0.53 | 0.03 | 0.00 | 0.00 | 0.11 | 0.00 |
| 60 kg | 0.49 | 0.48 | 0.03 | 0.00 | 0.00 | 0.04 | 0.00 |
| 80 kg | 0.46 | 0.46 | 0.08 | 0.00 | 0.00 | 0.03 | 0.00 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.42 | 0.64 | 0.82 | 0.00 | 1.00 | 0.45 | 0.57 | 0.77 | 0.00 |
| 40 kg | 1.00 | 0.41 | 0.63 | 0.80 | 0.00 | 1.00 | 0.42 | 0.60 | 0.78 | 0.00 |
| 60 kg | 1.00 | 0.42 | 0.61 | 0.81 | 0.00 | 1.00 | 0.40 | 0.61 | 0.80 | 0.00 |
| 80 kg | 1.00 | 0.44 | 0.60 | 0.78 | 0.00 | 1.00 | 0.41 | 0.59 | 0.78 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.85 | 6.34 | 0.02 | 0.82 | 6.95 | 0.04 |
| 40 kg | 0.85 | 6.64 | 0.04 | 0.85 | 6.86 | 0.05 |
| 60 kg | 0.85 | 7.26 | 0.06 | 0.85 | 6.73 | 0.06 |
| 80 kg | 0.85 | 7.09 | 0.07 | 0.85 | 5.87 | 0.08 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.51 | 0.49 | 0.59 |
| 40 kg | 0.50 | 0.53 | 0.51 |
| 60 kg | 0.50 | 0.56 | 0.40 |
| 80 kg | 0.48 | 0.53 | 0.33 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 2.14 | 0.38 | 22.26 | 0.00 | 0.00 | 0.00 | 15.65 | 0.00 | 0.40 |
| 40 kg | 2.14 | 0.40 | 21.03 | 0.00 | 0.00 | 0.00 | 15.25 | 0.00 | 0.39 |
| 60 kg | 2.77 | 0.42 | 19.92 | 0.00 | 0.00 | 0.00 | 12.27 | 0.00 | 0.38 |
| 80 kg | 2.59 | 0.39 | 19.14 | 0.00 | 0.00 | 0.00 | 9.69 | 0.00 | 0.44 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 83 | 199 | 161 |
| 40 kg | 120 | 260 | 232 |
| 60 kg | 143 | 294 | 276 |
| 80 kg | 166 | 322 | 311 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 481 | 0.36 | 0.51 (91) | 0.51 (65) | 0.49 (149) | 0.49 (85) | 0.61 (91) |
| 40 kg | 697 | 0.39 | 0.58 (152) | 0.49 (93) | 0.49 (218) | 0.55 (52) | 0.62 (181) |
| 60 kg | 1066 | 0.40 | 0.56 (250) | 0.53 (91) | 0.51 (336) | 0.49 (178) | 0.60 (211) |
| 80 kg | 1725 | 0.41 | 0.59 (378) | 0.48 (153) | 0.45 (717) | 0.38 (164) | 0.60 (314) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.04 | 0.08 | 0.00 | 0.00 |
| long | 0.01 | 0.00 | 0.00 | 0.00 |
| sphere | 0.00 | 0.00 | 0.00 | 0.00 |
| cylinder | 0.00 | 0.00 | 0.00 | 0.00 |
| arch | 0.00 | 0.00 | 0.01 | 0.01 |
| dumbbell | 0.00 | 0.00 | 0.01 | 0.01 |
| t_shape | 0.06 | 0.15 | 0.12 | 0.08 |
| beam | 0.00 | 0.00 | 0.00 | 0.01 |
| l_shape | 0.13 | 0.12 | 0.08 | 0.09 |
| asym | 0.04 | 0.07 | 0.09 | 0.04 |
| u_channel | 0.01 | 0.02 | 0.02 | 0.04 |
| plus | 0.02 | 0.00 | 0.00 | 0.01 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| T15 | 0.44 | 0.50 | 0.58 | 0.72 |
| T30 | 0.28 | 0.33 | 0.47 | 0.42 |
| T60 | 0.33 | 0.47 | 0.50 | 0.44 |
| T90 | 0.31 | 0.44 | 0.39 | 0.25 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 44% | 0% | 56% | 21% | 3% | 76% |  |  | 16% | 60% | 48% | 18% |
| 40 kg | 43% | 0% | 57% | 32% | 2% | 66% |  |  | 15% | 67% | 40% | 21% |
| 60 kg | 42% | 0% | 58% | 42% | 2% | 56% |  |  | 13% | 65% | 44% | 20% |
| 80 kg | 45% | 0% | 55% | 50% | 2% | 48% |  |  | 18% | 58% | 52% | 28% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 117 | 0.86 | 11% | 6% | 14% | 80% |
| 40 kg | 150 | 0.88 | 9% | 8% | 23% | 68% |
| 60 kg | 171 | 0.90 | 7% | 13% | 31% | 55% |
| 80 kg | 191 | 0.90 | 7% | 17% | 37% | 47% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 21% | 0.02 | -0.28 | 0.00 | 2.42 | 27 | 0 | 22 | 0 | 0 | 5 | 58 | 0.00 |  |
| 40 kg | 22% | 0.02 | -0.26 | 0.01 | 2.03 | 22 | 0 | 18 | 0 | 0 | 4 | 86 | 0.00 |  |
| 60 kg | 21% | 0.01 | -0.23 | 0.01 | 1.83 | 15 | 1 | 10 | 0 | 0 | 4 | 108 | 0.00 |  |
| 80 kg | 17% | 0.01 | -0.32 | 0.00 | 1.97 | 13 | 2 | 7 | 0 | 0 | 4 | 135 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.79 | 60% | 23% | 0.91 | 33% | 0.00 | 5 | 1 | 2 | 0 | 0 | 2 |
| long | 0.65 | 57% | 20% | 0.92 | 29% | 0.01 | 13 | 2 | 4 | 0 | 0 | 7 |
| sphere | 1.00 | 0% | 0% |  | 0% | -0.00 | 0 | 0 | 0 | 0 | 0 | 0 |
| cylinder | 0.29 | 14% | 3% | 0.94 | 23% | -0.00 | 15 | 0 | 7 | 0 | 0 | 8 |
| arch | 0.40 | 35% | 12% | 0.78 | 25% | 0.02 | 25 | 0 | 25 | 0 | 0 | 0 |
| dumbbell | 0.23 | 27% | 6% | 0.91 | 19% | 0.01 | 31 | 1 | 27 | 0 | 0 | 3 |
| t_shape | 0.00 | 34% | 7% | 0.86 | 13% | -0.00 | 25 | 2 | 14 | 0 | 0 | 9 |
| beam | 0.50 | 39% | 16% | 0.87 | 17% | 0.01 | 19 | 2 | 16 | 0 | 0 | 1 |
| l_shape | 0.25 | 31% | 10% | 0.93 | 17% | 0.00 | 33 | 2 | 29 | 0 | 0 | 3 |
| asym | 0.44 | 40% | 8% | 0.90 | 22% | 0.01 | 19 | 0 | 16 | 0 | 0 | 3 |
| u_channel | 0.15 | 27% | 9% | 0.94 | 17% | 0.00 | 28 | 1 | 27 | 0 | 0 | 1 |
| plus | 0.48 | 54% | 18% | 0.77 | 25% | 0.00 | 17 | 1 | 2 | 0 | 0 | 14 |
