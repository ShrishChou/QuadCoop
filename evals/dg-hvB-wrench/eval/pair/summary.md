# Pair evaluation: dg-hvB-wrench

policy: Stage 4 contact policy logs/marl2/hvB_aa_s0/model_13500.pt (robots start at their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.61 | 0.63 | 0.01 | 0.01 | 31.7 | 0.02 | 0.36 | 0.41 | 0.14 | 0.27 | 1.01 |
| 40 kg | 0.60 | 0.58 | 0.03 | 0.05 | 34.2 | 0.03 | 0.45 | 0.46 | 0.20 | 0.32 | 1.01 |
| 60 kg | 0.40 | 0.29 | 0.06 | 0.06 | 36.9 | 0.01 | 0.50 | 0.57 | 0.25 | 0.31 | 1.01 |
| 80 kg | 0.22 | 0.12 | 0.10 | 0.07 | 36.3 | 0.02 | 0.58 | 0.65 | 0.35 | 0.41 | 0.98 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x-y + part 0 corner -x+y | 0.92 | 0.83 | 0.50 | 0.08 |
| long | part 0 corner -x+y + part 0 -x seg 1/2 | 0.50 | 0.75 | 0.75 | 0.33 |
| sphere | sector 225 + sector 135 | 1.00 | 0.92 | 0.67 | 0.58 |
| cylinder | part 0 corner -x+y + part 0 -x seg 1/2 | 0.58 | 0.08 | 0.33 | 0.33 |
| arch | part 2 -x + part 3 -x | 0.75 | 0.83 | 0.50 | 0.25 |
| dumbbell | part 1 -x + part 0 -x | 0.67 | 0.50 | 0.42 | 0.17 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.25 | 0.75 | 0.58 | 0.33 |
| beam (unseen) | part 0 -x seg 4/5 + part 0 -x seg 2/5 | 0.58 | 0.25 | 0.00 | 0.00 |
| l_shape (unseen) | part 0 corner -x-y + part 1 -x | 0.67 | 0.58 | 0.33 | 0.00 |
| asym (unseen) | part 1 corner -x-y + part 0 -x | 0.25 | 0.58 | 0.00 | 0.00 |
| u_channel (unseen) | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.67 | 0.67 | 0.25 | 0.17 |
| plus (unseen) | part 1 corner -x+y + part 1 corner -x-y | 0.50 | 0.50 | 0.50 | 0.33 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.61 | 0.37 | 0.02 | 0.00 | 0.00 | 0.03 | 8.86 |
| 40 kg | 0.60 | 0.31 | 0.08 | 0.00 | 0.00 | 0.01 | 6.40 |
| 60 kg | 0.40 | 0.49 | 0.11 | 0.00 | 0.00 | 0.00 | 3.84 |
| 80 kg | 0.22 | 0.62 | 0.17 | 0.00 | 0.00 | 0.01 | 2.14 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.34 | 0.67 | 0.76 | 0.00 | 1.00 | 0.32 | 0.67 | 0.81 | 0.00 |
| 40 kg | 1.00 | 0.31 | 0.69 | 0.81 | 0.00 | 1.00 | 0.34 | 0.67 | 0.83 | 0.00 |
| 60 kg | 1.00 | 0.28 | 0.75 | 0.88 | 0.00 | 1.00 | 0.26 | 0.75 | 0.91 | 0.00 |
| 80 kg | 1.00 | 0.27 | 0.77 | 0.90 | 0.00 | 1.00 | 0.26 | 0.73 | 0.93 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.92 | 2.54 | 0.06 | 0.94 | 2.41 | 0.08 |
| 40 kg | 0.94 | 2.68 | 0.10 | 0.93 | 1.70 | 0.09 |
| 60 kg | 0.95 | 1.68 | 0.08 | 0.96 | 1.31 | 0.09 |
| 80 kg | 0.92 | 0.70 | 0.08 | 0.95 | 0.57 | 0.11 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.54 | 0.54 | 0.31 |
| 40 kg | 0.56 | 0.56 | 0.26 |
| 60 kg | 0.63 | 0.65 | 0.21 |
| 80 kg | 0.65 | 0.63 | 0.18 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 6.17 | 0.37 | 34.30 | 8.86 | 0.00 | 0.00 | 0.00 | 0.00 | 0.42 |
| 40 kg | 6.51 | 0.38 | 28.33 | 6.40 | 0.00 | 0.00 | 0.00 | 0.00 | 0.40 |
| 60 kg | 7.13 | 0.45 | 27.00 | 3.84 | 0.00 | 0.00 | 0.00 | 0.00 | 0.35 |
| 80 kg | 7.13 | 0.45 | 24.98 | 2.14 | 0.00 | 0.00 | 0.00 | 0.00 | 0.33 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 106 | 255 | 195 |
| 40 kg | 138 | 308 | 246 |
| 60 kg | 172 | 341 | 298 |
| 80 kg | 194 | 363 | 346 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.21 | 0.12 | 0.13 | 0.21 |
| long | 0.09 | 0.20 | 0.28 | 0.41 |
| sphere | 0.47 | 0.66 | 0.63 | 0.68 |
| cylinder | 0.17 | 0.37 | 0.34 | 0.46 |
| arch | 0.12 | 0.15 | 0.23 | 0.24 |
| dumbbell | 0.17 | 0.06 | 0.13 | 0.21 |
| t_shape | 0.08 | 0.21 | 0.28 | 0.45 |
| beam | 0.07 | 0.18 | 0.25 | 0.56 |
| l_shape | 0.07 | 0.07 | 0.10 | 0.06 |
| asym | 0.08 | 0.15 | 0.34 | 0.52 |
| u_channel | 0.07 | 0.14 | 0.17 | 0.23 |
| plus | 0.05 | 0.07 | 0.08 | 0.16 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.67 | 0.69 | 0.58 | 0.39 |
| B_left | 0.64 | 0.75 | 0.56 | 0.14 |
| C_backright | 0.58 | 0.50 | 0.31 | 0.25 |
| D_far_turn | 0.56 | 0.47 | 0.17 | 0.08 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 40% | 0% | 60% | 39% | 4% | 58% |  |  | 19% | 61% | 48% | 20% |
| 40 kg | 37% | 0% | 63% | 48% | 3% | 50% |  |  | 20% | 67% | 39% | 22% |
| 60 kg | 29% | 0% | 71% | 52% | 2% | 46% |  |  | 18% | 70% | 37% | 20% |
| 80 kg | 28% | 0% | 72% | 57% | 2% | 41% |  |  | 20% | 80% | 27% | 22% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 141 | 0.89 | 8% | 13% | 33% | 54% |
| 40 kg | 170 | 0.91 | 6% | 17% | 43% | 40% |
| 60 kg | 198 | 0.91 | 5% | 21% | 49% | 31% |
| 80 kg | 216 | 0.92 | 4% | 26% | 49% | 25% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 61% | 0.18 | 0.35 | 0.13 | 0.88 | 6 | 0 | 4 | 0 | 0 | 2 | 56 | 0.00 |  |
| 40 kg | 60% | 0.16 | 0.55 | 0.13 | 0.74 | 5 | 0 | 4 | 0 | 0 | 2 | 77 | 0.00 |  |
| 60 kg | 55% | 0.10 | 0.70 | 0.09 | 0.51 | 4 | 0 | 3 | 0 | 0 | 1 | 122 | 0.00 |  |
| 80 kg | 48% | 0.08 | 0.78 | 0.07 | 0.45 | 4 | 0 | 3 | 0 | 0 | 1 | 122 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.58 | 54% | 20% | 0.94 | 59% | 0.11 | 2 | 0 | 1 | 0 | 0 | 1 |
| long | 0.58 | 53% | 22% | 0.92 | 58% | 0.08 | 6 | 0 | 5 | 0 | 0 | 1 |
| sphere | 0.79 | 32% | 12% | 0.91 | 89% | 0.33 | 1 | 0 | 0 | 0 | 0 | 0 |
| cylinder | 0.33 | 32% | 12% | 0.91 | 66% | 0.15 | 5 | 0 | 5 | 0 | 0 | 1 |
| arch | 0.58 | 60% | 24% | 0.81 | 56% | 0.09 | 3 | 0 | 2 | 0 | 0 | 1 |
| dumbbell | 0.44 | 54% | 21% | 0.92 | 54% | 0.08 | 5 | 0 | 3 | 0 | 0 | 1 |
| t_shape | 0.48 | 56% | 25% | 0.93 | 57% | 0.08 | 5 | 0 | 3 | 0 | 0 | 2 |
| beam | 0.21 | 34% | 18% | 0.85 | 27% | 0.06 | 15 | 1 | 12 | 0 | 0 | 2 |
| l_shape | 0.40 | 49% | 14% | 0.93 | 50% | 0.06 | 4 | 0 | 3 | 0 | 0 | 1 |
| asym | 0.21 | 60% | 30% | 0.92 | 51% | 0.05 | 3 | 0 | 2 | 0 | 0 | 1 |
| u_channel | 0.44 | 50% | 18% | 0.92 | 52% | 0.07 | 3 | 0 | 2 | 0 | 0 | 2 |
| plus | 0.46 | 51% | 14% | 0.92 | 53% | 0.09 | 3 | 0 | 0 | 0 | 0 | 3 |
