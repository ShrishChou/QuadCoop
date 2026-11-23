# Pair evaluation: probe-planner-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 10 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.86 | 0.75 | 0.00 | 0.00 | 22.4 | 0.00 | 0.38 | 0.42 | 0.15 | 0.26 | 1.23 |
| 40 kg | 0.88 | 0.68 | 0.00 | 0.01 | 29.6 | 0.00 | 0.41 | 0.49 | 0.14 | 0.21 | 1.27 |
| 60 kg | 0.60 | 0.49 | 0.04 | 0.03 | 41.2 | 0.01 | 0.54 | 0.47 | 0.19 | 0.25 | 1.24 |
| 80 kg | 0.35 | 0.25 | 0.12 | 0.03 | 47.5 | 0.01 | 0.66 | 0.53 | 0.30 | 0.36 | 1.16 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| arch | part 3 -x + part 2 -x | 0.85 | 0.93 | 0.60 | 0.38 |
| long | part 0 corner -x-y + part 0 -x seg 2/2 | 0.88 | 0.82 | 0.60 | 0.33 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.86 | 0.14 | 0.00 | 0.00 | 0.00 | 0.03 | 13.91 |
| 40 kg | 0.88 | 0.11 | 0.01 | 0.00 | 0.00 | 0.00 | 11.66 |
| 60 kg | 0.60 | 0.34 | 0.06 | 0.00 | 0.00 | 0.00 | 8.61 |
| 80 kg | 0.35 | 0.50 | 0.15 | 0.00 | 0.00 | 0.00 | 5.84 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.26 | 0.69 | 0.81 | 0.00 | 1.00 | 0.28 | 0.70 | 0.83 | 0.00 |
| 40 kg | 1.00 | 0.20 | 0.78 | 0.91 | 0.00 | 1.00 | 0.21 | 0.80 | 0.90 | 0.00 |
| 60 kg | 1.00 | 0.22 | 0.81 | 0.93 | 0.00 | 1.00 | 0.19 | 0.82 | 0.95 | 0.00 |
| 80 kg | 1.00 | 0.19 | 0.83 | 0.95 | 0.00 | 1.00 | 0.19 | 0.80 | 0.95 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.78 | 1.97 | 0.07 | 0.80 | 1.97 | 0.05 |
| 40 kg | 0.76 | 1.81 | 0.08 | 0.80 | 2.02 | 0.06 |
| 60 kg | 0.75 | 1.78 | 0.05 | 0.78 | 1.75 | 0.08 |
| 80 kg | 0.79 | 1.64 | 0.06 | 0.79 | 1.95 | 0.07 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.49 | 0.57 | 0.29 |
| 40 kg | 0.56 | 0.63 | 0.31 |
| 60 kg | 0.67 | 0.62 | 0.30 |
| 80 kg | 0.72 | 0.63 | 0.25 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.72 | 0.44 | 22.64 | 13.91 | 0.12 | 0.00 | 8.12 | 0.00 | 0.26 |
| 40 kg | 0.38 | 0.48 | 21.45 | 11.66 | 0.35 | 0.46 | 5.86 | 0.00 | 0.18 |
| 60 kg | 1.70 | 0.51 | 25.20 | 8.61 | 0.45 | 2.73 | 1.93 | 0.00 | 0.19 |
| 80 kg | 0.68 | 0.56 | 24.23 | 5.84 | 0.30 | 4.38 | 1.01 | 0.00 | 0.18 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 102 | 272 | 201 |
| 40 kg | 146 | 332 | 266 |
| 60 kg | 180 | 366 | 307 |
| 80 kg | 205 | 384 | 346 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 660 | 0.36 | 0.42 (139) | 0.52 (127) | 0.53 (133) | 0.49 (142) | 0.59 (119) |
| 40 kg | 900 | 0.31 | 0.34 (415) | 0.52 (132) | 0.52 (106) | 0.55 (66) | 0.78 (183) |
| 60 kg | 1487 | 0.28 | 0.25 (477) | 0.45 (292) | 0.49 (193) | 0.54 (159) | 0.76 (366) |
| 80 kg | 2090 | 0.32 | 0.43 (53) | 0.49 (322) | 0.50 (1220) | 0.56 (409) | 0.79 (85) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| arch | 0.17 | 0.15 | 0.20 | 0.27 |
| long | 0.13 | 0.14 | 0.19 | 0.33 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.90 | 1.00 | 0.80 | 0.60 |
| B_left | 0.95 | 0.90 | 0.50 | 0.40 |
| C_backright | 0.70 | 0.75 | 0.55 | 0.20 |
| D_far_turn | 0.90 | 0.85 | 0.55 | 0.20 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 37% | 0% | 63% | 44% | 6% | 51% |  |  | 13% | 59% | 48% | 16% |
| 40 kg | 26% | 0% | 74% | 54% | 3% | 43% |  |  | 11% | 55% | 48% | 18% |
| 60 kg | 21% | 0% | 79% | 59% | 2% | 39% |  |  | 10% | 69% | 33% | 17% |
| 80 kg | 22% | 0% | 78% | 66% | 2% | 32% |  |  | 13% | 70% | 36% | 20% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 143 | 0.85 | 10% | 15% | 37% | 48% |
| 40 kg | 176 | 0.87 | 9% | 23% | 46% | 30% |
| 60 kg | 205 | 0.88 | 8% | 28% | 48% | 24% |
| 80 kg | 225 | 0.87 | 8% | 36% | 44% | 20% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 66% | 0.23 | 0.50 | 0.18 | 0.35 | 3 | 0 | 2 | 0 | 0 | 1 | 63 | 0.00 |  |
| 40 kg | 67% | 0.17 | 0.64 | 0.15 | 0.21 | 1 | 0 | 1 | 0 | 0 | 0 | 84 | 0.00 |  |
| 60 kg | 59% | 0.10 | 0.72 | 0.08 | 0.35 | 2 | 0 | 1 | 0 | 0 | 1 | 56 | 0.00 |  |
| 80 kg | 52% | 0.06 | 0.80 | 0.06 | 0.21 | 1 | 0 | 1 | 0 | 0 | 1 | 93 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| arch | 0.69 | 59% | 29% | 0.82 | 62% | 0.13 | 3 | 0 | 2 | 0 | 0 | 1 |
| long | 0.66 | 53% | 22% | 0.91 | 60% | 0.10 | 1 | 0 | 0 | 0 | 0 | 0 |
