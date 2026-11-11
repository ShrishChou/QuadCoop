# Pair evaluation: e6-endsA-expert

policy: Stage 4 contact policy logs/marl2/ends_a/model_16900.pt (robots start at their contacts; contact rule re-applied: first)

success = 10 cm / 6 deg held 1 s within 20 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.15 | 0.22 | 0.00 | 0.00 | 3.9 | 0.03 | 0.30 | 0.30 | 0.17 | 0.39 | 0.95 |
| 40 kg | 0.17 | 0.19 | 0.00 | 0.01 | 4.9 | 0.03 | 0.41 | 0.36 | 0.23 | 0.42 | 0.98 |
| 60 kg | 0.18 | 0.16 | 0.02 | 0.03 | 6.2 | 0.03 | 0.59 | 0.53 | 0.36 | 0.48 | 1.00 |
| 80 kg | 0.19 | 0.16 | 0.01 | 0.01 | 8.3 | 0.02 | 0.72 | 0.68 | 0.48 | 0.54 | 0.99 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube |  | 0.50 | 0.33 | 0.25 | 0.33 |
| long |  | 0.08 | 0.17 | 0.08 | 0.08 |
| sphere |  | 0.17 | 0.50 | 0.75 | 0.92 |
| cylinder |  | 0.17 | 0.08 | 0.17 | 0.17 |
| arch |  | 0.33 | 0.25 | 0.17 | 0.33 |
| dumbbell |  | 0.08 | 0.08 | 0.42 | 0.25 |
| t_shape |  | 0.08 | 0.00 | 0.08 | 0.00 |
| beam (unseen) |  | 0.00 | 0.17 | 0.00 | 0.00 |
| l_shape (unseen) |  | 0.08 | 0.17 | 0.08 | 0.08 |
| asym (unseen) |  | 0.00 | 0.08 | 0.00 | 0.00 |
| u_channel (unseen) |  | 0.17 | 0.17 | 0.08 | 0.08 |
| plus (unseen) |  | 0.17 | 0.00 | 0.08 | 0.08 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.15 | 0.85 | 0.00 | 0.00 | 0.00 | 0.22 | 0.00 |
| 40 kg | 0.17 | 0.83 | 0.01 | 0.00 | 0.00 | 0.12 | 0.00 |
| 60 kg | 0.18 | 0.76 | 0.06 | 0.00 | 0.00 | 0.02 | 0.00 |
| 80 kg | 0.19 | 0.78 | 0.03 | 0.00 | 0.00 | 0.01 | 0.00 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.11 | 0.92 | 1.00 | 0.00 | 1.00 | 0.15 | 0.84 | 0.98 | 0.00 |
| 40 kg | 1.00 | 0.12 | 0.90 | 1.00 | 0.00 | 1.00 | 0.15 | 0.85 | 0.98 | 0.00 |
| 60 kg | 1.00 | 0.13 | 0.87 | 0.99 | 0.00 | 1.00 | 0.16 | 0.80 | 1.00 | 0.00 |
| 80 kg | 1.00 | 0.14 | 0.85 | 1.00 | 0.00 | 1.00 | 0.16 | 0.78 | 1.00 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.02 | 0.02 | 1.00 | 0.02 | 0.03 |
| 40 kg | 1.00 | 0.02 | 0.04 | 1.00 | 0.02 | 0.06 |
| 60 kg | 1.00 | 0.02 | 0.07 | 1.00 | 0.02 | 0.10 |
| 80 kg | 1.00 | 0.02 | 0.10 | 1.00 | 0.02 | 0.13 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.82 | 0.65 | 0.76 |
| 40 kg | 0.82 | 0.66 | 0.69 |
| 60 kg | 0.80 | 0.68 | 0.55 |
| 80 kg | 0.78 | 0.68 | 0.39 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.00 | 0.58 | 7.98 | 0.00 | 0.00 | 0.00 | 3.38 | 0.00 | 0.20 |
| 40 kg | 0.00 | 0.58 | 8.28 | 0.00 | 0.00 | 0.00 | 2.94 | 0.00 | 0.19 |
| 60 kg | 0.00 | 0.60 | 7.90 | 0.00 | 0.00 | 0.00 | 1.76 | 0.00 | 0.22 |
| 80 kg | 0.02 | 0.59 | 7.62 | 0.00 | 0.00 | 0.00 | 0.75 | 0.00 | 0.22 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 81 | 219 | 140 |
| 40 kg | 117 | 285 | 206 |
| 60 kg | 154 | 332 | 267 |
| 80 kg | 182 | 359 | 317 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 252 | 0.42 | 0.43 (53) | 0.59 (37) | 0.52 (53) | 0.51 (36) | 0.61 (74) |
| 40 kg | 470 | 0.37 | 0.34 (95) | 0.51 (50) | 0.51 (103) | 0.50 (69) | 0.60 (153) |
| 60 kg | 788 | 0.35 | 0.37 (169) | 0.45 (121) | 0.51 (150) | 0.51 (164) | 0.64 (183) |
| 80 kg | 1049 | 0.34 | 0.36 (139) | 0.46 (177) | 0.50 (402) | 0.51 (193) | 0.63 (138) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.32 | 0.26 | 0.23 | 0.38 |
| long | 0.13 | 0.17 | 0.30 | 0.51 |
| sphere | 0.18 | 0.40 | 0.60 | 0.70 |
| cylinder | 0.19 | 0.18 | 0.30 | 0.30 |
| arch | 0.25 | 0.23 | 0.25 | 0.44 |
| dumbbell | 0.10 | 0.12 | 0.36 | 0.42 |
| t_shape | 0.16 | 0.19 | 0.31 | 0.55 |
| beam | 0.07 | 0.29 | 0.41 | 0.70 |
| l_shape | 0.11 | 0.19 | 0.30 | 0.50 |
| asym | 0.13 | 0.32 | 0.80 | 0.55 |
| u_channel | 0.17 | 0.24 | 0.25 | 0.50 |
| plus | 0.18 | 0.11 | 0.17 | 0.26 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| S_straight | 0.31 | 0.28 | 0.22 | 0.25 |
| S_side | 0.11 | 0.19 | 0.22 | 0.25 |
| S_moveturn | 0.08 | 0.14 | 0.14 | 0.17 |
| S_side_turn | 0.11 | 0.06 | 0.14 | 0.11 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 16% | 0% | 84% | 18% | 3% | 78% |  |  | 16% | 68% | 45% | 16% |
| 40 kg | 17% | 0% | 83% | 32% | 3% | 65% |  |  | 17% | 75% | 33% | 19% |
| 60 kg | 20% | 0% | 80% | 47% | 2% | 51% |  |  | 20% | 76% | 30% | 18% |
| 80 kg | 20% | 0% | 80% | 56% | 2% | 41% |  |  | 20% | 82% | 20% | 21% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 121 | 0.90 | 7% | 4% | 27% | 69% |
| 40 kg | 156 | 0.90 | 7% | 12% | 38% | 50% |
| 60 kg | 187 | 0.91 | 6% | 23% | 44% | 33% |
| 80 kg | 209 | 0.91 | 5% | 33% | 46% | 21% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 41% | 0.14 | 0.28 | 0.11 | 0.68 | 5 | 0 | 5 | 0 | 0 | 0 | 64 | 0.00 |  |
| 40 kg | 48% | 0.13 | 0.39 | 0.10 | 0.42 | 3 | 0 | 3 | 0 | 0 | 0 | 86 | 0.00 |  |
| 60 kg | 57% | 0.12 | 0.58 | 0.10 | 0.22 | 1 | 0 | 1 | 0 | 0 | 0 | 108 | 0.00 |  |
| 80 kg | 59% | 0.10 | 0.74 | 0.08 | 0.04 | 0 | 0 | 0 | 0 | 0 | 0 | 45 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.35 | 47% | 21% | 0.91 | 63% | 0.14 | 1 | 0 | 1 | 0 | 0 | 0 |
| long | 0.10 | 44% | 19% | 0.91 | 51% | 0.07 | 1 | 0 | 1 | 0 | 0 | 0 |
| sphere | 0.58 | 16% | 5% | 0.94 | 65% | 0.22 | 5 | 0 | 4 | 0 | 0 | 0 |
| cylinder | 0.15 | 20% | 6% | 0.91 | 50% | 0.08 | 4 | 0 | 4 | 0 | 0 | 0 |
| arch | 0.27 | 44% | 23% | 0.84 | 54% | 0.11 | 3 | 0 | 3 | 0 | 0 | 0 |
| dumbbell | 0.21 | 33% | 16% | 0.91 | 45% | 0.10 | 4 | 0 | 4 | 0 | 0 | 0 |
| t_shape | 0.04 | 43% | 20% | 0.93 | 50% | 0.07 | 2 | 0 | 2 | 0 | 0 | 0 |
| beam | 0.04 | 34% | 18% | 0.88 | 30% | 0.06 | 2 | 0 | 2 | 0 | 0 | 0 |
| l_shape | 0.10 | 41% | 17% | 0.90 | 54% | 0.09 | 1 | 0 | 1 | 0 | 0 | 0 |
| asym | 0.02 | 56% | 34% | 0.93 | 58% | 0.05 | 1 | 0 | 1 | 0 | 0 | 0 |
| u_channel | 0.12 | 39% | 15% | 0.94 | 45% | 0.10 | 4 | 0 | 4 | 0 | 0 | 0 |
| plus | 0.08 | 43% | 21% | 0.84 | 52% | 0.08 | 1 | 0 | 1 | 0 | 0 | 0 |
