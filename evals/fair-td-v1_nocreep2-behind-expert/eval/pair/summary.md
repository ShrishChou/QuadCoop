# Pair evaluation: fair-td-v1_nocreep2-behind-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto); WALKER OVERRIDE: anymal_c = /orcd/home/002/shrishc/quadcoop/logs/rsl_rl/walker_anymal_c/2026-11-09_00-10-27_v1_nocreep2/model_7997.pt (v1)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.65 | 0.60 | 0.11 | 0.06 | 26.4 | 0.01 | 0.48 | 0.35 | 0.16 | 0.27 | 1.15 |
| 40 kg | 0.60 | 0.53 | 0.10 | 0.06 | 27.8 | 0.00 | 0.52 | 0.40 | 0.17 | 0.26 | 1.13 |
| 60 kg | 0.49 | 0.40 | 0.15 | 0.10 | 36.1 | 0.01 | 0.62 | 0.40 | 0.25 | 0.35 | 1.11 |
| 80 kg | 0.33 | 0.26 | 0.14 | 0.12 | 37.6 | 0.01 | 0.73 | 0.51 | 0.37 | 0.44 | 1.06 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x+y + part 0 corner -x-y | 0.83 | 0.92 | 0.67 | 0.42 |
| long | part 0 -x seg 2/2 + part 0 corner -x-y | 0.67 | 0.83 | 0.58 | 0.42 |
| sphere | sector 135 + sector 225 | 0.83 | 0.75 | 0.75 | 0.75 |
| cylinder | part 0 corner -x-y + part 0 -x seg 2/2 | 0.33 | 0.25 | 0.00 | 0.17 |
| arch | part 3 -x + part 2 -x | 0.75 | 0.67 | 0.92 | 0.42 |
| dumbbell | part 0 -x + part 1 -x | 0.58 | 0.58 | 0.67 | 0.17 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.75 | 0.67 | 0.67 | 0.25 |
| beam (unseen) | part 0 -x seg 2/5 + part 0 -x seg 4/5 | 0.58 | 0.33 | 0.00 | 0.08 |
| l_shape (unseen) | part 1 -x + part 0 corner -x-y | 0.75 | 0.50 | 0.42 | 0.17 |
| asym (unseen) | part 1 -x + part 0 corner -x+y | 0.08 | 0.17 | 0.00 | 0.00 |
| u_channel (unseen) | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 1.00 | 1.00 | 0.75 | 0.50 |
| plus (unseen) | part 0 corner -x-y + part 0 corner -x+y | 0.67 | 0.50 | 0.50 | 0.58 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.65 | 0.17 | 0.17 | 0.01 | 0.00 | 0.03 | 9.83 |
| 40 kg | 0.60 | 0.23 | 0.16 | 0.01 | 0.00 | 0.01 | 8.64 |
| 60 kg | 0.49 | 0.23 | 0.26 | 0.02 | 0.00 | 0.00 | 9.26 |
| 80 kg | 0.33 | 0.41 | 0.26 | 0.01 | 0.00 | 0.00 | 7.79 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.30 | 0.65 | 0.87 | 0.00 | 1.00 | 0.32 | 0.62 | 0.84 | 0.00 |
| 40 kg | 1.00 | 0.27 | 0.68 | 0.89 | 0.00 | 1.00 | 0.27 | 0.69 | 0.88 | 0.00 |
| 60 kg | 1.00 | 0.29 | 0.68 | 0.92 | 0.00 | 1.00 | 0.30 | 0.63 | 0.89 | 0.00 |
| 80 kg | 1.00 | 0.25 | 0.70 | 0.95 | 0.00 | 1.00 | 0.30 | 0.62 | 0.91 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.78 | 1.81 | 0.09 | 0.74 | 1.79 | 0.09 |
| 40 kg | 0.78 | 1.81 | 0.11 | 0.75 | 1.96 | 0.12 |
| 60 kg | 0.81 | 2.08 | 0.12 | 0.77 | 2.37 | 0.15 |
| 80 kg | 0.79 | 2.08 | 0.14 | 0.77 | 2.40 | 0.19 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.53 | 0.43 | 0.29 |
| 40 kg | 0.56 | 0.51 | 0.28 |
| 60 kg | 0.58 | 0.44 | 0.26 |
| 80 kg | 0.63 | 0.45 | 0.25 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.56 | 0.37 | 26.31 | 9.83 | 0.52 | 0.65 | 6.04 | 0.00 | 0.32 |
| 40 kg | 0.43 | 0.41 | 25.48 | 8.64 | 0.64 | 0.46 | 5.12 | 0.00 | 0.28 |
| 60 kg | 0.56 | 0.37 | 24.29 | 9.26 | 0.58 | 0.87 | 2.22 | 0.00 | 0.34 |
| 80 kg | 0.56 | 0.41 | 24.21 | 7.79 | 0.46 | 3.93 | 0.95 | 0.00 | 0.34 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 125 | 281 | 208 |
| 40 kg | 162 | 332 | 270 |
| 60 kg | 186 | 355 | 306 |
| 80 kg | 210 | 366 | 343 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 1106 | 0.35 | 0.43 (255) | 0.51 (127) | 0.49 (222) | 0.52 (141) | 0.55 (361) |
| 40 kg | 1555 | 0.28 | 0.37 (354) | 0.51 (198) | 0.52 (317) | 0.54 (211) | 0.74 (475) |
| 60 kg | 1739 | 0.29 | 0.31 (278) | 0.43 (256) | 0.53 (345) | 0.55 (337) | 0.70 (522) |
| 80 kg | 2508 | 0.27 | 0.30 (78) | 0.41 (269) | 0.52 (1476) | 0.60 (396) | 0.75 (289) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.08 | 0.07 | 0.20 | 0.34 |
| long | 0.07 | 0.13 | 0.17 | 0.48 |
| sphere | 0.48 | 0.50 | 0.49 | 0.46 |
| cylinder | 0.21 | 0.23 | 0.29 | 0.45 |
| arch | 0.13 | 0.13 | 0.16 | 0.29 |
| dumbbell | 0.18 | 0.13 | 0.29 | 0.36 |
| t_shape | 0.08 | 0.10 | 0.20 | 0.45 |
| beam | 0.24 | 0.17 | 0.38 | 0.45 |
| l_shape | 0.07 | 0.09 | 0.12 | 0.27 |
| asym | 0.15 | 0.34 | 0.35 | 0.42 |
| u_channel | 0.09 | 0.12 | 0.25 | 0.31 |
| plus | 0.14 | 0.09 | 0.07 | 0.13 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.69 | 0.69 | 0.64 | 0.61 |
| B_left | 0.75 | 0.69 | 0.64 | 0.31 |
| C_backright | 0.58 | 0.42 | 0.25 | 0.17 |
| D_far_turn | 0.58 | 0.58 | 0.44 | 0.22 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 43% | 0% | 57% | 45% | 4% | 51% |  |  | 21% | 68% | 42% | 27% |
| 40 kg | 38% | 0% | 62% | 54% | 2% | 44% |  |  | 21% | 67% | 39% | 28% |
| 60 kg | 39% | 0% | 61% | 61% | 2% | 38% |  |  | 23% | 74% | 31% | 29% |
| 80 kg | 37% | 0% | 63% | 67% | 1% | 31% |  |  | 24% | 82% | 21% | 30% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 158 | 0.89 | 8% | 18% | 32% | 50% |
| 40 kg | 190 | 0.91 | 7% | 25% | 39% | 36% |
| 60 kg | 210 | 0.90 | 7% | 30% | 42% | 28% |
| 80 kg | 226 | 0.91 | 6% | 41% | 39% | 20% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 61% | 0.20 | 0.50 | 0.16 | 0.76 | 5 | 0 | 3 | 0 | 0 | 1 | 57 | 0.00 |  |
| 40 kg | 59% | 0.16 | 0.62 | 0.13 | 0.73 | 5 | 0 | 3 | 0 | 0 | 1 | 106 | 0.00 |  |
| 60 kg | 54% | 0.11 | 0.72 | 0.10 | 0.67 | 4 | 1 | 2 | 0 | 0 | 1 | 184 | 0.00 |  |
| 80 kg | 48% | 0.08 | 0.78 | 0.07 | 0.83 | 4 | 1 | 1 | 0 | 0 | 1 | 189 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.71 | 69% | 39% | 0.92 | 67% | 0.16 | 1 | 0 | 0 | 0 | 0 | 0 |
| long | 0.62 | 67% | 37% | 0.90 | 60% | 0.12 | 2 | 1 | 1 | 0 | 0 | 0 |
| sphere | 0.77 | 39% | 16% | 0.91 | 82% | 0.28 | 2 | 0 | 0 | 0 | 0 | 2 |
| cylinder | 0.19 | 42% | 19% | 0.90 | 59% | 0.09 | 5 | 0 | 4 | 0 | 0 | 0 |
| arch | 0.69 | 65% | 35% | 0.88 | 54% | 0.12 | 5 | 1 | 2 | 0 | 0 | 1 |
| dumbbell | 0.50 | 57% | 27% | 0.91 | 51% | 0.10 | 7 | 1 | 4 | 0 | 0 | 2 |
| t_shape | 0.58 | 67% | 32% | 0.91 | 53% | 0.08 | 4 | 0 | 2 | 0 | 0 | 2 |
| beam | 0.25 | 27% | 15% | 0.83 | 26% | 0.07 | 12 | 0 | 9 | 0 | 0 | 2 |
| l_shape | 0.46 | 68% | 32% | 0.91 | 53% | 0.09 | 5 | 1 | 2 | 0 | 0 | 2 |
| asym | 0.06 | 69% | 41% | 0.92 | 51% | 0.06 | 3 | 0 | 1 | 0 | 0 | 1 |
| u_channel | 0.81 | 55% | 22% | 0.93 | 50% | 0.11 | 5 | 1 | 2 | 0 | 0 | 2 |
| plus | 0.56 | 53% | 22% | 0.91 | 60% | 0.12 | 3 | 0 | 3 | 0 | 0 | 1 |
