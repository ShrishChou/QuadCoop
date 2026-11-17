# Spot-arm turn pilot: sa-heavy-mo_am_mappo_s0-t_shape-40kg-2m

logs/marl2/mo_am_mappo_s0/model_4000.pt, iteration 4000, mappo, arms learned. t_shape 40 kg, 2 m, 6 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 12 | 0.0% | 0.0% | - | 0.808 | 5.3 | -7.7 |
| both | straight | 12 | 0.0% | 0.0% | - | 0.858 | 27.3 | -23.7 |
| both | right | 12 | 0.0% | 0.0% | - | 1.002 | 31.4 | -40.6 |
| both | all | 36 | 0.0% | 0.0% | - | 0.874 | 15.7 | -24.0 |
| none | left | 12 | 0.0% | 0.0% | - | 0.790 | 2.5 | -0.7 |
| none | straight | 12 | 0.0% | 0.0% | - | 0.827 | 16.7 | -21.1 |
| none | right | 12 | 0.0% | 0.0% | - | 0.825 | 24.5 | -34.0 |
| none | all | 36 | 0.0% | 0.0% | - | 0.824 | 10.8 | -18.6 |
| solo_1 | left | 12 | 0.0% | 0.0% | - | 1.853 | 47.0 | +24.8 |
| solo_1 | straight | 12 | 0.0% | 0.0% | - | 1.921 | 33.3 | -41.0 |
| solo_1 | right | 12 | 0.0% | 0.0% | - | 1.882 | 106.0 | -100.8 |
| solo_1 | all | 36 | 0.0% | 0.0% | - | 1.882 | 52.2 | -39.0 |
| solo_2 | left | 12 | 0.0% | 8.3% | - | 1.870 | 72.0 | +84.1 |
| solo_2 | straight | 12 | 0.0% | 0.0% | - | 1.452 | 62.6 | +24.9 |
| solo_2 | right | 12 | 0.0% | 0.0% | - | 1.429 | 20.9 | -12.2 |
| solo_2 | all | 36 | 0.0% | 2.8% | - | 1.492 | 48.1 | +32.3 |

Ablation, paired per task against both (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| none | +0.0 [+0.0, +0.0] pts | 0 | 0 | -4.7 [-9.6, -0.1] |
| solo_1 | +0.0 [+0.0, +0.0] pts | 0 | 0 | +34.0 [+20.1, +49.1] |
| solo_2 | +0.0 [+0.0, +0.0] pts | 0 | 0 | +27.9 [+9.8, +46.5] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 0.0% | 0.0% | 0.0% | 0.1% | 1.0% | 27.2% |
| both | straight | 0.0% | 0.0% | 0.0% | 0.0% | 20.5% | 25.5% |
| both | right | 0.0% | 0.0% | 0.0% | 0.0% | 15.3% | 22.4% |
| none | left | 0.0% | 0.0% | 0.0% | 0.0% | 14.5% | 30.8% |
| none | straight | 0.0% | 0.0% | 0.0% | 0.0% | 30.6% | 16.6% |
| none | right | 0.0% | 0.0% | 0.0% | 0.0% | 24.4% | 22.4% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 12.0% | 0.5% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 2.1% | 38.9% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 1.1% | 2.3% |
