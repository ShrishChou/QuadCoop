# Pair evaluation: td-ends-behind-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.80 | 0.72 | 0.02 | 0.01 | 27.9 | 0.01 | 0.43 | 0.36 | 0.13 | 0.24 | 1.08 |
| 40 kg | 0.66 | 0.60 | 0.02 | 0.04 | 32.6 | 0.01 | 0.53 | 0.37 | 0.16 | 0.24 | 1.07 |
| 60 kg | 0.55 | 0.40 | 0.06 | 0.04 | 41.8 | 0.01 | 0.61 | 0.41 | 0.24 | 0.32 | 1.06 |
| 80 kg | 0.33 | 0.26 | 0.15 | 0.03 | 40.8 | 0.01 | 0.75 | 0.51 | 0.39 | 0.46 | 1.05 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 -x end + + part 0 corner -x-y | 0.92 | 0.92 | 0.83 | 0.33 |
| long | part 0 corner -x+y + part 0 -x seg 1/2 | 0.83 | 0.92 | 0.67 | 0.42 |
| sphere | sector 225 + sector 135 | 1.00 | 0.92 | 0.92 | 0.92 |
| cylinder | part 0 -x seg 1/2 + part 0 corner -x+y | 0.58 | 0.42 | 0.58 | 0.17 |
| arch | part 3 -x + part 2 -x | 0.92 | 0.83 | 0.83 | 0.50 |
| dumbbell | part 0 -x + part 1 -x | 0.92 | 0.42 | 0.58 | 0.25 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.83 | 0.75 | 0.67 | 0.42 |
| beam (unseen) | part 0 -x seg 2/5 + part 0 -x seg 4/5 | 0.67 | 0.42 | 0.17 | 0.00 |
| l_shape (unseen) | part 0 corner -x-y + part 1 -x | 0.83 | 0.75 | 0.42 | 0.08 |
| asym (unseen) | part 1 -x end - + part 0 -x end + | 0.58 | 0.08 | 0.00 | 0.00 |
| u_channel (unseen) | part 0 -x seg 1/3 + part 0 -x seg 3/3 | 0.83 | 0.67 | 0.50 | 0.50 |
| plus (unseen) | part 0 -x end - + part 0 -x end + | 0.67 | 0.83 | 0.42 | 0.33 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.80 | 0.17 | 0.03 | 0.01 | 0.00 | 0.01 | 12.54 |
| 40 kg | 0.66 | 0.28 | 0.06 | 0.00 | 0.00 | 0.01 | 8.97 |
| 60 kg | 0.55 | 0.35 | 0.10 | 0.00 | 0.00 | 0.00 | 10.27 |
| 80 kg | 0.33 | 0.49 | 0.18 | 0.00 | 0.00 | 0.00 | 8.02 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.28 | 0.67 | 0.87 | 0.00 | 1.00 | 0.30 | 0.64 | 0.85 | 0.00 |
| 40 kg | 1.00 | 0.24 | 0.73 | 0.90 | 0.00 | 1.00 | 0.26 | 0.67 | 0.89 | 0.00 |
| 60 kg | 1.00 | 0.23 | 0.73 | 0.94 | 0.00 | 1.00 | 0.26 | 0.66 | 0.92 | 0.00 |
| 80 kg | 1.00 | 0.22 | 0.73 | 0.96 | 0.00 | 1.00 | 0.25 | 0.65 | 0.94 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.79 | 1.92 | 0.08 | 0.77 | 1.98 | 0.08 |
| 40 kg | 0.78 | 1.90 | 0.08 | 0.76 | 1.98 | 0.11 |
| 60 kg | 0.79 | 2.25 | 0.09 | 0.78 | 2.68 | 0.12 |
| 80 kg | 0.77 | 1.63 | 0.11 | 0.78 | 2.28 | 0.15 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.53 | 0.48 | 0.31 |
| 40 kg | 0.61 | 0.52 | 0.29 |
| 60 kg | 0.63 | 0.51 | 0.29 |
| 80 kg | 0.66 | 0.51 | 0.25 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.63 | 0.41 | 25.99 | 12.54 | 0.18 | 0.24 | 7.20 | 0.00 | 0.33 |
| 40 kg | 0.41 | 0.45 | 26.50 | 8.97 | 1.01 | 0.69 | 5.69 | 0.00 | 0.30 |
| 60 kg | 0.29 | 0.42 | 28.53 | 10.27 | 0.35 | 0.90 | 2.62 | 0.00 | 0.31 |
| 80 kg | 0.71 | 0.44 | 27.70 | 8.02 | 0.49 | 2.58 | 0.68 | 0.00 | 0.31 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 103 | 257 | 201 |
| 40 kg | 141 | 309 | 254 |
| 60 kg | 167 | 342 | 303 |
| 80 kg | 191 | 368 | 338 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 1157 | 0.34 | 0.46 (221) | 0.51 (172) | 0.51 (348) | 0.49 (203) | 0.62 (213) |
| 40 kg | 1692 | 0.29 | 0.29 (430) | 0.48 (144) | 0.47 (352) | 0.53 (227) | 0.76 (540) |
| 60 kg | 2022 | 0.33 | 0.32 (387) | 0.46 (327) | 0.48 (360) | 0.56 (432) | 0.69 (516) |
| 80 kg | 2631 | 0.33 | 0.37 (40) | 0.42 (450) | 0.52 (1449) | 0.54 (459) | 0.67 (233) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.11 | 0.14 | 0.20 | 0.44 |
| long | 0.09 | 0.12 | 0.20 | 0.52 |
| sphere | 0.35 | 0.40 | 0.51 | 0.52 |
| cylinder | 0.16 | 0.22 | 0.27 | 0.43 |
| arch | 0.18 | 0.19 | 0.20 | 0.28 |
| dumbbell | 0.15 | 0.12 | 0.23 | 0.39 |
| t_shape | 0.13 | 0.13 | 0.14 | 0.31 |
| beam | 0.08 | 0.13 | 0.40 | 0.52 |
| l_shape | 0.06 | 0.11 | 0.17 | 0.32 |
| asym | 0.10 | 0.12 | 0.28 | 0.44 |
| u_channel | 0.10 | 0.17 | 0.19 | 0.43 |
| plus | 0.07 | 0.05 | 0.06 | 0.06 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.81 | 0.75 | 0.72 | 0.53 |
| B_left | 0.83 | 0.69 | 0.61 | 0.31 |
| C_backright | 0.83 | 0.56 | 0.47 | 0.31 |
| D_far_turn | 0.72 | 0.64 | 0.39 | 0.17 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 41% | 0% | 59% | 39% | 4% | 57% |  |  | 19% | 72% | 36% | 23% |
| 40 kg | 35% | 0% | 65% | 46% | 3% | 52% |  |  | 19% | 73% | 32% | 23% |
| 60 kg | 34% | 0% | 66% | 51% | 2% | 47% |  |  | 21% | 81% | 23% | 25% |
| 80 kg | 34% | 0% | 66% | 58% | 2% | 40% |  |  | 23% | 83% | 21% | 28% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 142 | 0.89 | 8% | 13% | 32% | 54% |
| 40 kg | 173 | 0.90 | 7% | 17% | 41% | 41% |
| 60 kg | 196 | 0.90 | 7% | 22% | 45% | 33% |
| 80 kg | 215 | 0.89 | 8% | 30% | 44% | 26% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 63% | 0.21 | 0.46 | 0.16 | 0.58 | 4 | 0 | 3 | 0 | 0 | 1 | 57 | 0.00 |  |
| 40 kg | 58% | 0.15 | 0.58 | 0.12 | 0.62 | 4 | 0 | 3 | 0 | 0 | 1 | 111 | 0.00 |  |
| 60 kg | 55% | 0.11 | 0.67 | 0.09 | 0.62 | 4 | 0 | 3 | 0 | 0 | 1 | 116 | 0.00 |  |
| 80 kg | 52% | 0.08 | 0.76 | 0.07 | 0.50 | 3 | 0 | 2 | 0 | 0 | 1 | 128 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.75 | 57% | 25% | 0.92 | 69% | 0.15 | 0 | 0 | 0 | 0 | 0 | 0 |
| long | 0.71 | 56% | 25% | 0.91 | 59% | 0.08 | 2 | 0 | 2 | 0 | 0 | 1 |
| sphere | 0.94 | 30% | 9% | 0.92 | 84% | 0.31 | 0 | 0 | 0 | 0 | 0 | 0 |
| cylinder | 0.44 | 34% | 14% | 0.91 | 65% | 0.11 | 3 | 0 | 2 | 0 | 0 | 0 |
| arch | 0.77 | 58% | 28% | 0.82 | 61% | 0.12 | 4 | 0 | 3 | 0 | 0 | 1 |
| dumbbell | 0.54 | 47% | 19% | 0.91 | 50% | 0.10 | 7 | 0 | 5 | 0 | 0 | 2 |
| t_shape | 0.67 | 54% | 23% | 0.91 | 53% | 0.07 | 5 | 0 | 4 | 0 | 0 | 1 |
| beam | 0.31 | 36% | 18% | 0.83 | 30% | 0.06 | 11 | 0 | 8 | 0 | 0 | 2 |
| l_shape | 0.52 | 53% | 22% | 0.92 | 56% | 0.07 | 3 | 0 | 2 | 0 | 0 | 1 |
| asym | 0.17 | 54% | 25% | 0.92 | 47% | 0.06 | 2 | 0 | 2 | 0 | 0 | 1 |
| u_channel | 0.62 | 51% | 21% | 0.92 | 53% | 0.11 | 5 | 0 | 2 | 0 | 0 | 3 |
| plus | 0.56 | 53% | 20% | 0.82 | 56% | 0.08 | 4 | 0 | 2 | 0 | 0 | 1 |
