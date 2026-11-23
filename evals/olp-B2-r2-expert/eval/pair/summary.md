# Pair evaluation: olp-B2-r2-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto); planner settings changed: fail_mem=1,fail_act=2

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.78 | 0.74 | 0.00 | 0.00 | 28.8 | 0.01 | 0.38 | 0.35 | 0.11 | 0.22 | 1.04 |
| 40 kg | 0.73 | 0.63 | 0.00 | 0.01 | 30.5 | 0.01 | 0.48 | 0.38 | 0.14 | 0.23 | 1.09 |
| 60 kg | 0.53 | 0.38 | 0.02 | 0.03 | 38.6 | 0.01 | 0.55 | 0.41 | 0.19 | 0.27 | 1.02 |
| 80 kg | 0.40 | 0.29 | 0.09 | 0.02 | 41.7 | 0.01 | 0.66 | 0.52 | 0.33 | 0.41 | 1.00 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 -x end - + part 0 corner -x+y | 1.00 | 0.92 | 0.67 | 0.42 |
| long | part 0 -x seg 2/2 + part 0 corner -x-y | 0.75 | 0.67 | 0.33 | 0.17 |
| sphere | sector 225 + sector 135 | 1.00 | 0.92 | 0.92 | 0.75 |
| cylinder | part 0 corner -x-y + part 0 -x seg 2/2 | 0.50 | 0.25 | 0.42 | 0.17 |
| arch | part 2 -x + part 3 -x | 0.75 | 0.75 | 0.67 | 0.58 |
| dumbbell | part 0 -x + part 1 -x | 0.67 | 0.75 | 0.42 | 0.50 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.75 | 0.75 | 0.25 | 0.42 |
| l_shape (unseen) | part 0 corner -x-y + part 1 -x | 0.75 | 0.92 | 0.67 | 0.33 |
| u_channel (unseen) | part 0 -x seg 1/3 + part 0 -x seg 3/3 | 0.92 | 0.75 | 0.58 | 0.58 |
| plus (unseen) | part 0 -x end - + part 0 -x end + | 0.67 | 0.67 | 0.42 | 0.08 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.78 | 0.23 | 0.00 | 0.00 | 0.00 | 0.03 | 11.97 |
| 40 kg | 0.73 | 0.26 | 0.01 | 0.00 | 0.00 | 0.00 | 10.28 |
| 60 kg | 0.53 | 0.42 | 0.04 | 0.00 | 0.00 | 0.00 | 11.02 |
| 80 kg | 0.40 | 0.49 | 0.11 | 0.00 | 0.00 | 0.02 | 10.03 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.29 | 0.66 | 0.86 | 0.00 | 1.00 | 0.30 | 0.63 | 0.86 | 0.00 |
| 40 kg | 1.00 | 0.25 | 0.72 | 0.89 | 0.00 | 1.00 | 0.26 | 0.70 | 0.87 | 0.00 |
| 60 kg | 1.00 | 0.26 | 0.72 | 0.92 | 0.00 | 1.00 | 0.23 | 0.72 | 0.92 | 0.00 |
| 80 kg | 1.00 | 0.24 | 0.72 | 0.95 | 0.00 | 1.00 | 0.25 | 0.66 | 0.93 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.77 | 1.90 | 0.06 | 0.74 | 1.77 | 0.06 |
| 40 kg | 0.76 | 1.81 | 0.08 | 0.74 | 1.93 | 0.09 |
| 60 kg | 0.75 | 1.76 | 0.09 | 0.77 | 2.07 | 0.10 |
| 80 kg | 0.77 | 1.97 | 0.10 | 0.78 | 2.29 | 0.14 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.48 | 0.47 | 0.31 |
| 40 kg | 0.58 | 0.52 | 0.30 |
| 60 kg | 0.59 | 0.55 | 0.29 |
| 80 kg | 0.62 | 0.53 | 0.26 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.10 | 0.37 | 27.95 | 11.97 | 0.25 | 0.16 | 6.62 | 0.00 | 0.33 |
| 40 kg | 0.73 | 0.44 | 25.60 | 10.28 | 0.55 | 0.57 | 5.66 | 0.00 | 0.29 |
| 60 kg | 1.26 | 0.42 | 28.39 | 11.02 | 0.52 | 1.76 | 1.80 | 0.00 | 0.30 |
| 80 kg | 0.45 | 0.45 | 28.02 | 10.03 | 0.62 | 1.79 | 1.25 | 0.00 | 0.32 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 106 | 256 | 203 |
| 40 kg | 140 | 308 | 255 |
| 60 kg | 169 | 344 | 304 |
| 80 kg | 193 | 377 | 347 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 926 | 0.36 | 0.46 (244) | 0.52 (149) | 0.52 (161) | 0.50 (223) | 0.61 (149) |
| 40 kg | 1265 | 0.36 | 0.42 (406) | 0.44 (118) | 0.51 (222) | 0.54 (121) | 0.65 (398) |
| 60 kg | 1656 | 0.29 | 0.27 (337) | 0.33 (237) | 0.52 (286) | 0.56 (218) | 0.77 (578) |
| 80 kg | 2159 | 0.34 | 0.45 (178) | 0.47 (229) | 0.50 (1090) | 0.58 (467) | 0.67 (195) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.11 | 0.10 | 0.19 | 0.32 |
| long | 0.09 | 0.07 | 0.11 | 0.39 |
| sphere | 0.23 | 0.42 | 0.48 | 0.42 |
| cylinder | 0.10 | 0.10 | 0.30 | 0.26 |
| arch | 0.08 | 0.07 | 0.15 | 0.27 |
| dumbbell | 0.20 | 0.19 | 0.19 | 0.41 |
| t_shape | 0.08 | 0.15 | 0.14 | 0.39 |
| l_shape | 0.03 | 0.11 | 0.12 | 0.24 |
| u_channel | 0.10 | 0.15 | 0.15 | 0.50 |
| plus | 0.07 | 0.07 | 0.10 | 0.10 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.87 | 0.77 | 0.77 | 0.57 |
| B_left | 0.80 | 0.60 | 0.60 | 0.47 |
| C_backright | 0.57 | 0.90 | 0.50 | 0.37 |
| D_far_turn | 0.87 | 0.67 | 0.27 | 0.20 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 42% | 0% | 58% | 38% | 4% | 58% |  |  | 18% | 66% | 42% | 24% |
| 40 kg | 36% | 0% | 64% | 46% | 2% | 52% |  |  | 18% | 65% | 41% | 24% |
| 60 kg | 33% | 0% | 67% | 49% | 2% | 49% |  |  | 17% | 76% | 28% | 23% |
| 80 kg | 34% | 0% | 66% | 57% | 2% | 41% |  |  | 22% | 81% | 24% | 26% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 142 | 0.88 | 9% | 12% | 31% | 57% |
| 40 kg | 172 | 0.90 | 7% | 17% | 40% | 43% |
| 60 kg | 198 | 0.90 | 6% | 19% | 45% | 37% |
| 80 kg | 219 | 0.91 | 5% | 27% | 45% | 28% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 63% | 0.20 | 0.40 | 0.14 | 0.73 | 7 | 0 | 5 | 0 | 0 | 2 | 65 | 0.00 |  |
| 40 kg | 61% | 0.16 | 0.54 | 0.13 | 0.61 | 6 | 0 | 4 | 0 | 0 | 2 | 96 | 0.00 |  |
| 60 kg | 56% | 0.11 | 0.67 | 0.09 | 0.59 | 5 | 0 | 3 | 0 | 0 | 2 | 94 | 0.00 |  |
| 80 kg | 55% | 0.09 | 0.74 | 0.08 | 0.35 | 2 | 0 | 1 | 0 | 0 | 1 | 131 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.75 | 56% | 23% | 0.92 | 68% | 0.15 | 1 | 0 | 1 | 0 | 0 | 0 |
| long | 0.48 | 49% | 17% | 0.92 | 53% | 0.08 | 4 | 0 | 2 | 0 | 0 | 1 |
| sphere | 0.90 | 31% | 11% | 0.91 | 83% | 0.28 | 1 | 0 | 1 | 0 | 0 | 0 |
| cylinder | 0.33 | 30% | 12% | 0.91 | 59% | 0.07 | 7 | 0 | 6 | 0 | 0 | 1 |
| arch | 0.69 | 57% | 26% | 0.83 | 58% | 0.11 | 7 | 0 | 2 | 0 | 0 | 5 |
| dumbbell | 0.58 | 44% | 20% | 0.90 | 51% | 0.10 | 9 | 0 | 9 | 0 | 0 | 1 |
| t_shape | 0.54 | 52% | 19% | 0.92 | 51% | 0.08 | 6 | 0 | 3 | 0 | 0 | 3 |
| l_shape | 0.67 | 50% | 18% | 0.92 | 56% | 0.08 | 3 | 0 | 2 | 0 | 0 | 1 |
| u_channel | 0.71 | 52% | 20% | 0.92 | 54% | 0.10 | 5 | 0 | 1 | 0 | 0 | 4 |
| plus | 0.46 | 54% | 20% | 0.83 | 52% | 0.07 | 5 | 0 | 2 | 0 | 0 | 3 |
