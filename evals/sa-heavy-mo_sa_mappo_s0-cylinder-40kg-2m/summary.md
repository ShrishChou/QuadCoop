# Spot-arm turn pilot: sa-heavy-mo_sa_mappo_s0-cylinder-40kg-2m

logs/marl2/mo_sa_mappo_s0/model_4000.pt, iteration 4000, mappo, arms learned. cylinder 40 kg, 2 m, 6 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 12 | 0.0% | 8.3% | - | 0.352 | 60.9 | +54.7 |
| both | straight | 12 | 50.0% | 0.0% | 26.1 | 0.110 | 4.8 | +0.9 |
| both | right | 12 | 0.0% | 0.0% | - | 0.299 | 35.2 | -36.3 |
| both | all | 36 | 16.7% | 2.8% | 26.1 | 0.252 | 33.7 | +6.4 |
| only_1 | left | 12 | 0.0% | 0.0% | - | 0.304 | 60.4 | +59.2 |
| only_1 | straight | 12 | 25.0% | 8.3% | 13.4 | 0.275 | 7.0 | -0.0 |
| only_1 | right | 12 | 0.0% | 0.0% | - | 0.235 | 50.5 | -44.6 |
| only_1 | all | 36 | 8.3% | 2.8% | 13.4 | 0.275 | 50.2 | +4.8 |
| only_2 | left | 12 | 0.0% | 0.0% | - | 0.350 | 61.1 | +57.5 |
| only_2 | straight | 12 | 25.0% | 0.0% | 21.3 | 0.125 | 3.0 | +4.6 |
| only_2 | right | 12 | 0.0% | 0.0% | - | 0.254 | 43.7 | -41.4 |
| only_2 | all | 36 | 8.3% | 0.0% | 21.3 | 0.218 | 40.9 | +6.9 |
| none | left | 12 | 0.0% | 8.3% | - | 0.289 | 57.4 | +57.8 |
| none | straight | 12 | 16.7% | 0.0% | 11.5 | 0.154 | 3.2 | +3.1 |
| none | right | 12 | 0.0% | 0.0% | - | 0.204 | 45.5 | -42.7 |
| none | all | 36 | 5.6% | 2.8% | 11.5 | 0.204 | 45.5 | +6.1 |
| solo_1 | left | 12 | 0.0% | 75.0% | - | 2.000 | 60.0 | +60.0 |
| solo_1 | straight | 12 | 0.0% | 91.7% | - | 2.000 | 0.0 | -0.0 |
| solo_1 | right | 12 | 0.0% | 83.3% | - | 2.000 | 60.0 | -60.0 |
| solo_1 | all | 36 | 0.0% | 83.3% | - | 2.000 | 60.0 | -0.0 |
| solo_2 | left | 12 | 0.0% | 0.0% | - | 0.812 | 46.5 | +45.5 |
| solo_2 | straight | 12 | 0.0% | 0.0% | - | 0.591 | 6.2 | -4.3 |
| solo_2 | right | 12 | 0.0% | 0.0% | - | 0.643 | 54.5 | -54.0 |
| solo_2 | all | 36 | 0.0% | 0.0% | - | 0.670 | 46.4 | -4.3 |

Ablation, paired per task against both (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| only_1 | -8.3 [-22.2, +5.6] pts | 5 | 2 | +4.8 [+2.0, +7.9] |
| only_2 | -8.3 [-22.2, +5.6] pts | 5 | 2 | +3.1 [-0.2, +6.6] |
| none | -11.1 [-22.2, -2.8] pts | 4 | 0 | +3.1 [+0.4, +6.1] |
| solo_1 | -16.7 [-30.6, -5.6] pts | 6 | 0 | +8.1 [+3.6, +13.0] |
| solo_2 | -16.7 [-30.6, -5.6] pts | 6 | 0 | +3.1 [-1.8, +7.9] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 0.0% | 0.0% | 3.1% | 1.4% | 8.0% | 8.9% |
| both | straight | 33.3% | 66.7% | 1.6% | 1.7% | 24.6% | 13.9% |
| both | right | 0.0% | 0.0% | 3.3% | 1.0% | 34.5% | 12.7% |
| only_1 | left | 0.0% | 0.0% | 2.1% | 0.7% | 6.4% | 1.6% |
| only_1 | straight | 50.0% | 0.0% | 2.0% | 0.5% | 18.6% | 9.2% |
| only_1 | right | 0.0% | 0.0% | 0.8% | 0.3% | 30.4% | 17.1% |
| only_2 | left | 0.0% | 0.0% | 0.1% | 0.5% | 20.8% | 2.4% |
| only_2 | straight | 50.0% | 0.0% | 0.0% | 0.2% | 37.9% | 12.3% |
| only_2 | right | 0.0% | 0.0% | 0.0% | 1.0% | 48.9% | 23.2% |
| none | left | 0.0% | 0.0% | 0.0% | 0.2% | 27.4% | 3.0% |
| none | straight | 0.0% | 33.3% | 0.0% | 0.0% | 25.7% | 12.2% |
| none | right | 0.0% | 0.0% | 0.0% | 0.0% | 38.1% | 17.5% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 35.2% | 38.7% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 32.4% | 37.1% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 37.8% | 37.5% |
