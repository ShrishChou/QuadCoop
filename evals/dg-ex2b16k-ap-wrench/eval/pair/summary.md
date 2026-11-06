# Pair evaluation: dg-ex2b16k-ap-wrench

policy: Stage 4 contact policy logs/marl2/ex2b_aa_s0/model_16000.pt (robots start at their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.58 | 0.56 | 0.03 | 0.00 | 30.6 | 0.01 | 0.52 | 0.48 | 0.22 | 0.32 | 1.00 |
| 40 kg | 0.57 | 0.48 | 0.02 | 0.01 | 28.2 | 0.01 | 0.56 | 0.58 | 0.28 | 0.35 | 0.99 |
| 60 kg | 0.38 | 0.31 | 0.03 | 0.02 | 31.3 | 0.01 | 0.57 | 0.69 | 0.33 | 0.37 | 0.97 |
| 80 kg | 0.19 | 0.17 | 0.02 | 0.04 | 37.6 | 0.01 | 0.65 | 0.75 | 0.43 | 0.46 | 0.96 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x-y + part 0 corner -x+y | 0.75 | 0.58 | 0.33 | 0.08 |
| long | part 0 corner -x+y + part 0 -x seg 1/2 | 0.83 | 0.67 | 0.67 | 0.17 |
| sphere | sector 225 + sector 135 | 0.67 | 1.00 | 0.92 | 0.75 |
| cylinder | part 0 corner -x+y + part 0 -x seg 1/2 | 0.42 | 0.17 | 0.25 | 0.25 |
| arch | part 2 -x + part 3 -x | 0.75 | 0.67 | 0.50 | 0.25 |
| dumbbell | part 1 -x + part 0 -x | 0.75 | 0.58 | 0.42 | 0.33 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.42 | 0.92 | 0.58 | 0.25 |
| beam (unseen) | part 0 -x seg 4/5 + part 0 -x seg 2/5 | 0.33 | 0.17 | 0.00 | 0.00 |
| l_shape (unseen) | part 0 corner -x-y + part 1 -x | 0.67 | 0.58 | 0.33 | 0.00 |
| asym (unseen) | part 1 corner -x-y + part 0 -x | 0.42 | 0.58 | 0.08 | 0.00 |
| u_channel (unseen) | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.58 | 0.50 | 0.08 | 0.00 |
| plus (unseen) | part 1 corner -x+y + part 1 corner -x-y | 0.33 | 0.42 | 0.33 | 0.17 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.58 | 0.40 | 0.03 | 0.00 | 0.00 | 0.05 | 7.13 |
| 40 kg | 0.57 | 0.40 | 0.03 | 0.00 | 0.00 | 0.02 | 5.25 |
| 60 kg | 0.38 | 0.57 | 0.06 | 0.00 | 0.00 | 0.01 | 3.21 |
| 80 kg | 0.19 | 0.75 | 0.06 | 0.00 | 0.00 | 0.01 | 1.44 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.25 | 0.79 | 0.84 | 0.00 | 1.00 | 0.33 | 0.73 | 0.79 | 0.00 |
| 40 kg | 1.00 | 0.26 | 0.81 | 0.86 | 0.00 | 1.00 | 0.27 | 0.79 | 0.85 | 0.00 |
| 60 kg | 1.00 | 0.20 | 0.84 | 0.92 | 0.00 | 1.00 | 0.21 | 0.86 | 0.91 | 0.00 |
| 80 kg | 1.00 | 0.17 | 0.90 | 0.96 | 0.00 | 1.00 | 0.21 | 0.87 | 0.93 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.95 | 1.89 | 0.02 | 0.92 | 1.69 | 0.02 |
| 40 kg | 0.94 | 1.33 | 0.03 | 0.94 | 1.13 | 0.02 |
| 60 kg | 0.94 | 0.85 | 0.04 | 0.96 | 0.86 | 0.02 |
| 80 kg | 0.98 | 0.76 | 0.02 | 0.95 | 0.28 | 0.03 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.69 | 0.64 | 0.25 |
| 40 kg | 0.73 | 0.71 | 0.22 |
| 60 kg | 0.77 | 0.79 | 0.19 |
| 80 kg | 0.84 | 0.80 | 0.17 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 9.13 | 0.46 | 24.13 | 7.13 | 0.00 | 0.00 | 0.00 | 0.00 | 0.34 |
| 40 kg | 9.93 | 0.54 | 18.72 | 5.25 | 0.00 | 0.00 | 0.00 | 0.00 | 0.29 |
| 60 kg | 5.55 | 0.64 | 18.98 | 3.21 | 0.00 | 0.00 | 0.00 | 0.00 | 0.21 |
| 80 kg | 5.55 | 0.69 | 19.71 | 1.44 | 0.00 | 0.00 | 0.00 | 0.00 | 0.17 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 95 | 230 | 172 |
| 40 kg | 131 | 290 | 227 |
| 60 kg | 160 | 318 | 278 |
| 80 kg | 178 | 329 | 306 |

## executor v2: holding and the team-ready barrier (time every robot of the push group is told to hold; the object's mean speed then and the share of it above 2 cm/s (gate: under 2 cm/s); each robot's contact force while told to hold; delay from team ready to both robots pressing (gate: under 0.2 s))

| mass | all holding (s) | object speed (m/s) | moving > 2 cm/s | force while holding (N) | ready to push (s) |
|---|---|---|---|---|---|
| 20 kg | 0.00 |  |  |  | 0.09 |
| 40 kg | 0.00 |  |  |  | 0.12 |
| 60 kg | 0.00 |  |  |  | 0.05 |
| 80 kg | 0.00 |  |  |  | 0.06 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.17 | 0.18 | 0.17 | 0.49 |
| long | 0.17 | 0.40 | 0.53 | 0.56 |
| sphere | 0.30 | 0.60 | 0.66 | 0.85 |
| cylinder | 0.30 | 0.28 | 0.43 | 0.57 |
| arch | 0.29 | 0.24 | 0.23 | 0.25 |
| dumbbell | 0.26 | 0.20 | 0.21 | 0.20 |
| t_shape | 0.18 | 0.38 | 0.37 | 0.50 |
| beam | 0.38 | 0.38 | 0.50 | 0.61 |
| l_shape | 0.09 | 0.07 | 0.06 | 0.12 |
| asym | 0.17 | 0.34 | 0.50 | 0.63 |
| u_channel | 0.20 | 0.22 | 0.22 | 0.34 |
| plus | 0.07 | 0.07 | 0.12 | 0.10 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.69 | 0.69 | 0.61 | 0.44 |
| B_left | 0.58 | 0.67 | 0.36 | 0.11 |
| C_backright | 0.56 | 0.64 | 0.33 | 0.14 |
| D_far_turn | 0.47 | 0.28 | 0.19 | 0.06 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 26% | 0% | 74% | 37% | 5% | 59% |  |  | 8% | 46% | 61% | 14% |
| 40 kg | 21% | 0% | 79% | 44% | 3% | 54% |  |  | 7% | 60% | 45% | 13% |
| 60 kg | 14% | 0% | 86% | 51% | 2% | 47% |  |  | 8% | 69% | 35% | 13% |
| 80 kg | 10% | 0% | 90% | 55% | 2% | 43% |  |  | 8% | 71% | 33% | 14% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 130 | 0.89 | 7% | 13% | 31% | 55% |
| 40 kg | 162 | 0.90 | 6% | 18% | 38% | 44% |
| 60 kg | 185 | 0.91 | 5% | 23% | 45% | 33% |
| 80 kg | 198 | 0.91 | 5% | 28% | 45% | 27% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 57% | 0.17 | 0.44 | 0.13 | 0.81 | 16 | 0 | 14 | 0 | 0 | 2 | 63 | 4.74 | 0.00 |
| 40 kg | 53% | 0.14 | 0.65 | 0.12 | 0.81 | 17 | 0 | 15 | 0 | 0 | 2 | 93 | 3.20 | 0.00 |
| 60 kg | 50% | 0.09 | 0.74 | 0.08 | 0.65 | 12 | 1 | 10 | 0 | 0 | 1 | 107 | 3.61 | 0.00 |
| 80 kg | 39% | 0.06 | 0.79 | 0.05 | 0.78 | 12 | 1 | 10 | 0 | 0 | 1 | 120 | 2.88 | 0.00 |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.44 | 54% | 25% | 0.94 | 56% | 0.08 | 4 | 0 | 4 | 0 | 0 | 0 |
| long | 0.58 | 54% | 27% | 0.92 | 60% | 0.10 | 5 | 0 | 5 | 0 | 0 | 0 |
| sphere | 0.83 | 37% | 15% | 0.92 | 90% | 0.26 | 1 | 0 | 0 | 0 | 0 | 1 |
| cylinder | 0.27 | 33% | 11% | 0.91 | 57% | 0.09 | 15 | 0 | 15 | 0 | 0 | 0 |
| arch | 0.54 | 54% | 25% | 0.85 | 50% | 0.11 | 15 | 1 | 10 | 0 | 0 | 4 |
| dumbbell | 0.52 | 49% | 19% | 0.91 | 48% | 0.10 | 12 | 1 | 12 | 0 | 0 | 0 |
| t_shape | 0.54 | 57% | 30% | 0.91 | 56% | 0.10 | 10 | 1 | 8 | 0 | 0 | 1 |
| beam | 0.12 | 37% | 20% | 0.83 | 18% | 0.04 | 36 | 2 | 33 | 0 | 0 | 1 |
| l_shape | 0.40 | 42% | 15% | 0.92 | 44% | 0.06 | 16 | 0 | 16 | 0 | 0 | 0 |
| asym | 0.27 | 62% | 33% | 0.92 | 53% | 0.05 | 6 | 0 | 5 | 0 | 0 | 0 |
| u_channel | 0.29 | 34% | 12% | 0.91 | 34% | 0.07 | 27 | 0 | 25 | 0 | 0 | 1 |
| plus | 0.31 | 46% | 12% | 0.90 | 33% | 0.06 | 24 | 1 | 14 | 0 | 0 | 9 |
