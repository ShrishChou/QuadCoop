# Spot-arm turn pilot: sa-heavy-mo_am_mappo_s0-cube-40kg-2m

logs/marl2/mo_am_mappo_s0/model_4000.pt, iteration 4000, mappo, arms learned. cube 40 kg, 2 m, 6 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left -30.0 to -30.0 deg, straight +0.0 to +0.0 deg, right +30.0 to +30.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 12 | 16.7% | 8.3% | 10.4 | 0.189 | 5.8 | -0.6 |
| both | straight | 12 | 8.3% | 0.0% | 18.2 | 0.480 | 4.0 | +1.7 |
| both | right | 12 | 8.3% | 0.0% | 24.1 | 0.785 | 3.4 | +4.7 |
| both | all | 36 | 11.1% | 2.8% | 18.2 | 0.418 | 3.4 | +2.0 |
| none | left | 12 | 0.0% | 0.0% | - | 0.275 | 6.0 | +3.7 |
| none | straight | 12 | 0.0% | 25.0% | - | 0.843 | 11.3 | +10.6 |
| none | right | 12 | 0.0% | 0.0% | - | 0.528 | 7.8 | +6.7 |
| none | all | 36 | 0.0% | 8.3% | - | 0.540 | 6.0 | +7.0 |
| solo_1 | left | 12 | 0.0% | 0.0% | - | 1.953 | 33.3 | -23.6 |
| solo_1 | straight | 12 | 0.0% | 0.0% | - | 1.936 | 27.0 | -14.3 |
| solo_1 | right | 12 | 0.0% | 0.0% | - | 1.903 | 15.7 | +9.1 |
| solo_1 | all | 36 | 0.0% | 0.0% | - | 1.934 | 25.3 | -9.6 |
| solo_2 | left | 12 | 0.0% | 0.0% | - | 1.883 | 30.1 | -24.5 |
| solo_2 | straight | 12 | 0.0% | 16.7% | - | 1.891 | 10.4 | -4.1 |
| solo_2 | right | 12 | 0.0% | 0.0% | - | 1.970 | 29.6 | +4.5 |
| solo_2 | all | 36 | 0.0% | 5.6% | - | 1.883 | 27.8 | -8.0 |

Ablation, paired per task against both (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| none | -11.1 [-22.2, -2.8] pts | 4 | 0 | +3.6 [+0.3, +6.7] |
| solo_1 | -11.1 [-22.2, -2.8] pts | 4 | 0 | +18.3 [+13.1, +23.5] |
| solo_2 | -11.1 [-22.2, -2.8] pts | 4 | 0 | +18.4 [+14.9, +22.2] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 0.0% | 33.3% | 0.0% | 0.0% | 34.4% | 13.9% |
| both | straight | 0.0% | 16.7% | 0.0% | 0.1% | 37.2% | 13.9% |
| both | right | 0.0% | 16.7% | 0.0% | 0.0% | 38.3% | 9.9% |
| none | left | 0.0% | 0.0% | 0.0% | 0.0% | 38.9% | 33.7% |
| none | straight | 0.0% | 0.0% | 0.0% | 0.1% | 40.1% | 14.4% |
| none | right | 0.0% | 0.0% | 0.0% | 0.0% | 39.3% | 23.1% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.4% | 31.8% |
| solo_2 | straight | 0.0% | 0.0% | 0.2% | 0.1% | 21.4% | 8.7% |
| solo_2 | right | 0.0% | 0.0% | 0.1% | 0.0% | 13.6% | 0.0% |
