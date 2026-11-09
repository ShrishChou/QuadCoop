# Pair evaluation: zs-nc2-proj-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto); WALKER OVERRIDE: anymal_c = /orcd/home/002/shrishc/quadcoop/logs/rsl_rl/walker_anymal_c/2026-11-09_00-10-27_v1_nocreep2/model_7997.pt (v1)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 1 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.75 | 0.75 | 0.02 | 0.04 | 30.7 | 0.01 | 0.45 | 0.40 | 0.14 | 0.24 | 1.12 |
| 40 kg | 0.73 | 0.56 | 0.02 | 0.02 | 31.0 | 0.00 | 0.56 | 0.38 | 0.17 | 0.25 | 1.08 |
| 60 kg | 0.46 | 0.31 | 0.04 | 0.02 | 36.1 | 0.00 | 0.67 | 0.39 | 0.25 | 0.33 | 1.11 |
| 80 kg | 0.29 | 0.27 | 0.04 | 0.04 | 42.9 | 0.01 | 0.76 | 0.48 | 0.37 | 0.45 | 1.06 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x+y + part 0 corner -x-y | 0.75 | 0.75 | 0.50 | 0.25 |
| long | part 0 -x seg 2/2 + part 0 corner -x-y | 0.75 | 0.75 | 0.75 | 0.25 |
| sphere | sector 225 + sector 135 | 1.00 | 1.00 | 0.75 | 1.00 |
| cylinder | part 0 -x seg 2/2 + part 0 corner -x-y | 0.50 | 0.75 | 0.25 | 0.25 |
| arch | part 2 -x + part 3 -x | 1.00 | 1.00 | 0.25 | 0.25 |
| dumbbell | part 0 -x + part 1 -x | 0.75 | 0.75 | 0.50 | 0.25 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.50 | 0.75 | 0.50 | 0.00 |
| beam (unseen) | part 0 -x seg 2/5 + part 0 -x seg 4/5 | 0.75 | 0.25 | 0.00 | 0.00 |
| l_shape (unseen) | part 0 corner -x-y + part 1 -x | 0.75 | 0.75 | 0.75 | 0.25 |
| asym (unseen) | part 0 corner -x+y + part 1 -x | 0.75 | 0.00 | 0.00 | 0.00 |
| u_channel (unseen) | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.50 | 1.00 | 0.50 | 0.75 |
| plus (unseen) | part 1 corner -x+y + part 1 corner -x-y | 1.00 | 1.00 | 0.75 | 0.25 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.75 | 0.19 | 0.06 | 0.00 | 0.00 | 0.02 | 9.00 |
| 40 kg | 0.73 | 0.21 | 0.04 | 0.02 | 0.00 | 0.00 | 9.77 |
| 60 kg | 0.46 | 0.46 | 0.06 | 0.02 | 0.00 | 0.00 | 9.19 |
| 80 kg | 0.29 | 0.62 | 0.08 | 0.00 | 0.00 | 0.00 | 6.98 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.25 | 0.71 | 0.87 | 0.00 | 1.00 | 0.27 | 0.65 | 0.84 | 0.00 |
| 40 kg | 1.00 | 0.21 | 0.75 | 0.90 | 0.00 | 1.00 | 0.26 | 0.64 | 0.88 | 0.00 |
| 60 kg | 1.00 | 0.19 | 0.76 | 0.95 | 0.00 | 1.00 | 0.25 | 0.64 | 0.93 | 0.00 |
| 80 kg | 1.00 | 0.20 | 0.75 | 0.96 | 0.00 | 1.00 | 0.27 | 0.62 | 0.94 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.78 | 2.19 | 0.08 | 0.71 | 2.37 | 0.10 |
| 40 kg | 0.81 | 2.10 | 0.09 | 0.73 | 2.27 | 0.16 |
| 60 kg | 0.79 | 1.96 | 0.14 | 0.74 | 2.38 | 0.21 |
| 80 kg | 0.82 | 2.70 | 0.15 | 0.74 | 2.25 | 0.23 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.53 | 0.49 | 0.28 |
| 40 kg | 0.60 | 0.48 | 0.27 |
| 60 kg | 0.66 | 0.45 | 0.26 |
| 80 kg | 0.64 | 0.42 | 0.24 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.50 | 0.38 | 28.33 | 9.00 | 0.17 | 0.00 | 6.50 | 0.00 | 0.35 |
| 40 kg | 0.25 | 0.40 | 26.17 | 9.77 | 0.33 | 1.15 | 4.85 | 0.00 | 0.36 |
| 60 kg | 0.17 | 0.41 | 27.43 | 9.19 | 0.75 | 1.67 | 2.71 | 0.00 | 0.34 |
| 80 kg | 0.32 | 0.37 | 28.21 | 6.98 | 0.38 | 5.75 | 0.88 | 0.00 | 0.34 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 119 | 271 | 214 |
| 40 kg | 153 | 316 | 266 |
| 60 kg | 187 | 337 | 307 |
| 80 kg | 205 | 351 | 316 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 471 | 0.32 | 0.40 (94) | 0.55 (91) | 0.53 (101) | 0.50 (95) | 0.56 (91) |
| 40 kg | 571 | 0.29 | 0.34 (191) | 0.42 (34) | 0.55 (67) | 0.53 (95) | 0.74 (184) |
| 60 kg | 776 | 0.28 | 0.28 (120) | 0.47 (128) | 0.38 (138) | 0.62 (170) | 0.74 (219) |
| 80 kg | 980 | 0.25 | 0.12 (56) | 0.40 (109) | 0.53 (466) | 0.58 (271) | 0.76 (78) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.09 | 0.08 | 0.17 | 0.45 |
| long | 0.07 | 0.15 | 0.35 | 0.22 |
| sphere | 0.42 | 0.29 | 0.35 | 0.36 |
| cylinder | 0.13 | 0.13 | 0.35 | 0.34 |
| arch | 0.17 | 0.18 | 0.19 | 0.20 |
| dumbbell | 0.09 | 0.22 | 0.26 | 0.31 |
| t_shape | 0.05 | 0.24 | 0.21 | 0.48 |
| beam | 0.18 | 0.15 | 0.23 | 0.73 |
| l_shape | 0.13 | 0.12 | 0.12 | 0.33 |
| asym | 0.29 | 0.26 | 0.23 | 0.34 |
| u_channel | 0.05 | 0.08 | 0.20 | 0.34 |
| plus | 0.03 | 0.11 | 0.29 | 0.34 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.67 | 0.83 | 0.83 | 0.50 |
| B_left | 0.67 | 0.58 | 0.58 | 0.17 |
| C_backright | 1.00 | 0.67 | 0.25 | 0.42 |
| D_far_turn | 0.67 | 0.83 | 0.17 | 0.08 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 42% | 0% | 58% | 45% | 4% | 51% |  |  | 20% | 56% | 51% | 28% |
| 40 kg | 39% | 0% | 61% | 52% | 2% | 45% |  |  | 22% | 64% | 42% | 26% |
| 60 kg | 35% | 0% | 65% | 64% | 2% | 34% |  |  | 23% | 72% | 32% | 33% |
| 80 kg | 36% | 0% | 64% | 71% | 1% | 27% |  |  | 25% | 83% | 20% | 37% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 152 | 0.90 | 7% | 18% | 34% | 48% |
| 40 kg | 180 | 0.91 | 6% | 24% | 42% | 34% |
| 60 kg | 204 | 0.91 | 5% | 39% | 41% | 20% |
| 80 kg | 217 | 0.91 | 6% | 48% | 37% | 15% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 64% | 0.18 | 0.48 | 0.14 | 0.69 | 3 | 0 | 2 | 0 | 0 | 1 | 76 | 0.00 |  |
| 40 kg | 58% | 0.15 | 0.64 | 0.12 | 0.77 | 4 | 0 | 3 | 0 | 0 | 1 | 121 | 0.00 |  |
| 60 kg | 55% | 0.10 | 0.74 | 0.09 | 0.81 | 4 | 2 | 1 | 0 | 0 | 1 | 195 | 0.00 |  |
| 80 kg | 43% | 0.06 | 0.80 | 0.05 | 0.96 | 4 | 2 | 1 | 0 | 0 | 1 | 171 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.56 | 70% | 37% | 0.93 | 62% | 0.14 | 2 | 2 | 0 | 0 | 0 | 0 |
| long | 0.62 | 70% | 42% | 0.91 | 60% | 0.09 | 2 | 1 | 1 | 0 | 0 | 1 |
| sphere | 0.94 | 38% | 16% | 0.93 | 84% | 0.24 | 0 | 0 | 0 | 0 | 0 | 0 |
| cylinder | 0.44 | 37% | 16% | 0.88 | 64% | 0.08 | 3 | 0 | 2 | 0 | 0 | 1 |
| arch | 0.62 | 59% | 33% | 0.89 | 55% | 0.13 | 3 | 0 | 2 | 0 | 0 | 1 |
| dumbbell | 0.56 | 56% | 29% | 0.90 | 54% | 0.09 | 5 | 1 | 1 | 0 | 0 | 2 |
| t_shape | 0.44 | 67% | 36% | 0.92 | 53% | 0.08 | 4 | 0 | 3 | 0 | 0 | 1 |
| beam | 0.25 | 34% | 21% | 0.80 | 23% | 0.07 | 14 | 2 | 9 | 0 | 0 | 3 |
| l_shape | 0.62 | 67% | 37% | 0.92 | 53% | 0.07 | 2 | 1 | 0 | 0 | 0 | 1 |
| asym | 0.19 | 72% | 48% | 0.93 | 45% | 0.05 | 4 | 3 | 1 | 0 | 0 | 1 |
| u_channel | 0.69 | 60% | 30% | 0.93 | 52% | 0.08 | 5 | 1 | 2 | 0 | 0 | 1 |
| plus | 0.75 | 69% | 42% | 0.93 | 59% | 0.07 | 0 | 0 | 0 | 0 | 0 | 0 |
