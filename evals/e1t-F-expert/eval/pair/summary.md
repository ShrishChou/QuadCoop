# Pair evaluation: e1t-F-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start at their contacts; contact rule re-applied: first); TASKS: turn in place (object at the goal position, heading off 15/30/60/90 deg, capped by symmetry)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.49 | 0.61 | 0.00 | 0.00 | 5.3 | 0.00 | 0.37 | 0.48 | 0.04 | 0.05 | 1.25 |
| 40 kg | 0.63 | 0.69 | 0.00 | 0.01 | 9.5 | 0.01 | 0.37 | 0.48 | 0.03 | 0.03 | 1.26 |
| 60 kg | 0.65 | 0.62 | 0.01 | 0.00 | 8.3 | 0.01 | 0.37 | 0.49 | 0.02 | 0.02 | 1.46 |
| 80 kg | 0.60 | 0.42 | 0.01 | 0.03 | 13.1 | 0.01 | 0.36 | 0.49 | 0.02 | 0.02 | 1.48 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube |  | 0.92 | 1.00 | 1.00 | 0.92 |
| long |  | 0.67 | 0.83 | 0.83 | 0.75 |
| sphere |  | 0.92 | 1.00 | 1.00 | 1.00 |
| cylinder |  | 0.42 | 0.25 | 0.25 | 0.25 |
| arch |  | 0.42 | 0.67 | 0.83 | 0.58 |
| dumbbell |  | 0.75 | 1.00 | 0.92 | 0.75 |
| t_shape |  | 0.00 | 0.00 | 0.00 | 0.17 |
| beam (unseen) |  | 0.67 | 0.67 | 0.58 | 0.33 |
| l_shape (unseen) |  | 0.25 | 0.75 | 0.67 | 0.67 |
| asym (unseen) |  | 0.33 | 0.50 | 0.67 | 0.67 |
| u_channel (unseen) |  | 0.00 | 0.08 | 0.17 | 0.33 |
| plus (unseen) |  | 0.50 | 0.83 | 0.83 | 0.75 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.49 | 0.51 | 0.00 | 0.00 | 0.00 | 0.08 | 0.00 |
| 40 kg | 0.63 | 0.36 | 0.01 | 0.00 | 0.00 | 0.06 | 0.00 |
| 60 kg | 0.65 | 0.34 | 0.01 | 0.01 | 0.00 | 0.01 | 0.00 |
| 80 kg | 0.60 | 0.36 | 0.04 | 0.00 | 0.00 | 0.03 | 0.00 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.14 | 0.90 | 0.98 | 0.00 | 1.00 | 0.12 | 0.92 | 0.99 | 0.00 |
| 40 kg | 1.00 | 0.14 | 0.88 | 0.99 | 0.00 | 1.00 | 0.11 | 0.93 | 1.00 | 0.00 |
| 60 kg | 1.00 | 0.14 | 0.90 | 1.00 | 0.00 | 1.00 | 0.11 | 0.91 | 1.00 | 0.00 |
| 80 kg | 1.00 | 0.14 | 0.90 | 1.00 | 0.00 | 1.00 | 0.11 | 0.92 | 1.00 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.02 | 0.03 | 1.00 | 0.02 | 0.02 |
| 40 kg | 1.00 | 0.02 | 0.05 | 1.00 | 0.02 | 0.03 |
| 60 kg | 1.00 | 0.02 | 0.05 | 1.00 | 0.02 | 0.05 |
| 80 kg | 1.00 | 0.02 | 0.06 | 1.00 | 0.02 | 0.05 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.72 | 0.84 | 0.63 |
| 40 kg | 0.74 | 0.88 | 0.51 |
| 60 kg | 0.78 | 0.87 | 0.38 |
| 80 kg | 0.77 | 0.87 | 0.31 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.18 | 0.66 | 15.37 | 0.00 | 0.00 | 0.00 | 19.50 | 0.00 | 0.17 |
| 40 kg | 0.01 | 0.70 | 12.59 | 0.00 | 0.00 | 0.00 | 18.69 | 0.00 | 0.13 |
| 60 kg | 0.00 | 0.72 | 11.27 | 0.00 | 0.00 | 0.00 | 17.12 | 0.00 | 0.13 |
| 80 kg | 0.01 | 0.71 | 12.90 | 0.00 | 0.00 | 0.00 | 14.24 | 0.00 | 0.13 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 95 | 239 | 196 |
| 40 kg | 132 | 299 | 267 |
| 60 kg | 157 | 329 | 310 |
| 80 kg | 172 | 337 | 329 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 734 | 0.47 | 0.56 (79) | 0.50 (74) | 0.48 (194) | 0.44 (71) | 0.41 (316) |
| 40 kg | 886 | 0.45 | 0.57 (170) | 0.54 (76) | 0.49 (327) | 0.52 (69) | 0.43 (244) |
| 60 kg | 1160 | 0.44 | 0.65 (253) | 0.55 (109) | 0.48 (437) | 0.45 (162) | 0.48 (199) |
| 80 kg | 2015 | 0.41 | 0.58 (342) | 0.54 (202) | 0.48 (986) | 0.41 (156) | 0.49 (329) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.13 | 0.02 | 0.01 | 0.02 |
| long | 0.01 | 0.00 | 0.01 | 0.00 |
| sphere | 0.00 | 0.00 | 0.00 | 0.00 |
| cylinder | 0.00 | 0.00 | 0.00 | 0.00 |
| arch | 0.08 | 0.00 | 0.01 | 0.01 |
| dumbbell | 0.00 | 0.00 | 0.02 | 0.05 |
| t_shape | 0.08 | 0.05 | 0.08 | 0.01 |
| beam | 0.00 | 0.00 | 0.01 | 0.02 |
| l_shape | 0.04 | 0.11 | 0.04 | 0.04 |
| asym | 0.03 | 0.03 | 0.01 | 0.03 |
| u_channel | 0.00 | 0.01 | 0.01 | 0.01 |
| plus | 0.06 | 0.08 | 0.00 | 0.00 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| T15 | 0.64 | 0.75 | 0.86 | 0.97 |
| T30 | 0.31 | 0.58 | 0.72 | 0.58 |
| T60 | 0.58 | 0.58 | 0.58 | 0.50 |
| T90 | 0.42 | 0.61 | 0.42 | 0.33 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 15% | 0% | 85% | 29% | 3% | 68% |  |  | 15% | 55% | 57% | 12% |
| 40 kg | 12% | 0% | 88% | 41% | 2% | 56% |  |  | 12% | 69% | 38% | 12% |
| 60 kg | 12% | 0% | 88% | 49% | 2% | 49% |  |  | 12% | 71% | 34% | 16% |
| 80 kg | 12% | 0% | 88% | 54% | 2% | 45% |  |  | 12% | 70% | 38% | 18% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 134 | 0.88 | 9% | 16% | 22% | 61% |
| 40 kg | 167 | 0.90 | 7% | 25% | 30% | 44% |
| 60 kg | 188 | 0.92 | 5% | 31% | 35% | 34% |
| 80 kg | 199 | 0.91 | 6% | 34% | 38% | 28% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 48% | 0.05 | -0.21 | 0.03 | 1.60 | 20 | 0 | 18 | 0 | 0 | 3 | 55 | 0.00 |  |
| 40 kg | 52% | 0.04 | -0.24 | 0.03 | 1.19 | 12 | 0 | 11 | 0 | 0 | 1 | 86 | 0.00 |  |
| 60 kg | 48% | 0.03 | -0.28 | 0.02 | 1.10 | 9 | 0 | 8 | 0 | 0 | 1 | 118 | 0.00 |  |
| 80 kg | 37% | 0.02 | -0.36 | 0.01 | 1.22 | 9 | 1 | 7 | 0 | 0 | 1 | 125 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.96 | 67% | 48% | 0.91 | 61% | 0.01 | 2 | 1 | 2 | 0 | 0 | 0 |
| long | 0.77 | 56% | 35% | 0.93 | 47% | 0.03 | 6 | 1 | 5 | 0 | 0 | 0 |
| sphere | 0.98 | 23% | 12% | 0.97 | 68% | -0.04 | 1 | 0 | 1 | 0 | 0 | 0 |
| cylinder | 0.29 | 16% | 7% | 0.94 | 29% | 0.00 | 16 | 0 | 16 | 0 | 0 | 0 |
| arch | 0.62 | 45% | 28% | 0.82 | 52% | 0.07 | 15 | 0 | 15 | 0 | 0 | 0 |
| dumbbell | 0.85 | 53% | 33% | 0.93 | 69% | 0.11 | 6 | 0 | 6 | 0 | 0 | 0 |
| t_shape | 0.04 | 33% | 9% | 0.86 | 17% | -0.00 | 27 | 0 | 15 | 0 | 0 | 12 |
| beam | 0.56 | 43% | 32% | 0.87 | 33% | 0.04 | 15 | 1 | 14 | 0 | 0 | 0 |
| l_shape | 0.58 | 50% | 29% | 0.93 | 43% | 0.02 | 14 | 0 | 11 | 0 | 0 | 3 |
| asym | 0.54 | 40% | 26% | 0.93 | 44% | 0.02 | 16 | 0 | 16 | 0 | 0 | 0 |
| u_channel | 0.15 | 27% | 15% | 0.94 | 22% | 0.01 | 32 | 1 | 30 | 0 | 0 | 1 |
| plus | 0.73 | 65% | 44% | 0.77 | 69% | 0.02 | 0 | 0 | 0 | 0 | 0 | 0 |
