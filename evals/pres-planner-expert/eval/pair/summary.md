# Pair evaluation: pres-planner-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.82 | 0.74 | 0.01 | 0.01 | 26.0 | 0.01 | 0.40 | 0.38 | 0.13 | 0.25 | 1.03 |
| 40 kg | 0.78 | 0.66 | 0.01 | 0.00 | 31.9 | 0.00 | 0.49 | 0.40 | 0.17 | 0.26 | 1.06 |
| 60 kg | 0.63 | 0.48 | 0.01 | 0.01 | 37.0 | 0.01 | 0.56 | 0.45 | 0.23 | 0.32 | 1.02 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg |
|---|---|---|---|---|
| cube | part 0 -x end - + part 0 corner -x+y | 1.00 | 0.92 | 0.83 |
| long | part 0 -x seg 2/2 + part 0 corner -x-y | 0.83 | 0.92 | 0.33 |
| sphere | sector 225 + sector 135 | 1.00 | 1.00 | 0.92 |
| cylinder | part 0 corner -x-y + part 0 -x seg 2/2 | 0.50 | 0.33 | 0.33 |
| arch | part 2 -x + part 3 -x | 0.75 | 0.92 | 0.75 |
| dumbbell | part 0 -x + part 1 -x | 0.92 | 0.75 | 0.50 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.83 | 0.67 | 0.75 |
| l_shape (unseen) | part 0 corner -x-y + part 1 -x | 0.92 | 0.67 | 0.58 |
| u_channel (unseen) | part 0 -x seg 1/3 + part 0 -x seg 3/3 | 0.83 | 0.92 | 0.75 |
| plus (unseen) | part 0 -x end - + part 0 -x end + | 0.58 | 0.67 | 0.58 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.82 | 0.17 | 0.02 | 0.00 | 0.00 | 0.02 | 11.50 |
| 40 kg | 0.78 | 0.22 | 0.01 | 0.00 | 0.00 | 0.00 | 10.03 |
| 60 kg | 0.63 | 0.35 | 0.02 | 0.00 | 0.00 | 0.00 | 10.85 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.29 | 0.65 | 0.86 | 0.00 | 1.00 | 0.30 | 0.63 | 0.84 | 0.00 |
| 40 kg | 1.00 | 0.28 | 0.69 | 0.89 | 0.00 | 1.00 | 0.25 | 0.70 | 0.88 | 0.00 |
| 60 kg | 1.00 | 0.27 | 0.70 | 0.92 | 0.00 | 1.00 | 0.26 | 0.70 | 0.91 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.78 | 1.88 | 0.07 | 0.75 | 2.02 | 0.08 |
| 40 kg | 0.75 | 1.92 | 0.09 | 0.75 | 1.88 | 0.09 |
| 60 kg | 0.76 | 1.76 | 0.10 | 0.76 | 1.91 | 0.11 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.49 | 0.48 | 0.29 |
| 40 kg | 0.55 | 0.54 | 0.30 |
| 60 kg | 0.59 | 0.52 | 0.28 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.94 | 0.38 | 25.24 | 11.50 | 0.11 | 0.08 | 7.49 | 0.00 | 0.34 |
| 40 kg | 0.87 | 0.42 | 25.13 | 10.03 | 0.23 | 0.71 | 5.39 | 0.00 | 0.29 |
| 60 kg | 1.13 | 0.41 | 26.94 | 10.85 | 0.52 | 1.44 | 2.48 | 0.00 | 0.31 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 105 | 262 | 193 |
| 40 kg | 140 | 316 | 253 |
| 60 kg | 172 | 348 | 303 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 820 | 0.33 | 0.40 (149) | 0.50 (113) | 0.52 (316) | 0.54 (115) | 0.63 (127) |
| 40 kg | 1185 | 0.31 | 0.31 (264) | 0.47 (161) | 0.49 (292) | 0.54 (143) | 0.70 (326) |
| 60 kg | 1513 | 0.30 | 0.29 (303) | 0.31 (257) | 0.49 (297) | 0.61 (263) | 0.76 (393) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg |
|---|---|---|---|
| cube | 0.13 | 0.22 | 0.30 |
| long | 0.09 | 0.07 | 0.16 |
| sphere | 0.21 | 0.43 | 0.48 |
| cylinder | 0.18 | 0.06 | 0.33 |
| arch | 0.16 | 0.16 | 0.18 |
| dumbbell | 0.17 | 0.22 | 0.23 |
| t_shape | 0.15 | 0.13 | 0.24 |
| l_shape | 0.04 | 0.11 | 0.09 |
| u_channel | 0.15 | 0.15 | 0.21 |
| plus | 0.05 | 0.13 | 0.10 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg |
|---|---|---|---|
| A_straight | 0.83 | 0.83 | 0.77 |
| B_left | 0.83 | 0.73 | 0.70 |
| C_backright | 0.83 | 0.83 | 0.50 |
| D_far_turn | 0.77 | 0.70 | 0.57 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 42% | 0% | 58% | 38% | 4% | 58% |  |  | 18% | 62% | 45% | 23% |
| 40 kg | 36% | 0% | 64% | 45% | 2% | 52% |  |  | 17% | 66% | 39% | 22% |
| 60 kg | 34% | 0% | 66% | 50% | 2% | 48% |  |  | 20% | 77% | 26% | 25% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 143 | 0.89 | 8% | 12% | 33% | 55% |
| 40 kg | 175 | 0.90 | 6% | 17% | 40% | 44% |
| 60 kg | 199 | 0.90 | 6% | 19% | 45% | 35% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 65% | 0.22 | 0.44 | 0.16 | 0.60 | 5 | 0 | 3 | 0 | 0 | 2 | 59 | 0.00 |  |
| 40 kg | 62% | 0.17 | 0.56 | 0.13 | 0.64 | 6 | 0 | 4 | 0 | 0 | 2 | 85 | 0.00 |  |
| 60 kg | 58% | 0.12 | 0.68 | 0.10 | 0.53 | 5 | 0 | 3 | 0 | 0 | 2 | 94 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.92 | 53% | 23% | 0.92 | 74% | 0.18 | 0 | 0 | 0 | 0 | 0 | 0 |
| long | 0.69 | 50% | 18% | 0.91 | 60% | 0.11 | 1 | 0 | 0 | 0 | 0 | 1 |
| sphere | 0.97 | 28% | 9% | 0.92 | 83% | 0.29 | 1 | 0 | 1 | 0 | 0 | 0 |
| cylinder | 0.39 | 29% | 12% | 0.92 | 58% | 0.09 | 10 | 0 | 9 | 0 | 0 | 1 |
| arch | 0.81 | 54% | 22% | 0.83 | 60% | 0.15 | 9 | 0 | 2 | 0 | 0 | 7 |
| dumbbell | 0.72 | 39% | 14% | 0.91 | 54% | 0.13 | 9 | 0 | 8 | 0 | 0 | 1 |
| t_shape | 0.75 | 46% | 16% | 0.91 | 54% | 0.11 | 9 | 0 | 7 | 0 | 0 | 2 |
| l_shape | 0.72 | 50% | 18% | 0.92 | 59% | 0.09 | 4 | 0 | 3 | 0 | 0 | 1 |
| u_channel | 0.83 | 47% | 14% | 0.93 | 57% | 0.12 | 7 | 0 | 4 | 0 | 0 | 3 |
| plus | 0.61 | 51% | 16% | 0.82 | 57% | 0.08 | 5 | 0 | 1 | 0 | 0 | 3 |
