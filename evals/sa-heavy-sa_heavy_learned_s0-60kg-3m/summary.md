# Spot-arm turn pilot: sa-heavy-sa_heavy_learned_s0-60kg-3m

logs/marl2/sa_heavy_learned_s0/model_4000.pt, iteration 4000, mappo, arms learned. long 60 kg, 3 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 0.0% | 0.0% | - | 2.501 | 37.4 | +31.7 |
| both | straight | 40 | 0.0% | 0.0% | - | 2.503 | 11.4 | -16.7 |
| both | right | 40 | 0.0% | 0.0% | - | 2.497 | 64.8 | -30.0 |
| both | all | 120 | 0.0% | 0.0% | - | 2.497 | 39.0 | -5.0 |
| only_1 | left | 40 | 0.0% | 0.0% | - | 2.710 | 46.7 | +41.0 |
| only_1 | straight | 40 | 0.0% | 0.0% | - | 2.697 | 8.8 | -9.3 |
| only_1 | right | 40 | 0.0% | 0.0% | - | 2.525 | 58.8 | -33.9 |
| only_1 | all | 120 | 0.0% | 0.0% | - | 2.661 | 40.6 | -0.8 |
| only_2 | left | 40 | 0.0% | 0.0% | - | 2.593 | 28.6 | +29.1 |
| only_2 | straight | 40 | 0.0% | 0.0% | - | 2.473 | 16.2 | -17.3 |
| only_2 | right | 40 | 0.0% | 0.0% | - | 2.573 | 61.3 | -44.7 |
| only_2 | all | 120 | 0.0% | 0.0% | - | 2.559 | 35.6 | -11.0 |
| none | left | 40 | 0.0% | 0.0% | - | 2.686 | 48.7 | +41.5 |
| none | straight | 40 | 0.0% | 0.0% | - | 2.572 | 14.1 | -15.9 |
| none | right | 40 | 0.0% | 0.0% | - | 2.702 | 64.1 | -44.6 |
| none | all | 120 | 0.0% | 0.0% | - | 2.668 | 45.1 | -6.3 |
| solo_1 | left | 40 | 0.0% | 0.0% | - | 3.000 | 60.0 | +60.0 |
| solo_1 | straight | 40 | 0.0% | 0.0% | - | 3.000 | 0.0 | +0.0 |
| solo_1 | right | 40 | 0.0% | 0.0% | - | 3.000 | 60.0 | -60.0 |
| solo_1 | all | 120 | 0.0% | 0.0% | - | 3.000 | 60.0 | +0.0 |
| solo_2 | left | 40 | 0.0% | 0.0% | - | 3.000 | 61.6 | +62.1 |
| solo_2 | straight | 40 | 0.0% | 0.0% | - | 3.000 | 0.1 | +1.2 |
| solo_2 | right | 40 | 0.0% | 0.0% | - | 3.000 | 60.0 | -59.9 |
| solo_2 | all | 120 | 0.0% | 0.0% | - | 3.000 | 60.0 | +1.1 |

Ablation, paired per task against both (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| only_1 | +0.0 [+0.0, +0.0] pts | 0 | 0 | -1.9 [-5.6, +1.9] |
| only_2 | +0.0 [+0.0, +0.0] pts | 0 | 0 | -1.2 [-3.8, +1.4] |
| none | +0.0 [+0.0, +0.0] pts | 0 | 0 | +2.8 [-0.3, +6.1] |
| solo_1 | +0.0 [+0.0, +0.0] pts | 0 | 0 | +2.3 [-1.8, +6.6] |
| solo_2 | +0.0 [+0.0, +0.0] pts | 0 | 0 | +3.4 [-0.9, +7.9] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 0.0% | 0.0% | 0.0% | 0.0% | 85.1% | 57.0% |
| both | straight | 0.0% | 0.0% | 0.0% | 0.0% | 72.5% | 70.0% |
| both | right | 0.0% | 0.0% | 0.0% | 0.0% | 84.5% | 81.2% |
| only_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 50.6% | 87.9% |
| only_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 55.2% | 63.2% |
| only_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 80.0% | 79.9% |
| only_2 | left | 0.0% | 0.0% | 0.0% | 0.2% | 84.4% | 53.8% |
| only_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 70.6% | 73.0% |
| only_2 | right | 0.0% | 0.0% | 0.0% | 0.1% | 86.0% | 84.4% |
| none | left | 0.0% | 0.0% | 0.0% | 0.0% | 54.0% | 86.6% |
| none | straight | 0.0% | 0.0% | 0.0% | 0.0% | 52.8% | 75.2% |
| none | right | 0.0% | 0.0% | 0.0% | 0.0% | 84.5% | 84.5% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 7.6% | 0.0% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 1.5% | 0.0% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.6% | 0.0% |
