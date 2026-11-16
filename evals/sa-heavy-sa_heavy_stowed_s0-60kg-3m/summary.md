# Spot-arm turn pilot: sa-heavy-sa_heavy_stowed_s0-60kg-3m

logs/marl2/sa_heavy_stowed_s0/model_4000.pt, iteration 4000, mappo, arms stowed. long 60 kg, 3 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| stowed | left | 40 | 0.0% | 0.0% | - | 2.770 | 66.4 | +59.6 |
| stowed | straight | 40 | 0.0% | 0.0% | - | 2.772 | 7.5 | +7.2 |
| stowed | right | 40 | 0.0% | 0.0% | - | 2.553 | 41.6 | -41.1 |
| stowed | all | 120 | 0.0% | 0.0% | - | 2.694 | 33.7 | +8.6 |
| solo_1 | left | 40 | 0.0% | 0.0% | - | 3.000 | 60.0 | +59.4 |
| solo_1 | straight | 40 | 0.0% | 0.0% | - | 3.000 | 0.1 | -1.0 |
| solo_1 | right | 40 | 0.0% | 0.0% | - | 3.000 | 61.0 | -61.1 |
| solo_1 | all | 120 | 0.0% | 0.0% | - | 3.000 | 60.0 | -0.9 |
| solo_2 | left | 40 | 0.0% | 0.0% | - | 2.945 | 64.4 | +62.0 |
| solo_2 | straight | 40 | 0.0% | 5.0% | - | 2.934 | 6.6 | +0.9 |
| solo_2 | right | 40 | 0.0% | 0.0% | - | 2.942 | 61.6 | -58.4 |
| solo_2 | all | 120 | 0.0% | 1.7% | - | 2.939 | 54.7 | +1.5 |

Ablation, paired per task against stowed (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| solo_1 | +0.0 [+0.0, +0.0] pts | 0 | 0 | +3.9 [+0.7, +7.3] |
| solo_2 | +0.0 [+0.0, +0.0] pts | 0 | 0 | +5.9 [+2.4, +9.6] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| stowed | left | 0.0% | 0.0% | 0.0% | 0.0% | 89.9% | 59.2% |
| stowed | straight | 0.0% | 0.0% | 0.0% | 0.0% | 91.7% | 70.7% |
| stowed | right | 0.0% | 0.0% | 0.0% | 0.0% | 71.9% | 82.8% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.1% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.3% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.3% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.8% | 23.4% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 10.0% | 22.5% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 3.3% | 13.6% |
