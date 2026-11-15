# Pair evaluation: pres-planner-r2-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.82 | 0.72 | 0.01 | 0.00 | 28.9 | 0.01 | 0.40 | 0.34 | 0.12 | 0.24 | 1.02 |
| 40 kg | 0.77 | 0.62 | 0.00 | 0.01 | 33.8 | 0.00 | 0.46 | 0.39 | 0.15 | 0.24 | 1.09 |
| 60 kg | 0.61 | 0.48 | 0.04 | 0.02 | 39.7 | 0.01 | 0.57 | 0.43 | 0.22 | 0.31 | 1.03 |
| 80 kg | 0.44 | 0.33 | 0.02 | 0.02 | 42.3 | 0.01 | 0.70 | 0.50 | 0.35 | 0.44 | 0.99 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 -x end - + part 0 corner -x+y | 1.00 | 0.92 | 0.75 | 0.50 |
| long | part 0 -x seg 2/2 + part 0 corner -x-y | 0.92 | 0.75 | 0.42 | 0.17 |
| sphere | sector 225 + sector 135 | 1.00 | 1.00 | 0.83 | 0.92 |
| cylinder | part 0 corner -x-y + part 0 -x seg 2/2 | 0.67 | 0.42 | 0.33 | 0.33 |
| arch | part 2 -x + part 3 -x | 0.92 | 0.92 | 0.67 | 0.42 |
| dumbbell | part 0 -x + part 1 -x | 0.92 | 0.83 | 0.67 | 0.42 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.58 | 0.67 | 0.67 | 0.50 |
| l_shape (unseen) | part 0 corner -x-y + part 1 -x | 0.83 | 0.83 | 0.58 | 0.50 |
| u_channel (unseen) | part 0 -x seg 1/3 + part 0 -x seg 3/3 | 0.67 | 0.75 | 0.67 | 0.42 |
| plus (unseen) | part 0 -x end - + part 0 -x end + | 0.67 | 0.58 | 0.50 | 0.25 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.82 | 0.17 | 0.01 | 0.00 | 0.00 | 0.01 | 12.01 |
| 40 kg | 0.77 | 0.23 | 0.01 | 0.00 | 0.00 | 0.01 | 9.93 |
| 60 kg | 0.61 | 0.33 | 0.06 | 0.00 | 0.00 | 0.00 | 10.43 |
| 80 kg | 0.44 | 0.53 | 0.03 | 0.00 | 0.00 | 0.00 | 9.72 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.29 | 0.65 | 0.86 | 0.00 | 1.00 | 0.28 | 0.65 | 0.85 | 0.00 |
| 40 kg | 1.00 | 0.27 | 0.70 | 0.89 | 0.00 | 1.00 | 0.25 | 0.69 | 0.88 | 0.00 |
| 60 kg | 1.00 | 0.25 | 0.73 | 0.93 | 0.00 | 1.00 | 0.26 | 0.70 | 0.92 | 0.00 |
| 80 kg | 1.00 | 0.23 | 0.73 | 0.95 | 0.00 | 1.00 | 0.24 | 0.67 | 0.94 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.76 | 2.00 | 0.07 | 0.75 | 1.99 | 0.06 |
| 40 kg | 0.77 | 1.96 | 0.08 | 0.77 | 2.00 | 0.09 |
| 60 kg | 0.76 | 2.42 | 0.10 | 0.76 | 2.24 | 0.11 |
| 80 kg | 0.78 | 1.95 | 0.11 | 0.78 | 2.19 | 0.15 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.48 | 0.50 | 0.31 |
| 40 kg | 0.54 | 0.54 | 0.30 |
| 60 kg | 0.60 | 0.53 | 0.29 |
| 80 kg | 0.64 | 0.52 | 0.27 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.56 | 0.40 | 27.01 | 12.01 | 0.44 | 0.23 | 6.92 | 0.00 | 0.33 |
| 40 kg | 0.94 | 0.43 | 26.87 | 9.93 | 0.45 | 0.60 | 4.62 | 0.00 | 0.30 |
| 60 kg | 1.04 | 0.43 | 27.44 | 10.43 | 0.20 | 2.02 | 2.55 | 0.00 | 0.30 |
| 80 kg | 0.62 | 0.44 | 28.57 | 9.72 | 0.13 | 2.45 | 0.62 | 0.00 | 0.34 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 104 | 252 | 200 |
| 40 kg | 140 | 312 | 261 |
| 60 kg | 171 | 346 | 306 |
| 80 kg | 190 | 374 | 350 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 932 | 0.34 | 0.43 (207) | 0.49 (121) | 0.50 (264) | 0.50 (145) | 0.57 (195) |
| 40 kg | 1228 | 0.33 | 0.34 (315) | 0.43 (180) | 0.51 (243) | 0.59 (109) | 0.70 (381) |
| 60 kg | 1618 | 0.31 | 0.31 (413) | 0.36 (222) | 0.52 (250) | 0.60 (229) | 0.74 (504) |
| 80 kg | 2378 | 0.33 | 0.35 (94) | 0.46 (276) | 0.50 (1274) | 0.58 (530) | 0.68 (204) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.14 | 0.11 | 0.24 | 0.43 |
| long | 0.07 | 0.10 | 0.13 | 0.45 |
| sphere | 0.27 | 0.37 | 0.47 | 0.45 |
| cylinder | 0.16 | 0.08 | 0.32 | 0.24 |
| arch | 0.14 | 0.19 | 0.15 | 0.26 |
| dumbbell | 0.16 | 0.12 | 0.23 | 0.44 |
| t_shape | 0.08 | 0.14 | 0.18 | 0.41 |
| l_shape | 0.05 | 0.10 | 0.11 | 0.31 |
| u_channel | 0.06 | 0.17 | 0.24 | 0.41 |
| plus | 0.09 | 0.10 | 0.14 | 0.10 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.87 | 0.80 | 0.77 | 0.60 |
| B_left | 0.83 | 0.83 | 0.70 | 0.50 |
| C_backright | 0.67 | 0.73 | 0.60 | 0.40 |
| D_far_turn | 0.90 | 0.70 | 0.37 | 0.27 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 42% | 0% | 58% | 37% | 4% | 59% |  |  | 18% | 66% | 42% | 23% |
| 40 kg | 37% | 0% | 63% | 45% | 2% | 52% |  |  | 18% | 67% | 38% | 22% |
| 60 kg | 33% | 0% | 67% | 50% | 2% | 48% |  |  | 18% | 77% | 27% | 24% |
| 80 kg | 34% | 0% | 66% | 57% | 2% | 42% |  |  | 23% | 80% | 24% | 28% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 141 | 0.88 | 9% | 12% | 32% | 56% |
| 40 kg | 173 | 0.90 | 6% | 16% | 40% | 43% |
| 60 kg | 198 | 0.89 | 7% | 20% | 46% | 34% |
| 80 kg | 217 | 0.90 | 6% | 28% | 45% | 28% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 64% | 0.21 | 0.42 | 0.15 | 0.61 | 5 | 0 | 2 | 0 | 0 | 3 | 48 | 0.00 |  |
| 40 kg | 62% | 0.16 | 0.53 | 0.12 | 0.78 | 6 | 0 | 3 | 0 | 0 | 3 | 84 | 0.00 |  |
| 60 kg | 59% | 0.12 | 0.67 | 0.10 | 0.46 | 3 | 0 | 2 | 0 | 0 | 1 | 93 | 0.00 |  |
| 80 kg | 55% | 0.09 | 0.75 | 0.08 | 0.37 | 2 | 0 | 1 | 0 | 0 | 1 | 122 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.79 | 57% | 24% | 0.92 | 68% | 0.14 | 0 | 0 | 0 | 0 | 0 | 0 |
| long | 0.56 | 50% | 20% | 0.91 | 56% | 0.09 | 1 | 0 | 0 | 0 | 0 | 1 |
| sphere | 0.94 | 31% | 11% | 0.91 | 85% | 0.30 | 0 | 0 | 0 | 0 | 0 | 0 |
| cylinder | 0.44 | 32% | 13% | 0.91 | 64% | 0.09 | 2 | 0 | 1 | 0 | 0 | 1 |
| arch | 0.73 | 55% | 24% | 0.83 | 60% | 0.13 | 7 | 0 | 1 | 0 | 0 | 6 |
| dumbbell | 0.71 | 45% | 20% | 0.90 | 53% | 0.10 | 7 | 0 | 6 | 0 | 0 | 2 |
| t_shape | 0.60 | 52% | 21% | 0.92 | 52% | 0.08 | 8 | 0 | 4 | 0 | 0 | 4 |
| l_shape | 0.69 | 51% | 19% | 0.91 | 56% | 0.07 | 2 | 0 | 1 | 0 | 0 | 1 |
| u_channel | 0.62 | 50% | 21% | 0.92 | 54% | 0.09 | 6 | 0 | 3 | 0 | 0 | 3 |
| plus | 0.50 | 49% | 19% | 0.79 | 51% | 0.07 | 7 | 0 | 3 | 0 | 0 | 4 |
