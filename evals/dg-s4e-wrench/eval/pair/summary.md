# Pair evaluation: dg-s4e-wrench

policy: Stage 4 contact policy logs/marl2/s4e_aa_s0/model_12000.pt (robots start at their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.69 | 0.61 | 0.01 | 0.01 | 26.1 | 0.02 | 0.50 | 0.51 | 0.25 | 0.37 | 0.99 |
| 40 kg | 0.60 | 0.49 | 0.03 | 0.01 | 30.6 | 0.02 | 0.52 | 0.60 | 0.29 | 0.38 | 1.00 |
| 60 kg | 0.37 | 0.28 | 0.06 | 0.04 | 34.2 | 0.01 | 0.57 | 0.70 | 0.36 | 0.42 | 0.98 |
| 80 kg | 0.21 | 0.16 | 0.05 | 0.05 | 30.3 | 0.01 | 0.66 | 0.74 | 0.45 | 0.48 | 0.95 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x-y + part 0 corner -x+y | 1.00 | 0.92 | 0.50 | 0.00 |
| long | part 0 corner -x+y + part 0 -x seg 1/2 | 0.50 | 0.58 | 0.50 | 0.33 |
| sphere | sector 225 + sector 135 | 0.92 | 0.83 | 0.92 | 0.92 |
| cylinder | part 0 corner -x+y + part 0 -x seg 1/2 | 0.50 | 0.33 | 0.25 | 0.25 |
| arch | part 2 -x + part 3 -x | 0.83 | 0.75 | 0.42 | 0.17 |
| dumbbell | part 1 -x + part 0 -x | 0.67 | 0.50 | 0.33 | 0.33 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.50 | 0.50 | 0.42 | 0.17 |
| beam (unseen) | part 0 -x seg 4/5 + part 0 -x seg 2/5 | 0.50 | 0.33 | 0.00 | 0.00 |
| l_shape (unseen) | part 0 corner -x-y + part 1 -x | 0.83 | 0.83 | 0.33 | 0.00 |
| asym (unseen) | part 1 corner -x-y + part 0 -x | 0.58 | 0.33 | 0.17 | 0.00 |
| u_channel (unseen) | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.75 | 0.58 | 0.17 | 0.08 |
| plus (unseen) | part 1 corner -x+y + part 1 corner -x-y | 0.75 | 0.75 | 0.42 | 0.25 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.69 | 0.28 | 0.02 | 0.00 | 0.00 | 0.01 | 6.84 |
| 40 kg | 0.60 | 0.35 | 0.04 | 0.00 | 0.00 | 0.01 | 4.93 |
| 60 kg | 0.37 | 0.53 | 0.10 | 0.00 | 0.00 | 0.00 | 2.90 |
| 80 kg | 0.21 | 0.69 | 0.10 | 0.00 | 0.00 | 0.00 | 1.73 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.32 | 0.75 | 0.80 | 0.00 | 1.00 | 0.28 | 0.75 | 0.84 | 0.00 |
| 40 kg | 1.00 | 0.29 | 0.77 | 0.82 | 0.00 | 1.00 | 0.25 | 0.81 | 0.88 | 0.00 |
| 60 kg | 1.00 | 0.18 | 0.86 | 0.93 | 0.00 | 1.00 | 0.23 | 0.82 | 0.92 | 0.00 |
| 80 kg | 1.00 | 0.17 | 0.87 | 0.94 | 0.00 | 1.00 | 0.21 | 0.85 | 0.94 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.93 | 1.72 | 0.03 | 0.96 | 1.85 | 0.04 |
| 40 kg | 0.93 | 1.76 | 0.04 | 0.95 | 1.56 | 0.04 |
| 60 kg | 0.95 | 1.20 | 0.04 | 0.97 | 1.65 | 0.04 |
| 80 kg | 0.97 | 0.64 | 0.05 | 0.94 | 0.33 | 0.04 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.63 | 0.63 | 0.26 |
| 40 kg | 0.65 | 0.71 | 0.24 |
| 60 kg | 0.76 | 0.74 | 0.20 |
| 80 kg | 0.78 | 0.77 | 0.18 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 6.29 | 0.43 | 23.60 | 6.84 | 0.00 | 0.00 | 0.00 | 0.00 | 0.35 |
| 40 kg | 6.83 | 0.49 | 24.42 | 4.93 | 0.00 | 0.00 | 0.00 | 0.00 | 0.30 |
| 60 kg | 4.85 | 0.59 | 24.61 | 2.90 | 0.00 | 0.00 | 0.00 | 0.00 | 0.23 |
| 80 kg | 5.73 | 0.62 | 24.80 | 1.73 | 0.00 | 0.00 | 0.00 | 0.00 | 0.20 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 90 | 237 | 156 |
| 40 kg | 131 | 296 | 223 |
| 60 kg | 163 | 328 | 277 |
| 80 kg | 186 | 344 | 323 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.23 | 0.20 | 0.25 | 0.44 |
| long | 0.27 | 0.28 | 0.51 | 0.61 |
| sphere | 0.63 | 0.64 | 0.74 | 0.76 |
| cylinder | 0.44 | 0.54 | 0.47 | 0.64 |
| arch | 0.13 | 0.21 | 0.15 | 0.23 |
| dumbbell | 0.12 | 0.12 | 0.22 | 0.24 |
| t_shape | 0.31 | 0.40 | 0.59 | 0.82 |
| beam | 0.17 | 0.27 | 0.42 | 0.48 |
| l_shape | 0.09 | 0.12 | 0.08 | 0.07 |
| asym | 0.32 | 0.39 | 0.59 | 0.56 |
| u_channel | 0.20 | 0.28 | 0.24 | 0.33 |
| plus | 0.11 | 0.08 | 0.09 | 0.20 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.94 | 0.89 | 0.61 | 0.44 |
| B_left | 0.72 | 0.67 | 0.25 | 0.11 |
| C_backright | 0.67 | 0.56 | 0.31 | 0.14 |
| D_far_turn | 0.44 | 0.31 | 0.31 | 0.14 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 31% | 0% | 69% | 28% | 4% | 68% |  |  | 13% | 47% | 61% | 17% |
| 40 kg | 27% | 0% | 73% | 41% | 2% | 57% |  |  | 11% | 53% | 53% | 16% |
| 60 kg | 19% | 0% | 81% | 48% | 2% | 50% |  |  | 10% | 54% | 51% | 15% |
| 80 kg | 16% | 0% | 84% | 53% | 2% | 45% |  |  | 11% | 64% | 42% | 14% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 130 | 0.90 | 7% | 7% | 30% | 63% |
| 40 kg | 164 | 0.90 | 6% | 12% | 40% | 47% |
| 60 kg | 190 | 0.91 | 5% | 19% | 47% | 34% |
| 80 kg | 208 | 0.92 | 4% | 24% | 49% | 28% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 53% | 0.18 | 0.57 | 0.15 | 1.35 | 14 | 0 | 12 | 0 | 0 | 2 | 62 | 0.00 |  |
| 40 kg | 53% | 0.14 | 0.70 | 0.12 | 1.06 | 12 | 0 | 10 | 0 | 0 | 1 | 87 | 0.00 |  |
| 60 kg | 51% | 0.09 | 0.80 | 0.08 | 0.72 | 7 | 0 | 6 | 0 | 0 | 1 | 98 | 0.00 |  |
| 80 kg | 42% | 0.06 | 0.83 | 0.06 | 0.45 | 4 | 0 | 4 | 0 | 0 | 0 | 149 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.60 | 53% | 19% | 0.94 | 63% | 0.12 | 0 | 0 | 0 | 0 | 0 | 0 |
| long | 0.48 | 43% | 19% | 0.93 | 52% | 0.11 | 12 | 0 | 12 | 0 | 0 | 0 |
| sphere | 0.90 | 30% | 9% | 0.92 | 90% | 0.30 | 1 | 0 | 0 | 0 | 0 | 1 |
| cylinder | 0.33 | 21% | 6% | 0.93 | 48% | 0.10 | 18 | 0 | 18 | 0 | 0 | 0 |
| arch | 0.54 | 55% | 19% | 0.82 | 48% | 0.09 | 4 | 0 | 2 | 0 | 0 | 2 |
| dumbbell | 0.46 | 47% | 14% | 0.91 | 45% | 0.08 | 9 | 0 | 8 | 0 | 0 | 1 |
| t_shape | 0.40 | 42% | 20% | 0.92 | 44% | 0.08 | 19 | 0 | 18 | 0 | 0 | 1 |
| beam | 0.21 | 35% | 20% | 0.87 | 23% | 0.05 | 24 | 1 | 23 | 0 | 0 | 1 |
| l_shape | 0.50 | 44% | 11% | 0.92 | 47% | 0.07 | 4 | 0 | 2 | 0 | 0 | 2 |
| asym | 0.27 | 54% | 24% | 0.92 | 50% | 0.07 | 7 | 0 | 6 | 0 | 0 | 1 |
| u_channel | 0.40 | 38% | 14% | 0.91 | 43% | 0.09 | 8 | 0 | 7 | 0 | 0 | 0 |
| plus | 0.54 | 48% | 10% | 0.91 | 45% | 0.08 | 5 | 0 | 3 | 0 | 0 | 2 |
