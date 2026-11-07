# Pair evaluation: fair-hvA-expert

policy: Stage 4 contact policy logs/keep/marl2/hvA_aa_s0/model_13500.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.65 | 0.59 | 0.01 | 0.01 | 29.0 | 0.01 | 0.45 | 0.46 | 0.17 | 0.25 | 1.07 |
| 40 kg | 0.63 | 0.49 | 0.02 | 0.01 | 28.0 | 0.00 | 0.56 | 0.48 | 0.23 | 0.31 | 1.09 |
| 60 kg | 0.44 | 0.32 | 0.05 | 0.03 | 33.8 | 0.00 | 0.67 | 0.57 | 0.39 | 0.48 | 1.03 |
| 80 kg | 0.27 | 0.21 | 0.11 | 0.04 | 34.4 | 0.01 | 0.77 | 0.72 | 0.59 | 0.67 | 1.01 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x+y + part 0 corner -x-y | 0.75 | 0.75 | 0.50 | 0.17 |
| long | part 0 -x seg 2/2 + part 0 corner -x-y | 0.83 | 0.75 | 0.58 | 0.25 |
| sphere | sector 135 + sector 225 | 0.92 | 1.00 | 1.00 | 1.00 |
| cylinder | part 0 corner -x-y + part 0 -x seg 2/2 | 0.25 | 0.33 | 0.25 | 0.17 |
| arch | part 3 -x + part 2 -x | 0.92 | 0.83 | 0.42 | 0.33 |
| dumbbell | part 0 -x + part 1 -x | 0.33 | 0.67 | 0.42 | 0.33 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.67 | 0.58 | 0.33 | 0.17 |
| beam (unseen) | part 0 -x seg 2/5 + part 0 -x seg 4/5 | 0.17 | 0.08 | 0.08 | 0.00 |
| l_shape (unseen) | part 1 -x + part 0 corner -x-y | 0.92 | 0.83 | 0.67 | 0.17 |
| asym (unseen) | part 1 -x + part 0 corner -x+y | 0.42 | 0.25 | 0.08 | 0.00 |
| u_channel (unseen) | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.75 | 0.58 | 0.42 | 0.42 |
| plus (unseen) | part 0 corner -x-y + part 0 corner -x+y | 0.92 | 0.92 | 0.50 | 0.25 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.65 | 0.33 | 0.01 | 0.00 | 0.00 | 0.01 | 7.46 |
| 40 kg | 0.63 | 0.34 | 0.03 | 0.00 | 0.00 | 0.01 | 6.66 |
| 60 kg | 0.44 | 0.49 | 0.08 | 0.00 | 0.00 | 0.01 | 7.94 |
| 80 kg | 0.27 | 0.58 | 0.15 | 0.00 | 0.00 | 0.00 | 5.79 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.20 | 0.80 | 0.89 | 0.00 | 1.00 | 0.23 | 0.76 | 0.88 | 0.00 |
| 40 kg | 1.00 | 0.19 | 0.82 | 0.91 | 0.00 | 1.00 | 0.21 | 0.80 | 0.91 | 0.00 |
| 60 kg | 1.00 | 0.21 | 0.80 | 0.93 | 0.00 | 1.00 | 0.19 | 0.82 | 0.92 | 0.00 |
| 80 kg | 1.00 | 0.19 | 0.78 | 0.95 | 0.00 | 1.00 | 0.20 | 0.84 | 0.93 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.83 | 2.10 | 0.04 | 0.78 | 2.19 | 0.03 |
| 40 kg | 0.81 | 2.11 | 0.05 | 0.77 | 1.88 | 0.03 |
| 60 kg | 0.83 | 2.30 | 0.07 | 0.78 | 2.42 | 0.04 |
| 80 kg | 0.80 | 2.46 | 0.07 | 0.79 | 2.44 | 0.04 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.66 | 0.65 | 0.32 |
| 40 kg | 0.71 | 0.68 | 0.30 |
| 60 kg | 0.72 | 0.72 | 0.27 |
| 80 kg | 0.73 | 0.77 | 0.23 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.41 | 0.58 | 24.12 | 7.46 | 2.18 | 0.25 | 7.71 | 0.00 | 0.21 |
| 40 kg | 0.87 | 0.61 | 23.12 | 6.66 | 2.02 | 1.92 | 3.97 | 0.00 | 0.17 |
| 60 kg | 0.83 | 0.65 | 24.82 | 7.94 | 2.56 | 2.28 | 1.65 | 0.00 | 0.20 |
| 80 kg | 0.39 | 0.68 | 25.50 | 5.79 | 2.58 | 3.77 | 1.35 | 0.00 | 0.17 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 93 | 235 | 170 |
| 40 kg | 135 | 293 | 234 |
| 60 kg | 162 | 325 | 277 |
| 80 kg | 183 | 346 | 318 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.19 | 0.22 | 0.49 | 0.73 |
| long | 0.21 | 0.30 | 0.50 | 0.65 |
| sphere | 0.32 | 0.35 | 0.60 | 0.64 |
| cylinder | 0.10 | 0.22 | 0.44 | 0.67 |
| arch | 0.15 | 0.24 | 0.21 | 0.33 |
| dumbbell | 0.10 | 0.28 | 0.36 | 0.69 |
| t_shape | 0.20 | 0.24 | 0.44 | 0.74 |
| beam | 0.07 | 0.13 | 0.35 | 0.45 |
| l_shape | 0.17 | 0.28 | 0.29 | 0.52 |
| asym | 0.21 | 0.12 | 0.42 | 0.66 |
| u_channel | 0.21 | 0.28 | 0.33 | 0.65 |
| plus | 0.06 | 0.14 | 0.20 | 0.31 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.75 | 0.86 | 0.72 | 0.56 |
| B_left | 0.56 | 0.67 | 0.44 | 0.14 |
| C_backright | 0.61 | 0.47 | 0.33 | 0.28 |
| D_far_turn | 0.69 | 0.53 | 0.25 | 0.11 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 29% | 0% | 71% | 32% | 4% | 64% |  |  | 9% | 46% | 61% | 18% |
| 40 kg | 24% | 0% | 76% | 44% | 3% | 54% |  |  | 9% | 54% | 50% | 17% |
| 60 kg | 24% | 0% | 76% | 50% | 2% | 48% |  |  | 10% | 55% | 51% | 18% |
| 80 kg | 21% | 0% | 79% | 56% | 2% | 42% |  |  | 10% | 64% | 42% | 19% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 132 | 0.89 | 7% | 11% | 29% | 60% |
| 40 kg | 166 | 0.91 | 5% | 15% | 42% | 42% |
| 60 kg | 189 | 0.91 | 6% | 21% | 44% | 35% |
| 80 kg | 206 | 0.90 | 6% | 28% | 44% | 28% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 53% | 0.16 | 0.50 | 0.13 | 1.26 | 14 | 0 | 13 | 0 | 0 | 1 | 61 | 0.00 |  |
| 40 kg | 58% | 0.14 | 0.63 | 0.12 | 0.77 | 8 | 0 | 7 | 0 | 0 | 1 | 74 | 0.00 |  |
| 60 kg | 52% | 0.10 | 0.72 | 0.09 | 0.72 | 5 | 0 | 4 | 0 | 0 | 1 | 103 | 0.00 |  |
| 80 kg | 48% | 0.07 | 0.78 | 0.06 | 0.67 | 5 | 0 | 3 | 0 | 0 | 2 | 120 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.54 | 53% | 22% | 0.92 | 58% | 0.10 | 6 | 0 | 5 | 0 | 0 | 1 |
| long | 0.60 | 56% | 26% | 0.92 | 61% | 0.10 | 1 | 0 | 0 | 0 | 0 | 0 |
| sphere | 0.98 | 32% | 10% | 0.93 | 84% | 0.25 | 1 | 0 | 0 | 0 | 0 | 1 |
| cylinder | 0.25 | 27% | 10% | 0.91 | 54% | 0.09 | 9 | 0 | 9 | 0 | 0 | 0 |
| arch | 0.62 | 54% | 21% | 0.84 | 56% | 0.11 | 5 | 0 | 4 | 0 | 0 | 1 |
| dumbbell | 0.44 | 47% | 21% | 0.90 | 50% | 0.09 | 11 | 0 | 9 | 0 | 0 | 2 |
| t_shape | 0.44 | 51% | 23% | 0.92 | 51% | 0.09 | 13 | 0 | 11 | 0 | 0 | 2 |
| beam | 0.08 | 30% | 15% | 0.85 | 22% | 0.04 | 24 | 1 | 20 | 0 | 0 | 2 |
| l_shape | 0.65 | 52% | 20% | 0.92 | 54% | 0.08 | 3 | 0 | 2 | 0 | 0 | 1 |
| asym | 0.19 | 52% | 23% | 0.92 | 41% | 0.04 | 7 | 0 | 6 | 0 | 0 | 1 |
| u_channel | 0.54 | 44% | 16% | 0.93 | 47% | 0.10 | 9 | 0 | 7 | 0 | 0 | 2 |
| plus | 0.65 | 47% | 17% | 0.90 | 55% | 0.09 | 6 | 0 | 4 | 0 | 0 | 3 |
