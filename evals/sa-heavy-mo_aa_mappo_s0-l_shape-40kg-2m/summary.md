# Spot-arm turn pilot: sa-heavy-mo_aa_mappo_s0-l_shape-40kg-2m

logs/marl2/mo_aa_mappo_s0/model_4000.pt, iteration 4000, mappo, arms stowed. l_shape 40 kg, 2 m, 6 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| stowed | left | 12 | 0.0% | 8.3% | - | 0.404 | 5.3 | +2.7 |
| stowed | straight | 12 | 0.0% | 0.0% | - | 0.299 | 5.5 | +0.5 |
| stowed | right | 12 | 16.7% | 0.0% | 22.7 | 0.257 | 8.8 | +1.7 |
| stowed | all | 36 | 5.6% | 2.8% | 22.7 | 0.290 | 6.2 | +1.7 |
| solo_1 | left | 12 | 0.0% | 0.0% | - | 1.942 | 61.3 | +35.9 |
| solo_1 | straight | 12 | 0.0% | 0.0% | - | 1.998 | 74.7 | -49.0 |
| solo_1 | right | 12 | 0.0% | 0.0% | - | 1.999 | 60.0 | -67.8 |
| solo_1 | all | 36 | 0.0% | 0.0% | - | 1.993 | 60.0 | -27.0 |
| solo_2 | left | 12 | 0.0% | 0.0% | - | 2.000 | 60.0 | +38.4 |
| solo_2 | straight | 12 | 0.0% | 0.0% | - | 2.000 | 34.2 | -26.2 |
| solo_2 | right | 12 | 0.0% | 0.0% | - | 1.899 | 84.8 | -82.3 |
| solo_2 | all | 36 | 0.0% | 0.0% | - | 2.000 | 60.0 | -23.4 |

Ablation, paired per task against stowed (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| solo_1 | -5.6 [-13.9, +0.0] pts | 2 | 0 | +49.1 [+34.4, +64.7] |
| solo_2 | -5.6 [-13.9, +0.0] pts | 2 | 0 | +44.2 [+32.9, +56.1] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| stowed | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| stowed | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| stowed | right | 33.3% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
