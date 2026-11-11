# Pair evaluation: e6-exec-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start at their contacts; contact rule re-applied: first)

success = 10 cm / 6 deg held 1 s within 20 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.18 | 0.24 | 0.00 | 0.00 | 3.9 | 0.03 | 0.29 | 0.35 | 0.18 | 0.41 | 0.97 |
| 40 kg | 0.14 | 0.23 | 0.00 | 0.01 | 4.9 | 0.02 | 0.38 | 0.40 | 0.22 | 0.40 | 1.00 |
| 60 kg | 0.22 | 0.19 | 0.01 | 0.03 | 7.7 | 0.01 | 0.55 | 0.61 | 0.37 | 0.47 | 1.01 |
| 80 kg | 0.18 | 0.16 | 0.04 | 0.01 | 8.2 | 0.02 | 0.72 | 0.71 | 0.50 | 0.55 | 0.98 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube |  | 0.33 | 0.33 | 0.42 | 0.17 |
| long |  | 0.25 | 0.17 | 0.33 | 0.00 |
| sphere |  | 0.17 | 0.08 | 0.42 | 0.83 |
| cylinder |  | 0.08 | 0.17 | 0.17 | 0.25 |
| arch |  | 0.33 | 0.25 | 0.33 | 0.33 |
| dumbbell |  | 0.17 | 0.25 | 0.42 | 0.25 |
| t_shape |  | 0.08 | 0.00 | 0.00 | 0.00 |
| beam (unseen) |  | 0.17 | 0.08 | 0.08 | 0.00 |
| l_shape (unseen) |  | 0.08 | 0.17 | 0.08 | 0.17 |
| asym (unseen) |  | 0.00 | 0.00 | 0.00 | 0.00 |
| u_channel (unseen) |  | 0.25 | 0.17 | 0.25 | 0.08 |
| plus (unseen) |  | 0.25 | 0.00 | 0.08 | 0.08 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.18 | 0.82 | 0.00 | 0.00 | 0.00 | 0.17 | 0.00 |
| 40 kg | 0.14 | 0.85 | 0.01 | 0.00 | 0.00 | 0.10 | 0.00 |
| 60 kg | 0.22 | 0.75 | 0.03 | 0.00 | 0.00 | 0.01 | 0.00 |
| 80 kg | 0.18 | 0.76 | 0.06 | 0.00 | 0.00 | 0.00 | 0.00 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.12 | 0.90 | 0.99 | 0.00 | 1.00 | 0.12 | 0.90 | 0.99 | 0.00 |
| 40 kg | 1.00 | 0.12 | 0.89 | 1.00 | 0.00 | 1.00 | 0.14 | 0.86 | 0.99 | 0.00 |
| 60 kg | 1.00 | 0.15 | 0.86 | 1.00 | 0.00 | 1.00 | 0.15 | 0.82 | 1.00 | 0.00 |
| 80 kg | 1.00 | 0.14 | 0.86 | 1.00 | 0.00 | 1.00 | 0.15 | 0.81 | 1.00 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.02 | 0.02 | 1.00 | 0.02 | 0.03 |
| 40 kg | 1.00 | 0.02 | 0.03 | 1.00 | 0.02 | 0.06 |
| 60 kg | 1.00 | 0.02 | 0.06 | 1.00 | 0.02 | 0.09 |
| 80 kg | 1.00 | 0.02 | 0.09 | 1.00 | 0.02 | 0.11 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.74 | 0.73 | 0.72 |
| 40 kg | 0.77 | 0.73 | 0.67 |
| 60 kg | 0.77 | 0.73 | 0.52 |
| 80 kg | 0.77 | 0.70 | 0.36 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.00 | 0.58 | 7.89 | 0.00 | 0.00 | 0.00 | 4.07 | 0.00 | 0.19 |
| 40 kg | 0.01 | 0.60 | 8.33 | 0.00 | 0.00 | 0.00 | 3.35 | 0.00 | 0.20 |
| 60 kg | 0.01 | 0.62 | 7.93 | 0.00 | 0.00 | 0.00 | 2.10 | 0.00 | 0.21 |
| 80 kg | 0.00 | 0.59 | 7.61 | 0.00 | 0.00 | 0.00 | 1.03 | 0.00 | 0.20 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 79 | 222 | 140 |
| 40 kg | 116 | 283 | 202 |
| 60 kg | 153 | 328 | 264 |
| 80 kg | 183 | 356 | 321 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 250 | 0.42 | 0.47 (64) | 0.53 (36) | 0.50 (54) | 0.45 (36) | 0.65 (60) |
| 40 kg | 498 | 0.38 | 0.37 (105) | 0.52 (56) | 0.50 (114) | 0.50 (72) | 0.61 (152) |
| 60 kg | 803 | 0.35 | 0.35 (180) | 0.50 (117) | 0.49 (150) | 0.52 (191) | 0.63 (165) |
| 80 kg | 1042 | 0.35 | 0.35 (136) | 0.49 (167) | 0.49 (449) | 0.53 (180) | 0.56 (110) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.15 | 0.14 | 0.30 | 0.46 |
| long | 0.20 | 0.23 | 0.42 | 0.50 |
| sphere | 0.19 | 0.18 | 0.38 | 0.69 |
| cylinder | 0.24 | 0.32 | 0.40 | 0.40 |
| arch | 0.25 | 0.23 | 0.30 | 0.42 |
| dumbbell | 0.15 | 0.25 | 0.35 | 0.45 |
| t_shape | 0.19 | 0.22 | 0.34 | 0.55 |
| beam | 0.13 | 0.20 | 0.43 | 0.68 |
| l_shape | 0.11 | 0.16 | 0.24 | 0.53 |
| asym | 0.12 | 0.42 | 0.83 | 0.59 |
| u_channel | 0.24 | 0.23 | 0.32 | 0.46 |
| plus | 0.19 | 0.11 | 0.15 | 0.25 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| S_straight | 0.47 | 0.31 | 0.36 | 0.25 |
| S_side | 0.11 | 0.08 | 0.25 | 0.25 |
| S_moveturn | 0.08 | 0.11 | 0.11 | 0.11 |
| S_side_turn | 0.06 | 0.06 | 0.14 | 0.11 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 16% | 0% | 84% | 18% | 4% | 78% |  |  | 16% | 62% | 44% | 12% |
| 40 kg | 17% | 0% | 83% | 32% | 3% | 66% |  |  | 17% | 72% | 34% | 15% |
| 60 kg | 19% | 0% | 81% | 47% | 2% | 51% |  |  | 19% | 75% | 29% | 17% |
| 80 kg | 19% | 0% | 81% | 56% | 2% | 42% |  |  | 19% | 81% | 22% | 22% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 122 | 0.90 | 7% | 4% | 26% | 70% |
| 40 kg | 156 | 0.91 | 6% | 11% | 38% | 50% |
| 60 kg | 187 | 0.92 | 5% | 22% | 44% | 34% |
| 80 kg | 209 | 0.91 | 5% | 32% | 46% | 23% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 42% | 0.15 | 0.33 | 0.12 | 0.76 | 6 | 0 | 5 | 0 | 0 | 0 | 58 | 0.00 |  |
| 40 kg | 45% | 0.12 | 0.42 | 0.10 | 0.48 | 3 | 0 | 3 | 0 | 0 | 0 | 67 | 0.00 |  |
| 60 kg | 56% | 0.11 | 0.62 | 0.10 | 0.22 | 1 | 0 | 1 | 0 | 0 | 0 | 70 | 0.00 |  |
| 80 kg | 57% | 0.09 | 0.76 | 0.08 | 0.10 | 1 | 0 | 0 | 0 | 0 | 0 | 121 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.31 | 47% | 21% | 0.92 | 59% | 0.12 | 1 | 0 | 1 | 0 | 0 | 0 |
| long | 0.19 | 43% | 21% | 0.92 | 54% | 0.10 | 1 | 0 | 1 | 0 | 0 | 0 |
| sphere | 0.38 | 14% | 5% | 0.94 | 53% | 0.16 | 7 | 0 | 6 | 0 | 0 | 0 |
| cylinder | 0.17 | 20% | 6% | 0.92 | 51% | 0.09 | 3 | 0 | 3 | 0 | 0 | 0 |
| arch | 0.31 | 46% | 23% | 0.86 | 57% | 0.12 | 1 | 0 | 1 | 0 | 0 | 0 |
| dumbbell | 0.27 | 36% | 16% | 0.93 | 51% | 0.11 | 4 | 0 | 4 | 0 | 0 | 0 |
| t_shape | 0.02 | 40% | 19% | 0.93 | 46% | 0.07 | 3 | 0 | 3 | 0 | 0 | 0 |
| beam | 0.08 | 34% | 16% | 0.89 | 30% | 0.06 | 3 | 0 | 3 | 0 | 0 | 0 |
| l_shape | 0.12 | 39% | 17% | 0.90 | 52% | 0.09 | 2 | 0 | 2 | 0 | 0 | 0 |
| asym | 0.00 | 55% | 31% | 0.93 | 56% | 0.05 | 1 | 0 | 1 | 0 | 0 | 0 |
| u_channel | 0.19 | 40% | 15% | 0.95 | 46% | 0.11 | 4 | 0 | 4 | 0 | 0 | 0 |
| plus | 0.10 | 42% | 18% | 0.83 | 49% | 0.09 | 2 | 0 | 1 | 0 | 0 | 0 |
