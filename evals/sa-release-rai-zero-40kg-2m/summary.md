# Spot-arm turn pilot: sa-release-rai-zero-40kg-2m

logs/marl2/sa_heavy_learned_s0/model_4000.pt, iteration 4000, mappo, arms learned. long 40 kg, 2 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

Walker: RAI (spot_locomotion.onnx). Torso: default (interface False, expanded []). Arm-object collisions: on. Release: zero for 5 s.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 70.0% | 12.5% | 16.3 | 0.087 | 1.8 | +0.3 |
| both | straight | 40 | 82.5% | 0.0% | 13.6 | 0.065 | 1.6 | +0.9 |
| both | right | 40 | 55.0% | 0.0% | 18.7 | 0.096 | 1.9 | -1.3 |
| both | all | 120 | 69.2% | 4.2% | 15.6 | 0.082 | 1.8 | -0.1 |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 55.0% | 85.0% | 0.3% | 0.6% | 43.7% | 23.9% |
| both | straight | 90.0% | 75.0% | 0.1% | 0.2% | 40.7% | 47.6% |
| both | right | 50.0% | 60.0% | 0.0% | 0.3% | 31.8% | 42.4% |

Release (zero), episodes that succeeded: retained = still within tolerance at the end of the release; displacement = object travel during it.

| arm mode | successes | retained | object displacement, median m | heading change, median abs deg | falls in release |
|---|---|---|---|---|---|
| both | 83 | 88.0% | nan | nan | 1.2% |
