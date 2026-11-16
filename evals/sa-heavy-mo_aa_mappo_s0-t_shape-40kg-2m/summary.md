# Spot-arm turn pilot: sa-heavy-mo_aa_mappo_s0-t_shape-40kg-2m

logs/marl2/mo_aa_mappo_s0/model_4000.pt, iteration 4000, mappo, arms stowed. t_shape 40 kg, 2 m, 6 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| stowed | left | 12 | 16.7% | 0.0% | 10.7 | 0.466 | 10.1 | +0.4 |
| stowed | straight | 12 | 8.3% | 0.0% | 24.5 | 0.308 | 7.2 | -4.2 |
| stowed | right | 12 | 0.0% | 0.0% | - | 0.327 | 18.6 | -17.1 |
| stowed | all | 36 | 8.3% | 0.0% | 10.7 | 0.372 | 10.1 | -7.0 |
| solo_1 | left | 12 | 0.0% | 8.3% | - | 1.875 | 60.0 | +42.3 |
| solo_1 | straight | 12 | 0.0% | 0.0% | - | 1.991 | 56.4 | -22.6 |
| solo_1 | right | 12 | 0.0% | 8.3% | - | 1.999 | 60.0 | -60.2 |
| solo_1 | all | 36 | 0.0% | 5.6% | - | 1.961 | 60.0 | -13.5 |
| solo_2 | left | 12 | 0.0% | 0.0% | - | 1.999 | 60.0 | +67.5 |
| solo_2 | straight | 12 | 0.0% | 0.0% | - | 1.995 | 12.6 | +2.0 |
| solo_2 | right | 12 | 0.0% | 0.0% | - | 1.527 | 60.2 | -40.9 |
| solo_2 | all | 36 | 0.0% | 0.0% | - | 1.716 | 59.9 | +9.5 |

Ablation, paired per task against stowed (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| solo_1 | -8.3 [-19.4, +0.0] pts | 3 | 0 | +38.4 [+27.3, +49.5] |
| solo_2 | -8.3 [-19.4, +0.0] pts | 3 | 0 | +39.4 [+27.9, +52.6] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| stowed | left | 33.3% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| stowed | straight | 16.7% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| stowed | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
