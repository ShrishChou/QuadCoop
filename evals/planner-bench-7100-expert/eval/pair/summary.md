# Pair evaluation: planner-bench-7100-expert

policy: Stage 4 contact policy logs/keep/marl2/turn_debug/model_15000.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.73 | 0.75 | 0.01 | 0.00 | 26.4 | 0.01 | 0.42 | 0.36 | 0.11 | 0.21 | 1.13 |
| 40 kg | 0.66 | 0.58 | 0.01 | 0.00 | 34.2 | 0.00 | 0.50 | 0.38 | 0.14 | 0.20 | 1.08 |
| 60 kg | 0.57 | 0.46 | 0.02 | 0.03 | 42.1 | 0.01 | 0.61 | 0.43 | 0.23 | 0.30 | 1.05 |
| 80 kg | 0.31 | 0.24 | 0.11 | 0.07 | 39.9 | 0.01 | 0.72 | 0.52 | 0.37 | 0.45 | 1.07 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| cube | part 0 -x end - + part 0 corner -x+y | 0.92 | 0.92 | 0.83 | 0.25 |
| long | part 0 -x seg 2/2 + part 0 corner -x-y | 0.75 | 0.83 | 0.50 | 0.17 |
| sphere | sector 225 + sector 135 | 0.92 | 0.92 | 0.92 | 0.92 |
| cylinder | part 0 corner -x-y + part 0 -x seg 2/2 | 0.50 | 0.17 | 0.25 | 0.33 |
| arch | part 2 -x + part 3 -x | 0.83 | 0.92 | 0.75 | 0.50 |
| dumbbell | part 0 -x + part 1 -x | 0.83 | 0.50 | 0.50 | 0.33 |
| t_shape | part 0 -x seg 3/3 + part 0 -x seg 1/3 | 0.67 | 0.83 | 0.67 | 0.58 |
| beam (unseen) | part 0 -x seg 5/5 + part 0 -x seg 1/5 | 0.67 | 0.33 | 0.08 | 0.00 |
| l_shape (unseen) | part 0 corner -x-y + part 1 -x | 0.58 | 0.92 | 0.92 | 0.25 |
| asym (unseen) | part 0 -x end + + part 1 -x end - | 0.58 | 0.17 | 0.17 | 0.00 |
| u_channel (unseen) | part 0 -x seg 1/3 + part 0 -x seg 3/3 | 0.75 | 0.67 | 0.58 | 0.17 |
| plus (unseen) | part 0 -x end - + part 0 -x end + | 0.75 | 0.75 | 0.67 | 0.25 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.73 | 0.26 | 0.01 | 0.00 | 0.00 | 0.01 | 11.31 |
| 40 kg | 0.66 | 0.32 | 0.01 | 0.01 | 0.00 | 0.01 | 9.42 |
| 60 kg | 0.57 | 0.38 | 0.06 | 0.00 | 0.00 | 0.00 | 10.67 |
| 80 kg | 0.31 | 0.51 | 0.18 | 0.00 | 0.00 | 0.00 | 7.99 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.27 | 0.69 | 0.88 | 0.00 | 1.00 | 0.30 | 0.64 | 0.86 | 0.00 |
| 40 kg | 1.00 | 0.23 | 0.73 | 0.93 | 0.00 | 1.00 | 0.25 | 0.69 | 0.91 | 0.00 |
| 60 kg | 1.00 | 0.24 | 0.73 | 0.94 | 0.00 | 1.00 | 0.25 | 0.69 | 0.92 | 0.00 |
| 80 kg | 1.00 | 0.23 | 0.73 | 0.96 | 0.00 | 1.00 | 0.26 | 0.64 | 0.93 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.78 | 1.87 | 0.07 | 0.76 | 2.32 | 0.08 |
| 40 kg | 0.78 | 2.06 | 0.08 | 0.75 | 2.21 | 0.10 |
| 60 kg | 0.76 | 2.25 | 0.09 | 0.76 | 2.17 | 0.12 |
| 80 kg | 0.77 | 1.88 | 0.11 | 0.76 | 2.35 | 0.17 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.53 | 0.49 | 0.30 |
| 40 kg | 0.59 | 0.54 | 0.31 |
| 60 kg | 0.63 | 0.54 | 0.29 |
| 80 kg | 0.64 | 0.49 | 0.25 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.05 | 0.39 | 27.52 | 11.31 | 0.11 | 0.42 | 7.37 | 0.00 | 0.34 |
| 40 kg | 0.34 | 0.44 | 28.29 | 9.42 | 0.39 | 0.78 | 5.76 | 0.00 | 0.29 |
| 60 kg | 0.90 | 0.44 | 30.04 | 10.67 | 0.27 | 0.99 | 2.33 | 0.00 | 0.32 |
| 80 kg | 1.03 | 0.42 | 27.29 | 7.99 | 0.41 | 2.60 | 0.44 | 0.00 | 0.35 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 102 | 254 | 197 |
| 40 kg | 142 | 306 | 253 |
| 60 kg | 167 | 338 | 304 |
| 80 kg | 188 | 365 | 337 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 1342 | 0.35 | 0.38 (207) | 0.48 (199) | 0.48 (373) | 0.46 (281) | 0.53 (283) |
| 40 kg | 1806 | 0.32 | 0.33 (479) | 0.48 (204) | 0.49 (359) | 0.54 (160) | 0.69 (604) |
| 60 kg | 2171 | 0.32 | 0.32 (536) | 0.39 (349) | 0.49 (270) | 0.58 (408) | 0.72 (609) |
| 80 kg | 2547 | 0.33 | 0.38 (112) | 0.49 (304) | 0.49 (1431) | 0.56 (370) | 0.73 (331) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| cube | 0.09 | 0.13 | 0.16 | 0.37 |
| long | 0.08 | 0.12 | 0.18 | 0.48 |
| sphere | 0.34 | 0.38 | 0.52 | 0.45 |
| cylinder | 0.10 | 0.07 | 0.31 | 0.26 |
| arch | 0.12 | 0.12 | 0.18 | 0.29 |
| dumbbell | 0.13 | 0.14 | 0.12 | 0.47 |
| t_shape | 0.07 | 0.08 | 0.22 | 0.42 |
| beam | 0.16 | 0.24 | 0.30 | 0.56 |
| l_shape | 0.05 | 0.08 | 0.11 | 0.24 |
| asym | 0.07 | 0.10 | 0.40 | 0.35 |
| u_channel | 0.10 | 0.06 | 0.12 | 0.40 |
| plus | 0.05 | 0.11 | 0.08 | 0.13 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.69 | 0.67 | 0.72 | 0.44 |
| B_left | 0.78 | 0.69 | 0.58 | 0.42 |
| C_backright | 0.81 | 0.61 | 0.58 | 0.22 |
| D_far_turn | 0.64 | 0.67 | 0.39 | 0.17 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 40% | 0% | 60% | 37% | 4% | 59% |  |  | 19% | 68% | 40% | 25% |
| 40 kg | 34% | 0% | 66% | 45% | 2% | 52% |  |  | 18% | 70% | 35% | 24% |
| 60 kg | 33% | 0% | 67% | 50% | 2% | 48% |  |  | 19% | 76% | 26% | 25% |
| 80 kg | 35% | 0% | 65% | 56% | 2% | 42% |  |  | 25% | 83% | 21% | 28% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 141 | 0.88 | 9% | 13% | 32% | 55% |
| 40 kg | 172 | 0.90 | 7% | 18% | 41% | 41% |
| 60 kg | 195 | 0.90 | 7% | 21% | 45% | 34% |
| 80 kg | 214 | 0.89 | 7% | 28% | 45% | 28% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 61% | 0.20 | 0.44 | 0.15 | 0.71 | 6 | 0 | 4 | 0 | 0 | 1 | 80 | 0.00 |  |
| 40 kg | 58% | 0.15 | 0.57 | 0.12 | 0.70 | 5 | 0 | 4 | 0 | 0 | 1 | 112 | 0.00 |  |
| 60 kg | 55% | 0.11 | 0.68 | 0.09 | 0.62 | 4 | 0 | 2 | 0 | 0 | 1 | 124 | 0.00 |  |
| 80 kg | 51% | 0.08 | 0.76 | 0.07 | 0.42 | 2 | 0 | 1 | 0 | 0 | 1 | 157 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.73 | 54% | 25% | 0.92 | 69% | 0.16 | 2 | 0 | 1 | 0 | 0 | 0 |
| long | 0.56 | 52% | 22% | 0.92 | 57% | 0.09 | 2 | 0 | 1 | 0 | 0 | 1 |
| sphere | 0.92 | 29% | 10% | 0.91 | 86% | 0.30 | 0 | 0 | 0 | 0 | 0 | 0 |
| cylinder | 0.31 | 33% | 13% | 0.91 | 61% | 0.07 | 4 | 0 | 3 | 0 | 0 | 1 |
| arch | 0.75 | 56% | 28% | 0.82 | 61% | 0.12 | 4 | 0 | 3 | 0 | 0 | 1 |
| dumbbell | 0.54 | 45% | 21% | 0.90 | 51% | 0.09 | 8 | 0 | 6 | 0 | 0 | 2 |
| t_shape | 0.69 | 50% | 19% | 0.91 | 52% | 0.08 | 6 | 0 | 3 | 0 | 0 | 3 |
| beam | 0.27 | 34% | 16% | 0.84 | 30% | 0.08 | 10 | 0 | 7 | 0 | 0 | 2 |
| l_shape | 0.67 | 53% | 22% | 0.91 | 58% | 0.07 | 2 | 0 | 2 | 0 | 0 | 1 |
| asym | 0.23 | 56% | 27% | 0.92 | 47% | 0.05 | 3 | 0 | 2 | 0 | 0 | 1 |
| u_channel | 0.54 | 48% | 18% | 0.92 | 50% | 0.09 | 5 | 0 | 3 | 0 | 0 | 2 |
| plus | 0.60 | 51% | 18% | 0.84 | 55% | 0.08 | 5 | 1 | 4 | 0 | 0 | 1 |
