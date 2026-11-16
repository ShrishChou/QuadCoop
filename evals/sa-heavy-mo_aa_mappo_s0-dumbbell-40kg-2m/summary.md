# Spot-arm turn pilot: sa-heavy-mo_aa_mappo_s0-dumbbell-40kg-2m

logs/marl2/mo_aa_mappo_s0/model_4000.pt, iteration 4000, mappo, arms stowed. dumbbell 40 kg, 2 m, 6 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| stowed | left | 12 | 8.3% | 0.0% | 34.0 | 0.459 | 22.9 | +18.2 |
| stowed | straight | 12 | 8.3% | 0.0% | 21.8 | 0.427 | 7.0 | +2.3 |
| stowed | right | 12 | 8.3% | 0.0% | 26.3 | 0.367 | 10.6 | -11.8 |
| stowed | all | 36 | 8.3% | 0.0% | 26.3 | 0.427 | 8.9 | +2.9 |
| solo_1 | left | 12 | 0.0% | 0.0% | - | 2.405 | 64.6 | -21.7 |
| solo_1 | straight | 12 | 0.0% | 0.0% | - | 1.784 | 69.2 | +47.8 |
| solo_1 | right | 12 | 0.0% | 8.3% | - | 1.936 | 38.8 | -11.6 |
| solo_1 | all | 36 | 0.0% | 2.8% | - | 1.784 | 56.2 | +4.9 |
| solo_2 | left | 12 | 0.0% | 8.3% | - | 1.823 | 49.3 | +28.1 |
| solo_2 | straight | 12 | 0.0% | 0.0% | - | 1.764 | 40.5 | -1.3 |
| solo_2 | right | 12 | 0.0% | 0.0% | - | 1.807 | 71.0 | -1.4 |
| solo_2 | all | 36 | 0.0% | 2.8% | - | 1.764 | 50.5 | +8.5 |

Ablation, paired per task against stowed (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| solo_1 | -8.3 [-19.4, +0.0] pts | 3 | 0 | +37.3 [+28.2, +45.7] |
| solo_2 | -8.3 [-19.4, +0.0] pts | 3 | 0 | +28.9 [+19.3, +38.4] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| stowed | left | 16.7% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| stowed | straight | 16.7% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| stowed | right | 16.7% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
