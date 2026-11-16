# Spot-arm turn pilot: sa-hand-sa_mappo_learned60_s0

logs/marl2/sa_mappo_learned60_s0/model_2000.pt, iteration 2000, mappo, arms learned. long 20 kg, 1 m, 20 placements per turn x swap, horizon 20 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 100.0% | 0.0% | 4.2 | 0.056 | 1.4 | -0.6 |
| both | straight | 40 | 100.0% | 0.0% | 3.9 | 0.044 | 0.8 | -0.8 |
| both | right | 40 | 95.0% | 0.0% | 4.1 | 0.056 | 3.1 | -1.7 |
| both | all | 120 | 98.3% | 0.0% | 4.0 | 0.052 | 1.5 | -1.0 |
| only_1 | left | 40 | 100.0% | 0.0% | 4.3 | 0.062 | 1.7 | -0.3 |
| only_1 | straight | 40 | 100.0% | 0.0% | 4.0 | 0.053 | 1.6 | -0.7 |
| only_1 | right | 40 | 95.0% | 0.0% | 5.2 | 0.062 | 2.1 | -0.9 |
| only_1 | all | 120 | 98.3% | 0.0% | 4.3 | 0.056 | 1.7 | -0.6 |
| only_2 | left | 40 | 97.5% | 0.0% | 5.1 | 0.068 | 1.3 | +1.0 |
| only_2 | straight | 40 | 100.0% | 0.0% | 4.3 | 0.070 | 0.7 | -0.4 |
| only_2 | right | 40 | 100.0% | 0.0% | 4.2 | 0.055 | 1.7 | -0.4 |
| only_2 | all | 120 | 99.2% | 0.0% | 4.3 | 0.061 | 1.2 | +0.1 |
| none | left | 40 | 97.5% | 2.5% | 4.6 | 0.062 | 1.4 | +2.2 |
| none | straight | 40 | 100.0% | 0.0% | 4.9 | 0.059 | 1.8 | -1.3 |
| none | right | 40 | 97.5% | 0.0% | 5.0 | 0.045 | 2.7 | -0.9 |
| none | all | 120 | 98.3% | 0.8% | 4.8 | 0.056 | 1.8 | -0.0 |

Arm ablation, paired per task against both arms active (the same policy; a locked arm stays stowed):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| only_1 | +0.0 [-3.3, +3.3] pts | 2 | 2 | -0.3 [-1.3, +0.4] |
| only_2 | +0.8 [-1.7, +3.3] pts | 1 | 2 | -0.7 [-1.7, -0.1] |
| none | +0.0 [-3.3, +3.3] pts | 2 | 2 | +0.1 [-1.0, +1.2] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 100.0% | 100.0% | 0.1% | 0.8% | 30.1% | 15.1% |
| both | straight | 100.0% | 100.0% | 0.1% | 5.6% | 20.6% | 15.0% |
| both | right | 90.0% | 100.0% | 0.1% | 0.7% | 11.6% | 25.4% |
| only_1 | left | 100.0% | 100.0% | 0.0% | 0.0% | 32.3% | 19.5% |
| only_1 | straight | 100.0% | 100.0% | 0.0% | 0.0% | 26.4% | 16.4% |
| only_1 | right | 90.0% | 100.0% | 0.0% | 0.0% | 17.6% | 32.6% |
| only_2 | left | 95.0% | 100.0% | 0.1% | 1.3% | 27.3% | 19.5% |
| only_2 | straight | 100.0% | 100.0% | 0.0% | 5.8% | 18.8% | 13.2% |
| only_2 | right | 100.0% | 100.0% | 0.0% | 0.6% | 12.7% | 28.6% |
| none | left | 95.0% | 100.0% | 0.0% | 0.0% | 31.9% | 22.8% |
| none | straight | 100.0% | 100.0% | 0.0% | 0.0% | 19.8% | 14.2% |
| none | right | 100.0% | 95.0% | 0.0% | 0.0% | 18.7% | 33.4% |
