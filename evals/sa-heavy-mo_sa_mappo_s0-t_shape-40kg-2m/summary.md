# Spot-arm turn pilot: sa-heavy-mo_sa_mappo_s0-t_shape-40kg-2m

logs/marl2/mo_sa_mappo_s0/model_4000.pt, iteration 4000, mappo, arms learned. t_shape 40 kg, 2 m, 6 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 12 | 0.0% | 8.3% | - | 0.456 | 47.6 | +36.8 |
| both | straight | 12 | 0.0% | 8.3% | - | 0.517 | 30.6 | -8.0 |
| both | right | 12 | 0.0% | 0.0% | - | 0.570 | 32.7 | -17.6 |
| both | all | 36 | 0.0% | 5.6% | - | 0.464 | 32.7 | +3.7 |
| only_1 | left | 12 | 0.0% | 8.3% | - | 0.471 | 36.5 | +32.4 |
| only_1 | straight | 12 | 0.0% | 0.0% | - | 0.316 | 30.6 | -0.2 |
| only_1 | right | 12 | 8.3% | 0.0% | 32.3 | 0.315 | 23.4 | -6.1 |
| only_1 | all | 36 | 2.8% | 2.8% | 32.3 | 0.343 | 25.6 | +8.7 |
| only_2 | left | 12 | 0.0% | 0.0% | - | 0.368 | 10.3 | -7.6 |
| only_2 | straight | 12 | 0.0% | 0.0% | - | 0.659 | 39.1 | -35.1 |
| only_2 | right | 12 | 0.0% | 0.0% | - | 0.597 | 47.7 | -33.2 |
| only_2 | all | 36 | 0.0% | 0.0% | - | 0.571 | 32.9 | -25.3 |
| none | left | 12 | 0.0% | 0.0% | - | 0.494 | 6.2 | -1.1 |
| none | straight | 12 | 0.0% | 0.0% | - | 0.518 | 31.7 | -3.3 |
| none | right | 12 | 0.0% | 0.0% | - | 0.454 | 52.2 | -5.2 |
| none | all | 36 | 0.0% | 0.0% | - | 0.483 | 20.7 | -3.2 |
| solo_1 | left | 12 | 0.0% | 75.0% | - | 2.000 | 60.0 | +60.0 |
| solo_1 | straight | 12 | 0.0% | 100.0% | - | 2.000 | 0.0 | -0.2 |
| solo_1 | right | 12 | 0.0% | 100.0% | - | 2.000 | 60.0 | -60.3 |
| solo_1 | all | 36 | 0.0% | 91.7% | - | 2.000 | 60.0 | -0.2 |
| solo_2 | left | 12 | 0.0% | 0.0% | - | 1.665 | 67.3 | +23.6 |
| solo_2 | straight | 12 | 0.0% | 0.0% | - | 1.743 | 23.0 | -2.4 |
| solo_2 | right | 12 | 0.0% | 0.0% | - | 1.796 | 48.7 | -47.2 |
| solo_2 | all | 36 | 0.0% | 0.0% | - | 1.737 | 43.3 | -8.7 |

Ablation, paired per task against both (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| only_1 | +2.8 [+0.0, +8.3] pts | 0 | 1 | -9.0 [-20.6, +2.1] |
| only_2 | +0.0 [+0.0, +0.0] pts | 0 | 0 | -9.3 [-21.5, +2.3] |
| none | +0.0 [+0.0, +0.0] pts | 0 | 0 | -15.0 [-29.5, -2.1] |
| solo_1 | +0.0 [+0.0, +0.0] pts | 0 | 0 | -0.2 [-12.4, +11.7] |
| solo_2 | +0.0 [+0.0, +0.0] pts | 0 | 0 | +3.5 [-7.9, +14.6] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 0.0% | 0.0% | 3.5% | 16.4% | 23.8% | 9.2% |
| both | straight | 0.0% | 0.0% | 7.2% | 6.5% | 32.3% | 16.5% |
| both | right | 0.0% | 0.0% | 6.2% | 4.6% | 32.9% | 22.8% |
| only_1 | left | 0.0% | 0.0% | 1.6% | 4.0% | 21.5% | 10.6% |
| only_1 | straight | 0.0% | 0.0% | 5.9% | 1.4% | 26.7% | 18.6% |
| only_1 | right | 0.0% | 16.7% | 4.5% | 3.2% | 31.7% | 19.8% |
| only_2 | left | 0.0% | 0.0% | 3.1% | 10.9% | 32.2% | 6.4% |
| only_2 | straight | 0.0% | 0.0% | 1.0% | 7.2% | 51.5% | 13.1% |
| only_2 | right | 0.0% | 0.0% | 1.7% | 5.9% | 46.6% | 26.0% |
| none | left | 0.0% | 0.0% | 0.0% | 0.0% | 40.6% | 11.8% |
| none | straight | 0.0% | 0.0% | 0.0% | 0.0% | 39.6% | 12.7% |
| none | right | 0.0% | 0.0% | 0.0% | 0.0% | 50.1% | 34.0% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.1% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.2% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.4% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 42.7% | 20.0% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 41.5% | 42.2% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 40.9% | 39.9% |
