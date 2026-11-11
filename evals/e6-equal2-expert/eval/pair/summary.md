# Pair evaluation: e6-equal2-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start at their contacts; contact rule re-applied: first)

success = 10 cm / 6 deg held 1 s within 20 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.26 | 0.22 | 0.01 | 0.00 | 5.6 | 0.07 | 0.44 | 0.48 | 0.31 | 0.51 | 0.93 |
| 40 kg | 0.27 | 0.22 | 0.01 | 0.00 | 6.7 | 0.06 | 0.58 | 0.59 | 0.40 | 0.53 | 0.95 |
| 60 kg | 0.26 | 0.19 | 0.00 | 0.01 | 8.5 | 0.05 | 0.66 | 0.67 | 0.48 | 0.57 | 0.96 |
| 80 kg | 0.17 | 0.13 | 0.01 | 0.01 | 9.4 | 0.05 | 0.75 | 0.76 | 0.60 | 0.66 | 0.94 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube |  | 0.17 | 0.08 | 0.08 | 0.00 |
| long |  | 0.17 | 0.00 | 0.00 | 0.00 |
| sphere |  | 1.00 | 1.00 | 1.00 | 0.92 |
| cylinder |  | 0.00 | 0.25 | 0.25 | 0.25 |
| arch |  | 0.50 | 0.50 | 0.50 | 0.08 |
| dumbbell |  | 0.33 | 0.42 | 0.33 | 0.33 |
| t_shape |  | 0.08 | 0.17 | 0.00 | 0.00 |
| beam (unseen) |  | 0.17 | 0.25 | 0.17 | 0.00 |
| l_shape (unseen) |  | 0.00 | 0.08 | 0.08 | 0.17 |
| asym (unseen) |  | 0.17 | 0.17 | 0.00 | 0.00 |
| u_channel (unseen) |  | 0.25 | 0.08 | 0.42 | 0.08 |
| plus (unseen) |  | 0.25 | 0.25 | 0.33 | 0.17 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.26 | 0.74 | 0.01 | 0.00 | 0.00 | 0.06 | 0.00 |
| 40 kg | 0.27 | 0.72 | 0.01 | 0.00 | 0.00 | 0.01 | 0.00 |
| 60 kg | 0.26 | 0.73 | 0.01 | 0.00 | 0.00 | 0.00 | 0.00 |
| 80 kg | 0.17 | 0.81 | 0.02 | 0.00 | 0.00 | 0.01 | 0.00 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.12 | 0.95 | 1.00 | 0.00 | 1.00 | 0.12 | 0.94 | 1.00 | 0.00 |
| 40 kg | 1.00 | 0.12 | 0.96 | 1.00 | 0.00 | 1.00 | 0.12 | 0.94 | 1.00 | 0.00 |
| 60 kg | 1.00 | 0.12 | 0.94 | 1.00 | 0.00 | 1.00 | 0.12 | 0.93 | 1.00 | 0.00 |
| 80 kg | 1.00 | 0.13 | 0.90 | 1.00 | 0.00 | 1.00 | 0.13 | 0.90 | 1.00 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.02 | 0.01 | 1.00 | 0.02 | 0.01 |
| 40 kg | 1.00 | 0.02 | 0.02 | 1.00 | 0.02 | 0.02 |
| 60 kg | 1.00 | 0.02 | 0.03 | 1.00 | 0.02 | 0.03 |
| 80 kg | 1.00 | 0.02 | 0.05 | 1.00 | 0.02 | 0.06 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.64 | 0.64 | 0.62 |
| 40 kg | 0.70 | 0.72 | 0.53 |
| 60 kg | 0.74 | 0.75 | 0.44 |
| 80 kg | 0.78 | 0.77 | 0.32 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.02 | 0.53 | 5.42 | 0.00 | 0.00 | 0.00 | 1.90 | 0.00 | 0.06 |
| 40 kg | 0.00 | 0.61 | 5.41 | 0.00 | 0.00 | 0.00 | 1.89 | 0.00 | 0.06 |
| 60 kg | 0.00 | 0.59 | 5.86 | 0.00 | 0.00 | 0.00 | 0.95 | 0.00 | 0.07 |
| 80 kg | 0.00 | 0.64 | 6.28 | 0.00 | 0.00 | 0.00 | 0.36 | 0.00 | 0.10 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 77 | 198 | 117 |
| 40 kg | 119 | 268 | 179 |
| 60 kg | 153 | 306 | 246 |
| 80 kg | 177 | 329 | 291 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 367 | 0.37 | 0.33 (44) | 0.41 (48) | 0.49 (148) | 0.54 (74) | 0.71 (54) |
| 40 kg | 666 | 0.30 | 0.20 (121) | 0.48 (90) | 0.49 (194) | 0.50 (114) | 0.76 (147) |
| 60 kg | 1008 | 0.29 | 0.27 (167) | 0.51 (154) | 0.50 (295) | 0.53 (209) | 0.77 (183) |
| 80 kg | 1394 | 0.28 | 0.21 (118) | 0.50 (195) | 0.50 (765) | 0.48 (201) | 0.78 (115) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.32 | 0.33 | 0.34 | 0.54 |
| long | 0.20 | 0.23 | 0.34 | 0.57 |
| sphere | 0.83 | 0.90 | 0.82 | 0.83 |
| cylinder | 0.10 | 0.32 | 0.37 | 0.29 |
| arch | 0.46 | 0.47 | 0.49 | 0.60 |
| dumbbell | 0.38 | 0.44 | 0.39 | 0.61 |
| t_shape | 0.18 | 0.28 | 0.52 | 0.76 |
| beam | 0.21 | 0.45 | 0.49 | 0.69 |
| l_shape | 0.15 | 0.22 | 0.34 | 0.48 |
| asym | 0.25 | 0.58 | 0.64 | 0.69 |
| u_channel | 0.28 | 0.24 | 0.51 | 0.59 |
| plus | 0.32 | 0.33 | 0.47 | 0.55 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| S_straight | 0.42 | 0.56 | 0.47 | 0.19 |
| S_side | 0.33 | 0.28 | 0.31 | 0.22 |
| S_moveturn | 0.08 | 0.11 | 0.11 | 0.08 |
| S_side_turn | 0.19 | 0.14 | 0.17 | 0.17 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 6% | 0% | 94% | 21% | 4% | 75% |  |  | 6% | 90% | 11% | 15% |
| 40 kg | 5% | 0% | 95% | 34% | 3% | 63% |  |  | 5% | 92% | 8% | 16% |
| 60 kg | 7% | 0% | 93% | 51% | 2% | 47% |  |  | 7% | 95% | 5% | 20% |
| 80 kg | 10% | 0% | 90% | 65% | 2% | 34% |  |  | 10% | 97% | 3% | 25% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 111 | 0.87 | 11% | 6% | 29% | 65% |
| 40 kg | 146 | 0.90 | 7% | 15% | 37% | 48% |
| 60 kg | 175 | 0.92 | 5% | 28% | 45% | 27% |
| 80 kg | 196 | 0.93 | 3% | 42% | 43% | 15% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 49% | 0.14 | 0.54 | 0.10 | 0.69 | 7 | 0 | 7 | 0 | 0 | 0 | 50 | 0.00 |  |
| 40 kg | 53% | 0.13 | 0.66 | 0.10 | 0.61 | 6 | 0 | 6 | 0 | 0 | 0 | 56 | 0.00 |  |
| 60 kg | 58% | 0.10 | 0.74 | 0.09 | 0.28 | 2 | 0 | 2 | 0 | 0 | 0 | 50 | 0.00 |  |
| 80 kg | 55% | 0.07 | 0.81 | 0.06 | 0.08 | 1 | 0 | 1 | 0 | 0 | 0 | 154 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.08 | 46% | 27% | 0.92 | 49% | 0.07 | 5 | 0 | 5 | 0 | 0 | 0 |
| long | 0.04 | 44% | 21% | 0.92 | 49% | 0.06 | 4 | 0 | 4 | 0 | 0 | 0 |
| sphere | 0.98 | 20% | 6% | 0.96 | 86% | 0.26 | 0 | 0 | 0 | 0 | 0 | 0 |
| cylinder | 0.19 | 32% | 9% | 0.88 | 67% | 0.05 | 4 | 0 | 4 | 0 | 0 | 0 |
| arch | 0.40 | 47% | 31% | 0.88 | 61% | 0.12 | 4 | 0 | 4 | 0 | 0 | 0 |
| dumbbell | 0.35 | 40% | 22% | 0.92 | 52% | 0.10 | 6 | 0 | 6 | 0 | 0 | 0 |
| t_shape | 0.06 | 50% | 27% | 0.88 | 53% | 0.06 | 4 | 0 | 4 | 0 | 0 | 0 |
| beam | 0.15 | 40% | 18% | 0.92 | 33% | 0.06 | 5 | 0 | 5 | 0 | 0 | 0 |
| l_shape | 0.08 | 40% | 21% | 0.93 | 42% | 0.06 | 6 | 0 | 6 | 0 | 0 | 0 |
| asym | 0.08 | 62% | 41% | 0.93 | 50% | 0.05 | 2 | 0 | 2 | 0 | 0 | 0 |
| u_channel | 0.21 | 43% | 24% | 0.92 | 48% | 0.08 | 6 | 0 | 6 | 0 | 0 | 0 |
| plus | 0.25 | 48% | 26% | 0.81 | 52% | 0.09 | 4 | 0 | 4 | 0 | 0 | 0 |
