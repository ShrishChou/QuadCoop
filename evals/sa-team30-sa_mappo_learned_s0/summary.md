# Spot-arm turn pilot: sa-team30-sa_mappo_learned_s0

logs/marl2/sa_mappo_learned_s0/model_2000.pt, iteration 2000, mappo, arms learned. long 20 kg, 1 m, 20 placements per turn x swap, horizon 20 s, seed 7100. Goal heading change as placed: left +30.0 to +30.0 deg, straight +0.0 to +0.0 deg, right -30.0 to -30.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 97.5% | 2.5% | 3.7 | 0.062 | 1.9 | -1.7 |
| both | straight | 40 | 90.0% | 0.0% | 3.8 | 0.059 | 1.4 | -1.7 |
| both | right | 40 | 100.0% | 0.0% | 4.0 | 0.043 | 1.3 | -0.9 |
| both | all | 120 | 95.8% | 0.8% | 3.8 | 0.049 | 1.6 | -1.4 |
| only_1 | left | 40 | 97.5% | 0.0% | 3.9 | 0.063 | 1.6 | -0.5 |
| only_1 | straight | 40 | 100.0% | 0.0% | 4.0 | 0.056 | 1.7 | -0.7 |
| only_1 | right | 40 | 100.0% | 0.0% | 4.2 | 0.061 | 1.8 | +0.9 |
| only_1 | all | 120 | 99.2% | 0.0% | 4.0 | 0.061 | 1.7 | -0.1 |
| only_2 | left | 40 | 92.5% | 0.0% | 3.9 | 0.062 | 1.6 | -0.7 |
| only_2 | straight | 40 | 95.0% | 0.0% | 4.2 | 0.046 | 1.4 | -0.2 |
| only_2 | right | 40 | 97.5% | 0.0% | 4.1 | 0.044 | 1.9 | -1.0 |
| only_2 | all | 120 | 95.0% | 0.0% | 4.1 | 0.047 | 1.6 | -0.6 |
| none | left | 40 | 97.5% | 0.0% | 4.0 | 0.070 | 1.2 | +0.6 |
| none | straight | 40 | 100.0% | 0.0% | 4.6 | 0.050 | 1.6 | +0.4 |
| none | right | 40 | 100.0% | 0.0% | 4.4 | 0.080 | 0.8 | +0.5 |
| none | all | 120 | 99.2% | 0.0% | 4.2 | 0.063 | 1.1 | +0.5 |
| solo_1 | left | 40 | 0.0% | 2.5% | - | 0.977 | 26.9 | +32.8 |
| solo_1 | straight | 40 | 0.0% | 0.0% | - | 0.851 | 26.2 | +1.6 |
| solo_1 | right | 40 | 0.0% | 0.0% | - | 0.777 | 62.3 | -19.9 |
| solo_1 | all | 120 | 0.0% | 0.8% | - | 0.898 | 31.2 | +4.8 |
| solo_2 | left | 40 | 0.0% | 0.0% | - | 1.000 | 30.0 | +30.0 |
| solo_2 | straight | 40 | 0.0% | 0.0% | - | 1.000 | 0.0 | +0.0 |
| solo_2 | right | 40 | 0.0% | 0.0% | - | 1.000 | 30.0 | -30.8 |
| solo_2 | all | 120 | 0.0% | 0.0% | - | 1.000 | 30.0 | -0.3 |

Ablation, paired per task against both (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| only_1 | +3.3 [+0.0, +7.5] pts | 1 | 5 | -0.1 [-0.4, +0.3] |
| only_2 | -0.8 [-6.7, +5.0] pts | 6 | 5 | -0.2 [-0.5, +0.2] |
| none | +3.3 [+0.0, +7.5] pts | 1 | 5 | -0.5 [-0.8, -0.1] |
| solo_1 | -95.8 [-99.2, -91.7] pts | 115 | 0 | +37.6 [+33.3, +42.0] |
| solo_2 | -95.8 [-99.2, -91.7] pts | 115 | 0 | +18.2 [+15.5, +20.8] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 95.0% | 100.0% | 0.2% | 0.3% | 20.9% | 16.3% |
| both | straight | 90.0% | 90.0% | 0.4% | 0.2% | 16.5% | 14.1% |
| both | right | 100.0% | 100.0% | 0.1% | 0.1% | 19.5% | 22.8% |
| only_1 | left | 95.0% | 100.0% | 0.0% | 0.0% | 19.8% | 18.0% |
| only_1 | straight | 100.0% | 100.0% | 0.0% | 0.1% | 16.4% | 15.1% |
| only_1 | right | 100.0% | 100.0% | 0.0% | 0.0% | 19.2% | 22.7% |
| only_2 | left | 95.0% | 90.0% | 0.0% | 0.0% | 21.7% | 17.8% |
| only_2 | straight | 95.0% | 95.0% | 0.0% | 0.0% | 16.4% | 16.7% |
| only_2 | right | 95.0% | 100.0% | 0.0% | 0.1% | 20.1% | 24.7% |
| none | left | 100.0% | 95.0% | 0.0% | 0.0% | 22.1% | 15.7% |
| none | straight | 100.0% | 100.0% | 0.0% | 0.0% | 14.3% | 12.3% |
| none | right | 100.0% | 100.0% | 0.0% | 0.0% | 19.1% | 23.2% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 4.6% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.9% | 0.0% | 5.4% | 0.0% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 6.8% | 0.4% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
