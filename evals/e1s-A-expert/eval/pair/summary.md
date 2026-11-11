# Pair evaluation: e1s-A-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.76 | 0.72 | 0.01 | 0.00 | 28.4 | 0.01 | 0.42 | 0.37 | 0.13 | 0.23 | 1.07 |
| 40 kg | 0.67 | 0.60 | 0.03 | 0.03 | 32.1 | 0.01 | 0.51 | 0.40 | 0.15 | 0.22 | 1.08 |
| 60 kg | 0.53 | 0.40 | 0.06 | 0.06 | 36.5 | 0.01 | 0.63 | 0.44 | 0.25 | 0.34 | 1.05 |
| 80 kg | 0.33 | 0.23 | 0.10 | 0.02 | 38.3 | 0.01 | 0.75 | 0.53 | 0.40 | 0.48 | 1.05 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 -x end + + part 0 corner -x-y | 0.83 | 0.92 | 0.75 | 0.42 |
| long | part 0 corner -x+y + part 0 -x seg 1/2 | 0.67 | 0.83 | 0.67 | 0.42 |
| sphere | sector 225 + sector 135 | 1.00 | 1.00 | 1.00 | 1.00 |
| cylinder | part 0 -x seg 1/2 + part 0 corner -x+y | 0.67 | 0.33 | 0.50 | 0.33 |
| arch | part 3 -x + part 2 -x | 0.83 | 0.92 | 0.75 | 0.42 |
| dumbbell | part 0 -x + part 1 -x | 0.75 | 0.67 | 0.67 | 0.42 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.75 | 0.42 | 0.50 | 0.17 |
| beam (unseen) | part 0 -x seg 2/5 + part 0 -x seg 4/5 | 0.75 | 0.42 | 0.08 | 0.00 |
| l_shape (unseen) | part 0 corner -x-y + part 1 -x | 0.92 | 0.83 | 0.58 | 0.17 |
| asym (unseen) | part 1 -x end - + part 0 -x end + | 0.50 | 0.17 | 0.00 | 0.00 |
| u_channel (unseen) | part 0 -x seg 1/3 + part 0 -x seg 3/3 | 0.83 | 0.83 | 0.50 | 0.42 |
| plus (unseen) | part 0 -x end - + part 0 -x end + | 0.58 | 0.67 | 0.42 | 0.25 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.76 | 0.23 | 0.01 | 0.00 | 0.00 | 0.01 | 11.58 |
| 40 kg | 0.67 | 0.28 | 0.06 | 0.00 | 0.00 | 0.01 | 9.12 |
| 60 kg | 0.53 | 0.35 | 0.12 | 0.00 | 0.00 | 0.00 | 10.17 |
| 80 kg | 0.33 | 0.55 | 0.12 | 0.00 | 0.00 | 0.00 | 8.47 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.29 | 0.65 | 0.87 | 0.00 | 1.00 | 0.29 | 0.64 | 0.85 | 0.00 |
| 40 kg | 1.00 | 0.25 | 0.72 | 0.91 | 0.00 | 1.00 | 0.25 | 0.69 | 0.89 | 0.00 |
| 60 kg | 1.00 | 0.25 | 0.72 | 0.93 | 0.00 | 1.00 | 0.25 | 0.68 | 0.91 | 0.00 |
| 80 kg | 1.00 | 0.23 | 0.74 | 0.96 | 0.00 | 1.00 | 0.25 | 0.66 | 0.93 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.79 | 2.07 | 0.07 | 0.76 | 1.96 | 0.08 |
| 40 kg | 0.79 | 1.88 | 0.08 | 0.77 | 2.03 | 0.10 |
| 60 kg | 0.79 | 2.11 | 0.09 | 0.78 | 1.96 | 0.12 |
| 80 kg | 0.78 | 1.68 | 0.11 | 0.78 | 2.25 | 0.15 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.54 | 0.50 | 0.30 |
| 40 kg | 0.58 | 0.55 | 0.29 |
| 60 kg | 0.64 | 0.51 | 0.28 |
| 80 kg | 0.66 | 0.51 | 0.24 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.83 | 0.42 | 27.39 | 11.58 | 0.40 | 0.01 | 8.35 | 0.00 | 0.33 |
| 40 kg | 0.56 | 0.45 | 26.24 | 9.12 | 0.77 | 0.84 | 5.56 | 0.00 | 0.29 |
| 60 kg | 0.28 | 0.44 | 27.49 | 10.17 | 0.34 | 1.49 | 1.92 | 0.00 | 0.30 |
| 80 kg | 0.68 | 0.44 | 28.53 | 8.47 | 0.19 | 2.85 | 0.69 | 0.00 | 0.31 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 105 | 258 | 197 |
| 40 kg | 139 | 309 | 254 |
| 60 kg | 170 | 346 | 301 |
| 80 kg | 192 | 367 | 343 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 1515 | 0.37 | 0.44 (267) | 0.51 (218) | 0.51 (407) | 0.50 (257) | 0.54 (366) |
| 40 kg | 1737 | 0.31 | 0.29 (350) | 0.48 (136) | 0.49 (430) | 0.53 (303) | 0.73 (519) |
| 60 kg | 2050 | 0.31 | 0.30 (393) | 0.45 (334) | 0.48 (379) | 0.54 (357) | 0.72 (588) |
| 80 kg | 2655 | 0.33 | 0.26 (95) | 0.41 (404) | 0.51 (1500) | 0.55 (438) | 0.71 (218) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.10 | 0.09 | 0.19 | 0.35 |
| long | 0.10 | 0.14 | 0.26 | 0.49 |
| sphere | 0.30 | 0.41 | 0.51 | 0.58 |
| cylinder | 0.20 | 0.17 | 0.23 | 0.41 |
| arch | 0.18 | 0.21 | 0.21 | 0.29 |
| dumbbell | 0.14 | 0.12 | 0.26 | 0.47 |
| t_shape | 0.11 | 0.09 | 0.19 | 0.31 |
| beam | 0.07 | 0.17 | 0.37 | 0.60 |
| l_shape | 0.06 | 0.11 | 0.15 | 0.37 |
| asym | 0.09 | 0.06 | 0.32 | 0.46 |
| u_channel | 0.10 | 0.20 | 0.21 | 0.36 |
| plus | 0.06 | 0.05 | 0.13 | 0.11 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.89 | 0.69 | 0.75 | 0.61 |
| B_left | 0.75 | 0.67 | 0.58 | 0.33 |
| C_backright | 0.75 | 0.67 | 0.44 | 0.31 |
| D_far_turn | 0.64 | 0.64 | 0.36 | 0.08 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 41% | 0% | 59% | 38% | 4% | 58% |  |  | 19% | 69% | 40% | 23% |
| 40 kg | 35% | 0% | 65% | 44% | 3% | 53% |  |  | 19% | 71% | 37% | 23% |
| 60 kg | 34% | 0% | 66% | 52% | 2% | 45% |  |  | 21% | 82% | 23% | 26% |
| 80 kg | 33% | 0% | 67% | 57% | 2% | 41% |  |  | 23% | 82% | 21% | 29% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 142 | 0.89 | 8% | 14% | 33% | 54% |
| 40 kg | 173 | 0.90 | 7% | 17% | 41% | 42% |
| 60 kg | 197 | 0.89 | 8% | 23% | 44% | 33% |
| 80 kg | 215 | 0.89 | 7% | 28% | 45% | 27% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 62% | 0.20 | 0.42 | 0.14 | 0.63 | 5 | 0 | 4 | 0 | 0 | 1 | 63 | 0.00 |  |
| 40 kg | 59% | 0.15 | 0.57 | 0.12 | 0.59 | 4 | 0 | 3 | 0 | 0 | 1 | 92 | 0.00 |  |
| 60 kg | 57% | 0.11 | 0.69 | 0.10 | 0.56 | 3 | 0 | 2 | 0 | 0 | 1 | 102 | 0.00 |  |
| 80 kg | 52% | 0.08 | 0.76 | 0.07 | 0.59 | 4 | 0 | 2 | 0 | 0 | 2 | 103 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.73 | 54% | 21% | 0.92 | 67% | 0.15 | 2 | 0 | 1 | 0 | 0 | 1 |
| long | 0.65 | 54% | 24% | 0.91 | 57% | 0.09 | 2 | 0 | 1 | 0 | 0 | 0 |
| sphere | 1.00 | 31% | 10% | 0.92 | 85% | 0.29 | 0 | 0 | 0 | 0 | 0 | 0 |
| cylinder | 0.46 | 34% | 13% | 0.91 | 66% | 0.11 | 2 | 0 | 2 | 0 | 0 | 0 |
| arch | 0.73 | 58% | 29% | 0.83 | 62% | 0.12 | 3 | 0 | 2 | 0 | 0 | 1 |
| dumbbell | 0.62 | 47% | 20% | 0.91 | 52% | 0.10 | 10 | 0 | 7 | 0 | 0 | 2 |
| t_shape | 0.46 | 51% | 21% | 0.90 | 50% | 0.08 | 6 | 0 | 3 | 0 | 0 | 2 |
| beam | 0.31 | 34% | 15% | 0.80 | 32% | 0.08 | 11 | 0 | 8 | 0 | 0 | 2 |
| l_shape | 0.62 | 54% | 22% | 0.91 | 57% | 0.08 | 2 | 0 | 1 | 0 | 0 | 2 |
| asym | 0.17 | 55% | 27% | 0.92 | 49% | 0.05 | 3 | 0 | 2 | 0 | 0 | 1 |
| u_channel | 0.65 | 50% | 19% | 0.93 | 53% | 0.10 | 5 | 0 | 2 | 0 | 0 | 3 |
| plus | 0.48 | 52% | 21% | 0.84 | 57% | 0.07 | 4 | 0 | 3 | 0 | 0 | 1 |
