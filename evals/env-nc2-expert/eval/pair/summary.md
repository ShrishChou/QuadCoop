# Pair evaluation: env-nc2-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto); WALKER OVERRIDE: anymal_c = /orcd/home/002/shrishc/quadcoop/logs/rsl_rl/walker_anymal_c/2026-11-09_00-10-27_v1_nocreep2/model_7997.pt (v1)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 1 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.65 | 0.65 | 0.06 | 0.12 | 28.4 | 0.00 | 0.49 | 0.37 | 0.16 | 0.26 | 1.12 |
| 40 kg | 0.69 | 0.62 | 0.12 | 0.04 | 25.9 | 0.00 | 0.56 | 0.37 | 0.18 | 0.27 | 1.22 |
| 60 kg | 0.50 | 0.35 | 0.08 | 0.08 | 30.8 | 0.00 | 0.69 | 0.37 | 0.23 | 0.30 | 1.07 |
| 80 kg | 0.33 | 0.31 | 0.27 | 0.06 | 30.3 | 0.01 | 0.73 | 0.54 | 0.42 | 0.52 | 1.09 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x+y + part 0 corner -x-y | 0.75 | 0.75 | 0.75 | 0.50 |
| long | part 0 -x seg 2/2 + part 0 corner -x-y | 0.50 | 0.75 | 0.50 | 0.25 |
| sphere | sector 225 + sector 135 | 0.75 | 0.75 | 1.00 | 1.00 |
| cylinder | part 0 -x seg 2/2 + part 0 corner -x-y | 0.75 | 0.50 | 0.25 | 0.25 |
| arch | part 2 -x + part 3 -x | 1.00 | 1.00 | 0.50 | 0.50 |
| dumbbell | part 0 -x + part 1 -x | 0.50 | 0.75 | 0.75 | 0.50 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.75 | 1.00 | 0.50 | 0.00 |
| beam (unseen) | part 0 -x seg 2/5 + part 0 -x seg 4/5 | 0.50 | 0.25 | 0.00 | 0.00 |
| l_shape (unseen) | part 0 corner -x-y + part 1 -x | 0.75 | 0.75 | 1.00 | 0.25 |
| asym (unseen) | part 0 corner -x+y + part 1 -x | 0.50 | 0.00 | 0.00 | 0.00 |
| u_channel (unseen) | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.50 | 1.00 | 0.50 | 0.75 |
| plus (unseen) | part 1 corner -x+y + part 1 corner -x-y | 0.50 | 0.75 | 0.25 | 0.00 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.65 | 0.15 | 0.19 | 0.02 | 0.00 | 0.02 | 10.56 |
| 40 kg | 0.69 | 0.12 | 0.17 | 0.02 | 0.00 | 0.00 | 8.71 |
| 60 kg | 0.50 | 0.29 | 0.17 | 0.04 | 0.00 | 0.00 | 10.46 |
| 80 kg | 0.33 | 0.33 | 0.33 | 0.00 | 0.00 | 0.00 | 8.83 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.29 | 0.65 | 0.86 | 0.00 | 1.00 | 0.29 | 0.66 | 0.85 | 0.00 |
| 40 kg | 1.00 | 0.25 | 0.71 | 0.91 | 0.00 | 1.00 | 0.28 | 0.66 | 0.88 | 0.00 |
| 60 kg | 1.00 | 0.22 | 0.73 | 0.95 | 0.00 | 1.00 | 0.26 | 0.64 | 0.94 | 0.00 |
| 80 kg | 1.00 | 0.24 | 0.68 | 0.96 | 0.00 | 1.00 | 0.28 | 0.63 | 0.94 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.77 | 1.66 | 0.08 | 0.74 | 1.64 | 0.10 |
| 40 kg | 0.77 | 1.76 | 0.10 | 0.70 | 1.86 | 0.13 |
| 60 kg | 0.78 | 1.45 | 0.12 | 0.72 | 2.22 | 0.17 |
| 80 kg | 0.79 | 2.06 | 0.18 | 0.76 | 2.46 | 0.19 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.50 | 0.49 | 0.28 |
| 40 kg | 0.58 | 0.47 | 0.27 |
| 60 kg | 0.63 | 0.45 | 0.26 |
| 80 kg | 0.61 | 0.46 | 0.23 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.72 | 0.35 | 27.94 | 10.56 | 0.17 | 0.08 | 5.65 | 0.00 | 0.36 |
| 40 kg | 0.14 | 0.41 | 22.21 | 8.71 | 0.33 | 1.75 | 4.35 | 0.00 | 0.30 |
| 60 kg | 0.17 | 0.40 | 25.98 | 10.46 | 1.67 | 2.02 | 1.81 | 0.00 | 0.29 |
| 80 kg | 0.36 | 0.41 | 21.63 | 8.83 | 0.40 | 3.42 | 1.21 | 0.00 | 0.31 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 131 | 293 | 242 |
| 40 kg | 157 | 330 | 267 |
| 60 kg | 195 | 361 | 307 |
| 80 kg | 202 | 365 | 367 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 403 | 0.32 | 0.43 (110) | 0.48 (72) | 0.51 (68) | 0.53 (64) | 0.58 (89) |
| 40 kg | 388 | 0.24 | 0.21 (138) | 0.32 (32) | 0.54 (49) | 0.59 (31) | 0.74 (138) |
| 60 kg | 683 | 0.26 | 0.38 (27) | 0.39 (104) | 0.45 (105) | 0.53 (175) | 0.79 (272) |
| 80 kg | 746 | 0.25 | 0.20 (9) | 0.52 (42) | 0.53 (459) | 0.60 (162) | 0.73 (73) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.06 | 0.05 | 0.15 | 0.36 |
| long | 0.21 | 0.09 | 0.12 | 0.34 |
| sphere | 0.50 | 0.43 | 0.42 | 0.55 |
| cylinder | 0.10 | 0.43 | 0.27 | 0.46 |
| arch | 0.22 | 0.23 | 0.22 | 0.22 |
| dumbbell | 0.11 | 0.11 | 0.23 | 0.54 |
| t_shape | 0.03 | 0.14 | 0.12 | 0.50 |
| beam | 0.12 | 0.19 | 0.31 | 0.61 |
| l_shape | 0.10 | 0.20 | 0.16 | 0.43 |
| asym | 0.31 | 0.25 | 0.46 | 0.31 |
| u_channel | 0.08 | 0.04 | 0.11 | 0.42 |
| plus | 0.09 | 0.04 | 0.23 | 0.26 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.67 | 0.83 | 0.75 | 0.50 |
| B_left | 0.58 | 0.83 | 0.50 | 0.42 |
| C_backright | 0.58 | 0.58 | 0.25 | 0.33 |
| D_far_turn | 0.75 | 0.50 | 0.50 | 0.08 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 43% | 0% | 57% | 46% | 4% | 50% |  |  | 21% | 58% | 48% | 23% |
| 40 kg | 38% | 0% | 62% | 52% | 2% | 46% |  |  | 19% | 58% | 46% | 26% |
| 60 kg | 35% | 0% | 65% | 61% | 2% | 38% |  |  | 23% | 80% | 25% | 30% |
| 80 kg | 36% | 0% | 64% | 70% | 2% | 29% |  |  | 24% | 92% | 9% | 35% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 163 | 0.90 | 8% | 19% | 32% | 49% |
| 40 kg | 186 | 0.90 | 8% | 23% | 42% | 35% |
| 60 kg | 213 | 0.90 | 7% | 34% | 41% | 25% |
| 80 kg | 222 | 0.90 | 7% | 47% | 36% | 17% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 63% | 0.21 | 0.50 | 0.16 | 0.60 | 3 | 0 | 2 | 0 | 0 | 2 | 82 | 0.00 |  |
| 40 kg | 61% | 0.17 | 0.69 | 0.15 | 0.62 | 3 | 0 | 2 | 0 | 0 | 1 | 81 | 0.00 |  |
| 60 kg | 58% | 0.12 | 0.74 | 0.11 | 0.73 | 3 | 1 | 2 | 0 | 0 | 1 | 190 | 0.00 |  |
| 80 kg | 53% | 0.09 | 0.80 | 0.08 | 0.75 | 4 | 1 | 2 | 0 | 0 | 1 | 188 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.69 | 66% | 33% | 0.92 | 68% | 0.17 | 0 | 0 | 0 | 0 | 0 | 0 |
| long | 0.50 | 69% | 39% | 0.92 | 64% | 0.13 | 3 | 1 | 1 | 0 | 0 | 1 |
| sphere | 0.88 | 40% | 18% | 0.91 | 87% | 0.29 | 0 | 0 | 0 | 0 | 0 | 0 |
| cylinder | 0.44 | 43% | 21% | 0.88 | 66% | 0.10 | 1 | 0 | 1 | 0 | 0 | 0 |
| arch | 0.75 | 62% | 33% | 0.89 | 64% | 0.17 | 2 | 0 | 1 | 0 | 0 | 1 |
| dumbbell | 0.62 | 53% | 24% | 0.91 | 53% | 0.11 | 6 | 0 | 4 | 0 | 0 | 1 |
| t_shape | 0.56 | 70% | 38% | 0.92 | 60% | 0.09 | 2 | 0 | 2 | 0 | 0 | 0 |
| beam | 0.19 | 23% | 18% | 0.76 | 24% | 0.08 | 13 | 1 | 8 | 0 | 0 | 4 |
| l_shape | 0.69 | 68% | 37% | 0.91 | 58% | 0.12 | 3 | 1 | 0 | 0 | 0 | 1 |
| asym | 0.12 | 72% | 47% | 0.92 | 51% | 0.05 | 3 | 1 | 2 | 0 | 0 | 0 |
| u_channel | 0.69 | 53% | 22% | 0.94 | 50% | 0.11 | 6 | 1 | 2 | 0 | 0 | 3 |
| plus | 0.38 | 66% | 40% | 0.90 | 57% | 0.09 | 1 | 1 | 0 | 0 | 0 | 1 |
