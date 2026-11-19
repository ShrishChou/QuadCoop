# Spot-arm turn pilot: sa-release-v2-s3-retract-20kg-1m

logs/marl2/sa_heavy_learned_s0/model_4000.pt, iteration 4000, mappo, arms learned. long 20 kg, 1 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

Walker: logs/rsl_rl/walker_spot_arm/2026-11-17_18-10-15_push_ft_s3_handload/model_2999.pt. Torso: default (interface False, expanded []). Arm-object collisions: on. Release: retract for 5 s.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 87.5% | 0.0% | 6.0 | 0.083 | 1.4 | +0.7 |
| both | straight | 40 | 95.0% | 0.0% | 3.6 | 0.068 | 1.9 | +0.8 |
| both | right | 40 | 87.5% | 0.0% | 3.9 | 0.080 | 1.7 | -0.3 |
| both | all | 120 | 90.0% | 0.0% | 3.8 | 0.075 | 1.6 | +0.4 |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 100.0% | 75.0% | 0.0% | 0.1% | 7.5% | 5.3% |
| both | straight | 100.0% | 90.0% | 0.2% | 0.0% | 8.1% | 6.8% |
| both | right | 100.0% | 75.0% | 0.0% | 0.0% | 6.5% | 7.7% |

Release (retract), episodes that succeeded (success only inside the task horizon; the simulation continues for the release window): complete = the follow-up window finished (or a fall ended it); rates over complete episodes. Inside at end = within tolerance at the end of the window; inside throughout = within tolerance at every step of it; displacement = object travel during it.

| arm mode | successes | complete | inside at end | inside throughout | object displacement, median m | heading change, median abs deg | falls in release |
|---|---|---|---|---|---|---|---|
| both | 108 | 108 | 80.6% | 80.6% | 0.011 | 0.6 | 0.0% |
