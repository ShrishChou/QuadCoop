# Spot-arm turn pilot: sa-heavy-mo_aa_mappo_s0-sphere-40kg-2m

logs/marl2/mo_aa_mappo_s0/model_4000.pt, iteration 4000, mappo, arms stowed. sphere 40 kg, 2 m, 6 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +0.0 to +0.0 deg, straight +0.0 to +0.0 deg, right +0.0 to +0.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| stowed | left | 12 | 100.0% | 0.0% | 5.9 | 0.062 | 0.0 | +0.0 |
| stowed | straight | 12 | 91.7% | 0.0% | 6.3 | 0.048 | 0.0 | +0.0 |
| stowed | right | 12 | 91.7% | 8.3% | 6.1 | 0.063 | 0.0 | +0.0 |
| stowed | all | 36 | 94.4% | 2.8% | 6.1 | 0.059 | 0.0 | +0.0 |
| solo_1 | left | 12 | 0.0% | 0.0% | - | 2.000 | 0.0 | +0.0 |
| solo_1 | straight | 12 | 0.0% | 0.0% | - | 1.999 | 0.0 | +0.0 |
| solo_1 | right | 12 | 0.0% | 0.0% | - | 2.000 | 0.0 | +0.0 |
| solo_1 | all | 36 | 0.0% | 0.0% | - | 2.000 | 0.0 | +0.0 |
| solo_2 | left | 12 | 0.0% | 0.0% | - | 2.000 | 0.0 | +0.0 |
| solo_2 | straight | 12 | 0.0% | 0.0% | - | 2.000 | 0.0 | +0.0 |
| solo_2 | right | 12 | 0.0% | 0.0% | - | 2.000 | 0.0 | +0.0 |
| solo_2 | all | 36 | 0.0% | 0.0% | - | 2.000 | 0.0 | +0.0 |

Ablation, paired per task against stowed (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| solo_1 | -94.4 [-100.0, -86.1] pts | 34 | 0 | +0.0 [+0.0, +0.0] |
| solo_2 | -94.4 [-100.0, -86.1] pts | 34 | 0 | +0.0 [+0.0, +0.0] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| stowed | left | 100.0% | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| stowed | straight | 100.0% | 83.3% | 0.0% | 0.0% | 0.0% | 0.0% |
| stowed | right | 100.0% | 83.3% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
