# Pair evaluation: r2dev-resid600-s4001-expert

policy: Stage 4 contact policy logs/marl2/resid2_beam_s0/model_600.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.67 | 0.58 | 0.08 | 0.00 | 29.2 | 0.00 | 0.47 | 0.39 | 0.17 | 0.29 | 1.41 |
| 40 kg | 0.25 | 0.33 | 0.08 | 0.00 | 52.9 | 0.01 | 0.66 | 0.41 | 0.15 | 0.18 | 1.42 |
| 60 kg | 0.00 | 0.00 | 0.50 | 0.00 |  | 0.01 | 0.87 | 0.45 | 0.42 | 0.46 | 1.47 |
| 80 kg | 0.00 | 0.00 | 0.42 | 0.08 |  | 0.01 | 0.87 | 0.52 | 0.48 | 0.55 | 1.53 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| beam (unseen) | part 0 -x seg 2/5 + part 0 -x seg 4/5 | 0.67 | 0.25 | 0.00 | 0.00 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.67 | 0.25 | 0.08 | 0.00 | 0.00 | 0.00 | 10.00 |
| 40 kg | 0.25 | 0.67 | 0.08 | 0.00 | 0.00 | 0.00 | 3.33 |
| 60 kg | 0.00 | 0.50 | 0.50 | 0.00 | 0.00 | 0.00 | 2.33 |
| 80 kg | 0.00 | 0.50 | 0.50 | 0.00 | 0.00 | 0.00 | 2.58 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.31 | 0.62 | 0.94 | 0.00 | 1.00 | 0.45 | 0.39 | 0.89 | 0.00 |
| 40 kg | 1.00 | 0.27 | 0.60 | 0.96 | 0.00 | 1.00 | 0.25 | 0.71 | 0.97 | 0.00 |
| 60 kg | 1.00 | 0.31 | 0.48 | 0.96 | 0.00 | 1.00 | 0.31 | 0.50 | 0.96 | 0.00 |
| 80 kg | 1.00 | 0.32 | 0.48 | 0.95 | 0.00 | 1.00 | 0.37 | 0.40 | 0.92 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.82 | 2.08 | 0.09 | 0.79 | 1.98 | 0.10 |
| 40 kg | 0.76 | 2.36 | 0.19 | 0.73 | 1.44 | 0.10 |
| 60 kg | 0.76 | 2.18 | 0.31 | 0.64 | 1.47 | 0.22 |
| 80 kg | 0.81 | 1.95 | 0.33 | 0.71 | 2.44 | 0.39 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.50 | 0.32 | 0.26 |
| 40 kg | 0.57 | 0.65 | 0.28 |
| 60 kg | 0.43 | 0.49 | 0.20 |
| 80 kg | 0.38 | 0.29 | 0.15 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.30 | 0.29 | 29.60 | 10.00 | 0.42 | 0.00 | 5.58 | 0.00 | 0.47 |
| 40 kg | 0.89 | 0.47 | 49.21 | 3.33 | 0.92 | 0.00 | 0.33 | 0.00 | 0.30 |
| 60 kg | 0.01 | 0.35 | 38.05 | 2.33 | 0.08 | 0.00 | 0.25 | 0.00 | 0.45 |
| 80 kg | 0.12 | 0.21 | 34.62 | 2.58 | 0.00 | 0.00 | 0.00 | 0.00 | 0.58 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 87 | 192 | 108 |
| 40 kg | 85 | 185 | 142 |
| 60 kg | 100 | 207 | 185 |
| 80 kg | 133 | 262 | 245 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 42 | 0.34 | 0.23 (17) | 0.52 (6) | 0.66 (7) | 0.47 (9) | 0.66 (3) |
| 40 kg | 119 | 0.47 | 0.58 (28) | 0.60 (25) | 0.58 (16) | 0.40 (19) | 0.57 (32) |
| 60 kg | 83 | 0.44 | 0.00 (0) | 0.65 (22) | 0.81 (12) | 0.51 (24) | 0.68 (26) |
| 80 kg | 51 | 0.38 | - | 0.76 (4) | 0.50 (38) | 0.66 (1) | 0.94 (9) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| beam | 0.17 | 0.15 | 0.42 | 0.48 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.67 | 0.33 | 0.00 | 0.00 |
| B_left | 1.00 | 0.33 | 0.00 | 0.00 |
| C_backright | 0.67 | 0.33 | 0.00 | 0.00 |
| D_far_turn | 0.33 | 0.00 | 0.00 | 0.00 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 52% | 0% | 48% | 26% | 3% | 71% |  |  | 36% | 90% | 14% | 31% |
| 40 kg | 35% | 0% | 65% | 24% | 4% | 72% |  |  | 29% | 96% | 6% | 37% |
| 60 kg | 53% | 0% | 47% | 34% | 4% | 61% |  |  | 47% | 96% | 9% | 48% |
| 80 kg | 64% | 0% | 36% | 44% | 3% | 53% |  |  | 57% | 83% | 23% | 55% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 112 | 0.87 | 11% | 6% | 28% | 66% |
| 40 kg | 114 | 0.86 | 13% | 10% | 37% | 53% |
| 60 kg | 129 | 0.84 | 13% | 18% | 43% | 39% |
| 80 kg | 159 | 0.81 | 17% | 26% | 46% | 28% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 39% | 0.18 | 0.59 | 0.15 | 1.58 | 9 | 0 | 8 | 0 | 0 | 1 | 42 | 0.00 |  |
| 40 kg | 24% | 0.07 | 0.63 | 0.05 | 2.83 | 13 | 0 | 12 | 0 | 0 | 1 | 59 | 0.00 |  |
| 60 kg | 27% | 0.05 | 0.69 | 0.04 | 2.42 | 15 | 1 | 13 | 0 | 0 | 2 | 100 | 0.00 |  |
| 80 kg | 20% | 0.02 | 0.71 | 0.02 | 0.92 | 5 | 0 | 2 | 0 | 0 | 2 | 107 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| beam | 0.23 | 32% | 15% | 0.85 | 28% | 0.07 | 10 | 0 | 8 | 0 | 0 | 2 |
