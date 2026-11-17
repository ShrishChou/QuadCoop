# Spot-arm turn pilot: sa-heavy-mo_am_mappo_s0-dumbbell-40kg-2m

logs/marl2/mo_am_mappo_s0/model_4000.pt, iteration 4000, mappo, arms learned. dumbbell 40 kg, 2 m, 6 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 12 | 0.0% | 8.3% | - | 0.895 | 12.0 | +18.8 |
| both | straight | 12 | 0.0% | 8.3% | - | 0.693 | 39.0 | -16.7 |
| both | right | 12 | 0.0% | 0.0% | - | 0.532 | 70.4 | -22.5 |
| both | all | 36 | 0.0% | 5.6% | - | 0.773 | 36.9 | -6.8 |
| none | left | 12 | 0.0% | 0.0% | - | 0.850 | 12.4 | +7.6 |
| none | straight | 12 | 0.0% | 8.3% | - | 0.878 | 41.6 | -2.1 |
| none | right | 12 | 0.0% | 0.0% | - | 0.988 | 74.9 | -19.8 |
| none | all | 36 | 0.0% | 2.8% | - | 0.860 | 34.1 | -4.7 |
| solo_1 | left | 12 | 0.0% | 0.0% | - | 2.000 | 61.5 | +24.8 |
| solo_1 | straight | 12 | 0.0% | 0.0% | - | 2.005 | 7.5 | +7.8 |
| solo_1 | right | 12 | 0.0% | 8.3% | - | 1.994 | 59.8 | -29.5 |
| solo_1 | all | 36 | 0.0% | 2.8% | - | 1.999 | 56.8 | +1.0 |
| solo_2 | left | 12 | 0.0% | 8.3% | - | 1.958 | 63.8 | +63.4 |
| solo_2 | straight | 12 | 0.0% | 8.3% | - | 1.752 | 13.0 | +5.5 |
| solo_2 | right | 12 | 0.0% | 8.3% | - | 1.902 | 58.3 | -38.5 |
| solo_2 | all | 36 | 0.0% | 8.3% | - | 1.814 | 58.5 | +10.1 |

Ablation, paired per task against both (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| none | +0.0 [+0.0, +0.0] pts | 0 | 0 | -0.2 [-8.7, +8.4] |
| solo_1 | +0.0 [+0.0, +0.0] pts | 0 | 0 | +7.6 [-3.9, +20.5] |
| solo_2 | +0.0 [+0.0, +0.0] pts | 0 | 0 | +7.2 [-5.9, +20.5] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 0.0% | 0.0% | 0.0% | 0.5% | 2.0% | 8.9% |
| both | straight | 0.0% | 0.0% | 0.0% | 1.3% | 3.8% | 12.0% |
| both | right | 0.0% | 0.0% | 0.0% | 0.0% | 6.1% | 21.9% |
| none | left | 0.0% | 0.0% | 0.0% | 0.0% | 2.4% | 4.8% |
| none | straight | 0.0% | 0.0% | 0.0% | 1.0% | 8.0% | 15.0% |
| none | right | 0.0% | 0.0% | 0.0% | 0.0% | 12.3% | 20.4% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 14.1% | 0.0% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 21.4% | 13.5% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 9.9% | 10.9% |
