# Pair evaluation: pres-planner-80kg-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 10 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 80 kg | 0.33 | 0.23 | 0.12 | 0.05 | 41.3 | 0.01 | 0.72 | 0.49 | 0.35 | 0.44 | 1.05 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 80 kg |
|---|---|---|
| cube | part 0 -x end - + part 0 corner -x+y | 0.12 |
| long | part 0 corner -x-y + part 0 -x seg 2/2 | 0.45 |
| sphere | sector 225 + sector 135 | 0.95 |
| cylinder | part 0 corner -x+y + part 0 corner -x-y | 0.28 |
| arch | part 3 -x + part 2 -x | 0.50 |
| dumbbell | part 0 -x + part 1 -x | 0.30 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.35 |
| beam (unseen) | part 0 -x seg 2/5 + part 0 -x seg 4/5 | 0.00 |
| l_shape (unseen) | part 0 corner -x-y + part 1 -x | 0.25 |
| asym (unseen) | part 1 corner -x-y + part 0 -x end - | 0.00 |
| u_channel (unseen) | part 0 -x seg 1/3 + part 0 -x seg 3/3 | 0.40 |
| plus (unseen) | part 0 -x end + + part 0 -x end - | 0.38 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 80 kg | 0.33 | 0.50 | 0.17 | 0.00 | 0.00 | 0.00 | 7.99 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 80 kg | 1.00 | 0.25 | 0.69 | 0.94 | 0.00 | 1.00 | 0.27 | 0.63 | 0.93 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 80 kg | 0.76 | 1.99 | 0.12 | 0.76 | 2.46 | 0.16 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 80 kg | 0.61 | 0.48 | 0.25 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 80 kg | 0.58 | 0.41 | 28.10 | 7.99 | 0.50 | 2.14 | 0.66 | 0.00 | 0.34 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 80 kg | 193 | 372 | 341 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 80 kg | 7897 | 0.34 | 0.36 (257) | 0.45 (911) | 0.50 (4036) | 0.54 (1855) | 0.63 (839) |

## both robots pushing (share of time) by object and mass

| object | 80 kg |
|---|---|
| cube | 0.38 |
| long | 0.32 |
| sphere | 0.43 |
| cylinder | 0.37 |
| arch | 0.20 |
| dumbbell | 0.45 |
| t_shape | 0.35 |
| beam | 0.50 |
| l_shape | 0.35 |
| asym | 0.38 |
| u_channel | 0.37 |
| plus | 0.11 |

## success by scenario and mass

| scenario | 80 kg |
|---|---|
| A_straight | 0.45 |
| B_left | 0.31 |
| C_backright | 0.38 |
| D_far_turn | 0.19 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 80 kg | 37% | 0% | 63% | 57% | 2% | 41% |  |  | 25% | 84% | 20% | 28% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 80 kg | 217 | 0.90 | 7% | 27% | 44% | 28% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 80 kg | 50% | 0.08 | 0.76 | 0.07 | 0.54 | 3 | 0 | 2 | 0 | 0 | 2 | 162 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.12 | 61% | 27% | 0.92 | 50% | 0.05 | 1 | 0 | 1 | 0 | 0 | 1 |
| long | 0.45 | 61% | 30% | 0.91 | 50% | 0.06 | 2 | 0 | 1 | 0 | 0 | 1 |
| sphere | 0.95 | 38% | 16% | 0.91 | 80% | 0.29 | 4 | 0 | 0 | 0 | 0 | 4 |
| cylinder | 0.28 | 37% | 15% | 0.90 | 61% | 0.08 | 4 | 0 | 1 | 0 | 0 | 3 |
| arch | 0.50 | 65% | 37% | 0.84 | 56% | 0.06 | 3 | 0 | 3 | 0 | 0 | 1 |
| dumbbell | 0.30 | 65% | 34% | 0.91 | 55% | 0.06 | 1 | 0 | 1 | 0 | 0 | 1 |
| t_shape | 0.35 | 60% | 27% | 0.92 | 50% | 0.05 | 5 | 1 | 3 | 0 | 0 | 2 |
| beam | 0.00 | 40% | 25% | 0.81 | 19% | 0.02 | 8 | 0 | 5 | 0 | 0 | 2 |
| l_shape | 0.25 | 62% | 27% | 0.92 | 48% | 0.06 | 2 | 0 | 1 | 0 | 0 | 1 |
| asym | 0.00 | 64% | 34% | 0.93 | 35% | 0.02 | 2 | 1 | 1 | 0 | 0 | 0 |
| u_channel | 0.40 | 59% | 27% | 0.93 | 48% | 0.05 | 4 | 0 | 1 | 0 | 0 | 3 |
| plus | 0.38 | 67% | 28% | 0.85 | 46% | 0.05 | 3 | 1 | 1 | 0 | 0 | 1 |
