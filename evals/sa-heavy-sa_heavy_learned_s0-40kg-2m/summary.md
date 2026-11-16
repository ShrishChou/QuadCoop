# Spot-arm turn pilot: sa-heavy-sa_heavy_learned_s0-40kg-2m

logs/marl2/sa_heavy_learned_s0/model_4000.pt, iteration 4000, mappo, arms learned. long 40 kg, 2 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 80.0% | 10.0% | 20.0 | 0.074 | 1.9 | +2.2 |
| both | straight | 40 | 85.0% | 0.0% | 14.9 | 0.074 | 1.7 | -0.1 |
| both | right | 40 | 55.0% | 0.0% | 13.7 | 0.093 | 2.2 | -0.5 |
| both | all | 120 | 73.3% | 3.3% | 15.9 | 0.079 | 1.9 | +0.5 |
| only_1 | left | 40 | 40.0% | 2.5% | 23.0 | 0.162 | 2.3 | +10.5 |
| only_1 | straight | 40 | 45.0% | 0.0% | 13.6 | 0.163 | 1.9 | -0.4 |
| only_1 | right | 40 | 57.5% | 0.0% | 26.2 | 0.091 | 2.5 | -2.5 |
| only_1 | all | 120 | 47.5% | 0.8% | 19.8 | 0.127 | 2.0 | +2.6 |
| only_2 | left | 40 | 72.5% | 2.5% | 24.6 | 0.086 | 1.9 | +1.3 |
| only_2 | straight | 40 | 87.5% | 0.0% | 17.0 | 0.083 | 1.8 | -0.4 |
| only_2 | right | 40 | 50.0% | 2.5% | 21.6 | 0.099 | 2.2 | -1.3 |
| only_2 | all | 120 | 70.0% | 1.7% | 20.9 | 0.087 | 1.9 | -0.1 |
| none | left | 40 | 50.0% | 0.0% | 29.8 | 0.098 | 1.5 | +6.6 |
| none | straight | 40 | 50.0% | 0.0% | 19.0 | 0.144 | 1.5 | -1.0 |
| none | right | 40 | 30.0% | 0.0% | 27.1 | 0.421 | 6.5 | +2.7 |
| none | all | 120 | 43.3% | 0.0% | 22.1 | 0.173 | 2.0 | +2.8 |
| solo_1 | left | 40 | 0.0% | 0.0% | - | 2.000 | 60.0 | +60.0 |
| solo_1 | straight | 40 | 0.0% | 0.0% | - | 2.000 | 0.0 | +0.0 |
| solo_1 | right | 40 | 0.0% | 0.0% | - | 2.000 | 60.0 | -60.0 |
| solo_1 | all | 120 | 0.0% | 0.0% | - | 2.000 | 60.0 | +0.0 |
| solo_2 | left | 40 | 0.0% | 0.0% | - | 2.000 | 60.0 | +64.1 |
| solo_2 | straight | 40 | 0.0% | 0.0% | - | 2.000 | 0.0 | +1.1 |
| solo_2 | right | 40 | 0.0% | 0.0% | - | 2.000 | 60.0 | -60.0 |
| solo_2 | all | 120 | 0.0% | 0.0% | - | 2.000 | 60.0 | +1.7 |

Ablation, paired per task against both (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| only_1 | -25.8 [-37.5, -14.2] pts | 44 | 13 | +3.8 [+1.7, +6.1] |
| only_2 | -3.3 [-13.3, +6.7] pts | 21 | 17 | +0.2 [-0.9, +1.2] |
| none | -30.0 [-41.7, -17.5] pts | 50 | 14 | +4.2 [+2.0, +6.6] |
| solo_1 | -73.3 [-80.8, -65.0] pts | 88 | 0 | +37.2 [+31.9, +42.2] |
| solo_2 | -73.3 [-80.8, -65.0] pts | 88 | 0 | +38.9 [+33.6, +44.0] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 65.0% | 95.0% | 0.0% | 0.1% | 45.0% | 23.2% |
| both | straight | 85.0% | 85.0% | 0.0% | 0.2% | 44.3% | 47.9% |
| both | right | 50.0% | 60.0% | 0.0% | 0.3% | 38.8% | 46.8% |
| only_1 | left | 40.0% | 40.0% | 0.0% | 0.1% | 47.8% | 45.9% |
| only_1 | straight | 35.0% | 55.0% | 0.0% | 0.0% | 42.2% | 54.7% |
| only_1 | right | 55.0% | 60.0% | 0.0% | 0.1% | 34.1% | 47.9% |
| only_2 | left | 55.0% | 90.0% | 0.0% | 0.1% | 45.1% | 21.5% |
| only_2 | straight | 80.0% | 95.0% | 0.0% | 0.2% | 43.6% | 49.3% |
| only_2 | right | 35.0% | 65.0% | 0.0% | 0.3% | 40.7% | 46.4% |
| none | left | 45.0% | 55.0% | 0.0% | 0.0% | 43.8% | 35.8% |
| none | straight | 50.0% | 50.0% | 0.0% | 0.0% | 41.9% | 54.3% |
| none | right | 45.0% | 15.0% | 0.0% | 0.0% | 40.5% | 51.4% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.3% | 0.0% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 6.5% | 0.0% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
