# Pair evaluation: t2-share-m40-expert

policy: Stage 4 contact policy logs/keep/marl2/hvB_aa_s0/model_13500.pt (robots start at their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 40 kg | 0.61 | 0.53 | 0.03 | 0.04 | 29.1 | 0.01 | 0.53 | 0.50 | 0.23 | 0.32 | 1.10 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 40 kg |
|---|---|---|
| cube | part 0 corner -x+y + part 0 corner -x-y | 0.67 |
| long | part 0 -x seg 2/2 + part 0 corner -x-y | 0.75 |
| sphere | sector 135 + sector 225 | 1.00 |
| cylinder | part 0 corner -x-y + part 0 -x seg 2/2 | 0.33 |
| arch | part 3 -x + part 2 -x | 1.00 |
| dumbbell | part 0 -x + part 1 -x | 0.42 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.75 |
| beam (unseen) | part 0 -x seg 2/5 + part 0 -x seg 4/5 | 0.33 |
| l_shape (unseen) | part 1 -x + part 0 corner -x-y | 0.67 |
| asym (unseen) | part 1 -x + part 0 corner -x+y | 0.17 |
| u_channel (unseen) | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.50 |
| plus (unseen) | part 0 corner -x-y + part 0 corner -x+y | 0.75 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 40 kg | 0.61 | 0.31 | 0.07 | 0.01 | 0.00 | 0.01 | 8.23 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 40 kg | 1.00 | 0.20 | 0.78 | 0.90 | 0.00 | 1.00 | 0.18 | 0.79 | 0.92 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 40 kg | 0.96 | 1.29 | 0.09 | 0.96 | 1.21 | 0.10 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 40 kg | 0.65 | 0.64 | 0.31 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 40 kg | 1.01 | 0.54 | 24.11 | 8.23 | 0.64 | 0.54 | 5.88 | 0.00 | 0.25 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 40 kg | 142 | 314 | 253 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 40 kg | 2015 | 0.33 | 0.36 (430) | 0.52 (269) | 0.50 (401) | 0.49 (289) | 0.69 (626) |

## both robots pushing (share of time) by object and mass

| object | 40 kg |
|---|---|
| cube | 0.16 |
| long | 0.19 |
| sphere | 0.56 |
| cylinder | 0.21 |
| arch | 0.28 |
| dumbbell | 0.27 |
| t_shape | 0.21 |
| beam | 0.31 |
| l_shape | 0.16 |
| asym | 0.19 |
| u_channel | 0.17 |
| plus | 0.09 |

## success by scenario and mass

| scenario | 40 kg |
|---|---|
| A_straight | 0.75 |
| B_left | 0.64 |
| C_backright | 0.56 |
| D_far_turn | 0.50 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 40 kg | 29% | 0% | 71% | 47% | 2% | 51% |  |  | 17% | 65% | 39% | 21% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 40 kg | 175 | 0.91 | 6% | 21% | 41% | 37% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 40 kg | 62% | 0.17 | 0.55 | 0.14 | 0.67 | 5 | 0 | 4 | 0 | 0 | 1 | 94 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.67 | 57% | 27% | 0.91 | 65% | 0.13 | 2 | 0 | 1 | 0 | 0 | 0 |
| long | 0.75 | 46% | 19% | 0.93 | 59% | 0.12 | 6 | 0 | 6 | 0 | 0 | 0 |
| sphere | 1.00 | 28% | 9% | 0.92 | 90% | 0.33 | 0 | 0 | 0 | 0 | 0 | 0 |
| cylinder | 0.33 | 27% | 9% | 0.93 | 60% | 0.10 | 3 | 0 | 2 | 0 | 0 | 1 |
| arch | 1.00 | 54% | 28% | 0.81 | 70% | 0.18 | 1 | 0 | 1 | 0 | 0 | 0 |
| dumbbell | 0.42 | 42% | 17% | 0.91 | 54% | 0.13 | 13 | 0 | 10 | 0 | 0 | 3 |
| t_shape | 0.75 | 55% | 26% | 0.91 | 60% | 0.11 | 4 | 0 | 4 | 0 | 0 | 1 |
| beam | 0.33 | 37% | 17% | 0.88 | 45% | 0.13 | 12 | 0 | 10 | 0 | 0 | 2 |
| l_shape | 0.67 | 54% | 26% | 0.92 | 62% | 0.10 | 3 | 0 | 3 | 0 | 0 | 0 |
| asym | 0.17 | 53% | 25% | 0.93 | 58% | 0.08 | 0 | 0 | 0 | 0 | 0 | 0 |
| u_channel | 0.50 | 51% | 25% | 0.92 | 52% | 0.10 | 12 | 0 | 11 | 0 | 0 | 1 |
| plus | 0.75 | 57% | 30% | 0.91 | 66% | 0.13 | 0 | 0 | 0 | 0 | 0 | 0 |
