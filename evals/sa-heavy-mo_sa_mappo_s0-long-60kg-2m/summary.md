# Spot-arm turn pilot: sa-heavy-mo_sa_mappo_s0-long-60kg-2m

logs/marl2/mo_sa_mappo_s0/model_4000.pt, iteration 4000, mappo, arms learned. long 60 kg, 2 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 0.0% | 12.5% | - | 1.549 | 57.7 | +57.5 |
| both | straight | 40 | 0.0% | 10.0% | - | 1.436 | 12.5 | -8.7 |
| both | right | 40 | 0.0% | 17.5% | - | 1.498 | 54.2 | -32.0 |
| both | all | 120 | 0.0% | 13.3% | - | 1.494 | 43.9 | +5.6 |
| only_1 | left | 40 | 0.0% | 7.5% | - | 1.603 | 56.1 | +56.4 |
| only_1 | straight | 40 | 0.0% | 0.0% | - | 1.459 | 13.1 | -6.0 |
| only_1 | right | 40 | 2.5% | 0.0% | 29.8 | 1.335 | 63.1 | -17.8 |
| only_1 | all | 120 | 0.8% | 2.5% | 29.8 | 1.499 | 51.5 | +10.9 |
| only_2 | left | 40 | 0.0% | 7.5% | - | 1.668 | 49.7 | +47.9 |
| only_2 | straight | 40 | 0.0% | 2.5% | - | 1.678 | 6.9 | -9.6 |
| only_2 | right | 40 | 0.0% | 5.0% | - | 1.666 | 63.6 | -35.2 |
| only_2 | all | 120 | 0.0% | 5.0% | - | 1.666 | 47.7 | +1.0 |
| none | left | 40 | 0.0% | 5.0% | - | 1.654 | 53.6 | +45.6 |
| none | straight | 40 | 0.0% | 2.5% | - | 1.624 | 8.7 | -10.3 |
| none | right | 40 | 0.0% | 0.0% | - | 1.764 | 65.5 | -57.3 |
| none | all | 120 | 0.0% | 2.5% | - | 1.667 | 50.1 | -7.4 |
| solo_1 | left | 40 | 0.0% | 70.0% | - | 2.000 | 60.0 | +60.0 |
| solo_1 | straight | 40 | 0.0% | 82.5% | - | 2.000 | 0.0 | -0.0 |
| solo_1 | right | 40 | 0.0% | 82.5% | - | 2.000 | 60.0 | -60.1 |
| solo_1 | all | 120 | 0.0% | 78.3% | - | 2.000 | 60.0 | -0.0 |
| solo_2 | left | 40 | 0.0% | 0.0% | - | 1.940 | 57.1 | +57.5 |
| solo_2 | straight | 40 | 0.0% | 0.0% | - | 1.939 | 4.9 | +1.4 |
| solo_2 | right | 40 | 0.0% | 0.0% | - | 1.952 | 58.2 | -58.0 |
| solo_2 | all | 120 | 0.0% | 0.0% | - | 1.944 | 55.9 | +0.3 |

Ablation, paired per task against both (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| only_1 | +0.8 [+0.0, +2.5] pts | 0 | 1 | +0.1 [-3.2, +3.5] |
| only_2 | +0.0 [+0.0, +0.0] pts | 0 | 0 | -2.9 [-6.4, +0.4] |
| none | +0.0 [+0.0, +0.0] pts | 0 | 0 | -3.7 [-7.4, +0.0] |
| solo_1 | +0.0 [+0.0, +0.0] pts | 0 | 0 | -3.9 [-7.2, -0.5] |
| solo_2 | +0.0 [+0.0, +0.0] pts | 0 | 0 | -3.7 [-6.8, -0.7] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 0.0% | 0.0% | 8.9% | 5.1% | 52.5% | 13.7% |
| both | straight | 0.0% | 0.0% | 6.8% | 12.9% | 59.6% | 24.3% |
| both | right | 0.0% | 0.0% | 3.6% | 16.7% | 61.6% | 31.1% |
| only_1 | left | 0.0% | 0.0% | 13.7% | 5.8% | 63.5% | 12.0% |
| only_1 | straight | 0.0% | 0.0% | 8.6% | 6.8% | 65.8% | 27.0% |
| only_1 | right | 5.0% | 0.0% | 5.4% | 10.9% | 75.7% | 60.7% |
| only_2 | left | 0.0% | 0.0% | 0.3% | 0.5% | 70.7% | 32.2% |
| only_2 | straight | 0.0% | 0.0% | 0.0% | 1.0% | 82.9% | 53.4% |
| only_2 | right | 0.0% | 0.0% | 0.2% | 0.2% | 83.6% | 66.8% |
| none | left | 0.0% | 0.0% | 0.0% | 0.4% | 78.3% | 28.0% |
| none | straight | 0.0% | 0.0% | 0.0% | 0.1% | 86.3% | 62.7% |
| none | right | 0.0% | 0.0% | 0.0% | 0.0% | 91.0% | 90.1% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.1% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.3% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 40.8% | 44.1% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 44.1% | 46.5% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 41.8% | 41.3% |
