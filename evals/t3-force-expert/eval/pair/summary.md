# Pair evaluation: t3-force-expert

policy: Stage 4 contact policy logs/keep/marl2/hvB_aa_s0/model_13500.pt (robots start at their contacts; contact rule re-applied: auto); TASKS: turn in place (object at the goal position, heading off 15/30/60/90 deg, capped by symmetry); planner settings changed: robot_push_force=320

success = 10 cm / 6 deg held 1 s within 30 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.69 | 0.72 | 0.00 | 0.00 | 8.7 | 0.00 | 0.36 | 0.35 | 0.02 | 0.04 | 1.20 |
| 40 kg | 0.74 | 0.67 | 0.00 | 0.00 | 7.8 | 0.00 | 0.36 | 0.42 | 0.02 | 0.03 | 1.41 |
| 60 kg | 0.65 | 0.51 | 0.00 | 0.01 | 7.9 | 0.00 | 0.30 | 0.48 | 0.01 | 0.02 | 1.56 |
| 80 kg | 0.48 | 0.29 | 0.01 | 0.01 | 8.8 | 0.00 | 0.33 | 0.47 | 0.01 | 0.01 | 1.56 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube |  | 0.67 | 0.50 | 0.42 | 0.25 |
| long |  | 0.67 | 0.92 | 0.75 | 0.58 |
| sphere |  | 0.92 | 1.00 | 1.00 | 1.00 |
| cylinder |  | 0.25 | 0.17 | 0.25 | 0.08 |
| arch |  | 1.00 | 1.00 | 0.92 | 0.75 |
| dumbbell |  | 0.92 | 0.83 | 0.75 | 0.50 |
| t_shape |  | 0.50 | 0.67 | 0.92 | 0.50 |
| beam (unseen) |  | 0.67 | 0.58 | 0.33 | 0.33 |
| l_shape (unseen) |  | 0.92 | 0.92 | 0.75 | 0.42 |
| asym (unseen) |  | 0.50 | 0.67 | 0.75 | 0.58 |
| u_channel (unseen) |  | 0.42 | 0.58 | 0.42 | 0.33 |
| plus (unseen) |  | 0.92 | 1.00 | 0.50 | 0.42 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.69 | 0.31 | 0.00 | 0.00 | 0.00 | 0.01 | 4.76 |
| 40 kg | 0.74 | 0.26 | 0.00 | 0.00 | 0.00 | 0.00 | 3.53 |
| 60 kg | 0.65 | 0.34 | 0.01 | 0.00 | 0.00 | 0.03 | 2.51 |
| 80 kg | 0.48 | 0.51 | 0.01 | 0.00 | 0.00 | 0.01 | 2.48 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.18 | 0.84 | 0.89 | 0.00 | 1.00 | 0.19 | 0.82 | 0.94 | 0.00 |
| 40 kg | 1.00 | 0.13 | 0.90 | 0.96 | 0.00 | 1.00 | 0.11 | 0.93 | 0.98 | 0.00 |
| 60 kg | 1.00 | 0.11 | 0.92 | 0.98 | 0.00 | 1.00 | 0.11 | 0.93 | 0.99 | 0.00 |
| 80 kg | 1.00 | 0.11 | 0.94 | 0.99 | 0.00 | 1.00 | 0.11 | 0.93 | 0.99 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.97 | 0.75 | 0.07 | 0.95 | 0.65 | 0.07 |
| 40 kg | 0.98 | 0.47 | 0.07 | 0.98 | 0.29 | 0.05 |
| 60 kg | 0.99 | 0.22 | 0.06 | 0.99 | 0.12 | 0.05 |
| 80 kg | 0.99 | 0.13 | 0.06 | 1.00 | 0.19 | 0.05 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.64 | 0.68 | 0.33 |
| 40 kg | 0.72 | 0.81 | 0.27 |
| 60 kg | 0.78 | 0.80 | 0.20 |
| 80 kg | 0.80 | 0.78 | 0.16 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.19 | 0.56 | 8.66 | 4.76 | 0.04 | 0.00 | 1.68 | 0.00 | 0.27 |
| 40 kg | 0.05 | 0.65 | 6.10 | 3.53 | 0.10 | 0.00 | 2.51 | 0.00 | 0.18 |
| 60 kg | 0.12 | 0.66 | 5.46 | 2.51 | 0.40 | 0.00 | 2.33 | 0.00 | 0.17 |
| 80 kg | 0.06 | 0.67 | 6.42 | 2.48 | 0.99 | 0.00 | 3.26 | 0.00 | 0.15 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 110 | 263 | 231 |
| 40 kg | 142 | 307 | 278 |
| 60 kg | 160 | 319 | 301 |
| 80 kg | 176 | 333 | 340 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 517 | 0.39 | 0.52 (115) | 0.49 (47) | 0.51 (160) | 0.49 (82) | 0.55 (113) |
| 40 kg | 716 | 0.42 | 0.51 (115) | 0.58 (92) | 0.54 (245) | 0.45 (85) | 0.51 (178) |
| 60 kg | 918 | 0.39 | 0.52 (124) | 0.64 (111) | 0.53 (447) | 0.48 (105) | 0.51 (132) |
| 80 kg | 1314 | 0.37 | 0.56 (112) | 0.58 (136) | 0.50 (781) | 0.43 (177) | 0.45 (107) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.01 | 0.00 | 0.00 | 0.00 |
| long | 0.00 | 0.02 | 0.00 | 0.00 |
| sphere | 0.01 | 0.00 | 0.00 | 0.00 |
| cylinder | 0.00 | 0.00 | 0.00 | 0.00 |
| arch | 0.00 | 0.00 | 0.03 | 0.03 |
| dumbbell | 0.01 | 0.03 | 0.02 | 0.00 |
| t_shape | 0.02 | 0.00 | 0.01 | 0.01 |
| beam | 0.09 | 0.05 | 0.02 | 0.02 |
| l_shape | 0.03 | 0.08 | 0.05 | 0.05 |
| asym | 0.03 | 0.05 | 0.00 | 0.01 |
| u_channel | 0.03 | 0.01 | 0.00 | 0.00 |
| plus | 0.00 | 0.01 | 0.00 | 0.00 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| T15 | 0.83 | 0.89 | 0.97 | 0.94 |
| T30 | 0.64 | 0.67 | 0.64 | 0.47 |
| T60 | 0.75 | 0.78 | 0.64 | 0.39 |
| T90 | 0.56 | 0.61 | 0.33 | 0.11 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 29% | 0% | 71% | 39% | 4% | 57% |  |  | 15% | 29% | 74% | 16% |
| 40 kg | 17% | 0% | 83% | 48% | 2% | 50% |  |  | 11% | 32% | 70% | 14% |
| 60 kg | 13% | 0% | 87% | 54% | 2% | 44% |  |  | 11% | 50% | 52% | 15% |
| 80 kg | 13% | 0% | 87% | 57% | 1% | 42% |  |  | 11% | 51% | 51% | 15% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 148 | 0.92 | 4% | 18% | 32% | 51% |
| 40 kg | 173 | 0.93 | 3% | 26% | 38% | 36% |
| 60 kg | 188 | 0.94 | 3% | 33% | 39% | 28% |
| 80 kg | 199 | 0.93 | 4% | 35% | 40% | 25% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 60% | 0.07 | -0.19 | 0.03 | 0.28 | 1 | 0 | 1 | 0 | 0 | 0 | 63 | 0.00 |  |
| 40 kg | 58% | 0.05 | -0.26 | 0.03 | 0.25 | 1 | 0 | 1 | 0 | 0 | 0 | 94 | 0.00 |  |
| 60 kg | 47% | 0.03 | -0.34 | 0.02 | 0.35 | 2 | 0 | 1 | 0 | 0 | 0 | 115 | 0.00 |  |
| 80 kg | 34% | 0.02 | -0.42 | 0.01 | 0.76 | 4 | 1 | 3 | 0 | 0 | 0 | 137 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.46 | 54% | 27% | 0.95 | 34% | 0.00 | 5 | 2 | 3 | 0 | 0 | 0 |
| long | 0.73 | 56% | 34% | 0.93 | 46% | 0.02 | 1 | 0 | 1 | 0 | 0 | 0 |
| sphere | 0.98 | 23% | 11% | 0.97 | 72% | -0.06 | 0 | 0 | 0 | 0 | 0 | 0 |
| cylinder | 0.19 | 19% | 8% | 0.93 | 31% | -0.00 | 4 | 0 | 4 | 0 | 0 | 0 |
| arch | 0.92 | 56% | 33% | 0.91 | 63% | 0.08 | 1 | 0 | 0 | 0 | 0 | 0 |
| dumbbell | 0.75 | 53% | 30% | 0.94 | 66% | 0.10 | 1 | 0 | 1 | 0 | 0 | 0 |
| t_shape | 0.65 | 64% | 40% | 0.94 | 58% | 0.02 | 0 | 0 | 0 | 0 | 0 | 0 |
| beam | 0.48 | 40% | 27% | 0.89 | 25% | 0.02 | 6 | 1 | 5 | 0 | 0 | 0 |
| l_shape | 0.75 | 61% | 37% | 0.93 | 54% | 0.02 | 1 | 0 | 1 | 0 | 0 | 0 |
| asym | 0.62 | 59% | 35% | 0.93 | 46% | 0.02 | 2 | 1 | 1 | 0 | 0 | 0 |
| u_channel | 0.44 | 57% | 31% | 0.94 | 51% | 0.02 | 1 | 0 | 1 | 0 | 0 | 0 |
| plus | 0.71 | 51% | 23% | 0.91 | 49% | 0.02 | 2 | 1 | 1 | 0 | 0 | 0 |
