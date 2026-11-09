# Pair evaluation: env-base-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 1 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.73 | 0.69 | 0.00 | 0.04 | 30.9 | 0.01 | 0.42 | 0.38 | 0.10 | 0.17 | 1.08 |
| 40 kg | 0.77 | 0.69 | 0.00 | 0.00 | 30.8 | 0.00 | 0.48 | 0.40 | 0.13 | 0.19 | 1.09 |
| 60 kg | 0.56 | 0.50 | 0.02 | 0.02 | 41.1 | 0.01 | 0.64 | 0.43 | 0.24 | 0.30 | 1.07 |
| 80 kg | 0.31 | 0.27 | 0.17 | 0.02 | 29.9 | 0.00 | 0.71 | 0.56 | 0.41 | 0.50 | 1.08 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x+y + part 0 corner -x-y | 0.75 | 0.75 | 0.75 | 0.25 |
| long | part 0 -x seg 2/2 + part 0 corner -x-y | 1.00 | 1.00 | 0.75 | 0.25 |
| sphere | sector 225 + sector 135 | 0.75 | 1.00 | 0.75 | 1.00 |
| cylinder | part 0 -x seg 2/2 + part 0 corner -x-y | 0.50 | 0.75 | 0.25 | 0.25 |
| arch | part 2 -x + part 3 -x | 1.00 | 1.00 | 0.75 | 0.50 |
| dumbbell | part 0 -x + part 1 -x | 0.75 | 0.75 | 0.50 | 0.25 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.50 | 0.50 | 0.50 | 0.50 |
| beam (unseen) | part 0 -x seg 2/5 + part 0 -x seg 4/5 | 0.50 | 0.25 | 0.00 | 0.00 |
| l_shape (unseen) | part 0 corner -x-y + part 1 -x | 0.50 | 0.75 | 0.75 | 0.25 |
| asym (unseen) | part 0 corner -x+y + part 1 -x | 0.75 | 0.50 | 0.25 | 0.00 |
| u_channel (unseen) | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 1.00 | 1.00 | 0.75 | 0.50 |
| plus (unseen) | part 1 corner -x+y + part 1 corner -x-y | 0.75 | 1.00 | 0.75 | 0.00 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.73 | 0.23 | 0.04 | 0.00 | 0.00 | 0.02 | 10.29 |
| 40 kg | 0.77 | 0.23 | 0.00 | 0.00 | 0.00 | 0.02 | 9.08 |
| 60 kg | 0.56 | 0.40 | 0.04 | 0.00 | 0.00 | 0.00 | 9.12 |
| 80 kg | 0.31 | 0.50 | 0.19 | 0.00 | 0.00 | 0.00 | 8.44 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.26 | 0.72 | 0.87 | 0.00 | 1.00 | 0.26 | 0.70 | 0.89 | 0.00 |
| 40 kg | 1.00 | 0.20 | 0.79 | 0.93 | 0.00 | 1.00 | 0.25 | 0.72 | 0.91 | 0.00 |
| 60 kg | 1.00 | 0.21 | 0.77 | 0.94 | 0.00 | 1.00 | 0.25 | 0.69 | 0.94 | 0.00 |
| 80 kg | 1.00 | 0.24 | 0.71 | 0.95 | 0.00 | 1.00 | 0.27 | 0.67 | 0.92 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.82 | 2.00 | 0.06 | 0.77 | 2.17 | 0.07 |
| 40 kg | 0.80 | 1.90 | 0.07 | 0.76 | 1.93 | 0.10 |
| 60 kg | 0.81 | 1.64 | 0.08 | 0.76 | 1.80 | 0.12 |
| 80 kg | 0.82 | 2.07 | 0.12 | 0.76 | 2.73 | 0.16 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.53 | 0.53 | 0.29 |
| 40 kg | 0.62 | 0.54 | 0.29 |
| 60 kg | 0.65 | 0.55 | 0.31 |
| 80 kg | 0.64 | 0.54 | 0.24 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.65 | 0.43 | 28.38 | 10.29 | 0.38 | 0.02 | 8.85 | 0.00 | 0.28 |
| 40 kg | 0.03 | 0.47 | 26.08 | 9.08 | 0.65 | 0.33 | 6.31 | 0.00 | 0.21 |
| 60 kg | 0.56 | 0.47 | 29.70 | 9.12 | 0.06 | 1.08 | 4.88 | 0.00 | 0.25 |
| 80 kg | 0.89 | 0.48 | 26.03 | 8.44 | 0.27 | 2.44 | 0.40 | 0.00 | 0.31 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 108 | 256 | 183 |
| 40 kg | 145 | 315 | 254 |
| 60 kg | 170 | 348 | 300 |
| 80 kg | 191 | 369 | 332 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 524 | 0.34 | 0.40 (86) | 0.50 (103) | 0.52 (168) | 0.53 (62) | 0.55 (105) |
| 40 kg | 547 | 0.34 | 0.39 (203) | 0.47 (99) | 0.50 (66) | 0.52 (50) | 0.69 (129) |
| 60 kg | 804 | 0.34 | 0.30 (92) | 0.49 (131) | 0.46 (154) | 0.52 (133) | 0.67 (294) |
| 80 kg | 900 | 0.34 | 0.33 (8) | 0.41 (132) | 0.51 (420) | 0.50 (208) | 0.71 (132) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.08 | 0.06 | 0.44 | 0.44 |
| long | 0.13 | 0.09 | 0.23 | 0.35 |
| sphere | 0.28 | 0.36 | 0.42 | 0.54 |
| cylinder | 0.08 | 0.08 | 0.25 | 0.44 |
| arch | 0.09 | 0.20 | 0.24 | 0.16 |
| dumbbell | 0.04 | 0.25 | 0.11 | 0.30 |
| t_shape | 0.11 | 0.05 | 0.23 | 0.52 |
| beam | 0.02 | 0.05 | 0.25 | 0.60 |
| l_shape | 0.11 | 0.10 | 0.23 | 0.44 |
| asym | 0.12 | 0.05 | 0.26 | 0.57 |
| u_channel | 0.10 | 0.11 | 0.14 | 0.25 |
| plus | 0.05 | 0.14 | 0.07 | 0.31 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.92 | 0.83 | 0.58 | 0.42 |
| B_left | 0.58 | 0.75 | 0.58 | 0.25 |
| C_backright | 0.83 | 0.83 | 0.50 | 0.50 |
| D_far_turn | 0.58 | 0.67 | 0.58 | 0.08 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 37% | 0% | 63% | 39% | 4% | 57% |  |  | 19% | 59% | 48% | 25% |
| 40 kg | 31% | 0% | 69% | 47% | 3% | 51% |  |  | 16% | 63% | 40% | 24% |
| 60 kg | 30% | 0% | 70% | 48% | 2% | 50% |  |  | 18% | 81% | 22% | 25% |
| 80 kg | 35% | 0% | 65% | 59% | 2% | 39% |  |  | 23% | 87% | 17% | 26% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 143 | 0.89 | 9% | 15% | 32% | 53% |
| 40 kg | 173 | 0.90 | 8% | 20% | 41% | 39% |
| 60 kg | 197 | 0.90 | 7% | 21% | 45% | 34% |
| 80 kg | 216 | 0.89 | 7% | 31% | 44% | 26% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 62% | 0.19 | 0.40 | 0.14 | 0.73 | 5 | 0 | 4 | 0 | 0 | 1 | 55 | 0.00 |  |
| 40 kg | 62% | 0.15 | 0.59 | 0.13 | 0.44 | 3 | 0 | 2 | 0 | 0 | 1 | 128 | 0.00 |  |
| 60 kg | 53% | 0.11 | 0.70 | 0.09 | 0.52 | 4 | 0 | 4 | 0 | 0 | 1 | 75 | 0.00 |  |
| 80 kg | 54% | 0.09 | 0.77 | 0.08 | 0.35 | 1 | 0 | 0 | 0 | 0 | 1 | 167 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.62 | 61% | 29% | 0.92 | 72% | 0.14 | 0 | 0 | 0 | 0 | 0 | 0 |
| long | 0.75 | 58% | 27% | 0.90 | 64% | 0.12 | 0 | 0 | 0 | 0 | 0 | 0 |
| sphere | 0.88 | 24% | 9% | 0.92 | 78% | 0.28 | 4 | 0 | 4 | 0 | 0 | 0 |
| cylinder | 0.44 | 31% | 10% | 0.90 | 62% | 0.10 | 6 | 0 | 6 | 0 | 0 | 0 |
| arch | 0.81 | 57% | 26% | 0.81 | 66% | 0.14 | 2 | 0 | 0 | 0 | 0 | 2 |
| dumbbell | 0.56 | 42% | 17% | 0.88 | 49% | 0.08 | 8 | 0 | 7 | 0 | 0 | 2 |
| t_shape | 0.50 | 58% | 29% | 0.91 | 57% | 0.06 | 4 | 0 | 3 | 0 | 0 | 1 |
| beam | 0.19 | 26% | 14% | 0.81 | 19% | 0.04 | 11 | 0 | 8 | 0 | 0 | 3 |
| l_shape | 0.56 | 60% | 29% | 0.92 | 61% | 0.09 | 1 | 0 | 0 | 0 | 0 | 1 |
| asym | 0.38 | 58% | 29% | 0.91 | 51% | 0.06 | 1 | 0 | 1 | 0 | 0 | 0 |
| u_channel | 0.81 | 50% | 17% | 0.92 | 54% | 0.11 | 3 | 0 | 1 | 0 | 0 | 2 |
| plus | 0.62 | 54% | 28% | 0.92 | 62% | 0.09 | 0 | 0 | 0 | 0 | 0 | 0 |
