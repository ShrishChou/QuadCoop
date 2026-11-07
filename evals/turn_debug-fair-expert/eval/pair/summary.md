# Pair evaluation: turn_debug-fair-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.67 | 0.68 | 0.00 | 0.01 | 26.8 | 0.01 | 0.43 | 0.37 | 0.12 | 0.21 | 1.07 |
| 40 kg | 0.67 | 0.50 | 0.03 | 0.02 | 30.6 | 0.00 | 0.51 | 0.37 | 0.14 | 0.21 | 1.08 |
| 60 kg | 0.57 | 0.47 | 0.06 | 0.03 | 36.7 | 0.01 | 0.62 | 0.44 | 0.25 | 0.34 | 1.09 |
| 80 kg | 0.38 | 0.28 | 0.07 | 0.03 | 38.8 | 0.01 | 0.72 | 0.55 | 0.40 | 0.47 | 1.06 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x+y + part 0 corner -x-y | 0.67 | 0.58 | 0.75 | 0.50 |
| long | part 0 -x seg 2/2 + part 0 corner -x-y | 0.67 | 0.92 | 0.67 | 0.42 |
| sphere | sector 135 + sector 225 | 1.00 | 1.00 | 1.00 | 1.00 |
| cylinder | part 0 corner -x-y + part 0 -x seg 2/2 | 0.50 | 0.42 | 0.50 | 0.42 |
| arch | part 3 -x + part 2 -x | 0.67 | 0.92 | 0.58 | 0.50 |
| dumbbell | part 0 -x + part 1 -x | 0.58 | 0.50 | 0.67 | 0.33 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.75 | 0.67 | 0.75 | 0.17 |
| beam (unseen) | part 0 -x seg 2/5 + part 0 -x seg 4/5 | 0.58 | 0.42 | 0.08 | 0.00 |
| l_shape (unseen) | part 1 -x + part 0 corner -x-y | 0.83 | 0.75 | 0.50 | 0.17 |
| asym (unseen) | part 1 -x + part 0 corner -x+y | 0.42 | 0.33 | 0.17 | 0.00 |
| u_channel (unseen) | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.83 | 0.75 | 0.58 | 0.67 |
| plus (unseen) | part 0 corner -x-y + part 0 corner -x+y | 0.58 | 0.75 | 0.58 | 0.33 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.67 | 0.31 | 0.01 | 0.01 | 0.00 | 0.03 | 10.24 |
| 40 kg | 0.67 | 0.28 | 0.05 | 0.00 | 0.00 | 0.00 | 9.73 |
| 60 kg | 0.57 | 0.35 | 0.08 | 0.00 | 0.00 | 0.01 | 9.74 |
| 80 kg | 0.38 | 0.53 | 0.10 | 0.00 | 0.00 | 0.00 | 8.31 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.28 | 0.68 | 0.87 | 0.00 | 1.00 | 0.28 | 0.68 | 0.87 | 0.00 |
| 40 kg | 1.00 | 0.24 | 0.72 | 0.90 | 0.00 | 1.00 | 0.28 | 0.69 | 0.88 | 0.00 |
| 60 kg | 1.00 | 0.26 | 0.71 | 0.93 | 0.00 | 1.00 | 0.26 | 0.66 | 0.91 | 0.00 |
| 80 kg | 1.00 | 0.23 | 0.73 | 0.96 | 0.00 | 1.00 | 0.25 | 0.67 | 0.94 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.80 | 2.11 | 0.06 | 0.77 | 1.91 | 0.06 |
| 40 kg | 0.80 | 2.14 | 0.08 | 0.76 | 2.26 | 0.10 |
| 60 kg | 0.81 | 2.05 | 0.10 | 0.79 | 2.47 | 0.13 |
| 80 kg | 0.79 | 2.00 | 0.10 | 0.77 | 2.52 | 0.16 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.55 | 0.53 | 0.31 |
| 40 kg | 0.58 | 0.52 | 0.30 |
| 60 kg | 0.61 | 0.49 | 0.28 |
| 80 kg | 0.66 | 0.51 | 0.25 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.17 | 0.44 | 27.83 | 10.24 | 0.04 | 0.50 | 8.40 | 0.00 | 0.28 |
| 40 kg | 0.77 | 0.42 | 26.66 | 9.73 | 0.42 | 0.78 | 4.46 | 0.00 | 0.29 |
| 60 kg | 0.65 | 0.42 | 27.81 | 9.74 | 0.50 | 1.14 | 1.70 | 0.00 | 0.31 |
| 80 kg | 0.58 | 0.45 | 28.76 | 8.31 | 0.33 | 2.42 | 0.61 | 0.00 | 0.30 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 107 | 259 | 196 |
| 40 kg | 141 | 306 | 249 |
| 60 kg | 172 | 345 | 301 |
| 80 kg | 192 | 366 | 344 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 1458 | 0.34 | 0.43 (217) | 0.51 (184) | 0.50 (398) | 0.52 (335) | 0.59 (325) |
| 40 kg | 1535 | 0.32 | 0.33 (426) | 0.52 (144) | 0.54 (141) | 0.56 (191) | 0.71 (633) |
| 60 kg | 1822 | 0.32 | 0.35 (311) | 0.45 (232) | 0.49 (305) | 0.59 (430) | 0.72 (544) |
| 80 kg | 2739 | 0.34 | 0.38 (112) | 0.41 (415) | 0.49 (1418) | 0.50 (538) | 0.68 (256) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.16 | 0.06 | 0.28 | 0.38 |
| long | 0.14 | 0.10 | 0.21 | 0.43 |
| sphere | 0.28 | 0.41 | 0.48 | 0.53 |
| cylinder | 0.07 | 0.11 | 0.30 | 0.44 |
| arch | 0.16 | 0.11 | 0.22 | 0.31 |
| dumbbell | 0.11 | 0.12 | 0.27 | 0.43 |
| t_shape | 0.12 | 0.11 | 0.22 | 0.38 |
| beam | 0.13 | 0.20 | 0.28 | 0.48 |
| l_shape | 0.06 | 0.08 | 0.17 | 0.36 |
| asym | 0.11 | 0.13 | 0.34 | 0.49 |
| u_channel | 0.08 | 0.11 | 0.18 | 0.40 |
| plus | 0.05 | 0.10 | 0.08 | 0.11 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.86 | 0.78 | 0.78 | 0.50 |
| B_left | 0.78 | 0.81 | 0.75 | 0.42 |
| C_backright | 0.47 | 0.61 | 0.42 | 0.36 |
| D_far_turn | 0.58 | 0.47 | 0.33 | 0.22 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 38% | 0% | 62% | 37% | 4% | 59% |  |  | 17% | 64% | 45% | 23% |
| 40 kg | 36% | 0% | 64% | 45% | 2% | 53% |  |  | 18% | 66% | 40% | 24% |
| 60 kg | 36% | 0% | 64% | 52% | 2% | 46% |  |  | 21% | 77% | 26% | 27% |
| 80 kg | 33% | 0% | 67% | 57% | 2% | 40% |  |  | 23% | 80% | 22% | 29% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 143 | 0.90 | 7% | 13% | 31% | 56% |
| 40 kg | 172 | 0.90 | 6% | 16% | 41% | 43% |
| 60 kg | 199 | 0.91 | 6% | 22% | 45% | 33% |
| 80 kg | 215 | 0.90 | 7% | 29% | 45% | 26% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 59% | 0.19 | 0.44 | 0.14 | 0.92 | 7 | 0 | 6 | 0 | 0 | 1 | 79 | 0.00 |  |
| 40 kg | 58% | 0.15 | 0.58 | 0.13 | 0.65 | 5 | 0 | 3 | 0 | 0 | 1 | 74 | 0.00 |  |
| 60 kg | 57% | 0.11 | 0.70 | 0.10 | 0.53 | 3 | 0 | 2 | 0 | 0 | 2 | 80 | 0.00 |  |
| 80 kg | 52% | 0.09 | 0.77 | 0.08 | 0.49 | 2 | 0 | 1 | 0 | 0 | 1 | 164 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.62 | 58% | 26% | 0.92 | 68% | 0.14 | 1 | 0 | 0 | 0 | 0 | 1 |
| long | 0.67 | 54% | 24% | 0.91 | 59% | 0.10 | 1 | 0 | 0 | 0 | 0 | 1 |
| sphere | 1.00 | 29% | 9% | 0.92 | 82% | 0.30 | 2 | 0 | 0 | 0 | 0 | 2 |
| cylinder | 0.46 | 28% | 10% | 0.91 | 58% | 0.09 | 7 | 0 | 7 | 0 | 0 | 0 |
| arch | 0.67 | 57% | 28% | 0.83 | 61% | 0.12 | 4 | 0 | 3 | 0 | 0 | 1 |
| dumbbell | 0.52 | 46% | 21% | 0.91 | 49% | 0.09 | 11 | 0 | 8 | 0 | 0 | 4 |
| t_shape | 0.58 | 55% | 24% | 0.92 | 56% | 0.08 | 3 | 0 | 2 | 0 | 0 | 1 |
| beam | 0.27 | 32% | 16% | 0.83 | 29% | 0.07 | 10 | 0 | 7 | 0 | 0 | 3 |
| l_shape | 0.56 | 54% | 19% | 0.91 | 53% | 0.07 | 2 | 0 | 1 | 0 | 0 | 1 |
| asym | 0.23 | 60% | 29% | 0.91 | 52% | 0.06 | 1 | 0 | 1 | 0 | 0 | 0 |
| u_channel | 0.71 | 49% | 17% | 0.94 | 53% | 0.10 | 6 | 0 | 3 | 0 | 0 | 2 |
| plus | 0.56 | 51% | 21% | 0.91 | 59% | 0.09 | 4 | 0 | 3 | 0 | 0 | 1 |
