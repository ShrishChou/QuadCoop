# Spot-arm turn pilot: sa-heavy-mo_sa_mappo_s0-arch-40kg-2m

logs/marl2/mo_sa_mappo_s0/model_4000.pt, iteration 4000, mappo, arms learned. arch 40 kg, 2 m, 6 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 12 | 0.0% | 0.0% | - | 0.186 | 65.0 | +12.2 |
| both | straight | 12 | 0.0% | 0.0% | - | 0.253 | 58.4 | +22.9 |
| both | right | 12 | 0.0% | 0.0% | - | 0.797 | 63.9 | -57.5 |
| both | all | 36 | 0.0% | 0.0% | - | 0.253 | 62.2 | -7.5 |
| only_1 | left | 12 | 0.0% | 0.0% | - | 0.639 | 72.1 | -13.9 |
| only_1 | straight | 12 | 0.0% | 8.3% | - | 0.403 | 27.4 | +0.5 |
| only_1 | right | 12 | 0.0% | 0.0% | - | 0.702 | 70.3 | -32.2 |
| only_1 | all | 36 | 0.0% | 2.8% | - | 0.473 | 40.2 | -15.2 |
| only_2 | left | 12 | 0.0% | 0.0% | - | 0.909 | 50.1 | -2.1 |
| only_2 | straight | 12 | 0.0% | 0.0% | - | 0.991 | 13.9 | -0.1 |
| only_2 | right | 12 | 0.0% | 0.0% | - | 0.941 | 56.8 | -43.7 |
| only_2 | all | 36 | 0.0% | 0.0% | - | 0.941 | 38.9 | -15.3 |
| none | left | 12 | 0.0% | 0.0% | - | 1.314 | 53.4 | +30.0 |
| none | straight | 12 | 0.0% | 0.0% | - | 0.861 | 10.4 | -2.2 |
| none | right | 12 | 0.0% | 0.0% | - | 1.088 | 61.9 | -29.1 |
| none | all | 36 | 0.0% | 0.0% | - | 1.006 | 40.5 | -0.5 |
| solo_1 | left | 12 | 0.0% | 75.0% | - | 2.000 | 60.0 | +60.0 |
| solo_1 | straight | 12 | 0.0% | 75.0% | - | 2.000 | 0.0 | -0.2 |
| solo_1 | right | 12 | 0.0% | 66.7% | - | 2.000 | 60.0 | -60.5 |
| solo_1 | all | 36 | 0.0% | 72.2% | - | 2.000 | 60.0 | -0.2 |
| solo_2 | left | 12 | 0.0% | 0.0% | - | 1.826 | 62.6 | +56.2 |
| solo_2 | straight | 12 | 0.0% | 0.0% | - | 1.881 | 8.3 | -0.5 |
| solo_2 | right | 12 | 0.0% | 0.0% | - | 1.833 | 64.2 | -60.0 |
| solo_2 | all | 36 | 0.0% | 0.0% | - | 1.833 | 49.3 | -1.4 |

Ablation, paired per task against both (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| only_1 | +0.0 [+0.0, +0.0] pts | 0 | 0 | -11.4 [-20.6, -2.6] |
| only_2 | +0.0 [+0.0, +0.0] pts | 0 | 0 | -18.2 [-28.9, -7.5] |
| none | +0.0 [+0.0, +0.0] pts | 0 | 0 | -18.5 [-28.4, -8.6] |
| solo_1 | +0.0 [+0.0, +0.0] pts | 0 | 0 | -17.0 [-26.1, -7.9] |
| solo_2 | +0.0 [+0.0, +0.0] pts | 0 | 0 | -15.3 [-24.6, -5.4] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 0.0% | 0.0% | 18.8% | 29.0% | 38.1% | 31.8% |
| both | straight | 0.0% | 0.0% | 27.3% | 30.7% | 46.8% | 46.2% |
| both | right | 0.0% | 0.0% | 14.4% | 16.7% | 64.8% | 58.3% |
| only_1 | left | 0.0% | 0.0% | 54.0% | 57.9% | 29.4% | 18.9% |
| only_1 | straight | 0.0% | 0.0% | 57.6% | 53.8% | 33.7% | 25.3% |
| only_1 | right | 0.0% | 0.0% | 50.5% | 58.3% | 34.0% | 31.0% |
| only_2 | left | 0.0% | 0.0% | 32.6% | 42.7% | 46.1% | 30.9% |
| only_2 | straight | 0.0% | 0.0% | 42.7% | 48.7% | 38.2% | 32.5% |
| only_2 | right | 0.0% | 0.0% | 48.4% | 48.7% | 35.0% | 40.9% |
| none | left | 0.0% | 0.0% | 71.8% | 89.8% | 35.3% | 7.8% |
| none | straight | 0.0% | 0.0% | 87.4% | 88.2% | 23.7% | 20.1% |
| none | right | 0.0% | 0.0% | 81.4% | 84.2% | 32.1% | 24.6% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.3% | 0.0% | 0.1% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.4% | 0.0% | 0.1% |
| solo_2 | left | 0.0% | 0.0% | 38.7% | 27.6% | 23.0% | 29.5% |
| solo_2 | straight | 0.0% | 0.0% | 40.4% | 6.8% | 20.2% | 40.4% |
| solo_2 | right | 0.0% | 0.0% | 18.7% | 1.7% | 32.2% | 41.2% |
