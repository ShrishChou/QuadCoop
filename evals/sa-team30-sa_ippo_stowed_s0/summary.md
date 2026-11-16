# Spot-arm turn pilot: sa-team30-sa_ippo_stowed_s0

logs/marl2/sa_ippo_stowed_s0/model_2000.pt, iteration 2000, ippo, arms stowed. long 20 kg, 1 m, 20 placements per turn x swap, horizon 20 s, seed 7100. Goal heading change as placed: left +30.0 to +30.0 deg, straight +0.0 to +0.0 deg, right -30.0 to -30.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| stowed | left | 40 | 75.0% | 0.0% | 4.3 | 0.078 | 1.0 | +1.7 |
| stowed | straight | 40 | 100.0% | 0.0% | 4.1 | 0.045 | 1.3 | +1.2 |
| stowed | right | 40 | 95.0% | 0.0% | 4.2 | 0.043 | 1.2 | +0.3 |
| stowed | all | 120 | 90.0% | 0.0% | 4.2 | 0.049 | 1.0 | +1.1 |
| solo_1 | left | 40 | 0.0% | 0.0% | - | 0.729 | 21.3 | +12.2 |
| solo_1 | straight | 40 | 0.0% | 0.0% | - | 0.641 | 29.6 | -26.4 |
| solo_1 | right | 40 | 0.0% | 0.0% | - | 0.615 | 62.8 | -58.1 |
| solo_1 | all | 120 | 0.0% | 0.0% | - | 0.645 | 35.5 | -24.1 |
| solo_2 | left | 40 | 0.0% | 0.0% | - | 0.882 | 81.2 | -26.4 |
| solo_2 | straight | 40 | 0.0% | 0.0% | - | 0.846 | 20.3 | -1.0 |
| solo_2 | right | 40 | 0.0% | 0.0% | - | 0.988 | 28.4 | -2.1 |
| solo_2 | all | 120 | 0.0% | 0.0% | - | 0.892 | 28.9 | -9.8 |

Ablation, paired per task against stowed (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| solo_1 | -90.0 [-95.0, -84.2] pts | 108 | 0 | +32.9 [+28.9, +36.9] |
| solo_2 | -90.0 [-95.0, -84.2] pts | 108 | 0 | +36.7 [+31.8, +42.0] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| stowed | left | 100.0% | 50.0% | 0.0% | 0.0% | 16.6% | 16.2% |
| stowed | straight | 100.0% | 100.0% | 0.0% | 0.0% | 18.7% | 21.6% |
| stowed | right | 100.0% | 90.0% | 0.0% | 0.0% | 23.6% | 22.9% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.6% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.4% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.4% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.1% | 2.4% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.1% | 17.3% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 10.8% |
