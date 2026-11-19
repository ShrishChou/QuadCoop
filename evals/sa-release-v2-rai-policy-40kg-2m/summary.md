# Spot-arm turn pilot: sa-release-v2-rai-policy-40kg-2m

logs/marl2/sa_heavy_learned_s0/model_4000.pt, iteration 4000, mappo, arms learned. long 40 kg, 2 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

Walker: RAI (spot_locomotion.onnx). Torso: default (interface False, expanded []). Arm-object collisions: on. Release: policy for 5 s.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 72.5% | 12.5% | 19.0 | 0.101 | 2.2 | +2.7 |
| both | straight | 40 | 85.0% | 5.0% | 14.4 | 0.119 | 1.6 | -1.3 |
| both | right | 40 | 52.5% | 2.5% | 11.9 | 0.159 | 2.7 | -0.9 |
| both | all | 120 | 70.0% | 6.7% | 16.0 | 0.117 | 2.1 | +0.2 |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 50.0% | 95.0% | 0.0% | 0.7% | 41.7% | 26.7% |
| both | straight | 85.0% | 85.0% | 0.1% | 0.3% | 41.6% | 47.5% |
| both | right | 45.0% | 60.0% | 0.1% | 0.2% | 33.7% | 44.5% |

Release (policy), episodes that succeeded (success only inside the task horizon; the simulation continues for the release window): complete = the follow-up window finished (or a fall ended it); rates over complete episodes. Inside at end = within tolerance at the end of the window; inside throughout = within tolerance at every step of it; displacement = object travel during it.

| arm mode | successes | complete | inside at end | inside throughout | object displacement, median m | heading change, median abs deg | falls in release |
|---|---|---|---|---|---|---|---|
| both | 84 | 84 | 41.7% | 32.1% | 0.090 | 2.0 | 3.6% |
