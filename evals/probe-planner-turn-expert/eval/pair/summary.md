# Pair evaluation: probe-planner-turn-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto); TASKS: turn in place (object at the goal position, heading off 15/30/60/90 deg, capped by symmetry)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 10 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.82 | 0.79 | 0.00 | 0.01 | 21.2 | 0.07 | 0.15 | 0.16 | 0.01 | 0.04 | 1.17 |
| 40 kg | 0.89 | 0.71 | 0.03 | 0.03 | 19.7 | 0.10 | 0.13 | 0.17 | 0.01 | 0.03 | 1.43 |
| 60 kg | 0.84 | 0.60 | 0.03 | 0.01 | 23.3 | 0.08 | 0.13 | 0.24 | 0.01 | 0.02 | 1.59 |
| 80 kg | 0.71 | 0.33 | 0.03 | 0.04 | 29.3 | 0.08 | 0.17 | 0.26 | 0.01 | 0.02 | 1.49 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| arch |  | 0.85 | 0.93 | 0.95 | 0.80 |
| long |  | 0.80 | 0.85 | 0.72 | 0.62 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.82 | 0.16 | 0.01 | 0.00 | 0.00 | 0.03 | 10.91 |
| 40 kg | 0.89 | 0.06 | 0.05 | 0.00 | 0.00 | 0.00 | 9.19 |
| 60 kg | 0.84 | 0.12 | 0.04 | 0.00 | 0.00 | 0.00 | 9.14 |
| 80 kg | 0.71 | 0.23 | 0.06 | 0.00 | 0.00 | 0.01 | 7.97 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.46 | 0.57 | 0.70 | 0.00 | 1.00 | 0.58 | 0.49 | 0.67 | 0.00 |
| 40 kg | 1.00 | 0.52 | 0.54 | 0.71 | 0.00 | 1.00 | 0.60 | 0.50 | 0.66 | 0.00 |
| 60 kg | 1.00 | 0.45 | 0.61 | 0.77 | 0.00 | 1.00 | 0.50 | 0.61 | 0.75 | 0.00 |
| 80 kg | 1.00 | 0.39 | 0.68 | 0.81 | 0.00 | 1.00 | 0.49 | 0.65 | 0.77 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.88 | 4.14 | 0.04 | 0.82 | 4.86 | 0.07 |
| 40 kg | 0.82 | 4.24 | 0.05 | 0.79 | 5.57 | 0.08 |
| 60 kg | 0.89 | 5.52 | 0.04 | 0.86 | 5.68 | 0.05 |
| 80 kg | 0.90 | 5.34 | 0.06 | 0.85 | 6.80 | 0.05 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.40 | 0.36 | 0.26 |
| 40 kg | 0.33 | 0.40 | 0.21 |
| 60 kg | 0.37 | 0.53 | 0.19 |
| 80 kg | 0.43 | 0.57 | 0.17 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 3.00 | 0.26 | 18.65 | 10.91 | 0.01 | 0.01 | 7.84 | 0.00 | 0.52 |
| 40 kg | 2.60 | 0.25 | 14.26 | 9.19 | 0.28 | 0.00 | 6.30 | 0.00 | 0.50 |
| 60 kg | 1.82 | 0.34 | 14.74 | 9.14 | 0.17 | 0.01 | 6.36 | 0.00 | 0.33 |
| 80 kg | 1.77 | 0.37 | 16.18 | 7.97 | 0.35 | 1.23 | 7.31 | 0.00 | 0.30 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 103 | 251 | 194 |
| 40 kg | 142 | 299 | 249 |
| 60 kg | 171 | 310 | 292 |
| 80 kg | 189 | 331 | 317 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 465 | 0.33 | 0.41 (69) | 0.51 (41) | 0.48 (191) | 0.46 (122) | 0.56 (42) |
| 40 kg | 365 | 0.35 | 0.34 (63) | 0.48 (56) | 0.45 (121) | 0.47 (55) | 0.60 (70) |
| 60 kg | 669 | 0.37 | 0.43 (93) | 0.61 (104) | 0.54 (378) | 0.58 (59) | 0.62 (36) |
| 80 kg | 1080 | 0.33 | 0.51 (23) | 0.55 (105) | 0.51 (907) | 0.46 (26) | 0.68 (19) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| arch | 0.01 | 0.01 | 0.01 | 0.01 |
| long | 0.01 | 0.01 | 0.01 | 0.01 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| T15 | 0.90 | 0.95 | 1.00 | 0.95 |
| T30 | 0.75 | 0.85 | 0.85 | 0.70 |
| T60 | 0.85 | 0.90 | 0.90 | 0.85 |
| T90 | 0.80 | 0.85 | 0.60 | 0.35 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 55% | 0% | 45% | 41% | 4% | 56% |  |  | 11% | 36% | 69% | 16% |
| 40 kg | 55% | 0% | 45% | 52% | 2% | 46% |  |  | 10% | 27% | 75% | 15% |
| 60 kg | 43% | 0% | 57% | 61% | 2% | 37% |  |  | 6% | 41% | 63% | 14% |
| 80 kg | 38% | 0% | 62% | 66% | 2% | 33% |  |  | 7% | 52% | 54% | 15% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 135 | 0.85 | 10% | 10% | 27% | 63% |
| 40 kg | 166 | 0.88 | 8% | 12% | 35% | 52% |
| 60 kg | 188 | 0.88 | 7% | 18% | 41% | 41% |
| 80 kg | 204 | 0.88 | 7% | 25% | 42% | 33% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 41% | 0.05 | -0.19 | 0.02 | 0.93 | 8 | 0 | 3 | 0 | 0 | 4 | 59 | 0.00 |  |
| 40 kg | 37% | 0.03 | -0.21 | 0.02 | 0.66 | 5 | 0 | 2 | 0 | 0 | 3 | 76 | 0.00 |  |
| 60 kg | 31% | 0.02 | -0.21 | 0.01 | 1.00 | 6 | 0 | 2 | 0 | 0 | 3 | 115 | 0.00 |  |
| 80 kg | 22% | 0.01 | -0.24 | 0.01 | 1.86 | 11 | 3 | 5 | 0 | 0 | 4 | 144 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| arch | 0.88 | 55% | 15% | 0.84 | 37% | 0.02 | 6 | 0 | 2 | 0 | 0 | 3 |
| long | 0.75 | 54% | 18% | 0.91 | 29% | 0.01 | 9 | 2 | 4 | 0 | 0 | 4 |
