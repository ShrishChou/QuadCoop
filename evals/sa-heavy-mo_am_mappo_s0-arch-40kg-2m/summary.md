# Spot-arm turn pilot: sa-heavy-mo_am_mappo_s0-arch-40kg-2m

logs/marl2/mo_am_mappo_s0/model_4000.pt, iteration 4000, mappo, arms learned. arch 40 kg, 2 m, 6 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 12 | 0.0% | 0.0% | - | 0.447 | 16.3 | +7.6 |
| both | straight | 12 | 0.0% | 0.0% | - | 0.460 | 39.9 | +18.7 |
| both | right | 12 | 0.0% | 0.0% | - | 0.789 | 54.2 | +37.6 |
| both | all | 36 | 0.0% | 0.0% | - | 0.454 | 19.0 | +21.3 |
| none | left | 12 | 0.0% | 0.0% | - | 0.759 | 14.7 | +2.1 |
| none | straight | 12 | 0.0% | 16.7% | - | 0.580 | 10.3 | +13.6 |
| none | right | 12 | 0.0% | 0.0% | - | 0.627 | 46.9 | +8.6 |
| none | all | 36 | 0.0% | 5.6% | - | 0.580 | 17.3 | +8.1 |
| solo_1 | left | 12 | 0.0% | 0.0% | - | 2.076 | 67.3 | +54.0 |
| solo_1 | straight | 12 | 0.0% | 8.3% | - | 2.000 | 1.7 | +5.0 |
| solo_1 | right | 12 | 0.0% | 0.0% | - | 1.999 | 60.0 | -42.9 |
| solo_1 | all | 36 | 0.0% | 2.8% | - | 2.000 | 59.7 | +5.4 |
| solo_2 | left | 12 | 0.0% | 8.3% | - | 1.869 | 65.4 | +64.5 |
| solo_2 | straight | 12 | 0.0% | 0.0% | - | 1.843 | 10.3 | -0.3 |
| solo_2 | right | 12 | 0.0% | 0.0% | - | 1.876 | 52.6 | -34.2 |
| solo_2 | all | 36 | 0.0% | 2.8% | - | 1.864 | 52.2 | +10.0 |

Ablation, paired per task against both (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| none | +0.0 [+0.0, +0.0] pts | 0 | 0 | +1.1 [-7.1, +10.4] |
| solo_1 | +0.0 [+0.0, +0.0] pts | 0 | 0 | +16.2 [+4.0, +28.6] |
| solo_2 | +0.0 [+0.0, +0.0] pts | 0 | 0 | +17.1 [+4.9, +29.2] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 0.0% | 0.0% | 2.3% | 6.2% | 6.6% | 7.3% |
| both | straight | 0.0% | 0.0% | 2.9% | 2.0% | 17.7% | 2.3% |
| both | right | 0.0% | 0.0% | 1.7% | 3.0% | 9.9% | 6.4% |
| none | left | 0.0% | 0.0% | 45.8% | 30.8% | 1.7% | 0.9% |
| none | straight | 0.0% | 0.0% | 31.1% | 21.2% | 3.6% | 1.6% |
| none | right | 0.0% | 0.0% | 41.2% | 38.7% | 6.8% | 18.8% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | left | 0.0% | 0.0% | 30.4% | 8.7% | 16.4% | 4.7% |
| solo_2 | straight | 0.0% | 0.0% | 31.1% | 8.5% | 24.8% | 11.5% |
| solo_2 | right | 0.0% | 0.0% | 34.0% | 7.8% | 12.1% | 12.8% |
