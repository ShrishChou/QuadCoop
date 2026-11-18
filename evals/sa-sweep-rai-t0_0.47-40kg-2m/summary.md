# Spot-arm turn pilot: sa-sweep-rai-t0_0.47-40kg-2m

logs/marl2/sa_heavy_learned_s0/model_4000.pt, iteration 4000, mappo, arms learned. long 40 kg, 2 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

Walker: RAI (spot_locomotion.onnx). Torso: 0,0.47 (interface False, expanded []). Arm-object collisions: on. Release: policy for 5 s.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 85.0% | 5.0% | 18.7 | 0.102 | 2.1 | +1.9 |
| both | straight | 40 | 92.5% | 2.5% | 12.3 | 0.103 | 1.8 | -0.2 |
| both | right | 40 | 65.0% | 2.5% | 13.1 | 0.152 | 3.7 | -4.3 |
| both | all | 120 | 80.8% | 3.3% | 15.5 | 0.107 | 2.3 | -0.9 |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 70.0% | 100.0% | 0.5% | 0.8% | 40.0% | 26.5% |
| both | straight | 90.0% | 95.0% | 0.2% | 0.6% | 40.8% | 45.7% |
| both | right | 65.0% | 65.0% | 0.4% | 0.6% | 33.5% | 40.6% |

Release (policy), episodes that succeeded: retained = still within tolerance at the end of the release; displacement = object travel during it.

| arm mode | successes | retained | object displacement, median m | heading change, median abs deg | falls in release |
|---|---|---|---|---|---|
| both | 97 | 42.3% | 0.026 | 2.0 | 1.0% |
