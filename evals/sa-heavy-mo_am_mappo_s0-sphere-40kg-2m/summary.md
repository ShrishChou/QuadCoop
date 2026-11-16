# Spot-arm turn pilot: sa-heavy-mo_am_mappo_s0-sphere-40kg-2m

logs/marl2/mo_am_mappo_s0/model_4000.pt, iteration 4000, mappo, arms learned. sphere 40 kg, 2 m, 6 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +0.0 to +0.0 deg, straight +0.0 to +0.0 deg, right +0.0 to +0.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 12 | 91.7% | 0.0% | 6.9 | 0.071 | 0.0 | +0.0 |
| both | straight | 12 | 83.3% | 0.0% | 6.9 | 0.086 | 0.0 | +0.0 |
| both | right | 12 | 100.0% | 0.0% | 7.5 | 0.072 | 0.0 | +0.0 |
| both | all | 36 | 91.7% | 0.0% | 6.9 | 0.071 | 0.0 | +0.0 |
| none | left | 12 | 100.0% | 0.0% | 7.2 | 0.081 | 0.0 | +0.0 |
| none | straight | 12 | 100.0% | 0.0% | 6.9 | 0.079 | 0.0 | +0.0 |
| none | right | 12 | 83.3% | 0.0% | 6.7 | 0.087 | 0.0 | +0.0 |
| none | all | 36 | 94.4% | 0.0% | 6.9 | 0.081 | 0.0 | +0.0 |
| solo_1 | left | 12 | 0.0% | 0.0% | - | 1.953 | 0.0 | +0.0 |
| solo_1 | straight | 12 | 0.0% | 0.0% | - | 1.761 | 0.0 | +0.0 |
| solo_1 | right | 12 | 0.0% | 0.0% | - | 1.500 | 0.0 | +0.0 |
| solo_1 | all | 36 | 0.0% | 0.0% | - | 1.636 | 0.0 | +0.0 |
| solo_2 | left | 12 | 0.0% | 0.0% | - | 1.764 | 0.0 | +0.0 |
| solo_2 | straight | 12 | 0.0% | 0.0% | - | 1.717 | 0.0 | +0.0 |
| solo_2 | right | 12 | 0.0% | 0.0% | - | 1.702 | 0.0 | +0.0 |
| solo_2 | all | 36 | 0.0% | 0.0% | - | 1.702 | 0.0 | +0.0 |

Ablation, paired per task against both (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| none | +2.8 [-8.3, +13.9] pts | 2 | 3 | +0.0 [+0.0, +0.0] |
| solo_1 | -91.7 [-100.0, -80.6] pts | 33 | 0 | +0.0 [+0.0, +0.0] |
| solo_2 | -91.7 [-100.0, -80.6] pts | 33 | 0 | +0.0 [+0.0, +0.0] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 83.3% | 100.0% | 0.0% | 0.0% | 5.5% | 3.9% |
| both | straight | 66.7% | 100.0% | 0.0% | 0.0% | 5.2% | 2.6% |
| both | right | 100.0% | 100.0% | 0.0% | 0.0% | 5.9% | 3.5% |
| none | left | 100.0% | 100.0% | 0.0% | 0.0% | 4.4% | 2.5% |
| none | straight | 100.0% | 100.0% | 0.0% | 0.0% | 5.1% | 3.4% |
| none | right | 83.3% | 83.3% | 0.0% | 0.0% | 3.4% | 3.0% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.1% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.1% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.1% | 0.1% |
