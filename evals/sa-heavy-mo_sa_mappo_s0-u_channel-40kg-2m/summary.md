# Spot-arm turn pilot: sa-heavy-mo_sa_mappo_s0-u_channel-40kg-2m

logs/marl2/mo_sa_mappo_s0/model_4000.pt, iteration 4000, mappo, arms learned. u_channel 40 kg, 2 m, 6 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 12 | 0.0% | 16.7% | - | 0.857 | 31.5 | +29.8 |
| both | straight | 12 | 0.0% | 0.0% | - | 0.472 | 35.9 | -27.0 |
| both | right | 12 | 0.0% | 16.7% | - | 0.293 | 64.9 | -53.6 |
| both | all | 36 | 0.0% | 11.1% | - | 0.600 | 38.1 | -16.9 |
| only_1 | left | 12 | 0.0% | 8.3% | - | 0.613 | 21.4 | +21.5 |
| only_1 | straight | 12 | 0.0% | 0.0% | - | 0.204 | 28.6 | -16.7 |
| only_1 | right | 12 | 0.0% | 0.0% | - | 0.251 | 26.4 | -13.1 |
| only_1 | all | 36 | 0.0% | 2.8% | - | 0.410 | 26.4 | -2.8 |
| only_2 | left | 12 | 0.0% | 25.0% | - | 0.480 | 18.5 | +18.9 |
| only_2 | straight | 12 | 0.0% | 0.0% | - | 0.440 | 29.3 | -26.8 |
| only_2 | right | 12 | 0.0% | 0.0% | - | 0.396 | 53.1 | -49.0 |
| only_2 | all | 36 | 0.0% | 8.3% | - | 0.440 | 35.0 | -19.0 |
| none | left | 12 | 0.0% | 0.0% | - | 0.576 | 13.7 | +12.0 |
| none | straight | 12 | 0.0% | 0.0% | - | 0.533 | 20.8 | -17.0 |
| none | right | 12 | 0.0% | 0.0% | - | 0.265 | 33.3 | -27.6 |
| none | all | 36 | 0.0% | 0.0% | - | 0.316 | 18.4 | -10.8 |
| solo_1 | left | 12 | 0.0% | 100.0% | - | 2.000 | 60.0 | +60.0 |
| solo_1 | straight | 12 | 0.0% | 83.3% | - | 2.000 | 0.0 | +0.0 |
| solo_1 | right | 12 | 0.0% | 83.3% | - | 2.000 | 60.0 | -60.2 |
| solo_1 | all | 36 | 0.0% | 88.9% | - | 2.000 | 60.0 | -0.1 |
| solo_2 | left | 12 | 0.0% | 0.0% | - | 1.736 | 60.4 | +52.7 |
| solo_2 | straight | 12 | 0.0% | 0.0% | - | 1.890 | 6.2 | -7.1 |
| solo_2 | right | 12 | 0.0% | 0.0% | - | 1.868 | 60.9 | -59.9 |
| solo_2 | all | 36 | 0.0% | 0.0% | - | 1.845 | 54.3 | -4.8 |

Ablation, paired per task against both (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| only_1 | +0.0 [+0.0, +0.0] pts | 0 | 0 | -14.8 [-21.6, -7.9] |
| only_2 | +0.0 [+0.0, +0.0] pts | 0 | 0 | -5.7 [-11.5, +0.0] |
| none | +0.0 [+0.0, +0.0] pts | 0 | 0 | -17.1 [-24.4, -9.4] |
| solo_1 | +0.0 [+0.0, +0.0] pts | 0 | 0 | +1.2 [-8.5, +11.7] |
| solo_2 | +0.0 [+0.0, +0.0] pts | 0 | 0 | +3.9 [-4.7, +13.5] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 0.0% | 0.0% | 5.6% | 3.7% | 35.2% | 3.9% |
| both | straight | 0.0% | 0.0% | 6.2% | 7.7% | 41.1% | 10.5% |
| both | right | 0.0% | 0.0% | 9.2% | 6.5% | 41.5% | 28.1% |
| only_1 | left | 0.0% | 0.0% | 5.0% | 1.2% | 32.4% | 5.5% |
| only_1 | straight | 0.0% | 0.0% | 3.5% | 2.1% | 36.5% | 17.1% |
| only_1 | right | 0.0% | 0.0% | 5.5% | 1.2% | 37.1% | 19.6% |
| only_2 | left | 0.0% | 0.0% | 1.2% | 6.9% | 43.2% | 10.5% |
| only_2 | straight | 0.0% | 0.0% | 1.6% | 10.7% | 45.2% | 14.3% |
| only_2 | right | 0.0% | 0.0% | 1.4% | 9.0% | 37.8% | 17.2% |
| none | left | 0.0% | 0.0% | 0.0% | 0.0% | 53.8% | 14.6% |
| none | straight | 0.0% | 0.0% | 0.0% | 0.0% | 49.2% | 24.8% |
| none | right | 0.0% | 0.0% | 0.0% | 0.0% | 49.8% | 29.4% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.1% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 40.9% | 39.2% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 37.9% | 40.4% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 39.1% | 39.9% |
