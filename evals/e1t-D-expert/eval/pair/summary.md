# Pair evaluation: e1t-D-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start at their contacts; contact rule re-applied: never); TASKS: turn in place (object at the goal position, heading off 15/30/60/90 deg, capped by symmetry)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.48 | 0.61 | 0.00 | 0.00 | 7.1 | 0.00 | 0.39 | 0.43 | 0.02 | 0.03 | 1.23 |
| 40 kg | 0.60 | 0.69 | 0.00 | 0.01 | 6.7 | 0.01 | 0.37 | 0.49 | 0.03 | 0.04 | 1.28 |
| 60 kg | 0.66 | 0.56 | 0.00 | 0.00 | 8.6 | 0.00 | 0.38 | 0.50 | 0.02 | 0.02 | 1.44 |
| 80 kg | 0.57 | 0.40 | 0.01 | 0.02 | 12.0 | 0.01 | 0.39 | 0.47 | 0.02 | 0.02 | 1.53 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube |  | 1.00 | 1.00 | 0.92 | 0.92 |
| long |  | 0.58 | 0.92 | 0.83 | 0.67 |
| sphere |  | 0.92 | 1.00 | 1.00 | 1.00 |
| cylinder |  | 0.42 | 0.42 | 0.25 | 0.25 |
| arch |  | 0.25 | 0.58 | 0.83 | 0.58 |
| dumbbell |  | 0.83 | 0.83 | 0.92 | 0.83 |
| t_shape |  | 0.00 | 0.00 | 0.08 | 0.17 |
| beam (unseen) |  | 0.58 | 0.67 | 0.75 | 0.25 |
| l_shape (unseen) |  | 0.33 | 0.75 | 0.75 | 0.58 |
| asym (unseen) |  | 0.25 | 0.50 | 0.67 | 0.50 |
| u_channel (unseen) |  | 0.00 | 0.00 | 0.08 | 0.33 |
| plus (unseen) |  | 0.58 | 0.58 | 0.83 | 0.75 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.48 | 0.52 | 0.00 | 0.00 | 0.00 | 0.09 | 0.00 |
| 40 kg | 0.60 | 0.39 | 0.01 | 0.00 | 0.00 | 0.06 | 0.00 |
| 60 kg | 0.66 | 0.34 | 0.00 | 0.00 | 0.00 | 0.03 | 0.00 |
| 80 kg | 0.57 | 0.40 | 0.03 | 0.00 | 0.00 | 0.02 | 0.00 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.14 | 0.89 | 0.98 | 0.00 | 1.00 | 0.12 | 0.90 | 0.99 | 0.00 |
| 40 kg | 1.00 | 0.13 | 0.90 | 0.99 | 0.00 | 1.00 | 0.11 | 0.92 | 0.99 | 0.00 |
| 60 kg | 1.00 | 0.13 | 0.92 | 1.00 | 0.00 | 1.00 | 0.11 | 0.91 | 1.00 | 0.00 |
| 80 kg | 1.00 | 0.13 | 0.92 | 0.99 | 0.00 | 1.00 | 0.11 | 0.92 | 1.00 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.02 | 0.03 | 1.00 | 0.02 | 0.02 |
| 40 kg | 1.00 | 0.02 | 0.04 | 1.00 | 0.02 | 0.04 |
| 60 kg | 1.00 | 0.02 | 0.05 | 1.00 | 0.02 | 0.05 |
| 80 kg | 1.00 | 0.02 | 0.05 | 1.00 | 0.02 | 0.05 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.70 | 0.83 | 0.64 |
| 40 kg | 0.75 | 0.88 | 0.50 |
| 60 kg | 0.78 | 0.88 | 0.37 |
| 80 kg | 0.78 | 0.87 | 0.32 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.04 | 0.64 | 16.09 | 0.00 | 0.00 | 0.00 | 19.01 | 0.00 | 0.18 |
| 40 kg | 0.00 | 0.70 | 12.48 | 0.00 | 0.00 | 0.00 | 19.19 | 0.00 | 0.14 |
| 60 kg | 0.00 | 0.72 | 11.05 | 0.00 | 0.00 | 0.00 | 16.03 | 0.00 | 0.13 |
| 80 kg | 0.00 | 0.72 | 13.33 | 0.00 | 0.00 | 0.00 | 14.25 | 0.00 | 0.12 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 95 | 238 | 195 |
| 40 kg | 131 | 300 | 267 |
| 60 kg | 155 | 324 | 304 |
| 80 kg | 172 | 337 | 327 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 696 | 0.47 | 0.55 (75) | 0.51 (66) | 0.47 (190) | 0.45 (74) | 0.41 (290) |
| 40 kg | 751 | 0.47 | 0.56 (160) | 0.52 (61) | 0.47 (194) | 0.53 (70) | 0.44 (266) |
| 60 kg | 1185 | 0.45 | 0.64 (278) | 0.53 (97) | 0.48 (426) | 0.46 (172) | 0.47 (212) |
| 80 kg | 2087 | 0.41 | 0.57 (383) | 0.53 (186) | 0.47 (976) | 0.43 (206) | 0.51 (337) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.10 | 0.01 | 0.01 | 0.01 |
| long | 0.01 | 0.01 | 0.01 | 0.00 |
| sphere | 0.00 | 0.00 | 0.00 | 0.00 |
| cylinder | 0.00 | 0.00 | 0.00 | 0.00 |
| arch | 0.00 | 0.00 | 0.01 | 0.01 |
| dumbbell | 0.01 | 0.00 | 0.01 | 0.04 |
| t_shape | 0.00 | 0.02 | 0.16 | 0.04 |
| beam | 0.00 | 0.07 | 0.01 | 0.01 |
| l_shape | 0.05 | 0.14 | 0.02 | 0.08 |
| asym | 0.00 | 0.01 | 0.01 | 0.02 |
| u_channel | 0.00 | 0.00 | 0.00 | 0.01 |
| plus | 0.06 | 0.05 | 0.00 | 0.00 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| T15 | 0.67 | 0.72 | 0.86 | 0.94 |
| T30 | 0.31 | 0.58 | 0.75 | 0.56 |
| T60 | 0.56 | 0.64 | 0.61 | 0.44 |
| T90 | 0.39 | 0.47 | 0.42 | 0.33 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 16% | 0% | 84% | 29% | 3% | 68% |  |  | 16% | 59% | 52% | 13% |
| 40 kg | 12% | 0% | 88% | 40% | 2% | 58% |  |  | 12% | 69% | 40% | 13% |
| 60 kg | 11% | 0% | 89% | 49% | 2% | 49% |  |  | 11% | 70% | 37% | 15% |
| 80 kg | 11% | 0% | 89% | 53% | 2% | 45% |  |  | 11% | 62% | 42% | 18% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 133 | 0.87 | 10% | 16% | 22% | 62% |
| 40 kg | 168 | 0.89 | 7% | 24% | 30% | 46% |
| 60 kg | 186 | 0.91 | 5% | 32% | 34% | 34% |
| 80 kg | 200 | 0.91 | 5% | 33% | 38% | 28% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 46% | 0.05 | -0.19 | 0.03 | 1.67 | 21 | 0 | 18 | 0 | 0 | 2 | 70 | 0.00 |  |
| 40 kg | 52% | 0.04 | -0.26 | 0.03 | 1.31 | 15 | 0 | 14 | 0 | 0 | 1 | 94 | 0.00 |  |
| 60 kg | 48% | 0.03 | -0.28 | 0.02 | 1.13 | 10 | 0 | 8 | 0 | 0 | 1 | 114 | 0.00 |  |
| 80 kg | 37% | 0.02 | -0.36 | 0.01 | 1.46 | 9 | 1 | 7 | 0 | 0 | 1 | 131 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.96 | 67% | 48% | 0.91 | 62% | 0.01 | 3 | 1 | 2 | 0 | 0 | 0 |
| long | 0.75 | 56% | 35% | 0.93 | 46% | 0.03 | 8 | 2 | 6 | 0 | 0 | 0 |
| sphere | 0.98 | 24% | 13% | 0.97 | 68% | -0.04 | 1 | 0 | 1 | 0 | 0 | 0 |
| cylinder | 0.33 | 16% | 7% | 0.95 | 30% | 0.00 | 18 | 0 | 17 | 0 | 0 | 0 |
| arch | 0.56 | 42% | 26% | 0.81 | 45% | 0.06 | 19 | 0 | 18 | 0 | 0 | 0 |
| dumbbell | 0.85 | 54% | 34% | 0.92 | 71% | 0.12 | 7 | 0 | 6 | 0 | 0 | 0 |
| t_shape | 0.06 | 33% | 10% | 0.85 | 17% | -0.00 | 27 | 1 | 15 | 0 | 0 | 11 |
| beam | 0.56 | 41% | 30% | 0.88 | 33% | 0.04 | 16 | 1 | 15 | 0 | 0 | 0 |
| l_shape | 0.60 | 51% | 30% | 0.93 | 44% | 0.02 | 15 | 0 | 12 | 0 | 0 | 2 |
| asym | 0.48 | 39% | 24% | 0.93 | 42% | 0.02 | 16 | 0 | 16 | 0 | 0 | 0 |
| u_channel | 0.10 | 24% | 14% | 0.94 | 17% | 0.00 | 35 | 1 | 32 | 0 | 0 | 1 |
| plus | 0.69 | 66% | 45% | 0.76 | 70% | 0.02 | 0 | 0 | 0 | 0 | 0 | 0 |
