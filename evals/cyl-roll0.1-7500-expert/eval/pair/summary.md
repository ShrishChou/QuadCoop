# Pair evaluation: cyl-roll0.1-7500-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto); planner settings changed: roll_ratio=0.1

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.33 | 0.50 | 0.08 | 0.00 | 15.1 | 0.00 | 0.50 | 0.40 | 0.11 | 0.16 | 0.87 |
| 40 kg | 0.17 | 0.17 | 0.00 | 0.08 | 38.1 | 0.00 | 0.64 | 0.36 | 0.08 | 0.10 | 0.92 |
| 60 kg | 0.33 | 0.17 | 0.25 | 0.00 | 39.5 | 0.02 | 0.67 | 0.41 | 0.22 | 0.29 | 0.90 |
| 80 kg | 0.08 | 0.08 | 0.08 | 0.17 | 27.3 | 0.01 | 0.64 | 0.59 | 0.37 | 0.49 | 0.84 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cylinder | part 0 corner -x-y + part 0 corner -x+y | 0.33 | 0.17 | 0.33 | 0.08 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.33 | 0.58 | 0.08 | 0.00 | 0.00 | 0.08 | 4.75 |
| 40 kg | 0.17 | 0.75 | 0.08 | 0.00 | 0.00 | 0.08 | 3.75 |
| 60 kg | 0.33 | 0.42 | 0.25 | 0.00 | 0.00 | 0.00 | 3.67 |
| 80 kg | 0.08 | 0.67 | 0.25 | 0.00 | 0.00 | 0.00 | 3.50 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.18 | 0.84 | 0.94 | 0.00 | 1.00 | 0.15 | 0.86 | 0.92 | 0.00 |
| 40 kg | 1.00 | 0.16 | 0.87 | 0.96 | 0.00 | 1.00 | 0.12 | 0.91 | 0.96 | 0.00 |
| 60 kg | 1.00 | 0.23 | 0.70 | 0.85 | 0.00 | 1.00 | 0.20 | 0.73 | 0.95 | 0.00 |
| 80 kg | 1.00 | 0.27 | 0.68 | 0.74 | 0.00 | 1.00 | 0.19 | 0.81 | 0.94 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.74 | 1.72 | 0.02 | 0.71 | 1.44 | 0.03 |
| 40 kg | 0.71 | 2.84 | 0.03 | 0.73 | 1.40 | 0.03 |
| 60 kg | 0.68 | 2.89 | 0.16 | 0.79 | 1.72 | 0.15 |
| 80 kg | 0.61 | 2.41 | 0.14 | 0.72 | 1.63 | 0.10 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.77 | 0.70 | 0.20 |
| 40 kg | 0.84 | 0.79 | 0.16 |
| 60 kg | 0.61 | 0.49 | 0.18 |
| 80 kg | 0.46 | 0.50 | 0.17 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.28 | 0.61 | 28.16 | 4.75 | 3.08 | 0.00 | 16.33 | 0.00 | 0.16 |
| 40 kg | 0.12 | 0.75 | 26.75 | 3.75 | 0.00 | 0.00 | 22.67 | 0.00 | 0.11 |
| 60 kg | 0.06 | 0.43 | 24.70 | 3.67 | 1.33 | 0.00 | 10.25 | 0.00 | 0.32 |
| 80 kg | 0.00 | 0.38 | 40.10 | 3.50 | 3.25 | 4.17 | 2.08 | 0.00 | 0.30 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 102 | 248 | 190 |
| 40 kg | 145 | 297 | 248 |
| 60 kg | 167 | 322 | 308 |
| 80 kg | 133 | 330 | 286 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 249 | 0.33 | 0.39 (6) | 0.44 (27) | 0.49 (120) | 0.48 (79) | 0.70 (17) |
| 40 kg | 411 | 0.35 | 0.41 (102) | 0.48 (17) | 0.53 (134) | 0.51 (123) | 0.73 (34) |
| 60 kg | 239 | 0.35 | 0.46 (64) | 0.41 (29) | 0.51 (45) | 0.64 (69) | 0.65 (33) |
| 80 kg | 168 | 0.39 | - | 0.37 (2) | 0.55 (113) | 0.54 (50) | 0.83 (2) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cylinder | 0.11 | 0.08 | 0.22 | 0.37 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.00 | 0.00 | 0.33 | 0.33 |
| B_left | 0.67 | 0.33 | 0.33 | 0.00 |
| C_backright | 0.67 | 0.33 | 0.67 | 0.00 |
| D_far_turn | 0.00 | 0.00 | 0.00 | 0.00 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 21% | 0% | 79% | 34% | 4% | 62% |  |  | 10% | 57% | 49% | 18% |
| 40 kg | 15% | 0% | 85% | 49% | 4% | 47% |  |  | 6% | 61% | 53% | 14% |
| 60 kg | 36% | 0% | 64% | 44% | 2% | 54% |  |  | 29% | 74% | 33% | 26% |
| 80 kg | 36% | 0% | 64% | 33% | 3% | 64% |  |  | 26% | 87% | 17% | 29% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 141 | 0.92 | 3% | 15% | 30% | 55% |
| 40 kg | 172 | 0.92 | 3% | 24% | 41% | 35% |
| 60 kg | 193 | 0.92 | 4% | 24% | 43% | 34% |
| 80 kg | 188 | 0.84 | 13% | 13% | 36% | 51% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 62% | 0.15 | 0.32 | 0.10 | 1.08 | 5 | 0 | 5 | 0 | 0 | 0 | 36 | 0.00 |  |
| 40 kg | 63% | 0.10 | 0.27 | 0.06 | 0.33 | 3 | 0 | 3 | 0 | 0 | 0 |  | 0.00 |  |
| 60 kg | 68% | 0.14 | 0.62 | 0.12 | 0.33 | 4 | 0 | 2 | 0 | 0 | 2 |  | 0.00 |  |
| 80 kg | 55% | 0.09 | 0.63 | 0.08 | 0.83 | 5 | 0 | 1 | 0 | 0 | 4 |  | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cylinder | 0.23 | 40% | 19% | 0.90 | 62% | 0.09 | 4 | 0 | 3 | 0 | 0 | 2 |
