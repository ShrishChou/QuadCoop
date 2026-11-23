# Pair evaluation: probe2v-planner-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 10 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.84 | 0.74 | 0.00 | 0.01 | 26.8 | 0.01 | 0.36 | 0.41 | 0.12 | 0.22 | 1.29 |
| 40 kg | 0.82 | 0.70 | 0.01 | 0.01 | 31.6 | 0.00 | 0.46 | 0.43 | 0.14 | 0.20 | 1.31 |
| 60 kg | 0.57 | 0.40 | 0.05 | 0.01 | 41.3 | 0.00 | 0.58 | 0.44 | 0.20 | 0.25 | 1.28 |
| 80 kg | 0.29 | 0.24 | 0.15 | 0.03 | 40.9 | 0.01 | 0.63 | 0.52 | 0.28 | 0.33 | 1.17 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| arch | part 3 -x + part 2 -x | 0.90 | 0.95 | 0.65 | 0.30 |
| long | part 0 corner -x-y + part 0 -x seg 2/2 | 0.78 | 0.70 | 0.50 | 0.28 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.84 | 0.15 | 0.01 | 0.00 | 0.00 | 0.01 | 13.56 |
| 40 kg | 0.82 | 0.15 | 0.03 | 0.00 | 0.00 | 0.00 | 10.04 |
| 60 kg | 0.57 | 0.36 | 0.06 | 0.00 | 0.00 | 0.00 | 8.09 |
| 80 kg | 0.29 | 0.54 | 0.17 | 0.00 | 0.00 | 0.00 | 6.06 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.28 | 0.69 | 0.81 | 0.00 | 1.00 | 0.28 | 0.70 | 0.81 | 0.00 |
| 40 kg | 1.00 | 0.19 | 0.80 | 0.91 | 0.00 | 1.00 | 0.21 | 0.79 | 0.88 | 0.00 |
| 60 kg | 1.00 | 0.20 | 0.82 | 0.94 | 0.00 | 1.00 | 0.19 | 0.81 | 0.94 | 0.00 |
| 80 kg | 1.00 | 0.21 | 0.80 | 0.95 | 0.00 | 1.00 | 0.20 | 0.80 | 0.93 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.79 | 2.10 | 0.07 | 0.80 | 2.22 | 0.06 |
| 40 kg | 0.78 | 1.71 | 0.07 | 0.78 | 2.01 | 0.06 |
| 60 kg | 0.77 | 1.95 | 0.05 | 0.74 | 1.93 | 0.07 |
| 80 kg | 0.78 | 1.83 | 0.06 | 0.78 | 1.92 | 0.08 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.48 | 0.55 | 0.29 |
| 40 kg | 0.59 | 0.61 | 0.32 |
| 60 kg | 0.68 | 0.60 | 0.29 |
| 80 kg | 0.71 | 0.61 | 0.24 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.63 | 0.43 | 24.95 | 13.56 | 0.05 | 0.01 | 8.38 | 0.00 | 0.25 |
| 40 kg | 0.79 | 0.48 | 22.34 | 10.04 | 0.06 | 0.88 | 6.25 | 0.00 | 0.19 |
| 60 kg | 1.05 | 0.49 | 24.99 | 8.09 | 0.55 | 3.11 | 1.94 | 0.00 | 0.19 |
| 80 kg | 1.52 | 0.55 | 24.01 | 6.06 | 0.60 | 3.66 | 0.78 | 0.00 | 0.20 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 106 | 271 | 188 |
| 40 kg | 142 | 328 | 255 |
| 60 kg | 180 | 366 | 306 |
| 80 kg | 205 | 385 | 346 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 750 | 0.35 | 0.43 (206) | 0.51 (133) | 0.51 (143) | 0.47 (146) | 0.63 (122) |
| 40 kg | 999 | 0.30 | 0.29 (354) | 0.51 (100) | 0.49 (185) | 0.54 (134) | 0.77 (227) |
| 60 kg | 1370 | 0.30 | 0.23 (337) | 0.48 (269) | 0.50 (200) | 0.54 (192) | 0.71 (372) |
| 80 kg | 2067 | 0.33 | 0.45 (52) | 0.50 (343) | 0.50 (1266) | 0.56 (353) | 0.54 (54) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| arch | 0.12 | 0.15 | 0.19 | 0.25 |
| long | 0.12 | 0.13 | 0.20 | 0.30 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.70 | 0.90 | 0.70 | 0.55 |
| B_left | 0.90 | 0.75 | 0.50 | 0.20 |
| C_backright | 0.90 | 0.70 | 0.45 | 0.15 |
| D_far_turn | 0.85 | 0.95 | 0.65 | 0.25 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 38% | 0% | 62% | 45% | 5% | 50% |  |  | 12% | 56% | 52% | 18% |
| 40 kg | 26% | 0% | 74% | 52% | 3% | 44% |  |  | 12% | 54% | 52% | 17% |
| 60 kg | 22% | 0% | 78% | 59% | 3% | 39% |  |  | 12% | 66% | 40% | 17% |
| 80 kg | 23% | 0% | 77% | 66% | 2% | 32% |  |  | 14% | 71% | 33% | 21% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 144 | 0.84 | 10% | 16% | 36% | 48% |
| 40 kg | 175 | 0.87 | 9% | 21% | 47% | 32% |
| 60 kg | 205 | 0.87 | 9% | 27% | 47% | 25% |
| 80 kg | 226 | 0.87 | 8% | 37% | 43% | 20% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 65% | 0.21 | 0.45 | 0.16 | 0.42 | 3 | 0 | 2 | 0 | 0 | 1 | 53 | 0.00 |  |
| 40 kg | 64% | 0.16 | 0.66 | 0.14 | 0.38 | 3 | 0 | 2 | 0 | 0 | 1 | 88 | 0.00 |  |
| 60 kg | 57% | 0.10 | 0.73 | 0.08 | 0.41 | 3 | 0 | 2 | 0 | 0 | 1 | 87 | 0.00 |  |
| 80 kg | 52% | 0.06 | 0.79 | 0.06 | 0.26 | 1 | 0 | 1 | 0 | 0 | 1 | 94 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| arch | 0.70 | 58% | 29% | 0.82 | 61% | 0.12 | 4 | 0 | 2 | 0 | 0 | 1 |
| long | 0.56 | 53% | 22% | 0.91 | 58% | 0.10 | 1 | 0 | 1 | 0 | 0 | 0 |
