# Pair evaluation: dg-ex2b16k-wrench

policy: Stage 4 contact policy logs/marl2/ex2b_aa_s0/model_16000.pt (robots start at their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.63 | 0.58 | 0.01 | 0.01 | 24.3 | 0.02 | 0.44 | 0.49 | 0.24 | 0.40 | 0.98 |
| 40 kg | 0.55 | 0.45 | 0.01 | 0.01 | 29.6 | 0.01 | 0.50 | 0.53 | 0.26 | 0.36 | 0.97 |
| 60 kg | 0.35 | 0.26 | 0.01 | 0.04 | 32.3 | 0.01 | 0.54 | 0.63 | 0.33 | 0.40 | 0.95 |
| 80 kg | 0.20 | 0.16 | 0.05 | 0.05 | 37.8 | 0.01 | 0.59 | 0.71 | 0.42 | 0.48 | 0.94 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x-y + part 0 corner -x+y | 1.00 | 0.92 | 0.42 | 0.08 |
| long | part 0 corner -x+y + part 0 -x seg 1/2 | 0.67 | 0.92 | 0.67 | 0.33 |
| sphere | sector 225 + sector 135 | 1.00 | 0.92 | 0.92 | 0.75 |
| cylinder | part 0 corner -x+y + part 0 -x seg 1/2 | 0.33 | 0.25 | 0.25 | 0.25 |
| arch | part 2 -x + part 3 -x | 0.75 | 0.58 | 0.33 | 0.25 |
| dumbbell | part 1 -x + part 0 -x | 0.58 | 0.42 | 0.33 | 0.17 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.83 | 0.58 | 0.58 | 0.33 |
| beam (unseen) | part 0 -x seg 4/5 + part 0 -x seg 2/5 | 0.50 | 0.25 | 0.00 | 0.00 |
| l_shape (unseen) | part 0 corner -x-y + part 1 -x | 0.67 | 0.67 | 0.17 | 0.00 |
| asym (unseen) | part 1 corner -x-y + part 0 -x | 0.58 | 0.50 | 0.08 | 0.00 |
| u_channel (unseen) | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.33 | 0.25 | 0.25 | 0.00 |
| plus (unseen) | part 1 corner -x+y + part 1 corner -x-y | 0.33 | 0.33 | 0.25 | 0.25 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.63 | 0.35 | 0.01 | 0.00 | 0.00 | 0.03 | 5.33 |
| 40 kg | 0.55 | 0.43 | 0.02 | 0.00 | 0.00 | 0.01 | 3.70 |
| 60 kg | 0.35 | 0.59 | 0.06 | 0.00 | 0.00 | 0.00 | 2.39 |
| 80 kg | 0.20 | 0.70 | 0.10 | 0.00 | 0.00 | 0.00 | 1.19 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.26 | 0.78 | 0.86 | 0.00 | 1.00 | 0.28 | 0.77 | 0.83 | 0.00 |
| 40 kg | 1.00 | 0.26 | 0.81 | 0.88 | 0.00 | 1.00 | 0.27 | 0.80 | 0.87 | 0.00 |
| 60 kg | 1.00 | 0.20 | 0.87 | 0.94 | 0.00 | 1.00 | 0.22 | 0.85 | 0.91 | 0.00 |
| 80 kg | 1.00 | 0.20 | 0.89 | 0.96 | 0.00 | 1.00 | 0.17 | 0.90 | 0.97 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.95 | 1.47 | 0.02 | 0.95 | 1.19 | 0.01 |
| 40 kg | 0.92 | 1.18 | 0.02 | 0.94 | 1.20 | 0.02 |
| 60 kg | 0.95 | 0.75 | 0.02 | 0.95 | 0.87 | 0.02 |
| 80 kg | 0.97 | 0.36 | 0.02 | 0.97 | 0.34 | 0.03 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.58 | 0.58 | 0.22 |
| 40 kg | 0.64 | 0.64 | 0.20 |
| 60 kg | 0.73 | 0.72 | 0.18 |
| 80 kg | 0.76 | 0.75 | 0.17 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 2.61 | 0.53 | 20.13 | 5.33 | 0.00 | 0.00 | 0.00 | 0.00 | 0.30 |
| 40 kg | 3.91 | 0.59 | 19.20 | 3.70 | 0.00 | 0.00 | 0.00 | 0.00 | 0.27 |
| 60 kg | 2.18 | 0.68 | 19.29 | 2.39 | 0.00 | 0.00 | 0.00 | 0.00 | 0.22 |
| 80 kg | 1.12 | 0.71 | 19.00 | 1.19 | 0.00 | 0.00 | 0.00 | 0.00 | 0.16 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 93 | 245 | 173 |
| 40 kg | 128 | 305 | 232 |
| 60 kg | 158 | 328 | 279 |
| 80 kg | 182 | 340 | 311 |

## executor v2: holding and the team-ready barrier (time every robot of the push group is told to hold; the object's mean speed then and the share of it above 2 cm/s (gate: under 2 cm/s); each robot's contact force while told to hold; delay from team ready to both robots pressing (gate: under 0.2 s))

| mass | all holding (s) | object speed (m/s) | moving > 2 cm/s | force while holding (N) | ready to push (s) |
|---|---|---|---|---|---|
| 20 kg | 1.08 | 0.03 | 0.15 | 7 | 0.13 |
| 40 kg | 0.97 | 0.01 | 0.10 | 10 | 0.07 |
| 60 kg | 1.01 | 0.01 | 0.07 | 13 | 0.33 |
| 80 kg | 0.88 | 0.01 | 0.06 | 11 | 0.08 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.31 | 0.22 | 0.25 | 0.51 |
| long | 0.29 | 0.36 | 0.42 | 0.44 |
| sphere | 0.44 | 0.55 | 0.81 | 0.84 |
| cylinder | 0.24 | 0.28 | 0.41 | 0.56 |
| arch | 0.24 | 0.28 | 0.24 | 0.25 |
| dumbbell | 0.14 | 0.21 | 0.16 | 0.24 |
| t_shape | 0.33 | 0.31 | 0.40 | 0.58 |
| beam | 0.38 | 0.43 | 0.43 | 0.50 |
| l_shape | 0.15 | 0.11 | 0.06 | 0.06 |
| asym | 0.19 | 0.22 | 0.46 | 0.61 |
| u_channel | 0.15 | 0.09 | 0.19 | 0.36 |
| plus | 0.05 | 0.06 | 0.08 | 0.08 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.83 | 0.78 | 0.58 | 0.42 |
| B_left | 0.56 | 0.50 | 0.28 | 0.14 |
| C_backright | 0.67 | 0.61 | 0.39 | 0.14 |
| D_far_turn | 0.47 | 0.31 | 0.17 | 0.11 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 24% | 24% | 52% | 38% | 5% | 57% | 6% | 49% | 11% | 53% | 53% | 15% |
| 40 kg | 21% | 21% | 58% | 48% | 3% | 49% | 8% | 46% | 9% | 59% | 43% | 14% |
| 60 kg | 14% | 15% | 71% | 53% | 2% | 45% | 8% | 53% | 9% | 67% | 35% | 13% |
| 80 kg | 10% | 10% | 80% | 55% | 2% | 43% | 7% | 59% | 9% | 76% | 28% | 14% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 135 | 0.89 | 7% | 11% | 24% | 66% |
| 40 kg | 165 | 0.90 | 6% | 15% | 29% | 56% |
| 60 kg | 187 | 0.91 | 5% | 22% | 35% | 44% |
| 80 kg | 202 | 0.91 | 6% | 26% | 39% | 35% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 47% | 0.17 | 0.57 | 0.14 | 1.19 | 22 | 0 | 4 | 15 | 0 | 3 | 58 | 3.33 | 15.86 |
| 40 kg | 45% | 0.13 | 0.71 | 0.11 | 1.38 | 25 | 0 | 6 | 17 | 0 | 2 | 114 | 3.00 | 9.66 |
| 60 kg | 45% | 0.09 | 0.77 | 0.08 | 1.01 | 22 | 0 | 5 | 15 | 0 | 1 | 108 | 3.04 | 7.88 |
| 80 kg | 39% | 0.06 | 0.80 | 0.05 | 0.85 | 17 | 0 | 5 | 11 | 0 | 1 | 124 | 2.56 | 5.37 |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.60 | 54% | 24% | 0.94 | 55% | 0.11 | 4 | 0 | 0 | 4 | 0 | 0 |
| long | 0.65 | 53% | 23% | 0.92 | 53% | 0.11 | 11 | 0 | 3 | 6 | 0 | 1 |
| sphere | 0.90 | 36% | 13% | 0.92 | 88% | 0.28 | 1 | 0 | 0 | 0 | 0 | 0 |
| cylinder | 0.27 | 36% | 11% | 0.91 | 48% | 0.08 | 23 | 0 | 7 | 15 | 0 | 0 |
| arch | 0.48 | 51% | 23% | 0.83 | 41% | 0.10 | 30 | 0 | 2 | 28 | 0 | 0 |
| dumbbell | 0.38 | 51% | 17% | 0.92 | 34% | 0.08 | 32 | 0 | 4 | 28 | 0 | 0 |
| t_shape | 0.58 | 61% | 28% | 0.93 | 52% | 0.12 | 18 | 0 | 0 | 17 | 0 | 0 |
| beam | 0.19 | 41% | 19% | 0.82 | 21% | 0.05 | 35 | 0 | 23 | 11 | 1 | 0 |
| l_shape | 0.38 | 42% | 11% | 0.90 | 39% | 0.07 | 19 | 0 | 7 | 7 | 0 | 4 |
| asym | 0.29 | 62% | 30% | 0.93 | 44% | 0.05 | 13 | 0 | 2 | 11 | 0 | 0 |
| u_channel | 0.21 | 40% | 11% | 0.91 | 28% | 0.05 | 37 | 0 | 13 | 21 | 0 | 3 |
| plus | 0.29 | 52% | 12% | 0.90 | 27% | 0.05 | 36 | 0 | 0 | 26 | 0 | 9 |
