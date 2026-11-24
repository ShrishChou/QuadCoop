# Pair evaluation: olp140-B2-r1-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto); planner settings changed: fail_mem=1,fail_act=2

success = 10 cm / 6 deg held 1 s within 140 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.87 | 0.77 | 0.02 | 0.03 | 30.8 | 0.01 | 0.41 | 0.36 | 0.13 | 0.24 | 1.03 |
| 40 kg | 0.88 | 0.72 | 0.00 | 0.01 | 37.0 | 0.00 | 0.46 | 0.41 | 0.15 | 0.25 | 1.08 |
| 60 kg | 0.67 | 0.49 | 0.07 | 0.04 | 50.9 | 0.01 | 0.55 | 0.40 | 0.21 | 0.31 | 1.03 |
| 80 kg | 0.56 | 0.39 | 0.11 | 0.03 | 62.2 | 0.01 | 0.65 | 0.49 | 0.30 | 0.38 | 1.00 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 -x end - + part 0 corner -x+y | 1.00 | 0.92 | 0.75 | 0.58 |
| long | part 0 -x seg 2/2 + part 0 corner -x-y | 1.00 | 0.92 | 0.75 | 0.17 |
| sphere | sector 225 + sector 135 | 1.00 | 1.00 | 0.83 | 0.75 |
| cylinder | part 0 corner -x-y + part 0 -x seg 2/2 | 0.50 | 0.67 | 0.42 | 0.25 |
| arch | part 2 -x + part 3 -x | 0.83 | 0.92 | 0.58 | 0.92 |
| dumbbell | part 0 -x + part 1 -x | 0.75 | 0.75 | 0.42 | 0.58 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 1.00 | 0.83 | 0.92 | 0.75 |
| l_shape (unseen) | part 0 corner -x-y + part 1 -x | 0.92 | 1.00 | 0.75 | 0.42 |
| u_channel (unseen) | part 0 -x seg 1/3 + part 0 -x seg 3/3 | 1.00 | 0.92 | 0.75 | 0.58 |
| plus (unseen) | part 0 -x end - + part 0 -x end + | 0.67 | 0.83 | 0.50 | 0.58 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.87 | 0.09 | 0.04 | 0.00 | 0.00 | 0.01 | 14.85 |
| 40 kg | 0.88 | 0.12 | 0.01 | 0.00 | 0.00 | 0.02 | 14.78 |
| 60 kg | 0.67 | 0.22 | 0.12 | 0.00 | 0.00 | 0.00 | 17.80 |
| 80 kg | 0.56 | 0.30 | 0.14 | 0.00 | 0.00 | 0.00 | 16.18 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.28 | 0.66 | 0.85 | 0.00 | 1.00 | 0.30 | 0.65 | 0.84 | 0.00 |
| 40 kg | 1.00 | 0.24 | 0.74 | 0.91 | 0.00 | 1.00 | 0.25 | 0.69 | 0.89 | 0.00 |
| 60 kg | 1.00 | 0.28 | 0.69 | 0.90 | 0.00 | 1.00 | 0.26 | 0.70 | 0.90 | 0.00 |
| 80 kg | 1.00 | 0.26 | 0.71 | 0.95 | 0.00 | 1.00 | 0.25 | 0.67 | 0.93 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.76 | 1.91 | 0.07 | 0.77 | 2.03 | 0.07 |
| 40 kg | 0.79 | 1.91 | 0.08 | 0.77 | 1.97 | 0.10 |
| 60 kg | 0.76 | 1.84 | 0.09 | 0.77 | 2.20 | 0.11 |
| 80 kg | 0.78 | 2.08 | 0.09 | 0.80 | 2.60 | 0.13 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.49 | 0.48 | 0.30 |
| 40 kg | 0.58 | 0.54 | 0.29 |
| 60 kg | 0.56 | 0.54 | 0.28 |
| 80 kg | 0.60 | 0.53 | 0.26 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.68 | 0.40 | 27.12 | 14.85 | 0.47 | 0.28 | 14.86 | 0.00 | 0.32 |
| 40 kg | 0.59 | 0.45 | 28.00 | 14.78 | 1.42 | 0.67 | 12.50 | 0.00 | 0.28 |
| 60 kg | 4.14 | 0.42 | 32.10 | 17.80 | 0.36 | 1.83 | 4.11 | 0.00 | 0.35 |
| 80 kg | 3.22 | 0.42 | 36.23 | 16.18 | 0.39 | 4.05 | 2.26 | 0.00 | 0.33 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 104 | 255 | 200 |
| 40 kg | 141 | 311 | 251 |
| 60 kg | 167 | 346 | 309 |
| 80 kg | 194 | 374 | 346 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 975 | 0.35 | 0.44 (188) | 0.52 (107) | 0.50 (314) | 0.50 (209) | 0.58 (158) |
| 40 kg | 1509 | 0.34 | 0.39 (387) | 0.51 (252) | 0.52 (332) | 0.53 (151) | 0.71 (387) |
| 60 kg | 1851 | 0.33 | 0.33 (347) | 0.35 (285) | 0.50 (252) | 0.58 (281) | 0.66 (687) |
| 80 kg | 2619 | 0.34 | 0.39 (155) | 0.47 (247) | 0.53 (1354) | 0.61 (589) | 0.69 (275) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.16 | 0.10 | 0.17 | 0.26 |
| long | 0.14 | 0.10 | 0.19 | 0.32 |
| sphere | 0.24 | 0.39 | 0.48 | 0.43 |
| cylinder | 0.12 | 0.11 | 0.28 | 0.30 |
| arch | 0.12 | 0.14 | 0.17 | 0.26 |
| dumbbell | 0.15 | 0.22 | 0.23 | 0.36 |
| t_shape | 0.10 | 0.13 | 0.19 | 0.36 |
| l_shape | 0.04 | 0.13 | 0.13 | 0.25 |
| u_channel | 0.16 | 0.15 | 0.23 | 0.34 |
| plus | 0.06 | 0.07 | 0.07 | 0.13 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.90 | 0.90 | 0.87 | 0.73 |
| B_left | 0.93 | 0.83 | 0.80 | 0.57 |
| C_backright | 0.77 | 0.90 | 0.47 | 0.53 |
| D_far_turn | 0.87 | 0.87 | 0.53 | 0.40 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 42% | 0% | 58% | 39% | 4% | 57% |  |  | 19% | 68% | 40% | 24% |
| 40 kg | 34% | 0% | 66% | 45% | 3% | 52% |  |  | 17% | 71% | 35% | 23% |
| 60 kg | 35% | 0% | 65% | 48% | 2% | 50% |  |  | 19% | 73% | 30% | 24% |
| 80 kg | 35% | 0% | 65% | 56% | 2% | 43% |  |  | 21% | 82% | 24% | 26% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 140 | 0.88 | 9% | 12% | 32% | 56% |
| 40 kg | 173 | 0.90 | 7% | 17% | 41% | 42% |
| 60 kg | 197 | 0.90 | 6% | 20% | 42% | 38% |
| 80 kg | 218 | 0.90 | 6% | 24% | 45% | 31% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 65% | 0.22 | 0.43 | 0.16 | 0.73 | 7 | 0 | 5 | 0 | 0 | 3 | 64 | 0.00 |  |
| 40 kg | 63% | 0.17 | 0.56 | 0.13 | 0.77 | 7 | 0 | 5 | 0 | 0 | 2 | 92 | 0.00 |  |
| 60 kg | 55% | 0.12 | 0.66 | 0.10 | 0.81 | 13 | 0 | 9 | 0 | 0 | 3 | 109 | 0.00 |  |
| 80 kg | 50% | 0.08 | 0.74 | 0.07 | 0.95 | 5 | 0 | 3 | 0 | 0 | 2 | 104 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.81 | 52% | 22% | 0.92 | 64% | 0.14 | 6 | 0 | 5 | 0 | 0 | 1 |
| long | 0.71 | 51% | 17% | 0.91 | 55% | 0.10 | 3 | 0 | 1 | 0 | 0 | 2 |
| sphere | 0.90 | 31% | 10% | 0.92 | 84% | 0.29 | 0 | 0 | 0 | 0 | 0 | 0 |
| cylinder | 0.46 | 33% | 14% | 0.91 | 60% | 0.08 | 10 | 0 | 9 | 0 | 0 | 1 |
| arch | 0.81 | 55% | 24% | 0.83 | 56% | 0.12 | 15 | 0 | 6 | 0 | 0 | 9 |
| dumbbell | 0.62 | 41% | 17% | 0.91 | 46% | 0.09 | 21 | 0 | 18 | 0 | 0 | 3 |
| t_shape | 0.88 | 51% | 20% | 0.91 | 53% | 0.09 | 6 | 0 | 4 | 0 | 0 | 2 |
| l_shape | 0.77 | 54% | 21% | 0.91 | 59% | 0.09 | 5 | 0 | 4 | 0 | 0 | 1 |
| u_channel | 0.81 | 53% | 19% | 0.93 | 55% | 0.10 | 4 | 0 | 1 | 0 | 0 | 3 |
| plus | 0.65 | 49% | 20% | 0.80 | 51% | 0.07 | 11 | 0 | 7 | 0 | 0 | 3 |
