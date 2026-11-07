# Pair evaluation: t3-base-expert

policy: Stage 4 contact policy logs/keep/marl2/hvB_aa_s0/model_13500.pt (robots start at their contacts; contact rule re-applied: auto); TASKS: turn in place (object at the goal position, heading off 15/30/60/90 deg, capped by symmetry)

success = 10 cm / 6 deg held 1 s within 30 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.75 | 0.80 | 0.00 | 0.00 | 8.5 | 0.00 | 0.35 | 0.35 | 0.01 | 0.02 | 1.23 |
| 40 kg | 0.74 | 0.69 | 0.00 | 0.01 | 6.9 | 0.00 | 0.34 | 0.45 | 0.02 | 0.03 | 1.38 |
| 60 kg | 0.63 | 0.49 | 0.01 | 0.01 | 7.9 | 0.00 | 0.32 | 0.49 | 0.02 | 0.03 | 1.48 |
| 80 kg | 0.55 | 0.36 | 0.01 | 0.01 | 10.0 | 0.00 | 0.32 | 0.49 | 0.01 | 0.02 | 1.59 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube |  | 0.75 | 0.50 | 0.42 | 0.33 |
| long |  | 0.83 | 0.83 | 0.75 | 0.58 |
| sphere |  | 0.92 | 1.00 | 1.00 | 1.00 |
| cylinder |  | 0.25 | 0.25 | 0.25 | 0.17 |
| arch |  | 0.92 | 1.00 | 0.92 | 0.75 |
| dumbbell |  | 0.92 | 1.00 | 0.75 | 0.75 |
| t_shape |  | 0.83 | 0.75 | 0.83 | 0.67 |
| beam (unseen) |  | 0.92 | 0.67 | 0.33 | 0.25 |
| l_shape (unseen) |  | 0.83 | 0.75 | 0.75 | 0.58 |
| asym (unseen) |  | 0.33 | 0.75 | 0.67 | 0.50 |
| u_channel (unseen) |  | 0.58 | 0.50 | 0.33 | 0.67 |
| plus (unseen) |  | 0.92 | 0.83 | 0.58 | 0.33 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.75 | 0.25 | 0.00 | 0.00 | 0.00 | 0.01 | 5.22 |
| 40 kg | 0.74 | 0.26 | 0.01 | 0.00 | 0.00 | 0.01 | 3.57 |
| 60 kg | 0.63 | 0.35 | 0.02 | 0.00 | 0.00 | 0.01 | 3.73 |
| 80 kg | 0.55 | 0.43 | 0.02 | 0.00 | 0.00 | 0.01 | 3.33 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.19 | 0.82 | 0.90 | 0.00 | 1.00 | 0.19 | 0.82 | 0.94 | 0.00 |
| 40 kg | 1.00 | 0.13 | 0.89 | 0.95 | 0.00 | 1.00 | 0.12 | 0.93 | 0.97 | 0.00 |
| 60 kg | 1.00 | 0.11 | 0.93 | 0.98 | 0.00 | 1.00 | 0.11 | 0.92 | 0.98 | 0.00 |
| 80 kg | 1.00 | 0.12 | 0.93 | 0.98 | 0.00 | 1.00 | 0.11 | 0.93 | 0.99 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.97 | 0.80 | 0.07 | 0.96 | 0.68 | 0.07 |
| 40 kg | 0.98 | 0.46 | 0.08 | 0.99 | 0.32 | 0.05 |
| 60 kg | 0.98 | 0.26 | 0.06 | 0.99 | 0.24 | 0.06 |
| 80 kg | 0.99 | 0.15 | 0.07 | 0.99 | 0.15 | 0.05 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.62 | 0.68 | 0.33 |
| 40 kg | 0.70 | 0.79 | 0.27 |
| 60 kg | 0.78 | 0.78 | 0.22 |
| 80 kg | 0.77 | 0.78 | 0.17 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.18 | 0.57 | 8.14 | 5.22 | 0.01 | 0.00 | 1.78 | 0.00 | 0.26 |
| 40 kg | 0.02 | 0.64 | 5.83 | 3.57 | 0.10 | 0.00 | 2.25 | 0.00 | 0.19 |
| 60 kg | 0.03 | 0.67 | 5.61 | 3.73 | 0.42 | 0.01 | 2.37 | 0.00 | 0.16 |
| 80 kg | 0.14 | 0.66 | 6.30 | 3.33 | 0.76 | 0.18 | 2.78 | 0.00 | 0.17 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 108 | 258 | 228 |
| 40 kg | 142 | 305 | 275 |
| 60 kg | 162 | 320 | 299 |
| 80 kg | 179 | 335 | 343 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 444 | 0.41 | 0.51 (84) | 0.50 (44) | 0.51 (127) | 0.48 (63) | 0.53 (126) |
| 40 kg | 630 | 0.43 | 0.54 (85) | 0.63 (78) | 0.56 (224) | 0.50 (79) | 0.50 (164) |
| 60 kg | 954 | 0.40 | 0.49 (156) | 0.62 (120) | 0.55 (447) | 0.46 (105) | 0.46 (127) |
| 80 kg | 1231 | 0.36 | 0.57 (92) | 0.60 (139) | 0.50 (787) | 0.46 (146) | 0.47 (67) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.01 | 0.00 | 0.00 | 0.00 |
| long | 0.00 | 0.03 | 0.02 | 0.00 |
| sphere | 0.01 | 0.00 | 0.00 | 0.00 |
| cylinder | 0.02 | 0.00 | 0.00 | 0.00 |
| arch | 0.01 | 0.00 | 0.06 | 0.02 |
| dumbbell | 0.02 | 0.04 | 0.05 | 0.04 |
| t_shape | 0.03 | 0.01 | 0.01 | 0.01 |
| beam | 0.01 | 0.08 | 0.05 | 0.01 |
| l_shape | 0.02 | 0.08 | 0.07 | 0.06 |
| asym | 0.02 | 0.03 | 0.01 | 0.02 |
| u_channel | 0.01 | 0.01 | 0.00 | 0.02 |
| plus | 0.01 | 0.00 | 0.01 | 0.00 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| T15 | 0.92 | 0.92 | 0.97 | 0.94 |
| T30 | 0.67 | 0.72 | 0.67 | 0.61 |
| T60 | 0.83 | 0.75 | 0.61 | 0.50 |
| T90 | 0.58 | 0.56 | 0.28 | 0.14 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 30% | 0% | 70% | 39% | 4% | 57% |  |  | 15% | 25% | 78% | 16% |
| 40 kg | 18% | 0% | 82% | 48% | 2% | 50% |  |  | 12% | 30% | 72% | 13% |
| 60 kg | 14% | 0% | 86% | 54% | 2% | 44% |  |  | 11% | 43% | 58% | 15% |
| 80 kg | 14% | 0% | 86% | 57% | 1% | 41% |  |  | 11% | 47% | 54% | 16% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 146 | 0.92 | 4% | 17% | 32% | 51% |
| 40 kg | 174 | 0.93 | 3% | 26% | 38% | 37% |
| 60 kg | 188 | 0.93 | 3% | 32% | 40% | 28% |
| 80 kg | 201 | 0.93 | 4% | 35% | 40% | 25% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 60% | 0.07 | -0.19 | 0.03 | 0.29 | 1 | 0 | 1 | 0 | 0 | 0 | 71 | 0.00 |  |
| 40 kg | 58% | 0.05 | -0.25 | 0.03 | 0.20 | 1 | 0 | 1 | 0 | 0 | 0 | 98 | 0.00 |  |
| 60 kg | 47% | 0.03 | -0.32 | 0.02 | 0.33 | 2 | 0 | 1 | 0 | 0 | 0 | 103 | 0.00 |  |
| 80 kg | 35% | 0.02 | -0.41 | 0.01 | 0.65 | 4 | 1 | 2 | 0 | 0 | 0 | 133 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.50 | 51% | 25% | 0.95 | 34% | 0.01 | 5 | 2 | 4 | 0 | 0 | 0 |
| long | 0.75 | 57% | 33% | 0.94 | 45% | 0.02 | 1 | 0 | 1 | 0 | 0 | 0 |
| sphere | 0.98 | 23% | 10% | 0.97 | 72% | -0.06 | 0 | 0 | 0 | 0 | 0 | 0 |
| cylinder | 0.23 | 19% | 8% | 0.93 | 31% | -0.00 | 4 | 0 | 4 | 0 | 0 | 0 |
| arch | 0.90 | 57% | 34% | 0.90 | 61% | 0.07 | 1 | 0 | 1 | 0 | 0 | 1 |
| dumbbell | 0.85 | 55% | 32% | 0.94 | 70% | 0.11 | 0 | 0 | 0 | 0 | 0 | 0 |
| t_shape | 0.77 | 64% | 37% | 0.94 | 60% | 0.02 | 0 | 0 | 0 | 0 | 0 | 0 |
| beam | 0.54 | 40% | 26% | 0.89 | 26% | 0.02 | 6 | 1 | 4 | 0 | 0 | 0 |
| l_shape | 0.73 | 61% | 37% | 0.93 | 56% | 0.02 | 1 | 0 | 1 | 0 | 0 | 0 |
| asym | 0.56 | 59% | 33% | 0.93 | 45% | 0.02 | 2 | 1 | 1 | 0 | 0 | 0 |
| u_channel | 0.52 | 57% | 31% | 0.93 | 52% | 0.02 | 1 | 0 | 0 | 0 | 0 | 0 |
| plus | 0.67 | 51% | 23% | 0.90 | 48% | 0.03 | 2 | 1 | 1 | 0 | 0 | 0 |
