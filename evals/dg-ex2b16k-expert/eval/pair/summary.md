# Pair evaluation: dg-ex2b16k-expert

policy: Stage 4 contact policy logs/marl2/ex2b_aa_s0/model_16000.pt (robots start at their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.59 | 0.58 | 0.01 | 0.00 | 22.0 | 0.01 | 0.53 | 0.48 | 0.25 | 0.37 | 1.03 |
| 40 kg | 0.47 | 0.40 | 0.02 | 0.00 | 25.9 | 0.01 | 0.60 | 0.53 | 0.26 | 0.32 | 1.06 |
| 60 kg | 0.38 | 0.31 | 0.01 | 0.02 | 31.7 | 0.01 | 0.70 | 0.62 | 0.43 | 0.50 | 1.04 |
| 80 kg | 0.24 | 0.20 | 0.08 | 0.04 | 32.1 | 0.01 | 0.79 | 0.79 | 0.65 | 0.72 | 1.00 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x+y + part 0 corner -x-y | 0.67 | 0.58 | 0.50 | 0.17 |
| long | part 0 -x seg 2/2 + part 0 corner -x-y | 0.92 | 0.50 | 0.58 | 0.25 |
| sphere | sector 135 + sector 225 | 1.00 | 1.00 | 0.92 | 0.92 |
| cylinder | part 0 corner -x-y + part 0 -x seg 2/2 | 0.58 | 0.42 | 0.17 | 0.08 |
| arch | part 3 -x + part 2 -x | 0.92 | 0.50 | 0.58 | 0.42 |
| dumbbell | part 0 -x + part 1 -x | 0.25 | 0.42 | 0.42 | 0.50 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.75 | 0.67 | 0.33 | 0.08 |
| beam (unseen) | part 0 -x seg 2/5 + part 0 -x seg 4/5 | 0.08 | 0.08 | 0.00 | 0.00 |
| l_shape (unseen) | part 1 -x + part 0 corner -x-y | 0.50 | 0.58 | 0.25 | 0.00 |
| asym (unseen) | part 1 -x + part 0 corner -x+y | 0.42 | 0.08 | 0.08 | 0.00 |
| u_channel (unseen) | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.58 | 0.33 | 0.33 | 0.17 |
| plus (unseen) | part 0 corner -x-y + part 0 corner -x+y | 0.42 | 0.50 | 0.33 | 0.25 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.59 | 0.40 | 0.01 | 0.00 | 0.00 | 0.10 | 6.32 |
| 40 kg | 0.47 | 0.51 | 0.02 | 0.00 | 0.00 | 0.04 | 4.08 |
| 60 kg | 0.38 | 0.59 | 0.03 | 0.01 | 0.00 | 0.02 | 3.95 |
| 80 kg | 0.24 | 0.65 | 0.12 | 0.00 | 0.00 | 0.00 | 2.53 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.18 | 0.84 | 0.92 | 0.00 | 1.00 | 0.17 | 0.87 | 0.93 | 0.00 |
| 40 kg | 1.00 | 0.15 | 0.88 | 0.96 | 0.00 | 1.00 | 0.14 | 0.91 | 0.97 | 0.00 |
| 60 kg | 1.00 | 0.13 | 0.93 | 0.97 | 0.00 | 1.00 | 0.14 | 0.92 | 0.97 | 0.00 |
| 80 kg | 1.00 | 0.13 | 0.93 | 0.99 | 0.00 | 1.00 | 0.14 | 0.94 | 0.99 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.95 | 1.01 | 0.03 | 0.97 | 1.06 | 0.02 |
| 40 kg | 0.98 | 0.87 | 0.03 | 0.99 | 0.77 | 0.02 |
| 60 kg | 0.98 | 0.79 | 0.02 | 0.98 | 0.97 | 0.02 |
| 80 kg | 0.97 | 0.34 | 0.02 | 0.99 | 0.46 | 0.02 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.68 | 0.72 | 0.33 |
| 40 kg | 0.75 | 0.80 | 0.31 |
| 60 kg | 0.83 | 0.84 | 0.30 |
| 80 kg | 0.84 | 0.84 | 0.24 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.79 | 0.67 | 20.32 | 6.32 | 4.03 | 0.58 | 6.12 | 0.00 | 0.19 |
| 40 kg | 0.66 | 0.72 | 19.98 | 4.08 | 4.65 | 2.47 | 5.43 | 0.00 | 0.14 |
| 60 kg | 0.56 | 0.79 | 20.91 | 3.95 | 2.23 | 4.14 | 3.97 | 0.00 | 0.10 |
| 80 kg | 0.23 | 0.81 | 19.66 | 2.53 | 3.35 | 5.49 | 1.47 | 0.00 | 0.11 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 93 | 236 | 175 |
| 40 kg | 131 | 290 | 229 |
| 60 kg | 157 | 320 | 275 |
| 80 kg | 179 | 337 | 308 |

## executor v2: holding and the team-ready barrier (time every robot of the push group is told to hold; the object's mean speed then and the share of it above 2 cm/s (gate: under 2 cm/s); each robot's contact force while told to hold; delay from team ready to both robots pressing (gate: under 0.2 s))

| mass | all holding (s) | object speed (m/s) | moving > 2 cm/s | force while holding (N) | ready to push (s) |
|---|---|---|---|---|---|
| 20 kg | 0.26 | 0.03 | 0.18 | 10 | 0.12 |
| 40 kg | 0.23 | 0.01 | 0.12 | 15 | 0.08 |
| 60 kg | 0.24 | 0.01 | 0.08 | 15 | 0.07 |
| 80 kg | 0.20 | 0.01 | 0.06 | 13 | 0.06 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.29 | 0.13 | 0.44 | 0.77 |
| long | 0.31 | 0.26 | 0.39 | 0.62 |
| sphere | 0.43 | 0.59 | 0.81 | 0.89 |
| cylinder | 0.19 | 0.29 | 0.31 | 0.68 |
| arch | 0.32 | 0.29 | 0.40 | 0.52 |
| dumbbell | 0.17 | 0.28 | 0.51 | 0.71 |
| t_shape | 0.29 | 0.34 | 0.38 | 0.72 |
| beam | 0.18 | 0.24 | 0.50 | 0.66 |
| l_shape | 0.26 | 0.17 | 0.32 | 0.58 |
| asym | 0.27 | 0.20 | 0.61 | 0.78 |
| u_channel | 0.25 | 0.27 | 0.36 | 0.65 |
| plus | 0.07 | 0.09 | 0.11 | 0.28 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.64 | 0.69 | 0.58 | 0.42 |
| B_left | 0.50 | 0.42 | 0.42 | 0.19 |
| C_backright | 0.61 | 0.39 | 0.33 | 0.28 |
| D_far_turn | 0.61 | 0.39 | 0.17 | 0.06 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 17% | 12% | 71% | 38% | 6% | 57% | 9% | 50% | 6% | 57% | 46% | 13% |
| 40 kg | 12% | 9% | 80% | 46% | 3% | 50% | 11% | 46% | 7% | 54% | 49% | 13% |
| 60 kg | 8% | 6% | 86% | 53% | 2% | 44% | 10% | 51% | 5% | 61% | 41% | 17% |
| 80 kg | 7% | 6% | 87% | 59% | 2% | 39% | 9% | 50% | 6% | 65% | 40% | 15% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 133 | 0.88 | 8% | 14% | 28% | 58% |
| 40 kg | 164 | 0.89 | 8% | 20% | 37% | 43% |
| 60 kg | 184 | 0.90 | 6% | 25% | 42% | 33% |
| 80 kg | 201 | 0.90 | 6% | 32% | 41% | 27% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 56% | 0.19 | 0.47 | 0.15 | 0.94 | 17 | 0 | 8 | 8 | 0 | 0 | 107 | 3.60 | 15.23 |
| 40 kg | 52% | 0.14 | 0.58 | 0.12 | 1.15 | 15 | 0 | 9 | 6 | 0 | 0 | 63 | 3.04 | 12.20 |
| 60 kg | 50% | 0.10 | 0.72 | 0.09 | 1.17 | 11 | 0 | 5 | 5 | 0 | 1 | 109 | 3.27 | 6.70 |
| 80 kg | 46% | 0.07 | 0.80 | 0.06 | 0.94 | 11 | 1 | 4 | 6 | 0 | 0 | 121 | 2.71 | 4.54 |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.48 | 58% | 33% | 0.91 | 60% | 0.10 | 4 | 0 | 3 | 2 | 0 | 0 |
| long | 0.56 | 56% | 28% | 0.91 | 57% | 0.10 | 5 | 0 | 3 | 2 | 0 | 0 |
| sphere | 0.96 | 30% | 11% | 0.92 | 92% | 0.33 | 0 | 0 | 0 | 0 | 0 | 0 |
| cylinder | 0.31 | 34% | 12% | 0.89 | 52% | 0.08 | 14 | 0 | 12 | 1 | 0 | 0 |
| arch | 0.60 | 53% | 28% | 0.83 | 57% | 0.13 | 14 | 0 | 9 | 5 | 0 | 0 |
| dumbbell | 0.40 | 49% | 23% | 0.90 | 45% | 0.10 | 25 | 0 | 9 | 15 | 0 | 0 |
| t_shape | 0.46 | 57% | 27% | 0.92 | 52% | 0.10 | 15 | 0 | 5 | 10 | 0 | 0 |
| beam | 0.04 | 41% | 17% | 0.88 | 17% | 0.03 | 31 | 1 | 23 | 7 | 0 | 0 |
| l_shape | 0.33 | 53% | 23% | 0.91 | 45% | 0.07 | 11 | 0 | 2 | 8 | 0 | 1 |
| asym | 0.15 | 59% | 31% | 0.90 | 47% | 0.05 | 11 | 0 | 6 | 4 | 0 | 1 |
| u_channel | 0.35 | 47% | 18% | 0.90 | 43% | 0.09 | 19 | 0 | 6 | 13 | 0 | 0 |
| plus | 0.38 | 54% | 24% | 0.88 | 48% | 0.08 | 12 | 0 | 2 | 10 | 0 | 1 |
