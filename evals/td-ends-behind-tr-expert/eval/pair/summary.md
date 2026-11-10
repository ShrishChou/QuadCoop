# Pair evaluation: td-ends-behind-tr-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.77 | 0.76 | 0.00 | 0.00 | 25.8 | 0.01 | 0.43 | 0.36 | 0.13 | 0.25 | 1.07 |
| 40 kg | 0.69 | 0.53 | 0.03 | 0.03 | 31.8 | 0.01 | 0.53 | 0.38 | 0.16 | 0.24 | 1.11 |
| 60 kg | 0.58 | 0.46 | 0.06 | 0.05 | 41.0 | 0.01 | 0.62 | 0.41 | 0.23 | 0.30 | 1.05 |
| 80 kg | 0.29 | 0.24 | 0.10 | 0.06 | 37.8 | 0.01 | 0.75 | 0.51 | 0.38 | 0.45 | 1.06 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 -x end + + part 0 corner -x-y | 1.00 | 0.83 | 0.83 | 0.08 |
| long | part 0 corner -x+y + part 0 -x seg 1/2 | 0.92 | 0.83 | 0.83 | 0.58 |
| sphere | sector 225 + sector 135 | 0.92 | 1.00 | 1.00 | 0.92 |
| cylinder | part 0 -x seg 1/2 + part 0 corner -x+y | 0.50 | 0.33 | 0.33 | 0.17 |
| arch | part 3 -x + part 2 -x | 0.92 | 0.92 | 0.83 | 0.42 |
| dumbbell | part 0 -x + part 1 -x | 0.67 | 0.67 | 0.58 | 0.25 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.83 | 0.58 | 0.42 | 0.08 |
| beam (unseen) | part 0 -x seg 2/5 + part 0 -x seg 4/5 | 0.83 | 0.42 | 0.17 | 0.00 |
| l_shape (unseen) | part 0 corner -x-y + part 1 -x | 0.83 | 0.83 | 0.58 | 0.17 |
| asym (unseen) | part 1 -x end - + part 0 -x end + | 0.42 | 0.33 | 0.08 | 0.00 |
| u_channel (unseen) | part 0 -x seg 1/3 + part 0 -x seg 3/3 | 0.67 | 0.83 | 0.67 | 0.58 |
| plus (unseen) | part 0 -x end - + part 0 -x end + | 0.75 | 0.67 | 0.67 | 0.25 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.77 | 0.22 | 0.00 | 0.01 | 0.00 | 0.01 | 11.71 |
| 40 kg | 0.69 | 0.25 | 0.06 | 0.00 | 0.00 | 0.01 | 8.94 |
| 60 kg | 0.58 | 0.31 | 0.10 | 0.00 | 0.00 | 0.00 | 9.68 |
| 80 kg | 0.29 | 0.55 | 0.16 | 0.00 | 0.00 | 0.00 | 7.75 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.28 | 0.66 | 0.87 | 0.00 | 1.00 | 0.29 | 0.64 | 0.85 | 0.00 |
| 40 kg | 1.00 | 0.25 | 0.72 | 0.91 | 0.00 | 1.00 | 0.26 | 0.68 | 0.89 | 0.00 |
| 60 kg | 1.00 | 0.24 | 0.74 | 0.94 | 0.00 | 1.00 | 0.25 | 0.67 | 0.92 | 0.00 |
| 80 kg | 1.00 | 0.22 | 0.74 | 0.96 | 0.00 | 1.00 | 0.25 | 0.64 | 0.93 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.79 | 1.93 | 0.08 | 0.76 | 2.08 | 0.08 |
| 40 kg | 0.78 | 2.02 | 0.08 | 0.76 | 1.94 | 0.10 |
| 60 kg | 0.79 | 1.74 | 0.10 | 0.78 | 2.43 | 0.13 |
| 80 kg | 0.78 | 1.58 | 0.11 | 0.76 | 2.32 | 0.17 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.51 | 0.48 | 0.30 |
| 40 kg | 0.60 | 0.53 | 0.29 |
| 60 kg | 0.63 | 0.50 | 0.28 |
| 80 kg | 0.65 | 0.50 | 0.25 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.65 | 0.39 | 25.82 | 11.71 | 0.26 | 0.23 | 7.37 | 0.00 | 0.35 |
| 40 kg | 0.41 | 0.46 | 26.30 | 8.94 | 0.37 | 0.92 | 6.15 | 0.00 | 0.29 |
| 60 kg | 0.49 | 0.42 | 28.67 | 9.68 | 0.32 | 1.20 | 2.36 | 0.00 | 0.31 |
| 80 kg | 0.72 | 0.41 | 29.30 | 7.75 | 0.19 | 2.24 | 0.40 | 0.00 | 0.34 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 102 | 259 | 191 |
| 40 kg | 140 | 309 | 257 |
| 60 kg | 172 | 345 | 305 |
| 80 kg | 192 | 369 | 341 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 1075 | 0.35 | 0.46 (213) | 0.50 (132) | 0.49 (302) | 0.51 (211) | 0.61 (216) |
| 40 kg | 1690 | 0.31 | 0.33 (347) | 0.49 (189) | 0.49 (405) | 0.53 (222) | 0.71 (526) |
| 60 kg | 1939 | 0.33 | 0.37 (366) | 0.46 (333) | 0.52 (319) | 0.54 (364) | 0.70 (557) |
| 80 kg | 2545 | 0.34 | 0.35 (74) | 0.43 (404) | 0.51 (1453) | 0.51 (436) | 0.63 (178) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.15 | 0.11 | 0.10 | 0.31 |
| long | 0.22 | 0.22 | 0.20 | 0.51 |
| sphere | 0.28 | 0.42 | 0.50 | 0.56 |
| cylinder | 0.12 | 0.18 | 0.24 | 0.38 |
| arch | 0.17 | 0.22 | 0.21 | 0.29 |
| dumbbell | 0.13 | 0.14 | 0.25 | 0.36 |
| t_shape | 0.12 | 0.09 | 0.17 | 0.30 |
| beam | 0.13 | 0.17 | 0.27 | 0.58 |
| l_shape | 0.08 | 0.12 | 0.15 | 0.33 |
| asym | 0.09 | 0.09 | 0.37 | 0.49 |
| u_channel | 0.07 | 0.10 | 0.20 | 0.36 |
| plus | 0.07 | 0.08 | 0.08 | 0.10 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.83 | 0.78 | 0.81 | 0.47 |
| B_left | 0.81 | 0.72 | 0.64 | 0.31 |
| C_backright | 0.78 | 0.58 | 0.44 | 0.22 |
| D_far_turn | 0.67 | 0.67 | 0.44 | 0.17 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 42% | 0% | 58% | 37% | 4% | 59% |  |  | 19% | 70% | 37% | 22% |
| 40 kg | 35% | 0% | 65% | 46% | 3% | 52% |  |  | 19% | 73% | 33% | 24% |
| 60 kg | 34% | 0% | 66% | 52% | 2% | 46% |  |  | 21% | 77% | 25% | 25% |
| 80 kg | 34% | 0% | 66% | 57% | 2% | 41% |  |  | 24% | 82% | 22% | 29% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 141 | 0.89 | 8% | 12% | 32% | 56% |
| 40 kg | 173 | 0.89 | 8% | 18% | 41% | 41% |
| 60 kg | 199 | 0.90 | 7% | 23% | 45% | 32% |
| 80 kg | 215 | 0.89 | 8% | 29% | 45% | 26% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 61% | 0.20 | 0.44 | 0.15 | 0.65 | 6 | 0 | 4 | 0 | 0 | 1 | 58 | 0.00 |  |
| 40 kg | 60% | 0.16 | 0.58 | 0.13 | 0.62 | 5 | 0 | 4 | 0 | 0 | 1 | 100 | 0.00 |  |
| 60 kg | 57% | 0.11 | 0.67 | 0.09 | 0.53 | 3 | 0 | 2 | 0 | 0 | 1 | 118 | 0.00 |  |
| 80 kg | 51% | 0.08 | 0.76 | 0.07 | 0.56 | 3 | 0 | 2 | 0 | 0 | 1 | 107 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.69 | 54% | 21% | 0.92 | 64% | 0.14 | 1 | 0 | 0 | 0 | 0 | 1 |
| long | 0.79 | 54% | 23% | 0.91 | 61% | 0.12 | 1 | 0 | 1 | 0 | 0 | 1 |
| sphere | 0.96 | 30% | 9% | 0.92 | 83% | 0.28 | 1 | 0 | 1 | 0 | 0 | 0 |
| cylinder | 0.33 | 35% | 15% | 0.91 | 66% | 0.10 | 3 | 0 | 3 | 0 | 0 | 0 |
| arch | 0.77 | 59% | 29% | 0.82 | 63% | 0.13 | 3 | 0 | 2 | 0 | 0 | 1 |
| dumbbell | 0.54 | 44% | 20% | 0.91 | 49% | 0.09 | 10 | 0 | 8 | 0 | 0 | 2 |
| t_shape | 0.48 | 53% | 22% | 0.91 | 52% | 0.08 | 5 | 0 | 4 | 0 | 0 | 1 |
| beam | 0.35 | 35% | 18% | 0.83 | 33% | 0.07 | 11 | 0 | 8 | 0 | 0 | 2 |
| l_shape | 0.60 | 55% | 23% | 0.92 | 57% | 0.08 | 2 | 0 | 2 | 0 | 0 | 1 |
| asym | 0.21 | 57% | 27% | 0.92 | 52% | 0.05 | 2 | 0 | 1 | 0 | 0 | 1 |
| u_channel | 0.69 | 50% | 20% | 0.92 | 50% | 0.08 | 6 | 0 | 3 | 0 | 0 | 3 |
| plus | 0.58 | 50% | 19% | 0.81 | 54% | 0.07 | 4 | 0 | 2 | 0 | 0 | 1 |
