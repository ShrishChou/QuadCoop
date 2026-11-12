# Pair evaluation: final-ppo0-s3000-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 12 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.74 | 0.70 | 0.00 | 0.01 | 22.8 | 0.00 | 0.39 | 0.41 | 0.15 | 0.26 | 1.37 |
| 40 kg | 0.79 | 0.65 | 0.02 | 0.01 | 33.4 | 0.00 | 0.44 | 0.43 | 0.14 | 0.20 | 1.48 |
| 60 kg | 0.53 | 0.42 | 0.03 | 0.03 | 41.4 | 0.01 | 0.55 | 0.43 | 0.18 | 0.25 | 1.41 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg |
|---|---|---|---|---|
| long | part 0 -x seg 1/2 + part 0 corner -x+y | 0.79 | 0.83 | 0.58 |
| arch | part 2 -x + part 3 -x | 0.75 | 0.88 | 0.52 |
| dumbbell | part 1 -x + part 0 -x | 0.69 | 0.67 | 0.50 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.74 | 0.25 | 0.01 | 0.00 | 0.00 | 0.02 | 11.83 |
| 40 kg | 0.79 | 0.18 | 0.03 | 0.00 | 0.00 | 0.00 | 9.43 |
| 60 kg | 0.53 | 0.40 | 0.06 | 0.00 | 0.00 | 0.00 | 7.89 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.27 | 0.68 | 0.85 | 0.00 | 1.00 | 0.28 | 0.71 | 0.86 | 0.00 |
| 40 kg | 1.00 | 0.25 | 0.74 | 0.90 | 0.00 | 1.00 | 0.23 | 0.78 | 0.88 | 0.00 |
| 60 kg | 1.00 | 0.23 | 0.79 | 0.94 | 0.00 | 1.00 | 0.20 | 0.82 | 0.93 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.76 | 2.24 | 0.06 | 0.78 | 2.14 | 0.05 |
| 40 kg | 0.79 | 2.27 | 0.07 | 0.78 | 2.06 | 0.06 |
| 60 kg | 0.76 | 1.83 | 0.07 | 0.77 | 2.05 | 0.06 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.52 | 0.57 | 0.32 |
| 40 kg | 0.53 | 0.61 | 0.31 |
| 60 kg | 0.62 | 0.62 | 0.31 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.65 | 0.46 | 24.74 | 11.83 | 0.22 | 1.16 | 8.28 | 0.00 | 0.26 |
| 40 kg | 1.42 | 0.44 | 25.08 | 9.43 | 0.76 | 0.55 | 4.84 | 0.00 | 0.22 |
| 60 kg | 2.04 | 0.46 | 27.12 | 7.89 | 0.67 | 3.26 | 1.43 | 0.00 | 0.20 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 95 | 257 | 173 |
| 40 kg | 141 | 321 | 252 |
| 60 kg | 180 | 363 | 306 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 1202 | 0.34 | 0.44 (222) | 0.52 (292) | 0.51 (429) | 0.50 (128) | 0.65 (131) |
| 40 kg | 1444 | 0.33 | 0.35 (451) | 0.50 (176) | 0.53 (212) | 0.54 (159) | 0.72 (446) |
| 60 kg | 2290 | 0.30 | 0.29 (578) | 0.47 (354) | 0.50 (340) | 0.56 (384) | 0.71 (634) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg |
|---|---|---|---|
| long | 0.13 | 0.11 | 0.23 |
| arch | 0.16 | 0.13 | 0.14 |
| dumbbell | 0.15 | 0.17 | 0.19 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg |
|---|---|---|---|
| A_straight | 0.92 | 0.94 | 0.75 |
| B_left | 0.69 | 0.78 | 0.56 |
| C_backright | 0.58 | 0.83 | 0.53 |
| D_far_turn | 0.78 | 0.61 | 0.31 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 36% | 0% | 64% | 38% | 5% | 56% |  |  | 14% | 63% | 45% | 18% |
| 40 kg | 29% | 0% | 71% | 48% | 3% | 50% |  |  | 13% | 59% | 44% | 20% |
| 60 kg | 23% | 0% | 77% | 54% | 2% | 44% |  |  | 13% | 68% | 35% | 21% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 138 | 0.86 | 10% | 13% | 33% | 54% |
| 40 kg | 174 | 0.88 | 8% | 19% | 42% | 39% |
| 60 kg | 204 | 0.89 | 7% | 25% | 45% | 30% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 59% | 0.20 | 0.49 | 0.16 | 0.85 | 7 | 0 | 6 | 0 | 0 | 1 | 50 | 0.00 |  |
| 40 kg | 60% | 0.15 | 0.64 | 0.13 | 0.64 | 5 | 0 | 4 | 0 | 0 | 1 | 75 | 0.00 |  |
| 60 kg | 54% | 0.09 | 0.70 | 0.08 | 0.56 | 4 | 0 | 4 | 0 | 0 | 1 | 105 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| long | 0.74 | 48% | 19% | 0.92 | 62% | 0.12 | 2 | 0 | 2 | 0 | 0 | 0 |
| arch | 0.72 | 52% | 23% | 0.81 | 61% | 0.14 | 5 | 0 | 4 | 0 | 0 | 1 |
| dumbbell | 0.62 | 39% | 15% | 0.90 | 50% | 0.11 | 9 | 0 | 8 | 0 | 0 | 2 |
