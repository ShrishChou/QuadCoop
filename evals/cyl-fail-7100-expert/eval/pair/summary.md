# Pair evaluation: cyl-fail-7100-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.42 | 0.33 | 0.08 | 0.08 | 27.2 | 0.02 | 0.52 | 0.42 | 0.17 | 0.26 | 0.91 |
| 40 kg | 0.42 | 0.17 | 0.00 | 0.17 | 36.2 | 0.00 | 0.43 | 0.40 | 0.07 | 0.11 | 1.07 |
| 60 kg | 0.17 | 0.17 | 0.17 | 0.17 | 45.0 | 0.00 | 0.54 | 0.50 | 0.23 | 0.30 | 0.97 |
| 80 kg | 0.33 | 0.08 | 0.00 | 0.08 | 30.8 | 0.01 | 0.70 | 0.46 | 0.29 | 0.37 | 0.92 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cylinder | part 0 -x seg 2/2 + part 0 corner -x-y | 0.42 | 0.42 | 0.17 | 0.33 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.42 | 0.42 | 0.17 | 0.00 | 0.00 | 0.00 | 8.00 |
| 40 kg | 0.42 | 0.42 | 0.17 | 0.00 | 0.00 | 0.00 | 7.50 |
| 60 kg | 0.17 | 0.50 | 0.33 | 0.00 | 0.00 | 0.08 | 6.42 |
| 80 kg | 0.33 | 0.58 | 0.08 | 0.00 | 0.00 | 0.00 | 9.33 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.25 | 0.68 | 0.89 | 0.00 | 1.00 | 0.24 | 0.72 | 0.85 | 0.00 |
| 40 kg | 1.00 | 0.24 | 0.72 | 0.86 | 0.00 | 1.00 | 0.22 | 0.78 | 0.84 | 0.00 |
| 60 kg | 1.00 | 0.24 | 0.69 | 0.88 | 0.00 | 1.00 | 0.21 | 0.78 | 0.88 | 0.00 |
| 80 kg | 1.00 | 0.17 | 0.81 | 0.97 | 0.00 | 1.00 | 0.18 | 0.78 | 0.95 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.76 | 1.44 | 0.05 | 0.76 | 1.97 | 0.03 |
| 40 kg | 0.80 | 1.59 | 0.05 | 0.73 | 1.29 | 0.02 |
| 60 kg | 0.76 | 1.54 | 0.09 | 0.72 | 1.70 | 0.07 |
| 80 kg | 0.78 | 2.17 | 0.09 | 0.76 | 2.09 | 0.12 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.53 | 0.62 | 0.33 |
| 40 kg | 0.61 | 0.62 | 0.35 |
| 60 kg | 0.58 | 0.67 | 0.31 |
| 80 kg | 0.68 | 0.62 | 0.29 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.02 | 0.53 | 27.60 | 8.00 | 1.08 | 2.83 | 11.83 | 0.00 | 0.16 |
| 40 kg | 0.02 | 0.60 | 29.71 | 7.50 | 0.08 | 3.42 | 12.25 | 0.00 | 0.14 |
| 60 kg | 0.00 | 0.60 | 34.08 | 6.42 | 1.25 | 0.58 | 6.83 | 0.00 | 0.16 |
| 80 kg | 0.01 | 0.53 | 35.32 | 9.33 | 0.75 | 2.58 | 2.75 | 0.00 | 0.24 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 95 | 243 | 206 |
| 40 kg | 146 | 312 | 283 |
| 60 kg | 141 | 315 | 239 |
| 80 kg | 162 | 358 | 315 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 106 | 0.33 | 0.34 (22) | 0.45 (19) | 0.50 (40) | 0.45 (21) | 0.80 (5) |
| 40 kg | 172 | 0.35 | 0.42 (46) | 0.39 (29) | 0.53 (65) | 0.51 (16) | 0.77 (16) |
| 60 kg | 192 | 0.31 | 0.25 (29) | 0.23 (54) | 0.44 (52) | 0.74 (32) | 0.87 (25) |
| 80 kg | 174 | 0.37 | 0.47 (1) | 0.35 (6) | 0.26 (113) | 0.65 (21) | 0.82 (33) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cylinder | 0.17 | 0.07 | 0.23 | 0.29 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.00 | 0.33 | 0.33 | 1.00 |
| B_left | 1.00 | 0.67 | 0.33 | 0.33 |
| C_backright | 0.33 | 0.67 | 0.00 | 0.00 |
| D_far_turn | 0.33 | 0.00 | 0.00 | 0.00 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 33% | 0% | 67% | 23% | 3% | 74% |  |  | 15% | 80% | 24% | 21% |
| 40 kg | 28% | 0% | 72% | 30% | 2% | 68% |  |  | 11% | 91% | 15% | 19% |
| 60 kg | 29% | 0% | 71% | 32% | 2% | 66% |  |  | 16% | 75% | 26% | 25% |
| 80 kg | 28% | 0% | 72% | 33% | 3% | 64% |  |  | 21% | 62% | 39% | 26% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 139 | 0.92 | 6% | 6% | 25% | 68% |
| 40 kg | 178 | 0.91 | 5% | 11% | 28% | 61% |
| 60 kg | 180 | 0.88 | 8% | 11% | 36% | 53% |
| 80 kg | 210 | 0.88 | 9% | 14% | 39% | 47% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 55% | 0.18 | 0.33 | 0.13 | 1.25 | 10 | 0 | 9 | 0 | 0 | 0 |  | 0.00 |  |
| 40 kg | 57% | 0.13 | 0.23 | 0.08 | 1.00 | 5 | 0 | 4 | 0 | 0 | 0 | 55 | 0.00 |  |
| 60 kg | 59% | 0.13 | 0.36 | 0.09 | 0.42 | 2 | 0 | 1 | 0 | 0 | 1 |  | 0.00 |  |
| 80 kg | 59% | 0.10 | 0.57 | 0.07 | 0.58 | 3 | 0 | 2 | 0 | 0 | 0 |  | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cylinder | 0.33 | 30% | 11% | 0.90 | 58% | 0.09 | 5 | 0 | 4 | 0 | 0 | 0 |
