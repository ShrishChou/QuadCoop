# Pair evaluation: dg-s4e-expert

policy: Stage 4 contact policy logs/marl2/s4e_aa_s0/model_12000.pt (robots start at their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.65 | 0.57 | 0.01 | 0.01 | 22.1 | 0.02 | 0.54 | 0.52 | 0.26 | 0.36 | 1.06 |
| 40 kg | 0.57 | 0.49 | 0.01 | 0.03 | 23.8 | 0.01 | 0.59 | 0.59 | 0.32 | 0.39 | 1.04 |
| 60 kg | 0.42 | 0.33 | 0.03 | 0.03 | 34.7 | 0.01 | 0.68 | 0.68 | 0.46 | 0.54 | 1.04 |
| 80 kg | 0.23 | 0.16 | 0.06 | 0.06 | 33.9 | 0.01 | 0.77 | 0.79 | 0.61 | 0.66 | 1.01 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x+y + part 0 corner -x-y | 1.00 | 0.83 | 0.50 | 0.17 |
| long | part 0 -x seg 2/2 + part 0 corner -x-y | 0.83 | 0.67 | 0.50 | 0.25 |
| sphere | sector 135 + sector 225 | 1.00 | 1.00 | 1.00 | 0.92 |
| cylinder | part 0 corner -x-y + part 0 -x seg 2/2 | 0.25 | 0.25 | 0.25 | 0.17 |
| arch | part 3 -x + part 2 -x | 0.50 | 0.42 | 0.67 | 0.33 |
| dumbbell | part 0 -x + part 1 -x | 0.58 | 0.58 | 0.42 | 0.33 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.75 | 0.75 | 0.42 | 0.08 |
| beam (unseen) | part 0 -x seg 2/5 + part 0 -x seg 4/5 | 0.42 | 0.33 | 0.00 | 0.00 |
| l_shape (unseen) | part 1 -x + part 0 corner -x-y | 0.75 | 0.42 | 0.58 | 0.08 |
| asym (unseen) | part 1 -x + part 0 corner -x+y | 0.67 | 0.25 | 0.17 | 0.00 |
| u_channel (unseen) | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.33 | 0.50 | 0.33 | 0.17 |
| plus (unseen) | part 0 corner -x-y + part 0 corner -x+y | 0.67 | 0.83 | 0.17 | 0.25 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.65 | 0.33 | 0.02 | 0.01 | 0.00 | 0.00 | 6.97 |
| 40 kg | 0.57 | 0.38 | 0.04 | 0.01 | 0.00 | 0.01 | 5.44 |
| 60 kg | 0.42 | 0.51 | 0.07 | 0.00 | 0.00 | 0.00 | 6.66 |
| 80 kg | 0.23 | 0.65 | 0.12 | 0.00 | 0.00 | 0.00 | 5.44 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.19 | 0.81 | 0.89 | 0.00 | 1.00 | 0.16 | 0.84 | 0.91 | 0.00 |
| 40 kg | 1.00 | 0.14 | 0.89 | 0.95 | 0.00 | 1.00 | 0.16 | 0.85 | 0.95 | 0.00 |
| 60 kg | 1.00 | 0.12 | 0.91 | 0.97 | 0.00 | 1.00 | 0.17 | 0.84 | 0.97 | 0.00 |
| 80 kg | 1.00 | 0.13 | 0.88 | 0.99 | 0.00 | 1.00 | 0.14 | 0.87 | 0.98 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.95 | 1.14 | 0.04 | 0.99 | 1.21 | 0.04 |
| 40 kg | 0.97 | 0.77 | 0.04 | 0.97 | 0.82 | 0.04 |
| 60 kg | 0.98 | 0.75 | 0.03 | 0.96 | 0.91 | 0.05 |
| 80 kg | 0.99 | 0.46 | 0.05 | 0.96 | 0.59 | 0.06 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.67 | 0.71 | 0.32 |
| 40 kg | 0.78 | 0.75 | 0.29 |
| 60 kg | 0.83 | 0.77 | 0.29 |
| 80 kg | 0.81 | 0.81 | 0.25 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 2.10 | 0.58 | 20.52 | 6.97 | 3.40 | 0.14 | 6.91 | 0.00 | 0.22 |
| 40 kg | 1.40 | 0.66 | 20.02 | 5.44 | 3.40 | 0.88 | 5.09 | 0.00 | 0.17 |
| 60 kg | 0.67 | 0.72 | 22.27 | 6.66 | 3.79 | 3.47 | 2.00 | 0.00 | 0.16 |
| 80 kg | 0.27 | 0.70 | 23.21 | 5.44 | 2.51 | 6.72 | 0.88 | 0.00 | 0.17 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 87 | 232 | 159 |
| 40 kg | 127 | 298 | 227 |
| 60 kg | 156 | 320 | 273 |
| 80 kg | 180 | 341 | 311 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.27 | 0.33 | 0.61 | 0.74 |
| long | 0.18 | 0.39 | 0.56 | 0.68 |
| sphere | 0.47 | 0.62 | 0.67 | 0.76 |
| cylinder | 0.19 | 0.27 | 0.45 | 0.52 |
| arch | 0.27 | 0.30 | 0.42 | 0.42 |
| dumbbell | 0.15 | 0.37 | 0.27 | 0.74 |
| t_shape | 0.42 | 0.44 | 0.48 | 0.74 |
| beam | 0.26 | 0.25 | 0.50 | 0.74 |
| l_shape | 0.21 | 0.24 | 0.40 | 0.54 |
| asym | 0.33 | 0.24 | 0.55 | 0.68 |
| u_channel | 0.28 | 0.24 | 0.39 | 0.52 |
| plus | 0.09 | 0.12 | 0.26 | 0.30 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.83 | 0.81 | 0.61 | 0.50 |
| B_left | 0.64 | 0.53 | 0.42 | 0.11 |
| C_backright | 0.58 | 0.53 | 0.36 | 0.22 |
| D_far_turn | 0.53 | 0.42 | 0.28 | 0.08 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 24% | 0% | 76% | 28% | 5% | 68% |  |  | 10% | 47% | 60% | 17% |
| 40 kg | 18% | 0% | 82% | 40% | 3% | 57% |  |  | 10% | 49% | 53% | 15% |
| 60 kg | 16% | 0% | 84% | 46% | 2% | 52% |  |  | 9% | 57% | 47% | 17% |
| 80 kg | 16% | 0% | 84% | 52% | 2% | 46% |  |  | 12% | 63% | 42% | 18% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 128 | 0.89 | 8% | 9% | 29% | 62% |
| 40 kg | 163 | 0.91 | 6% | 16% | 40% | 44% |
| 60 kg | 184 | 0.91 | 5% | 21% | 44% | 36% |
| 80 kg | 204 | 0.91 | 5% | 26% | 45% | 28% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 55% | 0.20 | 0.54 | 0.16 | 1.21 | 15 | 0 | 14 | 0 | 0 | 0 | 62 | 0.00 |  |
| 40 kg | 58% | 0.17 | 0.68 | 0.14 | 0.87 | 10 | 0 | 10 | 0 | 0 | 1 | 65 | 0.00 |  |
| 60 kg | 50% | 0.10 | 0.75 | 0.09 | 1.07 | 9 | 1 | 8 | 0 | 0 | 0 | 95 | 0.00 |  |
| 80 kg | 45% | 0.07 | 0.80 | 0.06 | 0.69 | 6 | 0 | 5 | 0 | 0 | 0 | 129 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.62 | 49% | 20% | 0.92 | 64% | 0.13 | 2 | 0 | 2 | 0 | 0 | 0 |
| long | 0.56 | 46% | 20% | 0.92 | 55% | 0.10 | 6 | 0 | 6 | 0 | 0 | 0 |
| sphere | 0.98 | 27% | 8% | 0.92 | 89% | 0.30 | 0 | 0 | 0 | 0 | 0 | 0 |
| cylinder | 0.23 | 19% | 6% | 0.92 | 45% | 0.10 | 18 | 0 | 18 | 0 | 0 | 0 |
| arch | 0.48 | 48% | 26% | 0.83 | 51% | 0.12 | 15 | 1 | 14 | 0 | 0 | 0 |
| dumbbell | 0.48 | 42% | 17% | 0.91 | 48% | 0.10 | 13 | 0 | 12 | 0 | 0 | 0 |
| t_shape | 0.50 | 47% | 23% | 0.92 | 51% | 0.10 | 12 | 0 | 11 | 0 | 0 | 0 |
| beam | 0.19 | 38% | 20% | 0.86 | 28% | 0.07 | 16 | 1 | 15 | 0 | 0 | 0 |
| l_shape | 0.46 | 44% | 15% | 0.90 | 47% | 0.08 | 7 | 0 | 6 | 0 | 0 | 1 |
| asym | 0.27 | 58% | 26% | 0.91 | 51% | 0.07 | 3 | 0 | 3 | 0 | 0 | 0 |
| u_channel | 0.33 | 36% | 14% | 0.92 | 46% | 0.11 | 17 | 0 | 16 | 0 | 0 | 1 |
| plus | 0.48 | 42% | 19% | 0.90 | 49% | 0.09 | 10 | 1 | 9 | 0 | 0 | 1 |
