# Pair evaluation: e1t-E-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: first); TASKS: turn in place (object at the goal position, heading off 15/30/60/90 deg, capped by symmetry)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.30 | 0.31 | 0.03 | 0.01 | 14.2 | 0.05 | 0.27 | 0.32 | 0.03 | 0.06 | 1.27 |
| 40 kg | 0.46 | 0.44 | 0.02 | 0.01 | 17.6 | 0.05 | 0.21 | 0.32 | 0.02 | 0.04 | 1.30 |
| 60 kg | 0.47 | 0.37 | 0.03 | 0.04 | 15.1 | 0.05 | 0.22 | 0.34 | 0.02 | 0.04 | 1.47 |
| 80 kg | 0.50 | 0.30 | 0.01 | 0.03 | 20.4 | 0.04 | 0.26 | 0.34 | 0.02 | 0.04 | 1.45 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube |  | 0.67 | 0.92 | 0.83 | 0.83 |
| long |  | 0.42 | 0.75 | 0.42 | 0.58 |
| sphere |  | 1.00 | 1.00 | 1.00 | 1.00 |
| cylinder |  | 0.25 | 0.33 | 0.25 | 0.25 |
| arch |  | 0.08 | 0.25 | 0.42 | 0.50 |
| dumbbell |  | 0.00 | 0.08 | 0.42 | 0.75 |
| t_shape |  | 0.00 | 0.00 | 0.08 | 0.25 |
| beam (unseen) |  | 0.33 | 0.58 | 0.58 | 0.33 |
| l_shape (unseen) |  | 0.00 | 0.50 | 0.50 | 0.25 |
| asym (unseen) |  | 0.17 | 0.42 | 0.50 | 0.58 |
| u_channel (unseen) |  | 0.17 | 0.17 | 0.17 | 0.08 |
| plus (unseen) |  | 0.50 | 0.50 | 0.50 | 0.58 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.30 | 0.66 | 0.04 | 0.00 | 0.00 | 0.13 | 0.04 |
| 40 kg | 0.46 | 0.51 | 0.03 | 0.00 | 0.00 | 0.09 | 0.04 |
| 60 kg | 0.47 | 0.46 | 0.07 | 0.00 | 0.00 | 0.04 | 0.04 |
| 80 kg | 0.50 | 0.44 | 0.05 | 0.01 | 0.00 | 0.01 | 0.04 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.38 | 0.66 | 0.83 | 0.00 | 1.00 | 0.42 | 0.58 | 0.79 | 0.00 |
| 40 kg | 1.00 | 0.41 | 0.62 | 0.81 | 0.00 | 1.00 | 0.46 | 0.57 | 0.76 | 0.00 |
| 60 kg | 1.00 | 0.42 | 0.61 | 0.81 | 0.00 | 1.00 | 0.41 | 0.59 | 0.78 | 0.00 |
| 80 kg | 1.00 | 0.39 | 0.63 | 0.81 | 0.00 | 1.00 | 0.37 | 0.63 | 0.81 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.84 | 6.28 | 0.02 | 0.83 | 7.20 | 0.05 |
| 40 kg | 0.84 | 6.52 | 0.05 | 0.82 | 6.45 | 0.04 |
| 60 kg | 0.86 | 6.43 | 0.06 | 0.84 | 6.29 | 0.07 |
| 80 kg | 0.89 | 7.56 | 0.06 | 0.86 | 6.36 | 0.07 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.54 | 0.50 | 0.62 |
| 40 kg | 0.51 | 0.52 | 0.50 |
| 60 kg | 0.50 | 0.52 | 0.40 |
| 80 kg | 0.53 | 0.56 | 0.33 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 2.52 | 0.39 | 23.25 | 0.04 | 0.00 | 0.00 | 15.78 | 0.00 | 0.41 |
| 40 kg | 2.15 | 0.38 | 21.19 | 0.04 | 0.00 | 0.00 | 14.66 | 0.00 | 0.42 |
| 60 kg | 2.26 | 0.40 | 19.55 | 0.04 | 0.00 | 0.00 | 12.50 | 0.00 | 0.42 |
| 80 kg | 2.38 | 0.45 | 19.20 | 0.04 | 0.00 | 0.00 | 11.07 | 0.00 | 0.38 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 84 | 198 | 160 |
| 40 kg | 119 | 262 | 228 |
| 60 kg | 149 | 297 | 278 |
| 80 kg | 168 | 330 | 322 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 630 | 0.35 | 0.49 (120) | 0.49 (83) | 0.48 (208) | 0.47 (132) | 0.63 (88) |
| 40 kg | 686 | 0.36 | 0.50 (165) | 0.49 (99) | 0.49 (239) | 0.52 (48) | 0.64 (135) |
| 60 kg | 1066 | 0.40 | 0.58 (247) | 0.51 (114) | 0.50 (333) | 0.47 (174) | 0.60 (199) |
| 80 kg | 1798 | 0.40 | 0.58 (391) | 0.51 (151) | 0.48 (767) | 0.45 (152) | 0.59 (337) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.05 | 0.04 | 0.02 | 0.00 |
| long | 0.01 | 0.01 | 0.00 | 0.00 |
| sphere | 0.00 | 0.00 | 0.00 | 0.00 |
| cylinder | 0.00 | 0.00 | 0.00 | 0.00 |
| arch | 0.00 | 0.00 | 0.01 | 0.01 |
| dumbbell | 0.00 | 0.00 | 0.01 | 0.01 |
| t_shape | 0.01 | 0.10 | 0.11 | 0.04 |
| beam | 0.00 | 0.00 | 0.01 | 0.00 |
| l_shape | 0.20 | 0.01 | 0.06 | 0.06 |
| asym | 0.06 | 0.03 | 0.02 | 0.06 |
| u_channel | 0.01 | 0.02 | 0.02 | 0.05 |
| plus | 0.02 | 0.01 | 0.00 | 0.00 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| T15 | 0.44 | 0.44 | 0.56 | 0.75 |
| T30 | 0.19 | 0.36 | 0.42 | 0.39 |
| T60 | 0.33 | 0.44 | 0.50 | 0.50 |
| T90 | 0.22 | 0.58 | 0.42 | 0.36 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 42% | 0% | 58% | 21% | 3% | 76% |  |  | 17% | 61% | 48% | 17% |
| 40 kg | 44% | 0% | 56% | 33% | 2% | 65% |  |  | 15% | 65% | 44% | 21% |
| 60 kg | 44% | 0% | 56% | 43% | 2% | 55% |  |  | 18% | 59% | 52% | 23% |
| 80 kg | 41% | 0% | 59% | 52% | 2% | 46% |  |  | 15% | 62% | 46% | 27% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 116 | 0.87 | 11% | 6% | 14% | 80% |
| 40 kg | 150 | 0.88 | 10% | 9% | 23% | 68% |
| 60 kg | 174 | 0.90 | 8% | 14% | 31% | 55% |
| 80 kg | 194 | 0.90 | 6% | 18% | 37% | 44% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 21% | 0.02 | -0.27 | 0.00 | 2.49 | 28 | 0 | 24 | 0 | 0 | 4 | 61 | 0.00 |  |
| 40 kg | 23% | 0.02 | -0.26 | 0.01 | 2.05 | 21 | 0 | 18 | 0 | 0 | 3 | 74 | 0.00 |  |
| 60 kg | 21% | 0.01 | -0.23 | 0.01 | 1.91 | 15 | 1 | 10 | 0 | 0 | 4 | 124 | 0.00 |  |
| 80 kg | 18% | 0.01 | -0.29 | 0.01 | 1.92 | 13 | 2 | 8 | 0 | 0 | 4 | 142 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.81 | 60% | 24% | 0.91 | 36% | 0.00 | 4 | 1 | 3 | 0 | 0 | 1 |
| long | 0.54 | 61% | 23% | 0.92 | 28% | 0.01 | 11 | 2 | 4 | 0 | 0 | 6 |
| sphere | 1.00 | 0% | 0% |  | 0% | -0.00 | 0 | 0 | 0 | 0 | 0 | 0 |
| cylinder | 0.27 | 17% | 4% | 0.93 | 23% | -0.00 | 18 | 0 | 9 | 0 | 0 | 9 |
| arch | 0.31 | 31% | 11% | 0.79 | 22% | 0.02 | 29 | 0 | 29 | 0 | 0 | 0 |
| dumbbell | 0.31 | 29% | 7% | 0.91 | 22% | 0.01 | 31 | 0 | 28 | 0 | 0 | 2 |
| t_shape | 0.08 | 40% | 12% | 0.86 | 18% | 0.00 | 20 | 1 | 10 | 0 | 0 | 10 |
| beam | 0.46 | 36% | 16% | 0.87 | 15% | 0.01 | 24 | 2 | 21 | 0 | 0 | 1 |
| l_shape | 0.31 | 34% | 10% | 0.93 | 20% | 0.01 | 31 | 1 | 27 | 0 | 0 | 3 |
| asym | 0.42 | 38% | 8% | 0.90 | 21% | 0.01 | 23 | 0 | 21 | 0 | 0 | 3 |
| u_channel | 0.15 | 28% | 9% | 0.94 | 16% | 0.00 | 28 | 1 | 27 | 0 | 0 | 1 |
| plus | 0.52 | 56% | 19% | 0.78 | 28% | 0.00 | 12 | 1 | 1 | 0 | 0 | 11 |
