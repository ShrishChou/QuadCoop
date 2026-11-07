# Pair evaluation: dg-hvB-expert

policy: Stage 4 contact policy logs/marl2/hvB_aa_s0/model_13500.pt (robots start at their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.75 | 0.73 | 0.01 | 0.01 | 28.4 | 0.01 | 0.47 | 0.42 | 0.18 | 0.29 | 1.08 |
| 40 kg | 0.68 | 0.58 | 0.01 | 0.02 | 29.1 | 0.01 | 0.53 | 0.49 | 0.22 | 0.30 | 1.06 |
| 60 kg | 0.58 | 0.43 | 0.07 | 0.04 | 37.7 | 0.01 | 0.61 | 0.58 | 0.36 | 0.45 | 1.07 |
| 80 kg | 0.36 | 0.26 | 0.06 | 0.08 | 38.8 | 0.01 | 0.71 | 0.69 | 0.50 | 0.57 | 1.04 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x+y + part 0 corner -x-y | 1.00 | 0.83 | 0.58 | 0.50 |
| long | part 0 -x seg 2/2 + part 0 corner -x-y | 0.67 | 0.83 | 0.58 | 0.17 |
| sphere | sector 135 + sector 225 | 1.00 | 0.75 | 0.83 | 1.00 |
| cylinder | part 0 corner -x-y + part 0 -x seg 2/2 | 0.50 | 0.42 | 0.25 | 0.25 |
| arch | part 3 -x + part 2 -x | 0.92 | 0.92 | 0.92 | 0.67 |
| dumbbell | part 0 -x + part 1 -x | 0.83 | 0.75 | 0.58 | 0.42 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.50 | 0.75 | 0.83 | 0.50 |
| beam (unseen) | part 0 -x seg 2/5 + part 0 -x seg 4/5 | 0.83 | 0.50 | 0.25 | 0.00 |
| l_shape (unseen) | part 1 -x + part 0 corner -x-y | 0.75 | 0.67 | 0.67 | 0.00 |
| asym (unseen) | part 1 -x + part 0 corner -x+y | 0.33 | 0.42 | 0.25 | 0.00 |
| u_channel (unseen) | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.75 | 0.75 | 0.58 | 0.42 |
| plus (unseen) | part 0 corner -x-y + part 0 corner -x+y | 0.92 | 0.58 | 0.58 | 0.42 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.75 | 0.23 | 0.02 | 0.00 | 0.00 | 0.01 | 9.47 |
| 40 kg | 0.68 | 0.28 | 0.03 | 0.00 | 0.00 | 0.02 | 8.61 |
| 60 kg | 0.58 | 0.31 | 0.11 | 0.00 | 0.00 | 0.00 | 9.03 |
| 80 kg | 0.36 | 0.50 | 0.14 | 0.00 | 0.00 | 0.00 | 7.35 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.21 | 0.75 | 0.86 | 0.00 | 1.00 | 0.21 | 0.76 | 0.89 | 0.00 |
| 40 kg | 1.00 | 0.18 | 0.81 | 0.91 | 0.00 | 1.00 | 0.20 | 0.77 | 0.92 | 0.00 |
| 60 kg | 1.00 | 0.18 | 0.81 | 0.93 | 0.00 | 1.00 | 0.21 | 0.75 | 0.96 | 0.00 |
| 80 kg | 1.00 | 0.19 | 0.78 | 0.96 | 0.00 | 1.00 | 0.20 | 0.76 | 0.97 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.96 | 1.62 | 0.07 | 0.96 | 1.50 | 0.07 |
| 40 kg | 0.98 | 1.46 | 0.08 | 0.95 | 1.20 | 0.09 |
| 60 kg | 0.98 | 1.61 | 0.07 | 0.96 | 1.34 | 0.11 |
| 80 kg | 0.96 | 0.90 | 0.11 | 0.95 | 1.03 | 0.12 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.60 | 0.60 | 0.32 |
| 40 kg | 0.69 | 0.64 | 0.32 |
| 60 kg | 0.72 | 0.65 | 0.29 |
| 80 kg | 0.69 | 0.66 | 0.25 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.56 | 0.51 | 25.99 | 9.47 | 0.16 | 0.24 | 8.57 | 0.00 | 0.26 |
| 40 kg | 0.60 | 0.55 | 24.21 | 8.61 | 1.07 | 0.56 | 6.31 | 0.00 | 0.22 |
| 60 kg | 1.52 | 0.56 | 24.04 | 9.03 | 0.97 | 1.48 | 2.18 | 0.00 | 0.24 |
| 80 kg | 1.02 | 0.54 | 24.84 | 7.35 | 0.60 | 2.56 | 0.54 | 0.00 | 0.25 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 108 | 260 | 202 |
| 40 kg | 139 | 311 | 249 |
| 60 kg | 166 | 347 | 296 |
| 80 kg | 188 | 359 | 328 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.23 | 0.22 | 0.43 | 0.60 |
| long | 0.11 | 0.21 | 0.36 | 0.39 |
| sphere | 0.40 | 0.46 | 0.75 | 0.71 |
| cylinder | 0.19 | 0.20 | 0.24 | 0.42 |
| arch | 0.29 | 0.24 | 0.32 | 0.43 |
| dumbbell | 0.15 | 0.23 | 0.28 | 0.56 |
| t_shape | 0.14 | 0.19 | 0.22 | 0.59 |
| beam | 0.14 | 0.27 | 0.43 | 0.60 |
| l_shape | 0.11 | 0.13 | 0.25 | 0.51 |
| asym | 0.11 | 0.19 | 0.58 | 0.63 |
| u_channel | 0.14 | 0.20 | 0.30 | 0.37 |
| plus | 0.11 | 0.10 | 0.10 | 0.15 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.86 | 0.75 | 0.86 | 0.58 |
| B_left | 0.75 | 0.69 | 0.58 | 0.28 |
| C_backright | 0.64 | 0.67 | 0.58 | 0.47 |
| D_far_turn | 0.75 | 0.61 | 0.28 | 0.11 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 33% | 0% | 67% | 40% | 4% | 56% |  |  | 16% | 60% | 47% | 20% |
| 40 kg | 27% | 0% | 73% | 48% | 3% | 50% |  |  | 14% | 69% | 34% | 21% |
| 60 kg | 25% | 0% | 75% | 52% | 2% | 46% |  |  | 17% | 78% | 26% | 22% |
| 80 kg | 26% | 0% | 74% | 59% | 2% | 39% |  |  | 19% | 78% | 25% | 26% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 145 | 0.89 | 7% | 17% | 33% | 50% |
| 40 kg | 173 | 0.90 | 6% | 21% | 43% | 36% |
| 60 kg | 196 | 0.90 | 6% | 25% | 45% | 30% |
| 80 kg | 213 | 0.90 | 6% | 31% | 47% | 22% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 66% | 0.21 | 0.39 | 0.15 | 0.69 | 5 | 0 | 4 | 0 | 0 | 1 | 76 | 0.00 |  |
| 40 kg | 62% | 0.17 | 0.54 | 0.14 | 0.47 | 3 | 0 | 3 | 0 | 0 | 1 | 71 | 0.00 |  |
| 60 kg | 59% | 0.13 | 0.68 | 0.11 | 0.57 | 4 | 0 | 3 | 0 | 0 | 1 | 102 | 0.00 |  |
| 80 kg | 55% | 0.09 | 0.75 | 0.08 | 0.18 | 1 | 0 | 0 | 0 | 0 | 0 | 137 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.73 | 56% | 27% | 0.91 | 69% | 0.14 | 1 | 0 | 1 | 0 | 0 | 0 |
| long | 0.56 | 55% | 25% | 0.91 | 57% | 0.09 | 1 | 0 | 1 | 0 | 0 | 0 |
| sphere | 0.90 | 29% | 12% | 0.92 | 88% | 0.33 | 3 | 0 | 3 | 0 | 0 | 0 |
| cylinder | 0.35 | 26% | 8% | 0.90 | 59% | 0.09 | 4 | 0 | 4 | 0 | 0 | 0 |
| arch | 0.85 | 59% | 31% | 0.81 | 66% | 0.14 | 3 | 0 | 2 | 0 | 0 | 1 |
| dumbbell | 0.65 | 48% | 22% | 0.90 | 58% | 0.11 | 6 | 0 | 4 | 0 | 0 | 1 |
| t_shape | 0.65 | 59% | 32% | 0.91 | 61% | 0.08 | 4 | 0 | 3 | 0 | 0 | 1 |
| beam | 0.40 | 42% | 23% | 0.85 | 37% | 0.09 | 6 | 0 | 5 | 0 | 0 | 1 |
| l_shape | 0.52 | 56% | 25% | 0.92 | 60% | 0.08 | 1 | 0 | 1 | 0 | 0 | 1 |
| asym | 0.25 | 59% | 30% | 0.92 | 54% | 0.05 | 3 | 0 | 3 | 0 | 0 | 1 |
| u_channel | 0.62 | 51% | 21% | 0.91 | 60% | 0.12 | 4 | 0 | 3 | 0 | 0 | 1 |
| plus | 0.62 | 53% | 24% | 0.91 | 58% | 0.10 | 3 | 0 | 2 | 0 | 0 | 0 |
