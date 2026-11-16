# Spot-arm turn pilot: sa-heavy-mo_am_mappo_s0-long-60kg-2m

logs/marl2/mo_am_mappo_s0/model_4000.pt, iteration 4000, mappo, arms learned. long 60 kg, 2 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 0.0% | 7.5% | - | 1.057 | 14.2 | +7.7 |
| both | straight | 40 | 0.0% | 10.0% | - | 0.970 | 10.1 | -17.0 |
| both | right | 40 | 0.0% | 7.5% | - | 0.905 | 37.2 | -1.2 |
| both | all | 120 | 0.0% | 8.3% | - | 1.016 | 19.0 | -3.5 |
| none | left | 40 | 0.0% | 2.5% | - | 1.048 | 12.4 | -0.6 |
| none | straight | 40 | 0.0% | 5.0% | - | 0.948 | 12.2 | -22.0 |
| none | right | 40 | 0.0% | 5.0% | - | 0.925 | 27.3 | +12.3 |
| none | all | 120 | 0.0% | 4.2% | - | 0.994 | 15.7 | -3.4 |
| solo_1 | left | 40 | 0.0% | 5.0% | - | 1.856 | 51.7 | +16.8 |
| solo_1 | straight | 40 | 0.0% | 0.0% | - | 1.800 | 19.6 | +7.6 |
| solo_1 | right | 40 | 0.0% | 0.0% | - | 1.928 | 60.2 | -34.9 |
| solo_1 | all | 120 | 0.0% | 1.7% | - | 1.815 | 46.5 | -3.5 |
| solo_2 | left | 40 | 0.0% | 0.0% | - | 1.953 | 63.4 | +62.5 |
| solo_2 | straight | 40 | 0.0% | 7.5% | - | 1.941 | 6.4 | +2.9 |
| solo_2 | right | 40 | 0.0% | 0.0% | - | 1.953 | 59.5 | -58.4 |
| solo_2 | all | 120 | 0.0% | 2.5% | - | 1.949 | 55.7 | +2.3 |

Ablation, paired per task against both (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| none | +0.0 [+0.0, +0.0] pts | 0 | 0 | -2.0 [-6.3, +2.1] |
| solo_1 | +0.0 [+0.0, +0.0] pts | 0 | 0 | +17.4 [+11.7, +22.9] |
| solo_2 | +0.0 [+0.0, +0.0] pts | 0 | 0 | +17.8 [+12.4, +23.3] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 0.0% | 0.0% | 0.0% | 0.2% | 32.1% | 22.3% |
| both | straight | 0.0% | 0.0% | 0.0% | 0.1% | 37.9% | 7.1% |
| both | right | 0.0% | 0.0% | 0.0% | 1.0% | 32.9% | 14.3% |
| none | left | 0.0% | 0.0% | 0.0% | 0.5% | 38.4% | 12.8% |
| none | straight | 0.0% | 0.0% | 0.0% | 0.8% | 38.0% | 4.3% |
| none | right | 0.0% | 0.0% | 0.0% | 0.3% | 35.5% | 6.2% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 18.8% | 0.2% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 8.8% | 6.5% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 1.1% | 25.3% |
