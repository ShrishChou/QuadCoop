# Spot-arm turn pilot: sa-sweep-rai-tdefault-40kg-2m

logs/marl2/sa_heavy_learned_s0/model_4000.pt, iteration 4000, mappo, arms learned. long 40 kg, 2 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

Walker: RAI (spot_locomotion.onnx). Torso: default (interface False, expanded []). Arm-object collisions: on. Release: policy for 5 s.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 67.5% | 15.0% | 17.1 | 0.098 | 2.0 | +2.3 |
| both | straight | 40 | 85.0% | 0.0% | 13.4 | 0.121 | 1.9 | -1.9 |
| both | right | 40 | 55.0% | 0.0% | 14.0 | 0.165 | 1.9 | -1.1 |
| both | all | 120 | 69.2% | 5.0% | 15.4 | 0.118 | 1.9 | -0.3 |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 50.0% | 85.0% | 0.1% | 0.5% | 44.6% | 26.4% |
| both | straight | 90.0% | 80.0% | 0.1% | 0.5% | 40.6% | 44.9% |
| both | right | 55.0% | 55.0% | 0.1% | 0.2% | 34.1% | 44.3% |

Release (policy), episodes that succeeded: retained = still within tolerance at the end of the release; displacement = object travel during it.

| arm mode | successes | retained | object displacement, median m | heading change, median abs deg | falls in release |
|---|---|---|---|---|---|
| both | 83 | 43.4% | 0.025 | nan | 1.2% |
