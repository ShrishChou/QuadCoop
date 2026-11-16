# Spot-arm turn pilot: sa-heavy-sa_heavy_solo_s0-60kg-3m

logs/marl2/sa_heavy_solo_s0/model_4000.pt, iteration 4000, mappo, arms learned. long 60 kg, 3 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 0.0% | 37.5% | - | 2.866 | 53.0 | +51.2 |
| both | straight | 40 | 0.0% | 17.5% | - | 2.859 | 8.7 | -10.2 |
| both | right | 40 | 0.0% | 22.5% | - | 2.870 | 67.7 | -69.1 |
| both | all | 120 | 0.0% | 25.8% | - | 2.868 | 53.0 | -9.3 |
| only_1 | left | 40 | 0.0% | 5.0% | - | 2.969 | 56.5 | +54.4 |
| only_1 | straight | 40 | 0.0% | 2.5% | - | 2.969 | 4.3 | -5.2 |
| only_1 | right | 40 | 0.0% | 5.0% | - | 2.942 | 65.2 | -65.5 |
| only_1 | all | 120 | 0.0% | 4.2% | - | 2.967 | 56.5 | -5.4 |
| only_2 | left | 40 | 0.0% | 7.5% | - | 2.872 | 56.4 | +52.4 |
| only_2 | straight | 40 | 0.0% | 25.0% | - | 2.880 | 5.2 | -6.9 |
| only_2 | right | 40 | 0.0% | 17.5% | - | 2.918 | 63.4 | -66.2 |
| only_2 | all | 120 | 0.0% | 16.7% | - | 2.889 | 56.4 | -6.9 |
| none | left | 40 | 0.0% | 2.5% | - | 2.958 | 54.7 | +54.2 |
| none | straight | 40 | 0.0% | 2.5% | - | 2.946 | 5.3 | -4.7 |
| none | right | 40 | 0.0% | 0.0% | - | 3.002 | 61.1 | -63.2 |
| none | all | 120 | 0.0% | 1.7% | - | 2.952 | 54.7 | -4.6 |
| solo_1 | left | 40 | 0.0% | 0.0% | - | 2.895 | 49.2 | +48.5 |
| solo_1 | straight | 40 | 0.0% | 0.0% | - | 2.898 | 5.8 | -7.9 |
| solo_1 | right | 40 | 0.0% | 0.0% | - | 2.900 | 66.6 | -51.5 |
| solo_1 | all | 120 | 0.0% | 0.0% | - | 2.896 | 49.2 | -3.6 |
| solo_2 | left | 40 | 0.0% | 0.0% | - | 2.984 | 58.3 | +58.2 |
| solo_2 | straight | 40 | 0.0% | 0.0% | - | 2.985 | 2.3 | -2.2 |
| solo_2 | right | 40 | 0.0% | 2.5% | - | 2.988 | 61.4 | -61.6 |
| solo_2 | all | 120 | 0.0% | 0.8% | - | 2.984 | 58.3 | -1.9 |

Ablation, paired per task against both (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| only_1 | +0.0 [+0.0, +0.0] pts | 0 | 0 | -2.0 [-3.7, -0.3] |
| only_2 | +0.0 [+0.0, +0.0] pts | 0 | 0 | -1.7 [-3.4, +0.0] |
| none | +0.0 [+0.0, +0.0] pts | 0 | 0 | -3.1 [-4.6, -1.5] |
| solo_1 | +0.0 [+0.0, +0.0] pts | 0 | 0 | -1.9 [-3.8, +0.0] |
| solo_2 | +0.0 [+0.0, +0.0] pts | 0 | 0 | -3.1 [-4.8, -1.2] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 0.0% | 0.0% | 14.2% | 3.6% | 20.8% | 7.2% |
| both | straight | 0.0% | 0.0% | 5.2% | 2.7% | 8.7% | 2.5% |
| both | right | 0.0% | 0.0% | 8.3% | 1.4% | 8.8% | 5.0% |
| only_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 15.9% | 0.1% |
| only_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 12.8% | 0.0% |
| only_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 22.2% | 0.7% |
| only_2 | left | 0.0% | 0.0% | 0.0% | 0.5% | 40.4% | 15.8% |
| only_2 | straight | 0.0% | 0.0% | 0.0% | 0.4% | 26.9% | 5.7% |
| only_2 | right | 0.0% | 0.0% | 0.0% | 0.2% | 26.3% | 2.7% |
| none | left | 0.0% | 0.0% | 0.0% | 0.1% | 35.1% | 4.8% |
| none | straight | 0.0% | 0.0% | 0.0% | 0.0% | 20.5% | 0.0% |
| none | right | 0.0% | 0.0% | 0.0% | 0.0% | 26.6% | 0.0% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 24.1% | 22.7% |
| solo_1 | straight | 0.0% | 0.0% | 0.5% | 0.0% | 34.0% | 8.5% |
| solo_1 | right | 0.0% | 0.0% | 9.7% | 0.0% | 36.4% | 29.4% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.5% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.4% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.5% |
