# Pair evaluation: zs-nc2-projrate-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto); WALKER OVERRIDE: anymal_c = /orcd/home/002/shrishc/quadcoop/logs/rsl_rl/walker_anymal_c/2026-11-09_00-10-27_v1_nocreep2/model_7997.pt (v1)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 1 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.58 | 0.69 | 0.08 | 0.00 | 40.1 | 0.01 | 0.38 | 0.31 | 0.09 | 0.18 | 1.09 |
| 40 kg | 0.54 | 0.52 | 0.00 | 0.02 | 34.9 | 0.00 | 0.51 | 0.32 | 0.11 | 0.17 | 1.12 |
| 60 kg | 0.42 | 0.42 | 0.06 | 0.04 | 38.1 | 0.00 | 0.61 | 0.40 | 0.22 | 0.31 | 1.14 |
| 80 kg | 0.27 | 0.23 | 0.02 | 0.02 | 40.2 | 0.01 | 0.72 | 0.51 | 0.36 | 0.44 | 1.11 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x+y + part 0 corner -x-y | 0.25 | 0.75 | 0.75 | 0.00 |
| long | part 0 -x seg 2/2 + part 0 corner -x-y | 0.25 | 0.75 | 0.25 | 0.50 |
| sphere | sector 225 + sector 135 | 1.00 | 1.00 | 0.75 | 1.00 |
| cylinder | part 0 -x seg 2/2 + part 0 corner -x-y | 0.75 | 0.50 | 0.25 | 0.25 |
| arch | part 2 -x + part 3 -x | 0.50 | 0.75 | 0.50 | 0.75 |
| dumbbell | part 0 -x + part 1 -x | 0.75 | 0.50 | 0.50 | 0.50 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.50 | 0.50 | 0.25 | 0.00 |
| beam (unseen) | part 0 -x seg 2/5 + part 0 -x seg 4/5 | 0.75 | 0.25 | 0.25 | 0.00 |
| l_shape (unseen) | part 0 corner -x-y + part 1 -x | 0.50 | 0.75 | 0.50 | 0.00 |
| asym (unseen) | part 0 corner -x+y + part 1 -x | 0.25 | 0.00 | 0.00 | 0.00 |
| u_channel (unseen) | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.50 | 0.75 | 0.50 | 0.00 |
| plus (unseen) | part 1 corner -x+y + part 1 corner -x-y | 1.00 | 0.00 | 0.50 | 0.25 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.58 | 0.31 | 0.08 | 0.02 | 0.00 | 0.04 | 11.52 |
| 40 kg | 0.54 | 0.44 | 0.02 | 0.00 | 0.00 | 0.02 | 8.90 |
| 60 kg | 0.42 | 0.44 | 0.10 | 0.04 | 0.00 | 0.00 | 9.69 |
| 80 kg | 0.27 | 0.69 | 0.04 | 0.00 | 0.00 | 0.00 | 7.27 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.27 | 0.61 | 0.80 | 0.00 | 1.00 | 0.27 | 0.64 | 0.81 | 0.00 |
| 40 kg | 1.00 | 0.24 | 0.70 | 0.88 | 0.00 | 1.00 | 0.25 | 0.69 | 0.87 | 0.00 |
| 60 kg | 1.00 | 0.22 | 0.74 | 0.93 | 0.00 | 1.00 | 0.25 | 0.65 | 0.91 | 0.00 |
| 80 kg | 1.00 | 0.21 | 0.73 | 0.95 | 0.00 | 1.00 | 0.27 | 0.63 | 0.94 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.80 | 2.74 | 0.12 | 0.76 | 2.64 | 0.10 |
| 40 kg | 0.81 | 2.92 | 0.11 | 0.75 | 2.33 | 0.14 |
| 60 kg | 0.78 | 2.43 | 0.10 | 0.75 | 3.05 | 0.19 |
| 80 kg | 0.80 | 2.47 | 0.15 | 0.72 | 2.72 | 0.22 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.41 | 0.44 | 0.30 |
| 40 kg | 0.52 | 0.50 | 0.29 |
| 60 kg | 0.62 | 0.46 | 0.25 |
| 80 kg | 0.63 | 0.44 | 0.23 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.28 | 0.37 | 40.94 | 11.52 | 0.12 | 0.00 | 4.69 | 0.00 | 0.38 |
| 40 kg | 0.88 | 0.38 | 33.99 | 8.90 | 0.27 | 0.56 | 5.00 | 0.00 | 0.36 |
| 60 kg | 0.34 | 0.41 | 30.06 | 9.69 | 0.58 | 1.00 | 3.46 | 0.00 | 0.32 |
| 80 kg | 0.29 | 0.38 | 31.57 | 7.27 | 0.56 | 4.54 | 1.38 | 0.00 | 0.33 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 131 | 267 | 222 |
| 40 kg | 161 | 313 | 264 |
| 60 kg | 186 | 330 | 294 |
| 80 kg | 203 | 348 | 321 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 499 | 0.30 | 0.40 (82) | 0.48 (47) | 0.51 (143) | 0.51 (117) | 0.53 (109) |
| 40 kg | 690 | 0.29 | 0.27 (162) | 0.46 (36) | 0.51 (105) | 0.56 (119) | 0.66 (267) |
| 60 kg | 801 | 0.29 | 0.34 (203) | 0.43 (77) | 0.50 (121) | 0.57 (136) | 0.70 (263) |
| 80 kg | 1019 | 0.25 | 0.47 (4) | 0.35 (122) | 0.53 (445) | 0.57 (253) | 0.76 (196) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.09 | 0.02 | 0.13 | 0.46 |
| long | 0.02 | 0.05 | 0.22 | 0.27 |
| sphere | 0.22 | 0.22 | 0.34 | 0.32 |
| cylinder | 0.12 | 0.15 | 0.19 | 0.41 |
| arch | 0.06 | 0.24 | 0.11 | 0.12 |
| dumbbell | 0.07 | 0.11 | 0.30 | 0.33 |
| t_shape | 0.11 | 0.10 | 0.23 | 0.31 |
| beam | 0.05 | 0.06 | 0.31 | 0.67 |
| l_shape | 0.04 | 0.08 | 0.14 | 0.44 |
| asym | 0.19 | 0.12 | 0.32 | 0.31 |
| u_channel | 0.03 | 0.04 | 0.18 | 0.26 |
| plus | 0.06 | 0.10 | 0.18 | 0.37 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.50 | 0.58 | 0.67 | 0.42 |
| B_left | 0.58 | 0.42 | 0.42 | 0.33 |
| C_backright | 0.67 | 0.67 | 0.25 | 0.25 |
| D_far_turn | 0.58 | 0.50 | 0.33 | 0.08 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 49% | 0% | 51% | 47% | 3% | 50% |  |  | 26% | 61% | 48% | 29% |
| 40 kg | 40% | 0% | 60% | 55% | 2% | 43% |  |  | 23% | 61% | 48% | 27% |
| 60 kg | 36% | 0% | 64% | 63% | 2% | 35% |  |  | 22% | 74% | 30% | 27% |
| 80 kg | 35% | 0% | 65% | 70% | 1% | 29% |  |  | 25% | 82% | 21% | 29% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 155 | 0.89 | 8% | 19% | 31% | 49% |
| 40 kg | 183 | 0.91 | 6% | 26% | 39% | 35% |
| 60 kg | 203 | 0.91 | 6% | 36% | 40% | 24% |
| 80 kg | 215 | 0.91 | 6% | 46% | 38% | 16% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 58% | 0.15 | 0.36 | 0.09 | 0.94 | 4 | 0 | 1 | 0 | 0 | 3 | 67 | 0.00 |  |
| 40 kg | 53% | 0.11 | 0.56 | 0.09 | 0.90 | 5 | 0 | 2 | 0 | 0 | 2 | 120 | 0.00 |  |
| 60 kg | 51% | 0.09 | 0.70 | 0.08 | 0.81 | 4 | 1 | 1 | 0 | 0 | 1 | 170 | 0.00 |  |
| 80 kg | 42% | 0.06 | 0.80 | 0.05 | 0.98 | 5 | 2 | 1 | 0 | 0 | 1 | 193 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.44 | 73% | 43% | 0.92 | 55% | 0.07 | 1 | 1 | 0 | 0 | 0 | 0 |
| long | 0.44 | 74% | 46% | 0.92 | 53% | 0.06 | 3 | 1 | 0 | 0 | 0 | 2 |
| sphere | 0.94 | 40% | 13% | 0.93 | 76% | 0.20 | 1 | 0 | 0 | 0 | 0 | 1 |
| cylinder | 0.44 | 31% | 13% | 0.89 | 57% | 0.08 | 2 | 0 | 1 | 0 | 0 | 0 |
| arch | 0.62 | 62% | 30% | 0.89 | 50% | 0.09 | 4 | 0 | 1 | 0 | 0 | 4 |
| dumbbell | 0.56 | 61% | 32% | 0.91 | 59% | 0.10 | 6 | 0 | 4 | 0 | 0 | 2 |
| t_shape | 0.31 | 66% | 35% | 0.92 | 47% | 0.07 | 8 | 2 | 3 | 0 | 0 | 3 |
| beam | 0.31 | 24% | 18% | 0.82 | 21% | 0.04 | 10 | 0 | 7 | 0 | 0 | 3 |
| l_shape | 0.44 | 73% | 41% | 0.91 | 49% | 0.06 | 4 | 2 | 0 | 0 | 0 | 2 |
| asym | 0.06 | 72% | 44% | 0.92 | 43% | 0.05 | 3 | 1 | 0 | 0 | 0 | 2 |
| u_channel | 0.44 | 60% | 27% | 0.92 | 48% | 0.07 | 4 | 1 | 1 | 0 | 0 | 2 |
| plus | 0.44 | 71% | 42% | 0.92 | 54% | 0.05 | 2 | 1 | 0 | 0 | 0 | 1 |
