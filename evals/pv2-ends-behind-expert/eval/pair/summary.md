# Pair evaluation: pv2-ends-behind-expert

policy: Stage 4 contact policy logs/marl2/pv2/model_17000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.83 | 0.78 | 0.03 | 0.02 | 26.8 | 0.01 | 0.42 | 0.34 | 0.12 | 0.24 | 1.02 |
| 40 kg | 0.72 | 0.61 | 0.02 | 0.05 | 30.5 | 0.01 | 0.52 | 0.32 | 0.15 | 0.24 | 1.03 |
| 60 kg | 0.56 | 0.40 | 0.06 | 0.03 | 37.3 | 0.02 | 0.61 | 0.39 | 0.23 | 0.32 | 1.03 |
| 80 kg | 0.26 | 0.20 | 0.17 | 0.08 | 36.6 | 0.01 | 0.72 | 0.52 | 0.40 | 0.49 | 1.03 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 -x end + + part 0 corner -x-y | 0.92 | 0.92 | 0.92 | 0.17 |
| long | part 0 corner -x+y + part 0 -x seg 1/2 | 0.92 | 0.67 | 0.92 | 0.25 |
| sphere | sector 225 + sector 135 | 0.92 | 1.00 | 1.00 | 0.92 |
| cylinder | part 0 -x seg 1/2 + part 0 corner -x+y | 0.83 | 0.58 | 0.42 | 0.25 |
| arch | part 3 -x + part 2 -x | 0.83 | 0.83 | 0.83 | 0.42 |
| dumbbell | part 0 -x + part 1 -x | 0.67 | 0.75 | 0.67 | 0.33 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 1.00 | 0.83 | 0.42 | 0.25 |
| beam (unseen) | part 0 -x seg 2/5 + part 0 -x seg 4/5 | 0.83 | 0.42 | 0.00 | 0.00 |
| l_shape (unseen) | part 0 corner -x-y + part 1 -x | 0.83 | 0.92 | 0.50 | 0.17 |
| asym (unseen) | part 1 -x end - + part 0 -x end + | 0.58 | 0.17 | 0.08 | 0.00 |
| u_channel (unseen) | part 0 -x seg 1/3 + part 0 -x seg 3/3 | 0.75 | 0.83 | 0.67 | 0.25 |
| plus (unseen) | part 0 -x end - + part 0 -x end + | 0.92 | 0.75 | 0.33 | 0.17 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.83 | 0.12 | 0.05 | 0.00 | 0.00 | 0.00 | 12.38 |
| 40 kg | 0.72 | 0.21 | 0.07 | 0.00 | 0.00 | 0.01 | 9.87 |
| 60 kg | 0.56 | 0.35 | 0.09 | 0.00 | 0.00 | 0.01 | 11.04 |
| 80 kg | 0.26 | 0.48 | 0.26 | 0.00 | 0.00 | 0.00 | 7.60 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.33 | 0.60 | 0.84 | 0.00 | 1.00 | 0.30 | 0.63 | 0.83 | 0.00 |
| 40 kg | 1.00 | 0.29 | 0.68 | 0.89 | 0.00 | 1.00 | 0.27 | 0.66 | 0.87 | 0.00 |
| 60 kg | 1.00 | 0.27 | 0.70 | 0.93 | 0.00 | 1.00 | 0.26 | 0.67 | 0.91 | 0.00 |
| 80 kg | 1.00 | 0.24 | 0.73 | 0.95 | 0.00 | 1.00 | 0.25 | 0.67 | 0.92 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.79 | 2.20 | 0.10 | 0.78 | 1.86 | 0.09 |
| 40 kg | 0.81 | 2.31 | 0.10 | 0.76 | 1.85 | 0.11 |
| 60 kg | 0.80 | 2.26 | 0.10 | 0.76 | 2.05 | 0.12 |
| 80 kg | 0.78 | 1.80 | 0.09 | 0.78 | 2.23 | 0.13 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.42 | 0.47 | 0.30 |
| 40 kg | 0.52 | 0.47 | 0.29 |
| 60 kg | 0.59 | 0.51 | 0.29 |
| 80 kg | 0.63 | 0.56 | 0.26 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.49 | 0.36 | 27.28 | 12.38 | 0.17 | 0.22 | 4.61 | 0.00 | 0.34 |
| 40 kg | 0.62 | 0.37 | 28.62 | 9.87 | 0.35 | 0.62 | 3.08 | 0.00 | 0.31 |
| 60 kg | 1.04 | 0.42 | 30.14 | 11.04 | 0.60 | 0.70 | 2.17 | 0.00 | 0.31 |
| 80 kg | 1.32 | 0.47 | 28.34 | 7.60 | 0.41 | 2.68 | 0.51 | 0.00 | 0.30 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 109 | 265 | 196 |
| 40 kg | 147 | 323 | 267 |
| 60 kg | 170 | 348 | 303 |
| 80 kg | 195 | 373 | 341 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 950 | 0.34 | 0.42 (109) | 0.51 (193) | 0.51 (231) | 0.49 (158) | 0.59 (260) |
| 40 kg | 1164 | 0.32 | 0.27 (174) | 0.45 (120) | 0.49 (135) | 0.58 (153) | 0.68 (581) |
| 60 kg | 1953 | 0.33 | 0.29 (242) | 0.44 (320) | 0.49 (358) | 0.55 (412) | 0.65 (621) |
| 80 kg | 2884 | 0.33 | 0.26 (91) | 0.42 (304) | 0.49 (1595) | 0.51 (530) | 0.66 (363) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.12 | 0.14 | 0.17 | 0.48 |
| long | 0.20 | 0.19 | 0.35 | 0.55 |
| sphere | 0.29 | 0.51 | 0.46 | 0.42 |
| cylinder | 0.19 | 0.17 | 0.21 | 0.42 |
| arch | 0.08 | 0.06 | 0.14 | 0.28 |
| dumbbell | 0.07 | 0.09 | 0.15 | 0.37 |
| t_shape | 0.09 | 0.11 | 0.19 | 0.40 |
| beam | 0.10 | 0.19 | 0.36 | 0.57 |
| l_shape | 0.06 | 0.12 | 0.14 | 0.29 |
| asym | 0.12 | 0.08 | 0.36 | 0.49 |
| u_channel | 0.09 | 0.07 | 0.15 | 0.41 |
| plus | 0.07 | 0.06 | 0.07 | 0.07 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.86 | 0.86 | 0.67 | 0.47 |
| B_left | 0.97 | 0.83 | 0.67 | 0.25 |
| C_backright | 0.69 | 0.64 | 0.50 | 0.19 |
| D_far_turn | 0.81 | 0.56 | 0.42 | 0.14 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 46% | 0% | 54% | 40% | 4% | 56% |  |  | 21% | 74% | 37% | 26% |
| 40 kg | 39% | 0% | 61% | 45% | 2% | 52% |  |  | 22% | 76% | 30% | 27% |
| 60 kg | 35% | 0% | 65% | 51% | 2% | 47% |  |  | 22% | 84% | 19% | 26% |
| 80 kg | 32% | 0% | 68% | 56% | 2% | 42% |  |  | 21% | 81% | 22% | 27% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 145 | 0.88 | 9% | 14% | 34% | 52% |
| 40 kg | 180 | 0.90 | 7% | 16% | 42% | 42% |
| 60 kg | 199 | 0.90 | 6% | 21% | 44% | 35% |
| 80 kg | 220 | 0.90 | 6% | 27% | 45% | 29% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 66% | 0.22 | 0.43 | 0.15 | 0.32 | 2 | 0 | 1 | 0 | 0 | 1 | 54 | 0.00 |  |
| 40 kg | 61% | 0.16 | 0.58 | 0.13 | 0.33 | 2 | 0 | 1 | 0 | 0 | 1 | 107 | 0.00 |  |
| 60 kg | 56% | 0.12 | 0.68 | 0.10 | 0.43 | 3 | 0 | 2 | 0 | 0 | 1 | 112 | 0.00 |  |
| 80 kg | 52% | 0.08 | 0.74 | 0.07 | 0.30 | 2 | 0 | 1 | 0 | 0 | 1 | 102 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.73 | 57% | 23% | 0.92 | 69% | 0.14 | 1 | 0 | 0 | 0 | 0 | 1 |
| long | 0.69 | 52% | 22% | 0.93 | 64% | 0.13 | 0 | 0 | 0 | 0 | 0 | 0 |
| sphere | 0.96 | 29% | 8% | 0.92 | 86% | 0.31 | 0 | 0 | 0 | 0 | 0 | 0 |
| cylinder | 0.52 | 33% | 12% | 0.92 | 66% | 0.11 | 1 | 0 | 1 | 0 | 0 | 0 |
| arch | 0.73 | 55% | 25% | 0.81 | 56% | 0.11 | 9 | 0 | 3 | 0 | 0 | 6 |
| dumbbell | 0.60 | 50% | 20% | 0.91 | 51% | 0.09 | 4 | 0 | 3 | 0 | 0 | 2 |
| t_shape | 0.62 | 54% | 21% | 0.90 | 57% | 0.08 | 1 | 0 | 0 | 0 | 0 | 0 |
| beam | 0.31 | 41% | 18% | 0.84 | 38% | 0.08 | 5 | 0 | 3 | 0 | 0 | 2 |
| l_shape | 0.60 | 51% | 20% | 0.92 | 57% | 0.09 | 2 | 0 | 2 | 0 | 0 | 0 |
| asym | 0.21 | 57% | 27% | 0.92 | 51% | 0.05 | 2 | 0 | 1 | 0 | 0 | 0 |
| u_channel | 0.62 | 51% | 21% | 0.93 | 54% | 0.09 | 2 | 0 | 1 | 0 | 0 | 2 |
| plus | 0.54 | 49% | 17% | 0.83 | 59% | 0.08 | 1 | 0 | 1 | 0 | 0 | 0 |
