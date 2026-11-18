# Spot-arm turn pilot: smoke-mech-a

logs/marl2/sa_heavy_learned_s0/model_4000.pt, iteration 4000, mappo, arms learned. long 40 kg, 2 m, 2 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

Walker: RAI (spot_locomotion.onnx). Torso: default (interface False, expanded []). Arm-object collisions: on. Release: none.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 4 | 75.0% | 25.0% | 23.3 | 0.095 | 1.4 | +0.3 |
| both | straight | 4 | 75.0% | 0.0% | 24.2 | 0.089 | 2.6 | +2.1 |
| both | right | 4 | 50.0% | 0.0% | 26.9 | 0.282 | 2.3 | -2.7 |
| both | all | 12 | 66.7% | 8.3% | 24.2 | 0.090 | 1.6 | -0.1 |
| none | left | 4 | 50.0% | 0.0% | 39.7 | 0.099 | 1.3 | -1.5 |
| none | straight | 4 | 50.0% | 0.0% | 31.4 | 0.813 | 3.9 | -2.1 |
| none | right | 4 | 75.0% | 0.0% | 14.3 | 0.090 | 1.5 | -2.0 |
| none | all | 12 | 58.3% | 0.0% | 19.0 | 0.090 | 1.5 | -1.8 |

Ablation, paired per task against both (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| none | -8.3 [-50.0, +33.3] pts | 4 | 3 | +0.9 [-1.3, +3.7] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 50.0% | 100.0% | 0.0% | 0.1% | 43.4% | 24.2% |
| both | straight | 50.0% | 100.0% | 0.0% | 0.1% | 48.4% | 57.2% |
| both | right | 0.0% | 100.0% | 0.1% | 0.2% | 28.7% | 47.6% |
| none | left | 50.0% | 50.0% | 0.0% | 0.2% | 40.8% | 27.6% |
| none | straight | 50.0% | 50.0% | 0.0% | 0.0% | 45.8% | 61.8% |
| none | right | 50.0% | 100.0% | 0.0% | 0.0% | 29.7% | 44.1% |
