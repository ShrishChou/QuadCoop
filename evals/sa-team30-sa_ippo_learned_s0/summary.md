# Spot-arm turn pilot: sa-team30-sa_ippo_learned_s0

logs/marl2/sa_ippo_learned_s0/model_2000.pt, iteration 2000, ippo, arms learned. long 20 kg, 1 m, 20 placements per turn x swap, horizon 20 s, seed 7100. Goal heading change as placed: left +30.0 to +30.0 deg, straight +0.0 to +0.0 deg, right -30.0 to -30.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 100.0% | 0.0% | 3.8 | 0.045 | 1.3 | -1.0 |
| both | straight | 40 | 100.0% | 0.0% | 3.9 | 0.044 | 1.3 | -0.3 |
| both | right | 40 | 100.0% | 0.0% | 4.1 | 0.050 | 1.6 | +1.4 |
| both | all | 120 | 100.0% | 0.0% | 4.0 | 0.045 | 1.4 | -0.0 |
| only_1 | left | 40 | 100.0% | 0.0% | 4.3 | 0.059 | 1.8 | +0.4 |
| only_1 | straight | 40 | 100.0% | 0.0% | 4.3 | 0.052 | 1.4 | +0.9 |
| only_1 | right | 40 | 100.0% | 0.0% | 4.6 | 0.061 | 2.5 | +1.5 |
| only_1 | all | 120 | 100.0% | 0.0% | 4.4 | 0.059 | 1.8 | +0.9 |
| only_2 | left | 40 | 100.0% | 0.0% | 4.2 | 0.065 | 1.5 | -1.6 |
| only_2 | straight | 40 | 100.0% | 0.0% | 4.2 | 0.062 | 1.6 | -1.1 |
| only_2 | right | 40 | 100.0% | 0.0% | 4.2 | 0.046 | 1.6 | +1.4 |
| only_2 | all | 120 | 100.0% | 0.0% | 4.2 | 0.054 | 1.5 | -0.4 |
| none | left | 40 | 100.0% | 0.0% | 4.9 | 0.064 | 1.4 | -0.3 |
| none | straight | 40 | 100.0% | 0.0% | 4.7 | 0.069 | 1.6 | -0.6 |
| none | right | 40 | 95.0% | 0.0% | 4.5 | 0.050 | 2.0 | +0.6 |
| none | all | 120 | 98.3% | 0.0% | 4.6 | 0.059 | 1.6 | -0.1 |
| solo_1 | left | 40 | 0.0% | 0.0% | - | 0.750 | 18.8 | +15.9 |
| solo_1 | straight | 40 | 0.0% | 0.0% | - | 0.874 | 23.8 | -15.2 |
| solo_1 | right | 40 | 0.0% | 0.0% | - | 0.661 | 75.5 | -23.6 |
| solo_1 | all | 120 | 0.0% | 0.0% | - | 0.816 | 31.0 | -7.6 |
| solo_2 | left | 40 | 0.0% | 2.5% | - | 0.814 | 53.8 | +17.8 |
| solo_2 | straight | 40 | 0.0% | 0.0% | - | 1.000 | 1.0 | +7.3 |
| solo_2 | right | 40 | 0.0% | 5.0% | - | 1.000 | 30.0 | -26.4 |
| solo_2 | all | 120 | 0.0% | 2.5% | - | 0.826 | 30.0 | -0.5 |

Ablation, paired per task against both (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| only_1 | +0.0 [+0.0, +0.0] pts | 0 | 0 | +0.3 [+0.0, +0.6] |
| only_2 | +0.0 [+0.0, +0.0] pts | 0 | 0 | +0.1 [-0.1, +0.3] |
| none | -1.7 [-4.2, +0.0] pts | 2 | 0 | +0.4 [+0.0, +0.9] |
| solo_1 | -100.0 [-100.0, -100.0] pts | 120 | 0 | +36.4 [+31.3, +41.8] |
| solo_2 | -100.0 [-100.0, -100.0] pts | 120 | 0 | +29.3 [+24.8, +33.9] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 100.0% | 100.0% | 0.7% | 0.4% | 16.9% | 22.2% |
| both | straight | 100.0% | 100.0% | 0.2% | 0.4% | 23.5% | 23.1% |
| both | right | 100.0% | 100.0% | 1.6% | 0.1% | 26.6% | 24.9% |
| only_1 | left | 100.0% | 100.0% | 0.0% | 0.6% | 17.9% | 23.5% |
| only_1 | straight | 100.0% | 100.0% | 0.0% | 0.1% | 20.8% | 25.5% |
| only_1 | right | 100.0% | 100.0% | 0.1% | 0.0% | 25.4% | 26.7% |
| only_2 | left | 100.0% | 100.0% | 0.1% | 0.5% | 13.6% | 22.7% |
| only_2 | straight | 100.0% | 100.0% | 0.0% | 0.3% | 20.6% | 26.2% |
| only_2 | right | 100.0% | 100.0% | 2.2% | 0.0% | 27.1% | 26.4% |
| none | left | 100.0% | 100.0% | 0.0% | 0.0% | 17.3% | 21.7% |
| none | straight | 100.0% | 100.0% | 0.0% | 0.0% | 16.6% | 25.2% |
| none | right | 100.0% | 90.0% | 0.0% | 0.0% | 24.5% | 24.5% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 3.3% | 2.2% |
| solo_1 | straight | 0.0% | 0.0% | 0.1% | 0.1% | 4.5% | 0.5% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 5.9% | 0.4% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.1% |
