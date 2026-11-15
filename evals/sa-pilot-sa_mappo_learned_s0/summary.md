# Spot-arm turn pilot: sa-pilot-sa_mappo_learned_s0

logs/marl2/sa_mappo_learned_s0/model_2000.pt, iteration 2000, mappo, arms learned. long 20 kg, 1 m, 20 placements per turn x swap, horizon 20 s, seed 7100. Goal heading change as placed: left +30.0 to +30.0 deg, straight +0.0 to +0.0 deg, right -30.0 to -30.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 97.5% | 0.0% | 3.6 | 0.056 | 2.4 | -2.2 |
| both | straight | 40 | 97.5% | 2.5% | 3.8 | 0.057 | 1.8 | -1.3 |
| both | right | 40 | 95.0% | 0.0% | 3.9 | 0.041 | 0.8 | -0.7 |
| both | all | 120 | 96.7% | 0.8% | 3.8 | 0.052 | 1.6 | -1.4 |
| only_1 | left | 40 | 97.5% | 0.0% | 3.8 | 0.065 | 1.4 | -0.4 |
| only_1 | straight | 40 | 100.0% | 0.0% | 4.0 | 0.057 | 1.9 | -1.0 |
| only_1 | right | 40 | 100.0% | 0.0% | 4.2 | 0.063 | 1.6 | +0.5 |
| only_1 | all | 120 | 99.2% | 0.0% | 4.0 | 0.062 | 1.7 | -0.3 |
| only_2 | left | 40 | 95.0% | 0.0% | 3.9 | 0.058 | 2.0 | -0.3 |
| only_2 | straight | 40 | 92.5% | 2.5% | 4.1 | 0.040 | 1.3 | +0.2 |
| only_2 | right | 40 | 100.0% | 0.0% | 4.2 | 0.049 | 1.8 | -1.0 |
| only_2 | all | 120 | 95.8% | 0.8% | 4.0 | 0.049 | 1.7 | -0.3 |
| none | left | 40 | 100.0% | 0.0% | 4.0 | 0.067 | 0.9 | +0.8 |
| none | straight | 40 | 100.0% | 0.0% | 4.7 | 0.055 | 1.5 | +0.4 |
| none | right | 40 | 97.5% | 0.0% | 4.6 | 0.065 | 1.0 | +0.5 |
| none | all | 120 | 99.2% | 0.0% | 4.3 | 0.062 | 1.1 | +0.6 |

Arm ablation, paired per task against both arms active (the same policy; a locked arm stays stowed):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| only_1 | +2.5 [-0.8, +6.7] pts | 1 | 4 | -0.0 [-0.4, +0.4] |
| only_2 | -0.8 [-5.8, +4.2] pts | 5 | 4 | -0.0 [-0.4, +0.3] |
| none | +2.5 [-0.8, +6.7] pts | 1 | 4 | -0.4 [-0.8, -0.1] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 95.0% | 100.0% | 0.2% | 0.4% | 20.7% | 15.8% |
| both | straight | 95.0% | 100.0% | 0.3% | 0.1% | 18.7% | 13.2% |
| both | right | 90.0% | 100.0% | 0.0% | 0.1% | 19.8% | 23.3% |
| only_1 | left | 95.0% | 100.0% | 0.0% | 0.0% | 20.9% | 19.1% |
| only_1 | straight | 100.0% | 100.0% | 0.0% | 0.0% | 16.6% | 13.7% |
| only_1 | right | 100.0% | 100.0% | 0.0% | 0.0% | 18.3% | 21.6% |
| only_2 | left | 90.0% | 100.0% | 0.0% | 0.0% | 23.0% | 17.3% |
| only_2 | straight | 85.0% | 100.0% | 0.0% | 0.0% | 16.0% | 16.5% |
| only_2 | right | 100.0% | 100.0% | 0.0% | 0.0% | 21.8% | 25.4% |
| none | left | 100.0% | 100.0% | 0.0% | 0.0% | 22.9% | 15.0% |
| none | straight | 100.0% | 100.0% | 0.0% | 0.0% | 13.4% | 12.6% |
| none | right | 100.0% | 95.0% | 0.0% | 0.0% | 18.8% | 22.7% |
