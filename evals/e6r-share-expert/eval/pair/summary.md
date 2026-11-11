# Pair evaluation: e6r-share-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start at their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 20 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.47 | 0.33 | 0.01 | 0.01 | 8.4 | 0.07 | 0.47 | 0.50 | 0.36 | 0.60 | 0.93 |
| 40 kg | 0.51 | 0.28 | 0.01 | 0.00 | 9.2 | 0.06 | 0.57 | 0.60 | 0.44 | 0.62 | 0.97 |
| 60 kg | 0.38 | 0.22 | 0.01 | 0.01 | 9.6 | 0.04 | 0.68 | 0.71 | 0.54 | 0.65 | 0.97 |
| 80 kg | 0.19 | 0.17 | 0.01 | 0.01 | 9.2 | 0.05 | 0.75 | 0.77 | 0.62 | 0.70 | 0.93 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube |  | 0.50 | 0.58 | 0.42 | 0.00 |
| long |  | 0.67 | 0.75 | 0.25 | 0.00 |
| sphere |  | 1.00 | 1.00 | 1.00 | 1.00 |
| cylinder |  | 0.50 | 0.25 | 0.25 | 0.25 |
| arch |  | 0.75 | 0.67 | 0.58 | 0.08 |
| dumbbell |  | 0.42 | 0.75 | 0.50 | 0.33 |
| t_shape |  | 0.25 | 0.33 | 0.17 | 0.00 |
| beam (unseen) |  | 0.33 | 0.17 | 0.08 | 0.00 |
| l_shape (unseen) |  | 0.25 | 0.42 | 0.17 | 0.00 |
| asym (unseen) |  | 0.42 | 0.25 | 0.00 | 0.00 |
| u_channel (unseen) |  | 0.25 | 0.42 | 0.67 | 0.25 |
| plus (unseen) |  | 0.33 | 0.50 | 0.50 | 0.42 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.47 | 0.51 | 0.02 | 0.00 | 0.00 | 0.22 | 2.21 |
| 40 kg | 0.51 | 0.49 | 0.01 | 0.00 | 0.00 | 0.07 | 1.40 |
| 60 kg | 0.38 | 0.60 | 0.01 | 0.00 | 0.00 | 0.01 | 0.94 |
| 80 kg | 0.19 | 0.78 | 0.03 | 0.00 | 0.00 | 0.00 | 0.71 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.24 | 0.72 | 0.94 | 0.00 | 1.00 | 0.21 | 0.74 | 0.94 | 0.00 |
| 40 kg | 1.00 | 0.18 | 0.83 | 0.97 | 0.00 | 1.00 | 0.19 | 0.80 | 0.96 | 0.00 |
| 60 kg | 1.00 | 0.15 | 0.90 | 0.99 | 0.00 | 1.00 | 0.15 | 0.88 | 0.99 | 0.00 |
| 80 kg | 1.00 | 0.15 | 0.89 | 0.99 | 0.00 | 1.00 | 0.15 | 0.88 | 0.99 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.86 | 0.91 | 0.12 | 0.91 | 1.05 | 0.11 |
| 40 kg | 0.94 | 0.63 | 0.07 | 0.93 | 0.70 | 0.09 |
| 60 kg | 0.96 | 0.34 | 0.04 | 0.96 | 0.34 | 0.06 |
| 80 kg | 0.96 | 0.16 | 0.06 | 0.96 | 0.20 | 0.07 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.55 | 0.58 | 0.24 |
| 40 kg | 0.66 | 0.64 | 0.22 |
| 60 kg | 0.74 | 0.75 | 0.22 |
| 80 kg | 0.77 | 0.75 | 0.18 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.16 | 0.51 | 8.56 | 2.21 | 0.00 | 0.10 | 0.01 | 0.00 | 0.24 |
| 40 kg | 0.17 | 0.56 | 7.07 | 1.40 | 0.00 | 0.04 | 0.03 | 0.00 | 0.18 |
| 60 kg | 0.09 | 0.63 | 6.36 | 0.94 | 0.19 | 0.03 | 0.17 | 0.00 | 0.12 |
| 80 kg | 0.05 | 0.64 | 6.54 | 0.71 | 0.24 | 0.31 | 0.08 | 0.00 | 0.12 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 84 | 217 | 142 |
| 40 kg | 123 | 282 | 192 |
| 60 kg | 151 | 311 | 251 |
| 80 kg | 176 | 332 | 289 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 355 | 0.35 | 0.18 (28) | 0.35 (44) | 0.50 (193) | 0.66 (66) | 0.81 (24) |
| 40 kg | 605 | 0.32 | 0.22 (54) | 0.43 (106) | 0.49 (246) | 0.61 (143) | 0.74 (57) |
| 60 kg | 1046 | 0.29 | 0.27 (103) | 0.45 (215) | 0.50 (360) | 0.56 (259) | 0.74 (109) |
| 80 kg | 1318 | 0.29 | 0.22 (23) | 0.49 (196) | 0.50 (856) | 0.52 (218) | 0.75 (26) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.32 | 0.38 | 0.43 | 0.34 |
| long | 0.44 | 0.38 | 0.59 | 0.61 |
| sphere | 0.87 | 0.93 | 0.91 | 0.86 |
| cylinder | 0.22 | 0.29 | 0.40 | 0.47 |
| arch | 0.45 | 0.47 | 0.47 | 0.53 |
| dumbbell | 0.30 | 0.33 | 0.37 | 0.70 |
| t_shape | 0.29 | 0.37 | 0.51 | 0.80 |
| beam | 0.25 | 0.44 | 0.44 | 0.70 |
| l_shape | 0.22 | 0.39 | 0.53 | 0.65 |
| asym | 0.27 | 0.51 | 0.81 | 0.53 |
| u_channel | 0.28 | 0.39 | 0.51 | 0.64 |
| plus | 0.35 | 0.37 | 0.48 | 0.60 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| S_straight | 0.81 | 0.86 | 0.58 | 0.31 |
| S_side | 0.44 | 0.53 | 0.53 | 0.25 |
| S_moveturn | 0.22 | 0.22 | 0.19 | 0.08 |
| S_side_turn | 0.42 | 0.42 | 0.22 | 0.14 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 29% | 0% | 71% | 35% | 5% | 59% |  |  | 11% | 83% | 18% | 17% |
| 40 kg | 20% | 0% | 80% | 47% | 3% | 50% |  |  | 9% | 90% | 11% | 18% |
| 60 kg | 11% | 0% | 89% | 57% | 3% | 40% |  |  | 7% | 94% | 6% | 18% |
| 80 kg | 12% | 0% | 88% | 68% | 2% | 30% |  |  | 9% | 95% | 5% | 25% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 120 | 0.88 | 11% | 13% | 43% | 44% |
| 40 kg | 152 | 0.90 | 7% | 21% | 47% | 31% |
| 60 kg | 176 | 0.92 | 5% | 33% | 46% | 21% |
| 80 kg | 195 | 0.93 | 3% | 46% | 40% | 14% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 74% | 0.21 | 0.45 | 0.11 | 0.04 | 0 | 0 | 0 | 0 | 0 | 0 |  | 0.00 |  |
| 40 kg | 69% | 0.16 | 0.65 | 0.12 | 0.09 | 0 | 0 | 0 | 0 | 0 | 0 | 44 | 0.00 |  |
| 60 kg | 65% | 0.12 | 0.78 | 0.10 | 0.06 | 0 | 0 | 0 | 0 | 0 | 0 | 48 | 0.00 |  |
| 80 kg | 58% | 0.08 | 0.83 | 0.07 | 0.08 | 0 | 0 | 0 | 0 | 0 | 0 | 162 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.38 | 59% | 37% | 0.92 | 65% | 0.10 | 0 | 0 | 0 | 0 | 0 | 0 |
| long | 0.42 | 56% | 31% | 0.92 | 65% | 0.11 | 0 | 0 | 0 | 0 | 0 | 0 |
| sphere | 1.00 | 21% | 6% | 0.96 | 87% | 0.27 | 0 | 0 | 0 | 0 | 0 | 0 |
| cylinder | 0.31 | 39% | 13% | 0.87 | 80% | 0.09 | 0 | 0 | 0 | 0 | 0 | 0 |
| arch | 0.52 | 55% | 33% | 0.87 | 69% | 0.13 | 0 | 0 | 0 | 0 | 0 | 0 |
| dumbbell | 0.50 | 50% | 27% | 0.90 | 64% | 0.10 | 1 | 0 | 1 | 0 | 0 | 0 |
| t_shape | 0.19 | 58% | 33% | 0.90 | 63% | 0.07 | 0 | 0 | 0 | 0 | 0 | 0 |
| beam | 0.15 | 49% | 20% | 0.90 | 39% | 0.06 | 2 | 1 | 2 | 0 | 0 | 0 |
| l_shape | 0.21 | 55% | 30% | 0.92 | 66% | 0.06 | 0 | 0 | 0 | 0 | 0 | 0 |
| asym | 0.17 | 68% | 45% | 0.92 | 56% | 0.05 | 0 | 0 | 0 | 0 | 0 | 0 |
| u_channel | 0.40 | 55% | 31% | 0.92 | 72% | 0.08 | 0 | 0 | 0 | 0 | 0 | 0 |
| plus | 0.44 | 58% | 34% | 0.86 | 71% | 0.12 | 0 | 0 | 0 | 0 | 0 | 0 |
