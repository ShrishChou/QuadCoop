# Spot-arm turn pilot: sa-team-sa_mappo_stowed60_s1

logs/marl2/sa_mappo_stowed60_s1/model_2000.pt, iteration 2000, mappo, arms stowed. long 20 kg, 1 m, 20 placements per turn x swap, horizon 20 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| stowed | left | 40 | 100.0% | 0.0% | 4.2 | 0.041 | 0.6 | +0.4 |
| stowed | straight | 40 | 100.0% | 0.0% | 4.2 | 0.057 | 2.1 | +1.9 |
| stowed | right | 40 | 90.0% | 0.0% | 4.5 | 0.072 | 1.8 | +1.9 |
| stowed | all | 120 | 96.7% | 0.0% | 4.2 | 0.055 | 1.3 | +1.4 |
| solo_1 | left | 40 | 0.0% | 0.0% | - | 1.000 | 60.0 | +60.0 |
| solo_1 | straight | 40 | 0.0% | 0.0% | - | 0.725 | 15.0 | +5.4 |
| solo_1 | right | 40 | 0.0% | 0.0% | - | 0.787 | 77.7 | -12.9 |
| solo_1 | all | 120 | 0.0% | 0.0% | - | 0.842 | 60.0 | +17.5 |
| solo_2 | left | 40 | 0.0% | 0.0% | - | 0.492 | 65.4 | -19.8 |
| solo_2 | straight | 40 | 0.0% | 0.0% | - | 0.569 | 32.0 | +36.3 |
| solo_2 | right | 40 | 0.0% | 0.0% | - | 0.544 | 29.7 | +0.2 |
| solo_2 | all | 120 | 0.0% | 0.0% | - | 0.531 | 50.1 | +5.6 |

Ablation, paired per task against stowed (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| solo_1 | -96.7 [-99.2, -93.3] pts | 116 | 0 | +49.3 [+44.1, +54.2] |
| solo_2 | -96.7 [-99.2, -93.3] pts | 116 | 0 | +43.7 [+38.8, +48.7] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| stowed | left | 100.0% | 100.0% | 0.0% | 0.0% | 23.4% | 24.8% |
| stowed | straight | 100.0% | 100.0% | 0.0% | 0.0% | 15.5% | 29.2% |
| stowed | right | 80.0% | 100.0% | 0.0% | 0.0% | 14.7% | 25.6% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 1.9% | 4.3% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.1% | 0.0% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.2% | 0.0% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.2% | 0.2% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 1.2% | 5.1% |
