# Pair evaluation: fair-td-v22-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto); WALKER OVERRIDE: anymal_c = /orcd/home/002/shrishc/quadcoop/logs/rsl_rl/walker_anymal_c_compliant/2026-11-08_11-35-10_v22/model_8997.pt (compliant)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.66 | 0.63 | 0.02 | 0.02 | 36.0 | 0.03 | 0.42 | 0.33 | 0.11 | 0.20 | 1.13 |
| 40 kg | 0.54 | 0.49 | 0.08 | 0.04 | 38.7 | 0.03 | 0.54 | 0.39 | 0.17 | 0.25 | 1.13 |
| 60 kg | 0.35 | 0.26 | 0.07 | 0.01 | 40.5 | 0.03 | 0.63 | 0.52 | 0.33 | 0.43 | 1.10 |
| 80 kg | 0.23 | 0.19 | 0.02 | 0.06 | 41.0 | 0.04 | 0.71 | 0.61 | 0.46 | 0.56 | 1.11 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x+y + part 0 corner -x-y | 0.92 | 0.58 | 0.17 | 0.00 |
| long | part 0 -x seg 2/2 + part 0 corner -x-y | 0.67 | 0.50 | 0.50 | 0.08 |
| sphere | sector 135 + sector 225 | 1.00 | 0.92 | 0.92 | 1.00 |
| cylinder | part 0 corner -x-y + part 0 -x seg 2/2 | 0.75 | 0.83 | 0.33 | 0.17 |
| arch | part 3 -x + part 2 -x | 0.92 | 0.83 | 0.83 | 0.42 |
| dumbbell | part 0 -x + part 1 -x | 0.50 | 0.42 | 0.33 | 0.25 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.75 | 0.33 | 0.25 | 0.33 |
| beam (unseen) | part 0 -x seg 2/5 + part 0 -x seg 4/5 | 0.50 | 0.17 | 0.00 | 0.00 |
| l_shape (unseen) | part 1 -x + part 0 corner -x-y | 0.58 | 0.67 | 0.25 | 0.08 |
| asym (unseen) | part 1 -x + part 0 corner -x+y | 0.33 | 0.17 | 0.00 | 0.00 |
| u_channel (unseen) | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.58 | 0.75 | 0.33 | 0.25 |
| plus (unseen) | part 0 corner -x-y + part 0 corner -x+y | 0.42 | 0.33 | 0.25 | 0.17 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.66 | 0.30 | 0.04 | 0.00 | 0.00 | 0.03 | 10.53 |
| 40 kg | 0.54 | 0.34 | 0.12 | 0.00 | 0.00 | 0.02 | 8.35 |
| 60 kg | 0.35 | 0.57 | 0.08 | 0.00 | 0.00 | 0.03 | 8.19 |
| 80 kg | 0.23 | 0.69 | 0.08 | 0.00 | 0.00 | 0.01 | 7.45 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.27 | 0.67 | 0.89 | 0.00 | 1.00 | 0.30 | 0.65 | 0.86 | 0.00 |
| 40 kg | 1.00 | 0.24 | 0.72 | 0.91 | 0.00 | 1.00 | 0.24 | 0.74 | 0.91 | 0.00 |
| 60 kg | 1.00 | 0.21 | 0.75 | 0.94 | 0.00 | 1.00 | 0.25 | 0.74 | 0.92 | 0.00 |
| 80 kg | 1.00 | 0.20 | 0.75 | 0.95 | 0.00 | 1.00 | 0.23 | 0.77 | 0.93 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.83 | 2.25 | 0.07 | 0.80 | 2.22 | 0.09 |
| 40 kg | 0.82 | 2.73 | 0.09 | 0.78 | 1.98 | 0.09 |
| 60 kg | 0.81 | 2.51 | 0.09 | 0.78 | 2.02 | 0.09 |
| 80 kg | 0.77 | 1.90 | 0.10 | 0.77 | 2.03 | 0.10 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.54 | 0.49 | 0.31 |
| 40 kg | 0.57 | 0.57 | 0.29 |
| 60 kg | 0.64 | 0.57 | 0.26 |
| 80 kg | 0.65 | 0.58 | 0.24 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.34 | 0.41 | 34.58 | 10.53 | 0.22 | 0.00 | 4.81 | 0.00 | 0.32 |
| 40 kg | 1.25 | 0.45 | 30.34 | 8.35 | 0.31 | 0.24 | 3.51 | 0.00 | 0.27 |
| 60 kg | 0.32 | 0.48 | 30.35 | 8.19 | 0.82 | 1.45 | 1.15 | 0.00 | 0.26 |
| 80 kg | 0.22 | 0.49 | 30.43 | 7.45 | 0.62 | 2.40 | 0.35 | 0.00 | 0.28 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 120 | 301 | 227 |
| 40 kg | 151 | 346 | 263 |
| 60 kg | 168 | 377 | 305 |
| 80 kg | 188 | 409 | 342 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 1407 | 0.38 | 0.45 (307) | 0.50 (211) | 0.50 (329) | 0.50 (255) | 0.58 (305) |
| 40 kg | 1786 | 0.37 | 0.35 (477) | 0.49 (177) | 0.49 (322) | 0.51 (231) | 0.62 (579) |
| 60 kg | 2478 | 0.38 | 0.38 (578) | 0.46 (665) | 0.47 (484) | 0.51 (347) | 0.62 (404) |
| 80 kg | 2934 | 0.40 | 0.40 (109) | 0.47 (762) | 0.47 (1717) | 0.47 (224) | 0.75 (121) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.10 | 0.13 | 0.24 | 0.31 |
| long | 0.09 | 0.21 | 0.41 | 0.70 |
| sphere | 0.12 | 0.16 | 0.30 | 0.44 |
| cylinder | 0.11 | 0.11 | 0.18 | 0.38 |
| arch | 0.09 | 0.14 | 0.33 | 0.34 |
| dumbbell | 0.16 | 0.17 | 0.45 | 0.61 |
| t_shape | 0.16 | 0.19 | 0.37 | 0.66 |
| beam | 0.16 | 0.48 | 0.58 | 0.60 |
| l_shape | 0.10 | 0.11 | 0.22 | 0.33 |
| asym | 0.08 | 0.20 | 0.34 | 0.59 |
| u_channel | 0.08 | 0.16 | 0.45 | 0.45 |
| plus | 0.04 | 0.04 | 0.04 | 0.08 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.67 | 0.67 | 0.58 | 0.50 |
| B_left | 0.64 | 0.67 | 0.36 | 0.19 |
| C_backright | 0.64 | 0.39 | 0.22 | 0.14 |
| D_far_turn | 0.69 | 0.44 | 0.22 | 0.08 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 39% | 0% | 61% | 35% | 3% | 61% |  |  | 18% | 68% | 40% | 23% |
| 40 kg | 32% | 0% | 68% | 40% | 3% | 57% |  |  | 16% | 69% | 35% | 23% |
| 60 kg | 29% | 0% | 71% | 41% | 3% | 55% |  |  | 16% | 75% | 26% | 24% |
| 80 kg | 29% | 0% | 71% | 43% | 3% | 54% |  |  | 19% | 70% | 32% | 28% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 163 | 0.88 | 10% | 12% | 34% | 54% |
| 40 kg | 189 | 0.88 | 10% | 15% | 41% | 44% |
| 60 kg | 206 | 0.87 | 11% | 16% | 45% | 39% |
| 80 kg | 225 | 0.87 | 11% | 17% | 46% | 37% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 65% | 0.18 | 0.29 | 0.10 | 0.30 | 1 | 0 | 1 | 0 | 0 | 1 | 43 | 0.00 |  |
| 40 kg | 60% | 0.13 | 0.49 | 0.09 | 0.20 | 1 | 0 | 1 | 0 | 0 | 0 | 74 | 0.00 |  |
| 60 kg | 52% | 0.08 | 0.64 | 0.06 | 0.20 | 1 | 0 | 0 | 0 | 0 | 0 | 77 | 0.00 |  |
| 80 kg | 44% | 0.06 | 0.73 | 0.05 | 0.46 | 2 | 1 | 1 | 0 | 0 | 1 | 79 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.42 | 45% | 17% | 0.90 | 58% | 0.08 | 0 | 0 | 0 | 0 | 0 | 0 |
| long | 0.44 | 45% | 17% | 0.88 | 61% | 0.08 | 0 | 0 | 0 | 0 | 0 | 0 |
| sphere | 0.96 | 19% | 5% | 0.93 | 84% | 0.16 | 0 | 0 | 0 | 0 | 0 | 0 |
| cylinder | 0.52 | 28% | 7% | 0.89 | 68% | 0.08 | 0 | 0 | 0 | 0 | 0 | 0 |
| arch | 0.75 | 38% | 12% | 0.88 | 57% | 0.10 | 2 | 0 | 1 | 0 | 0 | 1 |
| dumbbell | 0.38 | 45% | 18% | 0.88 | 53% | 0.07 | 2 | 0 | 0 | 0 | 0 | 1 |
| t_shape | 0.42 | 46% | 18% | 0.90 | 55% | 0.06 | 1 | 0 | 0 | 0 | 0 | 0 |
| beam | 0.17 | 41% | 19% | 0.69 | 23% | 0.03 | 8 | 2 | 5 | 0 | 0 | 1 |
| l_shape | 0.40 | 43% | 15% | 0.89 | 53% | 0.08 | 0 | 0 | 0 | 0 | 0 | 0 |
| asym | 0.12 | 49% | 22% | 0.86 | 46% | 0.04 | 0 | 0 | 0 | 0 | 0 | 0 |
| u_channel | 0.48 | 42% | 14% | 0.90 | 50% | 0.07 | 1 | 0 | 0 | 0 | 0 | 1 |
| plus | 0.29 | 38% | 18% | 0.89 | 52% | 0.06 | 0 | 0 | 0 | 0 | 0 | 0 |
