# Pair evaluation: cyl-roll0.1-7100-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto); planner settings changed: roll_ratio=0.1

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.58 | 0.50 | 0.00 | 0.00 | 14.4 | 0.01 | 0.51 | 0.31 | 0.07 | 0.11 | 0.88 |
| 40 kg | 0.17 | 0.17 | 0.00 | 0.00 | 24.9 | 0.00 | 0.55 | 0.41 | 0.06 | 0.08 | 0.98 |
| 60 kg | 0.42 | 0.17 | 0.00 | 0.00 | 41.0 | 0.02 | 0.63 | 0.43 | 0.23 | 0.31 | 0.80 |
| 80 kg | 0.33 | 0.17 | 0.25 | 0.08 | 37.2 | 0.02 | 0.63 | 0.46 | 0.26 | 0.36 | 0.79 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cylinder | part 0 corner -x+y + part 0 corner -x-y | 0.58 | 0.17 | 0.42 | 0.33 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.58 | 0.42 | 0.00 | 0.00 | 0.00 | 0.08 | 5.58 |
| 40 kg | 0.17 | 0.83 | 0.00 | 0.00 | 0.00 | 0.08 | 4.42 |
| 60 kg | 0.42 | 0.58 | 0.00 | 0.00 | 0.00 | 0.00 | 5.08 |
| 80 kg | 0.33 | 0.33 | 0.33 | 0.00 | 0.00 | 0.00 | 4.92 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.22 | 0.71 | 0.90 | 0.00 | 1.00 | 0.21 | 0.77 | 0.87 | 0.00 |
| 40 kg | 1.00 | 0.13 | 0.92 | 0.95 | 0.00 | 1.00 | 0.13 | 0.89 | 0.96 | 0.00 |
| 60 kg | 1.00 | 0.16 | 0.88 | 0.95 | 0.00 | 1.00 | 0.18 | 0.82 | 0.96 | 0.00 |
| 80 kg | 1.00 | 0.23 | 0.72 | 0.87 | 0.00 | 1.00 | 0.23 | 0.73 | 0.94 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.72 | 1.99 | 0.04 | 0.70 | 1.69 | 0.03 |
| 40 kg | 0.68 | 2.33 | 0.03 | 0.75 | 1.83 | 0.03 |
| 60 kg | 0.78 | 1.60 | 0.06 | 0.74 | 2.37 | 0.04 |
| 80 kg | 0.73 | 2.29 | 0.15 | 0.74 | 1.95 | 0.10 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.65 | 0.57 | 0.20 |
| 40 kg | 0.84 | 0.75 | 0.21 |
| 60 kg | 0.73 | 0.56 | 0.23 |
| 80 kg | 0.56 | 0.49 | 0.22 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.09 | 0.47 | 20.38 | 5.58 | 2.17 | 0.00 | 23.08 | 0.00 | 0.24 |
| 40 kg | 0.05 | 0.73 | 28.72 | 4.42 | 2.00 | 0.08 | 20.92 | 0.00 | 0.13 |
| 60 kg | 0.43 | 0.49 | 36.52 | 5.08 | 1.00 | 0.42 | 13.25 | 0.00 | 0.15 |
| 80 kg | 0.16 | 0.38 | 31.62 | 4.92 | 0.00 | 2.08 | 2.67 | 0.00 | 0.31 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 92 | 238 | 186 |
| 40 kg | 142 | 287 | 255 |
| 60 kg | 155 | 340 | 267 |
| 80 kg | 172 | 390 | 332 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 134 | 0.34 | 0.55 (4) | 0.53 (10) | 0.54 (82) | 0.52 (29) | 0.94 (10) |
| 40 kg | 412 | 0.36 | 0.52 (86) | 0.49 (22) | 0.61 (96) | 0.52 (180) | 0.95 (28) |
| 60 kg | 187 | 0.33 | 0.28 (18) | 0.59 (21) | 0.56 (66) | 0.85 (61) | 0.91 (21) |
| 80 kg | 122 | 0.37 | 0.51 (1) | 0.60 (9) | 0.58 (69) | 0.73 (40) | 0.89 (4) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cylinder | 0.07 | 0.06 | 0.23 | 0.26 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.67 | 0.00 | 0.67 | 1.00 |
| B_left | 1.00 | 0.33 | 0.33 | 0.00 |
| C_backright | 0.67 | 0.33 | 0.33 | 0.33 |
| D_far_turn | 0.00 | 0.00 | 0.33 | 0.00 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 33% | 0% | 67% | 30% | 4% | 66% |  |  | 15% | 56% | 63% | 16% |
| 40 kg | 16% | 0% | 84% | 46% | 3% | 51% |  |  | 9% | 44% | 61% | 19% |
| 60 kg | 19% | 0% | 81% | 35% | 3% | 62% |  |  | 12% | 74% | 40% | 22% |
| 80 kg | 33% | 0% | 67% | 36% | 2% | 62% |  |  | 21% | 84% | 28% | 28% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 131 | 0.93 | 3% | 8% | 28% | 64% |
| 40 kg | 170 | 0.92 | 3% | 22% | 38% | 40% |
| 60 kg | 194 | 0.90 | 7% | 10% | 44% | 46% |
| 80 kg | 213 | 0.89 | 8% | 13% | 41% | 47% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 64% | 0.21 | 0.45 | 0.17 | 0.92 | 7 | 0 | 7 | 0 | 0 | 0 |  | 0.00 |  |
| 40 kg | 59% | 0.09 | 0.31 | 0.06 | 0.58 | 3 | 0 | 3 | 0 | 0 | 0 | 95 | 0.00 |  |
| 60 kg | 57% | 0.08 | 0.55 | 0.07 | 0.67 | 3 | 0 | 3 | 0 | 0 | 0 | 197 | 0.00 |  |
| 80 kg | 57% | 0.11 | 0.64 | 0.09 | 0.50 | 2 | 0 | 1 | 0 | 0 | 0 |  | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cylinder | 0.38 | 37% | 13% | 0.91 | 59% | 0.10 | 3 | 0 | 3 | 0 | 0 | 0 |
