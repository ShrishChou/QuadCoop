# Pair evaluation: dg-hvA-wrench

policy: Stage 4 contact policy logs/marl2/hvA_aa_s0/model_13500.pt (robots start at their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.75 | 0.67 | 0.01 | 0.00 | 27.9 | 0.01 | 0.45 | 0.49 | 0.21 | 0.34 | 1.01 |
| 40 kg | 0.65 | 0.54 | 0.03 | 0.02 | 29.6 | 0.01 | 0.56 | 0.58 | 0.31 | 0.39 | 1.02 |
| 60 kg | 0.41 | 0.35 | 0.06 | 0.01 | 31.7 | 0.01 | 0.59 | 0.68 | 0.36 | 0.42 | 0.97 |
| 80 kg | 0.28 | 0.23 | 0.03 | 0.06 | 37.9 | 0.01 | 0.66 | 0.75 | 0.44 | 0.48 | 0.96 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x-y + part 0 corner -x+y | 1.00 | 0.83 | 0.42 | 0.08 |
| long | part 0 corner -x+y + part 0 -x seg 1/2 | 0.75 | 0.83 | 0.58 | 0.33 |
| sphere | sector 225 + sector 135 | 1.00 | 0.83 | 1.00 | 1.00 |
| cylinder | part 0 corner -x+y + part 0 -x seg 1/2 | 0.50 | 0.42 | 0.25 | 0.25 |
| arch | part 2 -x + part 3 -x | 0.75 | 0.92 | 0.33 | 0.33 |
| dumbbell | part 1 -x + part 0 -x | 0.75 | 0.67 | 0.42 | 0.42 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.58 | 0.75 | 0.50 | 0.25 |
| beam (unseen) | part 0 -x seg 4/5 + part 0 -x seg 2/5 | 0.75 | 0.25 | 0.00 | 0.00 |
| l_shape (unseen) | part 0 corner -x-y + part 1 -x | 0.75 | 0.75 | 0.42 | 0.00 |
| asym (unseen) | part 1 corner -x-y + part 0 -x | 0.92 | 0.33 | 0.17 | 0.00 |
| u_channel (unseen) | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.67 | 0.75 | 0.25 | 0.17 |
| plus (unseen) | part 1 corner -x+y + part 1 corner -x-y | 0.58 | 0.50 | 0.58 | 0.50 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.75 | 0.24 | 0.01 | 0.00 | 0.00 | 0.00 | 7.15 |
| 40 kg | 0.65 | 0.30 | 0.05 | 0.00 | 0.00 | 0.00 | 5.01 |
| 60 kg | 0.41 | 0.52 | 0.07 | 0.00 | 0.00 | 0.00 | 3.02 |
| 80 kg | 0.28 | 0.63 | 0.09 | 0.00 | 0.00 | 0.00 | 1.76 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.29 | 0.77 | 0.81 | 0.00 | 1.00 | 0.24 | 0.77 | 0.83 | 0.00 |
| 40 kg | 1.00 | 0.25 | 0.80 | 0.87 | 0.00 | 1.00 | 0.24 | 0.81 | 0.88 | 0.00 |
| 60 kg | 1.00 | 0.20 | 0.84 | 0.90 | 0.00 | 1.00 | 0.22 | 0.84 | 0.91 | 0.00 |
| 80 kg | 1.00 | 0.18 | 0.87 | 0.94 | 0.00 | 1.00 | 0.20 | 0.86 | 0.94 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.95 | 2.18 | 0.03 | 0.96 | 1.78 | 0.04 |
| 40 kg | 0.95 | 1.83 | 0.03 | 0.96 | 1.48 | 0.04 |
| 60 kg | 0.93 | 1.49 | 0.04 | 0.95 | 1.27 | 0.04 |
| 80 kg | 0.96 | 0.95 | 0.04 | 0.95 | 0.55 | 0.04 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.65 | 0.66 | 0.27 |
| 40 kg | 0.70 | 0.72 | 0.23 |
| 60 kg | 0.76 | 0.76 | 0.21 |
| 80 kg | 0.80 | 0.79 | 0.18 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 5.20 | 0.44 | 24.37 | 7.15 | 0.00 | 0.00 | 0.00 | 0.00 | 0.35 |
| 40 kg | 6.96 | 0.52 | 23.11 | 5.01 | 0.00 | 0.00 | 0.00 | 0.00 | 0.29 |
| 60 kg | 5.95 | 0.61 | 24.17 | 3.02 | 0.00 | 0.00 | 0.00 | 0.00 | 0.23 |
| 80 kg | 5.51 | 0.64 | 23.66 | 1.76 | 0.00 | 0.00 | 0.00 | 0.00 | 0.20 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 92 | 232 | 161 |
| 40 kg | 130 | 298 | 234 |
| 60 kg | 162 | 328 | 272 |
| 80 kg | 187 | 346 | 316 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.24 | 0.24 | 0.26 | 0.51 |
| long | 0.20 | 0.45 | 0.59 | 0.63 |
| sphere | 0.58 | 0.64 | 0.76 | 0.78 |
| cylinder | 0.23 | 0.62 | 0.58 | 0.64 |
| arch | 0.08 | 0.24 | 0.19 | 0.23 |
| dumbbell | 0.22 | 0.16 | 0.24 | 0.29 |
| t_shape | 0.23 | 0.32 | 0.53 | 0.62 |
| beam | 0.20 | 0.17 | 0.26 | 0.51 |
| l_shape | 0.09 | 0.10 | 0.06 | 0.07 |
| asym | 0.28 | 0.39 | 0.48 | 0.61 |
| u_channel | 0.12 | 0.26 | 0.22 | 0.28 |
| plus | 0.04 | 0.09 | 0.14 | 0.17 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.83 | 0.86 | 0.61 | 0.50 |
| B_left | 0.69 | 0.75 | 0.36 | 0.19 |
| C_backright | 0.86 | 0.56 | 0.33 | 0.25 |
| D_far_turn | 0.61 | 0.44 | 0.33 | 0.17 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 29% | 0% | 71% | 33% | 4% | 63% |  |  | 10% | 45% | 61% | 15% |
| 40 kg | 24% | 0% | 76% | 43% | 3% | 54% |  |  | 9% | 42% | 62% | 15% |
| 60 kg | 19% | 0% | 81% | 52% | 2% | 46% |  |  | 9% | 53% | 53% | 16% |
| 80 kg | 16% | 0% | 84% | 56% | 2% | 42% |  |  | 9% | 62% | 44% | 14% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 130 | 0.90 | 7% | 9% | 33% | 58% |
| 40 kg | 167 | 0.90 | 6% | 15% | 42% | 43% |
| 60 kg | 190 | 0.91 | 5% | 21% | 48% | 31% |
| 80 kg | 209 | 0.92 | 4% | 27% | 49% | 25% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 58% | 0.19 | 0.50 | 0.15 | 0.85 | 10 | 0 | 9 | 0 | 0 | 1 | 69 | 0.00 |  |
| 40 kg | 58% | 0.15 | 0.68 | 0.13 | 1.00 | 10 | 0 | 9 | 0 | 0 | 1 | 96 | 0.00 |  |
| 60 kg | 54% | 0.10 | 0.77 | 0.09 | 0.59 | 6 | 0 | 5 | 0 | 0 | 1 | 116 | 0.00 |  |
| 80 kg | 46% | 0.06 | 0.81 | 0.06 | 0.44 | 4 | 0 | 3 | 0 | 0 | 0 | 122 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.58 | 55% | 25% | 0.93 | 65% | 0.12 | 0 | 0 | 0 | 0 | 0 | 0 |
| long | 0.62 | 51% | 23% | 0.93 | 62% | 0.13 | 4 | 0 | 3 | 0 | 0 | 1 |
| sphere | 0.96 | 31% | 10% | 0.92 | 90% | 0.28 | 2 | 0 | 1 | 0 | 0 | 0 |
| cylinder | 0.35 | 28% | 10% | 0.92 | 56% | 0.10 | 7 | 0 | 7 | 0 | 0 | 0 |
| arch | 0.58 | 57% | 22% | 0.81 | 53% | 0.10 | 5 | 0 | 4 | 0 | 0 | 1 |
| dumbbell | 0.56 | 49% | 18% | 0.91 | 52% | 0.10 | 7 | 0 | 7 | 0 | 0 | 0 |
| t_shape | 0.52 | 49% | 23% | 0.92 | 51% | 0.11 | 14 | 1 | 13 | 0 | 0 | 0 |
| beam | 0.25 | 37% | 21% | 0.87 | 27% | 0.06 | 24 | 1 | 22 | 0 | 0 | 0 |
| l_shape | 0.48 | 45% | 12% | 0.92 | 49% | 0.07 | 6 | 0 | 5 | 0 | 0 | 1 |
| asym | 0.35 | 60% | 28% | 0.93 | 56% | 0.07 | 3 | 0 | 2 | 0 | 0 | 0 |
| u_channel | 0.46 | 40% | 13% | 0.92 | 42% | 0.08 | 8 | 0 | 7 | 0 | 0 | 1 |
| plus | 0.54 | 47% | 12% | 0.91 | 45% | 0.07 | 5 | 0 | 3 | 0 | 0 | 2 |
