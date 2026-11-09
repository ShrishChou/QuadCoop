# Pair evaluation: fair-td-v1nc6998-behind-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto); WALKER OVERRIDE: anymal_c = /orcd/home/002/shrishc/quadcoop/logs/rsl_rl/walker_anymal_c/2026-11-08_19-58-50_v1_nocreep/model_6998.pt (v1)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.69 | 0.71 | 0.07 | 0.05 | 27.4 | 0.01 | 0.46 | 0.37 | 0.14 | 0.24 | 1.13 |
| 40 kg | 0.61 | 0.49 | 0.11 | 0.03 | 29.3 | 0.01 | 0.54 | 0.39 | 0.17 | 0.24 | 1.11 |
| 60 kg | 0.51 | 0.41 | 0.11 | 0.08 | 38.3 | 0.01 | 0.63 | 0.41 | 0.24 | 0.33 | 1.09 |
| 80 kg | 0.26 | 0.24 | 0.13 | 0.19 | 40.5 | 0.01 | 0.71 | 0.50 | 0.36 | 0.45 | 1.05 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x+y + part 0 corner -x-y | 0.67 | 0.75 | 0.67 | 0.33 |
| long | part 0 -x seg 2/2 + part 0 corner -x-y | 0.67 | 0.75 | 0.75 | 0.42 |
| sphere | sector 135 + sector 225 | 0.92 | 0.75 | 0.50 | 0.50 |
| cylinder | part 0 corner -x-y + part 0 -x seg 2/2 | 0.50 | 0.33 | 0.25 | 0.08 |
| arch | part 3 -x + part 2 -x | 0.83 | 0.83 | 0.92 | 0.50 |
| dumbbell | part 0 -x + part 1 -x | 0.67 | 0.58 | 0.75 | 0.25 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.83 | 0.67 | 0.67 | 0.17 |
| beam (unseen) | part 0 -x seg 2/5 + part 0 -x seg 4/5 | 0.67 | 0.33 | 0.17 | 0.00 |
| l_shape (unseen) | part 1 -x + part 0 corner -x-y | 0.75 | 0.67 | 0.42 | 0.08 |
| asym (unseen) | part 1 -x + part 0 corner -x+y | 0.42 | 0.17 | 0.00 | 0.00 |
| u_channel (unseen) | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.75 | 0.75 | 0.67 | 0.42 |
| plus (unseen) | part 0 corner -x-y + part 0 corner -x+y | 0.67 | 0.75 | 0.42 | 0.33 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.69 | 0.19 | 0.12 | 0.00 | 0.00 | 0.01 | 10.12 |
| 40 kg | 0.61 | 0.25 | 0.14 | 0.00 | 0.00 | 0.00 | 8.34 |
| 60 kg | 0.51 | 0.30 | 0.19 | 0.00 | 0.00 | 0.00 | 8.60 |
| 80 kg | 0.26 | 0.42 | 0.32 | 0.00 | 0.00 | 0.00 | 7.02 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.29 | 0.64 | 0.86 | 0.00 | 1.00 | 0.30 | 0.65 | 0.83 | 0.00 |
| 40 kg | 1.00 | 0.26 | 0.71 | 0.90 | 0.00 | 1.00 | 0.27 | 0.67 | 0.88 | 0.00 |
| 60 kg | 1.00 | 0.27 | 0.71 | 0.93 | 0.00 | 1.00 | 0.26 | 0.68 | 0.92 | 0.00 |
| 80 kg | 1.00 | 0.25 | 0.70 | 0.95 | 0.00 | 1.00 | 0.29 | 0.62 | 0.92 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.79 | 2.09 | 0.08 | 0.75 | 2.01 | 0.08 |
| 40 kg | 0.80 | 2.05 | 0.09 | 0.74 | 2.15 | 0.12 |
| 60 kg | 0.79 | 2.30 | 0.12 | 0.78 | 2.71 | 0.15 |
| 80 kg | 0.79 | 2.31 | 0.14 | 0.77 | 2.97 | 0.20 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.52 | 0.50 | 0.29 |
| 40 kg | 0.57 | 0.52 | 0.28 |
| 60 kg | 0.59 | 0.50 | 0.27 |
| 80 kg | 0.63 | 0.45 | 0.24 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.69 | 0.41 | 27.35 | 10.12 | 0.14 | 0.15 | 7.65 | 0.00 | 0.33 |
| 40 kg | 0.37 | 0.43 | 26.52 | 8.34 | 0.46 | 1.02 | 6.28 | 0.00 | 0.29 |
| 60 kg | 0.67 | 0.40 | 27.57 | 8.60 | 0.50 | 1.83 | 2.74 | 0.00 | 0.32 |
| 80 kg | 0.18 | 0.42 | 24.42 | 7.02 | 0.61 | 4.92 | 0.68 | 0.00 | 0.35 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 124 | 283 | 212 |
| 40 kg | 161 | 327 | 265 |
| 60 kg | 186 | 341 | 290 |
| 80 kg | 205 | 353 | 319 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 1447 | 0.27 | 0.43 (178) | 0.51 (146) | 0.51 (490) | 0.52 (280) | 0.57 (355) |
| 40 kg | 1837 | 0.31 | 0.39 (389) | 0.47 (154) | 0.50 (361) | 0.49 (264) | 0.68 (669) |
| 60 kg | 2093 | 0.27 | 0.30 (280) | 0.41 (245) | 0.46 (326) | 0.62 (420) | 0.74 (822) |
| 80 kg | 2624 | 0.23 | 0.19 (61) | 0.45 (223) | 0.50 (1473) | 0.60 (481) | 0.81 (386) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.10 | 0.09 | 0.22 | 0.35 |
| long | 0.06 | 0.14 | 0.21 | 0.51 |
| sphere | 0.54 | 0.53 | 0.48 | 0.40 |
| cylinder | 0.13 | 0.22 | 0.24 | 0.25 |
| arch | 0.18 | 0.20 | 0.29 | 0.34 |
| dumbbell | 0.17 | 0.18 | 0.20 | 0.42 |
| t_shape | 0.06 | 0.08 | 0.20 | 0.42 |
| beam | 0.13 | 0.14 | 0.29 | 0.48 |
| l_shape | 0.06 | 0.11 | 0.16 | 0.29 |
| asym | 0.15 | 0.10 | 0.33 | 0.56 |
| u_channel | 0.05 | 0.11 | 0.20 | 0.22 |
| plus | 0.10 | 0.08 | 0.10 | 0.11 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.89 | 0.78 | 0.69 | 0.47 |
| B_left | 0.69 | 0.61 | 0.53 | 0.25 |
| C_backright | 0.58 | 0.58 | 0.39 | 0.14 |
| D_far_turn | 0.61 | 0.47 | 0.44 | 0.17 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 42% | 0% | 58% | 44% | 3% | 52% |  |  | 17% | 65% | 44% | 24% |
| 40 kg | 37% | 0% | 63% | 55% | 2% | 43% |  |  | 18% | 64% | 40% | 25% |
| 60 kg | 35% | 0% | 65% | 61% | 2% | 37% |  |  | 21% | 74% | 30% | 28% |
| 80 kg | 37% | 0% | 63% | 70% | 1% | 29% |  |  | 24% | 86% | 17% | 31% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 159 | 0.89 | 8% | 18% | 31% | 51% |
| 40 kg | 188 | 0.91 | 6% | 25% | 40% | 35% |
| 60 kg | 207 | 0.91 | 6% | 32% | 44% | 25% |
| 80 kg | 223 | 0.90 | 6% | 44% | 37% | 19% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 60% | 0.21 | 0.47 | 0.16 | 0.64 | 4 | 0 | 2 | 0 | 0 | 1 | 99 | 0.00 |  |
| 40 kg | 56% | 0.17 | 0.62 | 0.14 | 0.85 | 5 | 1 | 3 | 0 | 0 | 1 | 169 | 0.00 |  |
| 60 kg | 52% | 0.12 | 0.72 | 0.11 | 0.99 | 6 | 2 | 3 | 0 | 0 | 2 | 166 | 0.00 |  |
| 80 kg | 44% | 0.08 | 0.78 | 0.07 | 1.28 | 7 | 3 | 2 | 0 | 0 | 2 | 181 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.60 | 72% | 43% | 0.92 | 58% | 0.14 | 3 | 2 | 0 | 0 | 0 | 0 |
| long | 0.65 | 69% | 38% | 0.91 | 57% | 0.11 | 2 | 1 | 1 | 0 | 0 | 0 |
| sphere | 0.67 | 39% | 13% | 0.91 | 79% | 0.32 | 4 | 0 | 0 | 0 | 0 | 4 |
| cylinder | 0.29 | 41% | 16% | 0.90 | 63% | 0.13 | 3 | 0 | 3 | 0 | 0 | 0 |
| arch | 0.77 | 66% | 38% | 0.88 | 65% | 0.17 | 2 | 0 | 0 | 0 | 0 | 1 |
| dumbbell | 0.56 | 51% | 25% | 0.92 | 44% | 0.10 | 10 | 2 | 6 | 0 | 0 | 2 |
| t_shape | 0.58 | 67% | 35% | 0.91 | 49% | 0.08 | 7 | 3 | 2 | 0 | 0 | 2 |
| beam | 0.29 | 30% | 19% | 0.83 | 28% | 0.08 | 14 | 1 | 10 | 0 | 0 | 3 |
| l_shape | 0.48 | 67% | 35% | 0.92 | 46% | 0.08 | 5 | 3 | 2 | 0 | 0 | 1 |
| asym | 0.15 | 73% | 46% | 0.92 | 45% | 0.06 | 8 | 5 | 3 | 0 | 0 | 0 |
| u_channel | 0.65 | 54% | 18% | 0.92 | 47% | 0.10 | 5 | 1 | 2 | 0 | 0 | 2 |
| plus | 0.54 | 62% | 28% | 0.91 | 56% | 0.10 | 3 | 1 | 2 | 0 | 0 | 1 |
