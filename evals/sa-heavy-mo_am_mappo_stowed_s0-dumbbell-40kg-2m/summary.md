# Spot-arm turn pilot: sa-heavy-mo_am_mappo_stowed_s0-dumbbell-40kg-2m

logs/marl2/mo_am_mappo_stowed_s0/model_4000.pt, iteration 4000, mappo, arms stowed. dumbbell 40 kg, 2 m, 6 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| stowed | left | 12 | 0.0% | 0.0% | - | 0.650 | 23.5 | +5.2 |
| stowed | straight | 12 | 0.0% | 0.0% | - | 0.814 | 35.7 | -22.2 |
| stowed | right | 12 | 0.0% | 0.0% | - | 0.726 | 25.0 | +24.4 |
| stowed | all | 36 | 0.0% | 0.0% | - | 0.726 | 26.8 | +2.5 |
| solo_1 | left | 12 | 0.0% | 0.0% | - | 1.330 | 11.9 | +9.4 |
| solo_1 | straight | 12 | 0.0% | 0.0% | - | 0.845 | 79.5 | -59.4 |
| solo_1 | right | 12 | 0.0% | 0.0% | - | 1.173 | 69.0 | +67.8 |
| solo_1 | all | 36 | 0.0% | 0.0% | - | 1.173 | 66.8 | +6.0 |
| solo_2 | left | 12 | 0.0% | 0.0% | - | 2.000 | 60.0 | +60.0 |
| solo_2 | straight | 12 | 0.0% | 0.0% | - | 2.000 | 0.0 | +0.0 |
| solo_2 | right | 12 | 0.0% | 0.0% | - | 2.000 | 60.0 | -60.0 |
| solo_2 | all | 36 | 0.0% | 0.0% | - | 2.000 | 60.0 | +0.0 |

Ablation, paired per task against stowed (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| solo_1 | +0.0 [+0.0, +0.0] pts | 0 | 0 | +17.9 [+6.5, +29.1] |
| solo_2 | +0.0 [+0.0, +0.0] pts | 0 | 0 | +7.0 [-5.3, +19.9] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| stowed | left | 0.0% | 0.0% | 0.0% | 0.0% | 5.3% | 16.7% |
| stowed | straight | 0.0% | 0.0% | 0.0% | 0.0% | 23.1% | 11.4% |
| stowed | right | 0.0% | 0.0% | 0.0% | 0.0% | 6.8% | 24.3% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
