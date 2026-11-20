# Pair evaluation: cyl-roll0.2-7500-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto); planner settings changed: roll_ratio=0.2

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.58 | 0.25 | 0.00 | 0.00 | 18.9 | 0.01 | 0.42 | 0.50 | 0.16 | 0.26 | 0.84 |
| 40 kg | 0.25 | 0.17 | 0.17 | 0.08 | 27.3 | 0.00 | 0.52 | 0.42 | 0.12 | 0.17 | 0.99 |
| 60 kg | 0.25 | 0.08 | 0.25 | 0.00 | 40.0 | 0.02 | 0.63 | 0.40 | 0.19 | 0.26 | 0.85 |
| 80 kg | 0.33 | 0.33 | 0.17 | 0.08 | 31.1 | 0.01 | 0.76 | 0.56 | 0.45 | 0.56 | 0.83 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cylinder | part 0 corner -x-y + part 0 corner -x+y | 0.58 | 0.25 | 0.25 | 0.33 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.58 | 0.42 | 0.00 | 0.00 | 0.00 | 0.00 | 5.83 |
| 40 kg | 0.25 | 0.50 | 0.25 | 0.00 | 0.00 | 0.08 | 3.83 |
| 60 kg | 0.25 | 0.50 | 0.25 | 0.00 | 0.00 | 0.08 | 4.17 |
| 80 kg | 0.33 | 0.42 | 0.25 | 0.00 | 0.00 | 0.00 | 4.50 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.22 | 0.75 | 0.94 | 0.00 | 1.00 | 0.20 | 0.78 | 0.91 | 0.00 |
| 40 kg | 1.00 | 0.19 | 0.76 | 0.96 | 0.00 | 1.00 | 0.16 | 0.84 | 0.96 | 0.00 |
| 60 kg | 1.00 | 0.22 | 0.71 | 0.95 | 0.00 | 1.00 | 0.19 | 0.75 | 0.96 | 0.00 |
| 80 kg | 1.00 | 0.20 | 0.73 | 0.96 | 0.00 | 1.00 | 0.19 | 0.85 | 0.96 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.76 | 2.26 | 0.04 | 0.70 | 2.00 | 0.04 |
| 40 kg | 0.70 | 1.98 | 0.09 | 0.65 | 1.96 | 0.10 |
| 60 kg | 0.72 | 1.67 | 0.16 | 0.74 | 1.59 | 0.11 |
| 80 kg | 0.70 | 2.06 | 0.17 | 0.69 | 1.32 | 0.07 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.61 | 0.60 | 0.22 |
| 40 kg | 0.69 | 0.67 | 0.23 |
| 60 kg | 0.62 | 0.57 | 0.20 |
| 80 kg | 0.59 | 0.63 | 0.19 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.19 | 0.45 | 28.22 | 5.83 | 5.50 | 0.00 | 15.92 | 0.00 | 0.22 |
| 40 kg | 0.04 | 0.62 | 24.39 | 3.83 | 1.33 | 0.00 | 15.83 | 0.00 | 0.21 |
| 60 kg | 0.00 | 0.50 | 27.36 | 4.17 | 0.00 | 0.00 | 13.58 | 0.00 | 0.26 |
| 80 kg | 0.00 | 0.48 | 35.18 | 4.50 | 2.92 | 1.58 | 3.50 | 0.00 | 0.24 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 93 | 248 | 188 |
| 40 kg | 135 | 295 | 241 |
| 60 kg | 153 | 310 | 264 |
| 80 kg | 138 | 335 | 292 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 103 | 0.37 | 0.46 (45) | 0.51 (26) | 0.47 (11) | 0.55 (14) | 0.80 (7) |
| 40 kg | 244 | 0.35 | 0.38 (70) | 0.44 (11) | 0.55 (79) | 0.54 (29) | 0.56 (54) |
| 60 kg | 285 | 0.38 | 0.49 (104) | 0.35 (17) | 0.57 (49) | 0.67 (73) | 0.66 (42) |
| 80 kg | 157 | 0.38 | 0.36 (3) | 0.35 (3) | 0.62 (68) | 0.66 (63) | 0.75 (21) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cylinder | 0.16 | 0.12 | 0.19 | 0.45 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.33 | 0.00 | 0.33 | 1.00 |
| B_left | 1.00 | 0.67 | 0.33 | 0.33 |
| C_backright | 0.67 | 0.33 | 0.33 | 0.00 |
| D_far_turn | 0.33 | 0.00 | 0.00 | 0.00 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 29% | 0% | 71% | 25% | 4% | 71% |  |  | 14% | 81% | 27% | 22% |
| 40 kg | 27% | 0% | 73% | 41% | 3% | 56% |  |  | 19% | 67% | 40% | 25% |
| 60 kg | 32% | 0% | 68% | 46% | 3% | 51% |  |  | 25% | 81% | 27% | 31% |
| 80 kg | 26% | 0% | 74% | 35% | 3% | 62% |  |  | 19% | 89% | 15% | 33% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 139 | 0.91 | 6% | 8% | 27% | 65% |
| 40 kg | 173 | 0.91 | 6% | 20% | 37% | 44% |
| 60 kg | 183 | 0.89 | 8% | 23% | 43% | 34% |
| 80 kg | 189 | 0.86 | 13% | 15% | 40% | 45% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 61% | 0.19 | 0.45 | 0.14 | 0.33 | 2 | 0 | 2 | 0 | 0 | 0 |  | 0.00 |  |
| 40 kg | 61% | 0.15 | 0.45 | 0.12 | 0.92 | 5 | 0 | 5 | 0 | 0 | 1 |  | 0.00 |  |
| 60 kg | 69% | 0.15 | 0.58 | 0.13 | 0.00 | 0 | 0 | 0 | 0 | 0 | 0 |  | 0.00 |  |
| 80 kg | 63% | 0.10 | 0.63 | 0.09 | 0.17 | 1 | 0 | 0 | 0 | 0 | 0 |  | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cylinder | 0.35 | 37% | 17% | 0.89 | 63% | 0.12 | 2 | 0 | 2 | 0 | 0 | 0 |
