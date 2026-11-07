# Pair evaluation: game-hvB-allpairs

policy: Stage 4 contact policy logs/keep/marl2/hvB_aa_s0/model_13500.pt (robots start at their contacts; contact rule re-applied: never)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 40 kg | 0.05 | 0.06 | 0.01 | 0.01 | 12.6 | 0.01 | 0.23 | 0.28 | 0.09 | 0.21 | 1.18 |
| 80 kg | 0.02 | 0.01 | 0.07 | 0.08 | 37.3 | 0.01 | 0.47 | 0.49 | 0.23 | 0.33 | 1.15 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 40 kg | 80 kg |
|---|---|---|---|
| asym (unseen) | part 1 -x + part 0 corner -x+y |  | 0.00 |
| u_channel (unseen) | part 0 -x seg 1/3 + part 0 corner -x+y |  | 0.02 |
| plus (unseen) | part 1 -x + part 0 corner -x-y |  | 0.01 |
| cube | part 0 corner -x-y + part 0 corner -x+y | 0.14 |  |
| long | part 0 -x seg 1/2 + part 0 corner -x+y | 0.07 |  |
| sphere | sector 225 + sector 135 | 0.31 |  |
| cylinder | part 0 -x seg 1/2 + part 0 corner -x+y | 0.02 | 0.11 |
| arch | part 3 corner -x+y + part 3 corner -x-y | 0.04 | 0.02 |
| dumbbell | part 1 corner -x+y + part 1 corner -x-y | 0.02 | 0.01 |
| t_shape | part 0 -x seg 1/3 + part 0 corner -x+y |  | 0.02 |
| beam (unseen) | part 0 -x seg 3/5 + part 0 -x seg 1/5 |  | 0.00 |
| l_shape (unseen) | part 0 -x seg 1/2 + part 0 corner -x+y |  | 0.00 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 40 kg | 0.05 | 0.93 | 0.02 | 0.00 | 0.00 | 0.12 | 0.00 |
| 80 kg | 0.02 | 0.83 | 0.15 | 0.00 | 0.00 | 0.01 | 0.00 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 40 kg | 1.00 | 0.19 | 0.81 | 0.95 | 0.00 | 1.00 | 0.16 | 0.84 | 0.96 | 0.00 |
| 80 kg | 1.00 | 0.19 | 0.77 | 0.98 | 0.00 | 1.00 | 0.19 | 0.75 | 0.98 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 40 kg | 1.00 | 0.02 | 0.03 | 1.00 | 0.02 | 0.03 |
| 80 kg | 1.00 | 0.02 | 0.10 | 1.00 | 0.02 | 0.13 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 40 kg | 0.56 | 0.57 | 0.83 |
| 80 kg | 0.60 | 0.56 | 0.57 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 40 kg | 1.49 | 0.39 | 30.23 | 0.00 |  |  |  |  |  |
| 80 kg | 0.59 | 0.40 | 29.94 | 0.00 |  |  |  |  |  |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 40 kg | 116 | 290 | 203 |
| 80 kg | 179 | 345 | 312 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 40 kg | 5805 | 0.38 | 0.42 (2047) | 0.46 (407) | 0.50 (718) | 0.54 (523) | 0.67 (2111) |
| 80 kg | 38813 | 0.31 | 0.30 (12292) | 0.46 (3252) | 0.50 (4796) | 0.56 (4081) | 0.71 (14394) |

## both robots pushing (share of time) by object and mass

| object | 40 kg | 80 kg |
|---|---|---|
| asym |  | 0.36 |
| u_channel |  | 0.17 |
| plus |  | 0.08 |
| cube | 0.14 |  |
| long | 0.11 |  |
| sphere | 0.30 |  |
| cylinder | 0.19 | 0.35 |
| arch | 0.05 | 0.12 |
| dumbbell | 0.06 | 0.16 |
| t_shape |  | 0.14 |
| beam |  | 0.56 |
| l_shape |  | 0.08 |

## success by scenario and mass

| scenario | 40 kg | 80 kg |
|---|---|---|
| A_straight | 0.12 | 0.04 |
| B_left | 0.03 | 0.01 |
| C_backright | 0.03 | 0.01 |
| D_far_turn | 0.02 | 0.00 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 40 kg | 25% | 0% | 75% | 21% | 2% | 77% |  |  | 25% | 65% | 52% | 17% |
| 80 kg | 29% | 0% | 71% | 45% | 2% | 54% |  |  | 29% | 76% | 34% | 25% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 40 kg | 155 | 0.86 | 11% | 6% | 23% | 71% |
| 80 kg | 204 | 0.90 | 6% | 19% | 49% | 33% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 40 kg | 25% | 0.06 | 0.45 | 0.05 | 2.90 | 34 | 0 | 30 | 0 | 0 | 4 | 88 | 0.00 |  |
| 80 kg | 31% | 0.03 | 0.68 | 0.03 | 1.15 | 9 | 0 | 7 | 0 | 0 | 1 | 122 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| asym | 0.00 | 58% | 26% | 0.93 | 29% | 0.02 | 3 | 0 | 2 | 0 | 0 | 0 |
| u_channel | 0.02 | 44% | 16% | 0.92 | 32% | 0.02 | 6 | 0 | 5 | 0 | 0 | 1 |
| plus | 0.01 | 45% | 14% | 0.92 | 33% | 0.03 | 8 | 0 | 6 | 0 | 0 | 2 |
| cube | 0.14 | 29% | 11% | 0.91 | 32% | 0.09 | 28 | 0 | 21 | 0 | 0 | 7 |
| long | 0.07 | 23% | 7% | 0.92 | 28% | 0.05 | 24 | 0 | 22 | 0 | 0 | 2 |
| sphere | 0.31 | 17% | 6% | 0.92 | 46% | 0.17 | 40 | 0 | 36 | 0 | 0 | 4 |
| cylinder | 0.07 | 19% | 6% | 0.89 | 42% | 0.05 | 16 | 0 | 16 | 0 | 0 | 0 |
| arch | 0.03 | 39% | 16% | 0.80 | 30% | 0.04 | 23 | 1 | 20 | 0 | 0 | 2 |
| dumbbell | 0.02 | 31% | 10% | 0.90 | 27% | 0.03 | 25 | 0 | 21 | 0 | 0 | 4 |
| t_shape | 0.02 | 45% | 17% | 0.93 | 34% | 0.03 | 8 | 0 | 6 | 0 | 0 | 1 |
| beam | 0.00 | 41% | 26% | 0.87 | 17% | 0.02 | 9 | 1 | 7 | 0 | 0 | 1 |
| l_shape | 0.00 | 41% | 11% | 0.93 | 30% | 0.02 | 10 | 1 | 8 | 0 | 0 | 1 |
