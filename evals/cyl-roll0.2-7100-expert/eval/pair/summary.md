# Pair evaluation: cyl-roll0.2-7100-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto); planner settings changed: roll_ratio=0.2

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.17 | 0.17 | 0.08 | 0.00 | 16.7 | 0.01 | 0.47 | 0.33 | 0.04 | 0.06 | 0.91 |
| 40 kg | 0.25 | 0.25 | 0.00 | 0.00 | 15.5 | 0.00 | 0.59 | 0.25 | 0.06 | 0.09 | 0.94 |
| 60 kg | 0.25 | 0.17 | 0.17 | 0.08 | 20.7 | 0.00 | 0.58 | 0.49 | 0.20 | 0.29 | 0.85 |
| 80 kg | 0.42 | 0.17 | 0.00 | 0.00 | 39.4 | 0.02 | 0.68 | 0.50 | 0.32 | 0.43 | 0.76 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cylinder | part 0 corner -x+y + part 0 corner -x-y | 0.17 | 0.25 | 0.25 | 0.42 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.17 | 0.75 | 0.08 | 0.00 | 0.00 | 0.25 | 4.58 |
| 40 kg | 0.25 | 0.75 | 0.00 | 0.00 | 0.00 | 0.00 | 3.67 |
| 60 kg | 0.25 | 0.50 | 0.25 | 0.00 | 0.00 | 0.00 | 5.00 |
| 80 kg | 0.42 | 0.58 | 0.00 | 0.00 | 0.00 | 0.00 | 5.67 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.19 | 0.81 | 0.91 | 0.00 | 1.00 | 0.15 | 0.86 | 0.93 | 0.00 |
| 40 kg | 1.00 | 0.17 | 0.82 | 0.95 | 0.00 | 1.00 | 0.12 | 0.91 | 0.96 | 0.00 |
| 60 kg | 1.00 | 0.18 | 0.82 | 0.93 | 0.00 | 1.00 | 0.16 | 0.85 | 0.94 | 0.00 |
| 80 kg | 1.00 | 0.19 | 0.80 | 0.95 | 0.00 | 1.00 | 0.17 | 0.86 | 0.97 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.68 | 2.12 | 0.05 | 0.74 | 1.89 | 0.02 |
| 40 kg | 0.75 | 2.45 | 0.05 | 0.76 | 1.70 | 0.04 |
| 60 kg | 0.73 | 2.62 | 0.07 | 0.72 | 2.44 | 0.10 |
| 80 kg | 0.75 | 3.19 | 0.09 | 0.81 | 1.90 | 0.05 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.70 | 0.71 | 0.20 |
| 40 kg | 0.71 | 0.68 | 0.19 |
| 60 kg | 0.69 | 0.62 | 0.20 |
| 80 kg | 0.64 | 0.61 | 0.22 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.39 | 0.64 | 31.19 | 4.58 | 1.75 | 0.00 | 17.17 | 0.00 | 0.19 |
| 40 kg | 0.06 | 0.62 | 27.85 | 3.67 | 0.08 | 1.75 | 22.92 | 0.00 | 0.14 |
| 60 kg | 0.03 | 0.53 | 31.17 | 5.00 | 1.67 | 0.00 | 10.33 | 0.00 | 0.24 |
| 80 kg | 0.19 | 0.53 | 43.13 | 5.67 | 0.08 | 4.25 | 5.17 | 0.00 | 0.15 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 108 | 252 | 214 |
| 40 kg | 150 | 317 | 234 |
| 60 kg | 152 | 333 | 282 |
| 80 kg | 170 | 372 | 312 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 263 | 0.32 | 0.15 (1) | 0.53 (52) | 0.48 (132) | 0.49 (70) | 0.70 (7) |
| 40 kg | 361 | 0.33 | 0.44 (68) | 0.51 (14) | 0.52 (62) | 0.52 (179) | 0.83 (40) |
| 60 kg | 219 | 0.33 | 0.44 (32) | 0.46 (16) | 0.59 (67) | 0.59 (65) | 0.82 (39) |
| 80 kg | 192 | 0.36 | 0.28 (0) | 0.53 (4) | 0.62 (116) | 0.80 (50) | 0.83 (22) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cylinder | 0.04 | 0.06 | 0.20 | 0.32 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.00 | 0.00 | 0.67 | 1.00 |
| B_left | 0.33 | 0.33 | 0.00 | 0.33 |
| C_backright | 0.33 | 0.33 | 0.33 | 0.33 |
| D_far_turn | 0.00 | 0.33 | 0.00 | 0.00 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 23% | 0% | 77% | 33% | 3% | 64% |  |  | 10% | 68% | 47% | 23% |
| 40 kg | 19% | 0% | 81% | 44% | 2% | 54% |  |  | 11% | 65% | 36% | 16% |
| 60 kg | 25% | 0% | 75% | 37% | 3% | 60% |  |  | 15% | 64% | 40% | 28% |
| 80 kg | 21% | 0% | 79% | 32% | 2% | 66% |  |  | 15% | 80% | 26% | 28% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 141 | 0.91 | 5% | 16% | 26% | 58% |
| 40 kg | 178 | 0.91 | 4% | 22% | 37% | 41% |
| 60 kg | 190 | 0.90 | 7% | 15% | 41% | 44% |
| 80 kg | 214 | 0.90 | 8% | 11% | 41% | 47% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 59% | 0.15 | 0.28 | 0.11 | 0.75 | 3 | 0 | 3 | 0 | 0 | 0 | 181 | 0.00 |  |
| 40 kg | 63% | 0.14 | 0.37 | 0.10 | 0.50 | 7 | 0 | 7 | 0 | 0 | 0 | 88 | 0.00 |  |
| 60 kg | 64% | 0.12 | 0.49 | 0.09 | 0.50 | 2 | 0 | 2 | 0 | 0 | 0 | 89 | 0.00 |  |
| 80 kg | 58% | 0.09 | 0.56 | 0.07 | 0.50 | 2 | 0 | 1 | 0 | 0 | 1 |  | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cylinder | 0.27 | 37% | 16% | 0.91 | 61% | 0.09 | 4 | 0 | 3 | 0 | 0 | 0 |
