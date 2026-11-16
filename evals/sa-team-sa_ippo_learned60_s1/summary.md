# Spot-arm turn pilot: sa-team-sa_ippo_learned60_s1

logs/marl2/sa_ippo_learned60_s1/model_2000.pt, iteration 2000, ippo, arms learned. long 20 kg, 1 m, 20 placements per turn x swap, horizon 20 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 100.0% | 0.0% | 4.3 | 0.075 | 1.7 | +0.5 |
| both | straight | 40 | 92.5% | 0.0% | 3.9 | 0.049 | 1.6 | +0.0 |
| both | right | 40 | 100.0% | 0.0% | 4.4 | 0.061 | 1.8 | +1.4 |
| both | all | 120 | 97.5% | 0.0% | 4.2 | 0.061 | 1.7 | +0.7 |
| only_1 | left | 40 | 97.5% | 0.0% | 4.6 | 0.066 | 1.7 | +1.0 |
| only_1 | straight | 40 | 100.0% | 0.0% | 4.1 | 0.063 | 1.7 | +1.0 |
| only_1 | right | 40 | 100.0% | 0.0% | 4.2 | 0.062 | 1.3 | +1.4 |
| only_1 | all | 120 | 99.2% | 0.0% | 4.4 | 0.063 | 1.7 | +1.1 |
| only_2 | left | 40 | 100.0% | 0.0% | 4.3 | 0.047 | 1.7 | +1.0 |
| only_2 | straight | 40 | 100.0% | 0.0% | 4.0 | 0.048 | 1.4 | +0.2 |
| only_2 | right | 40 | 100.0% | 0.0% | 4.4 | 0.055 | 2.4 | +1.7 |
| only_2 | all | 120 | 100.0% | 0.0% | 4.3 | 0.048 | 1.7 | +1.0 |
| none | left | 40 | 97.5% | 0.0% | 4.6 | 0.064 | 2.3 | +2.3 |
| none | straight | 40 | 97.5% | 0.0% | 4.1 | 0.056 | 2.7 | +2.5 |
| none | right | 40 | 97.5% | 0.0% | 4.3 | 0.056 | 3.2 | +2.9 |
| none | all | 120 | 97.5% | 0.0% | 4.3 | 0.058 | 2.6 | +2.6 |
| solo_1 | left | 40 | 0.0% | 0.0% | - | 1.000 | 60.0 | +60.2 |
| solo_1 | straight | 40 | 0.0% | 0.0% | - | 1.000 | 0.0 | +0.0 |
| solo_1 | right | 40 | 0.0% | 0.0% | - | 1.000 | 60.0 | -60.0 |
| solo_1 | all | 120 | 0.0% | 0.0% | - | 1.000 | 60.0 | +0.1 |
| solo_2 | left | 40 | 0.0% | 0.0% | - | 1.024 | 24.0 | +24.0 |
| solo_2 | straight | 40 | 0.0% | 0.0% | - | 0.516 | 42.5 | +28.3 |
| solo_2 | right | 40 | 0.0% | 0.0% | - | 1.000 | 60.0 | -60.0 |
| solo_2 | all | 120 | 0.0% | 0.0% | - | 1.000 | 44.7 | -2.6 |

Ablation, paired per task against both (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| only_1 | +1.7 [-1.7, +5.0] pts | 1 | 3 | +0.1 [-0.2, +0.4] |
| only_2 | +2.5 [+0.0, +5.8] pts | 0 | 3 | +0.2 [-0.1, +0.5] |
| none | +0.0 [-4.2, +4.2] pts | 3 | 3 | +0.9 [+0.5, +1.2] |
| solo_1 | -97.5 [-100.0, -94.2] pts | 117 | 0 | +38.2 [+33.0, +43.2] |
| solo_2 | -97.5 [-100.0, -94.2] pts | 117 | 0 | +36.7 [+32.8, +40.6] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 100.0% | 100.0% | 0.0% | 0.2% | 24.4% | 20.3% |
| both | straight | 100.0% | 85.0% | 0.5% | 0.4% | 22.6% | 13.5% |
| both | right | 100.0% | 100.0% | 0.0% | 0.9% | 9.9% | 22.7% |
| only_1 | left | 100.0% | 95.0% | 0.0% | 1.6% | 26.8% | 19.6% |
| only_1 | straight | 100.0% | 100.0% | 0.5% | 0.6% | 23.5% | 13.7% |
| only_1 | right | 100.0% | 100.0% | 0.0% | 1.7% | 7.6% | 17.9% |
| only_2 | left | 100.0% | 100.0% | 0.2% | 0.0% | 25.3% | 16.1% |
| only_2 | straight | 100.0% | 100.0% | 0.0% | 0.0% | 25.2% | 14.1% |
| only_2 | right | 100.0% | 100.0% | 0.0% | 0.0% | 8.5% | 23.5% |
| none | left | 100.0% | 95.0% | 0.0% | 0.0% | 26.3% | 17.2% |
| none | straight | 100.0% | 95.0% | 0.0% | 0.0% | 21.9% | 13.0% |
| none | right | 100.0% | 95.0% | 0.0% | 0.0% | 8.4% | 17.7% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | left | 0.0% | 0.0% | 6.6% | 0.0% | 0.1% | 1.3% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 1.6% | 0.0% | 0.5% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
