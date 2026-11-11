# Pair evaluation: e1t-A-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto); TASKS: turn in place (object at the goal position, heading off 15/30/60/90 deg, capped by symmetry)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.83 | 0.78 | 0.01 | 0.01 | 20.6 | 0.04 | 0.19 | 0.21 | 0.02 | 0.08 | 1.21 |
| 40 kg | 0.81 | 0.66 | 0.01 | 0.01 | 18.9 | 0.05 | 0.18 | 0.22 | 0.02 | 0.08 | 1.33 |
| 60 kg | 0.72 | 0.55 | 0.01 | 0.03 | 19.2 | 0.04 | 0.19 | 0.29 | 0.03 | 0.07 | 1.38 |
| 80 kg | 0.74 | 0.47 | 0.05 | 0.01 | 23.7 | 0.05 | 0.22 | 0.31 | 0.04 | 0.08 | 1.31 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube |  | 0.92 | 1.00 | 0.92 | 0.92 |
| long |  | 0.83 | 0.83 | 0.67 | 0.75 |
| sphere |  | 1.00 | 1.00 | 1.00 | 1.00 |
| cylinder |  | 0.50 | 0.17 | 0.25 | 0.25 |
| arch |  | 0.92 | 1.00 | 0.92 | 0.92 |
| dumbbell |  | 0.75 | 0.75 | 0.42 | 0.50 |
| t_shape |  | 0.92 | 0.83 | 0.83 | 0.83 |
| beam (unseen) |  | 0.75 | 0.67 | 0.58 | 0.33 |
| l_shape (unseen) |  | 0.92 | 1.00 | 0.67 | 0.92 |
| asym (unseen) |  | 0.67 | 0.92 | 0.92 | 0.75 |
| u_channel (unseen) |  | 0.83 | 0.67 | 0.83 | 0.75 |
| plus (unseen) |  | 0.92 | 0.83 | 0.58 | 0.92 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.83 | 0.15 | 0.02 | 0.00 | 0.00 | 0.02 | 9.14 |
| 40 kg | 0.81 | 0.17 | 0.02 | 0.00 | 0.00 | 0.02 | 7.83 |
| 60 kg | 0.72 | 0.24 | 0.04 | 0.00 | 0.00 | 0.02 | 9.97 |
| 80 kg | 0.74 | 0.20 | 0.06 | 0.00 | 0.00 | 0.01 | 10.35 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.49 | 0.51 | 0.71 | 0.00 | 1.00 | 0.49 | 0.51 | 0.70 | 0.00 |
| 40 kg | 1.00 | 0.48 | 0.53 | 0.73 | 0.00 | 1.00 | 0.49 | 0.51 | 0.69 | 0.00 |
| 60 kg | 1.00 | 0.46 | 0.56 | 0.73 | 0.00 | 1.00 | 0.45 | 0.57 | 0.74 | 0.00 |
| 80 kg | 1.00 | 0.45 | 0.59 | 0.75 | 0.00 | 1.00 | 0.43 | 0.59 | 0.76 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.80 | 3.50 | 0.04 | 0.79 | 3.53 | 0.06 |
| 40 kg | 0.85 | 5.03 | 0.04 | 0.84 | 4.46 | 0.07 |
| 60 kg | 0.85 | 4.44 | 0.06 | 0.86 | 5.29 | 0.07 |
| 80 kg | 0.88 | 4.65 | 0.07 | 0.89 | 5.23 | 0.09 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.39 | 0.41 | 0.23 |
| 40 kg | 0.40 | 0.42 | 0.20 |
| 60 kg | 0.43 | 0.47 | 0.17 |
| 80 kg | 0.44 | 0.49 | 0.15 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.81 | 0.30 | 17.39 | 9.14 | 0.57 | 0.00 | 7.06 | 0.00 | 0.49 |
| 40 kg | 2.41 | 0.28 | 15.35 | 7.83 | 0.62 | 0.00 | 5.90 | 0.00 | 0.48 |
| 60 kg | 2.50 | 0.33 | 15.75 | 9.97 | 0.39 | 0.22 | 4.49 | 0.00 | 0.46 |
| 80 kg | 1.74 | 0.35 | 15.69 | 10.35 | 0.70 | 0.44 | 4.08 | 0.00 | 0.44 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 105 | 246 | 193 |
| 40 kg | 133 | 286 | 250 |
| 60 kg | 161 | 313 | 290 |
| 80 kg | 179 | 336 | 321 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 872 | 0.35 | 0.46 (105) | 0.46 (89) | 0.51 (251) | 0.50 (230) | 0.51 (197) |
| 40 kg | 670 | 0.42 | 0.48 (113) | 0.51 (110) | 0.58 (128) | 0.52 (88) | 0.51 (231) |
| 60 kg | 1004 | 0.40 | 0.45 (171) | 0.45 (150) | 0.53 (339) | 0.42 (194) | 0.53 (150) |
| 80 kg | 1280 | 0.38 | 0.57 (111) | 0.47 (130) | 0.47 (764) | 0.43 (183) | 0.50 (93) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.04 | 0.01 | 0.03 | 0.00 |
| long | 0.03 | 0.08 | 0.07 | 0.01 |
| sphere | 0.00 | 0.00 | 0.00 | 0.00 |
| cylinder | 0.01 | 0.00 | 0.01 | 0.00 |
| arch | 0.02 | 0.01 | 0.02 | 0.03 |
| dumbbell | 0.01 | 0.02 | 0.01 | 0.00 |
| t_shape | 0.02 | 0.02 | 0.03 | 0.08 |
| beam | 0.03 | 0.03 | 0.03 | 0.00 |
| l_shape | 0.02 | 0.04 | 0.05 | 0.13 |
| asym | 0.02 | 0.04 | 0.07 | 0.07 |
| u_channel | 0.02 | 0.01 | 0.03 | 0.08 |
| plus | 0.07 | 0.03 | 0.01 | 0.03 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| T15 | 0.89 | 0.92 | 0.89 | 1.00 |
| T30 | 0.75 | 0.67 | 0.67 | 0.75 |
| T60 | 0.89 | 0.86 | 0.78 | 0.69 |
| T90 | 0.78 | 0.78 | 0.53 | 0.50 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 55% | 0% | 45% | 38% | 4% | 58% |  |  | 12% | 49% | 59% | 23% |
| 40 kg | 54% | 0% | 46% | 46% | 2% | 52% |  |  | 11% | 52% | 57% | 25% |
| 60 kg | 50% | 0% | 50% | 52% | 2% | 47% |  |  | 11% | 53% | 53% | 23% |
| 80 kg | 47% | 0% | 53% | 56% | 2% | 42% |  |  | 15% | 51% | 56% | 28% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 138 | 0.89 | 8% | 11% | 24% | 65% |
| 40 kg | 165 | 0.90 | 6% | 11% | 31% | 58% |
| 60 kg | 185 | 0.90 | 6% | 14% | 36% | 50% |
| 80 kg | 203 | 0.91 | 5% | 19% | 38% | 43% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 39% | 0.05 | -0.20 | 0.01 | 0.72 | 7 | 0 | 4 | 0 | 0 | 3 | 54 | 0.00 |  |
| 40 kg | 33% | 0.03 | -0.20 | 0.01 | 0.87 | 8 | 0 | 5 | 0 | 0 | 3 | 88 | 0.00 |  |
| 60 kg | 27% | 0.02 | -0.21 | 0.01 | 1.24 | 9 | 1 | 5 | 0 | 0 | 3 | 90 | 0.00 |  |
| 80 kg | 21% | 0.01 | -0.24 | 0.01 | 1.32 | 9 | 2 | 4 | 0 | 0 | 3 | 140 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.94 | 58% | 20% | 0.91 | 34% | 0.01 | 5 | 1 | 3 | 0 | 0 | 1 |
| long | 0.77 | 54% | 16% | 0.90 | 27% | 0.01 | 13 | 2 | 5 | 0 | 0 | 6 |
| sphere | 1.00 | 2% | 0% | 0.98 | 1% | -0.00 | 0 | 0 | 0 | 0 | 0 | 0 |
| cylinder | 0.29 | 16% | 4% | 0.94 | 23% | -0.00 | 16 | 0 | 9 | 0 | 0 | 7 |
| arch | 0.94 | 56% | 16% | 0.83 | 40% | 0.02 | 2 | 0 | 1 | 0 | 0 | 1 |
| dumbbell | 0.60 | 41% | 10% | 0.91 | 29% | 0.02 | 20 | 2 | 13 | 0 | 0 | 5 |
| t_shape | 0.85 | 57% | 20% | 0.89 | 39% | 0.01 | 2 | 0 | 1 | 0 | 0 | 1 |
| beam | 0.58 | 40% | 13% | 0.88 | 18% | 0.01 | 18 | 1 | 14 | 0 | 0 | 3 |
| l_shape | 0.88 | 57% | 18% | 0.91 | 43% | 0.01 | 1 | 0 | 1 | 0 | 0 | 0 |
| asym | 0.81 | 66% | 18% | 0.92 | 37% | 0.01 | 3 | 0 | 1 | 0 | 0 | 2 |
| u_channel | 0.77 | 50% | 14% | 0.93 | 35% | 0.01 | 7 | 0 | 6 | 0 | 0 | 0 |
| plus | 0.81 | 56% | 16% | 0.86 | 35% | 0.01 | 12 | 0 | 0 | 0 | 0 | 11 |
