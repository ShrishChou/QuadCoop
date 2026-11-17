# Spot-arm turn pilot: sa-heavy-mo_am_mappo_s0-l_shape-40kg-2m

logs/marl2/mo_am_mappo_s0/model_4000.pt, iteration 4000, mappo, arms learned. l_shape 40 kg, 2 m, 6 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 12 | 0.0% | 0.0% | - | 0.790 | 3.8 | -1.8 |
| both | straight | 12 | 0.0% | 0.0% | - | 0.911 | 34.1 | -35.8 |
| both | right | 12 | 0.0% | 0.0% | - | 0.924 | 74.9 | -64.7 |
| both | all | 36 | 0.0% | 0.0% | - | 0.903 | 26.7 | -34.1 |
| none | left | 12 | 0.0% | 0.0% | - | 0.827 | 2.9 | -2.2 |
| none | straight | 12 | 0.0% | 0.0% | - | 1.024 | 34.5 | -34.5 |
| none | right | 12 | 0.0% | 0.0% | - | 0.743 | 80.6 | -68.6 |
| none | all | 36 | 0.0% | 0.0% | - | 0.848 | 19.7 | -35.1 |
| solo_1 | left | 12 | 0.0% | 0.0% | - | 1.751 | 44.4 | -2.1 |
| solo_1 | straight | 12 | 0.0% | 0.0% | - | 1.817 | 58.2 | -42.0 |
| solo_1 | right | 12 | 0.0% | 0.0% | - | 1.862 | 116.5 | -24.1 |
| solo_1 | all | 36 | 0.0% | 0.0% | - | 1.758 | 65.8 | -22.7 |
| solo_2 | left | 12 | 0.0% | 0.0% | - | 1.787 | 66.4 | +63.1 |
| solo_2 | straight | 12 | 0.0% | 0.0% | - | 1.804 | 18.0 | +0.7 |
| solo_2 | right | 12 | 0.0% | 0.0% | - | 1.681 | 45.9 | -40.1 |
| solo_2 | all | 36 | 0.0% | 0.0% | - | 1.766 | 43.7 | +7.9 |

Ablation, paired per task against both (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| none | +0.0 [+0.0, +0.0] pts | 0 | 0 | +1.5 [-3.3, +6.9] |
| solo_1 | +0.0 [+0.0, +0.0] pts | 0 | 0 | +41.7 [+23.9, +59.9] |
| solo_2 | +0.0 [+0.0, +0.0] pts | 0 | 0 | +8.1 [-7.1, +23.4] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 0.0% | 0.0% | 0.0% | 0.0% | 1.5% | 20.6% |
| both | straight | 0.0% | 0.0% | 0.0% | 0.0% | 34.9% | 23.2% |
| both | right | 0.0% | 0.0% | 0.0% | 0.0% | 35.1% | 17.1% |
| none | left | 0.0% | 0.0% | 0.0% | 0.0% | 12.2% | 17.3% |
| none | straight | 0.0% | 0.0% | 0.0% | 0.0% | 36.6% | 5.0% |
| none | right | 0.0% | 0.0% | 0.0% | 0.0% | 36.3% | 3.6% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | left | 0.0% | 0.0% | 0.1% | 0.0% | 18.1% | 0.8% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 12.1% | 17.4% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 13.2% | 6.8% |
