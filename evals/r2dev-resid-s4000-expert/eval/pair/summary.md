# Pair evaluation: r2dev-resid-s4000-expert

policy: Stage 4 contact policy logs/marl2/resid2_beam_s0/model_300.pt (robots start behind the object and walk to their contacts; contact rule re-applied: auto)

success = 10 cm / 6 deg held 1 s within 80 s; precise = 10 cm / 3 deg with the object at rest; 3 placements per object x scenario x mass; nominal object sizes; same tasks and robot placements as scripts/eval_coop2.py

## by mass

| mass | success | precise | anymal1 fell | anymal2 fell | time to success (s) | robots touching | anymal1 pushing | anymal2 pushing | both pushing | co-push share | contact spread (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 0.83 | 0.75 | 0.08 | 0.00 | 34.1 | 0.00 | 0.36 | 0.37 | 0.13 | 0.26 | 1.51 |
| 40 kg | 0.50 | 0.50 | 0.08 | 0.08 | 36.1 | 0.00 | 0.55 | 0.41 | 0.15 | 0.18 | 1.45 |
| 60 kg | 0.17 | 0.17 | 0.25 | 0.08 | 66.9 | 0.02 | 0.78 | 0.40 | 0.30 | 0.34 | 1.31 |
| 80 kg | 0.00 | 0.00 | 0.42 | 0.17 |  | 0.03 | 0.78 | 0.53 | 0.40 | 0.46 | 1.30 |

tasks using both robots: 1.00 (the rest: no room for two pushers toward the goal, robot 2 parked)

## success by object and mass

| object | contacts (A_straight, rep 0) | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|---|
| beam (unseen) | part 0 -x seg 5/5 + part 0 -x seg 1/5 | 0.83 | 0.50 | 0.17 | 0.00 |

## how episodes ended (share) by mass

| mass | success | ran out of time | a robot fell | object tipped | object lost | overshoot (within 20 cm, ended 30+ cm away) | contact changes per episode |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.83 | 0.08 | 0.08 | 0.00 | 0.00 | 0.00 | 10.83 |
| 40 kg | 0.50 | 0.33 | 0.17 | 0.00 | 0.00 | 0.00 | 6.33 |
| 60 kg | 0.17 | 0.50 | 0.33 | 0.00 | 0.00 | 0.00 | 3.42 |
| 80 kg | 0.00 | 0.42 | 0.58 | 0.00 | 0.00 | 0.00 | 2.25 |

## holding the assigned contact (while all the time)

| mass | anymal1 engaged | anymal1 front-contact dist (m) | anymal1 within 0.25 m | anymal1 facing it (45 deg) | anymal1 returns | anymal2 engaged | anymal2 front-contact dist (m) | anymal2 within 0.25 m | anymal2 facing it (45 deg) | anymal2 returns |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 1.00 | 0.33 | 0.63 | 0.87 | 0.00 | 1.00 | 0.44 | 0.54 | 0.84 | 0.00 |
| 40 kg | 1.00 | 0.31 | 0.63 | 0.95 | 0.00 | 1.00 | 0.28 | 0.63 | 0.94 | 0.00 |
| 60 kg | 1.00 | 0.30 | 0.56 | 0.96 | 0.00 | 1.00 | 0.34 | 0.49 | 0.97 | 0.00 |
| 80 kg | 1.00 | 0.31 | 0.57 | 0.95 | 0.00 | 1.00 | 0.34 | 0.42 | 0.93 | 0.00 |

## reaching the assigned contact (each assignment: at the start and at every contact change)

| mass | anymal1 reached | anymal1 time to reach (s) | anymal1 bumping off-contact | anymal2 reached | anymal2 time to reach (s) | anymal2 bumping off-contact |
|---|---|---|---|---|---|---|
| 20 kg | 0.94 | 2.60 | 0.07 | 0.90 | 2.72 | 0.07 |
| 40 kg | 0.88 | 2.02 | 0.15 | 0.88 | 2.26 | 0.14 |
| 60 kg | 0.85 | 2.12 | 0.27 | 0.82 | 3.25 | 0.19 |
| 80 kg | 0.78 | 1.49 | 0.25 | 0.78 | 2.34 | 0.31 |

## pressing the contact (front on the object while on its contact, share of time); mean pair residual (wrench rule)

| mass | anymal1 pressing | anymal2 pressing | residual |
|---|---|---|---|
| 20 kg | 0.57 | 0.45 | 0.29 |
| 40 kg | 0.59 | 0.56 | 0.36 |
| 60 kg | 0.50 | 0.45 | 0.31 |
| 80 kg | 0.48 | 0.39 | 0.16 |

## coordination (pressing alone while the partner is > 1 m from its contact; share of pressing time with both pressing; metres walked by both robots; expert rule: no-progress re-plans that penalise the place, re-plans for no progress at the force limit (no penalty), no-progress windows within 0.5 m of the goal (no penalty), seconds no pair could slide the object (needs more robots), share of on-contact time holding)

| mass | pressing alone, partner far (s) | both pressing | walked (m) | contact changes | stall re-plans | at-limit re-plans | finishing stalls | needs more robots (s) | holding |
|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 2.17 | 0.40 | 29.53 | 10.83 | 0.67 | 0.00 | 3.50 | 0.00 | 0.36 |
| 40 kg | 1.10 | 0.47 | 34.08 | 6.33 | 0.25 | 0.08 | 1.75 | 0.00 | 0.32 |
| 60 kg | 0.17 | 0.34 | 37.35 | 3.42 | 0.33 | 0.00 | 0.00 | 0.00 | 0.44 |
| 80 kg | 0.22 | 0.31 | 37.41 | 2.25 | 0.00 | 2.33 | 0.00 | 0.00 | 0.48 |

## push force (each robot's horizontal contact force on the object while pressing its contact and touching it, both robots pooled; mean over episodes of each episode's median and 90th percentile, and of the 90th percentile while the object is nearly still (< 0.05 m/s), i.e. what a robot sustains against the object's full resistance: the planner's robot_push_force should come from this)

| mass | median (N) | 90th percentile (N) | 90th percentile, object still (N) |
|---|---|---|---|
| 20 kg | 85 | 177 | 113 |
| 40 kg | 98 | 212 | 158 |
| 60 kg | 118 | 245 | 203 |
| 80 kg | 127 | 255 | 232 |

## following the force split (while both robots press their contacts: robot 1's measured share of the pair's push along the commanded directions, against its commanded share; pooled over episodes. A robot that follows its share tracks the commanded column; 0.5 everywhere = both push alike whatever they are told)

| mass | seconds | mean abs error | told 0.0-0.2: measured (s) | told 0.2-0.4: measured (s) | told 0.4-0.6: measured (s) | told 0.6-0.8: measured (s) | told 0.8-1.0: measured (s) |
|---|---|---|---|---|---|---|---|
| 20 kg | 58 | 0.45 | 0.44 (16) | 0.69 (14) | 0.58 (8) | 0.39 (3) | 0.58 (16) |
| 40 kg | 155 | 0.39 | 0.31 (32) | 0.53 (11) | 0.68 (12) | 0.60 (8) | 0.58 (91) |
| 60 kg | 131 | 0.37 | 0.45 (8) | 0.46 (22) | 0.54 (17) | 0.43 (27) | 0.67 (57) |
| 80 kg | 101 | 0.32 | - | 0.58 (33) | 0.71 (24) | 0.57 (8) | 0.86 (36) |

## both robots pushing (share of time) by object and mass

| object | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| beam | 0.13 | 0.15 | 0.30 | 0.40 |

## success by scenario and mass

| scenario | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| A_straight | 0.67 | 0.33 | 0.33 | 0.00 |
| B_left | 1.00 | 0.67 | 0.00 | 0.00 |
| C_backright | 1.00 | 0.67 | 0.33 | 0.00 |
| D_far_turn | 0.67 | 0.33 | 0.00 | 0.00 |

## diagnosis 1: what each robot is told, and what it does then
(shares of robot time; push: of the time told to push, pressing = touching the object with 30 N or more; hold: of the time told to hold, pressing 30 N+ or walking > 0.15 m/s; drifted: of the time engaged on its contact, outside the on-contact zone (0.25 m / 30 deg), and why; near edge: of the time inside the zone, beyond 80% of either limit. Stage 4e has no commands: on its contact = told to push)

| mass | walk | hold | push | push: pressing | push: light touch | push: not touching | hold: pressing | hold: moving | drifted off | ... by distance | ... by heading | near zone edge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 44% | 0% | 56% | 29% | 4% | 67% |  |  | 21% | 93% | 15% | 30% |
| 40 kg | 39% | 0% | 61% | 37% | 4% | 59% |  |  | 28% | 93% | 10% | 36% |
| 60 kg | 50% | 0% | 50% | 50% | 3% | 47% |  |  | 42% | 91% | 12% | 51% |
| 80 kg | 53% | 0% | 47% | 44% | 3% | 54% |  |  | 48% | 92% | 11% | 55% |

## diagnosis 2: the push (while told to push and pressing) and the team
(force = mean contact force; alignment = mean cosine between the force and the commanded push direction, 1 = exactly along it; misaligned = more than 45 deg off; team = share of episode time both robots press, one, none)

| mass | force (N) | alignment | misaligned | both pressing | one pressing | none pressing |
|---|---|---|---|---|---|---|
| 20 kg | 109 | 0.88 | 10% | 7% | 28% | 65% |
| 40 kg | 127 | 0.86 | 11% | 15% | 44% | 41% |
| 60 kg | 147 | 0.81 | 18% | 24% | 47% | 29% |
| 80 kg | 151 | 0.79 | 20% | 24% | 46% | 30% |

## diagnosis 3: the object and every standstill
(moving = speed > 2 cm/s or turning > 3 deg/s; alignment = cosine between its velocity and the planner's wanted motion; progress = pose error removed per second (m/s); standstill = still for 3 s or more before the goal, its seconds filed by what the robots did: push hard = told to push and pressing (the push does not move it), push soft = told to push but not pressing, wait = a robot holds while its partner is off its contact, hold = both on and holding, walk = nobody on a contact; per episode)

| mass | moving | speed (m/s) | alignment | progress (m/s) | standstills | standstill (s) | push hard | push soft | wait | hold | walk | force in push-hard standstills (N) | team-push breaks | push->hold per min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 kg | 42% | 0.19 | 0.49 | 0.15 | 1.83 | 9 | 0 | 6 | 0 | 0 | 3 | 87 | 0.00 |  |
| 40 kg | 39% | 0.12 | 0.63 | 0.10 | 1.25 | 5 | 0 | 3 | 0 | 0 | 2 | 101 | 0.00 |  |
| 60 kg | 39% | 0.07 | 0.68 | 0.06 | 0.58 | 2 | 0 | 1 | 0 | 0 | 1 | 163 | 0.00 |  |
| 80 kg | 21% | 0.03 | 0.74 | 0.02 | 0.25 | 1 | 0 | 0 | 0 | 0 | 1 | 114 | 0.00 |  |

## diagnosis 4: by object (all masses)

| object | success | push: pressing | both pressing | alignment | object moving | progress (m/s) | standstill (s) | push hard | push soft | wait | hold | walk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| beam | 0.38 | 40% | 17% | 0.84 | 35% | 0.08 | 4 | 0 | 3 | 0 | 0 | 2 |
