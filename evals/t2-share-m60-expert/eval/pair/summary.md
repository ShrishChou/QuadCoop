# Pair evaluation: t2-share-m60-expert

policy: Stage 4 contact policy logs/keep/marl2/hvB_aa_s0/model_13500.pt (robots start at their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 60 kg | 0.58 | 0.42 | 0.08 | 0.04 | 36.2 | 0.01 | 0.60 | 0.61 | 0.36 | 0.44 | 1.06 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 60 kg |
|---|---|---|
| cube | part 0 corner -x+y + part 0 corner -x-y | 0.92 |
| long | part 0 -x seg 2/2 + part 0 corner -x-y | 0.75 |
| sphere | sector 135 + sector 225 | 0.92 |
| cylinder | part 0 corner -x-y + part 0 -x seg 2/2 | 0.42 |
| arch | part 3 -x + part 2 -x | 0.58 |
| dumbbell | part 0 -x + part 1 -x | 0.67 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.58 |
| beam (unseen) | part 0 -x seg 2/5 + part 0 -x seg 4/5 | 0.17 |
| l_shape (unseen) | part 1 -x + part 0 corner -x-y | 0.50 |
| asym (unseen) | part 1 -x + part 0 corner -x+y | 0.08 |
| u_channel (unseen) | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.75 |
| plus (unseen) | part 0 corner -x-y + part 0 corner -x+y | 0.58 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 60 kg | 0.58 | 0.30 | 0.12 | 0.00 | 0.00 | 0.01 | 9.34 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 60 kg | 1.00 | 0.18 | 0.81 | 0.93 | 0.00 | 1.00 | 0.20 | 0.75 | 0.95 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 60 kg | 0.96 | 1.22 | 0.08 | 0.96 | 1.08 | 0.11 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 60 kg | 0.71 | 0.65 | 0.29 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 60 kg | 0.93 | 0.56 | 23.80 | 9.34 | 0.92 | 1.24 | 2.43 | 0.00 | 0.23 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 60 kg | 166 | 344 | 292 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 60 kg | 2603 | 0.34 | 0.35 (570) | 0.43 (390) | 0.49 (457) | 0.56 (482) | 0.66 (704) |

## both robots pushing (share of time) by object and mass

| object | 60 kg |
|---|---|
| cube | 0.32 |
| long | 0.38 |
| sphere | 0.61 |
| cylinder | 0.40 |
| arch | 0.33 |
| dumbbell | 0.34 |
| t_shape | 0.18 |
| beam | 0.52 |
| l_shape | 0.30 |
| asym | 0.53 |
| u_channel | 0.23 |
| plus | 0.12 |

## success by scenario and mass

| scenario | 60 kg |
|---|---|
| A_straight | 0.75 |
| B_left | 0.53 |
| C_backright | 0.61 |
| D_far_turn | 0.42 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 60 kg | 25% | 0% | 75% | 53% | 2% | 45% |  |  | 15% | 81% | 22% | 21% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 60 kg | 196 | 0.90 | 6% | 26% | 45% | 28% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 60 kg | 61% | 0.13 | 0.67 | 0.11 | 0.33 | 3 | 0 | 2 | 0 | 0 | 0 | 97 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.92 | 62% | 31% | 0.92 | 69% | 0.07 | 0 | 0 | 0 | 0 | 0 | 0 |
| long | 0.75 | 61% | 33% | 0.92 | 64% | 0.10 | 1 | 0 | 1 | 0 | 0 | 0 |
| sphere | 0.92 | 33% | 10% | 0.93 | 90% | 0.34 | 0 | 0 | 0 | 0 | 0 | 0 |
| cylinder | 0.42 | 28% | 11% | 0.89 | 60% | 0.09 | 6 | 0 | 6 | 0 | 0 | 0 |
| arch | 0.58 | 56% | 33% | 0.84 | 58% | 0.10 | 10 | 0 | 10 | 0 | 0 | 0 |
| dumbbell | 0.67 | 53% | 25% | 0.91 | 61% | 0.10 | 3 | 0 | 3 | 0 | 0 | 1 |
| t_shape | 0.58 | 59% | 31% | 0.91 | 52% | 0.07 | 5 | 0 | 4 | 0 | 0 | 1 |
| beam | 0.17 | 50% | 33% | 0.86 | 37% | 0.06 | 1 | 1 | 0 | 0 | 0 | 0 |
| l_shape | 0.50 | 62% | 25% | 0.91 | 57% | 0.09 | 0 | 0 | 0 | 0 | 0 | 0 |
| asym | 0.08 | 65% | 35% | 0.93 | 60% | 0.05 | 1 | 0 | 1 | 0 | 0 | 0 |
| u_channel | 0.75 | 55% | 23% | 0.92 | 60% | 0.12 | 1 | 0 | 1 | 0 | 0 | 0 |
| plus | 0.58 | 54% | 29% | 0.93 | 59% | 0.10 | 1 | 0 | 0 | 0 | 0 | 0 |
