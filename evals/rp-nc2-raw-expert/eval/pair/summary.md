# Pair evaluation: rp-nc2-raw-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto); WALKER OVERRIDE: anymal_c = /orcd/home/002/shrishc/quadcoop/logs/rsl_rl/walker_anymal_c/2026-11-09_00-10-27_v1_nocreep2/model_7997.pt (v1)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 1 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.00 | 0.00 | 0.10 | 0.06 |  | 0.04 | 0.10 | 0.06 | 0.02 | 0.19 | 1.12 |
| 40 kg | 0.02 | 0.00 | 0.15 | 0.02 | 80.0 | 0.08 | 0.13 | 0.14 | 0.04 | 0.17 | 1.09 |
| 60 kg | 0.00 | 0.00 | 0.12 | 0.21 |  | 0.04 | 0.24 | 0.12 | 0.06 | 0.21 | 1.04 |
| 80 kg | 0.00 | 0.00 | 0.21 | 0.15 |  | 0.08 | 0.26 | 0.17 | 0.07 | 0.21 | 1.03 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x+y + part 0 corner -x-y | 0.00 | 0.00 | 0.00 | 0.00 |
| long | part 0 -x seg 2/2 + part 0 corner -x-y | 0.00 | 0.00 | 0.00 | 0.00 |
| sphere | sector 225 + sector 135 | 0.00 | 0.00 | 0.00 | 0.00 |
| cylinder | part 0 -x seg 2/2 + part 0 corner -x-y | 0.00 | 0.25 | 0.00 | 0.00 |
| arch | part 2 -x + part 3 -x | 0.00 | 0.00 | 0.00 | 0.00 |
| dumbbell | part 0 -x + part 1 -x | 0.00 | 0.00 | 0.00 | 0.00 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.00 | 0.00 | 0.00 | 0.00 |
| beam (unseen) | part 0 -x seg 2/5 + part 0 -x seg 4/5 | 0.00 | 0.00 | 0.00 | 0.00 |
| l_shape (unseen) | part 0 corner -x-y + part 1 -x | 0.00 | 0.00 | 0.00 | 0.00 |
| asym (unseen) | part 0 corner -x+y + part 1 -x | 0.00 | 0.00 | 0.00 | 0.00 |
| u_channel (unseen) | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.00 | 0.00 | 0.00 | 0.00 |
| plus (unseen) | part 1 corner -x+y + part 1 corner -x-y | 0.00 | 0.00 | 0.00 | 0.00 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.00 | 0.81 | 0.17 | 0.00 | 0.02 | 0.08 | 5.62 |
| 40 kg | 0.02 | 0.79 | 0.17 | 0.02 | 0.00 | 0.00 | 5.17 |
| 60 kg | 0.00 | 0.65 | 0.33 | 0.00 | 0.02 | 0.00 | 4.94 |
| 80 kg | 0.00 | 0.60 | 0.35 | 0.00 | 0.04 | 0.00 | 3.75 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 2.26 | 0.10 | 0.54 | 0.00 | 1.00 | 2.26 | 0.09 | 0.40 | 0.00 |
| 40 kg | 1.00 | 2.17 | 0.13 | 0.42 | 0.00 | 1.00 | 1.91 | 0.15 | 0.46 | 0.00 |
| 60 kg | 1.00 | 2.51 | 0.20 | 0.55 | 0.00 | 1.00 | 2.51 | 0.15 | 0.48 | 0.00 |
| 80 kg | 1.00 | 3.06 | 0.18 | 0.49 | 0.00 | 1.00 | 3.15 | 0.12 | 0.53 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.41 | 1.51 | 0.10 | 0.32 | 1.82 | 0.08 |
| 40 kg | 0.41 | 1.43 | 0.10 | 0.35 | 1.45 | 0.12 |
| 60 kg | 0.45 | 1.45 | 0.11 | 0.39 | 1.61 | 0.16 |
| 80 kg | 0.50 | 1.76 | 0.19 | 0.43 | 2.06 | 0.18 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.05 | 0.05 | 0.18 |
| 40 kg | 0.07 | 0.09 | 0.18 |
| 60 kg | 0.16 | 0.08 | 0.18 |
| 80 kg | 0.12 | 0.08 | 0.16 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.34 | 0.13 | 35.63 | 5.62 | 0.00 | 0.00 | 0.00 | 0.00 | 0.52 |
| 40 kg | 1.90 | 0.11 | 29.68 | 5.17 | 0.02 | 0.00 | 0.00 | 0.00 | 0.64 |
| 60 kg | 2.08 | 0.15 | 33.76 | 4.94 | 0.00 | 0.02 | 0.00 | 0.00 | 0.64 |
| 80 kg | 3.33 | 0.08 | 37.12 | 3.75 | 0.00 | 0.00 | 0.00 | 0.00 | 0.74 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 100 | 288 | 177 |
| 40 kg | 152 | 353 | 278 |
| 60 kg | 190 | 381 | 301 |
| 80 kg | 207 | 380 | 348 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 22 | 0.38 | 0.36 (9) | 0.49 (4) | 0.56 (5) | 0.61 (1) | 0.64 (3) |
| 40 kg | 35 | 0.35 | 0.46 (3) | 0.51 (19) | 0.52 (7) | 0.55 (3) | 0.89 (2) |
| 60 kg | 43 | 0.30 | 0.52 (1) | 0.46 (18) | 0.54 (13) | 0.58 (9) | 0.78 (2) |
| 80 kg | 30 | 0.28 | - | 0.47 (7) | 0.51 (22) | 0.14 (0) | 0.51 (1) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.00 | 0.02 | 0.02 | 0.01 |
| long | 0.06 | 0.11 | 0.10 | 0.04 |
| sphere | 0.07 | 0.02 | 0.06 | 0.23 |
| cylinder | 0.00 | 0.03 | 0.12 | 0.13 |
| arch | 0.00 | 0.01 | 0.01 | 0.01 |
| dumbbell | 0.03 | 0.08 | 0.05 | 0.05 |
| t_shape | 0.01 | 0.01 | 0.03 | 0.04 |
| beam | 0.02 | 0.11 | 0.05 | 0.19 |
| l_shape | 0.02 | 0.01 | 0.01 | 0.02 |
| asym | 0.01 | 0.01 | 0.19 | 0.02 |
| u_channel | 0.01 | 0.02 | 0.02 | 0.04 |
| plus | 0.04 | 0.04 | 0.08 | 0.08 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.00 | 0.08 | 0.00 | 0.00 |
| B_left | 0.00 | 0.00 | 0.00 | 0.00 |
| C_backright | 0.00 | 0.00 | 0.00 | 0.00 |
| D_far_turn | 0.00 | 0.00 | 0.00 | 0.00 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 93% | 0% | 7% | 38% | 5% | 57% |  |  | 66% | 88% | 45% | 36% |
| 40 kg | 90% | 0% | 10% | 51% | 2% | 47% |  |  | 61% | 81% | 57% | 37% |
| 60 kg | 86% | 0% | 14% | 63% | 1% | 35% |  |  | 60% | 86% | 49% | 36% |
| 80 kg | 88% | 0% | 12% | 64% | 2% | 34% |  |  | 68% | 85% | 55% | 33% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 151 | 0.89 | 9% | 3% | 12% | 85% |
| 40 kg | 188 | 0.88 | 9% | 4% | 17% | 79% |
| 60 kg | 219 | 0.90 | 8% | 8% | 25% | 67% |
| 80 kg | 234 | 0.90 | 9% | 10% | 30% | 60% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 18% | 0.07 | 0.48 | 0.04 | 1.73 | 54 | 0 | 2 | 0 | 0 | 52 | 51 | 0.00 |  |
| 40 kg | 16% | 0.05 | 0.58 | 0.03 | 1.58 | 54 | 0 | 4 | 0 | 0 | 50 | 82 | 0.00 |  |
| 60 kg | 24% | 0.04 | 0.64 | 0.03 | 1.10 | 42 | 0 | 1 | 0 | 0 | 41 | 145 | 0.00 |  |
| 80 kg | 22% | 0.04 | 0.68 | 0.03 | 1.29 | 36 | 1 | 1 | 0 | 0 | 35 | 126 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.00 | 50% | 2% | 0.90 | 12% | 0.02 | 60 | 0 | 0 | 0 | 0 | 60 |
| long | 0.00 | 66% | 10% | 0.91 | 25% | 0.05 | 41 | 0 | 0 | 0 | 0 | 41 |
| sphere | 0.00 | 34% | 4% | 0.93 | 26% | 0.06 | 48 | 0 | 4 | 0 | 0 | 43 |
| cylinder | 0.06 | 37% | 5% | 0.88 | 31% | 0.06 | 36 | 0 | 0 | 0 | 0 | 36 |
| arch | 0.00 | 62% | 5% | 0.85 | 12% | 0.02 | 58 | 0 | 4 | 0 | 0 | 53 |
| dumbbell | 0.00 | 60% | 6% | 0.90 | 18% | 0.03 | 52 | 1 | 4 | 0 | 0 | 47 |
| t_shape | 0.00 | 65% | 7% | 0.91 | 21% | 0.01 | 46 | 0 | 0 | 0 | 0 | 46 |
| beam | 0.00 | 33% | 10% | 0.76 | 15% | 0.05 | 44 | 1 | 5 | 0 | 0 | 39 |
| l_shape | 0.00 | 64% | 7% | 0.93 | 18% | 0.01 | 50 | 0 | 4 | 0 | 0 | 46 |
| asym | 0.00 | 58% | 5% | 0.91 | 14% | 0.01 | 50 | 1 | 2 | 0 | 0 | 47 |
| u_channel | 0.00 | 57% | 2% | 0.91 | 16% | 0.02 | 45 | 0 | 0 | 0 | 0 | 45 |
| plus | 0.00 | 64% | 10% | 0.89 | 31% | 0.04 | 30 | 0 | 0 | 0 | 0 | 30 |
