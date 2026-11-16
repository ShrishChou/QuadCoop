# Spot-arm turn pilot: sa-heavy-mo_sa_mappo_s0-sphere-40kg-2m

logs/marl2/mo_sa_mappo_s0/model_4000.pt, iteration 4000, mappo, arms learned. sphere 40 kg, 2 m, 6 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +0.0 to +0.0 deg, straight +0.0 to +0.0 deg, right +0.0 to +0.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 12 | 91.7% | 8.3% | 7.6 | 0.078 | 0.0 | +0.0 |
| both | straight | 12 | 75.0% | 8.3% | 8.5 | 0.052 | 0.0 | +0.0 |
| both | right | 12 | 75.0% | 25.0% | 10.5 | 0.080 | 0.0 | +0.0 |
| both | all | 36 | 80.6% | 13.9% | 8.5 | 0.068 | 0.0 | +0.0 |
| only_1 | left | 12 | 83.3% | 16.7% | 8.6 | 0.082 | 0.0 | +0.0 |
| only_1 | straight | 12 | 83.3% | 16.7% | 10.0 | 0.077 | 0.0 | +0.0 |
| only_1 | right | 12 | 91.7% | 8.3% | 8.0 | 0.065 | 0.0 | +0.0 |
| only_1 | all | 36 | 86.1% | 13.9% | 8.8 | 0.077 | 0.0 | +0.0 |
| only_2 | left | 12 | 75.0% | 8.3% | 9.7 | 0.080 | 0.0 | +0.0 |
| only_2 | straight | 12 | 91.7% | 8.3% | 8.5 | 0.080 | 0.0 | +0.0 |
| only_2 | right | 12 | 66.7% | 0.0% | 9.0 | 0.096 | 0.0 | +0.0 |
| only_2 | all | 36 | 77.8% | 5.6% | 9.0 | 0.080 | 0.0 | +0.0 |
| none | left | 12 | 91.7% | 0.0% | 8.0 | 0.056 | 0.0 | +0.0 |
| none | straight | 12 | 75.0% | 0.0% | 9.3 | 0.091 | 0.0 | +0.0 |
| none | right | 12 | 66.7% | 0.0% | 7.9 | 0.098 | 0.0 | +0.0 |
| none | all | 36 | 77.8% | 0.0% | 8.6 | 0.083 | 0.0 | +0.0 |
| solo_1 | left | 12 | 0.0% | 83.3% | - | 2.000 | 0.0 | +0.0 |
| solo_1 | straight | 12 | 0.0% | 83.3% | - | 2.000 | 0.0 | +0.0 |
| solo_1 | right | 12 | 0.0% | 100.0% | - | 2.000 | 0.0 | +0.0 |
| solo_1 | all | 36 | 0.0% | 88.9% | - | 2.000 | 0.0 | +0.0 |
| solo_2 | left | 12 | 0.0% | 0.0% | - | 1.363 | 0.0 | +0.0 |
| solo_2 | straight | 12 | 0.0% | 0.0% | - | 1.279 | 0.0 | +0.0 |
| solo_2 | right | 12 | 0.0% | 0.0% | - | 1.389 | 0.0 | +0.0 |
| solo_2 | all | 36 | 0.0% | 0.0% | - | 1.338 | 0.0 | +0.0 |

Ablation, paired per task against both (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| only_1 | +5.6 [-13.9, +25.0] pts | 5 | 7 | +0.0 [+0.0, +0.0] |
| only_2 | -2.8 [-22.2, +16.7] pts | 7 | 6 | +0.0 [+0.0, +0.0] |
| none | -2.8 [-19.4, +13.9] pts | 5 | 4 | +0.0 [+0.0, +0.0] |
| solo_1 | -80.6 [-91.7, -66.7] pts | 29 | 0 | +0.0 [+0.0, +0.0] |
| solo_2 | -80.6 [-91.7, -66.7] pts | 29 | 0 | +0.0 [+0.0, +0.0] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 100.0% | 83.3% | 0.3% | 0.2% | 6.5% | 8.8% |
| both | straight | 66.7% | 83.3% | 1.0% | 0.6% | 6.8% | 8.0% |
| both | right | 66.7% | 83.3% | 0.5% | 0.5% | 5.4% | 8.5% |
| only_1 | left | 66.7% | 100.0% | 1.5% | 0.2% | 8.4% | 7.7% |
| only_1 | straight | 83.3% | 83.3% | 1.4% | 0.3% | 11.5% | 6.6% |
| only_1 | right | 83.3% | 100.0% | 1.5% | 0.3% | 7.4% | 7.5% |
| only_2 | left | 66.7% | 83.3% | 2.8% | 0.1% | 5.4% | 6.3% |
| only_2 | straight | 83.3% | 100.0% | 0.0% | 0.0% | 6.5% | 7.2% |
| only_2 | right | 33.3% | 100.0% | 0.0% | 0.2% | 2.7% | 5.6% |
| none | left | 83.3% | 100.0% | 0.0% | 0.0% | 8.3% | 6.5% |
| none | straight | 66.7% | 83.3% | 0.0% | 0.0% | 6.3% | 4.6% |
| none | right | 33.3% | 100.0% | 0.0% | 0.0% | 5.5% | 5.7% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.1% | 0.0% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.1% | 0.0% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 5.1% | 4.6% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 4.9% | 5.6% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 4.9% | 6.8% |
