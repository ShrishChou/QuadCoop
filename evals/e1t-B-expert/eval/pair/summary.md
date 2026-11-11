# Pair evaluation: e1t-B-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start at their contacts; contact rule re-applied: auto); TASKS: turn in place (object at the goal position, heading off 15/30/60/90 deg, capped by symmetry)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.91 | 0.83 | 0.00 | 0.00 | 11.0 | 0.00 | 0.36 | 0.37 | 0.03 | 0.04 | 1.18 |
| 40 kg | 0.90 | 0.82 | 0.01 | 0.01 | 8.8 | 0.00 | 0.38 | 0.43 | 0.02 | 0.04 | 1.37 |
| 60 kg | 0.85 | 0.65 | 0.01 | 0.02 | 12.7 | 0.00 | 0.35 | 0.52 | 0.02 | 0.03 | 1.35 |
| 80 kg | 0.76 | 0.53 | 0.03 | 0.03 | 15.6 | 0.00 | 0.36 | 0.52 | 0.03 | 0.03 | 1.43 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube |  | 1.00 | 1.00 | 0.92 | 0.92 |
| long |  | 0.92 | 1.00 | 0.83 | 0.67 |
| sphere |  | 1.00 | 1.00 | 1.00 | 1.00 |
| cylinder |  | 0.50 | 0.42 | 0.33 | 0.25 |
| arch |  | 1.00 | 1.00 | 1.00 | 0.83 |
| dumbbell |  | 0.92 | 0.92 | 0.83 | 0.92 |
| t_shape |  | 0.83 | 0.75 | 1.00 | 0.83 |
| beam (unseen) |  | 1.00 | 0.92 | 0.67 | 0.25 |
| l_shape (unseen) |  | 0.92 | 1.00 | 1.00 | 0.83 |
| asym (unseen) |  | 0.83 | 0.92 | 0.92 | 0.92 |
| u_channel (unseen) |  | 1.00 | 0.92 | 0.83 | 0.75 |
| plus (unseen) |  | 1.00 | 1.00 | 0.92 | 0.92 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.91 | 0.09 | 0.00 | 0.00 | 0.00 | 0.03 | 8.76 |
| 40 kg | 0.90 | 0.08 | 0.01 | 0.00 | 0.00 | 0.01 | 7.98 |
| 60 kg | 0.85 | 0.11 | 0.03 | 0.00 | 0.00 | 0.01 | 10.90 |
| 80 kg | 0.76 | 0.17 | 0.07 | 0.00 | 0.00 | 0.00 | 11.10 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.17 | 0.84 | 0.94 | 0.00 | 1.00 | 0.18 | 0.82 | 0.94 | 0.00 |
| 40 kg | 1.00 | 0.15 | 0.86 | 0.97 | 0.00 | 1.00 | 0.14 | 0.86 | 0.95 | 0.00 |
| 60 kg | 1.00 | 0.12 | 0.91 | 0.98 | 0.00 | 1.00 | 0.12 | 0.90 | 0.97 | 0.00 |
| 80 kg | 1.00 | 0.13 | 0.90 | 0.98 | 0.00 | 1.00 | 0.12 | 0.92 | 0.98 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.96 | 0.54 | 0.06 | 0.96 | 0.58 | 0.06 |
| 40 kg | 0.98 | 0.34 | 0.06 | 0.99 | 0.39 | 0.06 |
| 60 kg | 1.00 | 0.36 | 0.05 | 0.99 | 0.36 | 0.06 |
| 80 kg | 0.99 | 0.26 | 0.06 | 0.99 | 0.28 | 0.05 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.67 | 0.75 | 0.32 |
| 40 kg | 0.72 | 0.79 | 0.25 |
| 60 kg | 0.78 | 0.83 | 0.23 |
| 80 kg | 0.78 | 0.85 | 0.17 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.09 | 0.63 | 8.85 | 8.76 | 0.28 | 0.00 | 9.39 | 0.00 | 0.21 |
| 40 kg | 0.06 | 0.66 | 6.42 | 7.98 | 0.06 | 0.00 | 7.37 | 0.00 | 0.16 |
| 60 kg | 0.07 | 0.68 | 7.49 | 10.90 | 0.24 | 0.01 | 5.17 | 0.00 | 0.16 |
| 80 kg | 0.09 | 0.70 | 9.62 | 11.10 | 0.60 | 0.46 | 4.71 | 0.00 | 0.14 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 107 | 258 | 224 |
| 40 kg | 143 | 310 | 289 |
| 60 kg | 164 | 333 | 316 |
| 80 kg | 178 | 342 | 333 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 597 | 0.36 | 0.49 (64) | 0.51 (58) | 0.50 (229) | 0.46 (133) | 0.52 (113) |
| 40 kg | 612 | 0.38 | 0.37 (106) | 0.55 (87) | 0.50 (181) | 0.46 (117) | 0.51 (121) |
| 60 kg | 1024 | 0.38 | 0.51 (196) | 0.52 (160) | 0.49 (406) | 0.48 (149) | 0.57 (114) |
| 80 kg | 1602 | 0.37 | 0.63 (119) | 0.52 (191) | 0.49 (974) | 0.44 (216) | 0.50 (103) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.04 | 0.01 | 0.00 | 0.00 |
| long | 0.02 | 0.01 | 0.03 | 0.00 |
| sphere | 0.00 | 0.00 | 0.00 | 0.00 |
| cylinder | 0.00 | 0.00 | 0.00 | 0.00 |
| arch | 0.00 | 0.00 | 0.03 | 0.02 |
| dumbbell | 0.00 | 0.00 | 0.00 | 0.03 |
| t_shape | 0.01 | 0.01 | 0.06 | 0.04 |
| beam | 0.03 | 0.02 | 0.01 | 0.00 |
| l_shape | 0.07 | 0.11 | 0.06 | 0.08 |
| asym | 0.08 | 0.08 | 0.06 | 0.07 |
| u_channel | 0.02 | 0.01 | 0.03 | 0.06 |
| plus | 0.03 | 0.03 | 0.02 | 0.00 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| T15 | 0.97 | 0.97 | 1.00 | 0.94 |
| T30 | 0.83 | 0.83 | 0.83 | 0.81 |
| T60 | 0.97 | 0.97 | 0.92 | 0.75 |
| T90 | 0.86 | 0.83 | 0.67 | 0.53 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 24% | 0% | 76% | 42% | 4% | 54% |  |  | 10% | 49% | 57% | 14% |
| 40 kg | 18% | 0% | 82% | 51% | 2% | 46% |  |  | 9% | 57% | 47% | 14% |
| 60 kg | 15% | 0% | 85% | 55% | 2% | 43% |  |  | 10% | 58% | 45% | 15% |
| 80 kg | 13% | 0% | 87% | 58% | 2% | 40% |  |  | 10% | 55% | 47% | 18% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 145 | 0.89 | 7% | 21% | 32% | 47% |
| 40 kg | 176 | 0.91 | 5% | 29% | 38% | 34% |
| 60 kg | 193 | 0.93 | 4% | 34% | 38% | 28% |
| 80 kg | 204 | 0.92 | 4% | 37% | 39% | 24% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 65% | 0.07 | -0.17 | 0.05 | 0.42 | 3 | 0 | 3 | 0 | 0 | 0 | 70 | 0.00 |  |
| 40 kg | 63% | 0.05 | -0.17 | 0.04 | 0.38 | 3 | 0 | 3 | 0 | 0 | 0 | 83 | 0.00 |  |
| 60 kg | 53% | 0.03 | -0.21 | 0.02 | 0.42 | 3 | 0 | 3 | 0 | 0 | 0 | 94 | 0.00 |  |
| 80 kg | 42% | 0.02 | -0.30 | 0.01 | 0.87 | 5 | 1 | 4 | 0 | 0 | 0 | 135 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.96 | 65% | 45% | 0.91 | 57% | 0.02 | 4 | 1 | 3 | 0 | 0 | 0 |
| long | 0.85 | 59% | 37% | 0.93 | 51% | 0.03 | 5 | 1 | 4 | 0 | 0 | 0 |
| sphere | 1.00 | 21% | 9% | 0.97 | 67% | -0.05 | 0 | 0 | 0 | 0 | 0 | 0 |
| cylinder | 0.38 | 15% | 5% | 0.95 | 30% | 0.00 | 16 | 0 | 16 | 0 | 0 | 0 |
| arch | 0.96 | 58% | 34% | 0.90 | 66% | 0.09 | 1 | 0 | 0 | 0 | 0 | 0 |
| dumbbell | 0.90 | 55% | 35% | 0.93 | 73% | 0.12 | 5 | 0 | 5 | 0 | 0 | 0 |
| t_shape | 0.85 | 57% | 23% | 0.86 | 48% | 0.01 | 2 | 0 | 1 | 0 | 0 | 0 |
| beam | 0.71 | 47% | 33% | 0.89 | 37% | 0.04 | 5 | 1 | 3 | 0 | 0 | 1 |
| l_shape | 0.94 | 61% | 35% | 0.93 | 59% | 0.03 | 2 | 0 | 2 | 0 | 0 | 0 |
| asym | 0.90 | 64% | 40% | 0.92 | 63% | 0.04 | 1 | 0 | 1 | 0 | 0 | 0 |
| u_channel | 0.88 | 57% | 29% | 0.93 | 54% | 0.03 | 1 | 0 | 1 | 0 | 0 | 0 |
| plus | 0.96 | 62% | 36% | 0.83 | 65% | 0.02 | 0 | 0 | 0 | 0 | 0 | 0 |
