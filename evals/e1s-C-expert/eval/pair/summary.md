# Pair evaluation: e1s-C-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: never)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.08 | 0.10 | 0.03 | 0.01 | 8.9 | 0.08 | 0.14 | 0.21 | 0.04 | 0.15 | 0.97 |
| 40 kg | 0.09 | 0.09 | 0.03 | 0.02 | 14.3 | 0.08 | 0.24 | 0.26 | 0.07 | 0.19 | 1.03 |
| 60 kg | 0.05 | 0.06 | 0.10 | 0.06 | 17.4 | 0.08 | 0.34 | 0.34 | 0.14 | 0.29 | 1.07 |
| 80 kg | 0.06 | 0.04 | 0.10 | 0.07 | 28.9 | 0.07 | 0.50 | 0.39 | 0.22 | 0.34 | 1.02 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 -x end + + part 0 corner -x-y | 0.25 | 0.42 | 0.17 | 0.08 |
| long | part 0 corner -x+y + part 0 -x seg 1/2 | 0.00 | 0.00 | 0.00 | 0.08 |
| sphere | sector 225 + sector 135 | 0.08 | 0.08 | 0.08 | 0.17 |
| cylinder | part 0 -x seg 1/2 + part 0 corner -x+y | 0.17 | 0.25 | 0.00 | 0.08 |
| arch | part 3 -x + part 2 -x | 0.17 | 0.08 | 0.08 | 0.17 |
| dumbbell | part 0 -x + part 1 -x | 0.08 | 0.08 | 0.17 | 0.08 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.08 | 0.00 | 0.00 | 0.00 |
| beam (unseen) | part 0 -x seg 2/5 + part 0 -x seg 4/5 | 0.00 | 0.08 | 0.00 | 0.00 |
| l_shape (unseen) | part 0 corner -x-y + part 1 -x | 0.00 | 0.00 | 0.00 | 0.00 |
| asym (unseen) | part 1 -x end - + part 0 -x end + | 0.00 | 0.00 | 0.00 | 0.00 |
| u_channel (unseen) | part 0 -x seg 1/3 + part 0 -x seg 3/3 | 0.08 | 0.08 | 0.08 | 0.00 |
| plus (unseen) | part 0 -x end - + part 0 -x end + | 0.00 | 0.00 | 0.00 | 0.00 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.08 | 0.88 | 0.04 | 0.00 | 0.00 | 0.10 | 0.00 |
| 40 kg | 0.09 | 0.85 | 0.06 | 0.01 | 0.00 | 0.06 | 0.00 |
| 60 kg | 0.05 | 0.80 | 0.15 | 0.00 | 0.00 | 0.02 | 0.00 |
| 80 kg | 0.06 | 0.78 | 0.17 | 0.00 | 0.00 | 0.01 | 0.00 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.39 | 0.60 | 0.90 | 0.00 | 1.00 | 0.40 | 0.60 | 0.88 | 0.00 |
| 40 kg | 1.00 | 0.39 | 0.59 | 0.89 | 0.00 | 1.00 | 0.39 | 0.61 | 0.86 | 0.00 |
| 60 kg | 1.00 | 0.38 | 0.61 | 0.89 | 0.00 | 1.00 | 0.40 | 0.57 | 0.87 | 0.00 |
| 80 kg | 1.00 | 0.33 | 0.65 | 0.92 | 0.00 | 1.00 | 0.39 | 0.57 | 0.87 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.85 | 5.86 | 0.03 | 0.86 | 6.68 | 0.03 |
| 40 kg | 0.85 | 5.25 | 0.05 | 0.85 | 6.20 | 0.05 |
| 60 kg | 0.88 | 5.56 | 0.07 | 0.86 | 6.66 | 0.09 |
| 80 kg | 0.93 | 6.12 | 0.10 | 0.90 | 6.25 | 0.11 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.38 | 0.46 | 0.76 |
| 40 kg | 0.42 | 0.47 | 0.69 |
| 60 kg | 0.45 | 0.47 | 0.57 |
| 80 kg | 0.52 | 0.44 | 0.52 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 2.64 | 0.32 | 30.79 | 0.00 | 0.00 | 0.00 | 6.47 | 0.00 | 0.43 |
| 40 kg | 2.83 | 0.33 | 32.27 | 0.00 | 0.00 | 0.00 | 5.73 | 0.00 | 0.41 |
| 60 kg | 2.19 | 0.34 | 32.72 | 0.00 | 0.00 | 0.00 | 4.30 | 0.00 | 0.42 |
| 80 kg | 1.55 | 0.35 | 32.12 | 0.00 | 0.00 | 0.00 | 2.30 | 0.00 | 0.40 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 77 | 224 | 136 |
| 40 kg | 118 | 289 | 205 |
| 60 kg | 153 | 335 | 275 |
| 80 kg | 181 | 360 | 327 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 244 | 0.35 | 0.40 (97) | 0.52 (37) | 0.52 (31) | 0.54 (11) | 0.79 (68) |
| 40 kg | 706 | 0.38 | 0.33 (171) | 0.54 (150) | 0.41 (97) | 0.48 (44) | 0.59 (245) |
| 60 kg | 1433 | 0.35 | 0.35 (477) | 0.47 (264) | 0.49 (180) | 0.49 (149) | 0.64 (362) |
| 80 kg | 2092 | 0.34 | 0.35 (463) | 0.45 (274) | 0.53 (616) | 0.52 (322) | 0.65 (418) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.03 | 0.05 | 0.03 | 0.06 |
| long | 0.03 | 0.07 | 0.07 | 0.17 |
| sphere | 0.04 | 0.08 | 0.10 | 0.13 |
| cylinder | 0.08 | 0.12 | 0.14 | 0.13 |
| arch | 0.12 | 0.08 | 0.15 | 0.34 |
| dumbbell | 0.06 | 0.14 | 0.23 | 0.37 |
| t_shape | 0.03 | 0.02 | 0.11 | 0.27 |
| beam | 0.03 | 0.14 | 0.34 | 0.54 |
| l_shape | 0.00 | 0.03 | 0.04 | 0.09 |
| asym | 0.03 | 0.08 | 0.38 | 0.27 |
| u_channel | 0.03 | 0.07 | 0.12 | 0.20 |
| plus | 0.02 | 0.01 | 0.04 | 0.06 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.19 | 0.19 | 0.19 | 0.19 |
| B_left | 0.08 | 0.11 | 0.00 | 0.03 |
| C_backright | 0.03 | 0.03 | 0.00 | 0.00 |
| D_far_turn | 0.00 | 0.03 | 0.00 | 0.00 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 45% | 0% | 55% | 13% | 2% | 85% |  |  | 31% | 77% | 39% | 22% |
| 40 kg | 45% | 0% | 55% | 24% | 2% | 74% |  |  | 32% | 78% | 43% | 24% |
| 60 kg | 44% | 0% | 56% | 37% | 2% | 61% |  |  | 29% | 83% | 32% | 27% |
| 80 kg | 42% | 0% | 58% | 45% | 2% | 53% |  |  | 29% | 84% | 30% | 26% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 121 | 0.87 | 10% | 2% | 13% | 85% |
| 40 kg | 157 | 0.88 | 8% | 5% | 23% | 72% |
| 60 kg | 186 | 0.89 | 8% | 11% | 33% | 56% |
| 80 kg | 209 | 0.91 | 6% | 17% | 39% | 44% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 21% | 0.08 | 0.41 | 0.06 | 2.65 | 45 | 0 | 32 | 0 | 0 | 13 | 63 | 0.00 |  |
| 40 kg | 27% | 0.07 | 0.51 | 0.05 | 2.33 | 35 | 0 | 24 | 0 | 0 | 11 | 86 | 0.00 |  |
| 60 kg | 32% | 0.06 | 0.60 | 0.04 | 2.12 | 23 | 0 | 13 | 0 | 0 | 9 | 103 | 0.00 |  |
| 80 kg | 35% | 0.05 | 0.68 | 0.04 | 1.20 | 13 | 0 | 6 | 0 | 0 | 7 | 127 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.23 | 36% | 8% | 0.92 | 39% | 0.08 | 22 | 0 | 18 | 0 | 0 | 5 |
| long | 0.02 | 30% | 7% | 0.92 | 26% | 0.03 | 23 | 0 | 14 | 0 | 0 | 9 |
| sphere | 0.10 | 11% | 2% | 0.95 | 36% | 0.08 | 43 | 0 | 30 | 0 | 0 | 13 |
| cylinder | 0.12 | 24% | 6% | 0.90 | 40% | 0.07 | 22 | 0 | 17 | 0 | 0 | 5 |
| arch | 0.12 | 37% | 14% | 0.79 | 29% | 0.06 | 35 | 0 | 19 | 0 | 0 | 16 |
| dumbbell | 0.10 | 34% | 11% | 0.91 | 32% | 0.06 | 28 | 0 | 21 | 0 | 0 | 7 |
| t_shape | 0.02 | 31% | 12% | 0.91 | 28% | 0.04 | 29 | 0 | 23 | 0 | 0 | 6 |
| beam | 0.02 | 32% | 15% | 0.86 | 20% | 0.03 | 24 | 1 | 17 | 0 | 0 | 6 |
| l_shape | 0.00 | 22% | 4% | 0.91 | 21% | 0.03 | 33 | 0 | 22 | 0 | 0 | 10 |
| asym | 0.00 | 45% | 14% | 0.92 | 30% | 0.03 | 19 | 0 | 15 | 0 | 0 | 5 |
| u_channel | 0.06 | 24% | 6% | 0.90 | 26% | 0.05 | 31 | 0 | 24 | 0 | 0 | 7 |
| plus | 0.00 | 33% | 4% | 0.77 | 20% | 0.02 | 38 | 0 | 8 | 0 | 0 | 30 |
