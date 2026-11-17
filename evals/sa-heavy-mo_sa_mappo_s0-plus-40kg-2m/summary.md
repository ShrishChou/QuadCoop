# Spot-arm turn pilot: sa-heavy-mo_sa_mappo_s0-plus-40kg-2m

logs/marl2/mo_sa_mappo_s0/model_4000.pt, iteration 4000, mappo, arms learned. plus 40 kg, 2 m, 6 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left -30.0 to -30.0 deg, straight +0.0 to +0.0 deg, right +30.0 to +30.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 12 | 0.0% | 0.0% | - | 0.579 | 10.3 | +2.6 |
| both | straight | 12 | 8.3% | 0.0% | 14.1 | 0.709 | 5.0 | -3.7 |
| both | right | 12 | 8.3% | 0.0% | 8.1 | 0.662 | 4.4 | -4.4 |
| both | all | 36 | 5.6% | 0.0% | 14.1 | 0.612 | 5.3 | -1.8 |
| only_1 | left | 12 | 8.3% | 16.7% | 9.9 | 0.748 | 6.5 | +3.3 |
| only_1 | straight | 12 | 8.3% | 8.3% | 17.5 | 0.640 | 4.9 | -3.5 |
| only_1 | right | 12 | 0.0% | 0.0% | - | 0.598 | 5.2 | -2.4 |
| only_1 | all | 36 | 5.6% | 8.3% | 17.5 | 0.644 | 5.4 | -0.9 |
| only_2 | left | 12 | 0.0% | 0.0% | - | 0.544 | 7.7 | +6.7 |
| only_2 | straight | 12 | 0.0% | 0.0% | - | 0.745 | 8.9 | +3.0 |
| only_2 | right | 12 | 0.0% | 0.0% | - | 0.882 | 7.1 | +0.4 |
| only_2 | all | 36 | 0.0% | 0.0% | - | 0.739 | 7.4 | +3.4 |
| none | left | 12 | 0.0% | 8.3% | - | 0.880 | 11.2 | +7.7 |
| none | straight | 12 | 8.3% | 0.0% | 11.2 | 0.758 | 6.3 | +0.6 |
| none | right | 12 | 0.0% | 8.3% | - | 0.813 | 15.4 | -1.1 |
| none | all | 36 | 2.8% | 5.6% | 11.2 | 0.787 | 8.8 | +2.4 |
| solo_1 | left | 12 | 0.0% | 91.7% | - | 2.000 | 30.0 | -29.2 |
| solo_1 | straight | 12 | 0.0% | 100.0% | - | 2.000 | 0.0 | +0.1 |
| solo_1 | right | 12 | 0.0% | 91.7% | - | 2.000 | 30.6 | +30.8 |
| solo_1 | all | 36 | 0.0% | 94.4% | - | 2.000 | 29.6 | +0.6 |
| solo_2 | left | 12 | 0.0% | 0.0% | - | 1.877 | 27.8 | -13.3 |
| solo_2 | straight | 12 | 0.0% | 0.0% | - | 1.736 | 22.4 | +4.5 |
| solo_2 | right | 12 | 0.0% | 0.0% | - | 1.871 | 25.4 | +9.0 |
| solo_2 | all | 36 | 0.0% | 0.0% | - | 1.779 | 22.4 | +0.1 |

Ablation, paired per task against both (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| only_1 | +0.0 [-11.1, +11.1] pts | 2 | 2 | -0.1 [-2.1, +2.2] |
| only_2 | -5.6 [-13.9, +0.0] pts | 2 | 0 | +2.1 [+0.2, +4.0] |
| none | -2.8 [-13.9, +5.6] pts | 2 | 1 | +4.2 [+1.3, +7.3] |
| solo_1 | -5.6 [-13.9, +0.0] pts | 2 | 0 | +13.3 [+8.6, +18.3] |
| solo_2 | -5.6 [-13.9, +0.0] pts | 2 | 0 | +11.5 [+7.1, +15.9] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 0.0% | 0.0% | 3.0% | 6.9% | 22.3% | 35.4% |
| both | straight | 16.7% | 0.0% | 2.8% | 3.5% | 29.8% | 21.1% |
| both | right | 16.7% | 0.0% | 9.0% | 1.9% | 38.4% | 12.9% |
| only_1 | left | 0.0% | 16.7% | 0.1% | 13.7% | 30.5% | 42.6% |
| only_1 | straight | 16.7% | 0.0% | 3.8% | 1.6% | 27.6% | 23.3% |
| only_1 | right | 0.0% | 0.0% | 14.6% | 1.3% | 26.6% | 19.6% |
| only_2 | left | 0.0% | 0.0% | 1.2% | 0.1% | 30.1% | 41.5% |
| only_2 | straight | 0.0% | 0.0% | 0.7% | 2.0% | 29.0% | 17.4% |
| only_2 | right | 0.0% | 0.0% | 2.2% | 1.5% | 40.2% | 13.8% |
| none | left | 0.0% | 0.0% | 0.0% | 0.9% | 26.0% | 63.9% |
| none | straight | 16.7% | 0.0% | 0.0% | 0.1% | 45.0% | 24.2% |
| none | right | 0.0% | 0.0% | 0.0% | 0.8% | 41.1% | 13.6% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 41.2% | 44.5% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 40.6% | 41.9% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 43.2% | 35.3% |
