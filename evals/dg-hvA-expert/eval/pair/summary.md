# Pair evaluation: dg-hvA-expert

policy: Stage 4 contact policy logs/marl2/hvA_aa_s0/model_13500.pt (robots start at their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.69 | 0.62 | 0.01 | 0.00 | 22.5 | 0.01 | 0.53 | 0.50 | 0.26 | 0.37 | 1.04 |
| 40 kg | 0.60 | 0.47 | 0.01 | 0.01 | 28.5 | 0.00 | 0.56 | 0.55 | 0.28 | 0.37 | 1.06 |
| 60 kg | 0.50 | 0.39 | 0.05 | 0.00 | 32.4 | 0.01 | 0.64 | 0.66 | 0.42 | 0.49 | 1.04 |
| 80 kg | 0.28 | 0.22 | 0.06 | 0.06 | 31.8 | 0.01 | 0.79 | 0.85 | 0.68 | 0.72 | 1.02 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x+y + part 0 corner -x-y | 1.00 | 0.92 | 0.75 | 0.08 |
| long | part 0 -x seg 2/2 + part 0 corner -x-y | 0.75 | 0.58 | 0.42 | 0.33 |
| sphere | sector 135 + sector 225 | 1.00 | 1.00 | 1.00 | 1.00 |
| cylinder | part 0 corner -x-y + part 0 -x seg 2/2 | 0.25 | 0.33 | 0.25 | 0.25 |
| arch | part 3 -x + part 2 -x | 0.67 | 0.58 | 0.50 | 0.58 |
| dumbbell | part 0 -x + part 1 -x | 0.67 | 0.67 | 0.67 | 0.25 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.58 | 0.50 | 0.42 | 0.17 |
| beam (unseen) | part 0 -x seg 2/5 + part 0 -x seg 4/5 | 0.42 | 0.33 | 0.00 | 0.00 |
| l_shape (unseen) | part 1 -x + part 0 corner -x-y | 0.92 | 0.58 | 0.50 | 0.00 |
| asym (unseen) | part 1 -x + part 0 corner -x+y | 0.42 | 0.08 | 0.33 | 0.00 |
| u_channel (unseen) | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.67 | 0.67 | 0.50 | 0.25 |
| plus (unseen) | part 0 corner -x-y + part 0 corner -x+y | 0.92 | 1.00 | 0.67 | 0.50 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.69 | 0.31 | 0.01 | 0.00 | 0.00 | 0.02 | 6.71 |
| 40 kg | 0.60 | 0.38 | 0.02 | 0.00 | 0.00 | 0.01 | 5.83 |
| 60 kg | 0.50 | 0.45 | 0.05 | 0.00 | 0.00 | 0.00 | 7.13 |
| 80 kg | 0.28 | 0.60 | 0.11 | 0.00 | 0.00 | 0.00 | 5.48 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.19 | 0.81 | 0.89 | 0.00 | 1.00 | 0.17 | 0.83 | 0.92 | 0.00 |
| 40 kg | 1.00 | 0.18 | 0.86 | 0.93 | 0.00 | 1.00 | 0.15 | 0.88 | 0.95 | 0.00 |
| 60 kg | 1.00 | 0.14 | 0.90 | 0.96 | 0.00 | 1.00 | 0.16 | 0.87 | 0.96 | 0.00 |
| 80 kg | 1.00 | 0.13 | 0.88 | 0.98 | 0.00 | 1.00 | 0.12 | 0.90 | 0.99 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.95 | 1.12 | 0.04 | 0.97 | 1.17 | 0.03 |
| 40 kg | 0.95 | 1.10 | 0.04 | 0.98 | 0.94 | 0.03 |
| 60 kg | 0.99 | 0.86 | 0.04 | 0.98 | 0.85 | 0.05 |
| 80 kg | 0.97 | 0.51 | 0.06 | 0.98 | 0.57 | 0.06 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.71 | 0.70 | 0.33 |
| 40 kg | 0.75 | 0.78 | 0.32 |
| 60 kg | 0.81 | 0.80 | 0.29 |
| 80 kg | 0.80 | 0.84 | 0.24 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.84 | 0.60 | 20.29 | 6.71 | 2.54 | 0.19 | 7.74 | 0.00 | 0.20 |
| 40 kg | 2.55 | 0.65 | 21.16 | 5.83 | 2.07 | 1.62 | 5.74 | 0.00 | 0.16 |
| 60 kg | 1.50 | 0.72 | 21.31 | 7.13 | 2.06 | 2.69 | 3.28 | 0.00 | 0.14 |
| 80 kg | 0.21 | 0.72 | 23.03 | 5.48 | 1.74 | 5.68 | 1.48 | 0.00 | 0.15 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 92 | 237 | 168 |
| 40 kg | 126 | 290 | 219 |
| 60 kg | 156 | 324 | 266 |
| 80 kg | 186 | 345 | 315 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.35 | 0.27 | 0.60 | 0.88 |
| long | 0.19 | 0.30 | 0.47 | 0.71 |
| sphere | 0.53 | 0.69 | 0.71 | 0.85 |
| cylinder | 0.19 | 0.30 | 0.32 | 0.68 |
| arch | 0.27 | 0.29 | 0.30 | 0.50 |
| dumbbell | 0.14 | 0.25 | 0.30 | 0.61 |
| t_shape | 0.26 | 0.29 | 0.53 | 0.89 |
| beam | 0.10 | 0.18 | 0.38 | 0.70 |
| l_shape | 0.27 | 0.23 | 0.33 | 0.61 |
| asym | 0.23 | 0.11 | 0.58 | 0.78 |
| u_channel | 0.34 | 0.31 | 0.32 | 0.59 |
| plus | 0.21 | 0.20 | 0.18 | 0.32 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.81 | 0.78 | 0.72 | 0.56 |
| B_left | 0.72 | 0.61 | 0.56 | 0.17 |
| C_backright | 0.61 | 0.53 | 0.47 | 0.28 |
| D_far_turn | 0.61 | 0.50 | 0.25 | 0.14 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 23% | 0% | 77% | 32% | 4% | 63% |  |  | 9% | 51% | 54% | 15% |
| 40 kg | 17% | 0% | 83% | 41% | 3% | 56% |  |  | 8% | 49% | 54% | 16% |
| 60 kg | 15% | 0% | 85% | 50% | 2% | 48% |  |  | 8% | 54% | 49% | 16% |
| 80 kg | 14% | 0% | 86% | 58% | 2% | 41% |  |  | 11% | 66% | 38% | 18% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 131 | 0.90 | 7% | 11% | 32% | 57% |
| 40 kg | 160 | 0.90 | 7% | 16% | 42% | 42% |
| 60 kg | 186 | 0.91 | 6% | 24% | 44% | 31% |
| 80 kg | 207 | 0.90 | 6% | 32% | 47% | 21% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 59% | 0.20 | 0.51 | 0.17 | 0.77 | 14 | 0 | 12 | 0 | 0 | 1 | 55 | 0.00 |  |
| 40 kg | 56% | 0.16 | 0.63 | 0.14 | 0.81 | 10 | 0 | 10 | 0 | 0 | 0 | 93 | 0.00 |  |
| 60 kg | 56% | 0.11 | 0.72 | 0.10 | 0.63 | 7 | 0 | 6 | 0 | 0 | 0 | 80 | 0.00 |  |
| 80 kg | 52% | 0.08 | 0.79 | 0.07 | 0.37 | 3 | 0 | 2 | 0 | 0 | 0 | 135 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.69 | 53% | 25% | 0.92 | 70% | 0.16 | 1 | 0 | 1 | 0 | 0 | 0 |
| long | 0.52 | 54% | 27% | 0.91 | 57% | 0.10 | 4 | 0 | 4 | 0 | 0 | 0 |
| sphere | 1.00 | 30% | 10% | 0.93 | 94% | 0.32 | 0 | 0 | 0 | 0 | 0 | 0 |
| cylinder | 0.27 | 26% | 9% | 0.91 | 50% | 0.08 | 12 | 0 | 11 | 0 | 0 | 0 |
| arch | 0.58 | 50% | 29% | 0.81 | 57% | 0.12 | 15 | 0 | 14 | 0 | 0 | 1 |
| dumbbell | 0.56 | 48% | 20% | 0.91 | 52% | 0.09 | 10 | 0 | 9 | 0 | 0 | 1 |
| t_shape | 0.42 | 45% | 25% | 0.92 | 48% | 0.09 | 20 | 0 | 18 | 0 | 0 | 1 |
| beam | 0.19 | 42% | 23% | 0.87 | 31% | 0.06 | 15 | 1 | 14 | 0 | 0 | 1 |
| l_shape | 0.50 | 50% | 19% | 0.90 | 55% | 0.10 | 2 | 0 | 2 | 0 | 0 | 0 |
| asym | 0.21 | 53% | 26% | 0.91 | 47% | 0.05 | 7 | 0 | 6 | 0 | 0 | 0 |
| u_channel | 0.52 | 42% | 17% | 0.92 | 51% | 0.12 | 10 | 0 | 9 | 0 | 0 | 1 |
| plus | 0.77 | 49% | 21% | 0.90 | 57% | 0.11 | 3 | 0 | 2 | 0 | 0 | 0 |
