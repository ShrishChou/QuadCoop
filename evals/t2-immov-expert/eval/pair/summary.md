# Pair evaluation: t2-immov-expert

policy: Stage 4 contact policy logs/keep/marl2/hvB_aa_s0/model_13500.pt (robots start at their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 20 s; precise = 10 cm / 3 deg with the object at rest; 1 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 5000 kg | 0.00 | 0.00 | 0.00 | 0.02 |  | 0.00 | 0.39 | 0.42 | 0.12 | 0.18 | 1.17 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 5000 kg |
|---|---|---|
| cube | part 0 corner -x+y + part 0 corner +x-y | 0.00 |
| long | part 0 +y + part 0 corner +x-y | 0.00 |
| sphere | sector 90 + sector 225 | 0.00 |
| cylinder | part 0 -y + part 0 +y | 0.00 |
| arch | part 3 corner -x-y + part 2 -y | 0.00 |
| dumbbell | part 1 corner -x+y + part 1 +x | 0.00 |
| t_shape | part 0 corner -x+y + part 0 -y | 0.00 |
| beam (unseen) | part 0 corner +x-y + part 0 +y | 0.00 |
| l_shape (unseen) | part 1 corner -x+y + part 0 corner -x-y | 0.00 |
| asym (unseen) | part 0 corner +x+y + part 0 corner -x+y | 0.00 |
| u_channel (unseen) | part 0 corner -x-y + part 2 corner +x-y | 0.00 |
| plus (unseen) | part 0 corner +x+y + part 1 corner -x-y | 0.00 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 5000 kg | 0.00 | 0.98 | 0.02 | 0.00 | 0.00 | 0.00 | 0.25 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 5000 kg | 1.00 | 0.26 | 0.69 | 0.94 | 0.00 | 1.00 | 0.15 | 0.84 | 0.99 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 5000 kg | 0.96 | 0.02 | 0.06 | 1.00 | 0.03 | 0.06 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 5000 kg | 0.46 | 0.54 | 1.00 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 5000 kg | 0.12 | 0.27 | 7.92 | 0.25 | 0.00 | 3.42 | 0.00 | 19.90 | 0.42 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 5000 kg | 188 | 364 | 364 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 5000 kg | 176 | 0.30 | 0.28 (12) | - | 0.50 (121) | - | 0.90 (42) |

## both robots pushing (share of time) by object and mass

| object | 5000 kg |
|---|---|
| cube | 0.00 |
| long | 0.00 |
| sphere | 0.20 |
| cylinder | 0.24 |
| arch | 0.20 |
| dumbbell | 0.00 |
| t_shape | 0.27 |
| beam | 0.17 |
| l_shape | 0.35 |
| asym | 0.00 |
| u_channel | 0.00 |
| plus | 0.01 |

## success by scenario and mass

| scenario | 5000 kg |
|---|---|
| A_straight | 0.00 |
| B_left | 0.00 |
| C_backright | 0.00 |
| D_far_turn | 0.00 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 5000 kg | 29% | 0% | 71% | 37% | 2% | 61% |  |  | 27% | 78% | 35% | 25% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 5000 kg | 223 | 0.89 | 6% | 10% | 45% | 45% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 5000 kg | 0% | 0.00 |  | 0.00 | 0.98 | 20 | 5 | 13 | 0 | 0 | 2 | 230 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube | 0.00 | 34% | 2% | 0.90 | 0% | 0.00 | 20 | 4 | 9 | 0 | 0 | 8 |
| long | 0.00 | 42% | 4% | 0.93 | 0% | 0.00 | 20 | 5 | 15 | 0 | 0 | 0 |
| sphere | 0.00 | 33% | 2% | 0.93 | 0% | 0.00 | 20 | 6 | 14 | 0 | 0 | 0 |
| cylinder | 0.00 | 42% | 14% | 0.89 | 0% | 0.00 | 20 | 5 | 13 | 0 | 0 | 2 |
| arch | 0.00 | 28% | 15% | 0.71 | 0% | 0.00 | 20 | 4 | 14 | 0 | 0 | 2 |
| dumbbell | 0.00 | 33% | 7% | 0.89 | 0% | 0.00 | 20 | 3 | 16 | 0 | 0 | 1 |
| t_shape | 0.00 | 57% | 33% | 0.92 | 0% | 0.00 | 20 | 8 | 12 | 0 | 0 | 0 |
| beam | 0.00 | 19% | 10% | 0.74 | 0% | 0.00 | 15 | 0 | 13 | 0 | 0 | 2 |
| l_shape | 0.00 | 32% | 16% | 0.96 | 0% | 0.00 | 20 | 3 | 16 | 0 | 0 | 0 |
| asym | 0.00 | 52% | 10% | 0.91 | 0% | 0.00 | 20 | 10 | 10 | 0 | 0 | 0 |
| u_channel | 0.00 | 41% | 1% | 0.93 | 0% | 0.00 | 20 | 6 | 14 | 0 | 0 | 0 |
| plus | 0.00 | 32% | 11% | 0.93 | 0% | 0.00 | 20 | 4 | 12 | 0 | 0 | 4 |
