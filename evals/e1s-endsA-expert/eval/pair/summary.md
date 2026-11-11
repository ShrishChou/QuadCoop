# Pair evaluation: e1s-endsA-expert

policy: Stage 4 contact policy logs/marl2/ends_a/model_16900.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.85 | 0.81 | 0.02 | 0.02 | 29.1 | 0.01 | 0.45 | 0.30 | 0.11 | 0.21 | 1.05 |
| 40 kg | 0.71 | 0.56 | 0.03 | 0.03 | 30.3 | 0.01 | 0.52 | 0.35 | 0.14 | 0.21 | 1.07 |
| 60 kg | 0.56 | 0.43 | 0.09 | 0.05 | 38.7 | 0.02 | 0.62 | 0.41 | 0.24 | 0.32 | 1.02 |
| 80 kg | 0.32 | 0.28 | 0.16 | 0.08 | 40.0 | 0.02 | 0.73 | 0.47 | 0.34 | 0.43 | 1.00 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 -x end + + part 0 corner -x-y | 0.92 | 0.92 | 0.83 | 0.50 |
| long | part 0 corner -x+y + part 0 -x seg 1/2 | 0.92 | 0.83 | 0.58 | 0.25 |
| sphere | sector 225 + sector 135 | 1.00 | 1.00 | 1.00 | 0.92 |
| cylinder | part 0 -x seg 1/2 + part 0 corner -x+y | 0.75 | 0.58 | 0.50 | 0.25 |
| arch | part 3 -x + part 2 -x | 1.00 | 0.92 | 0.42 | 0.42 |
| dumbbell | part 0 -x + part 1 -x | 0.75 | 0.42 | 0.67 | 0.33 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.92 | 0.58 | 0.50 | 0.25 |
| beam (unseen) | part 0 -x seg 2/5 + part 0 -x seg 4/5 | 0.83 | 0.58 | 0.25 | 0.08 |
| l_shape (unseen) | part 0 corner -x-y + part 1 -x | 1.00 | 0.67 | 0.58 | 0.17 |
| asym (unseen) | part 1 -x end - + part 0 -x end + | 0.33 | 0.42 | 0.25 | 0.00 |
| u_channel (unseen) | part 0 -x seg 1/3 + part 0 -x seg 3/3 | 1.00 | 0.92 | 0.67 | 0.33 |
| plus (unseen) | part 0 -x end - + part 0 -x end + | 0.83 | 0.67 | 0.50 | 0.33 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.85 | 0.10 | 0.04 | 0.00 | 0.00 | 0.04 | 12.95 |
| 40 kg | 0.71 | 0.24 | 0.06 | 0.00 | 0.00 | 0.01 | 9.74 |
| 60 kg | 0.56 | 0.30 | 0.14 | 0.00 | 0.00 | 0.01 | 9.62 |
| 80 kg | 0.32 | 0.44 | 0.24 | 0.00 | 0.00 | 0.00 | 8.49 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.31 | 0.61 | 0.84 | 0.00 | 1.00 | 0.31 | 0.61 | 0.82 | 0.00 |
| 40 kg | 1.00 | 0.25 | 0.71 | 0.91 | 0.00 | 1.00 | 0.28 | 0.63 | 0.88 | 0.00 |
| 60 kg | 1.00 | 0.27 | 0.69 | 0.93 | 0.00 | 1.00 | 0.31 | 0.57 | 0.89 | 0.00 |
| 80 kg | 1.00 | 0.26 | 0.66 | 0.94 | 0.00 | 1.00 | 0.31 | 0.54 | 0.91 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.79 | 2.15 | 0.11 | 0.74 | 2.04 | 0.10 |
| 40 kg | 0.80 | 1.86 | 0.11 | 0.74 | 2.42 | 0.13 |
| 60 kg | 0.81 | 2.58 | 0.13 | 0.73 | 2.85 | 0.17 |
| 80 kg | 0.80 | 2.03 | 0.16 | 0.74 | 2.68 | 0.21 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.47 | 0.44 | 0.30 |
| 40 kg | 0.58 | 0.46 | 0.29 |
| 60 kg | 0.60 | 0.43 | 0.27 |
| 80 kg | 0.59 | 0.41 | 0.24 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.53 | 0.37 | 26.24 | 12.95 | 0.04 | 0.03 | 6.17 | 0.00 | 0.35 |
| 40 kg | 0.55 | 0.38 | 26.29 | 9.74 | 0.20 | 0.61 | 4.27 | 0.00 | 0.34 |
| 60 kg | 0.64 | 0.38 | 26.80 | 9.62 | 0.16 | 1.08 | 1.14 | 0.00 | 0.38 |
| 80 kg | 0.57 | 0.35 | 26.88 | 8.49 | 0.10 | 1.36 | 0.57 | 0.00 | 0.42 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 106 | 256 | 197 |
| 40 kg | 145 | 313 | 266 |
| 60 kg | 174 | 351 | 311 |
| 80 kg | 194 | 376 | 344 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 961 | 0.36 | 0.46 (193) | 0.52 (109) | 0.50 (267) | 0.52 (118) | 0.57 (274) |
| 40 kg | 1434 | 0.32 | 0.30 (307) | 0.51 (223) | 0.49 (341) | 0.54 (182) | 0.67 (382) |
| 60 kg | 1718 | 0.32 | 0.34 (392) | 0.46 (368) | 0.49 (283) | 0.57 (298) | 0.74 (377) |
| 80 kg | 1960 | 0.33 | 0.33 (89) | 0.46 (233) | 0.49 (1136) | 0.48 (294) | 0.70 (209) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.09 | 0.12 | 0.15 | 0.37 |
| long | 0.13 | 0.13 | 0.29 | 0.43 |
| sphere | 0.37 | 0.38 | 0.50 | 0.53 |
| cylinder | 0.16 | 0.16 | 0.25 | 0.35 |
| arch | 0.10 | 0.14 | 0.19 | 0.32 |
| dumbbell | 0.09 | 0.12 | 0.16 | 0.34 |
| t_shape | 0.06 | 0.05 | 0.16 | 0.37 |
| beam | 0.10 | 0.19 | 0.27 | 0.53 |
| l_shape | 0.03 | 0.05 | 0.16 | 0.27 |
| asym | 0.06 | 0.12 | 0.42 | 0.24 |
| u_channel | 0.12 | 0.15 | 0.20 | 0.29 |
| plus | 0.06 | 0.04 | 0.08 | 0.09 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.86 | 0.89 | 0.81 | 0.50 |
| B_left | 0.83 | 0.81 | 0.50 | 0.36 |
| C_backright | 0.81 | 0.58 | 0.47 | 0.22 |
| D_far_turn | 0.92 | 0.56 | 0.47 | 0.19 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 47% | 0% | 53% | 40% | 4% | 56% |  |  | 21% | 71% | 38% | 25% |
| 40 kg | 38% | 0% | 62% | 47% | 3% | 50% |  |  | 22% | 75% | 32% | 26% |
| 60 kg | 41% | 0% | 59% | 54% | 2% | 44% |  |  | 26% | 85% | 21% | 28% |
| 80 kg | 43% | 0% | 57% | 59% | 2% | 39% |  |  | 30% | 88% | 16% | 32% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 141 | 0.88 | 9% | 14% | 34% | 52% |
| 40 kg | 175 | 0.89 | 8% | 19% | 43% | 38% |
| 60 kg | 201 | 0.90 | 6% | 24% | 46% | 31% |
| 80 kg | 219 | 0.89 | 7% | 30% | 45% | 25% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 65% | 0.22 | 0.42 | 0.15 | 0.42 | 3 | 0 | 2 | 0 | 0 | 1 | 68 | 0.00 |  |
| 40 kg | 63% | 0.16 | 0.56 | 0.13 | 0.42 | 3 | 0 | 3 | 0 | 0 | 1 | 102 | 0.00 |  |
| 60 kg | 59% | 0.12 | 0.68 | 0.10 | 0.29 | 2 | 0 | 1 | 0 | 0 | 1 | 95 | 0.00 |  |
| 80 kg | 53% | 0.09 | 0.76 | 0.07 | 0.30 | 2 | 0 | 1 | 0 | 0 | 1 | 163 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.79 | 59% | 26% | 0.92 | 70% | 0.15 | 1 | 0 | 1 | 0 | 0 | 0 |
| long | 0.65 | 55% | 24% | 0.92 | 61% | 0.10 | 2 | 0 | 2 | 0 | 0 | 0 |
| sphere | 0.98 | 30% | 9% | 0.92 | 86% | 0.31 | 0 | 0 | 0 | 0 | 0 | 0 |
| cylinder | 0.52 | 43% | 18% | 0.90 | 75% | 0.12 | 0 | 0 | 0 | 0 | 0 | 0 |
| arch | 0.69 | 58% | 24% | 0.82 | 58% | 0.10 | 3 | 0 | 1 | 0 | 0 | 2 |
| dumbbell | 0.54 | 47% | 19% | 0.90 | 48% | 0.08 | 9 | 0 | 7 | 0 | 0 | 2 |
| t_shape | 0.56 | 56% | 26% | 0.90 | 58% | 0.08 | 1 | 0 | 1 | 0 | 0 | 0 |
| beam | 0.44 | 41% | 22% | 0.84 | 38% | 0.08 | 6 | 0 | 4 | 0 | 0 | 2 |
| l_shape | 0.60 | 53% | 22% | 0.91 | 56% | 0.08 | 2 | 0 | 1 | 0 | 0 | 1 |
| asym | 0.25 | 61% | 32% | 0.93 | 51% | 0.05 | 1 | 0 | 1 | 0 | 0 | 0 |
| u_channel | 0.73 | 50% | 17% | 0.93 | 58% | 0.11 | 3 | 0 | 1 | 0 | 0 | 1 |
| plus | 0.58 | 49% | 20% | 0.79 | 61% | 0.09 | 1 | 0 | 1 | 0 | 0 | 0 |
