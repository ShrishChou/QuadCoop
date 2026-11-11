# Pair evaluation: e6-share-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start at their contacts; contact rule re-applied: first)

success = 10 cm / 6 deg held 1 s within 20 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.32 | 0.26 | 0.00 | 0.00 | 5.5 | 0.08 | 0.52 | 0.54 | 0.37 | 0.54 | 0.93 |
| 40 kg | 0.35 | 0.22 | 0.00 | 0.00 | 6.8 | 0.07 | 0.65 | 0.61 | 0.46 | 0.59 | 0.95 |
| 60 kg | 0.28 | 0.21 | 0.01 | 0.01 | 8.2 | 0.05 | 0.69 | 0.73 | 0.54 | 0.63 | 0.97 |
| 80 kg | 0.19 | 0.15 | 0.02 | 0.02 | 9.7 | 0.04 | 0.80 | 0.81 | 0.65 | 0.69 | 0.95 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube |  | 0.25 | 0.25 | 0.08 | 0.00 |
| long |  | 0.33 | 0.33 | 0.25 | 0.00 |
| sphere |  | 0.92 | 1.00 | 1.00 | 0.92 |
| cylinder |  | 0.25 | 0.25 | 0.25 | 0.25 |
| arch |  | 0.50 | 0.50 | 0.50 | 0.08 |
| dumbbell |  | 0.33 | 0.33 | 0.33 | 0.33 |
| t_shape |  | 0.25 | 0.25 | 0.00 | 0.00 |
| beam (unseen) |  | 0.08 | 0.17 | 0.17 | 0.00 |
| l_shape (unseen) |  | 0.25 | 0.33 | 0.08 | 0.00 |
| asym (unseen) |  | 0.08 | 0.33 | 0.00 | 0.00 |
| u_channel (unseen) |  | 0.25 | 0.17 | 0.17 | 0.33 |
| plus (unseen) |  | 0.33 | 0.33 | 0.50 | 0.42 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.32 | 0.68 | 0.00 | 0.00 | 0.00 | 0.06 | 0.00 |
| 40 kg | 0.35 | 0.65 | 0.00 | 0.00 | 0.00 | 0.01 | 0.00 |
| 60 kg | 0.28 | 0.70 | 0.02 | 0.00 | 0.00 | 0.00 | 0.00 |
| 80 kg | 0.19 | 0.76 | 0.04 | 0.00 | 0.00 | 0.00 | 0.00 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.11 | 0.95 | 0.99 | 0.00 | 1.00 | 0.11 | 0.94 | 1.00 | 0.00 |
| 40 kg | 1.00 | 0.11 | 0.96 | 1.00 | 0.00 | 1.00 | 0.12 | 0.94 | 1.00 | 0.00 |
| 60 kg | 1.00 | 0.12 | 0.96 | 1.00 | 0.00 | 1.00 | 0.12 | 0.94 | 1.00 | 0.00 |
| 80 kg | 1.00 | 0.12 | 0.92 | 1.00 | 0.00 | 1.00 | 0.13 | 0.92 | 1.00 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.02 | 0.01 | 1.00 | 0.02 | 0.02 |
| 40 kg | 1.00 | 0.02 | 0.02 | 1.00 | 0.02 | 0.02 |
| 60 kg | 1.00 | 0.02 | 0.02 | 1.00 | 0.02 | 0.03 |
| 80 kg | 1.00 | 0.02 | 0.05 | 1.00 | 0.02 | 0.05 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.67 | 0.67 | 0.54 |
| 40 kg | 0.74 | 0.67 | 0.44 |
| 60 kg | 0.77 | 0.77 | 0.38 |
| 80 kg | 0.82 | 0.80 | 0.26 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.00 | 0.57 | 5.15 | 0.00 | 0.00 | 0.00 | 1.90 | 0.00 | 0.07 |
| 40 kg | 0.00 | 0.60 | 5.31 | 0.00 | 0.00 | 0.00 | 1.72 | 0.00 | 0.06 |
| 60 kg | 0.00 | 0.67 | 5.63 | 0.00 | 0.00 | 0.00 | 1.24 | 0.00 | 0.05 |
| 80 kg | 0.00 | 0.67 | 6.11 | 0.00 | 0.00 | 0.00 | 0.37 | 0.00 | 0.09 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 77 | 201 | 112 |
| 40 kg | 116 | 272 | 174 |
| 60 kg | 148 | 306 | 231 |
| 80 kg | 175 | 327 | 287 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 366 | 0.37 | 0.29 (34) | 0.36 (53) | 0.51 (178) | 0.61 (68) | 0.70 (33) |
| 40 kg | 639 | 0.33 | 0.30 (46) | 0.42 (117) | 0.49 (256) | 0.56 (137) | 0.68 (84) |
| 60 kg | 1088 | 0.31 | 0.35 (96) | 0.41 (222) | 0.49 (387) | 0.54 (255) | 0.70 (128) |
| 80 kg | 1447 | 0.29 | 0.29 (72) | 0.49 (246) | 0.50 (859) | 0.51 (214) | 0.70 (56) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.40 | 0.58 | 0.51 | 0.58 |
| long | 0.35 | 0.40 | 0.54 | 0.63 |
| sphere | 0.73 | 0.86 | 0.96 | 0.84 |
| cylinder | 0.26 | 0.27 | 0.37 | 0.37 |
| arch | 0.47 | 0.45 | 0.48 | 0.58 |
| dumbbell | 0.38 | 0.39 | 0.39 | 0.61 |
| t_shape | 0.30 | 0.34 | 0.46 | 0.80 |
| beam | 0.15 | 0.45 | 0.48 | 0.71 |
| l_shape | 0.42 | 0.46 | 0.48 | 0.59 |
| asym | 0.21 | 0.57 | 0.83 | 0.71 |
| u_channel | 0.35 | 0.35 | 0.43 | 0.72 |
| plus | 0.36 | 0.41 | 0.58 | 0.65 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| S_straight | 0.64 | 0.69 | 0.47 | 0.25 |
| S_side | 0.33 | 0.44 | 0.42 | 0.31 |
| S_moveturn | 0.06 | 0.08 | 0.08 | 0.06 |
| S_side_turn | 0.25 | 0.19 | 0.14 | 0.17 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 6% | 0% | 94% | 22% | 5% | 73% |  |  | 6% | 95% | 5% | 13% |
| 40 kg | 5% | 0% | 95% | 37% | 3% | 59% |  |  | 5% | 97% | 3% | 14% |
| 60 kg | 5% | 0% | 95% | 52% | 3% | 46% |  |  | 5% | 97% | 4% | 16% |
| 80 kg | 8% | 0% | 92% | 66% | 2% | 32% |  |  | 8% | 98% | 2% | 23% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 110 | 0.88 | 11% | 6% | 31% | 63% |
| 40 kg | 146 | 0.89 | 8% | 18% | 38% | 44% |
| 60 kg | 172 | 0.92 | 5% | 30% | 42% | 28% |
| 80 kg | 194 | 0.93 | 3% | 45% | 40% | 15% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 51% | 0.15 | 0.66 | 0.12 | 0.62 | 7 | 0 | 7 | 0 | 0 | 0 | 59 | 0.00 |  |
| 40 kg | 57% | 0.14 | 0.73 | 0.11 | 0.49 | 5 | 0 | 5 | 0 | 0 | 0 | 80 | 0.00 |  |
| 60 kg | 59% | 0.11 | 0.78 | 0.09 | 0.36 | 3 | 0 | 3 | 0 | 0 | 0 | 68 | 0.00 |  |
| 80 kg | 57% | 0.08 | 0.83 | 0.07 | 0.14 | 1 | 0 | 1 | 0 | 0 | 0 | 147 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.15 | 45% | 29% | 0.93 | 50% | 0.09 | 6 | 0 | 6 | 0 | 0 | 0 |
| long | 0.23 | 47% | 27% | 0.93 | 52% | 0.09 | 4 | 0 | 4 | 0 | 0 | 0 |
| sphere | 0.96 | 20% | 6% | 0.96 | 85% | 0.26 | 0 | 0 | 0 | 0 | 0 | 0 |
| cylinder | 0.25 | 30% | 8% | 0.87 | 68% | 0.08 | 4 | 0 | 4 | 0 | 0 | 0 |
| arch | 0.40 | 49% | 31% | 0.87 | 63% | 0.11 | 3 | 0 | 3 | 0 | 0 | 0 |
| dumbbell | 0.33 | 43% | 24% | 0.92 | 54% | 0.10 | 5 | 0 | 5 | 0 | 0 | 0 |
| t_shape | 0.12 | 52% | 29% | 0.88 | 55% | 0.07 | 3 | 0 | 3 | 0 | 0 | 0 |
| beam | 0.10 | 45% | 20% | 0.92 | 32% | 0.05 | 5 | 0 | 5 | 0 | 0 | 0 |
| l_shape | 0.17 | 46% | 24% | 0.92 | 54% | 0.08 | 4 | 0 | 4 | 0 | 0 | 0 |
| asym | 0.10 | 65% | 45% | 0.92 | 54% | 0.05 | 2 | 0 | 2 | 0 | 0 | 0 |
| u_channel | 0.23 | 40% | 24% | 0.91 | 47% | 0.09 | 7 | 0 | 7 | 0 | 0 | 0 |
| plus | 0.40 | 49% | 29% | 0.83 | 58% | 0.11 | 4 | 0 | 4 | 0 | 0 | 0 |
