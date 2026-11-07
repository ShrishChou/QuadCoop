# Pair evaluation: fair-hvB-expert

policy: Stage 4 contact policy logs/keep/marl2/hvB_aa_s0/model_13500.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.73 | 0.69 | 0.02 | 0.02 | 30.2 | 0.00 | 0.44 | 0.36 | 0.13 | 0.22 | 1.12 |
| 40 kg | 0.62 | 0.48 | 0.03 | 0.03 | 30.9 | 0.00 | 0.53 | 0.38 | 0.15 | 0.21 | 1.08 |
| 60 kg | 0.47 | 0.35 | 0.06 | 0.10 | 38.2 | 0.01 | 0.64 | 0.44 | 0.26 | 0.34 | 1.09 |
| 80 kg | 0.33 | 0.22 | 0.11 | 0.07 | 42.9 | 0.01 | 0.73 | 0.56 | 0.43 | 0.51 | 1.09 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x+y + part 0 corner -x-y | 0.83 | 0.67 | 0.75 | 0.58 |
| long | part 0 -x seg 2/2 + part 0 corner -x-y | 0.67 | 0.92 | 0.42 | 0.33 |
| sphere | sector 135 + sector 225 | 0.75 | 0.92 | 0.67 | 0.83 |
| cylinder | part 0 corner -x-y + part 0 -x seg 2/2 | 0.67 | 0.42 | 0.08 | 0.17 |
| arch | part 3 -x + part 2 -x | 0.83 | 1.00 | 0.75 | 0.42 |
| dumbbell | part 0 -x + part 1 -x | 0.67 | 0.42 | 0.50 | 0.33 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.83 | 0.50 | 0.42 | 0.25 |
| beam (unseen) | part 0 -x seg 2/5 + part 0 -x seg 4/5 | 0.50 | 0.25 | 0.08 | 0.00 |
| l_shape (unseen) | part 1 -x + part 0 corner -x-y | 0.92 | 0.58 | 0.42 | 0.17 |
| asym (unseen) | part 1 -x + part 0 corner -x+y | 0.75 | 0.33 | 0.08 | 0.00 |
| u_channel (unseen) | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.67 | 0.83 | 0.67 | 0.33 |
| plus (unseen) | part 0 corner -x-y + part 0 corner -x+y | 0.67 | 0.58 | 0.75 | 0.58 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.73 | 0.23 | 0.04 | 0.00 | 0.00 | 0.02 | 9.88 |
| 40 kg | 0.62 | 0.31 | 0.07 | 0.00 | 0.00 | 0.01 | 8.49 |
| 60 kg | 0.47 | 0.37 | 0.17 | 0.00 | 0.00 | 0.00 | 8.96 |
| 80 kg | 0.33 | 0.49 | 0.18 | 0.00 | 0.00 | 0.01 | 7.84 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.26 | 0.71 | 0.84 | 0.00 | 1.00 | 0.27 | 0.68 | 0.85 | 0.00 |
| 40 kg | 1.00 | 0.25 | 0.73 | 0.88 | 0.00 | 1.00 | 0.24 | 0.72 | 0.89 | 0.00 |
| 60 kg | 1.00 | 0.25 | 0.72 | 0.92 | 0.00 | 1.00 | 0.25 | 0.70 | 0.91 | 0.00 |
| 80 kg | 1.00 | 0.23 | 0.73 | 0.95 | 0.00 | 1.00 | 0.26 | 0.70 | 0.93 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.83 | 2.07 | 0.07 | 0.79 | 2.04 | 0.07 |
| 40 kg | 0.82 | 2.21 | 0.08 | 0.78 | 2.02 | 0.09 |
| 60 kg | 0.81 | 2.05 | 0.09 | 0.78 | 2.31 | 0.11 |
| 80 kg | 0.77 | 1.88 | 0.10 | 0.75 | 2.52 | 0.14 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.54 | 0.52 | 0.30 |
| 40 kg | 0.59 | 0.54 | 0.31 |
| 60 kg | 0.64 | 0.54 | 0.27 |
| 80 kg | 0.67 | 0.58 | 0.25 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.54 | 0.46 | 27.43 | 9.88 | 0.28 | 0.24 | 8.27 | 0.00 | 0.29 |
| 40 kg | 1.37 | 0.46 | 26.81 | 8.49 | 0.58 | 0.74 | 4.82 | 0.00 | 0.26 |
| 60 kg | 1.50 | 0.46 | 26.09 | 8.96 | 0.49 | 1.40 | 2.01 | 0.00 | 0.27 |
| 80 kg | 0.79 | 0.51 | 27.15 | 7.84 | 0.51 | 2.81 | 0.40 | 0.00 | 0.27 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 108 | 261 | 202 |
| 40 kg | 146 | 309 | 262 |
| 60 kg | 174 | 344 | 303 |
| 80 kg | 190 | 360 | 341 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.13 | 0.19 | 0.27 | 0.48 |
| long | 0.12 | 0.16 | 0.27 | 0.50 |
| sphere | 0.25 | 0.30 | 0.46 | 0.53 |
| cylinder | 0.14 | 0.20 | 0.31 | 0.46 |
| arch | 0.14 | 0.12 | 0.20 | 0.30 |
| dumbbell | 0.10 | 0.09 | 0.20 | 0.46 |
| t_shape | 0.09 | 0.07 | 0.18 | 0.48 |
| beam | 0.15 | 0.18 | 0.39 | 0.44 |
| l_shape | 0.11 | 0.11 | 0.15 | 0.30 |
| asym | 0.11 | 0.14 | 0.41 | 0.57 |
| u_channel | 0.11 | 0.13 | 0.19 | 0.43 |
| plus | 0.06 | 0.05 | 0.07 | 0.17 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.78 | 0.75 | 0.75 | 0.64 |
| B_left | 0.78 | 0.67 | 0.39 | 0.28 |
| C_backright | 0.64 | 0.56 | 0.39 | 0.28 |
| D_far_turn | 0.72 | 0.50 | 0.33 | 0.14 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 39% | 0% | 61% | 39% | 4% | 57% |  |  | 16% | 63% | 45% | 22% |
| 40 kg | 34% | 0% | 66% | 48% | 2% | 50% |  |  | 17% | 65% | 41% | 24% |
| 60 kg | 33% | 0% | 67% | 53% | 2% | 45% |  |  | 19% | 75% | 29% | 24% |
| 80 kg | 31% | 0% | 69% | 58% | 2% | 40% |  |  | 20% | 80% | 24% | 25% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 145 | 0.90 | 7% | 14% | 31% | 55% |
| 40 kg | 174 | 0.91 | 6% | 19% | 41% | 40% |
| 60 kg | 198 | 0.90 | 7% | 23% | 45% | 32% |
| 80 kg | 213 | 0.90 | 6% | 30% | 44% | 26% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 61% | 0.19 | 0.41 | 0.13 | 0.75 | 8 | 0 | 6 | 0 | 0 | 2 | 55 | 0.00 |  |
| 40 kg | 59% | 0.14 | 0.55 | 0.11 | 0.70 | 5 | 0 | 3 | 0 | 0 | 2 | 78 | 0.00 |  |
| 60 kg | 56% | 0.11 | 0.70 | 0.09 | 0.38 | 3 | 0 | 1 | 0 | 0 | 2 | 136 | 0.00 |  |
| 80 kg | 51% | 0.08 | 0.77 | 0.07 | 0.47 | 3 | 0 | 1 | 0 | 0 | 2 | 129 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.71 | 59% | 26% | 0.92 | 64% | 0.11 | 0 | 0 | 0 | 0 | 0 | 0 |
| long | 0.58 | 56% | 24% | 0.91 | 60% | 0.09 | 2 | 0 | 1 | 0 | 0 | 1 |
| sphere | 0.79 | 31% | 10% | 0.92 | 74% | 0.25 | 9 | 0 | 2 | 0 | 0 | 7 |
| cylinder | 0.33 | 31% | 11% | 0.90 | 62% | 0.13 | 5 | 0 | 5 | 0 | 0 | 0 |
| arch | 0.75 | 57% | 27% | 0.85 | 61% | 0.11 | 3 | 0 | 2 | 0 | 0 | 1 |
| dumbbell | 0.48 | 47% | 18% | 0.90 | 47% | 0.08 | 12 | 0 | 7 | 0 | 0 | 5 |
| t_shape | 0.50 | 59% | 29% | 0.91 | 57% | 0.07 | 1 | 0 | 1 | 0 | 0 | 1 |
| beam | 0.21 | 34% | 18% | 0.84 | 33% | 0.09 | 12 | 0 | 10 | 0 | 0 | 2 |
| l_shape | 0.52 | 55% | 25% | 0.92 | 57% | 0.08 | 2 | 0 | 0 | 0 | 0 | 2 |
| asym | 0.29 | 60% | 28% | 0.93 | 53% | 0.07 | 2 | 0 | 0 | 0 | 0 | 1 |
| u_channel | 0.62 | 53% | 20% | 0.92 | 56% | 0.09 | 5 | 0 | 3 | 0 | 0 | 2 |
| plus | 0.65 | 53% | 23% | 0.90 | 59% | 0.08 | 2 | 0 | 2 | 0 | 0 | 0 |
