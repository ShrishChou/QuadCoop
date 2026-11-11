# Pair evaluation: e6r-exec-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start at their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 20 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.51 | 0.60 | 0.00 | 0.00 | 10.4 | 0.01 | 0.41 | 0.45 | 0.20 | 0.33 | 1.00 |
| 40 kg | 0.56 | 0.50 | 0.01 | 0.01 | 9.0 | 0.01 | 0.52 | 0.59 | 0.33 | 0.44 | 1.03 |
| 60 kg | 0.48 | 0.38 | 0.01 | 0.02 | 10.7 | 0.01 | 0.62 | 0.68 | 0.42 | 0.50 | 1.03 |
| 80 kg | 0.23 | 0.22 | 0.06 | 0.05 | 10.2 | 0.02 | 0.72 | 0.75 | 0.54 | 0.59 | 1.00 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube |  | 0.58 | 0.83 | 0.58 | 0.17 |
| long |  | 0.67 | 0.67 | 0.50 | 0.08 |
| sphere |  | 0.75 | 0.75 | 0.83 | 0.92 |
| cylinder |  | 0.25 | 0.17 | 0.25 | 0.25 |
| arch |  | 0.67 | 0.92 | 0.58 | 0.42 |
| dumbbell |  | 0.58 | 0.50 | 0.42 | 0.33 |
| t_shape |  | 0.42 | 0.33 | 0.50 | 0.00 |
| beam (unseen) |  | 0.58 | 0.33 | 0.17 | 0.00 |
| l_shape (unseen) |  | 0.42 | 0.67 | 0.42 | 0.00 |
| asym (unseen) |  | 0.25 | 0.25 | 0.00 | 0.00 |
| u_channel (unseen) |  | 0.67 | 0.92 | 0.83 | 0.17 |
| plus (unseen) |  | 0.25 | 0.33 | 0.67 | 0.42 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.51 | 0.49 | 0.00 | 0.00 | 0.00 | 0.04 | 4.18 |
| 40 kg | 0.56 | 0.43 | 0.01 | 0.00 | 0.00 | 0.02 | 3.25 |
| 60 kg | 0.48 | 0.49 | 0.03 | 0.00 | 0.00 | 0.01 | 2.75 |
| 80 kg | 0.23 | 0.66 | 0.11 | 0.00 | 0.00 | 0.00 | 1.90 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.23 | 0.73 | 0.84 | 0.00 | 1.00 | 0.24 | 0.72 | 0.86 | 0.00 |
| 40 kg | 1.00 | 0.19 | 0.80 | 0.91 | 0.00 | 1.00 | 0.20 | 0.76 | 0.90 | 0.00 |
| 60 kg | 1.00 | 0.19 | 0.79 | 0.93 | 0.00 | 1.00 | 0.19 | 0.77 | 0.94 | 0.00 |
| 80 kg | 1.00 | 0.17 | 0.79 | 0.96 | 0.00 | 1.00 | 0.19 | 0.76 | 0.97 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.94 | 1.24 | 0.06 | 0.94 | 1.22 | 0.06 |
| 40 kg | 0.95 | 0.74 | 0.06 | 0.95 | 0.73 | 0.08 |
| 60 kg | 0.96 | 0.73 | 0.07 | 0.96 | 0.51 | 0.11 |
| 80 kg | 0.96 | 0.33 | 0.10 | 0.96 | 0.30 | 0.11 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.59 | 0.59 | 0.35 |
| 40 kg | 0.68 | 0.66 | 0.31 |
| 60 kg | 0.68 | 0.68 | 0.27 |
| 80 kg | 0.71 | 0.67 | 0.24 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.38 | 0.52 | 11.07 | 4.18 | 0.06 | 0.19 | 0.64 | 0.00 | 0.26 |
| 40 kg | 0.19 | 0.57 | 9.07 | 3.25 | 0.00 | 0.26 | 0.88 | 0.00 | 0.23 |
| 60 kg | 0.27 | 0.58 | 8.67 | 2.75 | 0.01 | 0.15 | 0.47 | 0.00 | 0.24 |
| 80 kg | 0.08 | 0.56 | 8.04 | 1.90 | 0.13 | 0.22 | 0.34 | 0.00 | 0.23 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 101 | 254 | 187 |
| 40 kg | 126 | 303 | 237 |
| 60 kg | 164 | 347 | 297 |
| 80 kg | 188 | 363 | 327 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 464 | 0.38 | 0.40 (99) | 0.51 (51) | 0.48 (105) | 0.50 (86) | 0.57 (124) |
| 40 kg | 594 | 0.37 | 0.37 (152) | 0.50 (75) | 0.52 (111) | 0.53 (90) | 0.63 (166) |
| 60 kg | 867 | 0.34 | 0.31 (168) | 0.48 (153) | 0.50 (169) | 0.55 (208) | 0.66 (168) |
| 80 kg | 914 | 0.35 | 0.49 (56) | 0.48 (175) | 0.50 (472) | 0.49 (159) | 0.63 (53) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.20 | 0.33 | 0.42 | 0.49 |
| long | 0.29 | 0.31 | 0.41 | 0.61 |
| sphere | 0.26 | 0.42 | 0.46 | 0.59 |
| cylinder | 0.15 | 0.40 | 0.38 | 0.54 |
| arch | 0.24 | 0.44 | 0.48 | 0.48 |
| dumbbell | 0.12 | 0.30 | 0.40 | 0.47 |
| t_shape | 0.25 | 0.32 | 0.32 | 0.65 |
| beam | 0.15 | 0.25 | 0.49 | 0.64 |
| l_shape | 0.18 | 0.20 | 0.27 | 0.65 |
| asym | 0.21 | 0.41 | 0.85 | 0.50 |
| u_channel | 0.26 | 0.36 | 0.40 | 0.53 |
| plus | 0.11 | 0.23 | 0.20 | 0.31 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| S_straight | 0.67 | 0.64 | 0.61 | 0.42 |
| S_side | 0.47 | 0.50 | 0.56 | 0.25 |
| S_moveturn | 0.44 | 0.64 | 0.39 | 0.11 |
| S_side_turn | 0.44 | 0.44 | 0.36 | 0.14 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 34% | 0% | 66% | 34% | 4% | 62% |  |  | 13% | 64% | 39% | 17% |
| 40 kg | 27% | 0% | 73% | 44% | 3% | 53% |  |  | 14% | 69% | 33% | 17% |
| 60 kg | 27% | 0% | 73% | 53% | 2% | 45% |  |  | 17% | 73% | 29% | 19% |
| 80 kg | 25% | 0% | 75% | 59% | 2% | 39% |  |  | 20% | 85% | 19% | 23% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 140 | 0.90 | 7% | 11% | 32% | 57% |
| 40 kg | 165 | 0.91 | 6% | 18% | 41% | 41% |
| 60 kg | 196 | 0.92 | 5% | 25% | 45% | 30% |
| 80 kg | 214 | 0.91 | 5% | 32% | 46% | 22% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 61% | 0.19 | 0.38 | 0.14 | 0.35 | 2 | 0 | 1 | 0 | 0 | 0 | 66 | 0.00 |  |
| 40 kg | 63% | 0.18 | 0.59 | 0.15 | 0.24 | 1 | 0 | 1 | 0 | 0 | 0 | 76 | 0.00 |  |
| 60 kg | 65% | 0.13 | 0.72 | 0.11 | 0.14 | 1 | 0 | 0 | 0 | 0 | 0 | 109 | 0.00 |  |
| 80 kg | 59% | 0.09 | 0.78 | 0.08 | 0.08 | 0 | 0 | 0 | 0 | 0 | 0 | 166 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.54 | 58% | 29% | 0.92 | 74% | 0.16 | 0 | 0 | 0 | 0 | 0 | 0 |
| long | 0.48 | 54% | 26% | 0.93 | 66% | 0.12 | 0 | 0 | 0 | 0 | 0 | 0 |
| sphere | 0.81 | 19% | 6% | 0.93 | 75% | 0.21 | 1 | 0 | 1 | 0 | 0 | 0 |
| cylinder | 0.23 | 29% | 9% | 0.92 | 61% | 0.09 | 2 | 0 | 2 | 0 | 0 | 0 |
| arch | 0.65 | 55% | 27% | 0.84 | 70% | 0.16 | 1 | 0 | 1 | 0 | 0 | 0 |
| dumbbell | 0.46 | 42% | 19% | 0.92 | 58% | 0.13 | 3 | 0 | 3 | 0 | 0 | 0 |
| t_shape | 0.31 | 53% | 23% | 0.92 | 58% | 0.09 | 1 | 0 | 0 | 0 | 0 | 0 |
| beam | 0.27 | 36% | 17% | 0.86 | 32% | 0.07 | 2 | 0 | 1 | 0 | 0 | 1 |
| l_shape | 0.38 | 54% | 24% | 0.91 | 62% | 0.10 | 0 | 0 | 0 | 0 | 0 | 0 |
| asym | 0.12 | 63% | 37% | 0.93 | 62% | 0.06 | 0 | 0 | 0 | 0 | 0 | 0 |
| u_channel | 0.65 | 52% | 18% | 0.94 | 63% | 0.15 | 1 | 0 | 0 | 0 | 0 | 1 |
| plus | 0.42 | 52% | 22% | 0.89 | 60% | 0.09 | 0 | 0 | 0 | 0 | 0 | 0 |
