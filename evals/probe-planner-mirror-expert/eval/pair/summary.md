# Pair evaluation: probe-planner-mirror-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 10 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.82 | 0.79 | 0.01 | 0.00 | 27.5 | 0.01 | 0.36 | 0.40 | 0.15 | 0.29 | 1.24 |
| 40 kg | 0.76 | 0.69 | 0.01 | 0.00 | 34.1 | 0.00 | 0.42 | 0.44 | 0.16 | 0.27 | 1.27 |
| 60 kg | 0.64 | 0.39 | 0.01 | 0.00 | 44.3 | 0.00 | 0.49 | 0.48 | 0.19 | 0.26 | 1.26 |
| 80 kg | 0.41 | 0.28 | 0.07 | 0.03 | 44.1 | 0.01 | 0.59 | 0.62 | 0.34 | 0.41 | 1.19 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| arch |  | 0.80 | 0.78 | 0.57 | 0.45 |
| long |  | 0.85 | 0.75 | 0.70 | 0.38 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.82 | 0.16 | 0.01 | 0.00 | 0.00 | 0.01 | 12.66 |
| 40 kg | 0.76 | 0.23 | 0.01 | 0.00 | 0.00 | 0.01 | 9.56 |
| 60 kg | 0.64 | 0.35 | 0.01 | 0.00 | 0.00 | 0.00 | 9.56 |
| 80 kg | 0.41 | 0.49 | 0.10 | 0.00 | 0.00 | 0.00 | 7.81 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.29 | 0.71 | 0.82 | 0.00 | 1.00 | 0.24 | 0.74 | 0.86 | 0.00 |
| 40 kg | 1.00 | 0.25 | 0.78 | 0.88 | 0.00 | 1.00 | 0.21 | 0.78 | 0.89 | 0.00 |
| 60 kg | 1.00 | 0.19 | 0.80 | 0.93 | 0.00 | 1.00 | 0.19 | 0.82 | 0.94 | 0.00 |
| 80 kg | 1.00 | 0.21 | 0.80 | 0.94 | 0.00 | 1.00 | 0.17 | 0.82 | 0.96 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.79 | 2.35 | 0.05 | 0.82 | 2.10 | 0.04 |
| 40 kg | 0.79 | 2.05 | 0.06 | 0.83 | 2.01 | 0.05 |
| 60 kg | 0.80 | 1.81 | 0.05 | 0.81 | 1.99 | 0.06 |
| 80 kg | 0.81 | 1.61 | 0.06 | 0.81 | 1.90 | 0.09 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.54 | 0.56 | 0.34 |
| 40 kg | 0.60 | 0.57 | 0.32 |
| 60 kg | 0.63 | 0.63 | 0.36 |
| 80 kg | 0.64 | 0.65 | 0.26 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.86 | 0.51 | 24.49 | 12.66 | 0.11 | 1.40 | 6.95 | 0.00 | 0.23 |
| 40 kg | 1.68 | 0.49 | 25.47 | 9.56 | 0.09 | 1.19 | 7.05 | 0.00 | 0.22 |
| 60 kg | 0.57 | 0.50 | 27.59 | 9.56 | 0.21 | 4.41 | 2.62 | 0.00 | 0.19 |
| 80 kg | 0.65 | 0.51 | 27.36 | 7.81 | 0.35 | 1.62 | 1.01 | 0.00 | 0.19 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 100 | 270 | 202 |
| 40 kg | 138 | 327 | 249 |
| 60 kg | 171 | 358 | 291 |
| 80 kg | 210 | 386 | 348 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 697 | 0.36 | 0.47 (186) | 0.50 (157) | 0.47 (137) | 0.52 (98) | 0.63 (120) |
| 40 kg | 1032 | 0.33 | 0.35 (295) | 0.43 (138) | 0.46 (237) | 0.52 (155) | 0.73 (207) |
| 60 kg | 1363 | 0.32 | 0.23 (269) | 0.40 (178) | 0.49 (142) | 0.53 (262) | 0.66 (512) |
| 80 kg | 1843 | 0.31 | 0.28 (65) | 0.51 (217) | 0.52 (936) | 0.58 (487) | 0.71 (139) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| arch | 0.17 | 0.16 | 0.19 | 0.26 |
| long | 0.12 | 0.17 | 0.20 | 0.42 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight_m | 0.95 | 0.90 | 0.75 | 0.50 |
| B_left_m | 0.85 | 0.85 | 0.75 | 0.55 |
| C_backright_m | 0.75 | 0.60 | 0.45 | 0.45 |
| D_far_turn_m | 0.75 | 0.70 | 0.60 | 0.15 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 34% | 0% | 66% | 40% | 5% | 55% |  |  | 10% | 53% | 56% | 19% |
| 40 kg | 28% | 0% | 72% | 48% | 3% | 50% |  |  | 10% | 53% | 54% | 17% |
| 60 kg | 22% | 0% | 78% | 53% | 2% | 45% |  |  | 11% | 64% | 42% | 18% |
| 80 kg | 22% | 0% | 78% | 65% | 2% | 34% |  |  | 13% | 69% | 34% | 17% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 142 | 0.87 | 9% | 14% | 33% | 53% |
| 40 kg | 172 | 0.87 | 9% | 18% | 43% | 39% |
| 60 kg | 199 | 0.88 | 7% | 22% | 47% | 31% |
| 80 kg | 228 | 0.90 | 6% | 36% | 43% | 20% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 59% | 0.19 | 0.46 | 0.15 | 0.65 | 7 | 0 | 6 | 0 | 0 | 1 | 72 | 0.00 |  |
| 40 kg | 56% | 0.15 | 0.59 | 0.12 | 0.84 | 7 | 0 | 6 | 0 | 0 | 1 | 77 | 0.00 |  |
| 60 kg | 52% | 0.10 | 0.71 | 0.08 | 0.94 | 6 | 0 | 5 | 0 | 0 | 1 | 83 | 0.00 |  |
| 80 kg | 56% | 0.07 | 0.80 | 0.06 | 0.57 | 3 | 0 | 2 | 0 | 0 | 1 | 103 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| arch | 0.65 | 50% | 23% | 0.84 | 53% | 0.11 | 9 | 0 | 7 | 0 | 0 | 1 |
| long | 0.67 | 52% | 22% | 0.92 | 59% | 0.09 | 3 | 0 | 2 | 0 | 0 | 1 |
