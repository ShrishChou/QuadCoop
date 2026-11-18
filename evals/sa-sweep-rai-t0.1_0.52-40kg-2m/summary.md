# Spot-arm turn pilot: sa-sweep-rai-t0.1_0.52-40kg-2m

logs/marl2/sa_heavy_learned_s0/model_4000.pt, iteration 4000, mappo, arms learned. long 40 kg, 2 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

Walker: RAI (spot_locomotion.onnx). Torso: 0.1,0.52 (interface False, expanded []). Arm-object collisions: on. Release: policy for 5 s.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 52.5% | 7.5% | 22.6 | 0.132 | 2.5 | +4.3 |
| both | straight | 40 | 70.0% | 0.0% | 14.9 | 0.138 | 2.8 | -1.4 |
| both | right | 40 | 42.5% | 0.0% | 13.2 | 0.253 | 1.8 | -1.8 |
| both | all | 120 | 55.0% | 2.5% | 16.7 | 0.145 | 2.3 | +0.4 |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 40.0% | 65.0% | 0.2% | 1.1% | 47.5% | 27.6% |
| both | straight | 70.0% | 70.0% | 0.1% | 0.4% | 45.5% | 48.7% |
| both | right | 40.0% | 45.0% | 0.2% | 0.8% | 38.8% | 42.2% |

Release (policy), episodes that succeeded: retained = still within tolerance at the end of the release; displacement = object travel during it.

| arm mode | successes | retained | object displacement, median m | heading change, median abs deg | falls in release |
|---|---|---|---|---|---|
| both | 66 | 36.4% | 0.026 | 0.0 | 0.0% |
