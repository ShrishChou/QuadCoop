# Pair evaluation: fm-test-D-turn-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto); TASKS: turn in place (object at the goal position, heading off 15/30/60/90 deg, capped by symmetry); planner settings changed: fail_mem=3

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 10 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 60 kg | 0.89 | 0.55 | 0.00 | 0.05 | 24.5 | 0.08 | 0.14 | 0.24 | 0.01 | 0.02 | 1.52 |
| 80 kg | 0.79 | 0.46 | 0.03 | 0.05 | 28.8 | 0.08 | 0.17 | 0.27 | 0.01 | 0.04 | 1.56 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 60 kg | 80 kg |
|---|---|---|---|
| arch |  | 0.95 | 0.85 |
| long |  | 0.82 | 0.72 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 60 kg | 0.89 | 0.06 | 0.05 | 0.00 | 0.00 | 0.00 | 9.97 |
| 80 kg | 0.79 | 0.14 | 0.07 | 0.00 | 0.00 | 0.00 | 9.70 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 60 kg | 1.00 | 0.48 | 0.58 | 0.77 | 0.00 | 1.00 | 0.51 | 0.58 | 0.74 | 0.00 |
| 80 kg | 1.00 | 0.41 | 0.64 | 0.81 | 0.00 | 1.00 | 0.46 | 0.64 | 0.75 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 60 kg | 0.86 | 5.39 | 0.05 | 0.86 | 5.61 | 0.05 |
| 80 kg | 0.86 | 4.53 | 0.05 | 0.84 | 4.82 | 0.05 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 60 kg | 0.37 | 0.50 | 0.21 |
| 80 kg | 0.46 | 0.54 | 0.19 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 60 kg | 1.99 | 0.30 | 15.19 | 9.97 | 0.17 | 0.00 | 4.41 | 0.00 | 0.40 |
| 80 kg | 2.00 | 0.40 | 15.75 | 9.70 | 0.66 | 0.89 | 4.51 | 0.00 | 0.33 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 60 kg | 173 | 322 | 297 |
| 80 kg | 195 | 340 | 331 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 60 kg | 560 | 0.34 | 0.38 (144) | 0.60 (75) | 0.48 (246) | 0.54 (47) | 0.65 (47) |
| 80 kg | 1087 | 0.33 | 0.50 (37) | 0.55 (152) | 0.48 (809) | 0.49 (53) | 0.63 (37) |

## both robots pushing (share of time) by object and mass

| object | 60 kg | 80 kg |
|---|---|---|
| arch | 0.01 | 0.02 |
| long | 0.01 | 0.01 |

## success by scenario and mass

| scenario | 60 kg | 80 kg |
|---|---|---|
| T15 | 1.00 | 0.95 |
| T30 | 0.95 | 0.80 |
| T60 | 0.90 | 0.80 |
| T90 | 0.70 | 0.60 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 60 kg | 45% | 0% | 55% | 59% | 2% | 39% |  |  | 6% | 51% | 56% | 14% |
| 80 kg | 40% | 0% | 60% | 65% | 2% | 33% |  |  | 7% | 44% | 58% | 19% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 60 kg | 192 | 0.88 | 7% | 18% | 39% | 43% |
| 80 kg | 209 | 0.88 | 8% | 24% | 41% | 35% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 60 kg | 32% | 0.02 | -0.18 | 0.01 | 0.79 | 5 | 0 | 1 | 0 | 0 | 4 | 84 | 0.00 |  |
| 80 kg | 25% | 0.01 | -0.24 | 0.01 | 0.99 | 7 | 1 | 1 | 0 | 0 | 5 | 147 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| arch | 0.90 | 63% | 20% | 0.85 | 34% | 0.02 | 5 | 0 | 1 | 0 | 0 | 3 |
| long | 0.78 | 61% | 22% | 0.91 | 22% | 0.00 | 7 | 1 | 1 | 0 | 0 | 5 |
