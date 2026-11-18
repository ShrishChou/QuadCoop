# Spot-arm turn pilot: sa-release-rai-retract-20kg-1m

logs/marl2/sa_heavy_learned_s0/model_4000.pt, iteration 4000, mappo, arms learned. long 20 kg, 1 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

Walker: RAI (spot_locomotion.onnx). Torso: default (interface False, expanded []). Arm-object collisions: on. Release: retract for 5 s.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 100.0% | 0.0% | 4.2 | 0.049 | 1.1 | +0.0 |
| both | straight | 40 | 100.0% | 0.0% | 4.2 | 0.064 | 1.3 | -0.1 |
| both | right | 40 | 100.0% | 0.0% | 4.3 | 0.054 | 1.5 | +0.3 |
| both | all | 120 | 100.0% | 0.0% | 4.2 | 0.055 | 1.3 | +0.1 |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 100.0% | 100.0% | 0.4% | 0.6% | 10.3% | 11.4% |
| both | straight | 100.0% | 100.0% | 0.0% | 0.0% | 12.7% | 11.2% |
| both | right | 100.0% | 100.0% | 0.0% | 0.0% | 10.0% | 14.9% |

Release (retract), episodes that succeeded: retained = still within tolerance at the end of the release; displacement = object travel during it.

| arm mode | successes | retained | object displacement, median m | heading change, median abs deg | falls in release |
|---|---|---|---|---|---|
| both | 120 | 91.7% | 0.009 | 0.2 | 0.0% |
