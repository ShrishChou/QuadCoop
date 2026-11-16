# Spot-arm turn pilot: sa-heavy-mo_sa_mappo_s0-long-20kg-1m

logs/marl2/mo_sa_mappo_s0/model_4000.pt, iteration 4000, mappo, arms learned. long 20 kg, 1 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 7.5% | 20.0% | 32.9 | 0.273 | 14.8 | +12.9 |
| both | straight | 40 | 10.0% | 7.5% | 4.7 | 0.288 | 9.3 | +8.4 |
| both | right | 40 | 15.0% | 20.0% | 21.2 | 0.269 | 11.8 | -1.2 |
| both | all | 120 | 10.8% | 15.8% | 21.2 | 0.269 | 11.0 | +6.7 |
| only_1 | left | 40 | 17.5% | 7.5% | 28.7 | 0.220 | 5.6 | +6.0 |
| only_1 | straight | 40 | 55.0% | 2.5% | 4.7 | 0.082 | 3.7 | -0.4 |
| only_1 | right | 40 | 27.5% | 15.0% | 18.9 | 0.257 | 7.7 | -3.6 |
| only_1 | all | 120 | 33.3% | 8.3% | 19.3 | 0.174 | 4.9 | +0.7 |
| only_2 | left | 40 | 25.0% | 0.0% | 21.8 | 0.141 | 13.3 | +11.6 |
| only_2 | straight | 40 | 30.0% | 0.0% | 6.4 | 0.135 | 11.0 | +16.5 |
| only_2 | right | 40 | 45.0% | 0.0% | 27.2 | 0.076 | 5.1 | -6.6 |
| only_2 | all | 120 | 33.3% | 0.0% | 21.4 | 0.106 | 9.0 | +7.2 |
| none | left | 40 | 10.0% | 0.0% | 26.8 | 0.140 | 15.7 | +26.5 |
| none | straight | 40 | 70.0% | 0.0% | 7.8 | 0.074 | 3.5 | +3.5 |
| none | right | 40 | 20.0% | 0.0% | 23.5 | 0.143 | 5.3 | -0.6 |
| none | all | 120 | 33.3% | 0.0% | 17.3 | 0.100 | 6.2 | +9.8 |
| solo_1 | left | 40 | 0.0% | 82.5% | - | 1.000 | 60.0 | +59.8 |
| solo_1 | straight | 40 | 0.0% | 72.5% | - | 1.000 | 0.0 | -0.1 |
| solo_1 | right | 40 | 0.0% | 82.5% | - | 1.000 | 60.0 | -60.3 |
| solo_1 | all | 120 | 0.0% | 79.2% | - | 1.000 | 60.0 | -0.2 |
| solo_2 | left | 40 | 0.0% | 0.0% | - | 2.817 | 21.2 | -4.8 |
| solo_2 | straight | 40 | 0.0% | 0.0% | - | 1.171 | 2.3 | -0.7 |
| solo_2 | right | 40 | 0.0% | 0.0% | - | 1.390 | 16.8 | +9.0 |
| solo_2 | all | 120 | 0.0% | 0.0% | - | 1.560 | 14.1 | +1.1 |

Ablation, paired per task against both (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| only_1 | +22.5 [+12.5, +32.5] pts | 8 | 35 | -7.9 [-12.4, -3.5] |
| only_2 | +22.5 [+11.7, +33.3] pts | 11 | 38 | -2.9 [-6.9, +1.1] |
| none | +22.5 [+12.5, +32.5] pts | 9 | 36 | -4.5 [-9.0, -0.0] |
| solo_1 | -10.8 [-16.7, -5.8] pts | 13 | 0 | +21.8 [+16.0, +27.2] |
| solo_2 | -10.8 [-16.7, -5.8] pts | 13 | 0 | +1.4 [-3.7, +6.3] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 5.0% | 10.0% | 6.8% | 2.6% | 20.0% | 11.6% |
| both | straight | 15.0% | 5.0% | 7.5% | 2.7% | 10.1% | 9.5% |
| both | right | 15.0% | 15.0% | 4.6% | 3.8% | 20.2% | 10.9% |
| only_1 | left | 0.0% | 35.0% | 5.3% | 4.0% | 9.2% | 12.6% |
| only_1 | straight | 65.0% | 45.0% | 7.4% | 4.2% | 22.5% | 5.9% |
| only_1 | right | 30.0% | 25.0% | 2.5% | 6.0% | 14.5% | 9.1% |
| only_2 | left | 50.0% | 0.0% | 2.8% | 0.1% | 21.3% | 16.9% |
| only_2 | straight | 60.0% | 0.0% | 11.2% | 0.2% | 13.6% | 7.1% |
| only_2 | right | 65.0% | 25.0% | 1.7% | 0.1% | 31.4% | 30.1% |
| none | left | 10.0% | 10.0% | 0.0% | 0.0% | 17.1% | 10.1% |
| none | straight | 65.0% | 75.0% | 0.0% | 0.0% | 24.8% | 16.7% |
| none | right | 20.0% | 20.0% | 0.0% | 0.0% | 12.8% | 20.1% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.1% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.1% | 0.0% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.1% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 5.3% | 1.8% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 36.7% | 39.0% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 20.2% | 20.7% |
