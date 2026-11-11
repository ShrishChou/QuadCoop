# Pair evaluation: e1s-D-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start at their contacts; contact rule re-applied: never)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.09 | 0.10 | 0.01 | 0.01 | 6.5 | 0.03 | 0.16 | 0.23 | 0.09 | 0.28 | 1.03 |
| 40 kg | 0.07 | 0.09 | 0.02 | 0.00 | 10.7 | 0.02 | 0.22 | 0.27 | 0.10 | 0.26 | 1.05 |
| 60 kg | 0.11 | 0.12 | 0.04 | 0.02 | 15.9 | 0.01 | 0.39 | 0.37 | 0.22 | 0.41 | 1.06 |
| 80 kg | 0.08 | 0.08 | 0.09 | 0.03 | 20.9 | 0.01 | 0.53 | 0.48 | 0.29 | 0.42 | 1.03 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 -x end + + part 0 corner -x-y | 0.17 | 0.25 | 0.17 | 0.08 |
| long | part 0 corner -x+y + part 0 -x seg 1/2 | 0.17 | 0.17 | 0.17 | 0.08 |
| sphere | sector 225 + sector 135 | 0.08 | 0.00 | 0.33 | 0.42 |
| cylinder | part 0 -x seg 1/2 + part 0 corner -x+y | 0.08 | 0.08 | 0.08 | 0.08 |
| arch | part 3 -x + part 2 -x | 0.25 | 0.17 | 0.25 | 0.25 |
| dumbbell | part 0 -x + part 1 -x | 0.08 | 0.08 | 0.17 | 0.08 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.00 | 0.00 | 0.00 | 0.00 |
| beam (unseen) | part 0 -x seg 2/5 + part 0 -x seg 4/5 | 0.25 | 0.00 | 0.00 | 0.00 |
| l_shape (unseen) | part 0 corner -x-y + part 1 -x | 0.00 | 0.00 | 0.00 | 0.00 |
| asym (unseen) | part 1 -x end - + part 0 -x end + | 0.00 | 0.08 | 0.08 | 0.00 |
| u_channel (unseen) | part 0 -x seg 1/3 + part 0 -x seg 3/3 | 0.00 | 0.00 | 0.08 | 0.00 |
| plus (unseen) | part 0 -x end - + part 0 -x end + | 0.00 | 0.00 | 0.00 | 0.00 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.09 | 0.90 | 0.01 | 0.00 | 0.00 | 0.16 | 0.00 |
| 40 kg | 0.07 | 0.91 | 0.02 | 0.00 | 0.00 | 0.05 | 0.00 |
| 60 kg | 0.11 | 0.83 | 0.06 | 0.00 | 0.00 | 0.05 | 0.00 |
| 80 kg | 0.08 | 0.79 | 0.12 | 0.00 | 0.00 | 0.01 | 0.00 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.18 | 0.82 | 0.98 | 0.00 | 1.00 | 0.19 | 0.80 | 0.96 | 0.00 |
| 40 kg | 1.00 | 0.18 | 0.82 | 0.99 | 0.00 | 1.00 | 0.19 | 0.80 | 0.95 | 0.00 |
| 60 kg | 1.00 | 0.19 | 0.81 | 0.99 | 0.00 | 1.00 | 0.19 | 0.78 | 0.98 | 0.00 |
| 80 kg | 1.00 | 0.18 | 0.79 | 0.98 | 0.00 | 1.00 | 0.22 | 0.73 | 0.97 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.02 | 0.02 | 1.00 | 0.02 | 0.02 |
| 40 kg | 1.00 | 0.02 | 0.03 | 1.00 | 0.02 | 0.05 |
| 60 kg | 1.00 | 0.02 | 0.06 | 1.00 | 0.02 | 0.08 |
| 80 kg | 1.00 | 0.02 | 0.10 | 1.00 | 0.02 | 0.12 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.59 | 0.59 | 0.84 |
| 40 kg | 0.63 | 0.61 | 0.82 |
| 60 kg | 0.66 | 0.62 | 0.69 |
| 80 kg | 0.64 | 0.58 | 0.59 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.31 | 0.44 | 24.27 | 0.00 | 0.00 | 0.00 | 10.88 | 0.00 | 0.31 |
| 40 kg | 0.74 | 0.47 | 27.87 | 0.00 | 0.00 | 0.00 | 10.81 | 0.00 | 0.29 |
| 60 kg | 0.19 | 0.49 | 28.95 | 0.00 | 0.00 | 0.00 | 6.43 | 0.00 | 0.29 |
| 80 kg | 0.59 | 0.44 | 27.03 | 0.00 | 0.00 | 0.00 | 3.99 | 0.00 | 0.30 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 75 | 220 | 129 |
| 40 kg | 112 | 289 | 205 |
| 60 kg | 149 | 331 | 268 |
| 80 kg | 181 | 358 | 319 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 381 | 0.44 | 0.48 (93) | 0.50 (61) | 0.52 (83) | 0.49 (51) | 0.56 (93) |
| 40 kg | 902 | 0.35 | 0.34 (179) | 0.54 (153) | 0.47 (151) | 0.50 (118) | 0.71 (300) |
| 60 kg | 1917 | 0.33 | 0.29 (432) | 0.51 (325) | 0.47 (307) | 0.49 (246) | 0.67 (607) |
| 80 kg | 2635 | 0.35 | 0.32 (590) | 0.46 (306) | 0.52 (758) | 0.50 (391) | 0.56 (590) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.04 | 0.07 | 0.03 | 0.13 |
| long | 0.08 | 0.13 | 0.28 | 0.27 |
| sphere | 0.18 | 0.06 | 0.39 | 0.46 |
| cylinder | 0.08 | 0.18 | 0.15 | 0.18 |
| arch | 0.23 | 0.17 | 0.32 | 0.43 |
| dumbbell | 0.09 | 0.12 | 0.24 | 0.41 |
| t_shape | 0.05 | 0.09 | 0.13 | 0.25 |
| beam | 0.15 | 0.09 | 0.28 | 0.59 |
| l_shape | 0.03 | 0.04 | 0.06 | 0.21 |
| asym | 0.05 | 0.14 | 0.52 | 0.35 |
| u_channel | 0.04 | 0.05 | 0.17 | 0.21 |
| plus | 0.01 | 0.02 | 0.02 | 0.03 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.25 | 0.22 | 0.39 | 0.25 |
| B_left | 0.08 | 0.03 | 0.00 | 0.03 |
| C_backright | 0.03 | 0.03 | 0.03 | 0.03 |
| D_far_turn | 0.00 | 0.00 | 0.03 | 0.03 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 25% | 0% | 75% | 12% | 3% | 85% |  |  | 25% | 71% | 43% | 18% |
| 40 kg | 25% | 0% | 75% | 20% | 2% | 78% |  |  | 25% | 74% | 41% | 19% |
| 60 kg | 25% | 0% | 75% | 35% | 2% | 63% |  |  | 25% | 80% | 31% | 21% |
| 80 kg | 27% | 0% | 73% | 46% | 2% | 52% |  |  | 27% | 84% | 25% | 24% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 121 | 0.87 | 10% | 2% | 14% | 83% |
| 40 kg | 156 | 0.89 | 8% | 6% | 21% | 72% |
| 60 kg | 183 | 0.89 | 8% | 15% | 36% | 50% |
| 80 kg | 209 | 0.90 | 7% | 21% | 45% | 34% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 23% | 0.10 | 0.39 | 0.08 | 2.91 | 46 | 0 | 42 | 0 | 0 | 4 | 58 | 0.00 |  |
| 40 kg | 24% | 0.07 | 0.50 | 0.06 | 2.57 | 39 | 0 | 34 | 0 | 0 | 5 | 79 | 0.00 |  |
| 60 kg | 37% | 0.08 | 0.58 | 0.06 | 1.72 | 20 | 0 | 18 | 0 | 0 | 2 | 107 | 0.00 |  |
| 80 kg | 41% | 0.06 | 0.70 | 0.05 | 1.15 | 10 | 0 | 8 | 0 | 0 | 2 | 100 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.17 | 31% | 10% | 0.93 | 34% | 0.08 | 29 | 0 | 25 | 0 | 0 | 4 |
| long | 0.15 | 33% | 12% | 0.92 | 38% | 0.08 | 16 | 0 | 16 | 0 | 0 | 0 |
| sphere | 0.21 | 14% | 5% | 0.93 | 36% | 0.15 | 47 | 0 | 42 | 0 | 0 | 5 |
| cylinder | 0.08 | 17% | 7% | 0.89 | 37% | 0.07 | 30 | 0 | 29 | 0 | 0 | 1 |
| arch | 0.23 | 37% | 21% | 0.81 | 40% | 0.10 | 27 | 0 | 27 | 0 | 0 | 0 |
| dumbbell | 0.10 | 30% | 13% | 0.91 | 34% | 0.06 | 28 | 0 | 26 | 0 | 0 | 2 |
| t_shape | 0.00 | 28% | 12% | 0.91 | 26% | 0.04 | 35 | 0 | 34 | 0 | 0 | 1 |
| beam | 0.06 | 29% | 14% | 0.87 | 23% | 0.06 | 22 | 1 | 20 | 0 | 0 | 1 |
| l_shape | 0.00 | 21% | 6% | 0.92 | 24% | 0.03 | 29 | 0 | 27 | 0 | 0 | 1 |
| asym | 0.04 | 42% | 21% | 0.92 | 37% | 0.03 | 18 | 0 | 18 | 0 | 0 | 0 |
| u_channel | 0.02 | 21% | 6% | 0.91 | 22% | 0.04 | 32 | 0 | 27 | 0 | 0 | 5 |
| plus | 0.00 | 35% | 7% | 0.75 | 22% | 0.03 | 30 | 0 | 12 | 0 | 0 | 18 |
