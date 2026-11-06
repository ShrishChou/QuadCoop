# Pair evaluation: dg-ex2b16k-ap-expert

policy: Stage 4 contact policy logs/marl2/ex2b_aa_s0/model_16000.pt (robots start at their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.54 | 0.49 | 0.01 | 0.00 | 22.4 | 0.01 | 0.55 | 0.46 | 0.21 | 0.30 | 1.04 |
| 40 kg | 0.49 | 0.40 | 0.02 | 0.01 | 30.0 | 0.01 | 0.60 | 0.51 | 0.27 | 0.35 | 1.06 |
| 60 kg | 0.35 | 0.26 | 0.02 | 0.03 | 32.2 | 0.01 | 0.72 | 0.61 | 0.43 | 0.50 | 1.05 |
| 80 kg | 0.24 | 0.19 | 0.03 | 0.03 | 33.2 | 0.02 | 0.80 | 0.80 | 0.65 | 0.70 | 1.00 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x+y + part 0 corner -x-y | 0.92 | 0.42 | 0.50 | 0.33 |
| long | part 0 -x seg 2/2 + part 0 corner -x-y | 0.75 | 0.58 | 0.58 | 0.33 |
| sphere | sector 135 + sector 225 | 1.00 | 1.00 | 0.92 | 0.92 |
| cylinder | part 0 corner -x-y + part 0 -x seg 2/2 | 0.33 | 0.33 | 0.25 | 0.25 |
| arch | part 3 -x + part 2 -x | 0.75 | 0.58 | 0.50 | 0.33 |
| dumbbell | part 0 -x + part 1 -x | 0.17 | 0.50 | 0.50 | 0.33 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.42 | 0.67 | 0.25 | 0.08 |
| beam (unseen) | part 0 -x seg 2/5 + part 0 -x seg 4/5 | 0.25 | 0.00 | 0.00 | 0.00 |
| l_shape (unseen) | part 1 -x + part 0 corner -x-y | 0.58 | 0.58 | 0.25 | 0.00 |
| asym (unseen) | part 1 -x + part 0 corner -x+y | 0.33 | 0.17 | 0.17 | 0.00 |
| u_channel (unseen) | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.58 | 0.42 | 0.25 | 0.17 |
| plus (unseen) | part 0 corner -x-y + part 0 corner -x+y | 0.42 | 0.58 | 0.08 | 0.17 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.54 | 0.45 | 0.01 | 0.00 | 0.00 | 0.12 | 5.85 |
| 40 kg | 0.49 | 0.48 | 0.03 | 0.01 | 0.00 | 0.06 | 4.98 |
| 60 kg | 0.35 | 0.59 | 0.06 | 0.00 | 0.00 | 0.03 | 4.46 |
| 80 kg | 0.24 | 0.70 | 0.06 | 0.00 | 0.00 | 0.01 | 3.15 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.17 | 0.85 | 0.93 | 0.00 | 1.00 | 0.19 | 0.85 | 0.92 | 0.00 |
| 40 kg | 1.00 | 0.16 | 0.90 | 0.95 | 0.00 | 1.00 | 0.15 | 0.90 | 0.96 | 0.00 |
| 60 kg | 1.00 | 0.12 | 0.93 | 0.97 | 0.00 | 1.00 | 0.15 | 0.91 | 0.98 | 0.00 |
| 80 kg | 1.00 | 0.13 | 0.92 | 0.99 | 0.00 | 1.00 | 0.14 | 0.93 | 0.99 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.96 | 0.99 | 0.03 | 0.98 | 1.19 | 0.03 |
| 40 kg | 0.97 | 0.91 | 0.03 | 0.98 | 0.92 | 0.02 |
| 60 kg | 0.99 | 0.77 | 0.02 | 0.98 | 0.82 | 0.03 |
| 80 kg | 0.98 | 0.39 | 0.02 | 0.98 | 0.46 | 0.02 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.73 | 0.74 | 0.32 |
| 40 kg | 0.78 | 0.82 | 0.33 |
| 60 kg | 0.87 | 0.84 | 0.30 |
| 80 kg | 0.86 | 0.86 | 0.24 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 2.38 | 0.62 | 21.32 | 5.85 | 4.58 | 0.62 | 7.31 | 0.00 | 0.21 |
| 40 kg | 1.76 | 0.69 | 20.01 | 4.98 | 4.29 | 2.34 | 6.42 | 0.00 | 0.12 |
| 60 kg | 0.38 | 0.78 | 20.70 | 4.46 | 2.95 | 3.56 | 4.56 | 0.00 | 0.10 |
| 80 kg | 1.02 | 0.76 | 20.29 | 3.15 | 2.58 | 6.53 | 1.58 | 0.00 | 0.11 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 97 | 230 | 175 |
| 40 kg | 131 | 286 | 235 |
| 60 kg | 156 | 317 | 269 |
| 80 kg | 177 | 334 | 304 |

## executor v2: holding and the team-ready barrier (time every robot of the push group is told to hold; the object's mean speed then and the share of it above 2 cm/s (gate: under 2 cm/s); each robot's contact force while told to hold; delay from team ready to both robots pressing (gate: under 0.2 s))

| mass | all holding (s) | object speed (m/s) | moving > 2 cm/s | force while holding (N) | ready to push (s) |
|---|---|---|---|---|---|
| 20 kg | 0.00 |  |  |  | 0.12 |
| 40 kg | 0.00 |  |  |  | 0.07 |
| 60 kg | 0.00 |  |  |  | 0.06 |
| 80 kg | 0.00 |  |  |  | 0.07 |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.18 | 0.16 | 0.47 | 0.78 |
| long | 0.28 | 0.24 | 0.50 | 0.65 |
| sphere | 0.38 | 0.61 | 0.83 | 0.90 |
| cylinder | 0.20 | 0.18 | 0.36 | 0.63 |
| arch | 0.27 | 0.29 | 0.34 | 0.50 |
| dumbbell | 0.14 | 0.22 | 0.37 | 0.69 |
| t_shape | 0.22 | 0.32 | 0.33 | 0.71 |
| beam | 0.15 | 0.32 | 0.68 | 0.75 |
| l_shape | 0.15 | 0.16 | 0.38 | 0.67 |
| asym | 0.23 | 0.30 | 0.50 | 0.65 |
| u_channel | 0.22 | 0.37 | 0.36 | 0.73 |
| plus | 0.11 | 0.11 | 0.07 | 0.21 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.78 | 0.61 | 0.50 | 0.50 |
| B_left | 0.53 | 0.44 | 0.36 | 0.14 |
| C_backright | 0.42 | 0.50 | 0.31 | 0.22 |
| D_far_turn | 0.44 | 0.39 | 0.25 | 0.11 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 18% | 0% | 82% | 38% | 5% | 57% |  |  | 7% | 53% | 51% | 14% |
| 40 kg | 11% | 0% | 89% | 46% | 3% | 51% |  |  | 5% | 50% | 51% | 14% |
| 60 kg | 8% | 0% | 92% | 53% | 3% | 45% |  |  | 5% | 64% | 38% | 18% |
| 80 kg | 6% | 0% | 94% | 57% | 3% | 41% |  |  | 6% | 68% | 34% | 16% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 131 | 0.89 | 7% | 18% | 32% | 51% |
| 40 kg | 160 | 0.89 | 8% | 22% | 42% | 37% |
| 60 kg | 181 | 0.89 | 8% | 27% | 45% | 28% |
| 80 kg | 199 | 0.90 | 6% | 32% | 45% | 23% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 62% | 0.19 | 0.41 | 0.14 | 0.72 | 14 | 0 | 14 | 0 | 0 | 0 | 70 | 4.35 | 0.00 |
| 40 kg | 55% | 0.14 | 0.55 | 0.11 | 0.76 | 10 | 0 | 10 | 0 | 0 | 0 | 66 | 3.13 | 0.00 |
| 60 kg | 52% | 0.10 | 0.70 | 0.09 | 0.81 | 8 | 0 | 7 | 0 | 0 | 1 | 106 | 3.42 | 0.00 |
| 80 kg | 47% | 0.07 | 0.79 | 0.07 | 0.94 | 8 | 1 | 7 | 0 | 0 | 0 | 118 | 3.59 | 0.00 |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.54 | 57% | 33% | 0.91 | 61% | 0.10 | 3 | 0 | 3 | 0 | 0 | 0 |
| long | 0.56 | 58% | 31% | 0.91 | 61% | 0.10 | 1 | 0 | 1 | 0 | 0 | 0 |
| sphere | 0.96 | 32% | 12% | 0.92 | 93% | 0.32 | 0 | 0 | 0 | 0 | 0 | 0 |
| cylinder | 0.29 | 37% | 16% | 0.90 | 57% | 0.09 | 11 | 0 | 11 | 0 | 0 | 0 |
| arch | 0.54 | 50% | 28% | 0.82 | 56% | 0.12 | 14 | 0 | 13 | 0 | 0 | 0 |
| dumbbell | 0.38 | 47% | 24% | 0.90 | 48% | 0.08 | 16 | 0 | 16 | 0 | 0 | 0 |
| t_shape | 0.35 | 53% | 28% | 0.92 | 51% | 0.09 | 12 | 0 | 11 | 0 | 0 | 0 |
| beam | 0.06 | 40% | 18% | 0.88 | 21% | 0.04 | 27 | 1 | 26 | 0 | 0 | 0 |
| l_shape | 0.35 | 49% | 22% | 0.89 | 48% | 0.06 | 9 | 0 | 8 | 0 | 0 | 1 |
| asym | 0.17 | 62% | 34% | 0.91 | 53% | 0.05 | 3 | 0 | 3 | 0 | 0 | 0 |
| u_channel | 0.35 | 43% | 18% | 0.91 | 46% | 0.10 | 17 | 1 | 16 | 0 | 0 | 0 |
| plus | 0.31 | 54% | 29% | 0.88 | 51% | 0.07 | 9 | 0 | 8 | 0 | 0 | 1 |
