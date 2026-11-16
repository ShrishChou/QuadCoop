# Spot-arm turn pilot: sa-heavy-mo_aa_mappo_s0-plus-40kg-2m

logs/marl2/mo_aa_mappo_s0/model_4000.pt, iteration 4000, mappo, arms stowed. plus 40 kg, 2 m, 6 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left -30.0 to -30.0 deg, straight +0.0 to +0.0 deg, right +30.0 to +30.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| stowed | left | 12 | 66.7% | 8.3% | 16.5 | 0.091 | 3.9 | +2.0 |
| stowed | straight | 12 | 8.3% | 0.0% | 8.6 | 0.204 | 3.6 | -1.2 |
| stowed | right | 12 | 33.3% | 0.0% | 9.5 | 0.184 | 2.8 | -1.5 |
| stowed | all | 36 | 36.1% | 2.8% | 9.5 | 0.163 | 3.2 | -0.2 |
| solo_1 | left | 12 | 0.0% | 0.0% | - | 1.849 | 16.2 | -0.1 |
| solo_1 | straight | 12 | 0.0% | 0.0% | - | 1.672 | 14.4 | -4.4 |
| solo_1 | right | 12 | 0.0% | 0.0% | - | 1.653 | 28.9 | +1.5 |
| solo_1 | all | 36 | 0.0% | 0.0% | - | 1.721 | 16.6 | -1.0 |
| solo_2 | left | 12 | 0.0% | 8.3% | - | 1.566 | 26.9 | +14.7 |
| solo_2 | straight | 12 | 0.0% | 0.0% | - | 1.891 | 23.8 | -10.2 |
| solo_2 | right | 12 | 0.0% | 8.3% | - | 1.990 | 29.1 | +20.6 |
| solo_2 | all | 36 | 0.0% | 5.6% | - | 1.784 | 24.2 | +8.4 |

Ablation, paired per task against stowed (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| solo_1 | -36.1 [-52.8, -19.4] pts | 13 | 0 | +15.5 [+11.1, +20.1] |
| solo_2 | -36.1 [-52.8, -19.4] pts | 13 | 0 | +19.7 [+15.7, +23.7] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| stowed | left | 83.3% | 50.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| stowed | straight | 16.7% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| stowed | right | 50.0% | 16.7% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
