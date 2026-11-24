# Pair evaluation: fm-test-B2-turn-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto); TASKS: turn in place (object at the goal position, heading off 15/30/60/90 deg, capped by symmetry); planner settings changed: fail_mem=1,fail_act=2

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 10 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 60 kg | 0.89 | 0.55 | 0.01 | 0.03 | 24.3 | 0.08 | 0.15 | 0.24 | 0.01 | 0.03 | 1.46 |
| 80 kg | 0.85 | 0.39 | 0.01 | 0.03 | 27.9 | 0.07 | 0.16 | 0.31 | 0.02 | 0.06 | 1.42 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 60 kg | 80 kg |
|---|---|---|---|
| arch |  | 0.97 | 0.88 |
| long |  | 0.80 | 0.82 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 60 kg | 0.89 | 0.07 | 0.04 | 0.00 | 0.00 | 0.01 | 11.06 |
| 80 kg | 0.85 | 0.11 | 0.04 | 0.00 | 0.00 | 0.00 | 9.89 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 60 kg | 1.00 | 0.46 | 0.58 | 0.76 | 0.00 | 1.00 | 0.50 | 0.59 | 0.74 | 0.00 |
| 80 kg | 1.00 | 0.38 | 0.67 | 0.82 | 0.00 | 1.00 | 0.48 | 0.64 | 0.76 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 60 kg | 0.90 | 5.54 | 0.05 | 0.84 | 5.49 | 0.05 |
| 80 kg | 0.87 | 3.80 | 0.05 | 0.87 | 4.39 | 0.05 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 60 kg | 0.37 | 0.51 | 0.22 |
| 80 kg | 0.47 | 0.55 | 0.19 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 60 kg | 1.91 | 0.31 | 15.54 | 11.06 | 0.17 | 0.00 | 3.51 | 0.00 | 0.41 |
| 80 kg | 2.23 | 0.41 | 15.40 | 9.89 | 0.57 | 0.46 | 4.40 | 0.00 | 0.31 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 60 kg | 168 | 316 | 290 |
| 80 kg | 195 | 348 | 332 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 60 kg | 558 | 0.34 | 0.30 (76) | 0.55 (81) | 0.49 (247) | 0.49 (77) | 0.55 (77) |
| 80 kg | 1012 | 0.33 | 0.43 (50) | 0.54 (146) | 0.47 (679) | 0.47 (92) | 0.57 (45) |

## both robots pushing (share of time) by object and mass

| object | 60 kg | 80 kg |
|---|---|---|
| arch | 0.01 | 0.02 |
| long | 0.01 | 0.02 |

## success by scenario and mass

| scenario | 60 kg | 80 kg |
|---|---|---|
| T15 | 1.00 | 1.00 |
| T30 | 0.90 | 0.90 |
| T60 | 0.85 | 0.85 |
| T90 | 0.80 | 0.65 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 60 kg | 45% | 0% | 55% | 60% | 2% | 38% |  |  | 9% | 44% | 64% | 16% |
| 80 kg | 38% | 0% | 62% | 65% | 2% | 33% |  |  | 6% | 40% | 63% | 17% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 60 kg | 191 | 0.88 | 7% | 19% | 39% | 41% |
| 80 kg | 209 | 0.88 | 7% | 25% | 41% | 33% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 60 kg | 33% | 0.02 | -0.17 | 0.01 | 0.81 | 6 | 0 | 1 | 0 | 0 | 5 | 95 | 0.00 |  |
| 80 kg | 26% | 0.02 | -0.23 | 0.01 | 0.81 | 5 | 1 | 1 | 0 | 0 | 4 | 147 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| arch | 0.93 | 64% | 21% | 0.85 | 36% | 0.02 | 4 | 0 | 1 | 0 | 0 | 2 |
| long | 0.81 | 61% | 24% | 0.92 | 23% | 0.00 | 8 | 1 | 1 | 0 | 0 | 6 |
