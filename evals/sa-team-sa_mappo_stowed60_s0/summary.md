# Spot-arm turn pilot: sa-team-sa_mappo_stowed60_s0

logs/marl2/sa_mappo_stowed60_s0/model_2000.pt, iteration 2000, mappo, arms stowed. long 20 kg, 1 m, 20 placements per turn x swap, horizon 20 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| stowed | left | 40 | 65.0% | 0.0% | 4.6 | 0.070 | 2.3 | -2.2 |
| stowed | straight | 40 | 85.0% | 0.0% | 6.3 | 0.064 | 3.2 | -0.9 |
| stowed | right | 40 | 95.0% | 0.0% | 4.6 | 0.064 | 1.2 | +1.4 |
| stowed | all | 120 | 81.7% | 0.0% | 5.4 | 0.064 | 2.5 | -0.6 |
| solo_1 | left | 40 | 0.0% | 0.0% | - | 0.913 | 60.0 | +60.6 |
| solo_1 | straight | 40 | 0.0% | 0.0% | - | 0.958 | 1.4 | -3.7 |
| solo_1 | right | 40 | 0.0% | 0.0% | - | 0.903 | 66.5 | -41.5 |
| solo_1 | all | 120 | 0.0% | 0.0% | - | 0.922 | 57.4 | +5.1 |
| solo_2 | left | 40 | 0.0% | 0.0% | - | 0.798 | 53.8 | +43.8 |
| solo_2 | straight | 40 | 0.0% | 0.0% | - | 0.743 | 29.9 | -17.0 |
| solo_2 | right | 40 | 0.0% | 0.0% | - | 0.841 | 71.0 | -28.0 |
| solo_2 | all | 120 | 0.0% | 0.0% | - | 0.801 | 56.7 | -0.4 |

Ablation, paired per task against stowed (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| solo_1 | -81.7 [-88.3, -74.2] pts | 98 | 0 | +36.3 [+31.0, +41.5] |
| solo_2 | -81.7 [-88.3, -74.2] pts | 98 | 0 | +44.1 [+39.2, +49.0] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| stowed | left | 100.0% | 30.0% | 0.0% | 0.0% | 19.7% | 15.1% |
| stowed | straight | 95.0% | 75.0% | 0.0% | 0.0% | 12.1% | 14.0% |
| stowed | right | 95.0% | 95.0% | 0.0% | 0.0% | 19.0% | 26.8% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.1% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.2% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 2.3% | 0.3% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 3.9% | 2.1% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 2.0% | 2.0% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 3.1% | 1.2% |
