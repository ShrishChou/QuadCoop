# Pair evaluation: e1s-E-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: first)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.13 | 0.15 | 0.01 | 0.01 | 9.1 | 0.01 | 0.20 | 0.22 | 0.07 | 0.21 | 1.03 |
| 40 kg | 0.11 | 0.13 | 0.04 | 0.01 | 11.7 | 0.01 | 0.31 | 0.27 | 0.10 | 0.22 | 1.08 |
| 60 kg | 0.12 | 0.12 | 0.04 | 0.05 | 21.7 | 0.02 | 0.44 | 0.35 | 0.18 | 0.31 | 1.07 |
| 80 kg | 0.07 | 0.06 | 0.07 | 0.07 | 14.6 | 0.01 | 0.59 | 0.38 | 0.25 | 0.35 | 1.06 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 -x end + + part 0 corner -x-y | 0.33 | 0.25 | 0.33 | 0.08 |
| long | part 0 corner -x+y + part 0 -x seg 1/2 | 0.08 | 0.08 | 0.08 | 0.00 |
| sphere | sector 225 + sector 135 | 0.33 | 0.25 | 0.42 | 0.50 |
| cylinder | part 0 -x seg 1/2 + part 0 corner -x+y | 0.17 | 0.17 | 0.17 | 0.17 |
| arch | part 3 -x + part 2 -x | 0.17 | 0.08 | 0.00 | 0.08 |
| dumbbell | part 0 -x + part 1 -x | 0.08 | 0.08 | 0.17 | 0.00 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.08 | 0.00 | 0.00 | 0.00 |
| beam (unseen) | part 0 -x seg 2/5 + part 0 -x seg 4/5 | 0.08 | 0.08 | 0.08 | 0.00 |
| l_shape (unseen) | part 0 corner -x-y + part 1 -x | 0.00 | 0.08 | 0.00 | 0.00 |
| asym (unseen) | part 1 -x end - + part 0 -x end + | 0.17 | 0.17 | 0.17 | 0.00 |
| u_channel (unseen) | part 0 -x seg 1/3 + part 0 -x seg 3/3 | 0.08 | 0.00 | 0.08 | 0.00 |
| plus (unseen) | part 0 -x end - + part 0 -x end + | 0.00 | 0.08 | 0.00 | 0.00 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.13 | 0.84 | 0.03 | 0.00 | 0.00 | 0.12 | 0.76 |
| 40 kg | 0.11 | 0.83 | 0.05 | 0.01 | 0.00 | 0.06 | 0.76 |
| 60 kg | 0.12 | 0.78 | 0.09 | 0.00 | 0.00 | 0.02 | 0.70 |
| 80 kg | 0.07 | 0.79 | 0.14 | 0.00 | 0.00 | 0.01 | 0.71 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.27 | 0.69 | 0.94 | 0.00 | 1.00 | 0.28 | 0.71 | 0.92 | 0.00 |
| 40 kg | 1.00 | 0.24 | 0.73 | 0.96 | 0.00 | 1.00 | 0.26 | 0.73 | 0.92 | 0.00 |
| 60 kg | 1.00 | 0.24 | 0.73 | 0.96 | 0.00 | 1.00 | 0.27 | 0.70 | 0.91 | 0.00 |
| 80 kg | 1.00 | 0.24 | 0.71 | 0.96 | 0.00 | 1.00 | 0.27 | 0.67 | 0.93 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.75 | 2.62 | 0.03 | 0.76 | 3.16 | 0.04 |
| 40 kg | 0.76 | 3.18 | 0.06 | 0.78 | 3.11 | 0.06 |
| 60 kg | 0.78 | 3.96 | 0.08 | 0.79 | 3.63 | 0.09 |
| 80 kg | 0.80 | 3.35 | 0.12 | 0.80 | 3.67 | 0.13 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.48 | 0.49 | 0.77 |
| 40 kg | 0.54 | 0.52 | 0.72 |
| 60 kg | 0.57 | 0.53 | 0.64 |
| 80 kg | 0.58 | 0.49 | 0.57 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.48 | 0.36 | 27.98 | 0.76 | 0.00 | 0.00 | 9.22 | 0.00 | 0.36 |
| 40 kg | 0.48 | 0.38 | 30.36 | 0.76 | 0.00 | 0.00 | 8.19 | 0.00 | 0.37 |
| 60 kg | 0.83 | 0.42 | 30.91 | 0.70 | 0.00 | 0.00 | 5.98 | 0.00 | 0.33 |
| 80 kg | 0.32 | 0.37 | 30.50 | 0.71 | 0.00 | 0.00 | 3.12 | 0.00 | 0.37 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 87 | 229 | 137 |
| 40 kg | 122 | 297 | 220 |
| 60 kg | 152 | 331 | 273 |
| 80 kg | 183 | 360 | 325 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 328 | 0.34 | 0.39 (115) | 0.54 (65) | 0.59 (50) | 0.63 (10) | 0.82 (87) |
| 40 kg | 968 | 0.35 | 0.39 (241) | 0.50 (121) | 0.49 (105) | 0.54 (83) | 0.68 (419) |
| 60 kg | 1800 | 0.34 | 0.34 (385) | 0.46 (293) | 0.50 (217) | 0.51 (192) | 0.67 (715) |
| 80 kg | 2278 | 0.29 | 0.27 (389) | 0.45 (203) | 0.49 (781) | 0.53 (272) | 0.77 (633) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.04 | 0.02 | 0.08 | 0.12 |
| long | 0.06 | 0.11 | 0.17 | 0.24 |
| sphere | 0.17 | 0.20 | 0.32 | 0.34 |
| cylinder | 0.10 | 0.21 | 0.15 | 0.23 |
| arch | 0.08 | 0.10 | 0.11 | 0.24 |
| dumbbell | 0.10 | 0.18 | 0.22 | 0.30 |
| t_shape | 0.03 | 0.02 | 0.09 | 0.18 |
| beam | 0.04 | 0.13 | 0.33 | 0.61 |
| l_shape | 0.01 | 0.02 | 0.04 | 0.13 |
| asym | 0.09 | 0.17 | 0.49 | 0.28 |
| u_channel | 0.07 | 0.05 | 0.09 | 0.23 |
| plus | 0.02 | 0.02 | 0.08 | 0.05 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.28 | 0.25 | 0.33 | 0.19 |
| B_left | 0.19 | 0.17 | 0.06 | 0.00 |
| C_backright | 0.03 | 0.00 | 0.06 | 0.00 |
| D_far_turn | 0.03 | 0.03 | 0.06 | 0.08 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 38% | 0% | 62% | 15% | 3% | 83% |  |  | 30% | 72% | 41% | 22% |
| 40 kg | 34% | 0% | 66% | 24% | 2% | 75% |  |  | 27% | 73% | 40% | 22% |
| 60 kg | 33% | 0% | 67% | 36% | 2% | 62% |  |  | 25% | 75% | 32% | 28% |
| 80 kg | 35% | 0% | 65% | 46% | 2% | 52% |  |  | 29% | 79% | 30% | 27% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 132 | 0.87 | 10% | 3% | 15% | 82% |
| 40 kg | 160 | 0.89 | 8% | 7% | 25% | 67% |
| 60 kg | 185 | 0.89 | 8% | 14% | 36% | 51% |
| 80 kg | 211 | 0.89 | 8% | 20% | 43% | 37% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 26% | 0.10 | 0.41 | 0.08 | 2.60 | 40 | 0 | 31 | 0 | 0 | 9 | 74 | 0.00 |  |
| 40 kg | 31% | 0.09 | 0.52 | 0.07 | 2.42 | 33 | 0 | 27 | 0 | 0 | 6 | 99 | 0.00 |  |
| 60 kg | 38% | 0.08 | 0.59 | 0.06 | 1.83 | 18 | 0 | 14 | 0 | 0 | 3 | 110 | 0.00 |  |
| 80 kg | 39% | 0.06 | 0.68 | 0.05 | 0.94 | 9 | 0 | 6 | 0 | 0 | 3 | 112 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.25 | 35% | 11% | 0.92 | 40% | 0.10 | 24 | 0 | 20 | 0 | 0 | 4 |
| long | 0.06 | 34% | 10% | 0.92 | 33% | 0.05 | 15 | 0 | 14 | 0 | 0 | 1 |
| sphere | 0.38 | 17% | 7% | 0.92 | 50% | 0.18 | 31 | 0 | 27 | 0 | 0 | 3 |
| cylinder | 0.17 | 21% | 8% | 0.89 | 45% | 0.09 | 20 | 0 | 20 | 0 | 0 | 0 |
| arch | 0.08 | 34% | 13% | 0.81 | 32% | 0.06 | 32 | 0 | 24 | 0 | 0 | 8 |
| dumbbell | 0.08 | 31% | 13% | 0.91 | 34% | 0.07 | 25 | 0 | 20 | 0 | 0 | 4 |
| t_shape | 0.02 | 28% | 11% | 0.90 | 26% | 0.03 | 30 | 0 | 23 | 0 | 0 | 6 |
| beam | 0.06 | 32% | 16% | 0.84 | 25% | 0.05 | 18 | 0 | 14 | 0 | 0 | 3 |
| l_shape | 0.02 | 27% | 8% | 0.91 | 29% | 0.04 | 26 | 0 | 24 | 0 | 0 | 2 |
| asym | 0.12 | 48% | 20% | 0.92 | 42% | 0.05 | 11 | 0 | 10 | 0 | 0 | 1 |
| u_channel | 0.04 | 21% | 6% | 0.92 | 23% | 0.04 | 38 | 0 | 30 | 0 | 0 | 8 |
| plus | 0.02 | 36% | 6% | 0.74 | 26% | 0.04 | 29 | 0 | 7 | 0 | 0 | 22 |
