# Spot-arm turn pilot: sa-heavy-mo_sa_mappo_s0-long-40kg-2m

logs/marl2/mo_sa_mappo_s0/model_4000.pt, iteration 4000, mappo, arms learned. long 40 kg, 2 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 0.0% | 7.5% | - | 0.922 | 40.9 | +33.9 |
| both | straight | 40 | 5.0% | 15.0% | 36.2 | 0.651 | 12.7 | +15.5 |
| both | right | 40 | 22.5% | 2.5% | 20.8 | 0.332 | 20.2 | +4.8 |
| both | all | 120 | 9.2% | 8.3% | 22.3 | 0.648 | 21.1 | +18.1 |
| only_1 | left | 40 | 0.0% | 2.5% | - | 0.949 | 45.0 | +40.6 |
| only_1 | straight | 40 | 0.0% | 2.5% | - | 0.402 | 14.3 | +12.0 |
| only_1 | right | 40 | 2.5% | 0.0% | 31.7 | 0.273 | 14.2 | +4.0 |
| only_1 | all | 120 | 0.8% | 1.7% | 31.7 | 0.387 | 20.7 | +18.9 |
| only_2 | left | 40 | 10.0% | 10.0% | 33.5 | 1.037 | 31.7 | +32.1 |
| only_2 | straight | 40 | 5.0% | 10.0% | 29.6 | 0.624 | 7.5 | -2.9 |
| only_2 | right | 40 | 12.5% | 0.0% | 26.5 | 0.599 | 14.8 | -4.3 |
| only_2 | all | 120 | 9.2% | 6.7% | 30.2 | 0.739 | 18.0 | +8.3 |
| none | left | 40 | 2.5% | 2.5% | 31.8 | 1.034 | 29.7 | +32.0 |
| none | straight | 40 | 0.0% | 0.0% | - | 0.381 | 4.0 | -3.1 |
| none | right | 40 | 7.5% | 0.0% | 12.0 | 0.391 | 17.0 | +0.3 |
| none | all | 120 | 3.3% | 0.8% | 19.4 | 0.451 | 12.6 | +9.8 |
| solo_1 | left | 40 | 0.0% | 70.0% | - | 2.000 | 60.0 | +59.9 |
| solo_1 | straight | 40 | 0.0% | 75.0% | - | 2.000 | 0.0 | -0.0 |
| solo_1 | right | 40 | 0.0% | 82.5% | - | 2.000 | 60.0 | -60.1 |
| solo_1 | all | 120 | 0.0% | 75.8% | - | 2.000 | 60.0 | -0.1 |
| solo_2 | left | 40 | 0.0% | 0.0% | - | 1.529 | 40.8 | +0.7 |
| solo_2 | straight | 40 | 0.0% | 2.5% | - | 1.761 | 9.9 | -3.1 |
| solo_2 | right | 40 | 0.0% | 0.0% | - | 1.839 | 54.3 | -48.1 |
| solo_2 | all | 120 | 0.0% | 0.8% | - | 1.755 | 33.6 | -16.8 |

Ablation, paired per task against both (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| only_1 | -8.3 [-14.2, -3.3] pts | 11 | 1 | +2.0 [-2.3, +6.4] |
| only_2 | +0.0 [-6.7, +6.7] pts | 8 | 8 | -3.5 [-8.3, +1.1] |
| none | -5.8 [-11.7, +0.0] pts | 10 | 3 | -4.8 [-9.6, -0.0] |
| solo_1 | -9.2 [-14.2, -4.2] pts | 11 | 0 | +14.2 [+8.4, +19.8] |
| solo_2 | -9.2 [-14.2, -4.2] pts | 11 | 0 | +8.1 [+2.8, +13.2] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 0.0% | 0.0% | 14.5% | 4.0% | 39.0% | 9.1% |
| both | straight | 5.0% | 5.0% | 15.0% | 3.3% | 46.3% | 10.0% |
| both | right | 45.0% | 0.0% | 3.6% | 7.7% | 38.2% | 32.2% |
| only_1 | left | 0.0% | 0.0% | 16.8% | 3.1% | 49.1% | 6.6% |
| only_1 | straight | 0.0% | 0.0% | 12.8% | 1.7% | 47.7% | 20.0% |
| only_1 | right | 0.0% | 5.0% | 5.4% | 4.2% | 34.2% | 35.6% |
| only_2 | left | 15.0% | 5.0% | 1.0% | 4.9% | 53.9% | 6.0% |
| only_2 | straight | 10.0% | 0.0% | 0.1% | 4.1% | 69.1% | 15.4% |
| only_2 | right | 20.0% | 5.0% | 0.8% | 1.4% | 56.0% | 31.3% |
| none | left | 0.0% | 5.0% | 0.0% | 0.0% | 59.6% | 5.8% |
| none | straight | 0.0% | 0.0% | 0.0% | 0.0% | 66.0% | 26.1% |
| none | right | 15.0% | 0.0% | 0.0% | 0.0% | 52.0% | 43.2% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.4% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 36.4% | 21.0% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 41.7% | 39.8% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 38.0% | 42.0% |
