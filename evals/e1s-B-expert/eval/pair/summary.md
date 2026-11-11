# Pair evaluation: e1s-B-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start at their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.72 | 0.69 | 0.01 | 0.02 | 24.0 | 0.01 | 0.43 | 0.45 | 0.18 | 0.29 | 1.06 |
| 40 kg | 0.69 | 0.63 | 0.03 | 0.07 | 30.2 | 0.01 | 0.49 | 0.53 | 0.25 | 0.36 | 1.05 |
| 60 kg | 0.58 | 0.47 | 0.06 | 0.07 | 37.7 | 0.01 | 0.57 | 0.61 | 0.33 | 0.41 | 1.05 |
| 80 kg | 0.35 | 0.27 | 0.11 | 0.07 | 37.6 | 0.01 | 0.68 | 0.65 | 0.44 | 0.52 | 1.04 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 -x end + + part 0 corner -x-y | 0.92 | 1.00 | 0.83 | 0.33 |
| long | part 0 corner -x+y + part 0 -x seg 1/2 | 0.92 | 0.75 | 0.67 | 0.42 |
| sphere | sector 225 + sector 135 | 0.92 | 0.83 | 0.58 | 0.83 |
| cylinder | part 0 -x seg 1/2 + part 0 corner -x+y | 0.33 | 0.58 | 0.50 | 0.42 |
| arch | part 3 -x + part 2 -x | 0.83 | 0.92 | 0.83 | 0.50 |
| dumbbell | part 0 -x + part 1 -x | 0.33 | 0.75 | 0.75 | 0.58 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.83 | 0.75 | 0.58 | 0.33 |
| beam (unseen) | part 0 -x seg 2/5 + part 0 -x seg 4/5 | 0.67 | 0.42 | 0.08 | 0.00 |
| l_shape (unseen) | part 0 corner -x-y + part 1 -x | 0.92 | 0.58 | 0.75 | 0.17 |
| asym (unseen) | part 1 -x end - + part 0 -x end + | 0.58 | 0.17 | 0.25 | 0.00 |
| u_channel (unseen) | part 0 -x seg 1/3 + part 0 -x seg 3/3 | 0.83 | 0.83 | 0.58 | 0.17 |
| plus (unseen) | part 0 -x end - + part 0 -x end + | 0.58 | 0.75 | 0.58 | 0.42 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.72 | 0.24 | 0.03 | 0.01 | 0.00 | 0.03 | 8.31 |
| 40 kg | 0.69 | 0.21 | 0.10 | 0.00 | 0.00 | 0.00 | 7.35 |
| 60 kg | 0.58 | 0.28 | 0.13 | 0.00 | 0.00 | 0.00 | 8.72 |
| 80 kg | 0.35 | 0.47 | 0.18 | 0.00 | 0.00 | 0.01 | 7.38 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.22 | 0.73 | 0.89 | 0.00 | 1.00 | 0.22 | 0.72 | 0.91 | 0.00 |
| 40 kg | 1.00 | 0.22 | 0.76 | 0.93 | 0.00 | 1.00 | 0.20 | 0.76 | 0.94 | 0.00 |
| 60 kg | 1.00 | 0.21 | 0.77 | 0.95 | 0.00 | 1.00 | 0.21 | 0.73 | 0.95 | 0.00 |
| 80 kg | 1.00 | 0.20 | 0.75 | 0.97 | 0.00 | 1.00 | 0.21 | 0.71 | 0.97 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.95 | 1.37 | 0.07 | 0.94 | 1.38 | 0.07 |
| 40 kg | 0.94 | 1.16 | 0.08 | 0.95 | 1.30 | 0.11 |
| 60 kg | 0.95 | 1.16 | 0.09 | 0.94 | 1.21 | 0.13 |
| 80 kg | 0.95 | 0.92 | 0.12 | 0.95 | 1.11 | 0.15 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.57 | 0.59 | 0.31 |
| 40 kg | 0.65 | 0.64 | 0.31 |
| 60 kg | 0.67 | 0.63 | 0.29 |
| 80 kg | 0.67 | 0.60 | 0.24 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.41 | 0.48 | 23.33 | 8.31 | 1.23 | 0.24 | 8.54 | 0.00 | 0.28 |
| 40 kg | 0.66 | 0.53 | 22.11 | 7.35 | 0.55 | 0.75 | 6.65 | 0.00 | 0.25 |
| 60 kg | 0.66 | 0.53 | 24.20 | 8.72 | 0.81 | 0.84 | 3.01 | 0.00 | 0.26 |
| 80 kg | 0.61 | 0.50 | 25.11 | 7.38 | 0.22 | 3.11 | 0.94 | 0.00 | 0.28 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 102 | 259 | 191 |
| 40 kg | 136 | 310 | 245 |
| 60 kg | 166 | 345 | 297 |
| 80 kg | 190 | 372 | 351 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 1164 | 0.37 | 0.39 (151) | 0.51 (190) | 0.50 (344) | 0.51 (182) | 0.53 (298) |
| 40 kg | 1689 | 0.35 | 0.43 (480) | 0.50 (246) | 0.47 (294) | 0.50 (206) | 0.70 (463) |
| 60 kg | 2144 | 0.32 | 0.35 (414) | 0.45 (468) | 0.48 (381) | 0.55 (387) | 0.75 (494) |
| 80 kg | 2811 | 0.34 | 0.33 (173) | 0.38 (509) | 0.49 (1413) | 0.52 (539) | 0.64 (176) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.14 | 0.20 | 0.22 | 0.35 |
| long | 0.27 | 0.27 | 0.41 | 0.58 |
| sphere | 0.29 | 0.41 | 0.49 | 0.67 |
| cylinder | 0.18 | 0.36 | 0.44 | 0.42 |
| arch | 0.26 | 0.23 | 0.30 | 0.41 |
| dumbbell | 0.16 | 0.22 | 0.36 | 0.56 |
| t_shape | 0.11 | 0.12 | 0.21 | 0.39 |
| beam | 0.18 | 0.41 | 0.45 | 0.60 |
| l_shape | 0.11 | 0.17 | 0.23 | 0.43 |
| asym | 0.18 | 0.33 | 0.52 | 0.49 |
| u_channel | 0.14 | 0.23 | 0.27 | 0.33 |
| plus | 0.10 | 0.08 | 0.08 | 0.09 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.83 | 0.83 | 0.78 | 0.53 |
| B_left | 0.67 | 0.64 | 0.58 | 0.33 |
| C_backright | 0.67 | 0.72 | 0.61 | 0.36 |
| D_far_turn | 0.72 | 0.58 | 0.36 | 0.17 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 33% | 0% | 67% | 37% | 4% | 59% |  |  | 17% | 73% | 33% | 20% |
| 40 kg | 28% | 0% | 72% | 46% | 3% | 51% |  |  | 17% | 75% | 30% | 19% |
| 60 kg | 28% | 0% | 72% | 51% | 2% | 47% |  |  | 19% | 78% | 26% | 24% |
| 80 kg | 29% | 0% | 71% | 56% | 2% | 42% |  |  | 22% | 82% | 23% | 26% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 142 | 0.88 | 8% | 14% | 32% | 54% |
| 40 kg | 170 | 0.90 | 7% | 21% | 42% | 37% |
| 60 kg | 196 | 0.90 | 6% | 24% | 46% | 30% |
| 80 kg | 216 | 0.90 | 6% | 30% | 47% | 23% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 64% | 0.22 | 0.46 | 0.17 | 0.67 | 9 | 0 | 7 | 0 | 0 | 2 | 44 | 0.00 |  |
| 40 kg | 63% | 0.18 | 0.59 | 0.16 | 0.47 | 5 | 0 | 5 | 0 | 0 | 0 | 90 | 0.00 |  |
| 60 kg | 59% | 0.12 | 0.70 | 0.11 | 0.58 | 5 | 0 | 4 | 0 | 0 | 1 | 92 | 0.00 |  |
| 80 kg | 55% | 0.09 | 0.76 | 0.08 | 0.24 | 2 | 0 | 1 | 0 | 0 | 0 | 117 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.77 | 56% | 24% | 0.93 | 72% | 0.17 | 0 | 0 | 0 | 0 | 0 | 0 |
| long | 0.69 | 55% | 28% | 0.92 | 66% | 0.14 | 0 | 0 | 0 | 0 | 0 | 0 |
| sphere | 0.79 | 26% | 10% | 0.93 | 79% | 0.27 | 8 | 0 | 8 | 0 | 0 | 0 |
| cylinder | 0.46 | 33% | 15% | 0.91 | 67% | 0.14 | 5 | 0 | 4 | 0 | 0 | 0 |
| arch | 0.77 | 57% | 31% | 0.81 | 66% | 0.15 | 3 | 0 | 3 | 0 | 0 | 0 |
| dumbbell | 0.60 | 47% | 23% | 0.90 | 57% | 0.11 | 10 | 0 | 10 | 0 | 0 | 1 |
| t_shape | 0.62 | 47% | 22% | 0.91 | 50% | 0.08 | 11 | 0 | 10 | 0 | 0 | 1 |
| beam | 0.29 | 40% | 22% | 0.86 | 40% | 0.11 | 5 | 0 | 4 | 0 | 0 | 1 |
| l_shape | 0.60 | 51% | 22% | 0.91 | 57% | 0.09 | 3 | 0 | 3 | 0 | 0 | 0 |
| asym | 0.25 | 60% | 31% | 0.92 | 55% | 0.07 | 5 | 0 | 2 | 0 | 0 | 3 |
| u_channel | 0.60 | 47% | 18% | 0.91 | 54% | 0.11 | 6 | 0 | 4 | 0 | 0 | 2 |
| plus | 0.58 | 51% | 21% | 0.83 | 58% | 0.09 | 5 | 0 | 1 | 0 | 0 | 3 |
