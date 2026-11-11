# Pair evaluation: e1s-R-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.87 | 0.46 | 0.00 | 0.05 | 24.9 | 0.05 | 0.53 | 0.42 | 0.26 | 0.44 | 1.04 |
| 40 kg | 0.76 | 0.44 | 0.01 | 0.02 | 29.2 | 0.04 | 0.59 | 0.41 | 0.26 | 0.37 | 1.02 |
| 60 kg | 0.55 | 0.28 | 0.07 | 0.03 | 39.9 | 0.03 | 0.67 | 0.50 | 0.35 | 0.45 | 1.00 |
| 80 kg | 0.22 | 0.17 | 0.12 | 0.08 | 39.2 | 0.03 | 0.79 | 0.58 | 0.49 | 0.58 | 1.02 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 -x end + + part 0 corner -x-y | 1.00 | 0.83 | 0.75 | 0.25 |
| long | part 0 corner -x+y + part 0 -x seg 1/2 | 0.83 | 0.83 | 0.67 | 0.08 |
| sphere | sector 225 + sector 135 | 1.00 | 0.92 | 1.00 | 0.92 |
| cylinder | part 0 -x seg 1/2 + part 0 corner -x+y | 0.83 | 0.83 | 0.50 | 0.17 |
| arch | part 3 -x + part 2 -x | 1.00 | 0.83 | 0.67 | 0.33 |
| dumbbell | part 0 -x + part 1 -x | 0.92 | 0.83 | 0.50 | 0.17 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.92 | 0.67 | 0.50 | 0.17 |
| beam (unseen) | part 0 -x seg 2/5 + part 0 -x seg 4/5 | 0.83 | 0.50 | 0.08 | 0.00 |
| l_shape (unseen) | part 0 corner -x-y + part 1 -x | 0.92 | 0.83 | 0.75 | 0.08 |
| asym (unseen) | part 1 -x end - + part 0 -x end + | 0.58 | 0.50 | 0.08 | 0.00 |
| u_channel (unseen) | part 0 -x seg 1/3 + part 0 -x seg 3/3 | 0.75 | 0.75 | 0.75 | 0.17 |
| plus (unseen) | part 0 -x end - + part 0 -x end + | 0.83 | 0.75 | 0.33 | 0.25 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.87 | 0.08 | 0.05 | 0.00 | 0.00 | 0.00 | 5.79 |
| 40 kg | 0.76 | 0.21 | 0.03 | 0.00 | 0.00 | 0.00 | 4.33 |
| 60 kg | 0.55 | 0.35 | 0.10 | 0.00 | 0.00 | 0.00 | 4.31 |
| 80 kg | 0.22 | 0.58 | 0.20 | 0.00 | 0.00 | 0.00 | 4.32 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.27 | 0.69 | 0.89 | 0.00 | 1.00 | 0.28 | 0.70 | 0.88 | 0.00 |
| 40 kg | 1.00 | 0.23 | 0.75 | 0.93 | 0.00 | 1.00 | 0.24 | 0.77 | 0.92 | 0.00 |
| 60 kg | 1.00 | 0.21 | 0.78 | 0.95 | 0.00 | 1.00 | 0.22 | 0.76 | 0.95 | 0.00 |
| 80 kg | 1.00 | 0.21 | 0.75 | 0.96 | 0.00 | 1.00 | 0.23 | 0.72 | 0.94 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.76 | 1.71 | 0.06 | 0.75 | 1.89 | 0.07 |
| 40 kg | 0.77 | 1.81 | 0.08 | 0.73 | 1.89 | 0.06 |
| 60 kg | 0.78 | 1.96 | 0.08 | 0.75 | 2.09 | 0.10 |
| 80 kg | 0.77 | 1.63 | 0.11 | 0.76 | 2.28 | 0.14 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.53 | 0.51 | 0.24 |
| 40 kg | 0.61 | 0.53 | 0.24 |
| 60 kg | 0.67 | 0.57 | 0.23 |
| 80 kg | 0.67 | 0.56 | 0.21 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.27 | 0.44 | 20.59 | 5.79 | 0.00 | 0.00 | 0.37 | 0.00 | 0.26 |
| 40 kg | 0.08 | 0.45 | 20.85 | 4.33 | 0.14 | 0.76 | 0.74 | 0.00 | 0.23 |
| 60 kg | 0.21 | 0.49 | 23.39 | 4.31 | 0.49 | 0.55 | 1.00 | 0.00 | 0.22 |
| 80 kg | 0.14 | 0.48 | 24.95 | 4.32 | 0.32 | 1.50 | 0.38 | 0.00 | 0.26 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 91 | 230 | 147 |
| 40 kg | 133 | 292 | 224 |
| 60 kg | 163 | 322 | 271 |
| 80 kg | 180 | 335 | 311 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 832 | 0.32 | 0.27 (44) | 0.41 (118) | 0.48 (364) | 0.60 (211) | 0.75 (95) |
| 40 kg | 1502 | 0.26 | 0.18 (124) | 0.41 (302) | 0.49 (405) | 0.67 (316) | 0.87 (356) |
| 60 kg | 2595 | 0.28 | 0.29 (222) | 0.44 (893) | 0.51 (638) | 0.59 (384) | 0.82 (459) |
| 80 kg | 3496 | 0.28 | 0.19 (24) | 0.49 (497) | 0.50 (2362) | 0.54 (504) | 0.87 (110) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.41 | 0.21 | 0.44 | 0.48 |
| long | 0.34 | 0.23 | 0.46 | 0.68 |
| sphere | 0.56 | 0.57 | 0.67 | 0.63 |
| cylinder | 0.20 | 0.33 | 0.22 | 0.46 |
| arch | 0.28 | 0.25 | 0.24 | 0.32 |
| dumbbell | 0.17 | 0.19 | 0.29 | 0.48 |
| t_shape | 0.17 | 0.13 | 0.27 | 0.59 |
| beam | 0.31 | 0.33 | 0.48 | 0.58 |
| l_shape | 0.15 | 0.16 | 0.27 | 0.46 |
| asym | 0.16 | 0.24 | 0.42 | 0.33 |
| u_channel | 0.26 | 0.33 | 0.34 | 0.56 |
| plus | 0.13 | 0.12 | 0.14 | 0.27 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.89 | 0.92 | 0.81 | 0.47 |
| B_left | 0.94 | 0.81 | 0.67 | 0.14 |
| C_backright | 0.81 | 0.61 | 0.42 | 0.14 |
| D_far_turn | 0.83 | 0.69 | 0.31 | 0.11 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 34% | 0% | 66% | 39% | 5% | 55% |  |  | 14% | 81% | 25% | 21% |
| 40 kg | 27% | 0% | 73% | 50% | 3% | 46% |  |  | 12% | 91% | 11% | 23% |
| 60 kg | 24% | 0% | 76% | 58% | 3% | 39% |  |  | 13% | 93% | 9% | 22% |
| 80 kg | 28% | 0% | 72% | 66% | 2% | 32% |  |  | 20% | 94% | 9% | 28% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 126 | 0.88 | 11% | 13% | 37% | 50% |
| 40 kg | 158 | 0.88 | 9% | 22% | 43% | 34% |
| 60 kg | 182 | 0.90 | 7% | 31% | 44% | 25% |
| 80 kg | 197 | 0.91 | 5% | 40% | 42% | 19% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 68% | 0.21 | 0.63 | 0.17 | 0.43 | 2 | 0 | 1 | 0 | 0 | 1 | 54 | 0.00 |  |
| 40 kg | 65% | 0.15 | 0.73 | 0.13 | 0.44 | 3 | 0 | 3 | 0 | 0 | 1 | 74 | 0.00 |  |
| 60 kg | 59% | 0.10 | 0.76 | 0.08 | 0.51 | 3 | 0 | 2 | 0 | 0 | 1 | 99 | 0.00 |  |
| 80 kg | 51% | 0.07 | 0.80 | 0.06 | 0.38 | 2 | 0 | 1 | 0 | 0 | 1 | 170 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.71 | 59% | 31% | 0.92 | 61% | 0.11 | 1 | 0 | 1 | 0 | 0 | 0 |
| long | 0.60 | 58% | 29% | 0.93 | 63% | 0.11 | 1 | 0 | 0 | 0 | 0 | 0 |
| sphere | 0.96 | 29% | 8% | 0.94 | 83% | 0.25 | 0 | 0 | 0 | 0 | 0 | 0 |
| cylinder | 0.58 | 45% | 18% | 0.89 | 75% | 0.11 | 2 | 0 | 2 | 0 | 0 | 0 |
| arch | 0.71 | 63% | 36% | 0.86 | 64% | 0.12 | 1 | 0 | 0 | 0 | 0 | 1 |
| dumbbell | 0.60 | 57% | 27% | 0.88 | 56% | 0.10 | 5 | 0 | 4 | 0 | 0 | 1 |
| t_shape | 0.56 | 58% | 32% | 0.91 | 57% | 0.08 | 3 | 0 | 3 | 0 | 0 | 0 |
| beam | 0.35 | 43% | 21% | 0.89 | 40% | 0.09 | 5 | 0 | 3 | 0 | 0 | 2 |
| l_shape | 0.65 | 54% | 24% | 0.92 | 58% | 0.08 | 3 | 0 | 2 | 0 | 0 | 1 |
| asym | 0.29 | 64% | 39% | 0.93 | 50% | 0.06 | 3 | 1 | 2 | 0 | 0 | 0 |
| u_channel | 0.60 | 58% | 29% | 0.93 | 62% | 0.10 | 3 | 0 | 1 | 0 | 0 | 2 |
| plus | 0.54 | 53% | 26% | 0.72 | 58% | 0.09 | 2 | 1 | 1 | 0 | 0 | 0 |
