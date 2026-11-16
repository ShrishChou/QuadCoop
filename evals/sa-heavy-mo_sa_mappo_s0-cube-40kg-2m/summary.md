# Spot-arm turn pilot: sa-heavy-mo_sa_mappo_s0-cube-40kg-2m

logs/marl2/mo_sa_mappo_s0/model_4000.pt, iteration 4000, mappo, arms learned. cube 40 kg, 2 m, 6 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left -30.0 to -30.0 deg, straight +0.0 to +0.0 deg, right +30.0 to +30.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 12 | 0.0% | 0.0% | - | 0.531 | 3.5 | -1.0 |
| both | straight | 12 | 0.0% | 8.3% | - | 1.033 | 3.5 | +4.1 |
| both | right | 12 | 0.0% | 25.0% | - | 1.165 | 9.4 | +11.3 |
| both | all | 36 | 0.0% | 11.1% | - | 0.941 | 4.3 | +4.8 |
| only_1 | left | 12 | 0.0% | 0.0% | - | 0.642 | 4.4 | -4.0 |
| only_1 | straight | 12 | 0.0% | 0.0% | - | 0.844 | 5.1 | +4.6 |
| only_1 | right | 12 | 0.0% | 8.3% | - | 1.274 | 8.0 | +10.2 |
| only_1 | all | 36 | 0.0% | 2.8% | - | 0.863 | 5.1 | +3.6 |
| only_2 | left | 12 | 0.0% | 0.0% | - | 0.612 | 5.9 | +3.7 |
| only_2 | straight | 12 | 0.0% | 0.0% | - | 1.066 | 7.1 | +3.6 |
| only_2 | right | 12 | 0.0% | 0.0% | - | 1.469 | 8.6 | +13.2 |
| only_2 | all | 36 | 0.0% | 0.0% | - | 1.066 | 7.6 | +6.8 |
| none | left | 12 | 25.0% | 0.0% | 15.3 | 0.681 | 5.4 | -0.9 |
| none | straight | 12 | 0.0% | 0.0% | - | 1.105 | 9.9 | +7.2 |
| none | right | 12 | 25.0% | 8.3% | 26.2 | 1.337 | 10.6 | +11.6 |
| none | all | 36 | 16.7% | 2.8% | 18.5 | 1.164 | 8.1 | +6.0 |
| solo_1 | left | 12 | 0.0% | 50.0% | - | 1.998 | 31.0 | -32.1 |
| solo_1 | straight | 12 | 0.0% | 50.0% | - | 2.000 | 0.0 | +0.0 |
| solo_1 | right | 12 | 0.0% | 50.0% | - | 2.000 | 30.0 | +30.0 |
| solo_1 | all | 36 | 0.0% | 50.0% | - | 2.000 | 30.0 | -0.7 |
| solo_2 | left | 12 | 0.0% | 0.0% | - | 1.797 | 16.3 | -14.5 |
| solo_2 | straight | 12 | 0.0% | 0.0% | - | 1.833 | 2.5 | +2.8 |
| solo_2 | right | 12 | 0.0% | 0.0% | - | 1.805 | 12.4 | +14.5 |
| solo_2 | all | 36 | 0.0% | 0.0% | - | 1.802 | 7.9 | +0.9 |

Ablation, paired per task against both (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| only_1 | +0.0 [+0.0, +0.0] pts | 0 | 0 | +1.0 [-1.6, +3.8] |
| only_2 | +0.0 [+0.0, +0.0] pts | 0 | 0 | +1.7 [-1.5, +5.3] |
| none | +16.7 [+5.6, +30.6] pts | 0 | 6 | +2.5 [-0.6, +5.7] |
| solo_1 | +0.0 [+0.0, +0.0] pts | 0 | 0 | +13.6 [+8.8, +18.5] |
| solo_2 | +0.0 [+0.0, +0.0] pts | 0 | 0 | +3.6 [+0.1, +7.3] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 0.0% | 0.0% | 8.0% | 1.9% | 43.4% | 33.7% |
| both | straight | 0.0% | 0.0% | 16.0% | 5.6% | 58.2% | 7.8% |
| both | right | 0.0% | 0.0% | 9.5% | 4.8% | 53.9% | 9.3% |
| only_1 | left | 0.0% | 0.0% | 2.6% | 1.7% | 41.2% | 43.0% |
| only_1 | straight | 0.0% | 0.0% | 7.2% | 0.3% | 53.0% | 14.2% |
| only_1 | right | 0.0% | 0.0% | 6.9% | 4.3% | 61.0% | 11.0% |
| only_2 | left | 0.0% | 0.0% | 1.0% | 2.7% | 49.4% | 30.5% |
| only_2 | straight | 0.0% | 0.0% | 0.0% | 2.8% | 72.3% | 26.4% |
| only_2 | right | 0.0% | 0.0% | 0.1% | 4.5% | 74.8% | 2.5% |
| none | left | 33.3% | 16.7% | 0.0% | 0.0% | 44.5% | 48.1% |
| none | straight | 0.0% | 0.0% | 0.0% | 0.0% | 78.3% | 16.0% |
| none | right | 33.3% | 16.7% | 0.0% | 0.8% | 76.3% | 7.7% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.1% | 0.0% | 0.9% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.2% | 0.0% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.1% | 0.0% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 43.6% | 40.6% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 43.1% | 45.7% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 43.1% | 38.5% |
