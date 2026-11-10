# Pair evaluation: td-plv2-behind-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.76 | 0.74 | 0.01 | 0.01 | 27.7 | 0.00 | 0.43 | 0.34 | 0.08 | 0.14 | 1.07 |
| 40 kg | 0.56 | 0.47 | 0.04 | 0.03 | 32.0 | 0.00 | 0.49 | 0.36 | 0.10 | 0.15 | 1.05 |
| 60 kg | 0.33 | 0.28 | 0.10 | 0.06 | 40.7 | 0.01 | 0.56 | 0.37 | 0.16 | 0.23 | 1.04 |
| 80 kg | 0.22 | 0.15 | 0.10 | 0.03 | 40.5 | 0.01 | 0.60 | 0.42 | 0.24 | 0.33 | 1.01 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x+y + part 0 corner -x-y | 0.75 | 1.00 | 0.42 | 0.25 |
| long | part 0 corner -x+y + part 0 -x seg 1/2 | 0.92 | 0.17 | 0.58 | 0.17 |
| sphere | sector 0 + sector 180 | 1.00 | 0.83 | 1.00 | 0.83 |
| cylinder | part 0 corner -x+y + part 0 -x seg 1/2 | 0.50 | 0.25 | 0.08 | 0.08 |
| arch | part 2 -x + part 3 -x | 0.83 | 0.58 | 0.58 | 0.42 |
| dumbbell | part 0 -x + part 1 -x | 0.67 | 0.50 | 0.00 | 0.00 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.75 | 0.67 | 0.17 | 0.25 |
| beam (unseen) | part 0 -x seg 4/5 + part 0 -x seg 2/5 | 0.75 | 0.17 | 0.08 | 0.00 |
| l_shape (unseen) | part 1 -x + part 0 corner -x-y | 0.83 | 0.75 | 0.50 | 0.25 |
| asym (unseen) | part 0 -x end + + part 1 -x end - | 0.67 | 0.17 | 0.00 | 0.00 |
| u_channel (unseen) | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.92 | 1.00 | 0.33 | 0.17 |
| plus (unseen) | part 0 -x end + + part 0 -x end - | 0.50 | 0.67 | 0.25 | 0.17 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.76 | 0.22 | 0.02 | 0.00 | 0.00 | 0.03 | 9.02 |
| 40 kg | 0.56 | 0.36 | 0.08 | 0.00 | 0.00 | 0.00 | 7.40 |
| 60 kg | 0.33 | 0.50 | 0.17 | 0.00 | 0.00 | 0.00 | 7.55 |
| 80 kg | 0.22 | 0.65 | 0.13 | 0.00 | 0.00 | 0.00 | 5.35 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.32 | 0.62 | 0.84 | 0.00 | 1.00 | 0.36 | 0.62 | 0.85 | 0.00 |
| 40 kg | 1.00 | 0.27 | 0.68 | 0.90 | 0.00 | 1.00 | 0.34 | 0.64 | 0.90 | 0.00 |
| 60 kg | 1.00 | 0.26 | 0.70 | 0.92 | 0.00 | 1.00 | 0.31 | 0.64 | 0.89 | 0.00 |
| 80 kg | 1.00 | 0.29 | 0.68 | 0.94 | 0.00 | 1.00 | 0.34 | 0.58 | 0.91 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.67 | 2.62 | 0.09 | 0.66 | 2.44 | 0.08 |
| 40 kg | 0.66 | 3.56 | 0.10 | 0.64 | 3.15 | 0.10 |
| 60 kg | 0.68 | 2.10 | 0.10 | 0.70 | 3.37 | 0.12 |
| 80 kg | 0.70 | 2.62 | 0.12 | 0.75 | 4.05 | 0.15 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.51 | 0.47 | 0.32 |
| 40 kg | 0.57 | 0.45 | 0.31 |
| 60 kg | 0.60 | 0.47 | 0.34 |
| 80 kg | 0.58 | 0.44 | 0.39 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.88 | 0.38 | 25.85 | 9.02 | 0.68 | 0.15 | 8.13 | 0.00 | 0.35 |
| 40 kg | 2.06 | 0.37 | 27.37 | 7.40 | 0.67 | 1.45 | 4.73 | 0.00 | 0.30 |
| 60 kg | 1.43 | 0.39 | 29.80 | 7.55 | 1.19 | 2.54 | 2.92 | 2.84 | 0.35 |
| 80 kg | 2.56 | 0.35 | 31.11 | 5.35 | 0.13 | 3.84 | 1.85 | 3.49 | 0.40 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 115 | 266 | 207 |
| 40 kg | 148 | 317 | 259 |
| 60 kg | 178 | 348 | 305 |
| 80 kg | 192 | 365 | 337 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 1258 | 0.34 | 0.44 (171) | 0.48 (174) | 0.49 (326) | 0.51 (297) | 0.58 (290) |
| 40 kg | 1634 | 0.29 | 0.27 (300) | 0.45 (288) | 0.50 (338) | 0.59 (189) | 0.76 (519) |
| 60 kg | 2213 | 0.29 | 0.27 (399) | 0.36 (301) | 0.47 (542) | 0.60 (342) | 0.79 (629) |
| 80 kg | 2199 | 0.32 | 0.31 (129) | 0.40 (240) | 0.48 (1141) | 0.59 (209) | 0.74 (481) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.09 | 0.15 | 0.11 | 0.21 |
| long | 0.07 | 0.08 | 0.26 | 0.27 |
| sphere | 0.13 | 0.09 | 0.21 | 0.21 |
| cylinder | 0.07 | 0.02 | 0.07 | 0.13 |
| arch | 0.07 | 0.06 | 0.06 | 0.16 |
| dumbbell | 0.15 | 0.07 | 0.13 | 0.29 |
| t_shape | 0.10 | 0.13 | 0.11 | 0.22 |
| beam | 0.06 | 0.12 | 0.37 | 0.46 |
| l_shape | 0.04 | 0.21 | 0.17 | 0.27 |
| asym | 0.06 | 0.06 | 0.24 | 0.39 |
| u_channel | 0.10 | 0.11 | 0.18 | 0.21 |
| plus | 0.04 | 0.09 | 0.05 | 0.04 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.78 | 0.61 | 0.36 | 0.25 |
| B_left | 0.94 | 0.61 | 0.36 | 0.17 |
| C_backright | 0.67 | 0.56 | 0.42 | 0.33 |
| D_far_turn | 0.64 | 0.47 | 0.19 | 0.11 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 45% | 0% | 55% | 43% | 4% | 53% |  |  | 19% | 63% | 46% | 26% |
| 40 kg | 39% | 0% | 61% | 46% | 3% | 51% |  |  | 18% | 70% | 38% | 25% |
| 60 kg | 37% | 0% | 63% | 52% | 2% | 46% |  |  | 20% | 78% | 27% | 25% |
| 80 kg | 40% | 0% | 60% | 57% | 2% | 41% |  |  | 24% | 86% | 18% | 29% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 149 | 0.88 | 8% | 15% | 32% | 53% |
| 40 kg | 178 | 0.89 | 8% | 17% | 41% | 42% |
| 60 kg | 201 | 0.89 | 7% | 20% | 45% | 34% |
| 80 kg | 215 | 0.89 | 8% | 25% | 47% | 29% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 62% | 0.19 | 0.47 | 0.14 | 0.76 | 6 | 0 | 4 | 0 | 0 | 2 | 68 | 0.00 |  |
| 40 kg | 55% | 0.13 | 0.64 | 0.11 | 0.75 | 6 | 0 | 4 | 0 | 0 | 2 | 68 | 0.00 |  |
| 60 kg | 50% | 0.08 | 0.71 | 0.07 | 0.55 | 4 | 0 | 2 | 0 | 0 | 2 | 142 | 0.00 |  |
| 80 kg | 43% | 0.06 | 0.76 | 0.06 | 0.56 | 4 | 0 | 1 | 0 | 0 | 2 | 133 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.60 | 60% | 29% | 0.92 | 62% | 0.09 | 1 | 0 | 1 | 0 | 0 | 1 |
| long | 0.46 | 56% | 23% | 0.91 | 54% | 0.09 | 3 | 0 | 1 | 0 | 0 | 2 |
| sphere | 0.92 | 34% | 9% | 0.93 | 81% | 0.22 | 1 | 0 | 0 | 0 | 0 | 1 |
| cylinder | 0.23 | 39% | 15% | 0.88 | 64% | 0.13 | 4 | 0 | 2 | 0 | 0 | 2 |
| arch | 0.60 | 60% | 25% | 0.77 | 52% | 0.08 | 4 | 0 | 1 | 0 | 0 | 3 |
| dumbbell | 0.29 | 45% | 16% | 0.89 | 40% | 0.07 | 9 | 0 | 7 | 0 | 0 | 2 |
| t_shape | 0.46 | 53% | 20% | 0.91 | 49% | 0.07 | 6 | 0 | 3 | 0 | 0 | 3 |
| beam | 0.25 | 35% | 16% | 0.82 | 32% | 0.07 | 10 | 0 | 8 | 0 | 0 | 2 |
| l_shape | 0.58 | 57% | 22% | 0.91 | 53% | 0.09 | 4 | 0 | 2 | 0 | 0 | 2 |
| asym | 0.21 | 57% | 24% | 0.92 | 43% | 0.06 | 3 | 0 | 1 | 0 | 0 | 2 |
| u_channel | 0.60 | 49% | 15% | 0.92 | 49% | 0.08 | 6 | 0 | 3 | 0 | 0 | 2 |
| plus | 0.40 | 51% | 19% | 0.85 | 52% | 0.06 | 7 | 0 | 4 | 0 | 0 | 3 |
