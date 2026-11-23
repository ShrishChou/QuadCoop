# Pair evaluation: olp-B2-r1-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto); planner settings changed: fail_mem=1,fail_act=2

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.77 | 0.73 | 0.02 | 0.01 | 29.7 | 0.01 | 0.39 | 0.35 | 0.12 | 0.24 | 1.05 |
| 40 kg | 0.81 | 0.65 | 0.00 | 0.00 | 33.0 | 0.01 | 0.46 | 0.38 | 0.15 | 0.24 | 1.08 |
| 60 kg | 0.60 | 0.46 | 0.01 | 0.03 | 34.7 | 0.01 | 0.59 | 0.42 | 0.23 | 0.31 | 1.02 |
| 80 kg | 0.38 | 0.29 | 0.07 | 0.04 | 40.1 | 0.01 | 0.69 | 0.52 | 0.34 | 0.42 | 1.02 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 -x end - + part 0 corner -x+y | 1.00 | 1.00 | 0.92 | 0.50 |
| long | part 0 -x seg 2/2 + part 0 corner -x-y | 0.83 | 0.75 | 0.58 | 0.08 |
| sphere | sector 225 + sector 135 | 1.00 | 0.92 | 0.92 | 0.67 |
| cylinder | part 0 corner -x-y + part 0 -x seg 2/2 | 0.42 | 0.50 | 0.33 | 0.17 |
| arch | part 2 -x + part 3 -x | 0.67 | 0.83 | 0.67 | 0.58 |
| dumbbell | part 0 -x + part 1 -x | 0.92 | 0.92 | 0.33 | 0.33 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.67 | 0.67 | 0.83 | 0.42 |
| l_shape (unseen) | part 0 corner -x-y + part 1 -x | 0.83 | 0.92 | 0.67 | 0.33 |
| u_channel (unseen) | part 0 -x seg 1/3 + part 0 -x seg 3/3 | 0.83 | 0.92 | 0.50 | 0.42 |
| plus (unseen) | part 0 -x end - + part 0 -x end + | 0.50 | 0.67 | 0.25 | 0.25 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.77 | 0.21 | 0.03 | 0.00 | 0.00 | 0.01 | 11.94 |
| 40 kg | 0.81 | 0.19 | 0.00 | 0.00 | 0.00 | 0.00 | 11.65 |
| 60 kg | 0.60 | 0.36 | 0.04 | 0.00 | 0.00 | 0.00 | 11.20 |
| 80 kg | 0.38 | 0.51 | 0.12 | 0.00 | 0.00 | 0.00 | 8.98 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.30 | 0.67 | 0.87 | 0.00 | 1.00 | 0.30 | 0.64 | 0.84 | 0.00 |
| 40 kg | 1.00 | 0.27 | 0.69 | 0.89 | 0.00 | 1.00 | 0.26 | 0.69 | 0.88 | 0.00 |
| 60 kg | 1.00 | 0.27 | 0.71 | 0.92 | 0.00 | 1.00 | 0.25 | 0.70 | 0.89 | 0.00 |
| 80 kg | 1.00 | 0.24 | 0.72 | 0.94 | 0.00 | 1.00 | 0.24 | 0.68 | 0.94 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.78 | 2.06 | 0.07 | 0.76 | 2.07 | 0.08 |
| 40 kg | 0.78 | 1.90 | 0.08 | 0.78 | 2.06 | 0.09 |
| 60 kg | 0.74 | 1.79 | 0.10 | 0.75 | 2.02 | 0.11 |
| 80 kg | 0.77 | 2.10 | 0.09 | 0.78 | 2.41 | 0.15 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.50 | 0.48 | 0.30 |
| 40 kg | 0.54 | 0.51 | 0.30 |
| 60 kg | 0.58 | 0.52 | 0.29 |
| 80 kg | 0.64 | 0.55 | 0.26 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 2.28 | 0.38 | 27.80 | 11.94 | 0.23 | 0.12 | 6.49 | 0.00 | 0.35 |
| 40 kg | 0.63 | 0.40 | 25.87 | 11.65 | 0.17 | 0.35 | 4.53 | 0.00 | 0.30 |
| 60 kg | 1.05 | 0.41 | 27.13 | 11.20 | 0.39 | 1.45 | 1.71 | 0.00 | 0.33 |
| 80 kg | 1.18 | 0.45 | 27.57 | 8.98 | 0.22 | 2.73 | 0.93 | 0.00 | 0.31 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 108 | 260 | 212 |
| 40 kg | 138 | 309 | 251 |
| 60 kg | 168 | 348 | 300 |
| 80 kg | 192 | 375 | 338 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 1024 | 0.33 | 0.43 (193) | 0.52 (160) | 0.50 (333) | 0.51 (172) | 0.60 (165) |
| 40 kg | 1033 | 0.33 | 0.30 (249) | 0.46 (97) | 0.54 (182) | 0.56 (168) | 0.67 (337) |
| 60 kg | 1426 | 0.30 | 0.33 (259) | 0.36 (202) | 0.52 (240) | 0.60 (231) | 0.76 (494) |
| 80 kg | 2265 | 0.33 | 0.40 (156) | 0.46 (260) | 0.50 (1141) | 0.59 (467) | 0.66 (241) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.13 | 0.14 | 0.23 | 0.37 |
| long | 0.10 | 0.08 | 0.16 | 0.39 |
| sphere | 0.21 | 0.34 | 0.53 | 0.43 |
| cylinder | 0.15 | 0.15 | 0.25 | 0.29 |
| arch | 0.12 | 0.12 | 0.20 | 0.32 |
| dumbbell | 0.17 | 0.22 | 0.25 | 0.39 |
| t_shape | 0.07 | 0.10 | 0.23 | 0.43 |
| l_shape | 0.04 | 0.09 | 0.13 | 0.24 |
| u_channel | 0.10 | 0.17 | 0.20 | 0.46 |
| plus | 0.09 | 0.05 | 0.09 | 0.10 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.80 | 0.90 | 0.87 | 0.60 |
| B_left | 0.80 | 0.83 | 0.60 | 0.40 |
| C_backright | 0.63 | 0.77 | 0.53 | 0.30 |
| D_far_turn | 0.83 | 0.73 | 0.40 | 0.20 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 42% | 0% | 58% | 38% | 4% | 58% |  |  | 18% | 64% | 44% | 23% |
| 40 kg | 37% | 0% | 63% | 45% | 3% | 53% |  |  | 18% | 67% | 38% | 23% |
| 60 kg | 36% | 0% | 64% | 51% | 2% | 48% |  |  | 20% | 71% | 33% | 25% |
| 80 kg | 33% | 0% | 67% | 58% | 2% | 41% |  |  | 21% | 82% | 20% | 26% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 145 | 0.88 | 8% | 14% | 31% | 55% |
| 40 kg | 171 | 0.90 | 7% | 15% | 40% | 44% |
| 60 kg | 198 | 0.90 | 6% | 20% | 44% | 36% |
| 80 kg | 218 | 0.90 | 6% | 28% | 45% | 27% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 64% | 0.20 | 0.41 | 0.15 | 0.62 | 6 | 0 | 4 | 0 | 0 | 2 | 77 | 0.00 |  |
| 40 kg | 62% | 0.16 | 0.57 | 0.13 | 0.61 | 6 | 0 | 4 | 0 | 0 | 2 | 84 | 0.00 |  |
| 60 kg | 59% | 0.13 | 0.67 | 0.11 | 0.56 | 5 | 0 | 2 | 0 | 0 | 3 | 123 | 0.00 |  |
| 80 kg | 56% | 0.09 | 0.75 | 0.08 | 0.38 | 2 | 0 | 1 | 0 | 0 | 1 | 111 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.85 | 55% | 23% | 0.92 | 70% | 0.16 | 0 | 0 | 0 | 0 | 0 | 0 |
| long | 0.56 | 50% | 19% | 0.91 | 54% | 0.08 | 3 | 0 | 2 | 0 | 0 | 1 |
| sphere | 0.88 | 30% | 10% | 0.92 | 83% | 0.28 | 2 | 0 | 2 | 0 | 0 | 0 |
| cylinder | 0.35 | 31% | 12% | 0.91 | 61% | 0.09 | 4 | 0 | 3 | 0 | 0 | 1 |
| arch | 0.69 | 53% | 25% | 0.83 | 56% | 0.12 | 11 | 0 | 6 | 0 | 0 | 5 |
| dumbbell | 0.62 | 49% | 22% | 0.91 | 56% | 0.11 | 7 | 0 | 5 | 0 | 0 | 2 |
| t_shape | 0.65 | 53% | 20% | 0.92 | 53% | 0.08 | 8 | 0 | 2 | 0 | 0 | 6 |
| l_shape | 0.69 | 54% | 21% | 0.92 | 60% | 0.09 | 1 | 0 | 1 | 0 | 0 | 0 |
| u_channel | 0.67 | 51% | 18% | 0.93 | 54% | 0.10 | 5 | 0 | 2 | 0 | 0 | 3 |
| plus | 0.42 | 53% | 21% | 0.80 | 54% | 0.07 | 5 | 0 | 2 | 0 | 0 | 2 |
