# Spot-arm turn pilot: sa-heavy-mo_am_mappo_stowed_s0-plus-40kg-2m

logs/marl2/mo_am_mappo_stowed_s0/model_4000.pt, iteration 4000, mappo, arms stowed. plus 40 kg, 2 m, 6 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left -30.0 to -30.0 deg, straight +0.0 to +0.0 deg, right +30.0 to +30.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| stowed | left | 12 | 0.0% | 0.0% | - | 0.619 | 17.1 | +1.7 |
| stowed | straight | 12 | 0.0% | 8.3% | - | 0.835 | 15.0 | +4.8 |
| stowed | right | 12 | 0.0% | 0.0% | - | 0.372 | 12.2 | -0.3 |
| stowed | all | 36 | 0.0% | 2.8% | - | 0.619 | 13.4 | +2.1 |
| solo_1 | left | 12 | 0.0% | 0.0% | - | 1.330 | 41.2 | +38.1 |
| solo_1 | straight | 12 | 0.0% | 0.0% | - | 1.218 | 41.2 | +0.1 |
| solo_1 | right | 12 | 0.0% | 0.0% | - | 1.675 | 18.2 | +12.1 |
| solo_1 | all | 36 | 0.0% | 0.0% | - | 1.317 | 35.2 | +16.8 |
| solo_2 | left | 12 | 0.0% | 0.0% | - | 1.997 | 29.8 | -29.3 |
| solo_2 | straight | 12 | 0.0% | 0.0% | - | 2.000 | 0.0 | +0.3 |
| solo_2 | right | 12 | 0.0% | 0.0% | - | 2.000 | 30.6 | +30.5 |
| solo_2 | all | 36 | 0.0% | 0.0% | - | 2.000 | 29.8 | +0.5 |

Ablation, paired per task against stowed (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| solo_1 | +0.0 [+0.0, +0.0] pts | 0 | 0 | +18.8 [+14.5, +22.9] |
| solo_2 | +0.0 [+0.0, +0.0] pts | 0 | 0 | +6.1 [+1.2, +11.3] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| stowed | left | 0.0% | 0.0% | 0.0% | 0.0% | 25.7% | 14.6% |
| stowed | straight | 0.0% | 0.0% | 0.0% | 0.0% | 9.1% | 17.3% |
| stowed | right | 0.0% | 0.0% | 0.0% | 0.0% | 17.1% | 11.4% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
