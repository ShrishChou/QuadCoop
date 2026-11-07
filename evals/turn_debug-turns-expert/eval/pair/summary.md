# Pair evaluation: turn_debug-turns-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start at their contacts; contact rule re-applied: auto); TASKS: turn in place (object at the goal position, heading off 15/30/60/90 deg, capped by symmetry)

success = 10 cm / 6 deg held 1 s within 30 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.76 | 0.83 | 0.00 | 0.00 | 7.4 | 0.00 | 0.34 | 0.36 | 0.02 | 0.03 | 1.21 |
| 40 kg | 0.81 | 0.74 | 0.00 | 0.01 | 6.2 | 0.00 | 0.36 | 0.39 | 0.02 | 0.03 | 1.50 |
| 60 kg | 0.68 | 0.56 | 0.01 | 0.01 | 6.8 | 0.00 | 0.30 | 0.47 | 0.02 | 0.02 | 1.48 |
| 80 kg | 0.58 | 0.34 | 0.00 | 0.01 | 9.8 | 0.00 | 0.30 | 0.46 | 0.01 | 0.01 | 1.49 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube |  | 0.92 | 0.67 | 0.50 | 0.42 |
| long |  | 0.92 | 0.83 | 0.75 | 0.42 |
| sphere |  | 1.00 | 1.00 | 1.00 | 1.00 |
| cylinder |  | 0.33 | 0.17 | 0.25 | 0.17 |
| arch |  | 0.92 | 1.00 | 0.92 | 0.75 |
| dumbbell |  | 1.00 | 0.92 | 0.75 | 0.83 |
| t_shape |  | 0.58 | 0.92 | 0.75 | 0.67 |
| beam (unseen) |  | 0.92 | 0.83 | 0.42 | 0.33 |
| l_shape (unseen) |  | 0.75 | 1.00 | 0.67 | 0.58 |
| asym (unseen) |  | 0.50 | 0.83 | 0.83 | 0.42 |
| u_channel (unseen) |  | 0.58 | 0.67 | 0.33 | 0.58 |
| plus (unseen) |  | 0.75 | 0.92 | 1.00 | 0.83 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.76 | 0.24 | 0.00 | 0.00 | 0.00 | 0.01 | 5.25 |
| 40 kg | 0.81 | 0.17 | 0.01 | 0.00 | 0.00 | 0.00 | 4.05 |
| 60 kg | 0.68 | 0.29 | 0.03 | 0.00 | 0.00 | 0.01 | 3.84 |
| 80 kg | 0.58 | 0.41 | 0.01 | 0.00 | 0.00 | 0.01 | 3.19 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.17 | 0.85 | 0.94 | 0.00 | 1.00 | 0.15 | 0.87 | 0.95 | 0.00 |
| 40 kg | 1.00 | 0.14 | 0.89 | 0.97 | 0.00 | 1.00 | 0.12 | 0.91 | 0.98 | 0.00 |
| 60 kg | 1.00 | 0.12 | 0.91 | 0.98 | 0.00 | 1.00 | 0.11 | 0.92 | 0.98 | 0.00 |
| 80 kg | 1.00 | 0.12 | 0.92 | 0.99 | 0.00 | 1.00 | 0.11 | 0.92 | 0.99 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.97 | 0.61 | 0.07 | 0.97 | 0.52 | 0.06 |
| 40 kg | 0.99 | 0.31 | 0.08 | 0.99 | 0.24 | 0.06 |
| 60 kg | 0.99 | 0.14 | 0.07 | 0.99 | 0.19 | 0.06 |
| 80 kg | 0.99 | 0.07 | 0.06 | 0.98 | 0.12 | 0.05 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.62 | 0.74 | 0.34 |
| 40 kg | 0.65 | 0.80 | 0.27 |
| 60 kg | 0.72 | 0.82 | 0.22 |
| 80 kg | 0.73 | 0.82 | 0.17 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.09 | 0.57 | 7.43 | 5.25 | 0.05 | 0.01 | 1.90 | 0.00 | 0.22 |
| 40 kg | 0.05 | 0.61 | 4.78 | 4.05 | 0.03 | 0.00 | 2.28 | 0.00 | 0.17 |
| 60 kg | 0.02 | 0.65 | 5.13 | 3.84 | 0.17 | 0.00 | 2.77 | 0.00 | 0.12 |
| 80 kg | 0.09 | 0.66 | 6.22 | 3.19 | 0.66 | 0.15 | 3.54 | 0.00 | 0.11 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 112 | 261 | 229 |
| 40 kg | 144 | 314 | 287 |
| 60 kg | 166 | 321 | 310 |
| 80 kg | 180 | 335 | 335 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 460 | 0.39 | 0.53 (64) | 0.47 (47) | 0.50 (119) | 0.46 (103) | 0.52 (128) |
| 40 kg | 548 | 0.39 | 0.53 (77) | 0.56 (43) | 0.50 (227) | 0.51 (72) | 0.55 (129) |
| 60 kg | 927 | 0.39 | 0.52 (172) | 0.56 (72) | 0.48 (481) | 0.41 (130) | 0.43 (72) |
| 80 kg | 1259 | 0.36 | 0.64 (99) | 0.53 (109) | 0.47 (876) | 0.46 (130) | 0.51 (45) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.00 | 0.00 | 0.00 | 0.00 |
| long | 0.01 | 0.03 | 0.01 | 0.00 |
| sphere | 0.02 | 0.00 | 0.00 | 0.00 |
| cylinder | 0.00 | 0.00 | 0.00 | 0.00 |
| arch | 0.01 | 0.01 | 0.01 | 0.02 |
| dumbbell | 0.00 | 0.02 | 0.00 | 0.00 |
| t_shape | 0.02 | 0.02 | 0.03 | 0.01 |
| beam | 0.02 | 0.01 | 0.01 | 0.00 |
| l_shape | 0.04 | 0.07 | 0.07 | 0.02 |
| asym | 0.03 | 0.06 | 0.02 | 0.00 |
| u_channel | 0.03 | 0.00 | 0.00 | 0.00 |
| plus | 0.00 | 0.01 | 0.05 | 0.00 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| T15 | 0.86 | 0.92 | 0.97 | 0.97 |
| T30 | 0.72 | 0.81 | 0.69 | 0.64 |
| T60 | 0.72 | 0.86 | 0.67 | 0.47 |
| T90 | 0.75 | 0.67 | 0.39 | 0.25 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 25% | 0% | 75% | 40% | 4% | 56% |  |  | 14% | 31% | 72% | 14% |
| 40 kg | 18% | 0% | 82% | 51% | 2% | 47% |  |  | 13% | 40% | 64% | 14% |
| 60 kg | 13% | 0% | 87% | 55% | 2% | 44% |  |  | 10% | 58% | 45% | 14% |
| 80 kg | 11% | 0% | 89% | 58% | 1% | 41% |  |  | 9% | 70% | 31% | 16% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 147 | 0.92 | 4% | 20% | 32% | 48% |
| 40 kg | 176 | 0.93 | 4% | 29% | 37% | 34% |
| 60 kg | 192 | 0.93 | 3% | 35% | 38% | 27% |
| 80 kg | 202 | 0.93 | 4% | 37% | 40% | 23% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 64% | 0.07 | -0.17 | 0.05 | 0.20 | 1 | 0 | 1 | 0 | 0 | 0 | 80 | 0.00 |  |
| 40 kg | 62% | 0.05 | -0.21 | 0.04 | 0.12 | 1 | 0 | 1 | 0 | 0 | 0 | 85 | 0.00 |  |
| 60 kg | 51% | 0.03 | -0.28 | 0.02 | 0.24 | 1 | 0 | 1 | 0 | 0 | 0 | 122 | 0.00 |  |
| 80 kg | 37% | 0.02 | -0.38 | 0.01 | 0.47 | 3 | 1 | 2 | 0 | 0 | 0 | 130 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.62 | 61% | 39% | 0.94 | 40% | 0.01 | 4 | 1 | 3 | 0 | 0 | 0 |
| long | 0.73 | 59% | 37% | 0.93 | 49% | 0.03 | 2 | 1 | 1 | 0 | 0 | 0 |
| sphere | 1.00 | 22% | 11% | 0.97 | 72% | -0.06 | 0 | 0 | 0 | 0 | 0 | 0 |
| cylinder | 0.23 | 16% | 6% | 0.95 | 31% | 0.00 | 4 | 0 | 4 | 0 | 0 | 0 |
| arch | 0.90 | 58% | 34% | 0.90 | 70% | 0.09 | 1 | 0 | 0 | 0 | 0 | 0 |
| dumbbell | 0.88 | 56% | 35% | 0.93 | 73% | 0.12 | 1 | 0 | 1 | 0 | 0 | 0 |
| t_shape | 0.73 | 62% | 36% | 0.94 | 57% | 0.02 | 0 | 0 | 0 | 0 | 0 | 0 |
| beam | 0.62 | 47% | 33% | 0.89 | 37% | 0.05 | 2 | 0 | 1 | 0 | 0 | 0 |
| l_shape | 0.75 | 61% | 37% | 0.93 | 57% | 0.02 | 0 | 0 | 0 | 0 | 0 | 0 |
| asym | 0.65 | 58% | 32% | 0.93 | 44% | 0.02 | 3 | 1 | 2 | 0 | 0 | 0 |
| u_channel | 0.54 | 56% | 30% | 0.93 | 53% | 0.03 | 1 | 0 | 1 | 0 | 0 | 0 |
| plus | 0.88 | 55% | 34% | 0.91 | 59% | 0.03 | 0 | 0 | 0 | 0 | 0 | 0 |
