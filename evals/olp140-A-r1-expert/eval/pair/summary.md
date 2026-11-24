# Pair evaluation: olp140-A-r1-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto); planner settings changed: fail_mem=0.5

success = 10 cm / 6 deg held 1 s within 140 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.78 | 0.67 | 0.02 | 0.01 | 28.5 | 0.01 | 0.36 | 0.36 | 0.12 | 0.23 | 1.04 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg |
|---|---|---|
| cube | part 0 -x end - + part 0 corner -x+y | 0.92 |
| long | part 0 -x seg 2/2 + part 0 corner -x-y | 0.75 |
| sphere | sector 225 + sector 135 | 1.00 |
| cylinder | part 0 corner -x-y + part 0 -x seg 2/2 | 0.50 |
| arch | part 2 -x + part 3 -x | 0.83 |
| dumbbell | part 0 -x + part 1 -x | 0.83 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.58 |
| l_shape (unseen) | part 0 corner -x-y + part 1 -x | 0.83 |
| u_channel (unseen) | part 0 -x seg 1/3 + part 0 -x seg 3/3 | 0.75 |
| plus (unseen) | part 0 -x end - + part 0 -x end + | 0.83 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.78 | 0.19 | 0.03 | 0.00 | 0.00 | 0.01 | 13.35 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.28 | 0.67 | 0.86 | 0.00 | 1.00 | 0.33 | 0.61 | 0.83 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.77 | 1.93 | 0.06 | 0.75 | 2.10 | 0.07 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.49 | 0.46 | 0.30 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 2.36 | 0.37 | 30.32 | 13.35 | 0.95 | 0.57 | 15.19 | 0.00 | 0.36 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 101 | 251 | 197 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 1023 | 0.33 | 0.43 (180) | 0.50 (158) | 0.50 (394) | 0.51 (146) | 0.61 (144) |

## both robots pushing (share of time) by object and mass

| object | 20 kg |
|---|---|
| cube | 0.12 |
| long | 0.09 |
| sphere | 0.18 |
| cylinder | 0.15 |
| arch | 0.13 |
| dumbbell | 0.20 |
| t_shape | 0.07 |
| l_shape | 0.03 |
| u_channel | 0.14 |
| plus | 0.07 |

## success by scenario and mass

| scenario | 20 kg |
|---|---|
| A_straight | 0.83 |
| B_left | 0.73 |
| C_backright | 0.73 |
| D_far_turn | 0.83 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 43% | 0% | 57% | 35% | 4% | 61% |  |  | 18% | 62% | 45% | 24% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 138 | 0.89 | 8% | 10% | 30% | 60% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 60% | 0.20 | 0.42 | 0.15 | 1.37 | 14 | 0 | 11 | 0 | 0 | 4 | 84 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.92 | 44% | 15% | 0.91 | 78% | 0.24 | 0 | 0 | 0 | 0 | 0 | 0 |
| long | 0.75 | 43% | 15% | 0.91 | 67% | 0.14 | 5 | 0 | 4 | 0 | 0 | 1 |
| sphere | 1.00 | 24% | 8% | 0.93 | 80% | 0.21 | 1 | 0 | 1 | 0 | 0 | 0 |
| cylinder | 0.50 | 25% | 10% | 0.91 | 59% | 0.12 | 12 | 0 | 11 | 0 | 0 | 1 |
| arch | 0.83 | 38% | 11% | 0.80 | 51% | 0.16 | 21 | 0 | 9 | 0 | 0 | 12 |
| dumbbell | 0.83 | 30% | 8% | 0.88 | 55% | 0.17 | 20 | 0 | 19 | 0 | 0 | 2 |
| t_shape | 0.58 | 34% | 12% | 0.90 | 47% | 0.09 | 32 | 0 | 25 | 0 | 0 | 7 |
| l_shape | 0.83 | 41% | 11% | 0.91 | 61% | 0.11 | 6 | 0 | 5 | 0 | 0 | 1 |
| u_channel | 0.75 | 32% | 6% | 0.91 | 49% | 0.14 | 24 | 0 | 22 | 0 | 0 | 2 |
| plus | 0.83 | 40% | 9% | 0.80 | 51% | 0.10 | 21 | 0 | 10 | 0 | 0 | 12 |
