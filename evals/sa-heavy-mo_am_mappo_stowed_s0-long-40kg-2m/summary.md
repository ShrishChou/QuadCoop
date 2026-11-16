# Spot-arm turn pilot: sa-heavy-mo_am_mappo_stowed_s0-long-40kg-2m

logs/marl2/mo_am_mappo_stowed_s0/model_4000.pt, iteration 4000, mappo, arms stowed. long 40 kg, 2 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| stowed | left | 40 | 5.0% | 2.5% | 14.7 | 0.571 | 14.0 | -12.0 |
| stowed | straight | 40 | 15.0% | 0.0% | 25.0 | 0.442 | 6.6 | -5.0 |
| stowed | right | 40 | 2.5% | 0.0% | 33.5 | 0.430 | 9.0 | -30.3 |
| stowed | all | 120 | 7.5% | 0.8% | 20.2 | 0.471 | 8.1 | -15.7 |
| solo_1 | left | 40 | 0.0% | 0.0% | - | 1.737 | 38.3 | +39.4 |
| solo_1 | straight | 40 | 0.0% | 2.5% | - | 1.266 | 67.9 | -32.1 |
| solo_1 | right | 40 | 0.0% | 0.0% | - | 1.475 | 77.9 | +78.5 |
| solo_1 | all | 120 | 0.0% | 0.8% | - | 1.480 | 67.9 | +28.6 |
| solo_2 | left | 40 | 0.0% | 0.0% | - | 2.000 | 60.0 | +60.2 |
| solo_2 | straight | 40 | 0.0% | 0.0% | - | 2.000 | 0.0 | +0.0 |
| solo_2 | right | 40 | 0.0% | 0.0% | - | 2.000 | 60.0 | -60.0 |
| solo_2 | all | 120 | 0.0% | 0.0% | - | 2.000 | 60.0 | +0.1 |

Ablation, paired per task against stowed (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| solo_1 | -7.5 [-12.5, -3.3] pts | 9 | 0 | +40.5 [+35.2, +45.5] |
| solo_2 | -7.5 [-12.5, -3.3] pts | 9 | 0 | +21.4 [+15.8, +27.1] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| stowed | left | 10.0% | 0.0% | 0.0% | 0.0% | 10.4% | 20.0% |
| stowed | straight | 30.0% | 0.0% | 0.0% | 0.0% | 13.2% | 25.3% |
| stowed | right | 5.0% | 0.0% | 0.0% | 0.0% | 19.1% | 33.9% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
