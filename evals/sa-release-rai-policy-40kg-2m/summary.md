# Spot-arm turn pilot: sa-release-rai-policy-40kg-2m

logs/marl2/sa_heavy_learned_s0/model_4000.pt, iteration 4000, mappo, arms learned. long 40 kg, 2 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

Walker: RAI (spot_locomotion.onnx). Torso: default (interface False, expanded []). Arm-object collisions: on. Release: policy for 5 s.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 80.0% | 7.5% | 16.2 | 0.085 | 1.9 | +1.7 |
| both | straight | 40 | 82.5% | 0.0% | 14.2 | 0.114 | 2.3 | -0.3 |
| both | right | 40 | 55.0% | 0.0% | 19.7 | 0.165 | 2.3 | -2.0 |
| both | all | 120 | 72.5% | 2.5% | 15.9 | 0.114 | 2.2 | -0.2 |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 65.0% | 95.0% | 0.0% | 0.6% | 43.9% | 26.8% |
| both | straight | 80.0% | 85.0% | 0.1% | 0.2% | 42.2% | 46.1% |
| both | right | 55.0% | 55.0% | 0.2% | 0.2% | 34.3% | 45.9% |

Release (policy), episodes that succeeded: retained = still within tolerance at the end of the release; displacement = object travel during it.

| arm mode | successes | retained | object displacement, median m | heading change, median abs deg | falls in release |
|---|---|---|---|---|---|
| both | 87 | 49.4% | 0.112 | nan | 0.0% |
