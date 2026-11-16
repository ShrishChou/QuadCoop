# Spot-arm turn pilot: sa-heavy-mo_sa_mappo_s0-dumbbell-40kg-2m

logs/marl2/mo_sa_mappo_s0/model_4000.pt, iteration 4000, mappo, arms learned. dumbbell 40 kg, 2 m, 6 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 12 | 0.0% | 33.3% | - | 0.981 | 57.5 | +36.3 |
| both | straight | 12 | 0.0% | 8.3% | - | 0.662 | 30.9 | -11.8 |
| both | right | 12 | 8.3% | 8.3% | 15.9 | 0.557 | 77.7 | +11.2 |
| both | all | 36 | 2.8% | 16.7% | 15.9 | 0.662 | 47.5 | +11.9 |
| only_1 | left | 12 | 0.0% | 0.0% | - | 0.860 | 52.0 | +25.2 |
| only_1 | straight | 12 | 0.0% | 0.0% | - | 0.557 | 22.3 | -7.7 |
| only_1 | right | 12 | 0.0% | 0.0% | - | 0.506 | 78.6 | -15.5 |
| only_1 | all | 36 | 0.0% | 0.0% | - | 0.557 | 41.4 | +0.7 |
| only_2 | left | 12 | 0.0% | 16.7% | - | 1.079 | 42.2 | +30.6 |
| only_2 | straight | 12 | 0.0% | 8.3% | - | 1.044 | 23.6 | -14.3 |
| only_2 | right | 12 | 0.0% | 0.0% | - | 0.952 | 63.1 | -28.5 |
| only_2 | all | 36 | 0.0% | 8.3% | - | 0.968 | 37.6 | -4.1 |
| none | left | 12 | 0.0% | 16.7% | - | 0.989 | 36.1 | +32.2 |
| none | straight | 12 | 0.0% | 8.3% | - | 0.981 | 24.6 | -17.0 |
| none | right | 12 | 0.0% | 0.0% | - | 0.704 | 59.4 | +2.0 |
| none | all | 36 | 0.0% | 8.3% | - | 0.949 | 31.3 | +5.7 |
| solo_1 | left | 12 | 0.0% | 83.3% | - | 2.000 | 60.0 | +60.0 |
| solo_1 | straight | 12 | 0.0% | 66.7% | - | 2.000 | 0.0 | -0.1 |
| solo_1 | right | 12 | 0.0% | 66.7% | - | 2.000 | 60.0 | -60.0 |
| solo_1 | all | 36 | 0.0% | 72.2% | - | 2.000 | 60.0 | -0.0 |
| solo_2 | left | 12 | 0.0% | 0.0% | - | 1.516 | 64.8 | -22.6 |
| solo_2 | straight | 12 | 0.0% | 0.0% | - | 1.545 | 39.3 | +14.5 |
| solo_2 | right | 12 | 0.0% | 0.0% | - | 1.618 | 36.9 | -32.7 |
| solo_2 | all | 36 | 0.0% | 0.0% | - | 1.545 | 48.2 | -13.6 |

Ablation, paired per task against both (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| only_1 | -2.8 [-8.3, +0.0] pts | 1 | 0 | -0.0 [-7.9, +8.5] |
| only_2 | -2.8 [-8.3, +0.0] pts | 1 | 0 | -5.1 [-14.2, +4.3] |
| none | -2.8 [-8.3, +0.0] pts | 1 | 0 | -9.1 [-20.8, +3.1] |
| solo_1 | -2.8 [-8.3, +0.0] pts | 1 | 0 | -3.4 [-13.6, +8.0] |
| solo_2 | -2.8 [-8.3, +0.0] pts | 1 | 0 | +6.7 [-6.6, +19.9] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 0.0% | 0.0% | 24.7% | 5.0% | 25.2% | 24.4% |
| both | straight | 0.0% | 0.0% | 16.6% | 2.9% | 29.2% | 25.3% |
| both | right | 16.7% | 0.0% | 7.2% | 7.4% | 33.3% | 24.5% |
| only_1 | left | 0.0% | 0.0% | 10.6% | 3.0% | 28.5% | 18.3% |
| only_1 | straight | 0.0% | 0.0% | 11.4% | 2.5% | 25.8% | 14.6% |
| only_1 | right | 0.0% | 0.0% | 8.9% | 3.7% | 45.8% | 29.1% |
| only_2 | left | 0.0% | 0.0% | 1.2% | 2.6% | 24.9% | 20.6% |
| only_2 | straight | 0.0% | 0.0% | 1.9% | 1.0% | 34.8% | 30.6% |
| only_2 | right | 0.0% | 0.0% | 1.7% | 3.3% | 41.3% | 28.7% |
| none | left | 0.0% | 0.0% | 0.0% | 9.2% | 21.8% | 26.7% |
| none | straight | 0.0% | 0.0% | 0.1% | 0.0% | 38.0% | 42.8% |
| none | right | 0.0% | 0.0% | 0.0% | 0.0% | 52.4% | 33.6% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.1% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.1% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 40.9% | 19.2% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 42.7% | 40.3% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 39.7% | 38.6% |
