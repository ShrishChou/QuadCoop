# Pair evaluation: e1t-R-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto); TASKS: turn in place (object at the goal position, heading off 15/30/60/90 deg, capped by symmetry)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.92 | 0.49 | 0.01 | 0.01 | 15.4 | 0.05 | 0.15 | 0.17 | 0.02 | 0.07 | 1.25 |
| 40 kg | 0.92 | 0.38 | 0.01 | 0.00 | 17.4 | 0.05 | 0.17 | 0.16 | 0.01 | 0.05 | 1.27 |
| 60 kg | 0.81 | 0.24 | 0.03 | 0.02 | 22.7 | 0.04 | 0.22 | 0.23 | 0.01 | 0.02 | 1.36 |
| 80 kg | 0.66 | 0.17 | 0.04 | 0.04 | 31.9 | 0.04 | 0.26 | 0.29 | 0.02 | 0.04 | 1.29 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube |  | 1.00 | 1.00 | 0.83 | 0.42 |
| long |  | 1.00 | 0.92 | 0.92 | 0.33 |
| sphere |  | 1.00 | 1.00 | 1.00 | 1.00 |
| cylinder |  | 0.92 | 0.83 | 0.33 | 0.33 |
| arch |  | 1.00 | 1.00 | 1.00 | 0.92 |
| dumbbell |  | 0.83 | 0.83 | 0.75 | 0.67 |
| t_shape |  | 0.92 | 0.92 | 0.83 | 0.67 |
| beam (unseen) |  | 0.92 | 0.83 | 0.58 | 0.42 |
| l_shape (unseen) |  | 0.83 | 0.92 | 1.00 | 0.83 |
| asym (unseen) |  | 0.75 | 1.00 | 0.92 | 0.92 |
| u_channel (unseen) |  | 1.00 | 1.00 | 0.83 | 0.83 |
| plus (unseen) |  | 0.83 | 0.83 | 0.75 | 0.58 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.92 | 0.06 | 0.02 | 0.00 | 0.00 | 0.03 | 3.22 |
| 40 kg | 0.92 | 0.06 | 0.01 | 0.00 | 0.00 | 0.03 | 1.90 |
| 60 kg | 0.81 | 0.14 | 0.05 | 0.00 | 0.00 | 0.02 | 2.23 |
| 80 kg | 0.66 | 0.26 | 0.08 | 0.00 | 0.00 | 0.01 | 2.99 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.55 | 0.48 | 0.68 | 0.00 | 1.00 | 0.52 | 0.51 | 0.70 | 0.00 |
| 40 kg | 1.00 | 0.51 | 0.53 | 0.74 | 0.00 | 1.00 | 0.51 | 0.54 | 0.72 | 0.00 |
| 60 kg | 1.00 | 0.45 | 0.60 | 0.79 | 0.00 | 1.00 | 0.43 | 0.62 | 0.77 | 0.00 |
| 80 kg | 1.00 | 0.41 | 0.65 | 0.81 | 0.00 | 1.00 | 0.38 | 0.65 | 0.83 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.87 | 4.50 | 0.04 | 0.81 | 4.27 | 0.05 |
| 40 kg | 0.85 | 5.19 | 0.05 | 0.87 | 5.18 | 0.05 |
| 60 kg | 0.87 | 4.81 | 0.05 | 0.87 | 5.06 | 0.06 |
| 80 kg | 0.89 | 4.67 | 0.06 | 0.92 | 5.70 | 0.08 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.34 | 0.35 | 0.18 |
| 40 kg | 0.38 | 0.38 | 0.14 |
| 60 kg | 0.45 | 0.46 | 0.13 |
| 80 kg | 0.51 | 0.50 | 0.12 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.86 | 0.21 | 11.84 | 3.22 | 0.00 | 0.00 | 0.82 | 0.00 | 0.51 |
| 40 kg | 1.99 | 0.23 | 10.92 | 1.90 | 0.00 | 0.00 | 0.58 | 0.00 | 0.45 |
| 60 kg | 1.72 | 0.32 | 13.02 | 2.23 | 0.16 | 0.00 | 2.71 | 0.00 | 0.36 |
| 80 kg | 1.71 | 0.39 | 16.40 | 2.99 | 0.03 | 0.18 | 6.68 | 0.00 | 0.32 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 81 | 197 | 144 |
| 40 kg | 113 | 242 | 212 |
| 60 kg | 141 | 274 | 261 |
| 80 kg | 152 | 286 | 280 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 308 | 0.30 | 0.42 (42) | 0.46 (67) | 0.51 (114) | 0.55 (59) | 0.69 (26) |
| 40 kg | 371 | 0.32 | 0.40 (55) | 0.41 (90) | 0.48 (108) | 0.57 (73) | 0.63 (45) |
| 60 kg | 908 | 0.30 | 0.37 (86) | 0.41 (275) | 0.49 (228) | 0.55 (232) | 0.72 (87) |
| 80 kg | 1832 | 0.29 | 0.34 (64) | 0.40 (324) | 0.49 (1063) | 0.60 (348) | 0.85 (33) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.02 | 0.00 | 0.00 | 0.00 |
| long | 0.02 | 0.00 | 0.01 | 0.00 |
| sphere | 0.00 | 0.00 | 0.00 | 0.00 |
| cylinder | 0.02 | 0.01 | 0.01 | 0.01 |
| arch | 0.00 | 0.00 | 0.00 | 0.00 |
| dumbbell | 0.00 | 0.00 | 0.00 | 0.00 |
| t_shape | 0.00 | 0.01 | 0.00 | 0.04 |
| beam | 0.02 | 0.01 | 0.00 | 0.01 |
| l_shape | 0.03 | 0.01 | 0.02 | 0.06 |
| asym | 0.06 | 0.04 | 0.04 | 0.02 |
| u_channel | 0.05 | 0.05 | 0.03 | 0.08 |
| plus | 0.00 | 0.01 | 0.01 | 0.01 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| T15 | 0.97 | 1.00 | 0.97 | 1.00 |
| T30 | 0.86 | 0.89 | 0.83 | 0.64 |
| T60 | 0.97 | 0.92 | 0.83 | 0.64 |
| T90 | 0.86 | 0.89 | 0.61 | 0.36 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 55% | 0% | 45% | 36% | 6% | 59% |  |  | 9% | 54% | 56% | 19% |
| 40 kg | 49% | 0% | 51% | 48% | 4% | 48% |  |  | 8% | 71% | 35% | 23% |
| 60 kg | 41% | 0% | 59% | 57% | 3% | 40% |  |  | 8% | 90% | 14% | 24% |
| 80 kg | 36% | 0% | 64% | 63% | 3% | 34% |  |  | 11% | 93% | 11% | 29% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 109 | 0.86 | 13% | 9% | 25% | 66% |
| 40 kg | 138 | 0.88 | 9% | 14% | 33% | 52% |
| 60 kg | 159 | 0.88 | 8% | 22% | 38% | 40% |
| 80 kg | 171 | 0.89 | 7% | 29% | 39% | 31% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 34% | 0.04 | -0.18 | 0.02 | 0.70 | 5 | 0 | 3 | 0 | 0 | 2 | 47 | 0.00 |  |
| 40 kg | 32% | 0.03 | -0.19 | 0.01 | 0.68 | 5 | 0 | 2 | 0 | 0 | 3 | 84 | 0.00 |  |
| 60 kg | 24% | 0.02 | -0.18 | 0.01 | 0.77 | 6 | 1 | 3 | 0 | 0 | 2 | 130 | 0.00 |  |
| 80 kg | 15% | 0.01 | -0.23 | 0.00 | 1.48 | 10 | 3 | 4 | 0 | 0 | 2 | 138 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.81 | 69% | 38% | 0.87 | 20% | 0.00 | 9 | 4 | 3 | 0 | 0 | 2 |
| long | 0.79 | 54% | 23% | 0.90 | 21% | 0.00 | 10 | 3 | 2 | 0 | 0 | 6 |
| sphere | 1.00 | 0% | 0% |  | 0% | 0.00 | 0 | 0 | 0 | 0 | 0 | 0 |
| cylinder | 0.60 | 45% | 19% | 0.86 | 43% | 0.00 | 8 | 0 | 2 | 0 | 0 | 6 |
| arch | 0.98 | 55% | 21% | 0.89 | 39% | 0.03 | 2 | 0 | 1 | 0 | 0 | 0 |
| dumbbell | 0.77 | 47% | 12% | 0.91 | 32% | 0.02 | 12 | 1 | 10 | 0 | 0 | 1 |
| t_shape | 0.83 | 53% | 21% | 0.87 | 31% | 0.01 | 4 | 0 | 3 | 0 | 0 | 0 |
| beam | 0.69 | 50% | 19% | 0.90 | 20% | 0.01 | 8 | 2 | 4 | 0 | 0 | 3 |
| l_shape | 0.90 | 51% | 19% | 0.89 | 27% | 0.01 | 6 | 0 | 5 | 0 | 0 | 0 |
| asym | 0.90 | 58% | 22% | 0.93 | 26% | 0.01 | 3 | 1 | 2 | 0 | 0 | 1 |
| u_channel | 0.92 | 53% | 17% | 0.91 | 30% | 0.02 | 3 | 1 | 2 | 0 | 0 | 0 |
| plus | 0.75 | 50% | 17% | 0.70 | 24% | 0.01 | 15 | 1 | 6 | 0 | 0 | 8 |
