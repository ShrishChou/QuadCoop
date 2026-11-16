# Spot-arm turn pilot: sa-heavy-sa_heavy_stowed_s0-20kg-1m

logs/marl2/sa_heavy_stowed_s0/model_4000.pt, iteration 4000, mappo, arms stowed. long 20 kg, 1 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| stowed | left | 40 | 100.0% | 0.0% | 4.2 | 0.062 | 1.6 | -1.6 |
| stowed | straight | 40 | 100.0% | 0.0% | 6.0 | 0.070 | 1.8 | -1.0 |
| stowed | right | 40 | 100.0% | 0.0% | 4.5 | 0.061 | 2.6 | -2.2 |
| stowed | all | 120 | 100.0% | 0.0% | 4.5 | 0.062 | 1.9 | -1.6 |
| solo_1 | left | 40 | 0.0% | 0.0% | - | 1.000 | 60.0 | +60.0 |
| solo_1 | straight | 40 | 0.0% | 0.0% | - | 1.000 | 0.0 | -4.1 |
| solo_1 | right | 40 | 0.0% | 0.0% | - | 1.000 | 65.5 | -64.1 |
| solo_1 | all | 120 | 0.0% | 0.0% | - | 1.000 | 60.0 | -2.8 |
| solo_2 | left | 40 | 0.0% | 0.0% | - | 0.725 | 65.1 | -28.9 |
| solo_2 | straight | 40 | 0.0% | 0.0% | - | 0.611 | 42.1 | +12.5 |
| solo_2 | right | 40 | 0.0% | 0.0% | - | 0.970 | 58.9 | -50.8 |
| solo_2 | all | 120 | 0.0% | 0.0% | - | 0.760 | 46.6 | -22.4 |

Ablation, paired per task against stowed (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| solo_1 | -100.0 [-100.0, -100.0] pts | 120 | 0 | +42.1 [+36.6, +47.3] |
| solo_2 | -100.0 [-100.0, -100.0] pts | 120 | 0 | +42.7 [+38.5, +46.5] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| stowed | left | 100.0% | 100.0% | 0.0% | 0.0% | 24.7% | 22.1% |
| stowed | straight | 100.0% | 100.0% | 0.0% | 0.0% | 23.9% | 13.7% |
| stowed | right | 100.0% | 100.0% | 0.0% | 0.0% | 21.9% | 26.0% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.2% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.2% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.1% | 2.0% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.1% | 0.6% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.1% | 0.0% |
