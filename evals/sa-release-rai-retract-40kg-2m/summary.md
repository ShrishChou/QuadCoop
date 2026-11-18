# Spot-arm turn pilot: sa-release-rai-retract-40kg-2m

logs/marl2/sa_heavy_learned_s0/model_4000.pt, iteration 4000, mappo, arms learned. long 40 kg, 2 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

Walker: RAI (spot_locomotion.onnx). Torso: default (interface False, expanded []). Arm-object collisions: on. Release: retract for 5 s.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 82.5% | 10.0% | 18.0 | 0.081 | 1.4 | +1.6 |
| both | straight | 40 | 85.0% | 0.0% | 14.5 | 0.067 | 1.8 | +0.4 |
| both | right | 40 | 55.0% | 0.0% | 18.1 | 0.097 | 1.4 | -0.8 |
| both | all | 120 | 74.2% | 3.3% | 16.5 | 0.081 | 1.4 | +0.4 |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 75.0% | 90.0% | 0.1% | 0.2% | 37.8% | 19.7% |
| both | straight | 85.0% | 85.0% | 0.0% | 0.1% | 36.5% | 40.0% |
| both | right | 50.0% | 60.0% | 0.0% | 0.3% | 31.0% | 41.2% |

Release (retract), episodes that succeeded: retained = still within tolerance at the end of the release; displacement = object travel during it.

| arm mode | successes | retained | object displacement, median m | heading change, median abs deg | falls in release |
|---|---|---|---|---|---|
| both | 89 | 92.1% | nan | nan | 0.0% |
