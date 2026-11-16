# Spot-arm turn pilot: sa-heavy-mo_sa_mappo_s0-long-60kg-3m

logs/marl2/mo_sa_mappo_s0/model_4000.pt, iteration 4000, mappo, arms learned. long 60 kg, 3 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 0.0% | 12.5% | - | 2.700 | 57.4 | +54.4 |
| both | straight | 40 | 0.0% | 7.5% | - | 2.494 | 6.6 | -5.2 |
| both | right | 40 | 0.0% | 2.5% | - | 2.506 | 55.8 | -24.9 |
| both | all | 120 | 0.0% | 7.5% | - | 2.615 | 48.9 | +8.1 |
| only_1 | left | 40 | 0.0% | 2.5% | - | 2.728 | 58.8 | +58.9 |
| only_1 | straight | 40 | 0.0% | 2.5% | - | 2.517 | 8.6 | -7.1 |
| only_1 | right | 40 | 0.0% | 2.5% | - | 2.237 | 59.4 | -36.5 |
| only_1 | all | 120 | 0.0% | 2.5% | - | 2.571 | 54.2 | +5.1 |
| only_2 | left | 40 | 0.0% | 0.0% | - | 2.694 | 59.7 | +50.1 |
| only_2 | straight | 40 | 0.0% | 2.5% | - | 2.595 | 10.7 | -11.9 |
| only_2 | right | 40 | 0.0% | 2.5% | - | 2.573 | 58.5 | -33.2 |
| only_2 | all | 120 | 0.0% | 1.7% | - | 2.610 | 51.1 | +1.7 |
| none | left | 40 | 0.0% | 0.0% | - | 2.610 | 55.3 | +41.1 |
| none | straight | 40 | 0.0% | 0.0% | - | 2.592 | 9.6 | -10.1 |
| none | right | 40 | 0.0% | 0.0% | - | 2.699 | 63.5 | -45.0 |
| none | all | 120 | 0.0% | 0.0% | - | 2.612 | 52.3 | -4.6 |
| solo_1 | left | 40 | 0.0% | 62.5% | - | 3.000 | 60.0 | +60.0 |
| solo_1 | straight | 40 | 0.0% | 72.5% | - | 3.000 | 0.0 | +0.0 |
| solo_1 | right | 40 | 0.0% | 92.5% | - | 3.000 | 60.0 | -60.0 |
| solo_1 | all | 120 | 0.0% | 75.8% | - | 3.000 | 60.0 | -0.0 |
| solo_2 | left | 40 | 0.0% | 0.0% | - | 2.932 | 56.6 | +56.6 |
| solo_2 | straight | 40 | 0.0% | 0.0% | - | 2.938 | 4.2 | +0.2 |
| solo_2 | right | 40 | 0.0% | 0.0% | - | 2.958 | 60.6 | -60.1 |
| solo_2 | all | 120 | 0.0% | 0.0% | - | 2.943 | 55.7 | -1.1 |

Ablation, paired per task against both (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| only_1 | +0.0 [+0.0, +0.0] pts | 0 | 0 | +3.0 [+0.3, +5.7] |
| only_2 | +0.0 [+0.0, +0.0] pts | 0 | 0 | +1.5 [-1.7, +4.5] |
| none | +0.0 [+0.0, +0.0] pts | 0 | 0 | +0.0 [-3.7, +3.5] |
| solo_1 | +0.0 [+0.0, +0.0] pts | 0 | 0 | -0.1 [-3.0, +2.9] |
| solo_2 | +0.0 [+0.0, +0.0] pts | 0 | 0 | +0.3 [-2.4, +3.0] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 0.0% | 0.0% | 6.3% | 17.8% | 52.7% | 10.1% |
| both | straight | 0.0% | 0.0% | 6.6% | 6.8% | 52.3% | 16.8% |
| both | right | 0.0% | 0.0% | 7.0% | 3.0% | 49.7% | 27.4% |
| only_1 | left | 0.0% | 0.0% | 13.1% | 15.6% | 60.3% | 5.5% |
| only_1 | straight | 0.0% | 0.0% | 13.3% | 7.5% | 57.0% | 30.6% |
| only_1 | right | 0.0% | 0.0% | 9.1% | 2.0% | 66.9% | 47.7% |
| only_2 | left | 0.0% | 0.0% | 0.2% | 0.1% | 71.8% | 25.2% |
| only_2 | straight | 0.0% | 0.0% | 0.1% | 0.2% | 78.0% | 47.1% |
| only_2 | right | 0.0% | 0.0% | 0.0% | 0.5% | 78.8% | 51.5% |
| none | left | 0.0% | 0.0% | 0.0% | 0.1% | 78.2% | 25.1% |
| none | straight | 0.0% | 0.0% | 0.0% | 0.1% | 83.1% | 56.9% |
| none | right | 0.0% | 0.0% | 0.0% | 0.0% | 87.2% | 78.1% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 40.0% | 43.4% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 43.1% | 46.3% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 23.5% | 44.2% |
