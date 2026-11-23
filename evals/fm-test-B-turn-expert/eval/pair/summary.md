# Pair evaluation: fm-test-B-turn-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto); TASKS: turn in place (object at the goal position, heading off 15/30/60/90 deg, capped by symmetry); planner settings changed: fail_mem=1

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 10 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 60 kg | 0.86 | 0.51 | 0.01 | 0.01 | 23.5 | 0.07 | 0.14 | 0.27 | 0.01 | 0.04 | 1.52 |
| 80 kg | 0.84 | 0.38 | 0.03 | 0.03 | 28.0 | 0.09 | 0.20 | 0.28 | 0.02 | 0.06 | 1.44 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 60 kg | 80 kg |
|---|---|---|---|
| arch |  | 0.93 | 0.93 |
| long |  | 0.80 | 0.75 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 60 kg | 0.86 | 0.11 | 0.03 | 0.00 | 0.00 | 0.00 | 10.51 |
| 80 kg | 0.84 | 0.11 | 0.05 | 0.00 | 0.00 | 0.00 | 10.78 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 60 kg | 1.00 | 0.45 | 0.60 | 0.77 | 0.00 | 1.00 | 0.50 | 0.59 | 0.75 | 0.00 |
| 80 kg | 1.00 | 0.40 | 0.67 | 0.81 | 0.00 | 1.00 | 0.46 | 0.63 | 0.76 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 60 kg | 0.89 | 5.05 | 0.05 | 0.81 | 4.44 | 0.05 |
| 80 kg | 0.89 | 4.18 | 0.05 | 0.86 | 4.09 | 0.05 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 60 kg | 0.37 | 0.52 | 0.21 |
| 80 kg | 0.48 | 0.54 | 0.18 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 60 kg | 2.85 | 0.30 | 15.67 | 10.51 | 0.12 | 0.00 | 3.55 | 0.00 | 0.41 |
| 80 kg | 2.76 | 0.41 | 15.33 | 10.78 | 0.61 | 0.64 | 3.89 | 0.00 | 0.35 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 60 kg | 172 | 318 | 291 |
| 80 kg | 196 | 350 | 331 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 60 kg | 562 | 0.32 | 0.38 (105) | 0.52 (70) | 0.49 (301) | 0.51 (31) | 0.78 (54) |
| 80 kg | 1038 | 0.33 | 0.54 (49) | 0.55 (136) | 0.49 (684) | 0.46 (120) | 0.58 (49) |

## both robots pushing (share of time) by object and mass

| object | 60 kg | 80 kg |
|---|---|---|
| arch | 0.02 | 0.03 |
| long | 0.01 | 0.02 |

## success by scenario and mass

| scenario | 60 kg | 80 kg |
|---|---|---|
| T15 | 1.00 | 1.00 |
| T30 | 0.85 | 0.80 |
| T60 | 0.85 | 0.85 |
| T90 | 0.75 | 0.70 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 60 kg | 45% | 0% | 55% | 59% | 2% | 39% |  |  | 8% | 47% | 60% | 14% |
| 80 kg | 39% | 0% | 61% | 66% | 2% | 32% |  |  | 7% | 51% | 50% | 16% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 60 kg | 191 | 0.88 | 7% | 19% | 39% | 42% |
| 80 kg | 213 | 0.89 | 6% | 25% | 41% | 34% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 60 kg | 32% | 0.02 | -0.18 | 0.01 | 0.90 | 6 | 0 | 2 | 0 | 0 | 5 | 127 | 0.00 |  |
| 80 kg | 27% | 0.02 | -0.23 | 0.01 | 0.93 | 6 | 1 | 1 | 0 | 0 | 4 | 142 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| arch | 0.93 | 64% | 21% | 0.86 | 36% | 0.02 | 4 | 0 | 1 | 0 | 0 | 2 |
| long | 0.78 | 61% | 23% | 0.92 | 22% | 0.00 | 8 | 1 | 2 | 0 | 0 | 6 |
