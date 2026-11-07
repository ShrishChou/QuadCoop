# Pair evaluation: game-hvB-r2-allpairs

policy: Stage 4 contact policy logs/keep/marl2/hvB_aa_s0/model_13500.pt (robots start at their contacts; contact rule re-applied: never)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 40 kg | 0.05 | 0.05 | 0.02 | 0.02 | 14.1 | 0.01 | 0.21 | 0.23 | 0.07 | 0.20 | 1.00 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 40 kg |
|---|---|---|
| asym (unseen) | part 1 -x + part 0 corner -x+y | 0.00 |
| u_channel (unseen) | part 0 -x seg 1/3 + part 0 corner -x+y | 0.07 |
| plus (unseen) | part 1 -x + part 0 corner -x-y | 0.05 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 40 kg | 0.05 | 0.91 | 0.04 | 0.00 | 0.00 | 0.09 | 0.00 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 40 kg | 1.00 | 0.21 | 0.74 | 0.94 | 0.00 | 1.00 | 0.20 | 0.74 | 0.96 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 40 kg | 1.00 | 0.02 | 0.06 | 1.00 | 0.02 | 0.06 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 40 kg | 0.49 | 0.49 | 0.84 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 40 kg | 0.35 | 0.34 | 28.69 | 0.00 |  |  |  |  |  |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 40 kg | 131 | 312 | 226 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 40 kg | 3129 | 0.37 | 0.40 (1154) | 0.44 (288) | 0.52 (418) | 0.55 (281) | 0.65 (988) |

## both robots pushing (share of time) by object and mass

| object | 40 kg |
|---|---|
| asym | 0.13 |
| u_channel | 0.07 |
| plus | 0.04 |

## success by scenario and mass

| scenario | 40 kg |
|---|---|
| A_straight | 0.10 |
| B_left | 0.05 |
| C_backright | 0.04 |
| D_far_turn | 0.03 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 40 kg | 34% | 0% | 66% | 24% | 1% | 74% |  |  | 34% | 75% | 39% | 24% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 40 kg | 167 | 0.91 | 6% | 7% | 28% | 65% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 40 kg | 27% | 0.06 | 0.45 | 0.04 | 2.36 | 29 | 0 | 23 | 0 | 0 | 6 | 97 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| asym | 0.00 | 34% | 12% | 0.92 | 36% | 0.04 | 16 | 0 | 15 | 0 | 0 | 1 |
| u_channel | 0.07 | 22% | 6% | 0.91 | 26% | 0.05 | 31 | 0 | 26 | 0 | 0 | 4 |
| plus | 0.05 | 23% | 5% | 0.91 | 24% | 0.04 | 32 | 0 | 20 | 0 | 0 | 12 |
