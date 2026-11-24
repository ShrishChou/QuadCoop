# Pair evaluation: olp140-A-r1-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto); planner settings changed: fail_mem=0.5

success = 10 cm / 6 deg held 1 s within 140 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.82 | 0.76 | 0.01 | 0.02 | 28.2 | 0.01 | 0.41 | 0.36 | 0.12 | 0.23 | 1.03 |
| 40 kg | 0.78 | 0.64 | 0.01 | 0.00 | 37.8 | 0.00 | 0.46 | 0.36 | 0.13 | 0.21 | 1.09 |
| 60 kg | 0.69 | 0.51 | 0.04 | 0.04 | 51.5 | 0.01 | 0.57 | 0.39 | 0.20 | 0.29 | 1.02 |
| 80 kg | 0.58 | 0.42 | 0.06 | 0.04 | 57.2 | 0.01 | 0.64 | 0.51 | 0.32 | 0.42 | 1.02 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 -x end - + part 0 corner -x+y | 1.00 | 0.92 | 0.83 | 0.58 |
| long | part 0 -x seg 2/2 + part 0 corner -x-y | 0.83 | 0.83 | 0.75 | 0.42 |
| sphere | sector 225 + sector 135 | 1.00 | 1.00 | 0.75 | 0.83 |
| cylinder | part 0 corner -x-y + part 0 -x seg 2/2 | 0.42 | 0.42 | 0.50 | 0.33 |
| arch | part 2 -x + part 3 -x | 0.92 | 0.75 | 0.83 | 0.67 |
| dumbbell | part 0 -x + part 1 -x | 0.75 | 1.00 | 0.75 | 0.58 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.75 | 0.75 | 0.75 | 0.42 |
| l_shape (unseen) | part 0 corner -x-y + part 1 -x | 0.83 | 0.92 | 0.67 | 0.58 |
| u_channel (unseen) | part 0 -x seg 1/3 + part 0 -x seg 3/3 | 0.92 | 0.83 | 0.67 | 0.67 |
| plus (unseen) | part 0 -x end - + part 0 -x end + | 0.83 | 0.42 | 0.42 | 0.75 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.82 | 0.15 | 0.03 | 0.00 | 0.00 | 0.01 | 13.38 |
| 40 kg | 0.78 | 0.21 | 0.01 | 0.00 | 0.00 | 0.00 | 12.72 |
| 60 kg | 0.69 | 0.22 | 0.08 | 0.01 | 0.00 | 0.00 | 18.27 |
| 80 kg | 0.58 | 0.32 | 0.10 | 0.00 | 0.00 | 0.00 | 16.79 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.29 | 0.67 | 0.85 | 0.00 | 1.00 | 0.29 | 0.66 | 0.85 | 0.00 |
| 40 kg | 1.00 | 0.26 | 0.71 | 0.90 | 0.00 | 1.00 | 0.25 | 0.70 | 0.88 | 0.00 |
| 60 kg | 1.00 | 0.27 | 0.72 | 0.93 | 0.00 | 1.00 | 0.27 | 0.67 | 0.90 | 0.00 |
| 80 kg | 1.00 | 0.25 | 0.72 | 0.94 | 0.00 | 1.00 | 0.26 | 0.68 | 0.93 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.76 | 1.83 | 0.06 | 0.75 | 2.03 | 0.07 |
| 40 kg | 0.77 | 1.90 | 0.09 | 0.76 | 1.93 | 0.08 |
| 60 kg | 0.76 | 1.82 | 0.09 | 0.77 | 2.78 | 0.11 |
| 80 kg | 0.78 | 2.02 | 0.09 | 0.80 | 2.31 | 0.13 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.51 | 0.50 | 0.31 |
| 40 kg | 0.55 | 0.54 | 0.30 |
| 60 kg | 0.59 | 0.52 | 0.29 |
| 80 kg | 0.62 | 0.55 | 0.26 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.10 | 0.42 | 27.74 | 13.38 | 0.92 | 1.47 | 15.32 | 0.00 | 0.30 |
| 40 kg | 2.39 | 0.43 | 29.94 | 12.72 | 0.65 | 1.00 | 11.76 | 0.00 | 0.31 |
| 60 kg | 2.74 | 0.41 | 33.49 | 18.27 | 0.54 | 0.93 | 5.20 | 0.00 | 0.35 |
| 80 kg | 2.08 | 0.45 | 35.20 | 16.79 | 0.39 | 3.77 | 3.39 | 0.00 | 0.30 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 106 | 256 | 210 |
| 40 kg | 143 | 309 | 259 |
| 60 kg | 167 | 345 | 307 |
| 80 kg | 192 | 372 | 343 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 1394 | 0.31 | 0.48 (221) | 0.50 (185) | 0.50 (565) | 0.48 (275) | 0.63 (147) |
| 40 kg | 1903 | 0.33 | 0.40 (407) | 0.51 (259) | 0.50 (561) | 0.52 (229) | 0.67 (446) |
| 60 kg | 1772 | 0.31 | 0.28 (334) | 0.35 (277) | 0.48 (275) | 0.59 (329) | 0.74 (557) |
| 80 kg | 2681 | 0.34 | 0.35 (220) | 0.40 (361) | 0.52 (1396) | 0.58 (509) | 0.66 (195) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.11 | 0.13 | 0.29 | 0.28 |
| long | 0.10 | 0.08 | 0.08 | 0.32 |
| sphere | 0.26 | 0.37 | 0.49 | 0.46 |
| cylinder | 0.12 | 0.08 | 0.34 | 0.34 |
| arch | 0.13 | 0.10 | 0.17 | 0.28 |
| dumbbell | 0.13 | 0.21 | 0.18 | 0.42 |
| t_shape | 0.06 | 0.08 | 0.17 | 0.38 |
| l_shape | 0.06 | 0.10 | 0.07 | 0.19 |
| u_channel | 0.16 | 0.10 | 0.18 | 0.42 |
| plus | 0.08 | 0.03 | 0.07 | 0.11 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.83 | 0.73 | 0.87 | 0.80 |
| B_left | 0.80 | 0.70 | 0.67 | 0.53 |
| C_backright | 0.83 | 0.80 | 0.63 | 0.53 |
| D_far_turn | 0.83 | 0.90 | 0.60 | 0.47 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 40% | 0% | 60% | 38% | 4% | 59% |  |  | 17% | 63% | 45% | 23% |
| 40 kg | 37% | 0% | 63% | 46% | 2% | 51% |  |  | 19% | 65% | 41% | 22% |
| 60 kg | 35% | 0% | 65% | 49% | 2% | 49% |  |  | 19% | 72% | 32% | 25% |
| 80 kg | 33% | 0% | 67% | 56% | 2% | 43% |  |  | 20% | 80% | 24% | 26% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 143 | 0.88 | 8% | 13% | 31% | 56% |
| 40 kg | 173 | 0.89 | 7% | 18% | 40% | 43% |
| 60 kg | 196 | 0.90 | 6% | 19% | 44% | 37% |
| 80 kg | 217 | 0.90 | 6% | 25% | 45% | 30% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 64% | 0.21 | 0.42 | 0.15 | 0.95 | 9 | 0 | 6 | 0 | 0 | 3 | 94 | 0.00 |  |
| 40 kg | 60% | 0.15 | 0.51 | 0.12 | 0.93 | 12 | 0 | 6 | 0 | 0 | 5 | 84 | 0.00 |  |
| 60 kg | 56% | 0.12 | 0.66 | 0.10 | 0.78 | 8 | 0 | 4 | 0 | 0 | 3 | 127 | 0.00 |  |
| 80 kg | 52% | 0.08 | 0.73 | 0.07 | 0.75 | 4 | 0 | 3 | 0 | 0 | 1 | 127 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.83 | 55% | 22% | 0.92 | 68% | 0.15 | 1 | 0 | 1 | 0 | 0 | 0 |
| long | 0.71 | 51% | 18% | 0.91 | 52% | 0.08 | 4 | 0 | 2 | 0 | 0 | 2 |
| sphere | 0.90 | 31% | 10% | 0.92 | 84% | 0.29 | 0 | 0 | 0 | 0 | 0 | 0 |
| cylinder | 0.42 | 31% | 13% | 0.91 | 59% | 0.08 | 11 | 0 | 9 | 0 | 0 | 2 |
| arch | 0.79 | 56% | 24% | 0.83 | 58% | 0.12 | 14 | 0 | 3 | 0 | 0 | 11 |
| dumbbell | 0.77 | 43% | 19% | 0.91 | 49% | 0.10 | 15 | 0 | 11 | 0 | 0 | 3 |
| t_shape | 0.67 | 49% | 19% | 0.91 | 50% | 0.08 | 12 | 0 | 8 | 0 | 0 | 4 |
| l_shape | 0.75 | 55% | 23% | 0.91 | 56% | 0.06 | 6 | 0 | 5 | 0 | 0 | 1 |
| u_channel | 0.77 | 50% | 20% | 0.92 | 52% | 0.09 | 7 | 0 | 2 | 0 | 0 | 5 |
| plus | 0.60 | 51% | 19% | 0.80 | 49% | 0.06 | 12 | 1 | 7 | 0 | 0 | 5 |
