# Spot-arm turn pilot: sa-team-sa_ippo_learned60_s0

logs/marl2/sa_ippo_learned60_s0/model_2000.pt, iteration 2000, ippo, arms learned. long 20 kg, 1 m, 20 placements per turn x swap, horizon 20 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 100.0% | 0.0% | 4.0 | 0.049 | 0.8 | -0.1 |
| both | straight | 40 | 100.0% | 0.0% | 3.9 | 0.056 | 1.3 | -1.2 |
| both | right | 40 | 100.0% | 0.0% | 4.5 | 0.075 | 1.9 | +1.1 |
| both | all | 120 | 100.0% | 0.0% | 4.3 | 0.066 | 1.1 | -0.1 |
| only_1 | left | 40 | 100.0% | 0.0% | 4.2 | 0.041 | 1.2 | +0.8 |
| only_1 | straight | 40 | 100.0% | 0.0% | 3.9 | 0.040 | 0.8 | +0.3 |
| only_1 | right | 40 | 100.0% | 0.0% | 4.4 | 0.072 | 0.7 | +0.5 |
| only_1 | all | 120 | 100.0% | 0.0% | 4.2 | 0.048 | 0.9 | +0.5 |
| only_2 | left | 40 | 100.0% | 0.0% | 4.3 | 0.057 | 1.0 | +0.6 |
| only_2 | straight | 40 | 100.0% | 0.0% | 4.0 | 0.061 | 1.0 | +0.0 |
| only_2 | right | 40 | 100.0% | 0.0% | 4.7 | 0.075 | 1.0 | +0.6 |
| only_2 | all | 120 | 100.0% | 0.0% | 4.3 | 0.067 | 1.0 | +0.4 |
| none | left | 40 | 97.5% | 0.0% | 4.3 | 0.060 | 2.1 | +1.6 |
| none | straight | 40 | 100.0% | 0.0% | 4.0 | 0.048 | 1.1 | +0.7 |
| none | right | 40 | 100.0% | 0.0% | 4.7 | 0.068 | 0.7 | +0.0 |
| none | all | 120 | 99.2% | 0.0% | 4.3 | 0.060 | 1.1 | +0.8 |
| solo_1 | left | 40 | 0.0% | 0.0% | - | 1.000 | 60.0 | +60.0 |
| solo_1 | straight | 40 | 0.0% | 2.5% | - | 0.960 | 2.4 | -3.0 |
| solo_1 | right | 40 | 0.0% | 0.0% | - | 0.606 | 79.5 | +0.1 |
| solo_1 | all | 120 | 0.0% | 0.8% | - | 0.960 | 60.0 | +19.0 |
| solo_2 | left | 40 | 0.0% | 0.0% | - | 1.127 | 85.3 | -75.3 |
| solo_2 | straight | 40 | 0.0% | 0.0% | - | 0.582 | 49.3 | +50.5 |
| solo_2 | right | 40 | 0.0% | 0.0% | - | 0.906 | 59.7 | -51.3 |
| solo_2 | all | 120 | 0.0% | 0.0% | - | 0.898 | 61.8 | -25.3 |

Ablation, paired per task against both (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| only_1 | +0.0 [+0.0, +0.0] pts | 0 | 0 | -0.3 [-0.6, -0.1] |
| only_2 | +0.0 [+0.0, +0.0] pts | 0 | 0 | -0.3 [-0.5, -0.0] |
| none | -0.8 [-2.5, +0.0] pts | 1 | 0 | -0.2 [-0.4, +0.1] |
| solo_1 | -100.0 [-100.0, -100.0] pts | 120 | 0 | +44.8 [+38.7, +50.5] |
| solo_2 | -100.0 [-100.0, -100.0] pts | 120 | 0 | +61.7 [+58.4, +65.1] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 100.0% | 100.0% | 0.5% | 0.2% | 17.9% | 15.5% |
| both | straight | 100.0% | 100.0% | 0.1% | 0.7% | 23.4% | 17.8% |
| both | right | 100.0% | 100.0% | 0.1% | 0.0% | 14.6% | 21.9% |
| only_1 | left | 100.0% | 100.0% | 0.2% | 0.3% | 14.3% | 17.4% |
| only_1 | straight | 100.0% | 100.0% | 0.0% | 0.8% | 26.3% | 20.5% |
| only_1 | right | 100.0% | 100.0% | 0.0% | 0.0% | 16.1% | 22.3% |
| only_2 | left | 100.0% | 100.0% | 0.4% | 0.0% | 11.3% | 17.0% |
| only_2 | straight | 100.0% | 100.0% | 0.1% | 0.0% | 25.9% | 20.1% |
| only_2 | right | 100.0% | 100.0% | 0.0% | 0.0% | 15.2% | 20.7% |
| none | left | 95.0% | 100.0% | 0.0% | 0.0% | 7.9% | 19.1% |
| none | straight | 100.0% | 100.0% | 0.0% | 0.0% | 27.1% | 21.8% |
| none | right | 100.0% | 100.0% | 0.0% | 0.0% | 16.4% | 21.4% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.2% | 0.0% | 0.0% | 0.0% |
| solo_1 | right | 0.0% | 0.0% | 0.1% | 0.0% | 2.0% | 0.2% |
| solo_2 | left | 0.0% | 0.0% | 0.5% | 0.4% | 3.6% | 4.5% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.1% | 0.1% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 4.3% | 22.3% |
