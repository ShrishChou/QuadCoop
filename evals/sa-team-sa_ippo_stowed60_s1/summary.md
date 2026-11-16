# Spot-arm turn pilot: sa-team-sa_ippo_stowed60_s1

logs/marl2/sa_ippo_stowed60_s1/model_2000.pt, iteration 2000, ippo, arms stowed. long 20 kg, 1 m, 20 placements per turn x swap, horizon 20 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| stowed | left | 40 | 100.0% | 0.0% | 4.8 | 0.058 | 2.3 | -1.3 |
| stowed | straight | 40 | 100.0% | 0.0% | 4.2 | 0.048 | 2.1 | +0.3 |
| stowed | right | 40 | 100.0% | 0.0% | 4.3 | 0.052 | 0.9 | -0.1 |
| stowed | all | 120 | 100.0% | 0.0% | 4.3 | 0.051 | 1.6 | -0.3 |
| solo_1 | left | 40 | 0.0% | 2.5% | - | 0.862 | 65.7 | +4.7 |
| solo_1 | straight | 40 | 0.0% | 2.5% | - | 0.941 | 35.9 | +27.2 |
| solo_1 | right | 40 | 0.0% | 0.0% | - | 1.000 | 60.0 | -50.3 |
| solo_1 | all | 120 | 0.0% | 1.7% | - | 1.000 | 60.0 | -6.1 |
| solo_2 | left | 40 | 0.0% | 0.0% | - | 0.779 | 78.8 | +58.1 |
| solo_2 | straight | 40 | 0.0% | 0.0% | - | 0.924 | 18.2 | +12.5 |
| solo_2 | right | 40 | 0.0% | 0.0% | - | 0.993 | 59.1 | -58.9 |
| solo_2 | all | 120 | 0.0% | 0.0% | - | 0.970 | 59.0 | +3.9 |

Ablation, paired per task against stowed (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| solo_1 | -100.0 [-100.0, -100.0] pts | 120 | 0 | +49.0 [+45.4, +52.7] |
| solo_2 | -100.0 [-100.0, -100.0] pts | 120 | 0 | +47.3 [+42.0, +52.4] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| stowed | left | 100.0% | 100.0% | 0.0% | 0.0% | 19.3% | 21.6% |
| stowed | straight | 100.0% | 100.0% | 0.0% | 0.0% | 25.8% | 16.7% |
| stowed | right | 100.0% | 100.0% | 0.0% | 0.0% | 18.5% | 20.2% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 1.5% | 3.2% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 2.9% | 2.5% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 1.2% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.3% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
