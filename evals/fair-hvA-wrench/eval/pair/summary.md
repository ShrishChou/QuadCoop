# Pair evaluation: fair-hvA-wrench

policy: Stage 4 contact policy logs/keep/marl2/hvA_aa_s0/model_13500.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.60 | 0.53 | 0.00 | 0.00 | 34.8 | 0.01 | 0.37 | 0.35 | 0.10 | 0.20 | 1.07 |
| 40 kg | 0.58 | 0.49 | 0.02 | 0.00 | 38.7 | 0.01 | 0.44 | 0.43 | 0.16 | 0.26 | 1.05 |
| 60 kg | 0.39 | 0.31 | 0.06 | 0.00 | 40.8 | 0.01 | 0.50 | 0.55 | 0.23 | 0.32 | 1.00 |
| 80 kg | 0.21 | 0.15 | 0.06 | 0.05 | 35.0 | 0.02 | 0.58 | 0.62 | 0.35 | 0.43 | 0.97 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x-y + part 0 corner -x+y | 0.75 | 0.75 | 0.50 | 0.00 |
| long | part 0 corner -x+y + part 0 -x seg 1/2 | 0.50 | 0.67 | 0.58 | 0.33 |
| sphere | sector 225 + sector 135 | 1.00 | 1.00 | 1.00 | 0.92 |
| cylinder | part 0 corner -x+y + part 0 -x seg 1/2 | 0.42 | 0.25 | 0.25 | 0.25 |
| arch | part 2 -x + part 3 -x | 0.67 | 0.58 | 0.33 | 0.25 |
| dumbbell | part 1 -x + part 0 -x | 0.67 | 0.67 | 0.33 | 0.17 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.50 | 0.50 | 0.75 | 0.17 |
| beam (unseen) | part 0 -x seg 4/5 + part 0 -x seg 2/5 | 0.50 | 0.25 | 0.00 | 0.00 |
| l_shape (unseen) | part 0 corner -x-y + part 1 -x | 0.83 | 0.67 | 0.17 | 0.00 |
| asym (unseen) | part 1 corner -x-y + part 0 -x | 0.42 | 0.42 | 0.08 | 0.00 |
| u_channel (unseen) | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.50 | 0.67 | 0.33 | 0.08 |
| plus (unseen) | part 1 corner -x+y + part 1 corner -x-y | 0.50 | 0.50 | 0.33 | 0.33 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.60 | 0.40 | 0.00 | 0.00 | 0.00 | 0.04 | 6.46 |
| 40 kg | 0.58 | 0.40 | 0.02 | 0.00 | 0.00 | 0.01 | 4.60 |
| 60 kg | 0.39 | 0.56 | 0.06 | 0.00 | 0.00 | 0.00 | 2.97 |
| 80 kg | 0.21 | 0.69 | 0.10 | 0.00 | 0.00 | 0.00 | 1.51 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.43 | 0.61 | 0.75 | 0.00 | 1.00 | 0.46 | 0.59 | 0.74 | 0.00 |
| 40 kg | 1.00 | 0.39 | 0.65 | 0.78 | 0.00 | 1.00 | 0.46 | 0.63 | 0.75 | 0.00 |
| 60 kg | 1.00 | 0.36 | 0.71 | 0.83 | 0.00 | 1.00 | 0.38 | 0.69 | 0.84 | 0.00 |
| 80 kg | 1.00 | 0.33 | 0.73 | 0.87 | 0.00 | 1.00 | 0.35 | 0.72 | 0.85 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.86 | 5.11 | 0.05 | 0.86 | 5.52 | 0.03 |
| 40 kg | 0.92 | 6.25 | 0.04 | 0.84 | 6.07 | 0.04 |
| 60 kg | 0.88 | 6.25 | 0.05 | 0.90 | 5.99 | 0.04 |
| 80 kg | 0.91 | 7.51 | 0.05 | 0.89 | 6.24 | 0.04 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.52 | 0.50 | 0.26 |
| 40 kg | 0.57 | 0.55 | 0.23 |
| 60 kg | 0.63 | 0.61 | 0.20 |
| 80 kg | 0.67 | 0.64 | 0.17 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 8.11 | 0.36 | 31.28 | 6.46 | 0.00 | 0.00 | 0.00 | 0.00 | 0.43 |
| 40 kg | 9.51 | 0.42 | 30.15 | 4.60 | 0.00 | 0.00 | 0.00 | 0.00 | 0.35 |
| 60 kg | 7.72 | 0.52 | 29.70 | 2.97 | 0.00 | 0.00 | 0.00 | 0.00 | 0.30 |
| 80 kg | 7.12 | 0.57 | 28.68 | 1.51 | 0.00 | 0.00 | 0.00 | 0.00 | 0.26 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 93 | 230 | 163 |
| 40 kg | 134 | 291 | 234 |
| 60 kg | 166 | 325 | 286 |
| 80 kg | 186 | 343 | 319 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.14 | 0.17 | 0.20 | 0.38 |
| long | 0.07 | 0.14 | 0.36 | 0.49 |
| sphere | 0.18 | 0.31 | 0.37 | 0.44 |
| cylinder | 0.13 | 0.36 | 0.39 | 0.52 |
| arch | 0.09 | 0.10 | 0.19 | 0.21 |
| dumbbell | 0.10 | 0.10 | 0.12 | 0.23 |
| t_shape | 0.07 | 0.12 | 0.30 | 0.64 |
| beam | 0.10 | 0.13 | 0.23 | 0.41 |
| l_shape | 0.03 | 0.05 | 0.04 | 0.06 |
| asym | 0.12 | 0.20 | 0.30 | 0.44 |
| u_channel | 0.15 | 0.18 | 0.20 | 0.22 |
| plus | 0.02 | 0.05 | 0.10 | 0.10 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.81 | 0.81 | 0.64 | 0.42 |
| B_left | 0.44 | 0.50 | 0.25 | 0.14 |
| C_backright | 0.64 | 0.61 | 0.36 | 0.14 |
| D_far_turn | 0.53 | 0.39 | 0.31 | 0.14 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 44% | 0% | 56% | 32% | 4% | 64% |  |  | 9% | 51% | 56% | 16% |
| 40 kg | 40% | 0% | 60% | 45% | 3% | 52% |  |  | 9% | 52% | 53% | 18% |
| 60 kg | 33% | 0% | 67% | 53% | 2% | 45% |  |  | 9% | 53% | 50% | 18% |
| 80 kg | 29% | 0% | 71% | 56% | 2% | 43% |  |  | 10% | 69% | 38% | 15% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 128 | 0.90 | 7% | 8% | 27% | 65% |
| 40 kg | 165 | 0.90 | 6% | 11% | 39% | 50% |
| 60 kg | 190 | 0.91 | 5% | 16% | 46% | 38% |
| 80 kg | 208 | 0.92 | 4% | 21% | 45% | 34% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 46% | 0.13 | 0.47 | 0.09 | 1.56 | 17 | 0 | 11 | 0 | 0 | 6 | 75 | 0.00 |  |
| 40 kg | 49% | 0.10 | 0.64 | 0.08 | 1.25 | 13 | 0 | 7 | 0 | 0 | 6 | 105 | 0.00 |  |
| 60 kg | 47% | 0.07 | 0.75 | 0.06 | 0.89 | 9 | 0 | 4 | 0 | 0 | 5 | 117 | 0.00 |  |
| 80 kg | 38% | 0.05 | 0.80 | 0.04 | 0.84 | 8 | 0 | 3 | 0 | 0 | 5 | 139 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.50 | 50% | 18% | 0.93 | 51% | 0.07 | 6 | 0 | 4 | 0 | 0 | 2 |
| long | 0.52 | 56% | 20% | 0.93 | 55% | 0.07 | 5 | 0 | 1 | 0 | 0 | 4 |
| sphere | 0.98 | 32% | 6% | 0.93 | 78% | 0.17 | 2 | 0 | 0 | 0 | 0 | 2 |
| cylinder | 0.29 | 28% | 6% | 0.93 | 40% | 0.07 | 22 | 0 | 5 | 0 | 0 | 17 |
| arch | 0.46 | 59% | 17% | 0.81 | 46% | 0.08 | 9 | 0 | 3 | 0 | 0 | 6 |
| dumbbell | 0.46 | 53% | 14% | 0.92 | 43% | 0.07 | 12 | 0 | 7 | 0 | 0 | 5 |
| t_shape | 0.48 | 52% | 19% | 0.92 | 45% | 0.06 | 15 | 0 | 10 | 0 | 0 | 5 |
| beam | 0.19 | 36% | 16% | 0.84 | 22% | 0.04 | 26 | 1 | 23 | 0 | 0 | 2 |
| l_shape | 0.42 | 46% | 10% | 0.92 | 46% | 0.06 | 7 | 0 | 4 | 0 | 0 | 3 |
| asym | 0.23 | 59% | 20% | 0.92 | 38% | 0.04 | 15 | 0 | 1 | 0 | 0 | 14 |
| u_channel | 0.40 | 38% | 11% | 0.93 | 37% | 0.06 | 12 | 0 | 8 | 0 | 0 | 3 |
| plus | 0.42 | 48% | 9% | 0.91 | 39% | 0.05 | 12 | 0 | 7 | 0 | 0 | 5 |
