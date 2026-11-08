# Pair evaluation: fair-td-v21-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto); WALKER OVERRIDE: anymal_c = /orcd/home/002/shrishc/quadcoop/logs/rsl_rl/walker_anymal_c_compliant/2026-11-08_03-50-04_v21/model_5998.pt (compliant)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.02 | 0.02 | 0.03 | 0.01 | 59.4 | 0.05 | 0.27 | 0.24 | 0.05 | 0.14 | 0.92 |
| 40 kg | 0.03 | 0.04 | 0.03 | 0.00 | 43.1 | 0.05 | 0.41 | 0.36 | 0.13 | 0.22 | 0.94 |
| 60 kg | 0.06 | 0.06 | 0.02 | 0.00 | 39.5 | 0.06 | 0.60 | 0.53 | 0.32 | 0.41 | 0.88 |
| 80 kg | 0.04 | 0.04 | 0.00 | 0.00 | 35.5 | 0.07 | 0.73 | 0.62 | 0.49 | 0.58 | 0.95 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x+y + part 0 corner -x-y | 0.00 | 0.00 | 0.00 | 0.00 |
| long | part 0 -x seg 2/2 + part 0 corner -x-y | 0.00 | 0.00 | 0.00 | 0.00 |
| sphere | sector 135 + sector 225 | 0.00 | 0.17 | 0.42 | 0.42 |
| cylinder | part 0 corner -x-y + part 0 -x seg 2/2 | 0.08 | 0.08 | 0.17 | 0.08 |
| arch | part 3 -x + part 2 -x | 0.00 | 0.00 | 0.00 | 0.00 |
| dumbbell | part 0 -x + part 1 -x | 0.00 | 0.00 | 0.00 | 0.00 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.00 | 0.00 | 0.00 | 0.00 |
| beam (unseen) | part 0 -x seg 2/5 + part 0 -x seg 4/5 | 0.00 | 0.00 | 0.00 | 0.00 |
| l_shape (unseen) | part 1 -x + part 0 corner -x-y | 0.00 | 0.00 | 0.00 | 0.00 |
| asym (unseen) | part 1 -x + part 0 corner -x+y | 0.08 | 0.00 | 0.00 | 0.00 |
| u_channel (unseen) | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.08 | 0.00 | 0.08 | 0.00 |
| plus (unseen) | part 0 corner -x-y + part 0 corner -x+y | 0.00 | 0.08 | 0.00 | 0.00 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.02 | 0.94 | 0.04 | 0.00 | 0.00 | 0.31 | 9.56 |
| 40 kg | 0.03 | 0.94 | 0.03 | 0.00 | 0.00 | 0.15 | 6.58 |
| 60 kg | 0.06 | 0.92 | 0.02 | 0.00 | 0.00 | 0.05 | 4.61 |
| 80 kg | 0.04 | 0.96 | 0.00 | 0.00 | 0.00 | 0.04 | 3.65 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.66 | 0.34 | 0.72 | 0.00 | 1.00 | 0.42 | 0.44 | 0.68 | 0.00 |
| 40 kg | 1.00 | 0.46 | 0.49 | 0.79 | 0.00 | 1.00 | 0.35 | 0.55 | 0.76 | 0.00 |
| 60 kg | 1.00 | 0.33 | 0.63 | 0.85 | 0.00 | 1.00 | 0.27 | 0.61 | 0.84 | 0.00 |
| 80 kg | 1.00 | 0.28 | 0.70 | 0.90 | 0.00 | 1.00 | 0.30 | 0.58 | 0.88 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.46 | 3.42 | 0.27 | 0.55 | 4.22 | 0.22 |
| 40 kg | 0.54 | 3.26 | 0.26 | 0.59 | 4.04 | 0.26 |
| 60 kg | 0.62 | 3.93 | 0.23 | 0.64 | 3.64 | 0.20 |
| 80 kg | 0.64 | 4.91 | 0.22 | 0.65 | 2.95 | 0.26 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.22 | 0.29 | 0.26 |
| 40 kg | 0.38 | 0.37 | 0.26 |
| 60 kg | 0.50 | 0.50 | 0.24 |
| 80 kg | 0.56 | 0.50 | 0.19 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 5.26 | 0.20 | 37.11 | 9.56 | 0.88 | 0.00 | 0.08 | 0.00 | 0.63 |
| 40 kg | 3.26 | 0.29 | 29.65 | 6.58 | 0.72 | 0.60 | 0.31 | 0.00 | 0.53 |
| 60 kg | 1.40 | 0.37 | 23.16 | 4.61 | 2.60 | 1.42 | 0.03 | 0.00 | 0.47 |
| 80 kg | 1.66 | 0.42 | 19.90 | 3.65 | 2.38 | 6.79 | 0.01 | 0.00 | 0.42 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 114 | 259 | 191 |
| 40 kg | 146 | 286 | 237 |
| 60 kg | 161 | 286 | 250 |
| 80 kg | 169 | 286 | 271 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 743 | 0.32 | 0.38 (117) | 0.48 (113) | 0.49 (141) | 0.52 (259) | 0.51 (112) |
| 40 kg | 1701 | 0.33 | 0.35 (395) | 0.48 (236) | 0.51 (191) | 0.50 (214) | 0.67 (665) |
| 60 kg | 2932 | 0.32 | 0.39 (587) | 0.45 (815) | 0.47 (560) | 0.52 (525) | 0.53 (445) |
| 80 kg | 3633 | 0.26 | 0.60 (17) | 0.49 (710) | 0.49 (2399) | 0.52 (466) | 0.56 (42) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.04 | 0.07 | 0.43 | 0.56 |
| long | 0.07 | 0.15 | 0.47 | 0.72 |
| sphere | 0.05 | 0.07 | 0.13 | 0.22 |
| cylinder | 0.03 | 0.13 | 0.26 | 0.27 |
| arch | 0.01 | 0.01 | 0.00 | 0.09 |
| dumbbell | 0.09 | 0.17 | 0.36 | 0.61 |
| t_shape | 0.07 | 0.14 | 0.40 | 0.85 |
| beam | 0.06 | 0.23 | 0.34 | 0.55 |
| l_shape | 0.05 | 0.14 | 0.32 | 0.48 |
| asym | 0.09 | 0.26 | 0.59 | 0.68 |
| u_channel | 0.06 | 0.14 | 0.40 | 0.61 |
| plus | 0.01 | 0.03 | 0.15 | 0.23 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.00 | 0.06 | 0.14 | 0.03 |
| B_left | 0.03 | 0.03 | 0.00 | 0.06 |
| C_backright | 0.03 | 0.03 | 0.06 | 0.06 |
| D_far_turn | 0.03 | 0.00 | 0.03 | 0.03 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 70% | 0% | 30% | 46% | 4% | 50% |  |  | 33% | 60% | 56% | 36% |
| 40 kg | 58% | 0% | 42% | 57% | 3% | 40% |  |  | 29% | 61% | 51% | 31% |
| 60 kg | 47% | 0% | 53% | 66% | 2% | 32% |  |  | 25% | 60% | 49% | 31% |
| 80 kg | 43% | 0% | 57% | 72% | 1% | 27% |  |  | 25% | 66% | 42% | 35% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 144 | 0.87 | 10% | 18% | 37% | 46% |
| 40 kg | 166 | 0.90 | 7% | 25% | 47% | 28% |
| 60 kg | 176 | 0.91 | 5% | 35% | 44% | 21% |
| 80 kg | 183 | 0.91 | 5% | 46% | 39% | 15% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 63% | 0.13 | 0.03 | 0.03 | 0.75 | 6 | 0 | 2 | 0 | 0 | 3 | 57 | 0.00 |  |
| 40 kg | 58% | 0.08 | 0.29 | 0.03 | 0.51 | 3 | 0 | 1 | 0 | 0 | 2 | 114 | 0.00 |  |
| 60 kg | 46% | 0.05 | 0.54 | 0.03 | 0.54 | 4 | 0 | 0 | 0 | 0 | 3 | 141 | 0.00 |  |
| 80 kg | 30% | 0.03 | 0.64 | 0.02 | 1.06 | 6 | 3 | 1 | 0 | 0 | 2 | 165 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.00 | 66% | 38% | 0.91 | 43% | 0.02 | 3 | 1 | 1 | 0 | 0 | 2 |
| long | 0.00 | 67% | 39% | 0.91 | 48% | 0.02 | 3 | 0 | 0 | 0 | 0 | 2 |
| sphere | 0.25 | 31% | 16% | 0.93 | 84% | 0.04 | 4 | 0 | 2 | 0 | 0 | 2 |
| cylinder | 0.10 | 53% | 24% | 0.91 | 72% | 0.04 | 1 | 0 | 0 | 0 | 0 | 1 |
| arch | 0.00 | 63% | 27% | 0.88 | 43% | 0.03 | 8 | 4 | 1 | 0 | 0 | 3 |
| dumbbell | 0.00 | 65% | 34% | 0.90 | 46% | 0.03 | 4 | 0 | 1 | 0 | 0 | 3 |
| t_shape | 0.00 | 65% | 36% | 0.90 | 52% | 0.03 | 2 | 0 | 0 | 0 | 0 | 1 |
| beam | 0.00 | 58% | 27% | 0.81 | 27% | 0.02 | 7 | 1 | 3 | 0 | 0 | 3 |
| l_shape | 0.00 | 61% | 27% | 0.89 | 45% | 0.02 | 5 | 0 | 1 | 0 | 0 | 4 |
| asym | 0.02 | 77% | 51% | 0.92 | 40% | 0.02 | 5 | 2 | 1 | 0 | 0 | 2 |
| u_channel | 0.04 | 62% | 29% | 0.91 | 47% | 0.03 | 3 | 0 | 0 | 0 | 0 | 3 |
| plus | 0.02 | 50% | 23% | 0.89 | 40% | 0.02 | 8 | 0 | 2 | 0 | 0 | 6 |
