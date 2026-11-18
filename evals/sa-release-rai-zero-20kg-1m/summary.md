# Spot-arm turn pilot: sa-release-rai-zero-20kg-1m

logs/marl2/sa_heavy_learned_s0/model_4000.pt, iteration 4000, mappo, arms learned. long 20 kg, 1 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

Walker: RAI (spot_locomotion.onnx). Torso: default (interface False, expanded []). Arm-object collisions: on. Release: zero for 5 s.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 100.0% | 0.0% | 4.2 | 0.054 | 1.4 | +0.3 |
| both | straight | 40 | 100.0% | 0.0% | 4.1 | 0.060 | 1.0 | +0.5 |
| both | right | 40 | 95.0% | 0.0% | 4.3 | 0.056 | 1.3 | +0.2 |
| both | all | 120 | 98.3% | 0.0% | 4.2 | 0.057 | 1.2 | +0.3 |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 100.0% | 100.0% | 3.2% | 3.0% | 23.8% | 18.1% |
| both | straight | 100.0% | 100.0% | 0.0% | 0.1% | 19.6% | 16.8% |
| both | right | 95.0% | 95.0% | 0.0% | 0.0% | 21.8% | 34.1% |

Release (zero), episodes that succeeded: retained = still within tolerance at the end of the release; displacement = object travel during it.

| arm mode | successes | retained | object displacement, median m | heading change, median abs deg | falls in release |
|---|---|---|---|---|---|
| both | 118 | 93.2% | 0.010 | 0.3 | 0.0% |
