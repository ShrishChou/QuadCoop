# Pair evaluation: fm-dev-C-turn_mirror-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto); planner settings changed: fail_mem=2

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 10 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 60 kg | 0.93 | 0.68 | 0.01 | 0.06 | 25.1 | 0.08 | 0.13 | 0.24 | 0.01 | 0.02 | 1.39 |
| 80 kg | 0.80 | 0.41 | 0.04 | 0.07 | 31.0 | 0.09 | 0.18 | 0.26 | 0.01 | 0.04 | 1.53 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 60 kg | 80 kg |
|---|---|---|---|
| arch |  | 0.95 | 0.85 |
| long |  | 0.90 | 0.75 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 60 kg | 0.93 | 0.00 | 0.07 | 0.00 | 0.00 | 0.00 | 8.90 |
| 80 kg | 0.80 | 0.09 | 0.11 | 0.00 | 0.00 | 0.00 | 10.76 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 60 kg | 1.00 | 0.48 | 0.60 | 0.79 | 0.00 | 1.00 | 0.42 | 0.62 | 0.78 | 0.00 |
| 80 kg | 1.00 | 0.48 | 0.64 | 0.79 | 0.00 | 1.00 | 0.39 | 0.68 | 0.81 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 60 kg | 0.91 | 4.72 | 0.06 | 0.91 | 4.19 | 0.06 |
| 80 kg | 0.88 | 4.05 | 0.05 | 0.89 | 4.04 | 0.05 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 60 kg | 0.35 | 0.51 | 0.19 |
| 80 kg | 0.43 | 0.57 | 0.16 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 60 kg | 2.09 | 0.30 | 14.04 | 8.90 | 0.21 | 0.00 | 2.38 | 0.00 | 0.37 |
| 80 kg | 2.83 | 0.40 | 16.13 | 10.76 | 0.31 | 0.86 | 3.27 | 0.00 | 0.29 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 60 kg | 180 | 328 | 305 |
| 80 kg | 202 | 350 | 337 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 60 kg | 403 | 0.35 | 0.41 (118) | 0.49 (53) | 0.45 (163) | 0.46 (28) | 0.70 (41) |
| 80 kg | 836 | 0.33 | 0.41 (48) | 0.50 (104) | 0.47 (581) | 0.46 (80) | 0.55 (23) |

## both robots pushing (share of time) by object and mass

| object | 60 kg | 80 kg |
|---|---|---|
| arch | 0.01 | 0.01 |
| long | 0.00 | 0.01 |

## success by scenario and mass

| scenario | 60 kg | 80 kg |
|---|---|---|
| T15_m | 0.85 | 0.65 |
| T30_m | 1.00 | 0.95 |
| T60_m | 0.90 | 0.80 |
| T90_m | 0.95 | 0.80 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 60 kg | 43% | 0% | 57% | 60% | 2% | 38% |  |  | 9% | 49% | 54% | 16% |
| 80 kg | 38% | 0% | 62% | 65% | 2% | 34% |  |  | 7% | 56% | 47% | 15% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 60 kg | 195 | 0.87 | 8% | 20% | 40% | 40% |
| 80 kg | 214 | 0.88 | 8% | 25% | 40% | 35% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 60 kg | 34% | 0.02 | -0.15 | 0.01 | 0.66 | 3 | 0 | 1 | 0 | 0 | 3 | 100 | 0.00 |  |
| 80 kg | 25% | 0.01 | -0.20 | 0.01 | 0.85 | 7 | 0 | 2 | 0 | 0 | 4 | 130 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| arch | 0.90 | 63% | 21% | 0.84 | 33% | 0.02 | 5 | 0 | 1 | 0 | 0 | 4 |
| long | 0.82 | 61% | 23% | 0.91 | 26% | 0.01 | 5 | 0 | 2 | 0 | 0 | 3 |
