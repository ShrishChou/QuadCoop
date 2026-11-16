# Spot-arm turn pilot: sa-heavy-sa_heavy_solo_s0-20kg-1m

logs/marl2/sa_heavy_solo_s0/model_4000.pt, iteration 4000, mappo, arms learned. long 20 kg, 1 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 0.0% | 42.5% | - | 0.434 | 75.9 | -17.7 |
| both | straight | 40 | 0.0% | 30.0% | - | 0.703 | 42.3 | +19.3 |
| both | right | 40 | 7.5% | 10.0% | 12.9 | 0.612 | 49.6 | -14.7 |
| both | all | 120 | 2.5% | 27.5% | 12.9 | 0.562 | 51.5 | -4.4 |
| only_1 | left | 40 | 2.5% | 5.0% | 35.5 | 0.956 | 41.9 | +23.7 |
| only_1 | straight | 40 | 0.0% | 0.0% | - | 0.527 | 17.6 | +5.6 |
| only_1 | right | 40 | 2.5% | 0.0% | 14.3 | 0.655 | 16.3 | -10.0 |
| only_1 | all | 120 | 1.7% | 1.7% | 35.5 | 0.723 | 19.2 | +6.4 |
| only_2 | left | 40 | 0.0% | 15.0% | - | 0.546 | 63.1 | -6.6 |
| only_2 | straight | 40 | 0.0% | 12.5% | - | 0.779 | 46.2 | +9.9 |
| only_2 | right | 40 | 0.0% | 45.0% | - | 0.669 | 53.8 | -19.6 |
| only_2 | all | 120 | 0.0% | 24.2% | - | 0.681 | 57.6 | -5.4 |
| none | left | 40 | 0.0% | 0.0% | - | 1.414 | 50.1 | +27.5 |
| none | straight | 40 | 0.0% | 0.0% | - | 1.278 | 52.6 | -6.9 |
| none | right | 40 | 0.0% | 0.0% | - | 1.450 | 69.2 | +4.0 |
| none | all | 120 | 0.0% | 0.0% | - | 1.389 | 58.7 | +8.2 |
| solo_1 | left | 40 | 100.0% | 0.0% | 9.7 | 0.070 | 2.9 | +1.7 |
| solo_1 | straight | 40 | 100.0% | 0.0% | 8.5 | 0.073 | 1.6 | +0.4 |
| solo_1 | right | 40 | 100.0% | 0.0% | 14.2 | 0.077 | 2.0 | +1.7 |
| solo_1 | all | 120 | 100.0% | 0.0% | 11.9 | 0.073 | 2.2 | +1.3 |
| solo_2 | left | 40 | 0.0% | 0.0% | - | 0.884 | 44.9 | +47.3 |
| solo_2 | straight | 40 | 0.0% | 7.5% | - | 0.885 | 20.0 | -16.8 |
| solo_2 | right | 40 | 0.0% | 10.0% | - | 0.902 | 78.0 | -69.2 |
| solo_2 | all | 120 | 0.0% | 5.8% | - | 0.885 | 44.9 | -12.9 |

Ablation, paired per task against both (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| only_1 | -0.8 [-4.2, +2.5] pts | 3 | 2 | -26.3 [-31.5, -20.9] |
| only_2 | -2.5 [-5.8, +0.0] pts | 3 | 0 | +3.5 [-2.8, +9.4] |
| none | -2.5 [-5.8, +0.0] pts | 3 | 0 | +7.6 [+1.3, +13.9] |
| solo_1 | +97.5 [+94.2, +100.0] pts | 0 | 117 | -48.3 [-53.0, -43.8] |
| solo_2 | -2.5 [-5.8, +0.0] pts | 3 | 0 | -4.4 [-10.7, +2.2] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 0.0% | 0.0% | 5.8% | 8.7% | 1.6% | 1.8% |
| both | straight | 0.0% | 0.0% | 11.2% | 7.3% | 4.6% | 5.7% |
| both | right | 5.0% | 10.0% | 1.6% | 7.1% | 1.1% | 6.9% |
| only_1 | left | 0.0% | 5.0% | 0.1% | 0.0% | 2.0% | 1.6% |
| only_1 | straight | 0.0% | 0.0% | 1.7% | 0.0% | 3.7% | 2.9% |
| only_1 | right | 0.0% | 5.0% | 0.0% | 0.0% | 4.1% | 3.7% |
| only_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 1.1% | 1.3% |
| only_2 | straight | 0.0% | 0.0% | 0.0% | 0.3% | 2.2% | 8.0% |
| only_2 | right | 0.0% | 0.0% | 0.0% | 0.1% | 3.6% | 2.6% |
| none | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.8% | 1.2% |
| none | straight | 0.0% | 0.0% | 0.0% | 0.0% | 1.6% | 1.6% |
| none | right | 0.0% | 0.0% | 0.0% | 0.0% | 1.9% | 1.6% |
| solo_1 | left | 100.0% | 100.0% | 5.2% | 2.0% | 4.5% | 5.9% |
| solo_1 | straight | 100.0% | 100.0% | 2.2% | 0.8% | 20.4% | 13.5% |
| solo_1 | right | 100.0% | 100.0% | 0.8% | 0.3% | 12.4% | 10.4% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.3% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.5% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.4% |
