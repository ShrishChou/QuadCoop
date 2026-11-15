# Spot-arm turn pilot: sa-pilot-sa_ippo_learned_s0

logs/marl2/sa_ippo_learned_s0/model_2000.pt, iteration 2000, ippo, arms learned. long 20 kg, 1 m, 20 placements per turn x swap, horizon 20 s, seed 7100. Goal heading change as placed: left +30.0 to +30.0 deg, straight +0.0 to +0.0 deg, right -30.0 to -30.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 100.0% | 0.0% | 3.9 | 0.038 | 1.3 | -1.2 |
| both | straight | 40 | 100.0% | 0.0% | 3.9 | 0.039 | 1.2 | -0.0 |
| both | right | 40 | 100.0% | 0.0% | 4.1 | 0.045 | 1.6 | +1.7 |
| both | all | 120 | 100.0% | 0.0% | 4.0 | 0.040 | 1.4 | +0.1 |
| only_1 | left | 40 | 100.0% | 0.0% | 4.3 | 0.058 | 1.5 | +0.5 |
| only_1 | straight | 40 | 100.0% | 0.0% | 4.4 | 0.054 | 2.0 | +0.9 |
| only_1 | right | 40 | 100.0% | 0.0% | 4.7 | 0.062 | 2.5 | +1.6 |
| only_1 | all | 120 | 100.0% | 0.0% | 4.4 | 0.058 | 2.0 | +1.0 |
| only_2 | left | 40 | 100.0% | 0.0% | 4.2 | 0.055 | 1.8 | -1.8 |
| only_2 | straight | 40 | 100.0% | 0.0% | 4.1 | 0.059 | 1.9 | -1.3 |
| only_2 | right | 40 | 100.0% | 0.0% | 4.2 | 0.050 | 1.4 | +1.2 |
| only_2 | all | 120 | 100.0% | 0.0% | 4.2 | 0.053 | 1.7 | -0.6 |
| none | left | 40 | 100.0% | 0.0% | 4.7 | 0.065 | 1.9 | +0.1 |
| none | straight | 40 | 100.0% | 0.0% | 4.6 | 0.060 | 1.7 | -0.0 |
| none | right | 40 | 97.5% | 0.0% | 4.6 | 0.054 | 2.1 | +1.3 |
| none | all | 120 | 99.2% | 0.0% | 4.6 | 0.060 | 1.9 | +0.5 |

Arm ablation, paired per task against both arms active (the same policy; a locked arm stays stowed):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| only_1 | +0.0 [+0.0, +0.0] pts | 0 | 0 | +0.4 [+0.1, +0.7] |
| only_2 | +0.0 [+0.0, +0.0] pts | 0 | 0 | +0.2 [-0.0, +0.5] |
| none | -0.8 [-2.5, +0.0] pts | 1 | 0 | +0.5 [+0.1, +0.9] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 100.0% | 100.0% | 1.3% | 0.2% | 16.9% | 21.9% |
| both | straight | 100.0% | 100.0% | 0.4% | 0.4% | 24.3% | 22.8% |
| both | right | 100.0% | 100.0% | 0.9% | 0.1% | 27.3% | 24.9% |
| only_1 | left | 100.0% | 100.0% | 0.0% | 0.4% | 19.7% | 22.7% |
| only_1 | straight | 100.0% | 100.0% | 0.0% | 0.4% | 20.1% | 25.6% |
| only_1 | right | 100.0% | 100.0% | 0.1% | 0.0% | 26.4% | 23.7% |
| only_2 | left | 100.0% | 100.0% | 0.2% | 0.7% | 13.6% | 21.5% |
| only_2 | straight | 100.0% | 100.0% | 0.0% | 0.3% | 20.6% | 26.1% |
| only_2 | right | 100.0% | 100.0% | 1.3% | 0.0% | 27.3% | 26.0% |
| none | left | 100.0% | 100.0% | 0.0% | 0.0% | 17.5% | 21.5% |
| none | straight | 100.0% | 100.0% | 0.0% | 0.0% | 17.7% | 26.6% |
| none | right | 100.0% | 95.0% | 0.0% | 0.0% | 24.7% | 25.1% |
