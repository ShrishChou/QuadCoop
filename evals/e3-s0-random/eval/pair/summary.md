# Pair evaluation: e3-s0-random

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start at their contacts; contact rule re-applied: never)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 5 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.04 | 0.04 | 0.00 | 0.03 | 6.4 | 0.02 | 0.16 | 0.13 | 0.04 | 0.18 | 0.82 |
| 80 kg | 0.01 | 0.01 | 0.04 | 0.05 | 21.0 | 0.02 | 0.46 | 0.45 | 0.21 | 0.30 | 0.86 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 80 kg |
|---|---|---|---|
| cube | part 0 corner -x-y + part 0 -x end + | 0.05 | 0.00 |
| long | part 0 -x seg 2/2 + part 0 corner -x-y | 0.05 | 0.00 |
| arch | part 3 -x + part 2 -x | 0.05 | 0.05 |
| asym (unseen) | part 0 corner -x+y + part 1 corner -x-y | 0.00 | 0.00 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.04 | 0.94 | 0.03 | 0.00 | 0.00 | 0.14 | 0.00 |
| 80 kg | 0.01 | 0.90 | 0.09 | 0.00 | 0.00 | 0.00 | 0.00 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.20 | 0.73 | 0.93 | 0.00 | 1.00 | 0.18 | 0.80 | 0.95 | 0.00 |
| 80 kg | 1.00 | 0.25 | 0.70 | 0.97 | 0.00 | 1.00 | 0.15 | 0.85 | 0.99 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.02 | 0.02 | 1.00 | 0.02 | 0.03 |
| 80 kg | 1.00 | 0.02 | 0.06 | 1.00 | 0.02 | 0.06 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.49 | 0.42 | 0.90 |
| 80 kg | 0.51 | 0.61 | 0.55 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.92 | 0.29 | 28.44 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.39 |
| 80 kg | 1.29 | 0.38 | 28.63 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.30 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 84 | 254 | 146 |
| 80 kg | 213 | 390 | 359 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 170 | 0.34 | 0.36 (33) | 0.54 (12) | 0.51 (25) | 0.56 (25) | 0.72 (75) |
| 80 kg | 1351 | 0.32 | 0.34 (288) | 0.52 (137) | 0.51 (147) | 0.44 (191) | 0.72 (589) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 80 kg |
|---|---|---|
| cube | 0.03 | 0.10 |
| long | 0.05 | 0.27 |
| arch | 0.03 | 0.12 |
| asym | 0.05 | 0.34 |

## success by scenario and mass

| scenario | 20 kg | 80 kg |
|---|---|---|
| A_straight | 0.05 | 0.05 |
| B_left | 0.05 | 0.00 |
| C_backright | 0.05 | 0.00 |
| D_far_turn | 0.00 | 0.00 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 32% | 0% | 68% | 14% | 2% | 84% |  |  | 32% | 69% | 53% | 21% |
| 80 kg | 25% | 0% | 75% | 52% | 2% | 46% |  |  | 25% | 81% | 29% | 25% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 128 | 0.85 | 11% | 2% | 14% | 83% |
| 80 kg | 231 | 0.91 | 5% | 19% | 51% | 30% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 19% | 0.07 | 0.48 | 0.06 | 3.05 | 45 | 0 | 39 | 0 | 0 | 6 | 78 | 0.00 |  |
| 80 kg | 33% | 0.03 | 0.73 | 0.03 | 0.80 | 7 | 0 | 6 | 0 | 0 | 1 | 138 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.03 | 24% | 4% | 0.93 | 22% | 0.04 | 35 | 0 | 32 | 0 | 0 | 3 |
| long | 0.03 | 29% | 11% | 0.91 | 31% | 0.05 | 21 | 0 | 20 | 0 | 0 | 0 |
| arch | 0.05 | 40% | 15% | 0.76 | 29% | 0.05 | 28 | 0 | 23 | 0 | 0 | 4 |
| asym | 0.00 | 39% | 12% | 0.92 | 23% | 0.02 | 20 | 0 | 14 | 0 | 0 | 5 |
