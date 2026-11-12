# Pair evaluation: smoke-coord-par-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 2 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.79 | 0.75 | 0.00 | 0.00 | 24.2 | 0.01 | 0.40 | 0.42 | 0.12 | 0.22 | 1.45 |
| 40 kg | 0.75 | 0.58 | 0.00 | 0.04 | 37.6 | 0.00 | 0.47 | 0.36 | 0.12 | 0.18 | 1.42 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg |
|---|---|---|---|
| long | part 0 -x seg 1/2 + part 0 corner -x+y | 0.75 | 0.75 |
| arch | part 2 -x + part 3 -x | 0.88 | 0.88 |
| dumbbell | part 0 -x + part 1 -x | 0.75 | 0.62 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.79 | 0.21 | 0.00 | 0.00 | 0.00 | 0.00 | 11.17 |
| 40 kg | 0.75 | 0.21 | 0.04 | 0.00 | 0.00 | 0.00 | 9.08 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.25 | 0.71 | 0.86 | 0.00 | 1.00 | 0.27 | 0.71 | 0.82 | 0.00 |
| 40 kg | 1.00 | 0.20 | 0.80 | 0.92 | 0.00 | 1.00 | 0.31 | 0.71 | 0.82 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.81 | 1.94 | 0.08 | 0.83 | 1.86 | 0.06 |
| 40 kg | 0.85 | 2.10 | 0.06 | 0.83 | 2.09 | 0.06 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.51 | 0.59 | 0.34 |
| 40 kg | 0.65 | 0.55 | 0.32 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.25 | 0.50 | 24.73 | 11.17 | 0.17 | 1.33 | 9.00 | 0.00 | 0.23 |
| 40 kg | 6.39 | 0.44 | 28.13 | 9.08 | 0.00 | 0.83 | 4.42 | 0.00 | 0.25 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 108 | 278 | 209 |
| 40 kg | 143 | 323 | 239 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 231 | 0.34 | 0.45 (39) | 0.53 (33) | 0.53 (95) | 0.51 (42) | 0.58 (22) |
| 40 kg | 280 | 0.31 | 0.32 (134) | 0.49 (28) | 0.54 (33) | 0.54 (25) | 0.78 (60) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg |
|---|---|---|
| long | 0.10 | 0.07 |
| arch | 0.15 | 0.17 |
| dumbbell | 0.11 | 0.12 |

## success by scenario and mass

| scenario | 20 kg | 40 kg |
|---|---|---|
| A_straight | 1.00 | 0.83 |
| B_left | 0.67 | 1.00 |
| C_backright | 0.83 | 0.83 |
| D_far_turn | 0.67 | 0.33 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 36% | 0% | 64% | 43% | 4% | 52% |  |  | 15% | 57% | 46% | 21% |
| 40 kg | 29% | 0% | 71% | 47% | 2% | 50% |  |  | 13% | 66% | 44% | 18% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 148 | 0.85 | 10% | 16% | 34% | 49% |
| 40 kg | 175 | 0.88 | 8% | 19% | 42% | 39% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 62% | 0.20 | 0.45 | 0.16 | 0.71 | 6 | 0 | 5 | 0 | 0 | 1 | 55 | 0.00 |  |
| 40 kg | 57% | 0.13 | 0.60 | 0.11 | 0.58 | 6 | 0 | 4 | 0 | 0 | 1 | 78 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| long | 0.75 | 54% | 24% | 0.91 | 66% | 0.12 | 1 | 0 | 0 | 0 | 0 | 0 |
| arch | 0.88 | 46% | 17% | 0.80 | 63% | 0.17 | 7 | 0 | 6 | 0 | 0 | 1 |
| dumbbell | 0.69 | 36% | 12% | 0.90 | 50% | 0.11 | 10 | 0 | 7 | 0 | 0 | 2 |
