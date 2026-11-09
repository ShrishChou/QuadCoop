# Pair evaluation: fair-td-nocreep-behind-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.54 | 0.58 | 0.15 | 0.21 | 24.8 | 0.01 | 0.45 | 0.37 | 0.16 | 0.29 | 1.10 |
| 40 kg | 0.58 | 0.50 | 0.18 | 0.17 | 28.3 | 0.01 | 0.55 | 0.36 | 0.18 | 0.28 | 1.11 |
| 60 kg | 0.31 | 0.28 | 0.35 | 0.23 | 29.9 | 0.01 | 0.65 | 0.38 | 0.25 | 0.35 | 1.07 |
| 80 kg | 0.26 | 0.20 | 0.33 | 0.33 | 39.7 | 0.01 | 0.68 | 0.50 | 0.36 | 0.47 | 1.05 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x+y + part 0 corner -x-y | 0.67 | 0.50 | 0.42 | 0.25 |
| long | part 0 -x seg 2/2 + part 0 corner -x-y | 0.58 | 0.67 | 0.25 | 0.17 |
| sphere | sector 135 + sector 225 | 0.92 | 0.50 | 0.50 | 0.50 |
| cylinder | part 0 corner -x-y + part 0 -x seg 2/2 | 0.33 | 0.25 | 0.17 | 0.00 |
| arch | part 3 -x + part 2 -x | 0.75 | 0.92 | 0.50 | 0.42 |
| dumbbell | part 0 -x + part 1 -x | 0.50 | 0.83 | 0.17 | 0.17 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.33 | 0.75 | 0.33 | 0.42 |
| beam (unseen) | part 0 -x seg 2/5 + part 0 -x seg 4/5 | 0.50 | 0.42 | 0.17 | 0.00 |
| l_shape (unseen) | part 1 -x + part 0 corner -x-y | 0.50 | 0.67 | 0.25 | 0.00 |
| asym (unseen) | part 1 -x + part 0 corner -x+y | 0.25 | 0.00 | 0.00 | 0.00 |
| u_channel (unseen) | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.67 | 0.67 | 0.50 | 0.50 |
| plus (unseen) | part 0 corner -x-y + part 0 corner -x+y | 0.50 | 0.75 | 0.42 | 0.67 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.54 | 0.10 | 0.35 | 0.01 | 0.00 | 0.03 | 9.28 |
| 40 kg | 0.58 | 0.07 | 0.35 | 0.01 | 0.00 | 0.00 | 7.78 |
| 60 kg | 0.31 | 0.10 | 0.58 | 0.01 | 0.00 | 0.00 | 8.07 |
| 80 kg | 0.26 | 0.08 | 0.67 | 0.00 | 0.00 | 0.00 | 6.18 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.33 | 0.60 | 0.82 | 0.00 | 1.00 | 0.34 | 0.63 | 0.80 | 0.00 |
| 40 kg | 1.00 | 0.29 | 0.66 | 0.88 | 0.00 | 1.00 | 0.31 | 0.65 | 0.85 | 0.00 |
| 60 kg | 1.00 | 0.30 | 0.65 | 0.90 | 0.00 | 1.00 | 0.32 | 0.60 | 0.85 | 0.00 |
| 80 kg | 1.00 | 0.30 | 0.64 | 0.91 | 0.00 | 1.00 | 0.33 | 0.59 | 0.85 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.76 | 1.99 | 0.08 | 0.75 | 1.79 | 0.07 |
| 40 kg | 0.79 | 1.98 | 0.11 | 0.75 | 1.81 | 0.10 |
| 60 kg | 0.77 | 1.81 | 0.12 | 0.75 | 2.01 | 0.14 |
| 80 kg | 0.77 | 2.07 | 0.12 | 0.75 | 2.53 | 0.16 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.46 | 0.48 | 0.29 |
| 40 kg | 0.54 | 0.48 | 0.26 |
| 60 kg | 0.56 | 0.42 | 0.24 |
| 80 kg | 0.56 | 0.45 | 0.22 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.41 | 0.40 | 25.70 | 9.28 | 0.06 | 0.08 | 3.35 | 0.00 | 0.33 |
| 40 kg | 0.31 | 0.41 | 22.93 | 7.78 | 0.23 | 0.38 | 3.75 | 0.00 | 0.30 |
| 60 kg | 0.27 | 0.39 | 21.00 | 8.07 | 0.08 | 0.78 | 1.26 | 0.00 | 0.35 |
| 80 kg | 0.43 | 0.41 | 18.23 | 6.18 | 0.18 | 0.90 | 0.41 | 0.00 | 0.35 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 123 | 295 | 210 |
| 40 kg | 160 | 348 | 270 |
| 60 kg | 188 | 377 | 306 |
| 80 kg | 207 | 382 | 333 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 1033 | 0.31 | 0.39 (161) | 0.49 (169) | 0.50 (273) | 0.50 (192) | 0.56 (238) |
| 40 kg | 1095 | 0.32 | 0.32 (242) | 0.45 (93) | 0.51 (153) | 0.55 (107) | 0.64 (500) |
| 60 kg | 1141 | 0.33 | 0.41 (127) | 0.46 (154) | 0.51 (200) | 0.57 (237) | 0.66 (423) |
| 80 kg | 1547 | 0.29 | 0.35 (60) | 0.43 (161) | 0.48 (927) | 0.52 (238) | 0.64 (160) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.13 | 0.09 | 0.19 | 0.48 |
| long | 0.16 | 0.15 | 0.30 | 0.38 |
| sphere | 0.37 | 0.46 | 0.40 | 0.37 |
| cylinder | 0.14 | 0.26 | 0.21 | 0.38 |
| arch | 0.20 | 0.19 | 0.19 | 0.31 |
| dumbbell | 0.22 | 0.16 | 0.30 | 0.39 |
| t_shape | 0.07 | 0.09 | 0.22 | 0.29 |
| beam | 0.11 | 0.20 | 0.41 | 0.35 |
| l_shape | 0.10 | 0.10 | 0.15 | 0.39 |
| asym | 0.22 | 0.24 | 0.34 | 0.52 |
| u_channel | 0.07 | 0.13 | 0.20 | 0.34 |
| plus | 0.12 | 0.10 | 0.12 | 0.17 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.64 | 0.67 | 0.56 | 0.42 |
| B_left | 0.56 | 0.47 | 0.11 | 0.19 |
| C_backright | 0.42 | 0.47 | 0.25 | 0.17 |
| D_far_turn | 0.56 | 0.69 | 0.31 | 0.25 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 46% | 0% | 54% | 42% | 3% | 55% |  |  | 20% | 63% | 45% | 25% |
| 40 kg | 42% | 0% | 58% | 52% | 2% | 46% |  |  | 21% | 63% | 42% | 26% |
| 60 kg | 43% | 0% | 57% | 59% | 2% | 40% |  |  | 24% | 74% | 33% | 28% |
| 80 kg | 43% | 0% | 57% | 64% | 1% | 34% |  |  | 24% | 81% | 24% | 28% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 163 | 0.90 | 7% | 14% | 32% | 54% |
| 40 kg | 194 | 0.91 | 6% | 20% | 39% | 40% |
| 60 kg | 218 | 0.90 | 7% | 26% | 41% | 33% |
| 80 kg | 234 | 0.90 | 7% | 32% | 40% | 28% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 61% | 0.23 | 0.49 | 0.18 | 0.48 | 2 | 0 | 1 | 0 | 0 | 1 | 52 | 0.00 |  |
| 40 kg | 59% | 0.19 | 0.60 | 0.16 | 0.40 | 2 | 0 | 2 | 0 | 0 | 1 | 125 | 0.00 |  |
| 60 kg | 55% | 0.14 | 0.67 | 0.12 | 0.38 | 2 | 0 | 1 | 0 | 0 | 1 | 179 | 0.00 |  |
| 80 kg | 49% | 0.10 | 0.75 | 0.09 | 0.31 | 1 | 0 | 0 | 0 | 0 | 1 | 205 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.46 | 66% | 36% | 0.92 | 62% | 0.14 | 0 | 0 | 0 | 0 | 0 | 0 |
| long | 0.42 | 60% | 24% | 0.91 | 60% | 0.13 | 1 | 0 | 1 | 0 | 0 | 0 |
| sphere | 0.60 | 37% | 12% | 0.91 | 78% | 0.31 | 1 | 0 | 0 | 0 | 0 | 1 |
| cylinder | 0.19 | 35% | 15% | 0.89 | 60% | 0.11 | 3 | 0 | 2 | 0 | 0 | 1 |
| arch | 0.65 | 63% | 30% | 0.87 | 60% | 0.17 | 2 | 0 | 0 | 0 | 0 | 1 |
| dumbbell | 0.42 | 54% | 23% | 0.91 | 54% | 0.14 | 3 | 0 | 1 | 0 | 0 | 1 |
| t_shape | 0.46 | 62% | 27% | 0.91 | 56% | 0.11 | 1 | 0 | 0 | 0 | 0 | 1 |
| beam | 0.27 | 34% | 16% | 0.81 | 30% | 0.08 | 6 | 0 | 5 | 0 | 0 | 1 |
| l_shape | 0.35 | 59% | 23% | 0.92 | 55% | 0.12 | 1 | 0 | 0 | 0 | 0 | 0 |
| asym | 0.06 | 65% | 32% | 0.92 | 51% | 0.08 | 1 | 0 | 0 | 0 | 0 | 0 |
| u_channel | 0.58 | 56% | 19% | 0.93 | 47% | 0.11 | 3 | 0 | 1 | 0 | 0 | 2 |
| plus | 0.58 | 57% | 20% | 0.91 | 59% | 0.13 | 2 | 0 | 2 | 0 | 0 | 0 |
