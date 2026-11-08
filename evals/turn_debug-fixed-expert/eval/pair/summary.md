# Pair evaluation: turn_debug-fixed-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start at their contacts; contact rule re-applied: never); TASKS: turn in place (object at the goal position, heading off 15/30/60/90 deg, capped by symmetry)

success = 10 cm / 6 deg held 1 s within 30 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.44 | 0.57 | 0.00 | 0.00 | 3.1 | 0.00 | 0.33 | 0.40 | 0.01 | 0.02 | 1.34 |
| 40 kg | 0.62 | 0.66 | 0.00 | 0.01 | 4.2 | 0.00 | 0.34 | 0.42 | 0.01 | 0.02 | 1.46 |
| 60 kg | 0.64 | 0.55 | 0.00 | 0.01 | 7.3 | 0.00 | 0.32 | 0.45 | 0.01 | 0.02 | 1.48 |
| 80 kg | 0.53 | 0.29 | 0.01 | 0.01 | 9.2 | 0.00 | 0.34 | 0.42 | 0.01 | 0.01 | 1.54 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube |  | 1.00 | 0.83 | 0.50 | 0.42 |
| long |  | 0.75 | 0.75 | 0.75 | 0.50 |
| sphere |  | 0.83 | 0.92 | 1.00 | 1.00 |
| cylinder |  | 0.33 | 0.17 | 0.17 | 0.17 |
| arch |  | 0.25 | 0.58 | 0.75 | 0.50 |
| dumbbell |  | 0.83 | 0.92 | 0.92 | 0.83 |
| t_shape |  | 0.08 | 0.33 | 0.58 | 0.50 |
| beam (unseen) |  | 0.58 | 0.75 | 0.58 | 0.25 |
| l_shape (unseen) |  | 0.25 | 0.67 | 0.67 | 0.42 |
| asym (unseen) |  | 0.08 | 0.67 | 0.75 | 0.58 |
| u_channel (unseen) |  | 0.00 | 0.17 | 0.08 | 0.42 |
| plus (unseen) |  | 0.33 | 0.75 | 0.92 | 0.75 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.44 | 0.56 | 0.00 | 0.00 | 0.00 | 0.02 | 0.00 |
| 40 kg | 0.62 | 0.36 | 0.01 | 0.00 | 0.00 | 0.01 | 0.00 |
| 60 kg | 0.64 | 0.35 | 0.01 | 0.00 | 0.00 | 0.00 | 0.00 |
| 80 kg | 0.53 | 0.45 | 0.02 | 0.00 | 0.00 | 0.01 | 0.00 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.12 | 0.93 | 0.98 | 0.00 | 1.00 | 0.10 | 0.94 | 0.99 | 0.00 |
| 40 kg | 1.00 | 0.11 | 0.92 | 0.98 | 0.00 | 1.00 | 0.10 | 0.94 | 1.00 | 0.00 |
| 60 kg | 1.00 | 0.11 | 0.93 | 1.00 | 0.00 | 1.00 | 0.10 | 0.94 | 1.00 | 0.00 |
| 80 kg | 1.00 | 0.11 | 0.92 | 1.00 | 0.00 | 1.00 | 0.10 | 0.94 | 1.00 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.02 | 0.04 | 1.00 | 0.02 | 0.04 |
| 40 kg | 1.00 | 0.02 | 0.07 | 1.00 | 0.02 | 0.04 |
| 60 kg | 1.00 | 0.02 | 0.06 | 1.00 | 0.02 | 0.05 |
| 80 kg | 1.00 | 0.02 | 0.06 | 1.00 | 0.02 | 0.06 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.64 | 0.76 | 0.59 |
| 40 kg | 0.69 | 0.83 | 0.42 |
| 60 kg | 0.74 | 0.84 | 0.30 |
| 80 kg | 0.74 | 0.83 | 0.20 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.00 | 0.58 | 7.68 | 0.00 | 0.00 | 0.00 | 6.19 | 0.00 | 0.18 |
| 40 kg | 0.00 | 0.64 | 5.51 | 0.00 | 0.00 | 0.00 | 5.44 | 0.00 | 0.14 |
| 60 kg | 0.00 | 0.67 | 5.61 | 0.00 | 0.00 | 0.00 | 4.66 | 0.00 | 0.10 |
| 80 kg | 0.00 | 0.68 | 6.22 | 0.00 | 0.00 | 0.00 | 5.15 | 0.00 | 0.10 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 101 | 245 | 211 |
| 40 kg | 136 | 295 | 273 |
| 60 kg | 163 | 318 | 306 |
| 80 kg | 177 | 323 | 318 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 361 | 0.38 | 0.51 (60) | 0.53 (27) | 0.48 (149) | 0.47 (57) | 0.58 (67) |
| 40 kg | 605 | 0.40 | 0.53 (157) | 0.51 (39) | 0.48 (243) | 0.49 (55) | 0.56 (111) |
| 60 kg | 1008 | 0.39 | 0.57 (212) | 0.54 (81) | 0.48 (474) | 0.45 (132) | 0.58 (108) |
| 80 kg | 1362 | 0.36 | 0.57 (143) | 0.59 (93) | 0.46 (875) | 0.49 (165) | 0.57 (87) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.01 | 0.00 | 0.00 | 0.00 |
| long | 0.03 | 0.01 | 0.01 | 0.00 |
| sphere | 0.00 | 0.00 | 0.00 | 0.00 |
| cylinder | 0.00 | 0.00 | 0.00 | 0.00 |
| arch | 0.01 | 0.00 | 0.01 | 0.01 |
| dumbbell | 0.00 | 0.00 | 0.00 | 0.03 |
| t_shape | 0.00 | 0.03 | 0.05 | 0.01 |
| beam | 0.00 | 0.01 | 0.01 | 0.00 |
| l_shape | 0.09 | 0.08 | 0.05 | 0.01 |
| asym | 0.02 | 0.01 | 0.00 | 0.00 |
| u_channel | 0.00 | 0.00 | 0.00 | 0.00 |
| plus | 0.00 | 0.00 | 0.01 | 0.00 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| T15 | 0.64 | 0.78 | 0.92 | 0.97 |
| T30 | 0.31 | 0.56 | 0.67 | 0.56 |
| T60 | 0.47 | 0.69 | 0.64 | 0.42 |
| T90 | 0.36 | 0.47 | 0.33 | 0.17 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 17% | 0% | 83% | 30% | 3% | 67% |  |  | 17% | 39% | 66% | 16% |
| 40 kg | 14% | 0% | 86% | 45% | 2% | 52% |  |  | 14% | 42% | 60% | 14% |
| 60 kg | 10% | 0% | 90% | 53% | 2% | 45% |  |  | 10% | 60% | 41% | 14% |
| 80 kg | 9% | 0% | 91% | 58% | 1% | 41% |  |  | 9% | 68% | 34% | 17% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 136 | 0.91 | 6% | 14% | 27% | 59% |
| 40 kg | 169 | 0.93 | 4% | 27% | 35% | 38% |
| 60 kg | 188 | 0.93 | 4% | 34% | 39% | 27% |
| 80 kg | 198 | 0.93 | 4% | 38% | 40% | 22% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 49% | 0.05 | -0.22 | 0.03 | 0.55 | 5 | 0 | 5 | 0 | 0 | 0 | 47 | 0.00 |  |
| 40 kg | 56% | 0.05 | -0.24 | 0.04 | 0.25 | 2 | 0 | 2 | 0 | 0 | 0 | 72 | 0.00 |  |
| 60 kg | 49% | 0.03 | -0.31 | 0.02 | 0.30 | 2 | 0 | 1 | 0 | 0 | 0 | 115 | 0.00 |  |
| 80 kg | 36% | 0.02 | -0.41 | 0.01 | 0.43 | 3 | 1 | 2 | 0 | 0 | 0 | 150 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.69 | 61% | 37% | 0.94 | 41% | 0.01 | 4 | 1 | 3 | 0 | 0 | 0 |
| long | 0.69 | 59% | 37% | 0.93 | 48% | 0.03 | 2 | 1 | 1 | 0 | 0 | 0 |
| sphere | 0.94 | 23% | 12% | 0.97 | 69% | -0.06 | 1 | 0 | 1 | 0 | 0 | 0 |
| cylinder | 0.21 | 17% | 6% | 0.95 | 32% | 0.00 | 5 | 0 | 5 | 0 | 0 | 0 |
| arch | 0.52 | 47% | 31% | 0.85 | 52% | 0.07 | 4 | 0 | 4 | 0 | 0 | 0 |
| dumbbell | 0.88 | 57% | 37% | 0.93 | 74% | 0.12 | 1 | 0 | 1 | 0 | 0 | 0 |
| t_shape | 0.38 | 55% | 35% | 0.94 | 45% | 0.01 | 1 | 0 | 1 | 0 | 0 | 0 |
| beam | 0.54 | 44% | 32% | 0.88 | 35% | 0.04 | 4 | 1 | 4 | 0 | 0 | 0 |
| l_shape | 0.50 | 57% | 34% | 0.93 | 48% | 0.02 | 2 | 0 | 1 | 0 | 0 | 1 |
| asym | 0.52 | 56% | 32% | 0.93 | 43% | 0.02 | 3 | 1 | 3 | 0 | 0 | 0 |
| u_channel | 0.17 | 38% | 21% | 0.94 | 34% | 0.01 | 5 | 0 | 5 | 0 | 0 | 0 |
| plus | 0.69 | 46% | 27% | 0.90 | 49% | 0.02 | 1 | 0 | 1 | 0 | 0 | 0 |
