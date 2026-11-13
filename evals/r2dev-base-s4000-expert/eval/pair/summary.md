# Pair evaluation: r2dev-base-s4000-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.75 | 0.58 | 0.00 | 0.00 | 34.5 | 0.00 | 0.34 | 0.45 | 0.08 | 0.13 | 1.57 |
| 40 kg | 0.33 | 0.17 | 0.33 | 0.00 | 34.0 | 0.00 | 0.54 | 0.48 | 0.23 | 0.31 | 1.48 |
| 60 kg | 0.08 | 0.08 | 0.50 | 0.00 | 76.0 | 0.02 | 0.77 | 0.41 | 0.29 | 0.33 | 1.31 |
| 80 kg | 0.00 | 0.00 | 0.58 | 0.08 |  | 0.00 | 0.85 | 0.61 | 0.56 | 0.63 | 1.36 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| beam (unseen) | part 0 -x seg 5/5 + part 0 -x seg 1/5 | 0.75 | 0.33 | 0.08 | 0.00 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.75 | 0.25 | 0.00 | 0.00 | 0.00 | 0.00 | 6.83 |
| 40 kg | 0.33 | 0.33 | 0.33 | 0.00 | 0.00 | 0.00 | 4.83 |
| 60 kg | 0.08 | 0.42 | 0.50 | 0.00 | 0.00 | 0.00 | 3.00 |
| 80 kg | 0.00 | 0.33 | 0.67 | 0.00 | 0.00 | 0.00 | 2.50 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.30 | 0.63 | 0.92 | 0.00 | 1.00 | 0.42 | 0.54 | 0.86 | 0.00 |
| 40 kg | 1.00 | 0.31 | 0.59 | 0.94 | 0.00 | 1.00 | 0.30 | 0.61 | 0.93 | 0.00 |
| 60 kg | 1.00 | 0.28 | 0.60 | 0.96 | 0.00 | 1.00 | 0.32 | 0.50 | 0.94 | 0.00 |
| 80 kg | 1.00 | 0.32 | 0.48 | 0.96 | 0.00 | 1.00 | 0.35 | 0.30 | 0.96 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.89 | 2.17 | 0.06 | 0.89 | 2.98 | 0.07 |
| 40 kg | 0.88 | 1.83 | 0.14 | 0.83 | 1.92 | 0.13 |
| 60 kg | 0.86 | 1.92 | 0.24 | 0.82 | 2.86 | 0.22 |
| 80 kg | 0.79 | 1.65 | 0.31 | 0.79 | 2.39 | 0.45 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.49 | 0.47 | 0.28 |
| 40 kg | 0.52 | 0.47 | 0.32 |
| 60 kg | 0.53 | 0.47 | 0.27 |
| 80 kg | 0.43 | 0.28 | 0.15 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.73 | 0.37 | 34.82 | 6.83 | 0.08 | 0.00 | 8.08 | 0.00 | 0.41 |
| 40 kg | 0.16 | 0.37 | 30.58 | 4.83 | 0.25 | 0.08 | 1.58 | 0.00 | 0.35 |
| 60 kg | 0.04 | 0.39 | 40.50 | 3.00 | 3.33 | 0.08 | 0.17 | 0.00 | 0.41 |
| 80 kg | 0.25 | 0.21 | 31.38 | 2.50 | 0.00 | 0.08 | 0.00 | 0.00 | 0.60 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 88 | 188 | 130 |
| 40 kg | 115 | 232 | 182 |
| 60 kg | 108 | 233 | 200 |
| 80 kg | 123 | 238 | 227 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 87 | 0.41 | 0.35 (12) | 0.59 (9) | 0.59 (8) | 0.46 (27) | 0.55 (32) |
| 40 kg | 91 | 0.33 | 0.53 (25) | 0.75 (13) | 0.68 (13) | 0.66 (5) | 0.93 (34) |
| 60 kg | 152 | 0.34 | 0.48 (10) | 0.55 (24) | 0.57 (12) | 0.55 (52) | 0.78 (54) |
| 80 kg | 54 | 0.43 | - | 0.70 (12) | 0.80 (33) | 0.73 (6) | 0.56 (3) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| beam | 0.08 | 0.23 | 0.29 | 0.56 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.33 | 0.33 | 0.00 | 0.00 |
| B_left | 1.00 | 0.67 | 0.33 | 0.00 |
| C_backright | 1.00 | 0.33 | 0.00 | 0.00 |
| D_far_turn | 0.67 | 0.00 | 0.00 | 0.00 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 45% | 0% | 55% | 29% | 3% | 68% |  |  | 28% | 94% | 15% | 27% |
| 40 kg | 43% | 0% | 57% | 34% | 2% | 64% |  |  | 32% | 89% | 14% | 44% |
| 60 kg | 47% | 0% | 53% | 46% | 4% | 50% |  |  | 41% | 93% | 10% | 51% |
| 80 kg | 64% | 0% | 36% | 53% | 3% | 44% |  |  | 59% | 94% | 13% | 57% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 112 | 0.87 | 10% | 7% | 28% | 65% |
| 40 kg | 139 | 0.85 | 15% | 11% | 40% | 50% |
| 60 kg | 140 | 0.77 | 21% | 21% | 49% | 30% |
| 80 kg | 147 | 0.83 | 17% | 33% | 42% | 24% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 39% | 0.16 | 0.49 | 0.12 | 2.50 | 15 | 0 | 12 | 0 | 0 | 3 | 47 | 0.00 |  |
| 40 kg | 38% | 0.12 | 0.65 | 0.10 | 1.83 | 10 | 0 | 8 | 0 | 0 | 2 | 73 | 0.00 |  |
| 60 kg | 32% | 0.06 | 0.67 | 0.05 | 1.17 | 7 | 1 | 5 | 0 | 0 | 2 | 86 | 0.00 |  |
| 80 kg | 29% | 0.04 | 0.77 | 0.03 | 0.83 | 7 | 0 | 3 | 0 | 0 | 3 | 105 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| beam | 0.29 | 40% | 18% | 0.83 | 35% | 0.08 | 10 | 0 | 7 | 0 | 0 | 3 |
