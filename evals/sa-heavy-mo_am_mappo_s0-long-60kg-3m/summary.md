# Spot-arm turn pilot: sa-heavy-mo_am_mappo_s0-long-60kg-3m

logs/marl2/mo_am_mappo_s0/model_4000.pt, iteration 4000, mappo, arms learned. long 60 kg, 3 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 0.0% | 0.0% | - | 1.576 | 9.7 | -2.3 |
| both | straight | 40 | 0.0% | 7.5% | - | 1.349 | 15.3 | -19.8 |
| both | right | 40 | 0.0% | 7.5% | - | 1.343 | 38.7 | -6.8 |
| both | all | 120 | 0.0% | 5.0% | - | 1.463 | 22.4 | -9.7 |
| none | left | 40 | 0.0% | 5.0% | - | 1.643 | 11.8 | +3.4 |
| none | straight | 40 | 2.5% | 17.5% | 14.8 | 1.332 | 10.2 | -14.6 |
| none | right | 40 | 0.0% | 2.5% | - | 1.400 | 41.2 | -2.1 |
| none | all | 120 | 0.8% | 8.3% | 14.8 | 1.544 | 17.5 | -4.4 |
| solo_1 | left | 40 | 0.0% | 2.5% | - | 2.612 | 48.5 | +9.5 |
| solo_1 | straight | 40 | 0.0% | 2.5% | - | 2.510 | 22.6 | +17.1 |
| solo_1 | right | 40 | 0.0% | 5.0% | - | 2.571 | 61.2 | -24.1 |
| solo_1 | all | 120 | 0.0% | 3.3% | - | 2.510 | 47.1 | +0.8 |
| solo_2 | left | 40 | 0.0% | 2.5% | - | 2.954 | 62.7 | +61.5 |
| solo_2 | straight | 40 | 0.0% | 17.5% | - | 2.946 | 5.8 | +2.3 |
| solo_2 | right | 40 | 0.0% | 2.5% | - | 2.945 | 61.7 | -58.4 |
| solo_2 | all | 120 | 0.0% | 7.5% | - | 2.946 | 54.9 | +1.8 |

Ablation, paired per task against both (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| none | +0.8 [+0.0, +2.5] pts | 0 | 1 | -2.0 [-6.2, +2.1] |
| solo_1 | +0.0 [+0.0, +0.0] pts | 0 | 0 | +13.2 [+7.0, +19.4] |
| solo_2 | +0.0 [+0.0, +0.0] pts | 0 | 0 | +16.3 [+10.7, +21.9] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 0.0% | 0.0% | 0.0% | 0.0% | 34.7% | 14.6% |
| both | straight | 0.0% | 0.0% | 0.0% | 0.0% | 34.9% | 6.0% |
| both | right | 0.0% | 0.0% | 0.0% | 0.1% | 33.0% | 6.2% |
| none | left | 0.0% | 0.0% | 0.0% | 0.3% | 37.5% | 2.1% |
| none | straight | 0.0% | 5.0% | 0.0% | 1.0% | 35.3% | 6.6% |
| none | right | 0.0% | 0.0% | 0.0% | 0.3% | 33.5% | 5.3% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.2% | 29.1% | 0.6% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 22.2% | 8.4% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 3.1% | 20.0% |
