# Spot-arm turn pilot: sa-release-v2-rai-zero-40kg-2m

logs/marl2/sa_heavy_learned_s0/model_4000.pt, iteration 4000, mappo, arms learned. long 40 kg, 2 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

Walker: RAI (spot_locomotion.onnx). Torso: default (interface False, expanded []). Arm-object collisions: on. Release: zero for 5 s.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 72.5% | 10.0% | 20.4 | 0.074 | 1.2 | +0.1 |
| both | straight | 40 | 82.5% | 0.0% | 13.4 | 0.070 | 1.7 | +0.7 |
| both | right | 40 | 55.0% | 0.0% | 15.0 | 0.093 | 2.2 | -1.8 |
| both | all | 120 | 70.0% | 3.3% | 17.4 | 0.081 | 1.7 | -0.3 |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 55.0% | 90.0% | 0.0% | 0.3% | 42.5% | 24.2% |
| both | straight | 85.0% | 80.0% | 0.0% | 0.1% | 42.9% | 46.7% |
| both | right | 50.0% | 60.0% | 0.1% | 0.2% | 33.1% | 41.8% |

Release (zero), episodes that succeeded (success only inside the task horizon; the simulation continues for the release window): complete = the follow-up window finished (or a fall ended it); rates over complete episodes. Inside at end = within tolerance at the end of the window; inside throughout = within tolerance at every step of it; displacement = object travel during it.

| arm mode | successes | complete | inside at end | inside throughout | object displacement, median m | heading change, median abs deg | falls in release |
|---|---|---|---|---|---|---|---|
| both | 84 | 84 | 100.0% | 100.0% | 0.003 | 0.2 | 0.0% |
