# Pair evaluation: final-teacher-s3001-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 12 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.80 | 0.74 | 0.01 | 0.00 | 26.2 | 0.00 | 0.38 | 0.39 | 0.14 | 0.25 | 1.33 |
| 40 kg | 0.80 | 0.62 | 0.00 | 0.00 | 33.0 | 0.00 | 0.45 | 0.43 | 0.14 | 0.21 | 1.45 |
| 60 kg | 0.62 | 0.50 | 0.03 | 0.01 | 40.0 | 0.00 | 0.57 | 0.45 | 0.21 | 0.28 | 1.43 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg |
|---|---|---|---|---|
| long | part 0 -x seg 1/2 + part 0 corner -x+y | 0.77 | 0.75 | 0.56 |
| arch | part 3 -x + part 2 -x | 0.85 | 0.85 | 0.71 |
| dumbbell | part 1 -x + part 0 -x | 0.77 | 0.79 | 0.60 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.80 | 0.19 | 0.01 | 0.00 | 0.00 | 0.01 | 11.85 |
| 40 kg | 0.80 | 0.20 | 0.00 | 0.00 | 0.00 | 0.03 | 9.24 |
| 60 kg | 0.62 | 0.34 | 0.03 | 0.00 | 0.00 | 0.00 | 8.45 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.29 | 0.66 | 0.83 | 0.00 | 1.00 | 0.28 | 0.71 | 0.84 | 0.00 |
| 40 kg | 1.00 | 0.25 | 0.75 | 0.91 | 0.00 | 1.00 | 0.24 | 0.78 | 0.89 | 0.00 |
| 60 kg | 1.00 | 0.25 | 0.77 | 0.93 | 0.00 | 1.00 | 0.20 | 0.82 | 0.93 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.78 | 2.33 | 0.07 | 0.78 | 2.08 | 0.05 |
| 40 kg | 0.78 | 2.26 | 0.07 | 0.75 | 2.12 | 0.06 |
| 60 kg | 0.78 | 2.25 | 0.07 | 0.76 | 2.12 | 0.07 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.50 | 0.58 | 0.31 |
| 40 kg | 0.59 | 0.62 | 0.31 |
| 60 kg | 0.62 | 0.64 | 0.32 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.76 | 0.45 | 24.68 | 11.85 | 0.17 | 0.46 | 8.40 | 0.00 | 0.28 |
| 40 kg | 1.78 | 0.49 | 25.08 | 9.24 | 0.29 | 0.87 | 6.15 | 0.00 | 0.23 |
| 60 kg | 1.40 | 0.51 | 26.41 | 8.45 | 0.53 | 2.89 | 1.64 | 0.00 | 0.20 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 98 | 258 | 191 |
| 40 kg | 140 | 320 | 248 |
| 60 kg | 178 | 364 | 304 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 1320 | 0.35 | 0.44 (255) | 0.52 (300) | 0.51 (368) | 0.50 (174) | 0.60 (222) |
| 40 kg | 1892 | 0.34 | 0.36 (595) | 0.46 (257) | 0.47 (327) | 0.54 (197) | 0.66 (515) |
| 60 kg | 2439 | 0.31 | 0.27 (554) | 0.46 (463) | 0.52 (368) | 0.52 (300) | 0.68 (754) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg |
|---|---|---|---|
| long | 0.12 | 0.12 | 0.22 |
| arch | 0.16 | 0.15 | 0.21 |
| dumbbell | 0.13 | 0.14 | 0.22 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg |
|---|---|---|---|
| A_straight | 0.89 | 0.83 | 0.72 |
| B_left | 0.75 | 0.86 | 0.72 |
| C_backright | 0.72 | 0.72 | 0.58 |
| D_far_turn | 0.83 | 0.78 | 0.47 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 37% | 0% | 63% | 39% | 5% | 57% |  |  | 14% | 58% | 49% | 17% |
| 40 kg | 29% | 0% | 71% | 49% | 3% | 48% |  |  | 12% | 58% | 48% | 18% |
| 60 kg | 24% | 0% | 76% | 56% | 2% | 42% |  |  | 12% | 67% | 34% | 21% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 140 | 0.86 | 10% | 14% | 33% | 53% |
| 40 kg | 174 | 0.88 | 8% | 20% | 43% | 37% |
| 60 kg | 204 | 0.89 | 8% | 26% | 45% | 29% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 59% | 0.19 | 0.45 | 0.16 | 0.68 | 6 | 0 | 5 | 0 | 0 | 1 | 77 | 0.00 |  |
| 40 kg | 60% | 0.14 | 0.59 | 0.12 | 0.66 | 5 | 0 | 4 | 0 | 0 | 1 | 85 | 0.00 |  |
| 60 kg | 57% | 0.10 | 0.70 | 0.09 | 0.68 | 4 | 0 | 3 | 0 | 0 | 1 | 117 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| long | 0.69 | 51% | 23% | 0.92 | 63% | 0.11 | 1 | 0 | 1 | 0 | 0 | 0 |
| arch | 0.81 | 51% | 21% | 0.82 | 62% | 0.14 | 5 | 0 | 4 | 0 | 0 | 1 |
| dumbbell | 0.72 | 41% | 15% | 0.90 | 52% | 0.11 | 8 | 0 | 6 | 0 | 0 | 2 |
