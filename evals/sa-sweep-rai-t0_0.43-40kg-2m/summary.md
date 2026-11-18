# Spot-arm turn pilot: sa-sweep-rai-t0_0.43-40kg-2m

logs/marl2/sa_heavy_learned_s0/model_4000.pt, iteration 4000, mappo, arms learned. long 40 kg, 2 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

Walker: RAI (spot_locomotion.onnx). Torso: 0,0.43 (interface False, expanded []). Arm-object collisions: on. Release: policy for 5 s.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 82.5% | 0.0% | 15.7 | 0.103 | 2.0 | +1.5 |
| both | straight | 40 | 90.0% | 0.0% | 12.6 | 0.087 | 2.3 | -0.5 |
| both | right | 40 | 65.0% | 0.0% | 12.4 | 0.115 | 2.9 | -0.8 |
| both | all | 120 | 79.2% | 0.0% | 13.4 | 0.100 | 2.5 | +0.0 |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 65.0% | 100.0% | 0.5% | 1.8% | 37.3% | 26.3% |
| both | straight | 95.0% | 85.0% | 0.1% | 0.5% | 38.0% | 45.7% |
| both | right | 60.0% | 70.0% | 0.5% | 0.7% | 28.9% | 41.4% |

Release (policy), episodes that succeeded: retained = still within tolerance at the end of the release; displacement = object travel during it.

| arm mode | successes | retained | object displacement, median m | heading change, median abs deg | falls in release |
|---|---|---|---|---|---|
| both | 95 | 54.7% | 0.027 | nan | 0.0% |
