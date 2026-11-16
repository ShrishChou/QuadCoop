# Spot-arm turn pilot: sa-heavy-mo_am_mappo_s0-long-20kg-1m

logs/marl2/mo_am_mappo_s0/model_4000.pt, iteration 4000, mappo, arms learned. long 20 kg, 1 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 0.0% | 0.0% | - | 0.469 | 7.5 | +5.4 |
| both | straight | 40 | 2.5% | 0.0% | 4.0 | 0.580 | 6.5 | +5.2 |
| both | right | 40 | 0.0% | 0.0% | - | 0.481 | 15.7 | -11.2 |
| both | all | 120 | 0.8% | 0.0% | 4.0 | 0.481 | 8.4 | -0.2 |
| none | left | 40 | 0.0% | 0.0% | - | 0.436 | 13.2 | +9.7 |
| none | straight | 40 | 0.0% | 0.0% | - | 0.523 | 10.2 | +1.1 |
| none | right | 40 | 0.0% | 0.0% | - | 0.353 | 11.2 | -10.6 |
| none | all | 120 | 0.0% | 0.0% | - | 0.392 | 11.4 | +0.1 |
| solo_1 | left | 40 | 0.0% | 0.0% | - | 0.840 | 47.9 | +39.2 |
| solo_1 | straight | 40 | 0.0% | 0.0% | - | 1.065 | 10.9 | -9.1 |
| solo_1 | right | 40 | 0.0% | 0.0% | - | 1.415 | 70.0 | -15.9 |
| solo_1 | all | 120 | 0.0% | 0.0% | - | 1.144 | 47.9 | +4.7 |
| solo_2 | left | 40 | 0.0% | 0.0% | - | 0.578 | 64.0 | -14.6 |
| solo_2 | straight | 40 | 0.0% | 0.0% | - | 0.679 | 62.4 | +9.1 |
| solo_2 | right | 40 | 0.0% | 0.0% | - | 0.711 | 39.9 | -34.9 |
| solo_2 | all | 120 | 0.0% | 0.0% | - | 0.686 | 56.8 | -13.5 |

Ablation, paired per task against both (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| none | -0.8 [-2.5, +0.0] pts | 1 | 0 | +1.4 [-0.3, +3.1] |
| solo_1 | -0.8 [-2.5, +0.0] pts | 1 | 0 | +32.6 [+27.5, +37.5] |
| solo_2 | -0.8 [-2.5, +0.0] pts | 1 | 0 | +42.6 [+39.2, +46.1] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 0.0% | 0.0% | 0.0% | 1.3% | 0.4% | 10.1% |
| both | straight | 5.0% | 0.0% | 0.0% | 0.0% | 2.5% | 19.9% |
| both | right | 0.0% | 0.0% | 0.0% | 0.0% | 7.6% | 0.6% |
| none | left | 0.0% | 0.0% | 0.0% | 0.0% | 1.6% | 35.1% |
| none | straight | 0.0% | 0.0% | 0.0% | 0.0% | 4.6% | 32.7% |
| none | right | 0.0% | 0.0% | 0.0% | 0.0% | 11.0% | 0.7% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.3% | 0.1% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.2% | 1.7% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.2% | 1.0% |
