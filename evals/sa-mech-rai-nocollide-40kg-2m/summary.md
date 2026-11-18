# Spot-arm turn pilot: sa-mech-rai-nocollide-40kg-2m

logs/marl2/sa_heavy_learned_s0/model_4000.pt, iteration 4000, mappo, arms learned. long 40 kg, 2 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

Walker: RAI (spot_locomotion.onnx). Torso: default (interface False, expanded []). Arm-object collisions: off. Release: none.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 82.5% | 5.0% | 17.7 | 0.084 | 1.7 | +2.7 |
| both | straight | 40 | 87.5% | 0.0% | 14.5 | 0.063 | 1.9 | -0.3 |
| both | right | 40 | 52.5% | 0.0% | 13.9 | 0.098 | 1.7 | -1.6 |
| both | all | 120 | 74.2% | 1.7% | 15.5 | 0.081 | 1.7 | +0.3 |
| only_1 | left | 40 | 40.0% | 5.0% | 25.7 | 0.242 | 2.2 | +8.8 |
| only_1 | straight | 40 | 45.0% | 0.0% | 17.9 | 0.206 | 1.8 | +0.1 |
| only_1 | right | 40 | 60.0% | 0.0% | 26.9 | 0.091 | 2.9 | -1.8 |
| only_1 | all | 120 | 48.3% | 1.7% | 21.3 | 0.105 | 2.2 | +2.4 |
| only_2 | left | 40 | 62.5% | 7.5% | 22.5 | 0.092 | 2.0 | +2.2 |
| only_2 | straight | 40 | 77.5% | 0.0% | 19.4 | 0.079 | 1.8 | -0.6 |
| only_2 | right | 40 | 55.0% | 2.5% | 22.8 | 0.091 | 1.5 | -1.6 |
| only_2 | all | 120 | 65.0% | 3.3% | 21.3 | 0.088 | 1.7 | -0.0 |

Ablation, paired per task against both (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| only_1 | -25.8 [-37.5, -14.2] pts | 44 | 13 | +3.3 [+0.8, +5.9] |
| only_2 | -9.2 [-19.2, +0.8] pts | 25 | 14 | +0.2 [-1.5, +1.7] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 65.0% | 100.0% | 0.0% | 0.0% | 46.2% | 24.2% |
| both | straight | 85.0% | 90.0% | 0.0% | 0.0% | 43.9% | 49.6% |
| both | right | 50.0% | 55.0% | 0.0% | 0.0% | 36.8% | 46.9% |
| only_1 | left | 30.0% | 50.0% | 0.0% | 0.0% | 51.4% | 49.3% |
| only_1 | straight | 35.0% | 55.0% | 0.0% | 0.0% | 39.3% | 54.6% |
| only_1 | right | 55.0% | 65.0% | 0.0% | 0.0% | 33.9% | 46.7% |
| only_2 | left | 45.0% | 80.0% | 0.0% | 0.0% | 43.1% | 21.4% |
| only_2 | straight | 65.0% | 90.0% | 0.0% | 0.0% | 40.1% | 48.3% |
| only_2 | right | 50.0% | 60.0% | 0.0% | 0.0% | 38.8% | 45.1% |
