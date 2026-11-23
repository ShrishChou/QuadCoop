# Pair evaluation: probe-planner-swap-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto); ACTORS SWAPPED (each robot runs the other's trained network)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 10 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.80 | 0.76 | 0.01 | 0.00 | 27.4 | 0.00 | 0.40 | 0.32 | 0.09 | 0.17 | 1.21 |
| 40 kg | 0.89 | 0.70 | 0.00 | 0.01 | 34.7 | 0.00 | 0.51 | 0.34 | 0.09 | 0.14 | 1.30 |
| 60 kg | 0.47 | 0.34 | 0.03 | 0.04 | 42.7 | 0.00 | 0.54 | 0.39 | 0.12 | 0.17 | 1.18 |
| 80 kg | 0.29 | 0.20 | 0.10 | 0.04 | 56.3 | 0.01 | 0.66 | 0.47 | 0.24 | 0.30 | 1.13 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| arch | part 3 -x + part 2 -x | 0.80 | 0.90 | 0.53 | 0.33 |
| long | part 0 corner -x-y + part 0 -x seg 2/2 | 0.80 | 0.88 | 0.42 | 0.25 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.80 | 0.19 | 0.01 | 0.00 | 0.00 | 0.04 | 12.80 |
| 40 kg | 0.89 | 0.10 | 0.01 | 0.00 | 0.00 | 0.01 | 11.10 |
| 60 kg | 0.47 | 0.46 | 0.06 | 0.00 | 0.00 | 0.00 | 6.72 |
| 80 kg | 0.29 | 0.57 | 0.14 | 0.00 | 0.00 | 0.00 | 5.50 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.30 | 0.69 | 0.80 | 0.00 | 1.00 | 0.25 | 0.70 | 0.81 | 0.00 |
| 40 kg | 1.00 | 0.26 | 0.73 | 0.86 | 0.00 | 1.00 | 0.20 | 0.77 | 0.88 | 0.00 |
| 60 kg | 1.00 | 0.19 | 0.81 | 0.96 | 0.00 | 1.00 | 0.17 | 0.86 | 0.95 | 0.00 |
| 80 kg | 1.00 | 0.18 | 0.81 | 0.96 | 0.00 | 1.00 | 0.19 | 0.79 | 0.95 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.78 | 2.10 | 0.08 | 0.79 | 2.20 | 0.05 |
| 40 kg | 0.79 | 2.57 | 0.11 | 0.78 | 2.24 | 0.07 |
| 60 kg | 0.79 | 1.90 | 0.10 | 0.77 | 1.97 | 0.05 |
| 80 kg | 0.77 | 1.96 | 0.09 | 0.79 | 3.67 | 0.07 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.51 | 0.52 | 0.30 |
| 40 kg | 0.59 | 0.57 | 0.32 |
| 60 kg | 0.66 | 0.58 | 0.33 |
| 80 kg | 0.71 | 0.58 | 0.26 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 3.04 | 0.41 | 25.32 | 12.80 | 0.00 | 0.03 | 7.74 | 0.00 | 0.29 |
| 40 kg | 1.27 | 0.44 | 24.20 | 11.10 | 0.35 | 0.39 | 5.81 | 0.00 | 0.25 |
| 60 kg | 0.79 | 0.43 | 26.50 | 6.72 | 0.94 | 3.91 | 2.61 | 0.00 | 0.18 |
| 80 kg | 0.66 | 0.47 | 27.63 | 5.50 | 0.39 | 4.36 | 0.97 | 0.00 | 0.22 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 104 | 266 | 194 |
| 40 kg | 143 | 327 | 258 |
| 60 kg | 181 | 356 | 305 |
| 80 kg | 206 | 382 | 349 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 742 | 0.34 | 0.40 (125) | 0.49 (144) | 0.51 (122) | 0.51 (139) | 0.57 (211) |
| 40 kg | 911 | 0.29 | 0.21 (210) | 0.50 (73) | 0.59 (194) | 0.56 (79) | 0.72 (354) |
| 60 kg | 1264 | 0.29 | 0.26 (340) | 0.40 (259) | 0.50 (131) | 0.60 (110) | 0.74 (424) |
| 80 kg | 1927 | 0.33 | 0.37 (34) | 0.42 (343) | 0.51 (1074) | 0.66 (354) | 0.59 (121) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| arch | 0.09 | 0.04 | 0.07 | 0.17 |
| long | 0.09 | 0.14 | 0.17 | 0.32 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.80 | 0.90 | 0.45 | 0.40 |
| B_left | 0.75 | 1.00 | 0.65 | 0.30 |
| C_backright | 0.80 | 0.80 | 0.30 | 0.05 |
| D_far_turn | 0.85 | 0.85 | 0.50 | 0.40 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 38% | 0% | 62% | 44% | 5% | 51% |  |  | 14% | 63% | 45% | 16% |
| 40 kg | 31% | 0% | 69% | 50% | 4% | 46% |  |  | 13% | 67% | 37% | 17% |
| 60 kg | 20% | 0% | 80% | 55% | 3% | 42% |  |  | 11% | 76% | 26% | 19% |
| 80 kg | 23% | 0% | 77% | 64% | 2% | 34% |  |  | 13% | 76% | 26% | 22% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 142 | 0.84 | 11% | 16% | 36% | 48% |
| 40 kg | 175 | 0.87 | 8% | 19% | 48% | 33% |
| 60 kg | 201 | 0.87 | 8% | 25% | 49% | 26% |
| 80 kg | 224 | 0.87 | 7% | 35% | 45% | 20% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 63% | 0.20 | 0.46 | 0.15 | 0.62 | 6 | 0 | 5 | 0 | 0 | 1 | 65 | 0.00 |  |
| 40 kg | 62% | 0.14 | 0.61 | 0.12 | 0.34 | 2 | 0 | 1 | 0 | 0 | 0 | 65 | 0.00 |  |
| 60 kg | 54% | 0.08 | 0.73 | 0.07 | 0.36 | 3 | 0 | 3 | 0 | 0 | 0 | 69 | 0.00 |  |
| 80 kg | 49% | 0.06 | 0.81 | 0.05 | 0.35 | 2 | 0 | 1 | 0 | 0 | 1 | 117 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| arch | 0.64 | 55% | 28% | 0.80 | 54% | 0.10 | 4 | 0 | 3 | 0 | 0 | 1 |
| long | 0.59 | 51% | 20% | 0.93 | 60% | 0.10 | 2 | 0 | 1 | 0 | 0 | 1 |
