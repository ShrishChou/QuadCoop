# Pair evaluation: rp-nc2-projrate-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto); WALKER OVERRIDE: anymal_c = /orcd/home/002/shrishc/quadcoop/logs/rsl_rl/walker_anymal_c/2026-11-09_00-10-27_v1_nocreep2/model_7997.pt (v1)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 1 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.00 | 0.00 | 0.12 | 0.04 |  | 0.09 | 0.14 | 0.08 | 0.03 | 0.17 | 0.88 |
| 40 kg | 0.00 | 0.00 | 0.06 | 0.02 |  | 0.05 | 0.14 | 0.06 | 0.03 | 0.18 | 0.96 |
| 60 kg | 0.02 | 0.02 | 0.08 | 0.06 | 14.9 | 0.09 | 0.18 | 0.10 | 0.05 | 0.20 | 0.93 |
| 80 kg | 0.00 | 0.00 | 0.06 | 0.10 |  | 0.07 | 0.28 | 0.25 | 0.11 | 0.28 | 0.90 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 corner -x+y + part 0 corner -x-y | 0.00 | 0.00 | 0.00 | 0.00 |
| long | part 0 -x seg 2/2 + part 0 corner -x-y | 0.00 | 0.00 | 0.00 | 0.00 |
| sphere | sector 225 + sector 135 | 0.00 | 0.00 | 0.00 | 0.00 |
| cylinder | part 0 -x seg 2/2 + part 0 corner -x-y | 0.00 | 0.00 | 0.00 | 0.00 |
| arch | part 2 -x + part 3 -x | 0.00 | 0.00 | 0.00 | 0.00 |
| dumbbell | part 0 -x + part 1 -x | 0.00 | 0.00 | 0.00 | 0.00 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.00 | 0.00 | 0.00 | 0.00 |
| beam (unseen) | part 0 -x seg 2/5 + part 0 -x seg 4/5 | 0.00 | 0.00 | 0.25 | 0.00 |
| l_shape (unseen) | part 0 corner -x-y + part 1 -x | 0.00 | 0.00 | 0.00 | 0.00 |
| asym (unseen) | part 0 corner -x+y + part 1 -x | 0.00 | 0.00 | 0.00 | 0.00 |
| u_channel (unseen) | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.00 | 0.00 | 0.00 | 0.00 |
| plus (unseen) | part 1 corner -x+y + part 1 corner -x-y | 0.00 | 0.00 | 0.00 | 0.00 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.00 | 0.83 | 0.17 | 0.00 | 0.00 | 0.08 | 5.50 |
| 40 kg | 0.00 | 0.90 | 0.08 | 0.00 | 0.02 | 0.02 | 4.52 |
| 60 kg | 0.02 | 0.81 | 0.15 | 0.00 | 0.02 | 0.00 | 4.94 |
| 80 kg | 0.00 | 0.83 | 0.17 | 0.00 | 0.00 | 0.00 | 3.88 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 2.18 | 0.15 | 0.53 | 0.00 | 1.00 | 2.07 | 0.06 | 0.47 | 0.00 |
| 40 kg | 1.00 | 2.02 | 0.19 | 0.51 | 0.00 | 1.00 | 2.40 | 0.10 | 0.38 | 0.00 |
| 60 kg | 1.00 | 3.39 | 0.15 | 0.42 | 0.00 | 1.00 | 3.39 | 0.10 | 0.42 | 0.00 |
| 80 kg | 1.00 | 2.67 | 0.16 | 0.60 | 0.00 | 1.00 | 3.86 | 0.15 | 0.47 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.34 | 1.55 | 0.16 | 0.27 | 1.58 | 0.09 |
| 40 kg | 0.40 | 1.79 | 0.15 | 0.31 | 1.52 | 0.09 |
| 60 kg | 0.42 | 2.05 | 0.17 | 0.34 | 1.53 | 0.14 |
| 80 kg | 0.42 | 2.42 | 0.23 | 0.36 | 1.81 | 0.21 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.04 | 0.03 | 0.19 |
| 40 kg | 0.10 | 0.04 | 0.18 |
| 60 kg | 0.08 | 0.04 | 0.19 |
| 80 kg | 0.11 | 0.10 | 0.17 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.32 | 0.14 | 28.99 | 5.50 | 0.00 | 0.00 | 0.00 | 0.00 | 0.59 |
| 40 kg | 4.26 | 0.10 | 27.71 | 4.52 | 0.00 | 0.00 | 0.00 | 0.00 | 0.64 |
| 60 kg | 2.40 | 0.12 | 35.07 | 4.94 | 0.00 | 0.00 | 0.00 | 0.00 | 0.76 |
| 80 kg | 4.44 | 0.15 | 35.11 | 3.88 | 0.02 | 0.19 | 0.00 | 0.00 | 0.68 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 87 | 255 | 169 |
| 40 kg | 130 | 305 | 216 |
| 60 kg | 173 | 354 | 288 |
| 80 kg | 209 | 360 | 317 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 21 | 0.39 | 0.42 (2) | 0.47 (6) | 0.47 (9) | 0.59 (3) | - |
| 40 kg | 31 | 0.34 | 0.38 (7) | 0.49 (10) | 0.45 (8) | 0.55 (3) | 0.65 (3) |
| 60 kg | 28 | 0.34 | 0.40 (0) | 0.48 (10) | 0.64 (14) | 0.57 (2) | 0.66 (3) |
| 80 kg | 79 | 0.27 | - | 0.61 (15) | 0.51 (55) | 0.53 (9) | 0.51 (1) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.00 | 0.01 | 0.01 | 0.01 |
| long | 0.05 | 0.09 | 0.15 | 0.04 |
| sphere | 0.01 | 0.02 | 0.05 | 0.21 |
| cylinder | 0.06 | 0.01 | 0.11 | 0.03 |
| arch | 0.00 | 0.00 | 0.00 | 0.00 |
| dumbbell | 0.02 | 0.03 | 0.03 | 0.10 |
| t_shape | 0.04 | 0.05 | 0.06 | 0.10 |
| beam | 0.01 | 0.01 | 0.05 | 0.42 |
| l_shape | 0.07 | 0.01 | 0.01 | 0.03 |
| asym | 0.01 | 0.07 | 0.01 | 0.04 |
| u_channel | 0.03 | 0.03 | 0.03 | 0.27 |
| plus | 0.08 | 0.04 | 0.04 | 0.10 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.00 | 0.00 | 0.08 | 0.00 |
| B_left | 0.00 | 0.00 | 0.00 | 0.00 |
| C_backright | 0.00 | 0.00 | 0.00 | 0.00 |
| D_far_turn | 0.00 | 0.00 | 0.00 | 0.00 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 95% | 0% | 5% | 38% | 6% | 56% |  |  | 65% | 79% | 55% | 36% |
| 40 kg | 91% | 0% | 9% | 53% | 4% | 43% |  |  | 59% | 77% | 62% | 30% |
| 60 kg | 93% | 0% | 7% | 64% | 2% | 34% |  |  | 65% | 83% | 56% | 39% |
| 80 kg | 88% | 0% | 12% | 66% | 3% | 32% |  |  | 62% | 85% | 51% | 43% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 137 | 0.87 | 11% | 3% | 14% | 83% |
| 40 kg | 168 | 0.90 | 7% | 5% | 17% | 78% |
| 60 kg | 203 | 0.88 | 6% | 7% | 22% | 71% |
| 80 kg | 221 | 0.93 | 3% | 12% | 30% | 58% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 19% | 0.06 | 0.50 | 0.04 | 1.67 | 55 | 0 | 0 | 0 | 0 | 55 |  | 0.00 |  |
| 40 kg | 16% | 0.04 | 0.64 | 0.02 | 1.40 | 60 | 1 | 5 | 0 | 0 | 55 | 65 | 0.00 |  |
| 60 kg | 19% | 0.04 | 0.58 | 0.03 | 1.35 | 51 | 0 | 0 | 0 | 0 | 50 | 140 | 0.00 |  |
| 80 kg | 16% | 0.02 | 0.69 | 0.02 | 1.92 | 46 | 1 | 2 | 0 | 0 | 43 | 156 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.00 | 63% | 3% | 0.92 | 10% | 0.02 | 62 | 0 | 5 | 0 | 0 | 57 |
| long | 0.00 | 58% | 9% | 0.92 | 22% | 0.04 | 50 | 2 | 2 | 0 | 0 | 47 |
| sphere | 0.00 | 39% | 3% | 0.92 | 25% | 0.06 | 48 | 0 | 0 | 0 | 0 | 48 |
| cylinder | 0.00 | 45% | 5% | 0.89 | 27% | 0.06 | 47 | 0 | 2 | 0 | 0 | 45 |
| arch | 0.00 | 68% | 4% | 0.89 | 15% | 0.01 | 56 | 0 | 0 | 0 | 0 | 56 |
| dumbbell | 0.00 | 57% | 14% | 0.89 | 23% | 0.02 | 48 | 0 | 5 | 0 | 0 | 44 |
| t_shape | 0.00 | 63% | 6% | 0.93 | 14% | 0.02 | 58 | 0 | 4 | 0 | 0 | 54 |
| beam | 0.06 | 22% | 5% | 0.72 | 7% | 0.01 | 61 | 1 | 5 | 0 | 0 | 55 |
| l_shape | 0.00 | 65% | 7% | 0.89 | 14% | 0.02 | 55 | 0 | 0 | 0 | 0 | 55 |
| asym | 0.00 | 66% | 7% | 0.92 | 12% | 0.01 | 49 | 1 | 0 | 0 | 0 | 48 |
| u_channel | 0.00 | 52% | 8% | 0.94 | 17% | 0.03 | 54 | 0 | 1 | 0 | 0 | 53 |
| plus | 0.00 | 61% | 12% | 0.93 | 22% | 0.02 | 46 | 0 | 0 | 0 | 0 | 46 |
