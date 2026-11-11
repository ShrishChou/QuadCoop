# Pair evaluation: e1s-Aw-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.76 | 0.71 | 0.00 | 0.00 | 28.8 | 0.01 | 0.42 | 0.39 | 0.13 | 0.22 | 1.07 |
| 40 kg | 0.65 | 0.56 | 0.01 | 0.03 | 30.3 | 0.00 | 0.52 | 0.39 | 0.16 | 0.23 | 1.06 |
| 60 kg | 0.55 | 0.41 | 0.06 | 0.03 | 36.8 | 0.01 | 0.62 | 0.43 | 0.25 | 0.33 | 1.06 |
| 80 kg | 0.34 | 0.28 | 0.13 | 0.06 | 36.5 | 0.01 | 0.75 | 0.51 | 0.38 | 0.45 | 1.06 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 -x end + + part 0 corner -x-y | 1.00 | 0.92 | 0.75 | 0.33 |
| long | part 0 corner -x+y + part 0 -x seg 1/2 | 1.00 | 0.75 | 0.67 | 0.42 |
| sphere | sector 225 + sector 135 | 0.92 | 0.92 | 1.00 | 1.00 |
| cylinder | part 0 -x seg 1/2 + part 0 corner -x+y | 0.33 | 0.42 | 0.50 | 0.42 |
| arch | part 3 -x + part 2 -x | 0.92 | 1.00 | 0.75 | 0.50 |
| dumbbell | part 0 -x + part 1 -x | 0.58 | 0.42 | 0.58 | 0.33 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.50 | 0.50 | 0.58 | 0.08 |
| beam (unseen) | part 0 -x seg 2/5 + part 0 -x seg 4/5 | 0.75 | 0.42 | 0.00 | 0.00 |
| l_shape (unseen) | part 0 corner -x-y + part 1 -x | 0.92 | 0.92 | 0.42 | 0.17 |
| asym (unseen) | part 1 -x end - + part 0 -x end + | 0.50 | 0.08 | 0.17 | 0.00 |
| u_channel (unseen) | part 0 -x seg 1/3 + part 0 -x seg 3/3 | 0.92 | 0.75 | 0.75 | 0.50 |
| plus (unseen) | part 0 -x end - + part 0 -x end + | 0.83 | 0.67 | 0.42 | 0.33 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.76 | 0.24 | 0.00 | 0.00 | 0.00 | 0.03 | 11.14 |
| 40 kg | 0.65 | 0.31 | 0.05 | 0.00 | 0.00 | 0.01 | 8.89 |
| 60 kg | 0.55 | 0.37 | 0.08 | 0.00 | 0.00 | 0.01 | 10.58 |
| 80 kg | 0.34 | 0.47 | 0.19 | 0.00 | 0.00 | 0.00 | 9.12 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.27 | 0.67 | 0.87 | 0.00 | 1.00 | 0.28 | 0.66 | 0.86 | 0.00 |
| 40 kg | 1.00 | 0.26 | 0.72 | 0.91 | 0.00 | 1.00 | 0.25 | 0.69 | 0.89 | 0.00 |
| 60 kg | 1.00 | 0.24 | 0.72 | 0.94 | 0.00 | 1.00 | 0.24 | 0.68 | 0.93 | 0.00 |
| 80 kg | 1.00 | 0.23 | 0.72 | 0.96 | 0.00 | 1.00 | 0.24 | 0.67 | 0.93 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.78 | 2.08 | 0.07 | 0.76 | 2.02 | 0.08 |
| 40 kg | 0.77 | 1.92 | 0.09 | 0.75 | 2.08 | 0.10 |
| 60 kg | 0.78 | 1.99 | 0.10 | 0.78 | 2.22 | 0.13 |
| 80 kg | 0.78 | 1.64 | 0.12 | 0.78 | 2.28 | 0.15 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.54 | 0.51 | 0.30 |
| 40 kg | 0.59 | 0.54 | 0.29 |
| 60 kg | 0.62 | 0.52 | 0.28 |
| 80 kg | 0.65 | 0.52 | 0.25 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.48 | 0.42 | 27.58 | 11.14 | 0.73 | 0.06 | 8.28 | 0.00 | 0.32 |
| 40 kg | 0.43 | 0.45 | 27.32 | 8.89 | 1.01 | 1.04 | 5.60 | 0.00 | 0.29 |
| 60 kg | 0.70 | 0.43 | 28.44 | 10.58 | 0.33 | 1.31 | 1.99 | 0.00 | 0.31 |
| 80 kg | 0.32 | 0.44 | 27.27 | 9.12 | 0.31 | 2.87 | 0.26 | 0.00 | 0.32 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 104 | 253 | 195 |
| 40 kg | 140 | 309 | 251 |
| 60 kg | 170 | 346 | 308 |
| 80 kg | 192 | 370 | 345 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 1389 | 0.37 | 0.48 (296) | 0.49 (253) | 0.50 (301) | 0.45 (235) | 0.57 (305) |
| 40 kg | 1618 | 0.30 | 0.32 (349) | 0.52 (184) | 0.47 (368) | 0.53 (186) | 0.75 (531) |
| 60 kg | 2039 | 0.32 | 0.32 (412) | 0.46 (327) | 0.50 (378) | 0.54 (384) | 0.74 (538) |
| 80 kg | 2597 | 0.33 | 0.33 (68) | 0.40 (335) | 0.51 (1541) | 0.53 (441) | 0.65 (212) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.13 | 0.07 | 0.13 | 0.37 |
| long | 0.18 | 0.17 | 0.24 | 0.51 |
| sphere | 0.30 | 0.42 | 0.49 | 0.56 |
| cylinder | 0.07 | 0.21 | 0.24 | 0.37 |
| arch | 0.20 | 0.24 | 0.20 | 0.28 |
| dumbbell | 0.14 | 0.09 | 0.28 | 0.42 |
| t_shape | 0.07 | 0.09 | 0.17 | 0.32 |
| beam | 0.11 | 0.18 | 0.38 | 0.54 |
| l_shape | 0.07 | 0.11 | 0.16 | 0.31 |
| asym | 0.06 | 0.11 | 0.35 | 0.49 |
| u_channel | 0.11 | 0.15 | 0.23 | 0.36 |
| plus | 0.09 | 0.08 | 0.10 | 0.07 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.83 | 0.81 | 0.69 | 0.53 |
| B_left | 0.75 | 0.78 | 0.72 | 0.39 |
| C_backright | 0.67 | 0.42 | 0.36 | 0.31 |
| D_far_turn | 0.81 | 0.58 | 0.42 | 0.14 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 39% | 0% | 61% | 38% | 4% | 58% |  |  | 17% | 70% | 39% | 22% |
| 40 kg | 34% | 0% | 66% | 44% | 2% | 54% |  |  | 18% | 73% | 32% | 24% |
| 60 kg | 34% | 0% | 66% | 52% | 2% | 46% |  |  | 21% | 81% | 23% | 25% |
| 80 kg | 33% | 0% | 67% | 58% | 2% | 40% |  |  | 22% | 79% | 23% | 28% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 140 | 0.87 | 9% | 14% | 32% | 54% |
| 40 kg | 173 | 0.90 | 7% | 17% | 40% | 43% |
| 60 kg | 197 | 0.90 | 6% | 24% | 44% | 32% |
| 80 kg | 216 | 0.89 | 8% | 30% | 44% | 26% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 62% | 0.20 | 0.42 | 0.15 | 0.68 | 6 | 0 | 5 | 0 | 0 | 1 | 67 | 0.00 |  |
| 40 kg | 57% | 0.15 | 0.58 | 0.12 | 0.69 | 6 | 0 | 4 | 0 | 0 | 1 | 108 | 0.00 |  |
| 60 kg | 57% | 0.11 | 0.69 | 0.10 | 0.60 | 4 | 0 | 2 | 0 | 0 | 2 | 126 | 0.00 |  |
| 80 kg | 52% | 0.08 | 0.77 | 0.07 | 0.40 | 2 | 0 | 1 | 0 | 0 | 1 | 136 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.75 | 57% | 23% | 0.92 | 66% | 0.15 | 1 | 0 | 0 | 0 | 0 | 0 |
| long | 0.71 | 53% | 23% | 0.92 | 61% | 0.11 | 1 | 0 | 0 | 0 | 0 | 1 |
| sphere | 0.96 | 29% | 10% | 0.92 | 82% | 0.29 | 3 | 0 | 3 | 0 | 0 | 0 |
| cylinder | 0.42 | 35% | 16% | 0.91 | 65% | 0.10 | 4 | 0 | 4 | 0 | 0 | 0 |
| arch | 0.79 | 61% | 31% | 0.83 | 66% | 0.14 | 1 | 0 | 0 | 0 | 0 | 1 |
| dumbbell | 0.48 | 47% | 22% | 0.91 | 52% | 0.09 | 8 | 0 | 6 | 0 | 0 | 2 |
| t_shape | 0.42 | 53% | 23% | 0.90 | 52% | 0.07 | 7 | 0 | 5 | 0 | 0 | 2 |
| beam | 0.29 | 37% | 19% | 0.82 | 32% | 0.07 | 10 | 0 | 8 | 0 | 0 | 2 |
| l_shape | 0.60 | 52% | 20% | 0.92 | 54% | 0.08 | 3 | 0 | 2 | 0 | 0 | 1 |
| asym | 0.19 | 56% | 29% | 0.92 | 49% | 0.05 | 4 | 0 | 3 | 0 | 0 | 0 |
| u_channel | 0.73 | 49% | 19% | 0.92 | 53% | 0.10 | 5 | 0 | 3 | 0 | 0 | 3 |
| plus | 0.56 | 49% | 18% | 0.81 | 53% | 0.08 | 6 | 0 | 3 | 0 | 0 | 3 |
