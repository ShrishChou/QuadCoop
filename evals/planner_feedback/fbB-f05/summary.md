# Pair evaluation: fbB-f05-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start at their contacts; contact rule re-applied: auto); planner settings changed: fb_on=1

success = 10 cm / 6 deg held 1 s within 20 s; precise = 10 cm / 3 deg with the object at rest; 8 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 40 kg | 0.44 | 0.38 | 0.06 | 0.00 | 10.9 | 0.00 | 0.60 | 0.58 | 0.34 | 0.42 | 1.51 |
| 60 kg | 0.00 | 0.00 | 0.38 | 0.00 |  | 0.00 | 0.79 | 0.78 | 0.65 | 0.71 | 1.35 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 40 kg | 60 kg |
|---|---|---|---|
| beam (unseen) |  | 0.44 | 0.00 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 40 kg | 0.44 | 0.50 | 0.06 | 0.00 | 0.00 | 0.00 | 2.62 |
| 60 kg | 0.00 | 0.62 | 0.38 | 0.00 | 0.00 | 0.00 | 1.19 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 40 kg | 1.00 | 0.28 | 0.66 | 0.91 | 0.00 | 1.00 | 0.27 | 0.64 | 0.86 | 0.00 |
| 60 kg | 1.00 | 0.28 | 0.51 | 0.96 | 0.00 | 1.00 | 0.29 | 0.48 | 0.97 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 40 kg | 0.98 | 1.21 | 0.12 | 0.97 | 1.04 | 0.16 |
| 60 kg | 0.95 | 0.73 | 0.32 | 0.95 | 0.67 | 0.35 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 40 kg | 0.61 | 0.60 | 0.33 |
| 60 kg | 0.47 | 0.46 | 0.20 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 40 kg | 0.32 | 0.46 | 11.14 | 2.62 | 0.25 | 0.00 | 0.69 | 0.00 | 0.33 |
| 60 kg | 0.11 | 0.27 | 10.68 | 1.19 | 0.00 | 0.00 | 0.00 | 0.00 | 0.56 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 40 kg | 120 | 228 | 180 |
| 60 kg | 135 | 236 | 205 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 40 kg | 54 | 0.38 | 0.26 (14) | 0.67 (8) | 0.59 (5) | 0.52 (7) | 0.51 (18) |
| 60 kg | 31 | 0.44 | 0.64 (6) | 0.59 (4) | 0.40 (8) | 0.44 (6) | 0.41 (7) |

## both robots pushing (share of time) by object and mass

| object | 40 kg | 60 kg |
|---|---|---|
| beam | 0.34 | 0.65 |

## success by scenario and mass

| scenario | 40 kg | 60 kg |
|---|---|---|
| S_straight | 0.88 | 0.00 |
| S_moveturn | 0.00 | 0.00 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 40 kg | 37% | 0% | 63% | 45% | 2% | 53% |  |  | 23% | 92% | 11% | 35% |
| 60 kg | 53% | 0% | 47% | 59% | 2% | 39% |  |  | 48% | 96% | 6% | 46% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 40 kg | 141 | 0.88 | 9% | 17% | 47% | 36% |
| 60 kg | 152 | 0.91 | 6% | 36% | 44% | 20% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 40 kg | 48% | 0.15 | 0.63 | 0.13 | 0.25 | 1 | 0 | 0 | 0 | 0 | 1 | 87 | 0.00 |  |
| 60 kg | 46% | 0.08 | 0.81 | 0.07 | 0.31 | 1 | 0 | 0 | 0 | 0 | 1 | 98 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| beam | 0.22 | 52% | 27% | 0.89 | 47% | 0.10 | 1 | 0 | 0 | 0 | 0 | 1 |
