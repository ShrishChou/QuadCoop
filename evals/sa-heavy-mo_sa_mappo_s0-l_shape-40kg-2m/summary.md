# Spot-arm turn pilot: sa-heavy-mo_sa_mappo_s0-l_shape-40kg-2m

logs/marl2/mo_sa_mappo_s0/model_4000.pt, iteration 4000, mappo, arms learned. l_shape 40 kg, 2 m, 6 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 12 | 25.0% | 8.3% | 36.9 | 0.327 | 5.5 | +1.3 |
| both | straight | 12 | 0.0% | 41.7% | - | 0.368 | 26.1 | +2.6 |
| both | right | 12 | 0.0% | 0.0% | - | 0.307 | 26.1 | +20.2 |
| both | all | 36 | 8.3% | 16.7% | 36.9 | 0.307 | 12.8 | +8.0 |
| only_1 | left | 12 | 8.3% | 0.0% | 36.4 | 0.145 | 17.1 | +18.1 |
| only_1 | straight | 12 | 16.7% | 0.0% | 31.7 | 0.116 | 24.4 | +20.4 |
| only_1 | right | 12 | 8.3% | 8.3% | 33.8 | 0.333 | 25.1 | -9.0 |
| only_1 | all | 36 | 11.1% | 2.8% | 33.8 | 0.147 | 17.1 | +9.9 |
| only_2 | left | 12 | 0.0% | 0.0% | - | 0.465 | 12.9 | +14.8 |
| only_2 | straight | 12 | 8.3% | 0.0% | 35.7 | 0.257 | 20.0 | -8.8 |
| only_2 | right | 12 | 33.3% | 0.0% | 31.0 | 0.237 | 16.8 | -4.9 |
| only_2 | all | 36 | 13.9% | 0.0% | 31.0 | 0.257 | 12.9 | +0.4 |
| none | left | 12 | 0.0% | 0.0% | - | 0.214 | 10.3 | +7.4 |
| none | straight | 12 | 8.3% | 0.0% | 30.5 | 0.171 | 15.0 | -3.4 |
| none | right | 12 | 0.0% | 0.0% | - | 0.308 | 17.7 | -6.4 |
| none | all | 36 | 2.8% | 0.0% | 30.5 | 0.218 | 14.7 | -0.8 |
| solo_1 | left | 12 | 0.0% | 91.7% | - | 2.000 | 60.0 | +60.0 |
| solo_1 | straight | 12 | 0.0% | 66.7% | - | 2.000 | 0.0 | +0.0 |
| solo_1 | right | 12 | 0.0% | 75.0% | - | 2.000 | 60.0 | -60.1 |
| solo_1 | all | 36 | 0.0% | 77.8% | - | 2.000 | 60.0 | -0.0 |
| solo_2 | left | 12 | 0.0% | 0.0% | - | 1.904 | 60.0 | +7.0 |
| solo_2 | straight | 12 | 0.0% | 0.0% | - | 1.739 | 35.9 | -36.3 |
| solo_2 | right | 12 | 0.0% | 0.0% | - | 1.911 | 70.0 | -69.1 |
| solo_2 | all | 36 | 0.0% | 0.0% | - | 1.826 | 60.0 | -32.8 |

Ablation, paired per task against both (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| only_1 | +2.8 [-11.1, +16.7] pts | 3 | 4 | +7.7 [-3.0, +19.2] |
| only_2 | +5.6 [-8.3, +19.4] pts | 3 | 5 | -1.8 [-10.4, +6.4] |
| none | -5.6 [-16.7, +2.8] pts | 3 | 1 | -2.9 [-10.3, +5.2] |
| solo_1 | -8.3 [-19.4, +0.0] pts | 3 | 0 | +21.0 [+9.9, +32.6] |
| solo_2 | -8.3 [-19.4, +0.0] pts | 3 | 0 | +35.3 [+22.7, +47.9] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 50.0% | 0.0% | 9.3% | 5.7% | 37.9% | 20.6% |
| both | straight | 0.0% | 0.0% | 9.0% | 3.2% | 37.5% | 24.2% |
| both | right | 0.0% | 0.0% | 4.4% | 1.3% | 44.2% | 28.4% |
| only_1 | left | 16.7% | 0.0% | 7.4% | 0.8% | 29.1% | 13.7% |
| only_1 | straight | 33.3% | 0.0% | 5.6% | 0.9% | 33.8% | 20.4% |
| only_1 | right | 0.0% | 16.7% | 5.5% | 0.6% | 39.5% | 20.3% |
| only_2 | left | 0.0% | 0.0% | 0.7% | 3.9% | 44.9% | 13.8% |
| only_2 | straight | 16.7% | 0.0% | 0.3% | 3.0% | 50.7% | 24.0% |
| only_2 | right | 0.0% | 66.7% | 0.5% | 1.9% | 40.5% | 28.8% |
| none | left | 0.0% | 0.0% | 0.0% | 0.0% | 44.6% | 18.6% |
| none | straight | 0.0% | 16.7% | 0.0% | 0.0% | 51.3% | 21.8% |
| none | right | 0.0% | 0.0% | 0.0% | 0.0% | 40.1% | 26.3% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 40.6% | 11.3% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 37.6% | 20.3% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 9.4% | 35.9% |
