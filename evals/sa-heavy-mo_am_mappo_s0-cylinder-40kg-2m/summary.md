# Spot-arm turn pilot: sa-heavy-mo_am_mappo_s0-cylinder-40kg-2m

logs/marl2/mo_am_mappo_s0/model_4000.pt, iteration 4000, mappo, arms learned. cylinder 40 kg, 2 m, 6 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 12 | 0.0% | 0.0% | - | 0.247 | 48.7 | +47.0 |
| both | straight | 12 | 33.3% | 0.0% | 6.4 | 0.251 | 5.2 | -4.7 |
| both | right | 12 | 0.0% | 8.3% | - | 0.325 | 58.4 | -54.6 |
| both | all | 36 | 11.1% | 2.8% | 6.4 | 0.252 | 45.6 | -4.1 |
| none | left | 12 | 0.0% | 8.3% | - | 0.247 | 53.1 | +52.3 |
| none | straight | 12 | 8.3% | 0.0% | 6.7 | 0.234 | 5.5 | -4.8 |
| none | right | 12 | 0.0% | 25.0% | - | 0.285 | 58.6 | -59.5 |
| none | all | 36 | 2.8% | 11.1% | 6.7 | 0.266 | 52.7 | -4.0 |
| solo_1 | left | 12 | 0.0% | 8.3% | - | 1.357 | 56.0 | +53.6 |
| solo_1 | straight | 12 | 0.0% | 0.0% | - | 1.456 | 3.0 | -8.1 |
| solo_1 | right | 12 | 0.0% | 0.0% | - | 1.361 | 71.8 | -56.2 |
| solo_1 | all | 36 | 0.0% | 2.8% | - | 1.357 | 55.8 | -3.6 |
| solo_2 | left | 12 | 0.0% | 0.0% | - | 1.565 | 64.1 | +64.5 |
| solo_2 | straight | 12 | 0.0% | 0.0% | - | 0.867 | 10.0 | +3.1 |
| solo_2 | right | 12 | 0.0% | 0.0% | - | 1.330 | 55.5 | -55.8 |
| solo_2 | all | 36 | 0.0% | 0.0% | - | 1.320 | 55.1 | +3.9 |

Ablation, paired per task against both (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| none | -8.3 [-19.4, +0.0] pts | 3 | 0 | +3.8 [+0.9, +7.1] |
| solo_1 | -11.1 [-22.2, -2.8] pts | 4 | 0 | +7.7 [+3.1, +12.5] |
| solo_2 | -11.1 [-22.2, -2.8] pts | 4 | 0 | +7.7 [+4.1, +11.5] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.2% | 9.1% |
| both | straight | 33.3% | 33.3% | 0.0% | 0.0% | 12.9% | 15.4% |
| both | right | 0.0% | 0.0% | 0.0% | 0.0% | 27.0% | 14.2% |
| none | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.2% | 6.9% |
| none | straight | 16.7% | 0.0% | 0.0% | 0.0% | 27.0% | 19.8% |
| none | right | 0.0% | 0.0% | 0.0% | 0.0% | 28.3% | 19.7% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 8.7% | 0.3% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 6.8% | 4.4% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.6% | 0.2% |
