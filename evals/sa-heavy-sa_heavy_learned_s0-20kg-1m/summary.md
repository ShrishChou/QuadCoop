# Spot-arm turn pilot: sa-heavy-sa_heavy_learned_s0-20kg-1m

logs/marl2/sa_heavy_learned_s0/model_4000.pt, iteration 4000, mappo, arms learned. long 20 kg, 1 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 100.0% | 0.0% | 4.2 | 0.051 | 1.0 | -0.2 |
| both | straight | 40 | 100.0% | 0.0% | 4.2 | 0.065 | 1.2 | +0.2 |
| both | right | 40 | 97.5% | 0.0% | 4.3 | 0.057 | 1.1 | +0.2 |
| both | all | 120 | 99.2% | 0.0% | 4.2 | 0.056 | 1.1 | +0.0 |
| only_1 | left | 40 | 100.0% | 0.0% | 4.6 | 0.057 | 1.1 | +0.7 |
| only_1 | straight | 40 | 100.0% | 0.0% | 4.9 | 0.073 | 1.4 | -0.2 |
| only_1 | right | 40 | 100.0% | 0.0% | 4.9 | 0.058 | 1.2 | -0.3 |
| only_1 | all | 120 | 100.0% | 0.0% | 4.7 | 0.059 | 1.1 | +0.1 |
| only_2 | left | 40 | 97.5% | 0.0% | 4.5 | 0.065 | 1.3 | +1.2 |
| only_2 | straight | 40 | 100.0% | 0.0% | 4.6 | 0.059 | 1.3 | +0.6 |
| only_2 | right | 40 | 100.0% | 0.0% | 4.9 | 0.070 | 1.6 | +0.4 |
| only_2 | all | 120 | 99.2% | 0.0% | 4.7 | 0.063 | 1.4 | +0.7 |
| none | left | 40 | 100.0% | 0.0% | 6.2 | 0.064 | 1.6 | +0.9 |
| none | straight | 40 | 100.0% | 0.0% | 6.8 | 0.066 | 1.4 | +0.4 |
| none | right | 40 | 100.0% | 0.0% | 6.1 | 0.057 | 1.4 | +0.3 |
| none | all | 120 | 100.0% | 0.0% | 6.2 | 0.063 | 1.4 | +0.6 |
| solo_1 | left | 40 | 0.0% | 0.0% | - | 1.000 | 60.0 | +60.0 |
| solo_1 | straight | 40 | 0.0% | 0.0% | - | 1.000 | 0.0 | +0.0 |
| solo_1 | right | 40 | 0.0% | 0.0% | - | 0.997 | 59.5 | -52.6 |
| solo_1 | all | 120 | 0.0% | 0.0% | - | 1.000 | 59.5 | +2.5 |
| solo_2 | left | 40 | 0.0% | 0.0% | - | 0.976 | 60.2 | +37.7 |
| solo_2 | straight | 40 | 0.0% | 0.0% | - | 1.000 | 0.0 | -0.0 |
| solo_2 | right | 40 | 0.0% | 0.0% | - | 1.000 | 60.0 | -60.0 |
| solo_2 | all | 120 | 0.0% | 0.0% | - | 1.000 | 60.0 | -7.4 |

Ablation, paired per task against both (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| only_1 | +0.8 [+0.0, +2.5] pts | 0 | 1 | +0.1 [-0.1, +0.4] |
| only_2 | +0.0 [-2.5, +2.5] pts | 1 | 1 | +0.3 [-0.0, +0.5] |
| none | +0.8 [+0.0, +2.5] pts | 0 | 1 | +0.4 [+0.1, +0.7] |
| solo_1 | -99.2 [-100.0, -97.5] pts | 119 | 0 | +36.3 [+31.3, +41.0] |
| solo_2 | -99.2 [-100.0, -97.5] pts | 119 | 0 | +41.7 [+35.9, +47.3] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 100.0% | 100.0% | 0.7% | 1.4% | 21.5% | 23.9% |
| both | straight | 100.0% | 100.0% | 0.0% | 0.1% | 26.5% | 22.4% |
| both | right | 100.0% | 95.0% | 0.0% | 0.0% | 20.5% | 29.6% |
| only_1 | left | 100.0% | 100.0% | 0.0% | 0.6% | 21.2% | 22.5% |
| only_1 | straight | 100.0% | 100.0% | 0.0% | 0.0% | 14.1% | 23.8% |
| only_1 | right | 100.0% | 100.0% | 0.0% | 0.0% | 19.0% | 25.8% |
| only_2 | left | 100.0% | 95.0% | 0.5% | 0.0% | 22.8% | 24.0% |
| only_2 | straight | 100.0% | 100.0% | 0.0% | 0.1% | 24.6% | 21.2% |
| only_2 | right | 100.0% | 100.0% | 0.0% | 0.0% | 20.9% | 29.6% |
| none | left | 100.0% | 100.0% | 0.0% | 0.0% | 19.6% | 21.5% |
| none | straight | 100.0% | 100.0% | 0.0% | 0.0% | 9.2% | 25.7% |
| none | right | 100.0% | 100.0% | 0.0% | 0.0% | 17.9% | 27.3% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.5% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
