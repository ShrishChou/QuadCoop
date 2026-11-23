# Pair evaluation: turn-swap-turn-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto); TASKS: turn in place (object at the goal position, heading off 15/30/60/90 deg, capped by symmetry); ACTORS SWAPPED (each robot runs the other's trained network)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 10 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 60 kg | 0.55 | 0.33 | 0.03 | 0.03 | 32.6 | 0.27 | 0.18 | 0.08 | 0.01 | 0.03 | 0.86 |
| 80 kg | 0.47 | 0.05 | 0.05 | 0.05 | 29.3 | 0.23 | 0.22 | 0.11 | 0.01 | 0.02 | 1.13 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 60 kg | 80 kg |
|---|---|---|---|
| long |  | 0.55 | 0.47 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 60 kg | 0.55 | 0.40 | 0.05 | 0.00 | 0.00 | 0.07 | 5.40 |
| 80 kg | 0.47 | 0.42 | 0.10 | 0.00 | 0.00 | 0.00 | 5.42 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 60 kg | 1.00 | 0.58 | 0.47 | 0.64 | 0.00 | 1.00 | 0.42 | 0.60 | 0.73 | 0.00 |
| 80 kg | 1.00 | 0.45 | 0.56 | 0.74 | 0.00 | 1.00 | 0.40 | 0.65 | 0.76 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 60 kg | 0.69 | 8.53 | 0.05 | 0.79 | 9.90 | 0.07 |
| 80 kg | 0.76 | 8.23 | 0.03 | 0.80 | 7.13 | 0.07 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 60 kg | 0.29 | 0.32 | 0.20 |
| 80 kg | 0.39 | 0.35 | 0.14 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 60 kg | 2.18 | 0.15 | 18.97 | 5.40 | 0.25 | 0.00 | 9.15 | 0.00 | 0.36 |
| 80 kg | 1.00 | 0.30 | 17.93 | 5.42 | 0.00 | 0.00 | 12.20 | 0.00 | 0.25 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 60 kg | 192 | 318 | 301 |
| 80 kg | 196 | 338 | 331 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 60 kg | 208 | 0.41 | 0.53 (2) | 0.51 (85) | 0.40 (49) | 0.48 (14) | 0.49 (57) |
| 80 kg | 411 | 0.37 | 0.51 (3) | 0.58 (3) | 0.54 (319) | 0.38 (71) | 0.48 (16) |

## both robots pushing (share of time) by object and mass

| object | 60 kg | 80 kg |
|---|---|---|
| long | 0.01 | 0.01 |

## success by scenario and mass

| scenario | 60 kg | 80 kg |
|---|---|---|
| T15 | 0.70 | 0.70 |
| T30 | 0.70 | 0.70 |
| T60 | 0.50 | 0.50 |
| T90 | 0.30 | 0.00 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 60 kg | 52% | 0% | 48% | 58% | 1% | 41% |  |  | 15% | 41% | 61% | 30% |
| 80 kg | 44% | 0% | 56% | 60% | 1% | 39% |  |  | 15% | 58% | 44% | 25% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 60 kg | 190 | 0.87 | 13% | 19% | 31% | 50% |
| 80 kg | 203 | 0.89 | 10% | 22% | 33% | 45% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 60 kg | 18% | 0.01 | -0.35 | 0.00 | 1.30 | 17 | 0 | 3 | 0 | 0 | 14 | 135 | 0.00 |  |
| 80 kg | 11% | 0.01 | -0.29 | 0.00 | 2.55 | 26 | 2 | 9 | 0 | 0 | 14 | 140 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| long | 0.51 | 59% | 20% | 0.88 | 14% | 0.00 | 22 | 1 | 6 | 0 | 0 | 14 |
