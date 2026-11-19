# Spot-arm turn pilot: sa-release-v2-s3-retract-40kg-2m

logs/marl2/sa_heavy_learned_s0/model_4000.pt, iteration 4000, mappo, arms learned. long 40 kg, 2 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

Walker: logs/rsl_rl/walker_spot_arm/2026-11-17_18-10-15_push_ft_s3_handload/model_2999.pt. Torso: default (interface False, expanded []). Arm-object collisions: on. Release: retract for 5 s.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 90.0% | 2.5% | 17.3 | 0.074 | 2.2 | +1.7 |
| both | straight | 40 | 100.0% | 0.0% | 12.4 | 0.074 | 1.5 | +0.9 |
| both | right | 40 | 95.0% | 2.5% | 11.3 | 0.082 | 2.1 | +0.6 |
| both | all | 120 | 95.0% | 1.7% | 14.3 | 0.075 | 1.8 | +1.1 |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 100.0% | 80.0% | 0.2% | 0.1% | 22.0% | 17.4% |
| both | straight | 100.0% | 100.0% | 0.4% | 0.0% | 17.4% | 20.2% |
| both | right | 95.0% | 95.0% | 0.1% | 0.1% | 18.1% | 20.7% |

Release (retract), episodes that succeeded (success only inside the task horizon; the simulation continues for the release window): complete = the follow-up window finished (or a fall ended it); rates over complete episodes. Inside at end = within tolerance at the end of the window; inside throughout = within tolerance at every step of it; displacement = object travel during it.

| arm mode | successes | complete | inside at end | inside throughout | object displacement, median m | heading change, median abs deg | falls in release |
|---|---|---|---|---|---|---|---|
| both | 114 | 114 | 94.7% | 94.7% | 0.003 | 0.1 | 0.0% |
