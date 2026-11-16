# Spot-arm turn pilot: sa-heavy-mo_am_mappo_s0-long-40kg-2m

logs/marl2/mo_am_mappo_s0/model_4000.pt, iteration 4000, mappo, arms learned. long 40 kg, 2 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 0.0% | 0.0% | - | 0.900 | 9.1 | +5.2 |
| both | straight | 40 | 0.0% | 0.0% | - | 0.642 | 4.1 | -2.1 |
| both | right | 40 | 5.0% | 0.0% | 9.7 | 0.537 | 7.6 | +3.3 |
| both | all | 120 | 1.7% | 0.0% | 9.7 | 0.720 | 6.1 | +2.1 |
| none | left | 40 | 0.0% | 0.0% | - | 0.889 | 9.3 | +0.5 |
| none | straight | 40 | 2.5% | 0.0% | 8.2 | 0.658 | 7.1 | -6.3 |
| none | right | 40 | 5.0% | 2.5% | 23.2 | 0.528 | 13.1 | +1.2 |
| none | all | 120 | 2.5% | 0.8% | 17.2 | 0.698 | 9.3 | -1.5 |
| solo_1 | left | 40 | 0.0% | 0.0% | - | 1.860 | 41.1 | +24.7 |
| solo_1 | straight | 40 | 0.0% | 2.5% | - | 1.851 | 28.7 | -24.1 |
| solo_1 | right | 40 | 0.0% | 0.0% | - | 1.862 | 77.4 | -31.7 |
| solo_1 | all | 120 | 0.0% | 0.8% | - | 1.857 | 46.0 | -10.4 |
| solo_2 | left | 40 | 0.0% | 0.0% | - | 1.875 | 64.2 | -3.0 |
| solo_2 | straight | 40 | 0.0% | 5.0% | - | 1.720 | 35.6 | +21.9 |
| solo_2 | right | 40 | 0.0% | 0.0% | - | 1.881 | 51.4 | -55.7 |
| solo_2 | all | 120 | 0.0% | 1.7% | - | 1.847 | 58.3 | -12.2 |

Ablation, paired per task against both (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| none | +0.8 [-2.5, +4.2] pts | 2 | 3 | +0.8 [-1.9, +3.4] |
| solo_1 | -1.7 [-4.2, +0.0] pts | 2 | 0 | +36.4 [+31.4, +41.3] |
| solo_2 | -1.7 [-4.2, +0.0] pts | 2 | 0 | +41.7 [+37.5, +46.0] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 0.0% | 0.0% | 0.0% | 0.0% | 16.9% | 16.9% |
| both | straight | 0.0% | 0.0% | 0.0% | 0.0% | 25.1% | 27.4% |
| both | right | 5.0% | 5.0% | 0.0% | 1.5% | 25.8% | 14.2% |
| none | left | 0.0% | 0.0% | 0.0% | 0.0% | 22.7% | 18.2% |
| none | straight | 0.0% | 5.0% | 0.0% | 0.0% | 29.7% | 17.7% |
| none | right | 10.0% | 0.0% | 0.0% | 0.0% | 27.0% | 16.4% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 4.2% | 0.3% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 1.6% | 3.5% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.7% | 17.3% |
