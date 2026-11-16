# Spot-arm turn pilot: sa-heavy-mo_am_mappo_stowed_s0-t_shape-40kg-2m

logs/marl2/mo_am_mappo_stowed_s0/model_4000.pt, iteration 4000, mappo, arms stowed. t_shape 40 kg, 2 m, 6 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| stowed | left | 12 | 0.0% | 0.0% | - | 0.805 | 17.8 | +17.6 |
| stowed | straight | 12 | 0.0% | 0.0% | - | 0.876 | 15.0 | -10.3 |
| stowed | right | 12 | 0.0% | 0.0% | - | 1.057 | 53.2 | -50.4 |
| stowed | all | 36 | 0.0% | 0.0% | - | 0.805 | 21.9 | -14.4 |
| solo_1 | left | 12 | 0.0% | 0.0% | - | 1.548 | 24.9 | +20.4 |
| solo_1 | straight | 12 | 0.0% | 0.0% | - | 1.367 | 57.4 | -44.3 |
| solo_1 | right | 12 | 0.0% | 0.0% | - | 1.316 | 113.8 | -116.9 |
| solo_1 | all | 36 | 0.0% | 0.0% | - | 1.355 | 57.4 | -46.9 |
| solo_2 | left | 12 | 0.0% | 0.0% | - | 2.000 | 60.0 | +60.0 |
| solo_2 | straight | 12 | 0.0% | 0.0% | - | 2.000 | 0.0 | +0.0 |
| solo_2 | right | 12 | 0.0% | 0.0% | - | 2.000 | 60.0 | -60.0 |
| solo_2 | all | 36 | 0.0% | 0.0% | - | 2.000 | 60.0 | +0.0 |

Ablation, paired per task against stowed (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| solo_1 | +0.0 [+0.0, +0.0] pts | 0 | 0 | +36.4 [+26.3, +46.7] |
| solo_2 | +0.0 [+0.0, +0.0] pts | 0 | 0 | +11.3 [+1.9, +21.2] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| stowed | left | 0.0% | 0.0% | 0.0% | 0.0% | 1.1% | 22.7% |
| stowed | straight | 0.0% | 0.0% | 0.0% | 0.0% | 6.2% | 11.3% |
| stowed | right | 0.0% | 0.0% | 0.0% | 0.0% | 1.9% | 7.8% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
