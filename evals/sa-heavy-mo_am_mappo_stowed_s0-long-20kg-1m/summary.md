# Spot-arm turn pilot: sa-heavy-mo_am_mappo_stowed_s0-long-20kg-1m

logs/marl2/mo_am_mappo_stowed_s0/model_4000.pt, iteration 4000, mappo, arms stowed. long 20 kg, 1 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| stowed | left | 40 | 0.0% | 0.0% | - | 0.311 | 5.8 | -3.7 |
| stowed | straight | 40 | 30.0% | 0.0% | 4.6 | 0.222 | 3.7 | -2.8 |
| stowed | right | 40 | 5.0% | 0.0% | 39.3 | 0.314 | 5.9 | -4.2 |
| stowed | all | 120 | 11.7% | 0.0% | 4.7 | 0.309 | 5.1 | -3.6 |
| solo_1 | left | 40 | 0.0% | 0.0% | - | 0.891 | 50.6 | +50.8 |
| solo_1 | straight | 40 | 0.0% | 0.0% | - | 1.168 | 83.7 | +33.1 |
| solo_1 | right | 40 | 0.0% | 0.0% | - | 0.519 | 83.0 | +82.3 |
| solo_1 | all | 120 | 0.0% | 0.0% | - | 0.779 | 75.2 | +55.4 |
| solo_2 | left | 40 | 0.0% | 0.0% | - | 0.997 | 60.9 | +61.7 |
| solo_2 | straight | 40 | 0.0% | 0.0% | - | 0.997 | 0.7 | +1.0 |
| solo_2 | right | 40 | 0.0% | 0.0% | - | 0.991 | 58.9 | -58.1 |
| solo_2 | all | 120 | 0.0% | 0.0% | - | 0.994 | 58.9 | +1.5 |

Ablation, paired per task against stowed (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| solo_1 | -11.7 [-17.5, -6.7] pts | 14 | 0 | +57.9 [+53.7, +62.1] |
| solo_2 | -11.7 [-17.5, -6.7] pts | 14 | 0 | +33.4 [+28.3, +38.2] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| stowed | left | 0.0% | 0.0% | 0.0% | 0.0% | 4.1% | 24.8% |
| stowed | straight | 55.0% | 5.0% | 0.0% | 0.0% | 8.6% | 17.7% |
| stowed | right | 10.0% | 0.0% | 0.0% | 0.0% | 26.7% | 11.6% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.1% | 0.0% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.1% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.4% |
