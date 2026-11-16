# Spot-arm turn pilot: sa-team-sa_mappo_learned60_s2

logs/marl2/sa_mappo_learned60_s2/model_2000.pt, iteration 2000, mappo, arms learned. long 20 kg, 1 m, 20 placements per turn x swap, horizon 20 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 92.5% | 0.0% | 3.9 | 0.065 | 1.3 | +0.5 |
| both | straight | 40 | 85.0% | 0.0% | 4.2 | 0.075 | 2.1 | -0.5 |
| both | right | 40 | 100.0% | 0.0% | 4.1 | 0.032 | 1.9 | +0.6 |
| both | all | 120 | 92.5% | 0.0% | 4.1 | 0.056 | 1.6 | +0.2 |
| only_1 | left | 40 | 100.0% | 0.0% | 4.1 | 0.043 | 1.2 | +0.7 |
| only_1 | straight | 40 | 100.0% | 0.0% | 4.0 | 0.053 | 1.2 | +0.0 |
| only_1 | right | 40 | 97.5% | 2.5% | 4.2 | 0.031 | 1.4 | -0.5 |
| only_1 | all | 120 | 99.2% | 0.8% | 4.1 | 0.041 | 1.2 | +0.1 |
| only_2 | left | 40 | 100.0% | 0.0% | 4.2 | 0.068 | 3.2 | +2.7 |
| only_2 | straight | 40 | 95.0% | 0.0% | 5.3 | 0.078 | 1.7 | +1.0 |
| only_2 | right | 40 | 97.5% | 0.0% | 4.7 | 0.049 | 2.1 | +1.6 |
| only_2 | all | 120 | 97.5% | 0.0% | 4.4 | 0.070 | 2.3 | +1.8 |
| none | left | 40 | 100.0% | 0.0% | 4.2 | 0.050 | 2.1 | +2.2 |
| none | straight | 40 | 100.0% | 0.0% | 4.1 | 0.067 | 2.0 | +1.1 |
| none | right | 40 | 100.0% | 0.0% | 4.6 | 0.059 | 1.5 | +0.9 |
| none | all | 120 | 100.0% | 0.0% | 4.2 | 0.060 | 1.7 | +1.4 |
| solo_1 | left | 40 | 0.0% | 0.0% | - | 0.746 | 62.8 | +39.0 |
| solo_1 | straight | 40 | 0.0% | 5.0% | - | 0.581 | 56.9 | -25.9 |
| solo_1 | right | 40 | 0.0% | 0.0% | - | 0.641 | 60.0 | +8.9 |
| solo_1 | all | 120 | 0.0% | 1.7% | - | 0.718 | 60.0 | +7.3 |
| solo_2 | left | 40 | 0.0% | 0.0% | - | 0.997 | 61.8 | +66.0 |
| solo_2 | straight | 40 | 0.0% | 0.0% | - | 1.000 | 4.0 | +6.0 |
| solo_2 | right | 40 | 0.0% | 0.0% | - | 0.997 | 59.6 | -49.4 |
| solo_2 | all | 120 | 0.0% | 0.0% | - | 0.997 | 59.6 | +7.5 |

Ablation, paired per task against both (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| only_1 | +6.7 [+1.7, +11.7] pts | 1 | 9 | -0.3 [-0.8, +0.2] |
| only_2 | +5.0 [+0.0, +10.8] pts | 3 | 9 | +0.4 [-0.0, +0.8] |
| none | +7.5 [+3.3, +12.5] pts | 0 | 9 | -0.0 [-0.4, +0.4] |
| solo_1 | -92.5 [-96.7, -87.5] pts | 111 | 0 | +52.5 [+48.5, +56.2] |
| solo_2 | -92.5 [-96.7, -87.5] pts | 111 | 0 | +38.5 [+33.5, +43.3] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 85.0% | 100.0% | 0.0% | 0.0% | 6.5% | 17.0% |
| both | straight | 75.0% | 95.0% | 0.1% | 0.0% | 19.4% | 16.7% |
| both | right | 100.0% | 100.0% | 0.0% | 0.0% | 2.1% | 23.1% |
| only_1 | left | 100.0% | 100.0% | 0.0% | 0.0% | 10.7% | 18.5% |
| only_1 | straight | 100.0% | 100.0% | 0.0% | 0.0% | 21.9% | 14.2% |
| only_1 | right | 100.0% | 95.0% | 0.0% | 0.0% | 2.8% | 21.1% |
| only_2 | left | 100.0% | 100.0% | 0.0% | 0.1% | 11.2% | 19.4% |
| only_2 | straight | 90.0% | 100.0% | 0.1% | 0.0% | 20.3% | 15.7% |
| only_2 | right | 100.0% | 95.0% | 0.0% | 0.0% | 3.7% | 25.9% |
| none | left | 100.0% | 100.0% | 0.0% | 0.0% | 12.9% | 20.1% |
| none | straight | 100.0% | 100.0% | 0.0% | 0.0% | 19.6% | 13.4% |
| none | right | 100.0% | 100.0% | 0.0% | 0.0% | 3.2% | 24.6% |
| solo_1 | left | 0.0% | 0.0% | 1.2% | 0.6% | 3.9% | 1.3% |
| solo_1 | straight | 0.0% | 0.0% | 0.9% | 0.0% | 1.3% | 1.1% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.4% | 0.3% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
