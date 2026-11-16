# Spot-arm turn pilot: sa-heavy-mo_aa_mappo_s0-u_channel-40kg-2m

logs/marl2/mo_aa_mappo_s0/model_4000.pt, iteration 4000, mappo, arms stowed. u_channel 40 kg, 2 m, 6 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| stowed | left | 12 | 0.0% | 0.0% | - | 0.465 | 12.4 | +2.1 |
| stowed | straight | 12 | 8.3% | 0.0% | 6.9 | 0.359 | 15.9 | -16.2 |
| stowed | right | 12 | 0.0% | 0.0% | - | 0.315 | 20.1 | -16.6 |
| stowed | all | 36 | 2.8% | 0.0% | 6.9 | 0.366 | 14.9 | -10.2 |
| solo_1 | left | 12 | 0.0% | 0.0% | - | 1.996 | 60.0 | +33.9 |
| solo_1 | straight | 12 | 0.0% | 0.0% | - | 2.000 | 4.9 | -22.2 |
| solo_1 | right | 12 | 0.0% | 0.0% | - | 1.999 | 60.0 | -66.4 |
| solo_1 | all | 36 | 0.0% | 0.0% | - | 1.997 | 60.0 | -18.2 |
| solo_2 | left | 12 | 0.0% | 0.0% | - | 2.000 | 60.0 | +56.1 |
| solo_2 | straight | 12 | 0.0% | 0.0% | - | 2.000 | 27.9 | -9.8 |
| solo_2 | right | 12 | 0.0% | 0.0% | - | 1.998 | 60.0 | -49.9 |
| solo_2 | all | 36 | 0.0% | 0.0% | - | 1.998 | 58.8 | -1.2 |

Ablation, paired per task against stowed (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| solo_1 | -2.8 [-8.3, +0.0] pts | 1 | 0 | +33.7 [+20.2, +47.8] |
| solo_2 | -2.8 [-8.3, +0.0] pts | 1 | 0 | +30.8 [+18.6, +43.0] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| stowed | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| stowed | straight | 0.0% | 16.7% | 0.0% | 0.0% | 0.0% | 0.0% |
| stowed | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
