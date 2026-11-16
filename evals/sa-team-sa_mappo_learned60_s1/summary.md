# Spot-arm turn pilot: sa-team-sa_mappo_learned60_s1

logs/marl2/sa_mappo_learned60_s1/model_2000.pt, iteration 2000, mappo, arms learned. long 20 kg, 1 m, 20 placements per turn x swap, horizon 20 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 100.0% | 0.0% | 4.1 | 0.042 | 1.1 | -0.3 |
| both | straight | 40 | 100.0% | 0.0% | 4.0 | 0.046 | 1.3 | +0.9 |
| both | right | 40 | 100.0% | 0.0% | 4.4 | 0.059 | 1.1 | -0.2 |
| both | all | 120 | 100.0% | 0.0% | 4.2 | 0.049 | 1.1 | +0.2 |
| only_1 | left | 40 | 100.0% | 0.0% | 4.1 | 0.050 | 1.3 | -0.6 |
| only_1 | straight | 40 | 100.0% | 0.0% | 3.9 | 0.045 | 1.6 | -0.8 |
| only_1 | right | 40 | 100.0% | 0.0% | 4.2 | 0.046 | 1.4 | -0.2 |
| only_1 | all | 120 | 100.0% | 0.0% | 4.1 | 0.048 | 1.4 | -0.5 |
| only_2 | left | 40 | 100.0% | 0.0% | 4.7 | 0.061 | 1.0 | +0.5 |
| only_2 | straight | 40 | 100.0% | 0.0% | 4.4 | 0.059 | 1.0 | +1.0 |
| only_2 | right | 40 | 97.5% | 0.0% | 4.4 | 0.051 | 1.3 | -0.3 |
| only_2 | all | 120 | 99.2% | 0.0% | 4.5 | 0.057 | 1.1 | +0.4 |
| none | left | 40 | 100.0% | 0.0% | 4.8 | 0.054 | 1.3 | -0.8 |
| none | straight | 40 | 100.0% | 0.0% | 4.1 | 0.038 | 1.6 | -0.2 |
| none | right | 40 | 97.5% | 0.0% | 4.4 | 0.046 | 1.7 | -0.1 |
| none | all | 120 | 99.2% | 0.0% | 4.3 | 0.048 | 1.5 | -0.3 |
| solo_1 | left | 40 | 0.0% | 0.0% | - | 1.000 | 60.0 | +60.5 |
| solo_1 | straight | 40 | 0.0% | 0.0% | - | 0.988 | 31.1 | -8.8 |
| solo_1 | right | 40 | 0.0% | 0.0% | - | 1.675 | 44.4 | +0.9 |
| solo_1 | all | 120 | 0.0% | 0.0% | - | 1.000 | 50.1 | +17.5 |
| solo_2 | left | 40 | 0.0% | 0.0% | - | 1.000 | 60.0 | +51.4 |
| solo_2 | straight | 40 | 0.0% | 0.0% | - | 0.933 | 1.5 | -3.9 |
| solo_2 | right | 40 | 0.0% | 0.0% | - | 1.000 | 60.0 | -60.1 |
| solo_2 | all | 120 | 0.0% | 0.0% | - | 1.000 | 60.0 | -4.2 |

Ablation, paired per task against both (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| only_1 | +0.0 [+0.0, +0.0] pts | 0 | 0 | +0.1 [-0.2, +0.4] |
| only_2 | -0.8 [-2.5, +0.0] pts | 1 | 0 | +0.0 [-0.3, +0.3] |
| none | -0.8 [-2.5, +0.0] pts | 1 | 0 | +0.5 [-0.0, +1.3] |
| solo_1 | -100.0 [-100.0, -100.0] pts | 120 | 0 | +43.2 [+39.2, +47.2] |
| solo_2 | -100.0 [-100.0, -100.0] pts | 120 | 0 | +38.0 [+33.1, +42.8] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 100.0% | 100.0% | 1.1% | 0.5% | 26.8% | 21.0% |
| both | straight | 100.0% | 100.0% | 0.2% | 0.5% | 20.0% | 21.0% |
| both | right | 100.0% | 100.0% | 0.1% | 2.6% | 18.8% | 28.5% |
| only_1 | left | 100.0% | 100.0% | 0.0% | 0.1% | 24.3% | 23.3% |
| only_1 | straight | 100.0% | 100.0% | 0.0% | 1.1% | 21.6% | 23.6% |
| only_1 | right | 100.0% | 100.0% | 0.0% | 0.1% | 18.7% | 29.4% |
| only_2 | left | 100.0% | 100.0% | 0.8% | 0.1% | 31.1% | 21.5% |
| only_2 | straight | 100.0% | 100.0% | 0.2% | 0.0% | 19.7% | 21.6% |
| only_2 | right | 95.0% | 100.0% | 0.2% | 2.7% | 18.4% | 27.7% |
| none | left | 100.0% | 100.0% | 0.0% | 0.0% | 26.8% | 21.8% |
| none | straight | 100.0% | 100.0% | 0.0% | 0.0% | 20.8% | 22.2% |
| none | right | 100.0% | 95.0% | 0.0% | 0.0% | 18.0% | 30.1% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 18.3% | 3.3% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 10.4% | 1.1% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.2% | 0.0% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.3% | 0.1% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
