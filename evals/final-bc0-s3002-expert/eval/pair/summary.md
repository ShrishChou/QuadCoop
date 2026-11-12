# Pair evaluation: final-bc0-s3002-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 12 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.79 | 0.68 | 0.01 | 0.01 | 25.0 | 0.00 | 0.40 | 0.39 | 0.14 | 0.24 | 1.34 |
| 40 kg | 0.76 | 0.60 | 0.00 | 0.01 | 31.1 | 0.00 | 0.46 | 0.41 | 0.13 | 0.20 | 1.41 |
| 60 kg | 0.59 | 0.45 | 0.02 | 0.01 | 42.8 | 0.00 | 0.54 | 0.45 | 0.21 | 0.29 | 1.40 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg |
|---|---|---|---|---|
| long | part 0 -x seg 1/2 + part 0 corner -x+y | 0.73 | 0.77 | 0.67 |
| arch | part 3 -x + part 2 -x | 0.92 | 0.88 | 0.69 |
| dumbbell | part 0 -x + part 1 -x | 0.73 | 0.65 | 0.42 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.79 | 0.19 | 0.02 | 0.00 | 0.00 | 0.02 | 11.96 |
| 40 kg | 0.76 | 0.23 | 0.01 | 0.00 | 0.00 | 0.00 | 9.66 |
| 60 kg | 0.59 | 0.38 | 0.03 | 0.00 | 0.00 | 0.01 | 8.50 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.28 | 0.69 | 0.84 | 0.00 | 1.00 | 0.27 | 0.72 | 0.84 | 0.00 |
| 40 kg | 1.00 | 0.29 | 0.71 | 0.87 | 0.00 | 1.00 | 0.23 | 0.79 | 0.87 | 0.00 |
| 60 kg | 1.00 | 0.27 | 0.76 | 0.92 | 0.00 | 1.00 | 0.22 | 0.81 | 0.92 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.80 | 2.23 | 0.07 | 0.79 | 2.01 | 0.05 |
| 40 kg | 0.80 | 2.22 | 0.07 | 0.79 | 1.94 | 0.05 |
| 60 kg | 0.81 | 2.45 | 0.07 | 0.78 | 2.07 | 0.06 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.52 | 0.57 | 0.31 |
| 40 kg | 0.53 | 0.62 | 0.32 |
| 60 kg | 0.61 | 0.62 | 0.31 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.07 | 0.46 | 24.23 | 11.96 | 0.50 | 0.73 | 8.03 | 0.00 | 0.26 |
| 40 kg | 1.45 | 0.46 | 24.87 | 9.66 | 0.30 | 1.40 | 5.64 | 0.00 | 0.23 |
| 60 kg | 2.95 | 0.50 | 27.97 | 8.50 | 0.48 | 1.84 | 2.58 | 0.00 | 0.21 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 98 | 261 | 187 |
| 40 kg | 141 | 321 | 245 |
| 60 kg | 177 | 360 | 303 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 1163 | 0.37 | 0.42 (259) | 0.51 (190) | 0.53 (279) | 0.54 (221) | 0.56 (214) |
| 40 kg | 1578 | 0.31 | 0.27 (485) | 0.49 (132) | 0.48 (353) | 0.55 (213) | 0.68 (394) |
| 60 kg | 2573 | 0.31 | 0.30 (745) | 0.50 (473) | 0.51 (404) | 0.53 (320) | 0.72 (631) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg |
|---|---|---|---|
| long | 0.14 | 0.15 | 0.23 |
| arch | 0.14 | 0.15 | 0.18 |
| dumbbell | 0.12 | 0.11 | 0.22 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg |
|---|---|---|---|
| A_straight | 0.94 | 0.92 | 0.72 |
| B_left | 0.75 | 0.72 | 0.53 |
| C_backright | 0.67 | 0.78 | 0.58 |
| D_far_turn | 0.81 | 0.64 | 0.53 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 36% | 0% | 64% | 39% | 5% | 56% |  |  | 13% | 55% | 52% | 18% |
| 40 kg | 30% | 0% | 70% | 48% | 3% | 49% |  |  | 12% | 54% | 53% | 17% |
| 60 kg | 25% | 0% | 75% | 55% | 2% | 43% |  |  | 12% | 71% | 35% | 21% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 140 | 0.86 | 10% | 13% | 34% | 53% |
| 40 kg | 175 | 0.89 | 7% | 18% | 42% | 40% |
| 60 kg | 202 | 0.89 | 7% | 24% | 47% | 29% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 60% | 0.20 | 0.47 | 0.16 | 0.74 | 5 | 0 | 4 | 0 | 0 | 1 | 88 | 0.00 |  |
| 40 kg | 58% | 0.14 | 0.62 | 0.12 | 0.63 | 7 | 0 | 5 | 0 | 0 | 2 | 94 | 0.00 |  |
| 60 kg | 55% | 0.09 | 0.69 | 0.08 | 0.57 | 4 | 0 | 3 | 0 | 0 | 1 | 125 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| long | 0.72 | 51% | 21% | 0.92 | 63% | 0.12 | 2 | 0 | 1 | 0 | 0 | 0 |
| arch | 0.83 | 53% | 21% | 0.82 | 61% | 0.14 | 5 | 0 | 2 | 0 | 0 | 3 |
| dumbbell | 0.60 | 38% | 14% | 0.90 | 48% | 0.10 | 10 | 0 | 8 | 0 | 0 | 2 |
