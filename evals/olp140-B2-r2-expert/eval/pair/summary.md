# Pair evaluation: olp140-B2-r2-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto); planner settings changed: fail_mem=1,fail_act=2

success = 10 cm / 6 deg held 1 s within 140 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.89 | 0.82 | 0.00 | 0.01 | 33.4 | 0.01 | 0.40 | 0.36 | 0.12 | 0.22 | 1.08 |
| 40 kg | 0.80 | 0.66 | 0.00 | 0.05 | 36.5 | 0.01 | 0.47 | 0.40 | 0.16 | 0.24 | 1.07 |
| 60 kg | 0.71 | 0.51 | 0.04 | 0.02 | 43.7 | 0.01 | 0.55 | 0.44 | 0.22 | 0.32 | 1.05 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg |
|---|---|---|---|---|
| cube | part 0 -x end - + part 0 corner -x+y | 0.92 | 1.00 | 0.92 |
| long | part 0 -x seg 2/2 + part 0 corner -x-y | 1.00 | 0.92 | 0.67 |
| sphere | sector 225 + sector 135 | 1.00 | 0.92 | 1.00 |
| cylinder | part 0 corner -x-y + part 0 -x seg 2/2 | 0.67 | 0.50 | 0.50 |
| arch | part 2 -x + part 3 -x | 0.83 | 0.92 | 0.67 |
| dumbbell | part 0 -x + part 1 -x | 0.92 | 0.75 | 0.58 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.83 | 0.83 | 0.92 |
| l_shape (unseen) | part 0 corner -x-y + part 1 -x | 0.92 | 0.75 | 0.92 |
| u_channel (unseen) | part 0 -x seg 1/3 + part 0 -x seg 3/3 | 0.92 | 0.75 | 0.58 |
| plus (unseen) | part 0 -x end - + part 0 -x end + | 0.92 | 0.67 | 0.33 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.89 | 0.10 | 0.01 | 0.00 | 0.00 | 0.02 | 17.13 |
| 40 kg | 0.80 | 0.15 | 0.05 | 0.00 | 0.00 | 0.00 | 14.57 |
| 60 kg | 0.71 | 0.23 | 0.06 | 0.00 | 0.00 | 0.00 | 17.93 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.29 | 0.66 | 0.86 | 0.00 | 1.00 | 0.28 | 0.66 | 0.85 | 0.00 |
| 40 kg | 1.00 | 0.27 | 0.70 | 0.89 | 0.00 | 1.00 | 0.25 | 0.71 | 0.88 | 0.00 |
| 60 kg | 1.00 | 0.26 | 0.71 | 0.91 | 0.00 | 1.00 | 0.25 | 0.70 | 0.91 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.77 | 2.00 | 0.07 | 0.76 | 2.01 | 0.07 |
| 40 kg | 0.77 | 1.87 | 0.08 | 0.76 | 1.89 | 0.08 |
| 60 kg | 0.75 | 1.97 | 0.09 | 0.76 | 2.31 | 0.10 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.50 | 0.50 | 0.30 |
| 40 kg | 0.57 | 0.55 | 0.30 |
| 60 kg | 0.59 | 0.54 | 0.28 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.61 | 0.39 | 29.34 | 17.13 | 0.61 | 0.27 | 16.07 | 0.00 | 0.33 |
| 40 kg | 0.42 | 0.44 | 28.25 | 14.57 | 0.71 | 1.22 | 11.30 | 0.00 | 0.28 |
| 60 kg | 1.60 | 0.41 | 31.24 | 17.93 | 0.44 | 2.24 | 5.13 | 0.00 | 0.32 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 105 | 255 | 204 |
| 40 kg | 142 | 308 | 258 |
| 60 kg | 166 | 341 | 295 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 1254 | 0.34 | 0.47 (208) | 0.53 (234) | 0.51 (353) | 0.51 (289) | 0.58 (171) |
| 40 kg | 1543 | 0.34 | 0.37 (375) | 0.49 (279) | 0.51 (235) | 0.50 (221) | 0.67 (434) |
| 60 kg | 1630 | 0.30 | 0.29 (347) | 0.38 (304) | 0.51 (246) | 0.57 (265) | 0.77 (468) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg |
|---|---|---|---|
| cube | 0.13 | 0.17 | 0.30 |
| long | 0.11 | 0.07 | 0.11 |
| sphere | 0.22 | 0.42 | 0.50 |
| cylinder | 0.13 | 0.11 | 0.29 |
| arch | 0.15 | 0.09 | 0.19 |
| dumbbell | 0.17 | 0.25 | 0.22 |
| t_shape | 0.08 | 0.12 | 0.18 |
| l_shape | 0.05 | 0.10 | 0.14 |
| u_channel | 0.11 | 0.15 | 0.23 |
| plus | 0.07 | 0.07 | 0.07 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg |
|---|---|---|---|
| A_straight | 0.90 | 0.87 | 0.87 |
| B_left | 0.87 | 0.77 | 0.93 |
| C_backright | 0.87 | 0.83 | 0.43 |
| D_far_turn | 0.93 | 0.73 | 0.60 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 41% | 0% | 59% | 38% | 4% | 58% |  |  | 18% | 66% | 43% | 23% |
| 40 kg | 35% | 0% | 65% | 45% | 2% | 53% |  |  | 17% | 69% | 37% | 23% |
| 60 kg | 34% | 0% | 66% | 50% | 2% | 48% |  |  | 19% | 76% | 27% | 24% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 142 | 0.88 | 9% | 12% | 32% | 55% |
| 40 kg | 173 | 0.89 | 7% | 16% | 40% | 43% |
| 60 kg | 196 | 0.90 | 7% | 19% | 44% | 37% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 65% | 0.21 | 0.41 | 0.15 | 0.80 | 7 | 0 | 4 | 0 | 0 | 3 | 72 | 0.00 |  |
| 40 kg | 62% | 0.16 | 0.54 | 0.13 | 0.85 | 10 | 0 | 8 | 0 | 0 | 3 | 71 | 0.00 |  |
| 60 kg | 57% | 0.12 | 0.68 | 0.11 | 1.07 | 12 | 1 | 8 | 0 | 0 | 3 | 97 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.94 | 54% | 23% | 0.93 | 75% | 0.18 | 1 | 0 | 1 | 0 | 0 | 0 |
| long | 0.86 | 50% | 19% | 0.91 | 61% | 0.10 | 2 | 0 | 0 | 0 | 0 | 1 |
| sphere | 0.97 | 28% | 9% | 0.92 | 84% | 0.29 | 0 | 0 | 0 | 0 | 0 | 0 |
| cylinder | 0.56 | 30% | 12% | 0.91 | 60% | 0.09 | 11 | 0 | 10 | 0 | 0 | 1 |
| arch | 0.81 | 50% | 18% | 0.83 | 58% | 0.14 | 17 | 0 | 5 | 0 | 0 | 12 |
| dumbbell | 0.75 | 38% | 15% | 0.91 | 52% | 0.11 | 22 | 0 | 21 | 0 | 0 | 1 |
| t_shape | 0.86 | 45% | 14% | 0.91 | 52% | 0.09 | 14 | 0 | 8 | 0 | 0 | 6 |
| l_shape | 0.86 | 52% | 18% | 0.91 | 62% | 0.10 | 4 | 0 | 3 | 0 | 0 | 0 |
| u_channel | 0.75 | 49% | 18% | 0.92 | 58% | 0.11 | 7 | 0 | 3 | 0 | 0 | 4 |
| plus | 0.64 | 44% | 15% | 0.74 | 52% | 0.09 | 20 | 1 | 14 | 0 | 0 | 4 |
