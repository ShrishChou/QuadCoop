# Pair evaluation: fair-td-nocreep-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start at their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.56 | 0.60 | 0.26 | 0.10 | 21.1 | 0.01 | 0.49 | 0.46 | 0.23 | 0.37 | 1.06 |
| 40 kg | 0.53 | 0.44 | 0.24 | 0.15 | 22.9 | 0.01 | 0.57 | 0.56 | 0.33 | 0.45 | 1.05 |
| 60 kg | 0.44 | 0.32 | 0.29 | 0.22 | 32.8 | 0.02 | 0.63 | 0.62 | 0.41 | 0.52 | 1.03 |
| 80 kg | 0.22 | 0.16 | 0.35 | 0.31 | 31.5 | 0.01 | 0.70 | 0.72 | 0.51 | 0.59 | 1.03 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x+y + part 0 corner -x-y | 0.67 | 0.50 | 0.25 | 0.25 |
| long | part 0 -x seg 2/2 + part 0 corner -x-y | 0.50 | 0.42 | 0.50 | 0.08 |
| sphere | sector 135 + sector 225 | 0.92 | 0.67 | 0.33 | 0.42 |
| cylinder | part 0 corner -x-y + part 0 -x seg 2/2 | 0.42 | 0.25 | 0.25 | 0.08 |
| arch | part 3 -x + part 2 -x | 0.42 | 0.83 | 0.67 | 0.33 |
| dumbbell | part 0 -x + part 1 -x | 0.58 | 0.58 | 0.67 | 0.25 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.58 | 0.75 | 0.75 | 0.33 |
| beam (unseen) | part 0 -x seg 2/5 + part 0 -x seg 4/5 | 0.50 | 0.42 | 0.08 | 0.00 |
| l_shape (unseen) | part 1 -x + part 0 corner -x-y | 0.67 | 0.67 | 0.42 | 0.17 |
| asym (unseen) | part 1 -x + part 0 corner -x+y | 0.25 | 0.00 | 0.00 | 0.00 |
| u_channel (unseen) | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.67 | 0.83 | 0.50 | 0.17 |
| plus (unseen) | part 0 corner -x-y + part 0 corner -x+y | 0.50 | 0.50 | 0.83 | 0.58 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.56 | 0.07 | 0.36 | 0.01 | 0.00 | 0.05 | 8.27 |
| 40 kg | 0.53 | 0.05 | 0.38 | 0.03 | 0.00 | 0.01 | 7.42 |
| 60 kg | 0.44 | 0.05 | 0.51 | 0.00 | 0.00 | 0.00 | 6.71 |
| 80 kg | 0.22 | 0.11 | 0.66 | 0.01 | 0.00 | 0.01 | 5.50 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.23 | 0.71 | 0.86 | 0.00 | 1.00 | 0.22 | 0.73 | 0.88 | 0.00 |
| 40 kg | 1.00 | 0.21 | 0.74 | 0.91 | 0.00 | 1.00 | 0.21 | 0.74 | 0.92 | 0.00 |
| 60 kg | 1.00 | 0.22 | 0.72 | 0.94 | 0.00 | 1.00 | 0.22 | 0.71 | 0.95 | 0.00 |
| 80 kg | 1.00 | 0.20 | 0.74 | 0.96 | 0.00 | 1.00 | 0.20 | 0.73 | 0.97 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.94 | 1.26 | 0.08 | 0.96 | 1.21 | 0.08 |
| 40 kg | 0.95 | 1.09 | 0.10 | 0.97 | 0.94 | 0.12 |
| 60 kg | 0.97 | 1.06 | 0.13 | 0.97 | 0.87 | 0.14 |
| 80 kg | 0.93 | 0.56 | 0.14 | 0.95 | 0.70 | 0.15 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.54 | 0.58 | 0.30 |
| 40 kg | 0.62 | 0.61 | 0.27 |
| 60 kg | 0.62 | 0.61 | 0.26 |
| 80 kg | 0.64 | 0.63 | 0.24 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.52 | 0.48 | 21.84 | 8.27 | 0.16 | 0.02 | 3.82 | 0.00 | 0.28 |
| 40 kg | 0.42 | 0.49 | 18.15 | 7.42 | 0.19 | 0.01 | 3.85 | 0.00 | 0.28 |
| 60 kg | 0.57 | 0.49 | 17.55 | 6.71 | 0.19 | 0.15 | 1.53 | 0.00 | 0.30 |
| 80 kg | 0.46 | 0.53 | 18.80 | 5.50 | 0.20 | 1.28 | 0.76 | 0.00 | 0.26 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 124 | 296 | 215 |
| 40 kg | 157 | 361 | 258 |
| 60 kg | 187 | 382 | 295 |
| 80 kg | 208 | 395 | 329 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 1172 | 0.34 | 0.44 (191) | 0.53 (154) | 0.49 (278) | 0.47 (293) | 0.55 (257) |
| 40 kg | 1094 | 0.34 | 0.36 (228) | 0.49 (144) | 0.50 (209) | 0.50 (205) | 0.60 (308) |
| 60 kg | 1274 | 0.32 | 0.40 (290) | 0.41 (219) | 0.53 (276) | 0.55 (226) | 0.73 (263) |
| 80 kg | 1901 | 0.31 | 0.32 (131) | 0.38 (305) | 0.52 (1023) | 0.56 (327) | 0.52 (114) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.14 | 0.12 | 0.49 | 0.50 |
| long | 0.18 | 0.18 | 0.30 | 0.56 |
| sphere | 0.51 | 0.67 | 0.54 | 0.56 |
| cylinder | 0.23 | 0.40 | 0.46 | 0.38 |
| arch | 0.27 | 0.16 | 0.32 | 0.37 |
| dumbbell | 0.18 | 0.25 | 0.40 | 0.54 |
| t_shape | 0.13 | 0.29 | 0.23 | 0.58 |
| beam | 0.13 | 0.48 | 0.56 | 0.63 |
| l_shape | 0.20 | 0.36 | 0.34 | 0.47 |
| asym | 0.45 | 0.73 | 0.76 | 0.83 |
| u_channel | 0.25 | 0.27 | 0.29 | 0.46 |
| plus | 0.10 | 0.08 | 0.20 | 0.28 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.69 | 0.67 | 0.64 | 0.39 |
| B_left | 0.64 | 0.50 | 0.39 | 0.19 |
| C_backright | 0.42 | 0.47 | 0.42 | 0.19 |
| D_far_turn | 0.47 | 0.50 | 0.31 | 0.11 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 36% | 0% | 64% | 42% | 4% | 54% |  |  | 20% | 68% | 41% | 21% |
| 40 kg | 32% | 0% | 68% | 51% | 2% | 46% |  |  | 21% | 72% | 35% | 23% |
| 60 kg | 33% | 0% | 67% | 59% | 2% | 39% |  |  | 25% | 82% | 25% | 23% |
| 80 kg | 30% | 0% | 70% | 64% | 1% | 35% |  |  | 23% | 78% | 28% | 25% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 163 | 0.89 | 7% | 17% | 35% | 48% |
| 40 kg | 197 | 0.91 | 6% | 24% | 43% | 33% |
| 60 kg | 221 | 0.91 | 5% | 30% | 46% | 24% |
| 80 kg | 237 | 0.91 | 5% | 38% | 43% | 19% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 69% | 0.28 | 0.48 | 0.23 | 0.38 | 2 | 0 | 1 | 0 | 0 | 1 | 63 | 0.00 |  |
| 40 kg | 69% | 0.25 | 0.62 | 0.22 | 0.28 | 2 | 0 | 1 | 0 | 0 | 0 | 136 | 0.00 |  |
| 60 kg | 65% | 0.18 | 0.72 | 0.16 | 0.24 | 1 | 0 | 0 | 0 | 0 | 1 | 161 | 0.00 |  |
| 80 kg | 58% | 0.13 | 0.79 | 0.12 | 0.21 | 2 | 0 | 1 | 0 | 0 | 1 | 165 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.42 | 66% | 35% | 0.93 | 68% | 0.16 | 0 | 0 | 0 | 0 | 0 | 0 |
| long | 0.38 | 65% | 35% | 0.92 | 64% | 0.14 | 1 | 0 | 0 | 0 | 0 | 0 |
| sphere | 0.58 | 35% | 15% | 0.92 | 90% | 0.41 | 1 | 0 | 0 | 0 | 0 | 1 |
| cylinder | 0.25 | 37% | 17% | 0.88 | 74% | 0.17 | 1 | 0 | 0 | 0 | 0 | 1 |
| arch | 0.56 | 60% | 33% | 0.84 | 63% | 0.18 | 2 | 0 | 1 | 0 | 0 | 1 |
| dumbbell | 0.52 | 50% | 24% | 0.91 | 62% | 0.18 | 7 | 0 | 5 | 0 | 0 | 2 |
| t_shape | 0.60 | 61% | 30% | 0.92 | 63% | 0.15 | 1 | 0 | 0 | 0 | 0 | 1 |
| beam | 0.25 | 39% | 24% | 0.86 | 44% | 0.15 | 3 | 0 | 2 | 0 | 0 | 1 |
| l_shape | 0.48 | 57% | 26% | 0.92 | 61% | 0.15 | 1 | 0 | 0 | 0 | 0 | 1 |
| asym | 0.06 | 68% | 41% | 0.92 | 67% | 0.12 | 0 | 0 | 0 | 0 | 0 | 0 |
| u_channel | 0.54 | 52% | 20% | 0.92 | 62% | 0.20 | 2 | 0 | 1 | 0 | 0 | 2 |
| plus | 0.60 | 57% | 29% | 0.92 | 68% | 0.19 | 0 | 0 | 0 | 0 | 0 | 0 |
