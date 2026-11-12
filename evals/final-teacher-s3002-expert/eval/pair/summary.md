# Pair evaluation: final-teacher-s3002-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 12 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.84 | 0.79 | 0.01 | 0.01 | 26.9 | 0.00 | 0.39 | 0.38 | 0.14 | 0.26 | 1.35 |
| 40 kg | 0.81 | 0.69 | 0.01 | 0.00 | 32.9 | 0.00 | 0.43 | 0.43 | 0.14 | 0.22 | 1.41 |
| 60 kg | 0.60 | 0.51 | 0.04 | 0.02 | 43.3 | 0.00 | 0.54 | 0.45 | 0.20 | 0.26 | 1.41 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg |
|---|---|---|---|---|
| long | part 0 -x seg 1/2 + part 0 corner -x+y | 0.90 | 0.83 | 0.62 |
| arch | part 3 -x + part 2 -x | 0.83 | 0.88 | 0.73 |
| dumbbell | part 0 -x + part 1 -x | 0.79 | 0.73 | 0.44 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.84 | 0.15 | 0.01 | 0.00 | 0.00 | 0.01 | 12.75 |
| 40 kg | 0.81 | 0.18 | 0.01 | 0.00 | 0.00 | 0.01 | 10.51 |
| 60 kg | 0.60 | 0.34 | 0.06 | 0.00 | 0.00 | 0.00 | 7.57 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.29 | 0.65 | 0.83 | 0.00 | 1.00 | 0.29 | 0.68 | 0.83 | 0.00 |
| 40 kg | 1.00 | 0.26 | 0.73 | 0.88 | 0.00 | 1.00 | 0.23 | 0.78 | 0.89 | 0.00 |
| 60 kg | 1.00 | 0.25 | 0.76 | 0.93 | 0.00 | 1.00 | 0.22 | 0.81 | 0.93 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.79 | 2.23 | 0.08 | 0.81 | 2.09 | 0.05 |
| 40 kg | 0.82 | 2.25 | 0.08 | 0.80 | 1.99 | 0.06 |
| 60 kg | 0.81 | 2.12 | 0.06 | 0.78 | 1.99 | 0.06 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.49 | 0.54 | 0.30 |
| 40 kg | 0.55 | 0.61 | 0.33 |
| 60 kg | 0.62 | 0.62 | 0.30 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.24 | 0.41 | 25.20 | 12.75 | 0.13 | 0.28 | 6.68 | 0.00 | 0.30 |
| 40 kg | 1.77 | 0.44 | 24.33 | 10.51 | 0.27 | 1.01 | 4.47 | 0.00 | 0.24 |
| 60 kg | 2.48 | 0.49 | 26.94 | 7.57 | 0.49 | 2.50 | 1.81 | 0.00 | 0.21 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 98 | 259 | 179 |
| 40 kg | 140 | 320 | 241 |
| 60 kg | 178 | 364 | 305 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 952 | 0.37 | 0.41 (282) | 0.53 (180) | 0.51 (150) | 0.51 (149) | 0.60 (191) |
| 40 kg | 1379 | 0.30 | 0.25 (544) | 0.47 (156) | 0.49 (246) | 0.54 (123) | 0.70 (310) |
| 60 kg | 2501 | 0.31 | 0.29 (594) | 0.49 (449) | 0.51 (436) | 0.56 (364) | 0.72 (657) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg |
|---|---|---|---|
| long | 0.14 | 0.13 | 0.22 |
| arch | 0.16 | 0.14 | 0.15 |
| dumbbell | 0.13 | 0.15 | 0.22 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg |
|---|---|---|---|
| A_straight | 0.86 | 0.83 | 0.78 |
| B_left | 0.78 | 0.86 | 0.67 |
| C_backright | 0.83 | 0.81 | 0.44 |
| D_far_turn | 0.89 | 0.75 | 0.50 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 40% | 0% | 60% | 38% | 5% | 57% |  |  | 15% | 57% | 51% | 19% |
| 40 kg | 30% | 0% | 70% | 47% | 3% | 50% |  |  | 14% | 56% | 51% | 17% |
| 60 kg | 24% | 0% | 76% | 55% | 2% | 42% |  |  | 12% | 69% | 36% | 20% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 139 | 0.86 | 10% | 12% | 33% | 54% |
| 40 kg | 174 | 0.88 | 8% | 18% | 43% | 39% |
| 60 kg | 204 | 0.89 | 8% | 24% | 46% | 29% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 60% | 0.20 | 0.48 | 0.16 | 0.88 | 7 | 0 | 5 | 0 | 0 | 1 | 81 | 0.00 |  |
| 40 kg | 59% | 0.15 | 0.61 | 0.13 | 0.76 | 7 | 0 | 6 | 0 | 0 | 1 | 82 | 0.00 |  |
| 60 kg | 55% | 0.09 | 0.69 | 0.08 | 0.51 | 4 | 0 | 3 | 0 | 0 | 1 | 94 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| long | 0.78 | 50% | 19% | 0.92 | 63% | 0.12 | 2 | 0 | 1 | 0 | 0 | 0 |
| arch | 0.81 | 51% | 21% | 0.81 | 61% | 0.14 | 5 | 0 | 4 | 0 | 0 | 1 |
| dumbbell | 0.65 | 40% | 15% | 0.90 | 51% | 0.11 | 10 | 0 | 8 | 0 | 0 | 2 |
