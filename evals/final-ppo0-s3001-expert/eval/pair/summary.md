# Pair evaluation: final-ppo0-s3001-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 12 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.88 | 0.77 | 0.00 | 0.00 | 23.8 | 0.00 | 0.43 | 0.37 | 0.15 | 0.26 | 1.40 |
| 40 kg | 0.75 | 0.60 | 0.00 | 0.01 | 34.3 | 0.00 | 0.46 | 0.38 | 0.11 | 0.18 | 1.47 |
| 60 kg | 0.55 | 0.50 | 0.03 | 0.01 | 40.0 | 0.01 | 0.60 | 0.44 | 0.22 | 0.29 | 1.39 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg |
|---|---|---|---|---|
| long | part 0 -x seg 1/2 + part 0 corner -x+y | 0.92 | 0.77 | 0.67 |
| arch | part 3 -x + part 2 -x | 0.92 | 0.85 | 0.62 |
| dumbbell | part 1 -x + part 0 -x | 0.81 | 0.62 | 0.35 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.88 | 0.12 | 0.00 | 0.00 | 0.00 | 0.02 | 12.45 |
| 40 kg | 0.75 | 0.24 | 0.01 | 0.00 | 0.00 | 0.01 | 9.59 |
| 60 kg | 0.55 | 0.39 | 0.05 | 0.01 | 0.00 | 0.00 | 8.07 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.29 | 0.65 | 0.83 | 0.00 | 1.00 | 0.26 | 0.71 | 0.85 | 0.00 |
| 40 kg | 1.00 | 0.27 | 0.73 | 0.89 | 0.00 | 1.00 | 0.21 | 0.80 | 0.89 | 0.00 |
| 60 kg | 1.00 | 0.22 | 0.80 | 0.94 | 0.00 | 1.00 | 0.20 | 0.82 | 0.94 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.78 | 2.29 | 0.07 | 0.79 | 1.93 | 0.05 |
| 40 kg | 0.79 | 2.40 | 0.07 | 0.77 | 1.89 | 0.05 |
| 60 kg | 0.77 | 1.96 | 0.06 | 0.76 | 1.95 | 0.06 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.49 | 0.56 | 0.29 |
| 40 kg | 0.56 | 0.61 | 0.32 |
| 60 kg | 0.67 | 0.62 | 0.32 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.63 | 0.44 | 22.79 | 12.45 | 0.34 | 0.89 | 6.94 | 0.00 | 0.27 |
| 40 kg | 0.79 | 0.47 | 25.96 | 9.59 | 0.35 | 1.12 | 5.08 | 0.00 | 0.23 |
| 60 kg | 0.73 | 0.54 | 27.25 | 8.07 | 0.33 | 3.31 | 1.40 | 0.00 | 0.18 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 95 | 260 | 178 |
| 40 kg | 142 | 321 | 246 |
| 60 kg | 177 | 363 | 303 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 909 | 0.34 | 0.38 (171) | 0.52 (148) | 0.52 (266) | 0.52 (140) | 0.64 (184) |
| 40 kg | 1771 | 0.32 | 0.32 (457) | 0.51 (203) | 0.48 (370) | 0.52 (218) | 0.70 (523) |
| 60 kg | 2533 | 0.31 | 0.26 (622) | 0.49 (402) | 0.53 (386) | 0.55 (360) | 0.68 (762) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg |
|---|---|---|---|
| long | 0.13 | 0.11 | 0.21 |
| arch | 0.16 | 0.14 | 0.22 |
| dumbbell | 0.15 | 0.09 | 0.24 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg |
|---|---|---|---|
| A_straight | 1.00 | 0.83 | 0.67 |
| B_left | 0.86 | 0.86 | 0.69 |
| C_backright | 0.81 | 0.78 | 0.44 |
| D_far_turn | 0.86 | 0.53 | 0.39 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 38% | 0% | 62% | 39% | 5% | 56% |  |  | 15% | 60% | 47% | 19% |
| 40 kg | 30% | 0% | 70% | 48% | 3% | 49% |  |  | 13% | 56% | 47% | 18% |
| 60 kg | 23% | 0% | 77% | 55% | 2% | 43% |  |  | 12% | 62% | 41% | 21% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 137 | 0.86 | 10% | 12% | 34% | 54% |
| 40 kg | 175 | 0.88 | 8% | 19% | 42% | 39% |
| 60 kg | 203 | 0.89 | 8% | 25% | 44% | 30% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 62% | 0.22 | 0.51 | 0.18 | 0.64 | 5 | 0 | 4 | 0 | 0 | 1 | 64 | 0.00 |  |
| 40 kg | 58% | 0.14 | 0.60 | 0.12 | 0.64 | 7 | 0 | 5 | 0 | 0 | 2 | 69 | 0.00 |  |
| 60 kg | 56% | 0.10 | 0.70 | 0.08 | 0.66 | 6 | 0 | 4 | 0 | 0 | 2 | 110 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| long | 0.78 | 49% | 20% | 0.92 | 64% | 0.12 | 1 | 0 | 1 | 0 | 0 | 0 |
| arch | 0.80 | 54% | 22% | 0.82 | 63% | 0.15 | 4 | 0 | 2 | 0 | 0 | 2 |
| dumbbell | 0.60 | 39% | 15% | 0.90 | 48% | 0.10 | 12 | 0 | 9 | 0 | 0 | 2 |
