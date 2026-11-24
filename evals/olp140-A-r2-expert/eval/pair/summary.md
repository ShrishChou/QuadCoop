# Pair evaluation: olp140-A-r2-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto); planner settings changed: fail_mem=0.5

success = 10 cm / 6 deg held 1 s within 140 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.81 | 0.77 | 0.02 | 0.02 | 32.0 | 0.01 | 0.42 | 0.36 | 0.12 | 0.22 | 1.03 |
| 40 kg | 0.79 | 0.65 | 0.01 | 0.01 | 36.0 | 0.00 | 0.50 | 0.37 | 0.15 | 0.24 | 1.06 |
| 60 kg | 0.74 | 0.54 | 0.03 | 0.03 | 48.6 | 0.01 | 0.59 | 0.43 | 0.24 | 0.33 | 1.05 |
| 80 kg | 0.52 | 0.37 | 0.08 | 0.05 | 58.0 | 0.01 | 0.63 | 0.52 | 0.32 | 0.41 | 1.01 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 -x end - + part 0 corner -x+y | 0.92 | 0.92 | 0.83 | 0.33 |
| long | part 0 -x seg 2/2 + part 0 corner -x-y | 0.92 | 0.92 | 0.67 | 0.33 |
| sphere | sector 225 + sector 135 | 1.00 | 1.00 | 1.00 | 0.83 |
| cylinder | part 0 corner -x-y + part 0 -x seg 2/2 | 0.33 | 0.42 | 0.42 | 0.25 |
| arch | part 2 -x + part 3 -x | 0.83 | 0.92 | 0.92 | 0.83 |
| dumbbell | part 0 -x + part 1 -x | 0.83 | 0.83 | 0.67 | 0.58 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.75 | 0.83 | 0.83 | 0.67 |
| l_shape (unseen) | part 0 corner -x-y + part 1 -x | 0.92 | 0.75 | 0.75 | 0.33 |
| u_channel (unseen) | part 0 -x seg 1/3 + part 0 -x seg 3/3 | 1.00 | 0.75 | 0.92 | 0.42 |
| plus (unseen) | part 0 -x end - + part 0 -x end + | 0.58 | 0.58 | 0.42 | 0.58 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.81 | 0.16 | 0.03 | 0.00 | 0.00 | 0.01 | 13.70 |
| 40 kg | 0.79 | 0.19 | 0.02 | 0.00 | 0.00 | 0.01 | 12.40 |
| 60 kg | 0.74 | 0.21 | 0.05 | 0.00 | 0.00 | 0.00 | 18.21 |
| 80 kg | 0.52 | 0.35 | 0.13 | 0.00 | 0.00 | 0.00 | 16.38 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.27 | 0.68 | 0.86 | 0.00 | 1.00 | 0.28 | 0.68 | 0.85 | 0.00 |
| 40 kg | 1.00 | 0.25 | 0.73 | 0.90 | 0.00 | 1.00 | 0.25 | 0.71 | 0.88 | 0.00 |
| 60 kg | 1.00 | 0.24 | 0.72 | 0.92 | 0.00 | 1.00 | 0.25 | 0.69 | 0.90 | 0.00 |
| 80 kg | 1.00 | 0.26 | 0.73 | 0.94 | 0.00 | 1.00 | 0.25 | 0.67 | 0.92 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.76 | 1.81 | 0.06 | 0.76 | 2.09 | 0.07 |
| 40 kg | 0.78 | 2.08 | 0.07 | 0.78 | 2.09 | 0.08 |
| 60 kg | 0.78 | 1.88 | 0.10 | 0.77 | 2.20 | 0.10 |
| 80 kg | 0.78 | 1.92 | 0.09 | 0.78 | 2.36 | 0.13 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.52 | 0.53 | 0.31 |
| 40 kg | 0.59 | 0.55 | 0.29 |
| 60 kg | 0.61 | 0.54 | 0.29 |
| 80 kg | 0.63 | 0.54 | 0.26 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.62 | 0.46 | 30.58 | 13.70 | 1.09 | 1.04 | 16.30 | 0.00 | 0.28 |
| 40 kg | 0.99 | 0.46 | 29.01 | 12.40 | 0.42 | 0.88 | 14.20 | 0.00 | 0.27 |
| 60 kg | 1.47 | 0.43 | 32.38 | 18.21 | 0.89 | 1.98 | 5.71 | 0.00 | 0.32 |
| 80 kg | 3.88 | 0.45 | 35.30 | 16.38 | 0.62 | 4.68 | 2.40 | 0.00 | 0.32 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 111 | 258 | 207 |
| 40 kg | 138 | 310 | 253 |
| 60 kg | 168 | 345 | 300 |
| 80 kg | 191 | 372 | 349 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 1683 | 0.33 | 0.44 (225) | 0.50 (255) | 0.51 (553) | 0.49 (315) | 0.54 (336) |
| 40 kg | 2079 | 0.33 | 0.36 (317) | 0.45 (158) | 0.50 (680) | 0.47 (466) | 0.66 (458) |
| 60 kg | 1958 | 0.30 | 0.28 (312) | 0.36 (238) | 0.47 (283) | 0.60 (357) | 0.73 (768) |
| 80 kg | 2780 | 0.33 | 0.32 (149) | 0.36 (398) | 0.52 (1459) | 0.61 (566) | 0.69 (209) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.10 | 0.14 | 0.29 | 0.35 |
| long | 0.10 | 0.11 | 0.18 | 0.31 |
| sphere | 0.24 | 0.42 | 0.49 | 0.46 |
| cylinder | 0.11 | 0.09 | 0.31 | 0.31 |
| arch | 0.13 | 0.15 | 0.18 | 0.31 |
| dumbbell | 0.21 | 0.23 | 0.23 | 0.33 |
| t_shape | 0.09 | 0.09 | 0.20 | 0.47 |
| l_shape | 0.06 | 0.11 | 0.11 | 0.17 |
| u_channel | 0.10 | 0.15 | 0.25 | 0.36 |
| plus | 0.05 | 0.05 | 0.11 | 0.11 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.90 | 0.77 | 0.90 | 0.67 |
| B_left | 0.73 | 0.80 | 0.80 | 0.47 |
| C_backright | 0.73 | 0.70 | 0.57 | 0.40 |
| D_far_turn | 0.87 | 0.90 | 0.70 | 0.53 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 39% | 0% | 61% | 41% | 4% | 56% |  |  | 17% | 63% | 47% | 24% |
| 40 kg | 34% | 0% | 66% | 47% | 3% | 51% |  |  | 18% | 67% | 39% | 23% |
| 60 kg | 34% | 0% | 66% | 51% | 2% | 47% |  |  | 19% | 73% | 30% | 24% |
| 80 kg | 34% | 0% | 66% | 56% | 2% | 42% |  |  | 21% | 79% | 25% | 26% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 145 | 0.88 | 8% | 15% | 32% | 53% |
| 40 kg | 172 | 0.90 | 7% | 18% | 40% | 42% |
| 60 kg | 197 | 0.90 | 7% | 20% | 45% | 35% |
| 80 kg | 218 | 0.90 | 6% | 25% | 44% | 31% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 65% | 0.21 | 0.39 | 0.15 | 0.90 | 8 | 0 | 5 | 0 | 0 | 3 | 75 | 0.00 |  |
| 40 kg | 61% | 0.16 | 0.53 | 0.13 | 0.89 | 10 | 0 | 7 | 0 | 0 | 3 | 75 | 0.00 |  |
| 60 kg | 56% | 0.12 | 0.65 | 0.10 | 0.59 | 7 | 1 | 4 | 0 | 0 | 2 | 124 | 0.00 |  |
| 80 kg | 51% | 0.09 | 0.73 | 0.08 | 0.89 | 7 | 1 | 3 | 0 | 0 | 3 | 137 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.75 | 58% | 26% | 0.92 | 68% | 0.14 | 0 | 0 | 0 | 0 | 0 | 0 |
| long | 0.71 | 52% | 19% | 0.91 | 55% | 0.09 | 4 | 0 | 2 | 0 | 0 | 1 |
| sphere | 0.96 | 31% | 11% | 0.91 | 85% | 0.30 | 0 | 0 | 0 | 0 | 0 | 0 |
| cylinder | 0.35 | 30% | 13% | 0.91 | 56% | 0.06 | 11 | 0 | 10 | 0 | 0 | 1 |
| arch | 0.88 | 59% | 25% | 0.83 | 61% | 0.13 | 9 | 0 | 0 | 0 | 0 | 9 |
| dumbbell | 0.73 | 45% | 19% | 0.91 | 51% | 0.10 | 12 | 0 | 11 | 0 | 0 | 1 |
| t_shape | 0.77 | 53% | 22% | 0.92 | 53% | 0.08 | 12 | 0 | 6 | 0 | 0 | 6 |
| l_shape | 0.69 | 52% | 20% | 0.91 | 54% | 0.07 | 7 | 0 | 5 | 0 | 0 | 2 |
| u_channel | 0.77 | 51% | 18% | 0.92 | 54% | 0.10 | 5 | 0 | 2 | 0 | 0 | 3 |
| plus | 0.54 | 54% | 21% | 0.80 | 49% | 0.06 | 17 | 2 | 10 | 0 | 0 | 5 |
