# Spot-arm turn pilot: sa-release-v2-s3-policy-40kg-2m

logs/marl2/sa_heavy_learned_s0/model_4000.pt, iteration 4000, mappo, arms learned. long 40 kg, 2 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

Walker: logs/rsl_rl/walker_spot_arm/2026-11-17_18-10-15_push_ft_s3_handload/model_2999.pt. Torso: default (interface False, expanded []). Arm-object collisions: on. Release: policy for 5 s.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 85.0% | 5.0% | 18.3 | 0.103 | 2.2 | +1.0 |
| both | straight | 40 | 97.5% | 5.0% | 14.4 | 0.095 | 2.0 | +0.5 |
| both | right | 40 | 97.5% | 2.5% | 12.8 | 0.108 | 1.8 | +0.0 |
| both | all | 120 | 93.3% | 4.2% | 15.5 | 0.098 | 1.9 | +0.5 |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 95.0% | 75.0% | 0.2% | 0.3% | 24.2% | 18.3% |
| both | straight | 100.0% | 95.0% | 0.2% | 0.5% | 19.9% | 25.0% |
| both | right | 95.0% | 100.0% | 0.2% | 0.4% | 24.5% | 26.2% |

Release (policy), episodes that succeeded (success only inside the task horizon; the simulation continues for the release window): complete = the follow-up window finished (or a fall ended it); rates over complete episodes. Inside at end = within tolerance at the end of the window; inside throughout = within tolerance at every step of it; displacement = object travel during it.

| arm mode | successes | complete | inside at end | inside throughout | object displacement, median m | heading change, median abs deg | falls in release |
|---|---|---|---|---|---|---|---|
| both | 112 | 112 | 52.7% | 27.7% | 0.092 | 1.8 | 1.8% |
