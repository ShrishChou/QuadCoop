# Pair evaluation: fair-hvB-wrench

policy: Stage 4 contact policy logs/keep/marl2/hvB_aa_s0/model_13500.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.65 | 0.64 | 0.00 | 0.03 | 40.7 | 0.04 | 0.32 | 0.32 | 0.07 | 0.16 | 1.06 |
| 40 kg | 0.53 | 0.47 | 0.06 | 0.06 | 38.7 | 0.07 | 0.39 | 0.35 | 0.10 | 0.19 | 1.02 |
| 60 kg | 0.35 | 0.26 | 0.06 | 0.10 | 43.7 | 0.06 | 0.39 | 0.49 | 0.15 | 0.22 | 0.98 |
| 80 kg | 0.12 | 0.10 | 0.09 | 0.12 | 39.8 | 0.05 | 0.47 | 0.54 | 0.21 | 0.29 | 0.98 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x-y + part 0 corner -x+y | 0.83 | 0.50 | 0.50 | 0.00 |
| long | part 0 corner -x+y + part 0 -x seg 1/2 | 0.58 | 0.33 | 0.42 | 0.17 |
| sphere | sector 225 + sector 135 | 0.83 | 0.67 | 0.67 | 0.42 |
| cylinder | part 0 corner -x+y + part 0 -x seg 1/2 | 0.42 | 0.33 | 0.25 | 0.08 |
| arch | part 2 -x + part 3 -x | 1.00 | 0.50 | 0.42 | 0.17 |
| dumbbell | part 1 -x + part 0 -x | 0.75 | 0.75 | 0.42 | 0.17 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.50 | 0.67 | 0.33 | 0.17 |
| beam (unseen) | part 0 -x seg 4/5 + part 0 -x seg 2/5 | 0.67 | 0.50 | 0.08 | 0.00 |
| l_shape (unseen) | part 0 corner -x-y + part 1 -x | 0.75 | 0.42 | 0.17 | 0.00 |
| asym (unseen) | part 1 corner -x-y + part 0 -x | 0.17 | 0.17 | 0.08 | 0.00 |
| u_channel (unseen) | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.58 | 0.75 | 0.50 | 0.17 |
| plus (unseen) | part 1 corner -x+y + part 1 corner -x-y | 0.75 | 0.75 | 0.33 | 0.17 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.65 | 0.32 | 0.03 | 0.00 | 0.00 | 0.02 | 8.35 |
| 40 kg | 0.53 | 0.35 | 0.12 | 0.00 | 0.00 | 0.01 | 5.26 |
| 60 kg | 0.35 | 0.49 | 0.16 | 0.00 | 0.00 | 0.00 | 3.29 |
| 80 kg | 0.12 | 0.67 | 0.21 | 0.00 | 0.00 | 0.00 | 1.69 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.47 | 0.53 | 0.71 | 0.00 | 1.00 | 0.48 | 0.53 | 0.72 | 0.00 |
| 40 kg | 1.00 | 0.46 | 0.55 | 0.77 | 0.00 | 1.00 | 0.48 | 0.51 | 0.75 | 0.00 |
| 60 kg | 1.00 | 0.44 | 0.59 | 0.82 | 0.00 | 1.00 | 0.48 | 0.56 | 0.80 | 0.00 |
| 80 kg | 1.00 | 0.36 | 0.65 | 0.86 | 0.00 | 1.00 | 0.44 | 0.58 | 0.82 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.85 | 5.55 | 0.07 | 0.84 | 4.80 | 0.07 |
| 40 kg | 0.85 | 5.84 | 0.08 | 0.83 | 5.98 | 0.09 |
| 60 kg | 0.84 | 6.36 | 0.07 | 0.83 | 6.13 | 0.10 |
| 80 kg | 0.86 | 6.65 | 0.08 | 0.86 | 6.66 | 0.10 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.40 | 0.43 | 0.29 |
| 40 kg | 0.45 | 0.41 | 0.23 |
| 60 kg | 0.50 | 0.48 | 0.20 |
| 80 kg | 0.55 | 0.49 | 0.18 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 6.88 | 0.27 | 39.24 | 8.35 | 0.00 | 0.00 | 0.00 | 0.00 | 0.50 |
| 40 kg | 5.87 | 0.29 | 33.30 | 5.26 | 0.00 | 0.00 | 0.00 | 0.00 | 0.44 |
| 60 kg | 7.51 | 0.36 | 32.04 | 3.29 | 0.00 | 0.00 | 0.00 | 0.00 | 0.45 |
| 80 kg | 7.11 | 0.38 | 30.97 | 1.69 | 0.00 | 0.00 | 0.00 | 0.00 | 0.42 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 107 | 252 | 191 |
| 40 kg | 145 | 309 | 252 |
| 60 kg | 176 | 348 | 310 |
| 80 kg | 191 | 368 | 342 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.07 | 0.10 | 0.12 | 0.16 |
| long | 0.11 | 0.11 | 0.23 | 0.21 |
| sphere | 0.09 | 0.14 | 0.21 | 0.26 |
| cylinder | 0.12 | 0.18 | 0.22 | 0.17 |
| arch | 0.10 | 0.11 | 0.13 | 0.17 |
| dumbbell | 0.08 | 0.06 | 0.10 | 0.15 |
| t_shape | 0.04 | 0.05 | 0.14 | 0.35 |
| beam | 0.07 | 0.16 | 0.20 | 0.36 |
| l_shape | 0.04 | 0.06 | 0.03 | 0.07 |
| asym | 0.05 | 0.10 | 0.19 | 0.31 |
| u_channel | 0.06 | 0.12 | 0.15 | 0.22 |
| plus | 0.02 | 0.04 | 0.04 | 0.13 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.72 | 0.58 | 0.56 | 0.22 |
| B_left | 0.72 | 0.61 | 0.42 | 0.08 |
| C_backright | 0.67 | 0.50 | 0.28 | 0.14 |
| D_far_turn | 0.50 | 0.42 | 0.14 | 0.06 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 53% | 0% | 47% | 39% | 4% | 57% |  |  | 20% | 60% | 52% | 23% |
| 40 kg | 52% | 0% | 48% | 49% | 2% | 49% |  |  | 21% | 70% | 41% | 24% |
| 60 kg | 45% | 0% | 55% | 52% | 2% | 46% |  |  | 19% | 78% | 30% | 23% |
| 80 kg | 41% | 0% | 59% | 54% | 2% | 44% |  |  | 19% | 82% | 26% | 22% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 140 | 0.89 | 8% | 10% | 30% | 60% |
| 40 kg | 176 | 0.90 | 7% | 12% | 39% | 49% |
| 60 kg | 202 | 0.91 | 5% | 14% | 44% | 41% |
| 80 kg | 214 | 0.91 | 5% | 18% | 46% | 36% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 53% | 0.14 | 0.35 | 0.09 | 1.33 | 9 | 0 | 4 | 0 | 0 | 5 | 72 | 0.00 |  |
| 40 kg | 51% | 0.11 | 0.58 | 0.08 | 1.01 | 8 | 0 | 2 | 0 | 0 | 6 | 89 | 0.00 |  |
| 60 kg | 45% | 0.07 | 0.71 | 0.06 | 0.83 | 8 | 0 | 3 | 0 | 0 | 4 | 129 | 0.00 |  |
| 80 kg | 38% | 0.05 | 0.75 | 0.04 | 0.85 | 6 | 0 | 2 | 0 | 0 | 4 | 131 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.46 | 51% | 14% | 0.93 | 47% | 0.07 | 7 | 0 | 2 | 0 | 0 | 5 |
| long | 0.38 | 55% | 16% | 0.92 | 50% | 0.07 | 5 | 0 | 3 | 0 | 0 | 2 |
| sphere | 0.65 | 28% | 4% | 0.93 | 62% | 0.14 | 9 | 0 | 2 | 0 | 0 | 7 |
| cylinder | 0.27 | 30% | 5% | 0.91 | 52% | 0.08 | 7 | 0 | 4 | 0 | 0 | 3 |
| arch | 0.52 | 60% | 19% | 0.81 | 49% | 0.08 | 7 | 0 | 3 | 0 | 0 | 4 |
| dumbbell | 0.52 | 55% | 14% | 0.92 | 48% | 0.07 | 6 | 0 | 2 | 0 | 0 | 5 |
| t_shape | 0.42 | 58% | 21% | 0.92 | 51% | 0.06 | 9 | 0 | 2 | 0 | 0 | 7 |
| beam | 0.31 | 39% | 14% | 0.84 | 27% | 0.06 | 14 | 1 | 9 | 0 | 0 | 4 |
| l_shape | 0.33 | 48% | 10% | 0.92 | 45% | 0.06 | 7 | 0 | 3 | 0 | 0 | 4 |
| asym | 0.10 | 57% | 17% | 0.91 | 38% | 0.03 | 9 | 0 | 2 | 0 | 0 | 7 |
| u_channel | 0.50 | 50% | 15% | 0.91 | 46% | 0.06 | 8 | 0 | 2 | 0 | 0 | 5 |
| plus | 0.50 | 49% | 13% | 0.91 | 48% | 0.06 | 3 | 0 | 0 | 0 | 0 | 3 |
